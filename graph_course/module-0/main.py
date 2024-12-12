from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

gpt4o_chat = ChatOpenAI(model="gpt-4o", temperature=0)
gpt35_chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

msg = HumanMessage(content="Hola. ¿Cómo estás?", name="Janobourian")

messages = [msg]

result = gpt4o_chat.invoke(messages)
print(result.content)
print(dir(result))
