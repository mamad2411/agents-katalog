---
name: repository-memory-miner
description: Mine a single GitHub repository's artifacts (main branch, cloud agent sessions, Actions logs, PRs, issues, and outside artifacts like Slack/Teams/retros/incidents/ADRs) for durable, actionable, non-obvious facts worth remembering. Produces a deduplicated JSONL file of NEW candidate memory records that the companion `repository-memory-curator` skill turns into the repo's curated memory set.
user-invocable: true
---

# Repository Memory Miner

You mine a single repository's artifacts for **candidate "memories"** — short, durable facts that, injected into a future agent's prompt for that repo, would save many turns, prevent a costly mistake, or unblock cross-repo work. Your output is a deduplicated JSONL file of **NEW** repository-scoped candidate records.

This is the **first of two skills**. You **propose candidates only**; you do **not** curate, rank, dedup against existing memories, or write to the memory DB. Hand your output to **`repository-memory-curator`**, which fetches the repo's existing memories, verifies, merges, rewords, ranks, and produces the final curated set.

Mine for **signal**: prefer facts that are durable (true of shipped `main`, not a passing detail), actionable, non-obvious, and likely to recur. Skip trivia — the curator cuts noise, but a thin or polluted candidate pool caps the final quality.

**Model requirements (mandatory).** Run every mining subagent on **Claude Opus 4.8 or later**, using the **strongest-reasoning configuration** the environment exposes (and, if a separate effort control exists, the maximal level). Run each mining subagent in a **clean context** (a fresh subagent that never saw the orchestration conversation).

## Contents

- [Helper scripts](#helper-scripts)

1. [Inputs](#1-inputs)
2. [Candidate record schema](#2-candidate-record-schema)
3. [What to mine](#3-what-to-mine)
4. [Where to look](#4-where-to-look)
5. [The mining procedure](#5-the-mining-procedure)
6. [Coverage & provenance report](#6-coverage--provenance-report)
7. [Handoff to the curator](#7-handoff-to-the-curator)

## Helper scripts

This skill ships helper scripts in its own `scripts/` directory — **use them, don't reinvent them**. They live with the installed skill, **not** in the target repo, so every command invokes them by absolute path as `"$SKILL_DIR/scripts/…"`, where `SKILL_DIR` is this skill's own directory (e.g. `~/.copilot/skills/repository-memory-miner`). Set `SKILL_DIR` once at the start of a run. The bare `scripts/…` names below are identifiers, not paths to run from a checkout.

- `scripts/run-workspace.sh` — sets up the run's output directory outside the mined checkout and polices checkout cleanliness. `init` guards the target, creates a parent-directory-sibling run dir, and prints it. `check` (run after every wave) fails closed if the pinned worktree or invocation checkout gained leaked files. See §1/§5.
- `scripts/dispatch.py` — the orchestrator's single planning command (§5 step 2). Plans the work as bounded streams (code subsystems split at a file threshold, artifact/external streams, collapsed test/data trees), resolves each stream's exact files, computes the git-churn hot-file ranking, coalesces tiny code streams into bounded `codebatch` units, and writes per unit: a churn-ordered `<safeName>.files` read-set, a ready-to-append `<safeName>.context.md`, a `scratch/<safeName>/` output dir, a `streams.tsv` ledger seed, and `dispatch-manifest.json`. Fails closed if streams aren't a clean partition or exceed `--max-streams`.
- `scripts/render-briefs.py` — at the start of a run, resolves each thin brief's `{{include: prompt-fragments/…}}` directives and `{OWNER}`/`{REPO}`/`{REPO_ROOT}` placeholders into ready-to-dispatch prompts under `$RUN_DIR/prompts/`, **failing closed** if any prompt is incomplete (unresolved include, leftover placeholder, missing safety section).
- `scripts/merge-dedup.py` — merges the candidate JSONL emitted by the fleet into one deduplicated candidate set. Unions citations and sanitizes each candidate to the NEW-only schema (dropping any `id` or server-managed field). Conservative: does not rank or cut trivia. Prints a per-input WARN for any file with unparseable/factless records.
- `scripts/validate-coverage.py` — validates the machine-readable coverage ledger (`coverage.json`) and enforces funnel monotonicity (§6).
- `scripts/citation_paths.py` — shared helper for citation path handling.
- `scripts/coverage-ledger.template.{md,json}` — the resumable working ledger to maintain across waves and finalize into the mandatory coverage report (§6).
- `scripts/prompt/subagent-templates/mine-brief.template.md` — the shared mining-subagent prompt brief.
- `scripts/prompt/prompt-fragments/` — shared prompt **fragments** (`what-to-mine`, `where-to-look`, `completeness`, `memory-schema`, `sanitization`, `injection`, `no-side-effects`): the single source for guidance the briefs and this SKILL.md reference.

---

## 1. Inputs

When invoked, establish these inputs (ask the user only if the target repo is unclear):

- **Target repo NWO** — e.g. `github/copilot-agent-runtime`. Required.
- **Output directory** (optional) — where to write all run artifacts. Default: a fresh per-run directory created **outside the target checkout**, as a sibling in the checkout's **parent directory**, named `memory-mining-<owner>-<repo>-<timestamp>/`. The override should also be outside the target checkout. Every artifact — merged candidates, per-unit `scratch/`, and the coverage report — lives inside it, so a run never pollutes the repo it mines.

**Mine `origin/main` HEAD only.** Memories describe what is true of the shipped default branch, so mine the current **`origin/main` HEAD** — never an unmerged feature branch, a PR checkout, or local uncommitted changes. §5 step 1 fetches and pins a clean detached worktree at that commit and mines only that tree, so a dirty or feature checkout can't leak branch-only or soon-stale facts into the output.

**Existing memories are out of scope for the miner.** You never fetch the repo's existing memories and never carry an `id`. Dedup-against-existing and `id` continuity are owned entirely by the curator. **User-scoped memories are also out of scope** — never mine or emit them; work only at repository scope.

---

## 2. Candidate record schema

Each candidate you emit is a NEW repository-scoped record with these fields (the canonical definition is `scripts/prompt/prompt-fragments/memory-schema.md`, rendered into the mine-brief):

```json
{
  "subject": "short topic, 1-2 words",
  "fact": "the memory text injected into prompts",
  "citations": ["file.ts:123", "User input: \"...\"", "..."],
  "reason": "why this fact is worth remembering / when it helps",
  "source": { "interactionId": "...", "agent": "memory-mining", "baseModel": "..." },
  "scope": "repository"
}
```

Rules:

- **`citations` must have ≥1 non-empty entry** pointing at the durable artifact that proves the fact (a file path with line, a PR/issue/run URL, a session id, a quoted user input).
- **NEW candidates only — never emit an `id`** or any server-managed field (`score`, `votes`, `totalVoteCount`, `createdAt`, `updatedAt`, `expiresAt`, `rank`). The existing memory set does not exist at mining time; the curator owns carry-forward and ranking. As defense in depth, `merge-dedup.py` strips any stray `id`/server field a subagent emits.
- `scope` is always `"repository"`.

---

## 3. What to mine

The **mine-for list** — the categories of durable, **actionable**, **non-obvious**, **likely-to-recur** repository facts worth mining — is the canonical fragment `scripts/prompt/prompt-fragments/what-to-mine.md`, rendered into every mining subagent's prompt. The orchestrator dispatches it rather than mining itself; open the fragment for the full list.

---

## 4. Where to look

Gather evidence from **every accessible source** for the target repo — **thoroughness is the whole point of this skill**. Every source is **mandatory**: it is either mined to its definition of done by a dispatched stream, or recorded in the coverage report (§6) with exactly why it couldn't be (and the user told about any missing access). Prefer current, on-main evidence; treat historical/chat/session evidence as supporting.

The canonical list of sources and the per-source **mining procedures** (the `gh`/GraphQL queries, the Slack tooling, the connector-agnostic fallbacks, how to record an inaccessible source) is `scripts/prompt/prompt-fragments/where-to-look.md`, rendered into the mine-brief; each subagent applies only the section for its assigned source. Sources group into three categories:

- **Code** — `main` branch, read to the code-saturation bar (§5 / `completeness.md`) in hot-file-ranked order.
- **Other repo artifacts** — agent sessions (`session_store_sql`), GitHub Actions logs, PRs, issues, Discussions, releases/changelog, repo metadata (Projects v2, wiki, security advisories).
- **External sources** — team chat (e.g. Slack), shared docs / email / meetings / retros (e.g. WorkIQ/M365), telemetry / data warehouse, design docs / ADRs / incident reports.

`dispatch.py` enumerates these as streams and tracks them one-per-row in the coverage ledger. It collapses each test/fixture/benchmark tree into one low-priority `TEST` stream and each extension-dominant data directory into one `DATA` stream, instead of fanning out thousands of streams.

Three §4 jobs stay with the orchestrator:

- **Resolve the issues repositories** — issues for this repo may live in multiple repositories; identify all relevant ones (§5 step 1).
- **Guarantee coverage of connector-backed streams** — sessions, team chat, shared docs/knowledge, telemetry/warehouse, connector-surfaced design docs. Tool surfacing to a given subagent is non-deterministic, so preflight which connectors exist (§5 step 1), then for any connector a subagent could not reach, **retry on a fresh subagent** and, **as a last resort, mine it yourself** (§5 step 4).
- **Surface missing access to the user** — when a source needs access you don't have (e.g. `read:project`, an unjoined Slack channel), tell the user the exact missing access and how to grant it, in addition to recording `no-access` in §6.

---

## 5. The mining procedure

A thorough pass is a **top-level, multi-wave orchestration**: you (the orchestrator) plan the work, dispatch a fleet of **fresh isolated subagents**, drive a resumable ledger to completion, then consolidate. Do **not** try to mine everything in one agent's context — the point of the fleet is parallel breadth and depth.

### 5.1 At a glance

Follow §5.3 for the detail; don't run from this list alone.

1. Establish inputs (§1).
2. Probe scale/access, pin a clean `origin/main` worktree, run `dispatch.py` to enumerate every §4 source/subsystem and materialize ready-to-dispatch per-stream units.
3. Wave-dispatch a fleet of **fresh isolated subagents** (one per stream, the rendered `mine-brief.md` on **Claude Opus 4.8+**) to mine §4 for the §3 targets; drive the §6 ledger to `done` across waves. Throttle each wave to the running-agent cap, refilling with fresh agents as they finish.
4. Consolidate candidates with `merge-dedup.py` → `candidates.merged.jsonl`.
5. **Gap-analysis self-audit** — cross-check the §4/subsystem checklist against what was *actually* mined; re-mine any **mandatory** source skipped without a real blocker.
6. Write the coverage report (§6) with the 🚩 Gaps section; report counts and any sources that were unavailable or any access the user must grant.
7. Hand `candidates.merged.jsonl` + the coverage report to `repository-memory-curator` (§7).

### 5.2 Completeness bars: code saturation vs. artifact breadth

Code and artifact streams have **different** definitions of `done`:

- A **CODE stream is `done`** only when the subagent read **every** high-signal file in scope — not a sample — and a final sweep surfaced no new durable facts.
- An **ARTIFACT/EXTERNAL stream is `done`** only when its source was paged to the breadth target (full PR/issue/discussion threads, not previews); otherwise it stays `partial`/`no-access`/`tool-missing` with the exact unread files/fractions and blocker recorded.

The full per-stream bar is the fragment `scripts/prompt/prompt-fragments/completeness.md` (rendered into the mine-brief).

**Volume sanity check (scaled to repo size).** Judge the raw candidate count against the repo's tracked-file count (from step 1), not an absolute floor: a large/non-trivial repo should surface **many hundreds** of raw candidates and a few dozen signals under-mining — but a **genuinely small repo** (tens of tracked files) may saturate at a few dozen high-quality candidates. Record both counts and judge them together.

### 5.3 The orchestration loop

**Fleet concurrency.** Subagents run under an **environment-specific cap on how many run *concurrently*** (order of dozens). A **finished agent does not count** — it drops to `idle` and frees its slot the moment it finishes — so manage the budget **per wave**, not across the run:

- Keep no more than ~the cap **running at once**; as agents finish, launch **fresh** subagents for the next streams. Idle agents are free; never reserve cross-phase headroom or recycle agents.
- A subagent's **model is fixed when it is created**, so create each on the right model. `write_agent` reuse keeps the agent's model **and** accumulated context — use it only for genuine **same-unit continuation** (e.g. asking a stream's own agent to finish writing a file), never to free capacity.
- Idle background agents linger in `list_agents` and **cannot be programmatically retired** (there is no stop/kill-agent tool), but they don't occupy a running slot.

Steps:

1. **Probe scale + access; pin a clean `origin/main` worktree.** Clone or `cd` into the target repo and note its absolute path as `TARGET` (the checkout you cloned/`cd`'d into — not a blind `git rev-parse --show-toplevel`, which could resolve an unrelated enclosing repo). Set `SKILL_DIR` to this skill's own directory so the `"$SKILL_DIR/scripts/…"` commands resolve regardless of working directory. Create the run's output directory **outside `TARGET`**:

   ```bash
   RUN_DIR="$(bash "$SKILL_DIR/scripts/run-workspace.sh" init --target "$TARGET" --owner <owner> --repo <repo>)"
   # pass --run-dir <dir> to override the default location (keep it outside TARGET)
   ```

   **Pin the mining tree to `origin/main` HEAD.** Find the default branch via the GitHub MCP server, assign it to `$DEFAULT_BRANCH`, then:

   ```bash
   git -C "$TARGET" fetch origin
   MAIN="$RUN_DIR/main"   # a sibling under $RUN_DIR, outside TARGET
   git -C "$TARGET" worktree add --detach "$MAIN" "origin/$DEFAULT_BRANCH"
   git -C "$MAIN" rev-parse HEAD   # record this SHA in §6; every stream is pinned to it
   ```

   Use **`$MAIN` as the repo root for every repo-reading step** (`dispatch.py`, churn, code reading, citation notes). Remove the worktree at the end (`git -C "$TARGET" worktree remove "$MAIN"`). Confine your own scratch to `$RUN_DIR/scratch/`. Record tracked-file count (`git -C "$MAIN" ls-files | wc -l`), rough PR/CI counts (`gh pr list`, `gh run list`), and which sources you can reach.

   **Run a connector preflight**: for each connector capability — `session_store_sql`, team chat (Slack/…), shared docs/knowledge (WorkIQ/…), telemetry/warehouse, doc-parsing (`markitdown`/…) — classify it **present-and-usable**, **present-but-permission-gated**, or **absent** by (a) **discovering** the tool (e.g. `tool_search_tool_regex`) and (b) **probing** it with a trivial call. Two gates to clear once and record: WorkIQ requires interactive **EULA acceptance** on first use (accept, then re-probe), and the warehouse tool may expose **no default cluster** (discover and record the cluster URI + database first). A capability **absent** from the environment is `tool-missing` (§6): record it (nothing to grant) and do not dispatch its stream. A **present-but-permission-gated** resource (e.g. `read:project`, an unjoined Slack channel) is `no-access`: record it and tell the user the exact access. A **present** connector is expected — step 4 dispatches its stream and retries on a fresh subagent if a subagent can't reach it. Resolve the **issues repositories** (§4). Cheaply pre-probe the unconditional artifact sources (Discussions enabled? any releases / Projects v2 / wiki / security advisories?) and mark each empty one `done` + `empty:true` instead of dispatching a subagent that finds nothing.

   **Clean-checkout assertion (run after every wave).** A subagent's shell cwd is the invocation checkout, so a stray relative write can land there. After every wave — and before the final report — assert both the pinned worktree and invocation checkout are pristine:

   ```bash
   bash "$SKILL_DIR/scripts/run-workspace.sh" check --run-dir "$RUN_DIR" --target "$TARGET"
   ```

   If it trips, **stop**: find the leaking subagent, move its strays under `$RUN_DIR`, tighten that dispatch's prompt, and continue — never auto-delete from `TARGET` (it may hold the user's own work).

2. **Plan and dispatch the streams.**

   ```bash
   python3 "$SKILL_DIR/scripts/dispatch.py" --repo-root "$MAIN" --run-dir "$RUN_DIR"
   ```

   `dispatch.py` enumerates the whole tree into bounded streams — `CODE` (every subsystem, large dirs split so none exceeds the threshold), `ARTIFACT` (PRs, CI, issues, discussions, releases, projects, sessions), `EXTERNAL` (team chat, shared docs/email, telemetry, design docs) — collapses each test/fixture/benchmark tree into one low-priority `TEST` stream (skim for testing conventions only) and each extension-dominant data directory into one `DATA` stream (skip — no durable memories), then **coalesces the many tiny CODE streams into bounded `codebatch` units**. Per dispatched unit it writes a churn-ordered `<safeName>.files` read-set and a `$RUN_DIR/dispatch/<safeName>.context.md`. It **fails closed** if streams aren't a clean partition (an empty code stream, two streams sharing a file, a union ≠ the mineable set) and if the code-stream count exceeds `--max-streams` (default 500) — naming the largest directories on stderr. When that happens, inspect those directories and **re-run with `--exclude <glob>`** (repeatable) to drop genuinely irrelevant data/vendor trees, recording each exclusion in §6; raise/disable the cap (`--max-streams 0`) only for a genuinely huge repo. Seed the coverage ledger from `$RUN_DIR/dispatch/streams.tsv` (status `dispatched`; each `DATA` row is pre-marked `skipped`).

   Then **render the subagent prompts once for this run**:

   ```bash
   python3 "$SKILL_DIR/scripts/render-briefs.py" --owner <owner> --repo <repo> --repo-root "$MAIN" --out-dir "$RUN_DIR/prompts"
   ```

   This resolves each brief's shared-fragment includes and repo placeholders and **fails closed** if any prompt is incomplete. Dispatch every subagent with the matching `$RUN_DIR/prompts/<role>-brief.md` plus its machine-written `<unit>.context.md` — never hand-author per-unit context.

   **Hot-file ranking (optional tuning).** `dispatch.py` computes git churn itself and orders every read-set **most-churned first** (default window 6 months; pass `--churn-window` to widen/narrow). The ranking **orders — never limits — reading**: a low-churn file is read later, not skipped. For a different ranking, compute a `<count> <path>` list yourself and pass `--hot-files <path>`.

3. **Wave 1 — dispatch one subagent per dispatch unit, in parallel** (each on **Claude Opus 4.8+**, max reasoning, **blank context**). Dispatch each with the rendered `mine-brief.md` **plus that unit's `$RUN_DIR/dispatch/<safeName>.context.md`** (written by `dispatch.py`), which carries everything stream-specific: id, **`kind`** (`CODE`/`TEST`/`ARTIFACT`/`EXTERNAL` — the bar the mine-brief keys off), scope, `REPO_ROOT`, the `<safeName>.files` read-set pointer (for CODE/TEST), connector metadata, and the candidate/coverage-note/scratch output paths under `$RUN_DIR/scratch/<safeName>/`. The mine-brief carries the per-source procedures (`where-to-look.md`); the subagent applies the section for its source. For ARTIFACT/EXTERNAL units the context carries only the source's one-line scope, so the subagent locates and pages the concrete artifacts itself.

   Special handling: a **`TEST`** unit is a single low-priority skim for testing conventions (one subagent, never split for depth); a **`DATA`** unit is **not dispatched at all** (carry its pre-marked `skipped` status + file count). A stray `DATA`/`TEST` row you judge might hold real code should be re-planned (narrow `--exclude`) and flagged as a gap.

4. **Connector-backed streams: delegate, but guarantee coverage with preflight + retry.** Sessions, team chat, shared docs/knowledge, telemetry/warehouse, and connector-surfaced design docs need a connector that may not be surfaced to a given subagent (surfacing is **non-deterministic**). They are still **dispatched** like the others (they can be context-heavy — keep them off the orchestrator's context), but the orchestrator owns the guarantee:

   - Each connector subagent **asserts the connector is callable as its first action** and, if absent, emits `TOOL_MISSING: <stream-id> <capability>` and writes no candidates.
   - A connector the preflight found **absent** is not dispatched (record `tool-missing` + gap; nothing to retry/grant).
   - A connector the preflight found **present** is expected: if its subagent returns `TOOL_MISSING` (or returns neither candidates nor a coverage note — a silent miss), **re-dispatch to a fresh subagent, up to ~3–5 retries** (fresh surfacing is likely to succeed). Track the retry count in the ledger.
   - **Last resort:** if still missing after retries, the **orchestrator mines that stream itself** (the preflight reached the connector) with targeted queries and compact notes — still writing the per-stream candidate JSONL and coverage note and flipping its ledger row (covering agent `orchestrator`) so the run stays resumable. If even the orchestrator can't reach it, record `tool-missing` + a gap.
   - **Per required tool.** A secondary tool (e.g. WorkIQ surfacing doc URLs a `markitdown` parser reads) is preflighted too; a stream whose primary is present but secondary is unsurfaced records the unparsed URLs in its coverage note and hands them to a wave-2 follow-up that has the parser.
   - **Bound each connector stream's wall-clock** so one can't stall the run: the subagent self-caps its calls/retries and finalizes; as a backstop the orchestrator checks elapsed time at its poll points and, when a stream is well over a sane per-stream budget, `write_agent`s a cooperative cutoff ("write up what you have, then stop"), then marks it `partial` with the unmined scope.

5. **Collect + ledger.** As subagents finish, record each stream's real coverage (`done`/`partial`, with the saturation basis or artifact fraction). If a subagent returns JSONL inline instead of writing a file, capture it and verify line counts — never assume a file exists. After the wave, run the clean-checkout assertion (step 1).

6. **Wave 2+ — close gaps** (re-dispatch the same `mine-brief.md` subagents on **Claude Opus 4.8+**). Re-dispatch focused follow-ups for every CODE stream left `partial` with unread high-signal files and every ARTIFACT/EXTERNAL stream below its breadth target. Repeat until every CODE stream is `done` by the saturation bar, each TEST stream is skimmed, and artifacts hit targets — or, on a genuine runtime cap, leave items `partial` and name exactly what's left (§6). Apply the volume sanity check, scaled to repo size.

7. **Consolidate.** Merge all candidate JSONL — collapses near-identical facts, unions citations, and sanitizes each candidate to the NEW-only schema:

   ```bash
   python3 "$SKILL_DIR/scripts/merge-dedup.py" <fleet-dir> --out "$RUN_DIR/candidates.merged.jsonl"
   ```

   This is the miner's deliverable. **Do not** fetch existing memories, rank, or cut trivia here — that is the curator's job.

**Resumability:** the ledger is the source of truth. If a run is interrupted, a later session reads it and re-dispatches only streams not yet `done`, so a multi-hour run can span many sessions.

---

## 6. Coverage & provenance report

Every run **must** emit both `<owner>-<repo>.coverage.json` and `<owner>-<repo>.coverage.md` alongside `candidates.merged.jsonl`. The JSON ledger (start from `coverage-ledger.template.json`) is validated by `validate-coverage.py`; the Markdown report (start from `coverage-ledger.template.md`) is the human-readable audit surface. The Markdown report must contain:

- **Per-source table** — one row per §4 source: status (`done`/`partial`/`skipped`/`no-access`/`tool-missing`), what was read (counts: files, PRs, issues, discussions, sessions, Slack channels/threads, WorkIQ queries), and the **exact searches/queries/IDs** run (so the run is reproducible).
- **Codebase coverage ledger** — the full subsystem list with a per-subsystem status (`done`/`partial`/`skipped`) and the covering agent/method; flag any subsystem left `partial` and why. Record any directory `dispatch.py` **collapsed** (`TEST`/`DATA`) or that you **`--exclude`d**, with the reason and approximate file count, and flag as a 🚩 gap any excluded/skipped tree that might still hold real code.
- **🚩 Gaps & "Not Done" (most important section)** — a prominent, complete list of: anything considered but skipped (and why), anything only partially covered, any source that timed out or returned nothing, any access/permission failure (`no-access`, with the exact error), any missing connector (`tool-missing`, naming the absent capability), and any artifact you think exists but couldn't read. **Do not bury or omit gaps — surfacing them is a primary deliverable.**
- **Candidate counts** — the **raw candidate count** before merge and the **merged candidate count**, judged against the tracked-file count (the volume sanity check). A tiny count on a non-trivial repo signals under-mining; re-audit before finishing.

Validate the JSON ledger:

```bash
python3 "$SKILL_DIR/scripts/validate-coverage.py" "$RUN_DIR/<owner>-<repo>.coverage.json" --run-dir "$RUN_DIR"
```

A run with an empty or vague gaps section is suspect: re-audit before finishing. In coverage JSON, use source statuses `done`/`partial`/`skipped`/`no-access`/`tool-missing` plus a separate `empty` boolean; use code statuses `done`/`partial`/`skipped`. `no-access` = connector present but resource permission/scope-gated (name the access); `tool-missing` = capability absent from the environment (nothing to grant). Any non-`done` source and any `partial` code stream must include an explicit gap.

---

## 7. Handoff to the curator

The miner's deliverables are:

- `$RUN_DIR/candidates.merged.jsonl` — the deduplicated NEW candidate pool.
- `$RUN_DIR/<owner>-<repo>.coverage.{md,json}` — the coverage report.

Pass these to **`repository-memory-curator`**, which fetches the repo's existing memories, verifies each candidate against its citations, dedups/merges against existing memories, rewords, ranks, and writes the final curated full-replacement set. Tell the user the path to `candidates.merged.jsonl` and surface any access the curator will still need (e.g. memory-read access) plus any 🚩 gaps from §6.
