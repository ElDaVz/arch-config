#!/bin/bash
killall -q picom
killall -q xbindkeys

# Teclado
setxkbmap latam &

# Fondo
feh --bg-scale ~/dotfiles/wallpapers/wallpaper.jpg &

# Compositor
picom &

xbindkeys &

bash ~/.config/polybar/launch.sh --forest &

libinput-gestures-setup start &
