#!encoding=utf-8
from tkinter import *
import configparser as con
import os
import fx
from tkinter import messagebox
import sys
from datetime import datetime


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


tD = datetime(year=2023, month=6, day=13, hour=8) - datetime.today()
tD = str(tD.days)
screenSize = config['section']['screenSize']  # "310x300+400+00"
wordStyle = config['section']['wordStyle']  # 黑体"
wordSize = int(config['section']['wordSize'])  # 40
buttonWordStyle = config['section']['buttonWordStyle']  # "黑体"
buttonWordSize = int(config['section']['buttonWordSize'])  # 20

window = Tk()
outputText = StringVar()


def showtime():
    tM = 60 - datetime.today().minute
    tS = 60 - datetime.today().second
    if datetime.today().hour > 8:
        tH = 24 - datetime.today().hour + 8
    else:
        tH = 8 - datetime.today().hour
    outputText.set("距离中考\n还有\n{}\n天\n{}时{}分{}秒".format(tD, str(tH), str(tM), str(tS)))
    window.after(1000, showtime)


showtime()
window.config(bg='white')
window.wm_attributes('-transparentcolor', 'white', '-topmost', '0')
window.overrideredirect(True)
window.wm_attributes('-topmost', False)
window.geometry(screenSize)
messagebox.showinfo(title='信息', message="本软件由樱花落制作\n全部代码已经在github上开源")
window.bind('<Button-1>', SaveLastClickPos)
window.bind('<B1-Motion>', Dragging)
lb = Label(window, textvariable=outputText, font=(wordStyle, wordSize), bg='white', fg='#FFFFF0')
# lb.master.attributes('-transparentcolor', 'white')
lb.pack()
Button(window, text='退出', command=tick, font=(buttonWordStyle, buttonWordSize)).pack()
# window.attributes('-alpha', 0.1)
window.mainloop()
