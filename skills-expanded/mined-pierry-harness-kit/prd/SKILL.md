---
name: prd
description: Generate a Product Requirements Document for an team squad. Business-facing artifact. Sensors and evals gate.
user_invocable: true
---

Generate a PRD. Follow guides/pipeline.md for retry, approval, and publish.

Ask once if missing: squad, problem in 1-2 sentences, customers, hypothesis, bet link, stage.

Compute feature_id = {YYYY-MM-DD}-{squad}-{slug}. Before generating, write the phase start marker:

```
.claude/runtime/outputs/pm/.markers/{feature_id}.prd-generate.start
```

Content: `{"timestamp": "<ISO-8601 UTC now>", "session_id": ""}`

Read:
- guides/product-guidelines.md
- guides/prd-guidelines.md
- guides/writing-style.md
- guides/templates/prd.md
- guides/pipeline.md
- guides/examples/good-prd-example.md
- .claude/shared/context-strategy.md § `/product-manager:prd`

Optional tools (`.claude/scripts/context-tools.sh`): memoria skill → prior decisions on same problem, cite in Evidence or Risks. atomize skill → atoms from problem + hypothesis, feed Success Metrics, save `.claude/runtime/outputs/pm/prd/{feature_id}.atoms.json`. Absent → skip, no block.

Save to .claude/runtime/outputs/pm/prd/{feature_id}.md.

Sensors: sensors/prd-structure.md, sensors/prd-acceptance-criteria.md.

Evals: evals/prd-quality.md, evals/prd-readiness.md.

After save reply: PRD saved at {path}. Score: {N}/10.
