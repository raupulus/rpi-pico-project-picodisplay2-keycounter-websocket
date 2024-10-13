import time
import random
from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P8


class PicoDisplay2:
    """
    Initialize the PicoDisplay2 object.

    :param controller: The controller for the raspberry pi pico.
    :param debug: Flag to enable debugging mode (default is False).
    """
    MODES = ['A', 'B', 'C', 'D'] # A: Normal, B: Score, C: Desde api ?, D: Red
    current_mode = 'A'

    button_a = Button(12)
    button_b = Button(13)
    button_x = Button(14)
    button_y = Button(15)

    led = RGBLED(6, 7, 8)

    wireless_info_client = None
    wireless_info_ap = None

    def __init__ (self, controller, debug=False) -> None:
        self.DEBUG = debug
        self.controller = controller

        self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2,
                                    pen_type=PEN_P8)

        self.on = True

        self.WIDTH, self.HEIGHT = self.display.get_bounds()

        self.WHITE = self.display.create_pen(255, 255, 255)
        self.BLACK = self.display.create_pen(0, 0, 0)
        self.CYAN = self.display.create_pen(0, 255, 255)
        self.MAGENTA = self.display.create_pen(255, 0, 255)
        self.YELLOW = self.display.create_pen(255, 216, 0)
        self.GREEN = self.display.create_pen(0, 145, 77)
        self.RED = self.display.create_pen(209, 34, 41)
        self.ORANGE = self.display.create_pen(246, 138, 30)
        self.INDIGO = self.display.create_pen(36, 64, 142)
        self.VIOLET = self.display.create_pen(115, 41, 130)
        self.PINK = self.display.create_pen(255, 175, 200)
        self.BLUE = self.display.create_pen(116, 215, 238)
        self.BROWN = self.display.create_pen(97, 57, 21)
        self.MAGENTA = self.display.create_pen(255, 33, 140)
        self.CYAN = self.display.create_pen(33, 177, 255)

        self.initialize()

    def initialize (self) -> None:
        """
        Prepara por primera vez la pantalla antes de ser dibujada.
        :return: None
        """
        self.led.set_rgb(0, 0, 200)
        self.display.set_backlight(1.0)
        self.display.set_font("bitmap6")
        self.display.set_pen(self.BLACK)
        self.display.clear()
        self.prepare_frame_a()

    def shutdown (self) -> None:
        """
        Simula el apagado de la pantalla, apaga el led y pone el brillo
        al máximo.
        :return: None
        """
        self.led.set_rgb(0, 0, 0)
        self.on = False
        self.display.set_backlight(0.2)
        # self.display.clear()

    def clear (self) -> None:
        """
        Limpia la pantalla completamente.
        :return: None
        """
        if self.DEBUG:
            print("Limpiando pantalla")

        self.display.set_pen(self.BLACK)
        self.led.set_rgb(0, 200, 0)
        self.display.clear()
        self.display.update()

    def update (self, position, device, showbar=False) -> None:
        """
        Actualiza los datos de la pantalla según la posición recibida siendo
        0 para la mitad superior y 1 para la mitad inferior.
        :param position: integer representing the position (0: top, 1:bottom)
        :param device: object containing system, streak, and session data
        :param showbar: boolean indicating whether to display a bar graph (default False)
        :return: None
        """

        if self.current_mode != 'A':
            return

        self.on = True
        self.display.set_backlight(1.0)
        self.led.set_rgb(200, 0, 0)

        if self.DEBUG:
            print("Actualizando Pico Display")

        self.display.set_pen(self.BLACK)

        border_thickness = 3
        clear_height = (self.HEIGHT // 2) - (2 * border_thickness)
        start_y = 2 * border_thickness if position == 0 else self.HEIGHT // 2 + border_thickness
        start_x = border_thickness * 2
        clear_width = self.WIDTH - start_x - border_thickness

        # Limpiando con un rectángulo negro la mitad correspondiente
        self.display.rectangle(start_x, start_y, clear_width, clear_height)

        system_data = device.system
        streak_data = device.streak
        session_data = device.session

        self.display.set_font("bitmap16")

        # Sistema Operativo o Nombre de equipo
        offset_text = start_y + 6
        self.display.set_pen(self.GREEN)
        self.display.text(f"OS:", 10 + border_thickness, offset_text)

        self.display.set_pen(self.RED)
        self.display.text(f"{system_data['so'] if system_data else 'N/A'}",
                          50 + border_thickness, offset_text)

        # Media de pulsaciones
        offset_text += 28
        self.display.set_pen(self.GREEN)
        self.display.text(f"AVG:", 10 + border_thickness, offset_text, scale=3)

        self.display.set_pen(self.MAGENTA)
        self.display.text(
            f"{streak_data['pulsation_average'] if streak_data else 'N/A'}",
            76 + border_thickness, offset_text, scale=3)

        # Total de pulsaciones en la sesión
        offset_text += 22
        self.display.set_pen(self.GREEN)
        self.display.text(f"ALL:", 10 + border_thickness, offset_text, scale=3)

        self.display.set_pen(self.RED)
        self.display.text(
            f"{session_data['pulsations_total'] if session_data else 'N/A'}",
            76 + border_thickness, offset_text, scale=3)

        # Hora del último registro recibido
        offset_text += 28
        self.display.set_font("bitmap14_outline")
        self.display.set_pen(self.ORANGE)
        self.display.text(f"{device.time}", 105 + border_thickness,
                          offset_text, scale=2)

        # Muestra la cantidad de pulsaciones actual
        self.display.set_font("bitmap16")
        self.display.set_pen(self.YELLOW)
        self.display.text(
            f"{streak_data['pulsations_current'] if streak_data else 'N/A'}",
            self.WIDTH - 132 - border_thickness * 2,
            start_y + ((clear_height - 70) // 2), scale=4)

        # Restablezco fuente y actualizo datos
        self.display.set_font("bitmap6")
        self.display.update()

        # Dibuja la barra de estadísticas si solo hay 1 dispositivo
        if showbar:
            self.showbar(device.avg_collection)

        self.led.set_rgb(0, 200, 0)

    def showbar (self, avg_collection) -> None:
        """
        Muestra la barra de estadísticas del dispositivo actual para ver
        la progresión con la velocidad media.

        :param avg_collection: Object containing system, streak, and session data
        :return: None
        """
        if not avg_collection or len(avg_collection) < 3:
            if self.DEBUG:
                print('Para pintar gráfico, avg_collection debe tener más de dos elementos')

            return

        # Limpio la parte de la pantalla por si hubiera datos anteriores
        self.display.set_pen(self.BLACK)
        self.display.rectangle(6, self.HEIGHT // 2 + 3, self.WIDTH - 9,
                               self.HEIGHT // 2 - 9)

        # Espacio las barras de 3 pixeles y resto la cantidad total de
        # espacios entre las barras del ancho total.
        bar_width = (self.WIDTH - 12 - (len(avg_collection) * 3)) // len(
            avg_collection)
        max_value = max(avg_collection)

        prev_height = None
        for i, value in enumerate(avg_collection):
            # Resto 10 píxeles de altura
            bar_height = (value / max_value) * ((self.HEIGHT // 2) - 10)
            bar_height = int(bar_height) if bar_height > 0 else 0

            # Selecciono el color de la barra en función del valor
            if value < 100:
                self.display.set_pen(self.BLUE)
            elif 150 <= value <= 250:
                self.display.set_pen(self.ORANGE)
            else:
                self.display.set_pen(self.RED)

            # Dibujo la barra
            self.display.rectangle((i * (bar_width + 3)) + 6,
                                   self.HEIGHT - bar_height - 6, bar_width,
                                   bar_height)

            # Dibujo un círculo en el pico
            self.display.set_pen(self.INDIGO)
            self.display.circle((i * (bar_width + 3)) + 6 + bar_width // 2,
                                self.HEIGHT - bar_height - 6,
                                2)  # radio de 2 para el círculo

            # Dibujo una línea encima de las barras con la misma restricción
            # de altura que las barras
            self.display.set_pen(self.YELLOW)
            if prev_height is not None:
                start_height = self.HEIGHT - prev_height - 6
                end_height = self.HEIGHT - bar_height - 6
                mid_height = (start_height + end_height) // 2
                mid_x = ((i - 1) * (bar_width + 3)) + 6 + bar_width // 2

                # Dibujo una línea desde la posición previa a la mitad de la
                # barra actual
                self.display.line(mid_x, start_height, mid_x, mid_height)

                # Dibujo una línea desde el centro de la barra hasta la
                # posición actual
                self.display.line(mid_x, mid_height,
                                  (i * (bar_width + 3)) + 6 + bar_width // 2,
                                  end_height)

            prev_height = bar_height

        self.display.update()

    def check_buttons(self):
        """
        Comprueba si hay un botón pulsado y devuelve su letra A,B,C,D o False

        :return: The value 'A' if button A is pressed, 'B' if button B is pressed, 'C' if button X is pressed, 'D' if button Y is pressed, False if no button is pressed.
        """
        if self.button_a.read():
            return 'A'
        elif self.button_b.read():
            return 'B'
        elif self.button_x.read():
            return 'C'
        elif self.button_y.read():
            return 'D'

        return False

    def change_mode(self, mode):

        if mode not in self.MODES:
            return

        self.current_mode = mode
        self.on = True
        self.clear()
        self.display.set_backlight(1.0)

        if mode == 'A':
            self.mode_a()
        elif mode == 'B':
            self.mode_b()
        elif mode == 'C':
            self.mode_c()
        elif mode == 'D':
            self.mode_d()

    def mode_a(self):
        """
        Modo Principal/Normal, muestra los datos recibidos por websocket.

        :return:
        """
        self.prepare_frame_a()

    def mode_b(self):
        """
        Modo B, muestra los datos de puntuación para la racha y sesión.

        :return:
        """
        self.display.set_pen(self.ORANGE)
        self.display.text("MODO B", 100, 100, scale=3)
        self.display.update()

    def mode_c(self):
        """
        Modo C, muestra los datos recibidos desde la API.

        :return:
        """
        self.display.set_pen(self.ORANGE)
        self.display.text("MODO C", 100, 100, scale=3)
        self.display.update()

    def mode_d (self):
        if not self.controller.wifi_is_connected():
            self.controller.wifi_connect()

        info_client = self.wireless_info_client
        info_ap = self.wireless_info_ap

        # Double the title height
        title_height = 26
        line_height = 13
        spacing = 2  # Spacing between text lines
        margin = 10  # Margin for blocks

        # Set title with RED
        self.display.set_pen(self.RED)
        self.display.rectangle(0, 0, self.WIDTH, title_height)
        self.display.set_pen(self.BLUE)
        self.display.text("Wireless", self.WIDTH // 3, spacing)

        offset_y = title_height

        # Add margin to the top of the client block
        offset_y += margin

        # Display client info
        for info in info_client:
            self.display.set_pen(self.BLACK)
            self.display.rectangle(0, offset_y, self.WIDTH, line_height)
            self.display.set_pen(self.GREEN)
            self.display.text(f"{info['name']} {info['value']}", spacing,
                              offset_y)
            offset_y += line_height + spacing

        # Add margin to the bottom of the client block and to the top of the AP block
        offset_y += margin

        # Draw a single yellow background rectangle for the AP block
        self.display.set_pen(self.YELLOW)
        self.display.rectangle(0, offset_y, self.WIDTH,
                               len(info_ap) * (line_height + spacing) + spacing)

        # Display AP info
        for info in info_ap:
            self.display.set_pen(self.BLACK)
            self.display.text(f"{info['name']} {info['value']}", spacing,
                              offset_y)
            offset_y += line_height + spacing

        # Add margin to the bottom of the AP block
        offset_y += margin

        self.display.update()

    def prepare_frame_a (self) -> None:
        """
        Create a frame on the display with specified border thickness.

        :return: None
        """
        # Grosor del trazo para el marco de la pantalla
        border_thickness = 3

        # Preparo línea para la división Horizontal de la pantalla
        self.display.set_pen(self.YELLOW)
        self.display.line(0, self.HEIGHT // 2, self.WIDTH, self.HEIGHT // 2)
        self.display.update()

        # Dibujo un marco alrededor de la pantalla
        self.display.set_pen(self.BLUE)

        # Borde superior
        self.display.line(border_thickness, border_thickness,
                          self.WIDTH - border_thickness, border_thickness)

        # Borde derecho
        self.display.line(self.WIDTH - border_thickness, border_thickness,
                          self.WIDTH - border_thickness,
                          self.HEIGHT - border_thickness)

        # Borde inferior
        self.display.line(border_thickness, self.HEIGHT - border_thickness,
                          self.WIDTH - border_thickness,
                          self.HEIGHT - border_thickness)

        # Borde izquierdo
        self.display.line(border_thickness, border_thickness, border_thickness,
                          self.HEIGHT - border_thickness)

        self.display.update()