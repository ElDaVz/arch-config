#!/usr/bin/env python3
import math, time, sys, os

def move(y, x): 
    sys.stdout.write(f"\033[{y};{x}H")

def clear_pos(y, x, w=3):
    move(y-1, x-1)
    print("   ", end="")
    move(y, x-1)
    print("   ", end="")
    move(y+1, x-1)
    print("   ", end="")

def draw(y, x, char, color):
    if y > 0 and x > 0:
        move(y, x)
        sys.stdout.write(f"{color}{char}\033[0m")

BLUE   = "\033[38;5;111m"
CYAN   = "\033[38;5;81m"
YELLOW = "\033[38;5;226m"
GRAY   = "\033[38;5;245m"
RESET  = "\033[0m"

CX, CY = 35, 10
R1x, R1y = 10, 4
R2x, R2y = 20, 7

os.system("tput civis")
os.system("clear")

# Draw sun
draw(CY-1, CX, "✦", YELLOW)
draw(CY,   CX, "☀", YELLOW)
draw(CY+1, CX, "✦", YELLOW)

# Draw orbits
for a in range(0, 360, 5):
    r = math.radians(a)
    x1 = int(CX + R1x * math.cos(r))
    y1 = int(CY + R1y * math.sin(r))
    x2 = int(CX + R2x * math.cos(r))
    y2 = int(CY + R2y * math.sin(r))
    if y1 > 0 and x1 > 0:
        draw(y1, x1, "·", GRAY)
    if y2 > 0 and x2 > 0:
        draw(y2, x2, "·", GRAY)

sys.stdout.flush()

a1, a2 = 0, 0
try:
    while True:
        r1 = math.radians(a1)
        r2 = math.radians(a2)

        x1 = int(CX + R1x * math.cos(r1))
        y1 = int(CY + R1y * math.sin(r1))
        x2 = int(CX + R2x * math.cos(r2))
        y2 = int(CY + R2y * math.sin(r2))

        draw(y1, x1, "◉", BLUE)
        draw(y2, x2, "●", CYAN)
        sys.stdout.flush()

        time.sleep(0.06)

        clear_pos(y1, x1)
        clear_pos(y2, x2)

        # Redraw orbit dots
        draw(y1, x1, "·", GRAY)
        draw(y2, x2, "·", GRAY)

        a1 = (a1 + 6) % 360
        a2 = (a2 + 3) % 360

except KeyboardInterrupt:
    os.system("tput cnorm")
    os.system("clear")