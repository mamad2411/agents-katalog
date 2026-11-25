---
name: handoff
description: Write the current conversation into a portable handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
license: MIT
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS, outside the current workspace. Tell the user the file's absolute path, so they can open it in the next session or send it on.

Include a "suggested skills" section in the document, naming which skills the next agent should load and follow through the host's skill mechanism. For a user-invoked skill, tell the user to run `/name` in Claude linked installs or Cursor, `/supermatt:name` from the Claude plugin, `$name` in Codex, or `/skill:name` in OMP.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Preserve the working state the next agent cannot recover from those pointers: the objective, decisions, failed attempts and their outcomes, blockers, explicit user stops, and the scope of authorization already given. End with one concrete next action. Carry authorization forward without inventing new permission or asking for an approval already supplied.

For repository work, inspect and record the repository, branch, commit, and dirty state. Tie each check or verdict to the state actually tested, including relevant configuration or environment; distinguish current evidence from an earlier claim. Missing or blocked checks stay incomplete. Tell the receiving agent to recheck mutable state before acting, including branch, worktree, running processes, and remote issue or PR state when relevant.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
