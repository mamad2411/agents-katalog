---
name: orc-handoff
description: Move an existing local Claude Code or Codex session into ORC so it can continue in an ORC terminal, including an SSH execution host. Use when the user asks to hand off or continue the current session in ORC.
---

# Hand off a native session to ORC

ORC copies the conversation into a new native session ID on its selected execution host.
The original session is preserved. Its project must already have a folder scope pointing
to the correct repository on that host. ORC creates `.orc/worktrees/<handoff-id>` in that
repository, with a unique local branch tracking the pushed branch at the recorded commit.

## Prepare the code state

1. Identify the ORC project, native agent (`claude` or `codex`), native session UUID,
   current folder, repository remote and branch. If inside a repository subfolder, record
   `git rev-parse --show-prefix` without its trailing slash as `subdirectory`.
   Use the session's actual native transcript;
   an ORC event snapshot is not a resumable native session.
2. Inspect Git status. Commit only the intended work. Explain any necessary ignored files,
   environment variables, dependencies, LFS objects or submodules that Git alone will not
   reproduce; resolve required missing state before declaring the handoff ready.
   Required tracked or untracked changes left outside the pushed commit block a complete
   handoff. Resolve what to include with the user when its scope is unclear.
3. Push to the intended branch using normal Git push. Use a dedicated branch when needed.
   Preserve existing work and the user's commit/push constraints; never force-push or push
   a protected/default branch without the user's authorization.
4. Record `git rev-parse HEAD` and verify `git ls-remote <remote> refs/heads/<branch>`
   reports that exact SHA. A failed push or unmatched remote SHA blocks the handoff.
   Report a credential-free repository URL; keep credential-helper and SSH authentication local.

## Request and upload

Call the one MCP tool `session_handoff` with:

```json
{
  "project": "project-name",
  "agent": "codex",
  "session_id": "native-session-uuid",
  "source_cwd": "/local/repo",
  "subdirectory": "",
  "repository": "git@github.com:owner/repo.git",
  "remote": "origin",
  "branch": "handoff/my-work",
  "commit": "40-character-pushed-commit-sha",
  "title": "Continue my work"
}
```

The same operation is `POST /api/session-handoffs` with normal ORC Bearer auth.
Read the returned `upload_url`, `max_bytes`, `id` and expiry. The upload URL grants only
one bounded upload for 15 minutes. Treat it as a secret; do not commit or publish it.

Find the native file:
- Claude Code: `${CLAUDE_CONFIG_DIR:-~/.claude}/projects/<encoded-cwd>/<session-id>.jsonl`.
  Include that session's `subagents/agent-*.jsonl` files when present.
- Codex: `${CODEX_HOME:-~/.codex}/sessions/YYYY/MM/DD/rollout-*-<session-id>.jsonl`.
  Archived native rollouts can also be supplied explicitly.
  Hand off the parent session rather than a standalone Codex child-agent session.

Use the included helper, resolved relative to this skill's directory:

```sh
python scripts/upload-session.py --agent codex --session-file /path/to/rollout.jsonl --upload-url '<returned-url>'
```

It snapshots text files and PUTs a version 1 JSON bundle containing `session.jsonl` and
supported sidecars. It never uploads credentials, agent settings, SQLite databases or
the project checkout. Keep the native session idle while snapshotting; do not edit or
commit additional work after recording the pushed state.

## Finish or recover

Successful upload returns `status: ready`, the destination cwd and `live_session_id`.
Tell the user to open **ORC → Sessions → Open in terminal** for that imported session.
Uploading alone is not success: check the returned status and report any error.

Inspect with `GET /api/session-handoffs/<id>`. If the upload was received but preparation
failed, fix the reported cause and retry `POST /api/session-handoffs/<id>/prepare` with
normal ORC Bearer auth. An expired or consumed upload link cannot be reused. If the
branch moved or the pushed SHA changed, initiate a new handoff with the verified state.

The session resumes with destination CLI credentials/configuration. Running processes,
open shells, ignored files and external attachments are not transferred. Old message
text retains historical source paths; structured session cwd metadata is relocated.
