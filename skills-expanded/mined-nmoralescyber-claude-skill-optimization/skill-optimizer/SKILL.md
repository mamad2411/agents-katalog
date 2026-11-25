---
name: skill-optimizer
description: Audits and rewrites SKILL.md files for installed skills to improve trigger accuracy, instruction clarity, and empirical performance. Use when the user wants to optimize, improve, audit, upgrade, fix, sharpen, or rewrite an existing skill, when a new skill is installed (auto-runs Phase 0 silently and surfaces findings on next session open), when the user asks "make my skills better", "audit my skills", "which skills should I work on first", or "optimize the skill library". Operates on the locally installed skill set ONLY — never invents skills that don't exist. Has full restructure authority: can merge redundant skills, split bloated ones, deprecate obsolete ones, and create replacement skills, with all destructive changes backed up first. Uses the SOE-v2 protocol: calibration → custom rubric → diagnostic battery → deliberate-practice loop with pre-commit prediction, spaced repetition, adversarial rounds, and mastery-via-transfer.
---

# Skill-Optimizer

A meta-skill that systematically audits and upgrades the SKILL.md files in the user's installed skill library. Built on the SOE-v2 (Skill Optimization Engine v2) protocol.

## What this skill is for

The user has a large skill library (~90+ skills as of install). Many were authored at different times, by different teams, with different quality bars. Symptoms of an unoptimized library include:

- Skills that under-trigger (Claude doesn't invoke them when it should)
- Skills that over-trigger (fire on the wrong queries, crowding out better fits)
- Skills with overlapping triggers that fight each other
- Stale instructions referring to old tools, models, or workflows
- Bloated SKILL.md files (>500 lines, slow to load, low signal density)
- Vague descriptions ("Help with X") instead of pushy, specific, example-laden ones
- Missing reference files where progressive disclosure would help

This skill fixes those defects systematically. It does NOT train the user — it improves the tools the user has.

## Hard scope rules

1. **Local-only.** Operate ONLY on skills physically present in the user's environment (anthropic-skills, plugin-installed skills, user-authored skills). Never propose optimizing a skill that isn't installed. Enumerate the actual skill directories before doing anything.
2. **Auto-overwrite with backup.** Before any rewrite, snapshot the original to `outputs/skill-backups/<timestamp>/<skill-name>/`. Then write the new version in place. Backup first, always — no exceptions.
3. **Restructure authority granted.** Can merge, split, deprecate, or create new skills as part of optimization. Every structural change still gets a one-line justification logged to `outputs/skill-optimizer-log.md`.
4. **96% confidence gate.** Do NOT begin Phase 1 (diagnostic) on a skill until Phase 0 calibration has answered enough to justify ≥96% confidence the optimization will be net-positive. If gaps remain, ask more questions. Don't guess.

## The SOE-v2 protocol (per skill)

### PHASE 0 — Calibration (gate: 96% confidence before proceeding)

Ask the user, one at a time, only the questions whose answers materially change the optimization. Skip questions whose answers can be inferred from the skill's own SKILL.md or from prior calibration. Typical questions:

1. **Definition probe.** "In one sentence, what should this skill do for you that you can't get from raw Claude?" Catches mismatches between user intent and current skill scope.
2. **Trigger probe.** "Give me three real prompts you've typed (or would type) where you want this skill to fire." These become the should-trigger eval set.
3. **False-positive probe.** "Give me one prompt where this skill currently fires but shouldn't, or one where you'd be annoyed if it did." Catches over-triggering risk.
4. **Output expectation.** "What does a perfect output look like? Paste an example or describe the shape." Anchors quality grading.
5. **Failure mode.** "Tell me about a time this skill (or any similar one) gave you something useless. What went wrong?" Surfaces the specific defect to target.

After answers, propose a custom 4-axis rubric specific to THIS skill — not the generic one. Example axes for a sales skill: Trigger Precision / Output Specificity / CRM-Integration Awareness / Brand-Voice Match. Each axis gets 5 anchor descriptions (Novice → Expert) and a weight summing to 100%. Wait for approval or edits.

Only proceed past Phase 0 when you can write down: "I am ≥96% confident the optimization plan will improve this skill on the user's actual usage patterns because [specific evidence from calibration]."

### PHASE 1 — Diagnostic battery (3 probes, not 1)

Run three independent diagnostics on the skill in its current state:

- **Probe A — Standards audit.** Score the skill against `references/skill-creator-standards.md`. Output a defect list with severity (Critical / Major / Minor) and citations from the SKILL.md.
- **Probe B — Empirical trigger test.** Generate 20 realistic queries (10 should-trigger, 10 should-not-trigger), use the skill-creator's optimization loop or a manual test to measure trigger precision and recall. Compute baseline F1.
- **Probe C — Adversarial transfer test.** Construct 3 queries from adjacent domains designed to look like they should fire the skill but actually need a different skill. A well-tuned skill doesn't bite on these.

Score each probe on the approved rubric. The lowest-scoring axis becomes the rewrite target.

### PHASE 2 — Deliberate-practice rewrite loop

For each iteration, output in this exact format:

```
[STATE]
  Iteration: N
  Skill: <skill-name>
  Target axis: <weakest axis from last cycle>
  Difficulty: <1–10> with delta justification
  Constraint stack: <e.g., "must not exceed 400 lines", "must preserve trigger phrase X">
  Spaced-repetition probe: <yes/no — every 4th iteration must retest a previously-fixed defect>

[CHANGE PROPOSAL]
  <description-frontmatter rewrite | body restructure | reference file extraction | merge with skill X | split into skills Y and Z | deprecate>
  Specific edits with before/after diff

[PRE-COMMIT]
  Predicted F1 delta on trigger eval: +/- N points
  Predicted defect-list reduction: N items
  Predicted side effects: <list any neighboring skills this change might disturb>

[APPLY]
  Snapshot original to outputs/skill-backups/<timestamp>/
  Write new SKILL.md in place
  Log change to outputs/skill-optimizer-log.md

[EVALUATION]
  Re-run Probe A standards audit — score delta per axis
  Re-run Probe B trigger eval — actual F1 delta
  Calibration delta: |predicted − actual|
  Regression flag: <yes if any axis dropped >10 pts>

[FEEDBACK]
  Top remaining weakness with citation
  Why it matters at scale
  What an expert SKILL.md would do instead, with concrete example

[LEVEL-UP]
  ONE specific technique to apply next iteration
  60-second drill: a tiny edit the user can verify in isolation

[NEXT]
  Next [STATE] + [CHANGE PROPOSAL] for iteration N+1
```

### Progression and exit rules

- Difficulty +1 only if last iteration's score ≥85 AND calibration delta ≤10.
- Difficulty −1 if score <70 OR regression flagged.
- Every 4th iteration: spaced-repetition probe — retest a defect from an earlier iteration to confirm the fix held.
- Every 8th iteration: ADVERSARIAL ROUND — rewrite a query set that looks superficially like prior tests but punishes pattern-matching.
- **Mastery declared when:** 3 consecutive iterations score ≥95 across DIFFERENT primary target axes, AND one transfer test shows the upgraded skill correctly defers to (or correctly wins over) a competing skill.
- After mastery: skill enters "maintenance mode" — re-audited once per quarter or whenever its dependencies change.

### Anti-gaming and trainer accountability

- The user can challenge any score by saying "defend." Re-grade with explicit citations from the SKILL.md text or revise the score.
- If the user says "lazy," the iteration is invalid — re-issue with sharper specificity.
- Never reveal which adversarial trap is embedded in the next iteration's eval set.
- The skill-optimizer itself is on the optimization queue — every 90 days, run it on itself.

---

## Library-wide operation: the auto-prioritized queue

When invoked without a specific skill target ("optimize my skills", "audit my library"), do this:

### Step 1 — Enumerate

List every skill currently installed. Group by source:
- `anthropic-skills:*`
- `plugin_*` (organized by plugin name)
- User-authored skills

Save the full inventory to `outputs/skill-inventory-<timestamp>.md`.

### Step 2 — Triage signals

Score each skill on three signals (each 0–10, multiplicative):

- **Quality gap (Q):** Static audit against skill-creator standards. Higher = more defects = bigger improvement headroom.
- **Usage frequency (U):** From session transcripts and task tracker if accessible. If unavailable, ask the user to self-report top 10 / never-used skills.
- **Strategic importance (S):** Based on the user's role and stated upcoming projects (gathered in a brief library-level Phase 0). A finance-focused user gets `finance:*` weighted up.

ROI = Q × U × S, range 0–1000.

### Step 3 — Surface the queue

Present the top 10 skills as the optimization backlog with ROI scores and one-line rationales. Ask the user to confirm or reorder. Then process in order, full SOE-v2 per skill.

### Step 4 — Library-level outputs

After every batch of 5 skills processed:
- Update `outputs/skill-optimizer-log.md` with cumulative stats (skills upgraded, defects closed, F1 deltas)
- Flag cross-skill issues: trigger collisions, redundant coverage, gaps where no skill exists for a frequent user need
- Propose merges/splits/new-skill creation as a structured recommendation

---

## Auto-trigger on new skill installation

When `available_skills` changes between sessions, detect the delta. For each new skill:

1. Silently run Phase 0 calibration in the background — generate the questions but don't surface yet.
2. Run Probe A (standards audit) and Probe B (trigger eval) automatically.
3. On the user's next Cowork session open, surface a single notification: "New skill detected: `<name>`. Baseline audit complete — Q score: N/10. Run full optimization?" with a one-click yes/no.

Detection mechanism: persist a `outputs/skill-optimizer-known.json` file listing all skills seen as of last run. On invocation, diff against current `available_skills`. Anything new triggers the auto-Phase-0.

---

## Output artifacts (every run)

Every optimization run produces:

1. **`outputs/skill-backups/<timestamp>/<skill-name>/`** — pristine copy of the original skill before edits.
2. **The upgraded SKILL.md in place** (overwriting the original at its installed path).
3. **`outputs/skill-optimizer-log.md`** — append-only log of every change with timestamp, skill name, change type, before/after rubric scores, and one-line rationale.
4. **`outputs/skill-inventory-<timestamp>.md`** — current library snapshot with ROI ranking.
5. **`outputs/skill-optimizer-report-<timestamp>.md`** — human-readable summary of what changed and why, presented at the end of each session.

Always end a session with a `present_files` call surfacing the report and log so the user can review without digging through directories.

---

## Reference files

- `references/skill-creator-standards.md` — Full text of the official Anthropic skill-authoring standards, used as the Probe A rubric.
- `references/rubric-templates.md` — Pre-built 4-axis rubric templates for common skill categories (sales, legal, data, design, productivity, etc.) so Phase 0 doesn't reinvent the wheel each time.
- `references/trigger-eval-patterns.md` — Recipes for generating realistic should-trigger and should-not-trigger queries, including category-specific traps.
- `references/restructure-decision-tree.md` — When to merge vs. split vs. deprecate, with worked examples.

---

## Operating principles

- **Backup before every write.** No exceptions. The skill-backups directory is sacred.
- **Cite the SKILL.md when grading.** Don't say "the description is vague" — quote the exact phrase and explain why.
- **Pre-commit predictions are mandatory.** Skipping the prediction invalidates the iteration. Calibration delta is the single best signal of whether the optimizer is improving or hallucinating.
- **Never declare mastery on a single axis.** Three consecutive ≥95s across DIFFERENT axes, plus transfer test. Otherwise it's overfitting.
- **The optimizer is not above the protocol.** When Skill-Optimizer optimizes itself, it follows the same rules — including the 96% gate, the diagnostic battery, and the adversarial round.
