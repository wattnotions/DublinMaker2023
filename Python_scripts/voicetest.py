import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    if b"english" in voice.languages[0].lower():
        print("Voice name:", voice.name)
        print("Voice ID:", voice.id)
        
        engine.setProperty('voice', voice.id)
        engine.say('The quick brown fox jumped over the lazy dog.')
        engine.runAndWait()
