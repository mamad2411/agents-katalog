---
name: harness-skill-prune
version: 1.0.0
description: >
  Audit the skills installed in a harness and decide, for each one, whether to
  retire, trim, or keep it. Use this whenever the user wants to clean up skills,
  asks whether a skill is still worth its tokens, complains that skills fire too
  often or burn usage limits, mentions that a model upgrade made their agent
  slower or "over-process" simple tasks, or asks which skills are obsolete.
  Also use after any major model or platform upgrade (new model generation,
  harness feature release) — that is exactly when engineered capabilities go
  native and skill inventories go stale. Skill staleness is blind spot #5
  (the Frozen Harness) applied to the skill layer.
  Triggers: "prune skills", "clean up skills", "skill audit", "which skills
  are obsolete", "retire skill", "restore skill", "清理skill", "精简skill",
  "淘汰skill", "skill瘦身", "技能清理".
---

# Harness Skill Prune

Skills are engineered capabilities. A skill exists because, at the time it was
written, neither the model nor the harness could do the thing natively. Models
and harnesses improve; skills don't. Every model generation moves some
capabilities from **engineered → native**, and every skill built on a
capability that made that transition turns from an asset into a liability —
it still loads, still triggers, still burns tokens, and now competes with a
model that does the job better unprompted.

This skill runs the audit and produces a disposition for every installed
skill: **retire**, **trim**, or **keep**. Retired skills are archived to a
`graveyard/` with an epitaph, so the inventory stays honest and the history
stays legible.

**What survives pruning, structurally:** capabilities with no path to native.
A model generation can absorb a planning ritual; it cannot absorb your
organization's schema, your private domain constraints, or your personal
definition of "good." Information asymmetry doesn't expire. Enforcement
doesn't expire either — a model can *know* an invariant and still skip it
under pressure, so invariants earn their context by force, not by information.
Everything else is on the clock.

---

## Workflow

Run the phases in order. Phases 1–5 are analysis and are always safe: they
end in a read-only report, never in file changes. Phase 4 (ablation) is
optional but is the strongest evidence you can get. Phase 6 executes the
report and runs **only after explicit user confirmation** — and only after
securing a restore path. The default invocation is audit-and-report;
"apply" and "restore" are separate, deliberate steps.

### Phase 1 — Inventory

Enumerate every installed skill for the target agent(s). Look everywhere
skills can load from: project `.claude/skills/`, user-level
`~/.claude/skills/`, plugin skill directories, skill registries
(`skills.json`, marketplace manifests), routing tables in `CLAUDE.md`, and
hooks or settings that inject content into every session. For each skill,
record:

- **Size**: word count of SKILL.md body + always-loaded metadata
- **Trigger posture**: on-demand, keyword-triggered, or self-injecting /
  mandatory (fires every conversation or every task)
- **Last substantive update** vs. the model generations that shipped since
- **Chaining**: does activating it force other skills or fixed process chains?

Estimated per-activation cost = size × trigger frequency. Self-injecting
skills with fixed chains are the highest-cost class and get audited first.

### Phase 2 — Classify what each skill compensates for

Every skill compensates for exactly one primary gap. Classify each:

| Class | The skill compensates for... | Native absorption path | Expected lifespan |
|---|---|---|---|
| **Model-capability** | reasoning the model couldn't do: planning rituals, step decomposition, "think before acting" ceremony, forced re-reading | absorbed by the next model generation | shortest |
| **Harness-capability** | machinery the platform lacked: todo tracking, worktree management, subagent orchestration, review chains | absorbed by platform-native features | short |
| **Information-asymmetry** | things no training run will ever contain: private domain knowledge, org conventions, personal methodology, environment-specific constraints | none | indefinite |
| **Enforcement** | invariants the model knows but skips under pressure: permission boundaries, evidence-before-claims, protection of user changes | none (knowing ≠ complying) | indefinite |

A single skill often mixes classes. Record the mix — it decides between
retire and trim in Phase 5.

### Phase 3 — Native-coverage check

For each model-capability and harness-capability item, check whether the
transition to native has already happened on the user's current stack:

- Does the current model do this unprompted? (Check its documented behavior
  and the user's own experience — ask.)
- Does the current harness ship this as a native feature? (Plan modes, task
  lists, worktrees, subagent APIs, hooks.)
- Red flag: the skill now triggers *more* often than before a model upgrade.
  That usually means the newer model follows the skill's self-injection
  instructions more faithfully — the skill's cost was always there; a more
  obedient model just stopped hiding it.

### Phase 4 — Ablation test (optional, strongest evidence)

Pick 2–3 representative tasks the skill claims to help with. Run each task
twice: with the skill installed, and with it removed. Compare output quality
and total token cost. Interpretation:

- No perceptible quality drop without the skill → the capability is native;
  the skill is pure overhead. **Retire.**
- Quality drops only on the parts encoding private constraints or invariants
  → the methodology is native but the constraints still pay rent. **Trim.**
- Quality drops across the board → the capability is still engineered-only.
  **Keep** (and re-audit next model generation).

### Phase 5 — Report (read-only, always runs first)

The default invocation of this skill ends here. Produce a **prune report**
and change nothing on disk.

The report contains, for every audited skill:

- A one-line disposition row: skill · class mix · native coverage · ablation
  result (if run) · recommended disposition · estimated context savings
- A short per-skill rationale (2–4 sentences): what it compensates for, what
  evidence says the transition to native has or hasn't happened, and — for
  trims — which content lands in which pile

Save it as `PRUNE_REPORT.md` inside the directory that holds the audited
skills (e.g. `.claude/skills/PRUNE_REPORT.md`) and present the summary
table in conversation. Then **stop and wait**. The user may accept
the report as-is, override individual dispositions (any override wins), or
walk away. No confirmation, no Phase 6.

### Phase 6 — Apply (only on explicit confirmation)

Never enter this phase from an inferred "sounds good." Require an explicit
go-ahead against a specific report, with per-skill overrides resolved.

**Before touching anything, secure the way back:**

1. If the skill directories are inside a git repository with a clean working
   tree, apply everything as **one atomic commit**
   (`prune: apply PRUNE_REPORT <date>`). Restore is then a single revert.
2. Whether or not git is available, write a **run manifest** at
   `graveyard/.prune/runs/<ISO-timestamp>.json` before executing, listing
   every planned action with the fields needed to reverse it:
   `{skill, action, from, to, backup, registry_entries_removed}`.
3. For every **trim**, copy the pre-trim skill directory to
   `graveyard/.prune/backups/<skill-name>/<ISO-timestamp>/` *before*
   rewriting anything.

Then execute:

**retire** — Move the entire skill directory to `graveyard/<skill-name>/`,
unchanged. Write `graveyard/<skill-name>/EPITAPH.md` from
`assets/EPITAPH_TEMPLATE.md`. Remove it from any skill registry / config,
recording exactly what was removed in the manifest.

**trim** — Separate the skill's content into two piles:
1. *Methodology ritual*: fixed process chains, mandatory step sequences,
   ceremony the model now performs unprompted. Delete.
2. *Invariants and private constraints*: permission boundaries,
   evidence-before-claims rules, org/domain-specific facts, personal
   standards. Keep, compressed.
Rewrite the skill around pile 2 only. Downgrade self-injecting triggers to
on-demand unless the skill is enforcement-class. Record the before/after
word count in the manifest. (Community reference point: a well-known
process-skill suite was community-trimmed by 85.5% under exactly this
split — the invariants survived, the ritual didn't.)

**keep** — No change now. Stamp it with the current model/harness generation
so the next audit knows when it was last verified.

If any step fails midway, use the manifest to roll back the steps already
completed, then report what happened. A half-applied prune is worse than no
prune.

### Restore (when the prune was wrong)

Pruning must be reversible for at least one model generation — an ablation
can mislead, and a "native" capability can turn out to be native only on
easy tasks. On request (`restore`, "undo the prune", "bring <skill> back"):

1. Locate the run manifest — most recent by default, or the run / skill the
   user names.
2. **Retired skills**: move the directory from `graveyard/<skill-name>/`
   back to its original path, delete its `EPITAPH.md`, and re-add the
   registry entries recorded in the manifest.
3. **Trimmed skills**: replace the trimmed version with the backup from
   `graveyard/.prune/backups/<skill-name>/<timestamp>/`.
4. Mark the run as reverted in the manifest (`"reverted": "<date>"`) rather
   than deleting it — a wrong prune is audit history too.

Restore selectively (a single skill) or wholesale (the entire run). If git
was used, `git revert` of the prune commit is the preferred wholesale path;
the manifest remains the source of truth for selective restores.

---

## The graveyard

`graveyard/` lives as a sibling of the skill directories it empties — one
per inventory (e.g. `.claude/skills/graveyard/`), not one global. It is not
a trash folder; it is the harness's record of where the
engineered→native frontier has moved. Each retired skill keeps its original
files plus an `EPITAPH.md` (template in `assets/`). The epitaph's
**survived-by** field matters most: when a trim or retirement relocates an
invariant into a living skill, record where it went. Skills die; invariants
move. The graveyard is the ledger of those moves.

After any major model or harness release, re-run this skill. Expect new
residents.

---

## Judgment guardrails

- **Prune never deletes.** Retire moves, trim rewrites-with-backup. The only
  content this skill is allowed to discard outright is methodology ritual
  inside a trim — and even then the pre-trim skill survives in backups.
  Actual deletion (emptying the graveyard, purging backups) is a decision
  the user makes themselves, later, outside this skill.
- **Report before touch, confirm before apply.** If there is any ambiguity
  about whether the user confirmed, there was no confirmation. Re-present
  the report and ask.
- Never retire an enforcement-class or information-asymmetry-class skill on
  cost grounds alone. High cost argues for trim, not retirement.
- "The model knows this" is not sufficient for retirement of enforcement
  content — compliance, not knowledge, is what enforcement skills buy.
- Don't retire based on one bad day. Prefer ablation evidence or a clear
  platform-native replacement over vibes.
- When a skill mixes classes, the default disposition is trim, not retire.
- This skill must pass its own audit. It encodes a pruning methodology —
  personalized methodology, information-asymmetry class, no native path.
  If a future harness ships native skill-lifecycle management, retire this
  skill into its own graveyard and write it a good epitaph.
