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

import Research_Agent as RA

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_human_input(quiry):
    return input(quiry)

# Implement tools
tools = [
    Tool(
        name = "Research",
        func = RA.do_research,
        description = "useful for when you need to answer questions about current events, or need things from the internet. You should ask targeted questions"
    ),
    Tool(
        name = "get_human_input",
        func = get_human_input,
        description = "useful for when you need further elaboration on the quiry you've been asked, or for when you need information about the human asking it."
    )]

# Create memory
MEMORY_KEY = "chat_history"
memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)

# Create llm and prompt
llm=ChatOpenAI(temperature=0, model = "gpt-3.5-turbo-16k-0613", openai_api_key=openai_api_key)
system_message = SystemMessage(content= """You are a devoted personal assistant, helping your human with a large variety of things.
                               You always try to be as helpful as possible, and you take your own initiative to decide which answers would best help your human.
                               
                               When doing anything, please keep the following things in mind:
                               // Only provide necessary information.
                               // When asked a question, try to think "Would I be able to provide a more helpful answer if I ask the human for more information?" For example: Human: "What's the weather like?" Thought: "It would be most helpful to the human, if my answer depicts their location" Action: get_human_input("Where do you live?")
                               // If a task consists of multiple objetives, you will split it up and do each objective in a series of actions.
                               // When doing research, you will use the output you give as a baseline for your knowledge, but create your own explanation, specifically focused on the original user quiry.""")
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
    # response_audio = gTTS(text=response, lang=language)
    # response_audio.save('responseFile.mp3')

    # # Play audio with playsound
    # playsound('responseFile.mp3')
    # os.remove('responseFile.mp3')