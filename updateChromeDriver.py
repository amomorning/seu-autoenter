import requests
import os
import zipfile
import re
import winreg

def get_chrome_version():
    FullChromeVersion = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome'),'DisplayVersion')[0]
    return int(FullChromeVersion.split('.')[0])

def get_latest_version(chrome_version, url):
    '''查询最新的Chromedriver版本'''
    rep = requests.get(url).text
    time_list = []                                          # 用来存放版本时间
    time_version_dict = {}                                  # 用来存放版本与时间对应关系
    result = re.compile(r'\d.*?/</a>.*?Z').findall(rep)     # 匹配文件夹（版本号）和时间
    for i in result:
        time = i[-24:-1]                                    # 提取时间
        version = re.compile(r''+str(chrome_version)+'.+?/').findall(i)        # 提取版本号
        # print(i)
        if(len(version) > 1):
            time_version_dict[time] = version[-1]                   # 构建时间和版本号的对应关系，形成字典
            time_list.append(time)                              # 形成时间列表
    latest_version = time_version_dict[max(time_list)][:-1] # 用最大（新）时间去字典中获取最新的版本号
    return latest_version

def download_driver(download_url):
    '''下载文件'''
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:        # 保存文件到脚本所在目录
        zip_file.write(file.content)
        print('下载成功')

def get_version():
    '''查询系统内的Chromedriver版本'''
    outstd2 = os.popen('chromedriver --version').read()
    return outstd2.split(' ')[1]

def get_path():
    '''查询系统内Chromedriver的存放路径'''
    outstd1 = os.popen('where chromedriver').read()
    return outstd1.strip('chromedriver.exe\n')

def unzip_driver(path):
    '''解压Chromedriver压缩包到指定目录'''
    f = zipfile.ZipFile("chromedriver.zip",'r')
    for file in f.namelist():
        f.extract(file, path)

if __name__ == "__main__":
    url = 'http://npm.taobao.org/mirrors/chromedriver/'

    chrome_version = get_chrome_version()
    print('当前系统安装的chrome版本为：', chrome_version)
    latest_version = get_latest_version(chrome_version, url)
    print('最新的chromedriver版本为：', latest_version)
    version = get_version()
    print('当前系统内的Chromedriver版本为：', version)
    if version == latest_version:
        print('当前系统内的Chromedriver已经是最新的')
    else:
        print('当前系统内的Chromedriver不是最新的，需要进行更新')
        download_url = url + latest_version + '/chromedriver_win32.zip'  # 拼接下载链接
        download_driver(download_url)
        path = get_path()
        print('替换路径为：', path)
        unzip_driver(path)
        print('更新后的Chromedriver版本为：', get_version())
