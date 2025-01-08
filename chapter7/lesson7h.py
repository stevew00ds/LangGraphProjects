from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI
import asyncio


llm = ChatOpenAI(model="o1-preview", temperature=1, disable_streaming=False)

graph_builder = StateGraph(MessagesState)


def chatbot(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

input = {"messages": {"role": "user", "content": "how many r's are in strawberry?"}}
try:
    for event in graph.stream_events(input, version="v2"):
        if event["event"] == "on_chat_model_end":
            print(event["data"]["output"].content, end="", flush=True)
except:
    print("Streaming not supported!")