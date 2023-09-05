import os
from dotenv import load_dotenv

import requests
from gtts import gTTS
from playsound import playsound
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
    
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

template = """You are a helpful personal assistant, you act like a gentleman, and speak like so."""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
chain = LLMChain(
    llm=ChatOpenAI(temperature=1, model = "gpt-3.5-turbo-16k-0613", openai_api_key="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"),
    prompt=chat_prompt
)

while True:
    # Create mp3 file from text
    user_message = input()
    response = chain.run(user_message)
    language = 'en'

    print(response)
    response_audio = gTTS(text=response, lang=language)
    response_audio.save('responseFile.mp3')

    # Play audio with playsound
    playsound('responseFile.mp3')
    os.remove('responseFile.mp3')