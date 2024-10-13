import socket
import json
import datetime
import random


def client (ip='172.18.1.209', port=80):
    datas = {  # Definir mensaje por defecto
        'device_id': 3,
        'session': {
            'pulsations_total': random.randint(6000, 30000)
        },
        'streak': {
            'pulsations_current': random.randint(140, 1200),
            'pulsation_average': random.randint(1, 400)
        },
        'timestamp': 'N/D',
        'time': 'N/D',
        'system': {
            'so': 'Debian Testing',
        }
    }

    datas1 = {  # Definir mensaje por defecto
        'device_id': 9,
        'session': {
            'pulsations_total': 3121
        },
        'streak': {
            'pulsations_current': 9999,
            'pulsation_average': 115
        },
        'timestamp': 'N/D',
        'time': 'N/D',
        'system': {
            'so': 'Macos 15',
        }
    }

    # Añadir el timestamp UTC al diccionario
    datas['timestamp'] = datetime.datetime.now(datetime.timezone.utc).strftime(
        '%Y-%m-%d %H:%M:%S')

    datas1['timestamp'] = datetime.datetime.now(datetime.timezone.utc).strftime(
        '%Y-%m-%d %H:%M:%S')

    # Añadir la hora al diccionario
    datas['time'] = datetime.datetime.now().strftime(
        '%H:%M:%S')

    datas1['time'] = datetime.datetime.now().strftime(
        '%H:%M:%S')

    # Convertir el diccionario a una cadena JSON
    data_string = json.dumps(datas)
    data1_string = json.dumps(datas1)

    # Creamos el socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Nos conectamos al servidor
        s.connect((ip, port))

        # Enviamos los datos
        s.send(data_string.encode('utf-8'))

        # Recibimos la respuesta
        data = s.recv(1024)
        print('Datos recibidos:', data)

    """
    # Creamos el socket 2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Nos conectamos al servidor
        s.connect((ip, port))

        # Enviamos los datos
        s.send(data1_string.encode('utf-8'))

        # Recibimos la respuesta
        data1 = s.recv(1024)
        print('Datos recibidos:', data1)
    """

client()
