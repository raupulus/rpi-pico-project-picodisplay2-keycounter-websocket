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
                     hostname="Raupulus KeyCounter")
#controller = RpiPico(debug=env.DEBUG)

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

sleep_ms(20)



#gc.collect()


sleep_ms(3000)


devices = []


def find_device_by_id (device_id):
    current_time = utime.time()  # time in seconds since the Epoch
    ten_minutes_ago = current_time - 300  # 300 seconds is 5 minutes

    current_device = None
    device_position = None

    # Iterate over a copy of the device list
    for index, device in enumerate(devices.copy()):
        device_last_seen_unix = utime.mktime(device.last_seen)

        if device.device_id == device_id:
            current_device = device
            device_position = index  # store the current position
        elif device_last_seen_unix < ten_minutes_ago:
            devices.remove(device)

    return device_position, current_device


def updateDisplay(data):
    global thread_lock_acquired

    try:
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

        display.update(pos, device, True if len(devices) is 1 else False)
    except Exception as e:
        if env.DEBUG:
            print('Error in updateDisplay function:', e)
    finally:
        thread_lock_acquired = False
        gc.collect()


def thread1 (data):
    """
    Segundo hilo para acciones secundarias.
    TODO: plantear si poner en este hilo bucle para botones y apagar pantalla
    """
    global thread_lock_acquired

    if not thread_lock_acquired:
        thread_lock_acquired = True

        if env.DEBUG:
            print('')
            print('Datos a procesar:', data)

        # Iniciar un nuevo hilo que llama a updateDisplay(data)
        #_thread.start_new_thread(updateDisplay, (data))

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

        display.update(pos, device, True if len(devices) is 1 else False)

        thread_lock_acquired = False
        gc.collect()


def thread0 ():
    """
    Primer hilo para lecturas y envío de datos a las acciones del segundo hilo.
    """

    print('Entra en el hilo 0')

    devices_info = api.get_computers_list()

    print(devices_info)

    # Iniciamos el servidor WebSocket en un nuevo hilo
    websocket_server = WebSocketServer(thread1)

    websocket_server.start()
    #_thread.start_new_thread(websocket_server.start, ())







#_thread.start_new_thread(display.debug_balls, ())

thread0()


"""
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
"""