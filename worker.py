from flask import Flask
from flask import request
import requests
import os
import json
app = Flask(__name__)

def get_api_key() -> str:
    secret = os.environ.get("COMPUTE_API_KEY")
    if secret:
        return secret
    else:
        #local testing
        with open('.key') as f:
            return f.read()
      
@app.route("/")
def hello():
    return "Add workers to the Spark cluster with a POST request to add"

@app.route("/test")
def test():
    #return "Test" # testing 
    return(get_api_key())

@app.route("/add",methods=['GET','POST'])
def add():
  if request.method=='GET':
    return "Use post to add" # replace with form template
  else:
    token=get_api_key()
    ret = addWorker(token,request.form['num'])
    return ret


def addWorker(token, num):
    with open('payload.json') as p:
      tdata=json.load(p)
    tdata['name']='slave'+str(num)
    data=json.dumps(tdata)
    url='https://www.googleapis.com/compute/v1/projects/try2-371019/zones/europe-west1-b/instances'
    headers={"Authorization": "Bearer "+ token}
    auth = "Authorization: Bearer ya29.a0AX9GBdWk2rBWMWyg0hEtmw2TYfFaW2TEiEbGUM-biaH_pNk6h_GlivienRbkm75KUraixg4xU3wDk9xPDwy8Yl9s0s5GwdXIsEVjMCORCvaEaBHPupZpQzg0C9d9HdXn_gLD6_LQZmbm4gh_3ngI5Xl43IYkxNnxBTtFkBsXqAmpyHfBH_Lyfl5WaSCkn9E4o3wQNUGnmsvyn8VAH3cvei5OE3VOWFuPOP716sIaCgYKAZoSARASFQHUCsbCUt5rnBLaiIzZdbh7bNOdAQ0238"
    #resp=requests.post(url,auth=auth, data=data)
    #if resp.status_code==200:     
    return data
    #else:
    #  print(resp.content)
    #  return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data
    #  return "ERROR"



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
