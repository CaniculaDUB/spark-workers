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
    #headers={"Authorization": "Bearer "+ token}
    url = "https://www.googleapis.com/compute/v1/projects/try2-371019/zones/europe-west1-b/instances"

    headers = {
        'Authorization': 'Bearer ya29.a0AX9GBdX8THSRMdcrUPcaZ9aieG_UpT7FGEfqA_WQZF-T-8xZgc2ABOgV4jnUNz4AbB0Yxj8X-bgxrgkDBjvwNo5aRDW1237OmBIBBK0A0cxasn76vO6jl5BnFCUs-oxPdwFVkLjLASl0zeeMmkISysh1pAEphkPmUkrcZGQ35hQTGF4zD4mUN4DxJcD9AVNNESNeAhtZjKzTY1yN8W4w3s-FWgcw8TyTo4ZnUCsaCgYKATYSARASFQHUCsbCQZ2uLdn3NUxbKRc-R1uijg0238',
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=data)

   
    if response.status_code==200:     
        return "Done"
    else:
       print(resp.content)
       return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data
       return "ERROR"



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
