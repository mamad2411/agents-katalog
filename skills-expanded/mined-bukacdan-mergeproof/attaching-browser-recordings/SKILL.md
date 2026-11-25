---
name: attaching-browser-recordings
description: Use when preparing, creating, or updating a GitHub pull request for browser-visible changes that reviewers can verify through a UI demo, screen recording, or visual evidence.
license: MIT
compatibility: Requires browser automation with video capture, GitHub CLI 2.99.0+, GitHub.com network access, and authenticated push access to the target repository.
---

# Attaching Browser Recordings

## Core principle

For a browser-visible change, PR evidence includes a short recording of verified behavior. Exercise the real flow and attach it in the same authorized PR operation.

## Decide whether to record

| Change | Action |
| --- | --- |
| UI, interaction, responsive behavior, animation, or rendered fix | Record the shortest reviewer-relevant flow. |
| No meaningful browser behavior | Skip and state why. |
| Flow or recorder unavailable | Report the blocker; never fabricate verification. |

If creating or updating the PR is in scope, attaching its evidence needs no separate confirmation. Otherwise stop before `gh` mutates GitHub and report the local path.

## Record and verify

1. Identify the changed behavior and expected final state. Use sanitized test data.
2. Prepare the page first. Exclude secrets, personal data, unrelated UI, and dead time.
3. Create a task-specific directory outside the worktree with `mktemp -d`.
4. Use the available browser automation's native recorder. With `agent-browser`:

```bash
recording_dir="$(mktemp -d)"
video_path="$recording_dir/profile-update.webm"
agent-browser open http://127.0.0.1:3000/settings/profile
agent-browser record start "$video_path"
agent-browser snapshot -i
agent-browser fill @e2 "Ada Lovelace"
agent-browser click @e3
agent-browser wait --text "Profile updated"
agent-browser record stop
```

5. Inspect the final state. Confirm the video exists, plays, shows the intended result, and is at most 10 MB; otherwise retake it.

## Attach to GitHub

Confirm `gh --version` is at least 2.99.0, `gh auth status` succeeds for `github.com`, and `gh repo view --json viewerPermission` reports `WRITE`, `MAINTAIN`, or `ADMIN`.

Write a concise body naming the flow and result. Put the exact local video path alone in its paragraph:

```markdown
## Browser verification

Exercised the profile-name update and observed the success confirmation.

![](/absolute/path/to/profile-update.webm)
```

- New PR: pass the body and the same path to `gh pr create --body-file "$body_file" --attach "$video_path"`.
- Existing PR: resolve its number, then run `gh pr comment "$pr_number" --body-file "$body_file" --attach "$video_path"`.

GitHub CLI rewrites the local reference; the standalone paragraph renders as a player. Video attachments do not support `#alt-text`. Never pass the same file twice in one command.

Success requires exit status zero and a returned GitHub URL. Report the URL, then remove the temporary directory. On failure, preserve the video, report its path and exact cause, and retry only after correcting that cause.

## Quick reference

| Requirement | Value |
| --- | --- |
| GitHub CLI | 2.99.0 or newer |
| Video types | WebM, MP4, MOV |
| Size | At most 10 MB |
| Host/access | GitHub.com with repository push access |

## Common mistakes

- The flag is `--attach`, not `--atach`.
- Preparing inside the recording produces setup footage.
- A video reference inside a sentence renders a link, not a player.
- An unreferenced attachment is appended instead of placed deliberately.
- A passing test without inspecting the recorded state is not visual verification.
- If sensitive data appears, retake the recording; editing comment text cannot remove it from the video.
