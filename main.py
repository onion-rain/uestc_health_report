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
        # headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "en-CN,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
        #     "Connection": "keep-alive",
        #     "Cookie": "route=b33ccb7ad9a0242cd671775d1be49fa3; FSSBBIl1UgzbN7Nenable=true; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=en; UM_distinctid=173e80bcaa72ad-0b0ee79ee1885-3323767-384000-173e80bcaa81f1; FSSBBIl1UgzbN7N443S=vSFUx8UO_NLszJc6KDO4MAUQObloytlM5z8Il2gLL85kPMYfFnk3sRzFBHkVTwcb; FSSBBIl1UgzbN7N80S=XxEiC7VGTc4OL5oLhjr4ffJZy51Kqm0g3z0V33TiRIbtr7x5wGUX2o6sE8vQUd.p; JSESSIONID=fb2x1BUvrkoRzR0qK8W3l8GrDXF1nRPH-uq4vPwfiO8IWv3PumkO!269640569; zg_did=%7B%22did%22%3A%20%221748211195f8c3-03dd903451f49a-333769-384000-1748211196043%22%7D; zg_=%7B%22sid%22%3A%201609301242389%2C%22updated%22%3A%201609301242394%2C%22info%22%3A%201608887637225%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22202021080612%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201609301242389%7D; FSSBBIl1UgzbN7N443T=4qZXM27TaE3ar3aYGYKTmMzkEa8YPWH0IANkYA9MY41N39mu.jLhcK5COOo_wOG8cgAilGK6.NM3FfwJ67yc0NrO_jwO9qnfa7fATCVYLAtTZXF_apjFweQTsfQLul9E_KDVMRE0GTgyhepCxYwGeWu8b0IhYDSR.tFW8rRNWCCC4PtLM.VCwzPkqX295or6TIOphm5BghVjzBy18fwvyc9RnZX0SVdXVlivVg_XwQQQ1g8xB2Yo8VUoRLF1K.z.Y0OVS9T.61MgytM6JDUxLSM2_DWl.OC6myIPTZun9qnPM8flbzyptSx5zQ1211VVQm.rk9JSVNEC54MTMWipWTcOMxM8SzR4kPtiS_DGQGrO9wa; FSSBBIl1UgzbN7N80T=4XSeGto1VfcRurg5.9R6J6hlc_9DlKGoxh_Y7EK6jyM69v46SgXo5Vo8xxJbn_zMK2EItGG22jMK2RlQQyUYRmIB2UqecnZjytP9NG.e5WlCyN2undoI5.14qy6FXX_WLCDzqKHhcN9C4gQ1_skAhdVfFsK9ayMXfhJZZPcCH3cvuHr_SUKoYtKxh4Q2C2.u1mx_dfz7zFaJ_IVezZW.t02gy3zbtWqRRRHbdDtXwpVLTngGR1Dol.wtEPv0oh2G4QBzQfiVQjT.8iYVFgfuGMzJgVHp6asOPmNXr5G.3SyKOfq",
        #     "Host": "idas.uestc.edu.cn",
        #     "Referer": "http://eportal.uestc.edu.cn/",
        #     "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        #     "sec-ch-ua-mobile": "?0",
        #     "Sec-Fetch-Dest": "document",
        #     "Sec-Fetch-Mode": "navigate",
        #     "Sec-Fetch-Site": "cross-site",
        #     "Sec-Fetch-User": "?1",
        #     "Upgrade-Insecure-Requests": "1",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        # }
        res = requests.get(self.login_url)
        # res = requests.get("https://www.baidu.com")
        res.encoding = 'utf-8'
        # print(res.text)
        pwdDefaultEncryptSalt = re.search(r'pwdDefaultEncryptSalt = "(?P<EncryptSalt>\w+)"', res.text)["EncryptSalt"]
        a = js_program.call("_etd2", self.password, pwdDefaultEncryptSalt)
        print(a)

        # print("[debug] json.loads(r.text): ", json.loads(res.text))
        # data = {
        #     "userName": self.username,
        #     "passWord": "+NT5YlvHSXvE+dXSA1f+D1WiBHDgFGFnIej7q9wVpJbse71XN5kJdzTECn8WVRbGD1vz+2vvAksfdtk6e61eWrPMqYYSep2bsQTLjZe9jQc=",
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
        # try:
        #     res = self.sess.post(self.login_url, data=data, headers=headers)
        #     # res = self.sess.get()
        #     res.raise_for_status()
        # except Exception as err:
        #     print("[error] ({}): {}".format(res.status_code, res.text))
        #     raise
        # else:
        #     print(res)
        #     print("[debug] json.loads(r.text): ", json.loads(res.text))

        # print(json.loads(res.text))

    def daily_report(self):
        return

    def temp_report(self):
        return

if __name__ == "__main__":
    js_program = compile_js("js_code/gas.js")
    # a = js_program.call("add", 1, 2)
    # print(a)
    username = "202021080612"
    password = "sdfasdfsdf"
    reportor = Reportor(username, password, js_program)
    reportor.login()
    print()
