# Mini Revvy Demo

Node.js + Express server with a vanilla HTML/CSS/JS frontend and a **Python FastAPI ML sidecar**.

## Run

```bash
# Full stack (recommended)
cd ml && .venv/bin/uvicorn serve:app --port 8000
ML_SERVICE_URL=http://127.0.0.1:8000 npm run dev   # :4000

# Node only (heuristic fallback)
npm run dev
```

- `npm run build` / `npm start` — production Node
- `./deploy/deploy.sh` — EC2 deploy (Node + ML systemd units)

## Layout

| Path | Role |
|---|---|
| `src/server.ts` | Express API + static frontend |
| `src/lib/orchestrator/` | Chat intent routing → agents |
| `src/lib/tools/` | Platform tools (search, score, 6QA, plays) |
| `src/lib/intent-decay.ts` | Surge half-life + 6QA qualification rules |
| `src/lib/ml-client.ts` | ML sidecar HTTP client |
| `src/lib/data/signalverse.ts` | Demo account seed data |
| `ml/serve.py` | FastAPI: score, search, metrics, themes |
| `ml/features.py` | Features, labels, decay, 6QA rules |
| `ml/retrieval.py` | Keyword / semantic / hybrid / co-occurrence |
| `ml/artifacts/` | `model.joblib`, `metrics.json`, `topic_tfidf.joblib`, `intent_themes.json` |
| `public/` | UI — chat, Model Lab, retrieval toggle, badges |

## Conventions

- Node never imports Python — HTTP boundary only; heuristic fallback if ML is down
- Demo accounts live in `signalverse.ts`; export to ML via `scripts/export-signalverse.ts`
- Classifier excludes `buying_stage_ordinal` from features (leakage avoidance)
- Intent surge uses **7-day half-life decay** in heuristics and retrieval ranking
- 6QA flag: Consideration+ stage, intent ≥65, decayed surge gate, classifier proba ≥0.45
- EC2 deploy uses `ml/requirements-serve.txt` (no PyTorch); training uses `requirements-train.txt`

## Docs

- `README.md` — feature overview, local run, API routes
- `DEPLOY_AWS.md` — EC2 deploy
- `private/DEMO_TALKING_POINTS.md` — interview walkthrough (gitignored)
- `private/DS_NOTE.md` — DS technical prep (gitignored)
