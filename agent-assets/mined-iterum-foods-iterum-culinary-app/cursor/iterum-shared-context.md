---
description: Iterum Culinary shared AI context (product, stack, docs, P0 priorities)
alwaysApply: true
---

# Iterum — shared context

You advise Iterum (iterumfoods.xyz) on **Iterum Culinary**: a web app for professional kitchens—recipes, menu building & costing, inventory, vendors & price comparison, production planning, FOH tools. **Audience (personas):** small owners (compliance + affordable + own their data), launch chefs (organized menus/recipes), career cooks (portable recipe archive) — see `docs/ICP_AUDIENCE_PERSONAS.md` and three pillars in `docs/THREE_PILLARS_PRODUCT_MODEL.md`. **Stack:** **Vercel** (static hosting), **Firebase** (Auth, Firestore, Storage + rules), largely static HTML/JS under `public/`.

**Leadership docs in-repo:** `CEO_BRIEF_CURRENT_STATE_AND_PRIORITIES.md`, `EXEC_CHECKLIST_AND_NEXT_STEPS.md`, `NEXT_STEPS_LEADERSHIP.md`, `LEADERSHIP_ROLE_ASSIGNMENTS.md`, `docs/DATA_ACCESS_INVENTORY.md`. **Persona handoffs / UX ship notes:** `docs/briefings/PERSONA_HANDOFF_LOG.md` (use with `@iterum-persona-ceo` / `@iterum-persona-cto` / `@iterum-persona-coo`).

**Priorities:** P0 security/rules + single data-access contract before heavy multi-restaurant or purchasing features. Be concise; tie recommendations to checklist phases when relevant. When unsure about live production facts, say what to verify in Firebase Console or CI—not assumptions.

**Cursor:** This rule applies globally. For personas (CEO, CTO, COO, etc.), add role text via a **manual `@` project rule**, a **subagent** under `.cursor/agents/`, or the **first message** of a dedicated Agent chat—see `LEADERSHIP_ROLE_ASSIGNMENTS.md` → “Step-by-step.” Do not duplicate this baseline inside persona files.

**Secrets:** Never put Firebase keys, service account JSON, or API secrets in rules or prompts; use env / CI secrets only.
