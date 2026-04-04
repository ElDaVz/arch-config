#!/bin/bash

# Teclado
setxkbmap latam &

# Fondo
feh --bg-scale ~/Imágenes/wallpaper.jpg &

# Compositor
picom &
xbindkeys &
~/.config/polybar/launch.sh &
~/.fehbg &