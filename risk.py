import argparse

from getpr import PullRequestReader


def assess_risk(changed_files):
    risky_words = (
        "auth",
        "security",
        "payment",
        "database",
        "deploy",
    )

    for file in changed_files:
        filename = file.filename.lower()

        if any(word in filename for word in risky_words):
            return "high"

    if len(changed_files) > 5:
        return "medium"

    return "low"


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
