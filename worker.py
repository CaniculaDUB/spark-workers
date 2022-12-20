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
    data={
  "canIpForward": false,
  "confidentialInstanceConfig": {
    "enableConfidentialCompute": false
  },
  "deletionProtection": false,
  "description": "",
  "disks": [
    {
      "autoDelete": true,
      "boot": true,
      "deviceName": "slave2",
      "initializeParams": {
        "diskSizeGb": "10",
        "diskType": "projects/try2-371019/zones/us-west4-b/diskTypes/pd-balanced",
        "labels": {},
        "sourceImage": "projects/debian-cloud/global/images/debian-11-bullseye-v20221206"
      },
      "mode": "READ_WRITE",
      "type": "PERSISTENT"
    }
  ],
  "displayDevice": {
    "enableDisplay": false
  },
  "guestAccelerators": [],
  "keyRevocationActionType": "STOP",
  "labels": {},
  "machineType": "projects/try2-371019/zones/europe-west1-b/machineTypes/e2-medium",
  "metadata": {
    "items": [
      {
        "key": "startup-script",
        "value": "apt update\ncurl --output spark.tgz https://dlcdn.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz\napt -y install default-jdk\ntar -xzvf spark.tgz\n./spark-3.3.1-bin-hadoop3/sbin/start-slave.sh spark://spark-master.europe-west1-b.c.try2-371019.internal:7077"
      }
    ]
  },
  "name": "slave2",
  "networkInterfaces": [
    {
      "accessConfigs": [
        {
          "name": "External NAT",
          "networkTier": "PREMIUM"
        }
      ],
      "stackType": "IPV4_ONLY",
      "subnetwork": "projects/try2-371019/regions/europe-west1/subnetworks/default"
    }
  ],
  "params": {
    "resourceManagerTags": {}
  },
  "reservationAffinity": {
    "consumeReservationType": "ANY_RESERVATION"
  },
  "scheduling": {
    "automaticRestart": false,
    "instanceTerminationAction": "STOP",
    "onHostMaintenance": "TERMINATE",
    "provisioningModel": "SPOT"
  },
  "serviceAccounts": [
    {
      "email": "832118026603-compute@developer.gserviceaccount.com",
      "scopes": [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring.write",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/trace.append"
      ]
    }
  ],
  "shieldedInstanceConfig": {
    "enableIntegrityMonitoring": true,
    "enableSecureBoot": false,
    "enableVtpm": true
  },
  "tags": {
    "items": []
  },
  "zone": "projects/try2-371019/zones/europe-west1-b"
}#json.dumps(tdata)
    url='https://www.googleapis.com/compute/v1/projects/try2-371019/zones/europe-west1-b/instances'
    headers={"Authorization": "Bearer "+ "ya29.a0AX9GBdWk2rBWMWyg0hEtmw2TYfFaW2TEiEbGUM-biaH_pNk6h_GlivienRbkm75KUraixg4xU3wDk9xPDwy8Yl9s0s5GwdXIsEVjMCORCvaEaBHPupZpQzg0C9d9HdXn_gLD6_LQZmbm4gh_3ngI5Xl43IYkxNnxBTtFkBsXqAmpyHfBH_Lyfl5WaSCkn9E4o3wQNUGnmsvyn8VAH3cvei5OE3VOWFuPOP716sIaCgYKAZoSARASFQHUCsbCUt5rnBLaiIzZdbh7bNOdAQ0238"} #token}
    auth = "Authorization: Bearer ya29.a0AX9GBdWk2rBWMWyg0hEtmw2TYfFaW2TEiEbGUM-biaH_pNk6h_GlivienRbkm75KUraixg4xU3wDk9xPDwy8Yl9s0s5GwdXIsEVjMCORCvaEaBHPupZpQzg0C9d9HdXn_gLD6_LQZmbm4gh_3ngI5Xl43IYkxNnxBTtFkBsXqAmpyHfBH_Lyfl5WaSCkn9E4o3wQNUGnmsvyn8VAH3cvei5OE3VOWFuPOP716sIaCgYKAZoSARASFQHUCsbCUt5rnBLaiIzZdbh7bNOdAQ0238"
    resp=requests.post(url,auth=auth, data=data)
    #if resp.status_code==200:     
    return "Done"
    #else:
    #  print(resp.content)
    #  return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data
    #  return "ERROR"



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
