#!/bin/bash

sudo apt install -y pip git
# 配置国内镜像
pip config set global.index-url https://repo.nju.edu.cn/repository/pypi/simple

# Debian12 为了避免pip影响系统禁止了一些操作，咱们来解开
pip config set global.break-system-packages true

# 安装依赖
pip install --no-cache --upgrade --no-build-isolation xcffib
pip install --no-cache --upgrade --no-build-isolation cairocffi

git clone https://github.com/qtile/qtile.git
cd qtile
# 安装qtile
pip install --no-cache --upgrade --no-build-isolation .

cat > ./temp << "EOF"
[Desktop Entry]
Name=Qtile
Comment=Qtile Session
Type=Application
Keywords=wm;tiling
EOF
sudo cp ./temp /usr/share/xsessions/qtile.desktop;rm ./temp
u=$USER
sudo echo "Exec=/home/$u/.local/bin/qtile start" | sudo tee -a /usr/share/xsessions/qtile.desktop
echo "qtile installed"

