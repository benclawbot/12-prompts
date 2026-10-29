# Publishing the project to GitHub

This distribution is ready to publish as a **new repository named `12-prompts`**. There are no credentials or secrets embedded in it.

## Option A: GitHub website + GitHub CLI

1. Create an empty **private** repository called `12-prompts` under your account at https://github.com/new. Don't add a generated README, license, or `.gitignore`; this project includes those already.
2. Download and unzip `12-prompts-complete.zip`, then open a terminal in the extracted `12-prompts` folder.
3. Run:

```bash
git init -b main
git add .
git commit -m "Add portable 12-prompts skill and evaluation suite"
git remote add origin https://github.com/YOUR-ACCOUNT/12-prompts.git
git push -u origin main
```

Replace `YOUR-ACCOUNT` with your account name. Authenticate normally with GitHub when prompted; do not paste credentials into a conversation.

## Option B: `gh` CLI, if installed and authenticated

After extracting the archive, open the project folder and run:

```bash
git init -b main
git add .
git commit -m "Add portable 12-prompts skill and evaluation suite"
gh repo create 12-prompts --private --source=. --remote=origin --push
```

If you want it public instead, change `--private` to `--public`. Review source credit and any desired repository settings before making it public.

## After publishing

- GitHub Actions runs the Python structural checks on each push and pull request.
- To update framework prompts, edit `skills/12-prompts/references/frameworks/`, rebuild the ChatGPT knowledge file using `python scripts/build.py`, and run `python scripts/lint.py` plus `python -m unittest discover -s tests -v`.
- To refresh the skill ZIP, run `python scripts/package.py`.

**Note:** GitHub API integrations differ. Some connected GitHub apps can write repository files but cannot create a new repository; if so, create the empty repo in GitHub first and grant it access to the app if needed.
