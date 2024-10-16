#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import urequests, gc
import ujson
from time import sleep

gc.enable()


class Api():
    def __init__(self, controller, url, path, token, device_id, debug=False):
        self.URL = url
        self.TOKEN = token
        self.DEVICE_ID = device_id
        self.URL_PATH = path
        self.CONTROLLER = controller
        self.DEBUG = debug

    def get_computers_list (self):
        """
        :return: List of computers retrieved from the API. If an error occurs, an empty dictionary is returned.
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
            return {}

