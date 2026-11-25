---
name: usage-review
description: Review how the maintainer's agents actually used the Agent Desktop MCP since the last field report, then write the dated report, update docs/USE_CASES.md and propose fixes. Use when asked to find, review or report MCP uses, usage, field reports or use cases.
---

# Usage review

Follow [docs/project/USAGE_REVIEW.md](../../../docs/project/USAGE_REVIEW.md). In short:

1. Read the "Reviewed through" date in `docs/USE_CASES.md`. Run
   `uv run python scripts/usage_review.py --since <that date>` and
   `uv run agent-desktop activity --days <days since then>`. Tell the person how many
   calls and transcripts it found.
2. Read `summary.md` in the printed folder, then the timelines for each flagged moment.
   Open the transcript itself only around a moment the timeline can't explain. Group
   the calls into uses (task, project, period). Every flag is a lead to check, not a
   finding.
3. Check each problem against the code (tool descriptions in
   `src/agent_desktop/mcp_server.py`, limits in `worker.py`), the docs, open issues and
   pull requests, and the previous report. Note what was fixed, unchanged or back.
4. On a branch in a worktree, write `docs/trials/<today>-<topic>.md`, update
   `docs/USE_CASES.md` (rows, coverage, "Reviewed through") and add a development log
   entry. Follow the privacy rules on the workflow page. Nothing from the review folder
   is committed.
5. Give the person the findings and a proposed list of fixes, most valuable first, with
   which ones need their decision. Open pull requests for the ones they agree to, and
   say how they depend on each other.

The review folder holds private transcript excerpts. Don't send its contents to
outside services or paste them into public text.
