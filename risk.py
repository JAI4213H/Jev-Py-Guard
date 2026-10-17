import argparse
from dataclasses import asdict

from getpr import PullRequestReader
from typesafe_sdk import Choice, TypeSafeClient


def assess_risk(changed_files):
    state = {
        "changed_files": [asdict(file) for file in changed_files]
    }

    with TypeSafeClient() as client:
        result = client.system_one(
            state=state,
            questions={
                "risk": Choice(
                    instructions="How risky are these code changes?",
                    criteria={
                        "low": "Documentation, comments, or formatting changes",
                        "medium": "Normal application logic changes",
                        "high": "Security, authentication, payments, databases, or deployment changes",
                    },
                )
            },
        )

    return result.choices["risk"].choice


def main():
    parser = argparse.ArgumentParser(
        description="Assess GitHub pull-request risk"
    )
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pull", type=int, required=True)

    args = parser.parse_args()

    reader = PullRequestReader(
        owner=args.owner,
        repo=args.repo,
        pull_number=args.pull,
    )

    changed_files = reader.get_changed_files()
    risk = assess_risk(changed_files)

    print("Changed files:", len(changed_files))
    print("Risk level:", risk)


if __name__ == "__main__":
    main()
