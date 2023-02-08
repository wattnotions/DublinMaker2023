import os
import openai

openai.api_key = "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"

question = "what should I do with my life?"
promptQ = "Respond to the question " + question  + " in the style of an ent from lord of the rings"
print(promptQ)

response = openai.Completion.create(
  model="text-davinci-003",
  
  prompt="Respond to the question " + question + " in the style of an ent from lord of the rings",
  temperature=0,
  max_tokens=60,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)


print(response)