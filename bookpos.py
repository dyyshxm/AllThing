# -*- coding:utf-8 -*-

import requests
import datetime
import re
import time
import threading

TIMEOUT = 2

def dprint(strp, chLine=True):
    if chLine:
        print("[%s LIN] %s" % (datetime.datetime.now(), strp))
    else:
        print("[%s LIN] %s" % (datetime.datetime.now(), strp), end='')

class bookman(object):
    username = "replace your id"
    password = "replace your password"
    LOGIN_URL = "http://your ipaddr/Default.aspx"
    QUEST_URL = "http://your ipaddr/FunctionPages/SeatBespeak/SeatLayoutHandle.ashx"
    REGISTER_URL = "http://your ipaddr/FunctionPages/SeatBespeak/BespeakSubmitWindow.aspx?parameters="
    DELAY_URL = "http://your ipaddr/FunctionPages/SeatBespeak/BespeakSelfSeat.aspx"
    HEADER = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': "en-US,en;q=0.5",
            'Content-Type': 'application/x-www-form-urlencoded',
    }
    REGISTER_HEADER = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    POST = {
            "__EVENTTARGET": '',
            "__EVENTARGUMENT": '',
            "__VIEWSTATE": "/wEPDwUKMTc2NzMyNTQ1NGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFBWNtZE9LMXUK2xtmp49P/wA0Th865ANJutBZnjujJAbadV0majc=",
            "__VIEWSTATEGENERATOR": "CA0B0334",
            "__PREVIOUSPAGE": "9ognCWjeg_DjXdpnxqjd2qJGwVF9ss2hhblP5GRP0wqWzkW6Uh0VagwBV2atgy1rj5m3N9iCLgfPT8LwhgbsMDACGkp2OKgywtUYUGMhnqE1",
            "__EVENTVALIDATION": "/wEWBAK90p4+AqXVsrMJArWptJELAuCKqIUOHPRewF0PlbJOiE/TaF3y5AKfFQGCniqS3tbXGEXwJcU=",
            "txtUserName": '',
            "txtPassword": '',
            "cmdOK.x": "45",
            "cmdOK.y": "3",
    }
    QUEST_POST = {
            "roomNum": "201001", #replace your Room Number
            "date": ""
    }
    REGISTER_POST = {
            "__EVENTTARGET": "ContentPanel1$btnBespeak",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": "/wEPDwULLTExNDEyODQ3MDVkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYHBQVGb3JtMgUURm9ybTIkY3RsMDMkcmJsTW9kZWwFIUZvcm0yJGN0bDA0JERyb3BEb3duTGlzdF9GcmVlVGltZQUdRm9ybTIkY3RsMDUkRHJvcERvd25MaXN0X1RpbWUFDUNvbnRlbnRQYW5lbDEFGENvbnRlbnRQYW5lbDEkYnRuQmVzcGVhawUWQ29udGVudFBhbmVsMSRidG5DbG9zZcavvh55RGcCMM9K0zJaNDRaZVKkO6wH008bMm4J4EWB",
            "__VIEWSTATEGENERATOR": "55344565",
            "__EVENTVALIDATION": "/wEWAgKDgpjgCwL+mI+WBlC/x6o71VDID5vaeu2Zh8hwUExR8i/qlQS08dCKAGLT",
            "roomOpenTime": "7:00",
            "Form2$ctl03$rblModel": "0",
            "Form2$ctl04$DropDownList_FreeTime": "7:10",
            "Form2$ctl05$DropDownList_Time": "10:00",
            "X_CHANGED": "false",
            "X_TARGET": "ContentPanel1_btnBespeak",
            "Form2_Collapsed": "false",
            "ContentPanel1_Collapsed": "false",
            "X_STATE": "eyJGb3JtMl9jdGwwMF9sYmxSb29tTmFtZSI6eyJUZXh0Ijoi5LqM5bGC5Lit5paH56eR5oqA5Zu+5Lmm6ZiF6KeI5Yy6In0sIkZvcm0yX2N0bDAxX2xibFNlYXRObyI6eyJUZXh0IjoiNDEzIn0sIkZvcm0yX2N0bDAyX2xibGJlZ2luRGF0ZSI6eyJUZXh0IjoiMjAxNy0xMC0yMSJ9LCJGb3JtMl9jdGwwM19yYmxNb2RlbCI6eyJIaWRkZW4iOnRydWV9LCJGb3JtMl9jdGwwNF9Ecm9wRG93bkxpc3RfRnJlZVRpbWUiOnsiSGlkZGVuIjp0cnVlLCJYX0l0ZW1zIjpbWyI3OjEwIiwiNzoxMCIsMV0sWyI3OjIwIiwiNzoyMCIsMV0sWyI3OjMwIiwiNzozMCIsMV0sWyI3OjQwIiwiNzo0MCIsMV0sWyI3OjUwIiwiNzo1MCIsMV0sWyI4OjAwIiwiODowMCIsMV0sWyI4OjEwIiwiODoxMCIsMV0sWyI4OjIwIiwiODoyMCIsMV0sWyI4OjMwIiwiODozMCIsMV0sWyI4OjQwIiwiODo0MCIsMV0sWyI4OjUwIiwiODo1MCIsMV0sWyI5OjAwIiwiOTowMCIsMV0sWyI5OjEwIiwiOToxMCIsMV0sWyI5OjIwIiwiOToyMCIsMV0sWyI5OjMwIiwiOTozMCIsMV0sWyI5OjQwIiwiOTo0MCIsMV0sWyI5OjUwIiwiOTo1MCIsMV0sWyIxMDowMCIsIjEwOjAwIiwxXSxbIjEwOjEwIiwiMTA6MTAiLDFdLFsiMTA6MjAiLCIxMDoyMCIsMV0sWyIxMDozMCIsIjEwOjMwIiwxXSxbIjEwOjQwIiwiMTA6NDAiLDFdLFsiMTA6NTAiLCIxMDo1MCIsMV0sWyIxMTowMCIsIjExOjAwIiwxXSxbIjExOjEwIiwiMTE6MTAiLDFdLFsiMTE6MjAiLCIxMToyMCIsMV1dLCJTZWxlY3RlZFZhbHVlIjoiNzoxMCJ9LCJGb3JtMl9jdGwwNV9Ecm9wRG93bkxpc3RfVGltZSI6eyJIaWRkZW4iOnRydWUsIlhfSXRlbXMiOltbIjEwOjAwIiwiMTA6MDAiLDFdLFsiMTI6MDAiLCIxMjowMCIsMV1dLCJTZWxlY3RlZFZhbHVlIjoiMTA6MDAifSwiRm9ybTJfY3RsMDZfbGJsRW5kRGF0ZSI6eyJUZXh0IjoiNjo0MOiHszg6MzAifX0=",
            "X_AJAX": "true",
    }
    DELAY_POST = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": "/wEPDwUKMTA4NDY1MTI5OA9kFgICAw9kFgICAw9kFgYCAQ8PFgIeBFRleHQFGeS4gOWxguaKpeWIiumYheiniOWMuiAwNjNkZAIDDw8WAh8ABQblnKjluqdkZAIFDw8WAh8ABRIyMDE3LTExLTUgMTc6NTY6MDlkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUPU2VhdFRpbWVTZXR0aW5nVWa5KNGxZPLAeK7gnrCZ/b3eb9JukdH2rfFqZTIrMtE=",
            "__VIEWSTATEGENERATOR": "0247C0F2",
            "__EVENTVALIDATION": "/wEWBAL83pXdCgL13qmuCQLoqobNBwLQ7urRBVMI8hWcVn0P9U82OADez3WOTYoxVWGpE340Jgft5Dw+",
            "SeatTimeSetting$btnDelayTime": "续时",
            "X_CHANGED": "false",
    }
    isBooked = False

    def __init__(self):
        self.seson = requests.session()
        self.POST["txtUserName"] = self.username
        self.POST["txtPassword"] = self.password

    def delayBookTime(self):
        r1 = self.seson.get(self.LOGIN_URL, headers=self.HEADER, timeout=TIMEOUT)
        strTime = r1.headers["Date"]
        dt=datetime.datetime.strptime(strTime, "%a, %d %b %Y %H:%M:%S %Z")
        return (8-dt.hour-1)*3600+(60-dt.minute-1)*60+(60-dt.second)

    def delayDelayTime(self):
        self.login()
        re5 = self.seson.get(self.DELAY_URL, headers=self.HEADER, timeout=TIMEOUT)
        strdtnow = re5.headers["Date"]
        dtnow=datetime.datetime.strptime(strdtnow, "%a, %d %b %Y %H:%M:%S %Z") + datetime.timedelta(hours=8)
        strdtpre = re.search('<span id="lblHoldTime">(.*?)</span>', re5.text).group(1)
        if strdtpre == '':
            return -1000
        dtpre=datetime.datetime.strptime(strdtpre, "%Y-%m-%d %H:%M:%S")
        dtcount = 3600*5 - 60*15 - (dtnow.hour-dtpre.hour)*3600 - (dtnow.minute-dtpre.minute)*60 - (dtnow.second-dtpre.second)
        return dtcount

    def login(self):
        re1 = self.seson.get(self.LOGIN_URL, headers=self.HEADER, timeout=TIMEOUT)
        re2 = self.seson.post(self.LOGIN_URL, headers=self.HEADER, data=self.POST, timeout=TIMEOUT)
        confinf = re.findall(r"读者状态", re2.text)
        if confinf :
            dprint('登录成功！')
            return True
        else:
            dprint('登录失败~~')
            return False

    def getKey(self):
        dt = datetime.datetime.now() + datetime.timedelta(days=1)
        dt2 = dt.strftime("%Y-%m-%d") + " 00:00:00"
        self.QUEST_POST['date'] = dt2
        re3 = self.seson.post(self.QUEST_URL, headers=self.REGISTER_HEADER, data=self.QUEST_POST, timeout=TIMEOUT)
        if self.username in re3.text:
            self.isBooked = True
        position_dicts = self.del_response(re3.text)
        return position_dicts

    def getSit(self, pos, posKey):
        if posKey.__contains__(pos) and posKey[pos] != '':
            REAL_REGISTER_URL = self.REGISTER_URL + posKey[pos]
            re4 = self.seson.post(REAL_REGISTER_URL, headers=self.REGISTER_HEADER, data=self.REGISTER_POST, timeout=TIMEOUT)
            dprint('座位 %s '% (pos), chLine=False)
            return self.confsit(re4.text)
        else:
            dprint("座位 %s 不可预约~~" % (pos))
            return False

    def del_response(self, request):
        sit_values = re.findall(r"BespeakSeatClick\(\"(.*?)\"\)\'", request)
        sit_keys = re.findall(r">(\d+)</div>", request)
        return dict(map(lambda x, y: [x, y], sit_keys, sit_values))

    def confsit(self, request):
        confinf = re.findall(r"座位预约成功", request)
        if confinf :
            print('预约成功！')
            return True
        else:
            print('预约失败~~')
            return False

    def bookSit(self):
        # replace your favour Position Number
        posList = ['055','051','031','032','033','061','062','063','043','042','046']
        while not self.isBooked:
            try:
                delaytime = self.delayBookTime()
                if delaytime>0:
                    dprint("预约座位延时%d秒" % (delaytime+3))
                    time.sleep(delaytime+3)
                    dprint("延时结束，开始预约座位……")
                if self.login():
                    gk = self.getKey()
                    if self.isBooked:
                        dprint('已经预约过座位了，去网站查看吧……')
                        break
                    for pos in posList:
                        if self.getSit(pos, gk):
                            self.isBooked = True
                            break
                        time.sleep(1)
            except:
                dprint('预约座位失败，稍后3秒后重试……')
                time.sleep(3)

    def delaySit(self):
        while True:
            try:
                dtcount = self.delayDelayTime()
                if dtcount>=0:
                    dprint("续时座位延时%d秒" % (dtcount))
                    time.sleep(dtcount)
                    dprint("延时结束，开始续时座位……")
                elif dtcount<-900:
                    dprint('注意：无座位，退出续时~~')
                    break
                else:
                    pass
                if self.login():
                    re6 = self.seson.get(self.DELAY_URL, headers=self.HEADER, timeout=TIMEOUT)
                    re7 = self.seson.post(self.DELAY_URL, headers=self.HEADER, data=self.DELAY_POST, timeout=TIMEOUT)
                    confinf = re.findall(r"续时成功", re7.text)
                    if confinf :
                        dprint('续时成功！')
                    else:
                        dprint('续时失败~~')
            except:
                dprint('续时出现一些错误，5秒后重试……')
                time.sleep(5)

if __name__ == "__main__":
    test = bookman()
    t = threading.Thread(target=test.delaySit)
    t.start()
    test.bookSit()
    if t.isAlive():
        t.join()
    pass

