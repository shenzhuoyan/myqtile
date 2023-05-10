#!/bin/bash
. ~/.profile

# CMDs
uptime="$(uptime -p | sed -e 's/up //g')"

# Options
shutdown=' '
reboot=' '
suspend=' '
hibernate=' '
logout='󰍃 '

# Rofi CMD
rofi_cmd() {
	rofi -dmenu \
		-p "Goodbye ${USER}" \
		-mesg "Uptime: $uptime" \
		-theme powermenu
}

# Pass variables to rofi dmenu
run_rofi() {
	echo -e "$suspend\n$hibernate\n$logout\n$reboot\n$shutdown" | rofi_cmd
}

# Actions
chosen="$(run_rofi)"
case ${chosen} in
"$shutdown")
	systemctl poweroff
	;;
"$reboot")
	systemctl reboot
	;;
"$hibernate")
	systemctl hibernate
	;;
"$suspend")
	systemctl suspend
	;;
"$logout")
	qtile cmd-obj -o cmd -f shutdown
	;;
esac
