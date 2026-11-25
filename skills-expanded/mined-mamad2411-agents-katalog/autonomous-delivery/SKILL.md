---
name: autonomous-delivery
description: Drives a pre-decomposed set of GitHub issues to done with minimal human input. Invoked by the main session when someone says "autonomous loop", "run until done", "don't stop until the goal", "self-sustaining loop", "orchestrate the whole build", "drive these issues to done", "agentic loop", or "/orchestrate". Assumes the goal has already been broken into tracked GitHub issues (via feature-delivery or project-management); this skill owns the dispatch-review-merge loop and all termination guards.
---

# Autonomous Delivery Skill

Runs the main Claude Code session in a self-sustaining loop: dispatch specialist → staff-engineer review gate → squash-merge, repeating until all open issues are closed or a guard trips. Requires a goal already decomposed into GitHub issues with agent assignments and dependency links.

Apply `principles-dry-kiss`: do not add phases or coordination overhead the task does not need. This skill is about execution, not planning.

## When to use

Use this skill when:
- A goal has already been decomposed into tracked GitHub issues (via `feature-delivery` / `project-management`).
- The main session should drive those issues to done without stopping for human input at each issue.
- The goal is bounded enough that a max-iteration CAP and token budget can guard against runaway execution.

Do not use this skill for untracked or undecomposed goals — run `feature-delivery` first.

## The loop

```
until (open issues == 0) or (iterations >= CAP) or (budget exhausted):
  ready = issues whose dependencies are all closed
  if ready empty and open > 0:
    report blocker; stop
  for issue in ready (respecting parallel-safe vs serial):
    dispatch specialist (model:'sonnet')  -> branch + implement + PR (git-workflow)
    dispatch staff-engineer review (model: OMIT => inherit top tier)  -> GATE 1
    if approved:
      if security-sensitive (or securityReview:'always'):     -> GATE 2
        dispatch security-architect deep audit (inherit top tier)
        if not approved: ONE security fix pass -> re-audit; still failing -> flag open
      squash-merge per git-workflow   (only after all required gates approve)
    else:
      ONE fix pass -> re-review
      if still failing: flag open
  iterations++

# flag open = persist the failure context, don't drop it: post the reviewer/audit
# findings as an issue COMMENT + add a `needs-rework` label, THEN release the
# in-progress claim (so scout re-picks it next run). The issue stays OPEN; the next
# engineering pass reads WHY it failed instead of re-opening it blind. Never re-loop
# the same issue this run — one fix pass is the cap (cost guard against thrash).

done when: 0 open issues AND CI/validate green AND tests pass
```

Parallel-safe issues (no shared file overlap, independent scope) may be dispatched concurrently — but **each in its own worktree** (two branches can't share one working tree even with zero file overlap). Serial issues (dependency edges, shared files) must run sequentially. The reference script is **serial by default**; concurrency is opt-in via `args.parallel: true` and only safe because the mutating agents carry `isolation: 'worktree'`.

The reference script can only see **declared `blockedBy` edges** — it cannot infer shared-file overlap from issue metadata. So any two issues that touch the same files MUST carry a `blockedBy` edge between them; the absence of an edge is the operator's assertion that the issues are parallel-safe. Encode file contention as a dependency when decomposing (in `feature-delivery` / `project-management`).

### Concurrency safety (learned the hard way)

Parallelism without isolation **loses work**. Two agents in one working tree race and clobber; a `--force` worktree teardown wipes a sibling's uncommitted changes; in-memory dedup doesn't survive a second session. Non-negotiable rules (see `git-workflow` → "Concurrency safety"):

- **Per-agent worktree isolation is mandatory for any parallel mutating agent.** The reference script dispatches implement/fix with `isolation: 'worktree'`. If you can't isolate, **dispatch serially** — never let two agents share a working tree.
- **One agent per issue, ever.** Claim the issue (`in-progress` label) on dispatch; the scout excludes claimed issues; a flagged-open issue releases its claim for retry. Never two agents on the same issue.
- **Commit-early.** Implementers commit as soon as a scaffold works — uncommitted work is the only work that can vanish.
- **One orchestration at a time per repo.** Don't run two `/orchestrate`/`/deliver` sessions against the same repo concurrently — they double-dispatch and collide.
- **Never `--force`-remove or reset a worktree with uncommitted/unpushed work.** Verify `git status --porcelain` and `git log @{u}..` are empty first; only the creator removes its worktree, after merge/push.

## Guards

| Guard | Rule |
|---|---|
| **TERMINATION** | The dispatch loop drains ready issues until open issues = 0 (or a RUNAWAY/budget guard trips). It then runs a **Verify** step — `node scripts/ci/validate.mjs` plus the project's test suites. A red Verify is reported as a non-success outcome (flag + stop), never silently swallowed. The goal counts as *reached* only when open issues = 0 AND validate is green AND tests pass. |
| **VERIFICATION** | Every PR passes through the staff-engineer review gate before merge. The reviewer is read-only and returns findings only — the **merge runs at the main-session/workflow level**, only after the gate approves. Never merge unreviewed. On non-approval: exactly one fix pass, then one re-review; if it still fails, flag the issue open and continue to the next. |
| **SECURITY GATE** | A second, conditional gate: after staff approves, `security-architect` runs the deep `security-review` audit when the diff is **security-sensitive** (the staff reviewer flags it) or the run forces `securityReview: 'always'`. Both gates must approve to merge; a failed audit gets one security fix pass, then re-audit, else flag open — same discipline as the review gate. Default `'sensitive'` keeps cost down (deep audit only on auth/crypto/secrets/untrusted-input/tenancy/supply-chain diffs); `'off'` disables it. Read-only, top-tier model. |
| **RUNAWAY** | Hard max-iteration CAP (default **20** rounds). Also stop when `budget.remaining() < THRESHOLD` (default **5000**) if running via the Workflow tool. (A consecutive-empty-rounds counter — default **3** — exists as a backstop, but because each issue is attempted at most once per run, the loop normally terminates first by exhausting *ready* issues — the CAP and budget are the load-bearing guards.) All three are **user-overridable** — see "Tuning the guards" below. |
| **DURABLE STATE** | GitHub issues + a progress ledger file (`.superpowers/delivery-progress.md`) are the resume map. They survive crash and context compaction. On resume, trust closed issues and `git log` over in-memory state — never reconstruct history from memory. |
| **CONTEXT-ROT** | Run the `handoff` skill before ending any session with open issues. Prefer a fresh Claude Code session between phases or large work chunks — long sessions accumulate stale reasoning. |

### Tuning the guards

All three RUNAWAY knobs are parameterizable per run; omit any to keep its default:

| Guard | Default | `/orchestrate` flag | Workflow `args` key |
|---|---|---|---|
| Max loop rounds (CAP) | 20 | `--rounds N` | `maxRounds` |
| Consecutive empty rounds | 3 | `--empty-rounds N` | `maxEmptyRounds` |
| Budget threshold (tokens) | 5000 | `--budget N` | `budgetThreshold` |

- Via command: `/orchestrate <goal> --rounds 30 --budget 0` (`--budget 0` disables the budget check).
- Via the Workflow tool directly: `args: { maxRounds: 30, maxEmptyRounds: 5, budgetThreshold: 0 }`. The reference script reads these from the `args` global and falls back to each default for any omitted key.

## Model & effort tiering

This is the concrete Scout → Build → Verify application of the **required Model selection rubric** in `project-management` → "Model selection (required at dispatch)" — read that for the general rule. Model is **always specified** per dispatch; an omitted model silently inherits the session's most expensive one. Tier by **task cognitive load, not agent identity** — complexity varies within an agent, and pinning a model in agent frontmatter is too coarse (and would override the user's session choice). Agents stay `model: inherit`; pick the tier per dispatch via the Workflow `agent()` `model`/`effort` opts (or, in `/loop` mode, by which model the dispatching step uses). The review gate omits `model` *deliberately* so it inherits the session's top model.

| Stage | Model | Effort | Why |
|---|---|---|---|
| Scout (list/parse issues) | haiku | low | mechanical: run `gh`, parse JSON |
| Implement / fix | sonnet | medium | strong, fast, cheap for spec→code |
| **Review / re-review (the GATE)** | **inherit (session top model, e.g. Opus)** | **high** | never downgrade the gate — it's the quality backstop |
| **Security audit (2nd gate, conditional)** | **inherit (session top model)** | **high** | `security-architect` deep audit — same tier as the review gate |
| Merge | haiku | low | runs one `gh pr merge` |
| Verify (CI + tests) | sonnet | low | run commands, interpret pass/fail |

The reference script encodes this in its `MODEL` map and applies it per stage; override any tier via `args.models` (e.g. `args: { models: { implement: { model: 'opus' } } }`). The rule to uphold: **keep the review gate at least as strong as the implementer** — a weaker reviewer than author defeats the gate. This holds by default *as long as the session runs a top-tier model* (review omits `model`, so it inherits the session's; implement is sonnet). If you run the session on a small model, or override the tiers, preserve review ≥ implement yourself — the script does not enforce it.

## Two execution modes

### (A) Workflow tool — preferred for a bounded goal

Run the reference script via the **Workflow tool**, passing its absolute path as `scriptPath`:

```
Workflow({
  scriptPath: "<plugin>/scripts/workflows/deliver.workflow.mjs",
  args: { maxRounds: 12, budgetThreshold: 50000, securityReview: "sensitive" },
})
```

Resolve `<plugin>` at runtime — it's `${CLAUDE_PLUGIN_ROOT}/scripts/workflows/deliver.workflow.mjs`, or locate the installed copy with `find ~/.claude/plugins -name deliver.workflow.mjs`. The script is a **reference template reached by `scriptPath`, not a registered workflow name** — `Workflow({ name: 'deliver' })` will not find it.

This gives deterministic Scout → Build → Verify fan-out, **automatic model tiering** (scout/merge haiku, implement sonnet, review + security gates inherit top), the guard caps, and the conditional security gate. The agents run in the **session's working directory**, so their `gh`/`git` target this repo's issues.

**Opt-in + the two gotchas:**
- The Workflow tool fires only on explicit user opt-in (e.g. "run it with the Workflow tool"). **`/orchestrate` does NOT auto-select mode A** — bare `/orchestrate` runs mode B below. To force the script from the command, the user appends "use the Workflow tool (mode A)".
- All overrides go through `args`: `maxRounds`, `maxEmptyRounds`, `budgetThreshold` (a literal `0` disables the budget check — set a real floor for unattended runs), `parallel`, `models`, `securityReview` (`sensitive` default / `always` / `off`), `labels`, `excludeLabels`. The script normalizes `args` whether it arrives as an object or a JSON string, so either is safe; omitted keys keep their defaults.
- **Scope to one epic/wave with `labels`** (string, comma-list, or array): the loop drives only issues carrying one of those labels — e.g. `args: { labels: 'wave-1' }`. Scout still lists ALL open issues for dependency truth, so a `wave-1` issue `blockedBy` a still-open `wave-0` issue is correctly held, not built blind. This is the mode-A way to do one-epic-per-cycle.
- **`epic`-labeled issues are NEVER dispatched** — they're milestone containers, not buildable units, and an epic only closes once its children do, so it's also excluded from dependency truth (treating it as a `blockedBy` dep would deadlock its children). Add more non-buildable labels via `excludeLabels` (string/array); `epic` is always excluded.

Review the script before first real use — it creates PRs and merges only after the staff-engineer review gate (and, on sensitive diffs, the security-architect gate) passes.

### (B) `/loop`, ScheduleWakeup, or plain main-session dispatch

Use Claude Code's built-in `/loop` command or `ScheduleWakeup` (host features, not skills in this plugin) to re-check ready issues on each tick (or self-paced), or just run the loop inline in the main session. Good for overnight runs or when the goal spans many sessions. Pair with the DURABLE STATE guard — write the progress ledger each tick so any session can resume.

> **MODEL TIERING IS NOT AUTOMATIC IN MODE B.** Unlike mode A (the Workflow script's `MODEL` map), when the main session dispatches directly it must **set the Agent tool's `model` parameter on every dispatch** — leaving it unset silently inherits the session's most expensive model (the Opus trap). This is mandatory, not advisory:
> - implementer + fix → `model: 'sonnet'`
> - scout / merge / status / validate → `model: 'haiku'`
> - **staff-engineer review gate → omit `model`** (deliberately inherits the session's top tier; never run the gate below the implementer)
>
> If you want tiering without having to remember this on every call, use **mode A** — the Workflow script applies the `MODEL` map deterministically. Mode B tiers only as well as the dispatcher remembers to set `model`.

## Honesty constraint

The loop and all dispatch run **only at the main Claude Code session level**. Subagents cannot spawn other subagents — the harness blocks agent nesting. Specialist agents produce PRs; the loop in the main session merges them per `git-workflow`. Unattended running requires pre-authorized permissions (tool allowlists and `gh` CLI auth).

## Cross-references

- `feature-delivery` — front door for full delivery including planning; run this before autonomous-delivery if the goal is not yet decomposed
- `project-management` — issue decomposition, dependency tracking, dispatch loop
- `git-workflow` — branching, commit conventions, PR sizing, squash-merge
- `staff-engineer` (agent) — review gate; invoked after every implementation PR
- `handoff` — write before ending any session with open issues
- `principles-dry-kiss` — KISS/YAGNI: only run the phases and guards the goal actually needs
