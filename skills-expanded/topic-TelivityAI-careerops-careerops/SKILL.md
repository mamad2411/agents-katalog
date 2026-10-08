---
name: careerops
version: 1.2.0
description: CareerOps agent skill — open-source career OS modes (scan, evaluate, rank, tailor, interview, followup, outcome, advise). Materials-first. Never invents experience. Never auto-applies.
---

# CareerOps skill

**Career OS** — operate on the user's **board pack** (exported JSON from the CareerOps web app) or their self-hosted Supabase project.

## Doctrine (non-negotiable)

1. **No invented facts** — employers, titles, dates, metrics, and skills must come from the user's materials / bullet memory / portfolio.
2. **No auto-apply / no auto-send** — drafts are copy/paste only; the human submits on the employer site and sends their own mail.
3. **Tags ≠ stage moves** — Apply / Stretch / Skip are suggestions until the user acts.
4. **Memory provenance** — `body_original` is immutable; AI polish requires Accept; promotion is bidirectional (`source_type` / `source_id` ↔ accomplishment links).
5. **`resume_struct` is canonical** — promotion and portfolio promote go through one atomic write that syncs `resume_text` (never silent dual-write divergence).
6. **Generate retrieval** — checked → role-linked → relevance → recency tie-break only (not newest-20).
7. **Enrichment = inbox + Accept** — GitHub/LinkedIn (and similar) proposals land as candidates; never silent scrape into resume.
8. **Deferred forever** (unless doctrine changes) — auto-apply, auto-send, silent scrape into resume, invented salary bands, ungated multi-agent writes of experience without accept.

See `docs/DOCTRINE_MEMORY.md` and `docs/ROADMAP.md` in the CareerOps repo.

## Modes

| Mode | Purpose |
|------|---------|
| `scan` | Review sourced roles; flag blocklist, age, remote, duplicates |
| `evaluate` | Build a decision pack (summary, risks, suggested call) |
| `rank` | Order roles by fit signals without applying |
| `tailor` | Draft resume/cover from checked / ranked materials only |
| `interview` | Prep angles + story-bank prompts (roadmap: durable interview events) |
| `followup` | Draft follow-up / thank-you notes (never send) |
| `outcome` | Record offer/reject notes (roadmap: structured offer fields via pack) |
| `advise` | Structured career advisor brief — materials-only past; labeled market judgment |

See `modes/` for prompts.

**Mode chains (shipped):** declared pipelines (e.g. `evaluate → rank → interview`) over one board pack; each step writes `mt_reports`; **human confirm** between steps.

```bash
npx @telivity/careerops run-chain --list
npx @telivity/careerops run-chain prep-pipeline --pack CareerOps_board_pack.json --role <role_id>
# after mode output → --report-file <file> → human --confirm
```

See `docs/CHAINS.md`. Plugins (board sources / report kinds / pack fields — hooks, not a browser extension): `docs/PLUGINS.md`.

## Setup

```bash
npx @telivity/careerops init
```

This copies the skill into local agent folders and writes `web/config.js` from `web/config.example.js` when present.

## Board pack

Export from **Settings → Your data → Board pack (skill)** in the web app.

**Durability (shipped):** prefer `CareerOps_board_pack.json` with `schema_version` **≥ 4** — roles, materials, match/evaluate/advisor/interview reports, story bank, **bullet memory** (provenance), **portfolio**, durable **outcomes**, Sent / version display metadata, interview events — never API keys. Optional additive `extensions` holds plugin ids + `chain_runs` (no schema bump required). Older packs migrate upward in the reader.
