# github_api.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_latest_workflow_run():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs?per_page=1"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error fetching workflows: {response.status_code}")
        return None

    data = response.json()
    if "workflow_runs" not in data or not data["workflow_runs"]:
        return None

    run = data["workflow_runs"][0]

    return {
        "status": run["status"],                 # e.g., completed
        "conclusion": run["conclusion"],         # e.g., success / failure
        "html_url": run["html_url"],             # link to the run
        "created_at": run["created_at"],
        "branch": run["head_branch"],
        "commit": run["head_commit"]["message"],
        "author": run["head_commit"]["author"]["name"]
    }
