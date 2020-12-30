import requests
import json
import re

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

temp_report_data = {
    "WID": "",
    "CZZ": "",
    "CZZXM": "",
    "CZRQ": "",
    "USER_ID": "202021080612",
    "USER_NAME": "杨中宇",
    "DEPT_CODE": "1008",
    "DEPT_NAME": "计算机科学与工程学院（网络空间安全学院）",
    "NEED_DATE": "2020-12-29",
    "DAY_TIME_DISPLAY": "中午",
    "DAY_TIME": "1",
    "TEMPERATURE": "36",
    "CREATED_AT": "2020-12-29 13:56",
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

        res = requests.get(self.login_url)
        # res = requests.get("https://www.baidu.com")
        res.encoding = 'utf-8'
        # 密码加密
        pwdDefaultEncryptSalt = re.search(r'pwdDefaultEncryptSalt = "(?P<EncryptSalt>\w+)"', res.text)["EncryptSalt"]
        EncryptedpassWord = js_program.call("_etd2", self.password, pwdDefaultEncryptSalt)

        # print("[debug] json.loads(r.text): ", json.loads(res.text))
        # data = {
        #     "userName": self.username,
        #     "passWord": EncryptedpassWord,
        #     "lt": "LT-1139506-PXYfWYjKB7pDEJTWYt0Adudlq3ZRge1609224254142-qPry-cas",
        #     "dllt": "userNamePasswordLogin",
        #     "execution": "e2s1",
        #     "_eventId": "submit",
        #     "rmShown": "1",
        #     "sign": "49300c2949a111eb9925c70ba008df64",
        # }
        # headers = {
        #     "Host": "idas.uestc.edu.cn",
        #     "Origin": "https://idas.uestc.edu.cn",
        #     "Referer": "https://idas.uestc.edu.cn/authserver/login?service=http%3A%2F%2Feportal.uestc.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Feportal.uestc.edu.cn%2Fnew%2Findex.html",
        #     "Upgrade-Insecure-Requests": "1",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        # }

        headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Accept-Language": "en-CN,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
        #     "Connection": "keep-alive",
            "Cookie": "route=c15b6c7b18cc91511f70ceb25a6181ef; EMAP_LANG=zh; THEME=indigo; _WEU=rz9GnA*xZpsAzc7ih8CqUah56Flr_II5zO*uDBeQEZog852gIzAGEmqgtdMJvsjOh_,qI1xLUEpRdCoetCv1SgbGMPRpLIo6jNuWiJNIIymhLYurw0tfb2CKnFdrVoB8jZIRJ4_HoobEizvQrEEx1ho..; UM_distinctid=173e80bcaa72ad-0b0ee79ee1885-3323767-384000-173e80bcaa81f1; route=30dfce7b7500cd543e989b26cda7c8b4; amp.locale=undefined; iPlanetDirectoryPro=N27wu2ftImmZG6MBWa2MCl; JSESSIONID=HyOyNnrZjXBs0GnthAUmrcff4mSPxRiJDscLPaKssX8QogHSALB6!1919497788; MOD_AUTH_CAS=MOD_AUTH_ST-819820-AMu9rLmrFwIAAZYGnX951609307735246-xnsO-cas; zg_did=%7B%22did%22%3A%20%221748211195f8c3-03dd903451f49a-333769-384000-1748211196043%22%7D; zg_=%7B%22sid%22%3A%201609307685865%2C%22updated%22%3A%201609307761080%2C%22info%22%3A%201608887637225%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22202021080612%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201609307685865%7D",
            # "Host": "eportal.uestc.edu.cn",
            # "Upgrade-Insecure-Requests": "1",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        }
        # try:
        res = self.sess.get(self.daily_report_url, headers=headers)
        #     # res = self.sess.get()
        #     res.raise_for_status()
        # except Exception as err:
        #     print("[error] ({}): {}".format(res.status_code, res.text))
        #     raise
        # else:
        #     print(res)
        #     # print("[debug] json.loads(r.text): ", json.loads(res.text))
        data = {
            "WID": "",
            "CZZ": "",
            "CZZXM": "",
            "CZRQ": "",
            "USER_ID": "202021080612",
            "USER_NAME": "杨中宇",
            "DEPT_CODE": "1008",
            "DEPT_NAME": "计算机科学与工程学院（网络空间安全学院）",
            "NEED_DATE": "2020-12-30",
            "DAY_TIME_DISPLAY": "中午",
            "DAY_TIME": "2",
            "TEMPERATURE": "36",
            "CREATED_AT": "2020-12-30 16:26",
        }
        headers = {
            # "Accept": "application/json, text/javascript, */*; q=0.01",
            # "Accept-Encoding": "gzip, deflate",
            # "Accept-Language": "en-CN,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
            # "Connection": "keep-alive",
            # "Content-Length": "45",
            # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "route=c15b6c7b18cc91511f70ceb25a6181ef; EMAP_LANG=zh; THEME=indigo; _WEU=rz9GnA*xZpsAzc7ih8CqUah56Flr_II5zO*uDBeQEZog852gIzAGEmqgtdMJvsjOh_qI1xLUEpRdCoetCv1SgbGMPRpLIo6jNuWiJNIIymhLYurw0tfb2CKnFdrVoB8jZIRJ4_HoobEizvQrEEx1ho..; UM_distinctid=173e80bcaa72ad-0b0ee79ee1885-3323767-384000-173e80bcaa81f1; route=30dfce7b7500cd543e989b26cda7c8b4; amp.locale=undefined; iPlanetDirectoryPro=N27wu2ftImmZG6MBWa2MCl; JSESSIONID=HyOyNnrZjXBs0GnthAUmrcff4mSPxRiJDscLPaKssX8QogHSALB6!1919497788; MOD_AUTH_CAS=MOD_AUTH_ST-819820-AMu9rLmrFwIAAZYGnX951609307735246-xnsO-cas; zg_did=%7B%22did%22%3A%20%221748211195f8c3-03dd903451f49a-333769-384000-1748211196043%22%7D; zg_=%7B%22sid%22%3A%201609307685865%2C%22updated%22%3A%201609307771250%2C%22info%22%3A%201608887637225%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22202021080612%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201609307685865%7D",
            # "Host": "eportal.uestc.edu.cn",
            # "Origin": "http://eportal.uestc.edu.cn",
            # "Referer": "http://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/index.do?",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            # "X-Requested-With": "XMLHttpRequest",
        }
        res = self.sess.post(self.temp_report_url, data=data, headers=headers)
        print(res)
        res.encoding = 'utf-8'
        print(res.text)
        # print(json.loads(res.text))

    def daily_report(self):
        return

    def temp_report(self):
        return

if __name__ == "__main__":
    js_program = compile_js("js_code/encrypt.js")
    # a = js_program.call("add", 1, 2)
    # print(a)
    username = "202021080612"
    password = "sdfasdfsdf"
    reportor = Reportor(username, password, js_program)
    reportor.login()
    print()
