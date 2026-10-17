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


if __name__ == "__main__":
    reader = PullRequestReader(
        owner="JAI4213H",
        repo="Machine-Learning-and-compe",
        pull_number=1,
    )

    changed_files = reader.get_changed_files()
    risk = assess_risk(changed_files)

    print("Changed files:", len(changed_files))
    print("Risk level:", risk)
