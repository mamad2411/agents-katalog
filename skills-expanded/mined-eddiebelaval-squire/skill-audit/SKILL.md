---
name: skill-audit
description: Audit, score, prune, and heal the skill library. Use when Eddie says "audit my skills", "skill QC", "skill bloat", "clean up my skills directory", "why isn't this skill triggering", "which skills never fire", "should this skill exist", or asks what a skill is costing him. Also use proactively when a skill visibly misfires - fired when it shouldn't have, failed to fire when it should have, or produced worse output than no skill at all. NOT for creating a new skill (that is skill-creator) and NOT for build-time worth checks on non-skill artifacts (that is /assay).
---

# Skill Audit

A skill library degrades in two directions: it accumulates skills that never earn
their context cost, and the ones that do earn it drift out of sync with reality.
This audits both.

Descriptions are the always-loaded layer. Every description in the library sits in
context for every request in every session, forever. That makes skill count a
permanent tax on every client engagement, not a free option.

**Baseline (2026-07-26): 593 registered skills, 13 of which fired in 30 days.**

Two things that look like bloat but are not - do not re-litigate them:

- The 62 copies under `gstack/.factory/` and `gstack/.agents/` are vendored shadow
  copies Claude Code does not register (`ship` loads, `gstack-ship` does not). Zero
  context cost. Do not count them, do not delete them.
- `~/.claude/plugins/marketplaces/` is a browse cache, not installed plugins. Only
  `plugins/cache/` (42 plugins, 219 skills) is registered. Counting the former
  reports ~71,000 skills.

## The chain

INVENTORY -> SCORE -> VERDICT -> SHARPEN -> EVAL -> LEDGER

Run it per skill. Do not batch the whole library into one pass - the scoring is
comparative and the judgments blur.

## 1. Inventory

```bash
find ~/.claude/skills -name SKILL.md -not -path "*/.factory/*" -not -path "*/.agents/*" \
  | xargs wc -l | sort -n
```

Record for each: path, description length, body length, bundled resources, last
modified. Total description length across the library is the single most useful
number in this audit.

## 2. Score

Five dimensions, 1-5 each. Be harsh; a 3 means "fine," not "good."

| Dimension | Failing looks like |
|---|---|
| **Trigger precision** | Fires on unrelated work, or never fires when it should. Vague description, no concrete user phrasings, no stated non-triggers. |
| **Context economy** | Body over ~500 lines, or detail in SKILL.md that belongs in `references/`. Personas and behavior scripts in the always-loaded layer. |
| **Determinism** | Repetitive or exact work described in prose instead of shipped as a script. Prose the model must re-derive every run. |
| **Non-redundancy** | Overlaps another skill, or instructs the model to do what it already does well unaided. |
| **Freshness** | Dead paths, stale model IDs, APIs that moved, steps that no longer match the tool surface. |

## 3. Verdict

- **KILL** - any skill whose baseline (same task, no skill) is as good. A skill with
  no lift is not neutral; it costs context and adds a failure mode. This is the most
  common correct verdict and the hardest to reach for. Reach for it.
- **MERGE** - overlapping trigger surfaces. Two skills competing for the same request
  means neither fires reliably. Name collisions in the curate output are this signal
  in its rawest form.
- **SHARPEN** - real lift, poor packaging.
- **KEEP** - leave it alone. Say so explicitly so it doesn't get re-litigated.

## 4. Sharpen

Fix in this order - earlier fixes make later ones cheaper:

1. Description: add the concrete phrasings Eddie actually says, and the contexts that
   should *not* trigger it.
2. Split: move anything the model needs only sometimes into `references/`.
3. Extract: anything deterministic becomes a script.
4. Cut: delete instructions the model already follows without being told.

## 5. Eval

Never accept a rewrite on vibes. For each sharpened skill run the same 2-3 realistic
prompts against old version, new version, and no skill at all. The three-way
comparison is what separates real lift from the feeling of lift. See `skill-creator`
for the eval harness.

## 6. Ledger - the healing loop

Healing needs an injury report, and the report has to write itself or it doesn't get
written. `~/.claude/hooks/skill-audit-capture.sh` appends to
`~/.claude/skills/LEDGER.jsonl` on three events, all async so no turn pays latency:

| Event | Captures |
|---|---|
| `PostToolUse` (matcher `Skill`) | model-initiated skill invocations |
| `UserPromptSubmit` | `/skillname` invocations, built-in CLI commands filtered out |
| `Stop` | end-of-turn self-correction, attributed to the last skill used in-session |

Capture is deliberately noisy. Precision at capture time is a trap: the agent that
just used a skill badly is the worst available judge of whether it did. Log wide,
separate later.

`scripts/curate.py` is where separation happens. It ranks active skills by fault
density and - the more useful half - names every installed skill that never fired at
all. Zero invocations over a month is the cleanest KILL signal available, and it
costs nothing to detect.

```bash
python3 ~/.claude/skills/skill-audit/scripts/curate.py --days 30
```

Run the chain above on whatever curate puts at the top. Faults are the signal; the
ledger is what makes the loop self-healing rather than a thing to remember.

**Watch the unattributed count.** If self-corrections vastly outnumber attributed
faults, the capture is measuring the model, not the skills - narrow it before acting.

## Repair notes (2026-07-26)

The upstream bundle shipped three defects, all verified against this machine before
fixing. Do not reintroduce them from a newer upstream copy without re-checking:

1. `Stop` does not provide `.last_assistant_message`. Upstream read that field and
   silently logged nothing, forever. The transcript must be walked - see
   `auto-journal-capture.sh`, which hit and documented the same trap in May 2026.
2. `UserPromptExpansion` is not a hook event here. Slash-command invocations went
   uncaptured, so every `/name`-invoked skill read as NEVER FIRED and would have
   landed wrongly on the kill list. Now `UserPromptSubmit` + prompt parse.
3. `curate.py` keyed installed skills by directory basename, collapsing 37 of 420
   entries into invisibility. Now path-keyed, with collisions reported as MERGE
   candidates.
