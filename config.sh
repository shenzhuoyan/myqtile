#!/bin/bash

# 复制配置文件
cp -r config/picom ~/.config/
cp -r config/qtile ~/.config/
cp -r config/rofi ~/.local/share/
cp -r config/Pictures ~/
cp -r config/.Xresources ~/
cp -r config/autostart ~/.config/

# 安装top bar的字体
mkdir -p ~/.local/share/fonts
wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.0/JetBrainsMono.zip
unzip JetBrainsMono.zip -d $HOME/.local/share/fonts/JetBrainsMono
fc-cache

# top bar的更新查看器要用
sudo apt install -y apt-show-versions

echo "configure complete"




