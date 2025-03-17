from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import pandas as pd
import duckdb


model = ChatOllama(model="granite3.2:2b")

def querycsv(query: str) -> str:
    """
query resource.csv using SQL only. The resource.csv contains subject and marks column.
Table name in SQL is always df
    """
    df = pd.read_csv("app/backend/resource.csv")
    # q1= """SELECT col1 FROM df"""
    query = query.replace("resource.csv", "df")

    mod_df = duckdb.query(query).df()
    return mod_df.to_string()


tools = [querycsv]
# prompt= """
# You are an AI Agent that queries resource.csv file and give information. You always call tools with SQL Query
# """
# agent_executor = create_react_agent(model, tools=tools, prompt=prompt)
agent_executor = create_react_agent(model, tools=tools)

config = {"configurable": {"thread_id": "test"}}
for step in agent_executor.stream(
    {"messages": [HumanMessage(content="Get average over marks column. Query resource.csv")]},
    config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()