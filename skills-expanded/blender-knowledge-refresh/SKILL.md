---
name: blender-knowledge-refresh
description: "Use when asked to run the per-version documentation refresh: review drifted documents and their evidence records in one PR."
disable-model-invocation: true
metadata:
  claude-command: "knowledge-refresh"
---

Run the [release refresh](../../../docs/maintenance/knowledge.md#release-refresh)
for the next version. Read `AGENTS.md` and `docs/maintenance/knowledge.md`
first. Run it once the version's scope is settled, as the only refresh in
progress. This command opens one PR; it never merges it or the release PR.

## Prepare

Match PRs by head branch, never by text search: release notes and PR bodies
mention refresh commits too.

1. Find the next version from the title of the open PR whose head branch starts
   with `release-please--`
   (`gh pr list --state open --json number,title,headRefName`). If none is
   open, ask.
2. In the same list, look for a head branch starting with
   `docs/knowledge-refresh-`. If one exists, stop and report it.
3. `git fetch origin main`, then create `docs/knowledge-refresh-<version>` from
   `origin/main` in a separate worktree. Record `origin/main`'s full SHA: it is
   the `reviewed_revision` for every record you refresh.
4. Run `uv run --locked --no-env-file python tools/check_knowledge.py --base origin/main --json`
   and keep its `drift` list. Stop if it reports errors that this refresh did
   not cause.

## Review each drifted document

Documents are independent. You may split them among helpers, one document each;
give each helper this section and collect its edits.

1. Read `git diff <reviewed_revision>..<main SHA> -- <sources>` with the drift
   entry's `sources`, and the document. Paths also in `removed` were deleted.
2. Correct only what the changes made wrong, following "Keep it short" below.
   The user guide stays short, plain-language help with no internal terms or
   test results.
3. Update the record: add newly relevant sources, drop removed or irrelevant
   ones, keep the list sorted. Set `reviewed_revision` to the main SHA and
   `reviewed_at` to today's UTC date. Rewrite `limits` as the current boundaries
   in at most 60 words, with no dates or re-check history. Change `coverage`
   only when you reviewed the claims it covers.
4. If you cannot review a document properly, leave its record unchanged and list
   it as still drifted.

## Keep it short

The refresh exists to keep documents accurate, not to record that it happened.
A refresh that makes documents longer has failed unless new behavior needs it.

- Replace or delete wrong sentences; do not append corrections, notes or
  "as of" paragraphs next to them.
- Describe current behavior only. Never add dates, PR or issue numbers for
  history, test runs, platforms checked, "re-checked" or "verified" remarks.
  Those belong in the PR body, and only briefly.
- Delete text that repeats another guide; link to the guide that owns it.
- Do not restate what code or tests say line by line; name the behavior and
  link the source file.
- One fact once: if two paragraphs say the same thing, keep the clearer one.
- No new sections unless a new feature has no home; then add the fewest lines
  that describe it.

Before publishing, run `git diff --stat origin/main` and check the Markdown
line counts. Each refreshed document should shrink or stay the same size. If one
grows, cut it again, or name the new behavior that needs the extra lines in the
PR body.

## Validate and publish

1. Run `make knowledge`, `make lint` when Python changed, and
   `uv run --locked --no-env-file python -m pytest tests/unit/test_knowledge.py`.
   The checker must report no drift for the documents you refreshed.
2. Commit with `docs(docs): refresh documentation for <version>` and open the PR
   against `main` with the repository template. Keep the body short: the main
   SHA reviewed, a table of refreshed documents with their line change, and the
   documents still drifted with one-line reasons. No per-document narratives.
3. Report the PR URL. Do not merge it.
