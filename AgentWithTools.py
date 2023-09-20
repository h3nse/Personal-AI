import os
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, tool
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor
from langchain.memory import ConversationSummaryBufferMemory
from gtts import gTTS
from playsound import playsound
import multiprocessing

import Research_Agent as RA

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(temperature=0, model = "gpt-3.5-turbo-16k-0613", openai_api_key=openai_api_key)
memory = ConversationSummaryBufferMemory(memory_key="memory", return_messages=True, llm=llm, max_token_limit=1000)

tools = [Tool(
            name = "Research",
            func = RA.do_research,
            description = "useful for when you need to answer questions about current events, or need things from the internet. You should ask targeted questions"
        )]

system_message = SystemMessage(content="You are very powerful assistant, but bad at knowing current events. If you need an answer to a question, you will use your tools to get the answer. You do not make anything up.")
prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while True:
    # Create mp3 file from text
    user_message = input()
    response = agent_executor.run(user_message)
    language = 'en'

    print(response)
    # response_audio = gTTS(text=response, lang=language)
    # response_audio.save('responseFile.mp3')

    # # Play audio with playsound
    # playsound('responseFile.mp3')
    # os.remove('responseFile.mp3')