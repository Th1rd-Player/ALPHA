import os
import pyttsx3
import speech_recognition as sr
from fuzzywuzzy import fuzz
import datetime
import win32com.client as wincl
import time
import sqlite3
from progress.bar import IncrementalBar


import site
import calculator
import envelope
import translator

conn = sqlite3.connect(r'DataBase/test-base.db')
cur = conn.cursor()
print("База данных создана и успешно подключена к SQLite")


print("Версия базы данных SQLite: ", cur.execute("select sqlite_version();").fetchall())












command_list = cur.execute("SELECT * FROM com;").fetchall()


total_rows = cur.execute("SELECT count(*) from com;").fetchone()

total_rows = str(total_rows)
total_rows = total_rows.split(",")[0]
total_rows = total_rows.split("(")[1]
total_rows = int(total_rows)


alias = cur.execute("SELECT * FROM alias").fetchall()
tbr_list = cur.execute("SELECT * FROM tbr;").fetchall()
#     alias
alias_list = tuple(alias[0]+alias[1]+alias[2])


with IncrementalBar('Загрузка команд:', max=total_rows) as bar:
    for i in range(total_rows):
        # Do some work
        bar.next()
bar.finish()

mode = 2
"""
    1 Включён,  работа толлько через микрофон 
    2 Включён, работа только через текстовый ввод
    3 Включён, смешаный режим
    
"""

startTime = 0
speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)
r = sr.Recognizer()
m = sr.Microphone(device_index=1)
voice = 'str'


def speak(what):
    print(what)
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(what)

if mode == 1:
    def callback(recognizer, audio):
        try:
            global voice
            voice = recognizer.recognize_google(audio, language="ru-RU").lower()

            print("[log] Распознано: " + voice)

            if voice.startswith(alias_list):
                cmd = voice

                for x in alias_list:
                    cmd = cmd.replace(x, "").strip()

                for x in tbr_list:
                    cmd = cmd.replace(x, "").strip()
                voice = cmd
                # распознаем и выполняем команду
                cmd = recognize_cmd(cmd)
                execute_cmd(cmd['cmd'])


        except sr.UnknownValueError:
            print("[log] Голос не распознан!")
        except sr.RequestError as e:
            print("[log] Неизвестная ошибка, проверьте интернет!")
elif mode == 2:
    def callback(recognizer, audio):
        global voice
        voice = input(":")
        print("[log] Введено: " + voice)
        if voice.startswith(alias_list):
            cmd = voice
            for x in alias_list:
                cmd = cmd.replace(x, "").strip()
            for x in tbr_list:
                cmd = cmd.replace(x, "").strip()
            voice = cmd
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd)


def listen():
    with m as source:
        r.adjust_for_ambient_noise(source)
    stop_listening = r.listen_in_background(m, callback)

    while True:
        time.sleep(0.1)



"""
def recognize_cmd(cmd):
    RC = {'id': '', 'percent': 0}
    for c, v in command_list:
        vrt = fuzz.ratio(cmd, v)
        # print(v, ":",vrt)
        if vrt > RC['percent']:
            RC['id'] = c
            RC['percent'] = vrt
    return RC
"""
def recognize_cmd(cmd):
    RC = {'id': '', 'percent': 0}
    for c, v in command_list:
        vrt = fuzz.ratio(cmd, v)
        print(v, ":",vrt)
        if vrt > RC['percent']:
            print(c)
            RC['id'] = c
            RC['percent'] = vrt
    print(RC)
    return RC['id']



def execute_cmd(cmd):
    global startTime
    if cmd == 11:
        print("SD")
        mode = 1
    elif cmd == 1:
        now = datetime.datetime.now()
        speak("Сейчас {0}:{1}".format(str(now.hour), str(now.minute)))
    elif cmd == 2:
        speak("Секундомер запущен")
        startTime = time.time()
    elif cmd == 3:
        if startTime != 0:
            Time = time.time() - startTime
            speak(f"Прошло {round(Time // 3600)} часов {round(Time // 60)} минут {round(Time % 60, 2)} секунд")
            startTime = 0
        else:
            speak("Секундомер не включен")
    elif cmd == 4:
        print("note")

    elif cmd == 5:
        calc.calculator()
    elif cmd == 6:
        os.system('shutdown -s')
        speak("Выключаю...")
    elif cmd == 7:
        convert.convertation()
    elif cmd == 8:
        browser.browser()
    elif cmd == 9:
        translate.translate()
    elif cmd == 10:
        speak("Пока отлично.")
    else:
        print("Команда не распознана!")

'''
    elif str(cmd) == "2":
        os.system('shutdown -s')
        speak("Выключаю...")
    elif str(cmd) == "3":
        calc.calculator()
    elif str(cmd) == '4':
        convert.convertation()
    elif str(cmd) == '5':
        translate.translate()
    elif str(cmd) == '6':
        anekdot.fun()
    elif str(cmd) == '7':
        browser.browser()
    elif str(cmd) == '8':
        speak("Секундомер запущен")
        startTime = time.time()
    elif str(cmd) == "9":
        if startTime != 0:
            Time = time.time() - startTime
            speak(f"Прошло {round(Time // 3600)} часов {round(Time // 60)} минут {round(Time % 60, 2)} секунд")
            startTime = 0
        else:
            speak("Секундомер не включен")
    elif str(cmd) == '10':
        speak("Пока отлично.")'''
