import usocket as socket
import ujson as json
import _thread


class WebSocketServer:

    def __init__ (self, callback, ip='0.0.0.0', port=80):
        self.callback = callback
        self.ip = ip
        self.port = port
        self.s = socket.socket()

    def start (self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.ip, self.port))
        self.s.listen(1)

        while True:
            conn, addr = self.s.accept()
            print('Conexión establecida con:', addr)

            # Creamos un nuevo hilo para manejar cada conexión
            self.handle_client(conn)

    def handle_client (self, conn):
        while True:
            data = conn.recv(1024)

            if data:
                try:
                    data = data.decode('utf-8')
                    print("Datos recibidos: ", data)
                    data_dict = json.loads(data)

                    response = json.dumps(data_dict)
                    conn.send(response.encode('utf-8'))

                    if "device_id" in data_dict:
                        self.callback(data_dict)
                except Exception as e:
                    print("Error en el manejo de datos: ", e)

            else:
                conn.close()
                break
