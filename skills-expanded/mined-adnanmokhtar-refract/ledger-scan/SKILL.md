---
name: ledger-scan
description: "Ledger rules: balanced and append-only postings, idempotent posting, balance cache, reconciliation, records retention."
kind: skill
pack: business
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: ledger-scan

## Premise

A ledger is the one place where the code may not be the source of truth about money: the entries are. Ledger practice converges on four invariants — every entry balances per transaction **and** per currency; posted entries are immutable and corrected by reversing entries; posting is idempotent on a key persisted before the first submit; a cached balance equals the fold of its entries and clearing accounts net to zero (TigerBeetle, Stripe's ledger write-up 2024-02-16, Modern Treasury, Square Books, pgledger, as read by the business research). Each is checkable with a **database-level** oracle — a constraint, a deferred trigger, a role grant, a replay, a reconciliation query — which beats reading code. Beside them sit the records of fact: invoices, orders, payments and ledger rows the law says must outlive the customer who asks to be forgotten, and the invariants (stock, balance, quota) a domain must enforce on every write path.

This skill owns research ids LG-1…LG-7, FR-1…FR-3 and DM-1/DM-2, shipped as `BIZ-<id>`. `@domain-model-auditor` keeps the invariant register DM rows are read against and judges them.

**Every finding cites the write or the missing control `<file:line>` + the ledger table or invariant it breaks + the seeded sequence and what the database accepted + the oracle (a direct-SQL probe, a replay, a reconciliation query) or the test that would settle it + the fix in the project's own posting function or schema.** A grep hit is a candidate. "The ledger looks sound" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/business.md`](../../../../snippets/precedents/business.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Business, V463–V468, V477 and V481.

## The rule

A candidate is a finding when all four hold:

1. **Reachable.** A posting service, consumer, cron, admin adjustment, backfill that runs in production, deletion flow or purge job writes the rows. A migration that ran once and a seed fail here.
2. **The schema is read, not assumed.** The ledger tables, their constraints, triggers and grants come from the schema after the last migration (grep 0; database `schema-map.py` when the database pack is installed). A ledger library or engine (TigerBeetle, Formance, pgledger) is read from the lockfile (F1): it enforces LG-1…LG-5 by construction.
3. **No existing control, across layers.** A deferred constraint trigger that sums each touched entry at commit; a role with INSERT/SELECT only; a unique `(source_type, source_id, leg)`; a balance cache written in the posting transaction plus a drift sweep; an archive before a tenant drop; a pseudonymisation path that keeps the invoice snapshot.
4. **The oracle fired, or the fact is two-ended.** A direct-SQL write that bypasses the code was accepted at commit, a replay posted twice, a reconciliation query returned rows — or the static fact cites both ends (the single-leg insert and the absence of any sum check in code and schema).

## Boundaries

- **The race on a balance, stock or limit** (check-then-act, lost update) → security `logic-race-scan` §5 and database `transaction-scan` §7/§8, when installed; §4 here owns the second source of truth (cache vs entries), not the race. Without the packs the race is listed tagged `concurrency (owner pack not installed)`.
- **Consumer dedupe, outbox, saga compensation** → distributed-systems `messaging-scan` §2, `dual-write-scan`, `workflow-scan`, when installed; §3 here owns the unique key **at the ledger**, which they corroborate.
- **FK `ON DELETE CASCADE` into records of fact; PII column mechanics, retention TTLs on PII tables** → database `schema-integrity-scan` §2 and §10, when installed. §8–§10 here own the **application** deletion flow, the legal retention period and the records-of-fact conflict with erasure.
- **Float money in a ledger column or in posting code** → database `schema-integrity-scan` §4 / code-quality `correctness-smell-scan` §4. **Status writes on a payment or order** → backend `state-transition-scan` (library) and `lifecycle-scan` (this pack, the graph). Each when installed, tagged otherwise.
- Same pack: the **refund share** a reversal posts → `pricing-rule-scan` §9 (computed there, conserved in §7 here); **issued invoices** → `tax-invoice-scan` §7; **dashboard ≠ books** reconciliation → `report-scan` §6 (this pack).

## Read the schema first — the ledger inventory

Written into the run folder (`$OUT/ledger-inventory.md`), never into the audited repo: one row per ledger-like table — `table · entity file · writers (functions that insert) · balance rule (code / CHECK / trigger / none) · immutability (trigger / grant / ORM @Immutable / none) · idempotency key (unique columns) · cache table and who writes it · currency per row or per account`. Sources: grep 0a/0b/0c, and when the database pack is installed `python3 -I -B .claude/skills/index-coverage-scan/scripts/schema-map.py . --emit=sql` (it replays the migrations, prints DDL with `-- @src` lines, and never writes into the tree); without it, the migrations as grep 0a prints them. Invariants for §11–§12 come from `@domain-model-auditor`'s register or `ai/business-domain.md`; none declared → §11 prints `N/A (no invariant register)` and names the register as the gap.

## Adapt to the codebase — the lanes

| Lane | Immutability / balance controls (decoys) | Mutation shapes (§2 candidates) | Idempotent posting (§3) |
|---|---|---|---|
| **TypeScript** — MikroORM / Prisma / TypeORM / Drizzle / Sequelize / Knex, raw SQL in template strings | a deferred constraint trigger, a `BEFORE UPDATE OR DELETE` trigger, a role grant in a migration; an aggregate that asserts balance before persist | MikroORM `nativeUpdate`/`nativeDelete`/`em.remove`; Prisma `ledgerEntry.update/delete(Many)`; TypeORM `repo.update/remove`; Drizzle `db.update(entries)`; `@UpdateDateColumn`, `paranoid: true` | a unique index in a migration; `ON CONFLICT DO NOTHING`; Prisma `upsert` on the source key |
| **Python** — Django ORM, SQLAlchemy | `CheckConstraint`; a DB trigger in a `RunSQL` migration | `Entry.objects.filter(...).update()/.delete()`, `session.delete(entry)`, `update(Entry)` | `UniqueConstraint(fields=[...])`, `get_or_create` inside `atomic()` |
| **Ruby** — Rails | `readonly?` returning true after create; a trigger in `structure.sql` | `update`, `update_column(s)`, `update_all`, `destroy`, `delete_all` | `add_index …, unique: true` |
| **PHP** — Laravel | a trigger in a migration's `DB::statement` | `->update()`, `->delete()`, `SoftDeletes` on the entry model | `->unique()`, `firstOrCreate` in a transaction |
| **Java / Kotlin** — JPA/Hibernate | Hibernate `@Immutable` on the entry entity | `@Modifying @Query("update Entry …")`, `repo.delete` | `@Table(uniqueConstraints = …)` |
| **Go / .NET** | DB triggers; EF interceptors | GORM `Update`/`Delete`; EF `Update`/`Remove` | `uniqueIndex` tags; `HasIndex(...).IsUnique()` |
| **Ledger engines** — TigerBeetle 0.17.x, Formance v2.3.x, pgledger | balanced, immutable, single-currency per ledger by construction | — | TigerBeetle: the transfer `id` is the key; `exists` counts as success |
| **Providers** — Stripe and regional PSPs | the provider's balance transactions and payouts are the external system of record (§6) | — | the provider key derived from the business id (Stripe prunes keys after ≥ 24 h) |

## Pre-flight greps

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; F1 and grep 0 build the inventory. Every `rg` names its path; include globs first, exclusions last; exclusions start with `**/`. Migrations are **out** of the code greps (`X`) and **in** the schema greps (`M`): a constraint or trigger lives there. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. SQL greps are case-insensitive and multi-line (`-U`) because raw SQL is often lowercase in template strings.

```bash
ROOTS=(.)   # server code; in a monorepo name the apps: ROOTS=(apps/api/src). Manifests and migrations always search .
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/ledger.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,rb,php,java,kt,go,cs}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,seeds,seeders}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/*.test-data.*' -g '!**/*.fixture*.*' -g '!**/test_*.py' -g '!**/*_test.go'
   -g '!**/{migrations,migration,db/migrate}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.min.*')
M=(-g '**/{migrations,migration,db/migrate}/**' -g '**/*.sql' -g '**/schema.prisma' -g '**/db/schema.rb' -g '!**/node_modules/**' -g '!**/vendor/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')
fl() { rg -l --pcre2 "$1" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$OUT/$2.txt"; ck "$2" $?; F=(); while IFS= read -r f; do F+=("$f"); done < "$OUT/$2.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none"); }
LT='(ledger|journal|posting|entries|entry_lines|wallet_?transactions?|balance_?transactions?|account_?entr(y|ies)|gl_\w+)'
# F1 ledger engines and payment providers (gate 2; §6 reads the providers)
h F1; rg -n --no-heading -i --pcre2 '"(tigerbeetle-node|@formance/[\w-]+|medici|stripe|@adyen/[\w-]+|@paypal/[\w-]+|braintree|@checkout\.com/[\w-]+|paymob\w*|moyasar\w*)"\s*:|^\s*["\x27]?(tigerbeetle|formance-sdk-python|stripe|adyen|paypalrestsdk|braintree)\b\s*[=<>~!^]|^\s*gem\s+["\x27](stripe|adyen-ruby-api-library|braintree)["\x27]|tigerbeetle-go|"stripe/stripe-php"|<PackageReference Include="(Stripe\.net|Adyen)' -g '**/{package.json,pyproject.toml,requirements*.txt,Gemfile,go.mod,composer.json,pom.xml,build.gradle*,*.csproj}' -g '!**/node_modules/**' .; ck F1 $?
# 0 THE INVENTORY — ledger tables in the schema (0a), ledger entities and table bindings in code (0b), triggers / CHECKs / grants on them (0c)
h 0a; rg -n -i --pcre2 "create\\s+table\\s+(if\\s+not\\s+exists\\s+)?[\"\\x60]?(\\w+[\"\\x60]?\\.)?[\"\\x60]?\\w*$LT\\w*|^\\s*model\\s+\\w*(ledger|journal|posting|entry|wallettransaction)\\w*\\s*\\{|create_table\\s+[:\"\\x27]\\w*$LT|Schema::create\\(\\s*[\"\\x27]\\w*$LT" "${M[@]}" .; ck 0a $?
# 0a Django lane: a table created by a migration, named by `options={"db_table": …}` or (no db_table) by the model name
rg -n -U -i --pcre2 "migrations\\.CreateModel\\(\\s*name\\s*=\\s*[\"\\x27]\\w*(ledger|journal|posting|entry|entries|wallettransaction|balancetransaction)\\w*[\"\\x27]|[\"\\x27]db_table[\"\\x27]\\s*:\\s*[\"\\x27]\\w*$LT" -g '**/migrations/*.py' -g '!**/node_modules/**' -g '!**/{.venv,venv,site-packages}/**' .; ck 0a-django $?
h 0b; rg -n --pcre2 "\\bclass\\s+\\w*(Ledger|Journal|Posting|WalletTransaction|BalanceTransaction)\\w*|(?i)\\b(table_?name|db_table|__tablename__|\\\$table|@Table\\(\\s*name)\\s*[:=(]?\\s*[\"\\x27]\\w*$LT" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 0b ${PIPESTATUS[0]}
h 0c; rg -n -i --pcre2 "create\\s+(constraint\\s+)?trigger\\s+\"?\\w+|deferrable(\\s+initially\\s+deferred)?|\\bcheck\\s*\\([^)\\n]*\\b(debit|credit|amount|balance)\\w*|\\b(revoke|grant)\\s+[\\w, ]*\\b(update|delete)\\b[^\\n]*\\bon\\b[^\\n]*$LT|before\\s+(update|delete)(\\s+or\\s+(update|delete))?\\s+on\\s+\"?\\w*$LT" "${M[@]}" .; ck 0c $?
fl "\\bclass\\s+\\w*(LedgerEntry|LedgerLine|JournalLine|JournalEntry|Posting|WalletTransaction|BalanceTransaction|Ledger)\\w*(Entity|Model|Record)?\\b|(?i)\\b(table_?name|db_table|__tablename__|\\\$table|@Table\\(\\s*name)\\s*[:=(]?\\s*[\"\\x27]\\w*$LT|\\b(insert\\s+into|update|delete\\s+from)\\s+\"?\\w*$LT\\w*\"?\\s" LED; L=("${F[@]}")   # the files that bind or write a ledger table; 1b, 2c, 3b, 5b, 7a and 10a read them
# 1 LG-1 balance asserted in code (1a); entry rows written by a single insert (1b: read whether the writer writes ≥ 2 legs and checks the sum)
h 1a; rg -n --pcre2 '(?i)\bassert\w*balanc\w*|\b\w*debits?\w*\s*(===?|!==?|==|!=)\s*\w*credits?\b|\bsum\w*debit\w*\s*(===?|!==?)|\b(unbalanced|not_?balanced|must_?balance|imbalance)\w*' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 1a ${PIPESTATUS[0]}
h 1b; rg -n -U --pcre2 "(?i)\\binsert\\s+into\\s+\"?\\w*$LT\\w*\"?|\\b(create|insert|persist|save|bulk_?create|insert_?all|createMany|insertMany|add)\\s*\\(\\s*(new\\s+)?\\w*(Ledger|Journal|Posting|Entry|WalletTransaction)\\w*\\b" "${L[@]}" | "${NC[@]}"; ck 1b ${PIPESTATUS[0]}
# 2 LG-2 UPDATE / DELETE on ledger tables: SQL (2a), ORM (2b); mutable markers on ledger entities (2c)
h 2a; rg -n -U --pcre2 "(?i)\\b(update|delete\\s+from)\\s+\"?(\\w+\"?\\.\"?)?\\w*$LT\\w*\"?\\s+(set\\b|where\\b|as\\b|using\\b)" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2a ${PIPESTATUS[0]}
h 2b; rg -n -U --pcre2 '\b(nativeUpdate|nativeDelete|update|delete|remove|destroy|update_all|delete_all|updateMany|deleteMany|update_column|update_columns)\s*\(\s*\w*(Ledger|Journal|Posting|Entry|WalletTransaction|BalanceTransaction)\w*\b|\.(ledger\w*|journal\w*|posting\w*|walletTransaction\w*)\.(update|delete|updateMany|deleteMany|upsert)\(|\b(Ledger|Journal|Posting|WalletTransaction)\w*(\.objects\.[^\n]*|::where\([^\n]*\)\s*->|\.where\([^\n]*\)\.)(update|delete|update_all|delete_all)\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2b ${PIPESTATUS[0]}
h 2c; rg -n -H --pcre2 '(?i)@UpdateDateColumn|\bonUpdate\s*:|\bparanoid\s*:\s*true|\bSoftDeletes?\b|acts_as_paranoid|\bdeleted_?at\b\s*[!?]?\s*[:=]|\bupdated_?at\b\s*[!?]?\s*[:=]' "${L[@]}" | "${NC[@]}"; ck 2c ${PIPESTATUS[0]}
# 3 LG-3 unique keys on ledger tables (3a, schema); idempotency / source keys and conflict handling in ledger code (3b)
h 3a; rg -n -i --pcre2 "\\bunique\\b[^\\n]{0,160}$LT|$LT\\w*[^\\n]{0,160}\\bunique\\b|@@unique\\(|add_index\\s+[:\"\\x27]\\w*$LT[^\\n]*unique" "${M[@]}" .; ck 3a $?
h 3b; rg -n -H --pcre2 '(?i)\b(idempotency_?key|source_?(type|id|ref)|external_?(id|ref)|event_?id|dedupe_?key|reference_?(id|key))\b|\bon\s+conflict\b|\bupsert\b|get_or_create|firstOrCreate|find_or_create' "${L[@]}" | "${NC[@]}"; ck 3b ${PIPESTATUS[0]}
# 4 LG-4 balance-cache writes (4a); a drift sweep that compares the cache with the entries (4b)
h 4a; rg -n --pcre2 '(?i)\b\w*(wallet|account|acct|ledger|holder|customer|merchant|courier)\w*\.\w*(balance|available)\w*\s*(\+|-)?=(?!=)|\bset\s+"?\w*balance\w*"?\s*=\s*"?\w*balance|\w*balance\w*["\x27]?\s*:\s*\{\s*(increment|decrement)\b|\bF\(\s*["\x27]\w*balance|->(increment|decrement)\(\s*["\x27]\w*balance' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 4a ${PIPESTATUS[0]}
h 4b; rg -n --pcre2 '(?i)\b\w*(balance_?drift|recompute_?balance|rebuild_?balance|verify_?balance|balance_?(check|audit|sweep|recon\w*)|reconcile_?balance)\w*\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 4b ${PIPESTATUS[0]}
# 5 LG-5 one transfer across two currencies (5a); currency fields in ledger code (5b)
h 5a; rg -n --pcre2 '(?i)\b(from|source|src|debit)_?currency\b|\b(to|target|dest|destination|credit)_?currency\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 5a ${PIPESTATUS[0]}
h 5b; rg -n -H --pcre2 '(?i)\bcurrency\w*\b\s*[!?]?\s*[:=](?!=)' "${L[@]}" | "${NC[@]}"; ck 5b ${PIPESTATUS[0]}
# 6 LG-6 reconciliation code that names a money movement (6a, files) and ingestion of the provider's balance transactions, payouts or statements (6b)
fl '(?i)\breconcil\w*' REC; h 6a; rg -l --pcre2 '(?i)\b(payouts?|settlements?|payments?|psp|provider|bank|cod|collections?|clearing|balance_?transactions?)\b' "${F[@]}"; ck 6a $?
h 6b; rg -n --pcre2 '(?i)\b(balance_?transactions?|balanceTransactions|payouts\.(list|retrieve)|settlement_?(report|file|batch)\w*|bank_?statement\w*|remittance\w*)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 6b ${PIPESTATUS[0]}
# 7 LG-7 reversal postings in ledger code (7a); capture posted as authorised vs received (7b)
h 7a; rg -n -H --pcre2 '(?i)\b\w*(revers|void|refund|chargeback|dispute|correction)\w*\s*\(' "${L[@]}" | "${NC[@]}"; ck 7a ${PIPESTATUS[0]}
h 7b; rg -n --pcre2 '(?i)\bamount_?(received|captured|to_?capture|capturable|authori[sz]ed)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 7b ${PIPESTATUS[0]}
# 8 FR-1 deletion and offboarding flows (8a, files); in them, writes that reach records of fact (8b)
fl '(?i)\b(delete_?account|delete_?user|delete_?customer|delete_?tenant|destroy_?tenant|close_?account|erase\w*|anonymi[sz]\w*|pseudonymi[sz]\w*|offboard\w*|forget_?me|right_?to_?(be_?forgotten|erasure)|gdpr\w*)\b' DEL
h 8a; cat "$OUT/DEL.txt"
h 8b; rg -n -H --pcre2 '(?i)\b(delete\s+from|truncate)\s+"?\w*(invoice|order|payment|ledger|journal|transaction|receipt|payout|refund)\w*|\bdrop\s+schema\b|\b\w*(invoice|order|payment|ledger|journal|transaction|receipt|payout|refund)\w*(repository|repo|Entity|Model)?\w*\s*[.,]\s*\w*(delete|destroy|remove|nativeDelete|deleteMany|delete_all)\w*\s*\(|\b(nativeDelete|deleteMany|remove|destroy)\s*\(\s*\w*(Invoice|Order|Payment|Ledger|Journal|Transaction|Receipt|Payout|Refund)\w*' "${F[@]}" | "${NC[@]}"; ck 8b ${PIPESTATUS[0]}
# 9 FR-2 purge / retention jobs that name a record of fact (9a, files) and the periods they use (9b)
fl '(?i)\b(retention\w*|purge\w*|prune\w*|older_?than|expire_?after)\b' RET; h 9a; rg -l --pcre2 '(?i)\b(invoices?|orders?|payments?|ledger|journal|transactions?|receipts?|payouts?|refunds?)\b' "${F[@]}" > "$OUT/RETF.txt"; ck 9a $?; cat "$OUT/RETF.txt"; F=(); while IFS= read -r f; do F+=("$f"); done < "$OUT/RETF.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none")
h 9b; rg -n -H --pcre2 '(?i)interval\s*["\x27]?\s*\d+\s*(year|month|day)s?|\b\d+\s*\*\s*365\b|\b(years?|months?|days?)\s*:\s*\d+|\bsub(Years|Months|Days)\(|\brelativedelta\(\s*(years|months|days)|\.years?\.ago\b|\btimedelta\(\s*days\s*=\s*\d{3,}|\b\w*retention\w*\s*[!?]?\s*[:=]\s*\d' "${F[@]}" | "${NC[@]}"; ck 9b ${PIPESTATUS[0]}
# 10 FR-3 personal data copied into ledger rows (10a); anonymisers that touch issued documents (10b — read in the 8a files)
h 10a; rg -n -H --pcre2 '(?i)\b\w*(email|phone|first_?name|last_?name|full_?name|customer_?name|buyer_?name|address|national_?id)\w*\b\s*[!?]?\s*[:=](?!=)' "${L[@]}" | "${NC[@]}"; ck 10a ${PIPESTATUS[0]}
fl '(?i)\b(anonymi[sz]\w*|pseudonymi[sz]\w*|erase\w*|redact\w*)\b' ANO; h 10b; rg -n -H --pcre2 '(?i)\b(invoice|receipt|credit_?note|buyer|billing_?address)\w*' "${F[@]}" | "${NC[@]}"; ck 10b ${PIPESTATUS[0]}
# 11 DM-1 invariants enforced in the schema (11a: CHECKs on guarded columns) and guards in code (11b)
h 11a; rg -n -i --pcre2 '\bcheck\s*\([^)\n]*\b\w*(balance|quantity|qty|stock|on_?hand|available|reserved|amount|total|debit|credit|limit|quota)\w*"?\s*(>=|>|<=|<|between|<>)' "${M[@]}" .; ck 11a $?
h 11b; rg -n --pcre2 '(?i)\bif\s*\(?[^\n]{0,80}\b\w*(balance|stock|on_?hand|available|reserved|quota|remaining)\w*\s*(<|<=)\s*[\w.(]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 11b ${PIPESTATUS[0]}
# 12 DM-2 bulk or raw writes to guarded columns — the paths that skip the guard
h 12; rg -n -U --pcre2 '(?i)\bupdate\s+"?\w+"?\s+set\b[^;`]{0,200}?\b\w*(balance|stock|quantity|on_?hand|available|reserved)\w*"?\s*=|\b(update_all|updateMany|nativeUpdate|bulk_update|update_columns?)\s*\([^\n]*\b\w*(balance|stock|quantity|on_?hand|available|reserved)\w*|\.objects\.[^\n]*\.update\([^\n]*\b\w*(balance|stock|quantity|on_?hand|available|reserved)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 12 ${PIPESTATUS[0]}
```

### Measured (2026-10-19)

- **Real repo, read-only** (a NestJS 11 + Fastify + MikroORM 6 + React monorepo with a general ledger, an append-only wallet ledger, courier wallets and an outbox dedupe ledger; `ROOTS=(apps/api/src)`): about 1 s, 0 `rg` errors, nothing written into the tree. 0a lists 9 ledger tables; 0c 36 schema controls, among them the **deferred constraint trigger** `gl_journal_lines_entry_balances` and the one-sided / non-negative CHECKs on journal lines — so **§1 is Traced** for the GL with 1a's `assertBalanced` in the aggregate as the second layer ([`precedents/business.md`](../../../../snippets/precedents/business.md) §10). The first draft of the ledger file list matched every identifier containing "ledger" and listed 87 files (webhook and outbound-operation dedupe "ledgers", inventory folds); bound to table names, entity classes and SQL writes it lists **22**, and the two dedupe ledgers that remain are decoys read once. **§2** 2a 0 and 2b 0 on one line each — the earlier eval's true negative — until 2b went multi-line (`-U`): it then prints the journal **header** written by `nativeUpdate(GlJournalEntryEntity, …, { status, entryDate })` with the entity on the next line; read: the aggregate allows `entryDate` only on a draft and makes posted entries immutable ([`precedents/business.md`](../../../../snippets/precedents/business.md) §11) → refuted, with a Hardening note that the guard lives in code only. **§3** 3a 14: a source-keyed unique index on machine-posted journal entries and a provider-reference unique index on wallet transactions — Traced. **§4** 4a 12 cache writes (`wallet.balance… = move.balance`) after narrowing from 39 (in-memory report buckets dropped); each is read for the posting transaction. **§7** 3: the GL reversal mirrors the original with sides swapped (decoy). **§8** 24 deletion-flow files, 8b 0: customers and orders are erased by a pseudonymising erasure port, not deletes ([`precedents/business.md`](../../../../snippets/precedents/business.md) §17). **§9** 7 period lines, all on logs, sweeps and idempotency rows (30–180 days), none on records of fact. **§12** 0 raw bulk writes to guarded columns.
- **Fixtures** (23 trees): 0 `rg` errors. `slow-marketplace` prints its payout ledger's single-leg `em.create(LedgerEntry, { amountCents: -amountCents })` (1b: a signed single-entry ledger — read for §1) and its settlement-file importer (6b); `ds-defects` prints its Java `INSERT INTO postings … ON CONFLICT` (1b/3b) and the outbox `UPDATE ledger_outbox_rows SET sent_at` (2a — a non-financial column, refuted); `quality-mix` prints the raw `update wallet set balance_cents = balance_cents - …` pair (4a/12) whose refund call swaps the parties (QM-CS-03, owned by code-quality — listed here as LG-7 corroboration); `backend-defects` prints `update merchant_balances set available = available + …` in its settlement cron (12; the overlap race is backend `job-lifecycle-scan`'s seed). No seeded ledger defect owned by another pack is graded here.
- **Fixture `business-rules`** (2026-10-19, same staging): 0.45 s, 0 `rg` errors, 162 lines. All 24 LG/FR/DM seeds print — 21 at their line; LG-6 as the absence the read closes (F1 `stripe`, 6a only a bank reconciliation, 6b a COD remittance import that compares no amount) and the TS LG-7 seed at its function head (7a). Decoys cleared at the read: 0c the GL's deferred balance trigger ([`precedents/business.md`](../../../../snippets/precedents/business.md) §10 — it covers the raw-SQL payment and refund postings too), 2a a `reconciled_at` stamp (§11), 3a the wallet unique source key (§12) beside no unique key on GL entries (the LG-3 seed), 4a/4b the in-transaction cache write and its sweep (§13), 11b the clearing accounts allowed below zero (§14), 8a/10b the pseudonymising erasure (§17). 0a's Django lane lists the back office's three settlement-ledger tables from `migrations.CreateModel(name=…, options={"db_table": …})` (the first run listed none); 0b finds the same `db_table` bindings in the models.

## The 3,000-hit path

The inventory decides most of a large run. Build it once (F1, 0a–0c): a ledger engine in the lockfile, or a deferred balance trigger plus an UPDATE/DELETE-refusing trigger or grant on the line table, closes §1/§2 for every writer of that table with **one** cited reason ([`precedents/business.md`](../../../../snippets/precedents/business.md) §10, §11), and the read narrows to tables without one. Then, in order: §8 (deletion flows reaching records of fact; few files, critical); §1b/§3 per ledger table (writers grouped by function); §2a/§2b per table (split financial columns from `memo`, `reconciled_at`, `exported_at`); §4 per cache table; §7 per reversal function; §6 once per provider; §9/§10 per purge or anonymiser job; §5, §11, §12 by invariant from the register. A group closes only with the reason checked (the trigger read, the column list read), never assumed; remaining groups print `Live, unreviewed (k groups / n hits)`.

## Scans for

| § | Class (`BIZ-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | LG-1 an unbalanced posting can commit (per transaction and currency) | critical | V463 |
| 2 | LG-2 ledger mutable; correction by edit, not reversal | high | V464 |
| 3 | LG-3 posting not idempotent at the ledger | critical | V465 |
| 4 | LG-4 balance cache as a second source of truth, no drift sweep | medium | V466 |
| 5 | LG-5 currencies mixed in an entry or account; no FX legs | high | V463 |
| 6 | LG-6 no reconciliation with the external system of record | medium | V467 |
| 7 | LG-7 reversal edges do not conserve | high | V477 |
| 8 | FR-1 records of fact erased by an application deletion flow | critical | V468 |
| 9 | FR-2 retention purge shorter than the legal minimum, or one TTL for all | high | V468 |
| 10 | FR-3 PII inside immutable records with no pseudonymisation path | high | V468 |
| 11 | DM-1 a money / stock / balance invariant enforced nowhere | critical | V481 |
| 12 | DM-2 an invariant enforced on one write path only | high | V481 |

### 1. An unbalanced posting can commit

```
BAD:   await em.insert(LedgerEntry, { account: wallet, amount: +500 })     // one leg; nothing sums
GOOD:  post([{ account: wallet, debit: 500 }, { account: clearing, credit: 500 }]) — asserted in code AND
       a deferred constraint trigger: SUM(debit) - SUM(credit) = 0 per (entry, currency) at COMMIT
```
**Read the code:** Does every writer of the line table (1b) write ≥ 2 legs through one function? Is the sum checked per transaction **and per currency**? Is the check in code only (1a), or also at a layer every writer hits (0c: a deferred constraint trigger, a SQL function, a ledger engine)? Can a raw insert, a backfill or a second service bypass the code check? **Finding when** a write that bypasses the posting function can commit an imbalance. A deferred trigger that sums each touched entry at commit is Traced ([`precedents/business.md`](../../../../snippets/precedents/business.md) §10). **Proof:** V463 — the balance property over generated postings, then a direct-SQL unbalanced insert rejected at COMMIT.

### 2. Ledger mutable

```
BAD:   update journal_lines set amount = $1 where id = $2          // "fix" a posted entry
GOOD:  post a reversing entry linked to the original; UPDATE/DELETE on financial columns refused by trigger or grant
```
**Read the code:** Which columns does each 2a/2b write touch — amount, account, currency, date, direction (financial) or `memo`, `reconciled_at`, `exported_at`, `metadata` (not, [`precedents/business.md`](../../../../snippets/precedents/business.md) §11)? Is the row `pending` (mutable until posted, Modern Treasury's model) or posted? Does the entity carry `updated_at`, soft-delete or `paranoid` (2c)? **Finding when** a posted entry's financial content can change or vanish. **Proof:** V464 — add a trigger or revoke UPDATE/DELETE on a test database and run the suite: still green; a golden ledger diff of a correction scenario shows added rows only.

### 3. Posting not idempotent at the ledger

```
BAD:   if (!(await repo.findOne({ eventId }))) await repo.insert({ eventId, … })   // two deliveries race past the find
GOOD:  unique (source_type, source_id, leg) + insert … on conflict do nothing, in the posting transaction
```
**Read the code:** What identifies a posting's cause (provider event id, refund id, order id + leg)? Is it unique **at the ledger table** (3a), or only checked in code? Is the key generated before the first submit, not at retry time? Consumer dedupe in front of it is distributed-systems' corroboration, not the control. **Finding when** one cause can post twice. **Proof:** V465 — deliver the same event N times, sequentially and concurrently: one entry set.

### 4. Balance cache as a second source of truth

**Read the code:** Is every 4a write inside the same transaction as the ledger insert it reflects? Does any other service write the cache? Is there a drift sweep (4b) that compares the cache with the fold of entries and alerts? Atomic increments and trigger-maintained balances are not this class; the race on a read-modify-write is security's or database's (§ Boundaries). **Finding when** the cache can diverge from the entries with nothing to notice. **Proof:** V466 — for generated sequences, cache = Σ entries per account and currency; a crash between the two writes is detected by the sweep.

### 5. Currencies mixed

**Read the code:** Is the currency fixed per account (not nullable, not updatable) and compared with each entry's? Does a cross-currency transfer post through FX or liquidity accounts on each currency's side, with the fee as its own leg (5a)? **Finding when** one entry pair moves value between two currencies, or an account holds two. Accounts per currency under one parent are not this class. **Proof:** V463 — per-currency sums are zero after an FX scenario; A→B→A never gains.

### 6. No reconciliation with the system of record

**Read the code:** For each provider in F1, does a job ingest its balance transactions, payouts or settlement files (6b) and compare them with the internal clearing entries (6a)? Do clearing accounts net to zero at steady state? Reconciliation in an external accounting tool, documented, is not this class. **Finding when** a provider is in the lockfile and nothing compares its money movements with the ledger. **Proof:** V467 — a golden provider export for a day against the ledger: every row matched, clearing nets to zero.

### 7. Reversal edges do not conserve

```
BAD:   refundEntry.amount = round(order.total * share)        // recomputed: the stray cent stays on the books
       capture posts payment.amount (authorised), not amount_received
GOOD:  the reversal mirrors the original legs (same rounding, opposite direction); capture posts what was captured
```
**Read the code:** Does each refund, void, chargeback or correction (7a) mirror the original entry's legs, or recompute them? Can it fire twice for one cause (§3)? Does a partial capture post the captured amount (7b)? **Finding when** a charge followed by its full reversal does not net to zero to the minor unit, or a reversal re-fires. **Proof:** V477 — charge → partial refunds → full refund → dispute won/lost: every account nets as expected.

### 8. Records of fact erased by a deletion flow

```
BAD:   async deleteAccount(id) { await em.nativeDelete(Order, { customer: id }); await em.nativeDelete(Invoice, …) }
GOOD:  orders, invoices and ledger rows kept and pseudonymised; PII erased from mutable tables; drafts deletable
```
**Read the code:** For each deletion or offboarding flow (8a), which tables does it delete from (8b), directly or through a cascade it triggers? Does a tenant drop (`DROP SCHEMA`, a bucket delete) archive financial records first? Unissued drafts are deletable ([`precedents/business.md`](../../../../snippets/precedents/business.md) §15). **Finding when** an application flow can erase an issued invoice, an order, a payment or a ledger row inside its retention period. **Proof:** V468 — delete a seeded user and a seeded tenant: the records remain, pseudonymised.

### 9. Retention period

**Read the code:** What period does each purge job (9a/9b) use, per record kind? Which jurisdictions does the tax policy row name, and what does each authority require — cite it: Germany § 147 AO reads 10 years for books and 8 for booking vouchers including invoices (the start date of the change varies by source); UK VAT ≥ 6 years; US IRS 3/6/7 years by case; Saudi Arabia 6/11/15 years and Egypt 5 years are secondary sources `[K?]`. **Finding when** a purge deletes records of fact before the cited minimum, or one TTL covers record kinds with different minimums. Without a cited period the row is `[report-flagged]`. **Proof:** V468 — seeded aged rows per kind: in-policy rows remain after the job runs.

### 10. PII inside immutable records

**Read the code:** Do ledger rows copy free-text names, e-mails or addresses (10a) instead of a pseudonymous party id? Does an anonymiser (10b) blank the buyer's legally required fields on issued invoices? The design that satisfies both: an invoice snapshot of legally required party data, kept under GDPR Art. 17(3)(b), and a separate PII table that can be erased ([`precedents/business.md`](../../../../snippets/precedents/business.md) §17). **Finding when** erasure would require mutating the ledger, or an anonymiser breaks an issued document. **Proof:** V468 — erase a seeded subject: PII gone from mutable tables, the invoice snapshot and the ledger intact.

### 11. Invariant enforced nowhere

**Read the code:** For each invariant in the register (non-negative stock, balance within limit, Σ allocations = total), where is it enforced: a CHECK or trigger (11a), a guard in the aggregate (11b), a conditional `UPDATE … WHERE balance >= :amt` with the row count checked? Accounts meant to go negative (clearing, liquidity, provider receivable) are not this class ([`precedents/business.md`](../../../../snippets/precedents/business.md) §14). **Finding when** an invariant has no enforcement site. **Proof:** V481 — a write that violates it through the real path is rejected.

### 12. Invariant enforced on one write path only

**Read the code:** For each guarded column, list every writer: services, bulk updates, raw SQL (12), admin panels, imports, a second service. Does each pass the guard, or does a database constraint cover all of them? **Finding when** one writer bypasses the guard. **Proof:** V481 — the violating write through each writer.

## Output

```
ledger-scan — lanes: typescript (@mikro-orm/core 6.6 — pnpm-lock.yaml); no ledger engine; providers: none in the lockfile
Inventory: $OUT/ledger-inventory.md — gl_journal_lines (balance: deferred constraint trigger, Migration…100000.ts:82; one-sided CHECKs);
           wallet_ledger (append-only, documented; cache: wallets.balance, written in the posting transaction)

Findings: 0 · Unconfirmed: 1 · Enabler: 1

1. src/accounts/delete-account.use-case.ts:40                              [report-flagged]   critical
   §8 FR-1 — the account deletion flow calls orders.deleteForCustomer; unproven link: whether issued orders reach it.
   Settling: V468 — delete a seeded customer with an issued order, then count orders and invoices.
2. (register)                                                              Enabler            —
   §11 DM-1 — no invariant register (ai/business-domain.md absent); @domain-model-auditor builds it.

Routed: 2 → database transaction-scan §8 (balance read-modify-write) · 1 → database schema-integrity-scan §2 (CASCADE into orders)
Verification: 19 candidates → 0 findings · 1 unconfirmed · 1 enabler · 17 refuted (self-verified; precedents §10, §11, §13)

Class coverage:
  §1  balanced posting       checked (1a 5, 1b 12 → 0: deferred trigger on gl_journal_lines; wallet postings through one function)
  §2  immutability           checked (2a 0, 2b 0, 2c 1 → 0: updated_at on the account, not the entries)
  §3  idempotent posting     checked (3a 4, 3b 9 → 0: unique (source_type, source_id, leg))
  §4  balance cache          checked (4a 6, 4b 1 → 0: cache in the posting transaction + nightly sweep)
  §5  currencies             checked (5a 0, 5b 7 → 0)
  §6  reconciliation         N/A (no payment provider in the lockfile; COD reconciliation read: matched per parcel)
  §7  reversals              checked (7a 8 → 0: reversals mirror the original legs)
  §8  deletion flows         checked (8a 3, 8b 2 → 1 unconfirmed)
  §9  retention              checked (9a 2, 9b 2 → 0: purges touch logs and sessions only)
  §10 PII in records         checked (10a 0, 10b 0)
  §11 invariants             N/A (no invariant register) — enabler
  §12 bypass writers         checked (12 3 → 0)
```

`[report-with-fix]`: the database accepted the violating write (or the replay posted twice) through the real schema, and the fix is local to the posting function, a constraint or trigger, or the deletion flow. `[report-flagged]`: one link is unproven (a writer not followed, the schema `UNREAD`, a retention period with no cited authority); the row names it and the settling probe. The coverage block lists **all twelve** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/business.md`](../../../../snippets/precedents/business.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. Numbers are [`precedents/business.md`](../../../../snippets/precedents/business.md) §s. The ones this skill meets most:
- §10 a ledger balance enforced by a deferred constraint trigger, or by TigerBeetle / Formance / pgledger, is Traced for §1 — a real NestJS + React monorepo asserts balance in its journal aggregate **and** adds a deferred constraint trigger that sums every touched entry at COMMIT, so a raw insert cannot commit an imbalance.
- §11 UPDATE of non-financial ledger columns (`memo`, `reconciled_at`, `exported_at`, `metadata`) is not §2; `pending` transactions are mutable until posted. §12 posting idempotency by a unique `(source_type, source_id, leg)` key, or a provider key derived from the business id.
- §13 a balance cache written in the same transaction as the ledger insert, plus a drift sweep ("the ledger is the truth"). §14 accounts meant to go negative (clearing, liquidity, equity, provider receivable).
- §15 drafts and unissued documents are deletable. §17 retaining invoices after an erasure request under GDPR Art. 17(3)(b), with PII pseudonymised in mutable tables and the invoice snapshot intact, is correct.

## When to run

- On any diff that touches a ledger, journal, wallet or balance table, a posting function, a reversal, a reconciliation job, an account or tenant deletion flow, a purge or anonymiser job, or a migration on those tables — `/audit-business`'s ledger signal.
- On every whole-repo `/audit-business`, reporting all twelve §s; before a new payment provider, a new currency or a data-retention change.

## Halt conditions

- **Do not report a high or critical row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the inventory row, the `file:line` and the probe — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/business.md`](../../../../snippets/precedents/business.md). Under `/audit-business` that is `@domain-model-auditor` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before §1–§5 when the schema is unread.** A verdict on balance or immutability without the triggers, constraints and grants on the table is invalid; read the migrations or `schema-map.py` output first.
- **Run every probe on a scratch database or inside a rolled-back transaction**, never on a shared or production database; a probe that cannot be isolated is `NOT-RUN`.
- **Never state a retention period from memory;** cite the authority's document with its date, or mark the row `[report-flagged]`.
- **No proposed fix may hide the class:** never "fix" a ledger by editing posted entries, never widen a CHECK, never add a tolerance to a reconciliation query, never regenerate a golden ledger in the same change as the code.
- **Business decisions are not code fixes:** a retention period, an erasure policy, an overdraft limit is the owner's call — the row names the decision and stops.
- **Do not grade a class another pack owns** (§ Boundaries). **Do not print "the ledger looks sound"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/audit-business` dispatches this skill and folds its coverage block into its class ledger; `@domain-model-auditor` judges these rows and keeps the invariant register §11–§12 read. `pricing-rule-scan` §9 (the refund share) and `tax-invoice-scan` §7 (issued documents) are the neighbours in this pack.
- database `schema-integrity-scan` §2/§4/§10 and `transaction-scan` §7/§8, security `logic-race-scan` §5, distributed-systems `messaging-scan` §2 / `dual-write-scan`, when those packs are installed; `index-coverage-scan/scripts/schema-map.py` (database pack) supplies the replayed schema.

## Sources

From the business research (2026-10-19): TigerBeetle docs (two-phase transfers, account flags, data modelling, reliable submission, correcting transfers, FX; client 0.17.x), Stripe's ledger write-up (2024-02-16; clearing nets to zero), Modern Treasury (pending vs posted, optimistic locking), Square Books (2019-10-16), pgledger (2025), Formance v2.3.x; Stripe balance transactions, payouts and idempotency-key pruning (≥ 24 h) from Stripe's docs; GDPR Art. 17(3)(b); § 147 AO (10 / 8 / 6 years; start date of the change `[K?]`), UK VAT Notice 700/21 (2024-03-18), IRS record keeping (2026-06-30); Saudi and Egyptian retention from secondary sources `[K?]`. The real-repo and fixture counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
