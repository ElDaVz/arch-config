#!/bin/bash

# Teclado
setxkbmap latam &

# Fondo
feh --bg-scale ~/dotfiles/wallpapers/wallpaper.jpg &

# Compositor
picom &

xbindkeys &

~/.config/polybar/launch.sh &
