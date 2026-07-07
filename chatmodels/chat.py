from dotenv import load_dotenv

load_dotenv()

from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq",temperature=0.8,MAX_TOKENS=20)

response = model.invoke("Write a poem on AI")

print(response.content)
