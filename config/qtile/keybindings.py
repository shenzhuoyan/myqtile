from libqtile.command import lazy
from libqtile.config import Key
from libqtile.utils import guess_terminal
import os
import subprocess

# mod4是win键， mod1是alt键
mod = "mod4"
mod1 = "mod1"
mod2 = "mod2"
terminal = guess_terminal()
#terminal = 'kitty' kitty里没法输入中文
#terminal = 'mate-terminal'

cmds={
	"powermenu":lazy.spawn("bash /home/baiguo/.config/qtile/rofi/powermenu.sh"),
	"rofi_drun":lazy.spawn("rofi -show drun -theme launchpad"),
	"rofi_windows":lazy.spawn("rofi -show window -theme window"),
	"print_screen":lazy.spawn("flameshot screen -n 0 -c"),
	"shot_screen":lazy.spawn("flameshot gui"),
}
keys = [
    # A list of available cmds that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # 移动窗口，Win + Shift + I/K/J/L ，上/下/左/右。
    # Win+Shift+j把窗口移动到左边
    Key([mod, "shift"], "j", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "i", lazy.layout.shuffle_up(), desc="Move window up"),

	# 调整窗口大小 Win + Ctrl + I/K/J/L，分别是向上/下/左/右
    Key([mod, "control"], "j", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "k", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "i", lazy.layout.grow_up(), desc="Grow window up"),
    # 重置窗口大小
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

	# 在窗口间移动光标, Win + I/K/JL
	Key([mod], "i", lazy.layout.up(), desc="Move focus up in current stack pane"),
    Key([mod], "k", lazy.layout.down(), desc="Move focus down in current stack pane"),
    Key([mod], "j", lazy.layout.left(), desc="Move focus left in current stack pane"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus right in current stack pane"),
    
    # 占/不占半屏
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Ctrl + Shift + T， 打开终端
    #Key(['control', mod1], "t", lazy.spawn(terminal), desc="Launch terminal"),
    
    # Win + 回车，打开一个悬浮的终端
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
	
	# Win + Tab 焦点在当前组的窗口间移动
	# 我还设置了 悬浮窗口获得焦点自动挪到最前面，这样就不会有悬浮窗口被挡住的风险了
	Key([mod], "Tab", lazy.group.next_window()),

    # Win + Z，窗口最大化、还原
    Key([mod], "z", lazy.window.toggle_maximize()),

	# Win + v， 窗口最小化，还原
	Key([mod], "x", lazy.window.toggle_minimize()),
	
    # Win + Q，关闭当前软件
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    # Win + Ctrl + W， 强制关闭
	Key([mod, "control"], "w", lazy.spawn("xkill"), desc="Force kill window"),

    # Win + Ctrl + R, 重新加载qtile的配置
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),

    # Win + Ctrl + Q, 退出Qtile
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Win + Enter, 执行命令，但bar上没添加输命令的框
    #Key([mod], "Return", lazy.spawncmd("command"),desc="Spawn a command using a prompt widget"),
    
    # 打开电源界面
	Key(['control', mod1], "Return", cmds["powermenu"]),
    
    # Win + A 用来快速打开软件
    Key([mod], "a", cmds["rofi_drun"]),

    # Win + E, 打开文件管理器
    Key([mod], "e", lazy.spawn("nemo"), desc="Launch File Manager"),

    # Alt + Tab，浏览当前窗口。跟Windows一样。主题文件放在~/.local/share/rofi/themes
    Key([mod1], "Tab", cmds["rofi_windows"]),

    # Win + Shift + S ，跟Windows一样，截图
    Key([mod, "shift"], "s", cmds["shot_screen"] , desc="Launches flameshot"),
    
    # 截图全屏
    Key([], "Print", cmds["print_screen"], desc="Shot display 0"),

    # 键盘上的媒体控制键
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"),desc="Play next audio"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Toggle play/pause audio"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Play previous audio" ),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q -D pulse sset Master toggle"), desc="Mute audio" ),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +1%"), desc="Raise volume" ),
    Key([],  "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -1%"), desc="Lower volume" ),
]

