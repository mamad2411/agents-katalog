---
name: orc-git-flow
description: "Preserve Git work and deliver reviewable branches/commits; publish a branch or PR when authorized by the task or user."
---

# Git delivery

Inspect repository root, current branch, status and relevant task/PR references.
Preserve unrelated work and use the task's existing worktree/branch when supplied.
On rework, verify the recorded branch and commit instead of choosing the closest
name. If ambiguous, resolve the actual checkout before editing.

For fresh work use an isolated feature branch, following project naming conventions.
Commit intended changes in verifiable units with a description of what changed and
why. Do not stage unrelated files or commit secrets, private transcripts or credentials.

When the user/task authorizes publishing, push the feature branch normally and
open or update its PR through available GitHub tooling. Reuse an existing PR;
never force-push or publish to a protected/default branch without explicit authorization.
When publishing is unavailable or unauthorized, deliver the local artifact and state
the limitation; do not invent a PR or require a push to report verified local work.

PR descriptions explain the problem, resulting behavior, validation and material
limits. Use structured arguments or a body file for multiline descriptions.
Include branch, commit, PR/worktree when applicable in the shared work summary.
Git operations do not change the flow protocol; report the node outcome and stop.
