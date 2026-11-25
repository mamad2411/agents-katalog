---
name: beacon-trace-share
description: Share the current agent session (or another local one) as a trace on beacon.sh with the Beacon CLI, and give the user the link. Use when the user asks to "share this session", "share to beacon", "publish this trace", "upload this session", wants a link to show a teammate what the agent did, or wants an already shared session updated with its latest steps.
license: MIT
compatibility: Requires the Beacon CLI (beacon) on PATH with endpoint capture installed, and a beacon.sh sign-in (beacon login) or a Beacon API key in BEACON_API_KEY. Uploads the chosen session's content to beacon.sh, only when the user asks.
metadata:
  author: asymptote-labs
  homepage: https://docs.beacon.sh/cli/share
  version: "0.1.0"
---

# Beacon trace share

`beacon share` publishes one agent session as a **shared trace** on beacon.sh: the prompts, the
agent's answers and reasoning, and every tool call with its result, after Beacon's secret
redaction and with local paths made relative. It prints a link the user can send to anyone they
choose.

Sharing uploads the conversation. Only share when the user asked for it, and never change the
visibility to public without asking.

## Step 1: check that Beacon is available

```bash
beacon version
```

If `beacon` is not found, tell the user that sharing needs the Beacon CLI, point them to
https://docs.beacon.sh/get-started/overview, and stop. Do not install it yourself.

## Step 2: share this session

Run this from the session's working directory, naming your own runtime with `--harness`:

```bash
beacon share --current --harness <runtime> --json
```

| You are | `<runtime>` |
|---------|-------------|
| Claude Code | `claude_code` |
| Codex CLI | `codex` |
| Cursor | `cursor` |
| OpenCode | `opencode` |
| Gemini CLI | `gemini` |
| GitHub Copilot CLI | `copilot` |
| Another runtime | its name from `beacon share --help`, or `auto` |

`--current` finds the session this command runs inside: from `BEACON_SESSION_ID` when the
runtime exports it, otherwise from the session Beacon's hooks last saw in this directory,
otherwise the most recent session here. `--harness` keeps it from picking another runtime's
session in the same directory.

The default visibility is **direct**: anyone with the link can open it, and it is not listed
anywhere. Keep that unless the user asked for something else:

- **private** (only the user, when signed in): add `--visibility private`.
- **public** (listed in Discover for anyone to find): first ask the user to confirm that the whole
  session may be public. Only after they say yes, add `--visibility public --yes`.

To see exactly what would be uploaded without uploading anything, run the same command with
`--print` in place of `--json`.

## Step 3: post the link

On success the output is one JSON document:

```json
{"ok":true,"data":{"shared_url":"https://beacon.sh/s/...","visibility":"direct","external_id":"claude_code:...","event_count":42,"uploaded":42,"selected_by":"env"}}
```

Reply with `shared_url` and its visibility, and say how many events it holds. If
`selected_by` is `recent`, mention which session was shared (the `external_id`), since Beacon
picked the newest session in the directory rather than one it knew was this one.

Sharing again later updates the same trace. To add only the steps since the last upload:

```bash
beacon share refresh --harness <runtime> --json
```

## Troubleshooting

On failure the output is `{"ok":false,"error":"..."}` and the command exits non-zero.

**No session found.** List what Beacon can see here, then share the right one by id:

```bash
beacon share --list --harness <runtime> --json
beacon share --session <session-id> --json
```

If the list is empty, Beacon is probably not capturing this runtime; suggest
`beacon endpoint install` and stop.

**Not signed in, or missing the traces:write permission.** Ask the user to run `beacon login`
in their own terminal (it opens a browser, so do not run it for them), then retry. In CI or
another headless environment, a Beacon API key in the `BEACON_API_KEY` environment variable is
used instead; never ask the user to paste a key into the conversation.

**A public share was refused.** Without a terminal, public needs `--yes`, which you add only after
the user confirmed.
