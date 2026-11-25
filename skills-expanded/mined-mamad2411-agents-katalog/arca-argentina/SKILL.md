---
name: arca-argentina
description: >-
  Current, source-backed guidance for Argentina's ARCA (formerly AFIP), federal
  taxes, Monotributo, IVA/Ganancias/Bienes Personales, autónomos, employers,
  invoicing, registrations, filings, payments, debt, notices, rentals, exports,
  cross-border cases, and common trámites; plus guarded Python clients for
  WSAA, WSFEv1 electronic invoices, and authorized taxpayer-registry queries.
  Use whenever a user asks what an Argentine tax rule means, what they must do,
  how to complete an ARCA trámite, or how to authenticate to and use a
  supported ARCA web service.
---

# ARCA Argentina

Use this skill as a dated, official-source research base and an operational safety layer. It was researched through **2026-08-15**. Explain in the user's language; preserve official Spanish names so they can find the correct portal service.

## Non-negotiable rules

1. Treat tax status, residence, dates, amounts, activities, jurisdictions, and prior filings as facts to establish—not assumptions.
2. Distinguish national ARCA obligations from provincial/CABA `Ingresos Brutos` and municipal levies. Never imply that an ARCA registration completes the other levels.
3. Use the bundled references first. Do not redo their baseline research. Perform a narrow live check against official sources for every item marked `LIVE RECHECK`, for a date after the research baseline, or when the user needs a deadline, threshold, rate, category amount, payment-plan window, form version, UI path, or currently effective rule.
4. State the tax period and the “as of” date. A present-day rule may not govern an older period.
5. Never invent a tax position, category, invoice class, deduction, exemption, deadline, payment allocation, or API code. Surface conflicts and uncertainty.
6. Separate explanation from action. Before a legally material submission, cancellation, payment, plan acceptance, deregistration, or production invoice, show what will happen and obtain the user's explicit approval.
7. Do not present this material as a binding professional opinion. Recommend a `contador público` or tax lawyer when the escalation conditions below apply.

## Route the request

Load only the documents needed for the request:

| Request | Read |
|---|---|
| Which government/tax applies; general orientation | `references/tax-system-map.md`, `references/source-policy.md` |
| CUIT, Clave Fiscal, RUT, DFE, service delegation | `references/access-registration-and-notices.md` |
| Monotributo, categories, recategorization, exclusion | `references/monotributo.md` |
| IVA, Ganancias, Bienes Personales, autónomos, companies | `references/general-regime.md` |
| Employee, retiree, SiRADIG/F.572, individual obligations | `references/individuals-and-employees.md` |
| Employer registration, F.931, payroll, casas particulares | `references/employers-and-social-security.md` |
| Ingresos Brutos, Convenio Multilateral, municipal issues | `references/provincial-and-municipal.md` |
| Official provincial portals or a Córdoba local-tax route | `references/jurisdiction-directory.md` |
| Rentals, service/goods exports, foreign income/assets, nonresidents | `references/rentals-exports-and-cross-border.md` |
| Portal invoicing, POS, voucher classes, corrections | `references/invoicing-procedures.md` |
| Returns, VEP, SCT/CCMA, debt and payment plans | `references/filings-payments-and-debt.md` |
| Certificates, deregistration, refunds, compensation, presentations | `references/common-procedures.md` |
| API setup and supported capability selection | `references/api-overview-and-credentials.md` |
| WSAA ticket authentication and certificates | `references/api-wsaa.md` |
| WSFEv1 requests, parameters, CAE and recovery | `references/api-wsfev1.md` |
| Constancia/padrón queries and access limits | `references/api-padron.md` |
| Safe CLI operation and production controls | `references/api-operations-and-safety.md` |

Read `references/source-policy.md` whenever rules conflict, a value is volatile, or research must be refreshed.

## Guidance workflow

### 1. Classify before advising

Establish only the facts needed for the branch:

- natural person, succession, company, nonprofit, or employer;
- Argentine tax residence and relevant province(s)/municipality;
- activity, start date, revenue and other applicable parameters;
- current registered taxes and status, if known;
- tax period and whether this is planning, an ordinary filing, an overdue matter, a notice, an audit, or a correction;
- for invoicing: issuer tax status, recipient tax status, transaction kind, currency, amount, date, and established point of sale.

Do not request unnecessary identifying or financial data. Redact CUITs, addresses, employee data, invoices, and notices in examples unless exact values are essential.

### 2. Build a responsibility map

Return the likely obligations by authority:

- **ARCA/federal:** registration, Monotributo or general regime, social security, federal returns, invoicing, and payment.
- **Province/CABA:** local `Ingresos Brutos` or `Convenio Multilateral`, plus local withholding/perception regimes.
- **Municipality:** safety/inspection or activity levies where applicable.

Label each item as confirmed, likely, not applicable, or fact still needed. Never silently choose Monotributo or general regime from revenue alone; other eligibility/exclusion conditions matter.

### 3. Give an executable trámite plan

For each procedure, provide:

1. prerequisites and exact service name;
2. navigation or command steps;
3. choices the user must make and their consequences;
4. submission/payment deadline and source date;
5. completion evidence to save (receipt, acuse, constancia, VEP/payment proof, CAE, or tracking number);
6. recovery path if the portal rejects, times out, or shows inconsistent status;
7. when to stop and involve a professional or ARCA support.

Never say “done” merely because a form, VEP, or request was generated. Verify the legally relevant acceptance or payment evidence.

### 4. Cite and qualify

Link the official page or consolidated rule nearest to each important claim. Say when a statement is an inference. If official pages disagree, apply the hierarchy and conflict procedure in `references/source-policy.md`; report rather than conceal the conflict.

## API capability boundary

The scripts implement a deliberately limited, inspectable SOAP client:

- WSAA: service-specific Ticket de Acceso (`token`/`sign`) with local secure caching;
- WSFEv1: health checks, live reference tables, sequence and voucher queries, and guarded **CAE** requests for supported domestic voucher types;
- `ws_sr_constancia_inscripcion`: authorized `getPersona_v2` and `getPersonaList_v2` queries.

They do **not** automate Clave Fiscal portal login, create portal authorizations, pay taxes, submit returns, issue every voucher regime, render a legally complete invoice PDF/QR, implement CAEA, item-detail WSMTXCA, export WSFEXv1, or expose arbitrary account balances/filings. Do not imply otherwise.

## Credential handoff

Never ask the user to paste a private key, key passphrase, Clave Fiscal password, certificate bundle, TA token, or TA signature into chat. Never put secrets in commands, arguments, logs, or source control.

Ask the user to load credentials locally with language like:

> Please set the ARCA variables in your own terminal or secret manager. Do not paste their values here. Tell me only when they are loaded; I will run a redacted offline check.

Required runtime variables:

```text
ARCA_ENV=homologacion                 # default; use produccion only deliberately
ARCA_CUIT=11-digit represented CUIT
ARCA_CERT_PATH=/absolute/path/certificate.pem
ARCA_PRIVATE_KEY_PATH=/absolute/path/private-key.pem
ARCA_PRIVATE_KEY_PASSPHRASE=...       # optional; keep in a secret manager
```

Optional variables are `ARCA_TA_CACHE_DIR`, `ARCA_TIMEOUT`, `ARCA_CA_BUNDLE`, `ARCA_WSAA_URL`, `ARCA_WSFE_URL`, `ARCA_PADRON_URL`, `ARCA_WSAA_DIGEST`, `ARCA_WSAA_SOAP_ACTION`, and `ARCA_OPENSSL_BIN`. Endpoint overrides are restricted to official `arca.gob.ar` and `afip.gov.ar` hosts, the exact supported service path, and a hostname consistent with `ARCA_ENV`; cross-environment overrides are rejected. Read `references/api-overview-and-credentials.md` before configuring them.

If the user uses a `.env` file, require it to be outside version control and access-restricted (for example mode `0600` on POSIX). The scripts do not load `.env` automatically; the user must export it through a trusted local mechanism.

## Running the Python tools

Use Python 3.10 or newer. Run commands from this skill directory. Install the single dependency into an isolated environment if it is not already available:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/arca.py --help
```

On Windows, use the virtual environment's corresponding `python.exe`. Do not install packages globally without the user's permission.

Use this progression:

1. `python scripts/arca.py doctor` — offline, redacted config/certificate/key check.
2. `python scripts/arca.py auth-check --service wsfe` — obtain or reuse a redacted homologation TA.
3. `python scripts/arca.py wsfe-dummy` and live parameter/POS queries.
4. Read-only voucher or padrón queries as authorized.
5. Invoice preview in homologation, then homologation issuance only after user approval.
6. Production only after the user has independently verified the portal configuration and reviewed a fresh, exact preview.

Use `python scripts/arca.py <command> --help` for exact arguments. Do not copy API request examples without querying the current parameter tables first.

## Invoice mutation protocol

Before `invoice-issue`:

1. Read `references/api-wsfev1.md` and `references/api-operations-and-safety.md`.
2. Verify the environment, represented CUIT, certificate authorization, active WS point of sale, voucher class, recipient condition, currency quote, dates, exact Decimal totals, associated voucher rules, and next number.
3. Run `invoice-preview`; show the entire non-secret preview and its environment/endpoint-bound SHA-256 to the user.
4. Ask for explicit approval to issue that exact preview. Initial setup requests or general permission are not approval for a specific legal voucher.
5. In either environment, pass `--confirm-issue --confirm-hash <fresh-preview-hash> --output <new-private-json-path>`; production additionally requires `--confirm-production`. The preview approval record is local, one-shot, and valid for 15 minutes. The code re-reads the sequence while holding a local lock; a changed sequence invalidates the hash.
6. Treat a detail as issued only when its response says approved and contains a 14-digit CAE. The CLI saves the complete response to the new mode-`0600` output path; preserve that file, CAE as a string, expiry, request hash, voucher number, and business record.

Never automatically retry `FECAESolicitar`. If transport fails after submission, the outcome is ambiguous: run `wsfe-voucher` for the exact point/type/number with a new private `--output`, then `wsfe-last`. In `FECompConsultar`, a recovered CAE appears as an approved, exact-key `ResultGet` with `EmisionTipo=CAE`, a 14-digit `CodAutorizacion`, and valid `FchVto`, not as a `CAE` field. Treat `response_error`, `key_mismatch`, or malformed results as unresolved—not absent. Resend only after the documented checks show ARCA did not consume the number.

## Escalate instead of guessing

Stop before making a definitive classification, calculation, filing, or mutation—and recommend a qualified Argentine professional—for material uncertainty involving:

- an ARCA notice, audit, assessment, exclusion, suspension, closure, injunction, or criminal/penalty exposure;
- missed or disputed deadlines, prescription, appeals, repetition, or waiver of rights;
- tax residence, permanent establishment, cross-border services/assets, transfer pricing, exchange-control interaction, or treaties;
- corporate reorganizations, trusts, estates/successions, director/shareholder transactions, or payroll disputes;
- large/sensitive transactions, special regimes, withholding/perception characterization, or a mismatch between books, portal data, and filed returns;
- any production API response whose legal outcome cannot be established safely.

You may still give a clearly qualified responsibility map, identify missing facts, preserve a deadline, and explain the official procedure at a high level. Give the user the facts, evidence, official source links, and focused questions to take to that professional.
