#!/bin/bash

sleep 1

# Teclado
setxkbmap latam &

# Fondo
feh --bg-scale ~/Imágenes/wallpaper.jpg &

# Compositor
picom &
