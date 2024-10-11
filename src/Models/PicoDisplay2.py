class PicoDisplay2:

    def __init__(self, controller, debug=False) -> None:
        self.DEBUG = debug
        self.controller = controller

        self.clear()

        self.update()

    # a handy function we can call to clear the screen
    # display.set_pen(15) is white and display.set_pen(0) is black
    def clear(self):
        if self.DEBUG:
            print("Clearing Pico Display")

        pass

    def update(self):
        """
        Actualiza la información de la pantalla
        """

        if self.DEBUG:
            print("Updating Pico Display")

        pass
