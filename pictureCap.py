
url = 'https://www.baidu.com'

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys #键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素
from selenium.webdriver.chrome.options import Options
from datetime import date, timedelta
import time
import random
import json
import codecs


# 加启动配置 禁用日志log
chrome_options = Options()
chrome_options.add_argument('–no-sandbox')# “–no - sandbox”参数是让Chrome在root权限下跑
chrome_options.add_argument('–disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_argument('--start-maximized')#最大化
chrome_options.add_argument('--incognito')#无痕隐身模式
chrome_options.add_argument("disable-cache")#禁用缓存
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome('./chromedriver',options=chrome_options)
browser.set_window_size(500,900)
browser.get(url)

flag = False
for i in range(5):
    time.sleep(3)
    el = browser.find_element(By.ID, 'code-name')
    if(el.text != ''):
        flag = True
        break

if(flag):
    filename = './imgs/{}.png'.format(date.today())
    browser.get_screenshot_as_file(filename)
else:
    print("WARNING: 无法保存")


# browser.quit()
