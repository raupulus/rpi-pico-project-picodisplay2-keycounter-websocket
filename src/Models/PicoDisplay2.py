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

    def initialize(self):
        self.led.set_rgb(0, 0, 200)
        self.display.set_backlight(1.0)
        self.display.set_font("bitmap6")
        self.display.set_pen(self.BLACK)
        self.display.clear()
        self.create_frame()

    def create_frame (self):
        # Grosor del trazo para el marco
        border_thickness = 3

        # Set pen to yellow and draw a horizontal line in the middle of the screen
        self.display.set_pen(self.YELLOW)
        self.display.line(0, self.HEIGHT // 2, self.WIDTH, self.HEIGHT // 2)

        # Set pen to blue
        self.display.set_pen(self.BLUE)

        # Draw blue border (clockwise)
        self.display.line(border_thickness, border_thickness,
                          self.WIDTH - border_thickness,
                          border_thickness)  # Top border
        self.display.line(self.WIDTH - border_thickness, border_thickness,
                          self.WIDTH - border_thickness,
                          self.HEIGHT - border_thickness)  # Right border
        self.display.line(border_thickness, self.HEIGHT - border_thickness,
                          self.WIDTH - border_thickness,
                          self.HEIGHT - border_thickness)  # Bottom border
        self.display.line(border_thickness, border_thickness, border_thickness,
                          self.HEIGHT - border_thickness)  # Left border



        # Show changes on the display
        self.display.update()

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

        border_thickness = 3
        clear_height = (self.HEIGHT // 2) - (2 * border_thickness)
        start_y = 2 * border_thickness if position == 0 else self.HEIGHT // 2 + border_thickness
        start_x = border_thickness * 2
        clear_width = self.WIDTH - start_x - border_thickness

        # Clear only half of the screen, preserving border and line.
        self.display.rectangle(start_x, start_y, clear_width, clear_height)

        system_data = device.system
        streak_data = device.streak
        session_data = device.session

        self.display.set_font("bitmap16")


        offset_text = start_y + 6
        self.display.set_pen(self.GREEN)  # set pen color to green for title
        self.display.text(f"OS:", 10 + border_thickness, offset_text)

        self.display.set_pen(self.RED)  # set pen color to red for value
        self.display.text(f"{system_data['so'] if system_data else 'N/A'}",
                          50 + border_thickness, offset_text)


        offset_text += 28
        self.display.set_pen(self.GREEN)
        self.display.text(f"AVG:", 10 + border_thickness, offset_text, scale=3)

        self.display.set_pen(self.MAGENTA)
        self.display.text(
            f"{streak_data['pulsation_average'] if streak_data else 'N/A'}",
            76 + border_thickness, offset_text, scale=3)

        offset_text += 22
        self.display.set_pen(self.GREEN)
        self.display.text(f"ALL:", 10 + border_thickness, offset_text, scale=3)

        self.display.set_pen(self.RED)
        self.display.text(
            f"{session_data['pulsations_total'] if session_data else 'N/A'}",
            76 + border_thickness, offset_text, scale=3)

        offset_text += 28

        self.display.set_font("bitmap14_outline")

        self.display.set_pen(self.ORANGE)
        self.display.text(f"{device.time}", 105 + border_thickness,
                          offset_text, scale=2)

        self.display.set_font("bitmap16")

        self.display.set_pen(self.YELLOW)
        self.display.text(
            f"{streak_data['pulsations_current'] if streak_data else 'N/A'}",
            self.WIDTH - 132 - border_thickness * 2,
            start_y + ((clear_height - 70) // 2), scale=4)

        self.display.set_font("bitmap6")

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