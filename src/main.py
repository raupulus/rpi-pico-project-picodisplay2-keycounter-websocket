#from machine import Pin, SPI
import _thread, gc
from time import sleep_ms, sleep, time
from Models.Api import Api
from Models.RpiPico import RpiPico
from Models.PicoDisplay2 import PicoDisplay2
from Models.WebSocketServer import WebSocketServer
from Models.Computer import Computer
import utime

# Importo variables de entorno
import env

# Habilito recolector de basura
gc.enable()

# Rpi Pico Model
controller = RpiPico(ssid=env.AP_NAME, password=env.AP_PASS, debug=env.DEBUG,
                     alternatives_ap=env.ALTERNATIVES_AP,
                     hostname="Raupulus KeyCounter")

# Display Model
display = PicoDisplay2(controller=controller, debug=env.DEBUG)

sleep_ms(20)

# Api
api = Api(controller=controller, url=env.API_URL, path=env.API_PATH,
          token=env.API_TOKEN, device_id=env.DEVICE_ID, debug=env.DEBUG)

sleep_ms(20)

# Variables para el manejo de bloqueo con el segundo core
thread_lock = _thread.allocate_lock()
thread_lock_acquired = False

sleep_ms(3000)

# Timer para apagar la pantalla
last_conn_time = utime.ticks_ms()

# Listado de dispositivos recientes
devices = []


def find_device_by_id (device_id):
    """
    Busca un dispositivo dentro de la lista de dispositivos para actualizarlo.

    :param device_id: int Identificador del dispositivo de hardware a buscar.
    :return: A tuple containing the position of the device in the device list and the device object itself. If the device is not found, the tuple contains (0, None)
    """
    current_time = utime.time()
    ten_minutes_ago = current_time - 300

    current_device = None
    device_position = None

    for index, device in enumerate(devices.copy()):
        device_last_seen_unix = utime.mktime(device.last_seen)

        if device.device_id == device_id:
            current_device = device
            device_position = index
        elif device_last_seen_unix < ten_minutes_ago:
            devices.remove(device)

    return device_position or 0, current_device or None


def updateDisplay(pos, device) -> None:
    """
    Busca el dispositivo en la lista de dispositivos para actualizarlo y
    posteriormente lo envía a la pantalla para que se dibuje en ella.

    Mientras la pantalla no está trabajando, se monitoriza si debe apagarse
    por inactividad o si se ha pulsado algún botón para interactuar con la
    pantalla para acceder a otra sección

    :param pos: Position to update display
    :param device: Device to display information for
    :return: None
    """
    thread_lock.acquire()
    global thread_lock_acquired, last_conn_time

    try:
        display.update(pos, device, True if len(devices) is 1 else False)
        last_conn_time = utime.ticks_ms()
    except Exception as e:
        if env.DEBUG:
            print('Error en la función updateDisplay:', e)
    finally:
        thread_lock.release()
        thread_lock_acquired = False

    while not thread_lock_acquired:
        # Compruebo si se ha pulsado un botón
        button_press = display.check_buttons()

        # Si se ha pulsado un botón, lanza el menú correspondiente
        if button_press:
            thread_lock.acquire()
            thread_lock_acquired = True
            try:
                last_conn_time = utime.ticks_ms()

                if env.DEBUG:
                    print('Se ha pulsado el botón:', button_press)

                display.change_mode(button_press)

            except Exception as e:
                if env.DEBUG:
                    print('Error en la función updateDisplay:', e)
            finally:
                thread_lock.release()
                thread_lock_acquired = False

        # Compruebo si tiene que apagar la pantalla
        if display.on:
            diff = utime.ticks_diff(utime.ticks_ms(), last_conn_time)

            if diff > env.TIME_TO_DISPLAY_OFF * 60 * 1000:
                thread_lock.acquire()
                thread_lock_acquired = True

                try:
                    if env.DEBUG:
                        print('Apagando pantalla')

                    display.shutdown()
                except Exception as e:
                    if env.DEBUG:
                        print('Error en la función updateDisplay:', e)
                finally:
                    thread_lock.release()
                    thread_lock_acquired = False


def thread1 (data):
    """
    Segundo hilo para acciones secundarias sobre la pantalla.
    """
    global thread_lock_acquired

    if not thread_lock_acquired:
        thread_lock_acquired = True

        if env.DEBUG:
            print('')
            print('Datos a procesar:', data)

        device_id = data['device_id']
        pos, device = find_device_by_id(device_id)

        if device is None:
            device = Computer(data)
            devices.append(device)
        else:
            device.update(data)

        if env.DEBUG:
            print('devices:', devices)
            print('device:', device)

        # Inicio un nuevo hilo que llama a updateDisplay(data)
        _thread.start_new_thread(updateDisplay, (pos, device))

def thread0 ():
    """
    Primer hilo para websockets y envío de datos a las acciones del segundo
    hilo.
    """

    if env.DEBUG:
        print('Inicia hilo principal (thread0)')

    devices_info = api.get_computers_list()

    if env.DEBUG:
        print(devices_info)

    # Iniciamos el servidor WebSocket
    websocket_server = WebSocketServer(thread1, debug=env.DEBUG)
    websocket_server.start()


while True:
    try:
        thread0()
    except Exception as e:
        if env.DEBUG:
            print('Error: ', e)
    finally:
        if env.DEBUG:
            print('Memoria antes de liberar: ', gc.mem_free())

        gc.collect()

        if env.DEBUG:
            print("Memoria después de liberar:", gc.mem_free())

        sleep(5)
