import speech_recognition as sr
import pyttsx3
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.request import urlopen
import wikipedia
import wolframalpha
import ctypes
import datetime
from time import strftime

engine = pyttsx3.init()

# RATE
rate = engine.getProperty('rate')   # Getting details of current speaking rate
engine.setProperty('rate', 170)     # Setting up new voice rate

# VOICE
voices = engine.getProperty('voices')   # Getting details of current voice
# Changing index, changes voices. o for male, 1 for female
engine.setProperty('voice', voices[0].id)

welcomeMessage = 'Hi, I am Erick, your personal voice assistant. How can I help you?'
print(welcomeMessage)
engine.say(welcomeMessage)
engine.runAndWait()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

app_id = 'wolfram_API'   # wolfram_API_here


def newCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Sorry I can\'t understand')
        command = newCommand()
    return command


def erickResponse(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def assistant(command):
    # if statements for executing commands

    # Questions about Erick
    if 'your name' in command:
        erickResponse('My name is Erick. Nice to meet you!')
    elif 'who are you' in command:
        erickResponse('I\'m Erick, your personal voice assistant!')
    elif 'do you feel' in command:
        erickResponse('I\'m doing great, thanks for asking.')
    elif 'old are you' in command:
        erickResponse('I was launched in June of 2019, but growing fastly.')
    elif 'who built you' in command:
        erickResponse(
            'Itiel Maimon, the greatest programmer of all time built me.')
    elif 'what can you do' in command:
        erickResponse(
            'I can do a lot of things, to help you throughout your day.')
    elif 'help me' in command:
        erickResponse('I\'m here to help, you can ask me what I can do.')
    elif 'like siri' in command:
        erickResponse('I like Siri, she\'s very nice.')

    # Greet Erick
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            erickResponse('Hello, Good morning!')
        elif 12 <= day_time < 18:
            erickResponse('Hello, Good afternoon!')
        else:
            erickResponse('Hello, Good evening!')
    elif 'thank you' in command:
        erickResponse('You\'re Welcome!')

    # Make Erick stop
    elif 'shut down' in command:
        erickResponse('Bye bye. Have a nice day!')
        sys.exit()

    # Open Twitter
    elif 'open twitter' in command:
        reg_ex = re.search('open twitter (.*)', command)
        url = 'https://www.twitter.com/'
        if reg_ex:
            handle = reg_ex.group(1)
            url = url + handle
        webbrowser.open(url)
        erickResponse(
            'Opening Twitter.')

    # Open Instagram
    elif 'open instagram' in command:
        reg_ex = re.search('open instagram (.*)', command)
        url = 'https://www.instagram.com/'
        if reg_ex:
            handle = reg_ex.group(1)
            url = url + handle
        webbrowser.open(url)
        erickResponse(
            'Opening Instagram.')

    # Open subreddit Reddit
    elif 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        erickResponse(
            'Opening Reddit.')

    # Open any website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            erickResponse(
                'Opening ' + domain)

    # Make a search on Google
    elif 'search' in command:
        reg_ex = re.search('search (.+)', command)
        if reg_ex:
            subject = reg_ex.group(1)
            url = 'https://www.google.com/search?q=' + subject
            webbrowser.open(url)
            erickResponse(
                'Searching for ' + subject + ' on Google.')

    # Play a song on Youtube
    elif 'play' in command:
        reg_ex = re.search('play (.+)', command)
        if reg_ex:
            searchedSong = reg_ex.group(1)
            url = 'https://www.youtube.com/results?q=' + searchedSong
            try:
                source_code = requests.get(url, headers=headers, timeout=15)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, "html.parser")
                songs = soup.findAll('div', {'class': 'yt-lockup-video'})
                song = songs[0].contents[0].contents[0].contents[0]
                hit = song['href']
                webbrowser.open('https://www.youtube.com' + hit)
                erickResponse('Playing ' + searchedSong + ' on Youtube.')
            except Exception as e:
                webbrowser.open(url)
                erickResponse('Searching for ' + searchedSong + ' on Youtube.')

    # Send Email
    elif 'email' in command:
        erickResponse('Who is the recipient?')
        recipient = newCommand()
        if 'someone' in recipient:
            erickResponse('What should I say to him?')
            content = newCommand()
            try:
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('sender_email', 'sender_password')
                mail.sendmail('sender_email', 'receiver_email', content)
                mail.close()
                erickResponse(
                    'Email has been sent successfuly.')
            except Exception as e:
                print(e)
        else:
            erickResponse('I don\'t know anyone named ' + recipient + '.')

    # Launch apps
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".exe"
            subprocess.call([appname1])
            erickResponse('Launching ' + appname + '.')

    # Get current time
    elif 'time' in command:
        now = datetime.datetime.now()
        erickResponse('Current time is %d:%d.' %
                      (now.hour, now.minute))

    # Get recent news
    elif 'news' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = BeautifulSoup(xml_page, "html.parser")
            news_list = soup_page.findAll("item")
            for news in news_list[:5]:
                erickResponse(news.title.text)
        except Exception as e:
            print(e)

    # Lock the device
    elif 'lock' in command:
        try:
            erickResponse("Locking the device.")
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            print(str(e))

    # Ask general questions
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                erickResponse(wikipedia.summary(topic, sentences=3))
        except Exception as e:
            erickResponse(e)
    elif any(c in command for c in ("what is", "what\'s")):
        reg_ex = re.search(' (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                erickResponse(wikipedia.summary(topic, sentences=2))
        except Exception as e:
            erickResponse(e)

    # All other cases
    else:
        try:
            # wolframalpha
            client = wolframalpha.Client(app_id)
            res = client.query(command)
            answer = next(res.results).text
            erickResponse(answer)
        except:
            try:
                # wikipedia
                erickResponse(wikipedia.summary(command, sentences=2))
            except Exception as e:
                erickResponse(e)


while True:
    assistant(newCommand())
