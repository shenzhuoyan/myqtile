#!/bin/bash
if [[ $(pgrep picom) ]]; then # 判断是否已运行，已经运行就杀掉重新运行
		killall picom
		# 下面这一行后面加#号会导致不执行
		exec "$HOME/.config/autostart/start_picom.sh" &
	fi
