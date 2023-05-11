from libqtile.config import (
    # KeyChord,
    # Key,
    Screen,
    # Group,
    # Drag,
    # Click,
    # ScratchPad,
    # DropDown,
    # Match,
)
from libqtile.command import lazy
from libqtile import bar, widget  # , hook, layout
import os
# from libqtile.lazy import lazy
from libqtile import qtile

# 用来获取家目录
import pathlib

# 获取自定义的颜色列表
from colors import colors

homedir = str(pathlib.Path.home())

conf_path = {
	"wallpaper":"~/Pictures/qtile/悬崖上的金鱼姬.jpeg",
	"power_menu": homedir+"/.config/qtile/rofi/powermenu.sh"
}

def open_pavu():
    qtile.cmd_spawn("pavucontrol")


group_box_settings = {
    "padding": 3,
    "borderwidth": 4,
    "active": colors["white"],
    "inactive": colors["grey"],
    "disable_drag": True,
    "rounded": True,
    "highlight_color": colors["background_lighter"],
    "block_highlight_text_color": colors["cyan"],
    "highlight_method": "block",
    "this_current_screen_border": colors["background"],
    "this_screen_border": colors["magenta"],
    "other_current_screen_border": colors["background"],
    "other_screen_border": colors["background"],
    "foreground": colors["foregound"],
    "background": colors["background"],
    "urgent_border": colors["red"],
    "fontsize": 25,
}

icon_size = 25
text_size_color = {
	"background": colors["background"],
    "foreground": colors["foregound"],
	"fontsize": 25,
}

# bar上个个组件之间的间隔
sep = widget.Sep(
        linewidth=0,
        background=colors["background"],
        padding=30,
        size_percent=40,
    )

# 由于默认硬盘容量类没有办法展示“已用空间”
# 所以用一个子类来重写该类的方法来实现
# 说个趣事，我一开始以为//后面是注释，我想这注释写的也不对啊就删了，
# 然后发现怎么我添加的ud这个参数没有自动/1024/1024/1024呢，
# 然后就看了半天源代码，一层一层网上找，觉得可能在哪个父类里实现的
# 怎么找也找不到相关代码，就搜measure用在哪儿来，才发现原来//不是注释，是除号。
# //是向下取整的除法
class CustomDF(widget.DF):
	def poll(self):
		statvfs = os.statvfs(self.partition)
		size = statvfs.f_frsize * statvfs.f_blocks // self.calc
		free = statvfs.f_frsize * statvfs.f_bfree // self.calc
		self.user_free = statvfs.f_frsize * statvfs.f_bavail // self.calc

		if self.visible_on_warn and self.user_free >= self.warn_space:
			text = ""
		else:
			text = self.format.format(
				p=self.partition,
				s=size,
				f=free,
				uf=self.user_free,
				m=self.measure,
				ud=size - free,
				r=(size - self.user_free) / size * 100,
			)

		return text

# 自定义硬盘类的实例化
newDF=CustomDF(
	**text_size_color,
	visible_on_warn=False,
	format='{ud:.0f}{m} {r:.0f}%', # 已用空间和所占百分比。但是无法展示已用容量
	measure='G',
	#partition='/', # 指定需要显示的硬盘分区，默认根目录
)
screens = [
    Screen(
        wallpaper=conf_path["wallpaper"],
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                # 分割条
                sep,
                # config.py里设置的6个任务区
                widget.GroupBox(
					**group_box_settings,
                ),
                sep,
                # 窗口标题
                widget.WindowName(
                    **text_size_color,
                    #format='{name}', # class是只显示class名，但这个class不一定是软件名
                    width=bar.CALCULATED,
                    for_current_screen=True,
                    empty_group_string='Desktop',
                    #max_chars=40, # 标题能展示的最大长度
                ),
                # 撑开bar, 把后面的组件挤到最右边
                widget.Spacer(background=colors["background"]),
                sep,
                # 系统托盘，就是windows的右下角托盘
                widget.Systray(
					background=colors["background"],
                    icon_size=icon_size,
                    padding=20,
                ),
                sep,
                # 更新
                # 图标
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["green"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                    
                ),
                # 检查更新组件
                widget.CheckUpdates(
                    **text_size_color,
                    distro='Debian',# 根据官网提示使用apt安装他需要的软件
                    no_update_string='No updates',
                    
                ),
                
                sep,
                # CPU
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["blue"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                ),
                widget.CPU(
                    **text_size_color,
                    format="{freq_current:3.1f}Ghz {load_percent:2.0f}%",
                ),
                widget.ThermalSensor(
					**text_size_color,
                    format=' {temp:.0f}{unit}',
                    tag_sensor='Tctl', #  在终端输入sensors 查看传感器
                ),
                sep,
                # 内存
                widget.TextBox(
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    background=colors["background"],
                    foreground=colors["green"],
                    fontsize=icon_size,
                ),
                widget.Memory(
                    **text_size_color,
                    format="{MemUsed:4.1f}G {MemPercent:2.0f}%",
                    measure_mem='G',
                    update_interval=1,
                ),
                sep,
                # 硬盘
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["super_blue"],
                    text="󰋊 ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                ),
                newDF,
                sep,
                # 音量
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["orange"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                ),
                widget.Volume(
                    **text_size_color,
                    limit_max_volume="True",
                    update_interval=0.1,
                    fmt='{:4}',
                    mouse_callbacks={"Button3": open_pavu},
                ),
                
                sep,
                # 日期时间
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["super_cyan"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                ),
                
                widget.Clock(
                    **text_size_color,
                    format="%F %A",
                ),
                sep,
                # 电源
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["red"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                    mouse_callbacks={"Button1": lazy.spawn(conf_path["power_menu"])}
                ),
                sep,
            ],
            50,
            margin=[0, 0, 5, 0],
        ),
        bottom=bar.Gap(5),
        left=bar.Gap(5),
        right=bar.Gap(5),
    ),
]
