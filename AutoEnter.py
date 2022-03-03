# coding=utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from datetime import date, timedelta
import time
import random
import json
import codecs
import base64
# import pyperclip

# 加启动配置 禁用日志log
chrome_options = Options()
chrome_options.add_argument('-no-sandbox')# “–no - sandbox”参数是让Chrome在root权限下跑
chrome_options.add_argument('-disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_argument('--start-maximized')#最大化
chrome_options.add_argument('--incognito')#无痕隐身模式
chrome_options.add_argument("disable-cache")#禁用缓存
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('disable-infobars')

dailyDone = False # 今日是否已经打卡
enterFlag = False # 是否需要申请入校

sucodeURL = ''

# 下载最新版本 chromedriver
# https://blog.csdn.net/weijiaxin2010/article/details/86651042
import requests
import os
import zipfile
import re
import winreg

# 创建打卡记录log文件
def writeLog(text):
    with open('log.txt', 'a') as f:
        s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + text
        print(s)
        f.write(s + '\n')
        f.close()

def readConfig():
    with codecs.open('./config.json','r', encoding='utf-8', errors='ignore') as load_f:
        enter_dict = json.load(load_f)
        user = enter_dict["username"]
        pw = enter_dict["password"]
        tel = enter_dict["tel"]
        address = enter_dict["address"]

        global enterFlag
        enterFlag = enter_dict["enter"]
        global sucodeURL
        sucodeURL = enter_dict["sucodeURL"]

        headless = enter_dict["headless"]
        if(headless):
            chrome_options.add_argument('--headless')
    
    # print(enter_dict)

    return user, pw, tel, address


def login(user, pw, url, browser):
    browser.get(url)
    browser.implicitly_wait(1)
    
    # 填写用户名密码
    username = browser.find_element(By.ID, 'username')
    password = browser.find_element(By.ID, 'password')
    username.clear()
    password.clear()
    username.send_keys(user)
    password.send_keys(pw)

    # 点击登录
    login_button = browser.find_element(By.CLASS_NAME, 'auth_login_btn')
    login_button.submit()

# 检查是否无text按钮
def check(text, browser):
    buttons = browser.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        if button.get_attribute("textContent").find(text)>= 0:
            return True
    return False
    
def click_select(rid, pos, browser):
    reqid = "document.getElementsByClassName('is-require')[" + str(rid) + "]"
    # click
    js = reqid + ".click();"
    # print(js)
    browser.execute_script(js)
    time.sleep(2)

    # select pos
    js = reqid + ".parentElement.getElementsByClassName('mt-picker-column-item')[" + str(pos) + "].click();"
    # print(js)
    browser.execute_script(js)
    time.sleep(2)

    # confirm
    js = reqid + ".parentElement.getElementsByClassName('mint-picker__confirm')[0].click();"
    # print(js)
    browser.execute_script(js)
    time.sleep(2)
    # print('finish select')


def click_checkbox(rid, browser):
    reqid = "document.getElementsByClassName('is-require')[" + str(rid) + "]"
    # click
    js = reqid + ".click();"
    # print(js)
    browser.execute_script(js)
    time.sleep(1)

    # click checkbox
    js = reqid + ".parentElement.getElementsByTagName('input')[1].click();"
    # print(js)
    browser.execute_script(js)
    time.sleep(1)

    # confirm
    js = reqid + ".parentElement.getElementsByClassName('mint-selected-footer-confirm')[0].click();"
    # print(js)
    browser.execute_script(js)
    time.sleep(1)


def click_enter_date(rid, tomorrow, hh, mm, browser):
    reqid = "document.getElementsByClassName('is-require')[" + str(rid) + "]"

    # click 
    js = reqid + ".click();"
    browser.execute_script(js)
    time.sleep(1)

    # set year
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[0].getElementsByClassName('mt-picker-column-item')[100].click()"
    browser.execute_script(js)
    time.sleep(1)

    # set month
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[1].getElementsByClassName('mt-picker-column-item')[" + str(tomorrow.month-1) + "].click()"
    browser.execute_script(js)
    time.sleep(1)


    # set day
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[2].getElementsByClassName('mt-picker-column-item')[" + str(tomorrow.day-1) + "].click()"
    browser.execute_script(js)
    time.sleep(1)

    # set hour
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[3].getElementsByClassName('mt-picker-column-item')[" + str(hh) + "].click()"
    browser.execute_script(js)
    time.sleep(1)

    # set minite
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[4].getElementsByClassName('mt-picker-column-item')[" + str(mm) + "].click();"
    browser.execute_script(js)
    time.sleep(1)

    # confirm
    js = reqid + ".parentElement.getElementsByClassName('mint-picker__confirm')[0].click()"
    browser.execute_script(js)
    time.sleep(1)

def click_select_way(browser):
    # 到校方式 (未标is_require 单独处理)
    # click
    js = "document.querySelector('#app > div > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(8) > div > a').click();"
    browser.execute_script(js)
    time.sleep(1)

    # select
    js = "document.querySelector('#app > div > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(8) > div > div > div > div:nth-child(2) > div > ul > li:nth-child(1)').click();"
    browser.execute_script(js)
    time.sleep(1)

    js = "document.querySelector('#app > div > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(8) > div > div > div > div:nth-child(1) > div:nth-child(2)').click();"
    browser.execute_script(js)
    time.sleep(1)


def input_field(placehold, text, browser):
    inputfileds = browser.find_elements(By.TAG_NAME,'input')
    for i in inputfileds:
        # print(i.get_attribute('placeholder'))
        if i.get_attribute("placeholder").find(placehold) >= 0:
            time.sleep(3)
            i.clear()
            i.send_keys(text)
            break

def click_confirm(text, log_text, browser):
    buttons = browser.find_elements(By.TAG_NAME,'button')
    for button in buttons:
        if button.get_attribute("textContent").find(text) >= 0:
            button.click()
            time.sleep(5)

            buttons = browser.find_elements(By.TAG_NAME,'button')
            button = buttons[-1]
            # 提交
            if button.get_attribute("textContent").find("确定") >= 0:
                button.click()
                time.sleep(5)
                dailyDone = True # 标记已完成打卡
                print(log_text)
                writeLog(log_text)
                return True
            else:
                print("WARNING: 学校可能改版，请及时更新脚本")
            break
    return False


def check_enter(browser):
    date_info_raw = browser.find_element(By.XPATH("/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[2]/span[2]"))
    date_info = re.findall(r"\d+\.?\d*",date_info_raw.text)
    year_info = date_info[0]
    month_info = date_info[1]
    day_info = date_info[2]

    today_year = date.today().strftime("%Y")
    today_month = date.today().strftime("%m")
    today_day = date.today().strftime("%d")

    if year_info == today_year and month_info == today_month and day_info == today_day:
        return True
    else:
        return False


def apply_enter(user, pw, tel, address):
    try:
        enter_url = "https://newids.seu.edu.cn/authserver/login?service=http://ehall.seu.edu.cn/qljfwapp3/sys/lwWiseduElectronicPass/*default/index.do"
        
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        print("------------------浏览器已启动----------------------")
        login(user, pw, enter_url, browser)
        browser.implicitly_wait(1)
        time.sleep(10)

        if(check_enter(browser) == True):
            print("今日已申请")
            return True

        buttons = browser.find_elements(By.CLASS_NAME, 'mint-fixed-button')
        # print(len(buttons))
        for button in buttons:
            button.click()
            break
        # print(browser.current_url)

        browser.implicitly_wait(1)
        time.sleep(10)

        # click_select(2, 0, browser)

        # for i in range(5, 7):
        #     click_select(i, 0, browser)
        
        click_select_way(browser)

        # click_checkbox(14, browser)

        tomorrow = (date.today() + timedelta(1))

        click_enter_date(15, tomorrow, 7, 31, browser)
        click_enter_date(16, tomorrow, 21, 59, browser)

        click_select(19, 2, browser)

        input_field("请输入所到楼宇（具体到门牌号）", address, browser)
        browser.implicitly_wait(1)
        time.sleep(1)

        if(tel != ""):
            input_field("请输入联系方式", tel, browser)
            browser.implicitly_wait(1)
            time.sleep(1)
        

        filename = './imgs/{}.png'.format(date.today())
        with open(filename, "rb") as f:
            b = 'data:image/png;base64,' + str(base64.b64encode(f.read()))[2:-1]
            
            js = "document.getElementsByClassName('upload_img')[2].src='{}'".format(b)
            # pyperclip.copy(js)

            browser.execute_script(js)

            time.sleep(10)


        time.sleep(60)
        # 确认并提交
        if(click_confirm("提交", "申请成功", browser)) : 
            browser.quit()
            print("------------------浏览器已关闭----------------------")
            time.sleep(10) 
            return True
        else:
            browser.close()
            print("------------------打卡出现故障----------------------")
            print("------------------浏览器已关闭----------------------")

    except Exception as r:
        print("未知错误 %s" %(r))

    return False


def auto_login(user, pw, tel, address):
    try:
        # 登录打卡一次试一试
        login_url = "https://newids.seu.edu.cn/authserver/login?service=http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/*default/index.do"

        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        print("------------------浏览器已启动----------------------")
        login(user, pw, login_url, browser)
        browser.implicitly_wait(10)
        time.sleep(10)

        # 确认是否打卡成功
        # 的确无新增按钮
        dailyDone = not check("新增", browser)
        # print(dailyDone)
        if(dailyDone):
            print("今日已打卡")
            browser.quit()
            return True

        if dailyDone is False: # 今日未完成打卡
            buttons = browser.find_elements(By.CSS_SELECTOR, 'button')
            for button in buttons:
                if button.get_attribute("textContent").find("新增")>= 0:
                    button.click()
                    browser.implicitly_wait(10)
                    break
            
            input_field("请输入当天晨检体温", str(random.randint(360,367)/10.0), browser)
            browser.implicitly_wait(10)

            if(click_confirm("确认并提交", "打卡成功", browser)) : 
                browser.quit()
                print("------------------浏览器已关闭----------------------")
                time.sleep(10) # 昏睡10s 为了防止网络故障未打上
                return True
            else:
                browser.close()
                print("------------------打卡出现故障----------------------")
                print("------------------浏览器已关闭----------------------")
        else:
            browser.close()
            print("------------------网站出现故障----------------------")
            print("------------------浏览器已关闭----------------------")
            time.sleep(300) # 昏睡5min 为了防止网络故障未打上卡
    except Exception as r:
        print("未知错误 %s" %(r))

    return False


def auto_sucode():
    if(sucodeURL == ''):
        print("WARNING: 没有苏康码链接，请检查配置文件中sucodeURL项")
        return False

    try:
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        print("------------------浏览器已启动----------------------")
        browser.set_window_size(500,900)
        browser.get(sucodeURL)

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
            browser.quit()
            print("------------------浏览器已关闭----------------------")
            return True
        else:
            print("WARNING: 无法保存苏康码")
            print("------------------打卡出现故障----------------------")
            print("------------------浏览器已关闭----------------------")
            browser.quit()
            return False
    except Exception as r:
        print("未知错误 %s" %(r))
    return False





if __name__ == "__main__":
    user, pw, tel, address = readConfig()

    if(user == "" or pw == "" or address == ""):
        print("Input is not valid, please check file './config.json' ")
    else:
        localtime = time.localtime(time.time())
        set_minite = localtime.tm_min # 首次登陆的分钟时刻，代表以后每次在此分钟时刻打卡
        set_hour = localtime.tm_hour # 首次登陆的时钟时刻，代表以后每次在此时钟时刻打卡

        if set_hour > 9:
            set_hour = 7 # 如果首次登录超过上午10点，则以后默认在7点钟打卡

        while True:

            while(True):
                if(auto_login(user, pw, tel, address)):
                    break

            # while(True):
            #     if(auto_sucode()):
            #         break

            while enterFlag:
                if(apply_enter(user, pw, tel, address)):
                    break
            
            sleep_time = (set_hour+24-time.localtime(time.time()).tm_hour)*3600 + (set_minite-time.localtime(time.time()).tm_min)*60
            writeLog("下次打卡时间：明天" + str(set_hour) + ':' + str(set_minite) + "，" + "即" + str(sleep_time) + 's后')
            time.sleep(sleep_time)

        


            

