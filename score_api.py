import json
import asyncio
from typing import List, Dict, Any, Optional


API_URL = "https://asteroids-backend.onrender.com"

try:
    from pyodide.http import pyfetch as fetch
    IS_BROWSER = True
except ImportError:
    IS_BROWSER = False
    # For testing outside the browser
    import requests

async def submit_score(name, score) -> bool:
    if not IS_BROWSER:
        print("Warning: Score submission only works in web browser")
        return False
    try:
        data = json.dumps({"name": name, "score":score})
        response = await fetch(f"{API_URL}/submit-score",
            method = "POST",
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                #allow CORS
                "Access-Control-Allow-Origin": "*"
            },
            mode = "cors",
            credentials = "omit",
            body = data
        )
        if not response.ok:
            print(f"Server responded with status: {response.status}")
            return False
        return True
    except Exception as e:
        print("Failed to submit score: ", e)
        return False

async def get_high_scores() -> List[Dict[str, Any]]:
    if not IS_BROWSER:
        print("Warning: High score retrieval only works in web browser")
        return []
    try:
        response = await fetch(
            f"{API_URL}/high-scores",
            method="GET",
            headers={
                "Accept": "application/json",
                # Allow CORS
                "Access-Control-Allow-Origin": "*"
            },
            mode="cors",  # Enable CORS mode
            credentials="omit"  # Don't send credentials for cross-origin requests
        )

        if not response.ok:
            print(f"Server responded with status: {response.status}")
            return []

        scores = await response.json()
        return scores
    except Exception as e:
        print("Failed to fetch scores:", e)
        return []