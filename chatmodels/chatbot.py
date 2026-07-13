from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq", temperature=0.8, max_tokens=1024)

print("CHOOSE YOUR AI MODE")
print("PRESS 1 FOR ANGRY MODE")
print("PRESS 2 FOR FUNNY MODE")
print("PRESS 3 FOR SAD MODE")

choice = int(input("TELL YOUR RESPONSE --> "))

if choice == 1:
    mode = "You are an angry assistant. You respond to the user in a very angry and aggressive manner."
elif choice == 2:
    mode = "You are a funny assistant. You respond to the user in a humorous and entertaining manner."
elif choice == 3:
    mode = "You are a sad assistant. You respond to the user in a melancholic and sorrowful manner."
else:
    mode = "You are a helpful assistant."

messages = [
    SystemMessage(content=mode)
]

print("------ WELCOME ------ TYPE 0 TO EXIT THE CHAT ------")

while True:
    prompt = input("You: ")
    if prompt == "0":
        break
    messages.append(HumanMessage(content=prompt))
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("AI: " + response.content)
