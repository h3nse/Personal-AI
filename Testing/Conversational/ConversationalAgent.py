import os
from dotenv import load_dotenv

from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from gtts import gTTS
from playsound import playsound
from langchain.schema import SystemMessage

load_dotenv() 
openai_api_key = os.getenv("OPENAI_API_KEY")

def weather(location):
    return "It is sunny today!"

tools = [
    Tool(
        name = "weather",
        func = weather,
        description = "Gives the current weather"
    )]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
system_message = SystemMessage(content="You are a friendly gentleman named James, you will do your best to give varied responses, and act like a gentleman")
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")],
    "system_message": system_message,
}

agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, agent_kwargs=agent_kwargs, memory=memory)

while True:
    # Create mp3 file from text
    user_message = input()
    response = agent_chain.run(user_message)
    language = 'en'

    print(response)
    response_audio = gTTS(text=response, lang=language)
    response_audio.save('responseFile.mp3')

    # Play audio with playsound
    playsound('responseFile.mp3')
    os.remove('responseFile.mp3')