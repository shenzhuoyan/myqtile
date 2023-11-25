#!/bin/bash

sudo apt install -y rofi
sudo apt install -y flameshot
sudo apt install mate-polkit
# 复制配置文件
cp -r config/picom ~/.config/
cp -r config/qtile ~/.config/
cp -r config/rofi ~/.local/share/
cp -r config/Pictures ~/
cp -r config/.Xresources ~/
cp -r config/autostart ~/.config/

# 不用这个字体了。
# # 安装top bar的字体。
# if [ ! -d ~/.local/share/fonts/JetBrainsMono ]; then
# 	mkdir -p ~/.local/share/fonts
# 	wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.0/JetBrainsMono.zip
# 	unzip JetBrainsMono.zip -d $HOME/.local/share/fonts/JetBrainsMono
# 	fc-cache
# 	rm -rf JetBrain*
# fi

# top bar的更新查看器要用
# sudo apt install -y apt-show-versions

# top bar的性能监控插件要用
pip install pyxdg
pip install psutil
# 这个是wifi插件用的，但我安装失败
#pip install iwlib
# 蓝牙插件用
# pip install dbus-next
# sudo apt install d-feet
# 执行d-feet可以查看蓝牙设备的地址

echo "configure complete"



