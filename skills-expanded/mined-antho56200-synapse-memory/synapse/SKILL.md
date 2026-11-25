---
name: synapse
description: Perpetual memory and shared brain for Claude Code. A two-level memory system — per-project memory plus a global cross-project brain — that makes Claude remember everything across all sessions and all projects. USE THIS SKILL whenever a session starts in any project, whenever the user mentions memory, remembering, recalling, forgetting, past decisions, past projects, "what did we decide", "have we done this before", knowledge reuse, memory map, or asks to install/setup/check/visualize a memory system. Also use it whenever you learn something reusable (research findings, best practices, patterns, tool knowledge) that future projects would benefit from — even if the user doesn't mention memory explicitly.
---

<!-- SYNAPSE_VERSION: 3.5 -->

# SYNAPSE v3 — Perpetual Memory & Shared Brain for AI Coding Agents

## 📄 For humans — 60-second read

**SYNAPSE turns your AI coding agent into one that never forgets.** Every project keeps a working memory (what you're building, what you decided, what broke). All your projects share one global brain (what you've learned — available everywhere, forever). Knowledge carries freshness dates, gets flagged for re-verification when it ages — and strengthens with use, like real synapses. A nightly "sleep cycle" compresses, deduplicates and organizes everything — fully automatic on Claude Code.

**Install (pick one):**
1. **Claude Code** — drag this file into any conversation (or paste its content). Say nothing else. Claude installs everything itself in under a minute.
2. **Any other AI agent** (Cursor, Codex CLI, Gemini CLI, Windsurf, aider…) — tell it: *"Read this file and set up SYNAPSE portable mode (Part 7)."* Same brain, shared between all your agents.

**What you get:** `/brief` (where were we?) · `/brief full` (complete memory report) · `/recall <topic>` (search all memory, all projects) · `/decision <what>` (log a decision) · `/learn <insight>` (promote to global brain) · `/forget <topic>` (clean, restorable removal) · `/memory-map` (visual dashboard in your browser) · `/consolidate` (run the sleep cycle now) · `/memory-doctor` (health check + auto-fix) · `/memory-budget` (choose how much memory auto-loads per session, from a 2k-token index up to full total-recall — you see the real cost before choosing; storage itself is unlimited).

**Your data:** plain markdown files on YOUR machine — `~/.claude/brain/` (global) + `<project>/.claude/memory/` (per project). No cloud, no telemetry, no lock-in: delete the folders and it's gone. Secrets, tokens and .env values are never stored, by protocol. Works on macOS, Linux, WSL and native Windows.

*Everything below is written for the AI agent. You never need to read it — but you can.*

---

> **⚡ INSTALL TRIGGER — agent, read this first.** If you are reading this file because the user dragged or pasted it into the conversation — with or without an accompanying message — that IS the instruction to install SYNAPSE. Act now, then report per Part 6. Four cases:
> 1. **You are Claude Code, file dragged** → copy it to `~/.claude/skills/synapse/SKILL.md` (step 1.1) and run Part 1.
> 2. **You are Claude Code, content pasted as text** → first Write this exact content, verbatim and complete, to `~/.claude/skills/synapse/SKILL.md`, then run Part 1.
> 3. **SYNAPSE already installed** → compare `SYNAPSE_VERSION` markers; if this file is newer, overwrite the installed SKILL.md and re-run Part 1 — it is idempotent (creates only what's missing, refreshes SYNAPSE-owned command files).
> 4. **You are NOT Claude Code** (different agent, no `~/.claude` skills system) → follow **Part 7 (portable mode)** instead of Part 1.

SYNAPSE gives your agent a brain-like memory: a **local memory** per project (working memory + archives) and a **global brain** shared across ALL projects (knowledge learned once, available everywhere). Projects can observe each other read-only. Knowledge has freshness dates. A nightly consolidation compresses, deduplicates, detects contradictions, and rotates memory — like sleep does for humans.

```
~/.claude/brain/                     GLOBAL BRAIN (all projects share it)
├── BRAIN.md                         tiny index — auto-loaded every session
├── knowledge/<domain>/*.md          semantic memory (facts, research) w/ freshness
├── practices/*.md                   procedural memory (how-tos, patterns)
├── projects/_index.md               registry of all known projects
├── projects/<name>.md               one summary card per project
└── episodic/*.md                    heavy archives (full briefs, L0 detail)
                                     └── attic/ (soft-forgotten notes, restorable)

<project>/.claude/memory/            LOCAL MEMORY (this project only)
├── primer.md                        working memory — auto-loaded, <150 lines
├── warm/                            on-demand depth (architecture, decisions log)
├── cold/hindsight/                  dated session archives
└── scratch/                         ephemeral (pre-compaction dumps)
```

**Compression gradient (3 levels, like human memory):**
- **L0 — full detail**: complete briefs/research → `brain/episodic/` or project `cold/`
- **L1 — structured summary**: 1 page max → `brain/knowledge/` or project `warm/`
- **L2 — index line**: 1 line + pointer → `BRAIN.md` or `primer.md`

Never load L0 by default. Hot context stays small; depth is one `Read` away.

---

## Part 1 — Bootstrap on Claude Code (run automatically when structure is missing)

When this skill activates, silently check three things: (a) does `~/.claude/brain/BRAIN.md` exist? (b) does `<project>/.claude/memory/primer.md` exist in SYNAPSE format? (c) are there **legacy memory artifacts** — any of: `.claude/memory/update-memory.sh` (V1), `.claude/memory/nightly-consolidation.sh` (CORTEX), `hindsight/` `decisions/` `learnings/` folders directly under `.claude/memory/`, a claude-mem install, or a `CLAUDE.md` bloated (>200 lines) with accumulated notes. If (a)+(b) are true and (c) is false, skip to Part 2. If legacy artifacts exist, run **1.4 migration first**. Otherwise run the missing steps below. Finish by telling the user what was installed/migrated in 3 lines max.

### 1.0 Platform notes (read once)
All hooks and scripts below are bash — and they work as-is on macOS, Linux, WSL **and native Windows**: when Git Bash is present (it ships with Git for Windows), Claude Code executes hook commands through it even on Windows (empirically verified); without Git Bash, hooks fall back to PowerShell and SYNAPSE runs degraded (Part 5). Only three Windows deltas, each handled in the step where it applies: the auto-load import must use an absolute path (1.3), the scheduler is Task Scheduler instead of cron (1.8), and every `.sh` file must be written with **LF line endings**.

### 1.1 Install the skill globally (if not already)
If this SKILL.md is not at `~/.claude/skills/synapse/SKILL.md`, copy it there — or Write the content verbatim if it arrived as pasted text — so every project gets it. If an older `SYNAPSE_VERSION` is installed there, replace it with this one.

### 1.2 Create the global brain (once per machine)
```bash
mkdir -p ~/.claude/brain/{knowledge,practices,projects,episodic}
```
Create `~/.claude/brain/BRAIN.md` if missing. First pick the **memory budget** — how much of the brain auto-loads into context at every session start. Show the user the four levels WITH the real estimated cost (estimate: total bytes of the files each level injects ÷ 4 ≈ tokens; on a fresh brain quote the typical range):
- `lean` — index only (BRAIN.md, index-limit 60). ≈1–2k tokens/session. Starters, ≤8 projects.
- `pro` — bigger index (150) + active-project cards precompiled into HOT.md. ≈3–8k. The regular.
- `deep` — pro + ALL practices + the top-20 L1 notes ranked by (golden, uses, last_used), precompiled into HOT.md. ≈10–40k. Heavy multi-project users.
- `full` — **total recall**: the entire L1 layer (all knowledge + all practices + project cards) in context every session; only L0 archives stay on-demand. Cost = the real size of the brain — compute and show it. Typically 50–150k tokens: for power users who'd rather pay tokens than ever re-explain anything.
The user chooses knowing the price; `/memory-budget` re-shows costs and switches anytime. Write the choice into the Budget line:
```markdown
# BRAIN — Global Index
> Budget: lean | index-limit: 60   (levels: lean|pro|deep|full — resize anytime: /memory-budget)
> One line per entry, pointer to the detail file. Hard limit = index-limit above.
> Freshness: stale entries get a ⏳ prefix on their line (see stale_after).

## Knowledge
(empty — filled as you learn)

## Practices
(empty)

## Projects
(empty — projects register themselves)
```
**The hot pack — `~/.claude/brain/HOT.md`**: for budgets ≥ `pro`, a single precompiled file holds everything the chosen level injects beyond the index (project cards / practices / L1 notes, concatenated). It is regenerated by every consolidation and by `/memory-budget`, and its first line states its own size: `> HOT PACK (deep) | ~34k tokens | rebuilt 2026-07-06`. Auto-loading = one import line (see 1.3). Never edit HOT.md by hand — it's a build artifact; edit the source notes.

Create `~/.claude/brain/projects/_index.md` if missing:
```markdown
# Project Registry
> Format: - name | absolute/path | one-liner | last-active YYYY-MM-DD
> Rule: paths here may be READ for reference. NEVER write outside the
> current project and ~/.claude/brain/.
```

### 1.3 Wire the brain into every session
Ensure `~/.claude/CLAUDE.md` exists and contains the import line below (add if missing). **macOS/Linux/WSL:**
```markdown
@~/.claude/brain/BRAIN.md
```
**Native Windows: the `~` import does NOT resolve (verified bug — it fails silently).** Write the absolute path with forward slashes instead:
```markdown
@C:/Users/<username>/.claude/brain/BRAIN.md
```
For budgets ≥ `pro`, add the hot-pack import on the next line (same Windows rule): `@~/.claude/brain/HOT.md`. Create HOT.md (even minimal) before adding the import. Removing the import is how `lean` switches the pack off.
This makes the global index (+ hot pack) auto-load in every session, in every project. Same rule applies to any import you add on Windows.

### 1.4 Migrate & absorb an existing memory system (only if legacy artifacts detected)
**Iron rule: never delete anything before the data is fully absorbed.** Steps:
1. **Backup first**: `cp -r .claude/memory .claude/memory-backup-$(date +%F)` (add the backup path to `.gitignore`).
2. **Read everything** the old system holds: old primer, `hindsight/`, `decisions/`, `learnings/`, claude-mem exports, and any accumulated notes inside a bloated `CLAUDE.md`.
3. **Re-route the content** using the Part 2 routing rules: project-specific state → new primer (≤150 lines) and `warm/`; dated session archives → `cold/hindsight/` (keep original dates); decisions → `warm/decisions-log.md`; **reusable knowledge** (techniques, research, patterns) → promote to `~/.claude/brain/knowledge/` or `practices/` with frontmatter (`origin_project`, best-guess `verified` date, appropriate `stale_after`) + L2 lines in `BRAIN.md`. Merge intelligently — no duplicates, no data loss.
4. **Retire the old machinery** (after confirming migration is complete, ask the user before deleting): old scripts (`update-memory.sh`, `nightly-consolidation.sh`), old git `pre-commit` memory hooks, obsolete crontab lines (`crontab -l | grep -v <old-script> | crontab -`) or scheduled tasks, and `settings.json` hook entries pointing to removed scripts. A bloated `CLAUDE.md` gets trimmed to ≤200 lines — overflow moves into the memory structure, never lost.
5. Keep the backup 7 days (nightly consolidation deletes it after). Then continue with 1.5 using the migrated primer.

### 1.5 Create local memory (once per project — skip creation of anything migration already produced)
```bash
mkdir -p .claude/memory/{warm,cold/hindsight,scratch} .claude/commands .claude/hooks
```
Then **scan the project** (structure, package/config files, git log, routes, schema — never read `.env` contents) and generate a real, no-placeholder `.claude/memory/primer.md` (HARD LIMIT 150 lines):
```markdown
# <project> — Primer
> Last updated: <ISO> | Lines: <n>/150

## Focus (top 3 priorities)
## State (works / in progress / blocked)
## Active decisions (max 10, dated)
## Conflicts to arbitrate (filled by consolidation)
## Quick map (stack 1 line, entry points, DB — depth: warm/architecture.md)
## Vitals (last commit, tests, deploy)
```
Generate `warm/architecture.md` (detailed map from the scan) and `warm/decisions-log.md` (empty, dated-entry format).

Ensure `./CLAUDE.md` exists and contains (relative imports work on every platform, Windows included):
```markdown
@.claude/memory/primer.md
```
Add to `.gitignore`: `.claude/memory/scratch/`, `.claude/memory/*.bak`, `.claude/settings.local.json`. (Team repo? If teammates shouldn't inherit your memory, gitignore all of `.claude/memory/` — you lose the git time machine, keep the privacy.)

### 1.6 Register the project in the brain
Append to `~/.claude/brain/projects/_index.md`:
`- <name> | <abs path> | <one-liner from scan> | <today>`
Create `~/.claude/brain/projects/<name>.md`: a 15-line card (what it is, stack, status, where its primer lives). Add one line under `## Projects` in `BRAIN.md`.

### 1.7 Install hooks (merge into `.claude/settings.json`, never overwrite existing hooks)
Write the three scripts below **with LF line endings**, then `chmod +x .claude/hooks/*.sh` (no-op on Windows, fine).
Create `.claude/hooks/synapse-brief.sh` (SessionStart — stdout is injected as context):
```bash
#!/bin/bash
M=".claude/memory"
echo "=== SYNAPSE BRIEF $(date '+%F %H:%M') ==="
git status -sb 2>/dev/null | head -3
L=$(ls -t $M/cold/hindsight/*.md 2>/dev/null | head -1)
[ -n "$L" ] && echo "Last consolidated: $(basename $L .md)" && grep -m3 -A2 "## Synthesis" "$L" 2>/dev/null
grep -qE "CONFLICT|MEMORY PRESSURE" $M/primer.md 2>/dev/null && echo "⚠ Conflicts or memory pressure flagged in primer"
S=$(ls $M/scratch/*.md 2>/dev/null | wc -l); [ "$S" -gt 0 ] && echo "📋 $S unconsolidated scratch dump(s)"
B=~/.claude/brain/BRAIN.md
STALE=$(grep -c "^-.*⏳" "$B" 2>/dev/null)
[ "${STALE:-0}" -gt 0 ] && echo "⏳ $STALE stale knowledge entries in global brain"
LIM=$(grep -m1 -o "index-limit: [0-9]*" "$B" 2>/dev/null | grep -o "[0-9]*"); CUR=$(wc -l < "$B" 2>/dev/null)
[ -n "$LIM" ] && [ "${CUR:-0}" -ge $((LIM*9/10)) ] && echo "⚠ Brain index $CUR/$LIM lines — raise /memory-budget or archive"
echo "=== END BRIEF ==="
```
Create `.claude/hooks/synapse-precompact.sh` (PreCompact — save state before context loss):
```bash
#!/bin/bash
M=".claude/memory/scratch"; mkdir -p "$M"
F="$M/precompact-$(date +%FT%H-%M-%S).md"
{ echo "# Pre-compaction snapshot"; git diff --stat 2>/dev/null | tail -8;
  git log --oneline --since="6 hours ago" 2>/dev/null; } > "$F"
echo '{"continue": true, "suppressOutput": true}'
```
Create `.claude/hooks/synapse-end.sh` (SessionEnd):
```bash
#!/bin/bash
mkdir -p .claude/memory/scratch
echo "$(date -Iseconds) | $(git log --oneline -1 2>/dev/null)" >> .claude/memory/scratch/sessions.log
echo '{"continue": true, "suppressOutput": true}'
```
Merge into `.claude/settings.json` (hook commands run through Git Bash on every platform, Windows included — verified; a `matcher` field is not required for these lifecycle events):
```json
{"hooks":{
 "SessionStart":[{"hooks":[{"type":"command","command":"bash .claude/hooks/synapse-brief.sh"}]}],
 "PreCompact":[{"hooks":[{"type":"command","command":"bash .claude/hooks/synapse-precompact.sh"}]}],
 "SessionEnd":[{"hooks":[{"type":"command","command":"bash .claude/hooks/synapse-end.sh"}]}]}}
```
If a hook event is unsupported in the installed version, note it and continue — SYNAPSE degrades gracefully (Part 5).

### 1.8 Install the consolidation script + optional schedule
Create `.claude/memory/synapse-consolidate.sh` (uses `claude -p` — runs on the user's subscription, no API key). Cleanup is deterministic shell, so the consolidation LLM gets **no Bash access at all**:
```bash
#!/bin/bash
set -uo pipefail
R="$(cd "$(dirname "$0")/../.." && pwd)"; N="$(basename "$R")"
M="$R/.claude/memory"; B="$HOME/.claude/brain"; T=$(date +%F); cd "$R"
LH=$(ls "$M/cold/hindsight/"*.md 2>/dev/null | sort | tail -1)
SINCE=$([ -n "$LH" ] && basename "$LH" .md || echo "24 hours ago")
{ echo "# Raw $T (since $SINCE)"; git log --since="$SINCE" --oneline 2>/dev/null;
  git log --since="$SINCE" --name-only --pretty=format:"" 2>/dev/null | sort -u | head -30;
  cat "$M/scratch/sessions.log" "$M"/scratch/precompact-*.md 2>/dev/null; } > "$M/scratch/raw-$T.md"
claude -p "You are SYNAPSE nightly consolidation for project $N. Read $M/scratch/raw-$T.md, $M/primer.md, $M/warm/decisions-log.md. Then: (1) write $M/cold/hindsight/$T.md with ## Synthesis (3 lines), ## Decisions, ## Learnings, ## Problems, ## End state. (2) Surgically update $M/primer.md — focus, state, decisions (max 10), timestamp; HARD LIMIT 150 lines, overflow moves to warm/. (3) Compare new decisions vs decisions-log.md — on contradiction add a CONFLICT entry to primer (do NOT arbitrate). (4) Move decisions-log entries older than 30 days to $M/cold/. (5) GLOBAL PASS: for each reusable learning (technique, research, pattern — NOT project-specific), write/update an L1 note in $B/knowledge/<domain>/ or $B/practices/ with frontmatter (created, verified, stale_after, confidence, sources, origin_project, tags, uses, last_used) and add/refresh its L2 line in $B/BRAIN.md. Mark ⏳ any BRAIN.md entry past its stale_after. SPACED REPETITION: when a note is re-verified unchanged, double its stale_after (cap 365d); when it changed, update it and halve stale_after (floor 30d). Dedupe. Keep BRAIN.md under its index-limit (read the Budget line in its header) — when full, evict the L2 lines with lowest uses + oldest last_used + lowest confidence first (their L1 files stay, greppable); never evict golden:true or recently-used high-confidence entries — if only those remain, do NOT evict: add a '⚠ MEMORY PRESSURE: index N/limit' line to the primer Conflicts section instead, the user decides. Promote hindsight Problems worth remembering into gotcha-tagged brain notes. (6) Refresh $B/projects/$N.md card + last-active in _index.md. (7) Regenerate $B/HOT.md per the Budget line in $B/BRAIN.md — pro: active-project cards (last 30d); deep: + all practices + top-20 L1 notes ranked by (golden first, then uses, last_used); full: + every L1 knowledge note. First line: '> HOT PACK (<level>) | ~<bytes/4>k tokens | rebuilt <date>'. Redaction rule: never store secrets, tokens, .env values, or personal identifiers." \
  --allowedTools "Read,Write,Edit,Glob,Grep" --max-turns 30 >> "$M/consolidation.log" 2>&1
find "$M/scratch" -name "*.md" -mtime +7 -delete 2>/dev/null
rm -f "$M/scratch/sessions.log"
find "$R/.claude" -maxdepth 1 -type d -name "memory-backup-*" -mtime +7 -exec rm -rf {} + 2>/dev/null
git add .claude/memory/primer.md .claude/memory/warm .claude/memory/cold 2>/dev/null
git diff --cached --quiet 2>/dev/null || git commit -m "chore(synapse): consolidation $T" --no-verify >/dev/null 2>&1
```
`chmod +x`. Then ASK the user (do not assume): install a nightly consolidation at 23:30?
**Timezone sanity-check first**: scheduled times are MACHINE-local. Compare the machine clock (`date`) with the user's actual time of day — remote workers and travelers often have a clock set to another country. If they differ, schedule the machine-time slot that matches the user's REAL late evening (e.g. machine on Paris time, user in Bali → 17:30 machine = 23:30 local) and tell them; offer to fix the OS timezone as the cleaner long-term option.
- **macOS/Linux/WSL** — cron:
```bash
(crontab -l 2>/dev/null | grep -v "synapse-consolidate.*$(basename $(pwd))"; \
 echo "30 23 * * * cd $(pwd) && bash .claude/memory/synapse-consolidate.sh") | crontab -
```
- **Native Windows** — Task Scheduler. First resolve Git Bash: run `where bash` in cmd and take the first hit NOT under `System32` or `WindowsApps` (those are WSL stubs); verify the file exists. Create `.claude/memory/synapse-nightly.cmd` with that absolute path:
```cmd
@echo off
cd /d "%~dp0..\.."
"C:\Program Files\Git\usr\bin\bash.exe" -l .claude/memory/synapse-consolidate.sh
```
then register it (quote the /TR path as shown if it contains spaces):
```
schtasks /Create /F /SC DAILY /ST 23:30 /TN "SYNAPSE <project>" /TR "\"<absolute path>\.claude\memory\synapse-nightly.cmd\""
```
- **No schedule (or user declines)**: the user runs `/consolidate` manually every day or two — same result.

### 1.9 Install slash commands
Every file starts with the line `<!-- synapse -->` (ownership marker). Before writing each one: if the target file already exists WITHOUT that marker, do not overwrite it — install yours as `syn-<name>.md` instead and tell the user. On upgrade, freely overwrite files that carry the marker. Create in `.claude/commands/`:
- `brief.md` → "Scope: $ARGUMENTS. If empty → quick brief: read .claude/memory/primer.md, the latest cold/hindsight file, git status; summarize in 5 lines: where we are, blockers, next action. If 'full'/'memory'/'all' → full State of the Union of BOTH memory levels: (project) focus, state, active decisions with dates, unarbitrated CONFLICTs, vitals, last consolidation date; (global brain) knowledge notes per domain with counts and ⏳ stale counts, practices list, known projects with last-active, episodic archive count; (health) limit gauges primer n/150, BRAIN.md n/60, CLAUDE.md n/200, scratch backlog. End with the 3 most useful next actions (e.g. /consolidate, /memory-doctor, refresh a stale note)."
- `recall.md` → "Search query: $ARGUMENTS (grep the query AND 2-3 obvious synonyms — frontmatter tags exist for this). Grep .claude/memory/{warm,cold}/ AND ~/.claude/brain/{knowledge,practices,episodic}/. Synthesize findings with dates and sources. If a knowledge note is past stale_after, say so. If a note answered the question, bump its uses/last_used (reinforcement). If nothing found, say so clearly."
- `decision.md` → "Record decision: $ARGUMENTS. Add to primer 'Active decisions' (dated, max 10) and warm/decisions-log.md (date+context+rationale). Check contradictions vs the log AND vs ~/.claude/brain/practices/ — flag immediately if found."
- `learn.md` → "Promote to global brain: $ARGUMENTS. Write/update an L1 note in ~/.claude/brain/knowledge/<domain>/ or practices/ with full frontmatter (incl. tags synonyms — 'gotcha' for bug+fix; uses: 1; last_used: today; golden: true if the user said golden/best/reference — then ⭐-prefix its L2 line), add its L2 line to BRAIN.md (respect the index-limit from its Budget header — merge, or evict the lowest-uses/oldest/lowest-confidence line if full; if nothing is safe to evict, flag MEMORY PRESSURE and ask the user)."
- `forget.md` → "Forget from memory: $ARGUMENTS. Search BOTH levels (BRAIN.md lines, knowledge/, practices/, episodic/, primer, warm/, cold/). List every match (file + index line) and ask ONE confirmation. Then: remove the L2 index lines, and move matched L1/L0 files to ~/.claude/brain/episodic/attic/<date>-<name> (soft-forget, default) — permanently delete ONLY if the user explicitly said 'delete permanently'. Log one line in warm/decisions-log.md. Report what was forgotten and how to restore it."
- `memory-map.md` → "Generate the visual memory map. Scope filter (optional): $ARGUMENTS. Scan ~/.claude/brain/ (BRAIN.md; knowledge/*/*.md frontmatter: domain, verified, stale_after, confidence, origin_project; practices/; projects/_index.md; episodic/ count) and .claude/memory/ (primer sections, warm/ files, cold/hindsight/ dates, scratch count, consolidation.log tail). Build ONE self-contained dark-theme HTML file at .claude/memory/memory-map.html — inline CSS/JS only, zero external requests. Layout: header with totals and 3 health gauges (BRAIN.md n/index-limit from its Budget header, primer n/150, CLAUDE.md n/200 — green <80%, orange <100%, red ≥100%); two columns: left 🧠 GLOBAL BRAIN — one card per knowledge domain listing each note with freshness badge (✓ fresh / ⏳ stale / ∞ evergreen), confidence dot and origin project, golden notes ⭐-marked and listed first, then a practices card, then a projects card (name, last-active, highlight if inactive >30 days); right 📁 THIS PROJECT — focus list, active decisions with dates, CONFLICT alerts in red, hindsight timeline (last 14 days), scratch/consolidation status. Every note title is a file:// link to its file. Then open it: `start` (Windows) / `open` (macOS) / `xdg-open` (Linux). If that fails or headless, print an annotated ASCII tree of the same data instead."
- `consolidate.md` → "Run bash .claude/memory/synapse-consolidate.sh and report the log tail. If claude -p is unavailable, perform the consolidation steps yourself following the prompt inside the script."
- `memory-budget.md` → "Memory budget: $ARGUMENTS. No args → report: current Budget line, real usage (index n/limit, HOT.md size, total per-session hot-load in tokens ≈ bytes÷4), and the menu with REAL costs computed from this brain's actual files: lean (index only, index-limit 60) · pro (index 150 + project cards) · deep (+ practices + top-20 L1, golden first) · full (total recall — the entire L1 layer; show its real size) · custom N (index-limit override). With args → rewrite the Budget line in BRAIN.md's header, regenerate HOT.md immediately per the new level (see consolidation step 7), and add/remove the HOT.md import in ~/.claude/CLAUDE.md (absolute path on Windows). If the new level is SMALLER than current usage, delete nothing — entries leaving the hot pack stay on disk, always recoverable via /recall. Storage is unlimited at every budget; only the per-session auto-load changes."
- `memory-doctor.md` → "Audit both levels, score /100: primer <150 lines; CLAUDE.md <200; BRAIN.md within its index-limit (Budget header); primer updated <48h; unarbitrated conflicts; scratch dumps >48h; consolidation ran <24h (if scheduled); stale ⏳ entries; decisions-log entries >30d not rotated; registry paths that no longer exist; index integrity (BRAIN.md/primer L2 lines pointing to missing files, orphan L1 notes with no L2 line); dormant notes (uses ≤1 AND last_used >90d, never golden) → suggest moving to episodic/attic/; HOT.md consistent with the Budget line and rebuilt <48h (regenerate if not); golden count ≤10. Report, then fix what is auto-fixable."

### 1.10 Commit
```bash
git add CLAUDE.md .claude/ .gitignore && git commit -m "feat(synapse): perpetual memory + shared brain"
```

---

## Part 2 — Memory protocol (every session, every project, every agent)

**Already auto-loaded** via imports: `BRAIN.md` (global index) + `primer.md` (project working memory) + the SessionStart brief. Do not re-read them; they are in context. (Portable mode: read those two files at session start yourself — Part 7.)

### Routing — where does new information go?
When you learn or produce something durable, route it:
1. **Project-specific** (this codebase's state, decisions, bugs) → local: primer (L2) / warm (L1) / cold (L0).
2. **Reusable across projects** (research findings, framework patterns, SEO/design/tooling knowledge, best practices) → global: `brain/knowledge/<domain>/` or `brain/practices/` (L1) + one line in `BRAIN.md` (L2). Full heavy version, if any → `brain/episodic/` (L0).
   **A painful bug and its fix → ALWAYS a brain note tagged `gotcha`**, even if it feels project-specific — the same wall exists in other projects. Six months later, in a different repo, the agent must remember how it was solved and never hit that wall again.
3. **Both?** Store once in the global brain, reference it from the project primer. Never duplicate content.
4. **Secrets, tokens, credentials, .env values, personal identifiers → NOWHERE. Ever.** This is non-negotiable and applies even if the user asks casually; confirm explicitly before storing anything sensitive.

Example: user says "analyze the latest Google core updates". You research, deliver — then write `brain/knowledge/seo/google-core-updates.md` (L1 summary + sources, `stale_after: 90d`) and index it. Next month, in a *different* project, the L2 line is already in context: you read the note instead of re-researching — and if it's ⏳ stale, you say so and offer to refresh.

### Knowledge note format (global brain)
```markdown
---
domain: seo            # folder = domain taxonomy, create as needed
created: 2026-07-04
verified: 2026-07-04    # bump when re-checked
stale_after: 90d        # or "never" for evergreen
confidence: high        # high | medium | low
sources: [urls or "session research"]
origin_project: <name>
tags: [synonyms, aliases, related-terms]   # widen /recall grep hits; use 'gotcha' for bug+fix notes
uses: 1                 # bumped on every real use (reinforcement)
last_used: 2026-07-04
golden: false           # ⭐ exemplar — never evicted, always in the hot pack (cap ~10)
---
# <Title>
<1 page max. Facts, not prose. Link L0 in episodic/ if one exists.>
```

### Cross-project observation — READ-ONLY
`projects/_index.md` lists every known project. When useful ("how did we solve auth in project X?"), you MAY read that project's `CLAUDE.md`, `primer.md`, `warm/`, and code **for reference**. You MUST NOT write, edit, or run anything outside (a) the current project tree and (b) `~/.claude/brain/`. State it when you borrow: "Pattern observed in <project>."

### Reinforcement — memory strengthens with use
When a brain note actually helps (you read it and it answered the question), bump its frontmatter in one surgical Edit: `uses` +1, `last_used: <today>`. Consolidation ranks the BRAIN.md index by these signals: frequently-used knowledge keeps its line, never-used notes become eviction candidates (their L1 file always remains, greppable). What fires, wires.

### ⭐ Golden references — the best of what you've built
The user (or you, with their OK) can mark a note as `golden: true` — the exemplar to imitate: the site with the best SEO/GEO performance, the auth pattern that never failed, the pipeline that just works. Golden notes get a ⭐ prefix on their L2 line, are NEVER evicted or archived, ride in the hot pack from `pro` up, and are the default starting point whenever building something similar ("basing this on ⭐ <note>, your best-performing setup"). Keep gold rare — cap ~10; gold that's everywhere is gold nowhere.

### Session triage (deep/full budgets) — remember like a human
With a big hot pack, most of the brain is in context at session start. Triage it consciously: identify the handful of notes relevant to today's task and work from them; the rest you have SEEN — you now know what you know, which is the point — set it aside and don't re-read it from disk. Seeing a note and deciding "not needed today" is not waste: that's exactly how human recall works.

### Quick capture during work
- User jots a quick note mid-work (`# <note>` prefix or plain "note this") → route it immediately per the rules above; don't wait for consolidation.
- Meaningful choice made → suggest or use `/decision`.
- Reusable insight discovered → use `/learn` (or route it yourself per the rules above; tell the user in one line what you stored and where).
- User wants something gone from memory → `/forget` (soft by default, restorable from the attic).
- User arbitrates a CONFLICT → record the resolution via `/decision` and delete the CONFLICT entry from the primer.
- Long, dense session (context likely to compact soon)? Proactively dump a 5-line state note to `scratch/` — don't rely on the PreCompact hook alone.

### Size discipline (hard limits at a chosen size — enforce, don't apologize)
The index limit comes from the Budget line in BRAIN.md's header (`lean` 60 · `pro`/`deep`/`full` 150 · `custom N`); primer ≤150 · CLAUDE.md ≤200 · knowledge note ≤1 page always. What distinguishes `pro`/`deep`/`full` is the HOT.md pack depth, not the index size. **Storage on disk is UNLIMITED at every budget** — the budget only caps what auto-loads per session. Overflow moves DOWN the gradient (L2→L1→L0), never accumulates in hot files. The Projects section of BRAIN.md lists only projects active in the last 30 days (the full registry lives in `projects/_index.md`).
**Never silently evict under real pressure**: if the index is full of fresh, used, high-confidence entries (nothing is safe to evict), write `⚠ MEMORY PRESSURE: index N/limit` in the primer's Conflicts section instead. At the next session, offer the user the choice: raise the budget (`/memory-budget`), archive least-used entries (always recoverable via `/recall` — files never leave the disk), or merge domains.

---

## Part 3 — Consolidation (the sleep cycle)

Nightly (cron / Task Scheduler) or manual (`/consolidate`), per Part 1.8. It covers everything since the LAST hindsight (no gaps if you skip days), then: writes the period's hindsight, surgically refreshes the primer, detects contradictions (project level AND vs global practices), rotates 30-day-old decisions to cold, promotes reusable learnings to the global brain, marks stale knowledge ⏳, applies spaced repetition to re-verified notes, re-ranks the index by reinforcement (uses/last_used), dedupes, refreshes the project card; then the script deterministically cleans scratch (>7 days), sessions.log and expired backups, and commits memory to git (memory history = time machine: `git log -- .claude/memory/`).

---

## Part 4 — Multi-machine sync (optional, ask before setup)

The global brain is plain files — make it a git repo to carry your brain across machines:
```bash
cd ~/.claude/brain && git init && git add -A && git commit -m "brain init"
# user adds a PRIVATE remote; then per machine:
git pull --rebase && git push
```
Warn the user: the brain may contain business knowledge → **private repo only**. Add a `sync` step to the consolidation script only if the user asks.

---

## Part 5 — Degraded mode & troubleshooting

- **No hooks support** → skip hooks; the `@imports` still auto-load memory; brief manually via `/brief`.
- **No scheduler (or user declined)** → `/consolidate` manually every day or two. Everything else identical.
- **`claude -p` unavailable in consolidation context** → do the consolidation steps yourself interactively when `/consolidate` is invoked.
- **Import not loading** → verify the import lines exist outside code blocks in the respective CLAUDE.md files. On Windows, `@~/...` NEVER loads (silent failure) — replace with the absolute forward-slash path (see 1.3). Empirical probe: `claude -p "quote the first line of BRAIN.md from context" --allowedTools ""` — if it can't, the import is broken.
- **Hook scripts failing on Windows** → almost always CRLF line endings; rewrite the `.sh` files with LF. If Git Bash is missing entirely, hooks fall back to PowerShell and the `.sh` hooks won't run — imports and slash commands still work; installing Git for Windows restores full SYNAPSE.
- **Brain bloated / adherence dropping** → `/memory-doctor`, then enforce the gradient: evict L2 lines whose L1 files exist, archive cold knowledge, split domains.
- **Uninstall** → remove the two `@import` lines; delete `~/.claude/brain/` and `.claude/memory/` (offer to export first); remove hooks entries and SYNAPSE files from `.claude/commands/`; remove the cron line or `schtasks /Delete /TN "SYNAPSE <project>" /F`; delete `~/.claude/skills/synapse/`.

---

## Part 6 — What to tell the user after bootstrap (keep it to this)

"SYNAPSE v<version from this file's SYNAPSE_VERSION marker> installed: project memory auto-loads every session, global brain shared across all your projects, [nightly cron / nightly Task Scheduler / manual] consolidation. Commands: /brief (+ 'full' for the complete memory report) /recall /decision /learn /forget /memory-map (visual dashboard) /memory-budget (resize what auto-loads) /consolidate /memory-doctor. Memory budget: [chosen profile] — storage itself is unlimited. Drop this same file in any other project — it joins the brain network automatically. It also works with other AI agents (portable mode, Part 7) — same brain." If a migration ran, add one line: "Your previous memory system was absorbed — X decisions, Y session archives, Z learnings promoted to the global brain. Backup kept 7 days at .claude/memory-backup-<date>/."

---

## Part 7 — Portable mode: running SYNAPSE on other AI agents

SYNAPSE is files + a protocol — nothing about the memory itself is Claude-specific. Any agent that can read/write files (and ideally run shell commands) can operate the SAME brain. One brain, every agent: Claude Code, Cursor, Codex CLI, Gemini CLI, Windsurf, aider… all read and write the same folders, interoperably.

**If you are an AI agent reading this and you are NOT Claude Code, install like this:**
1. Keep a copy of this file at `~/.claude/skills/synapse/SKILL.md` — the canonical shared location, used even when Claude isn't installed, so every agent on the machine references one copy. (No home-folder access? Put it at the project root as `SYNAPSE.md` and adjust paths below.)
2. Create the same structures as **1.2** (global brain) and **1.5** (project memory, with a real primer from a real project scan). Skip anything that already exists — you may be joining a brain another agent built. Never wipe or reformat existing memory.
3. **Auto-load replacement** — your platform has no `@import`. Add this block to your instruction file — `AGENTS.md` (Codex CLI; also read by several other agents), `.cursor/rules/synapse.mdc` (Cursor), `GEMINI.md` (Gemini CLI), `.windsurf/rules` (Windsurf), or your platform's equivalent:
   > SYNAPSE memory: at session start, read `~/.claude/brain/BRAIN.md`, `~/.claude/brain/HOT.md` (if present) and `.claude/memory/primer.md`. Full protocol: `~/.claude/skills/synapse/SKILL.md` Part 2 (routing, hard limits, freshness, redaction). Commands: when the user says "synapse <brief|recall|decision|learn|forget|map|budget|consolidate|doctor> [args]", execute the matching command spec from Part 1.9 of that file.
4. **Slash commands become trigger phrases**: `synapse brief`, `synapse brief full`, `synapse recall pricing`, `synapse map`… — run the corresponding 1.9 spec verbatim (they are written agent-agnostically).
5. **Hooks** (auto-brief, pre-compaction dump, session log) exist only where the platform supports lifecycle hooks or rules. If yours does, wire the three 1.7 scripts; if not, the brief simply runs when the user asks — everything else is identical.
6. **Consolidation**: if your platform has a headless CLI mode (an equivalent of `claude -p`), reuse the 1.8 script with that binary swapped in; otherwise run it interactively when the user says `synapse consolidate` — follow the prompt embedded in the script yourself, then apply the deterministic cleanup steps (delete scratch >7 days, sessions.log, expired backups).
7. **Same iron rules as everywhere** (Part 2): never write outside the current project and `~/.claude/brain/`; cross-project is read-only; the redaction rule (no secrets, ever) applies to you in full.

Result: full memory, shared with every other SYNAPSE-running agent on the machine. Only the automation depth differs by platform — the memory, formats and guarantees never do.

---

## Part 8 — Field manual (what living with SYNAPSE looks like)

**Day 1 — install.** You drag this file into Claude Code inside `shop-app/`. Under a minute later: brain created, project scanned into a real primer, hooks live, all commands installed, 3-line report. Nothing else about your workflow changes.

**Day 9 — a decision.** You pick Supabase Auth over Clerk. `/decision Supabase Auth over Clerk — pricing scales badly`. Logged in primer + decisions-log, automatically checked for contradictions against past decisions and global practices.

**Day 10 — another project.** In `client-site/` you ask about checkout patterns. The L2 line from `shop-app`'s research is already in context; the agent reads the L1 note instead of re-researching, says so — "Per brain note stripe-checkout-patterns (verified 9 days ago)…" — and bumps the note's `uses` count. Knowledge compounds across projects, and what gets used gets stronger.

**Day 40 — freshness.** The session brief warns: "⏳ 2 stale knowledge entries in global brain". `/brief full` shows which ones. You say "refresh the SEO one" → re-verified, `verified:` bumped, ⏳ cleared. Your memory never silently rots.

**Anytime.** `/memory-map` opens the visual dashboard of everything you know. `/recall auth` answers "have we solved this before?" across ALL projects. `/forget old-client` retires knowledge cleanly (restorable from the attic). `/memory-doctor` scores memory health and self-repairs.

---

## Part 9 — FAQ, design rationale & privacy model

**FAQ (answer from here when the user asks):**
- *Where is my data?* Plain markdown on your machine: `~/.claude/brain/` (global) + `<project>/.claude/memory/` (local). Nothing leaves the machine unless YOU git-push it (Part 4).
- *What does it cost in context?* Your choice — that's the memory budget, and you see the real price before choosing: lean ≈1–2k tokens/session (index only) · pro ≈3–8k (+ project cards) · deep ≈10–40k (+ practices + top-20 notes) · full = **total recall**, the entire L1 brain in context every session (typically 50–150k — for those who'd rather pay tokens than ever re-explain anything). Modern 1M-context models absorb even `full` easily: they scan it, keep what today's task needs, set the rest aside (see Session triage). **Storage on disk is unlimited at every budget.** Resize anytime with `/memory-budget`; when the index fills up with knowledge that's all fresh and in active use, SYNAPSE never silently drops it — it flags MEMORY PRESSURE and asks you: raise the budget, or archive (archived = out of the hot load, still on disk, still findable via /recall).
- *Several machines?* Part 4 — the brain becomes a private git repo you pull/push.
- *Team?* Memory is per-human by default (1.5 gitignore option). A shared team brain = sharing the brain folder as a repo — workable, but agree on who runs consolidation.
- *Other AI agents?* Part 7. Same brain, shared, interoperable.
- *How do I uninstall?* Part 5, last bullet. Export is offered first; deleting the two folders removes everything.
- *Which models work?* Any agent/model that follows markdown instructions can run the protocol; consolidation quality scales with model quality.
- *Is my memory ever sent anywhere?* Only into your own agent's context at session start (that is the point). SYNAPSE itself calls no external service, ever.

**Design rationale (invariants — preserve them when modifying SYNAPSE):**
- **Plain files over a database**: greppable, diffable, git-versionable, human-editable, agent-agnostic, zero dependencies, zero lock-in.
- **Hard line limits — at a size the user chooses — force compression**: that's what keeps memory USEFUL. A memory that grows unbounded stops being read; overflow moves down the gradient instead. The budget scales the ceiling (lean → full total-recall), never removes it — and the user always sees the real token price before choosing.
- **Freshness (`stale_after` / ⏳) because knowledge rots** — an agent confidently citing March pricing in July is worse than one saying "let me re-check".
- **Reinforcement (`uses`/`last_used`) because the index must earn its 60 lines**: memory self-ranks by real utility, not by write date. What fires, wires; what never fires moves down the gradient.
- **Spaced repetition on `stale_after` because stability earns trust**: knowledge that survives re-verification gets re-checked less often — the memory learns its own decay rate, like flashcards.
- **Consolidation is nightly and boring on purpose**: memory maintenance shouldn't tax working sessions.
- **Conflicts are flagged, never auto-arbitrated**: the human owns the truth.

**Privacy & safety model (non-negotiable, all platforms):**
- No secrets, tokens, keys, .env values, or personal identifiers in ANY memory file — even if asked casually; confirm before storing anything borderline.
- Cross-project observation is READ-only; writes only in the current project + `~/.claude/brain/`.
- The consolidation LLM runs with Read/Write/Edit/Glob/Grep only — no shell access.
- Memory files belong to the user: readable, editable, deletable at will.
