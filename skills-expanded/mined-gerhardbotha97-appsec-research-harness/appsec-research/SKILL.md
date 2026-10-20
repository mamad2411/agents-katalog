---
name: appsec-research
description: Multi-agent application security research harness. Use for full source-code security engagements, taint mapping, vulnerability hunting, precision triage, PoC validation, and advisory writing.
license: MIT
compatibility: opencode
metadata:
  audience: security-researchers
  workflow: application-security-research
  agent-count: "17"
---

# Appsec Research

Use `appsec-research-orchestrator` for a full engagement. Provide `repo` and `name`; optionally provide `stack`, `docker`, `scope`, and `commit`. Results are written under `TARGET-{name}/`.

```text
@appsec-research-orchestrator New engagement: target Gogs. Repo: https://github.com/gogs/gogs.git
```

The orchestrator owns phase order, gates, recall mode, candidate format, and artifact routing. Specialist prompts already contain their class methodology; do not paste this skill body or full prior artifacts into Task messages.

Core flow: environment and recon -> supply-chain inventory -> impact-scored taint mapping -> five consolidated hunters -> precision -> conditional chain/gap review -> PoC validation -> High/Critical advisory.

Cost controls are mandatory:

- Dispatch only consolidated hunters with plausible High/Critical paths: execution, access control, data boundary, state integrity, and trust/crypto.
- Run pass 1 for relevant hunters, pass 2 only for unsaturated coverage, and pass 3 only when pass 2 is at least 20% novel.
- Pass compact file paths, candidate IDs, and per-hunter steering rows. Keep raw scanner output and unrelated artifacts off-context.
- Skip downstream agents when their documented input gate is empty.
- Do not emit standalone Medium/Low/Informational findings. Keep a lower-impact primitive only in a concrete High/Critical chain.
- Recall over-reports inside that impact boundary; precision verifies. An empty verified set is valid.

Individual agents remain available as `appsec-research-<agent-id>` for targeted work.
