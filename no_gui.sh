#!/bin/bash

# 必要的显示环境
sudo apt install -y xserver-xorg xinit 

# 网络管理器，可以在系统托盘上直接管理网络
sudo apt install -y network-manager-gnome

sudo apt install -y psutil lxappearance

# 安装xfce4终端
sudo apt install -y xfce4-terminal
# 文件管理器，因为xfce4的thunar不能访问samba服务，所以就用这个了
sudo apt install -y nemo

# 为了在nemo中正确调用终端，还必须用gsettings设置
sudo apt-get install -y libglib2.0-dev
# 为了使用gsettings ，还必须安装 libglib2.0-dev
gsettings set org.cinnamon.desktop.default-applications.terminal exec xfce4-terminal

sudo apt install -y dialog mtools dosfstools avahi-daemon acpi acpid gvfs-backends xfce4-power-manager

sudo systemctl enable avahi-daemon

sudo systemctl enable acpid

# 音频插件
sudo apt install -y pulseaudio alsa-utils pavucontrol volumeicon-alsa

sudo apt install -y neofetch
sudo apt install -y cups

# 蓝牙管理器
sudo apt install -y bluez blueman

sudo systemctl enable cups

# 火狐浏览器
sudo apt install -y firefox-esr

sudo apt install -y picom dunst sxhkd rofi suckless-tools libnotify-bin unzip scrot geany geany-plugin-treebrowser

# 一些字体
sudo apt install -y fonts-font-awesome fonts-ubuntu fonts-liberation2 fonts-liberation fonts-terminus font-manager fonts-wqy-zenhei

xdg-user-dirs-update

sudo apt install lightdm -y

sudo systemctl enable lightdm

echo "ok"
