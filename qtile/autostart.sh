#!/bin/bash

# Teclado
setxkbmap latam &

# Fondo
feh --bg-scale ~/dotfiles/wallpapers/wallpaper.jpg &

killall -q picom
killall -q xbindkeys

# Compositor
picom --config ~/.config/picom/picom.conf &

xbindkeys &

#Bar
~/.config/polybar/launch.sh &
