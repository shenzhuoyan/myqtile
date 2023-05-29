from libqtile.config import (
    # KeyChord,
    # Key,
    Screen,
    Group,
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


#group_box_settings = {
#    "padding": 3,
#   "borderwidth": 4,
#    "active": colors["cyan"],
 #   "inactive": colors["grey"],
 #   "disable_drag": True,
 #   "rounded": True,
 #   "highlight_color": colors["background_lighter"],
#    "block_highlight_text_color": colors["white"],
#    "highlight_method": "block",
#    "this_current_screen_border": colors["background"],
#    "this_screen_border": colors["magenta"],
#    "other_current_screen_border": colors["background"],
#    "other_screen_border": colors["background"],
#    "foreground": colors["foregound"],
#    "background": colors["background"],
#    "urgent_border": colors["red"],
#    "fontsize": 25,
#    "font":"JetBrainsMono Nerd Font",
#}

icon_size = 32
font_size = 28
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


# top bar上展示软件的名字
def getAppName(text):
	names=qtile.current_window.get_wm_class()
	if len(names) > 1:
		return names[1]
	else: return names[0]

angle_font_size={
	"font":"MesloLGS NF Regular",
	"fontsize":32,
	"padding":0
}

screens = [
    Screen(
        wallpaper=conf_path["wallpaper"],
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                # 分割条
                widget.Sep(
					background=colors["background"],
					padding=10,
					linewidth=0,
                ),
                # config.py里设置的6个任务区
                widget.GroupBox(
					active= colors["white"], # 有窗口的组的颜色
					inactive= colors["magenta"], # 无窗口的组的颜色
					background= colors["background"], # 整体背景颜色
					highlight_method= "block", # 选中组背景是个块
					this_current_screen_border= colors["color4"], # 选中组的边框颜色（此时边框是个块）
					block_highlight_text_color= colors["white"], # 选中的组的颜色
					toggle=False,# 点本组跳到上一组，关掉
					font="JetBrainsMono Nerd Font Mono Bold",
					disable_drag=True, # 禁止拖动组名
					#fontsize=font_size,
                ),
                widget.TextBox(
                    background=colors["blue"],
                    foreground=colors["background"],
                    text="",
                    **angle_font_size,
                ),
                
                # 窗口标题
                widget.WindowName(
                    fontsize=font_size,
                    background=colors["blue"],
                    foreground=colors["black"],
                    #format='{name}', # class是只显示class名，但这个class不一定是软件名
                    for_current_screen=True,
                    empty_group_string='Desktop',
                    #max_chars=100, # 标题能展示的最大长度
                    parse_text=getAppName,
                    width=bar.CALCULATED,
                    fmt=' {}'
                ),
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["blue"],
                    text="",
                    **angle_font_size,
                ),
                # widget.Prompt(
				# 	fontsize=font_size,
				# 	ignore_dups_history=True,# 历史记录中不存储重复项
                # ),
                
                # 撑开bar, 把后面的组件挤到最右边
                widget.Spacer(background=colors["background"]),
                # 箭头
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["grey"],
                    text="",
                    **angle_font_size,
                    
                ),
                # 系统托盘，就是windows的右下角托盘
                widget.Systray(
					background=colors["grey"],
                    icon_size=32,
                    padding=15,
                ),
                widget.Sep(
					background=colors["grey"],
					padding=15,
					linewidth=0,
                ),
				# 箭头
                widget.TextBox(
                    background=colors["grey"],
                    foreground=colors["blue"],
                    text="",
                   **angle_font_size,
                    
                ),
                # 更新
                # 图标
                widget.TextBox(
                    background=colors["blue"],
                    foreground=colors["black"],
                    text="",
                    font="MesloLGS NF Regular",
                    fontsize=icon_size,
                    
                ),
                # 检查更新组件
                widget.CheckUpdates(
                    fontsize=font_size,
                    colour_have_updates=colors["black"],
                    colour_no_updates=colors["black"],
                    background=colors["blue"],
                    distro='Debian',# 根据官网提示使用apt安装他需要的软件
                    no_update_string='No updates',
                    
                ),
                widget.Sep(
					background=colors["blue"],
					padding=5,
					linewidth=0,
                ),
				# 箭头
                widget.TextBox(
                    background=colors["blue"],
                    foreground=colors["yellow"],
                    text="",
                    **angle_font_size,
                    
                ),
                # CPU
                widget.TextBox(
                    background=colors["yellow"],
                    foreground=colors["black"],
                    text="",
                    font="JetBrainsMono Nerd Font Mono",
                    fontsize=icon_size+8,
                ),
                widget.CPU(
                    fontsize=font_size,
                    background=colors["yellow"],
                    foreground=colors["black"],
                    format="{freq_current:1.1f}Ghz{load_percent:3.0f}%",
                ),
                widget.ThermalSensor(
					fontsize=font_size,
					background=colors["yellow"],
                    foreground=colors["black"],
                    format=' {temp:.0f}{unit}',
                    tag_sensor='Tctl', #  在终端输入sensors 查看传感器
                ),
                widget.Sep(
					background=colors["yellow"],
					padding=5,
					linewidth=0,
                ),
				# 箭头
                widget.TextBox(
                    background=colors["yellow"],
                    foreground=colors["green"],
                    text="",
                    **angle_font_size,
                    
                ),
                # 内存
                widget.TextBox(
                    text="",
                    font="MesloLGS NF Regular",
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
					background=colors["green"],
					padding=5,
					linewidth=0,
                ),
				# 箭头
                widget.TextBox(
                    background=colors["green"],
                    foreground=colors["color2"],
                    text="",
                    **angle_font_size,
                    
                ),
                # 硬盘
                widget.TextBox(
                    background=colors["color2"],
                    foreground=colors["black"],
                    text="󰋊",
                    font="MesloLGS NF Regular",
                    fontsize=icon_size,
                ),
                CustomDF(
					fontsize=font_size,
					visible_on_warn=False,
					format='{ud:.0f}{m} {r:.0f}%', # 已用空间和所占百分比。但是无法展示已用容量
					measure='G',
					#partition='/', # 指定需要显示的硬盘分区，默认根目录
					background=colors["color2"],
					foreground=colors["black"],
				),
                widget.Sep(
					background=colors["color2"],
					padding=5,
					linewidth=0,
                ),
				# 箭头
                widget.TextBox(
                    background=colors["color2"],
                    foreground=colors["color3"],
                    text="",
                    **angle_font_size,
                ),
                # 音量
                widget.TextBox(
                    background=colors["color3"],
                    foreground=colors["black"],
                    text="󰕾",
                    font="MesloLGS NF Regular",
                    fontsize=icon_size,
                ),
                widget.Volume(
                    fontsize=font_size,
                    background=colors["color3"],
                    foreground=colors["black"],
                    limit_max_volume="True",
                    update_interval=0.1,
                    fmt='{:4}',
                    mouse_callbacks={"Button3": open_pavu},
                ),
                widget.Sep(
					background=colors["color3"],
					padding=5,
					linewidth=0,
                ),
				# 箭头
                widget.TextBox(
                    background=colors["color3"],
                    foreground=colors["white"],
                    text="",
                    **angle_font_size,
                ),
                # Bluetooth
                widget.TextBox(
                    background=colors["white"],
                    foreground=colors["black"],
                    text="",
                    font="MesloLGS NF Regular",
                    fontsize=icon_size,
                ),
                widget.Bluetooth(
					fontsize=font_size,
					background=colors["white"],
                    mouse_callbacks={"Button1": lazy.spawn("blueman-manager")},
                    hci='/dev_C2_8A_A3_A4_26_A8',
                    foreground=colors["black"],
                ),
                widget.Sep(
					background=colors["white"],
					padding=5,
					linewidth=0,
                ),
				# 箭头
                widget.TextBox(
                    background=colors["white"],
                    foreground=colors["cyan"],
                    text="",
                    **angle_font_size,
                    
                ),
                # 日期时间
                widget.TextBox(
                    background=colors["cyan"],
                    foreground=colors["black"],
                    text="",
                    font="MesloLGS NF Regular",
                    fontsize=icon_size,
                ),
                
                widget.Clock(
                    fontsize=font_size,
                    format="%B %e日 %A %H:%M",
                    background=colors["cyan"],
                    foreground=colors["black"],
                ),
                widget.Sep(
					background=colors["cyan"],
					padding=5,
					linewidth=0,
                ),
				# 箭头
                widget.TextBox(
                    background=colors["cyan"],
                    foreground=colors["background"],
                    text="",
                    **angle_font_size,
                    
                ),
                # 电源
                widget.TextBox(
                    background=colors["background"],
                    foreground=colors["red"],
                    text="",
                    font="MesloLGS NF Regular",
                    fontsize=icon_size,
                    mouse_callbacks={"Button1": lazy.spawn(conf_path["power_menu"])}
                ),
                widget.Sep(
					background=colors["background"],
					padding=10,
					linewidth=0,
                ),
            ],
            40,
            margin=[0, 0, 6, 0],
        ),
        # 设置内部间隙，也就是各个窗口之间的间隙
        bottom=bar.Gap(6),
        left=bar.Gap(6),
        right=bar.Gap(6),
    ),
]
