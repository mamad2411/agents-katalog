---
name: grader
description: >-
  Scores software artifacts with fine-grained rubrics (category → type →
  dimension → sub-criterion) and produces graded reports with strengths,
  weaknesses, and prioritized fixes. Use when the user mentions grader, 打分,
  评分, scorecard, 项目体检, audit UI, 评架构, 代码质量, 无障碍, 前端性能,
  动效, 微动画, UI创意, 用户接受度, 移动端, App, iOS, Android, React Native,
  Flutter, motion, micro-interaction, resilience, grade my UI, score mobile,
  frontend-mobile, frontend-ux, frontend-a11y, frontend-motion, or asks for
  multi-dimension quality scores on UI, UX, mobile, motion, creativity, a11y,
  frontend code, performance, architecture, backend quality, resilience, API
  design, security, database, testing, or devops.
license: MIT
metadata:
  version: "1.4.0"
  author: mskill
---

# Grader

Fine-grained scoring: **category → type → dimension → sub-criterion**.
Emit totals, dimension scores, sub-scores, strengths, weaknesses, and P0–P2 fixes.

Rubrics are English. Reports follow [report-template.md](references/report-template.md)
(Chinese structure; match the user’s language for prose).

## Workflow

```
Grader Progress:
- [ ] 1. Resolve category, type(s), and scope
- [ ] 2. Load only matching rubric(s) + report template
- [ ] 3. Gather evidence
- [ ] 4. Score every sub-criterion (0–10), roll up to dimensions, then total
- [ ] 5. Emit report (Markdown + YAML) including sub-scores
```

### 1. Resolve category, type, scope

Infer from user intent/paths. If unclear, ask **one** question: category or type.

#### Categories → types

| Category | Type ID | Use when | Rubric |
|----------|---------|----------|--------|
| `frontend` | `frontend-ui` | Visual design, brand/hero, **UI creativity** | [frontend-ui.md](references/frontend-ui.md) |
| `frontend` | `frontend-ux` | Flows, IA, responsive, **user acceptance** | [frontend-ux.md](references/frontend-ux.md) |
| `frontend` | `frontend-motion` | Motion, micro-animations, motion acceptability | [frontend-motion.md](references/frontend-motion.md) |
| `frontend` | `frontend-mobile` | Mobile/app UI: touch, nav, safe area, offline | [frontend-mobile.md](references/frontend-mobile.md) |
| `frontend` | `frontend-a11y` | Accessibility deep-dive | [frontend-a11y.md](references/frontend-a11y.md) |
| `frontend` | `frontend-code` | Components, state, types, FE structure | [frontend-code.md](references/frontend-code.md) |
| `frontend` | `frontend-performance` | Runtime/perf, bundle, rendering cost | [frontend-performance.md](references/frontend-performance.md) |
| `backend` | `backend-architecture` | Boundaries, layering, cohesion, fit | [backend-architecture.md](references/backend-architecture.md) |
| `backend` | `backend-quality` | Correctness, errors, complexity, BE tests | [backend-quality.md](references/backend-quality.md) |
| `backend` | `backend-resilience` | Failure, degradation, observability design | [backend-resilience.md](references/backend-resilience.md) |
| `backend` | `api-design` | HTTP/RPC/GraphQL contracts | [api-design.md](references/api-design.md) |
| `security` | `security` | Authn/z, injection, secrets, data exposure | [security.md](references/security.md) |
| `data` | `database` | Schema, queries, migrations | [database.md](references/database.md) |
| `quality` | `testing` | Test strategy and case quality | [testing.md](references/testing.md) |
| `ops` | `devops` | CI/CD, release, config, supply chain | [devops.md](references/devops.md) |

**Routing aliases**

- “评 UI / 页面设计 / visual / UI创意” → `frontend-ui` (add `frontend-ux` / `frontend-motion` if also asked)
- “评交互 / UX / 信息架构 / 用户接受度” → `frontend-ux`
- “动效 / 微动画 / motion / micro-interaction” → `frontend-motion`
- “移动端 / App / iOS / Android / RN / Flutter / mobile web” → `frontend-mobile`
- “无障碍 / a11y / accessibility” → `frontend-a11y`
- “前端性能 / Core Web Vitals / jank” → `frontend-performance`
- “页面综合观感” → often `frontend-ui` + `frontend-ux` + `frontend-motion`
- “App 综合体验” → often `frontend-mobile` + `frontend-ui` + `frontend-motion`
- “架构” → `backend-architecture` (add `backend-resilience` for reliability focus)
- “后端质量 / code quality (BE)” → `backend-quality`
- “全面体检 / full audit” → pick **one type per relevant category** (typically 3–5 types), score each separately, then synthesize. Never invent unscored types.

**Scope:** user paths/files, else core dirs for that type. State scope in the report.

### 2. Load rubric

Load only the active type’s file + report template. For multi-type checkups, load one rubric at a time.

### 3. Gather evidence

- Read code, styles, configs, layout; prefer live UI preview when scoring UI/UX/a11y
- Every **sub-criterion** needs a cite (file/symbol/pattern) or `N/A`
- Never fake scores

### 4. Scoring model (fine-grained)

```
sub-criterion (0–10)
  → dimension = average of its non-N/A sub-criteria
  → total/100 = weighted average of dimensions (rubric weights)
  → grade S/A/B/C/D
```

Rules:

- Sub-criterion and dimension: **0–10** (integer or one decimal)
- `total = round(100 * Σ(dim_score * weight) / Σ(weight))` over non-N/A dimensions
- If a dimension’s sub-criteria are all `N/A`, dimension is `N/A`
- Grades: `S` ≥90 · `A` ≥80 · `B` ≥70 · `C` ≥60 · `D` <60
- Bands: 0–3 poor · 4–6 fair · 7–8 good · 9–10 excellent
- No flat identical scores across subs to “look balanced”
- Blocking defects (authz hole, keyboard trap, data-loss risk): affected subs ≤3 and call out in summary

### 5. Emit report

Follow [report-template.md](references/report-template.md): dimension table **and** sub-score breakdown + YAML with nested `subs`.

## Principles

- Evidence first; score only the active rubric
- Prefer the finer type when the user names a narrow concern (don’t dump everything into `frontend-ui`)
- Direct, actionable; no proprietary APIs; no exploit PoCs
