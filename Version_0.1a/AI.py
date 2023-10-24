import os
from dotenv import load_dotenv
import sys
import wave
import pyaudio
import threading
import io
from pydub import AudioSegment

from langchain.agents import AgentExecutor
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

from gtts import gTTS
from playsound import playsound

from Tools import Research_Agent, Base_Tools
from Functions.Respond import Respond

Debugging = True

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Implement tools
tools = [
    Tool(
        name = "Research",
        func = Research_Agent.do_research,
        description = "useful for when you need an in depth answer. You should ask targeted questions"
    ),
    Tool(
        name = "get_human_input",
        func = Base_Tools.get_human_input,
        description = "useful for when you need further elaboration on the quiry you've been asked, or for when you need information about the human asking it. You should sound pleasant when asking."
    ),
    Tool(
        name = "quick_search",
        func = Base_Tools.quick_search,
        description = "Useful for small searches with quick answers, or for getting a small amount of information about something. Ask targeted questions."
    )]

# Create memory
MEMORY_KEY = "chat_history"
memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)

# Create llm and prompt
llm=ChatOpenAI(temperature=0, model = "gpt-3.5-turbo-16k-0613", openai_api_key=openai_api_key)
system_message = SystemMessage(content= """You are a devoted personal assistant, helping your human with a large variety of things, through a large selection of tools.
                               You always try to be as helpful as possible, and you take your own initiative to decide which answers would best and most concisely help your human.
                               
                               When doing anything, please keep the following things in mind:
                               // Only provide necessary information.
                               // When asked a question, try to think "Would I be able to provide a more helpful answer if I ask the human for more information?". I.e. specifics about them such as where they're located etc.
                               // If a task consists of multiple objetives, you will split it up and do each objective in a series of actions.
                               // When doing research, you will use the output as a baseline for your knowledge, but create your own explanation, specifically focused on the original user quiry.""")
prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=system_message,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)])

# Create agent and agent executor with memory
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt, memory=memory)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=Debugging)

while True:
    user_message = input('>')
    response = agent_executor.run(user_message)

    Respond(response)
