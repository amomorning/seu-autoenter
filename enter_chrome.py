# coding=utf-8

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


# 加启动配置 禁用日志log
chrome_options = Options()
chrome_options.add_argument('–no-sandbox')# “–no - sandbox”参数是让Chrome在root权限下跑
chrome_options.add_argument('–disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_argument('--start-maximized')#最大化
chrome_options.add_argument('--incognito')#无痕隐身模式
chrome_options.add_argument("disable-cache")#禁用缓存
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--headless')

url = "https://newids.seu.edu.cn/authserver/login?service=http://ehall.seu.edu.cn/qljfwapp3/sys/lwWiseduElectronicPass/*default/index.do"
dailyDone = False # 今日是否已经打卡
address = '前工院南602'

# 创建打卡记录log文件
def writeLog(text):
    with open('log.txt', 'a') as f:
        s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + text
        print(s)
        f.write(s + '\n')
        f.close()



def enterUserPW():
    # 创建账号密码文件，以后都不用重复输入
    # 1.1版本之后更新可以读取 chrome.exe 的位置，防止用户Chrome浏览器未安装到默认位置导致的程序无法执行
    try:
        with open("loginData.txt", mode='r', encoding='utf-8') as f:
            # 去掉换行符
            lines = f.readlines()
            user = lines[0].strip()
            pw = lines[1].strip()
            if len(lines) > 2:
                loc = lines[2].strip()
            else:
                loc = ""
            f.close()
    except FileNotFoundError:
        print("Welcome to AUTO DO THE F***ING DAILY JOB, copyright belongs to S.H.")
        with open("loginData.txt", mode='w', encoding='utf-8') as f:
            user = input('Please Enter Your Username: ')
            pw = input('Then Please Enter Your Password: ')
            loc = ""
            f.write(user + '\n')
            f.write(pw + '\n')
            f.close()

    return user, pw, loc


def login(user, pw, browser):
    browser.get(url)
    browser.implicitly_wait(1)
    
    # 填写用户名密码
    username = browser.find_element_by_id('username')
    password = browser.find_element_by_id('password')
    username.clear()
    password.clear()
    username.send_keys(user)
    password.send_keys(pw)


    # 点击登录
    login_button = browser.find_element_by_class_name('auth_login_btn')
    login_button.submit()

# 检查是否无text按钮
def check(text, browser):
    buttons = browser.find_elements_by_class_name(text)
    if(len(buttons) > 0):
        return True
    return False
    
def click_select(rid, pos, browser):
    reqid = "document.getElementsByClassName('is-require')[" + str(rid) + "]"
    # click
    js = reqid + ".click();"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # select pos
    js = reqid + ".parentElement.getElementsByClassName('mt-picker-column-item')[" + str(pos) + "].click();"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # confirm
    js = reqid + ".parentElement.getElementsByClassName('mint-picker__confirm')[0].click();"
    print(js)
    browser.execute_script(js)
    time.sleep(1)
    print('finish select')


def click_checkbox(rid, browser):
    reqid = "document.getElementsByClassName('is-require')[" + str(rid) + "]"
    # click
    js = reqid + ".click();"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # click checkbox
    js = reqid + ".parentElement.getElementsByTagName('input')[1].click();"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # confirm
    js = reqid + ".parentElement.getElementsByClassName('mint-selected-footer-confirm')[0].click();"
    print(js)
    browser.execute_script(js)
    time.sleep(1)


def click_enter_date(rid, dd, hh, mm, browser):
    reqid = "document.getElementsByClassName('is-require')[" + str(rid) + "]"

    # click 
    js = reqid + ".click();"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # set day
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[2].getElementsByClassName('mt-picker-column-item')[" + str(dd-1) + "].click()"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # set hour
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[3].getElementsByClassName('mt-picker-column-item')[" + str(hh) + "].click()"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # set minite
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[4].getElementsByClassName('mt-picker-column-item')[" + str(mm) + "].click();"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # confirm
    js = reqid + ".parentElement.getElementsByClassName('mint-picker__confirm')[0].click()"
    print(js)
    browser.execute_script(js)
    time.sleep(1)


def input_address(rid, browser):
    reqid = "document.getElementsByClassName('is-require')[" + str(rid) + "]"
    # click 

    js = reqid + ".getElementsByTagName('input')[0].value = '" + address + "';"
    print(js)
    browser.execute_script(js)
    time.sleep(1)


if __name__ == "__main__":
    user, pw, browser_loc = enterUserPW()
    # 判断是否写入非默认安装位置的 Chrome 位置
    if len(browser_loc) > 10:
        chrome_options.binary_location = browser_loc
    
    localtime = time.localtime(time.time())
    set_minite = localtime.tm_min # 首次登陆的分钟时刻，代表以后每次在此分钟时刻打卡
    set_hour = localtime.tm_hour # 首次登陆的时钟时刻，代表以后每次在此时钟时刻打卡

    if set_hour > 9:
        set_hour = 7 # 如果首次登录超过上午10点，则以后默认在7点钟打卡
        first_time = True

    while True:
        try:
            # 登录打卡一次试一试
            browser = webdriver.Chrome('./chromedriver',options=chrome_options)
            print("------------------浏览器已启动----------------------")
            login(user, pw, browser)
            browser.implicitly_wait(1)
            time.sleep(10)

            # 确认是否打卡成功
            # 的确无新增按钮
            dailyDone = not check("mint-fixed-button", browser)
            print(browser.current_url)
            if dailyDone is True and check("退出", browser) is True: # 今日已完成打卡
                sleep_time = (set_hour+24-time.localtime(time.time()).tm_hour)*3600 + (set_minite-time.localtime(time.time()).tm_min)*60
                writeLog("下次打卡时间：明天" + str(set_hour) + ':' + str(set_minite) + "，" + "即" + str(sleep_time) + 's后')
                browser.quit()
                print("------------------浏览器已关闭----------------------")
                time.sleep(sleep_time)
            elif dailyDone is False: # 今日未完成打卡
                # 点击报平安
                buttons = browser.find_elements_by_class_name('mint-fixed-button')
                print(len(buttons))
                for button in buttons:
                    button.click()
                    browser.implicitly_wait(10)
                    print(browser.current_url)

                    for i in range(5, 9):
                        click_select(i, 0, browser)
                    
                    # 到校方式 (未标is_require 单独处理)
                    # click
                    js = "document.querySelector('#app > div > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(8) > div > a').click();"
                    print(js)
                    browser.execute_script(js)
                    time.sleep(1)

                    # select
                    js = "document.querySelector('#app > div > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(8) > div > div > div > div:nth-child(2) > div > ul > li:nth-child(2)').click();"
                    print(js)
                    browser.execute_script(js)
                    time.sleep(1)

                    # confirm
                    js = "document.querySelector('#app > div > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(8) > div > div > div > div:nth-child(1) > div:nth-child(2)').click();"
                    print(js)
                    browser.execute_script(js)
                    time.sleep(1)

                    click_checkbox(10, browser)

                    tomorrow = (date.today() + timedelta(1)).day

                    click_enter_date(11, tomorrow, 8, 31, browser)
                    click_enter_date(12, tomorrow, 21, 59, browser)

                    # TODO test input function
                    # 似乎会报未填写的问题, 需要测试
                    input_address(13, browser)

                    click_select(15, 2, browser)
                    # 确认并提交
                    buttons = browser.find_elements_by_tag_name('button')
                    for button in buttons:
                        print(button.get_attribute("textContent"))
                        if button.get_attribute("textContent").find("提交") >= 0:
                            button.click()
                            buttons = browser.find_elements_by_tag_name('button')
                            button = buttons[-1]

                            # 提交
                            if button.get_attribute("textContent").find("确定") >= 0:
                                button.click()
                                dailyDone = True # 标记已完成打卡
                                writeLog("打卡成功")
                            else:
                                print("WARNING: 学校可能改版，请及时更新脚本")
                            break
                    break

            else:
                browser.close()
                print("------------------网站出现故障----------------------")
                print("------------------浏览器已关闭----------------------")
                time.sleep(300) # 昏睡5min 为了防止网络故障未打上卡
        except Exception as r:
            print("未知错误 %s" %(r))
