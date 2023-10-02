import os
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo-16k-0613", temperature=0)

response = llm.predict("How are you?")
print(response)