# 电子科技大学研究生健康状况自动填报

## 免责说明

注意！！！！！仅做学习使用，禁止用来瞒报打卡，违者后果自负

## 2021.12.03更新
学校似乎又修复了登录漏洞，现在发现只有先完成滑块后才能登陆，只有滑块版本能用了。
```bash
python cv_main.py
```
然后推荐一个微信消息在线推送服务：[pushplus](https://pushplus.hxtrip.com/)

将`personal_info.py`中的`server_url`设置为`f"http://pushplus.hxtrip.com/send?token=your_token_of_pushplus&title=打卡通知&template=html&content="`

如果打卡失败或者登陆失败，脚本会将失败的消息推送至你的微信

## 2021.09.05更新：
学校似乎已经修复登录一个账号给所有人打卡的bug，
新版本程序略微修改personal_info.py格式，新增打卡人账号与密码属性。
![改动](readme_imgs/20210905change.png)

## selenium以及geckodriver

需要selenium模块来模拟浏览器操作，需要下载firefox浏览器的[geckodriver](https://github.com/mozilla/geckodriver/releases)。

注：经测试chromedriver无法满足需求

## 配置

配置python环境：`pip install -r requirements.txt`

修改personal_info_demo.py中的webdriver_path的值为你的电脑上geckodriver所在位置。

根据personal_info_demo.py添加自己的信息

personal_info_demo.py更名为personal_info.py

## 运行

### 每日打卡

程序会首先将今天的打卡完成，之后会自动在每日零时登录并打卡

```bash
python main.py
```
![效果图](readme_imgs/2.jpg)

### 一劳永逸

注意：未来体温填报经测试成功，但未来打卡未测试

```bash
python once_for_all.py
```
![效果图](readme_imgs/5.jpg)

## 实现思路
通过chrome的develop tools的network面板在每日打卡填报时候进行抓包，找到进行每日报平安以及体温上报的api。
+ 首先在postman中测试直接请求api是否可行，发现只需要带个人cookie以及报平安以及体温的参数即可。
 
+ 其次还偶然发现并不需要与个人cookie进行绑定才能进行打卡，换言之，只要登录上了，如果有别人的学号和姓名就可通过脚本帮他体温打卡，报平安填的个人参数会更多些也更私人。
    > 只要登录上了就可向体温上报和报平安的数据库中写数据，而这个数据只要符合格式就可，是谁的都可以
    >（以上为个人猜测的后端实现）

+ 对于体温上报的api，每日可以多次体温上报，并不只早中晚各一次，而是无限次，只是在前端做了限制。
    > 前端的逻辑是当点击了体温上报按钮后先调用查询体温上报的api，看当前时段是否打卡过，如果打过则弹窗已经打过结束；
    > 如果没打过，则调用体温打卡的api，打卡当前次，之后再调用一次查询全部体温打卡记录的api刷新整个页面。
  
+ 对于每日报平安的api，也是可以多次报平安，但页面上只显示最近的一次。故猜测后端有两种可能的实现方式，一是当天重复打卡的会覆盖掉上一次的，二是也是打卡无限次，但前端做了处理，只显示当天最近的一次打卡。

- [x] 每日三次体温上报、每日报平安均支持已打卡检测，避免重复打卡

## 待实现

- [ ] 滑块验证码的破解

## 版本说明

main.py(v1.0) 无浏览器页面打开，绕过验证码自动登录，定时打卡

cv_main.py(未完成) 模拟手动滑动验证码登录
