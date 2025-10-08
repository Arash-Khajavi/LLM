from langchain.tools import Tool
from datetime import datetime
from langchain_core.utils.pydantic import BaseModel
from langchain_openai.chat_models  import ChatOpenAI
from langchain.agents import create_tool_calling_agent
# Example of a Pydantic model for the tool
from langchain_core.tools import tool
from pydantic import BaseModel
from langchain_core.tools import tool
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup  # ✅ Correct
# Define the argument schema for the tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime


def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"


save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)



api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
wiki_tool = Tool(
    name="wikipedia",
    func=WikipediaQueryRun(api_wrapper=api_wrapper).run,
    description="Useful for answering questions using Wikipedia"
)


class IsraelipediaSearchArgs(BaseModel):
    query: str

# Tool function decorated properly for LangChain + OpenAI function calling
@tool(args_schema=IsraelipediaSearchArgs)
def israelipedia_search(query: str) -> str:
    """
      Searches https://www.flashscore.com/football/iran/persian-gulf-pro-league/standings/#/IkFPsKyR/table/overall for Football-related information.
      Returns the first 1000 characters of the result.
      """
    url = f"https://www.flashscore.com/football/iran/persian-gulf-pro-league/standings/#/IkFPsKyR/table/overall?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # Try to find the main content — this may need tweaking
        article = soup.find("div", class_="entry-content")
        text = article.get_text(separator=" ", strip=True) if article else "No relevant content found."

        return text[:1000]
    except Exception as e:
        return f"Error fetching data from Israelipedia: {str(e)}"
    # Simulated result for now — replace this with your real API logic if available
    return f"Simulated result from Israelipedia for query: {query}"
# google_search_url = f"https://www.google.com/search?q={query}"
class google(BaseModel):
    query: str

# Tool function decorated properly for LangChain + OpenAI function calling
@tool(args_schema=google)
def google(query: str) -> str:
    """
    Searches Google using a GET request and returns the first snippet of text.
    WARNING: This is fragile and may break due to Google blocking scrapers.
    """

    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Try getting the first answer snippet
        snippet = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
        if snippet:
            return snippet.get_text(strip=True)[:1000]

        # Fallback: get other parts of result page
        paragraphs = soup.find_all("span")
        combined_text = " ".join(p.get_text(strip=True) for p in paragraphs[:10])
        return combined_text[:1000] if combined_text else "No relevant content found."

    except Exception as e:
        return f"Error fetching Google search results: {str(e)}"
