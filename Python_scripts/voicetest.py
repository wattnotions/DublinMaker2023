import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 110)     # setting up new voice rate
volume = engine.getProperty('volume')
print(volume)


for voice in voices:
   print(voice)
   print(voice.id)
   engine.setProperty('voice', "en-scottish")
   engine.say('The quick brown fox jumped over the lazy dog.')
   engine.runAndWait()