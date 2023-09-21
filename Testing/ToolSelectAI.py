import os
from dotenv import load_dotenv

from langchain.agents import AgentExecutor
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

from gtts import gTTS
from playsound import playsound

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Implement tools
def weather(location):
    return "It is sunny today!"

tools = [
    Tool(
        name = "weather",
        func = weather,
        description = "Gives the current weather"
    )]

# Create memory
MEMORY_KEY = "chat_history"
memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)

# Create llm and prompt
llm=ChatOpenAI(temperature=0, model = "gpt-3.5-turbo-16k-0613", openai_api_key=openai_api_key)
system_message = SystemMessage(content="You are a friendly personal assistant")
prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=system_message,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)])

# Create agent and agent executor with memory
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt, memory=memory)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

# Input/Output
while True:
    # Create mp3 file from text
    user_message = input('>')
    response = agent_executor.run(user_message)
    language = 'en'

    print(response)
    response_audio = gTTS(text=response, lang=language)
    response_audio.save('responseFile.mp3')

    # Play audio with playsound
    playsound('responseFile.mp3')
    os.remove('responseFile.mp3')