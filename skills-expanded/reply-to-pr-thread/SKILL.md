---
name: reply-to-pr-thread
description: Use when the user asks to reply / comment on a CodeRabbit (or any) PR review thread, OR when posting a reasoning/explanation reply tagging @coderabbitai for a thread you've classified as invalid. Wraps `gh api .../pulls/N/comments/<id>/replies`. Body is read from stdin.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory>` once per session before using any `la-*` or `dr-*` command; if it fails, stop and show the user its output.

# Reply to a GitHub PR review thread

Wraps the GitHub `POST /repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies` endpoint. Works for any review thread on any PR, but the canonical use case is replying to CodeRabbit threads — never resolve them, always reply with rationale.

## How to run

```bash
# Form 1 — paste the discussion URL straight from the CodeRabbit comment:
echo "@coderabbitai <reason>" | \
  la-reply-to-pr-thread https://github.com/OWNER/REPO/pull/<PR>#discussion_r<COMMENT_ID>

# Form 2 — explicit IDs:
la-reply-to-pr-thread --comment-id <COMMENT_ID> --pr <PR> [--repo OWNER/REPO] <<'EOF'
@coderabbitai
multi-line
reasoning here
EOF
```

- Body is **always read from stdin**. No `--body` / `--body-file`. Pipe text in or use a heredoc.
- On success, the command prints the new reply's `html_url`. Report that URL back to the user.

## Steps

1. Identify the comment URL or comment ID. From the `la-fetch-coderabbit-threads` output, that's the URL printed in `Comment 1 — coderabbitai`. The integer after `discussion_r` is the comment ID.
2. Compose the reply body. For a CodeRabbit-invalid case: lead with `@coderabbitai`, then 1–3 sentences explaining why the comment doesn't apply (cite the relevant `CLAUDE.md` rule, the existing test, or the commit hash where it was already addressed).
3. Pipe the body into the command. Capture the printed URL.
4. **Never** call any "resolve" mutation (`resolveReviewThread` GraphQL or its UI equivalent). This command (or `la-reply-invalid-coderabbit`, which adds the `@coderabbitai` mention) is the only allowed channel for closing the loop on a CodeRabbit thread you've classified as invalid.

## Why use this instead of `gh api` directly

- Parses discussion URLs so you don't have to hand-extract owner/repo/PR/comment-id.
- Uses `jq` to build the JSON payload, so multi-line bodies with quotes / backticks / Markdown round-trip safely.
- Single output line (the reply URL) makes it easy to chain.

If the command is missing a flag you need, extend it rather than reaching for `gh` directly.
