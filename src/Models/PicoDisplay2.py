import time
import random
from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P8

class PicoDisplay2:
    MODES = ['A', 'B', 'C', 'D']
    current_mode = 'A'

    button_a = Button(12)
    button_b = Button(13)
    button_x = Button(14)
    button_y = Button(15)

    led = RGBLED(6, 7, 8)

    def __init__(self, controller, debug=False) -> None:
        self.DEBUG = debug
        self.controller = controller

        self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2,
                                   pen_type=PEN_P8)

        self.WIDTH, self.HEIGHT = self.display.get_bounds()

        self.WHITE = self.display.create_pen(255, 255, 255)
        self.BLACK = self.display.create_pen(0, 0, 0)
        self.CYAN = self.display.create_pen(0, 255, 255)
        self.MAGENTA = self.display.create_pen(255, 0, 255)
        self.YELLOW = self.display.create_pen(255, 216, 0)
        self.GREEN = self.display.create_pen(0, 121, 64)
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

    def initialize(self):
        self.led.set_rgb(0, 0, 200)
        self.display.set_backlight(1.0)
        self.display.set_font("bitmap8")
        self.display.set_pen(self.BLACK)
        self.display.clear()
        self.display.text("Inicializando...", 70, 100)
        self.display.update()

    # a handy function we can call to clear the screen
    # display.set_pen(15) is white and display.set_pen(0) is black
    def clear(self):
        if self.DEBUG:
            print("Clearing Pico Display")

        self.display.set_pen(self.BLACK)
        self.led.set_rgb(0, 200, 0)
        self.display.clear()
        self.display.update()

    def update (self, position, device):
        self.led.set_rgb(200, 0, 0)

        if self.DEBUG:
            print("Actualizando Pico Display")

        self.display.set_pen(self.BLACK)

        start_y = 0 if position == 0 else self.HEIGHT // 2
        height = self.HEIGHT // 2

        # Clear only half of the screen
        self.display.rectangle(0, start_y, self.WIDTH, height)

        self.display.set_pen(self.GREEN)

        # Información del Sistema
        system_data = device.system
        self.display.text(f"OS: {system_data['so'] if system_data else 'N/A'}",
                          10,
                          start_y + 10)

        # Racha actual
        streak_data = device.streak
        self.display.text(
            f"Strike: {streak_data['pulsations_current'] if streak_data else 'N/A'}",
            10, start_y + 30)

        # Media de pulsaciones
        self.display.text(
            f"AVG: {streak_data['pulsation_average'] if streak_data else 'N/A'}",
            10, start_y + 50)

        # Total de la sesión
        session_data = device.session
        self.display.text(
            f"Total: {session_data['pulsations_total'] if session_data else 'N/A'}",
            10, start_y + 70)

        self.display.text(f"Actualizado: {device.timestamp}", 10,
                          start_y + 90)

        self.display.update()

        self.led.set_rgb(0, 200, 0)

    def debug_balls(self):

        print('Entra en debug balls')

        class Ball:
            def __init__ (self, x, y, r, dx, dy, pen):
                self.x = x
                self.y = y
                self.r = r
                self.dx = dx
                self.dy = dy
                self.pen = pen

        # initialise shapes
        balls = []
        for i in range(0, 100):
            r = random.randint(0, 10) + 3
            balls.append(
                Ball(
                    random.randint(r, r + (self.WIDTH - 2 * r)),
                    random.randint(r, r + (self.HEIGHT - 2 * r)),
                    r,
                    (14 - r) / 2,
                    (14 - r) / 2,
                    self.display.create_pen(random.randint(0, 255),
                                       random.randint(0, 255),
                                       random.randint(0, 255)),
                )
            )

        BG = self.display.create_pen(40, 40, 40)

        while True:
            self.display.set_pen(BG)
            self.display.clear()

            for ball in balls:
                ball.x += ball.dx
                ball.y += ball.dy

                xmax = self.WIDTH - ball.r
                xmin = ball.r
                ymax = self.HEIGHT - ball.r
                ymin = ball.r

                if ball.x < xmin or ball.x > xmax:
                    ball.dx *= -1

                if ball.y < ymin or ball.y > ymax:
                    ball.dy *= -1

                self.display.set_pen(ball.pen)
                self.display.circle(int(ball.x), int(ball.y), int(ball.r))

            self.display.update()
            time.sleep(0.01)