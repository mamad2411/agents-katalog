---
name: strategic-review
group: domain
triggers:
  - "стратегический анализ"
  - "что строить"
  - "roadmap"
  - "приоритизация фич"
  - "что дальше делать с проектом"
  - "фичи для сервиса"
output: "structured strategic report: baseline / diagnosis / 5 areas / priority matrix / roadmap"
calls: []
---

# Skill: Strategic Review

**Purpose:** Analyze a service or project at phase transitions — identify what's working, what's broken, and what to build next. Produces a prioritized feature roadmap grounded in real metrics.
**When:** At phase transitions in plan.md, when metrics degrade, or when the backlog needs re-prioritization.
**Output:** Structured markdown report delivered in chat (no file written).

---

## PROCESS

### Step 1 — Collect project context

Read (in order):
1. `CLAUDE.md` — QUICK CONTEXT, GOAL, CURRENT STATE, Known Issues, LOG
2. `plan.md` — active phase, open/closed tasks, gates
3. Any metrics files mentioned in CLAUDE.md (backtest reports, precision logs)
4. `~/.claude/memory/episodic/best-practices.md` — grep for project stack tags

If project has a running DB (SQLite, Postgres) and CLAUDE.md has a schema reference → offer to run diagnostic queries:
```
"Запустить диагностические SQL-запросы для актуальных метрик? (да / нет)"
```
If "да" — run queries via Bash (sqlite3 / psql) to get: alert count, precision, PnL, open positions.
If "нет" — use values from CLAUDE.md/LOG.

### Step 2 — Build Baseline Table

Extract key metrics into a table:

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Precision | X% | ≥ 70% | 🔴/🟡/✅ |
| Paper/Live PnL | $X | > 0 | 🔴/🟡/✅ |
| Alert volume (today) | N | — | — |
| Monitor cycle | Xm | < 10m | 🔴/🟡/✅ |
| Notifications | status | working | 🔴/🟡/✅ |
| Open positions | N | ≤ max | — |

Mark each: ✅ on target / 🟡 acceptable / 🔴 below threshold.

### Step 3 — Diagnose Problems

For each 🔴 metric — one paragraph:
- What specifically is broken
- Most likely root cause (hypothesis, not fact)
- What data would confirm/deny it

Keep hypotheses labeled as hypotheses. Don't state unknowns as facts.

### Step 4 — Five Areas

Always structure proposals across 5 standard areas. Skip areas with no findings (don't force entries):

**A. Signal Quality** — precision, recall, detector performance, false positive sources
**B. Trading Bot** — entry logic, exit logic, position sizing, banned categories
**C. Infrastructure** — notifications, monitoring, deploy pipeline, reliability
**D. Analytics** — per-detector stats, per-category PnL, wallet tracking, outcome tagging
**E. Performance** — scan cycle time, API efficiency, DB query speed

For each finding: one-line description + concrete proposal.

### Step 5 — Priority Matrix

Rank all proposals:

| # | Feature | Area | Impact | Effort | ROI |
|---|---------|------|--------|--------|-----|
| 1 | [name] | A/B/C/D/E | 🔴 High / 🟡 Med | 🟢 1h / 🟡 3h / 🔴 1d | ⭐⭐⭐⭐⭐ |

Rules:
- Impact: 🔴 = directly fixes a 🔴 metric; 🟡 = improves 🟡 metric; 🟢 = nice to have
- Effort: 🟢 = < 2h; 🟡 = 2–8h; 🔴 = > 1 day
- ROI stars: Impact/Effort ratio, 1–5 stars
- Sort by ROI descending

### Step 6 — Roadmap

Three buckets:

**Quick wins (today, < 4h):** Top 3–4 by ROI — can be done in current session
**Medium term (next 2–3 sessions):** Important but need planning
**Long term (after gate/milestone):** Depends on data not yet available (paper trading results, A/B data)

For each item: one line, clear acceptance criterion.

### Step 7 — Offer to start

After report:
```
"С чего начнём? Могу сразу перейти к реализации любого пункта."
```

---

## RULES

- **Use real data.** If metric unavailable — say "unknown" not a guess.
- **Label hypotheses.** Root cause is a hypothesis until confirmed by data.
- **One proposal = one sentence.** No walls of text. Bulleted, scannable.
- **Don't propose what's already in plan.md** as open tasks — acknowledge it exists, don't duplicate.
- **Skip empty areas** — if Area C has no findings, omit it entirely.
- **Gate awareness** — note if a proposal requires a gate condition (paper trading data, precision threshold) before it can be implemented.

---

## PRE-FLIGHT

Before delivering report: verify all 5 areas were checked (even if skipped with reason), priority matrix is sorted by ROI, and roadmap has at least 1 quick win.

## PRE-DELIVERY CHECKLIST

- [ ] Baseline table complete — all key metrics present or marked "unknown"
- [ ] Each 🔴 metric has a diagnosis paragraph
- [ ] All 5 areas checked (skipped areas noted explicitly)
- [ ] Priority matrix sorted by ROI
- [ ] Roadmap has 3 buckets: quick / medium / long
- [ ] Step 7 offer included at end
