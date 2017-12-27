# -*- coding:utf-8 -*-

import requests
import re
import xlwt


ff = 'd:/1.txt'


class checkall(object):
    URL='http://replace your ip domain/gwyquery/publicQuery/gzwbkrsssquery'
    POST = {
        'yhid':'',
        'pxdm':'0',
        'zwdm':'',
        'page':'',
        'pageSize':'50'
    }

    def __init__(self):
        self.a = requests.session()

    def getdata(self, num):
        while True:
            try:
                self.POST['page'] = str(num)
                b = self.a.post(self.URL, data=self.POST,timeout=2)
                c = re.findall('<table class=\"table1\" id=\"tbl\">([\d\D]*?)</table>', b.text)
                return c
            except:
                pass


if __name__ == '__main__':
    a = checkall()
    output = open('1.txt', 'w+')
    for i in range(1, 43):
        print('Process Page %d ...' % i)
        b = a.getdata(i)
        c = re.findall('<tr>([\w\W]*?)</tr>', b[0])
        for j in range(1, len(c)):
            d = re.findall('<td>([\w\W]*?)</td>', c[j])
            output.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (d[0],d[1],d[2],d[3],d[4],d[5],d[6]))
    output.close()

    
