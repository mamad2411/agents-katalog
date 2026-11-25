---
name: forest-autonomous-research
description: Continue FOREST scientific research through evidence driven goals, plans, graph changes, execution, and recovery.
---

# FOREST autonomous research

Use this skill for research planning, execution, analysis, review, and recovery. The runtime also assembles the canonical shared policy from `research/agents/policy.py` for every research capable role.

Research is an evolving process. Update goals, hypotheses, plans, graph branches, configurations, protocols, candidate choices, interpretations, and manuscripts when evidence warrants it. Keep historical versions and provenance, while continuing from current state. A round boundary, recovered checkpoint, completed node, prior selection, or generated manuscript is not a scientific stop condition. Resume useful work automatically from saved state and inspect relevant history before proposing a repeated experiment.

Do not terminate research based on a cumulative count of agent actions. Execution rounds may checkpoint and continue; scientific completion follows the current goal and observed evidence.

Choose the next action for its information value and scientific relevance. When a method fails, inspect the evidence and alternative branches, then repair, replace, or redirect the method. Treat changed protocols as distinct comparison contexts until a common evaluation establishes comparability.

Perform actual research through the available execution tools. Separate proposed work from completed work; report an experiment, measurement, citation, or validation only when its output was observed. Preserve failures and contrary measurements. Do not make research progress depend on a content digest or a hash gate; use explicit record IDs, revisions, paths, and direct evidence references.

For decision analysis, use [forest-research-judgment](../forest-research-judgment/SKILL.md). For computational studies, use [forest-experimentation](../forest-experimentation/SKILL.md). For manuscript work, use [forest-academic-writing](../forest-academic-writing/SKILL.md). Canonical runtime assembly is implemented in `research/agents/policy.py` and `research/paper/style.py`.
