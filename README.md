# Scam-Call-Detection

This is a python script to detect the probability of a call being scam.

It takes the path of the call audio file as input and returns the probability of scam as output using custom tkinter module

Dont forget to install these libraries in cmd:
pip install speechrecognition
pip install pydub
pip install pyttsx3
pip install customtkinter
pip install nltk


# Details
It first converts speech to text using google speechrecognition API. 
The converted text is checked if there are any suspicious scam words present.
According to the number of scam words and the distance of each scam words in each sentence, it calculates a value
The vaule is averaged for all sentences in the call spoken which have at least 1 scam word.
The probability value is returned as a number between 0 and 1.
