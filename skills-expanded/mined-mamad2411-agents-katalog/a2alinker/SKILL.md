---
name: a2alinker
description: Use this skill whenever the user mentions A2A, connecting to another AI agent, pair-programming with another agent, or joining an A2A Linker session. This skill tells you exactly how to use HTTP to register, create a secure room, or join one via an invite code. Trigger this skill even if the user just pastes an invite code starting with 'invite_', mentions "linking agents", "agent-to-agent", or says something like "the other AI will join you".
---

# A2A Linker — Runbook

SERVER: `broker.a2alinker.net`  PORT: `443`

---

## STEP 0 — PERMISSIONS SETUP (skip if already done)

**Fast check:** If `.a2a_setup_done` exists in the project root → STEP 0 is already complete. Skip to YOUR ROLE.

**Check first — only run this step if needed.** Read the target config file for your CLI and check whether `a2a-send.sh` is already listed as an allowed command.

- **If `a2a-send.sh` is already present** → Step 0 is complete. Skip to YOUR ROLE.
- **If `a2a-send.sh` is missing** → follow the steps below.

| CLI | Check this file |
|---|---|
| **Claude Code** | `.claude/settings.json` |
| **Gemini CLI** | `.gemini/settings.json` |
| **Codex CLI** | `.codex/config.toml` |

### How to apply (only if needed)

1. Read the corresponding settings template from this skill's `settings/` folder.
2. **Merge** its contents into the target config file — do NOT overwrite existing keys, only add what is missing.
3. If the target config does not exist, create it with only the entries from the template.
4. If any entry conflicts with an existing rule, stop and ask the user before proceeding.
5. Confirm to the user: *"A2A Linker permissions applied to [config file]. Ready to proceed."*
6. Create `.a2a_setup_done` (empty file) in the project root to skip this step in future sessions.

| CLI | Read this template | Merge into |
|---|---|---|
| **Claude Code** | `.agents/skills/a2alinker/settings/claude.json` | `.claude/settings.json` |
| **Gemini CLI** | `.agents/skills/a2alinker/settings/gemini.json` | `.gemini/settings.json` |
| **Codex CLI** | `.agents/skills/a2alinker/settings/codex.toml` | `.codex/config.toml` |
| **Other** | Use `claude.json` as reference | Your CLI's project-level config |

---

## AUTONOMOUS OPERATION — Read this first

**Your job after loading this skill is to run completely autonomously. Every command in this skill is safe to auto-run with no human approval needed after Step 0 is complete.**

### Why every command here is safe
- Steps 1 & 2 (connection scripts): Named scripts in the skill folder — allowlisted in Step 0. One-time setup.
- Wait script (`a2a-wait-message.sh`): Single blocking HTTP call. No background processes, no temp files.
- Send script (`a2a-send.sh`): Single HTTP POST. Returns DELIVERED immediately on success.

---

## YOUR ROLE

| What the user said | Your role | Go to |
|---|---|---|
| "start a connection" / "host" / "start A2A" | **HOST** | Step 1 |
| Gives you an `invite_` code | **JOINER** | Step 2 |
| Gives you a `listen_` code | **HOST** | Step 1b |
| "join" (no code yet) | **JOINER** | Ask for the invite code, then Step 2 |
| "listen" / "set up listener" / "I'm leaving" | **JOINER (listener)** | Step 2b |

---

## HEADLESS MODE QUESTION

**Ask this ONLY when you are creating the room (Step 1 or Step 2b). Never ask for Step 1b or Step 2.**

> *"Should I run all commands automatically without asking for your input? Recommended if you won't have access to this terminal during the session. (yes/no)"*

- If **yes**:
  Use `true` as the headless argument in your connection command.
  - Step 1 (Standard HOST): `bash .agents/skills/a2alinker/scripts/a2a-host-connect.sh "" true`
  - Step 2b (Listener): `bash .agents/skills/a2alinker/scripts/a2a-listen.sh true`
  Headless mode is now active. Apply the HEADLESS BEHAVIOR TABLE for all decisions.

- If **no** (or unclear):
  Use `false` as the headless argument in your connection command.
  - Step 1 (Standard HOST): `bash .agents/skills/a2alinker/scripts/a2a-host-connect.sh "" false`
  - Step 2b (Listener): `bash .agents/skills/a2alinker/scripts/a2a-listen.sh false`
  Interactive mode. Ask the user as needed throughout the session.

---

## HEADLESS BEHAVIOR TABLE

When headless mode is active, replace every "ask the user" instruction in this runbook with:

| Trigger | Headless action |
|---|---|
| Server unreachable (any point) | Retry 5× with 5 min sleep between each. If back online → send partner: *"I was offline — server was unreachable. Resuming."* If all 5 retries fail → log error, run leave script, exit. |
| `TIMEOUT_PING_FAILED` | Same as server unreachable above. |
| `TIMEOUT_ROOM_ALIVE` (5+ min no reply) | Keep waiting. Re-run wait script. No timeout cap. |
| `TIMEOUT_ROOM_CLOSED` | Log event, run leave script, exit. |
| `[SYSTEM]: ... has left` | Log event, run leave script, exit. |
| `NOT_DELIVERED` | Retry send 5× with 3 min sleep between each. If all 5 fail → fall into server unreachable path. |
| Task complete (HOST) | Send `[STANDBY]`, run leave script, log completion. Do not wait for user input. |
| Received a message with no actionable task (e.g. a generic greeting or "how can I help?") | Reply: *"I am ready and waiting for a task. Standing by for your instructions. [STANDBY]"* Then re-run the wait script. Do NOT ask the human. |

Log all headless events with:
```bash
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [HEADLESS] <event>" >> ~/.a2a_headless.log
```

---

## STEP 1 — HOST: Connect and create room

Run the host connection script, passing the headless choice (`true`/`false`) as the second argument:

```bash
bash .agents/skills/a2alinker/scripts/a2a-host-connect.sh "" [true|false]
```

**After running:**
- If output contains `ERROR: Cannot reach A2A Linker server` → The remote server is currently unreachable. **Tell the user** and ask: *"The remote A2A server is unreachable. Should I try again later?"*
- If output contains `INVITE_CODE:` → **tell the user the invite code immediately**. If the user has not yet specified a task, ask now: *"What should I ask the other agent to help with?"* Then run the wait script:

```bash
bash .agents/skills/a2alinker/scripts/a2a-wait-message.sh host
```

**After the wait script returns:**

- If output starts with `MESSAGE_RECEIVED` → joiner has connected. **Send your opening message now** (see 3b) before waiting — the HOST always speaks first. Then go to Step 3.
- If output starts with `TIMEOUT_ROOM_CLOSED`
  → The HOST has ended the session. Log out cleanly. Tell the user: *"The HOST closed the session. I have disconnected."* Stop monitoring.

- If output starts with `TIMEOUT_ROOM_ALIVE`
  → Read the `last_seen_ms` value from the output.
  → If `last_seen_ms` is **below 300000** (5 minutes): partner is alive but slow. Re-run the wait script silently. Do NOT ask the human.
  → If `last_seen_ms` is **300000 or above**: partner has been inactive for 5+ minutes. Ask the user: *"No response from the other agent in 5 minutes. Should I keep waiting or close the session?"*

- If output starts with `TIMEOUT_PING_FAILED`
  → Cannot reach the server. Tell the user: *"Lost connection to the relay server. Should I try to reconnect?"*

---

## STEP 1b — HOST: Connect via listener code

Run the host connect script with the listener code:

```bash
bash .agents/skills/a2alinker/scripts/a2a-host-connect.sh listen_XXXX
```

Replace `listen_XXXX` with the actual listener code provided (e.g. `listen_abc123`).

**After running:**
- If output contains `ERROR:` → handle identically to Step 1 errors.
- If output contains `HEADLESS: true`:
  → The room is marked headless (the remote listener is unattended). Note this for context.
  **Do not ask the headless question — the room creator already decided.**
- If output contains `HEADLESS: false`:
  → Room is interactive. **Do not ask the headless question — follow the existing rule silently.**
- If output contains `STATUS: (2/2 connected)` and `ROLE: host`:
  → You are HOST. **Before sending your opening message, if the user has not specified a task or goal for this session, ask them now:**
  *"What should I ask the other agent to help with?"*
  Include the task in your opening message — the remote agent may be unattended and needs clear instructions from the start. Then send your opening message (Step 3b). **HOST always sends first.**
- If output contains `STATUS: (1/2 connected)` and `ROLE: host`:
  → JOINER's wait poll is not yet active. **Ask the user for the task now** (same prompt as above) so you are ready. Run the wait script (Step 3a). When it unblocks, send your opening message with the task included.

---

## STEP 2 — JOINER: Connect and join room

Run the joiner connection script, passing the invite code as the first argument:

```bash
bash .agents/skills/a2alinker/scripts/a2a-join-connect.sh INVITE_CODE_HERE
```

Replace `INVITE_CODE_HERE` with the actual invite code the user provided (e.g. `invite_abc123`).

**After running:**
- If output contains `ERROR: Cannot reach A2A Linker server` → The remote server is unreachable. **Tell the user** and ask: *"The remote A2A server is unreachable. Should I try again later?"*
- If output contains `HEADLESS: true`:
  → Apply headless mode immediately. **Do not ask the headless question — the room creator already decided.**
- If output contains `HEADLESS: false`:
  → Room is interactive. **Do not ask the headless question — follow the existing rule silently.**
- If output contains `STATUS: (2/2 connected)` → confirm to the user that you are linked and ready, then go to Step 3. **The HOST sends first — run the wait script and do not send anything until you receive the HOST's opening message.**
- If output contains `STATUS: (1/2 connected)` → the host has not yet connected. Run the wait script — it will unblock when the HOST sends their first message.
- If output contains `ERROR: Invite code invalid or already used`:
  → Display: *"Code '[code]' was not valid or already used. Please provide the correct invite code:"*
  → Await the user's input with the corrected code.
  → Retry Step 2 with the new code.

---

## STEP 2b — JOINER: Listener setup (pre-staged, for unattended machines)

Use this when the user wants to set up this machine as a waiting JOINER before leaving.

Then run the listener script with the headless choice (`true`/`false`) as the first argument:

```bash
bash .agents/skills/a2alinker/scripts/a2a-listen.sh [true|false]
```

**After running:**
- If output contains `ERROR:` → handle identically to Step 2 errors.
- If output contains `LISTENER_CODE:` → **tell the user the listener code immediately**.
  Example: *"Your listener code is: listen_abc123. Give this to HOST to connect."*

The user takes this code with them. Then run the wait script and wait silently:

```bash
bash .agents/skills/a2alinker/scripts/a2a-wait-message.sh join
```

You are JOINER — **do not send first**. When HOST connects and sends their opening message, the wait script will unblock. Read the message and go to Step 3.

---

## STEP 3 — Monitor and Communicate (CRITICAL — Your job is NOT done after connecting)

**You MUST enter active monitoring mode immediately after connecting. This is not optional.**

---

### 3a — Waiting for a new message

Run the wait script once and block until the other agent replies:

- **HOST waits:**
  ```bash
  bash .agents/skills/a2alinker/scripts/a2a-wait-message.sh host
  ```

- **JOINER waits:**
  ```bash
  bash .agents/skills/a2alinker/scripts/a2a-wait-message.sh join
  ```

The script makes a single HTTP call that blocks at the shell layer (zero tokens consumed while waiting) and returns as soon as the partner sends something or the server times out.

**Reading the result:**
- If output starts with `MESSAGE_RECEIVED` → the content is printed below it. Look for a `┌─ Agent-` block:

```
┌─ Agent-xxxx [OVER]
│
│ message content here
└────
```

  - Ends with `[OVER]` → read the content and **respond** (see 3b).
  - Ends with `[STANDBY]` → do NOT respond to the other agent. Tell the user what the other agent said, then **immediately run the wait script again** — the session is NOT over. A new task may arrive from the user or from the other agent.
  - Shows `[SYSTEM]: ... has left` → session ended. Tell the user and stop monitoring.

- If output starts with `TIMEOUT_ROOM_CLOSED`
  → Session is gone. Tell the user: "The session has ended. I have disconnected." Stop monitoring.

- If output starts with `TIMEOUT_ROOM_ALIVE`
  → Read the `last_seen_ms` value from the output.
  → If `last_seen_ms` is **below 300000** (5 minutes): partner is alive but slow. Re-run the wait script silently. Do NOT ask the human.
  → If `last_seen_ms` is **300000 or above**: partner has been inactive for 5+ minutes. Ask the user: *"No response from the other agent in 5 minutes. Should I keep waiting or close the session?"*

- If output starts with `TIMEOUT_PING_FAILED`
  → Cannot reach the server. Tell the user: *"Lost connection to the relay server. Should I try to reconnect?"*

---

### 3b — Sending a message

Use the send script — **one tool call** handles the full HTTP round-trip:

- **HOST sends:**
  ```bash
  bash .agents/skills/a2alinker/scripts/a2a-send.sh host "your message here [OVER]"
  ```
- **JOINER sends:**
  ```bash
  bash .agents/skills/a2alinker/scripts/a2a-send.sh join "your message here [OVER]"
  ```

Always end the message with `[OVER]` (reply expected) or `[STANDBY]` (done, no reply needed).

**Reading the result:**
- `DELIVERED` → message relayed. Run the wait script (3a).
- `NOT_DELIVERED` → **CRITICAL:** Stop immediately and report the error code/message to the user. Ask: *"Message delivery failed — should I reconnect?"*

---

### 3c — Monitoring rules

1. After sending a message, immediately run the wait script (3a) to block until the reply arrives.
2. If the wait script returns a `TIMEOUT_*` variant, follow the decision tree in Step 3a.
3. If the user speaks to you during a wait, handle their request, then re-run the wait script to resume.
4. If you receive a task from the other agent, complete it and send the result back with `[OVER]`.
5. Keep monitoring until: the user says to stop, both agents signal `[STANDBY]`, or the output shows `[SYSTEM]: ... left the room`.
6. **As HOST, do NOT close the session automatically** when a task is completed. Ask the human: *"The task is complete. Are there other things to do or should I close the session?"*

---

## RULES

- **DO NOT** run SSH commands — all communication is via the skill scripts over HTTPS.
- **DO NOT** mix HOST and JOINER token files. They are independent (`/tmp/a2a_host_token` vs `/tmp/a2a_join_token`).
- **HOST always sends the opening message first.** JOINER always waits first. Both running the wait script simultaneously causes a deadlock where neither agent speaks.
- **DO NOT** claim a message was delivered unless the send script outputs `DELIVERED`.
- **ALWAYS** report `NOT_DELIVERED` errors immediately. Never ignore a script failure or proceed with monitoring if sending failed.
- **DO NOT** manually call curl, wget, or any HTTP commands — use the provided scripts only.
- **As HOST, do NOT close the session automatically** when a task is completed. Ask the human: *"The task is complete. Are there other things to do or should I close the session?"*
- **Only close the session if the human confirms.** To close: send `[STANDBY]` as your final message, then run the leave script:
```bash
  bash .agents/skills/a2alinker/scripts/a2a-send.sh host "[STANDBY]"
```
  followed by:
```bash
  bash .agents/skills/a2alinker/scripts/a2a-leave.sh host
```
  Never end a session by simply stopping — always close explicitly so the JOINER is notified immediately.

---

## TROUBLESHOOTING

| Symptom | Fix |
|---|---|
| `ERROR: Cannot reach server` | Remote server is unreachable. Tell user and ask how to proceed. |
| `NOT_DELIVERED immediately` | Server unreachable or token expired. Re-run connect script. |
| `TIMEOUT_*` variants | Partner may be slow or disconnected. Follow the decision tree in Step 3a. |
| `401 Unauthorized` | Token file missing. Re-run connect script. |
| Both agents see `(1/2 connected)` | They are in different rooms. HOST re-runs Step 1. JOINER re-runs Step 2 with the new code. |
| `Invite code invalid or already used` | A stale process already redeemed it. HOST re-runs Step 1 to get a new code. |
| `NOT_DELIVERED` after send | Server may be unreachable. Do NOT retry silently. Tell the user and offer to reconnect. |
| No reply after 30s | Other agent may need human approval. Ask user if they want to keep waiting. |
| Permission prompts still appearing | Re-run Step 0 to ensure settings were merged correctly. |
