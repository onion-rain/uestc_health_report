import requests
from my_request import get_request
import json
import re
from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from personal_info import server_url, webdriver_path, daily_report_data, temp_report_data

from apscheduler.schedulers.blocking import BlockingScheduler

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import base64

from my_request import get_request
from slide import SlideCrack

MAX_TRY = 10

headers = {
    "Cookie": ""
}


def cookies2str(cookies):
    cookie = [item["name"]+"="+item["value"] for item in cookies]
    cookiestr = ';'.join(item for item in cookie)
    return cookiestr


class Reportor(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.host = "eportal.uestc.edu.cn"
        self.login_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/index.do?#/dailyReport"
        self.wid_url = '/jkdkapp/sys/lwReportEpidemicStu/modules/dailyReport/getMyTodayReportWid.do?'
        self.daily_report_check_url = "/jkdkapp/sys/lwReportEpidemicStu/modules/dailyReport/getMyDailyReportDatas.do?"
        self.daily_report_save_url = "/jkdkapp/sys/lwReportEpidemicStu/modules/dailyReport/T_REPORT_EPIDEMIC_CHECKIN_YJS_SAVE.do?"
        self.temp_report_check_url = "/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/getMyTempReportDatas.do?"
        self.temp_report_save_url = "/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/T_REPORT_TEMPERATURE_YJS_SAVE.do?"
        options = webdriver.firefox.options.Options()
        options.add_argument('--headless')  # 无窗口
        options.add_argument('--incognito')  # 无痕
        self.driver_service=Service(webdriver_path)
        self.driver_service.start()
        self.driver = webdriver.Firefox(executable_path=webdriver_path, options=options)
        self.wait = WebDriverWait(self.driver, 100)


    def login(self):
        print("logging in...\r", end="")
        def update_cookies():
            Cookies = self.driver.get_cookies()
            self.driver.quit()
            self.driver_service.stop()
            headers["Cookie"] = cookies2str(Cookies)
        
        def _login(i):
            print("第{}次尝试登录".format(i))
            self.driver.get(self.login_url)
            self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(self.username)
            self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
            self.driver.find_element_by_xpath('//*[@id="casLoginForm"]/p[4]/button').click()

            time.sleep(5)
            self.get_captcha1()
            self.get_captcha2()
            # 滑块图片
            image1 = "./front.png"
            # 背景图片
            image2 = "./bg.png"
            # 处理结果图片,用红线标注
            image3 = "./3.png"
            sc = SlideCrack(image1, image2, image3)
            distance = sc.discern()
            slider = self.get_slider()
            track = self.get_track(distance)
            self.move_to_gap(slider, track)
        def _check():
            """return 1 为检测登陆成功"""
            try:
                self.driver.find_element_by_xpath("/html/body/header/header[1]/div/div/div[4]/div[1]/img").click()
                time.sleep(2)
                username = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]').text
            except Exception:
                time.sleep(10)
                return 0
            else:
                print("登录账号 ： {}".format(username))
                update_cookies()
                return 1
        for i in range(MAX_TRY):  # 重复尝试登陆十次
            time.sleep(3)
            if _check():
                return
            _login(i+1)
            if _check():
                return
        if server_url is not None:
            requests.get(url=server_url+f'登陆失败，上服务器看看我觉得我还有救')
        raise RuntimeError("登录失败")

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

    def _daily_report(self, NEED_DATE, daily_report_data):
        # 获取WID
        wid_data = {
            'pageNumber': '1',
            'pageSize': '10',
            'USER_ID': daily_report_data["USER_ID"],
        }
        res = get_request(self.host, "POST", self.wid_url, wid_data, headers)
        if re.search("<title>统一身份认证</title>", res):
            raise RuntimeError("Cookie失效")
        elif re.search("<title>302 Found</title>", res):
            raise RuntimeError("Cookie失效") 
        try:
            wid_json_loads = json.loads(res)
            wid = wid_json_loads['datas']['getMyTodayReportWid']['rows'][0]['WID']
            daily_report_data['WID'] = wid
        except json.decoder.JSONDecodeError:
            print("json解析失败")
            return 1

        # check
        check_data = {
            'pageNumber': '1',
            'pageSize': '10',
            'USER_ID': daily_report_data["USER_ID"],
            'KSRQ': NEED_DATE,
            'JSRQ': NEED_DATE,
        }
        res = get_request(self.host, "POST", self.daily_report_check_url, check_data, headers)
        if re.search("<title>统一身份认证</title>", res):
            raise RuntimeError("Cookie失效")
        elif re.search("<title>302 Found</title>", res):
            raise RuntimeError("Cookie失效") 
        try:
            parsed_res = json.loads(res)
        except json.decoder.JSONDecodeError:
            print("json解析失败")
            return 1
        try:
            if parsed_res['datas']['getMyDailyReportDatas']['totalSize'] > 0:
                print("daily report has finished")
                return 0  # 打卡成功
        except KeyError:
            pass

        # save
        daily_report_data.update({
            "NEED_CHECKIN_DATE": NEED_DATE,
            "CZRQ": NEED_DATE+" 00:00:00",
        })
        res = get_request(self.host, "POST", self.daily_report_save_url, daily_report_data, headers)
        if re.search("<title>统一身份认证</title>", res):
            raise RuntimeError("Cookie失效")
        elif re.search("<title>302 Found</title>", res):
            raise RuntimeError("Cookie失效") 
        try:
            parsed_res = json.loads(res)
        except json.decoder.JSONDecodeError:
            print("json解析失败")
            return 1
        if parsed_res['code'] == '0' and parsed_res['datas']['T_REPORT_EPIDEMIC_CHECKIN_YJS_SAVE'] == 1:
            print("daily report sucessful")
            return 0  # 打卡成功
        else:
            print("打卡失败")
            return 1

    def _temp_report(self, NEED_DATE, DAY_TIME, temp_report_data):
        check_data = {
            "USER_ID": temp_report_data["USER_ID"],
            "NEED_DATE": NEED_DATE,
            "DAY_TIME": DAY_TIME,
        }
        res = get_request(self.host, "POST", self.temp_report_check_url, check_data, headers)
        if re.search("<title>统一身份认证</title>", res):
            raise RuntimeError("Cookie失效")
        elif re.search("<title>302 Found</title>", res):
            raise RuntimeError("Cookie失效") 
        if re.search('"NEED_DATE":"{}","DAY_TIME":"{}"'.format(NEED_DATE, DAY_TIME), res) is not None:
            print("temp report {} has finished".format(DAY_TIME))
            return int(DAY_TIME)

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

        res = get_request(self.host, "POST", self.temp_report_save_url, temp_report_data, headers)
        if re.search("<title>统一身份认证</title>", res):
            raise RuntimeError("Cookie失效")
        elif re.search("<title>302 Found</title>", res):
            raise RuntimeError("Cookie失效") 
        try:
            assert re.search(r'"T_REPORT_TEMPERATURE_YJS_SAVE":(?P<r_value>\d)', res)["r_value"] == '1'
            print("temp report {} sucessful".format(DAY_TIME))
            return int(DAY_TIME)  # 打卡成功
        except Exception:
            time.sleep(5)
            return 0

    def daily_report(self, NEED_DATE, daily_report_data):
        try:
            return self._daily_report(NEED_DATE, daily_report_data)
        except RuntimeError as e:
            print(e)
            if server_url is not None:
                requests.get(url=server_url+f'{e}，上服务器看看我还有救吗')
            exit(0)
        except Exception:
            return 1

    def temp_report(self, NEED_DATE, DAY_TIME, temp_report_data):
        try:
            return self._temp_report(NEED_DATE, DAY_TIME, temp_report_data)
        except RuntimeError as e:
            print(e)
            if server_url is not None:
                requests.get(url=server_url+f'{e}，上服务器看看我还有救吗')
            exit(0)
        except Exception:
            return 1

def daily_check(reportor, daily_report_data, temp_report_data, date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
        print("当前时间：" + str(datetime.now()))
    # 平安打卡
    for _ in range(MAX_TRY):
        if reportor.daily_report(date_str, daily_report_data) == 0:
            print("{} day {} report complete!\n".format(daily_report_data["USER_NAME"], date_str))
            return date_str
    # 打卡失败
    print("{} day {} report failed!\n".format(daily_report_data["USER_NAME"], date_str))
    return None
    # # 体温上报
    # r_value_list = []
    # for id in range(1, 4):
    #     while(id not in r_value_list):
    #         r_value_list.append(reportor.temp_report(date_str, str(id), temp_report_data))
    # 四项打卡全部完成


def check_job(daily_report_data, temp_report_data):
    date_str = []
    for id in range(len(daily_report_data)):
        reportor = Reportor(daily_report_data[id]["login_data"]['username'], daily_report_data[id]["login_data"]['password'])
        reportor.login()
        date_str.append(daily_check(reportor, daily_report_data[id], temp_report_data[id]))
    if server_url is not None:
        if None in date_str:
            requests.get(url=server_url+f'{date_str}打卡失败')
        # else:
        #     requests.get(url=server_url+f'?text={date_str}打卡完成')


if __name__ == "__main__":
    check_job(daily_report_data, temp_report_data)
    scheduler_report = BlockingScheduler()
    scheduler_report.add_job(check_job, 'cron', day='*', hour="0", minute="10", args=[
        daily_report_data, temp_report_data
    ], misfire_grace_time=300)
    print("job started")
    scheduler_report.start()
    if server_url is not None:
        requests.get(url=server_url+f'我挂了')
