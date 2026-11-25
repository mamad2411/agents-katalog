---
name: interactive-ui-qa
description: >-
  Run authored Interactive UI QA against Projectionist maintainer QA (:8790) in full
  (absolute baseline) or delta (open bugs + tagged subset) mode. Use when the
  user asks for browser QA, UI QA, role QA, absolute baseline, or delta
  regression — never exploratory pathway discovery; never prod :8788.
---

# Interactive UI QA

Two-mode, checklist-only browser QA for Projectionist. Replicates characterization
(full) + change-focused regression (delta). **Execute authored checklist IDs
only** — see [reference.md](reference.md).

## When to use

- User asks for browser / UI / role QA, absolute baseline, or delta retest
- After a chrome / gating / delight ship when verifying regressions
- Standing up or refreshing `ABSOLUTE_BASELINE.md` on the QA host

Do **not** use this skill for free-form exploratory testing, fixing product bugs
(unless the user also asks for a fix), or hitting production.

## Target environment (hard rules)

| Item | Value |
|------|--------|
| Base URL | `http://10.10.1.202:8790` (`QA_BASE_URL` in maintainer scripts) |
| Credentials | `/Volumes/appdata/projectionist-qa-scripts/.env.qa` — `QA_OWNER_*`, `QA_MEMBER_*`, `QA_YOUTH_*`, `QA_GUEST_*` |
| Never | Production / tunnel **`:8788`** — refuse and redirect to `:8790` |
| Artifacts | `/Volumes/appdata/projectionist-qa-scripts/qa-runs/` |

If `.env.qa` is missing, stop and tell the user to copy `.env.qa.example` and seed roles. Do not invent passwords. Do not log passwords into reports.

## Modes

### `full` — absolute characterization

When: first stand-up, major chrome releases, periodic audit, or user says “full / absolute baseline”.

1. Run **every** checklist ID in [reference.md](reference.md) for the requested role(s) (default campaign: member; prefer also owner, youth, guest-tour when user allows).
2. Recheck every open bug listed in `qa-runs/BASELINE.md` (if any).
3. Theme both ways where `theme` tags apply (Lights Up + Lights Down at least once each).
4. Scroll/overflow checks only where the checklist names them.
5. Write/overwrite `qa-runs/ABSOLUTE_BASELINE.md` and a dated `YYYY-MM-DD-<role>-full.md`.
6. Seed/update `qa-runs/BASELINE.md` open-bug board from graded findings.

### `delta` — default day-to-day

When: after a fix, patch, or scoped feature; or user says “delta / retest”.

1. Recheck **all** open bugs in `qa-runs/BASELINE.md`.
2. Add checklist IDs selected by:
   - tags matching recent CHANGELOG / ship notes / files touched, and/or
   - explicit user scope (e.g. “member nav + journey”).
3. Write dated `YYYY-MM-DD-<role>-delta.md`; update open-bug statuses only.
4. Compare regressions against `ABSOLUTE_BASELINE.md` when it exists.

If absolute baseline is still a stub, say so in the report and still grade the selected IDs.

## Severity rubric

| Severity | Meaning | Examples |
|----------|---------|----------|
| `blocker` | Cannot complete a core role path; data loss; auth break | Login broken; entire chat unusable; wrong role can administer |
| `major` | Wrong gating, broken primary control, serious visual/hydration defect on a primary surface | Admin flash for member; journey tree missing; Surprise Me does nothing; nested vertical scroll on poster strip |
| `minor` | Workaround exists; secondary surface wrong | Misaligned label; empty-state copy glitch; one rail CTA missing when empty is OK |
| `polish` | Cosmetic / delight only | Animation timing; icon weight; spacing nits |

**Verdict:**

- **FAIL** if any `blocker` or `major` is still open at end of run
- **PASS** otherwise (minors/polish = backlog, listed in Bugs)

Page-load alone is **never** PASS. Each ID requires its specified interaction and pass criteria.

## Hard rules (both modes)

1. **Authored IDs only** — no pathway discovery. New UI → edit `reference.md` in the same change (or immediately after).
2. Grade visual / a11y / hydration / scroll / wrong gating as bugs with severity.
3. Capture screenshots for fails and for representative passes on gating/theme/scroll IDs.
4. Prefer Cursor browser MCP against `QA_BASE_URL`; do not start Playwright suites unless the user asks.
5. Never commit `qa-runs/` contents into the projectionist git tree (host-local under `projectionist-qa-scripts/`).

## Procedure

1. Confirm mode (`full` | `delta`) and role(s) with the user if unclear; default mode is **delta**.
2. Read credentials from `.env.qa` (do not echo secrets).
3. Load open bugs from `qa-runs/BASELINE.md`.
4. Build the ID list:
   - `full` → all IDs whose `roles` include the run role(s)
   - `delta` → open-bug rechecks + tag/scope-selected IDs
5. For each ID: follow **steps**, assert **pass criteria**, record PASS/FAIL + notes + severity if fail.
6. Write the dated report under `qa-runs/` with sections: Mode, Verdict, Bugs, Regressions vs absolute/open baseline, Checklist results, Screenshots.
7. Update `BASELINE.md` (and `ABSOLUTE_BASELINE.md` on full).

## Role credentials map

| Role | Env user | Env password | Typical login |
|------|----------|--------------|---------------|
| owner | `QA_OWNER_USER` | `QA_OWNER_PASSWORD` | Local form on `/login` |
| member | `QA_MEMBER_USER` | `QA_MEMBER_PASSWORD` | Local form |
| youth | `QA_YOUTH_USER` | `QA_YOUTH_PASSWORD` | Local form (`is_youth`) |
| guest (signed-in) | `QA_GUEST_USER` | `QA_GUEST_PASSWORD` | Local form when `QA_SEED_GUEST_ROLE=1` |
| guest-tour | _(none)_ | _(none)_ | Public `/tour` when guest tour enabled |

## Related code

- Nav gating: `frontend/src/lib/primaryNav.js`, `frontend/src/components/PrimaryTopbar.jsx`
- Shells: `frontend/src/layouts/AppShell.jsx`, `frontend/src/lib/memberShell.js`
- Admin gate: `frontend/src/layouts/AdminLayout.jsx` (non-owner → `/settings`)
- Checklist inventory: [reference.md](reference.md) — includes `inbox`, `notifications`, `recommend` tags for delta selection
