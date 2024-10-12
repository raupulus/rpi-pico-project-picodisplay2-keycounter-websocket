import usocket as socket
import ujson as json


class WebSocketServer:
    def __init__ (self, callback, debug=False, ip='0.0.0.0', port=80):
        self.callback = callback
        self.ip = ip
        self.port = port
        self.s = socket.socket()
        self.DEBUG = debug

    def start (self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.ip, self.port))
        self.s.listen(1)

        while True:
            conn, addr = self.s.accept()

            if self.DEBUG:
                print('Conexión establecida con:', addr)

            # Creamos un nuevo hilo para manejar cada conexión
            self.handle_client(conn)

    def handle_client (self, conn):
        while True:
            data = conn.recv(1024)

            if data:
                try:
                    data = data.decode('utf-8')

                    if self.DEBUG:
                        print("Datos recibidos: ", data)

                    data_dict = json.loads(data)

                    if "device_id" in data_dict:
                        response = json.dumps({'status': 'ok'})
                        conn.send(response.encode('utf-8'))

                        self.callback(data_dict)
                except Exception as e:
                    if self.DEBUG:
                        print("Error en el manejo de datos: ", e)

            else:
                conn.close()
                break
