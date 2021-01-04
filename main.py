import requests
import json
import re
from datetime import datetime
import time
import pickle

from selenium import webdriver
# from personal_info import server_url, webdriver_path, daily_report_data, temp_report_data, login_data
from personal_info import server_url, daily_report_data, temp_report_data, login_data

from apscheduler.schedulers.blocking import BlockingScheduler

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO
from urllib.parse import urljoin
import cv2
import numpy as np
import base64

from personal_info import daily_report_data, temp_report_data, login_data
from slide import SlideCrack
headers = {
    "Cookie": "",
}


def cookies2str(cookies):
    cookie = [item["name"] + "=" + item["value"] for item in cookies]
    cookiestr = ';'.join(item for item in cookie)
    return cookiestr


class Reportor(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/index.do?#/dailyReport"
        self.wid_url = 'http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/modules/dailyReport/getMyTodayReportWid.do'
        self.daily_report_check_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/modules/dailyReport/getMyDailyReportDatas.do?"
        self.daily_report_save_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/modules/dailyReport/T_REPORT_EPIDEMIC_CHECKIN_YJS_SAVE.do?"
        self.temp_report_check_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/getMyTempReportDatas.do?"
        self.temp_report_save_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/T_REPORT_TEMPERATURE_YJS_SAVE.do?"
        self.sess = requests.Session()
        
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 100)
        # options = webdriver.firefox.options.Options()
        # options.add_argument('--headless')  # 无窗口
        # options.add_argument('--incognito')  # 无痕
        # self.driver = webdriver.Firefox(executable_path=webdriver_path, options=options)
        self.login()

    # def login(self):
    #     print("logging in...\r", end="")
    #     self.driver.get(self.login_url)
    #     time.sleep(3)
    #     js = """
    #         var casLoginForm = document.getElementById("casLoginForm");
    #         var username = document.getElementById("username");
    #         var password = document.getElementById("password");
    #         username.value = "{}"
    #         password.value = "{}"
    #         _etd2(password.value, document.getElementById("pwdDefaultEncryptSalt").value);
    #         casLoginForm.submit();
    #     """.format(self.username, self.password)
    #     self.driver.execute_script(js)
    #     time.sleep(10)
    #     try:
    #         self.driver.find_element_by_xpath("/html/body/header/header[1]/div/div/div[4]/div[1]/img").click()
    #         username = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]').text
    #     except Exception:
    #         raise Exception("登录失败")
    #     else:
    #         print("登录账号 ： {}".format(username))
    #     Cookies = self.driver.get_cookies()
    #     self.driver.quit()
    #     headers["Cookie"] = cookies2str(Cookies)

    def login(self):
        # self.driver.get(self.daily_report_url)
        # TODO selenium输入密码登录,并且实现滑块验证码破解
        self.driver.get(self.login_url)
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="casLoginForm"]/p[4]/button').click()

        self.get_captcha1()
        self.get_captcha2()
        # 滑块图片
        image1 = "./front.png"
        # 背景图片
        image2 = "./bg.png"
        # 处理结果图片,用红线标注
        image3 = "/.3.png"
        sc = SlideCrack(image1, image2, image3)
        distance = sc.discern()
        slider = self.get_slider()
        track = self.get_track(distance)
        self.move_to_gap(slider, track)
        # Cookies = self.driver.get_cookies()
        # self.driver.quit()
        # headers["Cookie"] = cookies2str(Cookies)

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()         # 利用动作链，获取slider，perform是

        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()       # xoffset横坐标，yoffset纵坐标。使得鼠标向前推进
        time.sleep(0.5)                                     # 推动到合适位置之后，暂停一会
        ActionChains(self.driver).release().perform()      # 抬起鼠标左键

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'slider')))
        return slider

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:                   # 所以 track是不会大于总长度的
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 移动距离x = v0t + 1/2 * a * t^2，现做了加速运动
            move = v0 * t + 1 / 2 * a * t * t
            # 当前速度v = v0 + at  速度已经达到v，该速度作为下次的初速度
            v = v0 + a * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))                   # track 就是最终鼠标在 X 轴移动的轨迹
        return track

    def get_captcha1(self):
        JS = 'return document.getElementsByTagName("canvas")[0].toDataURL("image/png");'
        # 执行 JS 代码并拿到图片 base64 数据
        im_info = self.driver.execute_script(JS)  #执行js文件得到带图片信息的图片数据
        im_base64 = im_info.split(',')[1]  #拿到base64编码的图片信息
        im_bytes = base64.b64decode(im_base64)  #转为bytes类型
        with open('bg.png','wb') as f:  #保存图片到本地
            f.write(im_bytes)

    def get_captcha2(self):
        JS = 'return document.getElementsByTagName("canvas")[1].toDataURL("image/png");'
        # 执行 JS 代码并拿到图片 base64 数据
        im_info = self.driver.execute_script(JS)  #执行js文件得到带图片信息的图片数据
        im_base64 = im_info.split(',')[1]  #拿到base64编码的图片信息
        im_bytes = base64.b64decode(im_base64)  #转为bytes类型
        with open('front.png','wb') as f:  #保存图片到本地
            f.write(im_bytes)
    def daily_report(self, NEED_DATE, daily_report_data):
        # 获取WID
        wid_data = {
            'pageNumber': '1',
            'pageSize': '10',
            'USER_ID': daily_report_data["USER_ID"],
        }
        res = requests.post(self.wid_url, data=wid_data, headers=headers)
        wid_json_loads = json.loads(res.text)
        wid = wid_json_loads['datas']['getMyTodayReportWid']['rows'][0]['WID']
        daily_report_data['WID'] = wid

        # check
        daily_report_check_url = self.daily_report_check_url
        check_data = {
            'pageNumber': '1',
            'pageSize': '10',
            'USER_ID': daily_report_data["USER_ID"],
            'KSRQ': NEED_DATE,
            'JSRQ': NEED_DATE,
        }
        res = requests.post(daily_report_check_url, data=check_data, headers=headers)
        if res.status_code != 200:
            print("网络错误")
            return 1
        res.encoding = 'utf-8'
        parsed_res = json.loads(res.text)
        try:
            if parsed_res['datas']['getMyDailyReportDatas']['totalSize'] > 0:
                print("daily report has finished")
                return 0
        except KeyError:
            pass

        # save
        daily_report_data.update({
            "NEED_CHECKIN_DATE": NEED_DATE,
            "CZRQ": NEED_DATE+" 00:00:00",
        })
        daily_report_save_url = self.daily_report_save_url
        # for key in daily_report_data.keys():
        #     daily_report_save_url += (key + "=" + daily_report_data[key] + "&")
        # daily_report_save_url = daily_report_save_url[:-1]
        res = self.sess.post(daily_report_save_url, data=daily_report_data, headers=headers)
        if res.status_code != 200:
            print("网络错误")
            return 1
        res.encoding = 'utf-8'
        parsed_res = json.loads(res.text)
        if parsed_res['code'] == '0' and parsed_res['datas']['T_REPORT_EPIDEMIC_CHECKIN_YJS_SAVE'] == 1:
            print("daily report sucessful")
            return 0  # 打卡成功
        else:
            print("打卡失败")
            return 1

    def temp_report(self, NEED_DATE, DAY_TIME, temp_report_data):
        # check
        # 此处服务器仅返回最近几次打卡信息故仅能验证最近几次打卡是否重复，若你已经打到明年了。。。那是没法验证的
        temp_report_check_url = self.temp_report_check_url
        check_data = {
            "USER_ID": temp_report_data["USER_ID"],
            "NEED_DATE": NEED_DATE,
            "DAY_TIME": DAY_TIME,
        }
        # temp_report_check_url += ("USER_ID=" + temp_report_data["USER_ID"] + "&")
        # temp_report_check_url += (NEED_DATE + "&")
        # temp_report_check_url += ("DAY_TIME=" + DAY_TIME)

        res = self.sess.post(temp_report_check_url, data=check_data, headers=headers)
        if res.status_code != 200:
            print("网络错误")
            return 1
        res.encoding = 'utf-8'
        if re.search('"NEED_DATE":"{}","DAY_TIME":"{}"'.format(NEED_DATE, DAY_TIME), res.text) is not None:
            print("temp report {} has finished".format(DAY_TIME))
            return int(DAY_TIME)
        elif re.search("<title>统一身份认证</title>", res.text):
            print("Cookie失效")
            exit(0)

        # save
        DAY_TIME_DISPLAY = {
            "1": "早上",
            "2": "中午",
            "3": "晚上",
        }
        temp_report_data.update({
            "DAY_TIME": DAY_TIME,
            "DAY_TIME_DISPLAY": DAY_TIME_DISPLAY[DAY_TIME],
            "NEED_DATE": NEED_DATE,
        })
        # temp_report_save_url = self.temp_report_save_url
        # for key in temp_report_data.keys():
        #     temp_report_save_url += (key + "=" + temp_report_data[key] + "&")
        # temp_report_save_url = temp_report_save_url[:-1]

        res = self.sess.post(temp_report_save_url, data=temp_report_data, headers=headers)
        if res.status_code != 200:
            print("网络错误")
            return 1
        res.encoding = 'utf-8'
        try:
            assert re.search(r'"T_REPORT_TEMPERATURE_YJS_SAVE":(?P<r_value>\d)', res.text)["r_value"] == '1'
            print("temp report {} sucessful".format(DAY_TIME))
            return int(DAY_TIME)
        except Exception:
            if re.search("<title>统一身份认证</title>", res.text):
                print("Cookie失效")
                exit(0)
            time.sleep(5)
            return 0


def daily_check(reportor, daily_report_data, temp_report_data, date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
        print("当前时间：" + str(datetime.now()))
    # 平安打卡
    while(reportor.daily_report(date_str, daily_report_data)):
        continue
    # 体温上报
    r_value_list = []
    for id in range(1, 4):
        while(id not in r_value_list):
            r_value_list.append(reportor.temp_report(date_str, str(id), temp_report_data))
    # 四项打卡全部完成
    print("day {} report complete!\n".format(date_str))
    return date_str


def check_job(daily_report_data, temp_report_data):
    reportor = Reportor(login_data['username'], login_data['password'])
    date_str = daily_check(reportor, daily_report_data, temp_report_data)
    # if server_url is not None:
    #     requests.get(url=server_url+f'?text={date_str}打卡完成')


if __name__ == "__main__":
    check_job(daily_report_data, temp_report_data)
    scheduler_report = BlockingScheduler()
    scheduler_report.add_job(check_job, 'cron', day='*', hour="0", minute="0", args=[
        daily_report_data, temp_report_data
    ])
    print("job started")
    scheduler_report.start()
    if server_url is not None:
        requests.get(url=server_url+f'?text=我挂了')
