import datetime
import os
import smtplib
import subprocess
import sys
import time
import webbrowser

import cv2
import psutil
import pyjokes
import pyttsx3
import pywhatkit as kit
import requests
import speech_recognition as sr
import speedtest
import wikipedia
import winshell
import wolframalpha
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import QDate, Qt, QTime, QTimer
from PyQt5.QtGui import *
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from twilio.rest import Client

from coraUI import Ui_MainWindow

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 140)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    print(f"stark : {audio}")
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning ")
    elif 12 <= hour < 18:
        speak("Good Afternoon ")
    else:
        speak("Good Evening ")
    assname = "stark"
    speak("I am your Assistant " + assname + " how can i help you")


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('nikhilgattu9@gmail.com', '#Nikhilkumar2000')
    server.sendmail('nikhilgattu9@gmail.com', to, content)
    server.close()


def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apikey=06416390f6324ef8af466e86cb99b4e5'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth"]
    for i in articles:
        head.append(i["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")


def playgame(self):
    speak("Welcome to Tic Tac Toe game!")
    theBoard = {'7': ' ', '8': ' ', '9': ' ',
                '4': ' ', '5': ' ', '6': ' ',
                '1': ' ', '2': ' ', '3': ' '}

    board_keys = []

    for key in theBoard:
        board_keys.append(key)

    def printBoard(board):
        print("                                         " +
              board['7'] + '|' + board['8'] + '|' + board['9'])
        print("                                         "+'-+-+-')
        print("                                         " +
              board['4'] + '|' + board['5'] + '|' + board['6'])
        print("                                         "+'-+-+-')
        print("                                         " +
              board['1'] + '|' + board['2'] + '|' + board['3'])

    def game():

        turn = 'X'
        count = 0

        for i in range(10):
            printBoard(theBoard)
            print("It's your turn," + turn + " Move to which place?")
            speak("It's your turn " + turn + " Move to which place?")

            move = input()
            if move.isdigit():
                if theBoard[move] == ' ':
                    theBoard[move] = turn
                    count += 1
                else:
                    print("That place is already filled.")
                    speak("That place is already filled.")
                    continue

                if count >= 5:
                    if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ':  # across the top
                        printBoard(theBoard)
                        print("\nGame Over.\n")
                        print(" **** " + turn + " won. ****")
                        speak(turn + " won.")
                        break
                    # across the middle
                    elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ':
                        printBoard(theBoard)
                        print("\nGame Over.\n")
                        print(" **** " + turn + " won. ****")
                        speak(turn + " won.")
                        break
                    # across the bottom
                    elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ':
                        printBoard(theBoard)
                        print("\nGame Over.\n")
                        print(" **** " + turn + " won. ****")
                        speak(turn + " won.")
                        break
                    # down the left side
                    elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ':
                        printBoard(theBoard)
                        print("\nGame Over.\n")
                        print(" **** " + turn + " won. ****")
                        speak(turn + " won.")
                        break
                    elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ':  # down the middle
                        printBoard(theBoard)
                        print("\nGame Over.\n")
                        print(" **** " + turn + " won. ****")
                        speak(turn + " won.")
                        break
                    # down the right side
                    elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ':
                        printBoard(theBoard)
                        print("\nGame Over.\n")
                        print(" **** " + turn + " won. ****")
                        speak(turn + " won.")
                        break
                    elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ':  # diagonal
                        printBoard(theBoard)
                        print("\nGame Over.\n")
                        print(" **** " + turn + " won. ****")
                        speak(turn + " won.")
                        break
                    elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ':  # diagonal
                        printBoard(theBoard)
                        print("\nGame Over.\n")
                        print(" **** " + turn + " won. ****")
                        speak(turn + " won.")
                        break

                if count == 9:
                    print("\nGame Over.\n")
                    print("It's a Tie!!")
                if turn == 'X':
                    turn = 'O'
                else:
                    turn = 'X'
            else:
                print("please enter a valid number")
                speak("please enter a valid number")
        restart = input("Do want to play Again?(y/n)")
        if restart == "y" or restart == "Y":
            for key in board_keys:
                theBoard[key] = " "

            game()

    game()


def get_num(self):
    dic = {"send it to aravind": 9381146833,
           "send it to sivaiah sir": 9505838400, "send it to nikhil": 8019997494}
    speak('whom do you want to send the message ')
    inpp = self.takecommand()
    print(inpp)
    if inpp in dic.keys():
        a = dic[inpp]
        return a
    elif "no thanks" in inpp:
        return "none"
    else:
        speak('there is no contact named ' + inpp)
        return get_num(self)


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=5)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"Human: {query}")
        except Exception:
            return "none"
        query = query.lower()
        return query

    def run(self):
        #speak("please say wakeup to continue..")
        while True:
            self.query = self.takecommand()
            # if "wake" in self.query or "wakeup" in self.query or "wake up" in self.query:
            self.pertask()

    def pertask(self):
        # wishMe()
        while True:
            self.query = self.takecommand()

            if 'open notepad' in self.query:
                npath = "C:\\Windows\\notepad.exe"
                os.startfile(npath)
            elif 'game' in self.query:
                playgame(self)
            elif 'close notepad' in self.query:
                speak("ok")
                os.system("taskkill /f /im notepad.exe")
            elif 'open code' in self.query:
                npath = "C:\\Users\\dello\\AppData\\Local\\Programs\\Microsoft VS Code\\bin\\code"
                os.startfile(npath)
            elif 'open command prompt' in self.query:
                npath = "C:\\Windows\\System32\\cmd.exe"
                os.startfile(npath)
            elif 'play' in self.query:
                song = self.query.replace('play', '')
                speak('playing' + song)
                print(song)
                kit.playonyt(song)
            elif 'good job' in self.query:
                speak('thank you! it is my responsibility')
            elif 'how old are you' in self.query:
                speak('it depends on how you look')
            elif 'hello' in self.query or 'hey' in self.query:
                speak("hello there how are you!")
            elif 'stark' in self.query:
                speak("how can i help you..")
            elif 'who made you' in self.query or 'who invented you' in self.query:
                speak("I have been created by team stark.")
            elif 'who are you' in self.query:
                speak('iam stark, I can perform various task\'s')
            elif 'tell me a joke' in self.query or 'joke' in self.query:
                speak(pyjokes.get_joke())
            elif 'how are you' in self.query:
                speak("I am good, Thank you and what about you?")
            elif "good" in self.query or "fine" in self.query:
                speak("It's good to know that")
            elif 'wikipedia' in self.query:
                qquery = self.query.replace("wikipedia", "")
                info = wikipedia.summary(qquery, sentences=1)
                speak('According to wikipedia ' + info)
            elif 'open youtube' in self.query:
                speak('here you go')
                webbrowser.open("https://www.youtube.com")
            elif 'open google' in self.query:
                speak('what should i have to search ')
                cm = self.takecommand().lower()
                webbrowser.open(f"{cm}")
            elif 'open gmail' in self.query:
                speak('here you go')
                webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
            elif 'send a message' in self.query:
                timef = datetime.datetime.now().strftime('%I:%M %p')
                timee = datetime.datetime.now().strftime('%H:%M')
                s1 = str(timee[0]) + str(timee[1])
                s2 = str(timee[3] + timee[4])
                if s2[0] == '0':
                    s2 = s2[1]
                elif 'AM' in timef and s1 == '12':
                    s1 = '00'
                speak('what i have to send ')
                mess = self.takecommand()
                number = get_num(self)
                if number != "none":
                    speak('message sending..')
                    kit.sendwhatmsg('+91' + str(number), mess,
                                    int(s1), int(s2) + 2)
                else:
                    pass
            elif 'send a email' in self.query:
                try:
                    speak("What should I say?")
                    content = self.takecommand().lower()
                    to = input("enter email : ")
                    sendEmail(to, content)
                    speak("Email has been sent !")
                except Exception as e:

                    print(e)
                    speak("I am not able to send this email")
            elif "calculate" in self.query:
                app_id = "E4AJ9J-WGXTR9AGEX"
                client = wolframalpha.Client(app_id)
                ind = self.query.lower().split().index("calculate")
                qquery = self.query.split()[ind + 1:]
                res = client.query(" ".join(qquery))
                answer = next(res.results).text
                speak("The answer is " + answer)

            elif "information" in self.query:
                try:
                    app_id = "E4AJ9J-WGXTR9AGEX"
                    client = wolframalpha.Client(app_id)
                    ind = self.query.lower().split().index("of")
                    qquery = self.query.split()[ind + 1:]
                    res = client.query(" ".join(qquery))
                    answer = next(res.results).text
                    speak(answer)
                except Exception:
                    speak("unable to fetch the information")
            elif "write a note" in self.query:
                speak("What should i write, ")
                note = self.takecommand()
                file = open('jarvis', 'w')
                speak("Should i include date and time")
                snfm = self.takecommand()
                if 'yes' in snfm or 'sure' in snfm:
                    timee = datetime.datetime.now().strftime('%I:%M %p')
                    file.write(timee)
                    file.write(" :- ")
                    file.write(note)
                    speak('notes taken!')
                else:
                    file.write(note)
                    speak('notes taken!')
            elif 'show me the notes' in self.query:
                speak("Showing Notes")
                file = open("jarvis", "r")
                s = file.read()
                print(s)
                speak(s)
            elif "restart" in self.query:
                subprocess.call(["shutdown", "/r"])
                exit()
            elif 'empty recycle bin' in self.query:
                winshell.recycle_bin().empty(confirm=False, show_progress=True, sound=True)
                speak("Recycle Bin Recycled")
            elif "hibernate" in self.query or "sleep" in self.query:
                speak("Hibernating")
                subprocess.call(["shutdown", "/h"])
                exit()
            elif "log off" in self.query or "shutdown" in self.query:
                speak("Make sure all the application are closed before sign-out")
                time.sleep(10)
                subprocess.call(["shutdown", "/l"])
                exit()
            elif 'quit' in self.query or 'thank you' in self.query:
                speak('have a good day, thank you')
                exit()
            elif 'news today' in self.query or 'news' in self.query:
                speak('please wait , fetching the latest news')
                news()
            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
            elif 'send sms' in self.query:
                speak('what should i have to send')
                msg = self.takecommand()

                account_sid = 'AC4a5e160677981459b0938b5769eab4ee'
                auth_token = '4a47f90ab357d1698c22d473979ae4ad'
                client = Client(account_sid, auth_token)

                message = client.messages \
                    .create(
                        body=msg,
                        from_='+13105987480',
                        to=input()
                    )
                print(message.sid)
                speak('message sent..')
            elif 'where are we' in self.query:
                speak('let me check!')
                try:
                    ipadd = requests.get('https://api.ipify.org').text
                    url = 'https://get.geojs.io/v1/ip/geo/' + ipadd + '.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    city = geo_data['city']
                    state = geo_data['region']
                    country = geo_data['country']
                    speak(
                        f" we are in state {state} of {city} city of {country} country")
                except Exception:
                    speak('unable to find location ')
                    pass
            elif "weather" in self.query:
                import math
                key = "4265b08b2aae7efa2e1c4456706c258d"
                weather_url = "http://api.openweathermap.org/data/2.5/weather?"
                ind = self.query.split().index("in")
                location = self.query.split()[ind + 1:]
                location = "".join(location)
                url = weather_url + "appid=" + key + "&q=" + location
                js = requests.get(url).json()
                if js["cod"] != "404":
                    weather = js["main"]
                    temperature = weather["temp"]
                    temperature = temperature - 273.15
                    humidity = weather["humidity"]
                    weather_response = " The temperature in Celcius is " + \
                        str(math.ceil(temperature)) + \
                        " The humidity is " + str(humidity)
                    speak(weather_response)
                else:
                    speak("City Not Found")
            elif "where is" in self.query:
                ind = self.query.lower().split().index("is")
                location = self.query.split()[ind + 1:]
                url = "https://www.google.com/maps/place/" + "".join(location)
                speak("This is where " + str(location[0]) + " is.")
                webbrowser.open(url)
            elif "laptop percentage" in self.query:
                battery = psutil.sensors_battery()
                per = battery.percent
                speak(str(per)+" percent")
            elif "join zoom meeting" in self.query:
                py="https://us04web.zoom.us/j/7687039381?pwd=OHpmdk1Nc1hydHRzU3RwWUdaQ3NJUT09"
                psec = datetime.datetime.now().strftime('%H:%M')
                s1 = str(psec[0]) + str(psec[1])
                s2 = str(psec[3] + psec[4])
                print(s1)
                print(s2)
                tm=input("enter time(hh:mm) : ")
                ss1=str(tm[0])+str(tm[1])
                ss2=str(tm[3])+str(tm[4])
                wh=int(ss1)-int(s1)
                wm=int(ss2)-int(s2)
                hrr=0
                min=0
                if wh>0:
                    hrr=int(wh)*3600
                if wm>0:
                    min=int(wm)*60
                time.sleep(hrr+min)
                webbrowser.open(py)
            elif "repeat me" in self.query:
                speak("what i have to repeat")
                str1 = self.takecommand()
                speak(str1)
            elif "internet speed" in self.query:
                st = speedtest.Speedtest()
                dl = st.download()
                ul = st.upload()
                speak("download speed is: "+str(dl[:3]) +
                    " upload speed is " + str(ul[:3]))
            else:
                print('\n')


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie(
            "C:/Users/nikhi/Downloads/Iron man.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(
            "C:/Users/nikhi/Downloads/Jarvis_Loading_Screen.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
stark = Main()
stark.show()
exit(app.exec_())
