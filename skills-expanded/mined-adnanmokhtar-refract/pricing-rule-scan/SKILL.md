---
name: pricing-rule-scan
description: "Money rules: rounding policy, units, FX, discounts, price snapshots, promotions, refunds, proration, billing periods."
kind: skill
pack: business
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: pricing-rule-scan

## Premise

A price is a rule before it is a number. Which rounding mode, at which point, in which currency exponent; whether a percentage coupon applies to the list price or the already-discounted one; which price a refund reads; which day a billing period ends on. When the rule is undeclared, two services each pick one, and the cent leaks at a tie, a stacked coupon, a partial refund or a month end. The demo passes on `$19.99 × 1`.

This skill was `pricing-tax-audit`. Tax and issued documents moved to `tax-invoice-scan`, and the arithmetic shapes it used to re-detect (float money, `toFixed`, `Math.round(x*100)`, idempotent charges) now have runnable owners in other packs (§ Boundaries). What is left is what none of them can decide: **the rule** a price, discount, promotion, refund share or billing period must obey — research ids MP-1…MP-3, PR-1…PR-6, BL-1…BL-4, shipped as `BIZ-<id>`.

**Every finding cites the code `<file:line>` + the policy row it breaks (or `UNDECLARED`) + the seeded input and what came out + the oracle, or the test that would settle it + the fix in the project's own money module.** A grep hit is a candidate. "Pricing looks right" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/business.md`](../../../../snippets/precedents/business.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Business, V450–V456 and V477.

## The rule

A candidate is a finding when all four hold:

1. **Reachable.** A route, consumer, cron or admin action reaches the code: checkout, cart, quote, order edit, refund, renewal, invoice run. Seeds, one-off scripts and dead exports fail here.
2. **Version read.** The money library, the billing SDK and the date library come from the lockfile (F1). Defaults moved: Ruby `money` 7.0 (2026-07-31) switched the default rounding from half-even to half-up and made `default_currency` nil; decimal.js and big.js round half-up; Python `quantize`, .NET `Math.Round` and NodaMoney round half-even; Postgres `round(numeric)` rounds half away from zero. Without a lockfile the row is `UNREAD` and every version-gated verdict is Unconfirmed.
3. **No existing control, across files.** One money module imported everywhere with a stated mode; a billing platform that owns proration; a date library that clamps month ends; a price snapshot on the order line; a refund bound checked in the same transaction.
4. **The oracle fired, or the fact is two-ended.** The V-oracle failed on the real code path, or the static fact cites both ends (the writer that stores minor units and the reader that divides by 100 twice; the policy row that says half-even and the call that rounds half-up). Without one the row is `[report-flagged]` / Unconfirmed with the settling input written out.

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration.
- **Arithmetic on money in code** (float money, `parseFloat`, `toFixed` round-tripped, `Math.round(x*100)`, allocation that does not re-sum, overflow) → code-quality `correctness-smell-scan` §4, when the code-quality pack is installed; §4 reads this skill's §1 policy row for the mode and the point. Without the pack the hits are listed tagged `money arithmetic (owner pack code-quality not installed)`, never graded here.
- **A value changed on the wire** (Decimal → JSON float, output rounding, float money in a carrier) → backend `wire-format-scan` §1/§4/§5, when the backend pack is installed; otherwise tagged `wire format (owner pack backend not installed)`.
- **A price, total, quantity or coupon the client chose; check-then-act on a coupon count or a balance; Idempotency-Key on money routes; a trial checked at the wrong time** → security `logic-race-scan` §1/§2/§4/§5/§6/§10, when the security pack is installed; otherwise tagged `security-class (owner pack security not installed)`. §9 here owns the refund **arithmetic** (the share of a discounted line, the bound as a rule); the race on it is security's.
- **Money in a float column** → database `schema-integrity-scan` §4; **calendar arithmetic, DST, `new Date('YYYY-MM-DD')`** → code-quality `correctness-smell-scan` §6. Each when installed, tagged otherwise.
- Same pack: **tax rate, tax base, inclusive/exclusive, issued documents** → `tax-invoice-scan`; **ledger postings, reversal conservation** → `ledger-scan` (§7 there conserves what §9 here computes).

## Read the policy first — the money policy register

The register is written into the run folder (`$OUT/money-policy.md`), never into the audited repo. One row per amount kind: line, discount, tax, fee, commission, refund, FX, proration.

| Amount kind | Representation | Rounding mode | Rounding point | Currency exponent source | Source |
|---|---|---|---|---|---|
| line total | integer minor units | half away from zero | once, at the line | ISO 4217 table in `money/currency.ts` | ADR-0012 · `money/rounding.ts:7` |
| FX conversion | decimal(18,8) rate | `UNDECLARED` | — | — | none found |

Sources, in order: an ADR or `ai/business-domain.md`; a single money module imported by every service that computes the amount (grep 0a); the library default at the locked version (F1), marked `default`. Anything else is `UNDECLARED`. An `UNDECLARED` row is not a finding by itself — it is the enabler §1 prints for code-quality §4 to read — and makes every dependent row `[report-flagged]`.

## Adapt to the codebase — the lanes

Read the money type and its version (F1) first; a row applied to the wrong library greps for calls the code never makes. Print the lanes you ran.

| Lane | Money type and default rounding | Proration / anchor primitive (decoy) | Snapshot shape (decoy) |
|---|---|---|---|
| **TypeScript** — NestJS with MikroORM / Prisma / TypeORM / Drizzle / Sequelize / Knex; raw SQL in template strings | integer minor units in `number`/`bigint`; decimal.js / big.js half-up; dinero.js 2 (integer + scale, `allocate`); `numeric` read as a string by node-postgres, MikroORM `decimal`, TypeORM and Sequelize (correct — the conversion site is code-quality's) | date-fns `addMonths`, Luxon `plus({ months })`, Day.js `add(1,'month')` clamp the day | `unit_price`, `currency`, `tax_rate`, `discount_alloc` columns on the order line entity |
| **Python** — Django ORM + DRF, SQLAlchemy | `Decimal`; `quantize` without `rounding=` takes the context (half-even); py-moneyed / django-money | `dateutil.relativedelta(months=1)` clamps; `date.replace(month=…)` raises on day 31 | `DecimalField` copies on `OrderItem` |
| **Ruby** — Rails ActiveRecord + money-rails | `BigDecimal`; `money` 7 half-up, 6 half-even; `monetize :price_cents` | `+ 1.month` / `advance(months:)` clamp | `price_cents` + `price_currency` on the line |
| **PHP** — Laravel Eloquent + brick/money or moneyphp | `decimal:2` cast reads a string; brick/money needs an explicit `RoundingMode` | Carbon `addMonthNoOverflow` clamps; `addMonth` overflows (Jan 31 → Mar 3) | casts on `order_items` |
| **Java / Kotlin** — Spring, JPA/Hibernate, Moneta | `BigDecimal`; `setScale(n)` with one argument throws when rounding is needed; Moneta `Monetary.getDefaultRounding()` | `java.time` `plusMonths` clamps | `@Embedded` money on the line |
| **Go** — GORM + shopspring/decimal or govalues/decimal | shopspring `Round` half away from zero, `RoundBank` half-even; govalues half-even | `time.AddDate(0,1,0)` normalises Jan 31 → Mar 3 (candidate) | struct fields on the line |
| **.NET** — EF Core | `decimal`; `Math.Round` without `MidpointRounding` is `ToEven`; NodaMoney rounds to the minor unit `ToEven` | `DateTime.AddMonths` clamps | owned type on the line |
| **Billing providers** — Stripe, Chargebee, Recurly, Paddle | integer minor units on the wire (Stripe `amount`, `unit_amount`) | Stripe `proration_behavior`, `billing_cycle_anchor_config.day_of_month` (clamps short months); test clocks are the oracle | the Price object id stored on the subscription item |

A regional PSP is read as "provider X, amounts and events read from the webhook handler"; nothing is assumed from a provider not in the lockfile.

## Pre-flight greps

Run as **one** script from the repo root (bash 3.2-safe; shell state does not survive between tool calls). Grep **N** feeds §N; F1 and grep 0 are the policy every § reads first. Every `rg` names its path (`.` or `"${ROOTS[@]}"`); include globs come **first**, exclusions last (rg-glob-order); globs match the path including the root you pass, so exclusions start with `**/`. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Identifiers are bounded (`\b`, or a camelCase edge) — a bare substring is the shape that returned 8,409 lines for "tax" on a real repo.

```bash
ROOTS=(.)   # server code; in a monorepo name the apps: ROOTS=(apps/api/src services/billing). Manifests always search .
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/pricing-rule.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,rb,php,java,kt,go,cs}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,seeds,seeders}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/*.test-data.*' -g '!**/*.fixture*.*' -g '!**/test_*.py' -g '!**/*_test.go'
   -g '!**/{migrations,migration,db/migrate}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.min.*')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')   # drops comment-only lines
fl() { rg -l --pcre2 "$1" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$OUT/$2.txt"; ck "$2" $?; F=(); while IFS= read -r f; do F+=("$f"); done < "$OUT/$2.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none"); }
# F1 money, billing and date libraries — ranges from manifests, exact versions from lockfiles (gate 2)
h F1; rg -n --no-heading --pcre2 '"(decimal\.js|big\.js|bignumber\.js|dinero\.js|@dinero\.js/core|currency\.js|stripe|chargebee|recurly|@paddle/paddle-node-sdk|date-fns|luxon|dayjs|moment)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .; ck F1a $?
rg -n --no-heading --pcre2 '^\s*["\x27]?/?(decimal\.js|big\.js|bignumber\.js|dinero\.js|stripe)@\d[\w.-]*|"node_modules/(decimal\.js|big\.js|bignumber\.js|dinero\.js|stripe)":\s*\{' -g '**/{package-lock.json,pnpm-lock.yaml,yarn.lock}' -g '!**/node_modules/**' .; ck F1b $?
rg -n --no-heading -i --pcre2 '^\s*(money|money-rails|stripe|chargebee|recurly)\s+\(\d|^\s*gem\s+["\x27](money|money-rails|stripe)["\x27]|^\s*["\x27]?(py-moneyed|django-money|stripe|python-dateutil)\b\s*[=<>~!^]|\b(moneta|joda-money)\b|\b(shopspring|govalues)/decimal\b|"(brick/money|moneyphp/money|laravel/cashier[\w-]*|stripe/stripe-php)"\s*:|<PackageReference Include="(NodaMoney|Stripe\.net)"' -g '**/{Gemfile,Gemfile.lock,pyproject.toml,poetry.lock,uv.lock,requirements*.txt,pom.xml,build.gradle*,go.mod,composer.json,composer.lock,*.csproj}' -g '!**/node_modules/**' .; ck F1c $?
# 0 THE POLICY — money modules (0a, read each once: the register's source) and mode-less rounding calls or library globals (0b)
h 0a; rg -l --pcre2 '\b(function|const|let|def|fun|func|static|public|private)\s+(round\w*|\w*Round(ing)?\w*|to_?minor\w*|toMinor\w*|allocate\w*|split_?cents\w*|splitCents)\b|\b(class|struct|record)\s+(Money|Monetary|MoneyAmount)\b|\b(ROUND_HALF_\w+|RoundingMode\.\w+|MidpointRounding\.\w+)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"; ck 0a $?
h 0b; rg -n --pcre2 '\.quantize\(\s*[^,()]+(\([^()]*\))?\s*\)|\bMath\.Round\(\s*[^,()]+(\([^()]*\))?\s*\)|\.setScale\(\s*\d+\s*\)|\bDecimal\.set\(|\bBig\.(RM|DP)\s*=|\bBigNumber\.config\(|\bMoney\.(default_)?rounding_mode\s*=|\bgetcontext\(\)\.rounding\s*=|(?<![.\w])(?i:round)\(\s*[^,()]+(\([^()]*\))?\s*(,\s*\d\s*)?\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 0b ${PIPESTATUS[0]}
# 2 MP-2 unit drift — percent / bps / fraction scaled by hand (2a); an amount whose unit depends on a sibling type column (2b);
#   a hard-coded two-digit exponent in files that also carry a currency code (2c; KWD/BHD/OMR have 3, JPY/KRW 0)
h 2a; rg -n --pcre2 '(?i)\b\w*(percent|pct|bps|basis_?points?|rate)\b\s*[*/]\s*(100|10_?000)\b(?!\.\d)|\b(100|10_?000)\s*[*/]\s*\w*(percent|pct|bps|basis_?points?)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2a ${PIPESTATUS[0]}
h 2b; rg -n --pcre2 '(?i)\b\w*(discount|value|amount|fee|commission|reward|adjustment)_?(type|kind|unit|mode)\b\s*(===?|!==?|==|\bis\b|\bin\b)\s*\S|\bcase\s+["\x27]?(percent(age)?|fixed|flat|ratio)["\x27]?\s*[:=]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2b ${PIPESTATUS[0]}
fl '(?i)\bcurrency(_?code)?\b' CUR; h 2c; rg -n -H --pcre2 '(?i)\b\w*(cents|minor|amount|price|total|cost|fee|net|owed|balance|payout)\w*\)?\s*[*/]\s*100\b(?![.\d%])|\btoFixed\(\s*2\s*\)|\bdecimal_places\s*=\s*2\b|\*\s*0\.01\b' "${F[@]}" | "${NC[@]}"; ck 2c ${PIPESTATUS[0]}
# 3 MP-3 FX — conversion calls (3a); a rate stored beside a converted amount (3b: its absence is the candidate)
h 3a; rg -n --pcre2 '(?i)\b(convert\w*(currency|amount|money|price)\w*|\w*(currency|money|amount|price)_?convert\w*|exchange_?rates?|fx_?rates?|to_?currency|rate_?for|(resolve|fetch|lookup|get|load|current|latest)_?(fx_?|exchange_?)?rates?)\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 3a ${PIPESTATUS[0]}
h 3b; rg -n --pcre2 '(?i)\b(fx|exchange|conversion)_?rate(_?(at|date|source|id|used))?\b\s*[!?]?\s*[:=]|\brate_?(at|date|source|snapshot)\b\s*[!?]?\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 3b ${PIPESTATUS[0]}
# 4 PR-1 composition — discount application sites (4a); in those files, the stacking flag and the floor at zero (4b)
fl '\b\w*[dD]iscount\w*\s*[*/](?!=)|\*\s*\(?\s*1\s*-\s*\w*([dD]iscount|[pP]ercent)|(?i)\b(total|sub_?total|price|amount)\w*\s*-=\s*\w*(discount|coupon|promo|voucher)' D4; h 4a; rg -n -H --pcre2 '\b\w*[dD]iscount\w*\s*[*/](?!=)|\*\s*\(?\s*1\s*-\s*\w*([dD]iscount|[pP]ercent)|(?i)\b(total|sub_?total|price|amount)\w*\s*-=\s*\w*(discount|coupon|promo|voucher)' "${F[@]}" | "${NC[@]}"; ck 4a ${PIPESTATUS[0]}
h 4b; rg -n -H --pcre2 '(?i)\b(stackable|combinable|can_?combine|exclusive|stacking_?(policy|rule|mode))\b|\bMath\.max\(\s*0\s*,|\bmax\(\s*0\s*,|\bGREATEST\(\s*0\s*,' "${F[@]}" | "${NC[@]}"; ck 4b ${PIPESTATUS[0]}
# 5 PR-2 snapshot — a catalog price read inside refund / invoice / credit / recalculation code
h 5; rg -n --pcre2 '(?i)\b(product|catalog|variant|sku|plan|offer|listing)s?\??\.(price|unit_?price|list_?price|base_?price|amount)\w*\b' -g '**/*{refund,invoice,credit,recalc,reprice,return,receipt,statement}*.{ts,js,py,rb,php,java,kt,go,cs}' -g '**/*{refund,invoice,credit,return}*/**/*.{ts,js,py,rb,php,java,kt,go,cs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 5 ${PIPESTATUS[0]}
# 6 PR-3 eligibility base — a threshold compared with a subtotal (which subtotal: before or after the discount?)
h 6; rg -n --pcre2 '(?i)\b\w*(sub_?total|gross\w*|cart_?(total|value)|order_?(total|value)|basket_?total)\w*\s*(>=|>|<=|<)\s*\w*(free|threshold|min(imum)?_?(order|spend|amount|purchase)|tier)\w*|\b\w*(free_?ship\w*|threshold|min(imum)?_?(order|spend|amount|purchase))\w*\s*(<=|<|>=|>)\s*\w*(sub_?total|gross|cart_?total|order_?total)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 6 ${PIPESTATUS[0]}
# 7 PR-4 promotion currency — fixed-amount promotions and stored credit (is a currency carried and compared?)
h 7; rg -n --pcre2 '(?i)\b(amount_?off|fixed_?(amount|discount|value)|value_?off|credit_?amount|store_?credit\w*|gift_?card_?(amount|balance|value))\b\s*[!?]?\s*[:=]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 7 ${PIPESTATUS[0]}
# 8 PR-5 validity window — an expiry or window bound compared with the clock, in promotion code
NOW='(new Date\(|Date\.now\(|\bnow\b|timezone\.now|datetime\.(now|utcnow)|Time\.(now|current)|Date\.(today|current)|LocalDate\.now|Instant\.now|DateTime\.(Now|UtcNow|Today)|CURRENT_(DATE|TIMESTAMP))'
WIN='(expires?|expiry|expiration|valid_?(until|to|through|from)|ends?_?(at|on|date)|starts?_?(at|on|date))'
fl '(?i)\b(coupons?|promo(tion)?s?|vouchers?|gift_?cards?|referral_?codes?|campaigns?)\b' PRO
h 8; rg -n -H --pcre2 "(?i)\\b\\w*$WIN\\w*\\b[^;\\n]{0,40}(<=?|>=?)[^;\\n]{0,40}$NOW|$NOW[^;\\n]{0,40}(<=?|>=?)[^;\\n]{0,40}\\b\\w*$WIN|\\b\\w*$WIN\\w*(__(gt|gte|lt|lte)\\b|\\s*:\\s*\\{\\s*\\\$(gt|gte|lt|lte)\\b)" "${F[@]}" | "${NC[@]}"; ck 8 ${PIPESTATUS[0]}
# 9 PR-6 refund share — a refund priced from unit price × quantity (9a); refund-creating files (9b) minus files that read the prior refunds (9c)
h 9a; rg -n --pcre2 '(?i)\brefund\w*\s*[:+]?=\s*[^;\n]*\b(unit_?price|price|list_?price)\w*\b[^;\n]*\*\s*\w*(qty|quantity|count)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 9a ${PIPESTATUS[0]}
h 9b; rg -l --pcre2 '(?i)\b\w*refund\w*\s*\((?!\s*\))' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"; ck 9b $?
h 9c; rg -l --pcre2 '(?i)\b(already_?refunded|refunded_?(amount|total|cents|minor|sum)|total_?refunded|refundable\w*|remaining_?refund\w*|amount_?refunded)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"; ck 9c $?
# 10 BL-1 proration by hand, and provider settings that turn proration off or re-anchor without it
h 10; rg -n --pcre2 '(?i)\bprorat\w*|\bproration_behavior["\x27]?\s*[:=]\s*["\x27]none|\bbilling_cycle_anchor["\x27]?\s*[:=]\s*["\x27]now' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 10 ${PIPESTATUS[0]}
# 11 BL-2 month arithmetic in billing code — overflowing shapes and clamping libraries both listed (read which date it starts from)
fl '(?i)\b(billing|renew\w*|subscription|recurr\w*|installment|invoice_?run|next_?(charge|billing|payment)|period_?(start|end))\b' BIL
h 11; rg -n -H --pcre2 '\.set(UTC)?Month\(|\bget(UTC)?Month\(\)\s*\+\s*\w|\bAddDate\(\s*0\s*,\s*[1-9]|\.replace\(\s*month\s*=|\bmonth\s*[:=]\s*[\w.]*month\s*\+\s*1\b|\b(addMonths?|add_months|plusMonths|AddMonths|addMonthNoOverflow|addMonthsNoOverflow)\b|\brelativedelta\(\s*months|\.add\(\s*\d+\s*,\s*["\x27]months?["\x27]|\.plus\(\s*\{\s*months?\s*:|\+\s*\d+\.months?\b' "${F[@]}" | "${NC[@]}"; ck 11 ${PIPESTATUS[0]}
# 12 BL-3 period builders and inclusive month ends
h 12; rg -n -H --pcre2 '(?i)\b(current_?)?(period|cycle|billing_?period)_?(start|end)s?(_?(at|on|date))?\b\s*(=(?!=)|:\s*[\w.]*\()|\bendOf\(\s*["\x27]month|\bend_of_month\b|\blastDayOfMonth\b|23:59:59|\.999\b' "${F[@]}" | "${NC[@]}"; ck 12 ${PIPESTATUS[0]}
# 13 BL-4 metering files (the usage window is read in each)
h 13; rg -l --pcre2 '(?i)\b(usage_?(records?|events?)|meter(ed)?_?(events?|usage|readings?)|record_?usage|report_?usage|usage_?based)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"; ck 13 $?
```

### Measured (2026-10-19)

- **Real repo, read-only** (a NestJS 11 + Fastify + MikroORM 6 + React monorepo, `ROOTS=(apps/api/src)`, pnpm lockfile present): the block runs in about 1.3 s, 0 `rg` errors, nothing written into the tree. **Before** (the `pricing-tax-audit` probes, no exclusions): float 218 + 755 lines, rounding 836, money additions 504, charge 1,147, tax 8,409 — a candidate set no run reads. **After:** about 130 lines in total. F1 reads decimal.js 10.6.0 and bignumber.js 9.3.1 (both transitive) and no billing SDK. 0a lists 18 files, among them the one money module (`roundHalfAwayFromZero`, imported by POS "so the system has one rounding rule") — the policy row, a decoy for §1 ([`precedents/business.md`](../../../../snippets/precedents/business.md) §2); 0b prints 1 mode-less SQL `round(…)` (Postgres `round(numeric)`, half away from zero — the same mode). **§2** 2b printed 17 lines and among them the live unit-drift candidate: `discount_value` holds minor units under `fixed` and a percent under `percentage`, read by a `/ 100` in one adapter and `major()` in another — Unconfirmed until V451. 2c printed 33 lines (display and export conversions `cents / 100`; whether every accepted currency has two minor digits is the policy row's exponent source — listed as code-quality §4 corroboration). **§3** 3a 6 conversion sites, 3b 14 stored-rate fields (supplier operations store `exchangeRate`): read once, rate pinned per operation. **§5** 1 line: a counter-swap replacement priced from the live catalog — a new sale line, not a historical document → refuted. **§8** 1 line: coupon expiry compared at the instant (`expiresAt <= now`), the bound parsed with `new Date(input)` — Unconfirmed until V453 shows whether the input is a date-only day (the parse itself is code-quality §6). **§9** 9b 22 refund files, 9c 4 that read prior refunds or a refundable remainder; the POS refund share (`refundShareOf`) is the control to read first. **§11** 4 lines: one local `addMonths` that clamps from the origin (decoy, [`precedents/business.md`](../../../../snippets/precedents/business.md) §9) and a **renewal that adds months with `Date.UTC(y, m + months, d)` from the current expiry** — overflow (Jan 31 → Mar 3) and chained drift: the live BL-2 candidate, Unconfirmed until V456. §10/§12/§13 print `N/A`-grade counts (no subscription billing, 3 report-period lines, 0 metering files). A bare `src` root (the old workflow probe's path) prints `BLOCKED (rg exit 2)` on every grep — never a silent zero.
- **Fixtures** (`benchmarks/fixtures/*`, 23 trees, run from inside each): 0 `rg` errors. `regression-baseline`'s seeded silent rounding change (`int(round(amount))`, half-even) is the only 0b line in its tree; `quality-mix` prints its two proration copies (TS and Python, §10 — the divergent copy is code-quality `duplication-scan`'s, the two-policy question §1's), its billing-anchor check (§11/§12; the date-only parse is code-quality §6's) and the JPY payout `Math.round(row.amount * 100)` (2c → code-quality §4). The float-money and lost-update seeds in `feature-refund` and `review-decoys` stay with their owners: 9b lists those refund files as the work list, and no § here grades them.
- **Fixture `business-rules`** (2026-10-19; NestJS + MikroORM and Django/DRF, `ROOTS=(apps/api/src services/backoffice)`, run on the staged copy): 0.38 s, 0 `rg` errors, 107 lines. All 26 MP/PR/BL seeds print — 23 at their line (0b both mode-less roundings, 2a/2b both unit drifts, 3a both FX seeds, then 4a–12 two each), 3 as a listed file (9b the store-credit refund with 9c empty; 13 both metering files). Decoys cleared at the read: 0a the two declared policy modules ([`precedents/business.md`](../../../../snippets/precedents/business.md) §2), 3b the rate pinned at checkout, 4b the declared promotion order and floor, 10 Stripe proration and 11 `addMonths` from the anchor (§9). 2c also prints six back-office `DecimalField(decimal_places=2)` lines (cleared by the policy row: back-office invoices are EUR/USD only) and the routed `parseFloat(…) * 100` import (code-quality §4 corroboration); 2a prints a fraction-to-basis-points conversion (correct).

## The 3,000-hit path

The policy decides most of a large run. Build the register once (F1, 0a, 0b): one money module with a stated mode closes every 0b call that goes through it with **one** cited reason (`41 rounding calls: all via money/rounding.ts:7 roundHalfAwayFromZero`), and §1 then reads only the calls that bypass it. Then, in order: §9 and §5 (refund and invoice code, few files, high stakes); §2b by entity (one read of the switch and its readers per unit-bearing column); §4 by pricing module; §10–§13 by billing module (a repo with no subscription billing prints `N/A`); §3 by conversion function; §6–§8 by promotion module; §2a/§2c last, grouped by file. A group closes only with the reason checked (the module imported, the clamp read, the bound read in the same transaction), never assumed. Remaining groups print `Live, unreviewed (k groups / n hits)` with the command that continues them.

## Scans for

Severity assumes a production path that charges, refunds or bills a customer. Critical only when money is created or lost on a path a customer reaches at volume, or with production evidence.

| § | Class (`BIZ-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | MP-1 money policy undeclared, or two policies on one amount | high (enabler row when alone) | V450 |
| 2 | MP-2 unit or scale drift | high | V451 |
| 3 | MP-3 FX rate not pinned, direction, undeclared conversion rounding | high | V452 |
| 4 | PR-1 discount composition undefined | high | V453 |
| 5 | PR-2 price and terms not snapshotted on the line | high | V454 |
| 6 | PR-3 eligibility evaluated on the wrong base | medium | V453 |
| 7 | PR-4 fixed-amount promotion in another currency | medium | V453 |
| 8 | PR-5 promotion validity window | medium | V453 |
| 9 | PR-6 refund share rule | high | V477 |
| 10 | BL-1 hand-rolled proration, undeclared day count | high | V455 |
| 11 | BL-2 billing anchor drift at month end | high | V456 |
| 12 | BL-3 period gaps or overlaps | medium | V456 |
| 13 | BL-4 usage window ≠ billing period | medium | V455 |

### 1. Money policy undeclared, or two policies on one amount

```
BAD:   api: new Decimal(x).toDecimalPlaces(2)          // decimal.js default ROUND_HALF_UP
       pdf worker: round(Decimal(x), 2)                # Python: half-even — 2.125 → 2.12 on the PDF, 2.13 charged
GOOD:  one money module per amount kind with the mode written (`roundHalfAwayFromZero`), imported by the API, the worker and the renderer
```
**Read the code:** Which modules round this amount kind — the API, a worker, the invoice renderer, a report? Does each call state its mode, or take the library default at the locked version (F1)? Is there one money module every path imports (0a), or two helpers? Does a currency carry its exponent, or is `2` hard-coded? **Finding when** two live paths that touch one charged, refunded or booked amount round it differently, or a library upgrade in F1 changed the default under an unstated call. Alone, an `UNDECLARED` row is an **enabler** (printed, not graded). **Proof:** V450 — the tie corpus `0.005, 1.005, 2.675, 0.125, -2.5` at exponents 0/2/3 through every path; all paths agree with the declared mode.

### 2. Unit or scale drift

```
BAD:   discount_value numeric(12,2) holds minor units when discount_type='fixed' and a percent when 'percentage'
       const fee = amount * feeRate / 100   // feeRate is already a fraction elsewhere (0.025)
GOOD:  discount_fixed_minor bigint · discount_bps integer — one unit per column; the exponent from the currency table
```
**Read the code:** For each 2b switch, list every writer and every reader of the column (services, raw SQL, the report, the export, the PSP call). Does each branch read the same unit the writer stored? For 2a, what unit does the right operand carry where it is defined? For 2c, is the file currency-generic (multi-currency settings, a currency column) or pinned to one 2-digit currency by a documented single-currency policy ([`precedents/business.md`](../../../../snippets/precedents/business.md) §6)? A 2c hit that stays inside one expression is code-quality §4's arithmetic (corroboration); this § grades the unit once it crosses a column, a payload or a module boundary. **Finding when** one writer and one reader disagree on the unit, or a hard-coded exponent is stored or sent for a 0- or 3-digit currency the product accepts. **Proof:** V451 — write each unit through the real writer, read it through every reader; values equal.

### 3. FX rate not pinned

```
BAD:   const total = convert(order.amount, order.currency, 'USD')   // today's rate, at read time, in a report
GOOD:  order.fx_rate, order.fx_rate_at, order.fx_source stored at the transaction; reads use them; conversion rounding stated
```
**Read the code:** Is the converted amount stored with the rate, its time and its source (3b)? Is the direction explicit (`EGP→USD` vs its inverse)? Is the display rate the settle rate? Is conversion rounding a policy row? Does the ledger carry an FX leg (`ledger-scan` §5)? **Finding when** a stored or charged amount is re-converted at a later rate, or the inverse rate is used. **Proof:** V452 — convert at t1, change the rate, re-read at t2: the booked amount is unchanged; A→B→A never gains.

### 4. Discount composition undefined

```
BAD:   for (const c of body.coupons) total = c.type === 'percent' ? total * (1 - c.value) : total - c.value
GOOD:  a declared order (item-level, then order-level), an exclusive / stackable flag, Math.max(0, total) at the end
```
**Read the code:** Does the order of application come from the request array? Is a percentage applied to the list price or the running total — and does the policy say which? Is there a floor at zero and a cap at the undiscounted total (4b)? **Finding when** permuting the same coupons changes the total under a policy that says order-independent, or a total can go below zero. **Proof:** V453 — permutation metamorphic test plus `0 ≤ total ≤ undiscounted` over generated carts.

### 5. Price not snapshotted on the order line

```
BAD:   refundLine(line) { return line.product.price * line.quantity }   // today's catalog price
GOOD:  refundLine(line) { return line.unitPriceMinor * line.quantity - line.discountAllocMinor }
```
**Read the code:** Does the order line store unit price, currency, tax rate and the allocated discount? Does the refund, credit, invoice or re-calculation read them, or the live catalog (grep 5)? Analytics that intend current prices are not this class ([`precedents/business.md`](../../../../snippets/precedents/business.md) §19). **Finding when** a historical document's amount changes after a catalog price change. **Proof:** V454 — place an order, change the catalog price, refund / re-render: the amounts are unchanged.

### 6. Eligibility on the wrong base

```
BAD:   if (cart.subtotal >= FREE_SHIPPING_MIN) shipping = 0     // subtotal before the coupon; never re-checked on edit
GOOD:  threshold on the post-discount merchandise subtotal, re-evaluated after every cart mutation
```
**Read the code:** Which subtotal — before or after discounts, with or without tax and shipping — does the policy name? Is the check repeated at order placement? **Finding when** an order keeps a benefit its final base no longer qualifies for. **Proof:** V453 — the property holds after each mutation (add, remove, apply coupon).

### 7. Fixed-amount promotion in another currency

```
BAD:   coupon { amountOff: 1000 }   applied to a JPY order as ¥1000 off
GOOD:  coupon { amountOffMinor: 1000, currency: 'USD' } and a guard that the order currency matches, or per-currency amounts
```
**Read the code:** Does the promotion, gift card or store credit carry a currency, and is it compared with the order's? A single-currency store, documented, is not this class ([`precedents/business.md`](../../../../snippets/precedents/business.md) §6). **Finding when** a fixed amount is applied across currencies. **Proof:** V453 — the property over currency pairs.

### 8. Promotion validity window

```
BAD:   if (coupon.expiresAt < new Date()) reject()   // expiresAt parsed from '2026-03-08' = midnight UTC; checked at apply only
GOOD:  expiry stored as an instant in the business zone's end of day, re-checked at order commit
```
**Read the code:** Where does the bound come from — a date-only input, an instant? Which zone owns "the last day" (the business-zone row in `report-scan`'s metric register (§8 there owns it))? Is the window checked again when the order is placed? Is the end inclusive in the label and the code? **Finding when** a promotion is honoured after its end or rejected before it in the declared zone. **Proof:** V453 — clock tests at 23:59 and 00:01 business-zone time; apply → advance → place.

### 9. Refund share rule

```
BAD:   refundAmount = line.unitPrice * qty                    // ignores the order-level discount the line absorbed
       refund(body.amount)                                    // no Σ previous refunds + amount ≤ paid share
GOOD:  share = paidAllocated(line) * qty / line.qty; assert(previousRefunds + share <= paidAllocated(line))
```
**Read the code:** How is the paid share of a discounted line computed (allocation of order-level discounts)? Are fees refundable under the policy? Does every refund path (provider, store credit, wallet) read the prior refunds of the same line in the same transaction? The provider bounds its own path ([`precedents/business.md`](../../../../snippets/precedents/business.md) §26); internal store-credit and wallet refunds still need it. Races and repeated keys are security's. **Finding when** a sequence of partial refunds returns more than the paid share. **Proof:** V477 — charge → partial refunds → full refund: Σ refunds ≤ captured, net zero to the minor unit.

### 10. Hand-rolled proration

```
BAD:   credit = price * daysLeft / 30   // a 30-day month; then a full new-plan charge on top
GOOD:  subscriptions.update({ items, proration_behavior: 'create_prorations' }) — the platform owns the formula
```
**Read the code:** Does the platform own proration ([`precedents/business.md`](../../../../snippets/precedents/business.md) §9)? If hand-rolled: what day count (actual days in the period, 30, 365), what rounding, and is credit + charge netted? Does `proration_behavior: 'none'` run on upgrades by policy? **Finding when** a plan change charges or credits differently from the declared formula. **Proof:** V455 — a provider test clock across the change, or the formula golden at period day 1, 15 and the last day.

### 11. Billing anchor drift

```
BAD:   next.setMonth(prev.getMonth() + 1)    // Jan 31 → Mar 3 (JS overflow); Go AddDate(0,1,0) the same
       next = addMonths(prevPeriodEnd, 1)     // clamps, but from the previous end: Jan 31 → Feb 28 → Mar 28
GOOD:  next = addMonths(anchor, n)            // from the anchor; or the provider's billing_cycle_anchor_config
```
**Read the code:** Does the next period start from the **anchor** or from the previous period's end? Does the primitive clamp or overflow (lane table)? **Finding when** the sequence from a day-31 anchor drifts. **Proof:** V456 — the sequence from Jan 31 over 13 months, across a leap February.

### 12. Period gaps or overlaps

```
BAD:   end = endOf(start, 'month') (23:59:59.999) and next.start = addMonths(start, 1); a filter uses <= on both ends
GOOD:  half-open periods [start, end); end(n) === start(n+1)
```
**Read the code:** Are periods half-open everywhere they are compared (billing, usage, reports)? Does the builder derive `start(n+1)` from `end(n)`? **Finding when** an instant belongs to two periods or none. **Proof:** V456 — the property: generated periods tile the timeline.

### 13. Usage window ≠ billing period

**Read the code:** Which timestamp assigns a usage event to a period (event time, receipt time, `created_at`), in which zone, and what happens to an event that arrives after the period closed (late-arrival window, next-period credit)? **Finding when** a late or zone-shifted event is dropped or billed twice. **Proof:** V455 — a golden metering fixture with a late event and one at 23:59 in the business zone.

## Output

```
pricing-rule-scan — lanes: typescript (nestjs 11.2.6, @mikro-orm/core 6.6.16, decimal.js 10.6.0 — pnpm-lock.yaml); python, ruby, php, jvm, go, .net absent
Policy register: $OUT/money-policy.md — line: integer minor units, half away from zero (money/rounding.ts:7); FX: UNDECLARED
Billing: no subscription platform in the lockfile

Findings: 1 · Unconfirmed: 1 · Enabler: 1

1. src/orders/domain/order.data.ts:76                                     [report-flagged]   high
   §2 MP-2 — discount_value numeric(12,2) holds minor units for 'fixed' and a percent for 'percentage';
   2 readers branch on discount_type, the CSV export does not (exports/orders.csv.ts:41).
   Unproven link: the export's consumer. Settling: V451 — write both units, read through the export. Fix: split the column.
2. src/finance/fx.ts:58                                                    Enabler            —
   §1 MP-1 — FX conversion rounding UNDECLARED; code-quality §4 reads this row (owner pack installed).
3. src/refunds/refund.service.ts:120                                       [report-with-fix]  high
   §9 PR-6 — wallet refund path reads no prior refunds; V477 failed: 3 partial refunds of 40.00 on a 100.00 line → 120.00.
   Fix: read Σ refunds for the line inside the refund transaction; reject above the paid share.

Routed: 7 → code-quality correctness-smell-scan §4 (float arithmetic) · 1 → security logic-race-scan §6 (coupon count race)
Verification: 23 candidates → 1 finding · 1 unconfirmed · 1 enabler · 20 refuted (self-verified; precedents §2, §6, §9)

Class coverage:
  §1  money policy            checked (0a 3 modules, 0b 41 calls → 1 enabler; 38 via the one module)
  §2  unit drift              checked (2a 6, 2b 4, 2c 12 → 1 unconfirmed)
  §3  FX                      checked (3a 5, 3b 2 → 0; rate stored with every converted amount)
  §4  composition             checked (4a 9 in 3 files → 0; declared order + floor in pricing.rules.ts:88)
  §5  snapshot                checked (0 catalog reads in refund/invoice code)
  §6  eligibility base        checked (1 → 0: post-discount subtotal, re-checked at placement)
  §7  promotion currency      N/A (single-currency store, documented in ai/business-domain.md)
  §8  validity window         checked (2 → 0)
  §9  refund share            checked (9b 4 files, 9c 3 → 1 finding)
  §10 proration               N/A (no subscription billing: 0 hits, no billing SDK in the lockfile)
  §11 anchor                  N/A (same)
  §12 periods                 N/A (same)
  §13 usage window            N/A (no metering files)
```

`[report-with-fix]`: the oracle failed on the real path at the installed version and the fix is local to the project's money module, its line model or its billing call. `[report-flagged]`: one link is unproven (the policy `UNDECLARED`, a reader not followed, a version `UNREAD`); the row names it and the settling input. The coverage block lists **all thirteen** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

**Evidence register** (every reached property; carried over from `pricing-tax-audit`): `| # | Property | Edge input | Expected | Observed | Evidence |`, where Evidence is `Probe:` (a REPL or script run), `Test:` (a test that ran), `Traced:` (a read of both ends with `file:line`) or `UNVERIFIED — <the input that would settle it>`. A bare checkmark is not evidence; a fabricated observed cent is worse than an honest UNVERIFIED.

## False positives / precedents

The verifier reads [`precedents/business.md`](../../../../snippets/precedents/business.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
Numbers are [`precedents/business.md`](../../../../snippets/precedents/business.md) §s.
- §1 a `numeric` / `DECIMAL` read back as a string (node-postgres, MikroORM's `decimal` default, TypeORM, Sequelize, Eloquent `decimal:`) is correct; only a conversion on the arithmetic path is a candidate, and that is code-quality §4's.
- §2 a declared mode other than half-even (half-up, half away from zero) applied by one money module everywhere is a policy, not a defect — a real NestJS + React monorepo declares `roundHalfAwayFromZero` once and imports it from POS "so the system has one rounding rule".
- §4 `toFixed` / `Intl.NumberFormat` in the view after exact arithmetic is display. §5 integer minor units converted for an authority payload that mandates JSON numbers is the carrier's format. §6 a single-currency product, documented, with a currency constant at the boundary.
- §9 proration delegated to the billing platform, and date-fns / `java.time` / Luxon / Stripe `billing_cycle_anchor_config` clamping. §19 analytics that intend current prices. §25 fields accepted in a body but recomputed server-side. §26 the provider bounds refunds on its own path only.

## When to run

- On any diff that touches a price, discount, coupon, promotion, refund, FX, subscription, renewal or metering path, a money module, or the money library's version — `/audit-business`'s money signal.
- On every whole-repo `/audit-business`, reporting all thirteen §s; before upgrading a money library or a billing SDK across a major (F1).

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the policy row, the version line, the `file:line` and the seed — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/business.md`](../../../../snippets/precedents/business.md). Under `/audit-business` that is `@domain-model-auditor` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before any § when F1 and grep 0 are unread.** A verdict on rounding without the declared mode and the locked library version is invalid; print the register first.
- **Halt on any finding missing its anchors:** the `file:line`, the policy row (or `UNDECLARED`), the seed and the observed amount, the fix in the project's own primitive.
- **No `[report-with-fix]` without the V-oracle failing on the real path** (or a two-ended static fact). A shape alone — a decimal type, a round-once step — is not correctness.
- **No proposed fix may hide the class:** never compare money with a tolerance (`toBeCloseTo` on cents, `abs(a-b) < 0.01`), never regenerate a golden file in the same change as the code, never re-implement the billing platform's proration.
- **Business decisions are not code fixes:** changing a rounding mode or point, a discount order, a refund policy or a billing anchor is the owner's call — the row names the decision and stops.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "pricing looks right"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/audit-business` dispatches this skill and folds its coverage block into its class ledger; `@domain-model-auditor` judges these rows. `tax-invoice-scan` and `ledger-scan` (this pack) are the neighbours in § Boundaries.
- code-quality `correctness-smell-scan` §4/§6, backend `wire-format-scan` §1/§4/§5, security `logic-race-scan` §1/§2/§4/§5/§6/§10, database `schema-integrity-scan` §4, when those packs are installed.
- `distributed-systems/ai-patterns/idempotency.md` (when that pack is installed) — the idempotent-charge primitive a refund or renewal path relies on.

## Sources

Library defaults and versions are from the business research (2026-10-19): decimal.js 10.6.0 and big.js 7.0.1 (half-up), Python `decimal` (half-even context), .NET `Math.Round` (ToEven, docs 2025-07-01), NodaMoney 2.9.0, Ruby `money` 7.0/7.1.1 (UPGRADING-7.0, 2026-07-31), shopspring/decimal 1.6.0 and govalues/decimal 0.1.36, Postgres 18 math functions (`round(numeric)` half away from zero), ISO 4217 List One (2026-09-17: 0 and 3 minor-unit currencies), dinero.js 2.0.2 `allocate`; Stripe billing cycle anchors, `proration_behavior` and test clocks from Stripe's docs as read by the research; PR/BL classes from OWASP BLA Top 10 2025, WSTG 4.10 and CWE-840/837/1284 as cited there. Brick/money, Moneta and Carbon behaviour are vendor documentation not re-run (`[K?]`): a verdict that rests on one is Unconfirmed until V450 runs. The real-repo and fixture counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
