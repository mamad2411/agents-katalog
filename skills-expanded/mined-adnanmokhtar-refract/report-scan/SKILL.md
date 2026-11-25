---
name: report-scan
description: "Report rules: fan-out totals, one metric two ways, exclusions, currency sums, ratio SQL, books reconciliation, business day."
kind: skill
pack: business
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: report-scan

## Premise

A report is a claim about the business, and nobody re-derives it by hand. A `SUM` over a one-to-many join counts each order once per line item (Looker's own example turns 124.84 into 223.44); "revenue" on the dashboard includes cancelled orders and "revenue" in the export does not; a day bucket in the database session's zone puts the 23:30 orders of one tenant on the wrong date; an average of averages, an integer division or a zero denominator turns a rate into noise; a metric derived on read from the current status rewrites last month's figure when a row changes today. None of it fails a test that seeds three rows in UTC, and the books never get compared with the dashboard.

This skill owns research ids RP-1…RP-7, BT-1 and BT-2, shipped as `BIZ-<id>`: **whether a reported number is the business's number**, and **which zone and which calendar own a business day**. The business-zone row it keeps is the one `pricing-rule-scan` §8 (promotion windows) and `tax-invoice-scan` §11 (the tax point) read.

**Every finding cites the query or code `<file:line>` + the metric definition it breaks (or `UNDECLARED`) + the golden input (two child rows, a cancelled order, a 23:30-local row, a second currency, a zero denominator) and what came out + the oracle or the test that would settle it + the fix in the project's own query or metric helper.** A grep hit is a candidate. "The reports look right" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/business.md`](../../../../snippets/precedents/business.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Business, V469–V473 and V479.

## The rule

A candidate is a finding when all four hold:

1. **Reachable.** The query or helper feeds a dashboard, an export, a scheduled report, a payout or commission run, a customer-facing statement, or a figure an operator acts on. A one-off script that already ran and a debug endpoint behind a flag that is off fail here.
2. **The definition is read.** The metric's definition comes from `ai/business-domain.md`, a metrics layer (dbt `metrics:`, a semantic layer, a `metrics.ts` module) or the label the user sees; the business zone from settings, an ADR or the tenant model. Without one the row is `[report-flagged]` with the definition named as the gap.
3. **No existing control, across files.** A pre-aggregated CTE or `distinct on` (§ 18), a currency in the `GROUP BY`, a `NULLIF` on the denominator, a stamped event column, a reconciliation test against the ledger, a dbt `unique` test on the grain, a zone passed into every bucket.
4. **The oracle fired, or the fact is two-ended.** The golden dataset produced the wrong figure through the real query, or the static fact cites both ends: two sites computing one named metric with different filters; the bucket in `UTC` and the same report's sibling in the tenant zone.

## Boundaries

- **Query cost, missing indexes, unbounded report reads** → database `query-shape-scan` / performance, when installed; **a report that leaks another tenant's rows** → security `@tenant-isolation-reviewer` / database's tenancy fallback. Each when installed, tagged otherwise.
- **Calendar arithmetic in code** (`new Date('YYYY-MM-DD')`, DST, week-year, naive `now()`) → code-quality `correctness-smell-scan` §6; **a cron's own schedule zone** → backend `job-lifecycle-scan` §6. §8 here owns which zone the *rule* uses for "a day", not the arithmetic that implements it.
- **Float money in report code** → code-quality `correctness-smell-scan` §4; **a float column** → database `schema-integrity-scan` §4.
- **A rollup's grain and refresh, and the SQL that implements the declared zone** (`AT TIME ZONE` direction, `BETWEEN` on instants, `CONVERT_TZ` without zone tables, fixed offsets) → data-engineering `derived-data-scan` §1–§10, when installed. §8 here keeps which zone a day should use.
- **Analytics events that drift from a tracking plan, or fire before their outcome** → product `tracking-plan-scan`, when installed. This skill owns the server-side figure, not the event stream.
- Same pack: **books** — the ledger and its reconciliation with the provider → `ledger-scan` §6 (the books §6 here reconciles against); **issued invoices and credit notes** → `tax-invoice-scan`; **the status graph a report reads** → `lifecycle-scan` (RP-7 reads its stamped-event columns).

## Read the definitions first — the metric register

Written into the run folder (`$OUT/metrics.md`), never into the audited repo. One row per named metric and one business-zone row:

| Metric | Definition source | Sites that compute it | Recognised at (event) | Filters (status, test, deleted) | Zone | Currency |
|---|---|---|---|---|---|---|
| revenue | `ai/business-domain.md` § Metrics | `reports/revenue.queries.ts:40` · `exports/orders.csv.ts:88` | payment captured (`paid_at`) | excludes cancelled, refunded, test | tenant zone | per row, grouped |
| business day | settings `tenant.timezone` | — | — | — | `Africa/Cairo` per tenant | — |

Sources, in order: a metrics layer or `ai/business-domain.md`; the label the user sees plus the one helper every report calls; else `UNDECLARED`. A metric with two sites and two definitions is §2's candidate; an `UNDECLARED` metric is an enabler row, never a finding by itself.

## Adapt to the codebase — the lanes

| Lane | Aggregates (grep 0a) | Zone-aware bucket (decoy) | Fan-out guard (decoy) |
|---|---|---|---|
| **SQL in TypeScript** — MikroORM `em.execute` / Knex / Kysely / Prisma `$queryRaw` / TypeORM `query()`, lowercase multi-line template strings | `sum(`, `count(`, `avg(` in `select … join …` | `date_trunc('day', x at time zone $1)`; `(x at time zone tz)::date` | a child CTE grouped by parent before the join; `distinct on`; a join on a primary key |
| **ORM aggregates** | Prisma `groupBy` / `aggregate`, TypeORM `getRawMany` with `SUM`, Sequelize `fn('SUM')`, Django `annotate(Sum())` / `aggregate`, SQLAlchemy `func.sum`, Rails `.sum` / `.group`, Eloquent `->sum()`, EF `GroupBy().Sum()` | Django `TruncDate('created_at', tzinfo=tz)`; Rails `group_by_day(…, time_zone:)` | `Subquery`/`OuterRef` per parent; `distinct=True` on `Count` |
| **dbt / warehouse** | `models/**/*.sql` | `convert_timezone(...)` before `date_trunc` | `unique` / `dbt_utils.unique_combination_of_columns` tests on the grain in `models/**/*.yml` (read statically; this skill never runs `dbt`) |
| **Business calendar** | — | — | a maintained holiday-calendar library, a provider settlement calendar, an edited calendar table (§ 37) |

## Pre-flight greps

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; grep 0 builds the register and the report surface every § reads. Every `rg` names its path; include globs first, exclusions last; exclusions start with `**/`. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. SQL greps are case-insensitive and multi-line (`-U`): report SQL is usually lowercase in template strings.

```bash
ROOTS=(.)   # server code; in a monorepo name the apps: ROOTS=(apps/api/src). dbt projects and docs are searched from .
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/report.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,rb,php,java,kt,go,cs,sql}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,seeds,seeders}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/*.test-data.*' -g '!**/*.fixture*.*' -g '!**/test_*.py' -g '!**/*_test.go'
   -g '!**/{migrations,migration,db/migrate}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.min.*')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[)|--)')   # drops comment-only lines (SQL -- included)
AGG='(?i)\b(sum|count|avg|min|max)\s*\(|\.(aggregate|annotate)\s*\(|\b(Sum|Count|Avg)\s*\(|\bfunc\.(sum|count|avg)\s*\(|\.(sum|count|average)\s*\(\s*[:"\x27]|\b(groupBy|group_by|GROUP\s+BY)\b'
# 0 THE REPORT SURFACE — raw SQL that aggregates (0a, anywhere) plus aggregating code under report / analytics / dashboard paths; metric names (0b)
{ rg -l -U --pcre2 '(?i)\bselect\b[\s\S]{0,2000}?\b(sum|count|avg)\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"; ck 0a-sql $? >&2
  rg -l -U --pcre2 "$AGG" -g '**/*{report,analytic,dashboard,stat,metric,kpi,insight,summary,rollup,board,export,fact,leaderboard}*' -g '**/*{report,analytic,dashboard,stat,metric,kpi,insight}*/**' "${X[@]}" "${ROOTS[@]}"; ck 0a-path $? >&2
} | grep -E '\.(ts|mts|cts|js|mjs|cjs|py|rb|php|java|kt|go|cs|sql)$' | sort -u > "$OUT/AGG.txt"; h 0a; wc -l < "$OUT/AGG.txt"
F=(); while IFS= read -r f; do F+=("$f"); done < "$OUT/AGG.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none")
h 0b; rg -o -N --no-filename -i --pcre2 '\b(net_?revenue|gross_?revenue|revenue|gmv|net_?sales|gross_?sales|mrr|arr|aov|average_?order_?value|refund_?rate|return_?rate|conversion_?rate|churn_?rate|ltv|clv|take_?rate|delivery_?rate|success_?rate|cancel\w*_?rate)\b' "${F[@]}" | tr 'A-Z' 'a-z' | tr -d '_' | sort | uniq -c | sort -rn; ck 0b ${PIPESTATUS[0]}
h 0c; rg -n -i --pcre2 '^\s*(-\s+)?(name|metric)\s*:\s*\w+|\b(unique|not_null|relationships|equal_rowcount|unique_combination_of_columns|expression_is_true)\b' -g '**/models/**/*.{yml,yaml}' -g '**/metrics/**/*.{yml,yaml}' -g '!**/node_modules/**' -g '!**/target/**' . | wc -l; ck 0c ${PIPESTATUS[0]}
# 1 RP-1 fan-out — an aggregate within 400 chars before a JOIN (1a, files: read the grain); ORM aggregates over a to-many join (1b)
h 1a; rg -l -U --pcre2 '(?i)\b(sum|count|avg)\s*\([\s\S]{0,400}?\bjoin\b' "${F[@]}"; ck 1a $?
h 1b; rg -n --pcre2 '\.joins\(\s*:\w+\s*\)[^\n]*\.(sum|count|average)\(|\.annotate\([^\n]*\b(Sum|Count|Avg)\(\s*["\x27]\w+__\w+|leftJoin(AndSelect)?\([^\n]*\)[^\n]*\.(select|addSelect)\([^\n]*\b(SUM|COUNT)\(' "${F[@]}" | "${NC[@]}"; ck 1b ${PIPESTATUS[0]}
# 2 RP-2 one metric two ways — for each metric name in 0b, the files that compute it (two or more: compare their filters)
h 2; for n in revenue net_revenue gross_revenue gmv net_sales aov average_order_value mrr arr refund_rate conversion_rate churn_rate delivery_rate; do c=$(rg -l -i --pcre2 "\\b${n}\\b" "${F[@]}" 2>/dev/null | wc -l | tr -d ' '); [ "$c" -gt 1 ] && echo "$n $c"; done
# 3 RP-3 exclusions — aggregate files that never name a status, test, deleted or livemode filter (the work list)
h 3; rg --files-without-match -i --pcre2 '\b(status|state|deleted_?at|is_?deleted|is_?test|test_?mode|livemode|archived|voided|cancell?ed|refunded)\b' "${F[@]}"; ck 3 $?
# 4 RP-4 currency sums — SUM of an amount with no currency within the next 300 chars; a Django sum already grouped by currency
#   (`.values(…, "currency").annotate(Sum(…))` — the GROUP BY comes BEFORE the aggregate) is skipped ((*SKIP)(*F))
h 4; rg -n -U --pcre2 '(?i)\.values\([^)]*currency[^)]*\)\s*\.annotate\([^\n]*?\bsum\([^)\n]*\)(*SKIP)(*F)|\bsum\(\s*[\w".]*(amount|total|price|value|revenue|fee|cost|net|gross|payout|balance)\w*"?\s*\)(?![\s\S]{0,300}?currency)' "${F[@]}" | "${NC[@]}"; ck 4 ${PIPESTATUS[0]}
# 5 RP-5 ratio math in SQL — division of aggregates (5a: read the cast and the zero guard); an average of an average (5b)
h 5a; rg -n -U --pcre2 '(?i)\b(count|sum)\s*\([^()]*(\([^()]*\))?[^()]*\)\s*(::\w+\s*)?/\s*(nullif\s*\(\s*)?(count|sum)\s*\(' "${F[@]}" | "${NC[@]}"; ck 5a ${PIPESTATUS[0]}
h 5b; rg -n -U --pcre2 '(?i)\bavg\s*\(\s*(avg\s*\(|"?\w*(avg|average|rate|ratio|pct|percent|mean)\w*"?\s*\))' "${F[@]}" | "${NC[@]}"; ck 5b ${PIPESTATUS[0]}
# 6 RP-6 books reconciliation — tests or jobs that compare a report figure with the ledger, invoices or the provider (tests IN scope)
h 6; rg -l -i --pcre2 '\breconcil\w*' "${CODE[@]}" -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build}/**' "${ROOTS[@]}" | grep -iE '(report|dashboard|revenue|ledger|invoice|payout|settlement|statement|books)'; ck 6 ${PIPESTATUS[0]}
# 7 RP-7 recognition — aggregate files that filter on the current status (7a) vs the event stamps the schema already has (7b)
h 7a; rg -l -i --pcre2 '\b(status|state)\b"?\s*(=|in\b|<>|!=|not\s+in)\s*[(\x27]' "${F[@]}"; ck 7a $?
h 7b; rg -o -N --no-filename -i --pcre2 '\b(paid|confirmed|delivered|shipped|completed|cancell?ed|refunded|captured|settled|recogni[sz]ed|fulfilled|returned)_at\b' "${F[@]}" | sort | uniq -c | sort -rn; ck 7b ${PIPESTATUS[0]}
# 8 BT-1 business day — day / week / month buckets with no zone (8a); the zone policies the report surface uses (8b)
h 8a; rg -n -U --pcre2 '(?i)\bdate_trunc\(\s*\x27(day|week|month|quarter|year)\x27\s*,\s*(?![^)]*\bat\s+time\s+zone\b)[^)]*\)|\bto_char\(\s*(?![^,]*\bat\s+time\s+zone\b)[^,]*_(at|on)\b"?\s*,\s*\x27(YYYY|IYYY|MM|DD)|"?\w+_at"?\s*::\s*date\b|\b(DATE|DATE_FORMAT)\(\s*`?\w*_at`?\s*[,)]|\bTrunc(Date|Day|Week|Month)\(\s*["\x27]\w+["\x27]\s*\)|\bfunc\.date(_trunc)?\(|\bstartOf(Day|Week|Month)\(\s*new\s+Date\(\s*\)\s*\)|\bdate\.today\(\)|\bLocalDate\.now\(\s*\)|\bDate\.today\b' "${F[@]}" | "${NC[@]}"; ck 8a ${PIPESTATUS[0]}
h 8b; rg -o -N --no-filename -i --pcre2 '\bat\s+time\s+zone\s+(\x27[\w/+-]+\x27|\$\{?\w+\}?|\$\d+|:\w+|\?|\w+)' "${F[@]}" | tr 'A-Z' 'a-z' | sed -E 's/[[:space:]]+/ /g' | sort | uniq -c | sort -rn; ck 8b ${PIPESTATUS[0]}
# 9 BT-2 business days — weekday arithmetic and holiday lists (a SQL column alias `as business_day` is a name, not arithmetic)
h 9; rg -n --pcre2 '(?i)\b(?<!\bas\s)(?<!\bas\s")(business_?days?|working_?days?|add_?business\w*|workdays?|bank_?holidays?|public_?holidays?)\b|\bget(UTC)?Day\(\)\s*(===?|!==?|==|<|>)\s*[06]\b|\.weekday\(\)\s*(<|>=|in)\s*|\bisoWeekday\(\)\s*[<>=]|\bDayOfWeek\.(Saturday|Sunday|Friday|SATURDAY|SUNDAY|FRIDAY)\b|\bCalendar\.(SATURDAY|SUNDAY)\b|\bholidays?\s*[:=]\s*\[' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 9 ${PIPESTATUS[0]}
```

### Measured (2026-10-19)

- **Real repo, read-only** (a NestJS 11 + Fastify + MikroORM 6 + React monorepo with 20+ report queries in raw SQL template strings, `ROOTS=(apps/api/src)`): under 1 s, 0 `rg` errors, nothing written into the tree. 0a: **62** report files (aggregating SQL plus report-path code); the first draft, every file with `.count(` or `groupBy`, listed 312. 0b names `revenue` 25 times, with net revenue, AOV and a delivery rate once each. **§1** 1a 20 files with an aggregate before a JOIN; the ones read pre-aggregate per order in CTEs or use `distinct on` (§ 18, refuted per file). **§2** `revenue` is computed in 8 files — the definition register decides whether they are one metric. **§3** 8 aggregate files name no status, test or deleted filter (the work list). **§4** 31 `SUM` lines with no currency nearby: the product's currency policy decides them (§ 6) before any is read. **§5** 0 division-of-aggregates in SQL (rates are computed in code — code-quality §4 territory). **§6** 15 files name a reconciliation beside reports, the ledger, payouts or settlements (cash-on-delivery matching, wallet sweeps) — whether any of them compares a dashboard figure with the books is the read. **§7** 11 aggregate files filter on the current status while the schema stamps `confirmed_at`, `shipped_at`, `settled_at`, `delivered_at`, `returned_at`: a confirmation figure derived on read from the current payment status (the eval's U2) is the live RP-7 candidate, Unconfirmed until V470 runs over a golden history. **§8** 8a 1 zone-less bucket: `to_char(s."created_at", 'YYYY-MM-DD')` on shipments, in the database session zone, while 8b shows 7 buckets in a tenant zone variable and 3 in literal `'utc'` — three zone policies for "a day" (§ 20 flips): the live BT-1 candidate, Unconfirmed until V471. **§9** 0 hand-rolled weekday or holiday code.
- **Fixtures** (24 trees): 0 `rg` errors; most have no report surface (`N/A`). `slow-marketplace` prints its sales-stats and payout-reminder SQL (`select coalesce(sum(gross_cents), 0) …`, §4 — a single-currency fixture, § 6), `port-pair` its finance and reporting views on both sides of the port (§1 reads the grain of each), `ds-defects` one money `SUM`. A first draft of 0a let Grafana dashboard JSON into the surface (path-matched `dashboard`): 0a now keeps code and SQL files only.
- **Fixture `business-rules`** (2026-10-19, same staging): 0.38 s, 0 `rg` errors, 87 lines; 0a 24 report files, 0b `revenue` 8 times. All 18 RP/BT seeds print — 9 at their line (1b, 4 ×2, 5a, 5b, 8a ×2, 9 ×2), the rest as work lists the read closes: 1a the fan-out file, 2 `revenue 4` and `refund_rate 2`, 3 both files with no status, test or deleted filter, 6 no reconciliation beside the statement or the commission export, 7a both current-status filters while 7b shows the `paid_at` / `delivered_at` stamps; 8b prints three zone policies (`?`, `utc`, `asia/riyadh`). Decoys cleared at the read: 1a a CTE pre-aggregation (§ 18), 4 the SAR-only POS takings (§ 6), 9 a maintained `holidays` calendar (§ 37). §4 skips Django's `.values(…, "currency").annotate(Sum(…))`, which groups by currency before the aggregate (the first run printed both seeded per-day report files), and §9 skips an `as business_day` column alias (decoy 19 printed at first): 84 lines after both.

## The 3,000-hit path

The register decides most of a large run. Build it once (0a–0c): a single currency documented closes §4 with **one** cited reason (§ 6); a declared UTC business day for a single-zone product closes §8 (§ 20); a metrics layer with tests names the grain of every model (§1). Then, in order: §7 and §2 (few metrics, the figures people act on); §8 per report helper (one read of the zone argument covers every caller); §1 per report file (name the grain of every joined table, or the CTE that pre-aggregates); §3 per metric (its filters against its definition); §5 per ratio; §6 once (is there any reconciliation test); §9 once. A group closes only with the reason checked; remaining groups print `Live, unreviewed (k groups / n hits)` with the command that continues them.

## Scans for

Severity assumes the figure drives money (payouts, commissions, invoices, pricing), a customer-facing statement, or an operator's decision. Grade lower for an internal operational chart (§ 35).

| § | Class (`BIZ-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | RP-1 fan-out double counting | high | V469 |
| 2 | RP-2 one named metric computed two ways | medium | V470 |
| 3 | RP-3 status / test / soft-deleted rows not excluded per the definition | medium | V473 |
| 4 | RP-4 SUM across currencies | high | V472 |
| 5 | RP-5 ratio math: average of averages, integer division, zero denominators | medium | V469 |
| 6 | RP-6 dashboard never reconciled with the books | medium | V470 |
| 7 | RP-7 metric recognised at the wrong event, or derived from the current status | medium | V470 |
| 8 | BT-1 the business zone of a rule undeclared or plural | medium | V471 |
| 9 | BT-2 business days with no business-day calendar | medium | V479 |

### 1. Fan-out double counting

```
BAD:   select sum(o.total) from orders o join order_items i on i.order_id = o.id   -- each order counted once per line
GOOD:  with items as (select order_id, count(*) n from order_items group by order_id)
       select sum(o.total) from orders o left join items i on i.order_id = o.id
```
**Read the code:** For each 1a file, what is the grain of every joined table — one row per summed key, or many? Is the summed column the parent's? Is the child pre-aggregated (CTE, subquery, `distinct on`), or the join on a primary key (§ 18)? For `COUNT`, is the counted entity the join's grain (§ 34)? **Finding when** a parent-level amount or count is multiplied by a to-many join on a reachable report. **Proof:** V469 — the golden dataset with two child rows per parent through the real query: the total equals the hand total.

### 2. One metric computed two ways

**Read the code:** For each metric name with two or more sites, do the sites agree on base (gross or net of discount, tax, shipping, refunds), filters (§3), recognition event (§7), zone (§8) and currency (§4)? Are they labelled as two metrics (gross vs net — § 19)? **Finding when** one label shows two different numbers for the same period on two surfaces. **Proof:** V470 — both sites over the same golden dataset: equal, or labelled as two metrics.

### 3. Exclusions not applied per the definition

```
BAD:   select sum(total) from orders where created_at >= $1          -- cancelled, test and soft-deleted orders included
GOOD:  … and status not in ('cancelled','refunded') and not is_test and deleted_at is null   -- per the metric definition
```
**Read the code:** Which rows does the definition exclude (cancelled, refunded, test, sandbox / `livemode = false`, soft-deleted, internal accounts)? Does the query apply each, or a global filter that the raw SQL bypasses? A definition that includes them on purpose is not this class. **Finding when** the figure counts rows its definition excludes. **Proof:** V473 — a golden day with one row of each excluded kind: the figure does not move.

### 4. SUM across currencies

```
BAD:   select sum(amount) as revenue from payments where tenant_id = $1
GOOD:  select currency, sum(amount) from payments where tenant_id = $1 group by currency   -- or converted at the pinned rate
```
**Read the code:** Can rows in one sum carry different currencies (a currency column, multi-currency settings, a provider account per region)? Is the currency in the `GROUP BY`, or converted at the rate pinned to each row (`pricing-rule-scan` §3)? A documented single-currency product is not this class (§ 6). **Finding when** two currencies can meet in one sum on a reachable report. **Proof:** V472 — a golden set with two currencies: the report returns per-currency totals or a converted total equal to the hand conversion at the stored rates.

### 5. Ratio math in SQL

**Read the code:** For each 5a division, are both sides cast to a decimal type before dividing (Postgres divides integers as integers: `5/2 = 2`)? Is the denominator guarded (`NULLIF(den, 0)`)? Is `NULL` handled (`COALESCE`)? For 5b, is an average taken over averages of unequal groups? **Finding when** a rate is truncated, divided by zero, or averaged without weights. **Proof:** V469 — golden rows with an odd count, a zero-denominator group and unequal group sizes.

### 6. Dashboard never reconciled with the books

**Read the code:** Which figures are money (revenue, payouts, balances, commissions)? Is there any test or job (grep 6) that compares a day's figure with the ledger (`ledger-scan`), the invoices (`tax-invoice-scan`) or the provider's export? An operational, labelled estimate is not this class (§ 35). **Finding when** a money figure that feeds a payout, an invoice, an export or finance has no reconciliation anywhere. Without the books in the repo the row is `[report-flagged]` with the missing source named. **Proof:** V470 — the report over a golden day equals the books' total for the same day (and V467 when the books are the provider's export).

### 7. Recognised at the wrong event, or derived from the current status

```
BAD:   select count(*) from orders where status = 'confirmed' and created_at between $1 and $2   -- March's figure changes in April
GOOD:  select count(*) from orders where confirmed_at between $1 and $2                           -- stamped at the event
```
**Read the code:** Which event recognises the metric in its definition (captured, confirmed, delivered)? Does the query read a stamped column for that event (7b) or the current status of a mutable row with `created_at` as the period? Is the metric a snapshot on purpose ("currently in shipping": § 19)? **Finding when** a closed period's figure changes when a row's status changes later. **Proof:** V470 — a golden history: change a row's status after the period closes; the closed period's figure does not move.

### 8. The business zone undeclared or plural

```
BAD:   reports bucket `to_char(created_at, 'YYYY-MM-DD')` (session zone) here, `at time zone 'utc'` there, `at time zone ${zone}` elsewhere
GOOD:  one business-zone row (per tenant or global), passed into every bucket, cutoff, daily limit and expiry
```
**Read the code:** What zone does each bucket use (8b)? Is there a declared business zone (settings, a tenant field, an ADR)? Do a report, a cutoff, a daily limit and a payout day agree on it? A single-zone business with a documented UTC policy is not this class (§ 20, § 36). **Finding when** one rule's "day" depends on which query computes it, or a tenant off UTC sees rows on the wrong day. **Proof:** V471 — rows at 23:30 and 00:30 local time (and a DST change date) through every bucket: each lands on the business day.

### 9. Business days with no calendar

```
BAD:   if (d.getDay() !== 0 && d.getDay() !== 6) businessDays++     // Saturday-Sunday weekend for a Friday-Saturday region; no holidays
GOOD:  a maintained calendar per region (library, provider settlement calendar, or an edited table) behind one helper
```
**Read the code:** Which rule needs business days (SLA, settlement T+n, due dates, payout day)? Which region's weekend and holidays apply? Is the calendar maintained, and by whom (§ 37)? **Finding when** a date that money or a contract depends on is computed with a hard-coded weekend or a literal holiday list for a region it does not fit. **Proof:** V479 — a decision table per region across a weekend and a holiday.

## Output

```
report-scan — lanes: sql in typescript (@mikro-orm/core 6.6, raw template strings); dbt absent
Register: $OUT/metrics.md — revenue: 3 sites (UNDECLARED definition); business day: UNDECLARED (UTC, tenant zone and session zone in use)

Findings: 0 · Unconfirmed: 2 · Enabler: 1

1. src/carriers/infrastructure/shipment.queries.ts:147                  [report-flagged]   medium
   §8 BT-1 — day bucket in the database session zone; sibling reports bucket in the tenant zone (ops-board.queries.ts:61)
   and in 'utc' (day-rollup.queries.ts:48). Unproven link: the session zone in production. Settling: V471 at 23:30 local.
2. src/reports/domain/report-assemblers.ts:688                           [report-flagged]   medium
   §7 RP-7 — confirmations derived from the current payment status; confirmed_at exists. Settling: V470 over a golden history.
3. (register)                                                            Enabler            —
   §2 RP-2 — "revenue" computed in 3 files with no written definition; ai/business-domain.md § Metrics is the gap.

Routed: 2 → code-quality correctness-smell-scan §6 (date-only parse in a cutoff) · 1 → database query-shape-scan (unbounded export)
Verification: 26 candidates → 0 findings · 2 unconfirmed · 1 enabler · 23 refuted (self-verified; precedents §6, §18, §19)

Class coverage:
  §1 fan-out            checked (1a 20 files → 0; CTE pre-aggregation or distinct on in each)
  §2 two ways           checked (revenue 3 sites → enabler: no definition)
  §3 exclusions         checked (8 files → 0; each is a count of a filtered sub-query)
  §4 currency sums      N/A (single currency per tenant, documented in ai/business-domain.md)
  §5 ratio math         checked (5a 0, 5b 0)
  §6 books              checked (grep 6: 2 reconciliation tests, payouts only → 0 for payouts; revenue unreconciled → enabler)
  §7 recognition        checked (7a 11 files → 1 unconfirmed)
  §8 business day       checked (8a 1, 8b 3 policies → 1 unconfirmed)
  §9 business days      N/A (no weekday or holiday logic)
```

`[report-with-fix]`: the golden dataset produced the wrong figure through the real query and the fix is local to the query, the metric helper or the zone argument. `[report-flagged]`: one link is unproven (the definition `UNDECLARED`, the production session zone, the books not in the repo); the row names it and the settling oracle. The coverage block lists **all nine** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/business.md`](../../../../snippets/precedents/business.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 6 a documented single-currency product; § 18 a pre-aggregated CTE, `distinct on` or a primary-key join is not fan-out; § 34 a count whose grain is the counted entity.
- § 19 two named metrics are not drift, and a snapshot metric that says so is not §7; § 20 and § 36 a documented UTC business day for a single-zone business, or an internal UTC axis that prints its zone.
- § 35 an operational, labelled estimate needs no books reconciliation; § 37 a maintained calendar is a calendar.

## When to run

- On any diff that touches a report query, a dashboard endpoint, an export, a scheduled report, a payout or commission run, a metric helper, a time-zone setting or a business-day helper — `/audit-business`'s report signal.
- On every whole-repo `/audit-business`, reporting all nine §s; before a new market (zone, currency, weekend) or a finance export.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the register row, the `file:line` and the golden input — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/business.md`](../../../../snippets/precedents/business.md). Under `/audit-business` that is `@domain-model-auditor` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before §2–§8 when the register is unread.** A verdict on a figure without its definition and the business zone is an opinion; print the register first.
- **Run golden datasets on a scratch database or inside a rolled-back transaction**, never on a shared or production database; a probe that cannot be isolated is `NOT-RUN`. This skill never runs `dbt` or a warehouse query against a shared target.
- **No `[report-with-fix]` without the V-oracle failing on the real query** (or a two-ended static fact). A `JOIN` near a `SUM` is a candidate, not a finding.
- **No proposed fix may hide the class:** never add a `DISTINCT` inside `SUM` to mask a fan-out (it drops equal amounts), never round a rate to hide a truncation, never change a golden dataset in the same change as the query.
- **Business decisions are not code fixes:** a metric's definition shown to customers or finance, and the business zone, are the owner's call — the row names the decision and stops.
- **Do not grade a class another pack owns** (§ Boundaries). **Do not print "the reports look right"** without the coverage block.

## Related

- `/audit-business` dispatches this skill and folds its coverage block into its class ledger; `@domain-model-auditor` judges these rows. `ledger-scan` §6 (the books), `pricing-rule-scan` §3 and §8 (FX rates, promotion windows read the business-zone row) and `lifecycle-scan` (stamped events) are the neighbours in this pack.
- code-quality `correctness-smell-scan` §4/§6, backend `job-lifecycle-scan` §6, database `query-shape-scan`, product `tracking-plan-scan`, when those packs are installed.

## Sources

From the business research (2026-10-19): fan and chasm traps (Looker symmetric aggregates, 2025-07-22: 124.84 → 223.44), Postgres integer division and `round(numeric)` (Postgres 18 math functions), dbt data tests and dbt-utils 1.4.1 (`unique`, `relationships`, `equal_rowcount`, `expression_is_true`), SQLGlot as a grain-reading aid; metric-definition and recognition classes A-R1…A-R13 and business-time classes B-T4/B-T10 as catalogued there. The real-repo and fixture counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
