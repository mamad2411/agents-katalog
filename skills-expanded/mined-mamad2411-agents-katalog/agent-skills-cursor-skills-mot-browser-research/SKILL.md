# MOT Browser Research

Use when `@Browser` is attached or the user wants web research for this repo.

## Scope

- Project: `/home/aimsgroupuol/AIMSgeneral/Gyanateet_tracking`
- Goal: **surgical tool MOT** on CholecTrack20 (boxes + track IDs), not robot policies
- Stay **GOT-JEPA + OccuSolver** unless user explicitly pivots

## Research loop

1. **Frame the question** — MOT detection, association, smoke/occlusion, SSL, or infra (Spark vs Aire)?
2. **Search** — Use web search or browser MCP. Prefer primary sources: arXiv, GitHub, dataset pages, [Seeing Through Smoke](https://smoke.art-ai.me/).
3. **Map to repo** — Tie findings to stages (`core_app/mot/`), configs (`configs/train_mot/dinov2/`), eval (`scripts/eval_mot_hota.py`).
4. **Strategic verdict** — Short answer first; table comparing paper vs this repo; recommend adopt / optional / reject.
5. **Cite everything** — Markdown links for every claim; end with Sources list.

## Direction guardrails

| Topic | Verdict |
|-------|---------|
| GOT-JEPA (tracking weights ω) | **Primary** — `core_app/mot/jepa.py` |
| VLA-JEPA / robot policies | **Different problem** — manipulation actions, not MOT |
| Pixel desmoking (Seeing Through Smoke) | **Optional ablation** — not core strategy |
| V-JEPA / Cholec_Vjepa-2 | **Complementary SSL** — not a replacement for per-track ω prediction |
| Temporal difference vision | **Explore only** — must connect to per-track predictor or visibility gating |

## Key references to check online

- [GOT-JEPA](https://arxiv.org/abs/2602.14771) — paper lineage for Stage 2
- [CholecTrack20](https://github.com/CAMMA-public/cholectrack20) — eval dataset
- [Seeing Through Smoke](https://smoke.art-ai.me/) — smoke stratification context
- CT20 baselines: Deformable-DETR ~38% mAP, YOLOv7 ~56% mAP (detection gap vs our ~2–3%)

## Leeds Aire (when asked)

- **Good on Aire:** HP sweeps, multi-seed, parallel SSL, eval arrays, 6+ L40S DDP
- **Keep on Spark (GB10):** memory-heavy Stage 4 full, finishing single-GPU baseline, CoTracker/OccuSolver probes

## Output template

```markdown
## Short answer
[One paragraph]

## Fit for Gyanateet_tracking
| | Paper / approach | This repo |
|---|---|---|

## Recommendation
- Adopt / optional / reject with next concrete step

## Sources
- [Title](url)
```

## Repo context files

- `AGENTS.md` — training status, blockers, preferences
- `agent_docs/cursor_repo_understanding.md` — strategic assessments
- `agent_docs/cursor_explore_mot_training_pipeline.md` — stage map
