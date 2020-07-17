#coding=utf-8
#adb connect 127.0.0.1:5555 雷电
#adb connect 127.0.0.1:7555 MUMU模拟器：
#python kuaishou.py #运行
#Ctrl + C 手动停止
#adb kill-server #异常adb devices无列表修复

import time
import os
import sys
import re
import random
type=sys.getfilesystemencoding() #强制UTF-8解码，防止WIN下提示输出乱码
import threading

#获得机器屏幕大小返回数组
def getSize(series):
    screensize = [[0] * 2] * 1
    cmd = 'adb -s {client} shell wm size'.format(client = series)
    print(cmd)
    size_str = os.popen(cmd).read()
    if not size_str:
        print '请安装 ADB 及驱动并配置环境变量'.decode('utf-8').encode(type)
        sys.exit()
    m = re.search(r'(\d+)x(\d+)', size_str)
    if m:
        screensize[0][0] = m.group(2)
        screensize [0][1]= m.group(1)
        return screensize

def rand(x0,x1): # 在x0 x1范围内生成随机两位小数
    a = random.uniform(x0,x1)
    return round(a,2)

def randint(x0,x1): #在x0 x1范围内生成随机整数
    return random.randint(x0,x1)

#屏幕向上滑动，随机防封
def swipeUp(series,screensize,t):
    cmd = 'adb -s {client} shell input touchscreen swipe {x1} {y1} {x1} {y2}'.format(
        client = series,
        x1 = int(int(screensize[0][0]) * rand(0.4,0.5)), #x坐标
        y1 = int(int(screensize[0][1]) * rand(0.4,0.5)), #起始y坐标
        y2 = int(int(screensize[0][1]) * rand(0.7,0.8)) #终点y坐标
        )
    print(cmd)
    os.system(cmd)

def liulan(series):#无限循环看视频
        screensize = getSize(series)
        print "屏幕宽度".decode('utf-8').encode(type),screensize[0][0]
        print "屏幕高度".decode('utf-8').encode(type),screensize[0][1]
        print "进入循环操作...".decode('utf-8').encode(type)
        while True:
            t4 = randint(40,60) #随机看视频时间，防封
            print '等待'.decode('utf-8').encode(type),t4,'秒进入下一个视频'.decode('utf-8').encode(type)
            time.sleep(t4)
            swipeUp(series,screensize,1000)

def piliang(series):
    liulan(series)
    timer = threading.Timer(3, piliang, [series])
    timer.start()

def run():
    reload(sys)
    sys.setdefaultencoding('utf8')
    devices = os.popen('adb devices').read()
    devices_lists = devices.splitlines()
    devices_counts = devices_lists.__len__()
    for i in range(1, devices_counts - 1):
        device_info = devices.splitlines()[i]
        device_series = device_info.split( )[0]
        print '设备ID:'.decode('utf-8').encode(type),device_series
        piliang(device_series)

run()
