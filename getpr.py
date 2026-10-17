import os
from dataclasses import dataclass

import requests
from unidiff import PatchSet


@dataclass
class ChangedFile:
    filename: str
    status: str
    added_lines: list[str]
    removed_lines: list[str]


class PullRequestReader:
    def __init__(self, owner: str, repo: str, pull_number: int):
        self.owner = owner
        self.repo = repo
        self.pull_number = pull_number

        self.url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/pulls/{pull_number}"
        )

        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        }

    def get_changed_files(self) -> list[ChangedFile]:
        response = requests.get(
            f"{self.url}/files",
            headers=self.headers,
            timeout=30,
        )
        response.raise_for_status()

        changed_files = []

        for github_file in response.json():
            patch = github_file.get("patch")

            # Binary files may not have a patch.
            if not patch:
                continue

            diff = (
                f"--- a/{github_file['filename']}\n"
                f"+++ b/{github_file['filename']}\n"
                f"{patch}\n"
            )

            parsed_patch = PatchSet(diff)

            for changed_file in parsed_patch:
                added_lines = [
                    line.value.rstrip("\n")
                    for line in changed_file
                    if line.is_added
                ]

                removed_lines = [
                    line.value.rstrip("\n")
                    for line in changed_file
                    if line.is_removed
                ]

                changed_files.append(
                    ChangedFile(
                        filename=github_file["filename"],
                        status=github_file["status"],
                        added_lines=added_lines,
                        removed_lines=removed_lines,
                    )
                )

        return changed_files

