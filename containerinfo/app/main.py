#!/usr/bin/python3.7
from flask import Flask,request
import subprocess,os
import json

tmp_pods = '/tmp/pods.json'
tmp_jq1 = '/tmp/out1.json'
tmp_jq2 = '/tmp/out2.json'

query = 'pod-label'

app = Flask(__name__)

@app.route("/container-resources", methods=['GET'])
def container_resources():
    label = request.args.get(query)

    if label is None:
        return "No label specified"

    # Kubectl get pods -l 'pod-label=<label>' -o json and save to tmp_pods
    p0 = subprocess.run(['kubectl', 'get','pod','-l',label,'--all-namespaces','-o','json'],stdout=open(tmp_pods, 'w'))
    
    # Read the output file and apply jq filters and save to tmp_jq1
    p1 = subprocess.run(["jq", "-r", '[.items[] | {pod_name: .metadata.name, namespace: .metadata.namespace, containers: .spec.containers[] | [ {container_name: .name, mem_req: .resources.requests.memory, mem_limit: .resources.limits.memory ,  cpu_req: .resources.requests.cpu, cpu_limit: .resources.limits.cpu} ] }]'], stdin=open(os.path.expanduser(tmp_pods), 'r'),stdout=open(tmp_jq1, 'w'))

    # Read the output file and apply jq filters and save to tmp_jq2
    p2 =  subprocess.run(["jq", "-r", '[ .[] | {pod_name: .pod_name, namespace: .namespace, container_name: .containers[0].container_name, mem_req: .containers[0].mem_req, mem_limit: .containers[0].mem_limit ,  cpu_req: .containers[0].cpu_req, cpu_limit: .containers[0].cpu_limit}]'], stdin=open(os.path.expanduser(tmp_jq1), 'r'),stdout=open(tmp_jq2, 'w'))

    # open the output file 
    with open(tmp_jq2) as fh:
        # Read the file as JSON
        data = json.load(fh)
        # Create the json response
        response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
        )
    # and return the json
    return response


# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0')