import os
import openai
import json
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from mouth_controller import PWMController



class GPT3Assistant:
    def __init__(self, api_key):
        openai.api_key = api_key

    def ask_gpt3(self, question):
        prompt_q = f"Respond to the question '{question}' in the style of an ent from Lord of the Rings."
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_q,
            temperature=0,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response["choices"][0]["text"]
        return answer


class VoiceAssistant:
    def __init__(self, gpt3_assistant, device_index=1):
        self.gpt3_assistant = gpt3_assistant
        self.device_index = device_index
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', "en-scottish")
        self.engine.setProperty('rate', 110)

    @staticmethod
    def list_microphones():
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Microphone with name \"{name}\" found for `Microphone(device_index={index})`")

    def listen_and_respond(self):
        while True:
            try:
                with sr.Microphone(device_index=self.device_index) as source:
                    print("opened mic")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.recognizer.listen(source)
                    text_input = self.recognizer.recognize_google(audio).lower()
                    gpt_reply = self.gpt3_assistant.ask_gpt3(text_input)
                    print("GPT-3 Says: ", gpt_reply)
                    self.engine.say(gpt_reply)
                    self.engine.runAndWait()

            except sr.RequestError as e:
                print(f"Could not request results; {e}")

            except sr.UnknownValueError:
                print("Unknown error occurred")

            except Exception as e:
                print(e)


if __name__ == "__main__":
    load_dotenv("api_key.env")
    api_key = os.environ.get("API_KEY")

    gpt3_assistant = GPT3Assistant(api_key)
    voice_assistant = VoiceAssistant(gpt3_assistant)

    pwm_controller = PWMController()
    pwm_controller.start()

    VoiceAssistant.list_microphones()
    voice_assistant.listen_and_respond()
