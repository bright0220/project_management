from flask import Flask, render_template, request
import random
import json
import uuid
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import time
app = Flask(__name__,static_folder='static')

server = "https://19f7-13-232-83-0.in.ngrok.io/"

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

#except Exception as e:
       # print(e)
        #return render_template("fail.html", link=server)


@app.route("/payment/<id>/")
def pay(id):
    id =id
   
    file_name = str(id) + ".json"
    try:
        with open(file_name) as outfile:
            data = json.load(outfile)
        outfile.close()
        try:
            tgs=data['tags'][0]
            if len(tgs)>=4:
                tgs=tgs[:3]
        except:
            tgs=data['tags']
    except:
        pass
    return render_template("payment.html", agent_name=data['agent_name'], company_name=data['company_name'], bot_info=data["bot_info"],tags=tgs,name=data['name'])

@app.route("/get")
def get_bot_response():
    msg = request.args.get("msg")
    id = request.args.get("id")
    cmny = request.args.get("cmny")
    if cmny.lower() == "instill":
        x = Chat_new(id)
    elif cmny.lower() == "celli":
        x = Cell_GPT(id,cmny)
    else:
        x=GPT(id,cmny)
   # try:
    ans = x.bot(msg)
   # except Exception as e:
       # print(e)
        #ans="Can you kindly resend the information as there seems to have been a rate limiting error with ChatGPT?"
       # pass
    
    if "AI" in ans:
        ans = ans[4:]
    return ans

@app.route("/spreebot_gpt", methods=["POST"])
def sbot_gpt():

    id = str(request.values.get("From", ""))+"_spree"
    incoming_msg = request.values.get("Body", "")
    chat_model=GPT(id,"spree")
    answer = chat_model.bot(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message(answer)
    time.sleep(2.5)
    return str(resp)

@app.route("/spreebot_gpt_spc", methods=["POST"])
def spcbot_gpt():

    id = str(request.values.get("From", ""))+"_spree"
    incoming_msg = request.values.get("Body", "")
    chat_model=GPT(id,"chase_chewning")
    answer = chat_model.bot(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message(answer)
    time.sleep(2.5)
    return str(resp)

@app.route("/spree_payment")
def spayment_gpt():    
    return render_template('payment_link_spree.html')

@app.route("/success")
def sucess_gpt():    
    return render_template('success.html')


@app.route("/cellibot_gpt", methods=["POST"])
def cellibot_gpt():

    id = str(request.values.get("From", ""))+"_celli"
    incoming_msg = request.values.get("Body", "")
    chat_model=Cell_GPT(id,"celli")
    answer = chat_model.bot(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message(answer)
    
    return str(resp)

 

@app.route("/handle_data", methods=["post"])
def handle_data():
    name = request.form["name"]
    link = request.form["url"]
    try:
        keywrd = request.form["keywordsa"]
    except:
        keywrd = ""
    res = False
    print(name, link)
    res_obj = Extract(link, name, keywrd)

    try:

        res = res_obj.combine()
    except Exception as e:
        print("------------------------")
        print(e)
        print("========================")

    print(res)

    # import time
    # time.sleep(10)
    name_cmny = "_".join(name.split())
    link = server + "chat/" + name_cmny + "/"
    if res:
        return render_template("success.html", link=link)
    else:
        return render_template("fail.html", link=server)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)
# while True:
#     input("u")
#     id = str(request.values.get("WaId", ""))
#     incoming_msg = request.values.get("Body", "")
#     chat_model=GPT(id,"spree")
#     answer = chat_model.bot(incoming_msg)
#     print(answer)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)