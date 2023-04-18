import re
from flask import Flask, request, jsonify,render_template,redirect
import openai
from twilio.twiml.messaging_response import MessagingResponse
import uuid  
import json
from chatgpt import GPT


app = Flask(__name__,static_folder='static')
server = "https://39a8-13-234-78-3.in.ngrok.io/"

@app.route("/")
def signup():

    return render_template("form.html")


@app.route("/plan_id/<planid>/")
def plhome(planid):
    id = planid
 
    file_name = f"{planid}.json"
    data_table={} 
    with open(file_name , "r") as jsonFile:
        data_table = json.load(jsonFile)
    jsonFile.close()
    return render_template("table.html", table=data_table['table'],col=list(data_table['table']['Workstream'][0]['Table'][0].keys()))
 

@app.route("/get")
def get_bot_response():
 
    msg = request.args.get("msg")
    id = request.args.get("id")
    cmny = request.args.get("cmny")
    x=GPT(id,cmny)
    try:
        ans = x.bot(msg)
    except Exception as e:
        print(e)
        ans="Can you kindly resend the information as there seems to have been a rate limiting error with ChatGPT?"
        pass
    
    
    return ans

@app.route("/info", methods=["POST"])
def sbot_gpt():
 
    id = str(request.values.get("From", ""))+"_shareos"
    incoming_msg = request.values.get("Body", "")
    chat_model=GPT(id,"infoagent")
    answer = chat_model.bot(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message(answer)
     
    return str(resp)

@app.route("/chat/<name>/")
def home(name):
    id = str(uuid.uuid4())
    print(name, id)
    file_name = name + ".json"
    if True:
        with open(file_name, encoding="utf8") as outfile:
            data = json.load(outfile)
        outfile.close()

        return render_template("chat.html", name=name, id=id, start=data["start_chat"]) 
#https://example.com/redirect?code=kihqCC8eeLETGNO4bU0dhFTV6hasPu
if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=8000 ,debug=True)
