---
name: using-workflows
description: Meta-router for the closed-loop workflow recipes (audits, consensus gates, plan/build pipelines, findings triage, fleet manifest). Invoke BEFORE picking a workflow whenever the user describes a situation like "docs drifted", "weird bug", "plan this feature", "review this design", "fix this pile of findings", or asks which workflow/recipe to use. It routes the situation to the right recipe, auto-fills args, chains the closed loop, and optionally co-fires with codex-dynamic-workflows (if installed) for run artifacts (.workflow/<YYYYMMDDHHMM>-<slug>/). Even a 1% chance this applies means invoke it.
---

# using-workflows

Meta-router for the workflow recipes living in `~/.claude/workflows/` (personal
layer, usable from ANY repo) and/or the current repo's `.claude/workflows/`.
You are not a recipe yourself — you pick **which** recipe the situation needs,
fill its args, run it, and keep the closed loop moving.

## Install / Deploy (first run on a new machine)

This skill bundles the full recipe set under `workflows/` so it deploys
standalone — no other checkout needed:

```bash
bash <skill-dir>/scripts/install.sh            # → ~/.claude/workflows/
bash <skill-dir>/scripts/install.sh /path/to/repo/.claude/workflows   # repo layer, shared with the team
```

The script refuses to overwrite files whose content differs (pass `--force`
after reviewing the diff it prints). Canonical source of truth is
`skills/using-workflows/workflows/` in the agent-scripts repo (this bundle);
edit it there and reinstall — never edit deployed copies in place.

## The Rule

1. **Discover live, never recite from memory.** The installed recipe set changes;
   list what actually exists right now:

   ```bash
   for f in ~/.claude/workflows/*.workflow.js .claude/workflows/*.workflow.js; do
     [ -f "$f" ] && node -e '
       const s=require("fs").readFileSync(process.argv[1],"utf8");
       const m=s.match(/export const meta = \{[\s\S]*?\n\}/);
       const g=k=>(m&&m[0].match(new RegExp(k+":\\s*'\''([^'\'']*)"))||[])[1]||"";
       console.log(process.argv[1].split("/").pop()+"\t"+g("name")+"\t"+g("description"))
     ' "$f"
   done
   ```

   Project layer shadows personal layer on name collisions. Before running a
   candidate, **read its header comment** — that comment block is the args
   contract; never guess args. If nothing is installed, run the install script
   above first.

2. **Route by situation**, using the decision tree below as the prior — but the
   live `description`/`whenToUse` fields win if they disagree (recipes evolve).

3. **After it returns, chain the loop** (see "Closed loop" below) instead of
   stopping at raw output.

## Decision tree — situation → recipe

```
What is the user actually facing?
│
├─ "docs/design and code disagree / drifted"   → docs-vs-code-audit | design-vs-code-audit
├─ weird bug, needs root-cause digging          → root-cause-deep-dive-audit
├─ an audit just returned confirmed findings    → findings-triage      (connector ① — offer this AUTOMATICALLY)
├─ has a brief (mini-PRD), wants it fully built → feature-lifecycle-auto
├─ freeze planning docs only, deliberately no build → plan-pipeline
├─ requirement → implementation plan (supervised, dual consensus) → feature-plan-consensus
├─ one design proposal needs adversarial consensus → design-consensus
├─ ANY artifact needs a "second model agrees" gate → consensus-gate
├─ build from spec + dual-model review + verify → spec-implement-dual-review-verify
├─ "what should this project do next"           → project-direction-review
├─ inventory/snapshot the recipe fleet, check machine drift → workflow-manifest
│
└─ just ONE bounded task to run in the background — no multi-stage control flow
    → NOT a workflow. Defer to the using-tmux-agent-tools skill
      (tmux-delegate gate → claude-oneshot / codex-oneshot).
```

## Auto-fill args (the lazy part)

Fill these WITHOUT asking when derivable; ask only what's genuinely the user's call:

- `cli` (REQUIRED by every adversarial-review recipe; no default by design):
  take, in order — the user's words → the repo's `CLAUDE.md` stated preference →
  ask once ("codex? claude-fable-gate-glm? agy?"). Valid values = any
  `~/.config/agent-tmux/profiles` name; verify with `ls` if unsure.
- `context`: compose yourself — one line with the repo abs path + stack +
  anything the user just said about scope. Quality of findings tracks this line.
- `repoPath` / paths: current repo unless told otherwise.
- `outputLanguage`: leave the recipe's default unless asked.
- Prefer **name invocation** over `scriptPath`: some environments drop `args`
  on scriptPath runs (symptom: `aborted: missing arg`). If stuck with
  scriptPath, temporarily fill the recipe's `BUILTIN = {}` and revert after.

## Closed loop — what to do after each recipe returns

```
audit → confirmed findings?
  ├─ yes → run findings-triage on them (don't make the user hand-sort)
  │        ├─ askUser[]   → surface to the human verbatim; NEVER auto-decide intent
  │        ├─ briefs[]    → one feature-lifecycle-auto call per brief (plan gate pauses for the human ✋)
  │        └─ directFix[] → one partitioned fix run (disjoint files, SKIP+report on missing assets)
  └─ after fixes/build → re-run the ORIGINATING audit with the SAME args (connector ②)
         confirmed == 0  → loop converged; report and stop
         confirmed  > 0  → back to findings-triage
```

Hard limits while chaining:

- **workflow() nesting cap = 1 level.** Chain recipes from the TOP level
  (you, the main loop), never from inside another recipe.
- Behavior-tier edits to any recipe require a `consensus-gate` pass FIRST;
  wording/docs edits go direct (canonical copy in the agent-scripts repo's
  `skills/using-workflows/workflows/`, then redeploy to `~/.claude/workflows/`
  — never the reverse).

## Run discipline — optional add-on: `codex-dynamic-workflows`

**This router works standalone** — recipes need nothing beyond
`~/.claude/workflows/`. But IF the `codex-dynamic-workflows` skill is
installed (check the available-skills list; do NOT assume), co-fire it: **this
skill picks the recipe; that one governs the run record.** For any non-trivial
recipe run (anything past a one-shot audit you'll discard), follow its
conventions in the TARGET repo simultaneously:

- Anchor the run in `.workflow/<YYYYMMDDHHMM>-<slug>/` — recipes already
  lean this way (`plan-pipeline` defaults `directionPath`/`planPath` there).
  The `<YYYYMMDDHHMM>` prefix is the run-creation timestamp; it is supplied
  by the orchestrator as part of the `slug`/run-id arg it passes in, never
  computed inside a Workflow script (`Date.now()` is banned there — recipes
  must stay deterministic/replayable). Keep `plan.md` human-readable,
  `state.json` for status/approval/verification state, `final-report.md`
  for the integrated outcome.
- Its operating contract applies verbatim: restate goal + success criteria
  before invoking; artifact before delegating; approval before risky/external
  steps; **integrate results — never paste raw recipe output as the answer**;
  verify with checks matched to blast radius.
- Note the directory split (a classic confusion): `.workflow/` = run
  artifacts (that skill's convention, NOT discovered by Claude Code);
  `.claude/workflows/` = the recipes themselves (discovered, `/name`-callable).
- Multi-recipe chains (audit → triage → lifecycle → re-audit) = one slug, one
  `.workflow/<YYYYMMDDHHMM>-<slug>/` dir; each recipe's return value lands in
  `results/`, loop convergence (connector ② confirmed==0) goes in
  `final-report.md`.

## Canonical references (never paraphrase these from memory)

- Per-recipe reference + args details: `workflows/README.md` in this bundle
  (canonical: `skills/using-workflows/workflows/README.md` in the agent-scripts repo).
- Worker mechanics (agent-tmux/profiles/send-wait): the `tmux-agent-tools`
  skill — defer to it for anything about driving the second-model CLI.
- Run-record conventions (`.workflow/<YYYYMMDDHHMM>-<slug>/`, goal mode,
  packets): the `codex-dynamic-workflows` skill — optional add-on; defer to
  it for run discipline only when it's installed.
