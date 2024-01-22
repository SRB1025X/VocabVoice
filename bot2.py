# -- coding: utf-8 --
"""
Created on Thur Aug 17 22:57:49 2023

@author: shreyasrameshbollavathini
"""

from tkinter import *
import pyttsx3
import speech_recognition as sr
from PyDictionary import PyDictionary
import threading

class Listening:
    @staticmethod
    def listen(listening_label):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            listening_label.config(text="Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            listening_label.config(text="Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(query + "\n")
            return query
        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "0"

class Speaking:
    @staticmethod
    def speak(audio):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        newVoiceRate = 160
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', newVoiceRate)
        engine.say(audio)
        engine.runAndWait()

class Prompt:
    @staticmethod
    def first():
        speak = Speaking()
        speak.speak("Which word do you want to find the meaning sir?")

class Dictionary:
    @staticmethod
    def fetch_meaning(query, meaning_label):
        speak = Speaking()
        dic = PyDictionary()
        word_meanings = dic.meaning(query)
        for part_of_speech, meanings in word_meanings.items():
            meaning = f"{part_of_speech.capitalize()} meaning: {', '.join(meanings)}"
            print(meaning)
            meaning_label.config(text=meaning)
            speak.speak(f"The {part_of_speech} meaning is {', '.join(meanings)}")

def search_button_click(listening_label, meaning_label):
    prompt = Prompt()
    prompt.first()
    query = '0'
    while query == '0':
        query = Listening.listen(listening_label)
        if query == '0':
            print("Try again... Speech not recognized")
    Dictionary.fetch_meaning(query, meaning_label)

if __name__ == '__main__':
    root = Tk()
    root.title("Voice Dictionary")
    root.geometry('400x300')

    lbl1 = Label(root, text="Voice search")
    lbl1.grid(column=0, row=0)

    listening_label = Label(root, text="")
    listening_label.grid(column=1, row=0)

    meaning_label = Label(root, text="", wraplength=350)
    meaning_label.grid(column=0, row=1, columnspan=2)

    btn = Button(root, text="Search", fg="red", command=lambda: threading.Thread(target=search_button_click, args=(listening_label, meaning_label)).start())
    btn.grid(column=1, row=2)

    root.mainloop()