import usocket as socket
import ujson as json


class WebSocketServer:
    def __init__ (self, controller, callback, debug=False, ip='0.0.0.0',
                  port=80):
        """
        Constructor para la clase que representa el servidor de websockets

        :param callback: Método a ejecutar cuando recibe datos
        :param debug: Indica si se activa el modo debug
        :param ip: Es la ip del servidor
        :param port: Es el puerto del servidor
        """
        self.controller = controller
        self.callback = callback
        self.ip = ip
        self.port = port
        self.s = socket.socket()
        self.DEBUG = debug

        self.lock = False

    def start (self) -> None:
        """
        Inicializa la escucha del servidor.

        :return: None
        """
        while True:
            try:
                self.controller.wifi_connect()
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.s.bind((self.ip, self.port))
                self.s.listen(1)

                while True:
                    try:
                        if not self.lock:
                            conn, addr = self.s.accept()

                            if self.DEBUG:
                                print('Conexión establecida con:', addr)

                            self.lock = True
                            # Al existir cliente se maneja la conexión
                            self.handle_client(conn)
                    except Exception as e:
                        if self.DEBUG:
                            print('Error al ejecutar la escucha del servidor en start() dentro del while', e)
                    finally:
                        self.lock = False
            except Exception as e:
                if self.DEBUG:
                    print('Error al ejecutar la escucha del servidor en start()', e)

    def handle_client (self, conn) -> None:
        """
        Procesa la recepción de datos.
        """

        conn.setblocking(False)
        conn.settimeout(5.0)  # wait for 5 seconds

        try:
            while True:
                data = conn.recv(1024)

                if data:
                    data = data.decode('utf-8')

                    if self.DEBUG:
                        print("Datos recibidos: ", data)

                    data_dict = json.loads(data)

                    if "device_id" in data_dict:
                        response = json.dumps({ 'status': 'ok' })
                        conn.send(response.encode('utf-8'))

                        self.callback(data_dict)
                else:
                    conn.close()

                    break

            conn.close()
        except Exception as e:
            print("Error Websocket Server en handle_client(): ", e)
