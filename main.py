import requests
import json
import re
from datetime import datetime
import time
from selenium import webdriver
from personInfo import personalData,loginData

from js_code.exejs import compile_js


NEED_DATE = datetime.now().strftime("%Y-%m-%d")
daily_report_data = {
    "WID": "B61E9C2E82A9EEDAE053D3A4C5DE9CA4",
    "NEED_CHECKIN_DATE": NEED_DATE,
    "DEPT_CODE": "1008",
    "CZR": "",
    "CZZXM": "",
    "CZRQ": NEED_DATE+" 00:00:00",
    "USER_ID": "202022081231",
    "USER_NAME": "贾黄春",
    "DEPT_NAME": "计算机科学与工程学院（网络空间安全学院）",
    "GENDER_CODE": "男",
    "AGE": "21",
    "PHONE_NUMBER": "15621038103",
    "IDCARD_NO": "370783199708090018",
    "LB": "全日制学术硕士",
    "PERSON_TYPE_DISPLAY": "留校",
    "PERSON_TYPE": "001",
    "TUTOR": "段立新",
    "LOCATION_PROVINCE_CODE_DISPLAY": "四川省",
    "LOCATION_PROVINCE_CODE": "510000",
    "LOCATION_CITY_CODE_DISPLAY": "成都市",
    "LOCATION_CITY_CODE": "510100",
    "LOCATION_COUNTY_CODE_DISPLAY": "郫都区",
    "LOCATION_COUNTY_CODE": "510117",
    "LOCATION_DETAIL": "电子科技大学清水河校区",
    "HEALTH_STATUS_CODE_DISPLAY": "正常",
    "HEALTH_STATUS_CODE": "001",
    "HEALTH_UNSUAL_CODE": "",
    "IS_HOT_DISPLAY": "否",
    "IS_HOT": "0",
    "IS_IN_HB_DISPLAY": "否",
    "IS_IN_HB": "0",
    "IS_HB_BACK_DISPLAY": "否",
    "IS_HB_BACK": "0",
    "IS_DEFINITE_DISPLAY": "否",
    "IS_DEFINITE": "0",
    "IS_QUARANTINE_DISPLAY": "否",
    "IS_QUARANTINE": "0",
    "IS_KEEP_DISPLAY": "否",
    "IS_KEEP": "0",
    "TEMPERATURE": "",
    "IS_SEE_DOCTOR_DISPLAY": "否",
    "IS_SEE_DOCTOR": "NO",
    "IS_IN_SCHOOL_DISPLAY": "是",
    "IS_IN_SCHOOL": "1",
    "MEMBER_HEALTH_STATUS_CODE_DISPLAY": "正常",
    "MEMBER_HEALTH_STATUS_CODE": "001",
    "MEMBER_HEALTH_UNSUAL_CODE_DISPLAY": "",
    "MEMBER_HEALTH_UNSUAL_CODE": "",
    "REMARK": "",
    "SAW_DOCTOR_DESC": "",
}

headers = {
    "Cookie": "route=c15b6c7b18cc91511f70ceb25a6181ef; EMAP_LANG=zh; THEME=indigo; _WEU=71ksOTcMX9DFDrNJgfBF4RFOTFeR5CPeaXTqYz1gu2pepJsfvNqWd1MLC3CSgButh5E3mBGCR1Zz6VDBxHzZ69_4XaHYkX25TJw2KBDm5KpQeX8AgpaKmG9Lv*p1hSdo70EJ2ohedPV3O1b6VP9WIS..; route=07f03ed1ed6e496f5392b5b234387177; UM_distinctid=174a121f5f4258-0423c1b268e18d-316e7004-1fa400-174a121f5f5d78; III_EXPT_FILE=aa3199; III_SESSION_ID=acf0f32366ee6d1aa904abe32ee40bd7; SESSION_LANGUAGE=eng; iPlanetDirectoryPro=0TqCamXHO3uon41IguQJ6y; MOD_AUTH_CAS=MOD_AUTH_ST-567976-XtCo2CkRoeep9fzUN2QX1609393032068-jByq-cas; asessionid=0f94523f-63b2-4d5c-9771-377ffcf5593b; amp.locale=undefined; JSESSIONID=Y463TObSmJkgPdbijqlNU_GY9cH66C-oV7fdRy45r1qu1h-7Boe8!1919497788; zg_did=%7B%22did%22%3A%20%22176b3c694a4616-046447613bcd5c-6d112d7c-1fa400-176b3c694a5f42%22%7D; zg_=%7B%22sid%22%3A%201609392217321%2C%22updated%22%3A%201609393037478%2C%22info%22%3A%201609333904555%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22eportal.uestc.edu.cn%22%2C%22cuid%22%3A%20%22202022081231%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201609392217321%7D",
}
data = {
    "USER_ID": "202022081231",
    "USER_NAME": "贾黄春",
    "DEPT_NAME": "计算机科学与工程学院（网络空间安全学院）",
    "DEPT_CODE": "1008",
}

class Reportor(object):

    def __init__(self, username, password, js_program):
        self.username = username
        self.password = password
        self.js_program = js_program
        self.login_url = "https://idas.uestc.edu.cn/authserver/login"
        self.daily_report_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/index.do?#/dailyReport"
        self.temp_report_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/index.do?#/tempReport"
        self.sess = requests.Session()
        # self.driver = webdriver.Chrome()

    def login(self):
        # res = requests.get(self.login_url)
        # res.encoding = 'utf-8'
        # # 密码加密
        # pwdDefaultEncryptSalt = re.search(r'pwdDefaultEncryptSalt = "(?P<EncryptSalt>\w+)"', res.text)["EncryptSalt"]
        # EncryptedpassWord = js_program.call("_etd2", self.password, pwdDefaultEncryptSalt)
        self.driver.get(self.login_url)
        time.sleep(10)
        js = """
            var casLoginForm = document.getElementById("casLoginForm");
            var username = document.getElementById("username");
            var password = document.getElementById("password");
            username.value = ""
            password.value = ""
            _etd2(password.value, document.getElementById(
                "pwdDefaultEncryptSalt").value);
            casLoginForm.submit();
            """
        self.driver.execute_script(js)
        time.sleep(20)
        name = self.driver.find_element_by_xpath(
            '/html/body/div[5]/div[2]/div[2]')
        info = self.driver.find_element_by_css_selector(
            '.bh-headerBar-userInfo-detail > div:nth-child(2)')
        cookie = self.driver.get_cookies()
        print(cookie)
        # headers.cookie = cookie
        return name.text

    def daily_report(self):
        if True:
            # save
            daily_report_save_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/modules/dailyReport/T_REPORT_EPIDEMIC_CHECKIN_YJS_SAVE.do?"
            for key in daily_report_data.keys():
                daily_report_save_url += (key + "=" + daily_report_data[key] + "&")
            daily_report_save_url = daily_report_save_url[:-1]

            res = self.sess.post(daily_report_save_url, headers=headers)
            res.encoding = 'utf-8'
            print(res.text)
            print("daily report sucessful")
            return 0  # 打卡成功
        else:
            return 1  # 打卡失败

    def temp_report(self, DAY_TIME):
        DAY_TIME_DISPLAY = {
            "1": "早上",
            "2": "中午",
            "3": "晚上",
        }
        data.update({
            "TEMPERATURE": "36",
            "DAY_TIME": DAY_TIME,
            "DAY_TIME_DISPLAY": DAY_TIME_DISPLAY[DAY_TIME],
            "NEED_DATE": NEED_DATE,
            "WID": "",
            # "CREATED_AT":"2020-12-31+19:03",
        })

        # check
        temp_report_check_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/getMyTempReportDatas.do?"
        temp_report_check_url += ("USER_ID=" + data["USER_ID"] + "&")
        temp_report_check_url += (NEED_DATE + "&")
        temp_report_check_url += ("DAY_TIME=" + DAY_TIME)

        res = self.sess.post(temp_report_check_url, headers=headers)
        res.encoding = 'utf-8'
        # print(res.text)
        if re.search('"NEED_DATE":"{}","DAY_TIME":"{}"'.format(NEED_DATE, DAY_TIME), res.text) is not None:
            print("temp report {} sucessful".format(DAY_TIME))
            return int(DAY_TIME)
        elif re.search("<title>统一身份认证</title>", res.text):
            print("Cookie失效")
            exit(0)

        # save
        temp_report_save_url = "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/T_REPORT_TEMPERATURE_YJS_SAVE.do?"
        for key in data.keys():
            temp_report_save_url += (key + "=" + data[key] + "&")
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

if __name__ == "__main__":
    js_program = compile_js("js_code/encrypt.js")
    reportor = Reportor(loginData['username'], loginData['password'], js_program)
    # reportor.login()

    reported_date = []
    while True:
        date_str = datetime.now().strftime("%Y-%m-%d")
        if date_str not in reported_date:
            r_value_list = []
            # 平安打卡
            while(reportor.daily_report()):
                continue
            # 体温上报
            for id in range(1, 4):
                while(id not in r_value_list):
                    r_value_list.append(reportor.temp_report(str(id)))
            # 四项打卡全部完成
            reported_date.append(date_str)
            print("day {} report complete!\n".format(date_str))
        time.sleep(36000)
    print()
