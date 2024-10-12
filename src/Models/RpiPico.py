from machine import ADC, Pin
import network
from time import sleep

# Constants
WIFI_DISCONNECTED = 0
WIFI_CONNECTING = 1
WIFI_CONNECTED = 3


class RpiPico:
    INTEGRATED_TEMP_CORRECTION = 27  # Corrección de temperatura interna para ajustar lecturas
    adc_voltage_correction = 0.706
    voltage_working = 3.3
    num_of_measurements = 0  # Número de mediciones de temperatura

    max = 0
    min = 0
    avg = 0
    current = 0
    sum_of_temps = 0  # Suma de todas las lecturas de temperatura
    locked = False

    # Inalámbrico
    wifi = None

    hostname = 'Rpi-Pico-W'

    def __init__ (self, ssid=None, password=None, debug=False, country="ES",
                  alternatives_ap=None,
                  hostname="Rpi-Pico-W"):
        """
        Constructor de la clase RpiPico.

        Args:
            ssid (str): ID de red para la conexión Wi-Fi. Por defecto None.
            password (str): Contraseña para la conexión Wi-Fi. Por defecto None.
            debug (bool): Indica si se muestran los mensajes de debug. Por defecto False.
            alternatives_ap (tuple): Puedes pasar una tupla con redes adicionales.
            country (str): Código del país. Por defecto 'ES'.
        """
        self.DEBUG = debug
        self.SSID = ssid
        self.PASSWORD = password
        self.COUNTRY = country
        self.hostname = hostname
        self.alternatives_ap = alternatives_ap

        self.TEMP_SENSOR = ADC(4)  # Sensor interno de Raspberry Pi Pico.

        self.LED_INTEGRATED = Pin("LED",
                                  Pin.OUT)  # Definición del GPIO para el LED integrado

        self.adc_conversion_factor = self.voltage_working / 65535  # Factor de conversión de 16 bits

        if ssid and password:  # Si se proporcionan credenciales Wi-Fi, intenta la conexión
            print('Iniciando la conexión inalámbrica')
            self.wifi_connect(ssid, password)

        sleep(0.100)

        self.reset_stats()

    def reset_stats (self, temp=None):
        """
        Reinicia las estadísticas de temperatura.

        Args:
            temp (float): Valor inicial con el que resetear las estadísticas. Por defecto None.
        """
        temp = temp if temp else self.read_sensor_temp()
        self.max = temp
        self.min = temp
        self.avg = temp
        self.current = temp

    def read_sensor_temp (self):
        """
        Lee la temperatura actual del sensor.

        Returns:
            float: Temperatura leída.
        """
        # Continúa si no está bloqueado
        if self.locked:
            return self.current

        reading = (
                              self.TEMP_SENSOR.read_u16() * self.adc_conversion_factor) - self.adc_voltage_correction
        value = self.INTEGRATED_TEMP_CORRECTION - reading / 0.001721

        cpu_temp = round(float(value), 1)
        self.current = cpu_temp

        # Actualiza las estadísticas
        if cpu_temp > self.max:
            self.max = cpu_temp
        if cpu_temp < self.min:
            self.min = cpu_temp

        self.num_of_measurements += 1
        self.sum_of_temps += cpu_temp
        self.avg = round(self.sum_of_temps / self.num_of_measurements, 1)

        return cpu_temp

    def get_temp (self):
        """
        Obtiene la temperatura actual.

        Returns:
            float: Temperatura actual.
        """
        return self.read_sensor_temp()

    def led_on (self):
        """
        Enciende el LED integrado.
        """
        self.LED_INTEGRATED.on()

    def led_off (self):
        """
        Apaga el LED integrado.
        """
        self.LED_INTEGRATED.off()

    def get_temp_stats (self):
        """
        Obtiene las estadísticas actuales de temperatura.

        Returns:
            dict: Contiene la temperatura máxima, mínima, promedio y actual.
        """
        return {
            'max': self.max,
            'min': self.min,
            'avg': self.avg,
            'current': self.current
        }

    def wifi_status (self):
        """
        Obtiene el estado de la conexión Wi-Fi.

        Returns:
            int: Constante que indica el estado de la conexión Wi-Fi.
        """
        return self.wifi.status() if self.wifi else WIFI_DISCONNECTED

    def wifi_is_connected (self):
        """
        Comprueba si el Wi-Fi está conectado.

        Returns:
            bool: True si está conectado, False en caso contrario.
        """
        return bool(
            self.wifi and self.wifi.isconnected() and self.wifi.status() == WIFI_CONNECTED)

    def wifi_debug (self):
        """
        Muestra información de debug de la conexión Wi-Fi.
        """
        print('Conectado a wifi:', self.wifi_is_connected())
        print('Estado del wi-fi:', self.wifi_status())
        print('Dirección IP Wi-fi:', self.wifi.ifconfig())
        print('Canal de Wi-fi: ', self.wifi.config('channel'))
        print('ESSID: ', self.wifi.config('essid'))
        print('Potencia de transmisión (TXPOWER):', self.wifi.config('txpower'))
        print('Hostname:', self.wifi.config('hostname'))

        import ubinascii
        import network

        # Convierte la dirección MAC a formato legible
        mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
        print('Dirección MAC: ', mac)

    def wifi_connect (self, ssid=None, password=None):
        """
        Intenta conectar a Wi-Fi con las credenciales dadas.

        Args:
            ssid (str): ID de red para la conexión Wi-Fi.
            password (str): Contraseña para la conexión Wi-Fi.

        Retorno:
            bool: True si se logra conectarse, False en caso contrario.
        """
        if ssid is None and password is None:
            ssid, password = self.SSID, self.PASSWORD

        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)

        # Establece el nombre del host
        network.hostname(self.hostname)

        # Desactiva el ahorro de energía
        self.wifi.config(pm=0xa11140)

        while not self.wifi_is_connected():
            # Escaneamos las redes disponibles
            available_ssids = self.wifi.scan()
            available_ssids = [ap[0].decode('utf-8') for ap in available_ssids]

            # Si la red principal se encuentra disponible, intenta conectar a ella
            if self.SSID in available_ssids:
                self.wifi.connect(self.SSID, self.PASSWORD)
            else:
                # Si no esta la red principal, intenta conectar a las redes secundarias disponibles
                for ap in self.alternatives_ap:
                    if ap['ssid'] in available_ssids:
                        self.wifi.connect(ap['ssid'], ap['password'])
            sleep(1)
            # Verificar y mostrar información de conexión si se encuentra conectado
            if self.wifi_is_connected():
                if self.DEBUG:
                    self.wifi_debug()
                return True
        return False

    def wifi_disconnect (self):
        """
        Desconecta el wi-fi.
        """
        self.wifi.disconnect()

    def read_analog_input (self, pin):
        """
        Lee una entrada analógica.

        Args:
            pin (int): Número del pin del que leer.

        Returns:
            float: Lectura analógica.
        """
        reading = ADC(pin).read_u16()

        return self.voltage_working - ((reading / 65535) * self.voltage_working)
