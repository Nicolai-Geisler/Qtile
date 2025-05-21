# IMPORTS
import subprocess # Manage subprocesses like picom
import psutil # System resources
import iwlib # Wlan
from libqtile import hook
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Start picom with qtile
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(['picom'])


def getInterface():
    
    interfaces = []
    try:
        with open('/proc/net/dev', 'r') as f:
            # Skip first two entries
            next(f)
            next(f)
            for line in f:
                if ':' in line:
                    interface = line.split(':')[0].strip()
                    if interface != 'lo':
                        interfaces.append(interface)
    except Exception as e:
        print(f"Error reading file: {e}")

    for interface in interfaces:
        if interface == 'enp0s3':
            return '󰈀'
        else:
            return '󰖩'

    return 'ERR'

# NORD THEME
colors = {
    "background": "#282a36", 
    "foreground": "#f8f8f2",  # White
    "polar_night": "#2e3440", # Dark blue 
    "snow_storm": "#d8dee9",  # Off-white
    "frost": "8fbcbb",        # Icy cyan
    "muted_red": "#bf616a",   # Muted Red
    "muted_yellow": "#ebcb8b",# Muted yellow
    "soft_green": "#a3be8c",  # Soft green
    "calm_purple": "#b48ead", # Calm purple
    "deep_fjord": "#5e81AC"   # Rich blue
}


mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key(
        [mod], "r",
        lazy.spawn("rofi -show drun -config ~/.config/rofi/config.rasi"),
        desc="Launch Rofi (drun)"
    ),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
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
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus = colors["deep_fjord"], # "#4287f5",
        border_normal = colors["polar_night"], # "#184080",
        border_width=2,
        margin=10,
        margin_on_single=10,
    ),
    layout.Max(
        margin=10,
        border_width=2,
        border_focus = "#4287f5",
        border_normal = "#184080",
    ),
    layout.Floating(
        border_normal = colors["deep_fjord"],# "#184080",
        border_focus = colors["polar_night"], # "#4287f5",
        border_width = 2,
        margin = 10,
    ),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=14,
    padding=4,
    background=colors["background"],
    foreground=colors["snow_storm"]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper='~/.config/qtile/wallpaper_nord_theme.jpg',
        wallpaper_mode='stretch',
        top=bar.Bar(
            [
                widget.Spacer(length=10),
                # widget.CurrentLayout(),
                widget.GroupBox(
                    highlight_method='block',
                    block_highlight_text_color=colors["foreground"],
                    this_current_screen_border=colors["deep_fjord"],
                    active=colors["calm_purple"],
                    inactive=colors["snow_storm"]
                ),
                widget.LaunchBar(
                    progs = [
                        (' 󰈹 ', 'firefox', 'Firefox'),
                        ('  ', 'alacritty', 'Alacritty'),
                        ('  ', 'pcmanfm', 'PCMan'),
                    ],
                    fontsize=18,
                    text_only=True,
                ),
                widget.Sep(
                    size_percent=66,
                    padding=20
                ),
                widget.TaskList(
                    parse_text = lambda self, win: win.window.get_wm_class()[0].capitalize() if win.window.get_wm_class() else win.name,
                ),
                widget.Spacer(),
                widget.OpenWeather(
                    location = "Wangen,DE",
                    # format = '{location_city}: {main_temp}°{units_temperature} {icon}',
                    format = '{icon}',
                    fontsize = 18,
                    padding = 12,
                    update_interval = 1800,
                    weather_symbols = {
                        '01d' : '󰖨', # Sunny
                        '01n' : '', # Clear night
                        '02d' : '', # Partly cloudy
                        '02n' : '', # Partly cloudy night
                        '03d' : '󰖐', # Cloudy
                        '03n' : '󰖐',
                        '04d' : '󰖐', # Overcast
                        '04n' : '󰖐',
                        '09d' : '', # Showers
                        '09n' : '',
                        '10d' : '', # Rain
                        '10n' : '',
                        '11d' : '', # Thunderstorm
                        '11n' : '',
                        '13d' : '', # Snow
                        '13n' : '',
                        '50d' : '', # Fog
                        '50n' : '',
                    }
                ),
                widget.Clock( format="%b %d, %H:%M" ),
                widget.Spacer(),
                widget.TextBox(
                    "",
                    foreground=colors["polar_night"],
                    fontsize=40,
                    padding=-4,
                ),
                widget.Systray(),
                widget.TextBox(
                    ' ',
                    padding=2,
                    fontsize=20,
                    foreground=colors["soft_green"],
                    # foreground='#8be858',
                    background = colors["polar_night"],                    
                ),
                widget.ThermalSensor( background=colors["polar_night"] ),
                widget.TextBox(
                    '  ',
                    padding=0,
                    fontsize=18,
                    foreground=colors["muted_yellow"],
                    # foreground='#e8c958',
                    background = colors["polar_night"],                    
                ),
                widget.CPU(
                    format='{load_percent}%',
                    background = colors["polar_night"],                    
                ),
                widget.TextBox(
                    '',
                    padding=6,
                    fontsize=18,
                    foreground=colors["calm_purple"],
                    # foreground='#da58e8',
                    background = colors["polar_night"],                    
                ),
                widget.Memory(
                    format='{MemUsed: .0f}{mm}',
                    padding=0,
                    background = colors["polar_night"],                    
                ),
                # widget.Bluetooth(),
                widget.TextBox(
                    getInterface(),
                    padding=20,
                    fontsize=18,
                    background = colors["polar_night"],                    
                ),
                # widget.Wlan(),
                # widget.Battery(),
                widget.Volume(
                    fmt='<b>{}</b>',
                    emoji=True,
                    emoji_list=['󰸈', '󰕿', '󰖀', '󰕾'],
                    fontsize=18,
                    step=2,
                    background = colors["polar_night"],                    
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn('amixer sset Master toggle'),
                    }
                    #get_volume_command="amixer sget Master | awk -F'[][]' '/Left:/ { print $2 }'",
                ),
                widget.QuickExit(
                    default_text="  ",
                    fontsize = 16,
                    countdown_format=" {}s",
                    countdown_start=5,
                    padding=10,
                    background = colors["polar_night"],                    
                ),
                widget.Spacer(length=5, background=colors["polar_night"])
            ],
            30,
            margin=[10, 10, 0, 10],
            opacity=0.9,
            # border_width=[0, 0, 0, 0],
            # border_color="#222222",
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

