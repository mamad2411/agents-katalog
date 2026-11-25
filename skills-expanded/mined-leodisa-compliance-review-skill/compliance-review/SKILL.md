---
name: compliance-review
description: >
  Build or review code for compliance with the EU AI Act, GDPR, the NIS2
  Directive (EU 2022/2555), and secure-development (SSDLC) best practice.
  Three modes. REVIEW: audit a repo and produce an evidence-based gap analysis —
  triggers on "compliance review", "gap analysis", "NIS2 check", "is this repo
  GDPR compliant", "security audit of the code". DESIGN/BUILD: apply the same
  requirements as compliance-by-design guardrails while writing new code, then
  self-check — triggers on "build X with GDPR/AI Act/NIS2 in mind",
  "compliant/secure/privacy by design". DATA MASKING: when the user shares a
  dataset (CSV, JSON, query result) that may contain personal data, never read
  it raw — ask whether to pseudonymise (keeps joins) or anonymise
  (k-anonymity), then protect it first — triggers on "anonymise/mask this
  data" or any dataset handed over for analysis. Use
  whenever code or data must meet a security/privacy/AI regulation, even if no
  framework is named. Advisory only, not legal advice.
license: MIT
---

# Compliance Review & Design

Help code **meet** the EU AI Act, the GDPR, the NIS2 Directive (EU 2022/2555),
and secure-development (SSDLC) best practice — either by **reviewing** an
existing repository or by **building it in from the start**. The EU frameworks
are public legal texts (articles cited directly); the SSDLC pillar aligns with
OWASP SAMM / ASVS and NIST SSDF. The reference files are the shared source of
truth in all modes:

- EU AI Act → `references/eu-ai-act.md`
- GDPR → `references/gdpr-quickcheck.md`
- NIS2 → `references/nis2.md`
- Secure development (SSDLC) → `references/secure-development.md`
- Data masking (safe dataset handling) → `references/data-masking.md`

## Read this first: scope and honesty (applies to all modes)

A codebase is only part of an organisation's compliance posture. NIS2 and GDPR
are largely governance regimes — policies, risk treatment, training, and
reporting to authorities live outside any code. Be honest about that boundary:
address only what code can actually carry, and flag the rest as organisational.

- This is an **advisory aid**, not a certification or legal opinion, and not
  legal advice. It helps prioritise and build correctly; it does not prove
  conformity.
- **Never read, print, or hardcode secret values.** Secrets come from env vars or
  a secret store — never committed or embedded. If you find a committed
  credential, report its location and that it must be rotated; do not print it.

### Avoid double-counting across frameworks

The four references overlap on purpose — NIS2 Art. 21(2)(e), the SSDLC
practices, and GDPR Art. 32 all touch SAST, dependency scanning, encryption,
access control and vulnerability handling. Assess each underlying fact **once**:
record the full finding (evidence, severity, remediation) in the **most specific
section** — usually SSDLC for engineering practice, NIS2 for the legal measure,
GDPR when personal data is the point — and in the other tables add a one-line
cross-reference (e.g. "see SSDLC §2.2") instead of repeating it. Count each
underlying gap **once** in the severity totals.

## Choose the mode

- The user has an **existing** repo/app and wants it checked → **Review mode**.
- The user is **starting or writing** something new (or adding a feature) and
  wants it done compliantly → **Design/build mode**.
- The user **shares a dataset** (file, paste, query result) that may contain
  personal data → **Data-masking mode** first, whatever else follows.

If both apply (e.g. "build this and then check it"), do Design/build first, then
finish with a Review-mode self-check.

---

## Design/build mode (compliance-by-design)

The goal is to bake the requirements in *while writing*, not to bolt them on
later. The reference files stop being an audit checklist and become a
**requirements list**.

### 1. Scope what applies

Before writing, work out which requirements are live for this project:

- **Personal data?** If the app processes personal data, GDPR applies — note the
  data categories (and whether any are special-category, Art. 9). See
  `references/gdpr-quickcheck.md`.
- **AI/ML component?** If it builds, integrates, or deploys AI, the AI Act
  applies — infer the likely risk class first. See `references/eu-ai-act.md`.
- **Security baseline (NIS2)** applies to essentially any networked service;
  treat Art. 21 technical measures as the security floor. See `references/nis2.md`.
- **Secure development (SSDLC)** applies to *all* code, always — treat
  `references/secure-development.md` as the engineering baseline (environment
  separation, secure coding, SAST/dependency scanning, security testing).

State these as premises so the user can correct them.

### 2. Turn the relevant items into build requirements

Read the applicable reference file(s) and translate each relevant item into a
concrete thing to implement. For example:

- Secrets → load from env/secret store from the first commit; add `.env` to
  `.gitignore`; never hardcode.
- Access control → put an authN/authZ model in from the start (RBAC, session/token
  expiry, least privilege); add MFA support where accounts matter.
- Cryptography → TLS everywhere, encryption at rest for sensitive data, strong
  password hashing (bcrypt/argon2).
- Logging/traceability → log security and access events with actor + timestamp;
  for AI, log inferences (input/output/model version) for record-keeping.
- Data minimisation & retention → collect only what's needed; add a deletion/
  retention path (GDPR Art. 5, 17) early, not later.
- Transparency (AI) → if it's a chatbot or generative AI, disclose AI use and
  mark AI-generated content.
- Supply chain → pin dependencies, add a lockfile, wire dependency/vulnerability
  scanning into CI from the start.
- Secure SDLC → separate dev/test/prod config, SAST in CI, input validation and
  parameterised queries by default, code review before release.

Prefer building the guardrail in now; if the user explicitly defers something,
note it as a known gap rather than silently skipping it.

### 3. Write the code applying them

Implement the feature/app normally, but with the requirements above as
non-negotiable defaults. When a requirement would materially change the design
(e.g. needing a secret store, or an audit-log table), call it out and do it
rather than choosing the non-compliant shortcut.

### 4. Self-check before finishing

Do a short Review-mode pass over what you just wrote (see below) and report which
requirements are now satisfied and which remain open (with a reason). This gives
the user a compliance-by-design summary, not just code.

**Output:** the code, plus a brief **"compliance built in"** summary — a short
list per framework of what was implemented and any deliberate gaps left for later.

---

## Data-masking mode (safe dataset handling)

When a dataset that may contain personal data enters the conversation, **do not
read the raw file**, and **ask the user which strategy they want before
processing** (unless they already said). One short question with the trade-off:

- **Pseudonymise** (default) — PII replaced by deterministic salted-hash tokens.
  Keeps full analytical utility (joins, group-bys, dedup, row-level detail), but
  the result is **still personal data** under GDPR Art. 4(5).
- **Anonymise** — direct identifiers, id columns, health and free-text columns
  are **dropped**; dates generalised (birth → decade, dates → year); numerics
  binned; **k-anonymity** enforced by suppressing rare combinations. Aims at
  leaving GDPR scope, at a real cost in detail and rows. Ask for the k threshold
  too if the user cares (default 5).

Then run the helper and work only on its output:

```bash
python scripts/data_masking.py <file> [--out masked.csv]            # pseudonymise
python scripts/data_masking.py <file> --anonymize --k 5 [--out ...] # anonymise
```

It infers the schema, detects likely-PII columns (names, value patterns, health
terms), and prints only structure + protected values; with `--out` it writes a
protected copy safe for analysis. Read `references/data-masking.md` for the
method and its honest limits (pseudonymised data is still personal data;
anonymisation here is strong risk reduction, not a legal guarantee — verify
quasi-identifiers and context). If code execution is unavailable, say you cannot
process the raw file safely and ask for a masked export — do not open it anyway.

This mode composes with the others: write loaders/models/pipelines from the
masked schema (the code will run on real data on the user's machine), and cite
GDPR Art. 25/32 when recommending which columns to mask before sharing.

---

## Review mode (audit an existing repo)

### 1. Scope the review

Confirm which frameworks apply and which repo. Default to all four (AI Act, GDPR,
NIS2, secure-development/SSDLC). AI Act only truly applies if there's an AI/ML
component (else mark it `Not applicable`); NIS2 organisational applicability is a
legal premise, not a code finding; secure-development practices apply to any
codebase.

### 2. Inventory the repo

Build a factual picture first. If code execution is available, run the optional
helper for a fast, deterministic pass (it never prints secret values):

```bash
python scripts/repo_inventory.py <repo-path>
```

The script is just an accelerator — if you can't run it, do the same inventory by
reading the repo directly. Either way, read what matters by hand: entrypoints,
auth/session code, logging, data-access layers, IaC/Docker/CI, dependency
manifests, backup/monitoring config. Note what personal data is processed, how
authentication and secrets work, and whether encryption/logging exist.

### 3. Map to requirements

Open each applicable reference file and work through it. For every item assign a
**Status** (`Compliant` / `Gap` / `Partial` / `N/A` / `Out-of-scope (org)`), cite
**Evidence** (file:line — no evidence ⇒ don't claim `Compliant`), and for gaps a
**Severity** (`High`/`Medium`/`Low`, weighted by exposure and data sensitivity)
and a one-line **Remediation**. Apply the double-counting rule above: one full
finding in the most specific table, cross-references elsewhere.

### 4. Write the report

Fill in `assets/review-template.md` exactly. Save it where the user asks; if not
specified, propose a path (e.g. `compliance/<repo>.md`) and confirm. Lead with the
summary and highest-severity gaps.

**Output:** a verdict summary (one paragraph + a counts line like
`High: 2 · Medium: 5 · Low: 3`), one table per framework, then a prioritised
remediation list.

---

## Examples

**Design/build:** "Build a small FastAPI service to store customer contacts,
GDPR-compliant." → Scope: personal data (names, emails) ⇒ GDPR + NIS2 baseline +
SSDLC, no AI. Build with: secrets from env, TLS, hashed auth, access control, a
delete endpoint (Art. 17), a documented data-map, access logging, SAST and
dependency scanning in CI. Deliver the code + a "compliance built in" summary
noting what's done and that lawful-basis/consent is an org decision.

**Review:** "Do a compliance review of the `payments-api` repo against NIS2 and
GDPR." → Inventory, map to `nis2.md` + `gdpr-quickcheck.md` (+ SSDLC baseline),
produce the table report with severities and a prioritised fix list. Example rows:

> | Requirement | Status | Evidence | Sev. | Remediation |
> |---|---|---|---|---|
> | NIS2 Art. 21(2)(h) Cryptography | Compliant | TLS enforced `config/server.py:20`; bcrypt `auth.py:55` | — | — |
> | NIS2 Art. 21(2)(d) Supply chain | Gap | no dependency scanning in CI | Medium | Add automated dependency scanning to the pipeline |
> | GDPR Art. 30 Records / data inventory | Gap | no documented list of PII fields | Medium | Add a data-map doc enumerating personal-data fields & purpose |
