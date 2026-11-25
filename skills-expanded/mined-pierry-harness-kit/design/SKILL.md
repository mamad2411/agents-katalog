---
name: design
description: Design any system from scratch into a rigorous System Design Doc. Generic fallback when no topic-specific playbook fits. Sensors and evals gate.
user_invocable: true
---

Produce a System Design Doc for an arbitrary system. Follow guides/pipeline.md for retry and approval.

Ask once if missing: system in 1-2 sentences, scale target (users / QPS / data / latency SLO),
internal vs web-scale, known constraints.

**Route first.** If the problem matches a topic playbook under
`.claude/agents/system-architect/skills/{topic}/SKILL.md` (e.g. search-engine), use that skill
instead, it carries a canned reference architecture. This generic skill is the fallback when no
topic fits.

Compute feature_id = {YYYY-MM-DD}-{slug}.

Read:
- guides/design-method.md  (the method and the canon)
- guides/writing-style.md
- guides/templates/system-design.md
- guides/pipeline.md
- guides/examples/good-system-design-example.md
- .claude/shared/context-strategy.md § `/system-design:design`

Existing system → ground current architecture first with semble + repowise context (probe `.claude/scripts/context-tools.sh {repo}`). Greenfield → skip.

Generate the SDD: walk all 13 stages of the template. Every non-functional claim carries a number.
Show back-of-envelope math. Name a trade-off per major choice. Mermaid for flow and architecture.

Save to .claude/runtime/outputs/architect/design/{feature_id}.md.

Sensors: sensors/design-structure.md, sensors/design-rigor.md.
Evals: evals/design-quality.md.

After save reply: Design saved at {path}. Score: {N}/10. Then offer /system-design:review.
