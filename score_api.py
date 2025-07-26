import json
import urllib.request

API_URL = "https://asteroids-backend.onrender.com"

def submit_score(name, score):
    try:
        data = json.dumps({"name": name, "score": score}).encode("utf-8")
        req = urllib.request.Request(f"{API_URL}/submit-score", data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
        print("score submitted")
        return True
    except Exception as e:
        return False

def get_high_scores():
    try:
        with urllib.request.urlopen(f"{API_URL}/high-scores") as response:
            scores = json.loads(response.read())
            return scores
    except Exception as e:
        print("Failed to fetch scores:", e)
        return []