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

from typing import List  # noqa: F401

from libqtile import layout, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match
from libqtile.lazy import lazy

from keybindings import keys

import subprocess
# 这里导入自定义的颜色
from colors import colors
# 桌面的导航栏等设置写在里screens.py里
from screens import screens
from libqtile.utils import send_notification

scripts={
	"autostart":os.path.expanduser("~/.config/qtile/autostart.sh"),
	"resume":os.path.expanduser("~/.config/qtile/resume.sh"),
}

@hook.subscribe.startup_once
def autostart():
    # 登陆时扫描~/.config/autostart/ 目录和 ~/.config/qtile/autostart.sh中的command
    # 来启动命令和脚本
    subprocess.call([scripts["autostart"]])

#@hook.subscribe.resume
#def after_resume():
#	# 从睡眠（挂起）、休眠等状态中唤醒，触发的事件
#	subprocess.call([scripts["resume"]])

# 左上角显示6个任务区
groups = [Group(i) for i in "123456"]
mod = "mod4"
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
layout_setting = {
	"border_focus" : colors["color4"],
	"border_normal" : colors["border"],
	"border_width":4,
	"margin" : 3, # 要跟screens的gap联合使用，把屏幕外边距加大，要不然窗口之间间距一叠加就是双倍，而屏幕四周还是单倍
	"grow_amount": 5, # 调整窗口宽高时，一次移动多少
}
# 布局
layouts = [
	layout.Columns(
        **layout_setting,
        border_on_single=colors["border"],
        border_focus_stack=colors["border"],
        border_normal_stack=colors["border"],
        fair=True,
	),
	#layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    #layout.Bsp(),
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
    font='JetBrains Mono',
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
    Click([mod], "Button2", lazy.window.toggle_floating()),
]
  
dgroups_key_binder = None
dgroups_app_rules = []  # type: List

# 以下配置很重要（对于uTools、QQ来说）
# 作用：当窗口显示，把这个窗口移动到当前焦点所在的窗口中。
# 再定义一个窗口规则，当打开这个窗口，将其移动到指定工作区，
# 并把屏幕切换到该工作区
# 格式 窗口的WM_CLASS : 工作区号
specify_group={
'Clash for Windows':'6', 
'星火应用商店':'6', 
'Motrix': '6'
	}
@hook.subscribe.client_new
def client_new(w):
	# if w.name in appArray:
		# w.togroup(qtile.current_group.name) # qtile识别当前组是看（真实）鼠标在哪个组
	# send_notification("qtile", f"{w}")  # 除了导入包，还需要安装显示通知的软件sudo apt install dunst
	for app in specify_group.keys():
		if app in w.name:
			group = specify_group[app]
			qtile.current_screen.toggle_group(group)
			w.togroup(group)
			return
	w.togroup(qtile.current_group.name)
	# 所有的软件只要一打开就挪到当前组

# @hook.subscribe.focus_change
# def focus_change():
	# #send_notification("qtile", f"现在组:{qtile.current_group.name}, 先前组{qtile.current_screen.previous_group.name},{qtile.current_window is None}")
	# if qtile.current_window is None and qtile.current_group.name == '6':
	#	qtile.current_screen.toggle_group()
	
# 鼠标是否跟随焦点，屏幕上没窗口，焦点跑到上一个操作的组中的窗口中，然后（虚假的）鼠标就挪到屏幕中间。
cursor_warp = False

# 当悬浮的窗口获得焦点，自动挪到最前面
@hook.subscribe.client_focus
def bringWindowFront(w):
	# 如果是悬浮窗口
	if w.floating:
		w.bring_to_front()

# 焦点是否跟随鼠标
follow_mouse_focus = False


# 当窗口需要焦点，自动获得焦点
focus_on_window_activation = "smart"

#bring_front_click = False
bring_front_click = "floating_only"
# 点击窗口移动到最前面（覆盖）= 仅限浮动窗口。

# 自动设为浮动窗口
floating_layout = layout.Floating(
	**layout_setting,
	float_rules=[
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
		# Match(wm_class="org.jackhuang.hmcl.Launcher"),
		# Match(wm_class="xfce4-terminal"),
		# Match(wm_class="QQ"),
		# Match(wm_class="spark-store"),
		# Match(wm_class="Nemo"),
		Match(wm_class="timeshift-gtk"),
		# Match(wm_class="VirtualBox Manager"),
		# Match(wm_class="xmcl"),
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
