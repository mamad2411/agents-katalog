---
name: debugging-observability
description: Debug production issues using observability data. Use when tracing
  a user-visible problem from production signals.
metadata:
  tags: debugging, observability
---

# Observability-Driven Debugging

## Use this skill when
- Finding which dependency or path is slow
- Correlating errors to releases or deploys
- Using traces, metrics, and logs together

## Do not use this skill when
- Code-only debugging without production data
- Hypothesis-free guessing

## Instructions
1. Start from the symptom: which SLO or user story broke.
2. Correlate timing: deploys, traffic spikes, config changes.
3. Use traces to find the slow hop; logs for the error context.
4. Check segmentation: version, region, tenant, device.
5. Rule out dependencies: latency to DB/cache/upstreams.
6. Form a hypothesis with evidence; verify with next step.
7. Document and synthesize findings to code actions.

## Checklist
- Claims tied to evidence
- Deploys correlated
- Distribution checked, not just average

## Output Format
- Symptom | timeline | evidence | root hypothesis | next experiment

## Common Mistakes
- Chasing the average instead of the distribution
- Ignoring deploy correlation
- Guessing without telemetry
