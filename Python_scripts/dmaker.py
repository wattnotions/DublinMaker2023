import os
import openai
import json
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from mouth_controller import PWMController
from eyes_controller import EyesController
from cam import WebcamStream
import threading
import time





class GPT3Assistant:
    def __init__(self, api_key):
        openai.api_key = api_key

    def ask_gpt3(self, conversation, question):
        conversation.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0,
            max_tokens=200
        )
        answer = response["choices"][0]["message"]["content"]
        return response



class VoiceAssistant:
    def __init__(self, gpt3_assistant, device_index=1):
        self.gpt3_assistant = gpt3_assistant
        self.device_index = device_index
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', "english-rp")
        self.engine.setProperty('rate', 130)
        self.is_listening = True  # <-- This flag will be used to stop the listening loop
        

    @staticmethod
    def list_microphones():
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Microphone with name \"{name}\" found for `Microphone(device_index={index})`")

    def listen(self):
        try:
            with sr.Microphone(device_index=self.device_index) as source:
                print("opened mic")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.speak("I'm listening")
                # Listen for audio input

                start_time = time.time()  # Record the starting time
                max_listen_duration = 5  # Set the maximum duration in seconds
                
                while time.time() - start_time <= max_listen_duration:
                    audio = self.recognizer.listen(source, timeout=1)  # Listen for a short period    
                
                
                    try:
                        text_input = self.recognizer.recognize_google(audio).lower()
                        #text_input = self.recognizer.recognize_whisper_api(audio, api_key=api_key).lower()
                        print(text_input)
                        return text_input
                    except sr.UnknownValueError:
                        return None  # No speech detected
                
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(e)
        
        return None  # Error occurred

   


    def speak(self, words_str):
        print(words_str)
        self.engine.say(words_str)
        self.engine.runAndWait()

    def idle_speak(self):
        pass


    

if __name__ == "__main__":
    load_dotenv("api_key.env")
    api_key = os.environ.get("API_KEY")

    gpt3_assistant = GPT3Assistant(api_key)
    voice_assistant = VoiceAssistant(gpt3_assistant)

    pwm_controller = PWMController()
    pwm_controller.start()

    #eyes = EyesController()
    #eyes.animate_eyes()

    eyes_controller = EyesController()

    # Create an instance of WebcamStream with the EyesController instance
    webcam_stream = WebcamStream(eyes_controller=eyes_controller, frame_rate=5)  # Adjust frame rate if needed

    # Start the threads
    eyes_controller.eyes_thread_instance.start()
    webcam_stream.start()

    
    #VoiceAssistant.list_microphones()

   # voice_assistant.start_listening()

    with open("prompts/system_prompt.txt", 'r') as file:
        pre_prompt = file.read()    

    conversation = []  # Initialize an empty conversation
    question = pre_prompt
    while True:
        print("text sent to openai = "+question)
        response=gpt3_assistant.ask_gpt3(conversation, question)
        gpt_reply = response["choices"][0]["message"]["content"]


        conversation.append({"role": "user", "content": question})
        conversation.append({"role": "assistant", "content": gpt_reply})

        total_tokens_used = response['usage']['total_tokens']
        print(total_tokens_used)
        # Check if the total tokens used exceed the max token context (4k tokens)
        if total_tokens_used > 3500:
            voice_assistant.speak("Total tokens used exceed max token context. Clearing conversation and starting again.")
            print("Total tokens used exceed max token context. Clearing conversation and starting again.")
            conversation = []
            question = pre_prompt
            continue
        
        
        
        print("speak response")
        print(len(conversation))

       # print(gpt_reply)
        voice_assistant.speak(gpt_reply)

        #wait for a few seconds to give person a chance to speak
        
        spoken_words = voice_assistant.listen()
    
        if spoken_words:
            voice_assistant.speak("I heard you")
            question = spoken_words
            print(question)
        else:
            voice_assistant.speak("I missed that")
            question =  "Nobody responded, just keep the conversation going"
            print("no voice detected")
