---
name: prp
description: Generate a Product Requirements Prompt for engineering handoff. Needs an approved PRD. Sensors, link validation, and eval gates.
user_invocable: true
---

Generate a PRP. Follow guides/pipeline.md for retry, approval, and publish.

Source PRD: if user passes a path, use it. Else pick the most recent in .claude/runtime/outputs/pm/prd/. None found, abort. Tell user to run /product-manager:prd first. hooks/pre-prp-check.sh blocks if the PRD lacks the approved marker.

Compute feature_id from the source PRD filename (basename without .md). Save the PRP to .claude/runtime/outputs/pm/prp/{feature_id}.md so it matches.

Before generating, write the phase start marker:

```
.claude/runtime/outputs/pm/.markers/{feature_id}.prp-generate.start
```

Content: `{"timestamp": "<ISO-8601 UTC now>", "session_id": ""}`

Read:
- the source PRD
- guides/prp-guidelines.md
- guides/writing-style.md
- guides/templates/prp.md
- guides/pipeline.md
- guides/examples/good-prp-example.md
- .claude/shared/context-strategy.md, pick the right tier when exploring target repos

Explore target repos. Ask user for repo paths if not provided. Run `.claude/scripts/context-tools.sh {repo}` once, then per `context-strategy.md` § `/product-manager:prp`:
1. semble search per PRD capability → files touched with file:line. semble find-related on best match → Context patterns.
2. repowise context/why on touched modules → gotchas. context7 for each external lib → external docs links.
3. atomize skill present → PRD atoms become `Success criteria (verifiable)`, one per atom.
4. Cached graphify graph / repomix pack if present. Fall back to Grep + Read.

Capture file:line. Never invent paths. Large repo with no semble/repowise and no cache → suggest `/context:graph {repo}`, don't auto-build.

Graph, only when `python3 .claude/scripts/hk-config.py get graph` not `off` (`.claude/shared/graph-engineering.md` § `/product-manager:prp`): write each success criterion as `- [ ] REQ-001: ...` (stable ids, never renumber; atomize ids when atoms.json exists), then `python3 .claude/scripts/trace.py init {feature_id} --prp {prp path}` (or `--atoms`).

Save to .claude/runtime/outputs/pm/prp/{feature_id}.md.

Sensors: sensors/prp-structure.md, sensors/prp-context-quality.md, sensors/prp-links.md.

Evals: evals/prp-quality.md, evals/prp-context-readiness.md.

After save reply: PRP saved at {path}. Score: {N}/10. Ready for handoff.
