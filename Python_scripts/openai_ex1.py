import os
import openai
import json

openai.api_key = "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"

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