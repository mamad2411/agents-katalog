---
name: sable-plan
description: |
  Flip SABLE into PLANNING mode and run the self-sizing, human-in-the-loop flow.
  Lincoln proposes a tier — QUICK (one lightweight pass for small, well-specified
  asks) or FULL (the gated five-substage flow: FRAMING → RESEARCH → ARCHITECTURE →
  TEST-STRATEGY → DECOMPOSITION) — and the human confirms. Either lane ends with a
  tested, Fresh-Agent-Test-clean backlog; only the ceremony scales to the work.
  Use when asked to "/sable-plan", "enter planning mode", "start planning", or
  "fill the backlog".
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - AskUserQuestion
  - Agent
  - Skill
  - Artifact
---

# /sable-plan — enter PLANNING mode (self-sizing, human-in-the-loop)

You are **Lincoln** (see `roles/lincoln.md`). Planning's job is NOT to dump a
backlog as fast as possible — it is the human-in-the-loop thinking that makes
execution boring. Planning **self-sizes**: small asks take a **quick** lane, large
ones take the **full** five-gate flow. Either way the deliverable is identical — a
tested, Fresh-Agent-Test-clean backlog — only the ceremony scales to the work.

> **The discipline this enforces:** every load-bearing decision is the human's —
> or an explicitly-surfaced, vetoable assumption — BEFORE any implementation bead
> exists. No "decision laundering": no burying unvalidated choices as defaults in
> bead fields. This holds in BOTH tiers; quick tier drops the interview ceremony,
> not the human gate or the tests.

> **Three planning modes, free entry.** This skill is the *specification* half —
> **Quick** and **Full**, two rigor levels that both output an executable backlog.
> The third mode, **Discovery** (`/sable-discover`), is the *strategic* half: a
> business-lens partner that decides WHAT should exist across a set of candidates
> and emits charters, not beads. Entry is free — start at Discovery, Full, or
> Quick directly; there is no mandatory ladder. A Full run launched on a Discovery
> charter starts at RESEARCH (its FRAMING already carried in via
> `sable-charter ingest`). See `PLANNING-MODES-DESIGN.md`.

## 0. Size the ask — propose a tier

Read the ask and **propose** a tier with `AskUserQuestion`; the human confirms
(you recommend, you never lock in):

- **Quick** — well-specified, no unknowns to research, no new interface/contract,
  bounded blast radius (~1–3 beads). e.g. "resize these 3 login cards L→XL".
- **Full** — unknowns to de-risk, architecture decisions to lock, or wide blast
  radius. When in doubt, propose Full.

The human's answer selects the lane below.

## Quick tier — one lightweight pass

```bash
sable-mode set planning --tier quick --fleet columbo
```

This telescopes the interlock's backlog gate to a single approval — you may author
the bead(s) without walking all five substages. Manager spawns and code `git push`
stay blocked (you hand to `/sable-execute` afterward).

1. **Frame it (one strategic line).** State what you'll do in a sentence; ask a
   question only if it's genuinely ambiguous. This is your lane — strategy, not
   spec.
2. **Test spec — run `/columbo --quick "<scope>"` inline.** columbo's process,
   non-interview: it emits the unit+integration delta, biased to *extending
   existing tests*. You do NOT author the test contract yourself — columbo does.
3. **Author the bead(s).** Fold columbo's spec into 1–3 implementation beads, each
   Fresh-Agent-Test-clean (file paths, the unit+integration test spec, acceptance).
   Stand up a bare epic only if there's more than one bead. A pure docs/config ask
   with no code change takes the `[no-test]` path — skip step 2.
4. **One consolidated gate.** Show the human the frame + columbo's test spec + the
   bead(s) in a single review. On approval, record that exact 1–3 bead scope:

   ```bash
   sable-mode handoff approve --beads SABLE-id1,SABLE-id2
   ```

   This is still one human gate; the command makes its result durable and binds
   it to the bead contracts, ready front, unresolved-question set, and current
   integration base. Then tell the operator to run `/sable-execute` (→ Tarzan
   drains it).

**Escalation (one-way only).** If a quick plan hits a real unknown or an
architecture fork mid-flight, say so and offer to bump to Full — never silently
downgrade rigor. Bump with `sable-mode set planning --tier full` and continue in
the full flow below from the substage that matters.

## Full tier — the gated five-substage flow

```bash
sable-mode set planning --tier full --fleet sherlock,columbo,gaudi,victor
```

Writes the **per-repo** mode-state file (`<repo>/.claude/sable/state/mode-state.json`,
resolved from the git common-dir) and initializes `substage=framing`. Because the
mode is scoped to this repo, a planning session here does not collide with an
execution session running in another repo. The interlock now
blocks spawning Optimus/Tarzan/Chuck, blocks code `git push`, and **blocks
populating the backlog (`bd create --parent` / `--graph` / `--file`) until
`substage=decomposition`** (soft — `--force` overrides). The bare epic shell
(`bd create --type=epic`) is allowed now: stand it up early as the planning home
producers attach their review to.

Check position with `sable-mode substage get`. Advance ONLY after the human signs
off on the current deliverable: `sable-mode substage advance`.

### Gate protocol — the planning dossier (every substage)

Each substage's producer drops a JSON deliverable into the per-repo planning
state dir `<repo>/.claude/sable/state/planning/<epic-id>/` (same git-common-dir
resolution as the mode-state file; gitignored): `framing.json` (you),
`research.json` (sherlock), `architecture.json` (gaudi), `test-strategy.json`
(columbo — the story×test matrix), `decomposition.json` (you + victor).
Canonical schemas live in the `bin/sable_dossier_lib.py` docstring.

**Before requesting signoff at ANY gate:**

1. `sable-dossier <epic-id> --highlight <substage>` — assembles every
   deliverable produced so far into one self-contained HTML page and prints
   its path. Missing substages render as "not yet produced"; the highlighted
   section is marked *awaiting signoff*.
2. Publish that file with the **Artifact tool** — use the SAME file path at
   every gate of the run (the dossier redeploys to one stable URL that grows
   section-by-section; keep the favicon constant across gates).
3. Give the user the URL, then ask for signoff via `AskUserQuestion`.
4. On approval for FRAMING through TEST-STRATEGY:
   `sable-mode substage advance`. At DECOMPOSITION, record the final approval
   instead (there is no sixth substage):
   `sable-mode handoff approve --epic <epic-id>`. Never advance or approve on a
   text-only summary — the dossier IS the signoff deliverable.

### Producer non-delivery — bounded fallback

Treat the expected JSON deliverable in the planning state dir as the completion
signal. An idle/completed notification, a claimed bead, or a chat summary without
that file does not count as delivery.

When any producer idles or completes without its deliverable:

1. Inspect the planning state dir and any durable producer output, then explicitly
   resume/pull that producer for the missing deliverable. Make at most **two**
   such pulls.
2. If the deliverable is still absent, spawn exactly **one** fresh producer with
   the same scope, epic id, state-dir path, and output contract. Do not keep
   respawning.
3. If the replacement also fails to deliver, stop pulling agents. Run the
   producer brief's verification commands and checklist yourself, write the
   required deliverable from that evidence, and record the substitution plus
   verification evidence in the epic notes before proceeding to signoff.

This fallback is the same for every producer substage; never wait or pull in an
unbounded loop for a missing verdict.

### FRAMING — owner: you, strategist hat (live with the user)
Most human-intensive, not parallelizable. Run it as a conversation via
`/office-hours` or `/plan-ceo-review`. Produce: user stories, non-goals, success
metric, the narrowest valuable wedge. Stand up the bare epic shell and record the
framing artifact on it. (This is the strategist identity expressed in planning —
same essence that does status/arbitration in execution.)

**Deliverable:** write `framing.json` to the planning state dir — stories with
stable ids (`S1..Sn`, later substages trace back to these), `non_goals`,
`success_metric`, `wedge` — then run the gate protocol.

**Charter ingestion (Discovery composition).** Before generating framing cold,
check whether this epic came from a Discovery charter: run
`sable-charter ingest <epic-id>`. If it returns framing fields (a charter whose
`epic_intention` matches this epic exists), FRAMING is already done — record those
fields as the framing artifact on the epic, map them into `framing.json` in the
planning state dir (same schema as the cold path), and skip straight ahead with
`sable-mode substage set research`. Only generate framing as above when ingest
returns nothing (exits nonzero). See PLANNING-MODES-DESIGN.md for the
Discovery→Full seam.

### RESEARCH — owner: sherlock subagent (greenfield mode); fallback: `/deep-research`
Prior art, domain pitfalls, unknowns to de-risk. Spawn the **sherlock** named
subagent with the research scope in the spawn prompt (e.g. "scope: --research
'<topic>'") and `run_in_background: true` — producer spawns are ALWAYS
background so the conversation stays free while they work; you are notified on
completion. The interlock allows producer subagents in planning mode. Surface
findings to the user.

**Deliverable:** include the planning state dir + epic id in the spawn prompt
and instruct sherlock to write `research.json` there alongside its usual
output; then run the gate protocol.

### ARCHITECTURE — owner: the /gaudi skill, run inline (`/gaudi --epic <id>`)
Lock interface contracts, system-design tradeoffs, smell risks. Gaudi is a
SKILL, not a subagent — it runs in your own conversation. It appends the locked
decisions to the epic's notes.

**Deliverable:** gaudi's epic mode also writes `architecture.json` to the
planning state dir (it detects the dir itself); then run the gate protocol.

### TEST-STRATEGY — owner: columbo subagent (`--epic` in the spawn prompt)
Lock the test contract: boundary cases, failure modes, the unit+integration
matrix per story. Spawn the **columbo** named subagent; it appends the locked
test architecture to the epic.

**Deliverable:** include the planning state dir in the spawn prompt and
instruct columbo to read `framing.json` (story ids — the traceability spine)
and write `test-strategy.json`: the story×test matrix with per-case layer tags
and gap flags. This section is the centerpiece of the dossier the user reviews
at this gate; then run the gate protocol.

### DECOMPOSITION — owner: you + a victor subagent
The interlock now unblocks backlog population. Author the implementation children
under the epic — each tracing to a story + acceptance scenario, passing the Fresh
Agent Test (file paths, unit+integration test spec, fingerprint + verify
command). Spawn **victor** for a freshness pass, then run the post-batch-create
verification: `bd dep tree <epic-id>` (edges match intent), `bd ready` (children
that should be blocked are NOT ready), and `bd swarm validate <epic-id>`.

**Every child's description MUST carry a `## File footprint` section** (SABLE-jd5fj.6):
a comma-separated list of the files/paths the bead will touch, planner-declared —
not left for a worker to infer. This is a scheduling constraint, not documentation:
`hooks/multi-manager/pre-dispatch-overlap.sh` (and `sable-spawn-worker`'s own
governance) DENY dispatching a bead whose declared footprint overlaps a
DIFFERENT in-progress bead's footprint. The two outs at dispatch time are wait,
or an explicit `Serialize-with: <bead-id>` line that tags both merges
serialize-together for Chuck. Decompose with this in mind: children whose
footprints are expected to overlap (shared files, sequential edits to the same
module) should either be scoped narrower to avoid the overlap, or you should
flag the expected serialization in the epic notes so the dispatching manager
isn't surprised by the constraint. Entries may be extension-less (e.g.
`bin/sable-spawn-worker`) — the footprint section is parsed as a dedicated
field, not the generic file-extension regex used as a fallback for older beads.

**Deliverable:** write `decomposition.json` to the planning state dir — the
children (id/title/type/deps/ready-state), the `bd swarm validate` verdict, and
victor's summary line — then run the gate protocol for the final signoff. The
approval command strictly validates all five dossier inputs, re-runs
`bd swarm validate --json`, proves a ready front and zero unresolved questions,
and records their hashes in the atomic mode state.

## Open-questions ledger

Any ambiguity surfacing in ANY substage (either tier) becomes a bead labelled
`open-question` addressed to the user. You may not hand off to `/sable-execute`
while open questions remain — draining them is what guarantees execution doesn't
need the human.

## Hand off to execution

When the backlog is authored and the tier-appropriate
`sable-mode handoff approve` command succeeds, tell the operator to run
`/sable-execute`. Do not hand off merely because the prose review finished: the
durable receipt is the mechanical boundary. Don't launch managers from planning
mode — the interlock blocks it, correctly.

## Deploying changes to this flow
Orchestration hooks/skills run from INSTALLED copies in `~/.claude/`. After editing
the SABLE repo (this skill, the interlock, `sable-mode`), run `install.sh` to
re-sync before changes take effect live.
