# Raspberry Pi Pico Display 2.0 (Pimoroni version, 320x240px)

Proyecto con raspberry pi pico como servidor websockets en el que se utiliza la pantalla Pico Display 2.0 para mostrar estadísticas de los equipos en la red local de la cantidad de teclas pulsadas 

Sitio web del autor: [https://raupulus.dev](https://raupulus.dev)

![Imagen del Proyecto](docs/images/6.png "Imagen del Proyecto 1")

La raspberry pi pico w se conecta a una api para obtener información de los
dispositivos (así validar de los que tiene permitido mostrar datos por la 
pantalla) y además comunicar al servidor que está encendido junto a la IP que
tiene en la intranet o red local en este momento. De esta forma desde los
clientes (ordenadores) podemos dinámicamente cambiar de red/routers y 
seguirá funcionando en todo momento con todos mis equipos.

Repository [https://gitlab.com/raupulus/rpi-pico-project-picodisplay2-keycounter-websocket](https://gitlab.com/raupulus/rpi-pico-project-picodisplay2-keycounter-websocket)

<p align="center">
  <img src="docs/images/1.jpeg" alt="Imagen del Proyecto 1" height="150">
  <img src="docs/images/2.jpeg" alt="Imagen del Proyecto 2" height="150">
  <img src="docs/images/4.jpeg" alt="Imagen del Proyecto 3" height="150">
  <img src="docs/images/5.jpeg" alt="Imagen del Proyecto 4" height="150">
</p>

## Modelo para la caja 3D

Puedes descargar mi diseño para **Pico Display 2.0** desde el siguiente enlace:

[https://www.thingiverse.com/thing:6662007](https://www.thingiverse.com/thing:6662007)

## Preparar proyecto

Antes de comenzar, hay que copiar el archivo **.env.example.py** a **env.py** 
y rellenar las variables con los datos del wireless y de acceso a la API.

Una vez preparado, subir a la raspberry todo el contenido del directorio **src**

## Instalar micropython para Pico Display 2.0

Sitio web de la pantalla: [Pimoroni](https://shop.pimoroni.com/products/pico-display-pack-2-0?variant=39374122582099)

[Ejemplos para probar la pantalla](https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/pico_display)

Para poder utilizar la pantalla necesitamos instalar el firmware de micropython con soporte para esta pantalla que lo podemos encontrar en el siguiente enlace:

[https://github.com/pimoroni/pimoroni-pico/releases](https://github.com/pimoroni/pimoroni-pico/releases)

En el momento de crear el proyecto está la versión 1.23.0 (https://github.com/pimoroni/pimoroni-pico/releases/download/v1.23.0-1/picow-v1.23.0-1-pimoroni-micropython.uf2)
