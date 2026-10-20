---
name: daily-pulsar-summarizer
version: 1.5.0
author: Hermes Agent
license: MIT
description: "End-of-day summarizer that reads ALL pulse digests from the daily digest and produces a structured 'PULSAR' report — synthesized, scannable, under 2000 chars. Adds actionable items to the unseen backlog."
metadata:
  hermes:
    tags: [pulsar, digest, summary, end-of-day, cron, reporting]
    triggers: [pulsar, end-of-day-review, daily-summary, pulse-digest-summary, the operator-daily-brief, daily-digest-synthesis]
    related_skills: [intelligence-pulse, quiet-hours-pulse-digest, blogwatcher]
---

# Daily Pulsar Summarizer

Run at end-of-day (ET) to synthesize all pulse outputs into one concise PULSAR report.

## Pre-flight

1. Determine the correct digest file:
   ```bash
   TODAY=$(TZ='America/New_York' date +%Y-%m-%d)
   DIGEST_DIR="${MY_REPOS}/_project/daily-digest"
   DIGEST_FILE="${DIGEST_DIR}/${TODAY}.md"
   ```
   **⚠️ Timezone pitfall:** The system clock may differ from America/New_York. `TZ='America/New_York' date` returns the ET date — use this, not the raw `date` output, to determine which digest is "today's."
   
   **⚠️ Digest may not exist yet:** If today's digest doesn't exist, list the directory and fall back to the most recent file (check if it was generated within the last 36h). The digest is typically created after midnight ET when the last pulse fires.

2. Check digest existence:
   ```bash
   ls -la "$DIGEST_FILE" 2>/dev/null || ls -la "$DIGEST_DIR" | tail -10
   ```

### Zero-Pulse-Day Handling

If `$DIGEST_FILE` doesn't exist, start by checking the most recent digest:

**Case A — Fresh previous-day digest (last modified <24h ago):** The digest for the prior ET day exists and was written within the last 24 hours. Pulses DID fire recently — they just haven't started today's cycle yet. **Do NOT report "0 pulses fired."** Instead note: "Today's digest not yet created — reading prior day's digest ([date])." This is normal for early morning ET before the first pulse fires.

**Case B — Stale previous-day digest (last modified 24-48h ago — one missed day):**
- **No pulses ran today.** This is itself a finding to report in the summary.
- Fall back to yesterday's digest for data. Note in the PULSAR header: "0 pulses fired today."
- Check git activity (see below) — if zero commits across ALL repos AND zero user sessions, the system is genuinely quiet.
- **Do not emit SILENT** — a zero-pulse day still warrants a short report with context.
- If git activity exists despite zero pulses, flag it as subagent/cron work keeping the lights on while the operator is absent.

**Case C — Multi-day pulse gap (last digest >48h old — 2+ missed days):**
- **This is not a normal gap.** Escalate the finding. The cron infrastructure may be down, the daily-digest pipeline stalled, or pulses are erroring silently. Do NOT start with "Weekend pause" framing unless it's Saturday AND the last digest was from Friday (normal weekend). If it's >48h regardless of day, it's a gap.
- **Elevate git scan to primary data source.** The pulse pipeline is blind — your only signal is what repos the user touched directly.
- In the PULSAR header, lead with: "⚠️ Pulse pipeline silent [N] days — last digest [date]."
- If git shows human-authored commits during the gap (like the operator shipping code on website-landlord while pulses were dark), flag the discrepancy: the pipeline missed real work. This is a higher-severity finding than the gap itself.
- Check container fleet health (`docker ps`) to rule out infrastructure collapse.
- **Do NOT default to "Weekend pause"** — verify day-of-week. Use `date +%u` (1=Mon, 7=Sun). Only use "Weekend pause" if the gap is Fri→Sat/Sun and <72h of silence.

**How to distinguish:** Check the most recent digest file's modification time:
```bash
stat -c "%y" "$DIGEST_DIR/$(ls -1t "$DIGEST_DIR" | head -1)"
```
If mtime is <24h ago → Case A (fresh). If 24-48h ago → Case B (one missed day). If >48h ago → Case C (multi-day gap).

### P0 Deep Check (14-day window)

Always check P0 repos even when the digest covers them — they often go cold between pulses:

```bash
# ⚠️ Use cd + git, NOT git -C. On MSYS/Windows, git -C can return exit code 128
# when a repo has a .git.broken.* directory alongside its .git dir.
for repo in ${MY_REPOS}/constructManage ${MY_REPOS}/website-landlord ${MY_REPOS}/bookends; do
  if [ -d "$repo" ]; then
    commits=$(cd "$repo" && git log --oneline --since="14 days ago" 2>/dev/null | wc -l)
    last=$(cd "$repo" && git log -1 --format="%as %s" --since="30 days ago" 2>/dev/null || echo "(none in 30d)")
    echo "  $(basename $repo): $commits commits (14d), last: $last"
  fi
done
```
If a P0 repo shows 0 commits in the last 7 days even though it had a burst in the prior window, flag the **stall-just-before-shipping** pattern.

### Cross-Repo Freeze Detection (same-date stall)

Also check for multi-repo same-date freezes — a systemic freeze across 3+ repos is worse than a single cold project:

```bash
# ⚠️ Use quoted Windows-native path — MSYS /c/ prefixes fail when passed to Windows Python
python "${USER_HOME}/AppData/Local/hermes/skills/productivity/intelligence-pulse/scripts/cross_repo_freeze_check.py"
```

Key flags:
- **Multi-repo stall**: >=3 repos frozen on the same date AND that date is >STALL_DAYS ago
- **Pre-migration freeze**: stalled repos whose commit messages contain "pre-migration" or "prep:" — the user attempted a migration, hit friction, and abandoned everything at once
- If detected, escalate the PULSAR wording: "N repos frozen since [date] — likely migration wall, not project-specific stall"
- Fallback if script not available: `for d in ${MY_REPOS}/*/; do repo=$(basename "$d"); last=$(cd "$d" && git log -1 --format="%as" 2>/dev/null || echo "none"); echo "$repo:$last"; done | sort -t':' -k2`

### Git Activity Scan (48h)

Check ALL repos for activity — catches scope creep on non-P0 projects and confirms user absence:

```bash
ACTIVE_REPOS=""
for d in ${MY_REPOS}/*/; do
  repo=$(basename "$d")
  if [ -d "${d}.git" ]; then
    commits=$(cd "$d" && git log --oneline --since="48 hours ago" 2>/dev/null | wc -l)
    if [ "$commits" -gt "0" ]; then
      latest=$(cd "$d" && git log -1 --format="%as %an: %s" 2>/dev/null)
      ACTIVE_REPOS="$ACTIVE_REPOS\\n  $commits in $repo: $latest"
    fi
  fi
done
echo -e "$ACTIVE_REPOS" || echo "  Zero commits in last 48h across all repos."
```

### User Activity Check

Cross-reference git authorship with session_search to determine if the user is present:

```bash
session_search()  # browse mode — list recent sessions with sources
```
If ALL recent sessions are `source: cron` and ALL git commits are from subagents, flag user absence in the PULSAR. Days-since-last-user-session goes in the system health line: "the operator last seen [date]."

## Step 1: Parser summary

```bash
python "${DIGEST_DIR}/../scripts/unseen-backlog.py" digest-summary "$DIGEST_FILE" | \
  python -c "
import sys, json
d = json.load(sys.stdin)
print(f'Total sections analyzed: {d[\"sections\"]}')
by_p = {}
for i in d['items']:
    by_p.setdefault(i['priority'], []).append(i['header'])
for p, items in sorted(by_p.items()):
    print(f'  [{p.upper()}]: {len(items)} items')
"
```

## Step 2: Read raw digest

Read the full digest to extract actual substance — don't rely only on the parser. **The parser's category/priority assignments are heuristic and regularly wrong** (e.g., Sentry clean sweep gets classified as `fyi/bizdev` when it's `high/project` or `high/infra`; Forge pipeline overhauls get `fyi/bizdev` when they're `high/infra`). Cross-reference every `priority` and `category` the parser emits against your own reading of the raw content before adding items to the backlog.

```bash
read_file "$DIGEST_FILE"
```

## Step 3: Categorize every entry

Go through each pulse entry and group:

- **🚨 MUST SEE** — critical/high priority items:
  * Anything marked 🔴 in the original pulse
  * Diverging dependencies, software bloat, drift
  * P0 projects going cold
  * Infrastructure issues (disk, GPU, crash-looping containers)
  * BizDev pipeline stalling (0 outreach, 0 contracts won)

- **🎯 ACTION ITEMS** — things to do:
  * Any "recommend" or "needs" or "should" statements
  * Blocked workflows needing human action
  * Rebase or merge decisions needed
  * P0 items one commit from shipping

- **💡 OPPORTUNITIES** — leads and improvements:
  * BizDev leads from pulse scans
  * Things "worth looking at" or "could improve"
  * New tools, repos, or approaches surfaced

### Step 3.5: Process Recruiter Email & Job Leads

If any digest entry mentions recruiter emails, job leads, or C2C opportunities (especially from the operator's Pulse or Manual Pulse entries), **these are cash-generation leads, not FYI.** Do not bury them in 💡 OPPORTUNITIES.

- A single C2C placement at $150/hr changes the month. Recruiter emails go cold in 48-72h.
- Flag them under 🚨 MUST SEE or 🎯 ACTION ITEMS with the company/role detail
- Add to backlog with `priority=critical` or `high`, `category=bizdev`
- Include explicit flag: "Classify through Job Agent before it goes cold"
- Reference the specific company and role so the operator can act without re-researching

Do NOT treat these as routine backlog items. Cash-generation leads get priority placement in the PULSAR + urgent backlog tags.

## Step 4: Add unseen items to backlog

For each actionable/critical item (including recruiter leads from Step 3.5), add to the unseen backlog:

```bash
SCRIPTS="${MY_REPOS}/_project/scripts/unseen-backlog.py"
TAG="daily-digest/${TODAY}.md"
python "$SCRIPTS" add "Daily Pulsar" <priority> <category> "<concise summary>" "$TAG"
```

**Priority levels:** critical, high, medium, low, fyi
**Categories:** action, important, improvement, infra, bizdev, intel, project

**Run the stats command after every batch of adds to confirm the total is still manageable:**

```bash
python "$SCRIPTS" stats 2>/dev/null
```

If unseen count exceeds 80, trigger the backlog-health escalation in Step 6 instead of adding more items.

### Step 4.5: Backlog Dedup Pre-Check (REQUIRED)

**⚠️ Before adding ANY item, check if a near-identical item already exists in the unseen backlog.** The backlog accumulates the same findings across consecutive days (P0 freeze, BizDev 0 outreach, brain.md crash window, etc.), and adding them again each day is the root cause of backlog bloat. A backlog full of duplicates is worse than no backlog — every duplicate buries the genuinely new signals.

Run this pre-check before every `add`:

```bash
# Quick keyword search in existing unseen backlog
python "$SCRIPTS" list --unseen-only 2>/dev/null | grep -i -c "YOUR-KEYWORD-HERE"
```

Replace `YOUR-KEYWORD-HERE` with the core theme of what you're about to add:

| If adding about... | Check for... | If count >= N, SKIP the add |
|---|---|---|
| P0 freeze / Bookends cold / ConstructManage cold | `P0 freeze\|P0 cold\|Bookends.*cold\|Construct.*cold` | >= 2 (already documented) |
| BizDev 0 outreach / stalled / 0 wins | `BizDev.*outreach\|0 outreach\|0 wins\|pipeline stall\|Cash generation.*bottleneck` | >= 3 (escalation framing handles this) |
| brain.md crash / crash window / uptime limit | `brain.md.*(crash|uptime|window|Dockerization)` | >= 2 — uptime is a moving target, track it in the PULSAR text, not backlog entries |
| GPU VRAM pressure / VRAM % | `GPU VRAM\|VRAM.*pressure\|GPU.*critical` | >= 1 (every gram counts — one entry is enough) |
| YT Animation sprawl / ADHD / infra-escape | `YT Animation.*sprawl\|ADHD.*sprawl\|infra.*escape\|P2.*effort` | >= 2 |
| Forge divergence / rebase needed | `Forge.*diverg\|rebase.*need\|delta.*unshipped` | >= 2 |
| Traefik / acme.json empty | `acme.json\|Traefik.*cert\|LetsEncrypt` | >= 1 (one is enough for this chronic issue) |
| Recruiter email / C2C lead / job lead | `recruiter\|C2C\|Job Agent\|[Cc]ash.*gen.*lead` | >= 1 per company (dedup by company+role, not source) |
| Roadmap stale / priorities outdated | `roadmap.*stale\|priorit.*stale\|monthly-priorities` | >= 2 |
| headroom-ai upgrade | `headroom-ai\|headroom.*upgrade\|headroom.*stuck` | >= 1 per version (if upgraded, don't add another) |

**After skipping the add, update the PULSAR text instead.** The escalation framing (Step 6) replaces the need for a new backlog entry — escalate language in the summary without bloating the backlog.

**Do NOT add items whose theme overlaps with an existing item added in the SAME PULSAR run.** If you already added "Fix commits lost to hard reset" and are about to add "Fix-commit-reset narrative continues", merge into one entry. Duplicate adds in the same pulse are worse than cross-day dupes because they happen within seconds of each other.

**Do NOT add items that are resolutions of problems flagged in prior backlog entries.** E.g., "brain.md at 107h — old crash window defeated" resolves a previously-added critical item. Adding a resolution entry doubles the backlog without helping the operator act. Instead, the PULSAR's 🚨 MUST SEE section can note which prior criticals are now resolved.

## Step 5: Check existing backlog for critical unread items

```bash
python "$SCRIPTS" list --unseen-only --priority=critical
```

Count totals for the summary footer using the stats command (cleaner, no pipe-fragility):

```bash
python "$SCRIPTS" stats 2>/dev/null
```

**⚠️ `stats` can fail silently.** Observed: returns exit code 2 with zero stdout when JSON is malformed. Fallback:

```bash
python -c "
import json
p = '$SCRIPTS/../../daily-digest/unseen-backlog.json'
with open(p) as f: d = json.load(f)
items = d.get('items', d.get('backlog', []))
unseen = sum(1 for i in items if not i.get('seen', i.get('acknowledged', False)))
critical = sum(1 for i in items if not i.get('seen', i.get('acknowledged', False)) and i.get('priority','') in ['critical','high'])
print(f'Total: {len(items)}, Unseen: {unseen}, Critical+High unseen: {critical}')
"
```

### Step 5.0: Backlog Stale-Items Cross-Check (REQUIRED)

**Critical items in the backlog often reference problems that were resolved in recent digest events.** Before re-flagging a backlog critical in the PULSAR, check whether the most recent digest contains event entries that resolve the issue.

**When to suppress a backlog critical:**
- If the most recent digest reports an issue as resolved (e.g., brain.md crash pattern defeated, rebase completed, Poste ClamAV fixed), do NOT re-flag the corresponding backlog critical as a current concern
- Instead, add a single line in the PULSAR: "Previously flagged: [N] critical backlog items now resolved by recent events"

**Detection command:**
```bash
DIGEST_FILE="${MY_REPOS}/_project/daily-digest/${TODAY}.md"
grep -iE "FIXED|REACHED|BROKEN|RESOLVED|COMPLETED|DEFEATED|RECOVERED" "$DIGEST_FILE" 2>/dev/null | head -5
```

**Common stale-backlog patterns:**
- brain.md crash window → "REACHED 119h milestone" / "DEFEATED crash pattern" → suppress
- rebase divergence → "divergence collapsed to 0" / "stasis broken" → suppress
- Poste ClamAV → "RECOVERED" / "running [N]h healthy" → suppress
- Authentik/oauth2-proxy → "Up N days (healthy)" → suppress
- job-agent OOM → "Up N days (healthy)" → suppress

**Do NOT suppress if resolution language is hedging** (e.g., "downgraded to routine monitoring" — could recur; "temporarily mitigated" — band-aid).

**Example PULSAR line after suppressing:**
```
Previously flagged criticals now resolved: brain.md crash (119h, old pattern defeated), rebase divergence cleared, Poste ClamAV fixed (17h+ healthy)
```

### Step 5.1: Cross-Reference Backlog Criticals Against Open Loops Register

**⚠️ The backlog accumulates warnings across days, but open-loops.json items get resolved without the backlog knowing.** Before reporting any backlog critical as a current issue, check if it references an open loop that has since been closed.

```bash
OPEN_LOOPS="${MY_REPOS}/_project/04-shared-memory/playbooks/open-loops.json"
# Check if the open-loops register has recently-closed items
python -c "
import json
with open('$OPEN_LOOPS') as f:
    data = json.load(f)
loops = data if isinstance(data, list) else data.get('loops', [])
for loop in loops:
    if loop.get('status') == 'closed' and loop.get('closed'):
        print(f\"  ✅ {loop['id']}: CLOSED {loop['closed']} — {loop['description'][:60]}\")
"
```

**What to do when resolved:** If a backlog critical item (e.g., "OL-001 overdue since June 10") matches a closed open loop, **do NOT re-flag it.** Either:
- Omit it from the 🚨 MUST SEE section entirely (if all instances are resolved)
- Add a note: "(OL-001 now closed June 16 — previously flagged as overdue)" in a separate resolved-items line or at the bottom of the section

This prevents the PULSAR from reporting stale overdue warnings that make the digest look unresponsive.

**Common scenarios where this matters:**
- OL-001 (Model Gateway Sprint review) was overdue June 10 but was marked closed June 16 — still appears in backlog criticals from June 10-16
- OL-002 (Quarterly tax payment) was due June 12 but closed June 16 — same stale-warning pattern
- Both are in the backlog as critical/overdue but are actually resolved. The PULSAR that ignores this sounds like it's repeating old news.

### Step 5.2: Backlog Structural Integrity Check (REQUIRED)

**Backlog entries can be structurally corrupted** — empty headers, missing sources, blank descriptions. This has been observed in production (156 entries with `header: "?"` and no source). A corrupted entry provides zero value and inflates the count.

Detection:
```bash
python -c "
import json
with open('${MY_REPOS}/_project/daily-digest/unseen-backlog.json') as f:
    d = json.load(f)
items = d.get('items', d.get('backlog', []))
if isinstance(items, dict):
    items = list(items.values())
bad = [i for i in items if i.get('header','?') == '?' or not i.get('source_ref','')]
if bad:
    print(f'BACKLOG CORRUPTED: {len(bad)}/{len(items)} entries have empty headers or sources')
    for i in bad[:5]:
        print(f'  {i.get(\"priority\",\"?\")}/{i.get(\"category\",\"?\")}: header={i.get(\"header\",\"?\")} source={i.get(\"source_ref\",i.get(\"source\",\"?\"))}')
    print(f'  (showing first {min(5,len(bad))} — flag full set in PULSAR)')
else:
    print('Backlog structure OK')
"
```

**What to do when corrupted:**
- **Do NOT add items to a structurally corrupted backlog.** Adding to a broken store just compounds the problem. Wait for a cleanup pass.
- Flag the corruption prominently in the PULSAR: "Backlog: [N] entries structurally corrupted (empty headers/sources) — needs a purge cycle."
- Set the backlog count in the PULSAR footer to 0 or "N corrupted — not tracked" since the numbers are unreliable.

**Root cause of empty entries:** The `unseen-backlog.py add` command was called with missing or truncated parameters (likely from a script invocation that dropped arguments). Prevention: always pass a real header string when calling `add`.

Parse the output for: total items, breakdown by priority. The output shape is:
```
[Backlog] Stats — 85 total, 85 unseen, 0 seen
  By priority: {'critical': 42, 'high': 31, 'medium': 9, 'fyi': 3}
```

**⚠️ Counting via `stats` vs `list`:** The `stats` command is preferred for summary totals — it returns a clean one-liner with all counts. The `list` command outputs Unicode bullets that don't pipe cleanly through MSYS `wc -l`. Use `stats` for the summary footer numbers.

**⚠️ Backlog health check — all-unseen threshold:** Run `stats` and check if `unseen == total` (i.e., every backlog item is unread). When ALL items are unseen, the backlog is growing unchecked and becoming noise. **Critical-mass threshold:** If unseen >= 50 items AND all-unseen percentage is 100%, flag in the PULSAR: "Backlog: [N] items, ALL unseen — value decreases with every addition. Recommend acknowledging/purging stale entries before adding more." Below 50 items or with some mix of seen/unseen, the backlog may still be salvageable — flag less aggressively (e.g. "Backlog: [N] items, [N] critical unread").

## Step 6: Deliver the PULSAR summary

Format — concise, scannable, under 2000 chars:

```
🌌 PULSAR — End of Day Review — [Day, Date]

System: [N] pulses fired, [N] issues detected. [health blurb]

🚨 MUST SEE ([N])
- Item 1 — why it matters
- Item 2 — why it matters

🎯 ACTION ITEMS ([N])
- Item 1 — [project]
- Item 2 — [project]

💡 OPPORTUNITIES ([N])
- Item 1 — [source]
- Item 2 — [source]

📋 Unseen backlog: [N] items total ([N] critical unread) — [worst offenders summary]
```

**Rules:**
- DO NOT dump raw pulse output. SYNTHESIZE. Find the signal, drop the noise.
- Start with a brief system health overview: "All pulses ran" or "[N] pulses fired, [N] issues detected" or "0 pulses fired today — system quiet."
- At the bottom add: *"When you're back, check the unseen backlog or ask me 'what did I miss' and I'll pull everything up with citations."*
- SILENT mode: if genuinely nothing new to report, respond with exactly `[SILENT]`.
- **Causal-framing rule — connect the dots when multiple symptoms share a root cause:** When the same digest triggers 3+ of these signals simultaneously, they are usually the same underlying problem, not independent failures:
  * P0 repos cold (Bookends/ConstructManage)
  * BizDev pipeline stalled (0 outreach, 0 wins)
  * User absence streak (no Discord/CLI sessions in N days)
  * All recent git commits from subagents/cron, not human
  
  **Do NOT list these as three separate 🚨 MUST SEE items.** Instead, lead the section with a synthesis: _"All three flags (P0 cold, BizDev stalled, user absent) share the same root cause: you've been away for [N] days. The individual warnings are symptoms, not independent problems."_ Then list each symptom briefly as sub-bullets under that framing.

  **When NOT to apply causal framing:** If one of the three signals is clearly false (e.g., git shows human-authored commits but session_search shows no user sessions — the user committed locally), don't collapse them. Causal framing only applies when ALL signals point the same direction.

### Escalation Framing (Multi-Day Repeated Findings)

**If any critical finding appears in 3+ consecutive daily digests, escalate the language.** Do not repeat the same warning verbatim day after day — the user will skim.

Escalation ladder (progress through these on consecutive appearances):
1. **First 1-2 days** — Standard factual framing: "P0 cold for 5 days."
2. **Days 3-4** — Switch to pattern-noticing: "P0 cold flagged for 4 straight days — this is now a pattern, not a blip."
3. **Days 5-6** — Direct framing: "7th straight pulse flagging P0 cold with zero action. The pattern is avoidance, not delay."
4. **Day 7+** — Change the ask size: Instead of "ship Bookends," recommend "open the Bookends dir and read one file. That's the task." Micro-commitments break avoidance loops.

**How to detect repetition:** Before writing the MUST SEE section, scan the unseen backlog for items with the same theme across multiple source dates (e.g., same `grep -o "BizDev"` pattern across June 4, 5, 7, 8, 9). If the same underlying theme appears 3+ times with `source` dates spanning 3+ consecutive days, escalate.

**Chronic-issue markers in the unseen backlog:**
- `grep -c "P0 projects COLD\|P0 cold\|P0 projects cold"` — if count >= 3 across source dates, escalate.
- `grep -c "BizDev.*0 outreach\|0 outreach\|0 contracts"` — if count >= 3, escalate.
- `grep -c "yt-anim-fishspeech.*crash\|fishspeech.*OOM\|crash-loop"` — if count >= 3, escalate infrastructure issues with direct framing.

## Pitfalls

- **Timezone bleed:** The script uses `TZ='America/New_York'` but the system date may report a different day. Always check the digest directory for the correct file rather than assuming `date +%Y-%m-%d` matches the digest date.
- **Parser category/priority misclassification:** The `unseen-backlog.py digest-summary` parser assigns categories and priorities heuristically based on content keywords, and gets them wrong regularly. Known misclassifications observed in production:
  * Sentry Pulse (225/225 test clean sweep) → classified as `fyi` priority and `bizdev` category (should be `high`/`critical` and `project`/`infra`)
  * Forge Pulse (Windows path rewrite fixes, pipeline overhaul) → classified as `fyi` priority and `bizdev` category (should be `high` and `infra`/`project`)
  * **Mitigation:** Always cross-reference parser output against the raw digest content (Step 2) before adding items to the backlog. The parser is a scoping aid, not an authority. Trust your own reading of the raw content for priority and category assignment.
- **MSYS/Windows path quirks:** Paths like `${MY_REPOS}/...` are MSYS-style mounts. Commands run via bash (git-bash) on Windows — use POSIX syntax in shell, not PowerShell.
- **Backlog count gotchas:** The `^○` character in backlog output may not pipe correctly through `wc -l` on MSYS. Use the `stats` command instead of parsing `list` output for totals. If you must grep list output, use bracket-pattern matching (`grep -c "\\[CRITICAL\\]"`) instead of line-start patterns.
- **Over-add to backlog:** Don't add every FYI item — only actionable/critical/important items that the operator needs to see when he returns. Too many items = backlog ignored. The 85-item/85-unseen state observed on June 14 shows the result of unchecked accumulation.
- **Duplicate-add cycle (most common bloat cause):** The same chronic findings surface every day (P0 freeze, BizDev 0 outreach, brain.md crash window). Without dedup checks (Step 4.5), each Daily Pulsar adds a NEW entry for the same underlying issue. Over 10+ days this creates 10+ near-identical entries on the same topic, inflating the backlog to 100+ items while the signal is actually just 3-4 recurring issues. **The fix is Step 4.5's keyword pre-check, not "add less to backlog."** If a chronic issue has already been captured, skip the add and escalate the PULSAR framing instead. A single excellent entry is more actionable than 10 copies of the same warning.

- **Backlog >75 unseen → STOP adding, escalate instead:** When the backlog exceeds 75 unseen items (as observed June 17: 99 total, 99 unseen, 50 critical), the backlog has crossed from "salvageable" to "noise." The PULSAR response should escalate: flag the count prominently and recommend a purge/acknowledgment session rather than adding more items. A backlog that's 100% unseen at 99 items is a backlog nobody reads — every new addition reduces the signal-to-noise ratio further. Consider: "Backlog is 99 items, all unseen, 50 critical — at this size, new items are noise, not signal. Recommend a 15-minute purge session: acknowledge or delete stale entries."

- **⚠️ DO NOT add items to a backlog already past the 75-unseen threshold.** At that point, stop adding entirely and use the PULSAR text itself as the signal delivery mechanism. Every add past the threshold makes the problem worse, not better. The only correct action is to flag the backlog bloat and recommend a purge cycle. If you catch yourself about to add to a 154-item backlog, stop — that violates this rule.
- **The user may be AFK:** This runs as a cron job. The user cannot respond or clarify. Make reasonable decisions about priority and don't ask questions.
- **Zero-pulse-day masking:** If today's digest doesn't exist, DON'T immediately fall back to the most recent file without flagging it. The absence of pulses is itself signal — it means the cron infrastructure may have issues, OR it's genuinely quiet. Always preface a zero-pulse digest with "0 pulses fired today" in the system health line.
- **Weekend/quiet-day confusion:** If today is Saturday or Sunday and the most recent digest is from Friday, that's a normal weekend gap — flag "Weekend pause (no pulses expected)" in the system health line, NOT "0 pulses fired — infrastructure may be down." Only escalate to "cron infrastructure issue" if the most recent digest is >48h old regardless of day of week. Check `date +%u` to determine weekday vs weekend before choosing the framing.
- **P0 cold vs system quiet — different root causes:** Zero commits on P0 can mean (a) the user is absent, (b) the project is stalled/avoided, or (c) the work happened elsewhere. Cross-reference git authorship and session_search source types to distinguish. Subagent commits ≠ user commits. A "P0 cold" finding backed only by subagent activity is really a "user absent" finding.
- **Escalation fatigue:** Don't deliver the same warning verbatim for the 7th time. Use the escalation ladder in Step 6. The user will start skimming if every pulse says "P0 cold / BizDev 0 outreach" with identical framing.
- **BizDev followups MCP quirk:** `bizdev_followups()` may return empty `[]` even when the BizDev dashboard shows `pending_followups: 14`. This is a known MCP server data inconsistency documented in `intelligence-pulse` skill Phase 3. When the PULSAR reads a digest entry mentioning "14 pending followups" but your own BizDev MCP calls return zero, do NOT flag the discrepancy as "data rot" — cross-check against the dashboard count. Use dashboard `pending_followups` as the source of truth, not the followups endpoint.
- **Backlog structural corruption inflates counts:** A backlog with 156 entries where all headers are "?" and sources are blank is not the same as 156 valid items. The `stats` command will report "156 unseen" but the effective signal is zero. Before reporting backlog totals, run the Step 5.2 structural integrity check. If >25% of entries are structurally empty, report the count as "corrupted — needs cleanup" rather than a raw number.
