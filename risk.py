import argparse
import subprocess
import sys
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
    parser.add_argument(
        "--test-location",
        required=False,
        help="Path to a pytest file or test directory",
    )

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

    if args.test_location:
        test_result = subprocess.run(
            [sys.executable, "-m", "pytest", args.test_location],
            check=False,
        )
        print("Test exit code:", test_result.returncode)
        return test_result.returncode

    print("Tests skipped: no test location provided")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
