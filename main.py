import requests
import os
import webbrowser
from time import sleep, localtime, strftime
import pyautogui
from pyperclip import copy, paste

x=0
shortcutsNow=0
shortcutsWas=0
isFirstCheck=False
shortcutsArr=[]
with open('channel.txt','r') as j:
    channel = str(j.read()) + "/videos?view=0&sort=da&flow=grid"
while True:
    myfile = requests.get(channel)
    temp_file_create=open("tmp_file", 'wb')
    temp_file_create.write(myfile.content)
    temp_file_create.close()

    f=open("tmp_file", encoding="utf-8")
    for line in f:
        shortcutCountingStr=str(line)
        howManyShortcutsInStr=shortcutCountingStr.count('watch?')
        while howManyShortcutsInStr>0:
            startLn='"url":"/watch?v='
            endLn='","webPageType":"WEB_PAGE_TYPE_WATCH"'
            pattern = shortcutCountingStr[shortcutCountingStr.find(startLn)+16:shortcutCountingStr.find(endLn)]
            shortcutCountingStr=shortcutCountingStr.replace('"url":"/watch?v=' + pattern + '","webPageType":"WEB_PAGE_TYPE_WATCH"','')
            howManyShortcutsInStr-=1
            if pattern not in shortcutsArr:
                shortcutsArr.append(pattern)

    t = localtime()
    time_now = strftime("%D %H:%M:%S", t)

    shortcutsNow=len(shortcutsArr)

    if shortcutsNow <= shortcutsWas or isFirstCheck == False:
        print(str(shortcutsNow)+" videos, "+time_now)
        with open('log.txt','a') as logFile:
            logFile.write("\n"+str(shortcutsNow)+" videos, "+time_now)
    else:
        print(str(shortcutsNow)+" videos - NEW VIDEO UPLOADED, "+time_now)
        with open('log.txt','a') as logFile:
            logFile.write("\n"+str(shortcutsNow)+" videos - NEW VIDEO UPLOADED, "+time_now)
        webbrowser.open('https://www.youtube.com/watch?v='+shortcutsArr[-1], new = 2)
        with open('msg.txt','r', encoding='utf-8') as msgFile:
            copy(str(msgFile.read()))
        sleep(10)
        pyautogui.FAILSAFE = False
        xy,yy=pyautogui.locateCenterOnScreen('youtube.png', confidence = 0.5)
        pyautogui.moveTo(xy+50,yy+70)
        sleep(1)
        pyautogui.scroll(-500)
        sleep(2)
        xc,yc=pyautogui.locateCenterOnScreen('comment.png', confidence = 0.5)
        pyautogui.moveTo(xc+10,yc+6)
        pyautogui.click()
        sleep(1)
        pyautogui.hotkey('ctrl','v')
        sleep(0.2)
        pyautogui.hotkey('ctrl','enter')
        sleep(0.5)
        pyautogui.hotkey('ctrl','w')

    shortcutsWas = shortcutsNow
    shortcutsNow=0
    f.close()
    os.remove("tmp_file")
    isFirstCheck=True