import requests
import json
import re
from datetime import datetime
import time

from js_code.exejs import compile_js

 
daily_report_data = {
    "WID": "B63D65084785EE87E053D3A4C5DEA774",
    "NEED_CHECKIN_DATE": "2020-12-29",
    "DEPT_CODE": "1008",
    "CZR": "",
    "CZZXM": "",
    "CZRQ": "2020-12-29 00:00:00",
    "USER_ID": "202021080612",
    "USER_NAME": "杨中宇",
    "DEPT_NAME": "计算机科学与工程学院（网络空间安全学院）",
    "GENDER_CODE": "男",
    "AGE": "23",
    "PHONE_NUMBER": "15520770863",
    "IDCARD_NO": "370684199710050016",
    "LB": "全日制学术硕士",
    "PERSON_TYPE_DISPLAY": "留校",
    "PERSON_TYPE": "001",
    "TUTOR": "薛瑞尼",
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
    "CREATED_AT": "2020-12-29 13:44",
    "SAW_DOCTOR_DESC": "",
}

headers = {  # 根据个人信息自行修改
    "Cookie": "c15b6c7b18cc91511f70ceb25a6181ef; EMAP_LANG=zh; THEME=indigo; _WEU=7p8xCGX4xzNvUUv8Ycxfw5jvmtxyxS*Uqmo8gw355T8MdA3P9y4DZQU16kkzrgmzA*ySr_uJsNstdxY83R3I1QcFAh8Jjv_r4aeOvBCN8xtNMIAHSjywL6wPSi5eiI5xqBPsXXcUXXicT6bU4nEC_S..; UM_distinctid=173e80bcaa72ad-0b0ee79ee1885-3323767-384000-173e80bcaa81f1; route=30dfce7b7500cd543e989b26cda7c8b4; amp.locale=undefined; JSESSIONID=uTezQsfgahKXM5_DSqGlFVDfSAE9mni0IwQblyxh3llyFWlwAxsW!1919497788; asessionid=dbb414d7-a441-4b56-b04f-062d53b1f36b; zg_did=%7B%22did%22%3A%20%221748211195f8c3-03dd903451f49a-333769-384000-1748211196043%22%7D; zg_=%7B%22sid%22%3A%201609334641875%2C%22updated%22%3A%201609335292909%2C%22info%22%3A%201608887637225%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22202021080612%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201609334641875%7D; iPlanetDirectoryPro=VCAFtdpnA7khPP2NkaMlSb; MOD_AUTH_CAS=MOD_AUTH_ST-837935-Iqbj0rrEjVW60h3999Ag1609335588321-xnsO-cas",
}
data = {
    "USER_ID": "202021080612",
    "USER_NAME": "杨中宇",
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

    def login(self):
        # res = requests.get(self.login_url)
        # res.encoding = 'utf-8'
        # # 密码加密
        # pwdDefaultEncryptSalt = re.search(r'pwdDefaultEncryptSalt = "(?P<EncryptSalt>\w+)"', res.text)["EncryptSalt"]
        # EncryptedpassWord = js_program.call("_etd2", self.password, pwdDefaultEncryptSalt)
        return
        
    def daily_report(self):
        if True:
            print("daily report sucessful")
            return 0  # 打卡成功
        else:
            return 1  # 打卡失败

    def temp_report(self, DAY_TIME):

        NEED_DATE = datetime.now().strftime("%Y-%m-%d")
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
    username = "202021080612"
    password = "sdfasdfsdf"
    reportor = Reportor(username, password, js_program)
    reportor.login()
    
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
