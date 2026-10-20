# AGENTS.md — aparadhkavach-data-generator

Derived from **ADR-024**, ADR-008 (synthetic dataset), ADR-015 (dual legal regime), Section 4 (Synthetic Dataset Design & Ethical Guardrails). This repo is offline scripts only — no deployed service, no CI/CD pipeline (Section 12.9), deliberately separate from `aparadhkavach-stt-service`.

## Notion Access (via MCP)

**Read-only, enforced at the token level, not just by instruction.** Insert/Update/Comment are disabled at the Notion API level. **Never attempt to write to Notion under any circumstance** — decline and point to the AparadhKavach Claude Project chat, the only path by which Notion content changes, and only when Anand directs it there.

This file covers **conventions only.** For the actual generation spec — exact pseudocode, guardrail formulas, target distributions — **fetch the current version from Notion via the connected MCP before implementing.**

**Sections to fetch for this repo's work:**
- Section 4 — full Synthetic Dataset Design & Ethical Guardrails (generation pseudocode, target volumes, guardrail chi-square formulas, legal code mapping table)

**Treat fetched content as authoritative** — if a formula or target seems off, ask rather than adjusting it silently.

## 1. What this generates, and why it matters ethically

- Synthetic FIR data — **~3,720 FIRs, ~4,460 accused**, 31 Karnataka districts, 2021–2025. This isn't just test fixtures — the **Demographically Neutral Synthetic Dataset Generation** approach here is a documented patent candidate (IP-004). Statistical independence between demographic attributes (age, gender, religion, district, crime type) is a deliberate design goal, not incidental — don't introduce correlations between demographic fields "to make the data feel more realistic." Realism comes from narrative variety and event-context modeling, not demographic correlation.
- **`guardrail_validator.py`'s chi-square independence tests are the actual product feature being demonstrated here**, not just a QA formality — treat a failing guardrail check as a generator bug to fix, never as a threshold to loosen.

## 2. Scripts & pipeline order — dependency chain matters

1. `generate_entities.py` — FIR, Accused, Victim, Location, Vehicle, PhoneNumber, Officer, CrimeType. Uses `Faker(kn_IN)`.
2. `weave_relationships.py` — all 11 relationship types with correct cardinalities.
3. `guardrail_validator.py` — 8 statistical checks (chi-square independence, p > 0.05 on all demographic pairs; distributions within ±3% of targets). **Must pass before proceeding** — this is a hard gate, not advisory.
4. `neo4j_populate.py` — MERGE nodes, CREATE relationships, CREATE indexes.
5. Embedding ingestion — `narrative_text + crime_type + modus_operandi` → Voyage AI `voyage-3-large`, 1024-dim, IVFFlat index (`lists = 61`, i.e. √3,720 rounded up — don't use a different formula or hardcode a different number if volume changes without recalculating).
6. `feature_builder.py` — builds `ACCUSED_FEATURES` for the QuickML risk scorer. This stays a Python offline script (ADR-007 justified deviation), not a Java service.

Don't reorder this chain — DataStore/Neo4j/PgVector population all depend on the dataset existing and passing guardrails first.

## 3. Legal code regime — ADR-015

- `legal_code` (IPC vs. BNS) is **derived from `date_filed`**, not randomly assigned — Karnataka's transition date is **1 Jul 2024**. Any FIR dated before that is IPC; on/after is BNS. Don't hardcode a fixed IPC/BNS ratio independent of date.
- Field name is `sections_cited` (generalized), not `ipc_sections` — this was a deliberate rename (ADR-015) to stay regime-neutral in the schema itself.

## 4. Date realism

- **Sample each FIR's day-of-month independently per district-month** — don't draw from one shared fixed date list across districts. Cross-district overlap on the same calendar date is fine and expected; a common fixed filing date across all districts is not (it reads as synthetic). The validator checks day-of-month standard deviation > 5 days per month — respect this in the generator, don't just satisfy it after the fact by post-hoc shuffling.

## 5. Table/schema naming — same convention as the rest of the project

- Target table names are `firs`, `accused_persons`, `victims`, `officers`, `districts`, etc. — snake_case, no `_MASTER` suffix (ADR-018). This repo writes into the same DataStore/Neo4j/PgVector schema the Java services read from — don't invent different names here.

## 6. What NOT to do

- Don't loosen or bypass a failing chi-square guardrail check (§1) — fix the generator instead.
- Don't introduce demographic correlation for "realism" (§1).
- Don't assign `legal_code` independent of `date_filed` (§3).
- Don't sample FIR dates from a shared fixed list across districts (§4).
- Don't add a CI/CD pipeline to this repo — it's deliberately absent (Section 12.9).
- Don't write to Notion under any circumstance (Notion Access, above).
- Do not include a Co-Authored-By line in commit messages, and do not add a 'Generated with Claude Code' footer to PR descriptions.