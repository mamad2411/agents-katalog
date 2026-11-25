---
name: personal-os
description: "Energy-aware personal operations system with vault-native persistent memory. Combines Apple HealthKit/Oura sleep data, Google Calendar, Gmail inbox intelligence, Google Drive task persistence, and Obsidian Kanban integration — all persisted to the MoxyWolf Obsidian vault. Use this skill whenever Dorian says 'morning standup,' 'daily ops,' 'what should I focus on,' 'brain dump,' 'triage my tasks,' 'process my backlog,' 'weekly review,' 'how did my week go,' 'what's my day look like,' 'clear my head,' 'organize what's on my plate,' 'Sunday planning,' or any request about structuring his day, prioritizing work, reviewing the week, or processing a task list. Also trigger when Dorian asks about his energy levels, sleep patterns, productivity patterns, or pillar balance. This skill should trigger aggressively — if the request touches planning, prioritization, task management, health-aware scheduling, or weekly reflection, use it."
---

# Personal OS — Vault-Native Master Orchestrator

> **Architecture:** Three-layer memory system (FelixCraft pattern) integrated with energy-aware daily operations. All persistence lives in the MoxyWolf Obsidian vault — the plugin itself is stateless.

---

## VAULT RESOLUTION (runs before anything else)

The vault is the single source of truth. Locate it by checking in order:

1. **Cowork workspace mount**: Check if the current workspace folder (`/sessions/*/mnt/*/`) contains `CLAUDE.md` at root with MoxyWolf Vault markers. If yes, that IS the vault. Set `${VAULT}` to that path.
2. **Google Drive mount**: Check `/sessions/*/mnt/GoogleDrive-dorianc@moxywolf.com/Shared drives/MoxyWolf Shared Files/MoxyWolf Vault/`
3. **Google Drive REST API fallback**: Use the bundled `${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py` helper to read/write directly against the Drive v3 API. Team Drive ID: `0AHxJ5CazJqxOUk9PVA`. This is the ONLY path available in scheduled-task VM sessions. **One-time setup required:** Drive service account JSON at `~/.config/moxywolf/drive-service-account.json` (or pointed-to via `DRIVE_SERVICE_ACCOUNT_JSON` env var), with the service account email granted Editor/Manager access to the Shared Drive. See `references/scheduled-task-vm-setup.md` for the full provisioning checklist.
4. If all fail: use `request_cowork_directory` to ask Dorian to mount the vault.

Once resolved, store the path as `${VAULT}` for all subsequent operations.

**Vault key paths:**
- System memory: `${VAULT}/_System/MEMORY.md`
- Identity: `${VAULT}/_System/IDENTITY.md`
- Memory backups: `${VAULT}/_System/backups/`
- Daily notes: `${VAULT}/Daily Journal/YYYY-MM-DD.md`
- Task files: `${VAULT}/Tasks/*.md`
- Kanban board: `${VAULT}/Tasks/KANBAN_VIEW.md`
- Goals: `${VAULT}/GOALS.md`
- Project knowledge: `${VAULT}/Projects/*/11-Knowledge/`
- Cross-cutting knowledge: `${VAULT}/_Shared Knowledge/`
- People: `${VAULT}/People/`

---

## KANBAN WRITE RULES (CRITICAL — READ THIS BEFORE TOUCHING KANBAN_VIEW.md)

These rules apply to ALL modes that read or write KANBAN_VIEW.md.

**In an interactive Cowork session (vault is mounted as a workspace folder):**
Use the standard `Read` and `Write`/`Edit` file tools against the mounted path
(e.g. `${VAULT}/Tasks/KANBAN_VIEW.md`). This is the primary path and avoids all
Drive API quirks.

**In a scheduled-task VM (no vault mount):**
Use the bundled helper for both reads and writes. The helper passes
`supportsAllDrives=true` automatically.

```bash
# Read — downloads current content to a local file
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py" download \
    --file-id 18W69E1XIVwtTEEhcMXFcNs96zYrV5hzh \
    --out /tmp/kanban.md

# Write — uploads the full updated markdown
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py" upload \
    --file-id 18W69E1XIVwtTEEhcMXFcNs96zYrV5hzh \
    --in /tmp/kanban-updated.md \
    --mime text/plain
```

Always do a fresh `download` before any `upload` so you have the current state to
diff against — the helper does a full content replace, not a patch.

**Emoji-safe writes (prevents mojibake):**
The Kanban column headers contain emoji (🔥, ⭐, 📅, 💭, ⏳, ✅, 📥). When writing through Google Drive API, emoji can get mangled into `â€` garbage if not handled carefully. To prevent this:
1. Always read the current file first via `GOOGLEDRIVE_DOWNLOAD_FILE` before any write.
2. Preserve the exact header lines byte-for-byte from the downloaded content — do NOT re-type or reconstruct them from this template.
3. If the headers are already mangled from a previous bad write, restore them to these canonical forms:
   - `## 📥 Backlog`
   - `## 🔥 P0 - Today (Max 3)`
   - `## ⭐ P1 - This Week (Max 7)`
   - `## 📅 P2 - Scheduled`
   - `## 💭 P3 - Someday`
   - `## ⏳ Waiting On`
   - `## ✅ Done`

**Respecting column placement (no auto-moving):**
When Dorian checks off a card in Obsidian, the markdown changes `- [ ]` to `- [x]` in place — the item stays in its source column. Do NOT scan all columns for `- [x]` items and move them to Done. Respect where items are. A checked item in P1 means "completed but not yet triaged" — Dorian will move it during standup or triage. Only Modes 1 (Standup) and 2 (Triage) should move items between columns, and only with Dorian's confirmation.

**Tombstone check before adding (Modes 1 and 2):**
Never add a task derived from Slack, Gmail, calendar, or Drive without first matching it (>80% fuzzy title, tags/source stripped) against BOTH the `## ✅ Done` column of `KANBAN_VIEW.md` AND the done-archive at `${VAULT}/_Shared Knowledge/Agents and Plugins/team-kanban-done-archive.md`. If it matches a completed/archived item and the candidate's source signal is no newer than the completion date (`#completed/YYYY-MM-DD`, or the leading `YYYY-MM-DD` in an archive line), do NOT re-add it — it's already done and the source signal is just resurfacing. Only add on a signal dated after completion (a real recurrence), noting the prior completion in the task context. When ambiguous, leave it off and raise it in triage. Without this, a finished task whose Slack/email signal still exists gets rewritten onto the board. Also keep each card's column and its `#priority/pN` tag in agreement. (Team rule: `Taskade/_Shared Files/_shared-memory/feedback_kanban_check_tombstones_before_readd.md`.)

**Obsidian sync conflict:**
If Obsidian is open and syncing to Drive, it will overwrite external writes within seconds. Before writing, Dorian should close Obsidian, or writes may be lost.

---

## STEP 0: MEMORY BOOTSTRAP (EVERY SESSION)

**This step runs FIRST, before ANY other work.** It is the reason this plugin exists.

1. Read `${VAULT}/_System/IDENTITY.md` — load identity and operating principles
2. Read `${VAULT}/_System/MEMORY.md` — load Layer 1 tacit knowledge (preferences, patterns, project states, security rules, relationship context)
3. Read the most recent 3 files in `${VAULT}/Daily Journal/` — load Layer 2 recent context (sorted by filename descending, since filenames are YYYY-MM-DD.md)
4. Silently internalize all context. Do NOT recite it back to Dorian unless asked.
5. If `_System/MEMORY.md` is missing or empty, warn Dorian: "Memory file not found in the vault. Starting fresh — I'll build context as we work and write it at end of session."
6. If `_System/` doesn't exist at all, run FIRST-RUN INITIALIZATION (see memory-system skill).

**Memory bootstrap happens automatically whenever the personal-os skill is invoked.** It does not require Dorian to ask for it.

---

## STEP 0.5: SHORTHAND DECODER (EVERY REQUEST)

After memory bootstrap, **decode any shorthand in Dorian's request before acting on it.** This is the "decoder ring" — it turns Claude into a colleague who speaks Dorian's internal language.

**Tiered lookup flow:**

```
Dorian: "ping todd about the PSR for gryphon"

1. Check MEMORY.md → Shorthand & Decoder Ring section (hot cache)
   → "todd" → Todd [Last Name], [Role] ✓
   → "PSR" → Pipeline Status Report ✓
   → "gryphon" → Gryphon advisory client ✓

2. If not found → search vault knowledge
   → Check ${VAULT}/Projects/ for matching project names
   → Check ${VAULT}/People/ for matching contact names
   → Check ${VAULT}/_Shared Knowledge/ for matching terms

3. If still not found → ask Dorian
   → "What does X mean? I'll remember it for next time."
   → Add to MEMORY.md Shorthand section + update vault knowledge if needed
```

**When Dorian teaches you a new term:**
- Add to MEMORY.md `## Shorthand & Decoder Ring` immediately
- If it's a person: also update `## Relationships & Contacts` and consider creating `${VAULT}/People/[Name].md`
- If it's a project: also update `## Active Projects`
- If used 3+ times in a week, it belongs in the hot section

**Promotion / Demotion rules for the decoder ring:**
- **Promote** (add to hot section) when: used frequently, part of active work, new contact Dorian interacts with regularly
- **Demote** (remove from hot section, keep in vault knowledge) when: project completed, person no longer frequent, term rarely used in 30+ days AND low access count
- Target: ~30 people, ~30 terms/acronyms in the hot section — covers 90% of daily decoding needs

---

## OPERATING MODES

The personal OS has 5 modes. Determine mode from the user's command or intent:

| Mode | Trigger | Description |
|------|---------|-------------|
| **Morning Standup** | `/personal-os standup` or "morning standup" or "what's my day" | Full daily-ops standup with memory context |
| **Backlog Triage** | `/personal-os triage` or "triage" or "brain dump" | Process and prioritize backlog with Kanban |
| **Weekly Review** | `/personal-os review` or "weekly review" or "how was my week" | Retrospective with memory consolidation |
| **Memory Extract** | `/personal-os extract` or triggered by scheduled task | Nightly extraction cycle — update all memory layers |
| **Memory Query** | `/personal-os recall [topic]` or "what do you know about..." | Search memory layers for specific context |

If no mode is specified, default to **Morning Standup**.

---

## MODE 1: MORNING STANDUP

Combines daily-ops standup with memory context.

**Enhanced flow:**
1. **Memory Bootstrap** (Step 0 above — already done)
2. **Harvest Team Completions from Jira** — This is the FIRST operational step. Before assessing energy, calendar, or inbox, read the Jira board (project MOXY) to see what the team accomplished since the last standup. This grounds the entire standup in forward progress rather than an open task list.

   **How to execute:**
   a. Read the team-kanban config note at `${VAULT}/_Shared Knowledge/Agents and Plugins/team-kanban-config.md` for the cloudId, project key, and `last_standup_read` timestamp.
   b. Query Jira with `searchJiraIssuesUsingJql`:
      - **Done:** `project = MOXY AND status = Done AND statusCategoryChangedDate >= "<last_standup_read>"` — items confirmed complete since last standup. These are wins to acknowledge. Include subtasks; roll subtask completions up under their parent.
      - **In Review:** `project = MOXY AND status = "In Review"` (or, if the board has no In Review status, `labels = in-review`) — items marked complete by the assignee, awaiting reviewer confirmation. Capture how long each has been waiting.
   c. Also check for issues resolved by teammates that the team-kanban sync hasn't reconciled into Obsidian yet (issue Done in Jira, card still `- [ ]`) — these surface in the reconciliation flag below.
   d. Build a **Completions Report** with three sections:
      - **Confirmed Done:** Done issues with assignee names — "Phil completed X", "Michael completed Y"
      - **Pending Review:** In Review issues — who completed it, who's reviewing (the `Review:` line / `review-<name>` label), how long it's been waiting
      - **Newly Done (not yet triaged):** Issues moved to Done directly by the assignee without passing In Review — these need a reviewer assigned per the default pairings (Dorian↔Phil, Michael↔Steven)
   e. Present the Completions Report as the **opening section** of the standup brief under a `### What the Team Got Done` header (see updated briefing format in Step 11).
   f. **Reconciliation flag:** Carry the list of completed issues forward to Step 9 (Kanban State) so that when the Obsidian Kanban is read, any discrepancies between Jira and Obsidian can be flagged — e.g., an issue Done in Jira but its card still open in Obsidian.
   g. **After the standup completes,** update the `last_standup_read` line in the config note to the current timestamp.

   **Team Roster for mention resolution:**
   | Name | Short Name | Slack ID |
   |------|-----------|----------|
   | Dorian Cougias | dorian | U08PV3UHTEX |
   | Philip Mudhir | phil | U096C551HBR |
   | Steven P | steven | U098H0X9CQ4 |
   | Michael Flanagan | michael | U09EB7N7B98 |

   **Default Review Pairings (for newly checked items):**
   | Assignee | Default Reviewer |
   |----------|-----------------|
   | Dorian | Phil |
   | Phil | Dorian |
   | Michael | Steven |
   | Steven | Michael |

   **If Jira is unreachable (Atlassian MCP not connected):** Log "Jira unavailable — skipping team completions harvest" and continue to Step 3. Do not block the standup on a Jira read failure.

3. **Stepson Schedule Check** — Determine if this is a stepson week. Check MEMORY.md Life Rhythm section and recent daily notes. Adjust energy expectations accordingly.
4. **Health Data Pull** — Read sleep/health data from the Health Auto Export JSON drop in Drive (`${VAULT}/../Personal OS/health-export/` or the path stored in MEMORY.md → Health section). The iOS Health Auto Export app writes a fresh JSON file nightly. If the latest file is more than 36 hours old, note "stale" and continue. If no file exists at all, fall back to the iMessage-prompt pattern described in `references/health-fallback.md` (delegated from `daily-ops`).
5. **Energy Assessment** — Compare to baselines:
   | Metric | Baseline | Yellow | Red |
   |--------|----------|--------|-----|
   | Total Sleep | 7h | < 6h | < 5h |
   | Deep Sleep | 45m | < 30m | < 20m |
   | REM Sleep | 70m | < 50m | < 35m |
   | Sleep Efficiency | 85% | < 75% | < 65% |
   | Resting HR | 69 bpm | > 75 | > 80 |
6. **Calendar Scan** — Google Calendar for today + tomorrow via gcal MCP tools. **Always display all times in Pacific Time (PT)** — Dorian is based in PT. Convert any ET/UTC times from calendar events before presenting.
7. **Gmail Scan (Full Inbox Intelligence)** — Run five sub-queries:
   - 7a: Unanswered emails needing reply (is:inbox -is:draft, sent in last 48h, no reply from Dorian)
   - 7b: Meeting-related emails cross-referenced with today's calendar
   - 7c: VIP/key contact messages (from contacts in MEMORY.md Relationships section)
   - 7d: Urgent/time-sensitive threads (subject contains "urgent", "asap", "deadline", "EOD")
   - 7e: Optional-reply items (newsletters, notifications, FYI threads)
   Deduplicate and sort by priority.
8. **Google Drive State** — Read ACTIVE TASKS, BACKLOG, GOALS from Team Drive:
   - Team Drive ID: `0AHxJ5CazJqxOUk9PVA`
   - Folder ID: `1MjSabHDWYjjnp17DshdO9pnESLyvm6Gs`
   - WEEKLY LOG file ID: `1gOh0kIuygCAIMv18wGFPhc7CmsOfI-sI`
   - GOALS file ID: `1cBpTwIPCFDZ4YTqkqn21dM-5AjX6R9Wp`
   - **In interactive Cowork sessions:** read/write via the mounted vault path — standard `Read`/`Write`/`Edit`.
   - **In scheduled-task VMs:** use `${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py` for both reads (`download --file-id ...`) and writes (`upload --file-id ... --in ... --mime text/plain`). The helper passes `supportsAllDrives=true` automatically. See `references/scheduled-task-vm-setup.md` for one-time service-account setup.
9. **Kanban State (READ + JIRA RECONCILIATION)** — Read `${VAULT}/Tasks/KANBAN_VIEW.md` in full and parse all items by column. This is **Dorian's private working board** — a local view of the Google-Drive-canonical task store — not the team board. (The team board is Jira project MOXY; the private layer syncs *up* to Jira via the Google Drive Active Tasks sweep in `team-kanban`, so Dorian keeps a fast local board while the team sees Jira.) Surface any P0 items still open, flag items overdue by their `#due/` tag. **Surface all `## ⏳ Waiting On` items** — flag any waiting > 3 days for a nudge/follow-up. Carry all existing board items into the briefing.

   **Jira Reconciliation (uses Step 2 data):** Compare the Completions Report from Step 2 against Dorian's Obsidian board. Since `team-kanban` no longer writes back to Obsidian (Jira-only as of v0.6.0), this reconciliation is the sole place the private board and Jira are squared up. Flag discrepancies:
   - Issues Done in Jira but their card still open (`- [ ]`) in Obsidian → "Jira says done, Obsidian says open — confirm and sync?"
   - Issues In Review in Jira but the card not tagged `#review/` in Obsidian → "Jira has this in review, Obsidian doesn't — update Obsidian?"
   - Items checked in Obsidian (`- [x]`) whose linked issue isn't In Review or Done in Jira → "Completed in Obsidian but Jira hasn't caught up"
   Present all discrepancies in the briefing for Dorian's confirmation before writing anything back.

10. **Life-Rhythm Context** — Apply stepson-week adjustments, energy model overlays:
    - Morning = strategic thinking, Afternoon = execution, Evening = creative/review
    - Stepson weeks: Mon/Tue lighter, Wed transition, Thu/Fri peak
    - Non-stepson weeks: Mon-Wed deep work, Thu/Fri meetings OK
    - Tuesdays are meeting-dense — avoid scheduling deep work
11. **Memory-Enhanced Briefing** — Generate the brief, enhanced with:
    - Patterns from MEMORY.md (e.g., "You tend to overcommit on Mondays")
    - Active long-running processes from recent daily notes
    - Life-rhythm context
    - **Open with the `### What the Team Got Done` section from Step 2 BEFORE the health/calendar/inbox sections.** The briefing should feel like it starts with momentum — what moved — before shifting to what's ahead.

    Updated briefing format (insert at top, before `### Your Body Says`):

    ```
    ### What the Team Got Done
    [Confirmed completions from Jira Done — "Phil completed X", "Steven completed Y"]
    [Items pending review — "Michael's Z is waiting on Steven's review (1 day)"]
    [Any newly checked items that need triage — "Phil checked off A in P1 — move to In Review?"]
    [If no completions: "No new completions on the board since yesterday."]

    ### Sync Check
    [Any Jira↔Obsidian discrepancies from Step 9 reconciliation]
    [Or: "Jira and Obsidian are in sync."]
    ```

12. **Priority Enforcement** — Max 3 P0, Max 7 P1. Push back if exceeded.
13. **Write Daily Note** — Create `${VAULT}/Daily Journal/YYYY-MM-DD.md` with today's date. Include energy level, top priorities, calendar summary, key decisions queue, and a **"Today's Board"** section that is an **embedded Jira query** — a live view of the team board (MOXY), not a snapshot of KANBAN_VIEW.md. Write it as a fenced Jira query block for the Obsidian Jira plugin to render live:

    ````
    ## Today's Board
    ```jira-search
    project = MOXY AND assignee = currentUser() AND statusCategory != Done ORDER BY priority DESC, updated DESC
    ```
    [🔗 Full board](https://moxywolf.atlassian.net/jira/software/projects/MOXY/boards/1)
    ````

    The query renders live each time the note is opened, so the daily note always shows current Jira state without a re-sync. **Fallback:** if no Jira-rendering Obsidian plugin is installed, fetch those issues via the Atlassian MCP at standup time and write them in as a rendered list plus the board link, noting it's a point-in-time snapshot.
14. **Update Kanban Board (WRITE BACK)** — This is CRITICAL. After generating the briefing and confirming priorities with Dorian, reconcile and write back to `${VAULT}/Tasks/KANBAN_VIEW.md`:
    - **Sync Jira completions first** — apply any confirmed Done/In Review moves from Step 2 that Dorian approved during the briefing. This ensures completed work from Jira is reflected in Obsidian before any other changes.
    - **Add new tasks** surfaced from calendar, inbox, or open threads that aren't already on the board. Place under the correct priority column with full tags.
    - **Promote/demote** existing tasks if priorities shifted (e.g., a P1 becomes P0 because a deadline hit today).
    - **Surface checked items for confirmation** — if any `- [x]` items exist in non-Done columns, show them to Dorian: "These are checked off — move to Done?" Only move to `## ✅ Done` with confirmation. Set `#status/d` on moved items.
    - **Update Waiting On** — if a task is now blocked on someone, move it to `## ⏳ Waiting On` with `#status/w` and a "waiting on [person] since YYYY-MM-DD" suffix.
    - **Purge stale Done items** — remove items from `## ✅ Done` older than 2 days (see DONE COLUMN CLEANUP). Individual task files are preserved.
    - **Create individual task files** in `${VAULT}/Tasks/` for any newly added items (following the Individual Task File Format).
    - **Respect priority limits** — max 3 P0, max 7 P1. If the reconciliation would exceed limits, present the conflict and let Dorian decide.
    - Write the complete updated KANBAN_VIEW.md back to the vault. Do NOT skip this step.
    - **Kanban writes:** Interactive sessions write directly to the mounted file. Scheduled-task VMs use `scripts/drive_rest.py upload ...` against the Kanban file ID. Always `download` fresh first, modify locally, then `upload` — the helper does a full content replace.

---

## MODE 2: BACKLOG TRIAGE

Process and prioritize the backlog with Kanban board integration.

1. **Read BACKLOG** from Google Drive
2. **Read MEMORY.md** for project context and priority patterns
3. **Read `${VAULT}/GOALS.md`** for current objectives and priority framework. Use this to validate priority assignments — P0/P1 items should directly advance quarterly objectives.
4. **For each backlog item**, consider: pillar alignment, energy cost, deadline proximity, dependency chains
5. **Apply MoxyWolf pillar classification:**
   - **Enterprise:** STIGViewer, SAMS — core products
   - **Joint Ventures:** RegGenome, DeepFeedback.ai — partnerships
   - **Advisory:** Gryphon, Fortreum — consulting clients
   - **Founder Enablement:** AssuredBook, PR-as-MVP — ecosystem plays
   - **Personal:** Health, family, learning
6. **Enforce priority limits** (max 3 P0, max 7 P1). If Dorian tries to add more: "You're at max P0. Which one drops to make room?"
7. **Write updated ACTIVE TASKS and BACKLOG** to Google Drive
8. **Append triage decisions** to today's daily note
9. **Write Obsidian task files** — For each triaged item, create an individual task file in `${VAULT}/Tasks/` directory following the Individual Task File Format (see OBSIDIAN TASK INTEGRATION section). Filename: kebab-case of the task title, max 50 chars, `.md` extension. Skip files that already exist (check first).
10. **Update KANBAN_VIEW.md** — Read the current `${VAULT}/Tasks/KANBAN_VIEW.md`, then add each new triaged item as a `- [ ]` checkbox line under the correct priority column header. Include all inline tags (`#priority/pN #cat/category #status/n #due/YYYY-MM-DD`). Do not duplicate items that already exist in the board. Write the complete updated file back.

---

## MODE 3: WEEKLY REVIEW

Retrospective with memory consolidation.

1. **Read all daily notes** from the past 7 days in `${VAULT}/Daily Journal/`
2. **Read WEEKLY LOG, GOALS, ACTIVE TASKS** from Google Drive
3. **Health trend analysis** (week-over-week patterns)
4. **Pillar attention distribution analysis** — flag if any pillar gets < 10% or > 40%
5. **Goal progress assessment**
6. **Memory Consolidation:**
   - Extract durable facts from the week's daily notes
   - Update `${VAULT}/_System/MEMORY.md` with new patterns, preferences, project states
   - Apply hybrid memory decay (frequency + recency — see MEMORY DECAY RULES)
   - Promote/demote Shorthand & Decoder Ring entries based on this week's usage
   - Supersede outdated facts (never delete — set status to "superseded")
7. **Write WEEKLY LOG entry** to Google Drive
8. **Write updated MEMORY.md** to `${VAULT}/_System/MEMORY.md`
9. **Update Kanban board** — Re-read the CURRENT state of KANBAN_VIEW.md fresh from Google Drive (use `GOOGLEDRIVE_DOWNLOAD_FILE`, NOT a cached version). Then:
   - Surface any `- [x]` items found in non-Done columns to Dorian: "These items are checked off — should I move them to Done?"
   - For items Dorian confirms as complete, or tasks verbally confirmed complete during this review: move to `## ✅ Done`, set `#status/d`.
   - Do NOT auto-move checked items without confirmation — respect column placement per KANBAN WRITE RULES.
   - **Purge stale Done items:** remove any items from the `## ✅ Done` column that are older than 2 days (see DONE COLUMN CLEANUP for date detection logic). Individual task files in `${VAULT}/Tasks/` are preserved as permanent records.
   - Normalize tags on remaining Done items: ensure `- [x]` and `#status/d`.
   - Write the complete updated KANBAN_VIEW.md back. In interactive sessions: write to the mounted path. In scheduled-task VMs: `python3 scripts/drive_rest.py upload --file-id ${KANBAN_FILE_ID} --in /tmp/kanban-updated.md --mime text/plain`. Remember to preserve emoji headers (see KANBAN WRITE RULES).
10. **Write weekly summary** to today's daily note

---

## MODE 4: MEMORY EXTRACT (Nightly Extraction Cycle)

Designed for the scheduled nightly task. Reviews the day's work and extracts durable knowledge.

**Note:** In scheduled-task VMs, the vault is NOT mounted locally. All reads/writes go through the Drive REST API via `${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py`. Requires the one-time service-account setup at `~/.config/moxywolf/drive-service-account.json`.

**Steps:**

1. **Pre-flight check — already extracted?**
   Read today's daily note (`${VAULT}/Daily Journal/YYYY-MM-DD.md`). Check the `## Extraction Status` section at the bottom. If it reads `Extracted: yes` or contains an extraction timestamp, log "Extraction already completed for today — skipping" and **exit immediately without modifying any files.** Only proceed if `Extracted: no`, or the daily note doesn't exist, or there is no Extraction Status section. This prevents duplicate extractions from double-fires or manual extractions done during a Cowork session.
2. **Read current MEMORY.md** — `${VAULT}/_System/MEMORY.md`
3. **Extract durable facts** from the day:
   - New preferences discovered (communication style, tool preferences, scheduling patterns)
   - Project state changes (new projects, milestones hit, blockers encountered)
   - Relationship updates (new contacts, changed roles, interaction patterns)
   - Security rules learned (API keys patterns, access notes — NEVER actual secrets)
   - Decisions made and their rationale
4. **Classify each fact** using the Atomic Fact Schema:
   ```json
   {
     "id": "fact-YYYYMMDD-NNN",
     "fact": "Description of the durable fact",
     "category": "preference|project|relationship|security|decision|pattern",
     "timestamp": "ISO-8601",
     "source": "conversation|email|calendar|drive|health",
     "status": "active",
     "relatedEntities": ["entity-names"],
     "lastAccessed": "ISO-8601",
     "accessCount": 1
   }
   ```
5. **Update MEMORY.md:**
   - Add new facts to appropriate sections
   - Bump `lastAccessed` and `accessCount` for facts referenced today
   - Apply hybrid decay (see MEMORY DECAY RULES)
   - Never delete facts — supersede with `supersededBy` pointer
6. **Update vault knowledge** — For significant entities, write/update notes in:
   - `${VAULT}/Projects/[Project]/11-Knowledge/` for project-specific knowledge
   - `${VAULT}/_Shared Knowledge/` for cross-cutting knowledge
   - `${VAULT}/People/[Name].md` for new contacts
   - All notes use vault YAML frontmatter, wikilinks, and tags per CLAUDE.md conventions
7. **Write all changes** to vault (via Google Drive API in scheduled tasks)
8. **Log extraction** — update today's daily note `## Extraction Status` to `Extracted: yes — YYYY-MM-DD HH:MM PT`
9. **Kanban Done cleanup** — Purge stale items from the Done column. See DONE COLUMN CLEANUP section for the full procedure. This keeps the board visually clean without losing any data (individual task files remain).

---

## MODE 5: MEMORY QUERY

Quick retrieval mode for specific context.

1. Parse the query topic from user's request
2. Search across all memory layers:
   - Layer 1: `${VAULT}/_System/MEMORY.md` sections (grep for keywords)
   - Layer 2: `${VAULT}/Daily Journal/` — recent daily notes (last 30 days)
   - Layer 3: `${VAULT}/Projects/` and `${VAULT}/_Shared Knowledge/` — vault knowledge
3. Return relevant context with source attribution:
   - "[From MEMORY.md]" — tacit knowledge
   - "[From Daily Journal YYYY-MM-DD]" — specific date context
   - "[From Projects/SAMS/11-Knowledge/note-name]" — project knowledge
4. If nothing found, say so honestly — don't fabricate context

---

## MEMORY FILE FORMATS

### MEMORY.md (Layer 1 — Tacit Knowledge)

Location: `${VAULT}/_System/MEMORY.md`

```markdown
# Memory — Dorian Cougias
> Last updated: YYYY-MM-DD HH:MM UTC
> Facts: N active, M superseded

## Shorthand & Decoder Ring
> Hot cache — target ~30 people, ~30 terms. Covers 90% of daily decoding.

| Nickname | Resolves To | Context |
|----------|-------------|---------|
| [nickname] | [Full Name], [Role] | [Prefers Slack, direct style] |

| Term | Meaning | Context |
|------|---------|---------|
| [acronym] | [Full expansion] | [When/where used] |

| Codename | Project |
|----------|---------|
| [codename] | [Full project name] |

## Who Dorian Is
[Persistent identity facts — role, company, working style]

## Preferences & Patterns
[Communication preferences, scheduling patterns, tool preferences]

## Active Projects
[Current project states with last-known status]

## Relationships & Contacts
[Key people, their roles, interaction patterns]

## Security & Access
[Systems, credentials patterns (NEVER actual secrets), access levels]

## Decisions Log
[Significant decisions with rationale — helps maintain consistency]

## Life Rhythm
[Stepson schedule, energy patterns, health baselines]

## Cold Storage
[Facts older than 30 days without access — kept but not surfaced in briefings]
```

### Daily Note (Layer 2 — `${VAULT}/Daily Journal/YYYY-MM-DD.md`)

```markdown
---
title: "YYYY-MM-DD — Day of Week"
date: YYYY-MM-DD
type: standup
tags: [daily, standup]
participants: [dorian]
status: active
---

# YYYY-MM-DD — Day of Week

## Energy
- Sleep: Xh (deep: Xm, REM: Xm, efficiency: X%)
- Assessment: [green/yellow/red]
- Stepson week: [yes/no]

## Today's Board
```jira-search
project = MOXY AND assignee = currentUser() AND statusCategory != Done ORDER BY priority DESC, updated DESC
```
[🔗 Full board](https://moxywolf.atlassian.net/jira/software/projects/MOXY/boards/1)
<!-- Live embedded Jira query (team board). Dorian's private checkbox board is Tasks/KANBAN_VIEW.md. If no Jira-render plugin is installed, replace this block with a rendered snapshot fetched via the Atlassian MCP at standup. -->


## Calendar
- [HH:MM] Meeting/event description
- [HH:MM] Meeting/event description

## Inbox Intelligence
- [Priority flag] Email summary → action needed
- [Priority flag] Email summary → FYI only

## Decisions Made
- [Decision with rationale]

## Facts Extracted
- [New durable facts discovered today]

## Open Threads
- [Items needing follow-up tomorrow]

## Extraction Status
- Extracted: no
```

**Note:** The "Today's Board" section is an **embedded Jira query** (a live `jira-search` block against MOXY — see Step 13), so it always reflects current team-board state, not a snapshot. Dorian's own checkbox board is separate: `KANBAN_VIEW.md` is his private working layer, and triage/review keep writing his tasks there as Obsidian checkboxes (the Google-Drive-canonical store syncs those up to Jira via team-kanban's Drive sweep). So the daily note *shows* the team board live and *works* the private board via checkboxes — two distinct surfaces.

---

## GOOGLE DRIVE INTEGRATION

Shared task persistence on Google Drive Team Drive:

- **Team Drive ID:** `0AHxJ5CazJqxOUk9PVA`
- **Folder ID:** `1MjSabHDWYjjnp17DshdO9pnESLyvm6Gs`
- **Documents:** BACKLOG, ACTIVE TASKS, GOALS, WEEKLY LOG
- **WEEKLY LOG file ID:** `1gOh0kIuygCAIMv18wGFPhc7CmsOfI-sI`
- **GOALS file ID:** `1cBpTwIPCFDZ4YTqkqn21dM-5AjX6R9Wp`

### Team Drive Read/Write Pattern (scheduled-task VM only)

In an interactive Cowork session, the vault is mounted as a workspace folder — use the normal `Read`/`Write`/`Edit` tools and skip this section. The patterns below only apply in scheduled-task VMs where there's no mount.

The bundled helper at `${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py` hits the Drive v3 REST API directly with a service account, always passing `supportsAllDrives=true`. See `references/scheduled-task-vm-setup.md` for one-time provisioning of `~/.config/moxywolf/drive-service-account.json`.

**Read file content:**
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py" download \
    --file-id "${FILE_ID}" --out /tmp/file.md
# Then read /tmp/file.md normally.
```

**Update existing file content:**
```bash
# Edit /tmp/file.md locally, then:
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py" upload \
    --file-id "${FILE_ID}" --in /tmp/file.md --mime text/plain
```

**Create a new file in the Team Drive:** the helper currently exposes `download`, `upload`, `search`, and `ls`. For first-time creation, either (a) create the file once in the Drive UI and then `upload` to its ID, or (b) extend `drive_rest.py` with a `create` subcommand that does a metadata POST + media upload (the two-step pattern is documented in Google's Drive API reference). The vast majority of personal-os writes are updates to existing files (Kanban, MEMORY, WEEKLY LOG, daily notes) so first-time creation is rare in the nightly path.

**.md file reads:** the helper's `download` uses `alt=media`, which works for `.md`, `.txt`, and other plain MIME types in a Team Drive. There's no special handling needed for markdown files in this path.

---

## OBSIDIAN TASK INTEGRATION

Dual-persistence model (Dorian's **private** layer): Google Drive is the canonical task store, the Obsidian vault provides a local Kanban board + individual task files for daily visibility. This private layer syncs *up* to the team board on Jira (project MOXY) via team-kanban's Google Drive Active Tasks sweep — personal-os itself only ever writes Obsidian checkboxes + the Drive store, never Jira issues. The team board (Jira) surfaces in the daily note as a live embedded query, not as a copy.

### Vault Task Structure

```
${VAULT}/
├── Tasks/
│   ├── KANBAN_VIEW.md          ← Kanban board (Obsidian Kanban plugin)
│   ├── DASHBOARD.md            ← Read-only (Dataview auto-queries, never edit)
│   ├── task-name-here.md       ← One file per task
│   └── ...
└── GOALS.md                    ← Goals, themes, priorities
```

### KANBAN_VIEW.md Format

```markdown
---

kanban-plugin: board

---

## 📥 Backlog

## 🔥 P0 - Today (Max 3)

- [ ] Task title #priority/p0 #cat/technical #status/n #due/2026-03-08

## ⭐ P1 - This Week (Max 7)

- [ ] Task title #priority/p1 #cat/outreach #status/n #due/2026-03-13

## 📅 P2 - Scheduled

- [ ] Task title #priority/p2 #cat/admin #status/n #due/2026-03-20

## 💭 P3 - Someday

## ⏳ Waiting On

- [ ] Task title — waiting on [person/event] since YYYY-MM-DD #priority/p1 #cat/outreach #status/w #due/2026-03-15

## ✅ Done

- [x] Completed task #priority/p1 #cat/technical #status/d

%% kanban:settings
{"kanban-plugin":"board"}
%%
```

**Tag reference:**
- Priority: `#priority/p0` | `#priority/p1` | `#priority/p2` | `#priority/p3`
- Category: `#cat/admin` | `#cat/technical` | `#cat/outreach` | `#cat/writing` | `#cat/content` | `#cat/research` | `#cat/personal` | `#cat/other`
- Status: `#status/n` (not started) | `#status/s` (started) | `#status/w` (waiting) | `#status/b` (blocked) | `#status/d` (done)
- Due: `#due/YYYY-MM-DD`
- Waiting: `#waiting/person-name` (optional — tracks WHO you're waiting on)

### Individual Task File Format

Filename: kebab-case, max 50 chars, `.md` extension.

```markdown
---
title: Human-readable task title
category: technical
priority: P1
status: n
created_date: 2026-03-08
due_date: 2026-03-13
estimated_time: 30
waiting_on:
waiting_since:
resource_refs: []
---

# Human-readable task title

## Quick View (Kanban)
- [ ] Human-readable task title #priority/p1 #cat/technical #status/n #due/2026-03-13

## Context
Tie to goals from GOALS.md. Cite the specific objective this supports.

## Next Actions
- [ ] First concrete step
- [ ] Second concrete step

## Progress Log
- YYYY-MM-DD: Task created from [source].
```

### Write Rules (CRITICAL)

**Every time tasks are created or updated, you MUST do BOTH:**
1. Create/update individual task files in `${VAULT}/Tasks/`
2. Update `${VAULT}/Tasks/KANBAN_VIEW.md` — add/move/check items under the correct column

**Task completion workflow:**
1. In KANBAN_VIEW.md: move line to `## ✅ Done`, change `- [ ]` to `- [x]`, change status tag to `#status/d`
2. In task file: change frontmatter `status: n` → `status: d`, check off completed Next Actions

**Waiting On workflow:**
1. Move task to `## ⏳ Waiting On` in KANBAN_VIEW.md
2. Change status to `#status/w`, add `#waiting/person-name`
3. Append " — waiting on [person/event] since YYYY-MM-DD"
4. Update task file frontmatter: `status` → `w`, add `waiting_on` and `waiting_since`
5. During morning standup: surface all Waiting On items, flag any waiting > 3 days
6. When unblocked: move back to priority column, change `#status/w` → `#status/s`

**DASHBOARD.md is read-only** — Dataview queries auto-update. Never write to it.

---

## HEALTH DATA INTEGRATION

### Baselines (Dorian's personal norms)

| Metric | Baseline | Yellow | Red |
|--------|----------|--------|-----|
| Total Sleep | 7h | < 6h | < 5h |
| Deep Sleep | 45m | < 30m | < 20m |
| REM Sleep | 70m | < 50m | < 35m |
| Sleep Efficiency | 85% | < 75% | < 65% |
| Resting HR | 69 bpm | > 75 | > 80 |

### Life Rhythm Calendar

- **Stepson (Aaron) weeks:** Mon/Tue lighter schedule, transition Wed, peak Thu/Fri
- **Non-stepson weeks:** Mon-Wed available for deep work
- **Energy model:** Morning = strategic thinking, Afternoon = execution, Evening = creative/review
- **Tuesdays:** Meeting-dense — avoid deep work
- **Wednesdays:** Can also be meeting-heavy
- **Best deep-work days:** Mon/Thu/Fri on non-stepson weeks

---

## MOXYWOLF PILLARS

All work maps to one of these five pillars:

1. **Enterprise:** STIGViewer, SAMS — core products
2. **Joint Ventures:** RegGenome, DeepFeedback.ai — partnerships
3. **Advisory:** Gryphon, Fortreum — consulting clients
4. **Founder Enablement:** AssuredBook, PR-as-MVP — ecosystem plays
5. **Personal:** Health, family, learning

Pillar attention is tracked weekly. Flag imbalance if any pillar gets < 10% or > 40% of attention.

---

## PRIORITY ENFORCEMENT

**Hard limits — enforced by the system, not suggestions:**

- Maximum 3 P0 tasks at any time
- Maximum 7 P1 tasks at any time
- If Dorian tries to add more, push back: "You're at max P0. Which one drops to make room?"
- Every P0 must have a clear definition of done and a deadline
- Tasks without a pillar assignment get flagged

---

## MEMORY DECAY RULES (Hybrid Frequency + Recency)

Pure time-based decay is too blunt. Use **both signals:**

**Decision matrix:**

| accessCount | Last Accessed | Action |
|-------------|--------------|--------|
| High (5+) | Recent (< 14 days) | **Keep hot** — active knowledge |
| High (5+) | Stale (14-30 days) | **Keep warm** — still valuable, monitor |
| High (5+) | Old (30+ days) | **Demote to cold** — was important, may return |
| Low (1-2) | Recent (< 14 days) | **Keep warm** — new, give it time |
| Low (1-2) | Stale (14-30 days) | **Demote to cold** — didn't stick |
| Low (1-2) | Old (30+ days) | **Cold storage** — archive candidate |

**During weekly review, also apply to Shorthand & Decoder Ring:**
- Terms/people used 3+ times this week → ensure in hot section
- Terms/people not used in 2+ weeks AND low total access → demote from hot section to vault knowledge only
- Completed projects → demote codenames, keep people if still active contacts

**Resurrection:** If a cold-storage fact is accessed again, immediately promote it back to the appropriate active section and reset its decay clock.

---

## TASK EXTRACTION FROM CONVERSATIONS

**Behavioral pattern — always active, not just during formal modes.**

When processing any conversation, email, meeting summary, or brain dump, **watch for implicit task commitments** and surface them:

**Extract when you detect:**
- Commitments Dorian made ("I'll send that over," "let me follow up on that")
- Action items assigned to him ("Can you handle X?" "You're on point for Y")
- Follow-ups mentioned ("We should circle back on this," "Need to check in with Z")
- Deadlines implied ("By end of week," "Before the meeting Thursday")

**Extraction protocol:**
1. Collect all detected tasks silently as you process content
2. At the end of the interaction, present them: "I caught N potential tasks — want me to add them?"
3. List each with: task title, implied owner, implied deadline (if any), source context
4. **Wait for confirmation** — never auto-add tasks without Dorian's approval
5. For approved tasks: create task files in `${VAULT}/Tasks/` + update KANBAN_VIEW.md + update Google Drive

**Priority inference:**
- Explicit deadlines within 48h → suggest P0
- This-week deadlines → suggest P1
- No deadline mentioned → suggest P2 or Backlog
- Always let Dorian override the suggestion

---

## DONE COLUMN CLEANUP

The `## ✅ Done` column on the Kanban board is a short-term visibility window, not a permanent archive. Items older than 2 days get removed from the board to keep it clean. The individual task files in `${VAULT}/Tasks/` are the permanent record and are never deleted by this process.

**When it runs:** During Mode 4 (Nightly Extraction), Mode 1 (Morning Standup), and Mode 3 (Weekly Review).

**Procedure:**

1. Read `Tasks/KANBAN_VIEW.md` fresh (use `GOOGLEDRIVE_DOWNLOAD_FILE`, not cached content).
2. Parse the `## ✅ Done` column only. For each `- [x]` item, determine its completion date using this priority order:
   a. **`#due/YYYY-MM-DD` tag** — if present, use that date.
   b. **Inline date in card text** — look for patterns like "verified fixed YYYY-MM-DD", "fixed YYYY-MM-DD", "since YYYY-MM-DD", "completed YYYY-MM-DD", or any bare YYYY-MM-DD in the card text.
   c. **Daily note cross-reference** — scan the last 7 daily notes for when the item first appeared under a Done heading or was marked `#status/d`.
   d. **If no date can be determined**, leave the item in place (err on the side of keeping).
3. Remove any Done item whose determined date is **more than 2 days before today**.
4. **Tag normalization** on remaining Done items (≤ 2 days old):
   - If still shows `#status/w`, `#status/n`, `#status/s`, or `#status/b` → change to `#status/d`
   - If still shows `- [ ]` → change to `- [x]`
5. Preserve all other columns exactly as-is. Do not reorder items, move items between columns, or change tags outside the Done column.
6. Write back using `GOOGLEDRIVE_EDIT_FILE`. Remember emoji-safe writes (see KANBAN WRITE RULES).

---

## SCHEDULED TASK INTEGRATION

This plugin works with Claude's scheduled task system:

- **Nightly Extraction** (11 PM daily): Runs Mode 4. Uses Google Drive API to access vault files since the VM can't mount the vault locally.
- **Morning Standup** (triggered by Dorian or Siri shortcut): Runs Mode 1.
- **Weekly Review** (Sunday evening): Runs Mode 3.

---

## FAILURE MODES & RECOVERY

### If vault is not mounted:
1. Fall back to the Drive REST API via `${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py` (scheduled-task VM path)
2. If the helper fails authentication (no service-account JSON, expired credentials), warn Dorian and pause — don't try to write blind
3. Queue updates locally and re-attempt on the next successful run

### If MEMORY.md is corrupted or missing:
1. Check `${VAULT}/_System/backups/` for most recent backup
2. Check daily notes in `${VAULT}/Daily Journal/` — they contain extracted facts
3. Check Google Drive documents for project state
4. Rebuild MEMORY.md from available sources
5. Log the recovery in a new daily note

### If Google Drive is unreachable:
1. Work with vault memory files only
2. Queue Drive updates for next successful connection
3. Note the outage in daily log

### If health data is unavailable:
1. Skip energy assessment
2. Use previous day's data if available
3. Default to "yellow" energy level (cautious scheduling)

### Context window overflow:
1. Load `${VAULT}/_System/MEMORY.md` + last 3 daily notes as standard bootstrap
2. Query vault knowledge on-demand for specific topics
3. Daily notes older than 30 days should be summarized, not loaded verbatim
