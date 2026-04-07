import os
from collections.abc import Callable

import libqtile.resources
import subprocess
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Output, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook

mod = "mod4"
terminal = "kitty"

keys = [
    # --- FOCUS (vim keys) ---
    # Move focus between windows with hjkl
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),

    # --- MOVE WINDOWS (vim keys) ---
    # Shuffle windows around with shift+hjkl
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # --- RESIZE WINDOWS (arrow keys) ---
    # ✅ NEW: grow/shrink with arrows instead of ctrl+hjkl (more intuitive)
    Key([mod], "Right", lazy.layout.grow_right()),
    Key([mod], "Left", lazy.layout.grow_left()),
    Key([mod], "Up", lazy.layout.grow_up()),
    Key([mod], "Down", lazy.layout.grow_down()),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset window sizes"),

    # --- LAYOUTS ---
    # ✅ KEPT: cycle layouts
    Key([mod], "Tab", lazy.next_layout()),
    # ✅ NEW: toggle fullscreen and floating
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),

    # --- APPS ---
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "r", lazy.spawn("rofi -show drun")),
    Key([mod], "e", lazy.spawn("nautilus")),
    # ✅ NEW: screenshot with scrot
    Key([mod, "shift"], "s", lazy.spawn("sh -c 'scrot -s /home/daniel/imagenes/%Y-%m-%d_%H-%M-%S.png'")),

    # --- WINDOW MANAGEMENT ---
    Key([mod], "w", lazy.window.kill()),
    # ✅ NEW: focus urgent window
    Key([mod], "u", lazy.next_urgent()),

    # --- QTILE ---
    # ✅ CHANGED: both ctrl+r and shift+r reload (shift+r is faster)
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "shift"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),

    # --- VOLUME ---
    # ✅ KEPT: media keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # --- BRIGHTNESS ---
    # ✅ NEW: brightness control (requires brightnessctl)
    # --- BRIGHTNESS ---
    Key([], "F7", lazy.spawn("brightnessctl set 10%-")),    
    Key([], "F8", lazy.spawn("brightnessctl set +10%")),    
]

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [Group(i) for i in "1234"]

for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Switch to & move focused window to group {i.name}"),
        ]
    )

layouts = [
    layout.Columns(
        border_focus="#82aaff",
        border_normal="#636d83",
        border_width=2,
        margin=8,
    ),
    layout.Max(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(),
]

fake_screens: list[Screen] | None = None
generate_screens: Callable[[list[Output]], list[Screen]] | None = None

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
idle_timers = []
idle_inhibitors = []
wmname = "LG3D"

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])