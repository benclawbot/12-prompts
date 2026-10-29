# 12-prompts

**Twelve evidence-aware thinking frameworks, one router, three AI environments.** An independent, English-language rewrite inspired by the framework *categories* collected in [hskelp9527-pixel/twelve-prompts](https://github.com/hskelp9527-pixel/twelve-prompts), which attributes the original Chinese prompts to [@Khazix0918](https://x.com/Khazix0918). This repository does **not** reproduce or claim to translate the original copyrighted Chinese prompt text.

## What it does

Given a problem, chooses an appropriate framework and works through it (or responds directly when a framework would add overhead). You can also select a framework explicitly, such as `Use 09 to evaluate A vs B`.

| ID | Framework | Typical use |
|---|---|---|
| 01 | Socratic Problem Framing | A problem is vague |
| 02 | Two-Layer Explanation | Learn something deeply |
| 03 | Reverse-Engineer an Example | Learn from a concrete artifact |
| 04 | Historical + Competitive Research | Explore a domain |
| 05 | Claim Verification | Fact-check an assertion |
| 06 | Complementary Expert Lenses | Resolve competing disciplines |
| 07 | First-Principles Redesign | Redesign a system |
| 08 | Cross-Domain Transfer | Unblock ideas from elsewhere |
| 09 | Fair Comparison of Two Options | Make a difficult choice |
| 10 | Minimum Viable Experiment | Test an assumption cheaply |
| 11 | Evidence-Based Strengths Discovery | Reflect on actual competence |
| 12 | Three Possible Futures | Consider life/career paths |

## Installation

**ChatGPT (Project; no code required)**

1. Create a ChatGPT Project; paste [`chatgpt/project-instructions.md`](chatgpt/project-instructions.md) into Project instructions.
2. Add [`chatgpt/12-prompts-knowledge.txt`](chatgpt/12-prompts-knowledge.txt) as a project source (or paste its text as a source).
3. Ask a question in the Project. Example: `Use 05: How reliable is this claim?`.

See [ChatGPT setup](chatgpt/README.md). This is **not** a ChatGPT plugin or automatic GitHub integration.

**Claude (web/desktop)** — upload the native skill ZIP:

1. Download `12-prompts-skill.zip` from the prepared release files (or generate it with `python3 scripts/package.py`).
2. In Claude, open **Customize → Skills → + → Create skill → Upload a skill**, then upload the ZIP and enable it. Claude requires code execution/skills enabled for custom skills.
3. Ask: `Help me choose between these two architectures using 12-prompts`.

This is a genuine Claude custom skill; it is separate from the ChatGPT Project approach. If you prefer a Claude Project, paste `chatgpt/project-instructions.md` into project instructions and upload `chatgpt/12-prompts-knowledge.txt` as project knowledge.

**Claude Code (global)** — from a local clone of this repo:

```bash
python3 scripts/install.py --target claude --scope global
```

This installs to `~/.claude/skills/12-prompts/SKILL.md` with all references. Restart/reload Claude Code, then say `/12-prompts I'm weighing two options`. For a project install, use `--scope project --project /path/to/your/project`.

**OpenCode (global)** — from a local clone:

```bash
python3 scripts/install.py --target opencode --scope global
```

This installs to `~/.config/opencode/skills/12-prompts/SKILL.md`. For a project install, use `--scope project --project /path/to/your/project`, which writes `.opencode/skills/12-prompts`. OpenCode discovers the skill automatically; ask it to use `12-prompts` or describe the task. On Windows, use `py -3` instead of `python3` where applicable. The installer refuses to overwrite an existing skill unless you add `--force`.

**No installer:** copy the entire `skills/12-prompts/` folder into either of the platform locations above. Copying only `SKILL.md` omits its references.

## Usage

- `I'm trying to decide whether to build or buy an internal agent` → 09.
- `Verify this statistic and its source` → 05.
- `Design a one-week test of this assumption` → 10.
- `Explain retrieval-augmented generation first intuitively, then technically` → 02.
- `Use framework 07 to redesign our deployment workflow` → 07.
- `What is 2+2?` → direct response, no framework.

## Architecture

```text
skills/12-prompts/SKILL.md                # canonical, platform-neutral skill entry
skills/12-prompts/references/routing.md   # select one framework
skills/12-prompts/references/quality.md   # shared rules
skills/12-prompts/references/frameworks/  # 12 complete prompts
chatgpt/project-instructions.md           # ChatGPT Project rules
chatgpt/12-prompts-knowledge.txt           # generated one-file knowledge pack
scripts/build.py                           # builds ChatGPT knowledge from canonical files
scripts/install.py                         # native Claude Code/OpenCode installer
scripts/package.py                         # reproducible skill + repository ZIPs
evals/cases.jsonl                           # routing and behavior examples
evals/rubric.md                            # manual LLM evaluation protocol
tests/                                     # deterministic structural and installer tests
```

One canonical skill powers both coding assistants; the ChatGPT knowledge file is generated from it. **No third-party Python packages or credentials are needed** for building/installing/testing locally.

## Validate / contribute

```bash
python3 scripts/build.py --check
python3 scripts/lint.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

These are **structural tests**, not claims of accuracy or behavioral superiority. Run the manual model-evaluation protocol in [`evals/rubric.md`](evals/rubric.md) for real behavior testing across models. Safety and authorization boundaries remain those of the host application.

For framework-by-framework editorial assessments, see [`docs/assessment.md`](docs/assessment.md). A GitHub Actions workflow runs the structural checks on pushes and pull requests.

## Attribution and license

Our new rewrites, router, installer, docs, and tests are MIT-licensed (see [LICENSE](LICENSE)). The Chinese originals are **not included** and their rights remain with their respective creator. See [`ATTRIBUTION.md`](ATTRIBUTION.md). No endorsement or affiliation is implied.
