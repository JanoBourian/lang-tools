from dotenv import load_dotenv
from typing_extensions import TypedDict
from pprint import pprint
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage, AnyMessage
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

load_dotenv()

# Chats
messages = [
    AIMessage(
        content="Disculpa, ¿quieres buscar sobre las apariciones Marianas?",
        name="Model",
    ),
    HumanMessage(content="Así es, sobre eso quiero saber", name="John"),
    AIMessage(content="¡Claro! Déjame buscar", name="Model"),
    HumanMessage(content="Además quiero que me brindes ejemplos", name="John"),
]

for message in messages:
    pprint(message)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
result = llm.invoke(messages)
print(type(result))
print(result)
print(result.content)
print(result.response_metadata)


# Tools
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


def addition(a: int, b: int) -> int:
    """Sum a and b

    Args:
        a: first int
        b: sencond int
    """
    return a + b


llm_with_tools = llm.bind_tools([multiply, addition])
tool_call = llm_with_tools.invoke(
    [HumanMessage(content="What is 2 addition by 3", name="Lance")]
)
print(tool_call)
print(tool_call.additional_kwargs.get("tool_calls"))


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


initial_messages = [
    AIMessage(content="Hola, ¿cómo puedo apoyarte hoy?", name="Model"),
    HumanMessage(
        content="Estoy buscando información sobre entrenamiento canino", name="Lance"
    ),
]

new_message = AIMessage(content="Claro, ¿en qué tema estás interesado?", name="Model")

add_messages(initial_messages, new_message)


def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))
