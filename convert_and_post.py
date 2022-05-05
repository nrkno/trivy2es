import json
import os
import requests
import datetime

# api_base_url = "4f560bf84bb74152a34d2072819b16ce.westeurope.azure.elastic-cloud.com"
api_base_url = os.environ.get('INPUT_ELASTICAPIADDRESS')
port = "9243"
# target_index = "ghactions"
target_index = os.environ.get('INPUT_TARGETINDEX')
api_key = os.environ.get('ELASTIC_API_KEY')
repo_name = os.environ.get('INPUT_GITHUBREPOSITORY')
repo_url = "https://" + "github.com" + "/" + repo_name
headers = { 'Authorization': f'ApiKey {api_key}', 'Content-Type': f'application/json' }
target_url = "https://" + api_base_url + ":" + port + "/" + target_index + "/" + "doc"
json_input = os.environ.get('INPUT_JSONINPUT')

with open("json_input", "r") as json_file:
    test = json.load(json_file)

# test = json.load(json_input)
timestamp = datetime.datetime.now().isoformat()
metadata = test["Metadata"]
for result in test["Results"]:
    for vulnerability in result["Vulnerabilities"]:
        if not "CVSS" in vulnerability.keys():
            continue
        if "nvd" in vulnerability["CVSS"]:
            if "V2Score" in vulnerability["CVSS"]["nvd"].keys():
                vulnerability["CVSS"]["nvd"]["V2Score"] = float(vulnerability["CVSS"]["nvd"]["V2Score"])
            if "V3Score" in vulnerability["CVSS"]["nvd"].keys():
                vulnerability["CVSS"]["nvd"]["V3Score"] = float(vulnerability["CVSS"]["nvd"]["V3Score"])
        if "redhat" in vulnerability["CVSS"]:
            if "V3Score" in vulnerability["CVSS"]["redhat"].keys():
                vulnerability["CVSS"]["redhat"]["V3Score"] = float(vulnerability["CVSS"]["redhat"]["V3Score"])

        payload = {
                    "@timestamp": timestamp,
                    "github_repository": repo_url,
                    "metadata": metadata,
                    "vulnerability": vulnerability
                    }

        post_vuln = requests.post(target_url, headers=headers, data=json.dumps(payload))
        post_vuln.raise_for_status()
