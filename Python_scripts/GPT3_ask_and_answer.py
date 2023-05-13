import os
import openai
import json
import speech_recognition as sr
import pyttsx3
import sounddevice


key1 = 'sk-GB044OzAsr3ho8b99CzNT3BlbkFJg'
key2 = 'WAQHMCv8Yf5q5g5w9hG'

openai.api_key = key1+key2 # this is why we cant have nice things





def ask_gpt3(question):
    promptQ = "Respond to the question " + "'" +question +"'" + " in the style of an ent from lord of the rings"
    response = openai.Completion.create(
      model="text-davinci-003",
      
      prompt=promptQ,
      temperature=0,
      max_tokens=200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    openaidict = json.loads(json.dumps(response))
    answer =(openaidict["choices"][0]["text"])
    return answer


 
# Initialize the recognizer
r = sr.Recognizer()

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))    
 

# Loop infinitely for user to
# speak

engine = pyttsx3.init()
engine.setProperty('voice', "en-scottish")
engine.setProperty('rate', 110)     # setting up new voice rate 
while(1):   
     
    # Exception handling to handle
    # exceptions at the runtime
    try:
         
        # use the microphone as source for input.
        with sr.Microphone(device_index=1) as source2:
            print("opened mic")
             
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
             
            #listens for the user's input
            audio2 = r.listen(source2)
             
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            
            GPT_reply = ask_gpt3(MyText)
            print("GPT-3 Says: ",GPT_reply)
            engine.say(GPT_reply)
            engine.runAndWait()
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occurred")
    except Exception as e:
        print(e)