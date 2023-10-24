import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains.openai_functions import create_openai_fn_chain
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import SimpleSequentialChain
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import Tool
from langchain.agents import AgentExecutor

from Tools import Research_Agent, Base_Tools

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0, model = "gpt-3.5-turbo-16k-0613", openai_api_key=openai_api_key)

# Instruction constructor AI
def construct_instructions(query):
    prefix = """
    You are an instructor with a specific set of tools availabe. You get a query from a user, and determine which tools, if any, to use and how, and input that to a list of instructions that would result in the best and most helpful answer to the query.
    These are your available tools:
    Search(For searching things on the internet)
    Research(For doing in depth research)
    Follow up question(For asking the user a follow up question)

    Do not instruct on anything outside of these tool's capabilities
    """

    examples = [{"query": "Who's the current prime minister?", "instructions": "1: Ask which country the user is referring to.\n2: Search for the prime minister of the country."},
                {"query": "How do I breed sniffers in minecraft?", "instructions": "1: Research sniffers in minecraft.\n2: Explain how to breed sniffers in minecraft"},]    
    example_template = """
        query: {query}
        instructions:
        {instructions}
    """
    example_prompt = PromptTemplate(template=example_template,
                            input_variables=["query", "instructions"])

    constructorPrompt = FewShotPromptTemplate(
        prefix=prefix,
        examples=examples, example_prompt=example_prompt, example_separator="",
        suffix="""
        query: {input}
        instructions:\n""",
        input_variables=["input"])

    constructorChain = LLMChain(llm=llm, prompt=constructorPrompt)
    return constructorChain.run(query)

# Instruction executor AI
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

system_message = SystemMessage(content="""You are designed to execute instructions, you are given a list of instructions, and will use your available functions to execute those instructions.
Execute these instructions:""")

prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

instructions = construct_instructions("Where is my cat?")
print(f"generated instructions:\n{instructions}")
response = agent_executor.run(instructions)
print(response)
# Memory

# Human input

# Research