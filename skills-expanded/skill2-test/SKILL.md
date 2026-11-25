---
name: skill2-test
description: "Use when checking whether a skill activates, avoids false activation, improves outcomes, or works in an isolated agent environment."
---

# Test Agent Skills

Measure behavior without inheriting current chat, global memory, or unrelated Skills.

## Ownership

- Test owns live activation, outcome, routing, and baseline evidence.
- Audit owns static structure and trigger-overlap review.
- Create owns Skill changes; Test never rewrites a failing Skill automatically.

## Layers

| Layer | Installed Skills | Measures |
| --- | --- | --- |
| Target-only | Target Skill only | Activation, outcome, baseline uplift |
| Pack | Candidate sibling Skills | Routing and false activation |

Use target-only for core outcomes. Use pack for adjacent and unrelated routing cases.

## Cases

- Core positive: target should activate and produce required artifact or answer.
- Paraphrase: same intent, different wording.
- Adjacent: sibling should own request.
- Unrelated: no package Skill should activate.
- Assertions: inspect files, output, commands, or explicit events.

Default one trial. Add repetitions only for known nondeterminism or regression confidence.

## Isolation

- Fresh session, temporary home, temporary workspace.
- Install only layer-required Skills.
- Minimal authentication/configuration; no user memory or chat history.
- Guard host-home reads and writes.
- Adapter owns harness-specific install and event parsing.
- Save raw events, final output, workspace, version, and Skill hash locally.

## Verdicts

- `pass`: activation and outcome assertions pass.
- `fail`: deterministic assertion fails.
- `inconclusive`: runner or evidence cannot support claim.
- Baseline also passes: no demonstrated deterministic uplift.
- Exact isolated `SKILL.md` read is medium-confidence activation; explicit activation event is high confidence.

Fake runner tests validate adapter plumbing, not provider behavior. Never claim unrun results.

```bash
uv run --script <skill-dir>/scripts/run -- test skills/<name> --agent <agent> --cases cases/<name>.yaml --baseline
uv run --script <skill-dir>/scripts/run -- test skills/<name> --agent <agent> --cases cases/<name>.yaml --pack
```
