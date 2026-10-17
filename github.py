import os

import requests


class GitHubClient:
    def __init__(self, owner: str, repo: str):
        self.owner = owner
        self.repo = repo
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        }

    def post_pull_request_comment(self, pull_number: int, body: str) -> str:
        url = (
            f"https://api.github.com/repos/{self.owner}/{self.repo}"
            f"/issues/{pull_number}/comments"
        )

        response = requests.post(
            url,
            headers=self.headers,
            json={"body": body},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["html_url"]
