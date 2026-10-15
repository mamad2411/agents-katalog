---
name: grok-build-connector
description: Initialize and operate a visible Codex–Grok Build collaboration with a loopback-only live UI in the Codex in-app browser. Use when the user asks to install or configure Grok Build, sign in to Grok, consult or debate with Grok, compare independent AI answers, continue a Grok session, review work with Grok, or watch Codex and Grok exchange messages in real time.
---

# Grok Build Connector

Keep Codex as orchestrator and final verifier. Use Grok Build as an independent counterpart, and mirror only public messages and status events to the bundled live UI.

## Resolve the skill

Set `SKILL_DIR` to this skill directory. Run all bundled scripts with Python 3 from `"$SKILL_DIR/scripts"`.

## Initialize Grok Build

Run the safe scan before the first collaboration in a task:

```bash
python3 "$SKILL_DIR/scripts/bootstrap.py" status
```

If the result reports `installed: false`:

1. Tell the user that installation downloads and runs xAI's official installer.
2. Show the reported official URL and command.
3. Obtain explicit approval before changing the user's global environment.
4. After approval, run:

```bash
python3 "$SKILL_DIR/scripts/bootstrap.py" install --yes
```

Never run `install --yes` silently. The installer is downloaded from `https://x.ai/cli/` to a temporary file before execution.

If Grok is installed but not authenticated, start an interactive login in a visible TTY:

```bash
python3 "$SKILL_DIR/scripts/bootstrap.py" login
```

For a headless or remote environment, add `--device-auth`. Pause while the user completes authentication; do not collect credentials. When the user says login is complete, verify with:

```bash
python3 "$SKILL_DIR/scripts/bootstrap.py" verify
```

After successful setup, briefly explain the four modes—consult, debate, review, and scoped implementation—and offer 2–4 relevant examples from `references/prompt-templates.md`.

## Open the live UI

Start or reuse the detached loopback server. A normal `start` always creates a new isolated conversation:

```bash
python3 "$SKILL_DIR/scripts/live_ui.py" start \
  --topic "<discussion title>" \
  --subtitle "<decision question>"
```

Follow this order before sending any round to Grok:

1. Read the JSON `url` and immediately send a commentary update containing a clickable `[Open Live UI](<url>)` link. This gives the user a manual recovery path before any browser automation.
2. Explicitly select the Codex in-app browser (`iab`) with the available browser-control skill. Claim an existing matching Live UI tab or create one, navigate it to the exact `url`, make the browser visible, and keep the Live UI tab as the user-facing deliverable.
3. Start the Codex–Grok exchange only after the link has been shown and in-app navigation has been attempted.

Never call a system-browser opener, Python `webbrowser`, macOS `open`, `live_ui.py start --open`, or any default-browser fallback. If Codex in-app browser control is unavailable, leave the clickable link in the conversation and explain that the user can open it manually inside Codex; do not silently substitute Safari, Chrome, or another external browser.

Keep the returned `conversationId`. Resume an exact earlier conversation only when the user asks:

```bash
python3 "$SKILL_DIR/scripts/live_ui.py" start --conversation "<conversation-id>"
```

The server binds only to `127.0.0.1`, uses a random bearer token, sends SSE keepalives, and remains active until explicitly stopped or the operating system ends it. Public messages, rounds, summaries, and errors are stored in a permission-restricted local SQLite database so conversations remain separate and survive a server restart. Transient phase and metric events are not retained.

## Run a visible exchange

Prepare one UTF-8 file containing Codex's public position and one containing the exact prompt for Grok. Run one read-only round:

```bash
python3 "$SKILL_DIR/scripts/run_round.py" \
  --mode debate \
  --conversation "<conversation-id>" \
  --round 1 \
  --total 3 \
  --round-label "提出主張" \
  --codex-file /tmp/codex-round-1.txt \
  --prompt-file /tmp/grok-round-1.txt \
  --cwd "$PWD"
```

The round runner automatically resumes the Grok session mapped to that conversation. Do not manually pass a Grok session ID. Obtain first proposals independently when bias matters, then pass each side's actual argument to the other.

Default to no more than three exchange rounds. Stop early on clear convergence; extend to five only when a concrete unresolved claim remains. End with Codex separating consensus, disagreements, evidence, and the recommended result. Model agreement is not verification.

Emit a summary or other allow-listed event with:

```bash
python3 "$SKILL_DIR/scripts/emit_event.py" \
  --conversation "<conversation-id>" \
  --json '{"kind":"summary","title":"結論","text":"..."}'
```

Only emit `session`, `round`, `message`, `phase`, `summary`, `metric`, or `error` events. Never send hidden reasoning, credentials, environment variables, or raw tool traces to the UI.

## Use Grok without the UI

Use the bundled safe wrapper directly for a single consultation or review:

```bash
python3 "$SKILL_DIR/scripts/grok_collab.py" ask \
  --mode consult \
  --cwd "$PWD" \
  --prompt "Give an independent solution and state the strongest uncertainty."
```

Use `implement --allow-writes` only after explicit authorization and only in an isolated or trusted worktree. Inspect Grok's diff and run the relevant verification yourself.

## Manage the server

```bash
python3 "$SKILL_DIR/scripts/live_ui.py" status
python3 "$SKILL_DIR/scripts/live_ui.py" list
python3 "$SKILL_DIR/scripts/live_ui.py" url --conversation "<conversation-id>"
python3 "$SKILL_DIR/scripts/live_ui.py" delete --conversation "<conversation-id>"
python3 "$SKILL_DIR/scripts/live_ui.py" stop
```

Reuse a healthy server rather than opening duplicates. Starting a new topic creates a new conversation inside that server; it never appends to an earlier conversation implicitly. The user can search, switch, and delete local conversations in the UI. Stop only when the user asks, the task requires cleanup, or the server must be upgraded.

## Handle failures

- If another process occupies port 8765, let the manager select a free loopback port.
- If login cannot open a browser, retry with `login --device-auth`.
- If Grok returns an authorization error, run `verify`; do not fabricate a reply.
- If the UI reconnects or the server restarts, reopen the same `conversationId`; its durable history remains available.
- If the UI cannot open inside Codex, keep the clickable Live UI link visible and report the limitation; never open an external browser automatically.
