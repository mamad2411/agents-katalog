---
name: extract-scan
description: "Exports and dumps as faithful copies; OFFSET paging of mutating tables, no snapshot, silent caps, lossy values."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: extract-scan

## Premise

An export is a copy someone acts on: a merchant reconciles a CSV against their bank, a partner loads a nightly file, an admin restores a dump. It is a faithful copy only if every row of the source **at one instant** appears **once**, with its values intact. Four mechanisms break that without an error: paging a table that is being written by `OFFSET` (newest-first, a row inserted at the head shifts every later page by one and a boundary row appears twice; a delete behind the cursor skips one), reading several tables in separate statements with no shared snapshot (a child row whose parent was read before it existed), a cap that truncates silently or a file published before the run finished, and a representation that loses data on the way out (an instant with no offset, a decimal through a float or a locale format, an id or a phone number through `Number`). Use The Index, Luke's "No Offset" and Laravel's `chunk` vs `chunkById` warning (research B26, B27) describe the first; the Postgres manual's transaction isolation chapter the second.

This skill owns research ids EX-1…EX-4 (`research-data-engineering.md` § 1.7), shipped as `DE-EX-<n>`: **whether an extract, export or dump is a faithful, consistent copy of its source.**

**Every finding cites the extract `<file:line>` + the source table and its write rate (does anything write it during the export?) + the paging key and the transaction boundary as read + the row that is duplicated, skipped, orphaned, truncated or altered + the oracle that would settle it + the fix in the project's own primitive.** A grep hit is a candidate. "The exports look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V560–V562.

## The rule

A candidate is a finding when all four hold:

1. **Reachable and consumed.** A route, job, queue processor or script produces the file or the push, and a person, a partner or a restore reads it. A one-off script that already ran fails here unless it is the documented path.
2. **The source is mutable during the read.** The table takes inserts, updates or deletes while the export runs (an order table, an activity log, a ledger with reversals). An immutable partition, a closed period, or a source stopped for the dump is precedent § 30 / the quiescent-source note.
3. **No existing control, across files.** Keyset paging on a unique key compared in SQL, one `REPEATABLE READ` / `SERIALIZABLE READ ONLY DEFERRABLE` transaction or an exported snapshot (`pg_export_snapshot()`), `pg_dump` (one snapshot by design), a ceiling that refuses with a message (precedent § 39), a temp-then-rename publish, ISO-8601 instants with an offset, decimals as strings, ids as text cells.
4. **The oracle fired, or the fact is two-ended.** V560/V561/V562 ran red against a scratch DB with a concurrent writer; or the static fact cites both ends — the advancing `page` and the newest-first order on a table the same module inserts into; the per-table statements and the absence of any isolation setting.

## Boundaries

- **The per-query cost of a deep OFFSET and a non-unique sort key on a paged API read** → database `query-shape-scan` §2/§8 (when installed); this skill owns the **consistency** of a multi-page copy, and a tie-breaker missing from an export's sort is §1 here with §8 corroborating. **Whole-file buffering and export memory** → performance `request-path-scan` §6 / `memory-growth-scan`. **CSV formula injection** → security `injection-scan`. **Who may export, and PII in the export** → security `@data-privacy-reviewer` and `pii-copy-scan` §5 (this pack). **API wire formats** → backend `wire-format-scan`. **A half-written temp file left on disk** → code-quality `error-handling-scan` §7. Each when installed; without them the row is `[report-flagged]` here with the route named.
- **Warehouse loads** that read an OLTP table incrementally → `incremental-load-scan`; **a migration that drops a column an extract reads** → `contract-diff` §4.

## Adapt to the codebase — the lanes

| Lane | Detect by | Paging / snapshot idiom read | Fix primitive |
|---|---|---|---|
| **Node / TS** (MikroORM, Prisma, TypeORM, Drizzle, Knex, Sequelize; exceljs, csv-stringify, fast-csv, papaparse, xlsx) | export/sheet/dump/runner/sync files; writer imports | `page` / `offset` / `skip` advancing; `cursor`, `lastId`, `id < $last`; `em.transactional(…, { isolationLevel })`, `$transaction(…, { isolationLevel })` | keyset on `(created_at, id)` compared in SQL; one `REPEATABLE READ` read-only transaction; stream from a server-side cursor |
| **Python** (Django, SQLAlchemy, pandas; `csv`, openpyxl, xlsxwriter) | `csv.writer`, `to_csv(`, `.iterator()`, `yield_per` | `[offset:offset+n]` slicing, `.iterator(chunk_size=)`, `Paginator` | `.iterator()` inside `transaction.atomic()` with `REPEATABLE READ`; keyset filter on `pk` |
| **Ruby / PHP** (ActiveRecord, Eloquent; `CSV.generate`, PhpSpreadsheet) | `find_each`, `in_batches`, `chunk(`, `chunkById(`, `cursor()` | `chunk` pages by OFFSET; `chunkById`/`find_each` page by key | `chunkById` / `find_each` on the PK |
| **Dumps** (`pg_dump`, `mysqldump`, `COPY … TO`, app-level table loops) | dump scripts, CI jobs, `information_schema.tables` loops | per-table statements; `--single-transaction`; `pg_export_snapshot` | `pg_dump` (one snapshot); `mysqldump --single-transaction` for InnoDB; one `REPEATABLE READ` transaction around the loop |
| **Pushes** (Google Sheets, partner SFTP, S3/GCS drops, webhooks) | `googleapis`, `sftp`, `putObject`, `upload(` in export files | publish order, temp names, completion markers | write to a temp key, rename on success; a manifest written last |

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; 0 builds the surface. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; **the export path glob stands alone** — it is never combined with an extension glob (ripgrep ORs two positive `-g` globs: path glob + code glob listed 31 files on a real repo where the path glob alone listed the runners). Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Nothing is written outside `$OUT`.

```bash
ROOTS=(.)   # monorepo: name the server roots, e.g. ROOTS=(apps/api/src)
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-ex.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,venv,logs}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/test_*.py' -g '!**/*_test.{py,go}'
   -g '!**/{locales,locale,i18n,translations,migrations,migration}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.{md,mdx,lock,min.js,snap,csv,json}')
CODE=(-g '*.{ts,mts,js,mjs,cjs,py,rb,php,java,kt,go,cs,sh}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#|--)')
# 0 THE EXTRACT SURFACE — 0a export/sheet/dump/runner/sync files by PATH (glob alone) · 0b files that write a file format or dump · union = EXP
h 0a; rg --files -g '**/*{export,Export,sheet,Sheet,dump,Dump,extract,Extract,runner,Runner,sync,Sync,backup,Backup}*' "${X[@]}" "${ROOTS[@]}" | rg -v --pcre2 '\.(?:md|json|ya?ml|csv|txt|svg|png)$' | sort -u > "$OUT/EXP0.txt"; wc -l < "$OUT/EXP0.txt"
h 0b; rg -l --pcre2 '(?:from|require\()\s*["\x27](?:exceljs|csv-stringify[\w/]*|fast-csv|@fast-csv/\w+|papaparse|json2csv|xlsx|write-excel-file|archiver)["\x27]|\bcsv\.(?:writer|DictWriter)\(|\.to_csv\(|\bopenpyxl\b|\bxlsxwriter\b|PhpSpreadsheet|\bCSV\.(?:generate|open)\b|\bcopy_expert\(|\bcopyTo\(|(?i:\bcopy\s+\(?[^;\n]*\bto\s+(?:stdout|program)\b)|\bpg_dump\b|\bmysqldump\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u > "$OUT/EXP1.txt"; ck 0b ${PIPESTATUS[0]}; wc -l < "$OUT/EXP1.txt"
cat "$OUT/EXP0.txt" "$OUT/EXP1.txt" | sort -u > "$OUT/EXP.txt"; E=(); while IFS= read -r f; do E+=("$f"); done < "$OUT/EXP.txt"; [ ${#E[@]} -gt 0 ] || E=("$OUT/none")
# 1 EX-1 multi-page reads — 1a a page/offset that advances into a list/find query · 1b the keyset controls in the same files (read each pair)
h 1a; rg -n --pcre2 '(?:async\s*)?\(\s*page\s*(?::\s*number)?\s*\)\s*=>|^\s*page\s*,\s*$|\bpage\s*:\s*page\b|\bpage\s*(?:\+\+|\+=\s*1)|\bpage\s*=\s*page\s*\+\s*1|\boffset\s*(?:\+=|=\s*offset\s*\+)|\.skip\(\s*[a-z]\w*|\boffset\s*:\s*\(?\s*(?:page|i|n)\b|(?:->|\.)chunk\(\s*\d+|(?i:\boffset\s+(?:\$\d+|\?|%s|:\w+|\$\{))|\.offset\(\s*[a-z]\w*|\[\s*\w+\s*:\s*\w+\s*\+\s*\w+\s*\]' "${E[@]}" | "${NC[@]}" | tee "$OUT/P1.txt"; ck 1a ${PIPESTATUS[0]}
P=(); while IFS= read -r f; do P+=("$f"); done < <(cut -d: -f1 "$OUT/P1.txt" | sort -u); [ ${#P[@]} -gt 0 ] || P=("$OUT/none")
h 1b; rg -c --pcre2 '\bpage\s*:\s*1\b|\blastId\b|\blast_id\b|\bcursor\b|\bafter\s*[:=(]|\bbelow\(|\bchunkById\(|\bfind_each\b|\bfind_in_batches\b|\bin_batches\b|\.iterator\(|\byield_per\(|\bkeyset\b|(?i:"?id"?\s*[<>]\s*(?:\$\d+|\?|:\w+|%s))' "${P[@]}"; ck 1b $?
h 1c; rg -n --pcre2 '(?i)\b(?:defaultSort|orderBy|order_by|order)\s*[:=(]\s*[\[{(]?\s*["\x27]?\w*(?:created|updated)_?at["\x27]?\s*(?::\s*["\x27]?desc|,\s*["\x27]?desc|\s+desc)|\bfield\s*:\s*["\x27]\w*(?:created|updated)_?at["\x27]\s*,\s*direction\s*:\s*["\x27]desc|\border\s+by\s+"?\w*(?:created|updated)_?at"?\s+desc\b(?!\s*,)|->latest\(\)|\.order\(\s*(?:created_at|updated_at)\s*:\s*:desc' "${CODE[@]}" "${X[@]}" $(for f in "${P[@]}"; do [ -f "$f" ] && dirname "$(dirname "$f")"; done | sort -u) "$OUT/none" | "${NC[@]}"; ck 1c ${PIPESTATUS[0]}
# 2 EX-2 multi-table reads with no shared snapshot — 2a table loops/catalog reads with no isolation in the file · 2b mysqldump without --single-transaction
h 2a; rg -l --pcre2 '(?i)\binformation_schema\.tables\b|\bpg_tables\b|\bpg_class\b|\bshow\s+tables\b|\bfor\s*\(\s*const\s+\w+\s+of\s+\w*tables\b|\bfor\s+\w+\s+in\s+\w*tables\b|\btables\.(?:map|forEach)\(|\bget_table_names\(' "${E[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '(?i)repeatable[\s_]+read|\bserializable\b|pg_export_snapshot|set\s+transaction\s+snapshot|--single-transaction|isolation_?level|IsolationLevel\.|REPEATABLE_READ|\bpg_dump\b'
h 2b; rg -n --pcre2 '\bmysqldump\b(?![^\n]*--single-transaction)' "${CODE[@]}" -g '**/Makefile' -g '**/*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2b ${PIPESTATUS[0]}
# 3 EX-3 caps and publication — 3a caps in extract files (read whether they refuse) · 3b the refusal and failure vocabulary per file · 3c where the stored path / ready status is written
h 3a; rg -n --pcre2 '\bslice\(\s*0\s*,\s*(?:[A-Z_][A-Z0-9_]*|\d{3,})\s*\)|\.limit\(\s*(?:MAX\w*|\d{3,})\s*\)|(?i:\blimit\s+\d{3,}\b)|\btake\s*:\s*(?:MAX\w*|\d{3,})|\[\s*:\s*(?:MAX\w*|\d{3,})\s*\]|\.head\(\s*\d{3,}\s*\)|\bMAX_(?:ROWS|EXPORT\w*|LINES)\b' "${E[@]}" | "${NC[@]}" | tee "$OUT/P3.txt"; ck 3a ${PIPESTATUS[0]}
Q=(); while IFS= read -r f; do Q+=("$f"); done < <(cut -d: -f1 "$OUT/P3.txt" | sort -u); [ ${#Q[@]} -gt 0 ] || Q=("$OUT/none")
h 3b; rg -c --pcre2 '(?i)\bthrow\b|\braise\b|\brefus\w*|toolarge|too_large|\bexceed\w*|\b413\b|\btruncat\w*' "${Q[@]}"; ck 3b $?
h 3c; rg -n --pcre2 '(?i)\bstatus\s*[:=]\s*["\x27](?:ready|done|completed?|available|succeeded)["\x27]|\b(?:file_?url|download_?url|storage_?path|s3_?key|object_?key|file_?path|file_?key)\s*[:=]|\b(?:putObject|upload|uploadFile|writeFile|rename)\s*\(' "${E[@]}" | "${NC[@]}"; ck 3c ${PIPESTATUS[0]}
# 4 EX-4 representation — locale/float/Number on amounts and ids, zone-less instant formatting, in row mappers
h 4; rg -n --pcre2 '\.toLocale(?:String|DateString|TimeString)\(|\.toFixed\(|\bparseFloat\(|\bNumber\(\s*[\w.?!]*\b(?:amount|price|total|balance|cost|fee|subtotal|cents|id|phone|mobile|msisdn|iban|code)\w*\s*\)|new\s+Date\([^)]*\)\.toString\(\)|\.get(?:Hours|Date|Month|FullYear)\(\)|\bstrftime\(\s*["\x27](?![^"\x27]*%z)[^"\x27]*%H|\bformat\(\s*[\w.]+\s*,\s*["\x27][^"\x27]*HH(?![^"\x27]*(?:X|Z|xxx|O))[^"\x27]*["\x27]\s*\)|\bfloat\(\s*\w+\.(?:amount|price|total)' "${E[@]}" | "${NC[@]}"; ck 4 ${PIPESTATUS[0]}
```

1b prints, per extract file, how many keyset or snapshot markers it holds: a file with 1a lines and a 1b count of 0 is the strongest §1 candidate; a file with both (a real repo's orders export: `page: 1` + `below(lastId)` beside an activity loop that advances `page`) is read method by method — one method can be the control and the next the defect. 1c lists newest-first orders in the modules that hold a 1a file (the runner's list call usually sorts in a port beside it): an advancing page over a newest-first order on an insert-heavy table duplicates the boundary row.

### Measured (2026-10-19)

- **Fixture** (`benchmarks/fixtures/data-pipelines`, `ROOTS=(.)`; under 1 s, 0 `rg` errors): 0a 19 path-matched files · 0b 5 writer files. 1a 5 lines (the activity runner's `page` callback, the customers runner's `offset +=`, and the shared `collectPages` helper) · 1c 2 newest-first orders in the same modules · 2a 1 (the platform dump; the `REPEATABLE READ` tenant export is excluded) · 2b 1 (`mysqldump` without `--single-transaction`) · 3a 3 (the silent `slice(0, MAX_EXPORT_ROWS)`; the dump's `limit 1000` page size, refuted) · 3b 0 refusals in those files · 3c 2 (`status: 'ready'` before the upload) · 4 2 (`toLocaleString`, `Number(phone)`). The keyset orders export and the refusing ceiling are not listed — they are the controls an agent should not report.
- **Real repo, read-only** (the NestJS monorepo, `ROOTS=(apps/api/src)`; 0.2 s; nothing written): 0a 114 · 0b 0 (its sheets are written by an in-house writer) · 1a 14 lines in six runners — the activity and customers runners page newest-first insert-heavy tables by OFFSET (the eval's two live EX-1 candidates), the wallet and system-wallet runners page ledgers (order and mutation rate decide), and `collectPages` itself · 1b: only the orders export holds keyset markers (`page: 1` + `below(lastId)`, compared in SQL — precedent § 30) · 1c 29 newest-first sorts in those modules · 2a 2 (the dump port: catalogue loop, per-table statements, no isolation — the eval's EX-2 candidate) · 3a 7 (two DSAR export caps that print a "truncated" marker, error-text truncation) · 4 10 (`(cents / 100).toFixed(2)` display formatting of integer minor units — read; not lossy below 2^53). **A first draft** combined the path glob with a code-extension glob and listed 31 files; a second listed newest-first sorts across the whole tree (70+ lines) — now only the modules that hold a paging file.
- **The Python, Ruby, PHP and dump-script lanes are fixture-measured only.**

## The 3,000-hit path

1. **Inventory the extracts once** (0a/0b) and group by **base helper** — a shared `collectPages` or export base class is one decision for every runner that calls it; fix it there.
2. **For each extract, read three facts**: the source table's writers (does the module insert into it?), the order (newest-first?), the transaction boundary (one snapshot or one per page). A row with all three facts is decided; the rest are `[report-flagged]`.
3. **Rank** by consumer: partner and financial files first (reconciled against money), then customer-facing exports, then admin dumps.
4. **Prefer the concurrent-writer oracle at scale**: one harness that runs every runner against a scratch DB while a writer inserts at the head and deletes behind the cursor, comparing exported id sets with a start snapshot (V560).
5. **Ledger the rest** as `Live, unreviewed (k extracts / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes the file is acted on (reconciled, loaded, restored). One step lower for an ad-hoc admin download.

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | EX-1 multi-page extract over a mutating table by OFFSET or a non-unique sort | medium (high for financial or partner files) | V560 |
| 2 | EX-2 multi-table extract or dump not read from one snapshot | medium | V561 |
| 3 | EX-3 silent truncation at a cap, or a partial file published on failure | medium | V562 |
| 4 | EX-4 representation loses data (zone, decimals, ids) | medium | V562 |

### 1. OFFSET paging over a mutating table

```
BAD:   collectPages(async (page) => this.activity.list({ ...filter, page, pageSize: 500 }))   // createdAt desc; the log is appended to
       Order::orderBy('created_at', 'desc')->chunk(1000, fn ($rows) => …)                      // Laravel chunk pages by OFFSET
GOOD:  where (created_at, id) < ($lastCreatedAt, $lastId) order by created_at desc, id desc limit 500   -- compared in SQL
       ->chunkById(1000, …) · find_each · .iterator() inside one REPEATABLE READ transaction
```
**Read the code:** Does anything write the source table while the export runs (the same module's inserts, a webhook, a job)? In which order does the list query sort — newest-first means every insert lands in front of the cursor and shifts the pages; oldest-first with an append-only table is safe for inserts but not for deletes? Is the sort unique (a `created_at` tie between two rows makes page boundaries non-deterministic)? Is the loop inside one snapshot (precedent § 30)? Is a keyset value compared in SQL or copied through a JS `Date` that drops microseconds (a real repo's comment names exactly that risk)? **Finding when** an insert or delete during the export duplicates or skips a row in the file. **Proof:** V560 — insert at the head and delete behind the cursor between pages on a scratch DB: the exported id set equals the start snapshot, with no duplicate.

### 2. Multi-table read with no shared snapshot

```
BAD:   for (const t of tables) { for (let after = null; ; ) { rows = await db.execute(`select * from ${t} where id > ? …`) } }
GOOD:  await em.transactional(dump, { isolationLevel: IsolationLevel.REPEATABLE_READ, readOnly: true })
       pg_dump (one snapshot) · mysqldump --single-transaction (InnoDB) · pg_export_snapshot() shared by parallel readers
```
**Read the code:** Are the tables (or the pages of one table) read in separate statements on separate connections, outside a transaction? Do foreign keys connect them (child after parent)? Is the source quiescent during the dump (maintenance mode, a replica stopped at an LSN)? `pg_dump` is consistent by itself; `mysqldump` needs `--single-transaction` for InnoDB. **Finding when** a write during the dump produces a file that cannot be restored with FKs on, or that shows a state the database never had. **Proof:** V561 — concurrent parent/child inserts during the dump: restore into a scratch DB with FKs on succeeds.

### 3. Silent truncation, or a partial file published

```
BAD:   rows.slice(0, MAX_ROWS)                     // the merchant gets 50,000 of 61,214 rows and no message
       await jobs.update(id, { status: 'ready', fileUrl }); await upload(stream)   // ready before the upload finished
GOOD:  if (count > MAX_ROWS) throw new ExportTooLarge(count, MAX_ROWS)   // precedent § 39
       upload to <key>.partial, rename on success, mark ready last; on failure delete the partial and mark failed
```
**Read the code:** What happens at the cap — refuse with a message, split into files, or cut silently? Does the file or the UI say it was capped? In what order are the upload, the stored path and the `ready` status written; what does the failure path do to a half-written object? **Finding when** a consumer can receive fewer rows than the source holds without being told, or a file that a failed run left behind. **Proof:** V562 — a run above the cap refuses or labels; a failure injected mid-upload publishes nothing.

### 4. The representation loses data

```
BAD:   created_at: row.createdAt.toLocaleString()       // server zone, no offset, locale-dependent
       amount: Number(row.amountMinor) / 100            // 0.1 + 0.2 territory; 17-digit totals lose digits
       phone: Number(row.phone)                         // drops the leading zero
GOOD:  created_at: row.createdAt.toISOString() · amount: formatMinor(row.amountMinor) as a string · phone as text
```
**Read the code:** Which zone does each instant come out in, and does the header or the value say so (a `(UTC)` header or ISO-8601 with `Z` is fine)? Are money amounts produced from integer minor units or decimals as strings, or through a float or a locale formatter? Are ids, phone numbers and account numbers written as text cells, or numbers that a spreadsheet will round or strip? **Finding when** the file holds a value that differs from the source value, or an instant a reader cannot place. **Proof:** V562 — round-trip a seeded row (an instant near midnight in a non-UTC zone, `0.1 + 0.2`, a 17-digit id, a leading-zero phone): every value read back equals the source.

## Output

```
extract-scan — lanes: node (mikro-orm 6.4, exceljs 4.4); dumps: app-level table loop; pushes: googleapis
Surface: 0a 14 path-matched · 0b 6 writers · EXP 16

Findings: 2 · Unconfirmed: 2

1. apps/reporting/src/exports/audit-export.runner.ts:40             [report-with-fix]   medium
   §1 EX-1 — `list({ ...filter, page, pageSize })` over activity_log, default order createdAt desc; the module appends
   to activity_log on every request (activity.service.ts:31). V560: 3 inserts mid-export → 3 duplicated rows.
   Fix: keyset on (created_at, id) compared in SQL — the invoices export's `below(lastId)` (invoices-export.runner.ts:88).
2. apps/reporting/src/platform/table-dump.port.ts:48                [report-with-fix]   medium
   §2 EX-2 — per-table pages in separate statements, no isolation anywhere in the file; order_items → orders FK.
   V561: restore with FKs on fails (order_items row with no order). Fix: one REPEATABLE READ read-only transaction.
3. apps/reporting/src/exports/members-export.runner.ts:33           [report-flagged]    medium
   §1 EX-1 — the same OFFSET loop. Unproven link: the members table's write rate during an export. Settling: V560.
4. apps/reporting/src/exports/settlement.mapper.ts:12               [report-flagged]    medium
   §4 EX-4 — paid_at.toLocaleString(). Unproven link: whether the partner parses the column. Settling: V562.

Routed: 1 → database query-shape-scan §2 (deep OFFSET cost on the same loop) · 1 → security injection-scan (formula guard present)
Verification: 11 candidates → 2 findings · 2 unconfirmed · 2 hardening · 5 refuted (self-verified; precedents § 30, § 39)

Class coverage:
  §1 OFFSET paging       checked (1a 9 · 1b 2 files with keyset · 1c 4 → 1 finding, 1 unconfirmed; orders export refuted § 30)
  §2 no snapshot         checked (2a 1 + 2b 0 → 1 finding)
  §3 caps / partial      checked (3a 2 · 3b refusals in both · 3c 3 → 0; ceiling refuses, precedent § 39)
  §4 representation      checked (4 5 → 1 unconfirmed; 4 ISO-8601 with Z → refuted)
```

`[report-with-fix]`: the concurrent-writer or round-trip oracle failed on a scratch DB, or the fact is two-ended (the advancing page + the newest-first order on a table the module writes; the per-table statements + no isolation), and the fix is local to the runner, the base helper or the mapper. `[report-flagged]`: one link is unproven (the write rate, the consumer's parser, the managed restore path); the row names it and the settling oracle. The coverage block lists **all four** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 30 OFFSET inside a `REPEATABLE READ` snapshot, over an immutable partition, or bounded by `id <= :max_id` with a unique order; keyset on `(created_at, id)` compared in SQL.
- § 39 a ceiling that refuses with a message; § 34 the controller exporting its own data to its own destination (for the PII question, which is `pii-copy-scan`'s).
- A quiescent source; `pg_dump`; a header that states the zone; ISO-8601 instants with `Z`.

## When to run

- On any diff that touches an export runner, a sheet push, a dump script, a CSV/XLSX mapper or the list query an export calls — `/audit-data-quality`'s extract signal.
- On every whole-repo `/audit-data-quality`, reporting all four §s; before a partner integration reads a new file.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the source table, its writers, the paging key, the order and the transaction boundary with their `file:line` — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md). Under `/audit-data-quality` that is `@data-quality-auditor` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Never run an export, a dump or a push against a shared or production database or a real destination.** Oracles run on a throwaway container with the project's migrations and a local writer; a destination is a temp directory or a stub server. A probe that cannot be isolated is `NOT-RUN`.
- **This skill writes nothing into the audited repo** and produces no export file outside `$OUT`. `find <root> -newer "$OUT/EXP.txt"` is empty at the end; a fix is `/data-fix`'s.
- **No `[report-with-fix]` without the V-oracle failing** or a two-ended fact. An advancing `page` alone is a candidate until the source's writers and the order are read.
- **Do not grade a class another skill owns** (§ Boundaries). **Do not print "the exports look fine"** without the coverage block.

## Related

- `/audit-data-quality` dispatches this skill; `@data-quality-auditor` judges EX rows; `/data-fix` closes them with V560–V562 failing first.
- This pack: `pii-copy-scan` §5 (personal data in stored exports), `derived-data-scan` (exports built from rollups), `contract-diff` §4 (a migration under an extract's columns).
- database `query-shape-scan` §2/§8, performance `request-path-scan` §6, security `injection-scan`, backend `wire-format-scan`, when those packs are installed.

## Sources

From the data-engineering research (2026-10-19): Use The Index, Luke — "No Offset" (2014, updated 2023-09-08); Laravel 12 query builder `chunk` vs `chunkById` (MIT docs); PostgreSQL 18 transaction isolation, `pg_export_snapshot` and `pg_dump` docs; MySQL 8.4 `mysqldump --single-transaction`; node-postgres type parsing notes (DE-B-10…13). The real-repo shapes (an OFFSET runner beside a keyset export, a catalogue-loop dump, a refusing ceiling) are from the batch-8 eval § 3 (read-only, 2026-10-19). Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
