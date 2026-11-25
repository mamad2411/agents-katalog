---
name: memory-health-audit
description: "Full memory system health audit — cross-correlates retrieval logs, diary, learnings, and memory file structure to assess what's working, what's wasteful, and what to change. Broader than the /multiplai-context:health check (which focuses on infrastructure). Use when the user asks 'how's memory doing', 'audit the memory system', 'what patterns have you noticed about memory', 'memory health check', or periodically (monthly) to track system health over time."
---

# Memory Health Audit

Full cross-source analysis of the memory system. Produces a dated assessment snapshot saved to `$CLAUDE_PLUGIN_DATA/memory-health/` for longitudinal tracking. Covers four data sources: retrieval logs, diary, learnings, and the memory corpus itself.

**Distinct from `/multiplai-context:health`:** That skill checks infrastructure (files exist, not stale, config wired). This skill cross-correlates ALL four data sources to surface systemic patterns — file overload, corpus bloat, learning gaps, project coverage, and actionable restructuring recommendations.

## Key Paths

| Source | Path | What It Contains |
|--------|------|-----------------|
| Retrieval logs | `$CLAUDE_PLUGIN_DATA/logs/context_manager-*.log` | Per-prompt routing decisions (`ROUTING` lines), fallback events (`FALLBACK` lines), no-context events (7-day retention) |
| Diary | `.multiplai/diary/*.md` | Session diary — what happened, which projects, commits |
| Learnings | `.multiplai/learnings/*.md` | Extracted insights — types, trust levels, target files |
| Memory corpus | `.multiplai/memory/*.md` | The actual memory files — structure, size, staleness |
| Memory catalog | `$CLAUDE_PLUGIN_DATA/catalogs/memory.json` | Routing descriptions, intent_domains, anti_domains |
| Utilisation | `$CLAUDE_PLUGIN_DATA/utilisation.jsonl` | Per-session injected-vs-estimated-used records (two estimators; see Phase 1.5) |
| Session transcripts | `$CLAUDE_CONFIG_DIR/projects/<proj>/<session>.jsonl` | Per-prompt hook attachments (the skills the model was shown) joined against Skill tool calls and slash commands (Phase 1.6) |
| Previous assessments | `$CLAUDE_PLUGIN_DATA/memory-health/*.md` | Past audit snapshots for delta comparison |

## Workflow

**CRITICAL: Delegate all heavy log parsing to background agents.** Each data source can be 1000s of lines. Never load raw logs into the main conversation. Launch 3-4 parallel agents, each returning aggregated metrics.

### Phase 1: Gather (parallel agents)

Launch these agents simultaneously:

#### Agent 1: Retrieval Log Analysis
Parse ALL `context_manager-*.log` files in `$CLAUDE_PLUGIN_DATA/logs/`. Return:
- Total routing decisions, NONE rate %, actual file load rate %, fallback rate %
- Per-file retrieval frequency from `ROUTING` lines
- Co-retrieval patterns (which files appear together, with co-occurrence counts)
- Fallback count (lines containing `FALLBACK`)

**Log line formats:**
- `ROUTING memory=["file1.md","file2.md"] skills=[] resources=[]` — router-selected files
- `FALLBACK memory=["file1.md",...]` — router picked nothing; metadata-ranked fallback used
- `No context to inject` — NONE: no memory, skills, resources, or project state

**Extraction commands:**
```bash
LOGS="$CLAUDE_PLUGIN_DATA/logs"

# File retrieval frequency (router picks only)
grep "ROUTING memory=" "$LOGS"/context_manager-*.log \
  | sed 's/.*ROUTING memory=\(\[.*\]\) skills=.*/\1/' \
  | python3 -c "
import sys, json, collections
counts = collections.Counter()
for line in sys.stdin:
    try:
        files = json.loads(line.strip())
        counts.update(files)
    except: pass
for f, n in counts.most_common(): print(n, f)
"

# NONE rate
total=$(grep -c "ROUTING memory=\|No context to inject" "$LOGS"/context_manager-*.log 2>/dev/null || echo 0)
none=$(grep -c "No context to inject" "$LOGS"/context_manager-*.log 2>/dev/null || echo 0)
echo "Total: $total  NONE: $none"

# Fallback rate
grep -c "FALLBACK memory=" "$LOGS"/context_manager-*.log 2>/dev/null || echo 0

# Co-retrieval patterns
grep "ROUTING memory=" "$LOGS"/context_manager-*.log \
  | sed 's/.*ROUTING memory=\(\[.*\]\) skills=.*/\1/' \
  | python3 -c "
import sys, json, collections
patterns = collections.Counter()
for line in sys.stdin:
    try:
        files = json.loads(line.strip())
        if len(files) > 1:
            patterns[tuple(sorted(files))] += 1
    except: pass
for p, n in patterns.most_common(10): print(n, list(p))
"
```

#### Agent 2: Diary Analysis
Read ALL `.multiplai/diary/*.md` files. Return:
- Session count and sessions/day
- Project mention frequency (top 15)
- Work type distribution (fix/build/research/write — estimate from keywords)
- Auto-commit count and commits/day
- Session clustering patterns (dates with abnormal session counts)
- Skill usage mentions (which skills appear in diary)

#### Agent 3: Learnings Analysis
Read ALL `.multiplai/learnings/*.md` files. Return:
- Total learnings count (processed vs pending)
- Type distribution (OBSERVATION, PATTERN, RULE-PROPOSAL, CORRECTION)
- Trust distribution (verified, high, medium)
- Target file frequency (which memory files get the most learnings directed at them)
- List ALL corrections found (full text) — these are highest signal

#### Agent 4: Memory Corpus Analysis
Read ALL `.multiplai/memory/*.md` files and `$CLAUDE_PLUGIN_DATA/catalogs/memory.json`. Return:
- Per-file: name, line count, section headers, density assessment (high/medium/low)
- Staleness: last modified date per file, flag anything >30 days
- Overlap identification: content that appears in multiple files
- Signal:noise estimate per file (% of lines that are actionable vs filler)
- Catalog quality: which files have specific vs vague intent_domains
- Files with no retrieval demand in logs (never loaded — dead weight or routing gap?)

### Phase 1.5: Utilisation table (run directly, do NOT delegate)

Retrieval frequency — everything Agent 1 returns — answers *what was loaded*.
It cannot answer *what was used*, and a section loaded on every prompt and
relevant on none of them scores best of all on retrieval count. The utilisation
table is the counterweight. One deterministic command, small output, so run it
in the main thread:

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/utilisation_report.py"
```

Add `--json` when you need the raw numbers for the assessment file.

**Report it verbatim, with its labels intact. These are not stylistic:**

- **Every number is an ESTIMATE, from a model, and must be described that way**
  wherever it appears in your output — the conversation, the assessment file,
  any table you build from it. Say which estimator produced a number and show
  its sample size.
- **There are two estimators and they are never blended.** Self-report (the
  session grading itself — biased upward, evidence required) and the offline
  judge (independent, sampled, so absent for most sessions). If the report
  marks a row `!` the two disagree past the margin: report the disagreement as
  a finding. Do **not** average them, and do not invent a combined score.
- **Do not rank or act on rows under "insufficient data".** They are there
  precisely because their sample is too small to mean anything.
- **"Never retrieved" is a routing finding, not a pruning finding.** A section
  that never reached a prompt has produced no evidence about its value; it
  belongs in Phase 4's "routing to broaden", not in a deletion list.
- **Nothing here is a deletion.** The highest-cost-per-use rows are
  *candidates* — a suggestion for a human, and never an instruction to remove
  anything. This skill proposes; only `/multiplai-context:dream-remember`
  writes to memory.

If `utilisation.jsonl` does not exist yet, or every row lands under
"insufficient data", say so plainly and skip the section. A table nobody can
act on is worse than no table.

### Phase 1.6: Skill routing precision (run directly, do NOT delegate)

The context hook suggests skills per prompt. Retrieval frequency says how
often each skill was suggested; it cannot say whether the suggestion was any
use. This step reads each session transcript: the prompt's `UserPromptSubmit`
hook attachment records the `=== SKILLS ===` block the model was actually
shown (after the re-recommendation cooldown), and the Skill tool calls and
slash commands that follow record what was used. It reports the share of
suggestion events where one of the suggested skills was then invoked before
the session's next prompt. Transcripts are kept for a year, so the window is
not capped by the 7-day log retention; the header prints the earliest prompt
actually read. Why it matters: "Demystifying Agent Skills" (arXiv 2608.14036)
measured actual-use retrieval precision falling from 29.6% to 3.3% as a skill
pool grew from 5 to 100. Derive the current pool from the router's own
catalog, which is what it chooses from:

```bash
python3 -c "import json,os; print(len(json.load(open(os.path.join(os.environ['CLAUDE_PLUGIN_DATA'],'catalogs','skills.json')))['entries']))"
```

One run gives both outputs:

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/skill_routing_precision.py" \
  --days 30 --json-out "${CLAUDE_PLUGIN_DATA}/memory-health/skill-precision-$(date +%Y-%m-%d).json"
```

Report three things verbatim:

- **Prompt-level precision** and its denominator (prompts with a skill
  suggestion). Under about 30 events the figure is noise; say so and skip
  the per-skill rows.
- **Suggested at least 3 times, never invoked.** These are routing findings:
  either the skill's catalog description matches prompts it should not, or
  the skill is right and the session did the work by hand. Decide which per
  row from the diary; do not propose removing a skill from this number alone.
- **Per-skill ratio** for the top rows, so a broad description (suggested on
  many prompts, invoked on few) is visible next to a narrow one.

Limits, so the number is not over-read: a suggestion invoked *after* the
session's next prompt is a miss for the prompt that suggested it; a skill
invoked inside a subagent is never credited; a skill used because Claude
already knew it, with no suggestion, is invisible here. The measure is
"did the hint precede a use", not "did the hint cause it".

### Phase 2: Cross-Correlate

After all agents return, correlate findings:

1. **Overloaded files** — High retrieval demand + low signal:noise + many learnings targeting it = needs splitting
2. **Underloaded files** — Never retrieved + fresh content = routing gap (domains too narrow)
3. **Wasteful retrievals** — High retrieval demand but content rarely actionable = loaded too eagerly. The utilisation table is the evidence for this row: high `retrieved`, high `B/est.use`. Quote both estimators and the sample size; never assert it from retrieval count alone
4. **Learning gaps** — Project with high diary activity but zero learnings = extraction not capturing
5. **Stale but active** — File loaded frequently but not updated in 30+ days = content may be outdated
6. **Correction clusters** — Multiple corrections targeting same file = systematic accuracy problem
7. **Fallback-heavy** — High fallback rate = router not selecting relevant files (catalog quality issue)

### Phase 3: Delta Comparison

Read the most recent previous assessment from `$CLAUDE_PLUGIN_DATA/memory-health/`. Compare:

| Metric | Previous | Current | Delta | Direction |
|--------|----------|---------|-------|-----------|
| NONE rate | | | | |
| File load rate | | | | |
| Fallback rate | | | | |
| Top file demand | | | | |
| Corpus size (lines) | | | | |
| Correction count | | | | |
| Stale files (>30d) | | | | |

If no previous assessment exists, skip delta and establish baseline.

### Phase 4: Recommendations

Based on the cross-correlation, produce prioritized recommendations:

1. **Files to split** — name the file, what to extract, where it goes
2. **Routing to tighten** — name the file, current domains, suggested narrower domains
3. **Routing to broaden** — name the never-loaded file, evidence it should be loaded
4. **Content to move** — research material in memory/ that belongs in RESOURCES/
5. **Files to merge** — small files with overlapping content
6. **Staleness to address** — files needing review with specific sections flagged

Each recommendation should include:
- **Evidence** — the specific metrics that justify the change
- **Expected impact** — what improves and by how much (estimate)
- **Effort** — trivial / moderate / significant

### Phase 5: Save Assessment

Write the full assessment to `$CLAUDE_PLUGIN_DATA/memory-health/YYYY-MM-DD-assessment.md` with:
- All metrics from Phase 1 (tabular format)
- Cross-correlation findings from Phase 2
- Delta comparison from Phase 3 (if available)
- Prioritized recommendations from Phase 4
- Method notes

Report key findings in the conversation. Keep the conversation output concise — the full data lives in the assessment file.

## Guidelines

- **Monthly cadence recommended.** Run after at least 50 routing decisions have accumulated since last assessment.
- **Always delegate to agents.** Raw logs are too large for the main context. Each agent returns only aggregated metrics.
- **Honest grading.** Don't inflate signal:noise ratios. If a file is bloated, say so.
- **Actionable over comprehensive.** 5 concrete recommendations beat 20 vague observations.
- **Track longitudinally.** The `memory-health/` directory is the longitudinal record. Each assessment is a dated snapshot. Deltas show whether changes improved the system.
- **Relationship to `/multiplai-context:health`:** That skill can run anytime for quick infrastructure checks. This skill runs monthly for the full systemic view. They complement each other.
