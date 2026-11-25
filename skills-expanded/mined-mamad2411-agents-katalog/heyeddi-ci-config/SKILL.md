---
name: heyeddi-ci-config
description: Author or update eddi-ci.yaml for HeyEddi CI and Spot runners. Use when enabling HeyEddi CI, runners, or the user asks to create/configure eddi-ci.yaml. Loads the live policy contract from cihook.heyeddi.com so knobs stay current.
version: 1.0.0
product-version: 3.0.6
author: HeyEddi-com
paths:
  - "eddi-ci.yaml"
  - ".github/**"
---

# HeyEddi CI Config

Authors a correct `eddi-ci.yaml` for HeyEddi Reviewer / optional Spot runners. **Do not invent knobs from memory.**

## Knowledge rule (mandatory)

The skill package does **not** ship a full knob table. On every run:

1. Run `load_policy_contract` (or `python …/scripts/load_policy_contract.py`).
2. Treat the returned `guide`, `knobs`, `rules`, and `minimal_example` as authoritative.
3. Prefer human docs for narrative: `docs_url` (default https://ci.heyeddi.com/docs#policy).
4. Read `context/ANTI_PATTERNS.md` for durable safety rules that never go stale.

Contract feed (production): `https://cihook.heyeddi.com/api/public/eddi-ci-policy`

Fallback order inside the script: local heyeddi-ci checkout → `HEYEDDI_CI_POLICY_URL` / production API → docs page text.

## Decision gate: add the file or not (mandatory)

Missing `eddi-ci.yaml` is **not** a defect. Safe defaults already apply (runners off, `on_ci_failure` off). Decide **before** writing anything:

### Write / create `eddi-ci.yaml` only when at least one is true

- User **explicitly asks** to create, add, or configure `eddi-ci.yaml`
- **`inspect_repo` reports `heyeddi_product.uses_heyeddi_product: true`** — the repo already uses a HeyEddi product (see signals below). Then add a **Reviewer-only safe** file (billable knobs off, `pipeline: {}`) unless the user declines.
- User wants **Reviewer policy beyond defaults** (e.g. `allow_external_prs`, higher `validation_max_attempts`, document team rules)
- User wants **Spot / isolated runners** (`pipeline:` jobs) and accepts that those jobs need real commands + path filters
- User is following the HeyEddi PR CTA and **confirms** they want to configure now (CTA alone ≠ auto-write; ask once if intent is unclear)

**HeyEddi product signals** (from `inspect_repo` → `heyeddi_product.evidence`):

- `.heyeddi/` workspace present
- `.agents/skills/heyeddi-*` installed
- `skills-lock.json` pins `HeyEddi-com/skills`
- `PRODUCT.md` / `.heyeddi/product.md` / `README.md` / package identity mention HeyEddi

### Do **not** create the file when

- The only signal is “file is missing” **and** no HeyEddi product markers
- User only wants a normal code review and never opted into config / not a HeyEddi project
- User declines after you explain that defaults are already safe
- You would have to invent test commands or path filters to fill `pipeline` (still OK to add Reviewer-only YAML without pipeline jobs)

### If not adding

Explain briefly: HeyEddi already runs with safe defaults; they can invoke `@heyeddi-ci-config` later when they want policy or runners. **Stop. Do not write the file.**

### If updating an existing file

Edit only when the user asked to change policy/runners, or when fixing invalid YAML they already committed. Do not “improve” an untouched valid config unprompted.

## When to use this skill

- Any of the “write / create” conditions above
- User asks how `eddi-ci.yaml` works (load contract + explain; create only if they then opt in)

## When not to use

Do **not** invent a config pass just because the file is absent.

## Instructions

1. Run `inspect_repo` and apply the **decision gate** (including `heyeddi_product`). If not adding, explain and stop.
2. If adding because HeyEddi product was detected: default to **Reviewer-only** safe YAML; ask before enabling runners or `on_ci_failure`.
3. If adding/updating for other reasons: confirm intent — Reviewer-only policy vs runners vs both.
4. **Load the live contract** via `load_policy_contract`.
5. Finish repo inspect for languages / real test commands when runners are in scope. Do not invent `pytest` / `npm test` without evidence.
6. Confirm billable knobs against the contract: keep `ai_review.on_ci_failure` **false** unless the user explicitly opts in; add `pipeline` jobs only when runners are wanted and commands are known.
7. Write `eddi-ci.yaml` at the repo root using only keys from the contract knobs.
8. Prefer empty `pipeline: {}` unless runners are requested and path filters are known.
9. Tell the user to commit/push; HeyEddi App lints the file when it changes on a PR.

## Tools

| Tool | Purpose |
|------|---------|
| `load_policy_contract` | Fetch living knobs/guide/rules/example |
| `inspect_repo` | HeyEddi product detection + languages / likely test cmds |

## Examples

### Reviewer-only (safe)

After loading the contract, write the contract’s `minimal_example` (or equivalent) with billable knobs off.

### Runners when requested

Only after `inspect_repo` (or equivalent) shows real commands and path prefixes, add `pipeline` jobs with `filter.paths`. Never enable `on_ci_failure` without explicit opt-in.

## Notes

- Unknown top-level keys fail schema (`extra=forbid`).
- Invalid YAML → App ignores file and uses safe defaults.
- See `context/EXAMPLES.md` for shapes; always re-check knobs from `load_policy_contract`.
