import requests
import json
import re
from datetime import datetime
import time
import pickle
from selenium import webdriver
from personal_info import daily_report_data, temp_report_data, login_data

from selenium import webdriver

from js_code.exejs import compile_js, js_from_file


headers = {
    "Cookie": "route=c15b6c7b18cc91511f70ceb25a6181ef; EMAP_LANG=zh; THEME=indigo; _WEU=71ksOTcMX9DFDrNJgfBF4RFOTFeR5CPeaXTqYz1gu2pepJsfvNqWd1MLC3CSgButh5E3mBGCR1Zz6VDBxHzZ69_4XaHYkX25TJw2KBDm5KpQeX8AgpaKmG9Lv*p1hSdo70EJ2ohedPV3O1b6VP9WIS..; route=07f03ed1ed6e496f5392b5b234387177; UM_distinctid=174a121f5f4258-0423c1b268e18d-316e7004-1fa400-174a121f5f5d78; III_EXPT_FILE=aa3199; III_SESSION_ID=acf0f32366ee6d1aa904abe32ee40bd7; SESSION_LANGUAGE=eng; iPlanetDirectoryPro=0TqCamXHO3uon41IguQJ6y; MOD_AUTH_CAS=MOD_AUTH_ST-567976-XtCo2CkRoeep9fzUN2QX1609393032068-jByq-cas; asessionid=0f94523f-63b2-4d5c-9771-377ffcf5593b; amp.locale=undefined; JSESSIONID=Y463TObSmJkgPdbijqlNU_GY9cH66C-oV7fdRy45r1qu1h-7Boe8!1919497788; zg_did=%7B%22did%22%3A%20%22176b3c694a4616-046447613bcd5c-6d112d7c-1fa400-176b3c694a5f42%22%7D; zg_=%7B%22sid%22%3A%201609392217321%2C%22updated%22%3A%201609393037478%2C%22info%22%3A%201609333904555%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22eportal.uestc.edu.cn%22%2C%22cuid%22%3A%20%22202022081231%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201609392217321%7D",
}


def cookies2str(cookies):
    cookie = [item["name"] + "=" + item["value"] for item in cookies ]
    cookiestr = ';'.join(item for item in cookie)
    return cookiestr


class Reportor(object):

    def __init__(self, username, password, js_program):
        self.username = username
        self.password = password
        self.js_program = js_program
        self.login_url = "https://idas.uestc.edu.cn/authserver/login"
        self.login_seccess_url = "https://idas.uestc.edu.cn/authserver/index.do"
        self.daily_report_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/index.do?#/dailyReport"
        self.temp_report_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/index.do?#/tempReport"
        self.sess = requests.Session()

        option = webdriver.ChromeOptions()
        option.add_argument(r"user-data-dir=C:/Users/onion_rain\AppData/Local/Google/Chrome/User Data")
        self.driver = webdriver.Chrome(r"D:/chromedriver.exe", options=option)

    def getUESTCCookies(self):
        self.driver.get(self.login_url)
        while True:
            print("Please login in !")
            time.sleep(3)
            # if login in successfully, url  jump to self.login_seccess_url
            while self.driver.current_url == self.login_seccess_url:
                Cookies = self.driver.get_cookies()
                self.driver.quit()
                cookies_str = cookies2str(Cookies)
                return cookies_str

    # # TODO selenium打开网页用户进行登录以获取cookie
    # def login(self):
    #     cookies_str = self.getUESTCCookies()
    #     headers["Cookie"] = cookies_str

    # # TODO request输入密码登录
    # def login(self):
    #     res = requests.get(self.login_url)
    #     res.encoding = 'utf-8'
    #     # 密码加密
    #     pwdDefaultEncryptSalt = re.search(r'pwdDefaultEncryptSalt = "(?P<EncryptSalt>\w+)"', res.text)["EncryptSalt"]
    #     EncryptedpassWord = js_program.call("_etd2", self.password, pwdDefaultEncryptSalt)

    def login(self):
        self.driver.get(self.daily_report_url)
        time.sleep(3)

        # TODO selenium输入密码登录
        # js = js_from_file("js_code/encrypt.js")
        # self.driver.execute_script(js)
        # time.sleep(10)

        try:
            username = self.driver.find_element_by_xpath('//*[@id="row0emapdatatable"]/td[3]/span').text
        except Exception:
            raise Exception("登录失败")
        else:
            print("登录账号 ： {}".format(username))
        Cookies = self.driver.get_cookies()
        self.driver.quit()
        headers["Cookie"] = cookies2str(Cookies)

    def daily_report(self, NEED_DATE, daily_report_data):
        # TODO 验证填报成功
        daily_report_data.update({
            "NEED_CHECKIN_DATE": NEED_DATE,
            "CZRQ": NEED_DATE+" 00:00:00",
        })

        # save
        daily_report_save_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/modules/dailyReport/T_REPORT_EPIDEMIC_CHECKIN_YJS_SAVE.do?"
        for key in daily_report_data.keys():
            daily_report_save_url += (key + "=" + daily_report_data[key] + "&")
        daily_report_save_url = daily_report_save_url[:-1]

        res = self.sess.post(daily_report_save_url, headers=headers)
        res.encoding = 'utf-8'
        print("daily report sucessful")
        return 0  # 打卡成功

    def temp_report(self, NEED_DATE, DAY_TIME, temp_report_data):
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

        # check
        temp_report_check_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/getMyTempReportDatas.do?"
        temp_report_check_url += ("USER_ID=" + temp_report_data["USER_ID"] + "&")
        temp_report_check_url += (NEED_DATE + "&")
        temp_report_check_url += ("DAY_TIME=" + DAY_TIME)

        res = self.sess.post(temp_report_check_url, headers=headers)
        res.encoding = 'utf-8'
        if re.search('"NEED_DATE":"{}","DAY_TIME":"{}"'.format(NEED_DATE, DAY_TIME), res.text) is not None:
            print("temp report {} has finished".format(DAY_TIME))
            return int(DAY_TIME)
        elif re.search("<title>统一身份认证</title>", res.text):
            print("Cookie失效")
            exit(0)

        # save
        temp_report_save_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/T_REPORT_TEMPERATURE_YJS_SAVE.do?"
        for key in temp_report_data.keys():
            temp_report_save_url += (key + "=" + temp_report_data[key] + "&")
        temp_report_save_url = temp_report_save_url[:-1]

        res = self.sess.post(temp_report_save_url, headers=headers)
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


def daily_check(reportor, date_str, daily_report_data, temp_report_data):
    r_value_list = []
    # 平安打卡
    # while(reportor.daily_report(date_str, daily_report_data)):
    #     continue
    # 体温上报
    for id in range(1, 4):
        while(id not in r_value_list):
            r_value_list.append(reportor.temp_report(date_str, str(id), temp_report_data))
    # 四项打卡全部完成
    print("day {} report complete!\n".format(date_str))
    return date_str


if __name__ == "__main__":
    js_program = compile_js("js_code/encrypt.js")
    reportor = Reportor(login_data['username'], login_data['password'], js_program)
    reportor.login()
    reported_date = []
    while True:
        date_str = datetime.now().strftime("%Y-%m-%d")
        print("当前时间：" + str(datetime.now()))
        if date_str not in reported_date:
            reported_date.append(
                daily_check(reportor, date_str, daily_report_data, temp_report_data)
            )
        time.sleep(3600)
