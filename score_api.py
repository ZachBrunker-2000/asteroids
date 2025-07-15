import json
import urllib.request

API_URL = database

def submit_score(name,score):
    data = json.dumps({"name":name,"score":score}).encode("utf-8")
    req = urllib.request.Request(f"{API_URL}/submit-score", data = data, headers={'content-type':'application/json'})
    urllib.request.urlopen(req)
    
def get_high_scores():
    with urllib.request.urlopen(f"{API_URL}/high-scores") as response:
        return json.loads(response.read())