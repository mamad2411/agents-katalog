---
name: opportunity-from-jd
description: >-
  Reads a raw JD and produces a YAML snippet for opportunities.yaml plus optional
  jd_catalog.csv row. Use when adding a new pipeline opportunity from data/raw,
  ingesting a JD file, or bootstrapping opportunity id and next_action fields.
---

# Add opportunity from a JD file

**Role:** Assistant — career / opportunity tracking (see `docs/AGENT_ROLES.md`).

**Context to load:**
- JD file: paste text or path to `data/<filename>.md`
- Schema: `templates/opportunities_tracker_template.yaml`
- Optional: `data/master.yaml` for fit notes
- Optional: `config/jd_catalog.csv` to register `job_id`

**Scope:**
- Needs only: JD, schema template, optional existing tracker/catalog rows.
- No broader vault context unless user asks.

**Task:**
1. Read JD. Extract **role_title** and **company_display** (exact JD text). Company not in JD: don't guess — use user-provided label (e.g. `"Unknown (SF-based startup)"`). No label either: ask first.
2. Propose **`id`**: short slug, unique in `data/opportunities.yaml` (e.g. `acme-senior-backend-2026`).
3. Set **`stage`**: usually `Interested` or `Applied` (user may override).
4. Set **`jd_source`**: min `raw_path: "data/raw/<FILENAME>"`. If user wants catalog tracking, output one CSV row for `jd_catalog.csv` with columns `job_id,alias,role,raw_path,normalized_path,status` (fill unknowns with placeholder or ask).
5. Set **`next_action`** and **`next_action_date`** (concrete, within 7 days if possible), **`priority`** (P0/P1/P2), short **`notes`**.
6. If user supplies contact info (recruiter, HM, referral), populate **`contacts[]`** — each: `name`, `role` (`recruiter|hiring_manager|referral|hr|other`), `channels` (free map: any platform key → handle/URL/number, e.g. `linkedin`, `email`, `zalo`, `whatsapp`, `telegram`, `messenger`, `phone`), `notes`. Omit key if no contacts known.
7. If JD or user provides portal/posting URL, populate **`links`** (`application_portal`, `job_posting`, or free key). Canonical spots for manual status checks. Omit key if no URLs known.
8. Set **`updated_at`** to today (ISO date).
9. Output **YAML snippet** ready to append under `active:` in `data/opportunities.yaml` (or merge instructions if file exists). No duplicate `id`.

**Output sections:**
- YAML block for new `active[]` item only
- If jd_catalog row suggested: CSV line or table row
- **Assumptions** / **Risk**

**Constraints:**
- **`data/` is gitignored** — full detail fine for YAML/chat drafts that stay local.
- **No fabrication.** Only values from JD or user. No invented role details, company facts, contact info, URLs.
- Field can't be extracted: use `Unknown`, note in **Assumptions**, ask one clarifying question before locking `id` or `company_display`.
- Every inference (stage from tone, priority from urgency language) → list in **Assumptions**, confirm before final output.

**My inputs (collect, confirm, or ask):**
- Any item below unknown from memory, prior messages, or repo (`data/raw/`, `opportunities.yaml`): **ask** before emitting final YAML.
- Inferred item (stage from tone, path from last-opened file): state briefly, **ask to confirm or correct** before final output.
- Path to JD under `data/raw/`: `<...>`
- Desired initial stage: `<Interested | Applied | ...>`
- job_id for catalog (or "skip catalog"): `<...>`
- Contacts (recruiter / HM / referral name + role + linkedin/email if known, or "none"): `<...>`
- Application portal / job posting URL (or "none"): `<...>`