from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

tavily_search = TavilySearchResults(max_results=5)
search_docs = tavily_search.invoke("¿Qué son las apariciones Marianas?")
print(search_docs)