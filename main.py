import pyttsx3
import speech_recognition as sr
import pickle
import datetime
import os.path
import sys

import userclass
import settingsclass
import defaulttext as dt


engine = pyttsx3.init()
r = sr.Recognizer()
mic = sr.Microphone()

settings = settingsclass.Settings(0, 0, 0, 0)
user = userclass.User("")


def main():
    clean_noise()

    global settings
    settings = get_settings()
    update_engine_settings(settings)

    global user
    user = get_user()
    say(dt.HELLO + user.username)

    while True:
        exec_cmd()
    
    
def clean_noise():
    with mic as source:
        r.adjust_for_ambient_noise(source)
    
    
def get_user() -> userclass.User:
    if os.path.exists(dt.USER):
        with open(dt.USER, "rb") as f:
            user = pickle.load(f)
        return user
    else:
        username = ""
        while username == "":
            say(dt.NAMEQ1)
            username = listen(True)
            say(dt.NAMEQ2 + username + dt.Q)
            if not(check_agree()):
                username = ""
        user = userclass.User(username)
        with open(dt.USER, "wb") as f:
            pickle.dump(user, f)
        return user
    
    
def get_settings() -> settingsclass.Settings:
    if os.path.exists(dt.SETTINGS):
        with open(dt.SETTINGS, "rb") as f:
            settings = pickle.load(f)
        return settings
    else:
        settings = settingsclass.Settings(150, 1.0, engine.getProperty('voices')[0].id, 0.5)
        with open(dt.SETTINGS, "wb") as f:
            pickle.dump(settings, f)
        return settings
    
    
def update_engine_settings(settings: settingsclass.Settings):
    engine.setProperty('rate', settings.rate)
    engine.setProperty('volume', settings.volume)
    engine.setProperty('voice', settings.voice)
    sr.pause_threshold = settings.pause_threshold


def check_agree() -> bool:
    answer = listen(True)
    for word in dt.DISAGREE:
        if answer.find(word) != -1:
            return False
    for word in dt.AGREE:
        if answer.find(word) != -1:
            return True
    return False


def say(text: str):
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def listen(need_back: bool) -> str:
    with mic as source:
        while True:
            audio = r.listen(source)
            try:
                f = r.recognize_google(audio, language="ru-RU").lower()
                return f
            except:
                if need_back:
                    say(dt.NOTUND)


def time_cmd():
    now = datetime.datetime.now()
    say(dt.TIME1 + str(now.hour) + dt.TIME2 + str(now.minute))


def end_cmd():
    say(dt.GOODBYE + user.username)
    sys.exit()


def exec_cmd():
    cmd = listen(False)

    for k, v in dt.CMDS['commands'].items():
        if cmd in v:
            print(globals()[k]())


if __name__ == '__main__':
    main()