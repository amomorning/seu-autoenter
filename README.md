# SEU AutoEnter

[![license](https://img.shields.io/github/license/amomorning/seu-autoenter)](https://github.com/amomorning/seu-autoenter/blob/master/LICENSE)

东南大学每日报平安健康打卡及入校申请自动化程序  

登录程序主体来自 [StephenHoo/AutoLogin](https://github.com/StephenHoo/AutoLogin)

## Requirements
- python3
- selenium
- chrome (测试过程使用的版本号为 84.0.4147.125 (Official Build) (64-bit))

## Usage
``` bash
conda create -n selenium
conda activate selenium
conda install -c conda-forge selenium

# 每日打卡
start /b python login_chrome.py
[输入用户名密码]

# 申请入校
start /b python enter_chrome.py
```

## FAQ
#### Q: 为什么需要这个程序?
A: 经常在中午12点超出一丢丢的时候意识到妹油申请入校 TAT 原先可以手动调本地时间避开申请时间限制，但是似乎在某此更新里学校修复了这个bug....
