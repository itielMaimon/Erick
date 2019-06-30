import speech_recognition as sr
import os
import pyttsx3
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import urllib
import urllib3
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
import datetime
from time import strftime

engine = pyttsx3.init()

""" RATE"""
rate = engine.getProperty('rate')   # Getting details of current speaking rate
engine.setProperty('rate', 170)     # Setting up new voice rate

"""VOICE"""
voices = engine.getProperty('voices')   # Getting details of current voice
# Changing index, changes voices. o for male, 1 for female
engine.setProperty('voice', voices[0].id)

engine.say("Hi, I am Erick, your personal voice assistant, how can I help you?")
engine.runAndWait()
engine.stop()


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
        erickResponse('I\'m 2 days old, but growing fastly.')
    elif 'who built you' in command:
        erickResponse(
            'Itiel Maimon, the greatest programmer of all time built me.')
    elif 'what can you do' in command:
        erickResponse(
            'I can do a lot of things, to help you throut your day.')
    elif 'help me' in command:
        erickResponse('I\'m here to help, you can ask me what I can do.')
    elif 'like siri' in command:
        erickResponse('I like Siri, she\'s very nice.')

    # Greet Erick
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            erickResponse('Hello Sir. Good morning!')
        elif 12 <= day_time < 18:
            erickResponse('Hello Sir. Good afternoon!')
        else:
            erickResponse('Hello Sir. Good evening!')
    elif 'thank you' in command:
        erickResponse('You\'re Welcome!')

    # Make Erick stop
    elif 'shut down' in command:
        erickResponse('Bye bye Sir. Have a nice day!')
        sys.exit()

    # Open Twitter
    elif 'open twitter' in command:
        reg_ex = re.search('open twitter (.*)', command)
        url = 'https://www.twitter.com/'
        if reg_ex:
            handle = reg_ex.group(1)
            url = url + handle
        webbrowser.open(url)
        erickResponse('The requested Twitter account has been opened for you Sir.')

    # Open Instagram
    elif 'open instagram' in command:
        reg_ex = re.search('open instagram (.*)', command)
        url = 'https://www.instagram.com/'
        if reg_ex:
            handle = reg_ex.group(1)
            url = url + handle
        webbrowser.open(url)
        erickResponse('The requested Instagram account has been opened for you Sir.')

    # Open subreddit Reddit
    elif 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        erickResponse('The requested Reddit content has been opened for you Sir.')

    # Open website
    elif 'go to' in command:
        reg_ex = re.search('go to (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            erickResponse(
                'The website you have requested has been opened for you Sir.')
        else:
            pass

    # Send Email
    elif 'email' in command:
        erickResponse('Who is the recipient?')
        recipient = newCommand()
        if 'someone' in recipient:
            erickResponse('What should I say to him?')
            content = newCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('sender_email', 'sender_password')
            mail.sendmail('sender_email', 'receiver_email', content)
            mail.close()
            erickResponse(
                'Email has been sent successfuly. You can check your inbox.')
        else:
            erickResponse('I don\'t know what you mean!')

    # Launch apps
    elif 'open' in command:
        reg_ex = re.search('open (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".exe"
            subprocess.call([appname1])
            erickResponse('I have launched the requested application.')

    # Get current time
    elif 'time' in command:
        now = datetime.datetime.now()
        erickResponse('Current time is %d hours %d minutes.' %
                       (now.hour, now.minute))

    # Ask general questions
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                erickResponse(ny.content[:300].encode('utf-8'))
        except Exception as e:
            print(e)
            erickResponse(e)
    elif 'what is' in command:
        reg_ex = re.search('what is (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                erickResponse(ny.content[:200].encode('utf-8'))
        except Exception as e:
            print(e)
            erickResponse(e)
    elif 'who is' in command:
        reg_ex = re.search('who is (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                erickResponse(ny.content[:100].encode('utf-8'))
        except Exception as e:
            print(e)
            erickResponse(e)

while True:
    assistant(newCommand())