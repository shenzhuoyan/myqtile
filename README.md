# Debian12 安装 qtile 教程

## 下载仓库

- 下载git仓库

  ```shell
  sudo apt update
  sudo apt install -y git
  git clone https://github.com/shenzhuoyan/myqtile.git
  cd myqtile
  ```

- 如果你**已经安装qtile**, 直接跳到 "**配置qtile**" 这一节

## Debian12的安装与配置

- 我安装系统时**选择不安装桌面环境**，只安装必要的系统工具，如果你**已经安装**好了**桌面环境**，直接跳到下一节 "**安装qtile**"

- 对于没有安装桌面环境的用户，执行

  ```shell
  ./no_gui.sh
  ```

## 安装qtile

- 执行

  ```shell
  ./install.sh
  ```

- 根据CPU品牌安装对应的微码

  ```shell
  sudo apt install -y amd64-microcode
  sudo apt install -y intel-microcode
  ```

- 然后重启，没有桌面环境的可以通过以下命令重启

  ```shell
  systemctl reboot
  ```

- 重启之后应该就可以看到一个登录窗口了，点击右上角的按钮**选择qtile**，然后输入用户名和密码登录

## 配置qtile

- qtile的默认快捷键

  - `Win + R` 可以在bar上输入名字来打开软件，tab可以补全
  - `Win + Enter` 打开终端
  - `Win + W` 关闭当前窗口

- 执行配置脚本

  ```shell
  cd myqtile
  ./config.sh
  ```

- 按`Win + Ctrl + R` 重新加载配置即可看到最终效果

## 配置路径

- `~/.config/qtile` 下面保存的是qtile的配置
- `~/Pictures/qtile/悬崖上的金鱼姬.jpeg` 是壁纸，可以在qtile的配置文件里修改
- `~/.config/picom/picom.conf`，picom是负责动画、阴影这些的
- `~/.config/autostart` 下存放开机自启动**脚本**
- `~/.config/qtile/autostart.sh` 里是简单的自启动命令

## 接管网络

- 对于一开始没有安装GUI的用户，由于安装的gnome-networkmanager需要接管系统的网络管理，所以需要修改以下设置

  ```shell
  sudo nano /etc/network/interfaces
  
  # 把allow-....往后都注释掉
  
  sudo systemctl restart NetworkManager
  ```

## 常用快捷键

- `Win + E` 打开文件管理器
- `Win + Ctrl + R` 重新加载qtile配置
- `Win + Shift + S` 选区截图
- `Print` 截屏
- `Ctrl + Alt + T` 打开终端
- `Win + Q` 关闭当前软件
- `Win + A` 浏览、搜索软件

 ## 其他

- uTools会与Steam冲突，我选择卸载Steam
- Fcitx输入法等软件自行安装
- Top栏的CPU部分最后一个是温度传感器，由于每个机器的传感器tag不一样，所以需要执行`sensors` 来检测自己的传感器tag
- uTools的Linux搜索文件的插件 https://github.com/shenzhuoyan/utools_linux_find
- 屏幕缩放，修改`~/.Xresources` 的`Xft.dpi`的值，建议是96的倍数，比如缩放1.5倍就是`144`, 执行`xrdb -merge ~/.Xresources` 生效

## 参考

- https://github.com/drewgrif/qtile-debian
- https://github.com/ayamir/dotfiles/tree/master/nord
- https://github.com/Fr4nk1in-USTC/dotfiles