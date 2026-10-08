---
name: create-specification
description: Drive end-to-end USDL Spec authoring across all four Sections top-down, or one Section at a time. Spawns the matching section-authoring Agent, shows the diff for confirmation, and proceeds only after confirm. Triggers on "create spec", "spec from scratch", "author all sections", "new USDL specification", and the `--section` argument.
user-invocable: true
---

# /create-specification

The Orchestration Command for USDL Spec authoring. Realises
`ifc.skill.create-specification`, governed by
`com.flow.orchestrate-in-create-specification`, and enacts use case
`beh.orchestrate-spec-creation`.

This file is description-only. Every non-trivial step is delegated to the
three bundled scripts under `scripts/`. Per
`con.no-implementation-code-in-skill-md` the body of this SKILL.md carries no
executable code blocks.

## Invocation

```
/create-specification [--section behaviour|topology|interfaces|composition]
```

- No argument — **full mode**. Walks behaviour, then topology, then
  interfaces, then composition, in that order. Each next Section starts only
  once the previous Section's diff is confirmed by the Spec author.
- `--section <name>` — **single-section mode**. Authors exactly the one named
  Section. No other Section is touched, even if the author rejects the diff
  many times.

## Sequential section creation rule

Per `beh.rule.sequential-section-creation`:

> When the Orchestration Command is invoked in full mode or for multiple
> Sections, the system shall author Sections top-down one at a time
> (behaviour, then topology, then interfaces, then composition), and shall
> start the next Section only after the Spec author has confirmed the
> previous Section's diff.

Confirmation is binary: the author either confirms or rejects. Rejection of
Section N never advances to Section N+1; the system re-spawns the matching
Agent for Section N with the author's amendment notes attached.

## Per-Section flow

For every Section the Orchestration Command runs the same loop:

1. **Explain.** State what the next Section needs from the Spec author —
   in plain prose, not a form — and what higher Sections it will read as
   authoritative input.
2. **Clarify.** Ask any clarifying questions the author should answer
   *before* the section-authoring Agent is spawned. This is the parent's
   conversation; the Agent will conduct its own interview later in
   isolation.
3. **Spawn.** Invoke `scripts/agent-spawner/spawn.py` to build the spawn
   payload (higher Section files plus amendment notes) and hand off to the
   matching section-authoring Agent
   (`top.agent.{behaviour,topology,interfaces,composition}-author`). Per
   `inv.agent-context-isolation` the Agent runs in its own context window;
   only a summary diff and a structured status return to this conversation.
   Per `beh.rule.agent-preloads-higher-sections` the payload includes only
   Section files matching a Skill the target Agent has preloaded.
4. **Review.** Hand the Agent's summary diff to
   `scripts/diff-presenter/present.py`, which renders every new, modified,
   and deleted Element id plus every changed cross-reference, then prompts
   the author for confirm-or-reject.
5. **Confirm.** On confirm, the Section file is committed and the loop
   either advances to the next Section (full mode) or terminates
   (single-section mode). On reject, the Orchestration Command captures the
   author's amendment notes and re-spawns the same Agent with those notes
   attached; advancement is gated on confirmation, not validation alone.

`scripts/section-runner/run.py` owns the state machine that drives this
loop top-down across Sections and handles the single-section short-circuit.

## Single-section mode

When invoked with `--section <name>`:

- Pre-check: `behaviour` requires no higher Section; `topology` requires a
  valid `behavior.xml`; `interfaces` requires valid `behavior.xml` and
  `topology.xml`; `composition` requires valid `behavior.xml`,
  `topology.xml`, and `interfaces.xml`.
- The runner never reaches Sections lower than the requested one. If the
  author rejects the diff, the runner re-spawns the same Agent indefinitely
  for the same Section; it never spills over to the next Section.

## Failure modes

Each condition is declared on `ifc.skill.create-specification`. The
Orchestration Command's response is fixed; the bundled scripts surface the
data and this command relays it to the author.

- **`missing-higher-section`** — a Section file required as authoritative
  input for the requested Section is absent or does not pass `usdl
  validate`. The Orchestration Command fails fast, names the missing or
  invalid Section, surfaces the Bin diagnostics, and refuses to spawn the
  section-authoring Agent. No Section file is created or modified. Detected
  by `scripts/agent-spawner/spawn.py` before the spawn payload is handed
  off.
- **`agent-spawn-failure`** — the section-authoring Agent could not be
  started or terminated abnormally before returning a summary diff. The
  Orchestration Command fails fast, surfaces the diagnostics returned by
  the host's spawn primitive, and commits nothing. The author may rerun
  `/create-specification` once the host's agent runtime is healthy.
- **`user-rejects-section`** — the Spec author rejected the diff for the
  current Section. The Orchestration Command retries with backoff: it asks
  the author what to change, captures the amendment notes via
  `scripts/diff-presenter/present.py`, and re-spawns the same Agent with
  those notes attached. The next Section does not start until this Section
  is re-confirmed; in single-section mode, no other Section is ever
  touched.
- **`validation-failure`** — the Agent returned a diff but the Section file
  it produced does not pass `usdl validate`. The Orchestration Command
  fails fast, surfaces the Bin diagnostics, and commits nothing. The author
  may rerun the Section pass; the runner will re-spawn the Agent with the
  diagnostics included in the amendment notes.

## Components and call-flow

The four components of `top.skill.create-specification`
(`cmp.orchestrator.skill-md`, `cmp.orchestrator.section-runner`,
`cmp.orchestrator.agent-spawner`, `cmp.orchestrator.diff-presenter`) are
called in the order declared by
`com.flow.orchestrate-in-create-specification`:

1. `cmp.orchestrator.skill-md` — this file. Triggers the host to enter the
   orchestration flow and points to the bundled scripts.
2. `cmp.orchestrator.section-runner` — `scripts/section-runner/run.py`.
   Drives the prompt → spawn → review → confirm → next state machine.
3. `cmp.orchestrator.agent-spawner` — `scripts/agent-spawner/spawn.py`.
   Builds the spawn payload, enforces chain-of-trust, hands off to the
   host's spawn primitive.
4. `cmp.orchestrator.diff-presenter` — `scripts/diff-presenter/present.py`.
   Renders the summary diff and captures the confirm-or-reject signal.

## See also

- `agents/behaviour-author/AGENT.md`
- `agents/topology-author/AGENT.md`
- `agents/interfaces-author/AGENT.md`
- `agents/composition-author/AGENT.md`
- `skills/usdl-bin/SKILL.md`
- `commands/create-specification/scripts/section-runner/run.py`
- `commands/create-specification/scripts/agent-spawner/spawn.py`
- `commands/create-specification/scripts/diff-presenter/present.py`
- `commands/create-specification/scripts/_lib/payload.py`
