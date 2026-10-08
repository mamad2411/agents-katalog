---
name: yolo-roadmap
description: Use when the user has a large or fuzzy goal that should be decomposed into several features. Produces N feature briefs (optionally sharing a milestone label) — a one-time act that returns briefs, not a container. Triggers on "break this epic into features", "plan a milestone", "decompose this".
---

# yolo-roadmap

Turn one big goal into several atomic feature briefs. There is no "release" container — just briefs, optionally tagged with a shared `milestone`.

## Procedure
1. Clarify the big goal and its boundary (what's out of scope). Optionally invoke yolo-research for codebase context.
2. Decompose into independent features, each shippable on its own. Note any cross-feature `depends_on` (honored by the model; there is no DAG machine).
3. For each feature, draft `workspace/features/<slug>/brief.md` from `.claude/yolo/templates/brief.md` — set `goal`, `success_criteria`, and a shared `milestone:` value if they ship as a set.
4. Present the proposed feature list for approval BEFORE creating the briefs — the plan-gate analogue for a roadmap; no billed code work happens here (`.claude/yolo/conventions.md` *The two gates*). Skip only if the user pre-consented.
5. On approval, write and commit each brief (`yolo: brief <slug>`). Each is later picked up by yolo-feature.

## Constraints
- You only create briefs (status "planned"). You do not branch, plan, or execute — that is yolo-feature, per feature.
- No container, no lifecycle, no status field. Grouping is the `milestone:` label only.
- Run decomposition/analysis at the `agents.roadmap` tier from `workspace/config.yaml`.
