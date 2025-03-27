import pandas as pd
import duckdb
from typing import Union
from typing_extensions import Literal, Any
from langchain_core.messages import AnyMessage
from pydantic import BaseModel
from rag import rag
from langchain.tools.retriever import create_retriever_tool
from config.config import Config

def initialize_retriever_tool(config: Config):
    retriever_tool = create_retriever_tool(
        rag.init_chroma_retiever(config),
        "retrieve_open_source_info",
        "Search and return information about open source like features and examples from opensource.txt",
    )
    return retriever_tool

def querycsv(query: str) -> str:
    """
query resource.csv using SQL only. The resource.csv contains subject and marks column.
Table name in SQL is always df
    """
    df = pd.read_csv("resources/resource.csv")
    query = query.replace("resource.csv", "df")

    mod_df = duckdb.query(query).df()
    return mod_df.to_string()

def read_text() -> str:
    """
read test.txt file from resources directory and return results.
    """
    f = open("resources/test.txt", "r")
    contents = f.read()
    return contents

def csv_tools_condition(
    state: Union[list[AnyMessage], dict[str, Any], BaseModel],
    messages_key: str = "messages",
) -> Literal["tools", "__end__"]:
    if isinstance(state, list):
        ai_message = state[-1]
    elif isinstance(state, dict) and (messages := state.get(messages_key, [])):
        ai_message = messages[-1]
    elif messages := getattr(state, messages_key, []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") or hasattr(ai_message, "tool_call") and len(ai_message.tool_calls) > 0:
        return "csv_tools"
    return "__end__"

def txt_tools_condition(
    state: Union[list[AnyMessage], dict[str, Any], BaseModel],
    messages_key: str = "messages",
) -> Literal["tools", "__end__"]:
    if isinstance(state, list):
        ai_message = state[-1]
    elif isinstance(state, dict) and (messages := state.get(messages_key, [])):
        ai_message = messages[-1]
    elif messages := getattr(state, messages_key, []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") or hasattr(ai_message, "tool_call") and len(ai_message.tool_calls) > 0:
        return "txt_tools"
    return "__end__"

def router_condition(
    state: Union[list[AnyMessage], dict[str, Any], BaseModel],
    messages_key: str = "messages",
) -> Literal["tools", "__end__"]:
    if isinstance(state, list):
        ai_message = state[-1]
    elif isinstance(state, dict) and (messages := state.get(messages_key, [])):
        ai_message = messages[-1]
    elif messages := getattr(state, messages_key, []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    ai_message_str = ai_message.dict()["content"]
    if "normal_query" in ai_message_str:
        return "normal_query"
    elif "query_file" in ai_message_str:
        return "txt_agent_input"
    elif "query_csv" in ai_message_str:
        return "csv_agent_input"
    
    return "normal_query"