from langchain_ollama import ChatOllama
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from tools.tool import querycsv

class State(TypedDict):
    messages: Annotated[list, add_messages]

def init_graph():
    graph_builder = StateGraph(State)
    tool = querycsv
    tools = [tool]
    llm = ChatOllama(model="granite3.2:2b")
    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    def describe_like_genie(state: State):
        toolMessage = str(state["messages"][-1].content)
        humanMessage = str(state["messages"][-2].content)
        response = llm.invoke(f"Describe this like a Genie. Keep answer short and precise : {humanMessage} \n{toolMessage}")
        state["messages"].append(response)
        return state


    graph_builder.add_node("chatbot", chatbot)

    tool_node = ToolNode(tools=[tool])
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_node("assistant", describe_like_genie)

    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    # Any time a tool is called, we return to the chatbot to decide the next step
    graph_builder.add_edge("tools", "assistant")
    graph_builder.add_edge("assistant", "chatbot")

    graph_builder.set_entry_point("chatbot")
    graph = graph_builder.compile()

    return graph
