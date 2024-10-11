#from machine import Pin, SPI
import _thread, gc
from time import sleep_ms, sleep, time
from Models.Api import Api
from Models.RpiPico import RpiPico
from Models.PicoDisplay2 import PicoDisplay2
from Models.WebSocketServer import WebSocketServer

# Importo variables de entorno
import env

# Habilito recolector de basura
gc.enable()

# Rpi Pico Model
controller = RpiPico(ssid=env.AP_NAME, password=env.AP_PASS, debug=env.DEBUG,
                     hostname="Raupulus KeyCounter")
#controller = RpiPico(debug=env.DEBUG)

# Display Model
display = PicoDisplay2(controller=controller)

sleep_ms(20)

# Api
api = Api(controller=controller, url=env.API_URL, path=env.API_PATH,
          token=env.API_TOKEN, device_id=env.DEVICE_ID, debug=env.DEBUG)

sleep_ms(20)

# Variables para el manejo de bloqueo con el segundo core
thread_lock = _thread.allocate_lock()
thread_lock_acquired = False

sleep_ms(20)

# Websocket Server
websocket_server = WebSocketServer()

#gc.collect()

def thread0():
    """
    Primer hilo para lecturas y envío de datos a las acciones del segundo hilo.
    """

    print('Entra en el hilo 0')

    devices_info = api.get_computers_list()

    print(devices_info)

    websocket_server.start()

def thread1():
    """
    Segundo hilo para acciones secundarias.
    """
    pass


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