import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("Hello from gen-ai!")
    print("OPENAI_API_KEY loaded:", bool(os.getenv("OPENAI_API_KEY")))
    print("GROQ_API_KEY loaded: ", bool(os.getenv("GROQ_API_KEY")))
    print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
    print("MISTRAL_API_KEY loaded:", bool(os.getenv("MISTRAL_API_KEY")))


if __name__ == "__main__":
    main()
