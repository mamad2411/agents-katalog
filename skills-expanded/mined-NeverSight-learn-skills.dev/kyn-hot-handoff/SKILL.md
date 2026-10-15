---
name: kyn-hot-handoff
description: Compact the current conversation into a handoff document under `.hot/` in the current working directory, snapshotting session state for another agent to pick up. Trigger when the user closes or wraps up the session (e.g., "save context", "I'm done for now").
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

1. **Archive prior state.** Resolve `.hot/HANDOFF.md` and `.hot/HISTORY.md` relative to the nearest `.git` root (walk up from the current working directory, not the literal CWD). If `HANDOFF.md` already exists, append it (with a timestamp) to the end of `HISTORY.md` before writing anything else — if `HISTORY.md` doesn't exist yet, create it first with a one-line header, `# {repo folder name} — history`, using the folder name of the resolved `.git` root. Before archiving, check the prior `HANDOFF.md`'s first line for a `suite:` marker: if it reads `suite: antu` or the marker is missing, note this for step 3's confirmation — it's foreign or unmarked content, archived in full with no attempt to recover pending items from it. Done when the previous content is preserved in `HISTORY.md`, or it's confirmed no prior `HANDOFF.md` existed.

2. **Compact the session.** Write `.hot/HANDOFF.md` (at the resolved `.git` root) from scratch with a summary of the current conversation, starting with a first line `suite: kuyen`. Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs) — reference them by path or URL instead. Redact any sensitive information (API keys, passwords, PII). If the user passed arguments, treat them as the focus of the next session and tailor the document accordingly. Ensure `.hot/` is listed in `.gitignore` at the repo root (add it if missing) — session state is never tracked. Done when `HANDOFF.md` reflects all of the above and contains no sensitive information.

3. **Confirm the close.** End your response with a short line: "Context saved." followed by what was written and, if applicable, what was archived. If step 1 found foreign or unmarked content, add: "previous HANDOFF.md looked like it came from Antu — archived in full; any pending items there won't carry forward automatically."
