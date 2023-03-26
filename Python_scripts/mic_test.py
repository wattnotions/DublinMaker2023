import speech_recognition as sr
import sounddevice
r = sr.Recognizer()
r.energy_threshold = 645
r.dynamic_energy_threshold = True

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))  
    
    
with sr.Microphone(device_index=1) as source2:
            print("opened mic")
             
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
             
            #listens for the user's input
            audio2 = r.listen(source2)
            
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            
            print(MyText)