# install these libraries before running
'''
pip install speechrecognition
pip install pydub
pip install pyttsx3
pip install customtkinter
pip install nltk
'''

# importing libraries
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
import random
import math
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import tkinter
import customtkinter

# defining suspicious scam words
scam_words = "aadhaar cvv username password access information special lucky money OTP credit card bonus code chance promo win last contact prizes rewards phone send give forward email message account number lottery"
scam_words = scam_words.split(" ")
print("\n\nScam words considered:", scam_words)

# Scam Sentences
scam_sentences = [
    ["I am speaking from XYZ bank. Can you send me your OTP which you received on your phone.".lower(), "True"],
    ["Please provide me with your Aadhaar Card details.".lower(), "True"],
    ["Can you tell us your Credit Card CVV number.".lower(), "True"],
    ["Please provide me with your Credit Card number.".lower(), "True"],
    ["What is your address.".lower(), "True"],
    [
        "You have won a lottery of 10 lakh rupees! To receive the amount, you will have to provide us with your bank account information.".lower(),
        "True"],
    ["I am your father's friend, he told me to ask you for some money.".lower(), "True"],
    ["Kindly tell me your Username and Password of your Google account.".lower(), "True"],
    ["We are from XYZ foundation. Donate money to bring a smile on underprivileged kids.".lower(), "True"],
    [
        "I am from technical support team. Can you give me access to your PC so that I can help you remove the virus.".lower(),
        "True"]
]

# Non-Scam Sentences
nonscam_sentences = [
    ["I am speaking from XYZ bank. We would like to verify your details.".lower(), "False"],
    ["Kindly go to our official website and provide us with the neccessary details.".lower(), "False"],
    ["Visit the nearest branch of XYZ bank to process your request.".lower(), "False"],
    [
        "We require some additional information about you to verify your identity. Please visit the centre with your KYC information.".lower(),
        "False"],
    ["Hey what's up! Long time no see. Let's catch up soon.".lower(), "False"],
    ["Tell your mom that XYZ aunty had called.".lower(), "False"],
    ["I am speaking from XYZ restaurant. Your parcel will arrive in few minutes.".lower(), "False"],
    ["I wanted to borrow XYZ book from you. Can you lend it to me for a few days?".lower(), "False"],
    ["This is the librarian of XYZ college. You have a pending fine, kindly pay it at the earliest.".lower(), "False"],
    [
        "Your monthly subscription for XYZ newspaper is due. Kindly pay it to the delivery man via Cash or Google Pay or Paytm".lower(),
        "False"]
]


# Performing Speech recognition

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              min_silence_len=500,
                              silence_thresh=sound.dBFS - 14,
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                pass
            else:
                text = f"{text.capitalize()}. "
                whole_text += text

    return whole_text


def filter_common_words(text_list):
    common_words = stopwords.words("english")
    # common words like ["me","your","to","a"] which have no contribution to detection
    word_seq = [i for i in text_list if (i not in common_words)]
    return word_seq


def ScamProbability(sentence):  # Calculates Scam probability of single Sentence(List)
    #sentence = filter_common_words(sentence)
    sentence = [word.lower() for word in sentence]
    if set(sentence).difference(scam_words) == set(sentence):
        return 0
    else:
        scamindices = [i for i in range(len(sentence)) if sentence[i] in scam_words]
        indexdiff = [scamindices[i] - scamindices[i - 1] for i in range(1, len(scamindices))]
        if len(indexdiff) == 0:
            probability = 1 / (len(sentence))
        elif len(scamindices) / len(sentence) > 0.5:
            return len(scamindices) / len(sentence)
        else:
            probability = 1 - (sum(indexdiff) / len(indexdiff)) / (2 * len(sentence))
    return probability


def calculate_accuracy(path):
    text = get_large_audio_transcription(path)
    text_list = text.split(" ")
    prob = ScamProbability(text_list)
    return prob


# Code for GUI

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("300x500")
app.title("Scam Call Detector v1.1")


def get_path():
    path = entry.get()
    return path

def button_function():  # calculates percentage
    path = get_path()
    print("\nSelected file: ", path)
    acc = calculate_accuracy(path)
    try:
        l2.destroy()
    except:
        pass
    l2 = customtkinter.CTkLabel(master=app, text="Scam Probability: " + str(round(acc * 100, 2)) + "%",
                                font=('Century Gothic', 17))
    l2.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)


l1 = customtkinter.CTkLabel(master=app, text="Scam Call Detector v1.1", font=('Century Gothic', 20))
l1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

entry = customtkinter.CTkEntry(master=app, width=220, placeholder_text='Enter Audio Path')
entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="Submit", command=button_function, font=('Century Gothic', 15))
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l3 = customtkinter.CTkLabel(master=app,
                            text="      ----- How It Works -----\n       1. Enter path to your audio file\n2. Click on Submit button\n       3. Probability will be displayed",
                            font=('Century Gothic', 12))
l3.place(relx=0.45, rely=0.8, anchor=tkinter.CENTER)

app.mainloop()
