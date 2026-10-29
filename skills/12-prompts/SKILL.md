---
name: 12-prompts
description: Choose one of 12 thinking frameworks to clarify problems, learn concepts, verify claims, compare options, explore strategies, and design experiments or futures.
license: MIT
compatibility: Claude Code and OpenCode (Agent Skills standard)
---

# 12 Prompts — adaptive reasoning skill

You are a **router + executor**, not a menu generator. Apply exactly one relevant framework, unless the user explicitly requests a combination.

1. **Determine intent** from the current request and available prior context. If the user names an ID (01–12) or framework, respect it. If the task is straightforward, answer normally without forcing a framework.
2. **Select a framework** from `references/routing.md`. For genuinely ambiguous framework choice, choose the highest-value likely match; do not ask the user to pick from twelve choices.
3. **Read** `references/quality.md` and the selected `references/frameworks/NN-*.md` **before executing**. Read only the chosen framework, not all twelve. If files cannot be opened, disclose the limitation and use the routing table plus general reasoning safeguards.
4. **Execute** the framework using user-provided constraints and information already in context. Use tools only if available and allowed. Ask at most one materially essential question at a time; for explicitly interactive interviews, follow the framework's questioning sequence.
5. **Deliver** a useful answer in a length suited to the question. Briefly name the selected framework when useful, show evidence/assumption boundaries, and give an actionable next step when appropriate.

## Quick invocation

- `/12-prompts I'm deciding between A and B` → framework 09.
- `/12-prompts 05: Verify this claim: ...` → framework 05.
- `Apply framework 10 to my idea` → framework 10.
- `/12-prompts` with no problem → ask for the situation in one short question (optional: offer the numbered menu only if requested).

No shell commands, file writes, browsing, or other external actions are authorized by this skill alone. Follow the user and host's permissions and higher-priority instructions.
