# SEU AutoEnter

[![license](https://img.shields.io/github/license/amomorning/seu-autoenter)](https://github.com/amomorning/seu-autoenter/blob/master/LICENSE)

东南大学每日报平安健康打卡及入校申请自动化程序  

登录程序主体来自 [StephenHoo/AutoLogin](https://github.com/StephenHoo/AutoLogin)

## Usage
在[Releases](https://github.com/amomorning/seu-autoenter/releases)中发布了无需配置环境的程序包
### Download
- 每日报平安只需下载 login_chrome.zip 
- 自动每日报平安并申请入校(次日 8:31-21:59 四牌楼校区) 下载 enter_chrome.zip
### Run
- 注意需要 chrome 更新到 83 以上 (settings - about - check update)
- 初次运行需要双击 login_chrome.exe 或 enter_chrome.exe 输入一卡通号及密码, 之后会自动读取保存的文件
- 后续将 login.vbs 或 enter.vbs 创建快捷方式添加到开机启动项, 重启电脑自动无窗口执行打卡程序
- 可以给电脑设定自动开机, 那么不管晚上是否关机第二天都能打上卡

## Requirements
自行编译运行需要以下环境
- python3
- selenium
- chrome (测试过程使用的版本号为 84.0.4147.125 (Official Build) (64-bit))

``` bash
conda create -n selenium
conda activate selenium
conda install -c conda-forge selenium

# 每日打卡
python login_chrome.py
[输入用户名密码]

# 申请入校
python enter_chrome.py
```

## FAQ
#### Q: 为什么需要这个程序?
A: 经常在中午12点超出一丢丢的时候意识到妹油申请入校 TAT 原先可以手动调本地时间避开申请时间限制，但是似乎在某此更新里学校修复了这个bug....
