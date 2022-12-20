from flask import Flask
from flask import request
import requests
import os
import json
app = Flask(__name__)

def get_api_key() -> str:
    secret = os.environ.get("COMPUTE_API_KEY")
    if secret:
        return secret.replace(\n,"")
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

    payload = "{\r\n  \"canIpForward\": false,\r\n  \"confidentialInstanceConfig\": {\r\n    \"enableConfidentialCompute\": false\r\n  },\r\n  \"deletionProtection\": false,\r\n  \"description\": \"\",\r\n  \"disks\": [\r\n    {\r\n      \"autoDelete\": true,\r\n      \"boot\": true,\r\n      \"deviceName\": \"slave1\",\r\n      \"initializeParams\": {\r\n        \"diskSizeGb\": \"10\",\r\n        \"diskType\": \"projects/try2-371019/zones/us-west4-b/diskTypes/pd-balanced\",\r\n        \"labels\": {},\r\n        \"sourceImage\": \"projects/debian-cloud/global/images/debian-11-bullseye-v20221206\"\r\n      },\r\n      \"mode\": \"READ_WRITE\",\r\n      \"type\": \"PERSISTENT\"\r\n    }\r\n  ],\r\n  \"displayDevice\": {\r\n    \"enableDisplay\": false\r\n  },\r\n  \"guestAccelerators\": [],\r\n  \"keyRevocationActionType\": \"STOP\",\r\n  \"labels\": {},\r\n  \"machineType\": \"projects/try2-371019/zones/europe-west1-b/machineTypes/e2-medium\",\r\n  \"metadata\": {\r\n    \"items\": [\r\n      {\r\n        \"key\": \"startup-script\",\r\n        \"value\": \"apt update\\ncurl --output spark.tgz https://dlcdn.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz\\napt -y install default-jdk\\ntar -xzvf spark.tgz\\n./spark-3.3.1-bin-hadoop3/sbin/start-slave.sh spark://spark-master.europe-west1-b.c.try2-371019.internal:7077\"\r\n      }\r\n    ]\r\n  },\r\n  \"name\": \"slave1\",\r\n  \"networkInterfaces\": [\r\n    {\r\n      \"accessConfigs\": [\r\n        {\r\n          \"name\": \"External NAT\",\r\n          \"networkTier\": \"PREMIUM\"\r\n        }\r\n      ],\r\n      \"stackType\": \"IPV4_ONLY\",\r\n      \"subnetwork\": \"projects/try2-371019/regions/europe-west1/subnetworks/default\"\r\n    }\r\n  ],\r\n  \"params\": {\r\n    \"resourceManagerTags\": {}\r\n  },\r\n  \"reservationAffinity\": {\r\n    \"consumeReservationType\": \"ANY_RESERVATION\"\r\n  },\r\n  \"scheduling\": {\r\n    \"automaticRestart\": false,\r\n    \"instanceTerminationAction\": \"STOP\",\r\n    \"onHostMaintenance\": \"TERMINATE\",\r\n    \"provisioningModel\": \"SPOT\"\r\n  },\r\n  \"serviceAccounts\": [\r\n    {\r\n      \"email\": \"832118026603-compute@developer.gserviceaccount.com\",\r\n      \"scopes\": [\r\n        \"https://www.googleapis.com/auth/devstorage.read_only\",\r\n        \"https://www.googleapis.com/auth/logging.write\",\r\n        \"https://www.googleapis.com/auth/monitoring.write\",\r\n        \"https://www.googleapis.com/auth/servicecontrol\",\r\n        \"https://www.googleapis.com/auth/service.management.readonly\",\r\n        \"https://www.googleapis.com/auth/trace.append\"\r\n      ]\r\n    }\r\n  ],\r\n  \"shieldedInstanceConfig\": {\r\n    \"enableIntegrityMonitoring\": true,\r\n    \"enableSecureBoot\": false,\r\n    \"enableVtpm\": true\r\n  },\r\n  \"tags\": {\r\n    \"items\": []\r\n  },\r\n  \"zone\": \"projects/try2-371019/zones/europe-west1-b\"\r\n}"
    headers = {
        'Authorization': 'Bearer ya29.a0AX9GBdVNdEU1ZzCiPajoQtuX8R8__iBKEJlUOcq622S1TDJecrh5zmITPibRlTeLKwnLdSeh_cKrqK5CCIRdfIOV0UeReJd8ziAf5HIWtogYnRl-77PMgWQXpT2pwJXyAwwlYa3MCcDMjZTuZvs0rlyH6QiePV9bBcDSPJ_OIHFwoeafKPhEhwP9TRemmKDrSFK5sBHxmMly4Bt_T56axNAcUoXsaC0yCgNs6t8aCgYKAcMSARASFQHUCsbClYbvtu4x3crCtVF2GMsTmA0238',
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=data)

    #if resp.status_code==200:     
    return "Done"
    #else:
    #  print(resp.content)
    #  return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data
    #  return "ERROR"



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
