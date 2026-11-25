---
name: wiki-init
description: Set up this project's wiki memory at .llm-wiki/. Attach its GitHub wiki, create a local wiki when requested, or scaffold an attachment that has no schema.
---

Ask the user whether they want to use a GitHub wiki or keep the wiki offline.
Wait for their answer before running initialization. If they have already made
that choice in the conversation, use it.

- For a GitHub wiki, keep `--github` in the command below.
- For an offline wiki, omit `--github`.

Run from the host project. Replace `<assistant-name>` with your actual assistant
name for attribution, such as `claude-code`, `codex`, or `cursor`:

```bash
bash "$SKILL_DIRECTORY/scripts/init-wiki.sh" --github --agent "<assistant-name>"
```

Report the outcome and wiki path. If setup cannot complete, explain the returned
error and next step, including the setup URL when provided. Do not describe an
inaccessible remote as a missing wiki or a failed commit as successful setup.

For `already-initialized`, report that briefly and stop. Ingest project documents
only if the user requested that too.
