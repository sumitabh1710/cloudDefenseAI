from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

conversation_history = []

def chat(conversation_history):    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    return completion.choices[0].message

print("Welcome to the ChatGPT Chatbot!")
print("Type 'exit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    conversation_history.append({"role": "user", "content": user_input})
    
    response = chat(conversation_history)
    
    conversation_history.append({"role": "system", "content": user_input})
    
    print("ChatGPT: " + response)
