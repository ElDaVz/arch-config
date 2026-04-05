#!/bin/bash
# Only run in kitty and not already in tmux
if [ "$TERM" = "xterm-kitty" ] && [ -z "$TMUX" ]; then
    tmux new-session \; \
        split-window -v -p 70 \; \
        select-pane -t 0 \; \
        send-keys "python3 ~/.config/kitty/planets.py" Enter \; \
        select-pane -t 1
fi