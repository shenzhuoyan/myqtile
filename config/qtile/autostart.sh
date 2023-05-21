#!/bin/bash

#randr
#setxkbmap -option "ctrl:swapcaps"

# 自动启动一些命令，分别是
# nm-applet bar上的网络管理器
# fcitx5 输入法
# blueman-applet bar上的蓝牙管理器
# polkit-mate-authentication-agent-1 当GUI程序需要提升权限时，用它才会弹出提权的窗口
cmds=("nm-applet"
		"fcitx5"
		#"blueman-applet"
		"/usr/lib/x86_64-linux-gnu/polkit-mate/polkit-mate-authentication-agent-1"
		"utools"
		#"kdeconnect-indicator"
		"qq"
		"xfce4-power-manager"
		"/opt/apps/com.github.clash-for-windows/files/cfw"
)
 
# 注意命令里不能带空格，否则请使用脚本
scripts=(`ls $HOME/.config/autostart/*.sh`)

# .desktop文件，一般是从/usr/share/applications/里复制过来的软件的“快捷方式”
# 注意，这里并不是执行的这里的.desktop, 而是/usr/share/applications里的原来的文件
# 因为gtk-launch只认那里面的desktop
desktops=(`ls $HOME/.config/autostart/*.desktop`)

# 自动启动一些软件的脚本在~/.config/autostart，分别是
# picom 实现桌面的动画效果、透明效果等
# syncthing 局域网数据同步
#all=(${cmds[@]}  ${scripts[@]}) # 脚本需要在前面加上路径名，所以与命令合在一起不便区分
# 有些命令写在脚本里是因为下面这个判断是否运行的命令里不能出现空格，所以带参数的命令都写在脚本里了
# 优点是可以不修改这个脚本，直接在autostart目录下创建脚本即可

for value in ${cmds[@]}; do
	if [[ ! $(pgrep ${value}) ]]; then # 判断是否已运行，已经运行的就不重复运行了
		# 下面这一行后面加#号会导致不执行
		exec "$value" &
	fi
done

# 执行那些启动脚本
for value in ${scripts[@]}; do
	exec "$value" &
done

# 执行那些.desktop文件
for value in ${desktops[@]}; do
	gtk-launch "${value##*/}" &
done

#if [[ ! $(pgrep xob) ]]; then # xob是一个进度条
#	exec "sxob"
#fi
