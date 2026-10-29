# ChatGPT setup

1. Create a **ChatGPT Project** named `12 Prompts`.
2. Open project settings and paste **all** of `project-instructions.md` as the project's instructions.
3. Add `12-prompts-knowledge.txt` (generated, already included in the release) as a **project source**. If the UI rejects `.txt`, paste the contents into a project source instead.
4. Start a new chat **inside** the project and say `Compare building versus buying this tool` or `Use 05 to verify this claim`.

This is a portable prompt pack. It is **not** a ChatGPT plugin, MCP server, or native SKILL.md installation. ChatGPT does not automatically ingest GitHub repository files from a URL. Project-source ingestion and instruction behavior depend on your ChatGPT setup.

To refresh after editing a framework: run `python scripts/build.py` and replace the project source with the freshly generated `.txt` file.

For one-off chats, attach `12-prompts-knowledge.txt` and paste `project-instructions.md` as your first message.
