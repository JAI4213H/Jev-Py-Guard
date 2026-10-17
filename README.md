# JevGuard

![JevGuard banner](assets/jevguard-banner.png)

JevGuard is a small Python tool that reviews a GitHub pull request with Jev,
runs an optional pytest file or test directory, and posts the result back to
the pull request.

## What it does

JevGuard follows this flow:

```text
GitHub pull request
        ↓
Read changed files
        ↓
Ask Jev for a risk level
        ↓
Optionally run the test location you provide
        ↓
Post a Markdown report on GitHub
```

The current Jev question returns one of three values:

- `low`: documentation, comments, or formatting changes
- `medium`: normal application logic changes
- `high`: security, authentication, payments, databases, or deployment changes

JevGuard does not merge or approve pull requests. It only reports a risk
estimate and the test result.

## Project layout

```text
Jev-Py-Guard/
├── assets/
│   └── jevguard-banner.png
├── getpr.py          # Reads changed files from GitHub
├── github.py         # Posts the report as a PR comment
├── risk.py           # Calls Jev and runs optional pytest tests
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.12 or newer
- A GitHub personal access token
- A TypeSafe/​Jev API key
- A GitHub repository with a pull request to inspect

## Installation

Clone the repository and enter its folder:

```powershell
git clone https://github.com/JAI4213H/Jev-Py-Guard.git
cd Jev-Py-Guard
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Set the keys for the current terminal

These commands last only until you close the current PowerShell window:

```powershell
$env:GITHUB_TOKEN="your_github_token"
$env:TYPESAFE_API_KEY="your_jev_api_key"
```

Do not commit either key. Do not put them directly in Python files.

## Make the keys permanent on Windows

Run these commands once in PowerShell:

```powershell
[Environment]::SetEnvironmentVariable(
    "GITHUB_TOKEN",
    "your_github_token",
    "User"
)

[Environment]::SetEnvironmentVariable(
    "TYPESAFE_API_KEY",
    "your_jev_api_key",
    "User"
)
```

Close and reopen PowerShell after setting them. Check that they exist without
printing the secret values:

```powershell
if ($env:GITHUB_TOKEN) { "GITHUB_TOKEN is set" }
if ($env:TYPESAFE_API_KEY) { "TYPESAFE_API_KEY is set" }
```

For security, use the smallest GitHub token permissions that work. The token
needs to read pull requests and write a normal pull-request comment. Never
share the token in a chat, commit, screenshot, or issue.

## Usage

### Bash, Git Bash, macOS, or Linux

Review a pull request without running tests:

```bash
python risk.py \
  --owner JAI4213H \
  --repo Machine-Learning-and-compe \
  --pull 1
```

Review a pull request and run one test file:

```bash
python risk.py \
  --owner JAI4213H \
  --repo Machine-Learning-and-compe \
  --pull 1 \
  --test-location tests/test_model.py
```

Review a pull request and run a test directory:

```bash
python risk.py \
  --owner JAI4213H \
  --repo Machine-Learning-and-compe \
  --pull 1 \
  --test-location tests
```

### PowerShell

PowerShell uses a backtick for line continuation:

```powershell
python risk.py `
  --owner JAI4213H `
  --repo Machine-Learning-and-compe `
  --pull 1 `
  --test-location tests
```

You can also write the PowerShell command on one line.

`--test-location` is optional. If you do not provide it, Jev still assesses
the pull request and JevGuard posts `Tests: skipped`.

## Example report

JevGuard posts a comment similar to:

```text
JevGuard Report

Risk level: high
Changed files: 3
Tests: passed
```

The process exits with pytest's exit code when tests are run. A zero exit code
means pytest passed; a non-zero exit code means at least one test failed or
pytest encountered an error.

## How the code works

1. `getpr.py` calls GitHub's pull-request files API.
2. `unidiff` separates added and removed lines.
3. `risk.py` sends the changed-file state to Jev using `Choice`.
4. Python runs the exact file or directory passed to `--test-location`.
5. `github.py` posts the risk and test status to the pull-request timeline.

The program keeps the final actions in normal Python code. Jev provides a
bounded risk judgment; it does not execute commands or merge code.

## Limitations

- The risk result is an AI estimate, not proof that code is safe.
- The tool currently posts a new comment on each run.
- Test selection is intentionally manual: the user chooses the pytest path.
- Binary files and files without a GitHub patch are skipped by the diff parser.
- A human should review high-risk or uncertain changes.

## License

This project is provided as-is for learning and experimentation.
