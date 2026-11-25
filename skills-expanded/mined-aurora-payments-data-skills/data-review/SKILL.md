---
name: data-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) in a data codebase (dbt, Dataform, SQL pipelines) along three axes: Standards (does the change follow this repo's documented conventions?), Spec (does the change match what the originating issue/spec asked for?), and Impact (what does the change do to the data, covering downstream consumers, contracts, destructive writes and cost?). Runs the reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, a model or pipeline change, work-in-progress changes, or asks to \"review since X\" in a warehouse or pipeline repo. For app-code repos, stock code-review applies instead."
---

Three-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the change conform to this repo's documented conventions?
- **Spec**: does the change faithfully implement the originating issue / spec?
- **Impact**: what will the change do to the data: who consumes the affected models, what breaks a contract, what write is irreversible, what does it cost?

All axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

The issue tracker should have been provided to you: run `/setup-data-skills` if `docs/agents/issue-tracker.md` is missing.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point: a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.). Fetch via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how transformations should be written, such as a SQL style guide, `CONTRIBUTING.md`, or the dbt project docs, plus the linter config (`.sqlfluff`, dbt-checkpoint hooks), which tells you what tooling already enforces so you can skip it.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below, a fixed set of data-modeling smells (drawn from the dbt structure guides, Kimball's grain discipline, and functional data engineering) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Silent Fan-Out"), never a hard violation. Like any standard here, skip anything tooling already enforces (SQLFluff rules, dbt-checkpoint hooks, the contract preflight).

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Undeclared Grain**: a new or reshaped model whose one-row-per-what isn't stated anywhere. → declare the grain in the model's description and pin it with a uniqueness test on the grain key; if no honest grain statement comes, the model's murky.
- **Staging That Joins**: a staging model containing joins or aggregations. → move them to an intermediate model; staging stays one-to-one with its source table: rename, cast, categorize, nothing more.
- **Source Reach-Around**: a raw source read outside the staging layer, or a hardcoded table name where a `ref()`/`source()` belongs. → route the read through the staging model; reference other models by `ref()`.
- **Silent Fan-Out**: a join that can multiply rows, with nothing guarding the declared grain. → test the grain key for uniqueness after the join, or aggregate back to grain before joining.
- **Duplicated Logic**: the same business rule (a metric formula, a classifying case-cascade) written out in more than one model in the change. → extract it upstream into one model or macro both sites read.
- **Department Fork**: a second mart for the same entity, split by audience (`finance_orders` beside `marketing_orders`). → one entity, one mart; the differences become columns or metrics.
- **Rollup Mart**: a mart at a time-aggregated grain (`orders_per_day`). → keep marts entity-grained; rollups belong to the metrics/semantic layer.
- **SELECT-Star Passthrough**: `SELECT *` flowing source columns straight into a downstream model, importing schema drift. → enumerate the columns; let the contract catch shape breaks instead of inheriting them.
- **Non-Idempotent Write**: output that depends on wall-clock time or prior runs (an incremental that double-counts on re-run). → make the transform deterministic and the write an idempotent overwrite of its partition.
- **Naked Destructive Write**: a truncate-and-replace, full refresh, or `DROP` in the change with no recovery note. → prefer append/merge semantics; if replacement is required, name the rollback path (snapshot, clone, time travel) in the PR.
- **Unbounded Scan**: a read of a large table with no partition filter, or a new large table with no partitioning at all. → filter on the partition column; require the filter on tables big enough to hurt.
- **Speculative Generality**: columns, parameters, or models added for consumers that don't exist yet. → delete them; inline back until a real consumer shows.

### 4. Identify the impact surfaces

What the Impact sub-agent will read, looked up in this order:

1. A state-comparison setup: a production manifest to select against (`dbt ls --select state:modified+`), or the repo's own CI state harness.
2. A consumer registry: dbt exposures, or whatever the repo uses to register downstream readers, including the BI registry mapping dashboards to the models and freshness columns they read (the org's dashboard config, where one exists).
3. A data-diff harness wired to PRs (Recce or equivalent).
4. A dry-run wrapper for cost (`bq query --dry_run` or the warehouse equivalent).

Contract-aware selection has a version floor: model contracts and `state:modified.contract` need dbt >= 1.5, and catching a deleted contracted model needs dbt >= 1.9. On older projects those checks silently pass, so name the project's dbt version in the sub-agent's inputs.

If none of these exist, the Impact sub-agent still runs: it reports blast radius from the DAG alone (the `ref()`/dependency edges of what changed) and lists what it could not check.

### 5. Spawn the sub-agents in parallel

**Standards sub-agent prompt**: include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full, because the sub-agent has no other access to it.
- The brief: "Report, per model/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls. Documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt**: include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

**Impact sub-agent prompt**: include:

- The diff command and commit list.
- The impact surfaces found in step 4, each named explicitly, and, just as explicitly, which lookups came up empty, so the sub-agent can report what it could not check.
- The brief: "Report: (a) blast radius, meaning every downstream model and registered consumer of what changed; (b) contract breaks, meaning removed or retyped columns on any contracted or public model; (c) write mode, meaning anything that replaces rather than appends to shared state, with its recovery path or lack of one; (d) cost, as dry-run bytes for new or reshaped queries where a dry run is available; (e) which changed models deserve a data diff before merge, with the diff evidence if a harness exists; (f) freshness-contract and control breaks, for any changed model a registered dashboard reads: freshness columns removed, renamed, or re-anchored to a rebuild timestamp, and any synced-control dimension whose value set the change alters. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 6. Aggregate

Present the reports under `## Standards`, `## Spec`, and `## Impact` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings; the axes are deliberately separate (see _Why three axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes, since that's the reranking the separation exists to prevent.

## Why three axes

A change can pass any two axes and fail the third:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**
- Code that satisfies both and still truncates a table it can't restore, or silently reshapes a mart three dashboards read → **Standards pass, Spec pass, Impact fail.**

The third failure is the data-engineering default: pipeline changes land on shared state, and their failure mode is plausible-wrong numbers that reading the diff will not catch. Reporting the axes separately stops any one from masking the others.
