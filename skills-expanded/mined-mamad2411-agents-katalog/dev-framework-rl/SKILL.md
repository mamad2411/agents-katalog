---
name: dev-framework-rl
description: "RL orchestrator: runs a problem idea-to-ship with critic gates and trajectory logging. Use for 'run an RL episode' or 'loop <target>'."
---

# /dev-framework-rl — Experiential-RL Orchestrator

Runs a development problem as an **episode**: brainstorm a framing, walk the `/dev-framework` stages, gate each stage with a critic sub-agent, log the whole trajectory to SQLite, and (later phases) compute a reward and learn from it.

The policy is prompts + memories — Claude's weights are frozen. This is experiential-RL: the system improves by accumulating trajectories and updating skill prompts, not by gradient descent.

## Current state

All phases through Tier 8 are shipped and tested (real-DB suite under `tests/`).
Full tier history, ship dates, and design detail live in `RL-PLAN.md` (v0.7) and
`README.md` — this file holds only operating instructions. Running today: episode
lifecycle + host locks (`episodes.db`), per-stage manifests, 7 verdict critics, 8
per-type reward rubrics, secret scrubbing on every DB write, per-episode +
cross-episode learning, the batch ritual, critic-trust attribution
(observation-only), and every command in the CLI table at the bottom.

Post-deploy outcomes: finalize auto-schedules a 7-day check; the `devrl-post-deploy`
cron (daily 09:00 Europe/London, prompt at
`~/clawd/memory/cron-prompts/devrl-post-deploy.md`) runs the
verification protocol (`gh pr checks` + revert-grep per episode). HARD GUARD:
never mass-mark `--clean` to clear the queue — uncertain outcomes stay `unknown`
and go to the human via Telegram.

## Prerequisites

`episodes.db` must be migrated:

```bash
python ~/.claude/dev-framework/scripts/migrate.py
```

**Invoking devrl — absolute path, never a persisting `cd` (CRITICAL anti-drift
rule).** The Bash-tool cwd PERSISTS across calls: a bare `cd ~/.claude/dev-framework`
silently re-homes every later feature-repo command — the single most recurring
orchestrator friction, and memory-recalled discipline demonstrably fails under load.
Mechanics: `python ~/.claude/dev-framework/scripts/devrl.py <cmd>` run FROM the
feature repo (the `python scripts/devrl.py` snippets below are shorthand for that
absolute form), OR a non-persisting subshell `( cd ~/.claude/dev-framework && ... )`;
give EVERY feature-repo command an explicit repo path in the SAME call: `git -C
<repo>` or `npm --prefix <repo>` first, `cd <repo> &&` only for a tool with no such flag.
While this session holds the episode lock, `pre-bash-guard.js` enforces this: it
denies a git/npm/npx/vitest/codex command with no absolute `cd`, `-C` or `--prefix`
in the same call, and git that throws away uncommitted work (checkout --, restore,
reset --hard, clean -f, stash other than list/show) unless the command carries
`DEVRL_ALLOW_DESTRUCTIVE=1`. Critics that mutate code change a copy, never the tree.
Full incident detail: AUDIT-RULES.md "cwd-drift".

## Episode lifecycle

### 1. Init and lock

```bash
python scripts/devrl.py episode-init "<problem statement>" --token-budget 200000 --wallclock-budget-sec 5400
```

Capture the printed 26-char episode id as `$EID`. Then claim the host lock:

```bash
python scripts/devrl.py lock-acquire $EID --session "$CLAUDE_CODE_SESSION_ID"
```

Pass the real Claude Code session id, never a made-up label: `episode_sessions` keeps it, and it is the join key to hippo's `recall_traces.session_id`.

Exit 1 / "denied" → another session owns this episode. **Stop.** Do not proceed.

Heartbeat the lock (`lock-heartbeat $EID`) at least every few minutes during long stages — a lock un-heartbeated for 5 minutes is reaped and the episode marked `stalled`.

**Background-op heartbeat discipline.** Long background ops (Workflow builds, full
test suites, codex reviews) silently burn the 5-minute lock window: heartbeat
immediately BEFORE and AFTER every such op; on `lock-vanished`, re-acquire and
continue. Never `&&`-chain a manifest write (or any required step) after
`lock-heartbeat` — a vanished lock exits non-zero and aborts the chain; write the
manifest unconditionally on its own line. A background heartbeat loop branches on
the exit code, never on stdout: `lock-heartbeat` prints `ok` on stdout, or
`lock-vanished` on stderr with exit 1. Loop shape: `python $D lock-heartbeat $EID
>/dev/null 2>/dev/null || python $D lock-acquire $EID --session "<session-id>"`.
Full incident: AUDIT-RULES.md
"background-op heartbeat".

**Isolate into a dedicated worktree at episode START for high-contention repos.**
TRIGGER: `git worktree list` shows active `.claude/worktrees/` agents, or another
session may checkout the shared tree. Right after `lock-acquire`:
`git worktree add -b <feat-branch> <path> origin/master`, then `npm install`
+ `npm run build` in the worktree (do NOT junction `node_modules`: npm
destroys a non-directory junction on its first install, arriving-empty cost a
build round on 2026-08-02; a real install is seconds on this repo), do ALL
edits/commits/codex/build/test there; remove at close-out (if a legacy
junction exists, `rmdir` it BEFORE `git worktree remove` or the removal can
follow it into the main repo's node_modules). Before any version bump:
`git fetch origin && git show origin/master:package.json | grep version` and bump
PAST a concurrent merge. Full incidents: AUDIT-RULES.md "episode-start worktree
isolation".

**Probation-memory exposure (R9, 2026-06-09).** Right after `lock-acquire`, run `python scripts/devrl.py memory-list --status probation`. Carry the relevant memories into this episode's stage briefs tagged `[PROBATION]` — they are unconfirmed hints, not settled law — and record each one's id on the steps where it was in scope (`step-record ... --memory-ref <id>`). This is what lets a useful memory earn its 3 shipped-episode confirmations and a useless one earn its deprecation; a probation memory kept out of context can never do either.

### 1.5 Codex availability probe (recommended)

The `review` stage gates on `codex-review-critic`, which requires the `codex` CLI. Probe at episode-init so an unreachable codex doesn't surface as a surprise blocker mid-episode. Run:

```bash
_CODEX_BIN=$(which codex 2>/dev/null || echo "")
if [ -z "$_CODEX_BIN" ]; then
  echo "WARN: codex CLI not installed. codex-review-critic at the review stage will fail."
  echo "  Either install: npm install -g @openai/codex"
  echo "  Or proceed knowing the review stage will need manual /codex from another session"
  echo "  (paste the verdict back to the orchestrator)."
  python scripts/devrl.py episode-friction $EID --note "codex CLI not installed at episode-init; codex-review-critic will need manual /codex from another session."
fi
```

If codex is missing, decide upfront whether to (a) install it, (b) skip codex-review-critic with explicit human override at the review stage, or (c) defer the episode entirely. Surfacing this at init beats surfacing it at review-stage round 1.

(Incident 2026-05-26, hippo C5: mid-episode codex unavailability paused the review stage; an init-time probe would have caught it upfront.)

**Pin cwd for `codex review --uncommitted` — use the wrapper.** `codex review
--uncommitted` reviews the CURRENT cwd's repo; after any devrl command that can
mean dev-framework itself. Never call it bare from an orchestrator session — invoke
`bash ~/.claude/dev-framework/scripts/codex-review-pinned.sh <feature-repo> [args]`
(subshell-cds, verifies codex's `workdir` line, exit 3 = review VOID). It adds
`--uncommitted` itself unless you pass `--uncommitted`, `--base` or `--commit`.
It also exits 3 before codex runs when an uncommitted review would see a clean
tree, and after codex when the output ends in "Review was interrupted" (usage
limit or capacity: zero findings, even when codex exited 0). Full incident:
AUDIT-RULES.md "codex review cwd pinning".

**Codex-on-Windows root cause + hard timeout (2026-08-02, episode 01KZ1FHCK).**
Codex's Windows sandbox helper receives its policy on the command line; at
~33.9KB payload it exceeds the 32,767-char CreateProcess limit (os error 206),
EVERY shell exec fails, and `codex review` stalls forever instead of failing
fast — a 2h14m silent hang. The wrapper now defaults
`-c 'sandbox_mode="danger-full-access"'` (bypasses the broken helper),
`-c 'notify=[]'` (disables the computer-use turn-end hook), and a hard
`timeout` (default 600s, override `CODEX_REVIEW_TIMEOUT`; 124 => exit 3 VOID).
The old `-c "mcp_servers={}"` guard no longer disables MCP in codex 0.144.x —
do not rely on it. NEVER run codex as an unbounded background job: watchdog by
output-file mtime, not just content.

**Base-aware invocation (2026-08-15, episode 01M025CW434ZAPVSFC61BGFGCT).**
Check `git status` in the feature repo BEFORE invoking the wrapper:
- Work already committed => `--uncommitted` reviews NOTHING, and the wrapper
  now VOIDs it (exit 3) before codex runs. Pass `--base origin/master` (or the base sha).
  Codex rejects `--base` combined with a positional prompt — use the flag alone.
- Re-review rounds after fix commits => scope to the DELTA with
  `--base <prior-commit-sha>`. A grown multi-commit branch (~4k insertions)
  blew a 900s timeout on a full re-review; the delta-scoped run completed.
- Full-branch reviews of substantial diffs => set `CODEX_REVIEW_TIMEOUT=900`
  or higher. The 600s default killed one review AFTER it had written complete
  findings (VOID by wrapper contract; findings salvageable only as unverified
  input, re-verify against source).
Memory: `feedback_codex_review_base_aware.md` (tier-1, probation).

### 1.6 Publish credentials probe (recommended for `library` / package releases)

If the episode will publish a package at the deploy stage (npm, PyPI, crates,
etc.), the publish credentials live with the human, not the orchestration
session. An episode that bumps versions, passes every gate, and merges, only to
hit a 401 at `npm publish`, has surfaced an avoidable blocker after the work is
already done. Probe at episode-init, the same way §1.5 probes codex:

```bash
# npm — only if this release publishes to npm
npm whoami >/dev/null 2>&1 || {
  echo "WARN: not authenticated to npm; deploy-stage 'npm publish' will 401."
  python scripts/devrl.py episode-friction $EID --note "npm not authenticated at episode-init; publish will be a manual operator step or needs 'npm login' first."
}
# PyPI — only if this release publishes a Python package
[ -n "$TWINE_PASSWORD" ] || [ -f ~/.pypirc ] || {
  echo "WARN: no PyPI token in env or ~/.pypirc; deploy-stage twine upload will hang/fail."
  python scripts/devrl.py episode-friction $EID --note "no PyPI token at episode-init; SDK publish will be a manual operator step (TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-... --non-interactive)."
}
```

If creds are missing, decide upfront whether to (a) have the operator authenticate (`! npm login`, export the PyPI token) so the deploy stage can publish, (b) treat publish as a documented manual handoff and tag-only, or (c) defer. Either way the deploy-gate human checkpoint should state the publish path explicitly rather than discovering the 401 after merge.

(Incident 2026-05-28, hippo v1.15.0: all gates passed and the PR merged, then `npm publish` 401'd — publish became a manual after-the-fact operator step.)

### 2. Brainstorm pre-stage

Run `/office-hours` (builder mode) or `/brainstorming` to generate 3-5 candidate framings of the problem. Pick the strongest.

**Then work your own pick, twice: build it out, then break it.**

**Build it out with `/grilling`.** Map the framing as a design tree and work the frontier: every decision whose prerequisites are already settled. Ask the whole frontier in one round, numbered, each question carrying your recommended answer. Then answer your own round: the orchestrator is the respondent here, and the recommendations exist so it can decide without a human. Escalate only a question whose answer is on the ASK-FIRST list in `~/.claude/CLAUDE.md` (a fork between two readings is not on it: pick one and record it); everything else takes the recommendation and records it. Finding facts is the orchestrator's job: dispatch a sub-agent for anything the repo, the DB or a tool can answer, and ask the rest of the frontier while it runs. The pre-stage is done when the frontier is empty, so nothing reaches `plan` silently assumed.

**Then break it with `/grill-me`.** "Me" is the orchestrator (you). The grill is adversarial: interrogate the assumptions in your own selection, name the weakest premise, surface what would have to be true for this framing to win, and what would falsify it. If the grill breaks the framing, return to the candidate list and pick a different one (or refine).

Two passes, not one. `/grill-me` attacks the answers you already have; it never surfaces the question you failed to ask. Every brainstorm concern from either pass is carried forward into `plan` under the §4 rule, so an unvisited branch here is an unvisited branch the plan-eng-critic will never see. Record the chosen framing + the grill's strongest counter-point + your response in the step summary:

```bash
python scripts/devrl.py step-record $EID brainstorm --skill /office-hours --critic-status n/a --summary "<chosen framing + grill's strongest objection + how you addressed it>"
```

(The `brainstorm-judge` critic that ranks candidates automatically is a separate follow-up — it needs a ranking contract distinct from the pass/fail verdict critics. For now, choose deliberately, grill your own choice, and record your reasoning in the summary.)

### 3. Discover and stage plan

Invoke `/dev-framework discover` with `$EID` in context. It emits `trajectories/$EID/stage-plan.json`. Validate it:

```bash
python scripts/validate_manifest.py plan trajectories/$EID/stage-plan.json
```

Read the plan's `project_type` and `rubric_file`, then:

```bash
python scripts/devrl.py set-project-type $EID <project_type> <rubric_file>
python scripts/devrl.py step-record $EID discover --skill /dev-framework --critic-status n/a --summary "<what discover found>"
```

### 3b. Pre-plan codebase audit (mandatory between discover and the first plan stage)

A deterministic audit pass between discover and the first plan invocation: greps are
free; the same drifts cost a critic round each when found later. Run the applicable
rules in ONE batch of parallel Grep calls before invoking `/dev-framework plan`.
Each rule: TRIGGER → action. Full detail + incidents: `AUDIT-RULES.md` (read a rule's
section when it fires or the plan matches its shape).

1. **TODOS staleness reproduce-check** — TRIGGER: the brief references TODO/backlog
   items. Grep each item's named symbol/test/CLI-flag/file; already shipped → abort
   the episode as a reproduce-check WIN (sync TODOS.md, finalize `aborted`; a WIN is
   a successful episode and breaker-exempt). → AUDIT-RULES.md #1
2. **Parallel allow-list grep** — TRIGGER: the plan adds an entry to ANY
   allow-list/registry/`Set`/`Map` (incl. repeatable-CLI-flag allow-lists in argv
   parsers). Grep the exact pattern repo-wide; N>1 sites → the plan must enumerate
   all N (a repeatable flag missing from the parser list is silently last-wins).
   → AUDIT-RULES.md #2
3. **Version-bump target count** — TRIGGER: the plan ships a version bump. Enumerate
   every manifest via git grep; for version CONSTANTS in code, also grep the TEST
   assertions that hard-code the old number. → AUDIT-RULES.md #3
4. **Roadmap-sync sweep**. TRIGGER: the episode cites a roadmap claim
   ("never measured", "Track X blocked"). Grep `docs/evals/` for results docs newer
   than the roadmap doc's mtime. → AUDIT-RULES.md #4
5. **Public-API caller audit** — TRIGGER: the plan changes a function signature.
   Grep callers at EVERY import surface (`from X import`, `sys.path` inserts,
   `spec_from_file_location`, dynamic `require()`), not just internal helpers.
   → AUDIT-RULES.md #5
6. **Functional-duplicate check** — TRIGGER: the plan ADDS a user-facing artifact
   (page/calculator/route/endpoint). Grep existing artifacts' titles AND
   descriptions for the same CAPABILITY — a slug/name collision check alone is
   insufficient. → AUDIT-RULES.md #6
7. **Temporal / as-of query check** — TRIGGER: the plan builds a "what was X at time
   T" query. Mirror an existing temporal pattern (hippo `src/recall-history.ts`
   successor-aware `asOf`); the plan must enumerate valid-time vs transaction-time,
   which row statuses are included, and the date-granularity contract.
   → AUDIT-RULES.md #7
8. **Sibling-clone audit** — TRIGGER: the plan mirrors an existing sibling
   route/module/handler. Audit the pattern being cloned for latent bugs before
   replicating (e.g. `?limit=` needs `Number.isInteger`); prefer one shared helper
   over an Nth copy. → AUDIT-RULES.md #8
9. **Cross-cap consistency** — TRIGGER: the plan generates/assembles a value stored
   into a length-capped field. Prove `N × per_item_cap + overhead <= column_cap` or
   require budget-aware assembly. → AUDIT-RULES.md #9
10. **Reserved-word column check** — TRIGGER: a migration adds a column. Check each
    name against SQL reserved words (`trigger`, `order`, `group`, ...); rename with
    a safe suffix and map back to the domain field. → AUDIT-RULES.md #10
11. **Bidirectional denormalized-value guard** — TRIGGER: a child row denormalizes a
    parent value with a "child matches parent" guard. A forward guard on the child
    is NOT sufficient — also spec a parent-side reverse guard (or explicitly accept
    parent immutability). Cover BOTH directions. → AUDIT-RULES.md #11
12. **Fail-soft post-commit side-effect** — TRIGGER: the plan adds a best-effort
    side-effect after a committed write (enqueue/mark-dirty/notify/invalidate).
    Enumerate the loss windows UP FRONT; state per window: closed, or accepted
    self-healing (and how). → AUDIT-RULES.md #12
13. **Bounded-neighbourhood / focus query** — TRIGGER: the plan builds a
    focus/subgraph/k-hop query with a limit. Run the six-point correctness
    checklist UP FRONT (seed, edges, SQL-pushed bound, truncation flags, cap
    alignment, one snapshot). → AUDIT-RULES.md #13
14. **FK-action / trigger firing — verify empirically** — TRIGGER: a migration
    combines FK `ON DELETE` actions with `BEFORE` triggers on the same table. Do NOT
    reason from docs; probe in a `:memory:` db (`node:sqlite` fires BEFORE UPDATE
    from `ON DELETE SET NULL` even with recursive_triggers OFF). → AUDIT-RULES.md #14
15. **Dual-provenance invariant matrix** — TRIGGER: row validity depends on >1
    provenance source or a denormalized copy. Enumerate the guard matrix at plan
    time; ONE shared invariant helper at EVERY write path. → AUDIT-RULES.md #15
16. **Already-shipped / already-fixed check** — TRIGGER: every episode, before
    brainstorm (direct invocations included). `git fetch origin`; resolve the
    DEFAULT branch (never hardcoded); diff `HEAD..origin/<default>` + grep the
    feature's key terms across the origin tree; `gh pr list --search "<terms>"`; and
    local work: running/stalled episodes, worktrees and branches naming the item.
    Hit → STOP and reframe to the user. Network/auth failure → warn and proceed.
    → AUDIT-RULES.md #16
17. **Per-site fix-plan greps** — TRIGGER: the plan maps fixes to specific sites.
    BEFORE writing the mapping, grep: existing helpers with the same purpose; the
    real call chain into each edited function; the enclosing function at each cited
    line; same-function siblings sharing the defect class. Names/line-proximity
    reasoning is reliably wrong. → AUDIT-RULES.md #17
18. **Search-first for external solutions** — TRIGGER: the plan BUILDS new
    non-trivial machinery (parser, scheduler, diff engine, retry/queue layer,
    protocol client, algorithm implementation). Before the plan stage, search for an
    existing library/built-in/pattern ("<runtime> <thing> built-in", "<thing> best
    practice <year>") and state in the plan what was found and why build-vs-adopt.
    Rules 6/16 catch internal and already-shipped duplicates; this catches
    reinventing an external wheel. → AUDIT-RULES.md #18
19. **Dataset-invariant audit (eval episodes)** — TRIGGER: the episode builds or
    pre-registers an eval harness/protocol over a dataset. BEFORE any pre-reg doc
    locks, script three <5-min checks against the REAL data: (a) temporal ordering
    (any context timestamps after the evaluation timestamp?), (b) per-feature
    variance through the real ingest path on a small sample, (c) duplicate-content
    rates (tie-break stress). Paste the outputs into the plan. Memory:
    `feedback_eval_prereg_dataset_invariant_audit`. (LC2-E1 2026-08-09: skipping
    this cost 2 protocol amendments + two 77-minute full reruns; a critic and codex
    each found one of the missed invariants empirically.) → AUDIT-RULES.md #19
20. **Researched-dataset verifier pass** — TRIGGER: the plan builds a facts table
    (vendor terms, prices, fees, perks) by sub-agent research from web sources. The
    plan must add a separate READ-ONLY verifier task: a second sub-agent re-opens each
    row's cited source and reports MATCH / MISMATCH per field before the execute
    manifest emits; the producer never grades its own rows. (boring-maths card
    rewards 2026-09-02: a 5-row spot-check of a 22-row Sonnet dataset found 3 field
    errors.) → AUDIT-RULES.md #20
21. **Per-value state matrix** — TRIGGER: the plan adds or changes a function that
    moves a row between states and takes an enum or union parameter (outcome, status,
    mode). The plan names, for EACH value, the target state and every side effect (rows
    promoted, runs closed, events emitted), and the test plan has one test per value.
    (hippo W2a 2026-09-13: `complete --outcome failure|partial` had no target state of
    its own and promoted dependents like `success`; no test covered either value, and
    it survived every gate until the ship-stage final review.) → AUDIT-RULES.md #21
22. **Cross-process concurrency drive** — TRIGGER: the plan's correctness rests
    on concurrent SQLite connections (`BEGIN IMMEDIATE`, `busy_timeout`, leases,
    claims, sweeps). The verify plan must race at least two OS processes against
    the built CLI, in both orderings, plus one writer blocked past `busy_timeout`.
    A worker thread inside one test process does not count. → AUDIT-RULES.md #22
23. **Census regen command.** TRIGGER: a plan, critic brief or PR body claims a count
    or a complete set ("N sites already do X", "every caller", a census table). The
    claim carries the one-line command that regenerates it, with its denominator, and
    the critic is briefed to re-run that command rather than read the table. A bucket
    marked "already guarded" says what the guard does on the bad input, not that one
    exists. (hippo 1.44.0 cycle: a "27 sites" count was 30; a hand-copied census lost
    four sites; `cli.ts:8197` sat in the safe bucket and was not safe.) → AUDIT-RULES.md #23

Record the audit as a step:
```bash
python scripts/devrl.py step-record $EID codebase-audit --skill /dev-framework-rl --critic-status n/a --summary "<grep results: N TODOS items reproduce-checked; M allow-list sites identified; K version-bump targets enumerated; J docs/evals/ results-docs scanned; L public-API caller surfaces audited>"
```

**Then record every rule you RAN, and say whether it found anything (C1 policy decay).** Record the ones that ran clean too, not only the ones that hit:
```bash
python scripts/devrl.py audit-record $EID \
  --rule <slug>[:what-you-checked] \      # ran, found nothing (repeatable)
  --caught <slug>[:what-it-found]         # ran and found something (repeatable)
```
A rule that runs every episode and never once catches anything costs tokens forever and scores highest on firing count alone, so `--rule` vs `--caught` is the whole measurement. Passing the same slug to both exits 2. Only the FIRST colon splits, so a note may contain `file.ts:42`.
Stable slugs (never renumbered; rule № → slug): 1=`todos-staleness`, 2=`parallel-allow-list`, 3=`version-bump-targets`, 4=`roadmap-evals-freshness`, 5=`public-api-callers`, 6=`functional-duplicate`, 7=`temporal-as-of`, 8=`sibling-clone`, 9=`cross-cap-consistency`, 10=`reserved-word-column`, 11=`bidirectional-guard`, 12=`fail-soft-post-commit`, 13=`bounded-neighbourhood`, 14=`fk-trigger-empirical`, 15=`dual-provenance-matrix`, 16=`already-shipped-origin`, 17=`per-site-plan-greps`, 18=`search-first-external`, 19=`dataset-invariant-audit`, 20=`researched-dataset-verify`, 21=`per-value-state-matrix`, 22=`cross-process-race-drive`, 23=`census-regen-command`. `policy-compact-report` proposes two kinds of retirement, both propose-only, and absence alone never demotes: `demotion_candidates` never fire at all, `never_caught_candidates` fire but have never found anything across at least `--min-scored` scored firings. Firings recorded before migration 0017 carry no verdict and count as `unscored`, never as clean, so they can never retire a rule.

If the audit surfaces a reproduce-check WIN, jump to finalize (skip plan/execute/verify/review/ship). The win IS the deliverable.

### 4. Stage loop

Iterate the `stages` list from `stage-plan.json` (NOT a hardcoded 9). For each stage after `discover`:

1. Invoke `/dev-framework <stage>` with `$EID` in context.
2. Validate the emitted manifest:
   ```bash
   python scripts/validate_manifest.py manifest trajectories/$EID/<stage>.manifest.json
   ```
   Validation failure → record the step with `--critic-status error` and **escalate to the human**.
3. If the stage has critic(s) — `critic_registry.STAGE_CRITICS` maps each gated stage to its critics (`plan` → `plan-eng-critic` + `plan-design-critic`, `execute` → `code-review-critic`, `review` → `independent-review-critic` + `codex-review-critic`, `ship` → `ship-readiness-critic`, `deploy` → `canary-monitor`). These are the exact names `critic-check` accepts — pass them verbatim (every critic carries the `-critic` suffix except `canary-monitor`). For each critic of this stage:
   - Launch a `senior-code-reviewer` sub-agent. Brief it with the full contents of that critic's briefing (`prompts/critic-<role>.md`) plus the milestone goal and the stage's artifacts from the manifest. Pass the briefing's findings shape through verbatim — `{"severity", "message", "location"}` per finding, extra keys forbidden — and never restate the output contract in your own words: a brief that asked for `{severity, section, issue, fix}` made `critic-check` reject a real plan-eng verdict and cost a round (2026-09-02, boring-maths `01M1H905JWGMPA1GGC9PR24JBB`). (`plan-design-critic` runs only for UI projects.) **Exception: `independent-review-critic` gets NO critic-briefing wrapper** — one Sonnet coordinator runs the `/code-review` plugin protocol and the orchestrator grades its findings into the critic contract (see the `review` bullet in §4a); the zero-tool-calls check below applies to that coordinator too.
   - **If the plan artifact is an existing repo doc** (e.g. `docs/.../plans/<date>-<name>.md`) rather than an in-episode draft, brief the critic explicitly that any `Status: Draft` or `not yet reviewed` marker means the doc has NOT been engineering-reviewed yet; fresh-eyes scrutiny is the point. A pre-existing plan author's reasoning is not pre-vetted, and the orchestrator should not defer to its existing prose. (Incident 2026-05-23, resona Phase A: fresh-eyes briefing caught a cross-org schema leak in a 5-day-old draft.)
   - **For the `plan` stage specifically: pre-stage brainstorm concerns must be carried forward into the revised plan.** When entering `plan`, re-read the brainstorm step's `summary` field (via `episode-steps`). Each concern surfaced there must be either explicitly addressed in the revised plan artifact OR explicitly noted as out-of-scope in the plan manifest. Don't let brainstorm-stage framing dissolve before the plan-eng-critic runs — the critic only judges what's IN the revised plan, not what was flagged during brainstorm. (Incident 2026-05-23, resona Phase B: brainstorm-flagged rate-limiting never reached the revised plan; the gap surfaced at review and cost a retry.)
   - **Confirm the sub-agent actually read the artifacts.** If its result reports zero tool calls, it produced a verdict from the prompt text without opening the diff / plan / files — discard it, do NOT `step-record` it, and re-launch the critic. If a re-launched critic again returns zero tool calls, record `--critic-status error` and escalate. A critic that read nothing has not reviewed; the critic briefings mandate file reads for the same reason.
   - Save the sub-agent's response to a temp file, then:
     ```bash
     python scripts/devrl.py critic-check <critic-name> <temp-file> --tool-uses <N>
     ```
     `<N>` is the sub-agent's tool-call count as the harness reports it. Without the flag `critic-check` exits 2 with `missing_tool_uses` (re-run it with the count); on `0` it exits 2 with `zero_tool_uses` (discard the verdict and relaunch, per the bullet above). Neither is the parse-error exit 2 below.
   - **Exit 0 (pass)** → `step-record ... --critic <critic-name> --critic-status pass --critic-score <n>`. **A pass is spot-checked like a fail:** if the brief singled out a question and the pass carries no finding on it, read the source for that question yourself before recording the pass. The zero-tool-call check catches a critic that read nothing; this catches one that read everything and missed what it was sent for (hippo `01M2ZSMFG8JXSM7PH10EVZNZBW`: pass 95 on 24 tool uses, then four plugin lanes found a verified HIGH on the brief's own focus item 3).
   - **Exit 1 (fail)** → `step-record ... --critic <critic-name> --critic-status fail --critic-score <n> --must-fix "..."`. Re-run the stage with the must-fix fed back, up to the per-stage cap (plan 3, execute 2, review 1, ship 1; `--retry-count <n+1> --retry-strategy revise_with_feedback`). Cap hit → **escalate to the human**. **Root-cause pass before the final retry (added
2026-07-18):** when a stage's critic has failed twice consecutively AND the must-fix
describes a DEFECT (failing test, wrong behavior, crash) rather than a plan/scope gap,
run `/investigate` on the defect BEFORE the last permitted retry — the final attempt
must be built on a named root cause, never a third revise-with-feedback guess (global
rule: after 2 failed iterations, reconsider instead of retry). Record the
investigation's one-line cause in the retry step's summary. **Cap-extension carve-out (learned 2026-06-02, hippo A7 recall-trace):** when a plan round returns score ≥ 75, 0 `crit`, and the SOLE remaining finding is a one-clause fix the orchestrator introduced in its OWN prior revision, a single one-round cap extension (with operator notification) is permitted before full escalation; escalate if that extension round also fails or introduces a new finding. The cap exists to stop thrashing on a broken plan, not to block a converged one over a self-inflicted typo.
   - **Exit 2 (parse error)** → `step-record ... --critic <critic-name> --critic-status error`, **escalate to the human**.
   - **Blocked by the environment** (usage limit or 429, quota, the critic could not be spawned) → `step-record ... --critic <critic-name> --critic-status n/a` with the request evidence (status, error type, model) in `--summary`, plus a row in `~/.claude/BLOCKERS.md`. Never `pass`: `critic-trust` and the reward would read a verdict nobody produced. A parse failure or a zero-tool-call critic is still `error`. The stage may close on its other critics only if at least one of them ran and passed and the summary names the blocked leg; if no critic of the stage could run, stop and escalate (headless: finalize `aborted`). (hippo `01M31TT9V02KG7STNABGYHEAA2`: both Sonnet review legs hit the weekly limit and the stage closed on codex alone, recorded as blocked.)

   **`--critic` is mandatory on every `pass` and `fail`** and `step-record` exits 2 without it. Pass the same registry name you gave `critic-check`. A verdict with no critic named cannot be attributed, and `critic_pass_rate` and `critic-trust` both read exactly these rows. Between 2026-05 and 2026-09-01 the flag was optional and 548 of 658 graded steps went unattributed (all 47 of July's), which is why no per-critic trend can be reconstructed for that period.
   The stage advances only when all of its critics pass, or under the blocked-leg rule above.

   **Two critics in one stage round each take their own `--retry-count`.** `steps` is `UNIQUE(episode_id, stage, retry_count)`, so the second critic's `step-record` at the first critic's count fails on that constraint. Record it at the next free count with no `--retry-strategy`, and say "second critic, same round, not a retry" in `--summary`; a real retry takes the count after that. `learn-check` already reads such a slot as a second critic, not a retry (`learn.py` `_is_second_critic_not_retry`), and the per-stage cap counts retries, not slots. suiren `01M36PTD3Q6V89C7E6DAXPCJQA` review: codex fail at 0, independent-review pass at 1, codex retry pass at 2.

   **CI gate (`ship` / `deploy` stages) — a critic verdict is not the repo's CI.**
   Before the `ship` stage opens a PR and before the `deploy` stage merges one,
   run `gh pr checks <PR>` and require every *required* check green. A red
   required check blocks — do not merge. A red *non-required* check must be
   explicitly classified as pre-existing (`gh run list` evidence it failed on
   the base branch before this episode) or fixed first. Never tell the human
   "all gates passed" meaning the critic gates while repo CI is red — they are
   different gates; report both. Mergeability is a reading that expires with the next
   push to master: at the ship stage, `git fetch`, re-run
   `git merge-tree --write-tree --name-only origin/master HEAD` and read its exit code
   (0 clean, 1 conflicts). Never carry a plan-stage mergeability note forward (hippo
   `01M31TT9V02KG7STNABGYHEAA2`).

   **Stacked PRs on a squash-merge repo (2026-09-02, boring-maths #25 → #26 → #27).**
   Squashing the base PR rewrites the commits the next PR still carries, so GitHub
   reports that PR CONFLICTING the moment it is retargeted. For each next PR, BEFORE
   `gh pr edit <N> --base master`: `git rebase --onto origin/master <old-base-tip>
   <branch>`, confirm `git diff --stat <old-tip> <branch>` is empty, then
   `git push --force-with-lease=refs/heads/<branch>:<old-sha>`. Never
   `--delete-branch` on an intermediate merge — GitHub auto-closes every PR stacked
   on a deleted base (memory `feedback_gh_pr_merge_delete_branch_cascade`).
4. If the stage has no critic → `step-record $EID <stage> --critic-status n/a --summary "..."`, advance.
5. Heartbeat the lock.

### 4a. Mandatory skill hooks per stage

Three Keith-validated release-chain skills are wired into the stage loop. They are NOT critics (no `critic-check` parsing) — they run *before* the stage's critics so the diff arriving at each critic has already been self-reviewed and sanity-checked. Skip them and the critics waste sub-agent budget on issues the skill would have caught.

- **`execute` stage — run `/self-review` as the tail step before manifest emit.** Same-session pass over the diff just produced. Catches missed requirements, regressions, and forgotten edge cases that `code-review-critic` would otherwise spend a sub-agent finding. Record the summary in the manifest's `self_review_summary` field — the schema enforces this at `stage: execute, status: completed`, so the validator will reject the manifest without it. If `/self-review` surfaces a must-fix, address it in-stage before emitting the manifest — do not advance. The self-review adds two checks of its own. **Before a second patch to the same function in one episode**, write the one line naming what the two attempts had in common; if that line names the approach, replace the mechanism instead of widening it (hippo `01M312K37C0262B66J70SM6PCQ`: line-based reasoning about block structure failed twice). **When a change widens what a guard, validator or check watches**, re-read every message it can emit and ask whether each is still true of the new set: a diagnostic that names a cause is an assertion (hippo `01M31DR9BAD95WQ5DJTX03Z1FC`: once the store guard watched every ancestor `.hippo`, "A test wrote a store without isolating it" could blame a test for a write made by ordinary session activity).

- **`verify` stage: drive the affected flow end-to-end as the tail step before manifest emit.**
  Re-running the test suite is necessary but not sufficient: exercise the AFFECTED
  FLOW in the real app/CLI and observe behavior — the class of runtime
  regression that green tests and `gh pr checks` both miss (the CI-red-merge incident's
  root cause). For UI projects use `/qa-only` (browser QA, report-only) as the driver;
  for CLIs/APIs run the real commands/requests against the built artifact. Record what was driven + observed in the verify manifest's
  `verify_skill_summary` field (optional schema field today; may be promoted to required
  once the workflow shape stabilises). A behavioral mismatch found here is fixed in-stage
  before the manifest emits — do not advance. **An absence assertion needs one mutation:**
  when a test's whole value is "this pattern is absent from the tree", verify is not done
  until one deliberate violation has been shown to turn it red (hippo
  `01M312K37C0262B66J70SM6PCQ`: the shape arm of `tests/rollback-guard.test.ts`).

- **`review` stage — the official `/code-review` plugin implements `independent-review-critic` (rewired 2026-08-02, no fallback — Keith directive).** Sequence: commit the episode's work in the worktree, push the branch, open a DRAFT PR (`gh pr create --draft`), then hand the plugin protocol (`claude-plugins-official:code-review`, with the PR number) to ONE `general-purpose` sub-agent on `model: "sonnet"`, briefed with the protocol verbatim: the five lenses, the 0-100 rubric, the false-positive list and the house blind-spot checklist. That coordinator re-derives the load-bearing facts from its own `git diff origin/master...HEAD` before it pools the lenses. Inline, the fan-out and every scorer run in the orchestrator's context and nothing checks a lens against the real diff (hippo `01M31DR9BAD95WQ5DJTX03Z1FC`: 191,476 tokens kept out of the orchestrator, and the coordinator's diff caught a lens reporting an uncommitted edit as PR content; this supersedes the inline precedent of PRs #200 to #203). The protocol fans out 5 parallel Sonnet reviewers + per-issue confidence scorers and filters findings below 80/100 — adversarially verified findings, which matters because the review stage has a retry cap of 1 and one false positive burns the only retry. **NEVER use Haiku anywhere in this skill (Keith directive 2026-09-13).** The plugin's prose prescribes Haiku for the eligibility check, the guidance-file list, the PR summary and the per-issue scorers; run every one of those on `model: "sonnet"`. Measured 2026-09-13 on hippo PR 191: the Haiku PR summary called a pre-existing file new, one Haiku scorer gave a comment-length nitpick 75, and another gave a real one-token bug 90 that Sonnet re-scored at 75 with better evidence. A judge that misfires in both directions defeats the 80 filter. Grade the surviving findings into the critic contract (findings -> `--must-fix`, score per `prompts/critic-independent-review.md`, then `critic-check independent-review-critic`); pass the briefing's house blind-spot checklist (SQL safety, LLM trust boundaries, conditional side effects, CLI dual-write patterns) in the invocation args. TWO TRAPS, both verified 2026-08-02: (a) the BUNDLED skill also named `code-review` is operator-only (`disable-model-invocation`) — a bare `Skill(code-review)` call errors; use the plugin-qualified name; (b) NEVER wire `/code-review ultra` — billed cloud review, user-triggered only. The `ship` stage then marks the PR ready-for-review instead of creating it. Both `independent-review-critic` and `codex-review-critic` still gate independently; codex stays the cross-model second opinion. **Convergence is design evidence:** when several independent reviewers land on one finding in code already patched once this episode, replace the mechanism rather than extend it (hippo `01M312K37C0262B66J70SM6PCQ`: reviewers 1, 2, 3 and 5 hit the same false negative in an area already widened once).

- **`ship` stage — run `/ship-check` as the first step.** Pre-PR sanity pass: what shipped, is it worth shipping, did we do enough QA? Save the output to the manifest's `ship_check_summary` field — the schema enforces this at `stage: ship, status: completed`, so the validator will reject the manifest without it. Pass the summary to `ship-readiness-critic` as input. A blocker from `/ship-check` short-circuits the stage — escalate to the human rather than asking the critic to rubber-stamp it.

- **`ship` stage: Opus final-review pass for the hardest changes (Keith directive, 2026-08-23; moved from Fable to Opus 2026-09-26 per the 2026-09-23 routing rule, Fable only on explicit ask).** TRIGGER (any): a schema migration; security- or tenant-isolation-touched code; a change to a core write-path / invariant primitive (the `upsertEntryRow` class); or a diff over ~500 changed lines. When it fires, after `/ship-check` but BEFORE `ship-readiness-critic`: spawn exactly ONE Agent sub-agent with `model: "opus"`, briefed with the full diff, the plan artifact, and all prior critic + codex verdicts. Its job is a fresh adversarial "would you ship this?" pass: surface what every earlier gate missed, not re-run their checklists. Real defects it finds are must-fix in-stage before `ship-readiness-critic` runs; append its one-line verdict to the ship step's `--summary`. Re-read the cited lines before applying a suggested fix, and record per finding whether the fix was taken, changed or passed over, with the reason. One pass per episode, at this point only, never a fan-out. Non-triggering episodes skip it silently: the stage critics and codex already cover routine diffs.

- **`ship` stage — record deploy metadata right after the ship step is recorded.** `python ~/.claude/dev-framework/scripts/devrl.py episode-deploy-record $EID --pr-url <PR-URL>` (the ship manifest schema now REQUIRES a `pr_url` artifact at `status: completed`; a sanctioned no-PR ship — direct-commit / quant pipelines — records the literal `none`). It attaches to the latest `ship`/`deploy` step and never creates one, so it exits 2 until `step-record $EID ship ...` has run. The draft PR opens back at `review`, but its URL is recorded here, on its own line after the ship `step-record` (failure cluster `record-ship-step`: calling it first aborted a chained command). At the `deploy` stage after merge, re-run with `--merge-commit <SHA>`. This is the producer feeding `episode-deploy-meta`, the `devrl-post-deploy` cron, and every outcome-weighted learning leg — an episode that skips it can never resolve a post-deploy outcome (the 0/95 outcome-starvation root cause, fixed 2026-06-09, PLAN-continuous-loop Phase A).

- **`ship` stage — run `/quiz-me from-diff HEAD` after `/ship-check`, before `ship-readiness-critic`.** Operator-knowledge gate. Generates 5 MC + 1 explain-back from the episode's diff, quizzes the human operator interactively, grades honestly. Then runs `python ~/.claude/skills/quiz-me/scripts/quiz.py gate` — exit 1 blocks the ship stage until the operator clears any failed cards via a follow-up `/quiz-me` session. **Ask before the first card.** Wherever the quiz runs with the operator present (here, or at the loop-mode batch gate), ask one plain question first: run the quiz now, or skip it. When the same sitting carries a sign-off question (a Stage 6 promotion gate, a merge yes or no), ask the sign-off first and the quiz question after it, never mixed in (suiren `01M36PTD3Q6V89C7E6DAXPCJQA`: the cards arrived inside the Stage 6 sitting and the operator stopped after card 1, "are you quizing me now? skip the quiz-me part"). Save the quiz summary in the manifest's `quiz_me_summary` field. The schema requires it at `stage: ship, status: completed` (`schemas/stage-manifest.schema.json`), so the validator rejects the manifest without it; a waived quiz records `quiz_me_summary: "Waived by the operator: <their words>"`. This is what enforces "no new features until the operator understands the last one" — the orchestrator's other gates protect against bad code, this one protects against bad operator mental models. Skip this gate in headless / spawned-session mode (no human at the keyboard to quiz); record `quiz_me_summary: "skipped (headless)"` in the manifest so the gap is visible. **Loop mode: defer, don't skip** — record `quiz_me_summary: "deferred to batch gate (loop mode)"` and run the accumulated quizzes (plus `quiz.py gate`) at the batch deploy gate, one sitting with the human present, asked after the deploy decision; a failed gate holds `batch-deploy`.

- **`plan` stage — run `/grill-me` as the tail step before plan-eng-critic.** "Me" here is the orchestrator (you). The grill interrogates the orchestrator's own plan: weakest premise, hidden assumptions, what would have to be true for this plan to work, what would falsify it, which scope claims are unsupported. The grill output is INPUT to plan-eng-critic — the critic should judge whether the plan addresses the grill's objections or explicitly accepts them as out-of-scope. Save the grill summary in the manifest's `self_grill_summary` field (optional schema field today; may be promoted to required in a future iteration once the workflow shape stabilises). If the grill destroys the plan (a premise can't be defended), revise the plan before plan-eng-critic runs — do not present a known-broken plan to the critic. The grill also restates each defect the plan fixes as the invariant the code needs, not the input shape that broke it; the filed trigger is one member of the class (hippo `01M31TT9V02KG7STNABGYHEAA2`: a guard against "value is boolean" would still have let `--threshold banana` reach the same data loss).

- **`plan` stage — run `/domain-modeling` against the repo's `CONTEXT.md` before the plan artifact is written.** If the repo has a `CONTEXT.md`, the plan uses its terms and no synonyms; a term the plan needs that the glossary does not define is a gap, and the fix is to settle it and write it there inline, not to invent a second word for it in the plan. If the repo has no `CONTEXT.md`, create one at the first term the episode settles and leave it at that: lazy creation, glossary only, no implementation detail, never a spec. Offer an ADR only when all three of the skill's tests hold (hard to reverse, surprising without context, a real trade-off with alternatives). Record the terms touched in the plan manifest's `self_grill_summary` alongside the grill. This is the cheapest defence the orchestrator has against multi-session drift: episodes on one target span compactions, and a glossary on disk survives what the context window does not.

- **`plan` and `execute` critic briefings — pass the `/codebase-design` vocabulary verbatim.** Brief `plan-eng-critic` and `code-review-critic` to phrase every structural finding in that skill's terms: module, interface, implementation, depth, seam, adapter, leverage, locality, plus the deletion test and "one adapter is a hypothetical seam, two is a real one". Do not let a critic reach for component, service, API or boundary. The reason is the learn step, not style: §6 clusters findings across episodes, and clustering is string-shaped, so two critics describing one defect in two vocabularies produce two clusters of one instead of one cluster of two, and the delta never crosses the tier threshold. Findings shape is unchanged (`{"severity", "message", "location"}`); this constrains the wording inside `message`.

- **(Optional, opt-in) Meta-critic mode** — when a critic returns `pass`, the orchestrator MAY run `/grill-me` against the critic's verdict + reasoning, asking "did this pass actually hold up under adversarial pressure?" If the grill breaks the pass (surfaces an issue the critic missed), the verdict becomes provisional: record as `friction` via `episode-friction` and either re-run the stage with the missed concern in the must-fix, or escalate to the human. This is expensive (extra sub-agent per pass) and OFF by default — opt-in via `episode-init --meta-critic-grill`. Reserve for high-stakes episodes (production deploys, schema migrations, security-touched diffs). Tier 10's `learn-evolve` reads `friction` notes flagged this way to propose critic-prompt mutations.

`/full-power` is deliberately NOT wired — the orchestrator already fans out sub-agents per critic, so layering it on inflates token cost without changing behaviour. The four grill-family wires each earn their slot at a different point: `/grilling` opens the design tree at brainstorm (what did we fail to ask?), `/grill-me` attacks the answers at brainstorm, plan and optionally each verdict (what did we get wrong?), `/domain-modeling` fixes the words at plan (are we all saying the same thing?), and `/codebase-design` fixes the words the critics use (can the learn step count these?). None of them is a general "try harder" mode; drop one and a specific failure comes back.

### 4b. Execution delegation: the orchestrator does not code

The session model is the ORCHESTRATOR:
framing, triage, plan authorship, sub-agent briefs, gate parsing, verdicts,
trajectory bookkeeping, and the final synthesis. It does NOT write
implementation code inline. (Incident 2026-07-04: the orchestrator implemented a whole execute stage
inline — expensive session-model tokens, no author/reviewer separation.)

- **Execute-stage implementation (code + tests + mechanical doc edits) goes to
  Agent-tool sub-agents with `model: "sonnet"`.** Brief each executor with:
  the plan file path, the episode's execute-entry checks, the exact files/
  regions to touch, the project conventions that bind (real-DB tests, additive
  public API, AGENTS.md rules), and what NOT to touch. Prefer one executor per
  coherent task (T1/T2/T3), parallel when files are disjoint, sequential when
  they overlap. The worktree-isolation rules above apply unchanged.
- **The orchestrator reviews every executor diff before accepting it** (read
  the diff, check it against the plan and entry checks), runs `/self-review`
  itself, and owns all commits. Executor output is a proposal, not a merge.
- **Small-fix carve-out:** one-to-few-line fixes the orchestrator can specify
  byte-exactly (a review round's single-clause fix, a version-string bump, a
  comment correction) MAY be applied directly — dispatching an executor for a
  two-line edit costs more than it saves. The moment a fix needs design
  judgment or touches more than ~10 lines, it goes to an executor.
- **Discovery fan-out** (broad greps across many files, existing-pattern
  hunts) goes to Explore/sonnet sub-agents when it would bloat orchestrator
  context; targeted single-file reads the orchestrator needs verbatim in
  context stay inline.
- **Never spawn `model: "haiku"` for any role in this skill: executor, critic, scorer, eligibility check, summary or lookup.** Keith directive 2026-09-13; evidence in the `review` bullet above. Sonnet is the floor.
- **Critic model routing: critics run `model: "opus"`.** A critic verdict is a
  review, and `~/.claude/CLAUDE.md` (Sub-agents, 2026-09-23) routes every review
  to Opus with no per-task cap. The CLOSED A/B below (flat reward, 2026-08-02)
  predates that rule. Mechanical roles (executors, discovery) stay on Sonnet.
- Record each executor dispatch on the execute step via `step-record ...
  --prompt <executor-brief-summary>` so the trajectory shows who authored what.

**Critic-model A/B — CLOSED (verdict read 2026-08-02 at the pre-registered
4-shipped-episodes-per-arm point).** The question was: do Opus critics earn
their premium over Sonnet 5 critics? Answer: no measured premium. Mean reward
23.06 (default-opus) vs 22.63 (default-sonnet); regression 0.0 in both arms
(2 known outcomes each); friction 4/4 vs 3/4 episodes. FLAT at this n; the
2026-09-23 routing rule then moved critics to `model: "opus"` (routing bullet
above). Labels retired: `episode-init` uses the plain `default` critic set;
do NOT alternate arms. Re-open only with a bigger pre-registered n if
critic-trust drops post-switch. Two standing notes survive the retirement: `codex-review-critic`
always runs — the cross-model catch is the safety net (01KWQF28's
window-starvation P2 was missed by three Opus-tier critics and caught only by
codex); and `independent-review-critic` runs via `/code-review` since
2026-08-02, so read `critic-ab-report` / `critic-trust` for that critic with
the swap-date confound in mind.

### 5. Finalize

The **final ship gate is human-in-loop** — the orchestrator never auto-marks an episode `shipped`. Present the trajectory (`episode-get $EID` + `episode-steps $EID`), let the human confirm, then:

```bash
python scripts/devrl.py episode-finalize $EID --status <shipped|aborted|cap-exceeded>
python scripts/devrl.py reward $EID --automated-score <0-100>
python scripts/devrl.py lock-release $EID
```

`reward` loads the per-type rubric, derives the gates (shipped, all-critics-passed) and the user-satisfaction component from the DB, and writes `final_reward` + `reward_breakdown`. Pass `--automated-score` from the verify-stage results. Downstream-stability is left deferred — it resolves after the next episode — so the score is **provisional** until then. The scalar is a dashboard metric; the learn step keys off the trajectory, not this number.

**"Ship it" includes the npm build (Keith standing directive, 2026-08-03).** For npm-package projects (hippo), the human's "ship it" covers merge AND refreshing the live binary: from a CLEAN checkout of merged master (temp worktree if the main checkout is dirty), `npm install` + `npm run build:all` + `npm pack` + `npm i -g ./<tarball>.tgz`. NEVER `npm i -g .` from a temp dir — folder installs SYMLINK to the folder, and tearing the worktree down guts the global (2026-08-03 incident: MODULE_NOT_FOUND an hour after "verified"). Verify AFTER teardown: `<cli> --version` works and the global package is a real dir, not a symlink. Registry publish stays a separate /publish-repo decision.

Roughly 7 days after a shipped episode's deploy, record whether it held up: `python scripts/devrl.py episode-postdeploy $EID --clean` (or `--regressed`). This feeds the learn mode's `regression_rate` weighting.

At the start of any orchestrator session, run `devrl.py status` — it surfaces pending satisfaction prompts; record them then (`satisfaction-pending` prints ready-to-run commands, `satisfaction-record-batch ID=SCORE ...` records several at once).

### 5b. Episode close-out (MANDATORY after finalize, ship AND abort)

"Ship it" ends when the environment is clean, not when the merge lands.
Nothing may be reported to the operator as "left over" unless it is
human-only (quiz, satisfaction scores) or held by ANOTHER live session's
resources — and then name exactly which. Checklist, in order:

1. **Kill your own orphans FIRST.** TaskStop kills the harness task, NOT
   detached process trees. Query by path before teardown:
   `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*<worktree-name>*' }`
   — wrapper bash shells, tsserver/typingsInstaller from the worktree's
   node_modules, and build daemons are the usual holders. Kill only
   processes traceable to THIS episode's commands; never another session's
   (the shared repo runs concurrent agents).
2. **Teardown**: `git worktree remove --force <path>` (then `rm -rf` the
   husk), `git worktree prune`, delete the merged branch local AND remote.
   A dir that stays busy after step 1 is another session's handle — report
   it by name, don't fight it.
3. **npm projects on "ship it"**: build + refresh the global install per
   the standing directive above; verify `<cli> --version` and (for hippo)
   that the live store migrated.
4. **Docs the episode owns**: commit + push episode-related doc edits
   sitting in the MAIN checkout (rebase with `--autostash` if the tree
   carries other WIP). Non-episode WIP: identify it precisely (read the
   diff, say what it IS) and report — NEVER absorb, commit, or discard it.
5. **Memory writebacks**: project memory files + MEMORY.md index + hippo
   remember/capture/outcome; confirm probation memories that earned their
   keep (`devrl.py memory-confirm`).
6. **Sweep**: no running background tasks from this episode (check by CIM,
   not by task list), scratchpad temp files are disposable by location, the
   trajectory dir holds all manifests.

### 6. Learn step (per-episode)

After finalize + reward, run the learn check:

```bash
python scripts/devrl.py learn-check $EID
```

Exit 0 → nothing to learn; the episode is done. Exit 1 → a learn trigger fired (`critic_pass_rate < 0.6`, `human_redirects >= 2`, or `operator_friction` — any recorded friction note). The command prints a JSON report of the trajectory facts: failed stages, retried stages, the aggregated `must_fix` items from the failing critics, and `friction_items`.

**Recording friction.** If at any point during the episode you hit operator friction — a missing command, a manifest that misled, a doc that lied, a step painful for a reason no critic would catch — record it:

```bash
python scripts/devrl.py episode-friction $EID --note "<what was painful / what should improve>"
```

Notes accumulate on a single `friction` step and are inert to the critic, reward, and budget math. A clean episode with friction has nothing for the critics to fail, so friction is the channel that carries that signal into the learn step.

When triggered, read the report and propose **1-3** concrete deltas — each an audit rule, a hippo memory, a skill prompt, or (rarely) a CLAUDE.md, per the tier model under Learn mode, asking tier 0's "before X, check Y" question first — that would have prevented the observed failure or friction pattern. Present them as a consolidated-revisions blob: section reference, one-sentence issue, concrete fix.

**Never auto-apply tier-2 (skill prompts) or tier-3 (CLAUDE.md) deltas** — even headless; wait for the human's explicit "apply" and the human makes the edit. **The single exception (B4, Keith-approved 2026-06-09): tier-1 hippo probation memories.** The per-episode learn step MAY write the hippo memory and register it without waiting:

```bash
python scripts/devrl.py memory-register <memory-id> --auto-tier1 --episode $EID [--cluster <cluster-id>] --summary "<one-line delta summary>"
```

The command REJECTS memories lacking a valid `warning_pattern:` frontmatter (add the regex first — never accept-and-flag) and writes the `policy_updates(trigger='auto-tier1')` audit row in the same transaction. Auto-added memories auto-promote at 3 QUALIFYING confirmations (the confirming episode terminated `shipped`) and auto-deprecate on 0 qualifying confirmations across the next 10 terminal episodes OR a regressed-scope hit (the memory was in `step_prompts.hippo_memory_refs` of a failing stage of a later-regressed episode). The weekly digest lists every auto-added / promoted / deprecated memory.

Base the proposal on the *trajectory* (the failed stages, their `must_fix` items, and any `friction_items`), not on `final_reward`. The scalar reward is a dashboard metric; the structured trajectory is the learning signal.

The batch `learn` mode below does cross-episode failure-mode clustering and owns the `policy_updates` audit trail. This per-episode step is deliberately thin: detect, surface, propose.

## Learn mode (`/dev-framework-rl learn`)

A separate mode from running an episode — the cross-episode pass. Run it periodically (weekly, or after a batch of episodes): cluster recurring failures, propose policy deltas, record what gets applied.

### Where a delta lands — the tier model

Pick the tier by how settled and how cross-cutting the lesson is:

0. **Audit rule**: reach here FIRST whenever the lesson can be written as "before X, check Y". An audit rule is a TRIGGER plus a concrete check that a later episode either runs or does not, and `audit-record` logs each firing. That makes it the only tier that produces its own evidence: `devrl.py policy-compact-report` prints the current firings per rule. Tiers 1 to 3 are prose, and prose cannot be counted or pruned. (`audit_rule_firings.prevented` is that note, a TEXT column, not a count. Do not aggregate it arithmetically.) Adding one means editing three surfaces that must stay 1:1: `episode_store.AUDIT_RULE_SLUGS`, the compact rule plus its `→ AUDIT-RULES.md #N` pointer and slug line in §3b of this file, and the numbered detail section in `AUDIT-RULES.md`. Run `pytest tests/test_audit_rules_sync.py` after; it fails on any surface you miss. A lesson that cannot be phrased as a pre-check is not an audit rule: send it to tier 1.
1. **Hippo memory** — for lessons with no check to run. Small or tentative. Cheap, decays, probation-gated (`--memory-added`).
2. **Skill prompt** — when a workflow or critic actually behaved wrong. Medium weight. Recorded with `--skill-changed <path>`.
3. **CLAUDE.md (project or global)** — the top tier, deliberately rare. Only a lesson that recurred across many episodes, is a genuine cross-cutting rule, and would keep happening otherwise — a "law", not a tip. Tips go to tier 1.

Tier 3's bar is high because a CLAUDE.md loads into every session: it costs tokens every run and is the highest-blast-radius place to be wrong. A cluster qualifies only when its `regression_rate` is non-trivial (it recurred *and* caused real post-deploy regressions), not merely high `occurrences`. Record it like a skill: `--skill-changed <path-to-that-CLAUDE.md>` (the audit trail hashes any path). Two guards apply: the learn loop never auto-applies, so Keith approves every promotion, and a full rewrite of a CLAUDE.md still needs show-content and an explicit apply (global Hand-Maintained-Files rule). A targeted Edit goes straight in, with git history as the backup. Episodes record `project_type`, not a project path; the human names the exact file at approval time.

### 0. Score what you already applied

```bash
python scripts/devrl.py learn-effect
python scripts/devrl.py policy-compact-report
```

Run BOTH first, before proposing anything new. They score the two halves of the
policy surface: `learn-effect` scores deltas, `policy-compact-report` scores
audit rules. Pruning is half of getting better, and only these two commands can
tell you what to cut.

`policy-compact-report` lists every rule's firings, catches, clean runs and
catch rate, then names two retirement classes: `demotion_candidates` never fire
at all, and `never_caught_candidates` fire but have never found anything. Both
propose only; a human demotes. It also prints `unknown_slugs_recorded`, which is
non-empty when a rule exists on some surfaces but not in `AUDIT_RULE_SLUGS`.
Treat any entry there as a bug in the three-surface contract, not as data.

A rule with a high firing count and a `catch_rate` of 0.0 is the expensive case:
it runs every episode, costs tokens every episode, and has never once paid for
itself. Firing count alone rates that rule highest, which is why catch rate
exists. A `catch_rate` of `null` means the rule has no scored firings yet.

For every cluster with a fix
recorded against it, it prints occurrences before vs after `applied_at`, plus
`episodes_since` — zero recurrence with zero episodes since is `untested`, not a
win. Three verdicts: `held`, `recurred`, `untested`.

This is the only falsifier the learn loop has. A delta that changed nothing
recurs at the same rate, and without this step the loop proposes forever and
never finds out. Read it as a brief: a `recurred` cluster means the previous
delta was wrong, so propose a different KIND of fix, not the same one again.

It also prints `policy updates: N total, M linked to no failure mode`. That M is
the count of deltas nothing can ever score. Keep it near zero.

### 1. Recompute clusters

```bash
python scripts/devrl.py learn-cluster
```

Re-clusters every failed step's `must_fix` item and every operator `friction` note across all episodes into lexical failure modes. Human-acted clusters (applied / rejected) keep their status across the recompute.

### 2. List actionable clusters

```bash
python scripts/devrl.py learn-list
```

Prints the `pending` clusters — those with at least 5 occurrences — each with its pattern, example snippets, and `regression_rate` (the fraction of its occurrences whose episode regressed post-deploy; `null` until outcomes are known).

### 3. Propose deltas

For each actionable cluster, propose **one** policy delta per the tier model above. Ask tier 0's question first: can this be phrased as "before X, check Y"? If yes, propose an audit rule and say which of the cluster's occurrences the check would have caught. Only when the answer is no does the proposal become a hippo memory, a skill prompt, or (rarely) a CLAUDE.md. Weight attention by `regression_rate` first (clusters whose failures led to real post-deploy regressions), then by `occurrences`. Present all proposals as a single consolidated-revisions blob: cluster id, one-sentence pattern, concrete fix.

**Never auto-apply** — even headless. Wait for the human's explicit "apply" / "reject" per cluster. (Tier-1 probation memories are the single auto-apply exception — but ONLY in the per-episode learn step, never in this weekly/batch mode: the weekly pass stays strictly propose-only, R8.)

### 4. Record the decision

On apply — the human (or you, with approval) makes the edit, then:

```bash
python scripts/devrl.py learn-apply --summary "<what changed>" --failure-mode <id> [--failure-mode <id> ...] [--skill-changed <path> ...] [--memory-added <id> ...]
```

Writes a `policy_updates` audit row, a `policy_skill_changes` row per edited skill file (with its post-edit SHA-256), and marks the addressed clusters `applied` with an `applied_at` timestamp.

`--failure-mode` is required. It is the join that makes the delta measurable by `learn-effect` later; without it the delta is invisible forever. For a genuine orphan edit — friction below the 5-occurrence cluster threshold, so there is no cluster to name — pass `--unlinked --unlinked-reason "<why no cluster fits>"` instead, and accept that it can never be scored. Between 2026-05-24 and 2026-09-01 the flag was optional and all 44 recorded deltas omitted it, which is why nothing in the loop could ever be evaluated. `--unlinked-reason` became mandatory on 2026-09-04 so that count stops growing by accident; the reason is the only record an unlinked delta leaves behind.

A delta that adds a hippo memory passes `--memory-added <id>` — the memory enters on **probation**, not yet trusted. Probation memories DO recall into episodes: at episode init run `memory-list --status probation`, carry the relevant ones into stage briefs tagged `[PROBATION]` (an unconfirmed hint — weigh it accordingly, never as settled law), and record their ids via `step-record --memory-ref <id>` so the auto-confirm machinery sees them as active. (R9 fix, 2026-06-09: the old "keep out of episode context until promoted" rule was a deadlock — a memory that is never in context can never earn confirmations; 5 sat stuck with 0 promotions ever.) Promotion to `active` takes 3 QUALIFYING confirmations — auto-confirm only counts episodes that terminated `shipped` (`devrl.py memory-confirm <id>` for manual ones); `memory-deprecate <id>` retires one that is not helping; `memory-list --status probation` shows what is still on probation.

On reject:

```bash
python scripts/devrl.py learn-reject --failure-mode <id> [--failure-mode <id> ...]
```

Applied and rejected clusters are not re-proposed on the next `learn-cluster`. Weight the deltas by what kept failing, not by `final_reward` — see RL-PLAN "Scalar Reward vs Learning Signal".

## Loop mode (`/dev-framework-rl loop <target> [--batch N] [--max-episodes M]`)

The continuous-improvement mode (added 2026-06-10, Keith-approved): one
command, episodes run back-to-back, and the orchestrator SOURCES ITS OWN WORK
when nothing is queued. `<target>` is ONE repo per loop run (e.g. `hippo`) —
a multi-repo product gets one loop per repo, never one loop spanning repos.
Defaults: `--batch 5`, `--max-episodes 15` per loop run.

**No external scheduler is required.** Loop mode runs cycle after cycle
within the live session — finishing an episode starts the next one; ending
the turn mid-loop is a bug, not a feature. External re-entry is only for
session-boundary survival: wrap with `/loop` for self-paced re-invocation
across idle periods, or use the Phase D nightly cron (gated; see
PLAN-continuous-loop.md) for fully headless runs.

### Run state + compaction protocol (context is scratch; files are truth)

All run-level state lives in `<repo>/.devrl-loop-state.json`, rewritten at
every cycle boundary — never carried in conversation memory:

```json
{"run_id": "<ULID>", "target": "<repo>", "batch_id": null,
 "episodes_run": 0, "max_episodes": 15, "batch_size": 5,
 "started_at": "<ISO>", "in_flight_eid": null, "breaker_tally": 0,
 "status": "running"}
```

- **Compact at cycle boundaries, deliberately.** After each episode's
  finalize + reward + lock-release + state-file write — and at every batch
  deploy gate — run `/compact` with a focus instruction naming `run_id`,
  `batch_id`, `episodes_run`/`max_episodes`, and the next backlog item.
  Never let autocompact fire mid-stage: at the boundary everything
  load-bearing is externalized by construction, so compaction is lossless;
  mid-stage (sub-agent verdicts, unrecorded must-fix text) it is not. The
  boundary compact doubles as the externalization test — anything lost there
  was a bookkeeping bug, surfaced immediately instead of at a random
  autocompact.
- **Re-hydrate after any compaction or session resume.** Treat remembered
  context as untrusted: re-read `.devrl-loop-state.json`, `devrl.py status`,
  `batch-get <batch_id>`, `.devrl-backlog.md`, and `episode-steps
  <in_flight_eid>` (if any) BEFORE the next action. Memory-recalled loop
  state fails under load exactly like cwd discipline does; mechanical
  re-derivation doesn't.
- **Run-level caps are wallclock-honest.** Enforce `--max-episodes` from the
  state file's `episodes_run`, never from conversation memory. Check the
  run-level wallclock cap from `started_at` at every boundary. Token totals
  stay advisory, as ever. In loop mode run `budget-check $EID` after EVERY
  stage (not just headless) — it is the PAUSE-sentinel and per-episode
  wallclock enforcement point.

### Target-level loop lock

Episode host-locks do not cover triage/sourcing collisions between two loops
on the same repo. Before the first cycle, claim `<repo>/.devrl-loop.lock`
(JSON: `{"session": "<id>", "heartbeat": "<ISO>"}`; refresh at each cycle
boundary). Another session's lock with a heartbeat younger than 10 minutes →
do NOT loop this target; report and stop. Stale lock → take it over and note
the takeover in `## Done`. Remove the lock on EVERY exit path (see Stop
epilogue).

### Per-cycle procedure

0. **Batch lifecycle.** If the state file has no open `batch_id`:
   `batch-init "<target>-loop-<run_id>-<n>"` and record the returned id in
   the state file. (Tier 7 requires an open batch before any `batch-add`; a
   fresh batch is opened after every deploy gate, never reused across gates.)
1. **Source the backlog** (priority order; reproduce-check every item per the
   triage rules above before it qualifies as an A-item):
   a. `<repo>/.devrl-backlog.md` — the ordered episode backlog this mode
      maintains (create via triage if missing; keep it ordered, dated, with
      one-line acceptance criteria per item).
   b. The repo's `TODOS.md` / issue tracker.
   c. **Trajectory-derived follow-ups for this repo**: low-severity critic
      advisories from PASSED gates, `episode-friction` follow-ups, and
      actionable clusters (`learn-list`) scoped to this target. These are
      pre-vetted by real reviews — they outrank speculative work. NOTE:
      nothing indexes pass-verdict advisories after the fact (`failure_modes`
      stores only failing must-fix items), so capture them AT THE MOMENT a
      pass verdict is parsed — append them to `.devrl-backlog.md`'s candidate
      section right then, while they are still in context.
   d. Known bugs in memory (hippo context / Claude memory files) that
      reproduce-check against current master.
   e. **Opportunity scan — the "go out of your way" stage.** Only when a-d
      are dry: run an improvement audit (standards/security pass, performance
      profile, DX/help-text review, dead-code sweep, test-coverage gaps) and
      GENERATE candidate episodes, ranked by user-visible impact.
2. **Anti-make-work guard (hard).** Every episode entering the backlog —
   especially scan-generated ones — must state (i) the user-visible benefit
   OR a named risk-reduction with a falsifiable failure scenario (security,
   data-loss, correctness debt — "cleaner code" alone does not qualify)
   and (ii) a falsifiable acceptance criterion. A candidate that can't name
   both is logged in `.devrl-backlog.md` under `## Below the bar` and NOT
   run. When a scan yields nothing above the bar, the loop STOPS honestly
   ("backlog dry, no above-bar opportunities") — continuous improvement
   never means inventing busywork.
3. **Run the top item as a full episode** — every gate, hook, and worktree
   rule in this skill applies unchanged, with two loop-mode adjustments:
   (a) **`/quiz-me` is deferred, not skipped** — record
   `quiz_me_summary: "deferred to batch gate (loop mode)"` in the ship
   manifest and run the accumulated quizzes at the batch deploy gate (the
   human is present there anyway); N synchronous quiz interrupts between
   gates would defeat back-to-back execution. (b) **Remove the episode
   worktree right after the ship-stage PR push** (the branch survives;
   `rmdir` a junctioned `node_modules` first, per the worktree section) —
   do not accumulate N worktrees waiting for the batch gate. Ship stage
   stops before deploy; `batch-add` the episode (Tier 7); update the state
   file (`episodes_run += 1`, `in_flight_eid: null`); then compact per the
   protocol above.
4. **Batch deploy gate** every `--batch` episodes, when the backlog empties,
   or on operator request: `batch-finalize`, present the PRs together, ONE
   human deploy decision, then ask whether to run the deferred `/quiz-me`
   sessions (then `quiz.py gate`: a failed gate holds `batch-deploy` exactly
   as it blocks a ship stage), `batch-deploy`, then `episode-deploy-record
   --merge-commit` per merged PR. A project CLAUDE.md may set a standing
   pre-authorization (e.g. "patch-level, all-gates-clean episodes
   auto-merge") — that standing rule IS the human decision, made once (the
   closed-list "Final ship gate" carve-out); without one, deploy always
   waits for the human. After the gate, clear `batch_id` in the state file —
   the next cycle's step 0 opens a fresh batch.
5. **Learn pass after each batch** (`learn-cluster` + `learn-list` +
   propose-only blob; per-episode auto-tier1 memory rules apply as ever),
   then the next cycle begins.

### Stop conditions (closed list)

- `--max-episodes` reached (from the state file's `episodes_run`), or the
  run-level wallclock cap spent (from `started_at`; per-episode budgets as
  usual — token totals stay advisory)
- `PAUSE` sentinel (`~/.claude/dev-framework/PAUSE`) — surfaced by the
  per-stage `budget-check`
- Any operator message mid-loop: heartbeat the lock and **answer the
  operator FIRST** (direct messages pre-empt loop work — global rule), then
  resume the in-flight stage; pause at the next clean boundary only if the
  operator asked for a stop. The lock heartbeat + worktree isolation are
  what make mid-stage resumption safe.
- Two consecutive episodes ending `aborted`/`cap-exceeded` — circuit
  breaker: stop and report instead of burning budget on a stuck pipeline.
  **Reproduce-check WINs are excluded from the tally** (§3b finalizes a
  stale-TODOS win as `aborted`, but a win is not a failure — record it as a
  WIN in `## Done` and leave `breaker_tally` untouched).
- Backlog dry after an opportunity scan with nothing above the bar

### Stop epilogue (mandatory on EVERY exit path, including errors)

1. **Never exit with a silently open batch.** If the current batch has
   members: run the deploy gate now if the human is present; otherwise
   append a `## Handoff` block to `.devrl-backlog.md` naming the open
   `batch_id`, member episode ids, and PR URLs — and say so in the stop
   report. Rationale: `batch-add` NULLs `post_deploy_due_at` and
   `batch-deploy` is its SOLE re-writer (`batch_store.py`), so an abandoned
   open batch makes its episodes invisible to `postdeploy-due` forever —
   the 0/95 outcome-starvation hole, selectively re-opened.
2. Write the state file with `status: "stopped:<reason>"`.
3. Remove `<repo>/.devrl-loop.lock`.

### Loop-mode bookkeeping

Record the loop run itself as friction-free trajectory data: each episode is
normal; additionally append one line per cycle to `.devrl-backlog.md`'s
`## Done` section — `<run_id> | <episode id> | <item> | <outcome>`. The
run_id attribution is what makes `--max-episodes` accounting reconstructable
across compactions and distinguishes concurrent or historical runs. The
weekly learn cron picks up everything else automatically.

## Running across a multi-item roadmap

A single episode is one shippable problem. A project roadmap (a `TODOS.md`, an
issue tracker, a backlog) is not a flat list of episodes: its items range from
one-line fixes to multi-week projects. Do not iterate a backlog top-to-bottom
feeding each line in as an episode. Triage it into episode-sized units first.
This procedure is project-agnostic — it works on any backlog.

### 1. Triage pass (cheap — not itself an episode)

Bucket every open backlog item:

- **A — episode-sized.** A coherent fix or self-contained feature that ships as
  roughly one PR. One `/dev-framework-rl` episode each.
- **B — trivial.** A one-line test gap, a defensive guard, a doc typo. The nine
  stages and the critic sub-agents cost far more than the work and have nothing
  to catch. Batch 4-6 into ONE "hardening pass" episode, or do them as an
  ordinary small PR outside this orchestrator.
- **C — project-sized.** A multi-week effort (a redesign, a new subsystem). Not
  an episode. Run a decomposition pass first (`/office-hours` or
  `/plan-ceo-review`) that splits it into A-sized episodes.

**Reproduce-check every A-item before it enters the backlog.** A backlog item
describes a defect as it was when the item was written; an unrelated refactor
may already have fixed it. Before listing an A-item as an episode, open the
code it names and confirm the described behaviour still exists in current
`master`. An item that no longer reproduces is not an episode — move it to
backlog hygiene and mark the source TODO done, citing the fixing commit. A
`TODOS.md`-internal consistency pass does not catch this; staleness left by a
refactor is only visible in the code.

Also record dependencies and clusters: items that must ship in order, or
together. The output is an **ordered episode backlog**, not a flat checklist.

### 2. Run a batch, holding the gates

Run the backlog about five episodes at a time. Take each episode through
`discover` to `ship` — all the reversible work, including local commits — and
**stop before `deploy`**. Deploy is irreversible (publish, merge, tag) and is a
human-in-loop gate; do not spend that gate once per episode.

### 3. One batched deploy gate

Present the batch's ship-ready episodes together: the human reviews N PRs in one
sitting and makes one deploy decision, instead of N separate interrupts. A
project may instead set a standing pre-authorization (for example "a patch-level
episode that passed every critic clean auto-deploys; minor or major needs the
gate"), recorded in that project's `CLAUDE.md`.

### 4. Learn pass after the batch

After 5-10 episodes, run `/dev-framework-rl learn` (the cross-episode
clustering). One episode's `learn-check` is thin signal; recurring failure modes
only surface across a batch. Apply the policy deltas, then start the next batch.

### Scaling notes

- Fix orchestrator defects before scaling a batch. Running N episodes on a
  known-buggy pipeline multiplies the friction N times.
- Episode cost is real (nine stages, several critic sub-agents, repeated
  build/test). Triage is what keeps the spend proportionate to the work.
- Nothing in this procedure or the critic/reward machinery is project-specific.
  If a future gate genuinely needs project-specific behaviour, key it off the
  `project_type` from `stage-plan.json`, never off a hardcoded project path.

## Human-in-loop gates (closed list — auto-progress everywhere else)

- Schema/migration changes to live data
- Production deploys, force pushes, irreversible shared-infra ops
- Destructive ops (>100 lines deleted, file/branch deletion, DB drops, locked-signal overwrites)
- Paid services / new external services
- Critic retry-cap exceeded (per-stage cap)
- Critic parse error (`critic-check` exit 2)
- Manifest validation failure
- Final ship gate — always (a standing pre-authorization recorded in the project's CLAUDE.md counts as that human decision, made once — see Loop mode step 4 / "One batched deploy gate"; absent one, per-episode or per-batch human confirmation)

**Every escalation on this list appends one row to `~/.claude/BLOCKERS.md`** before the orchestrator stops or parks the episode:

```markdown
## <target>
- [ ] <what Keith must do, one line> | clock: <lead time or "none"> | blocks: episode $EID at <stage> | source: trajectories/$EID/<stage>.manifest.json
```

Clear the row when the gate clears. This is the producer half of `/human-blockers`; without it a parked episode is only discoverable by whoever remembers to open its trajectory. Loop mode makes that worse, not better: a batch can park three episodes on three different human gates overnight, and the loop's own stop epilogue reports them one at a time to a session nobody is reading. Rows in `BLOCKERS.md` survive the session that wrote them.

## Worktree isolation for code episodes (execute stage)

TRIGGER: any CODE episode in a repo with concurrent multi-agent activity (check
`git worktree list`). Do the execute stage in a DEDICATED worktree from the START —
`git worktree add <tmp-path> -b feat/<episode> origin/master` — and edit/build/test
there only. Edit-in-place is unsafe even pre-commit: a concurrent session CAN and
WILL `git checkout` the shared tree mid-stage, moving your uncommitted edits onto
the wrong branch. Reuse the same worktree for the ship-stage commit/push.
`node_modules`: junction from the main checkout; `rmdir` the junction BEFORE
`git worktree remove`. Recovery from a hit (non-destructive, costs a detour) +
both incidents: AUDIT-RULES.md "execute-stage worktree isolation".

## Real test-DB convention (`verify` stage)

If the project's tests need a real database (per the project's rules), start it **outside the execute agent's process group** so the verify stage can re-run against it cheaply.

- Project should ship a `scripts/test-db-up.sh` (or equivalent) the orchestrator session invokes before the execute stage. Port and auth pinned in `.env.example`.
- The execute agent uses the existing instance; it does NOT bootstrap its own. If the execute agent stands up an ad-hoc DB inside its own subprocess tree, the DB dies with the agent and the verify stage cannot re-run.
- The verify agent re-runs `npm test` (or equivalent) against the same instance — second confirmation is cheap.
- If the DB ends up bootstrapped inside the execute agent regardless, document the limitation in the verify manifest (`status: completed` with caveat) and recommend the human re-run before merge. Do NOT auto-fail verify on a one-shot run; do NOT pretend the run is a second confirmation when it is not.
- A brief that drives a CLI names the source file that defines its flags, and bans `--help` probes unless the parser has a help branch for that subcommand. Every drive runs from a temp cwd with a temp store.

(Incident 2026-05-23, resona Phase A: an execute-agent ad-hoc `/tmp/pgdata` PG died with its process group and surviving backends held the port, so verify could not re-run.)

## Headless mode

Run an episode unattended: `claude -p "/dev-framework-rl '<problem>'" --output-format json`. Set the wallclock budget at init — `episode-init --wallclock-budget-sec N`.

After each stage, run the safety check:

```bash
python scripts/devrl.py budget-check $EID --consecutive-fail-cap 3
```

Idle time is not work. When you resume after a human gate, a provider limit (usage limit, 429, auth outage) or an idle session, declare the wait before doing more work:

```bash
python scripts/devrl.py episode-wait $EID --reason "<what it waited on>"
```

The wait runs from the latest recorded step to now. `--since` and `--until` take ISO times with an offset. The command refuses a span that has a recorded step inside it. budget-check leaves declared waits off the wallclock and shows them as `waited_sec`. Never declare work time. If budget-check trips on a wait you never declared, declare it with `--since` and `--until` from the step times (`episode-steps`), then run budget-check again.

Exit 0 → continue. Exit 1 → stop; the JSON `verdict` is one of:
- `paused`: the `~/.claude/dev-framework/PAUSE` sentinel file exists
- `wallclock-exceeded`: elapsed time is past the episode's `wallclock_budget_sec`
- `consecutive-fail-cap`: too many substantive critic fails in a row (`error` and `timeout` are skipped, never counted)
- `critic-unavailable`: the critic errored or timed out N times in a row, so nothing was judged

On a stop verdict, finalize the episode (`--status cap-exceeded`, or `aborted` for a pause or a critic outage) and stop the run. **Read `wallclock-exceeded` against the step timestamps before believing it:** the clock counts sleep, so a large gap since the last step (`episode-steps`) means the session was idle, not that the work stalled. If the gap explains the overrun, continue and record an `episode-friction` note naming it (hippo `01M31TT9V02KG7STNABGYHEAA2`: 108,055 s against a 14,400 s budget, the overrun an overnight gap between verify and review).

Enforced caps are wallclock, consecutive-fail, consecutive critic outages (same cap), and the PAUSE sentinel — all reliably checkable. Token budget is recorded (`episode-init --token-budget`) but advisory only: Claude cannot reliably self-count tokens mid-run, so wallclock is the honest hard cap.

To pause every running episode: `touch ~/.claude/dev-framework/PAUSE` — remove the file to resume.

## CLI reference (`python scripts/devrl.py <cmd>`)

| Command | Purpose | Exit codes |
|---|---|---|
| `status [--json]` | operator dashboard: in-flight + last cluster + last shipped (Tier 0.0) | 0 |
| `episode-init "<problem>" [--critic-set <s>]` | create episode; `--critic-set default\|minimal\|full\|random` (Tier 4) | 0 |
| `episode-get <id>` | print episode JSON | 0 / 2 missing |
| `episode-steps <id>` | print the episode's recorded steps as JSON | 0 / 2 missing |
| `episode-friction <id> --note S` | record an operator friction note (feeds learn-check) | 0 / 2 missing |
| `episode-wait <id> --reason S [--since ISO] [--until ISO]` | declare idle time (human gate, usage limit) so budget-check leaves it off the wallclock; refuses a span with a recorded step inside | 0 / 2 bad span or missing |
| `set-project-type <id> <type> <rubric>` | set type + rubric | 0 |
| `episode-finalize <id> --status <s> [--user-satisfaction N\|deferred] [--redirects N] [--learn-emit] [--no-prompt]` | close episode; `--learn-emit` writes pending_apply blob (Tier 0.2 / Tier 3) | 0 / 2 |
| `satisfaction-record <id> N` | fill in deferred user_satisfaction post-hoc (Tier 0.2) | 0 / 2 missing |
| `episode-postdeploy <id> --clean/--regressed` | record 7-day post-deploy outcome | 0 / 2 missing |
| `postdeploy-due` | list shipped episodes whose 7-day window has passed (Tier 0.1) | 0 |
| `postdeploy-prompt [--within-days N] [--json]` | operator-facing pending summary (table or cron-friendly JSON) (Tier 0.4) | 0 |
| `episode-deploy-meta <id>` | emit pr_url + merge_commit (+ `*_source` provenance) + ended_at (Tier 0.1 / Phase A) | 0 / 2 missing |
| `episode-deploy-record <id> --pr-url U [--merge-commit C] [--source backfill]` | record deploy metadata on the latest ship/deploy step (Phase A producer; `none` = sanctioned no-PR ship) | 0 / 2 |
| `satisfaction-pending [--limit N] [--unnotified-only] [--mark-notified] [--json]` | list deferred satisfaction scores, oldest first (Phase A) | 0 |
| `satisfaction-record-batch ID=SCORE [ID=SCORE ...]` | bulk-record deferred scores, all-or-none (Phase A) | 0 / 2 |
| `lock-acquire <id> --session <s>` | claim host lock | 0 ok / 1 denied |
| `lock-heartbeat <id>` | refresh lock | 0 ok / 1 vanished |
| `lock-release <id>` | release lock | 0 |
| `reap` | mark stale episodes stalled | 0 |
| `step-record <id> <stage> [--prompt SKILL] [--memory-ref ID ...] [--artifact KIND=VALUE ...] [...]` | log a step + optional step_prompts row + value-artifacts (Tier 0.3 / Phase A) | 0 / 2 bad artifact spec |
| `critic-check <critic-name> <file> --tool-uses N` | parse critic response; `N` is the critic sub-agent's harness-reported tool-call count, required (missing or `0` exits 2) | 0 pass / 1 fail / 2 error |
| `brainstorm-rank <id> <candidates.json> --judge <file>\|--select-idx N` | record candidates + ranking (Tier 2) | 0 / 2 |
| `reward <id> [--automated-score N]` | compute + store episode reward | 0 / 2 missing |
| `learn-check <id>` | per-episode learn-trigger check | 0 none / 1 triggered / 2 missing |
| `budget-check <id> [--consecutive-fail-cap N]` | headless safety check; the cap bounds fails and critic outages separately | 0 continue / 1 stop / 2 missing |
| `learn-cluster [--mode lexical\|embedding] [--threshold F]` | recompute failure-mode clusters (Tier 1) | 0 |
| `learn-list` | list actionable clusters | 0 |
| `learn-effect [--json] [--top-unfixed N]` | did applied fixes stop the failure recurring? | 0 |
| `learn-apply --summary S (--failure-mode ID ... \| --unlinked --unlinked-reason R)` | record an applied policy delta | 0 / 2 |
| `learn-reject --failure-mode ID ...` | reject a cluster | 0 |
| `apply-pending <id> [--clear]` | view or clear pending_apply/<id>.json (Tier 3) | 0 / 2 |
| `embed-cache-prune [--older-than N]` | remove embed cache entries older than N days (Tier 1) | 0 |
| `codex-shadow <id> <stage> --local-verdict <v> [--max-wait-sec N] [--brief <file>]` | log codex second opinion; never gates (Tier 5; DEPRECATED 2026-05-24) | 0 / 2 |
| `codex-shadow-report [--since DATE]` | list codex disagreements (Tier 5) | 0 |
| `critic-ab-report [--since DATE]` | per critic_set aggregates over shipped episodes (Tier 4) | 0 |
| `batch-init <name>` | create a batch (Tier 7); fails if name exists | 0 / 2 |
| `batch-add <batch_id> <episode_id>` | add episode (clears its `post_deploy_due_at`) (Tier 7) | 0 / 1 / 2 |
| `batch-list [--open-only]` | list batches (Tier 7) | 0 |
| `batch-get <batch_id>` | show batch + members (Tier 7) | 0 / 2 |
| `batch-finalize <batch_id>` | finalize batch + auto-cluster (Tier 7) | 0 / 1 / 2 |
| `batch-deploy <batch_id> --decision shipped\|aborted\|partial` | record deploy + set due_at for shipped members (Tier 7) | 0 / 1 / 2 |
| `learn-attribute [--since DATE] [--include-backfill]` | recompute critic_trust_scores incl. v2 (Tier 8/9; backfill outcomes excluded by default per R4) | 0 |
| `critic-trust [--critic NAME] [--json]` | read view over critic_trust_scores (Tier 8) | 0 |
| `stage-gate <id> <stage> [--weighted]` | evaluate a stage's gate from recorded verdicts; trust-weighted when episode opted in (Tier 9c) | 0 pass / 1 fail / 2 error |
| `audit-record <id> [--rule SLUG[:note] ...] [--caught SLUG[:note] ...]` | record §3b audit rules that ran; `--rule` found nothing, `--caught` found something (C1) | 0 / 2 |
| `policy-compact-report [--min-episodes N] [--min-scored N]` | propose-only policy-decay report over rule firings and catch rates (C1) | 0 |
| `memory-register <id> [--auto-tier1 --episode E --summary S [--cluster C]]` | register a learn-added memory (probation); auto-tier1 = B4 auto-apply path, rejects without valid warning_pattern | 0 / 2 dup or rejected |
| `memory-confirm <id>` | confirm a memory useful | 0 / 2 missing |
| `memory-deprecate <id>` | retire a memory | 0 / 2 missing |
| `memory-status <id>` | show memory lineage | 0 / 2 missing |
| `memory-list [--status S]` | list memories by lineage status | 0 |
| `memory-needs-pattern` | list probation memories missing `warning_pattern` (Tier 6) | 0 |

All free-text fields are secret-scrubbed before they reach the DB.

## Files

Orchestrator infrastructure lives in `~/.claude/dev-framework/` (see its `README.md`):
- `RL-PLAN.md` — full design (v0.7)
- `episodes.db` — SQLite trajectory store
- `scripts/devrl.py` — the CLI this skill drives
- `scripts/` — `episode_store`, `scrubber`, `critic_contract`, `critic_registry`, `rubric`, `reward`, `learn`, `clustering`, `ulid_gen`, `validate_manifest`, `migrate`
- `adapters/critics.py` — the 7 verdict critics (data-driven)
- `prompts/critic-*.md` — the 7 verdict-critic briefings + `critic-brainstorm-judge.md`
- `rubrics/REWARD.*.md` — 8 per-project-type reward rubrics
- `schemas/` — stage-manifest + stage-plan JSON schemas
- `tests/` — real-DB test suite (`python -m pytest tests/`)
