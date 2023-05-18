# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess
from typing import List  # noqa: F401

from libqtile import layout, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

#import subprocess
# 这里导入自定义的颜色
from colors import colors
# 桌面的导航栏等设置写在里screens.py里
from screens import screens

# mod4是win键， mod1是alt键
mod = "mod4"
mod1 = "mod1"
mod2 = "mod2"
terminal = guess_terminal()
#terminal = 'kitty' kitty里没法输入中文
#terminal = 'mate-terminal'

cmds={
	"autostart":os.path.expanduser("~/.config/qtile/autostart.sh"),
	"resume":os.path.expanduser("~/.config/qtile/resume.sh"),
	"powermenu":lazy.spawn("bash /home/baiguo/.config/qtile/rofi/powermenu.sh"),
	"rofi_drun":lazy.spawn("rofi -show drun -theme launchpad"),
	"rofi_windows":lazy.spawn("rofi -show window -theme window"),
	"print_screen":lazy.spawn("flameshot screen -n 0 -c"),
	"shot_screen":lazy.spawn("flameshot gui"),
}
@hook.subscribe.startup_once
def autostart():
    # 登陆时扫描~/.config/autostart/ 目录和 ~/.config/qtile/autostart.sh中的command
    # 来启动命令和脚本
    subprocess.call([cmds["autostart"]])

#@hook.subscribe.resume
#def after_resume():
#	# 从睡眠（挂起）、休眠等状态中唤醒，触发的事件
#	subprocess.call([cmds["resume"]])

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

    # Win + Tab，窗口最大化、还原
    Key([mod], "Tab", lazy.window.toggle_maximize()),

	# Win + v， 窗口最小化，还原
	Key([mod], "v", lazy.window.toggle_minimize()),
	
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

# 左上角显示6个任务区
groups = [Group(i) for i in "123456"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
       Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

       # mod1 + shift + letter of group = switch to & move focused window to group
       Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
           desc="Switch to & move focused window to group {}".format(i.name)),
       # Or, use below if you prefer not to switch to that group.
        # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])


# Command to find out wm_class of window: xprop | grep WM_CLASS

# 布局
layouts = [
	layout.Columns(
        border_focus_stack=['#d75f5f', '#8f3d3d'], 
        border_width=4,
        margin=[5, 5, 5, 5], # 设置上下左右的空隙
	),
	layout.Max(),
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

# 设置顶栏组件（widget）的默认字体
widget_defaults = dict(
    font='JetBrainsMono Nerd Font Mono Medium',
    fontsize=25,
    padding=3,
    background=colors["foregound"],
)
extension_defaults = widget_defaults.copy()

#screens = [
#    Screen(
#        bottom=bar.Bar(
#            [
#                widget.CurrentLayout(),
#                widget.GroupBox(),
#                widget.Prompt(),
#                widget.WindowName(),
#                widget.Chord(
#                    chords_colors={
#                        'launch': ("#ff0000", "#ffffff"),
#                    },
#                    name_transform=lambda name: name.upper(),
#                ),
#                widget.TextBox("default config", name="default"),
#                widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
#                widget.Systray(),
#                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
#                widget.QuickExit(),
#            ],
#            24,
 #           # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
#            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
 #       ),
 #   ),
#]

# Drag floating layouts.
# 按住win键点击鼠标左键，就可以拖动窗口
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", #lazy.window.bring_to_front()
          lazy.window.toggle_floating())
]
  
dgroups_key_binder = None
dgroups_app_rules = []  # type: List

# 以下配置很重要（对于uTools、QQ来说）
# 作用：当窗口显示，把这个窗口移动到当前焦点所在的窗口中。
# 先定义一个应用列表
# appArray=['uTools','QQ']
@hook.subscribe.client_new
def moveWindowToCurrentGroup(w):
    #if w.name in appArray:
    #    w.togroup(qtile.current_group.name) # qtile识别当前组是看（真实）鼠标在哪个组
	w.togroup(qtile.current_group.name)
	# 直接设置所有的软件只要一打开就挪到当前组

# 鼠标是否跟随焦点，屏幕上没窗口，焦点跑到上一个操作的组中的窗口中，然后（虚假的）鼠标就挪到屏幕中间。
cursor_warp = False



# 焦点是否跟随鼠标
follow_mouse_focus = False


# 当窗口需要焦点，自动获得焦点
focus_on_window_activation = "smart"

#bring_front_click = False
bring_front_click = "floating_only"



# 自动设为浮动窗口
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    #Match(wm_class='uTools'),
    Match(title='图片查看器'),
    Match(wm_class="org.jackhuang.hmcl.Launcher"),
    Match(wm_class="xfce4-terminal"),
])
auto_fullscreen = True



reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
# wmname是用来在各种fetch（比如neofetch）中显示WM的字符串而已
# 这里里代码用来显示qtile版本,但是为显示版本是0.0.0
#version = subprocess.run(['/home/baiguo/.local/bin/qtile', '--version'],
#                         capture_output=True, text=True
#                        ).stdout.strip()
#wmname = f"Qtile {version}"
