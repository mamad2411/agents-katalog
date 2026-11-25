---
name: demo-readiness
description: Pre-demo checklist — wake backend, verify frontend, demo script, pages to show/avoid.
---

# Demo readiness

## When to use

- Stakeholder demo on Vercel + Render or local demo.
- Morning-of check before presenting MVP+.

## Goal

Predictable demo: live API, seeded data, known caveats, script order.

## Safety rules

- Prefer production URLs from `docs/DEMO_SCRIPT.md` for stakeholder demo.
- Do not run production DB cleanup without `db-safety-cleanup` skill.
- Do not implement auth during demo prep.

## Read first

- `docs/DEMO_SCRIPT.md`
- `docs/MVP_PLUS_SCOPE.md`

## Checklist

### Backend awake (Render)

```bash
curl -s https://logistics-mvp.onrender.com/api/health
# First request after sleep may take 30s
```

### Frontend

- Open Vercel app URL from `README.md` / `DEMO_SCRIPT.md`
- Network: requests to Render `/api`, not localhost
- No API-unavailable banner

### Data

- [ ] Shipments list populated
- [ ] Tracking map loads
- [ ] Managers/clients present
- [ ] Finance rows consistent (paid/partial/unpaid)

### Pages to show

1. Dashboard — KPIs and charts
2. Shipments — list, detail, create (optional)
3. Tracking — map, checkpoints
4. Managers / Partners
5. Finance — report + export
6. Telegram — settings save

### Pages to avoid / caveats

- **Users** — mock/post-MVP
- **Settings** — partial
- Auth not implemented
- Telegram does not send real messages
- Mention Render cold start if applicable

## Local demo alternative

```bash
cd backend && php artisan serve --host=127.0.0.1 --port=8000
VITE_API_BASE_URL=http://127.0.0.1:8000/api npm run dev -- --host localhost --port 5173
```

## Output format

- **READY** / **NOT READY**
- Failed checks
- Demo script order (short)
- Caveats for presenter (3–5 bullets)
