#!/bin/bash

# Teclado
setxkbmap latam &

# Fondo
feh --bg-scale ~/dotfiles/wallpapers/wallpaper.jpg &

killall -q picom
killall -q xbindkeys

# Compositor
picom &

xbindkeys &

~/.config/polybar/launch.sh &
