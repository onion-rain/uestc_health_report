import requests
import json
import re
from datetime import datetime
import time
import pickle

from selenium import webdriver
from personal_info import server_url, webdriver_path, daily_report_data, temp_report_data, login_data

from apscheduler.schedulers.blocking import BlockingScheduler


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
        
        # options = webdriver.ChromeOptions()
        # options.add_argument(r"user-data-dir= /Users/shell0108/Library/Application\Support/Google/Chrome/Default")
        # self.driver = webdriver.Chrome(r"/usr/local/bin/chromedriver", options=options)
        options = webdriver.firefox.options.Options()
        options.add_argument('--headless')  # 无窗口
        options.add_argument('--incognito')  # 无痕
        self.driver = webdriver.Firefox(executable_path=webdriver_path, options=options)
        self.login()
        self.update_cookies()

    def login(self):
        print("logging in...\r", end="")
        self.driver.get(self.login_url)
        time.sleep(3)
        js = """
            var casLoginForm = document.getElementById("casLoginForm");
            var username = document.getElementById("username");
            var password = document.getElementById("password");
            username.value = "{}"
            password.value = "{}"
            _etd2(password.value, document.getElementById("pwdDefaultEncryptSalt").value);
            casLoginForm.submit();
        """.format(self.username, self.password)
        self.driver.execute_script(js)
        time.sleep(10)
        try:
            self.driver.find_element_by_xpath("/html/body/header/header[1]/div/div/div[4]/div[1]/img").click()
            username = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]').text
        except Exception:
            raise Exception("登录失败")
        else:
            print("登录账号 ： {}".format(username))

    def update_cookies(self):
        Cookies = self.driver.get_cookies()
        self.driver.quit()
        headers["Cookie"] = cookies2str(Cookies)

    def daily_report(self, NEED_DATE, daily_report_data):
        # 获取WID
        wid_data = {
            'pageNumber': '1',
            'pageSize': '10',
            'USER_ID': daily_report_data["USER_ID"],
        }
        res = requests.post(self.wid_url, data=wid_data, headers=headers)
        res.encoding = 'utf-8'
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
    if server_url is not None:
        requests.get(url=server_url+f'?text={date_str}打卡完成')


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
