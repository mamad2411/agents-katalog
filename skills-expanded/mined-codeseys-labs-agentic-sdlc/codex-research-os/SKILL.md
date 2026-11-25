---
name: codex-research-os
description: Bootstrap and operate a Codex-native autonomous research operating system in a repository. Use when a user asks to create, install, formalize, package, reuse, or run a disciplined research team setup with specialist agents, persistent memory, claim ledgers, experiment tracking, literature discovery, ablation workflows, strict review gates, greenfield/brownfield research loops, reusable workflows, or continuation state across projects/repos.
---

# Codex Research OS

## Overview

Use this skill to install or run a portable research organization inside a repo: a director, specialists, persistent ledgers, workflows, review gates, and scripts. It is deliberately repo-native and does not depend on Helios or any external orchestrator.

## Decision Flow

1. If the repo lacks the research OS, install it with `scripts/install_research_os.py`.
2. If the repo already has it, read `research/README.md`, `research/status.md`, and `research/state/next_action.md`, then run one loop.
3. For existing code/papers/benchmarks, use `research/workflows/brownfield_loop.md`.
4. For a broad new research area, use `research/workflows/greenfield_loop.md`.
5. Before final synthesis, run `make validate-claims`, `make validate-experiments`, and `make review-gates`.

## Install

From the bundle root:

```bash
mise run research-os:install -- --target /path/to/repo --project-name "Project Name"
```

Default behavior is conservative:
- create missing files and directories;
- skip existing files;
- do not overwrite project-specific instructions;
- leave historical docs in place;
- create a generic OS layer that future agents adapt.

`--target` is required and never defaults to the current directory, so an argument-less run
refuses instead of scaffolding the whole OS into whatever repo invoked it.

Use `--force` only when intentionally replacing the generated OS files. Use `--dry-run` to preview.

After install, run in the target repo:

```bash
make status
make validate-agents
make validate-claims
make validate-experiments
make review-gates
```

## Operate

Always run one meaningful unit of work per loop. The director chooses the unit, assigns a specialist, validates output, updates memory, and ends with a concrete next action.

Role boundaries matter:
- literature scout maps prior art but does not declare novelty;
- theorist proposes hypotheses but does not approve them;
- experimentalist logs evidence but does not declare publication readiness;
- adversarial reviewer attacks claims and does not fix them;
- synthesis writer summarizes only validated evidence;
- research director coordinates and enforces gates.

Read `references/operating-model.md` when designing or modifying the OS. Read `references/agent-roster.md` when updating roles or agent prompts.

Two refinement references describe designed-not-built changes to the generated layer. Read them
when redesigning the claim gate or when running a bounded self-improving loop; both state
explicitly which parts ship today and which do not:

- `references/claim-obligations.md` — the shipped review gate substring-matches free text the
  claim's own author writes, so an author's honest caveats satisfy it. Typed obligations that
  resolve against independent review records replace that check, with revision matching so
  editing a reviewed claim auto-demotes it.
- `references/bounded-lab-loop.md` — the three-owner split (human-owned program, digest-frozen
  harness, probe workspace), the two-plane autonomy boundary, the exploration reserve and stall
  rule that fix pure metric ratcheting, and the seven invariants.

## Required Invariants

- No meaningful untracked claims: use `research/claims/claims.yaml`.
- No improvement claim without a baseline or explicit baseline plan.
- No novelty claim without novelty review.
- No empirical claim promotion without replication review.
- No important synthesis without adversarial review.
- Negative results stay in memory and experiment logs.
- Every loop updates `research/state/next_action.md`.
- Provider-neutral generated roles omit static `model` and `model_reasoning_effort` pins and
  never dispatch themselves. Before spawn, the conductor supplies one conductor-supplied certified
  `RuntimeAssignment` with a certified exact model ID. Its `resolution_state` must be `resolved`.
  Exact model/effort request injection is mandatory and immutable. Provider/model source may be
  unavailable only for an unambiguous exact-ID mapping backed by immutable request/model evidence;
  effective effort/context readback may honestly be unavailable, and requested values never become
  readback. Requested, inherited, unresolved, or incomplete assignments stop before spawn and
  return one `SeedProposal`. The selected host or launcher must inject the exact requested model
  and effort; if it cannot inject both, return one `SeedProposal`, not a dispatch. Prompt prose
  does not enforce a Codex model or effort. Reject host-default policy and unverified aliases.
- The Research Director is Seeds-read-only. It may inspect only through the exact
  `Seeds(<target>, ...)` launcher contract in `agentic-sdlc`, and it emits exactly
  one typed `SeedProposal` for conductor triage; it never creates, claims, updates, closes,
  syncs, or dispositions Seeds.

## External Research Doctrine

A research run is a cost, so run live external research only when
external evidence is load-bearing for the decision at hand; otherwise reason from the
repository, existing ledgers, and prior notes. When a run is warranted, return a versioned
research record carrying, at minimum:

- sources: each cited item with its version, date, or URL so it can be re-fetched;
- claims: what the evidence supports, written into `research/claims/claims.yaml`;
- counterevidence: findings that weaken or contradict the claims;
- uncertainty: what remains unknown and how it could be resolved;
- decision-impact: how the evidence changes (or fails to change) the pending decision;
- next-action: the single cheapest decisive follow-up.

Work that outlives the session becomes exactly one typed `SeedProposal` for conductor
triage; the research OS proposes durable work and never mutates any queue. Sources and
claims are versioned so a later run can tell fresh evidence from stale echoes.
