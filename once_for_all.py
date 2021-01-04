import datetime
import time

from main import daily_check, Reportor
from personal_info import daily_report_data, temp_report_data, login_data

times = 2  # 你要打未来多少天的卡

if __name__ == "__main__":
    # 注意！！未来体温填报经测试成功，未来打卡未测试
    reportor = Reportor(login_data['username'], login_data['password'])
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