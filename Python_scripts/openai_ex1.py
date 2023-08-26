import os
import openai
import json
from dotenv import load_dotenv
import os

load_dotenv("open_ai_api.env")  # Load environment variables from .env file

openai.api_key = os.environ.get("API_KEY")

question = input()

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
print("\n")
print("Answer: "+ answer)
