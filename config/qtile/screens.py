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
from libqtile import bar, widget, hook #, layout
import os
# from libqtile.lazy import lazy
from libqtile import qtile

# 获取自定义的颜色列表
from colors import colors


conf_path = {
	"wallpaper":"~/Pictures/qtile/悬崖上的金鱼姬.jpeg",
	"power_menu": os.path.expanduser("~/.config/qtile/rofi/powermenu.sh") # 将~替换为/home/username/
}

def open_pavu():
    qtile.cmd_spawn("pavucontrol")


group_box_settings = {
    "padding": 3,
    "borderwidth": 4,
    "active": colors["cyan"],
    "inactive": colors["grey"],
    "disable_drag": True,
    "rounded": True,
    "highlight_color": colors["background_lighter"],
    "block_highlight_text_color": colors["white"],
    "highlight_method": "block",
    "this_current_screen_border": colors["background"],
    "this_screen_border": colors["magenta"],
    "other_current_screen_border": colors["background"],
    "other_screen_border": colors["background"],
    "foreground": colors["foregound"],
    "background": colors["background"],
    "urgent_border": colors["red"],
    "fontsize": 25,
    "font":"JetBrainsMono Nerd Font",
}

icon_size = 30
font_size = 25

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
	fontsize=font_size,
	visible_on_warn=False,
	format='{ud:.0f}{m} {r:.0f}%', # 已用空间和所占百分比。但是无法展示已用容量
	measure='G',
	#partition='/', # 指定需要显示的硬盘分区，默认根目录
	background=colors["color1"],
	foreground=colors["black"],
)
# top bar上展示软件的名字
def getAppName(text):
	names=qtile.current_window.get_wm_class()
	if len(names) > 1:
		return names[1]
	else: return names[0]

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
                    fontsize=font_size,
                    background=colors["background"],
                    foreground=colors["foregound"],
                    #format='{name}', # class是只显示class名，但这个class不一定是软件名
                    for_current_screen=True,
                    empty_group_string='Desktop',
                    #max_chars=100, # 标题能展示的最大长度
                    parse_text=getAppName,
                ),
                # sep,
                # widget.Prompt(
				# 	fontsize=font_size,
				# 	ignore_dups_history=True,# 历史记录中不存储重复项
                # ),
                sep,
                
                # 撑开bar, 把后面的组件挤到最右边
                widget.Spacer(background=colors["background"]),
                
                # 系统托盘，就是windows的右下角托盘
                widget.Systray(
					background=colors["background"],
					#background=colors["green"],
                    icon_size=25,
                    padding=30,
                ),
                widget.Sep(
					linewidth=0,
					background=colors["background"],
					padding=20,
					size_percent=40,
				),
				# 箭头
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["grey"],
                    text="",
                    font="JetBrainsMono Nerd Font",
                    fontsize=35,
                    padding=-1,
                    
                ),
                # 更新
                # 图标
                widget.TextBox(
                    background=colors["grey"],
                    foreground=colors["black"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                    
                ),
                # 检查更新组件
                widget.CheckUpdates(
                    fontsize=font_size,
                    colour_no_updates=colors["black"],
                    background=colors["grey"],
                    distro='Debian',# 根据官网提示使用apt安装他需要的软件
                    no_update_string='No updates',
                    
                ),
                
                widget.Sep(
					linewidth=0,
					background=colors["grey"],
					padding=10,
					size_percent=40,
				),
				# 箭头
                widget.TextBox(
                    background=colors["grey"],
                    foreground=colors["magenta"],
                    text="",
                    font="JetBrainsMono Nerd Font",
                    fontsize=35,
                    padding=-1,
                    
                ),
                # CPU
                widget.TextBox(
                    background=colors["magenta"],
                    foreground=colors["black"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                ),
                widget.CPU(
                    fontsize=font_size,
                    background=colors["magenta"],
                    foreground=colors["black"],
                    format="{freq_current:3.1f}Ghz {load_percent:2.0f}%",
                ),
                widget.ThermalSensor(
					fontsize=font_size,
					background=colors["magenta"],
                    foreground=colors["black"],
                    format=' {temp:.0f}{unit}',
                    tag_sensor='Tctl', #  在终端输入sensors 查看传感器
                ),
                widget.Sep(
					linewidth=0,
					background=colors["magenta"],
					padding=10,
					size_percent=40,
				),
				# 箭头
                widget.TextBox(
                    background=colors["magenta"],
                    foreground=colors["green"],
                    text="",
                    font="JetBrainsMono Nerd Font",
                    fontsize=35,
                    padding=-1,
                    
                ),
                # 内存
                widget.TextBox(
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    background=colors["green"],
                    foreground=colors["black"],
                    fontsize=icon_size,
                ),
                widget.Memory(
                    fontsize=font_size,
                    background=colors["green"],
                    foreground=colors["black"],
                    format="{MemUsed:4.1f}G {MemPercent:2.0f}%",
                    measure_mem='G',
                    update_interval=1,
                ),
                widget.Sep(
					linewidth=0,
					background=colors["green"],
					padding=10,
					size_percent=40,
				),
				# 箭头
                widget.TextBox(
                    background=colors["green"],
                    foreground=colors["color1"],
                    text="",
                    font="JetBrainsMono Nerd Font",
                    fontsize=35,
                    padding=-1,
                    
                ),
                # 硬盘
                widget.TextBox(
                    background=colors["color1"],
                    foreground=colors["black"],
                    text="󰋊 ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                ),
                newDF,
                widget.Sep(
					linewidth=0,
					background=colors["color1"],
					padding=10,
					size_percent=40,
				),
				# 箭头
                widget.TextBox(
                    background=colors["color1"],
                    foreground=colors["color2"],
                    text="",
                    font="JetBrainsMono Nerd Font",
                    fontsize=35,
                    padding=-1,
                    
                ),
                # 音量
                widget.TextBox(
                    background=colors["color2"],
                    foreground=colors["black"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                ),
                widget.Volume(
                    fontsize=font_size,
                    background=colors["color2"],
                    foreground=colors["black"],
                    limit_max_volume="True",
                    update_interval=0.1,
                    fmt='{:4}',
                    mouse_callbacks={"Button3": open_pavu},
                ),
                widget.Sep(
					linewidth=0,
					background=colors["color2"],
					padding=10,
					size_percent=40,
				),
				# 箭头
                widget.TextBox(
                    background=colors["color2"],
                    foreground=colors["color3"],
                    text="",
                    font="JetBrainsMono Nerd Font",
                    fontsize=35,
                    padding=-1,
                    
                ),
                # Bluetooth
                widget.TextBox(
                    background=colors["color3"],
                    foreground=colors["black"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                ),
                widget.Bluetooth(
					fontsize=font_size,
					background=colors["color3"],
                    mouse_callbacks={"Button1": lazy.spawn("blueman-manager")},
                    hci='/dev_F1_AB_EF_40_85_45',
                    foreground=colors["black"],
                ),
                widget.Sep(
					linewidth=0,
					background=colors["color3"],
					padding=10,
					size_percent=40,
				),
				# 箭头
                widget.TextBox(
                    background=colors["color3"],
                    foreground=colors["color4"],
                    text="",
                    font="JetBrainsMono Nerd Font",
                    fontsize=35,
                    padding=-1,
                    
                ),
                # 日期时间
                widget.TextBox(
                    background=colors["color4"],
                    foreground=colors["black"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                ),
                
                widget.Clock(
                    fontsize=font_size,
                    format="%B %e日 %A %H:%M",
                    background=colors["color4"],
                    foreground=colors["black"],
                ),
                widget.Sep(
					linewidth=0,
					background=colors["color4"],
					padding=10,
					size_percent=40,
				),
				# 箭头
                widget.TextBox(
                    background=colors["color4"],
                    foreground=colors["background"],
                    text="",
                    font="JetBrainsMono Nerd Font",
                    fontsize=35,
                    padding=-1,
                    
                ),
                # 电源
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["red"],
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=icon_size,
                    mouse_callbacks={"Button1": lazy.spawn(conf_path["power_menu"])}
                ),
            ],
            40,
            margin=[0, 0, 5, 0],
        ),
        bottom=bar.Gap(5),
        left=bar.Gap(5),
        right=bar.Gap(5),
    ),
]
