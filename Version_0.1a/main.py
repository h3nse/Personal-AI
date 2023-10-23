import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains.openai_functions import create_openai_fn_chain
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import SimpleSequentialChain

from Tools import Research_Agent, Base_Tools

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Instruction constructor AI
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

llm = ChatOpenAI(temperature=0, model = "gpt-3.5-turbo-16k-0613", openai_api_key=openai_api_key)

constructorChain = LLMChain(llm=llm, prompt=constructorPrompt)

# Instruction executor AI
template = """
You are designed to execute instructions, you are given a list of instructions, and will use your available functions to execute those instructions.
Execute these instructions:
{instructions}"""
executorPrompt = PromptTemplate(template=template,
                        input_variables=["instructions"])
executorChain = create_openai_fn_chain(llm=llm, prompt=executorPrompt, functions=[Research_Agent.do_research, Base_Tools.get_human_input, Base_Tools.quick_search])

# Take the outputted functions with their arguments, and call the functions

generateExecuteChain = SimpleSequentialChain(chains=[constructorChain, executorChain], verbose=True)

generateExecuteChain.run("How do I write an email?")

# Memory

# Human input

# Research