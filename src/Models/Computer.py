import utime


class Computer:
    """
    Clase que representa cada dispositivo
    """
    avg_collection = []

    def __init__ (self, data):
        self.device_id = None
        self.session = None
        self.streak = None
        self.timestamp = None
        self.time = None
        self.system = None
        self.counter = 0
        self.update(data)
        self.last_seen = utime.localtime()

    def update (self, data):
        """
        Actualiza los datos asociados a este dispositivo.
        :param data: Dictionary containing updated values for device information.
        :return: None
        """
        self.device_id = data.get('device_id', self.device_id)
        self.session = data.get('session', self.session)
        self.streak = data.get('streak', self.streak)
        self.timestamp = data.get('timestamp', self.timestamp)
        self.time = data.get('time', self.time)
        self.system = data.get('system', self.system)
        self.last_seen = utime.localtime()

        self.counter += 1

        # Comprueba si existe la racha para añadir las pulsaciones
        if self.streak and 'pulsation_average' in self.streak:
            self.avg_collection.append(self.streak['pulsation_average'])

            # Limito cantidad de muestras a máximo 30
            if len(self.avg_collection) > 30:
                self.avg_collection.pop(0)

        if self.counter >= 100000:
            self.counter = 0
