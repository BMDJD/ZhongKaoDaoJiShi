#!encoding=utf-8
# 导入 GUI，时间计算，系统函数等库
from tkinter import *
import configparser as con
import os
from tkinter import messagebox
import sys
from datetime import datetime


# Pyinstall打包时的绝对路径
def app_path():
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)  # 使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)  # 没打包前的py目录


# 导入config库
config = con.ConfigParser()

# 读取目录下的config
curPath = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(curPath, r'config.ini')
config.read(filenames=path, encoding='utf-8')

# 以下为取消自带的应用窗口，把不必要的背景转为透明，并且增加移动函数
lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x, y))


# 关闭软件
def tick():
    import subprocess
    cmd = 'taskkill /f /im 中考倒计时.exe'
    res = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exit()


# 读取需要的参数
screenSize = config['section']['screenSize']  # "310x300+400+00"
wordStyle = config['section']['wordStyle']  # 黑体"
wordSize = int(config['section']['wordSize'])  # 40
buttonWordStyle = config['section']['buttonWordStyle']  # "黑体"
buttonWordSize = int(config['section']['buttonWordSize'])  # 20
targetDay = int(config['section']['targetDay'])
targetMonth = int(config['section']['targetMonth'])
targetYear = int(config['section']['targetYear'])
targetHour = int(config['section']['targetHour'])
showSeconds = eval(config['section']['showSeconds'])
showExitButton = eval(config['section']['showExitButton'])
showMessage = eval(config['section']['showMessage'])
n = config['section']['n']
message = str(config['section']['message'])
message = message.replace(n, '\n')
wordWithSecond = config['section']['wordWithSecond']
wordWithSecond = wordWithSecond.replace(n, '\n')
wordWithoutSecond = config['section']['wordWithoutSecond']
wordWithoutSecond = wordWithoutSecond.replace(n, '\n')
tD = datetime(year=targetYear, month=targetMonth, day=targetDay, hour=targetHour) - datetime.today()
tD = str(tD.days)

# 建立窗口
window = Tk()
outputText = StringVar()


# 时间计算
def showtime():
    tM = 59 - datetime.today().minute
    tS = 59 - datetime.today().second
    if datetime.today().hour > 8:
        tH = 24 - datetime.today().hour + 8
    else:
        tH = 8 - datetime.today().hour
    if showSeconds:
        outputText.set(wordWithSecond.format(tD, str(tH), str(tM), str(tS)))
        window.after(1000, showtime)
    else:
        outputText.set(wordWithoutSecond.format(tD))
        window.after(1000, showtime)


# 显示文字
showtime()
window.config(bg='white')
window.wm_attributes('-transparentcolor', 'white', '-topmost', '0')
window.overrideredirect(True)
window.wm_attributes('-topmost', False)
window.geometry(screenSize)

if showMessage:
    messagebox.showinfo(title='!', message=message)

window.bind('<Button-1>', SaveLastClickPos)
window.bind('<B1-Motion>', Dragging)
lb = Label(window, textvariable=outputText, font=(wordStyle, wordSize), bg='white', fg='#FFFFF0')
lb.pack()

if showExitButton:
    Button(window, text='退出', command=tick, font=(buttonWordStyle, buttonWordSize)).pack()

window.mainloop()
