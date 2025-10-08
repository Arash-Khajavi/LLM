from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import  wiki_tool, save_tool, israelipedia_search,google
from flask import Flask,render_template,redirect,url_for,request,jsonify
import random
import string
import os
emails=[]
j1=[]
k=[]
app=Flask(__name__,template_folder='Templates')
@app.route("/",methods=["POST","GET"])
def IsraelGPT():
 if request.method == "POST":
    user=request.form.get("user1")
    email=request.form.get("email")
    if str(email) not in emails:
        j1.append(str(email))
        return redirect(url_for("code"))
    class ResearchResponse(BaseModel):
        topic: str
        summary: str
        output: str
        sources: list[str]
        tools_used: list[str]
    # openai.api_key=token
    llm= ChatOpenAI(model="gpt-4o-mini",
    api_key=os.getenv("APIKEY"),
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
@app.route("/deepseek")

@app.route("/l")
def ch():
    return render_template("email.html")
lo=[]
lp=[]
# @app.route("/oi")
# def oi():
li=random.choices(string.digits, k=6)
@app.route("/code",methods=["POST","GET"])
def code():
    # lp=[]
    # max_retries = 5
    # base_wait_time = 2
    # # if request.method == "POST":
    # if request.method == "POST":
    #             code = request.form.get("code")
                # email=request.form.get("email")
     # if email not in signed_in_users:
     #     return redirect(url_for("sign_in"))
     # else:
                # language = request.form.get("language of response")
                # user = request.form.get("user")
                # email2=request.form.get("email1")
                # email1=input("")
                import smtplib
                from email.message import EmailMessage
                l=[]
                # Configure your Outlook email credentials
                OUTLOOK_EMAIL = os.getenv("EMAIL")  # Replace with your Outlook email address
                OUTLOOK_PASSWORD = "zvju tgad kioo pspy"  # Replace with your password or App Password
                email = EmailMessage()
                email["from"] = "Mosh Khajavi"  # Replace with your name
                email["to"] = f"{j1[0]}"  # Replace with the recipient's email address
                # print(str(email2))
                email["subject"] = "scholarship and registration"
                # lu=random.randint(0,9)
                email.set_content(
                    "".join(li)
                )
                p = []
                # p.append(li)
                # Send the email using Outlook's SMTP server
                # e=str(email2)
                # lp.append(e)
                # for e in str(email2):
                #     p.append(e)
                # pr = "".join(p)
                # lp.append(str(pr))
                # print(lp)
                # try:
                k=[]
                with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
                        smtp.ehlo()  # Identify yourself to the server
                        smtp.starttls()  # Secure the connection
                        smtp.login(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)  # Log in to your Outlook account
                        smtp.send_message(email)
                        k.append(email)# Send the email

                        # return str(email)
        #                 print(str(email).split("1.0")[1].strip())
        #                 if str(code) == str(str(email).split("1.0")[1].strip()):
        # #             lk.append(j1[0])
        # #             print(lk)
        #
        #
        #
        # #             #  re=request.form.get("choice1")
        # #             #  if str(re) == "fast":
        #                     j1.clear()
        #                     return redirect(url_for("IsraelGPT"))
                if request.method == "POST":
                 code = request.form.get("code")
                 print(str(email).split("1.0")[1].strip())
                 if str(code) == str(str(email).split("1.0")[1].strip()):
                 #             lk.append(j1[0])
                 #             print(lk)
                 #             #  re=request.form.get("choice1")
                 #             #  if str(re) == "fast":
                 #                     k.append(j1[0])
                 #                     j1.clear()
                                     emails.append(j1[0])
                                     return redirect(url_for("IsraelGPT"))
                            #  elif str(re) == "slow":
                            #   return redirect(url_for("chat"))
                # else:
                #             import time
                #             time.sleep(10)
                            # li="".join(random.choices(str//
                            # return redirect(url_for("oi"))
                            # li=random.choices(string.digits,k=6)
                            # return f"unsuccessful , {str(code)} , {str(li)}"
                # except:
                #     pass
                    # if str(code) == str(email).split("1.0")[1].strip():
                    #     lk.append(lp[0])
                    #     print(lk)
                    #     # if request.method == "POST":
                    #     #  re=request.form.get("choice1")
                    #     #  if str(re) == "fast":
                    #     return redirect(url_for("IsraelGPT"))
                    #     #  elif str(re) == "slow":
                    #     #   return redirect(url_for("chat"))
                    # else:
                    #     import time
                    #     time.sleep(10)
                    #     # li="".join(random.choices(str//
                    #     # return redirect(url_for("oi"))
                    #     # li=random.choices(string.digits,k=6)
                    #     # return f"unsuccessful , {str(code)} , {str(li)}"


                return redirect(url_for("ch"))
    # return render_template("fl.html")
if __name__ == "__main__":
 app.run(debug=True)
