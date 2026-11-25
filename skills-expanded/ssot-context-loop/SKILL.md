---
name: ssot-context-loop
description: "When the user wants a governed, persistent product marketing source of truth, to set up an SSOT, scan field signals for drift, audit AI output, or manage approval gates for positioning changes. Use commands such as /setup, /scan, /confirm, /propose, /approve, /stale, /state, /brief, /manifest, and /audit-output. For lightweight bootstrap context, see product-marketing-context. This skill governs ongoing PMM knowledge and requires human approval for core changes."
metadata:
  version: 1.1.0
---

# SSOT Context Loop

Maintain a governed PMM knowledge system for one client or project. It separates
approved strategy from living field intelligence, detects drift, records decisions,
and never changes canonical strategy without human approval.

## When to Use

Use this skill to create or maintain `ssot/<client-slug>/`, scan new field or market
inputs, review drift, audit generated assets, or manage canon decisions. Load
`references/ssot-spec.md` before acting. It is the detailed operational
specification for the file schemas, commands, signal model, gates, and templates.

## Relationship to Other Skills

- `product-marketing-context` establishes understanding and assembles proposals at
  `.agents/product-marketing-context.md`. It remains separate. If no SSOT exists,
  it may serve as context. If an SSOT exists for the active client or project, the
  SSOT is more authoritative for claims it covers.
- Never automatically overwrite `.agents/product-marketing-context.md`.
- `positioning-strategy` may develop strategy, but canon changes enter this SSOT
  only through its evidence and approval gates.
- `messaging-framework` should source differentiators from core and persona
  messaging from SSOT persona research. Do not create either standalone.
- `icp-and-buyer-personas` and `customer-research` can inform persona and living evidence
  files. `competitor-profiling` can inform competitive and market evidence.
- `sales-enablement`, `marketing-copy`, `launch-strategy`, `market-entry-orchestration`, and
  `launch-readiness-check` can read mapped SSOT files to keep assets aligned.
- `events` can adapt approved messages for event context and routes material
  narrative conflicts through this SSOT's evidence and human-approval gates.
- `output-quality-check` checks a skill's artifact against that skill's declared
  requirements. It does not audit canon consistency or change this SSOT.
- Use repo-level `manifest.yaml` in the user's project to map skills or agents to
  the SSOT files they read. Start with `/manifest` to create or update it.
- The SSOT is upstream context. Other skills do not call this skill to decide
  canon, and this skill does not depend on their outputs as authority by default.

## Operating Rules

- Separate facts, which are recorded events, from opinions, which are strategy.
  Document opinions and ground them in facts.
- Never invent a claim. Cite the quote or data, speaker and role, account type,
  system, date, and outcome or cost when known.
- Every content line in every canonical SSOT file must end with exactly one
  evidence tag: `[C]`, `[A]`, or `[G]`. `[C]` is cited, `[A]` is assumed, and `[G]`
  is a gap. Apply decision-specific readiness: hold consequential unsupported
  decisions, continue independent work, and retain weak-evidence hypotheses
  with the evidence needed to resolve them. Approval remains separate.
- Core holds its existing strategy domains; scoped approved decisions/references
  cover topics without a core home, per the spec. Initial specialist proposals
  may use supplied evidence before canon exists. Existing canon remains authoritative.
- Give each claim one canonical home and reference dependencies. Update only
  explicitly approved affected sections, which may span files. Record uncertain
  placement in `09-iteration.md`.
- Field signals inform the canon, but do not automatically change it. Every
  finding gets one proposed verdict and waits at the required human gate.
- Never write to core without Gate 2 approval. Never edit or delete `comms/` input.
  Deprecate a section in place and name its replacement instead of deleting it.
- Follow the reference's file schema, staleness thresholds, taxonomy, and command
  outputs. `state.md` is written only by the reconciler, never by hand.
- Output without em dashes. Keep sentences to two lines at most. Lead bullets with
  outcomes and remove filler.

## Command Routing

Route explicit commands to the matching workflow in `references/ssot-spec.md`:

- `/setup <client>` creates the baseline SSOT from supplied source documents.
- `/scan <client>` archives new inputs, classifies signals, and reports drift.
- `/confirm <IDs>` and `/reject <ID> <reason>` perform Gate 1 decisions.
- `/propose` prepares confirmed changes and impact analysis for Gate 2.
- `/approve <IDs>` and `/revise <ID> <notes>` handle Gate 2 decisions.
- `/stale`, `/state`, `/brief`, `/manifest`, and `/audit-output` produce their
  specified reports or project files.

For reviewed context proposals, read `../_shared/context-establishment.md` and
follow the spec's intake path. Preserve provenance and incoming IDs. Baselines
wait at Gate 2; existing-context updates pass Gate 1 then Gate 2. Evidence readiness
and human approval are separate; partial approval does not settle held decisions.
For unstructured goal/material intake without a command, route to PMC to establish
understanding. Resolve only missing scope. Never infer approval from silence.

## Output Behavior

Write or propose files in the user's working project, never inside this skill or
the PMM-Skills repository. Keep raw uploaded material in the project's immutable
`ssot/<client-slug>/comms/` directory. Respect the workflow's stop points.

After each workflow-authorized file creation or change, commit and push the
generated SSOT output to the project's GitHub-backed repository. GitHub is the
durable source of truth, not the chat. Preserve the required stop points: `/scan`
stops at Gate 1, and proposed changes wait at Gate 2. Never modify core or commit
a core change before explicit human approval at Gate 2.

For Gate 2 approval, return each ready-to-commit file in full, one code block per
file with its path as the heading. Include the decision record for every core
change, regenerated `state.md`, and a commit message. Commit and push the approved
files after approval.

For `/scan`, return the drift report, three one-line priority findings, and
"Needs your call" questions, then stop at Gate 1. For `/brief`, keep the team
summary to ten lines or fewer and omit internal gate details.
