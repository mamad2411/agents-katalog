---
name: harness-creator
description: >-
  Create, update, modify, or retire an agent harness through governed intake. A harness is a
  repeatable, enforced pipeline: AI steps, deterministic checks, human gates and an independent
  verifier, with declared capabilities and hard stops. A four-quadrant intake runs before any spec
  is written. A six-fact runbook (how to run, stage and scale, live-environment access, QA method and
  receipts, roadmap, guardrails) is a hard gate: every fact needs an answer or an explicit N/A with a
  reason. The skill writes a documented registry (harnesses/registry.yaml), per-harness pipeline specs
  and intake transcripts, and checks them with a bundled checker. Every harness starts as 'unproven'
  and becomes 'active' only after each seeded failure has been shown to fail on bad input. Use when
  the user says "create a harness", "new harness", "scaffold a pipeline", "update / modify / retire
  a harness", "make this workflow enforceable", or when a repeatable agent workflow needs gates and
  proof instead of prose.
---

# Harness Creator

A **harness** is a repeatable pipeline an agent runs to get a class of work done under enforcement.
It has ordered nodes (AI steps, deterministic checks, human gates, an independent verifier),
declared capabilities, a way to prove each run happened, and hard stops. This skill is the governed
way in for creating one, changing one, and retiring one.

Everything below rests on one lesson: **a harness written only as prose is not a harness.** If the
executing agent can grant itself an exemption from a step, it eventually will. The verifier gets
skipped "because the diff is trivial". A run reports "shipped" with no commit behind it. A root
cause found in the plan gets dropped during implementation. So every harness made here carries its
own enforcement (deterministic nodes, an unskippable verifier, a final postcheck). It stays
`unproven` until that enforcement has been caught failing on bad input.

## What this skill creates in the user's repo

Paths are relative to the repo root. The default directory is `harnesses/`. If discovery (Q3) finds
that the repo already has a registry of pipelines or workflows, ask whether to adopt it. Never run
two registries side by side.

| Path | Contents | Lifecycle |
|------|----------|-----------|
| `harnesses/registry.yaml` | The index: one entry per harness | Entries are never deleted; retired ones stay, and an id is never reused |
| `harnesses/{id}.yaml` | The pipeline definition: nodes, terminal states, seeded failures | Written only once the pipeline is real (see the honesty rule) |
| `harnesses/intake/{id}-{verb}-{YYYY-MM-DD}.md` | Intake transcripts. The first one is the harness's **birth certificate** | Append-only; never deleted |
| `harnesses/verifier-{id}.md` | Verifier persona (optional; start from `references/verifier-persona.md`) | Versioned with the harness |
| `harnesses/scripts/` | Helper scripts the nodes call, such as the postcheck (or keep them elsewhere and cite the path in the node's `command`) | Versioned with the harness |

The full field-by-field schema is in `references/schema.md`. Copyable skeletons are in
`references/templates.md`. The bundled checker (`scripts/harness_check.py`) enforces the schema.

## Lifecycle verbs

Every verb goes through the same governance. Only the depth of the intake changes.

| Verb | Intake | Runbook gate | Status effect | Output |
|------|--------|--------------|---------------|--------|
| **create** | Full Q1-Q4 | All six facts required | `unproven` | New entry + birth certificate |
| **update** | Diff-based: read the current state, ask only about what changed | Confirm all six facts are still true | Unchanged if the pipeline shape is unchanged | Updated entry + amendment transcript |
| **modify** | Full Q1-Q4 again (the scope or shape changes) | All six facts re-verified | **Reset to `unproven`** | New version + modification transcript + new seeded failures |
| **retire** | Reason + impact analysis | Not required | `retired` | Retirement block + retirement transcript |

To tell update from modify, ask: would the seeded failures written for the old version still prove
the new one? If not (a node added, removed or reordered, a gate moved, a new mode, a new live system
touched), it is a **modify**.

For update, modify and retire, start from the existing registry entry, the definition and the
earlier transcripts, not from a blank page.

## Phase 1: Four-quadrant intake (mandatory, always first)

Do not write a line of spec until the intake has converged.

### Q1. Known knowns (the contract)
These are facts both sides already hold. Collect them up front: the id (kebab-case), name,
one-paragraph description, target project or repo, the lifecycle verb, and what triggers the
request (a recurring manual workflow, a failure that keeps coming back, a new capability).

### Q2. Known unknowns (open questions, asked one at a time)
These are things you know you don't know. Ask **one question per turn**. Use the agent's structured
question tool if it has one; otherwise ask in plain text. Never batch questions, never guess, and
never fill an answer from a default. The usual sources are:
- runbook facts not yet answered (Phase 2)
- capability scope that the description leaves unclear
- how this harness connects with other harnesses (does it fire one, or get fired by one?)
- access the harness needs beyond what the repo shows

### Q3. Unknown knowns (discovered, never asked)
These are facts the repo already holds. Read them without asking, and cite each one in the
transcript. Understand the project before making anything up.
- CI config, package scripts, Makefile or other task runners: which test, lint, typecheck and build
  commands **actually exist**. A gate that calls a missing script is a blocked node, not a passing
  one. Record the gap as a blocking fact.
- existing agent commands, subagent definitions, hooks and workflow docs the harness would wrap or
  duplicate
- state and receipt files that current workflows already write
- documented access: READMEs and contributor docs that say how to reach a database, log source or
  deploy target. (One real failure: an implementer claimed it had "no DB access" when the access
  was documented in the repo's own instructions.)
- harnesses already in the registry: overlaps, and things this one can reuse or chain into

If the harness targets a different repo from the one you're in, do a read-only scan of that repo
first. Don't ask the human anything the code already answers.

### Q4. Unknown unknowns (completeness-critic pass)
When Q1-Q3 are done, critique the whole picture:
- What could go wrong that nobody has talked about?
- What access or infrastructure are we assuming without having checked it?
- Which node has an edge case with no gate on it?
- If this harness failed silently, who would notice, and when?
- What would a lazy run that still looks compliant look like, and what stops it?

If you can spawn a subagent with a fresh context, run the critic there, since fresh eyes find more.
Otherwise do the pass yourself. Each finding becomes a Q2 question. Repeat until a full critic pass
turns up no new questions. That is convergence.

### Birth certificate
Save the whole intake as `harnesses/intake/{id}-create-{YYYY-MM-DD}.md` (template in
`references/templates.md`): every Q1 fact, Q2 answer, Q3 discovery with its source, Q4 finding, and
the runbook table. Never delete it. Each later update, modify or retire adds its own transcript, and
the registry entry's `intake:` list names all of them.

## Phase 2: Six-fact runbook (HARD GATE)

Do not produce a final spec until all six facts have an answer or an explicit N/A with a reason.
No exceptions, no defaults, no inference.

| # | Registry key | Question |
|---|--------------|----------|
| R1 | `how_to_run` | What command, trigger or event fires it? What inputs does it need? |
| R2 | `stage_and_scale` | Where does it run (local / CI / production)? How often? What is the budget per run (tokens, time, money)? |
| R3 | `live_env_access` | Which live systems does it read or write (databases, APIs, servers, file systems, third-party services)? Read-only or read-write? |
| R4 | `qa_method` | How is its output validated? What proof does a run produce, and where are receipts stored? |
| R5 | `roadmap` | Where does it sit in the project's priorities? What depends on it, and what does it depend on? |
| R6 | `guardrails` | What must it NEVER do? Rate limits, blast-radius limits, forbidden paths, human gates? |

An **acceptable answer** is specific (at least 8 characters), or has the form `N/A (reason)` where
the reason passes the same test. These are **not acceptable**: a blank; an answer that opens with a
deferral word, meaning uppercase `TBD`/`TBA`/`TODO`, or any case followed by nothing or a separator,
or a leading `?` (so "TBD - ask ops" fails, while "Todo app backend API" is a real answer); a bare
`none`, `unknown`, `N/A`,
"standard", "the usual", "as usual" or "same as before"; leftover `{template braces}`; and anything
you inferred rather than were told or found (a discovered fact must cite its source in the
transcript). The checker catches all of these except the last, which is your judgment call.

```
for fact in R1..R6:
    if fact is missing, a placeholder, or an N/A without a reason:
        REFUSE to continue to Phase 3
        tell the human exactly which fact is missing
        ask for it (one question), or for an explicit N/A with a reason
```

**Blocked harnesses.** Sometimes a fact can't be answered because something doesn't exist yet
(no feedback source, no analytics store). Record it as `N/A (blocked: what is missing)` and add a
`blocking_facts:` list to the entry. A blocked harness may be registered as `unproven`, which keeps
the intent and the answers already given. It cannot become `active` while any blocking fact stands.

**Shared facts.** When you register several harnesses for the same project in one session, ask the
project-level facts (R2, R3, R5) once. Later harnesses inherit them and are asked only for the
differences. Mark inherited answers in their transcripts as `(shared, from {other-id} intake)`.

## Phase 3: Write the spec

### Registry entry
Every entry has an id, name, project, status, version, created date, description, the full
`runbook:` (six keys), a non-empty `capabilities:` list (what the harness CAN do, one line each,
concrete) and the `intake:` transcript list. On create the status is always `unproven`. Optional
fields are `definition`, `source` (the workflow, command, hooks and state files it wraps),
`blocking_facts`, `depends_on`, `tags` and, once retired, `retired`. See `references/schema.md`.

### Definition file (the honesty rule)
Write `harnesses/{id}.yaml` only when the pipeline is real: you can name every node's command or
role, inputs and outputs. A harness that is still just a runbook plus capabilities is registered
without a definition. Don't invent nodes to fill the file; nodes come with the first real pipeline.
A harness without a definition cannot become `active`.

### Pipeline design rules
The checker enforces the rules marked **(checked)**.

1. **Every deterministic node has a `command` and an `on_failure.prompt`** that states the norm AND
   the remediation. (checked) A remediation may never be "disable the rule", "skip the test",
   "weaken the assertion" or "silence the type error".
2. **The verifier is independent and unskippable**: `fresh_session: true`, `read_only: true`,
   `unskippable: true`, `exemptions: none`. (checked) It sees only the original task, the output or
   diff, and the check results, never the implementer's reasoning. Its default posture is REJECT.
   There is no "trivial change" bypass. `read_only` means it writes nothing but its verdict: it is
   still expected to run tests, linters and the plan's verification commands itself. Persona:
   `references/verifier-persona.md`.
3. **Every human gate declares `terminal_on_reject: true` and a declared `terminal_state`**, and the
   rejection reason goes into the receipt. (checked)
4. **The last node is a deterministic postcheck.** It checks every artifact the success receipt will
   claim: the commit exists, the branch is not the default branch, the verdict file exists, the PR
   or deploy URL is real. For a local-merge ship with no remote, check instead that the feature
   commit is an ancestor of the target branch. No run may report success unless it passes. (checked)
   This is what stops receipt inflation.
5. **Implementation happens in a fresh context**, working from the approved plan alone, on a fresh
   branch or worktree (never the default branch), with a bounded number of attempts (3 is a good
   default). After that the run ends as `exhausted`.
6. **Terminal states come from one vocabulary**: `success`, `blocked`, `approval-required`,
   `exhausted`, `no-progress`, `clean-no-op`. Declare the ones the pipeline can reach; `success` is
   required. (checked) Every run ends in exactly one of them.
7. **Hard stops go in `constraints:`**: a budget cutoff (for example, stop at 80% of the run's
   budget and write the receipt), the maximum number of attempts, and paths the harness must never
   touch (secrets, credentials, payment code).
8. **Every run writes a receipt** to the R4 location: the terminal state, the commands run and
   their exit codes, and the artifact paths. A receipt without evidence is a claim, not a receipt.

If an AI node writes things and the pipeline has no verifier, the checker warns about
self-verification. Treat that warning as a question for the human, not as noise.

### Capability blocks
If the pipeline has a plan, implement, review or ship shape, read `references/capability-blocks.md`.
Adopt the blocks that fit, and record every block as adopted or skipped, with a reason, under
`capability_blocks:` in the definition.

## Phase 4: Seeded failures (unproven to active)

A harness moves from `unproven` to `active` only when **every seeded failure has been shown to fail
on bad input**. A gate that has only ever been seen passing hasn't been shown to work.

Minimum set (at least 3 in total):

| `kind` | Required when | Proves |
|--------|---------------|--------|
| `verifier-rejects-bad` | a verifier node exists | the verifier REJECTs a deliberately bad output (fabricated result, silenced error, untouched root cause) |
| `verifier-approves-good` | recommended alongside the above | a control case. A verifier that rejects everything also passes the first test |
| `deterministic-fails-broken` | any deterministic node other than the postcheck | each check fails on deliberately broken input: write one per deterministic node (the checker only requires one in total, so covering every node is on you) |
| `postcheck-fails-missing` | always (the postcheck is mandatory) | the postcheck fails a "success" that has no commit, no branch, no artifact |

For each one: build the bad input, run the **real** node against it, see it fail, then record
`proven: true`, `proven_at`, and a `proof` (the command, the exit code or verdict you observed, and
the artifact path).

Proof discipline, learned the hard way:
- **Use the production invocation.** Run it with the same interpreter, shell, flags and working
  directory that the harness itself uses. A check that fails correctly in your test shell but
  crashes under the real invocation (an encoding or quoting error, say) can quietly "pass" everything.
- **Fail-open is a failure.** If a gate errors out, the harness must treat that as `blocked`, never
  as a pass. Seed at least one malformed input to confirm this.
- **A stub proves the plumbing, not the instruction-following.** For an AI node that depends on a
  model following the spec's prose, do one real model run per node before going active. A stub
  emits what the test told it to, so it only confirms that the test agrees with itself.
- **Never touch a live system to prove a red.** Use fixtures, temporary copies or a scratch branch.

Only then set the status to `active`. When a **modify** changes the shape, the status goes back to
`unproven`. Keep the old proofs on record, and add and prove seeded failures for the new shape.

## Phase 5: Validate

Run the bundled checker after every registry or definition write, from the repo root:

```
python .claude/skills/harness-creator/scripts/harness_check.py --root harnesses
```

Exit code 0 means no errors (warnings are printed and should be reported to the human), 1 means
errors, and 2 means a usage or environment problem. The checker needs PyYAML. If it's missing, tell
the user to install it (`pip install pyyaml`), or walk through the manual checklist in
`references/schema.md` item by item. If the project has its own validator or CI, run that too. Do
not report the work as done while the checker shows errors.

The checker is enforcement too, so it has its own seeded failures: `--selftest` builds a valid
fixture, confirms it passes, then applies a series of deliberate breakages and confirms each one is
caught.

## Retiring a harness

1. Record the reason for retirement.
2. Do an impact analysis: what fires it (commands, schedules, CI jobs, other harnesses' nodes), what
   consumes its outputs or receipts, and whether anything replaces it.
3. Set `status: retired` and add `retired: {at, reason, replaced_by}`.
4. Keep the entry, the definition and every transcript. Ids are never reused.
5. Write the retirement transcript and add it to `intake:`.

## Evolving an active harness

Change a harness because of evidence (its receipts), not taste. If it misses its QA metric three runs
in a row, don't tweak it in place. Run a structured experiment with a rollback: one change, measured
against the same metric, then kept or reverted. Each real failure should turn into a rule or a check
(a ratchet), with a line in the next transcript saying which failure caused it.

## Guard rails (never)

- Never write a spec before the Phase 1 intake converges.
- Never write the final spec while any runbook fact is missing, a placeholder, or an N/A without a
  reason.
- Never set `active` before every seeded failure is proven on bad input and the checker is clean.
- Never skip or delete a transcript; the birth certificate is permanent.
- Never let a verifier have exemptions, and never let a run claim success without the postcheck.
- Never delete a registry entry or reuse an id.
- Never touch live systems, secrets or production to prove a seeded failure.

## Report back

Lead with what changed: the harness id, the verb, the old and new status, and the version. Then:
which runbook facts are N/A or blocked, which seeded failures are still unproven, the checker's
output, and the one decision the human needs to make next.
