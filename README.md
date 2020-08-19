# SEU AutoEnter

[![license](https://img.shields.io/github/license/amomorning/seu-autoenter)](https://github.com/amomorning/seu-autoenter/blob/master/LICENSE)

东南大学每日报平安健康打卡及入校申请自动化程序  

登录程序主体来自 [StephenHoo/AutoLogin](https://github.com/StephenHoo/AutoLogin)

## Usage
在[Releases](https://github.com/amomorning/seu-autoenter/releases)中发布了无需配置环境的程序包
### Download
- 每日报平安只需下载 [login_chrome.zip](https://github.com/amomorning/seu-autoenter/releases/download/v1.0/login_chrome.zip) 
- 自动每日报平安并申请入校(次日 8:31-21:59 四牌楼校区) 下载 [enter_chrome.zip](https://github.com/amomorning/seu-autoenter/releases/download/v1.0/enter_chrome.zip)
- 注意需要 chrome 更新到 83 以上 (settings - about - check update)

### 每日打卡
- login_chrome.zip 对应源码 login_chrome.py
- 该程序随机填入36.0-36.7体温并提交打卡记录
#### 使用步骤
1. 在`_login.json`中填入一卡通号、密码
2. 双击`login.vbs`, 约一分钟内能完成打卡, 如不关机下次打卡时间为`hh>10?7:hh`时`mm`分.
3. 将`login.vbs`快捷方式复制到开机启动项中, 那么开机自动打卡(不能使用Windows睡眠)
4. 日志文件为`./bin/log.txt`


### 申请入校
- enter_chrome.zip 对应源码 enter_chrome.py
- 该程序随机填入36.0-36.7体温并提交打卡记录, 再执行自动填表申请入校, 到校后所到地址需在`_enter.json`中写明
#### 使用步骤
1. 在`_enter.json`中填入一卡通号、密码，以及每日申请入校所到的地址
2. 双击`enter.vbs`, 约两分钟内能完成打卡和申请, 如不关机下次打卡时间为`hh>10?7:hh`时`mm`分.
3. 将`enter.vbs`快捷方式复制到开机启动项中, 那么开机自动打卡(不能使用Windows睡眠)
4. 日志文件为`./bin/log.txt`


## Requirements
自行编译运行需要以下环境
- python3
- selenium
- chrome (测试过程使用的版本号为 84.0.4147.125 (Official Build) (64-bit))
- pyinstaller (用于导出exe)

``` bash
conda create -n selenium
conda activate selenium
conda install -c conda-forge selenium

# 每日打卡
python login_chrome.py

# 申请入校
python enter_chrome.py
```

## FAQ
#### Q: 为什么需要这个程序?
A: 经常在中午12点超出一丢丢的时候意识到妹油申请入校 TAT 原先可以手动调本地时间避开申请时间限制，但是似乎在某此更新里学校修复了这个bug....
