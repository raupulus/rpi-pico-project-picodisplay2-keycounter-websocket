import uwebsockets
import ujson


class WebSocketServer:

    def __init__ (self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port

    def start (self):
        server = uwebsockets.Server(self.port)
        server.run(self._handle_message)

    def _handle_message (self, websocket, msg):
        msg = ujson.loads(msg)  # Convertir mensaje JSON a diccionario

        default_msg = {  # Definir mensaje por defecto
            'device_id': 'N/D',
            'session': {
                'pulsations_total': 'N/D'
            },
            'streak': {
                'pulsations_current': 'N/D',
                'pulsation_average': 'N/D'
            },
            'timestamp': 'N/D',
            'system': {
                'so': 'N/D',
            }
        }

        # Actualizar el mensaje por defecto con valores entrantes
        for key in msg:
            default_msg[key] = msg[key]

        print(f"Received message: {default_msg}")