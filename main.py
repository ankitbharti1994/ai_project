from dataclasses import field
from this import d
from turtle import mode
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from urllib3.util import response
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from tavily import TavilyClient
from langchain_tavily import TavilySearch

# For structured output
from typing import List
from pydantic import BaseModel, Field

# load environment variables like API Key
load_dotenv()

class Source(BaseModel):
    """Schema for a source used by the agent"""

    url:str = Field(description="URL of the source")


class AgentResponse(BaseModel):
    """Schema for the agent response with answer and sources"""

    answer:str = Field(description="The agent's answer to the query")
    sources: List[Source] = Field(default=list, description="The list of sources used to generate the answer")
    

def main():
    """Entry point: prints a greeting and runs model testing."""
    print("Hello from ai-project!")
    # model_testing()
    agentTesting()
    
def agentTesting():
    llm = ChatOpenAI(model="gpt-5")
    # tools = [search]
    tools = [TavilySearch()]
    agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)
    result = agent.invoke({"messages": HumanMessage("How is the wheather in Hyderabad, India ?")})
    print(result)

@tool
def search(query: str):
    """
    Tool that search over internet

    Args:
        query: The user's search query string.

    Returns:
        return the search response based on user query.
    """
    print(f'human query is: {query}')
    tavily = TavilyClient()
    return tavily.search(query=query)

    
def model_testing():
    """Runs a sample LLM chain: summarizes given text via a prompt template and Ollama."""
    information = """
    Mahendra Singh Dhoni ⓘ; born 7 July 1981) is an Indian professional cricketer who plays as a right-handed batter and a wicket-keeper. Widely regarded as one of the most prolific wicket-keeper batsmen and captains, he represented the Indian cricket team and was the captain of the team in limited overs formats from 2007 to 2017 and in Test cricket from 2008 to 2014. Dhoni has captained the most international matches and is the most successful Indian captain. He has led India to victory in the 2007 ICC World Twenty20, the 2011 Cricket World Cup, and the 2013 ICC Champions Trophy, being the only captain to win three different limited overs ICC tournaments. He also led the teams that won the Asia Cup in 2010 and 2016, and he was a member of the title winning squad in 2018.

    Born in Ranchi, Dhoni made his first class debut for Bihar in 1999. He made his debut for the Indian cricket team on 23 December 2004 in an ODI against Bangladesh and played his first test a year later against Sri Lanka. In 2007, he became the captain of the ODI team before taking over in all formats by 2008. Dhoni retired from Test cricket in 2014 but continued playing in limited overs cricket till 2019. He has scored 17,266 runs in international cricket including 10,000 plus runs at an average of more than 50 in ODIs.

    In the Indian Premier League (IPL), Dhoni plays for Chennai Super Kings (CSK), leading them to the final on ten occasions and winning it five times (2010, 2011, 2018, 2021 and 2023) jointly sharing this record with Rohit Sharma. He has also led CSK to two Champions League T20 titles in 2010 and 2014. Dhoni is among the few batsmen to have scored more than five thousand runs in the IPL, as well as being the first wicket-keeper to do so.

    In 2008, Dhoni was awarded India's highest sport honour Major Dhyan Chand Khel Ratna Award by Government of India. He received the fourth highest civilian award Padma Shri in 2009 and third highest civilian award Padma Bhushan in 2018. Dhoni holds an honorary rank of Lieutenant colonel in the Parachute Regiment of the Indian Territorial Army which was presented to him by the Indian Army in 2011. In June 2025, he was inducted into ICC Cricket Hall of Fame.
    """

    summary_template = """
    Given the information {information} about a person, I want you to create:
    1. A short summary of the person's life
    2. Two interestig facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        template=summary_template
        )

    # llm = ChatOpenAI(temperature=0, model="gpt-5")
    llm = ChatOllama(temperature=0, model="gemma3:270m")
    chain = summary_prompt_template | llm
    response = chain.invoke(input={'information': information})
    print(response.content)

if __name__ == "__main__":
    main()
