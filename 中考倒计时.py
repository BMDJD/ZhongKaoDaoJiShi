from tkinter import *
import configparser as con
import os
import datetime
import time
from tkinter import messagebox
import sys


def app_path():
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)  # 使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)  # 没打包前的py目录


config = con.ConfigParser()

curPath = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(curPath, r'config.ini')
# pathText = os.path.join(curPath, r'Text.txt')
# print(path)
config.read(filenames=path, encoding='utf-8')

lastClickX = 0
lastClickY = 0


def checkYear(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    else:
        return False


def getDay():
    extraDay = 0
    today = datetime.datetime.today()
    toDay = today.day
    toMon = today.month
    toYear = today.year
    if checkYear(toYear):
        if toMon == 1:
            extraDay = 31 - toDay + 29 + 31 + 30 + 31 + 13
        elif toMon == 2:
            extraDay = 29 - toDay + 31 + 30 + 31 + 13
        elif toMon == 3:
            extraDay = 31 - toDay + 30 + 31 + 13
        elif toMon == 4:
            extraDay = 30 - toDay + 31 + 13
        elif toMon == 5:
            extraDay = 31 - toDay + 13
        elif toMon == 6 and toDay < 13:
            extraDay = 13 - toDay
        else:
            return '上学期好好学习，中考是下学期的事情'
    else:
        if toMon == 1:
            extraDay = 31 - toDay + 29 + 31 + 30 + 31 + 13
        elif toMon == 2:
            extraDay = 28 - toDay + 31 + 30 + 31 + 13
        elif toMon == 3:
            extraDay = 31 - toDay + 30 + 31 + 13
        elif toMon == 4:
            extraDay = 30 - toDay + 31 + 13
        elif toMon == 5:
            extraDay = 31 - toDay + 13
        elif toMon == 6 and toDay < 13:
            extraDay = 13 - toDay
        else:
            return '上学期好好学习，中考是下学期的事情'
    return extraDay


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x, y))


def tick():
    os.system("taskkill /f /im 中考倒计时.exe")
    exit()


# with open(pathText, 'r', encoding='utf-8') as file:
#    outputText = file.read().format('\n', '\n', str(getDay()), '\n')
#    file.close()

outputText = "距离中考{}还有{}{}{}天".format('\n', '\n', str(getDay()), '\n')
screenSize = config['section']['screenSize']  # "310x300+400+00"
wordStyle = config['section']['wordStyle']  # 黑体"
wordSize = int(config['section']['wordSize'])  # 40
buttonWordStyle = config['section']['buttonWordStyle']  # "黑体"
buttonWordSize = int(config['section']['buttonWordSize'])  # 20

window = Tk()
window.config(bg='white')
window.wm_attributes('-transparentcolor', 'white', '-topmost', '0')
window.overrideredirect(True)
window.wm_attributes('-topmost', False)
window.geometry(screenSize)
messagebox.showinfo(title='信息', message="本软件由樱花落制作\n全部代码已经在github上开源")
window.bind('<Button-1>', SaveLastClickPos)
window.bind('<B1-Motion>', Dragging)
lb = Label(window, text=outputText, font=(wordStyle, wordSize), bg='white', fg='#FFFFF0')
# lb.master.attributes('-transparentcolor', 'white')
lb.pack()
Button(window, text='退出', command=tick, font=(buttonWordStyle, buttonWordSize)).pack()
# window.attributes('-alpha', 0.1)
window.mainloop()
