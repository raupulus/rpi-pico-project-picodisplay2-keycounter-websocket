#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import urequests
import ujson


class Api():
    """
    A class representing an API connection with methods to interact with the endpoint.

    :param controller: The controller object for raspberry pi pico.
    :param url: The base URL of the API.
    :param path: The specific path for the API endpoint.
    :param token: The authentication token for accessing the API.
    :param device_id: The unique identifier of the device.
    :param debug: Optional boolean flag for debugging mode.
    """

    def __init__ (self, controller, url, path, token, device_id, debug=False):
        self.URL = url
        self.TOKEN = token
        self.DEVICE_ID = device_id
        self.URL_PATH = path
        self.CONTROLLER = controller
        self.DEBUG = debug

    def get_computers_list (self) -> dict:
        """
        Obtiene de la Api una lista de diccionarios con los dispositivos de
        tipo computadora para habilitar los que se permiten mostrar por la
        pantalla.
        :return: A list of dictionaries containing information about computers retrieved from the API.
        """
        try:
            ip_address = str(self.CONTROLLER.wifi.ifconfig()[0])

            headers = {
                "Authorization": "Bearer " + self.TOKEN,
                "Local-Ip": ip_address,
                "Device-Id": str(self.DEVICE_ID)
            }

            response = urequests.get(self.URL + '/' + self.URL_PATH,
                                     headers=headers)

            data = ujson.loads(response.text)

            return data
        except Exception as e:
            if self.DEBUG:
                print("Error al obtener los datos de la api: ", e)
            return { }
