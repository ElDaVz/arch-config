#!/usr/bin/env python3
import math, time, sys, os, threading, tty, termios

BLUE   = "\033[38;5;111m"
CYAN   = "\033[38;5;81m"
YELLOW = "\033[38;5;226m"
GRAY   = "\033[38;5;245m"
MAGENTA= "\033[38;5;183m"
RESET  = "\033[0m"

def move(y, x):
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()

def draw(y, x, char, color):
    if y > 1 and x > 1:
        move(y, x)
        sys.stdout.write(f"{color}{char}{RESET}")

# Big sphere made of ASCII chars — rotates through frames
SPHERE1 = [
    [
        "   ██████   ",
        " ██▓▓▓▓▓▓██ ",
        "██▓▓░░░░▓▓██",
        "██▓░░██░░▓██",
        "██▓▓░░░░▓▓██",
        " ██▓▓▓▓▓▓██ ",
        "   ██████   ",
    ],
    [
        "   ██████   ",
        " ██▓▓▓▓▓▓██ ",
        "██▓░░██░░▓██",
        "██▓▓░░░░▓▓██",
        "██░░██░░░▓██",
        " ██▓▓▓▓▓▓██ ",
        "   ██████   ",
    ],
    [
        "   ██████   ",
        " ██▓▓▓▓▓▓██ ",
        "██░░██░░░▓██",
        "██▓▓░░░░▓▓██",
        "██▓░░██░░▓██",
        " ██▓▓▓▓▓▓██ ",
        "   ██████   ",
    ],
    [
        "   ██████   ",
        " ██▓▓▓▓▓▓██ ",
        "██▓▓░░░░▓▓██",
        "██░░██░░░▓██",
        "██▓▓░░░░▓▓██",
        " ██▓▓▓▓▓▓██ ",
        "   ██████   ",
    ],
]

SPHERE2 = [
    [
        " ████ ",
        "██░░██",
        "██████",
        "██░░██",
        " ████ ",
    ],
    [
        " ████ ",
        "██████",
        "██░░██",
        "██████",
        " ████ ",
    ],
    [
        " ████ ",
        "██░░██",
        "██████",
        "██░░██",
        " ████ ",
    ],
    [
        " ████ ",
        "██████",
        "██░░██",
        "██████",
        " ████ ",
    ],
]

def draw_sphere(frames, frame_idx, cy, cx, color):
    frame = frames[frame_idx % len(frames)]
    for i, line in enumerate(frame):
        y = cy + i - len(frame)//2
        x = cx - len(line)//2
        if y > 0 and x > 0:
            draw(y, x, line, color)

def clear_sphere(frames, cy, cx):
    frame = frames[0]
    for i, line in enumerate(frame):
        y = cy + i - len(frame)//2
        x = cx - len(line)//2
        if y > 0 and x > 0:
            move(y, x)
            sys.stdout.write(" " * len(line))

# Draw orbits
def draw_orbit(cx, cy, rx, ry):
    for a in range(0, 360, 4):
        r = math.radians(a)
        x = int(cx + rx * math.cos(r))
        y = int(cy + ry * math.sin(r))
        if y > 0 and x > 0:
            draw(y, x, "·", GRAY)

os.system("tput civis")
os.system("clear")

# Sun position (center)
SX, SY = 40, 12
RX, RY = 28, 9  # orbit radii

draw_orbit(SX, SY, RX, RY)
sys.stdout.flush()

a = 0
f1 = 0
f2 = 0

try:
    while True:
        r = math.radians(a)
        px = int(SX + RX * math.cos(r))
        py = int(SY + RY * math.sin(r))

        # Draw sun (planet 1 - big)
        draw_sphere(SPHERE1, f1, SY, SX, BLUE)

        # Draw orbiting planet (planet 2 - small)
        draw_sphere(SPHERE2, f2, py, px, CYAN)

        sys.stdout.flush()
        time.sleep(0.12)

        # Clear
        clear_sphere(SPHERE1, SY, SX)
        clear_sphere(SPHERE2, py, px)

        # Redraw orbit dots that got cleared
        draw_orbit(SX, SY, RX, RY)

        a = (a + 4) % 360
        f1 = (f1 + 1) % len(SPHERE1)
        f2 = (f2 + 1) % len(SPHERE2)

except KeyboardInterrupt:
    os.system("tput cnorm")
    os.system("clear")