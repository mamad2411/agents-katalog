---
name: collaborate
description: Multi-person collaborative document writing skill. Use when two or more people need to co-author a document (strategy memo, decision paper, analysis, report) through Claude with shared context, turn-based handoffs, reviewer feedback tracking, versioned history, and a persistent timeline log. Storage: Google Drive or local. Notifications: Signal, Slack, or email.
---

# Co-Write

Collaborative document authoring for teams. One shared source of truth. Context — not just text — travels between contributors.

---

## Natural Language Detection

Users should never need to know command names. Detect intent from what they say and map it to the right command.

| If the user says something like... | Run |
|------------------------------------|-----|
| "start a new document", "set up a co-write", "new session" | `init` |
| "show my sessions", "what documents am I working on", "find my co-writes" | `list` |
| "what's waiting for me", "where am I needed", "any documents need my attention", "my inbox" | `inbox` |
| "it's my turn", "I want to continue", "start working", "pick up the document" | `pickup` |
| "I need to add a file", "here's some background", "add this document" | `add-context` |
| "I'm done", "pass it on", "finished my part", "hand it over" | `handoff` |
| "I need to step away", "save my progress", "come back later", "done for now", "I'll finish later", "gotta go", "be back soon" | `pause` |
| "who's working on what", "where are we", "what's the status" | `status` |
| "put the sections together", "combine everything" | `merge` |
| "I approve this", "looks good", "sign off" | `approve` |
| "we're done", "archive this", "close the project" | `complete` |
| "go back to an earlier version", "undo", "restore" | `rollback` |
| "I want to make a change after approval", "can we reopen this", "need to edit the approved doc" | `reopen` |
| "export this", "save as PDF", "create a PDF", "export to PDF", "export as markdown", "give me a copy I can share" | `export` |
| "remove someone", "take them off the team", "they dropped out", "they're no longer involved" | `remove` |

If intent is ambiguous, ask one clarifying question. Never ask the user to retype something in a specific format.

**Special case — content pasted before pickup is complete:** If the user pastes substantial text (>50 words) while the skill is still in the session discovery, identity, or onboarding phase, acknowledge it before continuing: *"Got it — I've saved that. Let me finish getting you set up (takes about 10 seconds), and then we'll use what you just shared."* Store the pasted content in memory for the active turn and resume the pickup flow immediately. Do not lose the pasted content.

**Special case — `pause` detected:** Always offer a save prompt before closing: *"Before you go — want me to save your progress? It only takes a second and means you won't lose anything."* Wait for explicit yes/no. If no response (conversation ends), log the abandonment with a note that work may be unsaved.

---

## Commands

**Everyday commands** (most users only ever need these):

| Command | What it does |
|---------|-------------|
| `init` | Start a new co-write session |
| `pickup` | Start your turn on a document |
| `handoff` | Finish your turn and pass it on |
| `status` | See where things stand |
| `inbox` | See all documents waiting for your input, across all sessions |
| `pause` | Save progress and step away |
| `add-context` | Add background files or notes |

**Team management** (usually just the lead):

| Command | What it does |
|---------|-------------|
| `assign` | Assign sections to team members |
| `approve` | Give final sign-off |
| `complete` | Close and archive a finished session |

**Recovery** (when something goes wrong):

| Command | What it does |
|---------|-------------|
| `list` | Find active sessions |
| `rollback` | Restore an earlier version |
| `reopen` | Revert an approved document back to review for further edits |
| `export` | Export the document as PDF, Markdown, or both |
| `remove` | Remove a team member and reassign or close their work |

---

## Roles

Three roles. Keep it simple.

| Role | What they do |
|------|-------------|
| **writer** | Drafts and revises content |
| **reviewer** | Reads and gives feedback — doesn't rewrite |
| **approver** | Final sign-off — usually one person |

A person can hold multiple roles (e.g. writer on §1, reviewer on §2). When picking up, a dual-role person will be asked which role they're acting in for this session.
If only 2 people and no roles specified: both are writers, Ping-Pong mode. In this case, either writer can run `approve` and `complete` — there is no designated approver. The first person to call `approve` becomes the approver of record for that session.

---

## Modes

Auto-detected at `init`. Can be switched mid-session via `status`.

| Mode | Best for | Auto-detect |
|------|----------|------------|
| **Ping-Pong** | Sequential back-and-forth | Default / 2 writers |
| **Structured Critique** | One writer, one reviewer | Writer + reviewer roles |
| **Section Ownership** | Parallel work on sections | 3+ people or explicit sections |
| **Challenger/Defender** | Decision documents | Doc type is decision |
| **Annotation Loop** | Reviewing an existing draft | Existing doc provided |
| **Round Robin** | Everyone reviews everyone's sections | "Everyone should give feedback" / peer review |

---

## Document Structure Templates

Offered at `init` if the user doesn't have a structure in mind.

| Template | Sections |
|----------|----------|
| **Problem/Solution** | Problem → Analysis → Recommendation → Next Steps |
| **Situation/Complication/Resolution** | Situation → Complication → Resolution |
| **Report** | Executive Summary → Findings → Implications → Appendix |
| **Decision** | Context → Options → Recommendation → Risks |
| **Custom** | User defines sections |

---

## File Structure

```
shared-folder/
  {doc-name}.md              ← the document
  {doc-name}.status.md       ← session config (machine-written, don't edit)
  {doc-name}.log.md          ← full history — append-only
  {doc-name}.digest.md       ← summary of older history (auto-generated)
  .sections/
    01-{name}.md             ← section files (Section Ownership mode)
    02-{name}.md
  .context/
    {source-files}
    context-index.md         ← source file summaries
    context-digest.md        ← summary of older source entries
  .versions/
    {doc-name}.v1.md         ← snapshot before each handoff (non-Section Ownership)
    {doc-name}.v2.md         ← every handoff creates a new version, including revision turns
    {doc-name}.§1.v1.md      ← per-section snapshot (Section Ownership — T1)
    {doc-name}.§1.v2.md      ← T2 (post-review revision), T3, etc. — all turns snapshot
  .drafts/
    {doc-name}.{name}.draft.md  ← saved mid-turn draft
  .archive/                  ← created by `complete`
    {doc-name}/
  .{doc-name}.lock           ← held during handoff to prevent concurrent writes
  .{doc-name}.op             ← handoff operation log (exists only during active handoff)
  .{doc-name}.contacts       ← contact details per person (Signal numbers, Slack handles, emails)
                               ⚠ Contains PII — share this folder only with people on the team
```

---

## Storage Backends

| Backend | MCP tools |
|---------|-----------|
| **Google Drive** | Discover at runtime — see Google Drive MCP Discovery below |
| **Local** | Native `Read` / `Write` / `Edit` — includes iCloud shared folders (they appear as regular file paths) |

Selected once at `init`. Stored in `{doc-name}.status.md`.

### Google Drive MCP Discovery

Google Drive MCP tool names vary by installation (the UUID differs per user). At `init` when the user selects Google Drive, discover the right tools:

1. Look for available tools whose names match the pattern `mcp__*__read_file_content` or `mcp__*__create_file` and whose server description mentions Google Drive or gdrive.
2. Extract the server prefix (e.g. `mcp__abc123__`) and use it for all subsequent Drive operations: `read_file_content`, `create_file`, `copy_file`, `download_file_content`, `search_files`.
3. Store the discovered prefix in memory for the session — do not re-discover on every operation.
4. If no matching tools are found: *"I can't find a Google Drive MCP on your setup. You'll need to install one first — or we can save the document locally instead. Which would you prefer?"*

---

## Notifications

Optional. Selected at `init`. Can combine backends (e.g. Signal + email, Slack + Signal).

**Sending order with fallback:** Try primary → if error, try secondary → if both fail, show the user the message text to send manually.

| Backend | MCP |
|---------|-----|
| Signal | `mcp__signal__send_message` |
| Slack | `mcp__slack__send_message` — DM the user by their Slack user ID or @handle |
| Email | `mcp__proton-mail-bridge__send_email` |

**Per-person contact at `init`:** ask how to reach each person and which backend to use. A person may have Signal, Slack, or email — or none (they'll be notified manually).

On failure: *"I couldn't send the notification automatically. Here's the message to send to {Name}:"* → show full text.

---

## Lock File

Prevents two people from handing off simultaneously and corrupting the log.

**Lock file location depends on mode:**
- All modes except Section Ownership: `.{doc-name}.lock` (global)
- Section Ownership — writers: `.{doc-name}.§{N}.lock` (per section, allows parallel work)
- Section Ownership — reviewers/approvers: `.{doc-name}.review.lock` (one at a time)

**Lock file contents:**
```
Locked by: {Name}
Since: {YYYY-MM-DD HH:MM}
Turn: {turn-id}
Role: {writer|reviewer|approver}
Token: {session-token}
```

**Session token:** A short identifier written to `{doc-name}.status.md` at `init` (format: `sess_{YYYY-MM-DD}_{4-char-random}`, e.g. `sess_2026-06-04_a3f7`). Every lock file must include the token from the current session. At lock-check time, verify the token in the lock matches the token in status.md. A lock with a missing or mismatched token is treated as invalid (stale or forged) — remove it silently and proceed. This prevents fake lock files from other sessions or bad actors with folder access.

**`pickup` acquires the appropriate lock** after session discovery and identity confirmation — before reading the document or showing the briefing.

For Section Ownership writers: check only their section's lock (`.{doc-name}.§N.lock`). Other sections being locked by other writers is expected and fine — do not block.

For Section Ownership reviewers/approvers: check `.{doc-name}.review.lock`. If held, wait.

If the relevant lock already exists:
- Show: *"It looks like {Name} is currently working on this right now (started at {time}). Wait a moment and try again — it usually only takes a minute."*
- Do not proceed. Do not override.
- Exception: if the lock is older than 30 minutes, offer: *"This lock is over 30 minutes old — {Name} may have stepped away. Remove it and continue?"* Require confirmation before removing.

**`handoff` removes the lock** as its final step, after notifying the next person.

**`complete` removes all locks** matching `.{doc-name}.*.lock` and `.{doc-name}.status.lock` if any exist (cleanup).

**`pause` does not acquire or release the lock** — pausing mid-turn leaves the session unlocked.

**Status file lock (Section Ownership only):** Any operation that writes to `{doc-name}.status.md` must first acquire `.{doc-name}.status.lock`. Write the lock, make the update, then delete the lock.

**Retry strategy if lock already exists:**
- Wait 1s → retry
- Wait 2s → retry
- Wait 4s → retry
- If still locked after 3 retries: proceed with last-write-wins. Re-read status.md immediately after writing and verify your section row is correct and no other rows were dropped. If rows are missing, rewrite only the dropped rows (do not overwrite the full file). Append a note to the current log entry: `**Status conflict:** wrote under contention, re-verified post-write.`

This is best-effort — LLMs cannot enforce true atomicity. The exponential backoff handles bursts of parallel writers; the re-read catches overwrites that slip through.

---

## Schema & Consistency Rules

Every machine-read field must use exactly these values. No synonyms, no variations.

**Section status labels** — only these strings, exactly:
```
NOT STARTED | IN PROGRESS | DONE | REVIEWING | APPROVED | CLOSED
```

**Turn ID format** — only these patterns, exactly:
```
Turn {N}          ← non-Section Ownership modes
§{N}-T{N}         ← Section Ownership mode
```

**Timeline entry header** — exactly this pattern:
```
## {turn-id} — {Name} ({role}) — {YYYY-MM-DD HH:MM}
```

**Required timeline field** — every entry must have `**Changed:**` with non-empty content. All other fields are optional and omitted when empty (never written as blank).

**Role labels** — only: `writer` | `reviewer` | `approver`

**Storage backend labels** — only: `Google Drive` | `Local`

**Notification labels** — only: `Signal` | `Slack` | `Email` | `Signal+Email` | `Slack+Signal` | `Slack+Email` | `None`

**Session status** — only: `ACTIVE` | `CLOSED`

### Self-Validation After Every Write

After writing any structured file (`{doc-name}.log.md`, `{doc-name}.status.md`, `context-index.md`), re-read the written content and verify:

**After writing a timeline entry:**
- Header matches `## {turn-id} — {Name} ({role}) — {YYYY-MM-DD HH:MM}` format
- `**Changed:**` field is present and non-empty
- If feedback resolution was expected: at least one resolution line is present
- If reviewer feedback was left: at least one `- [ ] #` line is present

**After updating status file:**
- Turn counter incremented correctly
- Section status uses a canonical label
- Team table still intact (no rows dropped)
- `Log-checksum` updated to match the last timeline entry just written (see Log Integrity below)

**After writing context-index.md:**
- New entry has `**Summary:**` and `**Key facts:**` fields

If validation fails: show the written content to the user, explain what's wrong, and rewrite it before proceeding.

---

## Log Integrity

The log is append-only by convention, but nothing prevents direct edits. A lightweight checksum catches tampering.

**Checksum format:** `{entry-count}:{first-20-chars-of-last-header}` — e.g. `7:## Turn 7 — Alice (w`. Simple enough to compute by reading the log; specific enough to catch edits.

**Written:** After every `handoff` timeline write, update `Log-checksum` in status.md to reflect the new last entry.

**Checked:** At every `pickup`, before showing the briefing:
1. Read the last timeline entry header from the log
2. Count total timeline entries (`## Turn` + `### INIT` + `### PAUSE` + `### CONTEXT ADDED` + `### REOPEN` + `### MODE SWITCH` + `### REMOVE`)
3. Recompute checksum and compare to `Log-checksum` in status.md
4. **If mismatch:** *"Something looks off — the history may have been edited since the last turn. This could be accidental or a sync issue. I'll continue, but flag this: the log may not be reliable."* Log the mismatch in the current turn's timeline entry under `**Integrity flag:**`.
5. **If match:** proceed silently.

Do not block pickup on a mismatch — surface it and continue. The log is a record, not a gate.

---

## Error Recovery

### Operation File

`handoff` is a multi-step operation. If the session dies mid-way, the next `pickup` detects the incomplete state and offers recovery.

**Operation file location:**
- Non-Section Ownership: `.{doc-name}.op`
- Section Ownership — writers: `.{doc-name}.§{N}.op` (matches the section being handed off)
- Section Ownership — reviewers: `.{doc-name}.review.op`

**Written at the start of `handoff`**, before any other step:
```markdown
# Handoff in progress
Started: {YYYY-MM-DD HH:MM} by {Name}
Turn: {turn-id}

Steps:
- [ ] feedback_resolved
- [ ] draft_checked
- [ ] snapshot: {path}
- [ ] document_written
- [ ] timeline_written
- [ ] status_updated
- [ ] compressed
- [ ] lock_released
- [ ] notified
```

**Each step checks off its line** in the operation file as it completes (e.g. `- [ ] snapshot` → `- [x] snapshot: .versions/strategy-memo.v4.md`).

**Deleted on successful completion** of `handoff` (after lock released and notification sent).

### Recovery at `pickup`

After session discovery, before the lock check: look for op files.

- Non-Section Ownership: look for `.{doc-name}.op`
- Section Ownership: look for `.{doc-name}.§*.op` (any section) and `.{doc-name}.review.op`

If one or more op files are found, handle each one before proceeding. If multiple exist (rare — two writers crashed simultaneously), address them in section order.

Show this for each — no technical terms, no jargon:

> *"Hi! Before we start, something to sort out: it looks like {Name} was in the middle of passing the document to you, but something interrupted them — maybe their computer crashed or they lost connection. Their work is safe, but I need to tidy things up first.*
>
> *I have three options:*
> *1. Finish it for them — I'll complete what they started and you'll get their full update*
> *2. Undo it — go back to just before they started, as if their turn didn't happen*
> *3. Skip it — move on as-is (some notes from their turn may be missing)*
>
> *What would you like to do?"*

**If they choose "Finish it"** — resume from the first unchecked step. Never show step names to the user:
- Saving not done → save now silently
- Notes not recorded → ask: *"Do you know what {Name} changed? Even a rough summary helps — I'll record it."* If they don't know: *"No worries — I'll note that their turn was interrupted."*
- Status not updated → update silently
- Tidy-up not done → do silently
- Notification not sent → send now

**If they choose "Undo it"** — restore the snapshot if one was taken, clean up silently. Tell the user: *"Done — the document is back to just before {Name}'s turn. You can start fresh from here."*

**If they choose "Skip it"** — clean up silently, proceed with normal pickup. Tell the user: *"Okay, moving on. Just so you know, {Name}'s notes from that turn may not be recorded."*

### Other Recovery Scenarios

**Stuck from a previous session (stale lock, no interruption):**
> *"It looks like {Name} has this document open right now (they've had it since {time}). I'll wait until they're done — usually just a minute or two. Try again shortly."*
> If older than 30 minutes: *"{Name} has had this open since {time} — that seems like a long time. Did they step away? I can clear it if you're sure they're not mid-save."*

**Something looks wrong with the document history:**
> *"I noticed a saved version of the document that doesn't have any notes attached to it. Want to add a quick note about what changed? It helps everyone understand the history."*

**The session file is missing or damaged:**
> *"I can't find the session information for this document. I can try to rebuild it from the history — it'll take a moment. Want me to try?"*
> If yes: read all timeline entries, reconstruct team, turn count, and section statuses silently, then proceed.

---

## Turn Numbering

**All modes except Section Ownership:** Global sequential — Turn 1, Turn 2, Turn 3...

**Section Ownership:** Section-scoped — `§1-T1`, `§2-T1` etc. Each section has its own counter. Two people can work simultaneously without conflict.

---

## Timeline Entry Format

Appended to `{doc-name}.log.md` at every `handoff`. Never edited. Internal — users never write this directly.

```markdown
## {turn-id} — {Name} ({role}) — {YYYY-MM-DD HH:MM}

**Section(s):** {section name or "full doc"}
**Changed:** {required}
**Tried and dropped:** {omit if nothing}
**Assumptions baked in:** {omit if nothing}
**For next person:** {omit if nothing}

**Feedback resolution** (if feedback was open):
- ✅ #{n} {summary} — done: {how}
- ⏳ #{n} {summary} — not yet: {reason}, revisit by {turn/date}
- ⛔ #{n} {summary} — skipping: {reason}
- ⚠️ #{n} {summary} — DISPUTED: reviewer disagrees, escalated to approver

**Reviewer feedback** (if this turn was a review):
- [ ] #{n} {feedback item}
```

---

## Feedback Tracking

**When a reviewer finishes their turn:** their feedback items are saved as a numbered list.

**When the writer runs `handoff` with open feedback:**
1. Show all open items as a numbered list first so the writer can see the full scope
2. Ask: *"Want to go through these one by one, or handle several at once?"*
   - **One by one:** ask each item individually — *"Did you handle this, skip it, or come back later?"*
   - **Batch:** writer can say *"I fixed 1–4, skipping 5–7 (same reason: out of scope), not yet on 8"* — parse and record each accordingly
3. For each item, record one of:
   - **Done** — handled, explain briefly how
   - **Not yet** — give a reason and when you'll get to it
   - **Skipping** — give a reason (disagree, out of scope, your call as the author)
4. Don't allow handoff until every item has an answer

**When the reviewer runs `pickup`:**
1. Show how each of their items was handled:
   - ✅ done — how it was addressed
   - ⏳ not yet — reason + when
   - ⛔ skipping — reason
2. If the reviewer disagrees with a "skipping" decision:
   - They can flag it as **DISPUTED**
   - This appears in `status` and the approver is notified to resolve it
   - Once the approver resolves a dispute (either direction), it is **final** — the reviewer cannot re-open it. If the reviewer still disagrees after the approver's decision, they may note their disagreement in the log, but the item stays resolved. The approver's word closes the loop.

---

## User Identification

At `pickup` and `handoff`, if the user hasn't identified themselves in this conversation:
→ Ask: *"What's your name?"* — match against the team list in `{doc-name}.status.md`

If no match: ask to confirm or add them as a writer.

---

## Session Discovery

At `pickup`:
1. Check if a `*.status.md` exists in the current directory
   - One found → *"I found a document called {doc title} here — is that the one you want to work on?"*
   - Multiple found → *"I found a few documents here — which one is yours?"* List titles (not filenames)
   - None found → *"I need to find your document. If you got a notification with a link or location, paste it here."*

2. If the user pastes a file path: accept silently, don't explain what a path is.
   If the user pastes a Drive link: use Drive MCP to read it.
   If unrecognizable: *"That doesn't quite look right — try copying it again from the message you received."*
   If the user says they don't have the path / deleted the notification: *"No problem — do you remember roughly what the document was called? I can search for it."* If they give a title, scan for `*.status.md` files whose doc title matches. If found: confirm with them. If not found: *"I can't find it automatically. Ask {whoever set this up} to resend the location — it only takes a second."*

3. Read `{doc-name}.status.md`. If missing: *"I couldn't find the document there. Double-check the link from your notification, or ask whoever set this up to resend it."*

---

## Diff Strategy

No text diff tool available. Use section-by-section structural comparison:

1. Read current doc — extract top-level headers + first sentence of each section
2. Find the person's last version snapshot in `.versions/` (the most recent version from before their last turn). **If no prior snapshot exists for this person** (first time they're seeing this document), skip the diff entirely and say: *"This is the first time you're seeing this document — I'll walk you through what's here."* Then present the document structure in plain language.
3. For each section:
   - New → **added**
   - Changed → **updated** + one-sentence summary (compare word count + first/last sentence)
   - Gone → **removed**
   - Same → skip

Output in plain language:
```
What changed since you were last here:
  §2 Complication  — updated (argument reframed around cost, not risk)
  §3 Resolution    — updated (new timeline sub-section added)
  §4 Appendix      — added
```

---

## Context Compression

**Log:** When `{doc-name}.log.md` exceeds 10 entries:
1. Summarize older entries into `{doc-name}.digest.md` — silently, no confirmation required
2. Keep last 3 entries verbatim in the log
3. At the start of the next briefing (not mid-pickup), show a one-line note: *"I've summarized older history into a digest — everything is preserved in `{doc-name}.digest.md`."*

Compression is silent because it is non-destructive (full log still exists in the archive) and blocking the briefing for confirmation creates unnecessary friction.

Digest format:
```markdown
# {doc title} — History Summary (up to {turn-id})
**Contributors so far:** {list}
**Key decisions:** {bullets}
**Sections completed:** {list}
**Things tried and dropped:** {bullets}
**Feedback still open:** {list with expected resolution turns}
**Disputed items:** {list if any}
```

**Context index:** When `context-index.md` exceeds 15 entries:
1. Summarize older entries into `context-digest.md` — silently, no confirmation required
2. Keep last 5 entries in `context-index.md`

---

## Command Workflows

### `init`

One question at a time. Warm, conversational tone.

**Before Q1 — silent capability check.** Scan available tools and surface what will and won't work, once, up front:

- **Google Drive:** look for any tool matching `mcp__*__read_file_content` whose server mentions Drive/gdrive
- **Signal:** check for `mcp__signal__send_message`
- **Slack:** check for any tool matching `mcp__slack__*`
- **Email:** check for `mcp__proton-mail-bridge__send_email`

If anything is missing, show this before asking Q1 (skip entirely if everything is available):

```
Before we set things up — here's what's available on your system:
  Storage:       Local ✓   Google Drive ✗
  Notifications: Signal ✓  Slack ✗  Email ✗

You can still run a full session with what's connected. I'll only ask about what works.
```

Do not block on missing tools — just inform. Then continue.

```
Q1: What's this document about? Give it a title.

Q2: What kind of document is it?
    → decision / report / analysis / strategy / something else

Q3: Do you have a structure in mind, or want me to suggest one?
    [If suggest: show templates, let them pick]

Q4: Who else is working on this with you?
    → Names please. I'll ask how to reach each person.
    [Per person]: How do I reach {Name}?
    → Only offer backends confirmed available in the capability check (e.g. if only Signal is available, only ask for Signal number — don't ask for Slack handle or email)
    → Options shown: [available backends] / no notifications for them
    [If all contacts collected and all have a notification method: skip Q8]
    [If any person has no contact or the user said "I'll do it myself": proceed to Q8]

Q5: What's each person's role — writer, reviewer, or approver?
    [If 2 people, no roles given: both writers, Ping-Pong]

Q6: Where should the document live?
    → Google Drive link or folder path on your computer

Q7: Any background files to add now?
    → Reports, data, emails, notes — paste a path or link
    [If none: skip]

Q8: How should I send turn notifications? (only ask if not resolved in Q4)
    → Signal / Slack / email / combination / I'll do it myself
```

Before creating any files, verify notification backends are available:
- If Signal selected for any person: check that `mcp__signal__send_message` is listed as an available tool. If not: *"Signal notifications won't work — the Signal MCP server isn't running. You can set it up at https://github.com/googlarz/signal-mcp, or I can notify {Name} via a different method. What would you prefer?"* Do not proceed until resolved.
- If Slack selected for any person: check that a tool matching `mcp__slack__send_message` (or discovered Slack MCP prefix) is available. If not: *"Slack notifications won't work — the Slack MCP server isn't connected. You can set it up at https://github.com/modelcontextprotocol/servers/tree/main/src/slack, or use a different method for {Name}."* Do not proceed until resolved.
- If Email selected: check that `mcp__proton-mail-bridge__send_email` is available. If not: *"Email notifications won't work — the Proton Mail MCP isn't running. Switch to Signal or Slack for {Name}, or I'll remind you to notify them manually each time."* Do not proceed until resolved.
- If "I'll do it myself": no check needed. At every handoff, show the user the full notification message to send manually.

After answers:
- Auto-detect mode, confirm: *"Based on what you've told me, I'll set this up as [mode]. Sound right?"*
- Create `{doc-name}.status.md`, `{doc-name}.log.md`, and `.{doc-name}.contacts`

**Contacts file** — written at `init`, read at every notification step. Contains actual contact details (numbers, handles) separated from the status file so team members know what's PII:
```
# {doc title} — contacts
# ⚠ Contains personal contact details. Share this folder only with the team.

{Name}: Signal +{number}
{Name}: Slack @{handle}
{Name}: Email {address}
{Name}: manual (no notifications)
```
- If Section Ownership: *"What are the section names?"* → scaffold `.sections/` with chosen template. Create each section file: `.sections/{N}-{section-name}.md` containing `# §{N} {Section Name}\n\n[{Writer name} to write]`. Then confirm that every template section has an assigned writer — *"These sections don't have a writer yet: {list}. Want to assign them now, or leave them for later?"* Do not proceed until all sections are assigned or explicitly deferred.
- Ingest source files via `add-context`
- Notify team (with fallback):

```
[Co-Write] {doc title} — you've been added

Hi {Name},

{Initiator} has started a document project and added you as a {role}.

When it's your turn, I'll message you. To jump in now:

1. Open Claude
2. Type: "I want to work on {doc title}"
3. When asked, paste this:
   → {path or Drive link}

That's it!
```

**Status file** (machine-written):
```markdown
<!-- Machine-written by co-write. Do not edit manually. -->

# Co-Write: {title}
- **Storage:** {backend} — {path}
- **Mode:** {mode}
- **Structure:** {template}
- **Notifications:** {method}
- **Started:** {date}
- **Status:** ACTIVE
- **Token:** {session-token}
- **Log-checksum:** {last-entry-checksum}

## Team
| Name | Role | Notify via |
|------|------|-----------|
| {Name} | {role} | {method} |

<!-- Include the Sections block only when mode is Section Ownership: -->
## Sections
| Section | Writer | Turn | Status |
|---------|--------|------|--------|
| §1 {name} | {Name} | §1-T0 | NOT STARTED |
<!-- End Section Ownership block -->

## Turn Counter (non-Section Ownership)
Current turn: {N}

## Disputed Items
{empty}
```

---

### `pickup`

1. **Session discovery** — check current dir first, then ask (see Session Discovery)
2. **User identification** — confirm who's picking up. Match against the team list in `{doc-name}.status.md`. If no match: *"I don't see a {Name} on the team list. Are you sure you've got the right document, or did someone add you recently?"* Do not proceed until name matches.
3. **Role and section check:**

   - **Approver:** Do not enter the normal pickup flow. Instead: *"Hi {Name} — as approver, your job is to give the final sign-off once everything is reviewed and merged. Right now, {status summary}. Would you like to see the current state of the document, or do you want to wait until it's ready for approval?"* If they want to see the doc: show it with a brief summary. If the document is merged and reviewed, walk them through `approve`. Do not acquire a lock unless they're actively approving.

   - **Dual-role (writer + reviewer on same session):** Ask explicitly: *"Are you here to work on your section, or to review the others?"* Route accordingly. If writing: continue as writer for their section. If reviewing: continue as reviewer.

   - **Writer (Section Ownership):** Confirm the person's assigned section from the status file. If they name a section that belongs to someone else: *"That section is {Other person}'s — I can't open it for you. Do you have a different section, or did something change with the assignments?"* If they have no assigned section: *"You're on the team but don't have a section assigned yet. Check with whoever set this up — they can assign you one."* Do not proceed until they have an authorized section.

   - **Reviewer (Section Ownership):** After acquiring the review lock, update all sections currently marked DONE to REVIEWING in the status file (using the status file lock). This signals to other writers that review is in progress. When the reviewer hands off, sections they reviewed move back to DONE (or remain REVIEWING if the writer hasn't resolved feedback yet — the writer's T2 handoff sets them back to DONE).

4. **Recovery check** — look for op files (see Error Recovery). If found, follow recovery flow before continuing.
5. **Lock check** — check for the appropriate lock file (see Lock File). If locked by someone with the same name as the current user: *"It looks like you were already working on this — did your last session get interrupted? The lock from {time} is still here."* Offer to clear it after confirmation. If locked by a different person, block. If clear, write the lock file. Then immediately re-read and verify it contains the correct name.
6. **First-time check** — if this person has no previous turns in the log, show onboarding:

   > *"Welcome to the {doc title} session! Here's how this works: you'll work with me on the document, then pass it to the next person when you're done. I'll keep track of everything — what changed, why, and what each person was asked to focus on. Ready to dive in?"*

7. **Check for paused draft** — if `.drafts/{doc-name}.{name}.draft.md` exists:
   *"You left off mid-turn on {date} at {time}. Want to pick up where you left off, or start fresh?"*
   - If "pick up where I left off": load draft content as the working document. Delete the draft file.
   - If "start fresh": delete the draft file silently. Work from the current document state.

8. **Load session data — read in this order, stop early if something needs attention:**
   - Read `{doc-name}.status.md` (always required — roles, sections, turn counter)
   - Read `{doc-name}.digest.md` if it exists (replaces older log entries)
   - Read last 3 entries of `{doc-name}.log.md`
   - Apply compression if log exceeds 10 entries — but do this **after** showing the briefing, not before. Compression requires user confirmation and should not delay the briefing.
   - Read current document (`{doc-name}.md` or the person's section file)
   - Read `context-digest.md` then `context-index.md` **only if** the briefing references context, or the person asks about source material. Defer this — most turns don't need full context at pickup.
   
   **For Google Drive sessions:** issue reads in parallel where the backend allows — status + digest + log in one batch, not sequential round-trips.

9. **Log integrity check** — count `## Turn` and `### INIT` entries in the log. Compare to turn counter in status file. If they don't match: *"Something looks off with the history — the document shows {N} turns but the log has {M} entries. I'll keep going, but you may want to let {whoever set this up} know."* Do not block pickup, but always surface the mismatch.

10. If reviewer with previous feedback: show resolution status in plain language

11. Show diff in plain language (see Diff Strategy)

12. **Briefing — conversational, not a dashboard.**

Use the right version based on role:

**Writer (sequential or section owner returning):**
```
Hi {Name} 👋
{Previous name} just finished their part. Here's where things stand:

They {summary of what changed — in plain English, 2-3 sentences}.

{If "for next person" exists}: They'd like you to {focus request}.

{If context updated}: A new file was added since you were last here: {filename}. I'll use it as we work.

{If writer seeing open feedback from reviewer}:
{Reviewer} left {N} comment(s) for you to look at. You'll go through them when you hand back — no action needed yet.
• "{feedback #1 summary}"
• "{feedback #2 summary}"

Ready to start? Tell me what you want to do, or I'll guide you through it.
```

**Reviewer/approver (Section Ownership — reviewing multiple sections):**
```
Hi {Name} 👋
Here's where everything stands across the document:

{List each section that has new content since your last review:}
• §{N} {name} — written by {Name}: {one-sentence summary}
• §{N} {name} — written by {Name}: {one-sentence summary}

{If any section is still in progress}: §{N} isn't finished yet — you can review what's there or wait for it.

{If you've reviewed before and there's resolved feedback to show}:
Here's what happened with your earlier comments:
• "{feedback #1}" — {done/not yet/skipped}: {reason}
{If any skipped items you disagree with}: Want to flag any of these as disputed? I'll escalate to {approver name}.

Ready to start? Tell me which section you'd like to look at first, or I'll start from the top.
```

**Reviewer (sequential mode — Structured Critique):**
```
Hi {Name} 👋
{Writer} just finished their part. Here's what they changed:

They {summary in plain English, 2-3 sentences}.

{If "for next person" exists}: They'd like you to focus on: {focus request}.

{If resolved feedback to show}:
Here's what happened with your earlier comments:
• "{feedback #1}" — {done/not yet/skipped}: {reason}
{If any disputed}: Want to flag any of these as disputed? I'll escalate to {approver name}.

Ready to review? I'll walk you through it.
```

13. Begin working. Ask questions before writing anything substantial. Follow mode behavior below.

---

### Mode Behaviors (during active turn)

**Ping-Pong (writer):**
- *"What's the goal of your turn — writing something new, revising, or responding to feedback?"*
- New doc: walk through structure template section by section. For each: *"What's the main point of this section?"* before writing
- Reference context when relevant facts are needed

**Structured Critique (reviewer):**
- Read the full document
- Apply: Logic | Evidence | Main point clear? | Well structured? | Easy to read?
- For each issue: write a plain-language comment with the location and what to improve
- Don't rewrite — explain what's unclear and why
- *"Anything else you want to flag?"*

**Structured Critique (writer resolving review):**
- Go through each comment one at a time in plain language
- Help address it or capture the done/not yet/skipping response

**Section Ownership (writer):**
- Stay within the assigned section(s) only
- At handoff: note any cross-section issues (terminology, flow) for the merge step
- **Cross-section communication:** There is no direct writer-to-writer channel in parallel mode. If a writer needs to flag something for a peer (e.g. a financial figure that affects the executive summary), they have two options: (1) leave a note in their handoff "For next person" field — the reviewer will see it and can relay it; (2) use `status` to append a note to the log that all participants can read at their next pickup. Do not attempt to edit another writer's section.

**Section Ownership (reviewer):**
- Review all sections marked DONE in the status file, one at a time
- Before showing each section: *"Let's look at §{N} — {name}. Tell me what you think, and I'll help turn it into specific feedback for {writer}."*
- After reading their reaction (even vague: "this is confusing", "seems fine", "I don't understand it"): ask one follow-up to locate the issue: *"Which part specifically — is it the opening, a particular point, or the overall structure?"*
- Translate their response into a concrete, located comment before recording it
- At handoff: check that all DONE sections have been reviewed. If any were skipped: *"You haven't looked at §{N} yet — want to review it now, or skip it this time?"* Do not allow handoff until the reviewer explicitly confirms they're done with all sections or consciously skips one.
- Route feedback to section owners — each writer only receives items tagged to their section.

**Challenger/Defender:**
- Positions are assigned at `init` — ask: *"Who is defending the proposal, and who is challenging it?"* Store in status file as `writer (Defender)` and `writer (Challenger)`.
- At `pickup`, greet with: *"You're arguing the [Defender/Challenger] position this turn."*
- Build the strongest version of their assigned position — do not hedge or present the other side.
- If this is Turn 2+, reference the opposing argument from the previous turn: *"Last turn, [Name] argued… your response should address that directly."*
- Turn structure: Defender argues first (Turn 1) → Challenger responds (Turn 2) → Defender rebuts (Turn 3, optional) → approver decides (final turn). Approver reads both positions and records their decision as a Recommendation section update.
- If both writers converge before the approver turn, either can note it at handoff: *"We've reached agreement — see Recommendation."* Approver still confirms.

**Annotation Loop:**
- Load the draft. The reviewer goes first — the document already exists.
- *"Which part do you want to look at first?"* — guide them section by section.
- Help write clear, specific comments: push vague feedback ("this feels weak") to actionable feedback ("this claim needs a source" or "reorder: put the conclusion first").
- Inline annotation format: `> **[{ReviewerName}]:** {comment}` inserted directly after the relevant paragraph in the document.
- At handoff: compile all inline annotations into numbered feedback items in the standard format:
  ```
  **Reviewer feedback:**
  - [ ] #1 {plain-English summary of the annotation}
  - [ ] #2 ...
  ```
  Then remove the inline annotations from the document body (feedback is now in the log).
- Turn structure: reviewer annotates (Turn 1) → writer revises (Turn 2, resolves each item) → repeat if needed.

**Round Robin:**
- Used after all sections are written. Each person reviews every section they didn't write.
- At pickup (reviewer): *"You're reviewing {N} sections this turn — §{X}, §{Y}, §{Z}. Want to go through them one at a time?"* Present sections in order. For each: *"Let's look at §{N} — {name}, written by {writer}. What's your read?"* Push vague reactions to specific, located feedback the same way as Annotation Loop.
- At handoff (reviewer): compile all feedback into per-section bundles. Route each bundle only to the section's writer — writers never see feedback on sections they didn't write. Log the routing.
- At pickup (writer resolving Round Robin feedback): briefing shows only their own sections' feedback. Walk through each item: done / not yet / skipping. Same resolution flow as Structured Critique.
- At handoff (writer after resolving): notify the approver once all writers have resolved their feedback. Check the status file — if other writers still have open items, hold the approver notification and tell the current user: *"Done — I've saved your resolutions. I'll notify {approver} once everyone has responded."*
- Turn structure: all sections written (Section Ownership turns) → Round Robin review turn (all reviewers simultaneously, Section Ownership scoped) → each writer resolves their own feedback → approver signs off.
- If a reviewer is also a writer (dual role): they skip reviewing their own sections, review all others.

---

### `handoff`

1. **Check for open feedback** — if unresolved, go through each item one at a time (done / not yet / skipping). Block until all have answers. Mark `feedback_resolved` in op file.

2. **Write operation file** — create the appropriate op file now, before any writes (see Error Recovery): `.{doc-name}.op` for non-Section Ownership, `.{doc-name}.§{N}.op` for section writers, `.{doc-name}.review.op` for reviewers. Mark `feedback_resolved` as `[x]`. All remaining steps start as `[ ]`.

3. **Check for paused draft** — if one exists, show save date/time: *"You saved a draft on {date} at {time}. Use it as the final version, or keep what we just worked on?"* Mark `draft_checked` in op file.

4. **Collect timeline fields — keep it light:**
   - *"In a sentence or two, what did you change?"* — required. Target: 1–3 sentences, under 60 words. If the answer is fewer than 10 words, prompt once for more. If the answer exceeds 60 words, extract the core 1–3 sentence summary and confirm: *"I'll save this as your summary: '{condensed version}' — OK?"* Offer to save the longer version in the 'things tried' field instead.
   - *"Anything you tried that didn't work, or want the next person to know?"* — single optional prompt. Longer explanations are fine here.

5. **Content quality check** — before snapshotting, read the section/document being handed off. If it contains only placeholder text (patterns: `[... to write]`, `[TBD]`, `[placeholder]`, fewer than 20 words of actual content): *"It looks like this section is mostly empty — just a placeholder. Is that what you meant to hand off, or did something go wrong?"* Require explicit confirmation before proceeding with an empty handoff.

6. **Snapshot** — copy doc to `.versions/{doc-name}.v{N}.md` (non-Section Ownership) or `.versions/{doc-name}.§{N}.v{T}.md` (Section Ownership, where N = section number, T = turn number for that section). Validate the file was written. Mark `snapshot: {path}` in op file.

7. **Write document** — save to `{doc-name}.md` or relevant `.sections/` file. Validate file is non-empty. Mark `document_written` in op file.

8. **Write timeline entry** — append to log using exact schema (see Schema & Consistency Rules). Re-read and self-validate (see Self-Validation). Mark `timeline_written` in op file.

9. **Update status** — re-read `{doc-name}.status.md` fresh before writing (in Section Ownership, another writer may have updated it since you started). For Section Ownership writers: update only your own section row and the log's last-activity field — do not overwrite the full file. Re-read after writing and verify your section row is correct and no other rows changed. Mark `status_updated` in op file.

10. **Apply log compression** if log exceeds 10 entries — silently, no user confirmation. Mark `compressed` in op file.

11. **Release lock** — delete the appropriate lock file (`.{doc-name}.lock`, `.{doc-name}.§{N}.lock`, or `.{doc-name}.review.lock`). Mark `lock_released` in op file.

12. **Notify next person** — plain English, with fallback. Mark `notified` in op file.

For Section Ownership writers: notify the reviewer only when all sections are DONE (check the status file). If other sections are still IN PROGRESS, do not notify the reviewer yet — just update your section status silently and tell the current user: *"Done — I've saved your section. I'll notify {reviewer} once all sections are finished."* If all sections are now DONE, notify the reviewer.

13. **Delete operation file.** Handoff complete.

Notification message (plain English, numbered steps so non-tech users know exactly what to do):

```
[Co-Write] {doc title} — your turn!

Hi {Name},

{Previous name} has finished their part — it's over to you now.

{If focus exists}: They'd like you to focus on: {focus in plain English}.
{If feedback}: They've also left {N} comment(s) for you to look at.

Here's how to start:
1. Open Claude
2. Type: "I want to work on {doc title}"
   (copy that exactly — it's the document name)
3. When asked where the document is, paste this:
   → {path or Drive link}

Takes about 30 seconds to get going! If you have any trouble, just reply to this message.
```

---

### `pause`

1. *"Want me to save what we've worked on so you can come back to it?"*
2. Save to `.drafts/{doc-name}.{name}.draft.md` with a timestamp header:
   ```
   <!-- Paused: {YYYY-MM-DD HH:MM} by {Name} -->
   {draft content}
   ```
3. Append to log:
   ```markdown
   ### PAUSE — {Name} — {date} {time}
   In-progress draft saved. Turn not yet complete.
   ```
4. Do not snapshot, notify, or increment turn count.
5. *"Saved. When you're back, just say 'I want to continue {doc title}' and I'll pick up where we left off."*

---

### `add-context`

1. *"What would you like to add? You can paste a file path, a Drive link, or just paste the text directly."*
2. Read content:
   - PDF (local file): try `mcp__plugin_pdf-viewer_pdf__display_pdf` to open, then `mcp__plugin_pdf-viewer_pdf__interact` with `action: get_text` to extract content. If the viewer fails to mount, fall back: *"I couldn't open that PDF automatically. Can you paste the key sections you'd like me to use as context?"*
   - Drive file: use discovered Drive MCP prefix + `read_file_content` or `download_file_content`
   - Local file: native `Read`
   - Pasted text: use directly
3. Append to `context-index.md`:
   ```markdown
   ## {filename} — added by {Name} on {date}
   **Type:** {PDF / spreadsheet / email / note / other}
   **Summary:** {2-3 sentences}
   **Key facts:** {bullet list}
   ```
4. Save original to `.context/{filename}` if it's a file
5. Apply context index compression if entries exceed 15 (confirm with user)
6. Append to log:
   ```markdown
   ### CONTEXT ADDED — {Name} — {date}
   Added: {filename} ({type})
   ```
7. Re-read updated index immediately. Confirm: *"Got it — I've read through {filename} and will use it as we work."*

---

### `assign`

Section Ownership mode only.

1. Show current sections and who's assigned from `{doc-name}.status.md`
2. Ask who writes each unassigned section, OR ask if an existing assignment should change: *"Do you want to add assignments, or move a section from one person to another?"*
3. **Reassignment:** If moving §{N} from {OldWriter} to {NewWriter}:
   - Check if {OldWriter} has a lock on this section — if so, warn: *"{OldWriter} is currently working on §{N}. Are you sure you want to reassign it?"*
   - Check if {OldWriter} has started writing (section file non-empty beyond placeholder) — if so, warn: *"{OldWriter} has already started §{N}. Their draft will stay — {NewWriter} will pick up from there."*
   - Log the reassignment with reason
   - Notify both: old writer (*"§{N} has been reassigned to {NewWriter} — you're off the hook for that section"*) and new writer (standard assignment notification)
4. Update `{doc-name}.status.md` using the status file lock (see below)
5. Notify newly assigned writers (with fallback):
```
[Co-Write] {doc title} — you've got a section to write

Hi {Name},

You're working on: {section name}

When it's your turn I'll message you. To start now:
1. Open Claude
2. Type: "I want to work on {doc title}"
3. When asked, paste this:
   → {path or Drive link}
```

---

### `status`

Read `{doc-name}.status.md`, check for active lock files (`.{doc-name}.§*.lock`, `.{doc-name}.review.lock`), and read last 3 log entries. Show in plain language:

```
📄 {doc title}

WHO'S DOING WHAT:
  §1 {name}   → {Name}   [✏️ writing now]          ← lock file exists
  §2 {name}   → {Name}   [✅ done]
  §3 {name}   → {Name}   [⏳ not started — 3 days]  ← NOT STARTED + days since notification
  §4 {name}   → {Name}   [⚠️ overdue — 5 days]      ← NOT STARTED > 4 days = overdue

WAITING ON:
  {Reviewer} hasn't reviewed §2 yet ({Name} finished on {date})

COMMENTS NEEDING ATTENTION:
  {Name} left 2 comments on §2 — {Owner} hasn't responded yet

DISPUTED:
  §2 comment #3 — {Owner} said skipping, {Reviewer} disagrees — {Approver} to decide

RECENT ACTIVITY:
  {Name} — {date} — {one-line summary}

OPTIONS: switch mode · add someone · reassign a section · send reminder
```

**Overdue threshold:** a section is ⚠️ overdue if NOT STARTED more than 4 days after the session was created (or after the last notification was sent to that writer).

**"send reminder" option:** if selected, prompt *"Who do you want to nudge? I'll send them a quick note."* Send via notification backend with: *"Hi {Name} — just a heads up that your section ({section name}) for {doc title} is still waiting. No rush, but the team is ready when you are. To pick up: [standard instructions]."*

If user selects "switch mode": ask which, confirm, update status file, log the change using this format:
```markdown
### MODE SWITCH — {Name} — {YYYY-MM-DD HH:MM}
**From:** {old mode}
**To:** {new mode}
**Role changes:** {e.g. "Tom changed from writer to reviewer"} (omit if none)
**Note:** {any structural implications — e.g. "sections defined below" if switching to Section Ownership}
```
If switching **to Section Ownership**: ask for section names and scaffold `.sections/` files (same as `init`). Update status file with section table.
If switching **from Section Ownership**: remove section table from status, reset turn counter to global sequential (starting from the next turn number).
If user selects "reassign a section": see `assign` command — supports reassignment from one writer to another.

---

### `merge`

1. Load sections and statuses from status file
2. Warn about any section not marked done or approved — *"§3 isn't finished yet. Merge anyway or wait?"*
3. **Extract key terms from each section** — 8-10 important nouns/concepts per section
4. **Cross-check terminology** — flag where the same thing is called different things across sections (e.g. "users" vs "customers") as specific named conflicts
5. **Check argument flow** — does each section set up the next? Flag gaps by name
6. **Check transitions** — flag mismatched endings/openings between sections
7. Present issues as a numbered list: *"Before I combine everything, I noticed a few things:"*
8. *"Want to fix any of these now, or should I merge and let the approver handle them?"*
9. Concatenate sections into `{doc-name}.md`, snapshot to `.versions/{doc-name}.merged.v{N}.md`, log the merge, notify approver

---

### `approve`

**Who can approve:** The designated approver from the team list. In Ping-Pong mode with no designated approver, either writer may approve — the person who runs `approve` is recorded as approver of record.

1. *"Are you approving one section or the whole document?"*
2. Show the content
3. **Completeness check** — scan for placeholder text (`[not yet written]`, `[to be added]`, `[TBD]`, empty sections with only a heading). If found: *"Looks like {section} hasn't been filled in yet — approve anyway or sort that out first?"* Require explicit confirmation before approving a document with empty sections.
4. *"Any final tweaks?"*
5. **Edit size check** — if the edit changes more than one paragraph or adds/removes a section header:
   *"That's a fairly substantial change. Should I send this back to {writer} to handle, or do you want to make the call as approver?"*
   Log which was chosen.
6. Apply edits, snapshot, update status, log approval
7. If full doc: notify everyone, suggest `complete`

---

### `complete`

Normally requires the document to be approved. If the approver is unavailable or approval isn't needed, an escape hatch is available — see step 1.

1. Verify `{doc-name}.md` exists in the session folder. In Section Ownership mode, this requires `merge` to have been run first. If missing: *"The final merged document isn't here yet. Run merge first to combine the sections, then you can archive."*

   **Approval check:** If the document is not yet approved, surface this:
   *"This document hasn't been formally approved yet. You can:*
   *1. Wait for {approver name} to approve it first (recommended)*
   *2. Archive without approval — I'll note it wasn't formally signed off"*
   If they choose option 2: proceed, but record `Approved by: none (archived without approval)` in the summary.

2. *"Ready to wrap this up and archive everything? The final document will stay where it is — everything else gets tucked away."*
3. Write `{doc-name}.archive-summary.md` in the session root **before** moving anything — this file stays in root alongside the final document:
   ```markdown
   # {doc title} — Completed {date}
   - **Team:** {list}
   - **Turns:** {N}
   - **Mode:** {mode}
   - **Approved by:** {Name} on {date}  ← or "none (archived without approval)"
   - **Archive:** .archive/{doc-name}/
   ```
4. Create `.archive/{doc-name}/`
5. Remove all lock files matching `.{doc-name}.*.lock` and `.{doc-name}.lock` if any exist (cleanup)
6. Move to archive: log, digest, status, contacts, sections, context, versions, drafts
7. Leave `{doc-name}.md` and `{doc-name}.archive-summary.md` in root
8. Notify everyone:
```
[Co-Write] {doc title} — done!

{Name} has given the final sign-off. The document is complete.

You can find the finished document here:
→ {path or Drive link}
```

---

### `export`

Available at any time during an active session, or after `complete`. Works on the current document state.

1. Read the current `{doc-name}.md`. In Section Ownership mode, if sections haven't been merged yet: *"The sections aren't merged yet — the export will include each section as a separate part. Want to merge first for a cleaner result, or export as-is?"*

2. *"Export as PDF, Markdown, or both?"*

3. **Markdown export:**
   - Write a clean copy to `{doc-name}-export.md` in the session folder (same location as the doc)
   - Add a title block at the top:
     ```markdown
     # {doc title}
     {Team: Name (role), Name (role), ...}
     {Exported: YYYY-MM-DD}
     ---
     ```
   - Strip internal metadata comments (`<!-- ... -->`) and placeholder markers (`[to be written]`, `[TBD]`)
   - Preserve all headings, body text, and tables

4. **PDF export:**
   - Try: `pandoc "{doc-name}-export.md" -o "{doc-name}.pdf"` via Bash
   - If pandoc succeeds: *"PDF saved to {path}."*
   - If pandoc is not installed: *"pandoc isn't installed — I can't generate a PDF directly. The Markdown file is ready at {path}. You can convert it at [pandoc.org/try](https://pandoc.org/try), paste into Google Docs and download as PDF, or install pandoc with `brew install pandoc`."*

5. Confirm what was saved:
   *"Done — exported to {path(s)}."*

---

### `list`

Search strategy depends on what's known:

**Local sessions:**
1. Scan current directory for `*.status.md` files
2. Check any folder paths used earlier in this session

**Google Drive sessions:**
- If the user has previously used a Drive folder in this session, use discovered Drive MCP prefix + `search_files` with query `name contains ".status.md"` to find sessions in Drive
- If no Drive folder is known: ask *"Are your documents on Google Drive? If so, paste the Drive folder link and I'll search there."*

**Combine results from both sources**, deduplicate, then show in plain language:
```
Here are the co-write sessions I found:

1. Strategy Memo
   You're a writer · Alice last worked on it 2 days ago
   Location: Google Drive — drive.google.com/...

2. Product Decision
   You're a reviewer · Waiting on you since yesterday
   Location: ~/shared/product-decision/

Which one do you want to open?
```

If none found anywhere: *"I didn't find any active sessions. Want to start a new one, or is it saved somewhere specific?"*

---

### `inbox`

Shows all collaborate sessions across known locations where it's currently the user's turn or where their input is needed.

1. **Identify the user** — ask for their name if not known in this conversation
2. **Scan known locations:**
   - Current directory
   - Any paths used in this session
   - Any paths recorded in `~/.collaborate-locations` if it exists (a plain text file, one path per line, maintained automatically — see below)
   - Google Drive sessions: if a Drive MCP is available, search for `*.status.md` files
3. **For each session found**, read its status.md and check:
   - Is this person's turn active (their name matches the current turn holder or an open section)?
   - Is there open reviewer feedback addressed to them?
   - Are they the approver and the document is awaiting approval?
4. **Show only sessions needing their attention:**
```
📬 Your inbox — {Name}

  1. Barcelona Trip                  — your turn to write (§2 Daily Plan)
     ~/iCloud Drive/Shared/Barcelona/

  2. Q3 Strategy Memo                — reviewer feedback waiting for you (3 items)
     ~/Shared/Strategy/

  3. Hiring Policy                   — awaiting your approval
     ~/Docs/HR/

Nothing else needs you right now.
```
5. *"Which one do you want to open?"* — route to `pickup` for whichever they choose

**Maintaining `~/.collaborate-locations`:** After every `init` (new session created) and every `pickup` (session opened from a path), append that path to `~/.collaborate-locations` if it's not already there. This builds the inbox scan list automatically over time without requiring the user to configure anything.

---

### `rollback`

1. List versions with plain-language summaries. For Section Ownership mode, ask if they want to roll back a specific section or all sections:
```
Here are the saved versions:

v1 — May 10, Alice — "First draft of the structure and opening section"
v2 — May 11, Bob   — "Complication section written"
v3 — May 12, Alice — "Conclusion added"

Which version do you want to go back to?
```
For Section Ownership, list per-section versions:
```
Versions for §5 Strategic Options:
  §5-v1 — May 10, Dana — "Full options analysis, Option A recommended"
  §5-v2 — May 11, Dana — "Revised after reviewer feedback"

Which version do you want to restore?
```
2. Confirm: *"Going back to {version} will replace what's there now. Anything since then won't be lost — it's still saved as the latest version. OK to restore?"*
3. Restore, log the rollback with reason

---

### `reopen`

Only available when document status is APPROVED.

Used when an approver or partner wants to make changes after approving.

1. *"This document was approved by {Name} on {date}. What needs to change?"*
2. Confirm: *"I'll revert the approval and set the document back to 'In Review' so edits can be made. The approved version is saved — nothing is lost. OK to continue?"*
3. Update status to ACTIVE, log the reopen using this format:
```markdown
### REOPEN — {Name} — {YYYY-MM-DD HH:MM}
**Requested by:** {Name}
**Reason:** {what needs to change}
**Approved version saved to:** .versions/{doc-name}.approved-before-reopen.md
```
4. Snapshot the approved version to `.versions/{doc-name}.approved-before-reopen.md`
5. Notify the team: *"[Co-Write] {doc title} — reopened for edits. {Name} has asked for some changes before final sign-off. You'll get a message when it's ready to review again."*
6. If a specific section needs changing: identify the section's writer from the status file. Send them a notification using the standard handoff message format, with the reason for reopening in the focus field. Their next `pickup` will enter a normal writer turn on that section — they resolve the issue and run `handoff` back to the reviewer, who then re-runs `approve`. If the approver wants to make the edit themselves: walk through the `approve` edit flow (step 4–5 of `approve`), then re-approve immediately.

---

### `remove`

Remove a team member who has dropped out, become unavailable, or left the project.

1. *"Who are you removing, and why?"* — log reason
2. **Check their current state:**
   - Do they hold a lock? → warn: *"{Name} is currently working on this. Remove them anyway?"* Require confirmation, then delete their lock and create an op-file entry noting forced removal.
   - Do they have open feedback items (as reviewer)? → ask: *"{Name} left {N} feedback items that haven't been resolved. Mark them all as closed, or reassign them to {approver}?"*
   - Do they own unstarted sections (Section Ownership)? → immediately offer to reassign: *"§{N} was {Name}'s — who should take it over?"*
   - Do they own an in-progress section? → warn: *"{Name} has started §{N} but hasn't finished. Their draft stays. Who should complete it?"*
3. Update `{doc-name}.status.md`: remove their row from the team table, reassign any open sections. Remove their entry from `.{doc-name}.contacts`.
4. Log the removal:
   ```markdown
   ### REMOVE — {Requestor} — {YYYY-MM-DD HH:MM}
   **Removed:** {Name} ({role})
   **Reason:** {reason}
   **Open work handled:** {how sections/feedback were resolved}
   ```
5. Notify the removed person if they have a contact method: *"[Co-Write] {doc title} — you've been removed from this project. Your work has been saved."*
6. Notify the rest of the team: *"[Co-Write] {doc title} — {Name} has left the project. Any reassignments have been made."*

---

## Context Usage

At `pickup` and before writing — load in this order:
1. `{doc-name}.status.md` — always
2. `{doc-name}.digest.md` if it exists, then last 3 entries of `{doc-name}.log.md`
3. Current document (`{doc-name}.md` or the person's section file)
4. `context-digest.md` then `context-index.md` — **only on demand** (when briefing references context, or the person asks about source material; defer otherwise)
5. Use `mcp__plugin_context-mode_context-mode__ctx_search` when a specific fact from source material is needed during writing

Do not load full source files unless specifically needed. Context compression (when log > 10 entries) runs **after** the briefing is shown, not before.

Do not load full source files unless specifically needed.

---

## Guiding Principles

- **Natural language first** — detect intent from what users say; never require command syntax.
- **One question at a time** — always, especially with non-technical users.
- **Warm, not clinical** — briefings and notifications should sound like a thoughtful colleague, not a dashboard.
- **First-timers get onboarded** — anyone picking up for the first time gets a 3-sentence explainer before the briefing.
- **Identity first** — know who's in the session before reading or writing anything.
- **Session discovery checks current dir first** — minimize typing.
- **Notification failures are explicit** — always give the user the message text if sending fails.
- **Feedback has three answers** — done, not yet, or skipping. All valid. Disputed is an escalation state, not a fourth regular option.
- **Digests are human-confirmed** — never compress without showing the user what will be saved.
- **Section Ownership uses scoped turn IDs** — `§N-TN`, never global counters.
- **Handoff is lightweight** — only "what changed" is required. Everything else is one optional prompt.
- **`add-context` reloads immediately** — new context is live in the current turn.
- **Schema is strict** — status labels, turn IDs, roles, and timeline headers use exact canonical strings. No synonyms.
- **Self-validate every write** — re-read structured files after writing and verify required fields before proceeding.
- **Op file brackets every handoff** — written before the first step, deleted after the last. Its presence at `pickup` means something interrupted and recovery is needed.
- **Recovery is always offered** — never silently skip a broken state. Surface it, explain it, offer finish/rollback/leave.
- **The log is sacred** — append-only, never edited.
- **Versions protect work** — always snapshot before overwriting.
- **`complete` closes cleanly** — final doc stays, everything else archives.
