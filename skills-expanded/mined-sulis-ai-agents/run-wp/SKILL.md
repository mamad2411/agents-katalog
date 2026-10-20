---
name: run-wp
description: "Builds and ships a single task."
---

# /sulis:run-wp

This skill **dispatches the executor agent** for one Work Package's
Steps 1-7. What happens after Step 7 depends on the flag:

- **Default (train path):** flip INDEX status to `step-7-complete` and
  report back. The next `wpx-train run` invocation picks it up (along
  with any other `step-7-complete` WPs) and batches them through Steps
  8-11.
- **`--force-single` (hotfix path):** invoke `wpx-pipeline run` for
  Steps 8-12 immediately, the same way runs worked pre-v0.11.0. Use
  when you need to ship a single WP urgently without waiting for the
  train trigger (size ≥3 or 4h staleness).

## How to invoke

When this skill is loaded, you (the calling session) drive the
single-WP lifecycle. Step 1-7 work happens via an `Agent` tool call
to the executor; Steps 8-12 happen inline in the calling session via
the wpx-* tools (per v0.9.0).

### Resolving wpx-* tool paths (MUST — first action, v0.10.1+)

Before reading the WP file or dispatching the executor, resolve the
wpx-* tool directory ONCE and capture it as `$WPX_DIR`:

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

Capture the printed `WPX_DIR` and substitute it inline at every
wpx-* invocation below (e.g., `"$WPX_DIR/wpx-journal" read ...`).
Environment variables do NOT persist between Bash tool calls; the
substitution lives in the prompt text you send to Bash. The
executor subagent you dispatch has the same resolution preamble in
`agents/executor.md` and resolves independently.

### Step 0 — Detect change context (CW-04, v0.12.0+)

Before dispatching the executor, check whether this skill is running
inside a change worktree:

```bash
CURRENT_BRANCH=$(git -C <repo-root> branch --show-current)
if [[ "$CURRENT_BRANCH" == change/* ]]; then
    BASE_BRANCH="$CURRENT_BRANCH"
else
    BASE_BRANCH="main"
fi
```

`BASE_BRANCH` is the ref the WP's feature branch will rebase against
and merge into. In v0.11.0+ this is `dev` directly; in a change-bounded
workflow (v0.12.0+) it's the change branch. Pass it as `--base-branch
$BASE_BRANCH` to wpx-pipeline (Step 2b) and wpx-train (when run-all
fires the train). The dev-SHA-at-creation sidecar uses
`origin/$BASE_BRANCH`'s SHA (the trunk, `origin/main`).

The executor itself does not need to know about the change context —
it just works in its WP worktree, branched off whatever the calling
session tells it.

### Step 0a — Dispatch the executor (Steps 1-7)

Given the user invokes `/sulis:run-wp WP-NNN`:

1. Parse the WP-NNN argument from the user's invocation.
2. Verify the WP file exists at the expected path; if not, surface a
   clear error and exit.
3. Read the WP frontmatter. If it has an `executor_model` field
   (optional; one of `haiku | sonnet | opus`), include the `model`
   parameter in the Agent call. Otherwise omit `model` (the executor
   inherits the calling session's model — typically Opus).
4. **Flip INDEX status `pending → in_progress` BEFORE invoking the
   Agent (#142).** The run-all loop relies on the executor to do this
   at Step 1; the single-WP path historically didn't, so the eventual
   Step 12.2 (`wpx-step12 wrap` → `flip-status --expected in_progress`)
   failed at ship-time on a still-`pending` WP. Doing it here makes the
   single-WP path symmetric with run-all:

   ```bash
   "$WPX_DIR/wpx-index" flip-status \
     --wp WP-NNN --project <slug> --repo-root <repo> \
     --to in_progress --expected pending
   ```

   The flip is **idempotent** (#142): a WP already at `in_progress` (or
   `done` on a replay) returns success without rewriting the row. Run
   it unconditionally — no pre-check needed.

```
Agent({
  subagent_type: "sulis:executor",
  description: "Ship WP-NNN Steps 1-7",
  model: <executor_model from WP frontmatter, if present>,
  prompt: """
You are dispatched to ship WP-NNN through Steps 1-7 of the lifecycle:
worktree, plan generation (Step 1.5, v0.10.0+), RED, GREEN, BLUE,
docs, lint, commit, push. Read your agent prompt (agents/executor.md)
for the full contract.

At Step 1.5 you MUST emit a structured plan to the journal via
`wpx-journal seed-plan` before starting Step 2 (RED). The plan is
the pre-execution audit surface — this skill (the calling session)
will read it on your return to determine where you parked if you
didn't reach Step 7.

Steps 8-12 (CI poll, squash-merge, deploy, health, smoke, security
review, INDEX flip, acceptance evidence, worktree removal) are the
calling session's responsibility per v0.9.0 — do NOT do them.

WP file: .architecture/{project}/work-packages/WP-NNN-<title>.md
INDEX:   .architecture/{project}/work-packages/INDEX.md
TDD:     .architecture/{project}/TDD.md
ADRs:    .architecture/{project}/adrs/

Use wpx-* CLI tools for all bookkeeping (journal, blocker) per
"Bookkeeping via wpx-* tools" in agents/executor.md. Direct Markdown
edits to journal or BLOCKER files are FORBIDDEN.

Continuation Discipline applies: do not return control until Step 7
is journal-recorded (push succeeded; wpx-journal complete-step
--step 7 called with the pushed SHA in --outcome) OR a BLOCKER is
written via wpx-blocker.

If the journal at .architecture/{project}/work-packages/
.executor-WP-NNN.md exists with an incomplete tail, resume from the
last started-but-not-completed step (read via wpx-journal read
--field step-trace). Do not start over.

Return when Step 7 is journal-recorded OR a BLOCKER is written. Do
NOT do Steps 8-12.
""",
})
```

Replace `{project}` and `<title>` based on the actual project path
and WP title. The `subagent_type` value is **exactly**
`executor`.

### Step 1 — Classify the executor's outcome

When the executor returns, read its journal to determine the
outcome using the MCP tool `mcp__sulis-execution-mcp__journal_read`
with `wp: WP-NNN, project: <slug>, field: step-7-status`.

> Fallback (no MCP):
> `wpx-journal read --wp WP-NNN --project <slug> --field step-7-status`

Three branches:

**(a) Step 7 complete** — proceed to Step 2 (run the pipeline).

**(b) BLOCKER written** (BLOCKER-WP-NNN.md exists at
`.architecture/{project}/work-packages/`) — surface its plain-English
summary; flip INDEX to blocked via MCP tool
`mcp__sulis-execution-mcp__index_flip_status` with
`wp: WP-NNN, project: <slug>, to: blocked, expected: in_progress`; exit.

> Fallback (no MCP):
> ```bash
> wpx-index flip-status --wp WP-NNN --project <slug> \
>   --to blocked --expected in_progress
> ```

**(c) Step 7 NOT complete AND no BLOCKER** — classify as "error".
Optionally read the journal's plan to determine where the executor
parked (`wpx-journal read --field plan` returns the item statuses).
Surface:

```
WP-NNN: executor returned before Step 7 completed and no BLOCKER
was written. Plan: <N items, M done>. Likely parked at
<step inferred from in-progress item>. Re-invoke this skill to
resume from journal.
```

Do NOT proceed to Step 2 (the v0.9.0 Steps 8-12 pipeline).

### Step 2 — Queue for the next train (default path, v0.11.0+)

**Skip this step and jump to Step 2b if the caller passed `--force-single`.**

After the executor returns success and the WP file is on disk with the
feature branch pushed, **flip the INDEX status to `step-7-complete`**
and report back. The next `wpx-train run` invocation (typically fired
by `/sulis:run-all` at the end of its parallel batch) picks
this WP up along with any other ready WPs.

Use the MCP tool `mcp__sulis-execution-mcp__index_flip_status` with
`wp: WP-NNN, project: <slug>, to: step-7-complete, expected: in_progress`.

> Fallback (no MCP):
> ```bash
> "$WPX_DIR/wpx-index" flip-status \
>   --wp WP-NNN \
>   --project <slug> \
>   --to step-7-complete \
>   --expected in_progress
> ```

Then report to the calling session in plain English:

> WP-NNN queued for the next train. Train fires when 3 WPs are ready
> or after 4 hours staleness. Run `/sulis:status` to see
> the queue.

Do NOT proceed to Step 2b (wpx-pipeline). Steps 8-11 (CI, merge,
deploy, health, smoke, security review) happen per-train, not
per-WP, in v0.11.0+.

### Step 2b — Run wpx-pipeline directly (`--force-single` path)

Only invoke this step when the caller passed `--force-single` (hotfix
or solo-ship). Otherwise Step 2 above is the path.

Read frontmatter for pipeline arguments:

```bash
wpx-wp read-frontmatter --wp WP-NNN --project <slug> --field '*'
```

**Resolve the branch name from the canonical emitter — do NOT hand-template
it (ADR-001).** In a change this yields the scoped `wp/{primitive}-{slug}/
wp-NNN-<slug>` shape; outside one, the legacy `feat/wp-NNN-<slug>`. Using the
emitter is what makes newly minted branches collision-safe (#105/#106):

```bash
BRANCH=$("$WPX_DIR/wpx-wp" branch-name --wp WP-NNN --project <slug> \
  --repo-root <repo-root> | jq -r '.data.branch')
```

Use `"$BRANCH"` for every subsequent `--branch` below.

Capture: branch, smoke_test, deploy_workflow, staging_url,
post_deploy_verification, security_model. Read the dev-SHA-at-creation
from the sidecar at `.architecture/{project}/work-packages/
.executor-WP-NNN-dev-sha`.

**Invoke wpx-pipeline via top-level `Bash(run_in_background:true)`.**
This is the canonical v0.9.0 long-wait mechanism — the harness
auto-notifies the calling session when the background Bash exits.
Typical wall time: 15-45 min.

```
Bash({
  command: """"$WPX_DIR/wpx-pipeline" run \
     --wp WP-NNN --project <slug> \
     --branch "$BRANCH" \
     --worktree-path ../wp-NNN-worktree \
     --dev-sha-at-creation <sha> \
     --base-branch <BASE_BRANCH> \
     --deploy-workflow "<workflow name>" \
     --staging-url <staging-url> \
     --smoke-cmd "<smoke command>" \
     --repo <org/repo> \
     > /tmp/pipeline-WP-NNN.json 2> /tmp/pipeline-WP-NNN.log""",
  run_in_background: true,
  timeout: 5400000   # 90 min cap
})
```

On notification, read `/tmp/pipeline-WP-NNN.json`.

If `outcome: "blocker"`: write a BLOCKER via `wpx-blocker write`
capturing the pipeline failure, flip INDEX to blocked, exit. Surface
the plain-English summary.

If `outcome: "success"`: proceed to Step 3.

### Step 3 — Security review (Step 11)

Spawn the `sulis-security:security-reviewer` agent synchronously
(blocks the calling turn until the review completes; typically
5-15 min).

```
Agent({
  subagent_type: "sulis:security-reviewer",
  description: "Step 11 post-deploy verification for WP-NNN",
  model: <security_model from frontmatter, if present>,
  prompt: """
    Review the squash-merge at <merge_sha> on main (deployed to
    <deploy_url>). Health: <health_status>. Smoke: <smoke_verdict>.

    Verify against WP-NNN's Definition of Done. Categorise findings
    by severity (CRITICAL / CONCERN / ADVISORY). Return a structured
    verdict JSON per plugins/sulis/agents/security-reviewer.md.
  """,
})
```

For each non-CRITICAL finding:

```bash
# Register (signature-hash dedup handled automatically)
wpx-findings register --wp WP-NNN --project <slug> \
  --severity <CONCERN|ADVISORY> \
  --summary "<one-line>" \
  --file <path> \
  --evidence-json @/tmp/finding-N.json \
  --suggested-fix "<suggested fix>" \
  --primitive <SEC-NN>

# If not is_duplicate, auto-draft the follow-up WP
"$WPX_DIR/wpx-findings" auto-draft-wp --project <slug> \
  --source-finding <SF-NNN> \
  --source-wp WP-NNN \
  --auto-wp-id <WP-AUTO-NNN> \
  --primitive <Secure|Harden|Instrument|Gate> \
  --severity <CONCERN|ADVISORY>

# (v0.10.3+) Register the new auto-draft WP in INDEX so downstream
# dispatch + wpx-step12 wrap can see it. The tool reads the WP file's
# frontmatter (id, title, primitive, dependsOn, blocks, status) and
# appends a row. Status remains `auto-draft` until the founder
# promotes it via the concierge's slice-end review.
"$WPX_DIR/wpx-index" add-wp \
  --wp <WP-AUTO-NNN> --project <slug> --from-wp-file
```

If CRITICAL findings exist: write a BLOCKER and stop. Do NOT proceed
to Step 4.

Otherwise record the verdict:

```bash
wpx-journal record-postdeploy --wp WP-NNN --project <slug> \
  --verdict PASS \
  --findings-summary "0 CRITICAL, N CONCERN, M ADVISORY"
```

### Step 4 — Atomic wrap (Step 12)

```bash
jq '.' /tmp/pipeline-WP-NNN.json > /tmp/pipeline-result-WP-NNN.json

"$WPX_DIR/wpx-step12" wrap \
  --wp WP-NNN --project <slug> \
  --branch "$BRANCH" \
  --pipeline-result @/tmp/pipeline-result-WP-NNN.json \
  --worktree-path ../wp-NNN-worktree
```

Emit plain-English status:

```
WP-NNN done — deployed and healthy at <deploy_url>.
Security: PASS (N CONCERN, M ADVISORY auto-drafted as WP-AUTO-XXX for
founder review).
```

#### The seam-close gate (at the WP-done transition)

`wpx-step12 wrap` runs the **seam-close gate** at the moment this WP
becomes done — step 12.2a, immediately after the `in_progress → done`
status flip. You do not call the gate yourself; it fires inside the
wrap above. This subsection tells you what it does and how to surface
its result.

**When it fires.** At the WP-done transition (the `wpx-step12 wrap`
done-transition), once per WP. For a single-WP run that is right here
at Step 4. The gate first asks: *did a seam just close?* A seam closes
when the contract WP and all the producer + consumer WPs that depend on
it have reached done (or when an integration WP completes). If this WP
is part of no seam — the common case — the gate is silent and the wrap
proceeds untouched.

**What it does when a seam closes.** It drives the closing seam's
covering Scenarios — the end-to-end checks that exercise the real data
crossing the seam — through the acceptance runner, and reads the
verdict over the **real saved record**: **observed** or **blocked**.
This is the same observed-or-blocked discipline the ship-stage check
uses, re-timed to the moment the seam closes (cheap to fix) rather than
deferred to ship.

**What `blocked` means.** Seam-close halts as "not done". The done flip
is **not** rolled back — this WP genuinely reached done; it is the
*seam* that is not done. `wpx-step12 wrap` emits a `gate_block` field in
its JSON envelope. Surface that field's message to the founder verbatim
— **do not invent your own**. The block is written in founder English
and names the seam by its title and what wasn't driven, for example:

```
The "checkout-to-ledger" handover isn't done yet. Nothing has driven a
real order all the way through to a saved ledger entry, so we can't
confirm the two halves actually work together. Holding this as not-done
until that end-to-end path runs for real.
```

**The escape — `--allow-deferred`.** A seam whose only honest check
needs a capability that isn't live yet (e.g. a real browser-driven
step) can proceed as a **conscious, recorded deferral** by threading
`--allow-deferred` through the wrap. The deferral is logged. The default
is observed-or-blocked: the escape is a deliberate choice, never the
silent path.

> Cross-refs: the seam-close timing rule is **CF-12** in
> `CONTRACT_FIRST_STANDARD.md`; the ship-stage acceptance check (gate
> 4.8) remains as a backstop per **ADR-002** (defence in depth — the
> seam-close gate is the primary, earlier catch). The gate logic lives
> in `_seam_close_gate` and is wired at `wpx-step12 wrap` per ADR-003;
> this skill only surfaces the wrap envelope's `gate_block`.

## What you do NOT do in this skill's session

- **Do not write tests, code, lint, commit, or push.** Those are the
  executor's job (Steps 1-7).
- **Do not edit `.executor-WP-NNN.md`, `INDEX.md`, `BLOCKER-*.md`,
  `findings-register.md`, or `SF-NNN-*.md` directly.** All updates go
  through `wpx-*` tools.
- **Do not poll CI / deploy / health manually.** That's `wpx-pipeline`'s
  job, invoked once via `Bash(run_in_background:true)`.
- **Do not summarise the executor's output for the user.** When the
  executor's Agent tool call returns, surface its terminal status
  line directly. The concierge (if upstream) does the founder
  translation; this skill is power-user-facing.

## When to use this skill

- **Single-WP execution** — when you want to ship one specific WP
  rather than walking the whole INDEX. The orchestrator's
  `/sulis:run-all` is the normal multi-WP path; this is
  the single-shot.
- **Re-running a blocked WP** after fixing an external blocker. The
  semantically-clearer alternative is `/sulis:retry WP-NNN`,
  which archives the prior BLOCKER and dispatches a fresh executor.

## Gotchas

- If the WP's `primitive` is outside the v0.5 scope (the file
  doesn't yet define the scaffold), the executor escalates
  immediately with a primitive-coverage BLOCKER. The skill itself
  doesn't pre-check this — the executor's primitive-selection check
  at step 3 handles it.
- If the project's git remote isn't reachable, the executor will
  fail at Step 7 (push). That's a connectivity issue surfaced by
  the executor; not the skill's problem.
- If a prior executor session left an in-flight WP (journal shows
  steps complete up to step N, but no Step 7 success and no
  BLOCKER), invoking this skill resumes from step N+1. Do not
  manually delete the journal to "start fresh" — the journal is the
  audit trail.
- The `wpx-pipeline` background Bash invocation has a 90-min
  timeout. If your project's CI + deploy + smoke truly exceed
  90 min, increase the `timeout` parameter on the `Bash()` call.

## See also

- `agents/executor.md` — the Steps 1-7 contract this skill spawns.
- `references/lifecycle.md` — the 12-step contract; Steps 8-12 are
  the calling session's responsibility per v0.9.0.
- `references/self-heal-budget.md` — per-failure-type budgets
  (executor side).
- `/sulis:run-all` — multi-WP orchestrator path with
  parallel dispatch.
- `/sulis:status` — read-only INDEX summary.
- `/sulis:retry` — re-run a blocked WP with archive.
