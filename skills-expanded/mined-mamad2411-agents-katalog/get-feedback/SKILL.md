---
name: get-feedback
description: Retrieves pending review feedback from Monocle. Use when the reviewer has submitted feedback through the Monocle TUI, or after receiving a feedback_submitted notification.
---

# Get Review Feedback

## Usage

Run `monocle review get-feedback` to retrieve pending review feedback.

## Handling the response

- If feedback is available, read it carefully and act on it — the feedback contains your reviewer's comments, issues, and suggestions about your code changes
- If no feedback is pending, inform the user that no review feedback is available yet

## Replying to Monocle threads

- Always answer the user's comments in the corresponding Monocle thread
- If a comment asks for a change, reply in that thread after handling it; state whether the change was implemented, and explain precisely what changed
- If a requested change was not implemented, reply in that thread and justify why it was not implemented
- If a comment asks a question, reply in that thread with a clear, concise answer in plain English
- Never mark a Monocle thread resolved; only the user may resolve threads

After receiving feedback, address the reviewer's comments in your code, then continue with your work.

If Monocle reports multiple running sessions, ask the user which listed repo to use. After they choose, rerun the command with `-C <chosen repo>`.

If the command fails with a message that Monocle is not running, let the user know they need to start Monocle with `monocle` for the repo they want reviewed, or rerun with `-C <repo>` if Monocle is already running elsewhere.
