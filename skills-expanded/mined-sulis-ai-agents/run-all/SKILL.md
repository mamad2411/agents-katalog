---
name: run-all
description: "Builds and ships every ready task in the to-do list."
---

# /sulis:run-all

## Required Reading (load before dispatching)

The loop dispatches executors per `kind:` — every executor brief MUST cite
its per-kind doctrine so the implementation conforms:

- `../../references/standards/WORK_PACKAGE_STANDARD.md` — the `kind:` enum
  (incl. `contract`); the executor dispatches on `kind:`.
- `../../references/standards/WP_BACKEND_STANDARD.md` — load when
  dispatching a `kind: backend` WP.
- `../../references/standards/WP_FRONTEND_STANDARD.md` — load when
  dispatching a `kind: frontend` WP.
- `../../references/standards/CONTRACT_FIRST_STANDARD.md` — load when the
  batch spans a producer/consumer seam (contract WP first, parallel
  per-kind, integration last).
- `../../references/standards/UX_VISUAL_DESIGN_STANDARD.md` — load when
  dispatching a `kind: frontend` WP on a user-facing surface (the visual
  contract is the design artifact the WP builds against).

Pass the relevant per-kind standard to the spawned executor as part of the
WP brief, not as background context — the executor needs the rubric
in-hand.

Walk the Work Package INDEX and ship every ready WP, with parallel
executor dispatch and train-based integration:

- **Per-WP (executors, Steps 1-7):** parallel — `max_parallel` executors
  at a time, gated by INDEX dependency graph.
- **Per-batch (Steps 8-10, wpx-train):** after each executor batch
  returns success and WPs are flipped to `step-7-complete`, this
  skill polls `wpx-train queue-list` and fires `wpx-train run` if
  the trigger is met. The train batches up to 5 WPs into one rebase
  + bundled-tip CI + sequential merge + deploy + health + smoke.
- **Per-batch (Step 10.5, in the calling session, v0.21.1+):** after
  `wpx-train run` returns `outcome: success`, the calling session
  dispatches `/sulis:code-review` against the BATCH DIFF RANGE
  (`<first WP's pre_train_sha>..<last WP's merge_sha_on_dev>`).
  Catches cross-WP composition issues — N+1 across sibling WPs,
  integration regressions, contract drift between interdependent
  WPs. Findings auto-draft remediation WPs (`WP-AUTO-*`); CRITICAL
  findings BLOCKER batch-wide. **Note:** this is post-merge — it
  catches + remediates but doesn't pre-merge-gate; the pre-merge
  variant is deferred future work.
- **Per-batch (Step 11, in the calling session):** after Step 10.5,
  the calling session iterates over the batch's `wps_shipped` and
  dispatches the `sulis-security:security-reviewer` Agent per WP.
  Findings register; non-duplicate findings auto-draft remediation
  WPs (`WP-AUTO-*`). CRITICAL findings BLOCKER + `step-11-blocked`.
  The distributed loop terminates when a subsequent train's Step 11
  produces zero NEW findings (signature-hash dedup ensures
  convergence).
- **Per-WP again (Step 12):** worktree cleanup + INDEX flip from
  `step-7-complete` → `done`. Owned by the WP's executor return
  contract; documented in lifecycle.md.

## How to invoke (MUST — run the loop inline, with parallel batching)

**This is the marketplace's load-bearing dispatch logic.**

When this skill loads, **YOU (the calling session) run the dispatch
loop directly**. Do NOT call `Agent({subagent_type:
"orchestrator", ...})` first. The orchestrator agent
file is architectural-intent reference only — Claude Code's runtime
treats spawned subagents as leaves of the agent tree, so an
orchestrator subagent could not dispatch executor subagents
(production failure observed 2026-05-18).

The calling session DOES have Agent at the top level. So the loop
runs in the calling session; the calling session spawns multiple
executors in parallel as its own subagents (Steps 1-7); after the
executors return, the calling session itself spawns the
security-reviewer for Step 11 (v0.9.0+). All Agent calls are one
level deep from the calling session — well within Claude Code's
depth limits.

### Resolving wpx-* tool paths (MUST — first action, v0.10.1+)

The wpx-* CLI tools (journal, pipeline, blocker, step12, …) live
inside the sulis plugin. When the plugin is installed in
a downstream project, the scripts are at
`~/.claude/plugins/cache/sulis-ai-agents/sulis/<version>/scripts/`,
NOT at a project-relative path. You MUST resolve the tool directory
ONCE at the start of every dispatch session, before reading the
INDEX or doing anything else, and capture the result as
`$WPX_DIR`:

```bash
# Resolve the wpx-* tools dir from the ACTIVE plugin version (the one Claude
# Code loaded — its bin/ is on PATH). Avoids the lexical-sort cache pick that
# mis-ranks 0.98.0 above 0.126.0 (#49).
WPX_DIR=""
_sulis_bin=$(printf '%s\n' "$PATH" | tr ':' '\n' | grep -E 'sulis-ai-agents/sulis/[^/]+/bin$' | head -1)
if [ -n "$_sulis_bin" ] && [ -d "$(dirname "$_sulis_bin")/scripts" ]; then
  WPX_DIR="$(dirname "$_sulis_bin")/scripts"
fi
# Dev fallback: marketplace repo cwd.
if [ -z "$WPX_DIR" ] && [ -f "plugins/sulis/scripts/wpx-journal" ]; then
  WPX_DIR="$(pwd)/plugins/sulis/scripts"
fi
# Last-resort fallback ONLY if PATH anchor + dev both miss: a PORTABLE
# version-aware cache pick (numeric, NOT lexical, NOT `sort -V`).
if [ -z "$WPX_DIR" ]; then
  WPX_DIR=$(find ~/.claude/plugins/cache -name wpx-journal -type f -path '*/sulis/*/scripts/*' 2>/dev/null \
    | sed -E 's#(.*/sulis/)([^/]+)(/scripts/.*)#\2 &#' \
    | sort -t. -k1,1n -k2,2n -k3,3n \
    | tail -1 | cut -d' ' -f2- | xargs -I{} dirname {} 2>/dev/null)
fi
if [ -z "$WPX_DIR" ]; then
  echo "ERROR: cannot locate wpx-* scripts. Run: claude plugin install sulis@sulis-ai-agents" >&2
  exit 1
fi
echo "WPX_DIR=$WPX_DIR"
```

Capture the printed `WPX_DIR` value into your working memory. Every
subsequent wpx-* invocation in this skill uses `"$WPX_DIR/wpx-NAME"`
— substitute the resolved literal path inline at each Bash call.
Environment variables do NOT persist between Bash tool invocations
in Claude Code, so the substitution happens in the prompt text the
agent sends to Bash, not in shell state.

The executor subagents you spawn have the same resolution preamble
in their own prompts (`agents/executor.md`) — they resolve
independently in their own contexts. You do NOT pass `$WPX_DIR` to
them; each subagent finds its own.

## Founder progress discipline (MUST — this is a multi-hour run the founder must be able to TRACK)

A `run-all` is the longest unattended thing Sulis does. The founder is
trusting a multi-hour process they can't watch line-by-line. If the only
signal is an operator firehose (raw SHAs, WP/DC IDs, `rebase+merge`,
`ruff I001`, critical-path arrows), they can't track it and trust collapses
— "it may be right, but I'm putting huge faith in something I can't follow."
Founder-mode is the **default** for the whole loop; the raw stream is opt-in
(`--raw` / `/sulis:jargon on`). Two rules:

**1. Every founder-visible string passes the FE-06 scan — including the
high-frequency surfaces.** This is where jargon leaks because it feels like
"ops chatter, not a real message" (founder-english.md Anchor case 5). It is
not exempt:
- **Bash `description`** and **Agent `description`** — the one line rendered
  above each tool call. Plain English, always (the plain translation of the
  WP title), never a WP/DC ID, SHA, or "Ship WP-NNN". (The raw command +
  output below it are unavoidable harness chrome — leave them; the founder
  accepts those. It's the *description* + your *prose* that must be legible.)
- **Per-wave prose** — no SHAs, no `WP-AJ-NNN`/`DC-NN`, no `rebase`/`FF`/
  `ruff`/`I001`/critical-path arrows. Translate WP titles to what the founder
  asked for ("the sign-up screen", "the billing screen").

**2. Emit a fixed-shape progress frame at each WAVE boundary — not
per-command.** Same template every wave, so the founder tracks the *delta*,
not the mechanism. Four things, always:

> *"Building your app — **{done} of {total} pieces done ({pct}%)**.
> Just finished: {plain titles of the wave that just merged}.
> Now building: {plain titles in flight}.
> Next up: {plain titles of the next ready set}.
> {Nothing needs you — I'll surface anything that does. | ⚠ One thing needs
> you: {plain-English blocker/decision}.}"*

The "needs you / nothing needs you" line is the trust anchor — it tells the
founder, every wave, that nothing is silently broken. Surface blockers +
founder decisions in this frame in plain English (no rule codes); keep the
per-command narration out of the founder's way (it lives in `--raw`).

(Layer-3 follow-on, out of scope here: a living `/sulis:dashboard` / PROGRESS
view at the piece level so tracking can leave the chat stream entirely.)

### The parallel loop

```
loop:
    0. Pre-flight: base branch CI-clean gate (MUST — run BEFORE
       reading the INDEX, before any wave is dispatched).

       Determine the base branch with the SAME CW-04 detection the
       train uses at Step 12 (reuse it — do not re-derive):

           CURRENT_BRANCH=$(git -C <repo-root> branch --show-current)
           if [[ "$CURRENT_BRANCH" == change/* ]]; then
               BASE_BRANCH="$CURRENT_BRANCH"
           else
               BASE_BRANCH="main"
           fi

       Then read the base branch HEAD's CURRENT recorded CI
       conclusion (no polling) via the wpx-preflight gate:

           PREFLIGHT=$("$WPX_DIR/wpx-preflight" dev-clean \
             --repo <org/repo> --branch "$BASE_BRANCH")

       The gate emits the same {"ok", "errors", "warnings"} envelope
       as wpx-arrival-check (parse it the way the loop already parses
       that contract):

       - ok:false  → STOP. The base branch HEAD has pre-existing CI
         failures (landed via a manual/non-train merge). Surface ONE
         plain-English blocker and dispatch NOTHING. This is a hard
         stop — there is no "proceed anyway" path (a red base branch
         is inherited by every branch cut from it, so every WP would
         rediscover the SAME red per-branch). The blocker copy is
         founder-English — no internal IDs, no rule codes, no script
         names. Name the count and the failing checks, lead with what
         to do:

             "<BASE_BRANCH> has N pre-existing CI failures — fix
              these first, then re-run. (Failing checks: <names>.)
              Nothing was dispatched."

         (The count + check names come from the gate's PRE-01 error:
         its `actual` carries "N pre-existing CI failures: [names]".)

       - ok:true   → proceed to step 1 below, exactly as today. A
         green base branch makes the run behave byte-for-byte as it
         did before this gate existed. An advisory `warnings` entry
         (no CI recorded yet, or CI still running) does NOT block —
         the pre-flight reads recorded state, it never waits; an
         absence of evidence is not a red.

       After the dev-clean gate passes (ok:true), and BEFORE reading
       the INDEX, probe branch protection on the base branch ONCE per
       run. This is purely informational — it NEVER blocks the run,
       no matter what it returns:

           PROTECTION=$("$WPX_DIR/wpx-preflight" protection-status \
             --repo <org/repo> --branch "$BASE_BRANCH")

       Read `data.protection` from the JSON it emits:

       - `protected` → say nothing. Protection is in force; the
         automated checks gate every merge. (Public / properly-
         protected repos behave byte-for-byte as before — no notice.)
       - `unconfigured` → say nothing here. The repo CAN enforce
         gating but hasn't set it up; that is a one-time repo-setup
         matter the arrival check already surfaces, not a per-run
         notice.
       - `unavailable-free-plan` → emit the one-time warning below
         (founder-English — no rule codes, no HTTP status, no script
         or command names), THEN PROCEED with the run regardless. Show
         it at most once per run:

             "Heads-up before I start: branch protection isn't
              available on your plan, so the automated checks can't
              block a manual merge — only merges I route through Sulis
              are checked before landing. If you merge by hand or push
              straight to the shared line, nothing stops a broken
              change from landing. To close that gap you can make the
              repo public or move to a paid plan. I'll carry on now."

         This is the awareness notice, not a gate: the run continues
         exactly as it would on a protected repo.

    1. Read .architecture/{project}/work-packages/INDEX.md.

    2. Read INDEX header for max_parallel (default 3 if absent).
       Example header:
           ## Orchestrator Config
           max_parallel: 3

    3. Read .architecture/{project}/work-packages/BLOCKER-*.md
       (any existing blockers).

    4. Build the ready set:
       - All WPs with status == "pending"
       - AND all their dependsOn WPs have status == "done"
       - EXCLUDE status == "auto-draft" (await founder disposition
         via concierge slice-end review)
       - EXCLUDE status == "blocked" / "cancelled" /
         "dependency_blocked"

       HD-008 note (v0.24.0+): status here refers to the STORED
       INDEX.md cell for "pending" / "auto-draft" / "blocked" / etc.
       (operator/executor intent — no authoritative-state correlate)
       and to the COMPUTED status for the "done" check on dependencies
       (derived from origin + train-runs via compute_wp_status). The
       ready-set rule is therefore: stored pending + computed-done
       deps. In practice the loop reads stored cells from INDEX.md
       and treats them as authoritative for operator-intent states;
       the computed-done check fires through wpx-index status
       (--mode computed) or implicitly through wpx-train queue-list
       which now uses computed status per HD-008. A dep whose stored
       cell says done but whose computed status is step-7-complete
       (reverted) correctly blocks the downstream WP from entering
       the ready set.

    5. If ready set is empty:
       - If any WPs have status == "auto-draft" → surface count +
         source-finding IDs to concierge / founder; exit.
       - If any WPs remain "pending" (deps not met) → blocked on
         dependencies; surface what's blocking; exit.
       - If no WPs remain pending and no auto-drafts → the batch is
         **merged**, but DO NOT claim "shipped / complete / main is
         green" yet — that claim must be grounded in the gate that
         actually blocks (Definition of Done, agents/sulis.md). Run the
         gate check before the completion report:

         ```bash
         PROT=$("$WPX_DIR/wpx-preflight" protection-status \
                  --repo <owner/repo> --branch dev 2>/dev/null)
         # required check present  → branch-CI is a real ship gate
         # protection unavailable  → branch-CI is ADVISORY (the common
         #   founder repo: private + free plan)
         ```

         - **branch-CI is a required check (protection present)** and
           green → honest to report "shipped / all WPs done."
         - **branch-CI is advisory (protection unavailable)** → branch-CI
           green is NOT a ship signal. Report, in founder English:
           *"All {N} pieces are built and merged to main — but automated
           checks are advisory on this repo, so this isn't verified-
           shippable yet. The real gate is the deploy run; I'll confirm
           it's green before calling this done."* Then verify the
           blocking gate (the deploy-to-dev workflow conclusion, read
           explicitly — never a watched exit code) and only claim
           complete once it's green. NEVER report "journey complete /
           main is green / nothing blocked" off advisory CI. (#79;
           wires the #52 unprotected-repo detection into the "done"
           claim. Programmatic deploy-gate polling is the scoped
           follow-on.)

    6. Compute the parallel-eligible subset (cap at max_parallel):

       Greedy selection — iterate ready set in lowest-sequence_id
       order; pick a WP if it satisfies ALL of these vs every WP
       already picked for THIS batch:
           (a) Neither dependsOn the other (transitively).
           (b) Declared file scope (from WP Contract section)
               doesn't overlap.
           (c) They don't share a dependsOn descendant currently
               in the same batch (prevents racing two children
               of the same parent on the same descendant outcome).
           (d) **Migration-lock serialisation (v0.8.1+).** No WP
               with `requires_migration_lock: true` in its
               frontmatter is included unless the batch contains
               EXACTLY that one WP. If the next-ready WP has the
               flag, the batch is just that one WP — dispatch
               solo, wait for completion, then continue. This
               handles WPs that touch shared persistent state
               non-idempotently (schema migrations, database
               seeds, Redis flushes) where parallel execution
               would deadlock, race on row locks, or leave the
               schema in an inconsistent state.

       Stop when batch has max_parallel WPs OR ready set is
       exhausted. Single-WP batch (size 1) is fine — sequential
       fallback when no parallelism is available, or required
       serialisation when a migration-locked WP is up.

    7. Mark each picked WP status: in_progress in INDEX with
       timestamp.

    7.5. **Pin ONE base ref for the whole batch (#106 — MUST).**
       Parallel executors that resolve their own `--base-branch` will
       drift: one ends up off the local `change/*` tip, another off
       `origin/main` after a fetch — the calling session then has to
       reconcile bases by hand before the train. Pick
       the base ref **once, here**, and pass it verbatim to every
       executor in the wave so all worktrees branch off the same SHA:

       ```bash
       CURRENT_BRANCH=$(git -C <repo-root> branch --show-current)
       if [[ "$CURRENT_BRANCH" == change/* ]]; then
           # Shipping into a change — use the change branch (LOCAL ref,
           # since the change branch may not exist on origin yet).
           BATCH_BASE_BRANCH="$CURRENT_BRANCH"
       else
           # Shipping direct to main (the trunk) — fetch origin/main once
           # so every executor branches off the same fresh tip.
           git -C <repo-root> fetch origin main
           BATCH_BASE_BRANCH="main"
       fi
       BATCH_BASE_SHA=$(git -C <repo-root> rev-parse "$BATCH_BASE_BRANCH")
       ```

       Substitute `<BATCH_BASE_BRANCH>` into every executor brief in
       Step 8 below — every Agent prompt MUST include
       `--base-branch <BATCH_BASE_BRANCH>` on its `wpx-worktree create`
       call. Capture `<BATCH_BASE_SHA>` for the drift gate at Step 12.5
       so any in-batch drift is detected before the train pass.

    8. Dispatch ALL picked WPs in a SINGLE message containing
       multiple Agent tool_use blocks — Claude Code runs them
       concurrently. The Agent `description` is rendered on the
       founder's screen — it MUST be founder-English (the plain
       translation of the WP's title), NEVER a raw WP ID or
       "Ship WP-NNN". See "Founder progress discipline" below.

       **Every executor prompt in this dispatch MUST include
       `--base-branch <BATCH_BASE_BRANCH>` on its `wpx-worktree create`
       call (per Step 7.5 #106).** Don't let executors resolve their
       own base independently — that's the divergence the pin closes.

       Agent({
         subagent_type: "sulis:executor",
         description: "Building the sign-up screen",   # plain-English WP title
         model: <executor_model from WP frontmatter, if present>,
         prompt: """<executor brief per below — the WP-NNN lives HERE,
                     not in the founder-facing description>""",
       })
       Agent({
         subagent_type: "sulis:executor",
         description: "Building the billing screen",
         model: <executor_model from WP frontmatter, if present>,
         prompt: """<executor brief per below>""",
       })
       Agent({
         subagent_type: "sulis:executor",
         description: "Building the device-connection screen",
         model: <executor_model from WP frontmatter, if present>,
         prompt: """<executor brief per below>""",
       })

       Send all three in one message. Claude Code dispatches them
       in parallel; the calling turn blocks until ALL return.

    9. Per-WP executor brief (v0.9.0+; substitute WP-NNN, project,
       etc.):

       You are dispatched by the run-all loop (parallel batch
       of N) to ship WP-NNN through Steps 1-7 of the lifecycle:
       worktree, plan generation (Step 1.5, v0.10.0+), RGB, docs,
       lint, commit, push. Steps 8-12 (CI poll, merge, deploy,
       health, smoke, security review, INDEX flip, acceptance
       evidence, worktree removal) are the calling session's
       responsibility — do NOT do them.

       At Step 1.5 you MUST emit a structured plan to the journal
       via `wpx-journal seed-plan` before starting Step 2 (RED).
       See agents/executor.md "Step 1.5 — Plan generation (MUST)"
       for the approach + item-list shape. The plan is the
       calling session's pre-execution audit surface.

       WP file: .architecture/{project}/work-packages/WP-NNN-<title>.md
       INDEX:   .architecture/{project}/work-packages/INDEX.md
       TDD:     .architecture/{project}/TDD.md
       ADRs:    .architecture/{project}/adrs/

       Continuation Discipline applies (see agents/executor.md):
       do not return control until Step 7 is journal-recorded
       (push succeeded; wpx-journal complete-step --step 7 called
       with the pushed SHA in --outcome) OR a BLOCKER is written
       via wpx-blocker. No polling boundaries inside your
       contract — Steps 1-7 are all synchronous; the calling
       session handles the long async waits at Steps 8-10.

       You are running in your own git worktree (wpx-worktree
       create at Step 1). Parallel peers are running their own
       worktrees. No file-system collision between you.

       Use wpx-* CLI tools for all bookkeeping (journal, blocker)
       per "Bookkeeping via wpx-* tools" in agents/executor.md.
       Direct Markdown edits to .executor-WP-NNN.md or BLOCKER-*.md
       are FORBIDDEN. Issue every wpx-journal call as a single,
       output-visible Bash invocation — never chained into a
       multi-line block, never output-suppressed — so you confirm
       each one actually ran before moving on (a silently-skipped
       call leaves the journal incomplete, which this loop trusts).

       If the journal at .architecture/{project}/work-packages/
       .executor-WP-NNN.md exists with an incomplete tail (read
       via wpx-journal read --field step-trace), resume from the
       last started-but-not-completed step.

       Output: journal updated through Step 7 with Completed
       timestamp; pushed branch + SHA in the Step 7 trace row.

       Or: BLOCKER-WP-NNN.md written via wpx-blocker.

       Return when Step 7 is journal-recorded OR a BLOCKER is
       written. Do NOT do Steps 8-12.

   10. Wait for ALL parallel Agent calls to return. Claude Code's
       Agent tool blocks the calling turn until every parallel
       call resolves.

   11. For each returned executor, classify the outcome by reading
       the journal at .architecture/{project}/work-packages/
       .executor-WP-NNN.md. Use the MCP tool
       `mcp__sulis-execution-mcp__journal_read` with
       `wp: WP-NNN, project: <slug>, field: step-7-status`.

       (Fallback if the MCP server isn't loaded:
       `wpx-journal read --wp WP-NNN --project <slug> --field step-7-status`.)

       Three branches:

       (a) **Step 7 complete** (status: complete; outcome row
           records branch + pushed SHA) — proceed with Steps 8-12
           via the calling-session pipeline below.

       (b) **BLOCKER written** (BLOCKER-WP-NNN.md exists at
           .architecture/{project}/work-packages/) — surface its
           plain-English summary; flip INDEX to blocked via MCP tool
           `mcp__sulis-execution-mcp__index_flip_status` with
           `wp: WP-NNN, project: <slug>, to: blocked, expected: in_progress`.

           Then propagate dependency_blocked to descendants via MCP
           tool `mcp__sulis-execution-mcp__index_mark_downstream_blocked`
           with `wp: WP-NNN, project: <slug>`.

           (Fallbacks if MCP unavailable:
           `wpx-index flip-status --wp ... --to blocked --expected in_progress`,
           then `wpx-index propagate-blocked --wp ...` — same wire format.)

           Skip Steps 8-12. Continue to next WP in the loop.

           Note: a Step 1.5 scope-guard BLOCKER (executor identified
           that the WP's Contract references files outside scope, or
           the plan would violate scope) lands here too — surface the
           plain-English summary normally; the upstream fix is for
           SEA to reconcile the WP Contract.

       (c) **Step 7 NOT complete AND no BLOCKER** (executor returned
           prematurely) — classify as "error". Halt the entire loop.
           Optionally check whether the journal has a populated
           `## Plan` section (read via `wpx-journal read --field plan`)
           to determine where the executor parked:

               "WP-NNN: executor returned before Step 7 completed
                and no BLOCKER was written. Plan: <N items, M done>.
                Likely parked at <step inferred from in-progress
                item>. Re-dispatch via /sulis:run-wp WP-NNN
                to resume from journal."

           The plan in the journal makes the parked-state diagnosis
           specific. v0.10.0+ executors that have completed Step 1.5
           leave a readable item list showing exactly which item was
           in-progress when the session ended.

   12. **For each Step-7-complete WP, flip INDEX status; the train ships them as a batch.**

       In v0.11.0+, individual WPs do NOT invoke wpx-pipeline directly
       at the end of run-all's executor batch. Instead:

       - Flip the WP's INDEX status to `step-7-complete` (the executor
         contract emits this via the journal).
       - After all WPs in this run-all parallel batch are flipped,
         invoke `wpx-train run` ONCE for the project. The train picks
         up all `step-7-complete` WPs (whose dependencies are merged
         and whose branches are CI-green) and batches them into one
         rebase / merge / deploy / health / smoke pass.

       Per CW-04, when run-all is invoked from inside a change worktree,
       detect the change branch first and pass it as `--base-branch`:

       ```bash
       CURRENT_BRANCH=$(git -C <repo-root> branch --show-current)
       if [[ "$CURRENT_BRANCH" == change/* ]]; then
           BASE_BRANCH="$CURRENT_BRANCH"
       else
           BASE_BRANCH="main"
       fi

       "$WPX_DIR/wpx-train" run \
         --project <slug> \
         --repo <org/repo> \
         --base-branch "$BASE_BRANCH" \
         --deploy-workflow "<workflow name>" \
         --staging-url "<staging-url>" \
         --smoke-cmd "<smoke command>" \
         --health-path "<health-path>" \
         --enable-gate-handoff \
         # Add --force to bypass size/staleness trigger
       ```

       **v0.23.0 (HD-007): pass `--enable-gate-handoff`** so the train
       stops at the new `verifying_gates` phase after deploy/health/smoke
       complete green, instead of going directly to terminal success.
       The train emits `outcome: awaiting_gates` (exit 0) with a
       `gate_handoff` envelope describing the batch diff range +
       wps_shipped. The calling session (this skill) then dispatches
       Step 10.5 + Step 11 inside that phase and invokes
       `wpx-train mark-gates-complete --train-id <id>` to finalise (see
       Step 14.5 below). The gates are now part of the train's
       transaction in lifecycle terms — the dispatch mechanism stays
       here because a Python CLI can't spawn Agents.

       **Legacy fallback:** if `--enable-gate-handoff` is omitted, the
       train returns `outcome: success` directly (today's pre-v0.23.0
       behaviour) and Steps 13-14 below run as post-train follow-on.
       Both shapes are supported during the deprecation cycle; new
       projects SHOULD pass the flag.

       If the train trigger isn't met (e.g. only 1 WP eligible and no
       force), `wpx-train run` exits cleanly with `outcome:
       not_triggered`. The eligible WPs wait for the next invocation
       (typically the next run-all loop, or a manual
       `wpx-train run --force`).

       For backwards-compatibility / hotfix shipping of a single WP,
       see `/sulis:run-wp WP-X --force-single` which preserves
       the wpx-pipeline per-WP path.

       The remainder of this section (the historical Steps 8-12
       per-WP flow via wpx-pipeline) is preserved below as v0.10.7
       fallback documentation. **Do not invoke this in v0.11.0+ —
       wpx-train is the path.**

   13. **Step 10.5 (per-batch, v0.21.1+): bundled-tip code-review
       for cross-WP composition issues.**

       After `wpx-train run` returns, but BEFORE Step 11, review the
       composition of all WPs in the batch via `/sulis:code-review` against
       the batch's diff range on the base branch. This catches issues
       only visible when WPs compose: N+1 queries across sibling WPs,
       integration regressions, contract drift between interdependent
       WPs.

       **Trigger outcome (v0.23.0, HD-007):**

       - When `--enable-gate-handoff` was passed (recommended), the
         train returns `outcome: awaiting_gates` (exit 0) and the train
         state is in phase=`verifying_gates`. Dispatch Step 10.5 + 11
         INSIDE this phase. The `gate_handoff` envelope on the result
         JSON carries the diff range + wps_shipped — use those instead
         of reading the train state YAML.
       - When `--enable-gate-handoff` was omitted (legacy), dispatch
         ONLY when `outcome: "success"` per pre-v0.23.0 semantics.
       - In either case: if `outcome` is `not_triggered`, `paused`,
         `failed`, or `blocker`, **skip Step 10.5** — the train's own
         recovery flow owns those states.

       Capture the batch diff range from the train state YAML:

           BATCH_START_SHA=$(jq -r '.data.result.bundle[0].pre_train_sha' \
             /tmp/train-result.json)
           BATCH_END_SHA=$(jq -r '.data.result.final_merge_sha' \
             /tmp/train-result.json)

           # Diff range: from "just before the train started" to
           # "after the last squash-merge lands".
           # Equivalent: <BATCH_START_SHA>..<BATCH_END_SHA> on the base branch.

       Invoke `/sulis:code-review` against the range:

           /code-review "${BATCH_START_SHA}..${BATCH_END_SHA}" <project>

       The skill writes its bundle to:
           .architecture/<project>/code-reviews/PR-<range-or-hash>-<TS>/
             REVIEW.md
             signals.json
             tool-outputs/

       Capture the bundle path:

           BUNDLE_DIR=$(ls -td .architecture/<project>/code-reviews/PR-*-*/ \
             | head -1)

       Parse `signals.json`. For each finding (mirroring Step 11's
       loop pattern):

       - **CRITICAL** → write a BLOCKER for the batch; SKIP Step 12
         for the affected WPs; founder responds via remediation WPs
         that ship in the next train:

             "$WPX_DIR/wpx-blocker" write \
               --wp <project>-train-<train_id> --project <project> \
               --title "Step 10.5 CRITICAL composition finding" \
               --step "Step 10.5 (bundled-tip code-review)" \
               --trigger "step-10.5-critical" \
               --observation "<finding summary>" \
               --root-cause "Cross-WP composition issue surfaced by /sulis:code-review against batch diff <range>" \
               --scope in-scope \
               --suggested-next "Founder review; auto-drafted remediation WPs ship in next train cycle"

       - **CONCERN or ADVISORY** → register the finding (signature-hash
         dedup automatic); if not a duplicate, auto-draft a follow-up
         WP and register it in INDEX:

             # 1. Register
             "$WPX_DIR/wpx-findings" register \
               --wp <project>-train-<train_id> --project <project> \
               --severity <CONCERN|ADVISORY> \
               --summary "<one-line>" \
               --file <path> \
               --evidence-json @/tmp/finding-N.json \
               --suggested-fix "<suggested fix>" \
               --primitive <CR-NN code>

             # 2. Auto-draft (only if is_duplicate == false)
             "$WPX_DIR/wpx-findings" auto-draft-wp --project <project> \
               --source-finding <SF-NNN> \
               --source-wp <project>-train-<train_id> \
               --auto-wp-id <WP-AUTO-NNN from register output> \
               --primitive Refactor \
               --severity <CONCERN|ADVISORY>

             # 3. Register in INDEX
             "$WPX_DIR/wpx-index" add-wp \
               --wp WP-AUTO-NNN --project <project> --from-wp-file

       Record the verdict in the journal:

           "$WPX_DIR/wpx-journal" record-step \
             --wp <project>-train-<train_id> --project <project> \
             --step 10.5 \
             --outcome "addressed: <K_total> findings (<K_critical> CRITICAL, <K_concern> CONCERN, <K_advisory> ADVISORY); bundle=<BUNDLE_DIR>"

       Emit a plain-English summary, then proceed to Step 11 (security
       review per-WP — same batch, complementary perspective):

           "Step 10.5 complete for train <train_id>.
            Bundled-tip code-review against <range>.
            <K_total> findings (<K_critical> CRITICAL → BLOCKER;
             <K_new_drafts> CONCERN/ADVISORY → WP-AUTO-* drafted;
             <K_duplicates> duplicates skipped).
            Founder: review the drafted WPs in INDEX; promote to
            `pending` for the next train cycle. The next train's
            Step 10.5 will re-review the new bundled-tip — this is
            the loop-until-clean closure (the distributed loop
            terminates when an iteration produces zero NEW findings)."

       **Honesty about this post-merge variant:** Step 10.5 catches
       cross-WP findings AFTER merges land — it doesn't pre-merge-gate
       them. CRITICAL findings result in BLOCKER + remediation-WP
       cycle, not in a halt of the deploy. The TRUE pre-merge gate
       (cmd_run pause/resume; v0.16.1 deferred design) is still
       future work; this commit ships the visibility + remediation
       loop without that refactor.

   14. **Step 11 (per-batch, v0.20.0+): post-deploy security review
       for every WP shipped by the train.**

       Read the train's JSON envelope (the `/tmp/train-result.json`
       file from the previous step):

           jq -r '.data.result | {outcome, train_id, wps_shipped, deploy_url, final_merge_sha}' \
             /tmp/train-result.json > /tmp/train-summary.json

       Dispatch only when `outcome: "success"`. If `outcome` is
       `not_triggered`, `paused`, `failed`, or `blocker`, **skip Step 11**
       — the train's own recovery flow owns the WPs in those states.

       For each `wp_id` in `result.wps_shipped`, spawn the
       security-reviewer Agent ONCE. Iterate sequentially (subagent
       calls are synchronous and one level deep). Up to 2 attempts per
       WP if the subagent errors out transiently; on third failure
       write a BLOCKER and skip that WP's Step 12.

           # For each wp_id in wps_shipped:
           Agent({
             subagent_type: "sulis:security-reviewer",
             description: "Step 11 post-batch verification for <wp_id>",
             model: <security_model from frontmatter, if present>,
             prompt: """
               Review the squash-merge at <merge_sha> on main
               (deployed to <deploy_url>). Health: <health_status>.
               Smoke: <smoke_verdict>.

               Verify against <wp_id>'s Definition of Done. Categorise
               findings by severity (CRITICAL / CONCERN / ADVISORY).
               Return a structured verdict JSON in the format
               documented at plugins/sulis/agents/
               security-reviewer.md.
             """,
           })

       Parse the returned verdict. For each finding from this WP:

       - **CRITICAL** → write a BLOCKER for the WP; flip status to
         `step-11-blocked`; **skip Step 12 for this WP only**; continue
         with the next WP in `wps_shipped` (do NOT halt the whole
         per-batch loop):

             "$WPX_DIR/wpx-blocker" write \
               --wp <wp_id> --project <slug> \
               --title "Step 11 CRITICAL finding on <wp_id>" \
               --step "Step 11 (post-deploy security review)" \
               --trigger "step-11-critical" \
               --observation "<finding summary>" \
               --root-cause "<root cause from verdict>" \
               --scope in-scope \
               --suggested-next "Founder review; remediate before next train cycle"

             "$WPX_DIR/wpx-index" flip-status \
               --wp <wp_id> --project <slug> \
               --to step-11-blocked --expected done

       - **CONCERN or ADVISORY** → register the finding (signature-hash
         dedup automatic); if not a duplicate, auto-draft a follow-up
         WP and register it in INDEX:

             # 1. Register
             "$WPX_DIR/wpx-findings" register --wp <wp_id> --project <slug> \
               --severity <CONCERN|ADVISORY> \
               --summary "<one-line>" \
               --file <path> \
               --evidence-json @/tmp/finding-N.json \
               --suggested-fix "<suggested fix>" \
               --primitive <SEC-NN>

             # 2. Auto-draft (only if is_duplicate == false in register output)
             "$WPX_DIR/wpx-findings" auto-draft-wp --project <slug> \
               --source-finding <SF-NNN> \
               --source-wp <wp_id> \
               --auto-wp-id <WP-AUTO-NNN from register output> \
               --primitive <Secure|Harden|Instrument|Gate> \
               --severity <CONCERN|ADVISORY>

             # 3. Register in INDEX (status: auto-draft; founder promotes)
             "$WPX_DIR/wpx-index" add-wp \
               --wp WP-AUTO-NNN --project <slug> --from-wp-file

       After ALL findings handled for this WP (and assuming no CRITICAL),
       record the verdict in the journal:

           "$WPX_DIR/wpx-journal" record-postdeploy \
             --wp <wp_id> --project <slug> \
             --verdict <PASS|PASS-WITH-FOLLOW-UPS> \
             --findings-summary "0 CRITICAL, <N> CONCERN, <M> ADVISORY"

       After the loop completes — every WP in `wps_shipped` reviewed —
       emit a plain-English summary:

           "Step 11 complete for train <train_id>.
            <N> WPs reviewed; <K_total> findings registered
            (<K_critical> CRITICAL → BLOCKER + step-11-blocked;
             <K_new> CONCERN/ADVISORY new → <K_new> WP-AUTO-* drafted;
             <K_dup> duplicates skipped).
            Founder: review the auto-drafted WPs in INDEX (status
            `auto-draft`); promote to `pending` for the next train
            cycle. The next train's Step 11 will re-review their
            merge SHAs — this is the loop-until-clean closure (the
            distributed loop terminates when an iteration produces
            zero NEW findings)."

       **Loop-until-clean semantic (the user-required behaviour):**

       Step 11 doesn't tight-loop within one train run (re-spawning
       the reviewer per WP after a fix isn't useful — the merge is
       already on main). Instead, the loop is DISTRIBUTED across trains:

       - This train's Step 11 produces N findings + M auto-drafted WPs
       - Founder promotes WP-AUTO-* to `pending`
       - The next train ships them
       - That train's Step 11 re-reviews their merge SHAs
       - If new findings → more WP-AUTO; if zero new findings → loop
         closes (the codebase is clean from Step 11's perspective)

       `wpx-findings register`'s signature-hash dedup ensures
       previously-registered findings don't generate duplicate
       WP-AUTO drafts (the loop converges, doesn't oscillate).

       For an explicit, retroactive sweep over WPs that shipped
       before v0.20.0 (i.e., slice-1 and slice-2's 12 WPs that
       missed Step 11), invoke `/sulis:backfill-gates`
       (v0.20.2+).

   14.5. **HD-007 gate completion (v0.23.0+, only when `--enable-gate-handoff`
        was passed at Step 12).**

        After Step 10.5 + Step 11 have both completed for every WP in
        the batch, finalise the train by invoking the new
        `mark-gates-complete` subcommand:

            # Clean verdict — no CRITICAL found in Step 10.5 OR Step 11:
            "$WPX_DIR/wpx-train" mark-gates-complete \
              --project <slug> \
              --train-id <train_id from train-result.json> \
              --gate-findings "$BUNDLE_DIR/REVIEW.md"

            # CRITICAL verdict — at least one Step 10.5 or Step 11 CRITICAL
            # finding fired (and the dispatcher above already wrote BLOCKERs +
            # drafted remediation WPs):
            "$WPX_DIR/wpx-train" mark-gates-complete \
              --project <slug> \
              --train-id <train_id> \
              --gate-findings "$BUNDLE_DIR/REVIEW.md" \
              --critical-found

        Behaviour:

        - **Clean** → train transitions to terminal `success`; YAML
          record's `outcome` becomes `success`; state file cleaned up.
          Exits 0.
        - **`--critical-found`** → transitions to terminal `failed`;
          YAML record's `outcome` becomes `gate_blocker`. **No ADR-212
          revert runs** — the gate dispatchers above (Steps 13-14)
          already wrote per-WP BLOCKERs + drafted remediation WPs.
          Production stays live; the founder owns the remediation
          cycle (the next train ships the remediation WPs and that
          train's Step 10.5 + 11 re-evaluate). Exits 1.

        **Skip this step when `--enable-gate-handoff` was NOT passed at
        Step 12** — the train already transitioned to terminal `success`
        on its own, and `mark-gates-complete` will reject the call with
        "expected phase=verifying_gates" since the state file no longer
        exists.

   14.6. **Per-WP Step 12 wrap — batched gate-handoff path (#75).**
        The train ships a *batch* and does NOT run the per-WP Step 12
        wrap (acceptance evidence + INDEX flip + worktree removal) the
        legacy per-WP path runs at Step 12 — the train operates on its
        own clone and never sees the executor worktrees. So after a
        **clean** `mark-gates-complete` (Step 14.5), the shipped WPs are
        merged on `dev` but their worktrees + branches are still present
        and their INDEX cache cells still read `step-7-complete`. Left
        undone, the calling session ends up flipping status, removing
        worktrees, and deleting branches by hand for every WP (the toil
        lesson #75 captured across 6 train runs).

        `mark-gates-complete`'s clean-success envelope carries a
        `pending_step12` checklist — one `{wp, branch}` per shipped WP.
        **For each entry, run the same Step 12 wrap the legacy path uses,
        then delete the merged branch:**

            # one per pending_step12 entry; <worktree> is the executor
            # worktree this run-all session created for the WP at Step 1-7
            "$WPX_DIR/wpx-step12" wrap \
              --wp <wp> --project <slug> \
              --branch <branch> \
              --pipeline-result @<batch deploy/verify result JSON> \
              --worktree-path <worktree> \
              --from-gate-handoff
            git branch -D <branch>   # merged to main; safe to delete

        **Pass `--from-gate-handoff` (#267).** On this path the WPs were
        flipped to `step-7-complete` before the train (not `in_progress`),
        so the wrap's INDEX flip must expect `step-7-complete`. Without the
        flag the wrap fails (`status is 'step-7-complete', expected
        'in_progress'`) and you end up doing its three jobs — flip,
        worktree-remove, branch-delete — by hand for every WP.

        Only the calling run-all session has the per-WP worktree paths,
        so this step lives here, not in `mark-gates-complete`. Skip it on
        a `--critical-found` finalise — those WPs got BLOCKERs, not a
        clean ship.

   14.7. **Worktree cleanup safety — scope to THIS change only (#211/#253/#130 — MUST).**
        Remove ONLY the worktrees this run-all batch created for the
        current change. Each is an explicit path you already hold (the
        `--worktree-path` you passed to `wpx-step12 wrap` / `wpx-worktree
        create`, co-located under the current change's worktree parent
        `~/.sulis/changes/<this-change-id>/`).

        Always remove via the **scope-guarded tool**, passing the owning
        change so the guard can enforce the boundary (#130):

        ✓ `wpx-worktree remove --change-id <this-change-id> --worktree-path <path>`

        The tool now **refuses** any `--worktree-path` outside
        `~/.sulis/changes/<this-change-id>/` — cross-change / out-of-scope
        removal is structurally blocked, not just discouraged. (`--change-id`
        defaults to `SULIS_CHANGE_ID`; pass it explicitly to be safe.)

        **NEVER** use raw git for cleanup — raw `git worktree remove` BYPASSES
        the guard, and `git worktree list | grep …` is the exact move that has
        now twice matched + removed **worktrees belonging to OTHER in-flight
        changes** (#211, then again #130 — WP numbers restart per change, so a
        name/number glob in the shared repo crosses change boundaries and
        discards the only unique key, the change-id in the path):

        ✗ `git worktree remove <path>`  (bypasses the #130 guard)
        ✗ `for w in $(git worktree list | grep wp- | awk …); do git worktree remove "$w"; done`

        If a worktree path you expect is already gone, that's fine
        (idempotent) — never widen the match to "find" it. This composes
        with the #106 base-pin discipline: a batch operates entirely
        within its own change's worktree parent.

       ---

       **(v0.10.7 fallback — preserved for reference)**

       Read frontmatter to determine pipeline arguments:

           wpx-wp read-frontmatter --wp WP-NNN --project <slug> \
             --field '*'

       Capture: branch, smoke_test, deploy_workflow, staging_url,
       ci_poll_interval_seconds, post_deploy_verification,
       security_model, dev-sha-at-creation (from the sidecar at
       .architecture/{project}/work-packages/.executor-WP-NNN-dev-sha).

       **Resolve the branch from the canonical emitter — do NOT
       hand-template it (ADR-001).** In a change this yields the scoped
       `wp/{primitive}-{slug}/wp-NNN-<slug>` shape; outside one, the legacy
       `feat/wp-NNN-<slug>`. The emitter is what makes newly minted branches
       collision-safe (#105/#106). Use `"$BRANCH"` for every `--branch` below.

           BRANCH=$("$WPX_DIR/wpx-wp" branch-name --wp WP-NNN \
             --project <slug> --repo-root <repo-root> | jq -r '.data.branch')

       **Step 8-10: invoke wpx-pipeline via top-level
       Bash(run_in_background:true).** This is the load-bearing
       v0.9.0 change — the wait happens in a deterministic Python
       script, not in an agent's turn. Typical wall time: 15-45 min.

           Bash({
             command: """"$WPX_DIR/wpx-pipeline" run \
                --wp WP-NNN --project <slug> \
                --branch "$BRANCH" \
                --worktree-path ../wp-NNN-worktree \
                --dev-sha-at-creation <sha-from-sidecar> \
                --deploy-workflow "<workflow name from frontmatter>" \
                --staging-url <staging-url> \
                --smoke-cmd "<smoke command from frontmatter>" \
                --repo <org/repo> \
                > /tmp/pipeline-WP-NNN.json 2> /tmp/pipeline-WP-NNN.log""",
             run_in_background: true,
             timeout: 5400000   # 90 min cap
           })

       The harness auto-notifies the calling session when the
       background Bash exits. **No polling, no sleep, no manual
       check.** Read /tmp/pipeline-WP-NNN.json on completion.

       `wpx-pipeline` reads the CI *conclusion* explicitly (`_poll_ci`:
       merge only when `conclusion == success`) — that is why this path
       is safe. If you ever confirm CI by hand instead, read the
       conclusion, never a shell exit code: NEVER trust a chained
       `gh run watch <id>; echo $?` (the echo's exit is always 0) and
       NEVER use `gh run watch` without `--exit-status` — both report a
       false green and have merged a foundation WP on a red (issue #59).
       See `git-workflow-standard.md` GIT-04 *"Confirm CI by reading the
       conclusion, not a shell exit code"*.

       Inspect the JSON. If `outcome: "blocker"`:

           # Write BLOCKER capturing the pipeline failure
           "$WPX_DIR/wpx-blocker" write \
             --wp WP-NNN --project <slug> \
             --title "<pipeline step> failed" \
             --step <8|9|10> \
             --trigger budget-exhausted \
             --observation @/tmp/pipeline-WP-NNN.log \
             --root-cause "<from blocker_reason>" \
             --scope out-of-scope \
             --plain-english "..." \
             --suggested-next "..."

           wpx-index flip-status --wp WP-NNN --project <slug> \
             --to blocked --expected in_progress
           wpx-index propagate-blocked --wp WP-NNN --project <slug>
           # Skip Steps 11-12; continue to next WP

       If `outcome: "success"`, proceed to Step 11.

       **Step 11: spawn the security-reviewer Agent.** Synchronous
       Agent call; ~5-15 min wall time.

           Agent({
             subagent_type: "sulis:security-reviewer",
             description: "Step 11 post-deploy verification for WP-NNN",
             model: <security_model from frontmatter, if present>,
             prompt: """
               Review the squash-merge at <merge_sha> on main
               (deployed to <deploy_url>). Health: <health_status>.
               Smoke: <smoke_verdict>.

               Verify against the WP's Definition of Done. Categorise
               findings by severity (CRITICAL / CONCERN / ADVISORY).
               Return a structured verdict JSON in the format
               documented at plugins/sulis/agents/
               security-reviewer.md.
             """,
           })

       Parse the returned verdict. For each non-CRITICAL finding:

           # Register the finding (signature-hash dedup automatic)
           wpx-findings register --wp WP-NNN --project <slug> \
             --severity <CONCERN|ADVISORY> \
             --summary "<one-line>" \
             --file <path> \
             --evidence-json @/tmp/finding-N.json \
             --suggested-fix "<suggested fix>" \
             --primitive <SEC-NN>

           # If new (not is_duplicate), auto-draft the follow-up WP
           "$WPX_DIR/wpx-findings" auto-draft-wp --project <slug> \
             --source-finding <SF-NNN> \
             --source-wp WP-NNN \
             --auto-wp-id <WP-AUTO-NNN from register output> \
             --primitive <Secure|Harden|Instrument|Gate> \
             --severity <CONCERN|ADVISORY>

           # (v0.10.3+) Register the new auto-draft WP in INDEX so
           # downstream dispatch + wpx-step12 wrap can see it. The
           # tool reads the WP file's frontmatter (id, title,
           # primitive, dependsOn, blocks, status) and appends a row.
           # Status remains `auto-draft` — the founder promotes to
           # `pending` via the concierge's slice-end review.
           "$WPX_DIR/wpx-index" add-wp \
             --wp WP-AUTO-NNN --project <slug> --from-wp-file

       If CRITICAL findings exist, write a BLOCKER and stop (do NOT
       proceed to Step 12). Otherwise record the post-deploy verdict
       in the executor's journal:

           wpx-journal record-postdeploy --wp WP-NNN --project <slug> \
             --verdict PASS \
             --findings-summary "0 CRITICAL, N CONCERN, M ADVISORY"

       **Step 12: atomic wrap.** Composes acceptance evidence + INDEX
       flip + worktree remove into one transactional call.

           # Build pipeline-result file
           jq '.' /tmp/pipeline-WP-NNN.json > /tmp/pipeline-result-WP-NNN.json

           "$WPX_DIR/wpx-step12" wrap \
             --wp WP-NNN --project <slug> \
             --branch "$BRANCH" \
             --pipeline-result @/tmp/pipeline-result-WP-NNN.json \
             --worktree-path ../wp-NNN-worktree

       Emit plain-English status:

           "WP-NNN done — deployed and healthy at <deploy_url>.
            Security: PASS (N CONCERN, M ADVISORY auto-drafted as
            WP-AUTO-XXX for founder review)."

       **Step 12a: seam-close gate (fires inside wpx-step12 wrap).**
       The wrap above runs the seam-close gate at the WP-done flip. You
       do not call it — it is internal to wrap. When a **seam-spanning
       WP completes** (an integration / composite WP, or the last WP of
       a contract fan-out reaching done), the gate drives the closing
       seam's covering Scenarios and reads observed-or-blocked over the
       real saved record. On a `blocked` seam the wrap envelope carries
       a `gate_block` field — surface that founder-English message
       verbatim and treat the seam as not-done (do NOT roll back the
       flip; the WP is done, the seam is not). See the
       **"Seam-close gate"** subsection below for the full discipline.

   13. Emit per-batch plain-English status to the founder /
       concierge / calling session:
       - "Starting N in parallel: WP-A (title), WP-B (title), ..."
       - As each completes (in the order they return):
         "WP-A done — deployed and healthy at <url>. N-1 still in
          flight."
       - When the batch returns:
         "Batch complete. M done, K blocked. Starting next batch:
          WP-X, WP-Y, ..."

   14. Goto step 1.
```

### Seam-close gate — fires when a seam-spanning WP completes

The seam-close gate runs **inside `wpx-step12 wrap`** at each WP's
done-transition (step 12.2a, right after the `in_progress → done`
flip). Because run-all finalises every WP — single or batched —
through `wpx-step12 wrap`, the gate fires on this path automatically.
You do not invoke it; you surface its result.

**When it fires.** Once per WP, at the WP-done transition. The gate
first asks *did a seam just close?* The case that matters for run-all
is a **seam-spanning WP completing**: an integration / `kind:
composite` WP reaching done, or the last producer/consumer WP of a
contract fan-out reaching done so that the contract WP and all the WPs
that depend on it are now done. When a WP is part of no seam — the
common single-kind case — the gate is silent.

**What it does.** For the closing seam it drives the covering
Scenarios (the end-to-end checks that exercise the real data crossing
the seam) through the acceptance runner and reads the verdict over the
**real saved record**: **observed** or **blocked**. Same
observed-or-blocked rule the ship-stage check uses, re-timed to the
moment the seam closes — when the two slices are freshly adjacent and
cheap to unwind — instead of waiting for ship.

**What `blocked` means.** Seam-close halts as "not done". The done
flip is **not** rolled back: the WP genuinely reached done; it is the
*seam* that is not done. `wpx-step12 wrap` emits a `gate_block` field
in its JSON envelope. Surface that message to the founder **verbatim**
— do not invent your own. It is written in founder English and names
the seam by its title and what wasn't driven, for example:

```
The "checkout-to-ledger" handover isn't done yet. Nothing has driven a
real order all the way through to a saved ledger entry, so we can't
confirm the two halves actually work together. Holding this as not-done
until that end-to-end path runs for real.
```

In a batch, a blocked seam means that seam is held as not-done; the
other WPs in the batch are unaffected, and the calling session reports
it alongside the per-batch status (step 13).

**The escape — `--allow-deferred`.** A seam whose only honest check
needs a capability that isn't live yet can proceed as a **conscious,
recorded deferral** by threading `--allow-deferred` through the wrap.
The deferral is logged. The default is observed-or-blocked: the escape
is a deliberate, recorded choice, never the silent path.

> Cross-refs: the seam-close timing rule is **CF-12** in
> `CONTRACT_FIRST_STANDARD.md`; the ship-stage acceptance check (gate
> 4.8) stays as a backstop per **ADR-002** (defence in depth — the
> seam-close gate is the primary, earlier catch). The gate logic lives
> in `_seam_close_gate`, wired at `wpx-step12 wrap` per ADR-003; this
> skill only surfaces the wrap envelope's `gate_block`.

### v0.9.0 sequencing — sequential post-push, parallel pre-push

Steps 1-7 (the executor's contract) run in parallel: N executors
dispatched at once via N Agent tool_use blocks in a single message.
The harness runs them concurrently and the calling turn blocks until
all N return.

Steps 8-12 (the calling session's pipeline) run **sequentially per
WP** in v0.9.0 — the calling session invokes `wpx-pipeline` for the
first Step-7-complete WP, waits for the harness notification, then
proceeds. This preserves merge ordering on `dev` (avoids racing two
WPs trying to squash-merge concurrently) and keeps the calling
session's reasoning simple.

A future v0.9.1 may add concurrent `wpx-pipeline` invocations per WP
(N parallel `Bash(run_in_background:true)` calls; harness aggregates
notifications) when many WPs are in late stages simultaneously. For
v0.9.0, the sequential pattern is enough — most projects have
sub-five-WP batches and `wpx-pipeline` typically completes in 20-30
min, so the wall-clock benefit of concurrent pipelines is modest.

## Concurrency limit configuration

Default: `max_parallel: 3`. Configurable per-project via the INDEX
header. To change:

```yaml
## Orchestrator Config
max_parallel: 5   # If staging cluster + machine can handle more.
```

Three is a safe starting point covering most graph-parallelisable
cases without overwhelming staging. The founder can dial up as
confidence grows.

## Per-WP model override (opt-in)

Optional WP frontmatter field:

```yaml
executor_model: opus | sonnet | haiku
```

When present, the run-all skill includes the `model` parameter in
that WP's Agent call:

```
Agent({
  subagent_type: "sulis:executor",
  model: "haiku",
  ...
})
```

When absent (default behaviour), no `model` parameter is sent and
the executor inherits the calling session's model (typically Opus).
**No automatic model substitution.** The override is purely opt-in;
defaults are unchanged from v0.7.1.

## Per-executor isolation

Each parallel executor uses its own `git worktree` per GIT-07. Worktree
paths use the WP ID: `../wp-NNN-worktree/`. A relative `--worktree-path`
anchors to the executor's `--repo-root` (the **target change's**
worktree), NOT the calling session's cwd (#309) — so each executor must
pass `--repo-root <target-change-worktree>`, or the worktree lands under
the wrong change's parent when the calling session is bound to a
different change. Concurrent worktrees do not share working files; they
share only the bare repository's git objects + refs (which git handles
thread-safely).

Per-executor journals live at `.architecture/{project}/work-packages/
.executor-WP-NNN.md` — one per WP, no cross-WP collisions.

## Failure isolation

One executor's BLOCKER doesn't affect concurrent peers. Each executor
runs its own OODA spiral (per executor-loop-standard.md EL-01..08)
independently. When the parallel batch returns, the calling session
sees a mix of outcomes (some done, some blocked) and updates INDEX
accordingly.

The next loop iteration uses the updated INDEX to compute the new
ready set. Transitively-dependent descendants of blocked WPs get
`dependency_blocked`; the loop continues with what's still ready.

## When NOT to use

- **One specific WP.** Use `/sulis:run-wp WP-NNN` — single-
  WP dispatch (also runs Agent in the calling session; no parallel
  logic needed).
- **Retry a blocked WP.** Use `/sulis:retry WP-NNN` after
  the external blocker is resolved.

## Gotchas

- The skill expects a non-empty
  `.architecture/{project}/work-packages/INDEX.md`. If empty,
  surface: *"INDEX is empty. Run `/sulis:plan-work` first."*
- `max_parallel: 1` in INDEX header is a valid configuration —
  forces sequential dispatch. Useful when staging capacity is
  constrained or the founder wants one-at-a-time observability.
- An executor's Agent call that returns mid-lifecycle (no Step 7
  success AND no BLOCKER written via wpx-blocker) is classified as
  `error` and halts the entire loop. This is intentional — silent
  advance past a half-finished WP is the failure mode v0.6.1 +
  v0.7.1 + v0.9.0 each tightened.
- WPs with declared file scope that's *very* broad (e.g. "everywhere
  under src/") will conflict with every other WP and effectively
  serialise. SEA's decompose should produce narrower file scopes;
  if your WPs systematically over-claim scope, that's a SEA
  configuration concern, not a run-all issue.
- The depth chain via concierge (v0.9.0+): concierge (depth 0) →
  run-all skill (inline in concierge) → executor at depth 1 (Steps
  1-7) → calling session resumes → security-reviewer at depth 1
  (Step 11). All Agent calls one level deep from the concierge.
  Same shape one level shallower from a top-level user session.

## Stamp the workflow stage (when the run reaches implementation)

When the loop has started shipping WPs and you're inside a change (the
`SULIS_CHANGE_ID` env var is set — every change-bound session has it), record
that the change has reached the **implement** stage so `/sulis:dashboard`
reflects it. Resolve the tool path, then stamp:

```bash
# Resolve from the ACTIVE plugin version (its bin/ is on PATH) — avoids the
# lexical-sort cache pick that mis-ranks 0.98.0 above 0.126.0 (#49).
SCRIPTS_DIR=""
_sulis_bin=$(printf '%s\n' "$PATH" | tr ':' '\n' | grep -E 'sulis-ai-agents/sulis/[^/]+/bin$' | head -1)
[ -n "$_sulis_bin" ] && [ -d "$(dirname "$_sulis_bin")/scripts" ] \
  && SCRIPTS_DIR="$(dirname "$_sulis_bin")/scripts"
[ -z "$SCRIPTS_DIR" ] && [ -f "plugins/sulis/scripts/sulis-change" ] \
  && SCRIPTS_DIR="$(pwd)/plugins/sulis/scripts"
# Last-resort: PORTABLE numeric (NOT lexical, NOT `sort -V`) cache pick.
[ -z "$SCRIPTS_DIR" ] && SCRIPTS_DIR=$(find ~/.claude/plugins/cache -name sulis-change -type f \
  -path '*/sulis/*/scripts/*' 2>/dev/null \
  | sed -E 's#(.*/sulis/)([^/]+)(/scripts/.*)#\2 &#' \
  | sort -t. -k1,1n -k2,2n -k3,3n | tail -1 | cut -d' ' -f2- | xargs -I{} dirname {} 2>/dev/null)
[ -n "$SCRIPTS_DIR" ] && [ -n "$SULIS_CHANGE_ID" ] \
  && "$SCRIPTS_DIR/sulis-change" stage implement
```

Branch-independent, best-effort; it never blocks the run. If
`SULIS_CHANGE_ID` is unset (a run outside a change), skip it. Don't narrate
this to the founder; the dashboard simply stays current (FE-09).

## See also

- `agents/executor.md` — what the loop spawns per WP.
- `../../scripts/sulis-change` — `stage` stamps the workflow position read by
  `/sulis:dashboard`.
- `agents/orchestrator.md` — architectural-intent reference for the
  dispatch logic (not actively invoked).
- `references/lifecycle.md` — the 12-step contract per WP.
- `/sulis:run-wp WP-NNN` — single-WP dispatch.
- `/sulis:status` — read-only INDEX summary.
- `/sulis:retry WP-NNN` — re-run a blocked WP.
