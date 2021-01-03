import datetime
import time

from main import daily_check, Reportor
from js_code.exejs import compile_js, js_from_file
from personal_info import daily_report_data, temp_report_data, login_data

times = 365  # 你要打未来多少天的卡

if __name__ == "__main__":
    js_program = compile_js("js_code/encrypt.js")
    reportor = Reportor(login_data['username'], login_data['password'], js_program)
    reportor.login()
    reported_date = []
    for days in range(times):
        date_str = (datetime.datetime.now()+datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        print("当前时间：" + str(datetime.datetime.now()))
        print("打卡时间：" + date_str)
        print()
        if date_str not in reported_date:
            reported_date.append(
                daily_check(reportor, date_str, daily_report_data, temp_report_data)
            )
        # time.sleep(1)