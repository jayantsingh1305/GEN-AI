from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq", temperature=0.8, max_tokens=1024)

messages = [
    SystemMessage(content="You are a helpful assistant.")
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
