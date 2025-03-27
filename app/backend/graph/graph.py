from langchain_ollama import ChatOllama
from typing import Annotated
from typing_extensions import TypedDict, Literal, Any
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from tools.tool import querycsv, csv_tools_condition,initialize_retriever_tool, txt_tools_condition, router_condition
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, AIMessage
from config.config import Config


class State(TypedDict):
    messages: Annotated[list, add_messages]

class Route(BaseModel):
    step: Literal["query_csv","query_file","normal_query"] = Field(
        None, description="The next step in the routing process"
    )


def init_graph():
    config = Config()
    graph_builder = StateGraph(State)
    csv_tools = [querycsv]
    txt_tools = [initialize_retriever_tool(config)]
    llm = ChatOllama(model=config.model_name)
    router_llm_with_structure = llm.with_structured_output(Route)
    csv_llm_with_tools = llm.bind_tools(csv_tools)
    txt_llm_with_tools = llm.bind_tools(txt_tools)

    # Nodes
    def normal_query(state: State):
        return {"messages": [llm.invoke(state["messages"])]}
    def csv_llm_input(state: State):
        x = state["messages"][-2]
        state["messages"].clear()
        state["messages"].append(x)
        return {"messages": [csv_llm_with_tools.invoke(state["messages"])]}
    
    def txt_llm_input(state: State):
        x = state["messages"][-2]
        state["messages"].clear()
        state["messages"].append(x)
        get= {"messages": [txt_llm_with_tools.invoke(state["messages"])]}
        return get
    
    def router(state: State):
        decision = router_llm_with_structure.invoke(
            [
                SystemMessage(
                content="Route the input to query_csv, query_file or normal_query based on the user's request. If user mentions a csv file in input, it will be query_csv. If user wants to understand something from text file it will be query_file. Else it will be normal_query"
                ),
                state["messages"][-1],
            ]
        )
        decision_str = decision.dict()["step"]
        ctx = ""
        if decision_str == "normal_query":
            ctx = decision_str
        else:
            ctx = decision_str + " tool_call"
        state["messages"].append(AIMessage(content=ctx))
        return state

    def describe_like_genie(state: State):
        toolMessage = str(state["messages"][-1].content)
        humanMessage = str(state["messages"][-2].content)
        response = llm.invoke(f"Describe this like a Genie. Keep answer short and precise : {humanMessage} \n{toolMessage}")
        state["messages"].append(response)
        return state
    
    def summarize_text(state: State):
        toolMessage = str(state["messages"][-1].content)
        humanMessage = str(state["messages"][-3].content)
        response = llm.invoke(f"summarize text for {humanMessage} : \n{toolMessage}")
        state["messages"].append(response)
        return state
    
    csv_tool_node = ToolNode(tools=csv_tools)
    txt_tool_node = ToolNode(tools=txt_tools)

    graph_builder.add_node("normal_query", normal_query)
    graph_builder.add_node("csv_agent_input", csv_llm_input)
    graph_builder.add_node("csv_tools", csv_tool_node)
    graph_builder.add_node("assistant", describe_like_genie)
    graph_builder.add_node("router", router)
    graph_builder.add_node("txt_agent_input", txt_llm_input)
    graph_builder.add_node("txt_tools", txt_tool_node)
    graph_builder.add_node("summarize_text", summarize_text)


    graph_builder.add_conditional_edges(
        "csv_agent_input",
        csv_tools_condition,
    )

    graph_builder.add_conditional_edges(
        "txt_agent_input",
        txt_tools_condition,
    )

    graph_builder.add_conditional_edges(
        "router",
        router_condition,
    )

    graph_builder.add_edge("csv_tools", "assistant")
    graph_builder.add_edge("txt_tools", "summarize_text")

    graph_builder.set_entry_point("router")

    graph = graph_builder.compile()
    # print(graph.get_graph().draw_ascii())
    return graph
