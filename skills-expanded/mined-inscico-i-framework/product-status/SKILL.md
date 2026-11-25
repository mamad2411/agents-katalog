---
name: product-status
description: Render a read-only dashboard of the Product/ folder — stage/gate completion, risk-burndown state, feature counts by classification and priority, the ranked innovation edge list, and gaps (UVP elements with no feature, features missing acceptance criteria, unclassified features). Use to review progress or spot holes.
allowed-tools: Read, Glob, Grep
---

# /product-status — the dashboard (read-only)

You summarize the whole `Product/` folder at a glance. Never modify files — if you find problems, list them as gaps for the founder to fix with the relevant skill.

## Procedure

1. **Read everything.** The three stage artifacts (and their `gate:` frontmatter), `Product/Features/F*.md` (frontmatter + body), `Product/features-index.md` if present, and `Product/competition.md` if present.

2. **Compute:**
   - **Stage/gate completion** — which of the three gates are passed vs. open (the risk-burndown line).
   - **Feature counts** — total, by `classification`, by `priority` (MoSCoW), by `status`.
   - **Innovation edge list** — innovation features sorted by `innovation_weight` desc, each with its `contributes_to` UVP.
   - **Weight distribution** — are weights spread or clustered?

3. **Run integrity checks** (the high-value part) — validate cross-file consistency and list every violation:
   - **Dangling UVP reference:** a feature's `contributes_to` value that matches no UVP id in `innovation.md`.
   - **UVP orphan:** a UVP element in `innovation.md` with no innovation feature tracing to it.
   - **Classification/weight mismatch:** implementation with weight ≠ 0; innovation with weight 0; innovation missing `contributes_to`.
   - **Thin feature:** missing a user-story clause, or **<3 acceptance criteria**.
   - **Broken dependency:** a `depends_on` id that points to no existing feature.
   - **Portfolio flags:** apply the same thresholds as `/classify` — >40% innovation; and, *only when there are ≥3 innovation features*, innovation weight span <30 points (skip the spread check below that count).
   - **Cherry-picked matrix:** if `competition.md` exists and the "Us" column is ✓ on every row, flag it — a credible comparison has ≥1 row where a rival matches or beats us.
   - **Unverified competitor claims:** if `competition.md` exists, count cells marked `?` and surface them as items to verify (with the snapshot date).

4. **Render** a concise dashboard — a risk-burndown header, a counts table, the ranked edge list, and a clearly separated **Gaps / next actions** section that names which skill fixes each gap (`/feature`, `/classify`, `/innovate`).
