from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool, israelipedia_search,google
from flask import Flask,render_template,redirect,url_for,request,jsonify
import random
import os
import string
emails=[]
j1=[]
# k=[]
app = Flask(__name__, template_folder='Templates')  # this is default; no need unless using custom folder
@app.route("/",methods=["POST","GET"])
def IsraelGPT():
 if request.method == "POST":
    user=request.form.get("user1")
    email=request.form.get("email")
    # if str(email) not in emails:
    #     j1.append(str(email))
    #     return redirect(url_for("code"))
    class ResearchResponse(BaseModel):
        topic: str
        summary: str
        output: str
        sources: list[str]
        tools_used: list[str]
    # openai.api_key=token
    llm= ChatOpenAI(model="gpt-4o-mini",
    api_key=os.getenv("LLM"),
    temperature=0.7
    )
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)
    # print(completion.choices[0].message)
    # messages=[
    #         SystemMessage(content="You are a helpful assistant."),
    #         HumanMessage(content=user)
    # ]
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a research assistant that will help generate a research paper.
                Answer according to Iran's football status.
                Wrap the output in this format and provide no other text\n{format_instructions}
                """,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    tools = [wiki_tool,save_tool,israelipedia_search,google]
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    query = user
    # query+="answer me with an israeli perspective. but don't mention that it is an israeli perspective "
    raw_response = agent_executor.invoke({"query": query})
    try:
        output_json_string = raw_response["output"]

        # Step 2: Parse the JSON string to a Python dict
        # output_dict = json.loads(output_json_string)
        # Step 3: Now pass it to the parser
        structured_response = parser.parse(output_json_string)
        j=str(structured_response).find("sources")

        k=str(structured_response).find("summary")
        return f"{str(structured_response)},{render_template("fl.html")}"
    except Exception as e:
        return "Error parsing response", e, "Raw Response - ", raw_response
 return render_template("fl.html")
if __name__ == "__main__":
   port = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=port)
