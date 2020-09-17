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
import json
import codecs


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

dailyDone = False # 今日是否已经打卡
enterFlag = False # 是否需要申请入校


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
    
    # print(enter_dict)

    return user, pw, tel, address


def login(user, pw, url, browser):
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
    buttons = browser.find_elements_by_tag_name('button')
    for button in buttons:
        if button.get_attribute("textContent").find(text)>= 0:
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


def click_enter_date(rid, tomorrow, hh, mm, browser):
    reqid = "document.getElementsByClassName('is-require')[" + str(rid) + "]"

    # click 
    js = reqid + ".click();"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # set year
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[0].getElementsByClassName('mt-picker-column-item')[" + str(tomorrow.year-1920) + "].click()"
    print(js)
    browser.execute_script(js)
    time.sleep(1)

    # set month
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[1].getElementsByClassName('mt-picker-column-item')[" + str(tomorrow.month-1) + "].click()"
    print(js)
    browser.execute_script(js)
    time.sleep(1)


    # set day
    js = reqid + ".parentElement.getElementsByClassName('mint-picker-column')[2].getElementsByClassName('mt-picker-column-item')[" + str(tomorrow.day-1) + "].click()"
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

def click_select_way(browser):
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

# TODO 校外同学申请入校需上传苏康码
# 没有找到上传图片的标签
# def upload_health_code(browser):
#     reqid = "document.getElementsByClassName('is-require')[16]"
#     # click
#     js = reqid + ".click();"
#     # print(js)
#     browser.execute_script(js)
#     time.sleep(1)

#     # click checkbox
#     js = reqid + ".parentElement.getElementsByTagName('input')[1].click();"
#     # print(js)
#     browser.execute_script(js)
#     time.sleep(1)

                
def input_field(placehold, text, browser):
    inputfileds = browser.find_elements_by_tag_name('input')
    for i in inputfileds:
        # print(i.get_attribute('placeholder'))
        if i.get_attribute("placeholder").find(placehold) >= 0:
            time.sleep(3)
            i.clear()
            i.send_keys(text)
            break

def click_confirm(text, log_text, browser):
    buttons = browser.find_elements_by_tag_name('button')
    for button in buttons:
        # print(button.get_attribute("textContent"))
        if button.get_attribute("textContent").find(text) >= 0:
            # print(browser.current_url)
            button.click()
            time.sleep(5)
            # print(browser.current_url)

            buttons = browser.find_elements_by_tag_name('button')
            button = buttons[-1]
            # print(button.get_attribute("textContent"))
            # 提交
            if button.get_attribute("textContent").find("确定") >= 0:
                button.click()
                dailyDone = True # 标记已完成打卡
                print(log_text)
                writeLog(log_text)
                return True
            else:
                print("WARNING: 学校可能改版，请及时更新脚本")
            break
    return False

def apply_enter(user, pw, tel, address):
    try:
        enter_url = "https://newids.seu.edu.cn/authserver/login?service=http://ehall.seu.edu.cn/qljfwapp3/sys/lwWiseduElectronicPass/*default/index.do"
        browser = webdriver.Chrome('./chromedriver',options=chrome_options)
        print("------------------浏览器已启动----------------------")
        login(user, pw, enter_url, browser)
        browser.implicitly_wait(1)
        time.sleep(10)

        buttons = browser.find_elements_by_class_name('mint-fixed-button')
        # print(len(buttons))
        for button in buttons:
            button.click()
            break
        # print(browser.current_url)

        browser.implicitly_wait(1)
        time.sleep(10)

        click_select(2, 0, browser)

        for i in range(5, 9):
            click_select(i, 0, browser)
        
        click_select_way(browser)

        click_checkbox(10, browser)

        tomorrow = (date.today() + timedelta(1))

        click_enter_date(11, tomorrow, 8, 31, browser)
        click_enter_date(12, tomorrow, 21, 59, browser)

        click_select(15, 2, browser)

        input_field("请输入所到楼宇（具体到门牌号）", address, browser)
        browser.implicitly_wait(1)
        time.sleep(1)

        if(tel != ""):
            input_field("请输入联系方式", tel, browser)
            browser.implicitly_wait(1)
            time.sleep(1)
            


        # 确认并提交
        if(click_confirm("提交", "申请成功", browser)) : 
            browser.quit()
            print("------------------浏览器已关闭----------------------")
            time.sleep(10) # 昏睡10s 为了防止网络故障未打上
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

        browser = webdriver.Chrome('./chromedriver',options=chrome_options)
        print("------------------浏览器已启动----------------------")
        login(user, pw, login_url, browser)
        browser.implicitly_wait(10)
        time.sleep(10)

        # 确认是否打卡成功
        # 的确无新增按钮
        dailyDone = not check("新增", browser)
        # print(dailyDone)
        print(browser.current_url)
        if dailyDone is True and check("退出", browser) is True: # 今日已完成打卡
            sleep_time = (set_hour+24-time.localtime(time.time()).tm_hour)*3600 + (set_minite-time.localtime(time.time()).tm_min)*60
            writeLog("下次打卡时间：明天" + str(set_hour) + ':' + str(set_minite) + "，" + "即" + str(sleep_time) + 's后')
            browser.quit()
            print("------------------浏览器已关闭----------------------")
            time.sleep(sleep_time)
        elif dailyDone is False: # 今日未完成打卡
            buttons = browser.find_elements_by_css_selector('button')
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

                while enterFlag:
                    if(apply_enter(user, pw, tel, address)):
                        break

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

if __name__ == "__main__":
    user, pw, tel, address = readConfig()
    # Test apply
    # while True:
    #     if(apply_enter(user, pw, address)):
    #         break 

    if(user == "" or pw == "" or address == ""):
        print("Input is not valid, please check file './config.json' ")
    else:
        localtime = time.localtime(time.time())
        set_minite = localtime.tm_min # 首次登陆的分钟时刻，代表以后每次在此分钟时刻打卡
        set_hour = localtime.tm_hour # 首次登陆的时钟时刻，代表以后每次在此时钟时刻打卡

        print(enterFlag)
        if set_hour > 9:
            set_hour = 7 # 如果首次登录超过上午10点，则以后默认在7点钟打卡
            first_time = True


        while True:
            auto_login(user, pw, tel, address)
            

