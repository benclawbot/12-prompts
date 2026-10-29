# Maintaining the published repository

The canonical repository is **[benclawbot/12-prompts](https://github.com/benclawbot/12-prompts)**. Its default branch is `main`.

## Clone and validate

```bash
git clone https://github.com/benclawbot/12-prompts.git
cd 12-prompts
python3 scripts/lint.py
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
```

## Edit and publish

1. Make changes in `skills/12-prompts/` (the canonical source).
2. Regenerate the ChatGPT project knowledge bundle: `python3 scripts/build.py`.
3. Run lint, unit tests, and `python3 scripts/package.py`.
4. Review changes using `git diff`. Commit and push using your normal authenticated GitHub workflow.

```bash
git add .
git commit -m "Improve reasoning framework"
git push origin main
```

## Build the downloadable archives

```bash
python3 scripts/package.py
```

This creates `dist/12-prompts-skill.zip` for Claude's skill uploader and `dist/12-prompts-complete.zip` as a source archive. These archives are generated build artifacts, not required for GitHub source checkout; attach them to a release if desired.

## Platform deployment

- **ChatGPT:** update Project instructions from `chatgpt/project-instructions.md` and replace the uploaded knowledge file from `chatgpt/12-prompts-knowledge.txt`.
- **Claude Code:** run `python3 scripts/install.py --target claude --scope global --force`, or install inside a project.
- **OpenCode:** run `python3 scripts/install.py --target opencode --scope global --force`, or install inside a project.
- **Claude web:** upload the newly built `dist/12-prompts-skill.zip` in Customize → Skills.

GitHub Actions runs structural tests on pushes and pull requests. These do not measure actual response quality; use the manual model-evaluation protocol in `evals/rubric.md` for that.
