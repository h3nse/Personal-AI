import os
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.agents import tool
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(temperature=0, model = "gpt-3.5-turbo-16k-0613", openai_api_key=openai_api_key)

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

tools = [get_word_length]

system_message = SystemMessage(content="You are very powerful assistant, but bad at calculating lengths of words.")
prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.run("how many letters in the word educa?")