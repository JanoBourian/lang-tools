import random
from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

# State
class State(TypedDict):
    """
    Represents the state of the graph
    """
    graph_state: str

# Nodes
def node_1(state: State) -> dict:
    """
    Node 1
    """
    print("--Node 1---")
    return {"graph_state": state.get("graph_state", "") + "I am"}

def node_2(state: State) -> dict:
    """
    Node 2
    """
    print("--Node 2---")
    return {"graph_state": state.get("graph_state", "") + " happy!"}

def node_3(state: State) -> dict:
    """
    Node 3
    """
    print("--Node 3---")
    return {"graph_state": state.get("graph_state", "") + " sad!"}

# Edges
def decide_mood(state: State) -> Literal["node_2", "node_3"]:
    """
    Decide the mood of the graph
    """
    print("--Decide Mood---")
    return random.choice(["node_2", "node_3"])

# Graph Construction

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

result = graph.invoke(input={"graph_state": "Hi, this is John Doe. "})
print(result)