---
name: tax-invoice-scan
description: "Tax and issued documents: rate dating, tax base, rounding level, credit notes, e-invoice validation, chains."
kind: skill
pack: business
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: tax-invoice-scan

## Premise

Tax is the money rule a third party writes: the authority sets the rate and its effective date, the base, whether a price includes the tax, the rounding level the document must satisfy, and what an issued document may never become again. Code that hard-codes a rate, taxes the pre-discount amount, rounds per line where the emitted totals must round per category, edits an issued invoice in place, or never runs the authority's validator produces documents that look right and are rejected or non-compliant at volume. E-invoicing makes this a dated surface: EN 16931 / Peppol BIS 3.0.21 rules BR-CO-10…17 and BR-DEC-* are fatal (a one-cent mismatch rejects the invoice); Belgium (Peppol B2B, 2026-01-01), Poland KSeF (Feb/Apr 2026), France (from 2026-09-01), Germany (issuing from 2027/2028), the UAE (2027-01-01 for revenue ≥ AED 50m), Saudi ZATCA phase 2 and Egypt's ETA e-receipts each add code-visible fields (dates from the business research, secondary sources marked `[K?]` in § Sources).

This skill owns research ids TX-1…TX-6 and IV-1…IV-5, shipped as `BIZ-<id>`. **It never states an authority's rule from memory.** The tax policy register names its source; a row whose rule has no cited authority document is `[report-flagged]`.

**Every finding cites the code `<file:line>` + the tax policy row it breaks (or `UNDECLARED`) + the seeded document and what came out + the oracle (a golden invoice, the authority's validator exit) or the test that would settle it + the fix in the project's own tax module.** A grep hit is a candidate. "Tax looks right" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/business.md`](../../../../snippets/precedents/business.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Business, V457–V462 and V480.

## The rule

A candidate is a finding when all four hold:

1. **Reachable.** The code computes, stores, renders or transmits a tax amount or an issued document on a production path: checkout, POS, invoice run, credit-note creation, e-invoice submission, PDF render, export.
2. **Version and authority read.** The tax engine SDK and e-invoice libraries come from the lockfile (F1). The authority's rule comes from the authority's own document (the VAT Directive articles, the Peppol rule id, the authority's SDK or spec page), cited with its date. Without it the row is Unconfirmed — never a hard-coded table of law.
3. **No existing control, across files.** A tax engine called with the address and the tax code; a rate table with effective dates and the rate persisted on each line; a status guard that makes issued documents read-only; the authority's validator in CI.
4. **The oracle fired, or the fact is two-ended.** A golden invoice or the validator failed on the real builder, or the static fact cites both ends (the rate constant and the invoice line that does not store it; the per-line rounding and the document total computed from unrounded lines).

## Boundaries

- **Gapless numbering from a sequence, per-series uniqueness** → database `schema-integrity-scan` §11, when the database pack is installed; this skill supplies the jurisdiction fact its finding needs (the tax policy row: which authority requires consecutive numbers). Without the pack the row is listed tagged `numbering (owner pack database not installed)`.
- **Cascade from a user or tenant into invoices; invoices erased by an account-deletion flow** → database `schema-integrity-scan` §2 (the FK) and `ledger-scan` §8 (the deletion flow, this pack).
- **Float money, rounding arithmetic in code** → code-quality `correctness-smell-scan` §4, which reads this skill's rounding-level row; **Decimal or minor units changed on the wire** → backend `wire-format-scan` §1/§4. Each when installed, tagged otherwise.
- **A PDF or template rendering defect** (layout, fonts, a missing field in the template) → the document-generation domain overlay when installed; this skill owns the values the template is given.
- Same pack: the **money policy** (mode, point, exponent) → `pricing-rule-scan` §1; **discount composition and the eligibility base** → `pricing-rule-scan` §4/§6 (§2 here owns the tax base after them).

## Read the policy first — the tax policy register

Written into the run folder (`$OUT/tax-policy.md`), never into the audited repo.

| Field | Value | Source |
|---|---|---|
| Jurisdictions served | e.g. EG (B2C e-receipts), SA (B2B + B2C) | ADR / settings / the tax engine config |
| Rate table and effective dates | where rates live; `valid_from`/`valid_to` or immutable rate rows | the rate entity or the engine |
| Inclusive / exclusive | per price list, per line | the price or line field (grep 3) |
| Rounding level | per line, per category, per document — and the authority rule that allows it | the authority's document |
| Tax point / issue date | which instant, in which zone | the authority's document + the business zone row |
| E-invoice standard | EN 16931 / Peppol BIS 3.0.21, XRechnung, ZATCA, ETA, KSeF, none | builders (grep 9a) |
| Chain fields | previous-document hash or UUID, counter — required or not | the authority's spec (`[K?]` until read) |

Rounding is national, not EU-wide: the VAT Directive prescribes no method and the CJEU left it to member states (*Ahold*, C-484/06, 2008). Stripe's line-level vs invoice-level choice exists only for manual tax rates; automatic Stripe Tax sums, then rounds. So per-line rounding is a policy question with the validator as the oracle, not a defect by shape ([`precedents/business.md`](../../../../snippets/precedents/business.md) §3).

## Adapt to the codebase — the lanes

| Lane | Tax computation (decoy) | Issued-document shape | Validator / oracle |
|---|---|---|---|
| **TypeScript** — NestJS + MikroORM / Prisma / TypeORM / Drizzle; raw SQL in template strings | a tax module over integer minor units; Stripe Tax `automatic_tax` / Avalara `createTransaction` with address + tax code ([`precedents/business.md`](../../../../snippets/precedents/business.md) §8) | an `Invoice`/`Receipt` entity with a status enum; UBL/CII built with xmlbuilder2 or a template | KoSIT, Peppol Schematron (Saxon-HE), the authority's preprod |
| **Python** — Django + DRF, SQLAlchemy | `Decimal` with `quantize(..., rounding=)`; django-money | drafthorse / factur-x for CII/ZUGFeRD; lxml builders | the same CLIs; dbt tests on the reporting copy |
| **Ruby** — Rails | `BigDecimal`; avatax / taxjar-ruby gems | AASM or a status column on `Invoice` | — |
| **PHP** — Laravel | brick/money with explicit `RoundingMode`; Cashier delegates tax to Stripe | horstoeko/zugferd, josemmo/einvoicing | — |
| **Java / Kotlin** — Spring, JPA | `BigDecimal.setScale(2, RoundingMode.X)` | Mustang (ZUGFeRD), ph-ubl | the validator in the Maven build |
| **Go / .NET** | shopspring `Round`/`RoundBank`; `decimal` + `MidpointRounding` | hand-built XML | — |

| Authority lane | Code-visible requirement | Oracle (run offline when the project vendors it) |
|---|---|---|
| **EN 16931 / Peppol BIS 3.0.21** (BE, DE XRechnung, UAE PINT AE later) | line net = price ÷ base qty × qty + charges − allowances, parts rounded separately, 2 decimals; BR-CO-10…17 sums; BR-CO-17 category tax rounded to 2 dp; BT-111 VAT in accounting currency | KoSIT validator 1.6.3 + XRechnung config 3.0.2: `java -jar validator-<v>-standalone.jar -s scenarios.xml -r <repo> -o <out> invoice.xml` (non-zero exit on reject; flags vary — `--help`) |
| **ZATCA (Saudi Arabia)** | UUID, ICV counter per CSID, PIH = SHA-256 of the previous invoice (zero hash first), mandatory B2C QR; standard invoices cleared, simplified reported within 24 h `[K?]` | the Fatoora SDK CLI (`fatoora -validate -invoice <file>` — flags `[K?]`, read `--help`); proprietary terms: `NOT-RUN` unless the project already vendors it |
| **Egypt ETA** | UUID, seller and buyer tax ids, signature; e-receipts with `previousUUID` / `referenceUUID` `[K?]` | the authority's preprod environment (`NOT-RUN` offline) |
| **Tax engine delegation** (Stripe Tax, Avalara, TaxJar, Vertex) | address and tax code on the call; TaxRate rows immutable (Stripe: create new, archive old) | the engine's sandbox; a recorded golden response |

## Pre-flight greps

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; F1 and grep 0 build the register. Every `rg` names its path; include globs come first, exclusions last; exclusions start with `**/` because globs match the root you pass. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Tax identifiers are bounded by a non-letter or a camelCase edge — the bare substring `tax|vat|gst` matches `syntax`, `private`, `activate` (measured below).

```bash
ROOTS=(.)   # server code; in a monorepo name the apps: ROOTS=(apps/api/src). Manifests and CI files always search .
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/tax-invoice.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,rb,php,java,kt,go,cs}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,seeds,seeders}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/*.test-data.*' -g '!**/*.fixture*.*' -g '!**/test_*.py' -g '!**/*_test.go'
   -g '!**/{migrations,migration,db/migrate}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.min.*')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')
fl() { rg -l --pcre2 "$1" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$OUT/$2.txt"; ck "$2" $?; F=(); while IFS= read -r f; do F+=("$f"); done < "$OUT/$2.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none"); }
TAXID='(?<![A-Za-z])(tax|vat|gst)(?=[A-Z_]|\b)|\b(tax|vat|gst)[A-Z_]\w*|(?<=[a-z])(Tax|Vat|VAT|Gst|GST)(?=[A-Z_]|\b)|\b(TAX|VAT|GST)(?=_|\b)'
NOW='(new Date\(|Date\.now\(|\bnow\b|timezone\.now|datetime\.(now|utcnow)|Time\.(now|current)|LocalDate\.now|Instant\.now|DateTime\.(Now|UtcNow|Today)|CURRENT_(DATE|TIMESTAMP))'
# F1 tax engines and e-invoice libraries — ranges from manifests (gate 2)
h F1; rg -n --no-heading --pcre2 '"(stripe|avatax|@avalara/[\w-]+|taxjar|@vertexinc/[\w-]+|xmlbuilder2|libxmljs2?|xml-crypto|node-forge|qrcode)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .; ck F1a $?
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(avalara|taxjar|stripe|lxml|signxml|drafthorse|factur-x)\b\s*[=<>~!^]|^\s*gem\s+["\x27](avatax|taxjar-ruby|stripe)["\x27]|"(avalara/avataxclient|horstoeko/zugferd|easybill/zugferd-php|josemmo/einvoicing)"\s*:|\b(mustangproject|ph-ubl)\b|<PackageReference Include="(Avalara\.AvaTax|s2industries\.ZUGFeRD)' -g '**/{pyproject.toml,requirements*.txt,poetry.lock,Gemfile,composer.json,pom.xml,build.gradle*,*.csproj}' -g '!**/node_modules/**' .; ck F1b $?
# 0 THE TAX SURFACE — files with tax-named identifiers and their line counts (0a: the set §1–§6 narrow); engine calls (0b)
h 0a; rg -c --pcre2 "$TAXID" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"; ck 0a $?; fl "$TAXID" TAX
h 0b; rg -n -H --pcre2 '(?i)\b(automatic_tax|tax_behaviou?r|tax_code|taxCode|avatax|createTransaction|calculate_?tax\w*|tax\.calculations|tax_for_order|taxForOrder|tax_?rates?\.create)\b' "${F[@]}" | "${NC[@]}"; ck 0b ${PIPESTATUS[0]}
# 1 TX-1 a positive rate literal in a tax-named assignment (1a); effective-dating fields in tax files (1b: their absence is the candidate)
h 1a; rg -n -H --pcre2 '(?i)\b\w*(tax|vat|gst)_?\w*(rate|percent|pct|bps|basis_?points?)\w*\b\s*[!?]?\s*[:=]\s*(0?\.\d*[1-9]\d*|[1-9]\d{0,3}(\.\d+)?)\b' "${F[@]}" | "${NC[@]}"; ck 1a ${PIPESTATUS[0]}
h 1b; rg -n -H --pcre2 '(?i)\b(valid_?(from|to|until|since)|effective_?(from|to|at|date|on|since)|applies_?from|rate_?(start|end)s?_?(at|on)?)\b' "${F[@]}" | "${NC[@]}"; ck 1b ${PIPESTATUS[0]}
# 2 TX-2 the tax base — gross-up, back-out and tax-equals-price-times-rate shapes
h 2; rg -n -H --pcre2 '(?i)\b\w*(price|amount|total|sub_?total|net|base|gross)\w*\s*\*\s*\(\s*1\s*\+\s*\w*(tax|vat|gst|rate)\w*|/\s*\(\s*1\s*\+\s*\w*(tax|vat|gst|rate)\w*|\(\s*(100|10_?000)\s*\+\s*\w*(rate|bps?|percent|pct)\w*\s*\)|\b\w*(price|amount|total|gross|line)\w*\s*\*\s*\w*(tax|vat|gst)_?(rate|percent|pct)\w*' "${F[@]}" | "${NC[@]}"; ck 2 ${PIPESTATUS[0]}
# 3 TX-3 inclusive / exclusive carried on the price or the line
h 3; rg -n -H --pcre2 '(?i)\b(tax_?behaviou?r|(is_?)?tax_?inclusive|inclusive|prices?_?includes?_?tax|tax_?included|vat_?included|is_?gross|gross_?prices?)\b\s*[!?]?\s*(:|=(?!=)|\?\?)' "${F[@]}" | "${NC[@]}"; ck 3 ${PIPESTATUS[0]}
# 4 TX-4 every rounding call in a tax file (per line? per category? per document?) and line-tax sums
h 4; rg -n -H --pcre2 '(?i)(?<![.\w])(round\w*|quantize|setScale)\s*\(|\.(quantize|setScale|toFixed|round\w*)\s*\(|\bMath\.round\s*\(|\b(reduce|sum\w*)\s*\([^\n]*\b\w*(tax|vat|gst)' "${F[@]}" | "${NC[@]}"; ck 4 ${PIPESTATUS[0]}
# 5 TX-5 jurisdiction, reverse charge and exemption reasons
h 5; rg -n -H --pcre2 '(?i)\b(reverse_?charge\w*|tax_?exempt\w*|exempt(ion)?_?(reason|code|category)\w*|(vat|tax)_?category\w*|jurisdiction\w*|nexus|place_?of_?supply|tax_?(region|country|zone|state)\w*|ship_?(from|to)_?(country|state|address))\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 5 ${PIPESTATUS[0]}
# 6 TX-6 tax stated in the authority's currency
h 6; rg -n -H --pcre2 '(?i)\b(tax_?currency\w*|vat_?currency\w*|accounting_?currency\w*|functional_?currency\w*|TaxCurrencyCode|(tax|vat)_?amount_?(local|national|accounting|functional)\w*|BT-?111)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 6 ${PIPESTATUS[0]}
# 7 IV-1 writes to issued documents: SQL (7a), ORM (7b), delete routes (7c); the status guard in those files (7d)
DOC='(invoice|receipt|credit_?note|debit_?note|bill)'
h 7a; rg -n -U --pcre2 "(?i)\\b(update|delete\\s+from)\\s+\"?\\w*$DOC\\w*\"?\\s+(set\\b|where\\b|as\\b)" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 7a ${PIPESTATUS[0]}
h 7b; rg -n --pcre2 '\b(nativeUpdate|nativeDelete|update|delete|remove|destroy|update_all|delete_all|updateMany|deleteMany|save|upsert)\s*\(\s*\w*(Invoice|Receipt|CreditNote|DebitNote)\w*\b|\.(invoice|receipt|creditNote)\w*\.(update|delete|updateMany|deleteMany|upsert)\(|\b(Invoice|Receipt|CreditNote)\w*(\.objects\.[^\n]*|::where\([^\n]*\)\s*->|\.where\([^\n]*\)\.)(update|delete|update_all|delete_all)\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 7b ${PIPESTATUS[0]}
h 7c; rg -n --pcre2 "(?i)@Delete\\([^)]*$DOC|\\b(router|app|r)\\.delete\\(\\s*[\"\\x27][^\"\\x27]*$DOC|Route::delete\\([^)]*$DOC|^\\s*delete\\s+[\"\\x27][^\"\\x27]*$DOC|@DeleteMapping\\([^)]*$DOC|\\bdef\\s+(destroy|delete)\\w*$DOC" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 7c ${PIPESTATUS[0]}
fl "(?i)\\b(class|interface|type|table|model)\\s+\\w*$DOC\\w*|\\b(create\\s+table|from|into|update)\\s+\"?\\w*$DOC\\w*\"?" IV
h 7d; rg -n -H --pcre2 '(?i)\b(status|state)\w*\s*(===?|!==?|==|\bin\b|\bnot\s+in\b|:)\s*[^\n]{0,60}\b(issued|finali[sz]ed|posted|submitted|cleared|transmitted|locked|draft)\b|\b(is_?(draft|issued|finali[sz]ed|locked))\b' "${F[@]}" | "${NC[@]}"; ck 7d ${PIPESTATUS[0]}
# 8 IV-2 credit notes (8a: the files) and the link to the original (8b)
h 8a; rg -l --pcre2 '(?i)\b(credit_?notes?|creditnote\w*|credit_?memos?|debit_?notes?|return_?receipts?)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"; ck 8a $?
h 8b; rg -n --pcre2 '(?i)\b(original_?(invoice|document|receipt)_?(id|uuid|number|ref)?\w*|billing_?reference|BillingReference|related_?invoice\w*|parent_?invoice\w*|corrects_?invoice\w*|reference_?(uuid|document|invoice)\w*|referenceUUID|returnOf)\b\s*[!?]?\s*[:=]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 8b ${PIPESTATUS[0]}
# 9 IV-3 e-invoice builders in code (9a) vs the authority's validator in CI, scripts or tests (9b — tests are IN scope here)
h 9a; rg -l --pcre2 '(?i)\b(ubl|cii|xrechnung|zugferd|factur_?x|peppol|zatca|fatoora|e_?receipts?|e_?invoic\w*|einvoic\w*|ksef|eta_?(receipt|invoice|document)\w*)\b|\b(cbc|cac):\w+|urn:cen\.eu:en16931' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"; ck 9a $?
V9='\b(kosit|validator-configuration|schematron|fatoora\s+-validate|en16931|xrechnung|peppol-bis|xmllint|preprod)\b'
h 9b; rg -n -i --pcre2 "$V9" -g '**/{Jenkinsfile,Makefile,azure-pipelines.yml,bitbucket-pipelines.yml}' -g '**/package.json' -g '**/{test,tests,spec,e2e,__tests__,scripts}/**' -g '**/*.{spec,test}.*' -g '!**/node_modules/**' .; ck 9b $?
# CI config lives in hidden paths: rg skips them unless --hidden, and an include glob does not override that (9b-ci)
rg -n -i --pcre2 --hidden "$V9" -g '**/.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci.yml' -g '!**/.git/**' -g '!**/node_modules/**' .; ck 9b-ci $?
# 10 IV-4 chain fields — previous hash / UUID, counters; a constant empty value is the first read
h 10; rg -n --pcre2 '(?i)\b(pih|previous_?(invoice_?|document_?|receipt_?)?(hash|uuid|id)|prev_?(hash|uuid)|previousUUID|icv|invoice_?counter\w*|(invoice|document|receipt)_?hash|chain_?hash)\b\s*[!?]?\s*[:=]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 10 ${PIPESTATUS[0]}
# 11 IV-5 the issue date or tax point taken from the clock at render time (11a); party tax ids read from live settings (11b)
h 11a; rg -n --pcre2 "(?i)\\b(issue_?(date|d_?at)|issued_?(at|on)|date_?time_?issued|tax_?point|supply_?date|invoice_?date|document_?date)\\w*\\s*[!?]?\\s*[:=]\\s*[^;\\n]*$NOW" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 11a ${PIPESTATUS[0]}
h 11b; rg -n --pcre2 '(?i)\b(settings|config|tenant|company|merchant|org\w*|profile|seller)\w*\??\.(vat|tax)_?(id|number|no|registration\w*|rin)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 11b ${PIPESTATUS[0]}
```

### Measured (2026-10-19)

- **Real repo, read-only** (a NestJS 11 + Fastify + MikroORM 6 + React monorepo, `ROOTS=(apps/api/src)`): about 1 s, 0 `rg` errors, nothing written into the tree. **Before:** the old `pricing-tax-audit` tax probe (`tax|vat|gst|sales_tax`, substring, no exclusions) printed **8,409** lines — `syntax`, `private`, `activate`, migrations and tests. The eval's word-bounded identifier grep prints 125 lines today (161 when the eval ran). **After:** 0a counts **155 lines in 24 files** (it adds camelCase `lineTax…` and `VAT_`), and every later § reads only those files. F1 and 0b: no tax engine, no e-invoice library — tax is computed in-house. **§1** 1a 0 (the rate is a basis-points setting, no literal) · 1b 0. **§2** 0 shape hits; the POS tax function (read through 0a) taxes the discounted base and carves an inclusive tax out with `base × bp / (10000 + bp)` — the decoy ([`precedents/business.md`](../../../../snippets/precedents/business.md) §5 for its 5-decimal authority payload). **§3** 3 lines: the inclusive flag on the tax settings. **§4** 16 rounding calls in tax files, all through the one money module or the authority payload's 5-decimal formatter. **§7** 7b/7c 1 + 1: a delete of a *handover* receipt (a delivery document, not a fiscal one) → refuted on reading; 7d 3 status lines on the e-receipt filing. **§8** 8b 6: return receipts carry `referenceUUID` to the filed sale. **§9** 9a 7 builder files (ETA e-receipts) vs 9b 2 lines — both preprod URLs asserted in a unit test that stubs `fetch`, not a validator run → Unconfirmed until V462 runs against preprod. **§10** 1: `previousUUID: ''` on every receipt — Unconfirmed `[K?]` until the authority's receipt spec is read (eval § 3.3). **§11** 11a 1: the issue date is `submittedAt ?? new Date()` at filing — Unconfirmed until a retry is shown to re-stamp it; 11b 1: the seller's registration number read from live company settings at filing (one filing per receipt, so a snapshot by construction → Hardening).
- **Fixtures** (23 trees): 0 `rg` errors; 0a 35 lines in 9 trees. `regression-baseline` prints its `TAX_RATE_BP = 825` constant in both the base and the change (§1, read: single jurisdiction, rate in code — the policy row decides). `backend-defects`' seeded mode-less `quantize(CENT)` on VAT (BD-WF-4b, owned by backend `wire-format-scan` §4) appears in §4 beside its decoy `quantize(CENT, rounding=ROUND_HALF_UP)`; `port-pair` prints V1's per-line `round($net * rate, 2)` and V2's half-away helper applied once to `subtotal * taxRate` — the rounding-level difference is migration `semantics-parity-scan`'s I-MONEY row, corroborated here. 7a lists the admin `update invoices set status = 'void' … and status = 'issued'` (a status transition with a guard, not a content edit) and the Django `….update(status="closed")` bulk write (lifecycle, not content) — both read and closed as non-financial columns.
- **Fixture `business-rules`** (2026-10-19, same staging): 0.33 s, 0 `rg` errors, 128 lines; 0a 96 lines in 26 files. All 22 TX/IV seeds print — 19 at their line, 3 as listed files (8a the back-office credit-note module; 9a both builders validated nowhere). Decoys cleared at the read: 1a the POS rate effective-dated and persisted per line ([`precedents/business.md`](../../../../snippets/precedents/business.md) §7), 2 the inclusive carve-out on the discounted base, 4 the POS receipt and the Peppol builder summing the rounded lines they list (§3), 7b/7d the status-guarded draft edit (§15), 0b Stripe Tax with the address (§8). 9b's CI lane (`--hidden`, scoped to `.github/workflows` and `.gitlab-ci.yml`: `rg` skips hidden paths and an include glob does not override that) prints the 3 KoSIT lines of `.github/workflows/einvoice.yml`, so the validated Peppol builder clears at the read; the first run, without `--hidden`, printed 0. Noise the read clears: 11a a credit note stamped once at issue, 7a an `invoice_deliveries.sent_at` stamp.

## The 3,000-hit path

Build the register first (F1, 0a, 0b): a tax engine called with the address and the tax code closes §1, §2 and §5 for the paths that call it with **one** cited reason ([`precedents/business.md`](../../../../snippets/precedents/business.md) §8), and the read narrows to the paths that compute tax themselves. Group 0a by file and read the tax module(s) — tax is often computed in four places (cart, checkout, invoice, PDF), so list every computing file before judging one. Then, in order: §7 (issued documents; few files, critical); §9 (builder present, validator absent: one row per standard); §10 (chain fields, per document type); §1–§4 per computing file; §5/§6 per document builder; §8 and §11 last. A group closes only with the reason checked; remaining groups print `Live, unreviewed (k groups / n hits)`.

## Scans for

| § | Class (`BIZ-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | TX-1 rate constant, not effective-dated, or resolved at `now` instead of the tax point | high | V458 |
| 2 | TX-2 tax base wrong (before discount, shipping inconsistent, inclusive applied twice) | high | V459 |
| 3 | TX-3 inclusive / exclusive not carried on the price or line | medium | V459 |
| 4 | TX-4 rounding level contradicts the declared or authority rule; totals ≠ Σ lines | high | V457, V462 |
| 5 | TX-5 jurisdiction, reverse charge or exemption reason lost | high | V457 |
| 6 | TX-6 tax not stated in the currency the authority requires | medium | V462 |
| 7 | IV-1 issued document mutable; corrections by edit | critical | V460 |
| 8 | IV-2 credit note not linked, or Σ credits > original | high | V461 |
| 9 | IV-3 e-invoice never validated against the authority's rules | high | V462 |
| 10 | IV-4 chain fields not maintained where the authority requires them | high `[K?]` per authority | V480, V462 |
| 11 | IV-5 issue date / tax point from render time or the wrong zone; party ids not snapshotted | medium | V457 |

### 1. Rate constant or not effective-dated

```
BAD:   const VAT_RATE = 0.15; line.tax = line.net * VAT_RATE            // the rate the day it ships, forever
GOOD:  rate = rates.at(line.taxCategory, invoice.taxPoint); line.taxRateBp = rate.bp; line.taxMinor = …   // stored per line
```
**Read the code:** Where does the rate come from — a constant, a settings row editable in place, a dated table, an engine? Is it resolved at the **tax point** or at `now` (re-render)? Is the rate persisted on each line, so a re-render after a rate change keeps the old one? A single-jurisdiction business with a dated config and the rate persisted per line is not this class ([`precedents/business.md`](../../../../snippets/precedents/business.md) §7). **Finding when** a document issued before a rate change shows the new rate after it. **Proof:** V458 — a golden invoice dated the day before and the day after a rate change (Saudi Arabia moved 5 % → 15 % on 2020-07-01).

### 2. Tax base wrong

```
BAD:   tax = round(line.unitPrice * qty * rate)                    // before the discount
       gross = price * (1 + rate)                                  // on a price already flagged inclusive
GOOD:  base = net - allocatedDiscount; tax = inclusive ? base * bp / (10000 + bp) : base * bp / 10000
```
**Read the code:** Is the base the discounted net? Is shipping in or out of the base, and does the jurisdiction row say so? For an inclusive price, is tax carved out (`base × r / (1 + r)`) and never added? Are exempt and reverse-charge customers taxed zero with a reason (§5)? **Finding when** a cell of the base matrix (discount × shipping × inclusive/exclusive × exempt) differs from the golden. **Proof:** V459 — the base matrix through the real tax function.

### 3. Inclusive / exclusive not carried

```
BAD:   Price { amount }            // whether it includes tax lives in a developer's head
GOOD:  Price { amount, taxBehavior: 'inclusive' | 'exclusive' }; the line copies it
```
**Read the code:** Does every price list and every line carry the flag? Do the cart, the invoice and the PDF read the same flag? **Finding when** two paths treat one price differently. **Proof:** V459.

### 4. Rounding level

```
BAD:   lines.map(l => round(l.net * r)).sum() as the tax total, while the XML category tax is round(Σnet × r)   // BR-CO-14/17 mismatch
GOOD:  one declared level; the emitted document's totals computed from the same rounded parts it lists
```
**Read the code:** Per line, per category or per document — what does the policy row say, and what does the authority document allow? Are document totals computed from the rounded line parts the document lists? Do the cart, the invoice and the PDF round at the same level? **Finding when** the emitted totals fail the authority's sum rules, or two paths round one document differently. Per-line rounding where the national rule allows it is a policy ([`precedents/business.md`](../../../../snippets/precedents/business.md) §3). **Proof:** V457 golden invoices per jurisdiction, then V462 — the validator exits 0.

### 5. Jurisdiction, reverse charge, exemption

**Read the code:** Is the tax resolved from the buyer's and seller's location (or the engine's address), or one `tax_rate` per order? Does a zero-rated line carry its category and exemption reason (Peppol VAT category codes and exemption text)? **Finding when** an out-of-region or exempt buyer gets the domestic rate, or a zero-tax line has no reason. A single-jurisdiction product, documented, is not this class. **Proof:** V457 — golden invoices for a domestic, an exempt and a reverse-charge buyer.

### 6. Tax in the required currency

**Read the code:** Can a document be issued in a currency other than the accounting currency? If so, does it state the tax in the national currency with the rate used (VAT Directive Art. 230; Peppol BT-111)? **Finding when** a foreign-currency document lacks it where the authority requires it. **Proof:** V462 — the validator on a foreign-currency golden.

### 7. Issued document mutable

```
BAD:   await em.nativeUpdate(Invoice, { id }, { total })       // after status = 'issued'
       router.delete('/invoices/:id', …)
GOOD:  a status guard (drafts only) on every write path; corrections are a credit note; the DB rejects UPDATE of financial columns once issued
```
**Read the code:** For each 7a/7b write, is the target issued or draft, and is the guard (7d) on **every** write path — services, admin panels, raw SQL, bulk updates? Which columns change: amounts, lines, tax, parties (financial) or `pdf_url`, `sent_at`, `exported_at` (not)? Drafts are mutable and deletable; a void before transmission may be allowed by the authority — cite it ([`precedents/business.md`](../../../../snippets/precedents/business.md) §15). **Finding when** an issued document's financial content can change or disappear. **Proof:** V460 — edit an issued document through each writer → rejected; the only path is a credit note.

### 8. Credit note not linked or unbounded

**Read the code:** Does each credit note (or return receipt) carry the original's id or UUID (VAT Directive Art. 219; UBL `BillingReference`; ETA `referenceUUID`)? Is Σ credits per original bounded by the original, in the same transaction? **Finding when** a credit note can exist without its original, or over-credit it. **Proof:** V461 — credit 60 % twice on one invoice → the second is rejected.

### 9. E-invoice never validated

**Read the code:** For each standard a builder emits (9a), does CI, a script or a test run the authority's validator (9b) on a generated document? Is the validator's exit code checked? Passing the SDK is not authority approval (ZATCA). **Finding when** a builder ships with no validator run anywhere. **Proof:** V462 — generate a document from the real builder and run the validator offline; exit 0.

### 10. Chain fields not maintained

```
BAD:   header.previousUUID = ''            // every receipt, after the first
       pih = sha256(lastBuiltXml)         // the last *built*, not the last *persisted and accepted*
GOOD:  pih = hash(lastPersisted(deviceId)); counter = next(deviceId) in the issuing transaction, serialised per device
```
**Read the code:** Does the authority chain documents (previous hash or UUID, a counter per device or CSID) — cite its spec (`[K?]` until read)? Is the previous value read from the **persisted** last document, inside a transaction serialised per issuer? Is the hash regenerated on retry? **Finding when** a cited chaining rule is broken. Without the authority's document the row is `[report-flagged]`. **Proof:** V480 — the sequence property over N issues (one chain, no reuse, contiguous counter), then V462.

### 11. Issue date, tax point and party ids at render time

**Read the code:** Is the issue date stamped once at issue and stored, or computed at render (`new Date()` in the builder)? In which zone does the authority want it? Are seller and buyer tax ids snapshotted on the document, or read from live settings at render (11b)? **Finding when** re-rendering an old document changes its date, period or party ids. **Proof:** V457 — render, change settings and the clock, re-render: identical.

## Output

```
tax-invoice-scan — lanes: typescript (nestjs 11, @mikro-orm/core 6.6 — pnpm-lock.yaml); no tax engine, no e-invoice library in the lockfile
Tax register: $OUT/tax-policy.md — EG; rate from settings in basis points, inclusive flag on the settings; rounding: one money module;
              e-receipt builder: ETA v1.2 (pos/domain/eta-receipt.ts); validator: none in CI; chain rule: UNREAD [K?]

Findings: 0 · Unconfirmed: 2

1. src/pos/domain/eta-receipt.ts:158                                       [report-flagged]   high
   §10 IV-4 — previousUUID is '' on every receipt. Unproven link: whether the authority accepts an empty previous UUID after the
   first receipt (spec not read). Settling: the authority's receipt spec, then V480 over two receipts from one device.
2. src/pos/domain/eta-receipt.ts:1                                         [report-flagged]   high
   §9 IV-3 — an ETA receipt builder with no validator or preprod run in CI or tests. Settling: V462 against preprod (NOT-RUN offline).

Routed: invoice numbers from a sequence → database schema-integrity-scan §11 (jurisdiction fact supplied: EG)
Verification: 14 candidates → 0 findings · 2 unconfirmed · 12 refuted (self-verified; precedents §3, §5, §15)

Class coverage:
  §1  rate dating              checked (1a 0, 1b 0 → 0: one rate setting, persisted per receipt line)
  §2  tax base                 checked (2 → 0: carve-out on the discounted base)
  §3  inclusive flag           checked (3 → 0)
  §4  rounding level           checked (4 → 0: per line through the money module; the receipt totals re-sum the lines)
  §5  jurisdiction             N/A (single jurisdiction, documented)
  §6  tax currency             N/A (documents only in EGP)
  §7  issued mutable           checked (7a 0, 7b 0, 7c 0)
  §8  credit notes             checked (8a 3, 8b 2 → 0: return receipts carry referenceUUID)
  §9  validator                checked (9a 2, 9b 0 → 1 unconfirmed)
  §10 chain                    checked (2 → 1 unconfirmed)
  §11 issue date               checked (11a 0, 11b 1 → 0: seller id snapshotted at issue)
```

`[report-with-fix]`: the golden or the validator failed on the real builder and the fix is local to the project's tax module, its document model or its builder. `[report-flagged]`: one link is unproven (the authority rule not read, a writer not followed, the validator `NOT-RUN`); the row names it and the settling document. The coverage block lists **all eleven** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/business.md`](../../../../snippets/precedents/business.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. Numbers are [`precedents/business.md`](../../../../snippets/precedents/business.md) §s. The ones this skill meets most:
- §3 per-line tax rounding where the national rule or the spec allows it (*Ahold*; Peppol rounds line parts separately; Stripe manual rates) — a finding only when the emitted totals then fail the authority's sum rules, or two paths round differently.
- §5 integer minor units converted to decimal major units for an authority payload that mandates JSON numbers (a real e-receipt payload carries 5 decimals) is the carrier's format, not float money.
- §7 a hard-coded rate in a single-jurisdiction business with a dated config **and** the rate persisted on each line. §8 tax delegated to a tax engine with the address and the tax code on the call; Stripe Tax always sums, then rounds.
- §15 drafts and unissued documents are mutable and deletable under a status guard; a void before transmission may be allowed — cite the authority. §16 gaps in internal ids are fine; the legal number is a separate per-series counter (database §11's). §28 a date-only issue date stored as a `DATE` is not a time-binding issue.

## When to run

- On any diff that touches a tax computation, a rate table, a price's tax flag, an invoice / receipt / credit-note model or writer, an e-invoice builder, its CI validation step, or a tax engine call — `/audit-business`'s tax signal.
- On every whole-repo `/audit-business`, reporting all eleven §s; before a new jurisdiction, a rate change or an e-invoicing mandate date the policy row names.

## Halt conditions

- **Do not report a high or critical row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the tax policy row, the authority citation, the `file:line` and the golden — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/business.md`](../../../../snippets/precedents/business.md). Under `/audit-business` that is `@domain-model-auditor` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Never assert an authority's rule from memory** — rounding level, chaining, numbering, retention, mandate dates. Cite the authority's document with its date, or mark the row `[report-flagged]` with the document that would settle it.
- **Halt on any finding missing its anchors:** the `file:line`, the policy row, the golden or validator run, the fix in the project's own primitive.
- **Never run a validator or SDK the project does not already vendor or the user has not approved** (the ZATCA SDK's terms must be accepted); print `NOT-RUN (<why>)`. Never submit to an authority's live or preprod endpoint from an audit.
- **No proposed fix may hide the class:** never skip the validator, never widen a totals tolerance, never regenerate a golden invoice in the same change as the code, never edit an issued document to correct it.
- **Business decisions are not code fixes:** a tax rate, a tax point, a rounding level, a document format sent to an authority is the owner's call — the row names the decision and stops.
- **Do not grade a class another pack owns** (§ Boundaries). **Do not print "tax looks right"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/audit-business` dispatches this skill and folds its coverage block into its class ledger; `@domain-model-auditor` judges these rows. `pricing-rule-scan` (the money policy, the discount base) and `ledger-scan` (records retention, the deletion flow) are the neighbours in this pack.
- database `schema-integrity-scan` §2/§11, code-quality `correctness-smell-scan` §4, backend `wire-format-scan` §1/§4, when those packs are installed.

## Sources

From the business research (2026-10-19): EU VAT Directive 2006/112 consolidated 2025-04-14 (Arts 219, 226, 230, 233, 247); *Koninklijke Ahold* C-484/06 (2008) via commentary; Stripe tax-rate docs (line vs invoice rounding for manual rates, automatic tax sums then rounds, immutable TaxRate rows, discounts before exclusive tax); Peppol BIS Billing 3.0.21 and its rules (BR-CO-10…17, BR-DEC-*); KoSIT validator 1.6.3 (2026-08-20) with XRechnung configuration 3.0.2. Mandate dates (BE, PL, FR, DE, UAE, ViDA) are from secondary sources as read by the research; ZATCA field rules (UUID, ICV, PIH, QR) are from the ZATCA SDK page (2025-05-28), its developer forum and a vendor guide — `[K?]`; Egypt ETA e-receipt waves and fields are secondary — `[K?]`. A verdict that rests on a `[K?]` row is Unconfirmed until the authority's own document is read. The real-repo and fixture counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
