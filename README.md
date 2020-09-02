# SEU AutoEnter

[![license](https://img.shields.io/github/license/amomorning/seu-autoenter)](https://github.com/amomorning/seu-autoenter/blob/master/LICENSE)
[![Release Version](https://img.shields.io/github/release/amomorning/seu-autoenter)](https://github.com/amomorning/seu-autoenter/releases)


东南大学每日报平安健康打卡及入校申请自动化程序  

登录程序主体来自 [StephenHoo/AutoLogin](https://github.com/StephenHoo/AutoLogin)

## Usage
在[Releases](https://github.com/amomorning/seu-autoenter/releases)中发布了无需配置环境的程序包
### Download
- 每日报平安和申请入校整合在一个文件 AutoEnter.zip 中，可从最外层的README.md文件查看操作说明

### AutoEnter
1. 确认Chrome已升级到最新，否则应下载对应版本的 [ChromeDriver](https://chromedriver.chromium.org/downloads) 并替换 
2. 在`config.json`中填入一卡通号(username)、密码(password)，是否申请入校(enter)填`true`或`false`
3. 每日申请入校所填资料中所到的地址(address)为必填项，手机号码(tel)为可选项，如果你平时就无需填写直接留空即可。
4. 第一次使用双击`AutoEnter.exe`以便确认是否能成功打卡，网络正常情况下，约30秒出现**打卡成功**，约2分钟出现**申请成功**
5. 双击`AutoEnter.vbs`可无窗口自动运行，从任务管理器可以看到`AutoEnter.exe`在后台运行, 如不关机下次打卡时间为`hh>10?7:hh`时`mm`分.
6. `AutoEnter.vbs`创建快捷方式并复制到开机启动项中, 那么开机自动打卡(不能使用Windows睡眠)
7. 第一次成功打卡后产生日志文件`log.txt`



## Requirements
自行编译运行需要以下环境
- python3
- selenium
- chrome (Version 85.0.4183.83)
- pyinstaller (用于导出exe)

``` bash
conda create -n selenium
conda activate selenium
conda install -c conda-forge selenium

# 每日打卡
python login_chrome.py

# 申请入校
python enter_chrome.py

# 每日打卡并申请入校
python AutoEnter.py
```

## FAQ
#### Q: 为什么需要这个程序?
A: 经常在中午12点超出一丢丢的时候意识到妹油申请入校 TAT 原先可以手动调本地时间避开申请时间限制，但是似乎在某此更新里学校修复了这个bug....
#### Q: 如果学校申请入校填写内容有更新怎么办?
A: 会无法成功打卡或申请入校，你可以自己编译这个 repo 的代码或者联系 amomorning@gmail.com 修改。
#### Q: 程序如何确定申请入校的时间段? 
A: 在四牌楼入校可申请的最大时间段为8:31 - 21:59，程序中固定使用了这一时间。根据学校规定，申请成功的时间段内才能刷卡进出学校、宿舍、图书馆等地。
