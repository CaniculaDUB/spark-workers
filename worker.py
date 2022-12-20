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
    #resp=requests.post(url,headers=headers, data=data)
    url = "https://www.googleapis.com/compute/v1/projects/try2-371019/zones/europe-west1-b/instances"

    headers = {
        'Authorization': 'Bearer ya29.a0AX9GBdUhaKQrLlSGeKbg_7oKeQe25_Qd2n2J8HEkWtY3JHUoWFrnWbhI9mnMCGvsmOv8fD7Uqp3aNSQfDALRacwIOrnC19bgv_Q9f4Yq8x3k1-16npeVscrtFwHmPcCJ5dRydAasFjLSjul738DxIjoaRM-9YwupSpFu86NyVd-GbR3aGgXz4ob4cECDzN9hLR6ClSf3Ulb3uVAHYBzhPAOr_gCxAPfyh6NytgYaCgYKASwSARASFQHUCsbCSHX_t3QAmMJsMIjlHvTV6A0238',
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
