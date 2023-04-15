import openai
import re
import json
import requests
import uuid
OPENAI_API_KEY = "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"


class GPT:
    def __init__(self, id, cmny):
        self.id = id
        self.cmny = cmny
        self.data = {}
        with open(f"{self.cmny}.json") as outfiles:
            self.data = json.load(outfiles)
        outfiles.close()

        self.file_name = f"{str(self.id)}.json"
        self.session = {
            "start": True,
            "start_chat": self.data["start_chat"],
            "log": [
                {"role": "system", "content": self.data["prmt"]},
                {
                    "role": "assistant",
                    "content": self.data["start_chat"],
                },
            ],
            "flag_website":self.data.get("flag_website"),
            "flag_plan":self.data['flag_plan'],
            "url":self.data['url'],
        }

        try:
            with open(self.file_name) as outfile:
                data = json.load(outfile)
            outfile.close()
            self.session = data
        except Exception:
            with open(self.file_name, "w") as outfile:
                json.dump(self.session, outfile)
            outfile.close()

    def bot(self, input_query):
        if self.session["flag_plan"]:
            self.session['flag_plan']=False    
            with open(self.file_name, "w") as jsonFile:
                json.dump(self.session, jsonFile)
            jsonFile.close() 
            return self.session['url']    
        if self.session["start"]:
            self.session['start']=False    
            with open(self.file_name, "w") as jsonFile:
                    json.dump(self.session, jsonFile)
            jsonFile.close()
            return self.session['start_chat']    
        # if self.session["flag_website"]:
        #     if "http" in input_query:
        #         input_query=input_query.replace("http://","")
        #     if "https" in input_query:    
        #         input_query=input_query.replace("https://","")
        #     web = re.findall("^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$", input_query)
            # print(web)
            # if len(web)>=1:
            #     web_data=scrape_website(web[0])
            #     tmp=self.session["log"][0]["content"]
            #     tmp=tmp.format(probelm_solving=web_data)
            #     self.session["log"][0]["content"]=tmp
            #     self.session["flag_website"]=False

        openai.api_key = OPENAI_API_KEY

        self.session["log"].append({"role": "user", "content": input_query})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.session["log"],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

        )

        res = response["choices"][0]["message"]["content"]
        if "drafted" in res:
                tmp=self.session["log"][1:]
                cov=""
                for i in tmp:
                     cov+=i['content']+"\n\n"
                tses=[
                {"role": "system", "content": "understand the whole conversation extract the below\n\nOutput:\nVenture Info:\nStage:\nWorkstreams:\nGoals:\nTeam Lead:"},
                {
                    "role": "user",
                    "content":cov,
                }
                ]
                intresponse = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=tses,
                    temperature=0.7,
                    max_tokens=1800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0

                )
                intres = intresponse["choices"][0]["message"]["content"]
                 
                ids= str(uuid.uuid4())
                prmtt="Generate a simple tracking table for the given venture , stage, workstream  and goal.Include columns for Task,\tTime/Speed (days),\tCost ($),\tJob Function,\tSeniority\tType, Team Lead Name\t,Execution Score\tPerformance Score,\tVisual Outputs and Comments.List tasks related to creating a functional prototype may involve various team members, priorities, and time frames. \n\n .List tasks related to creating a functional prototype may involve various team members, priorities, and time frames. \n\nInput:\n\n Venture Info:\nStage:\nWorkstreams:\nGoals:\nTeam Lead:\n\nOutput: \n\n{\n\"Venture\": \"\",\n\"Stage\": \"\",\n\"Workstream\": [\n{\n\"Name\": \"\",\n\"Goal\": \"\",\n\"Table\": [{}]\n}\n]\n}"
                ses=[
                {"role": "system", "content": prmtt},
                {
                    "role": "user",
                    "content":intres,
                }
                ]
                sintresponse = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=ses,
                    temperature=0.7,
                    max_tokens=1800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0

                )
                outs=sintresponse["choices"][0]["message"]["content"].strip()
                outs=outs[outs.index("{"):]
                print(outs)
                sintres = json.loads(outs)
                sfile_name=str(ids)+".json"
                with open(sfile_name, "w") as jsonFile:
                        json.dump({"table":sintres}, jsonFile)
                jsonFile.close()
                
                res=res+"\n"+"https://65af-43-205-230-148.in.ngrok.io/"+str(ids)+"\nThank You"
                print(res)
                if self.session['flag_plan']==False:
                     self.session['flag_plan']=True
                     self.session['url']="https://65af-43-205-230-148.in.ngrok.io/plan_id/"+str(ids)+"\nThank You"

        self.session["log"].append({"role": "assistant", "content": res})
        with open(self.file_name, "w") as jsonFile:
            json.dump(self.session, jsonFile)
        jsonFile.close()

        return res


