---
name: pii-copy-scan
description: "Personal data copied into models, rollups, snapshots and exports; classification, erasure reach, masking."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: pii-copy-scan

## Premise

Personal data is protected where it is stored first: the customers table has its access rules, its retention job and its erasure path. Every **copy** escapes them unless someone carries them along: a mart that selects `email`, a dbt snapshot that keeps every historical version of a customer row (SCD2 history survives the erasure of the source row), a rollup keyed by a phone number, a nightly CSV left in a bucket with no lifecycle, a production dump restored into staging, a "safe to share" column that is an unsalted SHA-256 of an email (a dictionary reverses it, and pseudonymised data stays personal data — EDPB Guidelines 01/2025 on pseudonymisation, consultation version 2025-01-16; ICO guidance on the right to erasure, accessed 2026-10-19). Masking can be configured and still not apply: dbt `policy_tags` reach BigQuery only when `persist_docs` writes the columns, and a Snowflake tag-based masking policy applies only to columns whose type matches the policy's.

This skill owns research ids PC-1…PC-6 (`research-data-engineering.md` § 1.8), shipped as `DE-PC-<n>`: **personal data in analytical and exported copies — whether it is classified, reached by erasure, masked where it claims to be, and kept out of lower environments.**

**Every finding cites the copy `<file:line>` (model, snapshot, rollup DDL, export mapper, dump script, bucket) + the personal-data column and its source + the classification found (or none) + the erasure path read (or its absence) + the oracle that would settle it + the fix in the project's own primitive.** A grep hit is a candidate. "Personal data looks protected" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V565–V567.

## The rule

A candidate is a finding when all four hold:

1. **The copy exists and is reachable.** A model is built (not `enabled: false`), a snapshot runs, a rollup is written, an export is produced or pushed, a dump is restored. Seed CSVs with synthetic data fail here.
2. **The column is personal data of a real subject.** An `email`, phone, name, address, national id, IP or birth date of a customer, user or employee — not a merchant's business support address, a system sender, or a value already reduced to an aggregate with no identifier.
3. **No existing control, across files.** A classification the platform enforces (dbt `meta`, a policy tag persisted to the column, a masking policy), an erasure job whose table list covers the copy (or an FK `on delete cascade`, or a trigger that deletes the derived rows), a keyed HMAC with the key in a KMS (precedent § 31), a masking step in the restore pipeline, a lifecycle rule on the bucket, the controller exporting its own data to its own destination (precedent § 34).
4. **The oracle fired, or the fact is two-ended.** V565 (erase a seeded subject, scan every copy) or V567 (a dictionary of common emails hashed with the repo's function finds join hits) ran red on a scratch target; or the static fact cites both ends — the erasure job's table list and the derived table that carries the identifier; the PII column in the model and the absence of any classification for it.

## Boundaries

- **OLTP storage, retention and the erasure mechanics of the source tables** → database `schema-integrity-scan` §10 (when installed); this skill reads its erasure-path row and checks the copies. **Who may read or export personal data, PII in logs, traces and error trackers** → security `data-exposure-scan` §6 and `@data-privacy-reviewer`. **Analytics SDK payloads** (Segment, Mixpanel event properties) → security and product `tracking-plan-scan`. **Backups** (retention, encryption, restore) → infrastructure `dr-audit`; precedent § 32 covers erased subjects in rotating backups. Each when installed; without them the row is `[report-flagged]` here with the route named.
- **A copy that is wrong for a non-privacy reason** (stale, doubled) → `derived-data-scan` / `incremental-load-scan`; **an export's consistency** → `extract-scan`. Deletes that never reach a warehouse table are `incremental-load-scan` §4; when the deleted row is a subject's personal data the row is cited here as §2 too.
- **This skill never decides a legal basis or a retention period.** A missing policy is `UNDECLARED`, printed as an enabler; `/data-fix` asks before writing one.

## Adapt to the codebase — the lanes

| Lane | Detect by | Classification / erasure idioms read | Fix primitive |
|---|---|---|---|
| **dbt** (any adapter) | `dbt_project.yml`; `models/**/*.yml`; `snapshots/` | column `meta: {pii: true}` / `contains_pii`, `tags: [pii]`, `policy_tags:` (BigQuery) + `persist_docs: {columns: true}`, Snowflake masking policies and tags, Databricks column masks | classify in YAML; mask or drop in staging; `hard_deletes: invalidate` + an erasure macro over snapshots |
| **In-app derived tables** (Postgres/MySQL; any ORM) | migrations and entities of `*_daily`, `*_stats`, `*_snapshots`, `*_exports`, analytics/reporting tables | the erasure handler's table list; FK `on delete cascade`; delete triggers | carry the subject id and cover it in the erasure job, or keep only aggregates |
| **Exports and pushes** | export runners and mappers (`extract-scan` 0a/0b), storage buckets, third-party clients | retention on stored files; destination ownership | expire stored files; push only the controller's own data to its own destination |
| **Lower environments** | `pg_dump`/`pg_restore`/`mysqldump` scripts, CI jobs, Makefiles, seed-from-prod scripts | a masking step (`pg_anonymizer`/`anon.`, a masking view, `--exclude-table-data`, faker) | restore through a masking step; synthetic seeds |
| **Hashing** | `createHash`, `hashlib`, SQL `md5`/`sha2` on identifiers | key, salt, pepper, HMAC | keyed HMAC with a managed key; treat the output as personal data |
| **IaC** (Terraform, Pulumi, CloudFormation) | `aws_s3_bucket`, `google_storage_bucket`, BigQuery datasets | lifecycle rules, `partition_expiration_days`, `default_table_expiration_ms` | a lifecycle rule; table expiration on raw landing |

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; 0 builds the surface. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; two **path** globs may stand together (they are meant to OR) but a path glob is never combined with an extension glob. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. **Migrations, CI files and IaC are in scope.** Nothing is written outside `$OUT`; no personal value is printed — the greps print column names and lines of code, and a probe that would sample rows prints counts only.

```bash
ROOTS=(.)   # monorepo: name the analytics, app and infra roots, e.g. ROOTS=(analytics apps/api/src infra)
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-pc.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,venv,dbt_packages,logs}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/test_*.py' -g '!**/*_test.{py,go}'
   -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.{md,mdx,lock,min.js,snap}')
CODE=(-g '*.{ts,mts,js,mjs,cjs,py,rb,php,java,kt,go,cs,sql}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#|--)')
PV='(?i)\b(?:\w+_)?(?:e_?mail(?:_?address)?|phone(?:_?number)?|mobile(?:_?number)?|msisdn|ip_?address|first_?name|last_?name|full_?name|customer_?name|address(?:_?line_?\d)?|street(?:_?address)?|dob|date_?of_?birth|birth_?date|national_?id|ssn|iban|passport(?:_?(?:no|number))?|tax_?id)\b'
# 0 THE COPY SURFACE — 0a dbt projects · 0b analytical/derived tables in migrations · 0c erasure handlers · 0d export and dump files
h 0a; rg --files -g '**/dbt_project.yml' "${X[@]}" "${ROOTS[@]}"; ck 0a $?
AN='((?:\w+_)?\w+_(?:daily|hourly|weekly|monthly|summary|summaries|stats|rollups?|agg|aggregates?|totals|facts|snapshots?|history|exports?|extracts?|report\w*|analytics|events_flat)|(?:analytics|reporting|warehouse|dw|mart)_\w+)'
h 0b; rg -n -U --pcre2 "(?i)\\bcreate\\s+table\\s+(?:if\\s+not\\s+exists\\s+)?[\"\\x27\`]?$AN(?!\\w)[\"\\x27\`]?\\s*\\([^;]{0,4000}?$(printf '%s' "$PV" | sed 's/^(?i)//')" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg -o --pcre2 "(?i)^[^:]+:\\d+:.*?create\\s+table\\s+(?:if\\s+not\\s+exists\\s+)?[\"\\x27\`]?\\w+" | sort -u | tee "$OUT/PCT.txt"; ck 0b ${PIPESTATUS[0]}
h 0c; rg -l --pcre2 '(?i)\b(?:erase|erasure|anonymi[sz]e\w*|right_?to_?be_?forgotten|forget(?:Customer|User|Subject)\w*|redact(?:Customer|User|Subject)\w*|gdpr|dsar|purge(?:Customer|User|Account|Subject)\w*)\b' "${CODE[@]}" "${X[@]}" -g '!**/{migrations,migration}/**' "${ROOTS[@]}" | sort -u | tee "$OUT/ERASE.txt"; ck 0c ${PIPESTATUS[0]}
h 0d; rg --files -g '**/*{export,Export,sheet,Sheet,dump,Dump,extract,Extract,backup,Backup,seed,Seed,restore,Restore}*' "${X[@]}" "${ROOTS[@]}" | rg -v --pcre2 '\.(?:md|json|csv|txt|svg|png)$' | sort -u > "$OUT/EXP.txt"; wc -l < "$OUT/EXP.txt"
E=(); while IFS= read -r f; do E+=("$f"); done < "$OUT/EXP.txt"; [ ${#E[@]} -gt 0 ] || E=("$OUT/none")
# 1 PC-1 classification — 1a dbt YAML files that declare a PII-named column and carry no classification · 1b PII selected in marts/snapshots SQL · 1c 0b's tables (read)
h 1a; rg -l --pcre2 "^\\s*-\\s*name:\\s*[\"\\x27]?$(printf '%s' "$PV" | sed 's/^(?i)//')[\"\\x27]?\\s*\$" -i -g '**/models/**/*.{yml,yaml}' -g '**/snapshots/**/*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '(?i)\b(?:pii|contains_pii|personal_data|sensitive|classification|policy_tags|masking_policy|mask)\b'
h 1b; rg -n -w --pcre2 "$PV" -g '**/models/marts/**' -g '**/models/intermediate/**' -g '**/snapshots/**' -g '**/models/**/*{mart,fct,dim,rpt,agg}*' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\.sql:' | "${NC[@]}" | head -60; ck 1b ${PIPESTATUS[0]}
# 2 PC-2 erasure reach — 2a the tables the erasure handlers touch · 2b dbt snapshots (SCD2 history) of any source · 2c 0b tables the handlers never name · 2d Delta deletes with no VACUUM
ERS=(); while IFS= read -r f; do ERS+=("$f"); done < "$OUT/ERASE.txt"; [ ${#ERS[@]} -gt 0 ] || ERS=("$OUT/none")
h 2a; rg -o -I --no-filename --pcre2 -r '$1$2' '(?i)\b(?:delete\s+from|update|truncate(?:\s+table)?)\s+"?(\w+)"?|\bnative(?:Delete|Update)\(\s*(\w+)' "${ERS[@]}" | sort -u | tee "$OUT/ERASED.txt" | tr '\n' ' '; echo
h 2b; rg -l --pcre2 '\{%-?\s*snapshot\s+\w+|^\s*snapshots\s*:' -g '**/snapshots/**' "${X[@]}" "${ROOTS[@]}"; ck 2b $?
h 2c; sed -E 's/.*create[[:space:]]+table[[:space:]]+(if[[:space:]]+not[[:space:]]+exists[[:space:]]+)?["`'"'"']?//I' "$OUT/PCT.txt" | sort -u | while IFS= read -r t; do [ -n "$t" ] || continue; grep -qixF "$t" "$OUT/ERASED.txt" && echo "$t erased-by-handler" || echo "$t NOT named by any erasure handler (read FKs/cascades/triggers)"; done
h 2d; rg -l --pcre2 '(?i)\bdelete\s+from\b[^;\n]*' -g '*.{py,sql,scala}' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg -l --pcre2 '(?i)\bdelta\b|DeltaTable' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '(?i)\bvacuum\b|reorg\s+table[^;]*apply\s*\(\s*purge'
# 3 PC-3 pseudonymisation treated as anonymisation — unkeyed hashes of identifiers; columns named anon* fed by them
h 3; rg -n --pcre2 '(?i)createHash\(\s*["\x27](?:md5|sha1|sha256|sha512)["\x27]\s*\)\s*\.update\([^)]*(?:email|phone|mobile|msisdn|national|ssn)|\bhashlib\.(?:md5|sha1|sha256|sha512)\([^)]*(?:email|phone|mobile|msisdn|ssn)|\b(?:md5|sha1|sha256|sha2|sha512|farm_fingerprint|hash)\s*\(\s*(?:lower\s*\(\s*)?(?:trim\s*\(\s*)?(?:\w+\.)?\w*(?:email|phone|mobile|msisdn|ssn)\w*|\b\w*anon\w*\s*(?:=|:|as)\s*[^\n]*(?:md5|sha1|sha256|createHash|hashlib)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg -v --pcre2 '(?i)\bhmac\b|createHmac|\bsalt\b|\bpepper\b|\bsecret\b|\bkms\b' | "${NC[@]}"; ck 3 ${PIPESTATUS[0]}
# 4 PC-4 production copied down — dump/restore/seed-from-prod pipelines with no masking step in the same file
h 4; rg -l --pcre2 '(?i)\bpg_dump\b[^\n]*(?:\|\s*psql|-f)|\bpg_restore\b|\bmysqldump\b[^\n]*\|\s*mysql|\bseed[_-]?from[_-]?prod\w*|\bcopy[_-]?prod\w*|\b(?:prod|production)\b[^\n]{0,80}\b(?:staging|stage|dev|qa|preview)\b[^\n]{0,80}\b(?:restore|load|import|sync)\b' -g '*.{sh,bash,py,ts,js,rb,yml,yaml,toml}' -g '**/Makefile' -g '**/Dockerfile*' --hidden "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '(?i)\bpg_anonymi[sz]er\b|\banon\.\w+|\banonymi[sz]e\b|\bmask\w*|\bfaker\b|\bscrub\w*|\bsanitiz\w*|--exclude-table-data'
# 5 PC-5 stored or pushed exports — 5a buckets/datasets with no lifecycle or expiry (IaC) · 5b export files that store a file and name no expiry · 5c third-party destinations in export files (read § 34)
h 5a; rg -l --pcre2 '\bresource\s+"(?:aws_s3_bucket|google_storage_bucket|google_bigquery_dataset|azurerm_storage_container)"\s+"\w*(?:export|extract|report|dump|landing|raw|analytics)\w*"' -g '*.{tf,tf.json}' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'aws_s3_bucket_lifecycle_configuration|lifecycle_rule|partition_expiration_days|default_table_expiration_ms|default_partition_expiration_ms'
h 5b; rg -l --pcre2 '(?i)\b(?:putObject\w*|upload\w*|writeFile|createWriteStream|save_to|blob\.upload|bucket\.file)\s*\(' "${E[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '(?i)\b(?:expires?_?(?:at|in)|ttl|retention|lifecycle|delete_?after|purge\w*|cleanup\w*|prune\w*)\b'
h 5c; rg -n --pcre2 '(?i)\bgoogleapis\b|sheets\.spreadsheets|\bsftp\b|\bhubspot\b|\bmailchimp\b|\bsalesforce\b|\bsegment\b|\bamplitude\b|\bmixpanel\b|\bintercom\b|\bklaviyo\b' "${E[@]}" | "${NC[@]}" | head -20; ck 5c ${PIPESTATUS[0]}
# 6 PC-6 masking configured but not effective — policy_tags with no persist_docs columns · masking policies and their tagged columns (read the types)
h 6a; rg -l --pcre2 '\bpolicy_tags\s*:' -g '*.{yml,yaml,sql}' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do echo "$f"; done; rg -n -U --pcre2 'persist_docs\s*[:=]\s*\{?[\s\S]{0,80}?columns\s*[:=]\s*(?:true|True)' -g '*.{yml,yaml,sql}' "${X[@]}" "${ROOTS[@]}"; ck 6a $?
h 6b; rg -n --pcre2 '(?i)\bcreate\s+(?:or\s+replace\s+)?masking\s+policy\s+[\w.]+\s+as\s*\(\s*\w+\s+(\w+)[^)]*\)\s*returns\s+\w+|\bset\s+masking\s+policy\b|\bset\s+tag\b|\balter\s+tag\b[^;]*\bset\s+masking\s+policy\b' -g '*.{sql,yml,yaml,tf,py}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 6b ${PIPESTATUS[0]}
```

2c prints each 0b table with a PII column and whether any erasure handler names it: `NOT named` is a §2 candidate until a foreign key `on delete cascade`, a delete trigger, or a whole-period recompute that drops the subject's rows is read (a real repo closes its rollup's erasure through an `after delete` trigger on the source — read the triggers before reporting). 2b lists every dbt snapshot: a snapshot of a PII-bearing source keeps history after erasure unless an erasure macro or `hard_deletes` plus a scrub runs over it.

### Measured (2026-10-19)

- **Fixture** (`benchmarks/fixtures/data-pipelines`, `ROOTS=(.)`; under 1 s, 0 `rg` errors; no personal value printed): 0b 1 derived table with a PII column (`customer_ltv_daily`) · 0c 1 erasure handler · 0d 17 export/dump/seed files · 1a 1 (the customer dimension's model YAML; the classified contacts file is excluded) · 1b 14 lines · 2a the handler's tables (`customers orders sessions`) · 2b 2 snapshots · 2c 1 `NOT named` · 3 2 (an unkeyed SHA-256 in a partner feed and in a mart; the keyed HMAC is not listed) · 4 2 (a `pg_dump | psql` into staging, a `pg_restore` target; the masked preview restore is excluded) · 5a 1 bucket without lifecycle (the archive bucket with one is excluded) · 5b 2 · 5c 2 (the merchant's own-data sheet push, precedent § 34) · 6a 1 (`policy_tags`, no `persist_docs`) · 6b 4 (a string masking policy tagged onto a NUMBER column).
- **Real repo, read-only** (the NestJS monorepo, `ROOTS=(apps/api/src)`; 0.4 s; nothing written): 0a 0 (no dbt) · 0b 0 — no derived table carries a PII-named column; the order-day rollup holds counts and amounts, and its erasure is closed by the delete trigger on orders · 0c 20 files (customer and order erasure ports, a purge executor, and words like `purge` in unrelated modules — read) · 2a names entity classes (`CustomerEntity`, `CustomerPhoneEntity`, …) because the handlers delete through the ORM; the read maps them to tables · 3 0 · 4 0 in code (dumps are an operator download, `extract-scan` §2) · 5–6 0. The purge manifest's sentence that "no daily rollup table" exists is documentation drift (documentation `doc-drift-scan`), not PC-2. **First drafts this measurement corrected:** the PII vocabulary missed prefixed columns (`customer_email`) behind a `\b`; the upload grep missed the AWS SDK v3 `PutObjectCommand`; the SQL hash grep missed qualified columns (`lower(c.email)`).
- **The dbt, IaC and masking-policy lanes are fixture-measured only.**

## The 3,000-hit path

1. **Build the copy inventory once**: every model, snapshot, derived table, export and dump that carries a PII-named column (0a, 0b, 1b, 0d). Group by **source column** — one `customers.email` flowing into twelve marts is one classification decision at the staging model.
2. **Join it with the erasure path once** (0c, 2a): the copies the handler never names are the §2 list; read cascades and triggers for each before it is a candidate.
3. **Rank** by exposure: copies that leave the database (exports, pushes, lower environments, shared datasets) first; internal marts with access control next; aggregates last.
4. **Prefer erase-then-scan at scale** (V565): seed one subject with distinctive values, run the erasure and every build, then grep every derived table, snapshot, refreshed view and stored export for those values — one run settles the whole §2 list.
5. **Ledger the rest** as `Live, unreviewed (k copies / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes a real subject's data. One step lower when the copy is access-controlled and internal; a copy that leaves the organisation (a push, a shared bucket, a lower environment) stays at its default or higher.

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | PC-1 PII in models, rollups, snapshots or landing tables with no classification | medium | V566 |
| 2 | PC-2 erasure does not reach derived copies (snapshots, rollups with identifiers, stored exports, landing tables) | high | V565 |
| 3 | PC-3 pseudonymisation treated as anonymisation | medium | V567 |
| 4 | PC-4 production data copied to a lower environment without masking | high | V567 |
| 5 | PC-5 stored or pushed exports with no retention or access rule | medium | V565 |
| 6 | PC-6 masking configured but not effective | medium | V566 |

### 1. Unclassified personal data in an analytical copy

```
BAD:   models/marts/dim_customers.yml:  - name: email   (no meta, no policy tag)
       create table customer_ltv_daily (day date, customer_email text, ltv numeric)
GOOD:  - name: email  meta: {contains_pii: true}  policy_tags: ['…/pii_email']   (+ persist_docs columns)
       keep customer_id only; resolve the email at read time behind the app's access rules
```
**Read the code:** Is the column a real subject's (a customer, a user, an employee) or a business contact? Does the project classify anywhere (a `+meta` default in `dbt_project.yml` by path, a policy-tag macro, a masking view) — read the effective value, not only the model's YAML? Does the copy need the raw value at all, or would the id do? **Finding when** personal data sits in an analytical copy with no classification the platform or the team acts on. **Proof:** V566 — every PII column in analytical copies carries a classification (two-ended: the column and the absent classification); a low-privilege role reads masked values.

### 2. Erasure does not reach the copy

```
BAD:   erase-account.handler.ts deletes from accounts and orders; snapshots/accounts_snapshot.sql keeps every version
       customer_ltv_daily keyed by customer_email, written by a cron, never named by the erasure handler
GOOD:  the erasure job's table list includes every copy (or the copy holds no identifier); snapshots get an erasure macro;
       stored exports are deleted or expire; a delete trigger or FK cascade removes derived rows
```
**Read the code:** Which tables does the erasure handler touch (2a), and through what — direct statements, an FK `on delete cascade`, a delete trigger on the source that removes or marks derived rows, a recompute that drops the subject's contribution? For dbt snapshots (2b): is there a scrub over the snapshot table, or does SCD2 history keep the subject forever? Delta tables: `DELETE` without `VACUUM` keeps the files (2d). Backups on rotation are precedent § 32. **Finding when** an erased subject's values remain in a derived table, snapshot, refreshed view, stored export or landing table. The OLTP erasure path itself is database `schema-integrity-scan` §10's. **Proof:** V565 — erase a seeded subject; no copy holds its values.

### 3. Pseudonymisation treated as anonymisation

```
BAD:   anon_email = sha256(lower(email))                       // shared with a partner as "anonymous"
       createHash('md5').update(user.email).digest('hex')      // reversible by a dictionary of common emails
GOOD:  createHmac('sha256', kms.key('pii-join')).update(email)  // keyed; the output is still personal data (precedent § 31)
```
**Read the code:** Is the hash keyed (HMAC with a secret from a KMS or a secret store) or a bare digest? Is the output shared, exported, labelled anonymous, or used only as an internal join key (precedent § 33)? **Finding when** an unkeyed hash of an identifier leaves the controlled environment or is treated as non-personal. **Proof:** V567 — hash 10k common emails with the repo's function: zero join hits against the shared column.

### 4. Production data copied to a lower environment

**Read the code:** Does a script, Makefile target or CI job restore a production dump into staging, dev, QA or a preview environment? Is there a masking step in the same pipeline (`pg_anonymizer`, a masking view, `--exclude-table-data` for the PII tables, a faker pass)? Synthetic seeds are not this class. **Finding when** production personal data reaches an environment with weaker access control. **Proof:** V567 — a sample of the lower environment holds no production identifier.

### 5. Stored or pushed exports with no retention or access rule

**Read the code:** Where does the export land — a bucket, a disk path, an email attachment, a third-party API? Does the bucket have a lifecycle rule, the job an expiry, the download a signed URL with a short life? Is the destination the controller's own (precedent § 34: a merchant pushing its own customers to its own sheet) or a third party's? Raw landing datasets: table or partition expiration? **Finding when** exported personal data is kept with no rule that ends it, or pushed to a destination nobody controls. **Proof:** V565 — after erasure and the retention window, the stored export no longer holds the subject.

### 6. Masking configured but not effective

**Read the code:** BigQuery: are `policy_tags` declared and `persist_docs: {columns: true}` set for the same models (6a)? Snowflake: does each tag-based masking policy's input type match the type of every column the tag reaches (6b) — a `string` policy skips a `number` column? Databricks: is the column mask attached to the table the readers query, or to a staging copy? **Finding when** a column the team believes masked is readable in clear by a role that should see it masked. **Proof:** V566 — the low-privilege role reads masked values.

## Output

```
pii-copy-scan — lanes: dbt 1.9 (dbt-duckdb; bigquery in prod profile); app: postgres 17 migrations; iac: terraform (aws)
Surface: 0b 2 tables with PII columns · 0c 2 erasure handlers · 2b 2 snapshots · 0d 9 export/dump files

Findings: 2 · Unconfirmed: 2 · Enabler: 1

1. analytics/snapshots/accounts_snapshot.sql:1                     [report-with-fix]   high
   §2 PC-2 — SCD2 snapshot of raw.accounts (email, phone, full_name); the erasure handler
   (apps/reporting/src/privacy/erase-account.handler.ts:14) names accounts and orders only. V565 on duckdb:
   the erased subject's email remains in 3 snapshot versions. Fix: an erasure macro over the snapshot + hard_deletes.
2. apps/reporting/migrations/Migration20260410.ts:12               [report-with-fix]   high
   §2 PC-2 — customer_ltv_daily keeps customer_email; no handler, cascade or trigger reaches it. Two-ended.
   Fix: key by customer_id and resolve the email at read time; add the table to the erasure job until then.
3. apps/reporting/src/exports/affiliate-feed.ts:33                 [report-flagged]    medium
   §3 PC-3 — sha256(lower(email)) as anon_id in a partner feed. Unproven link: whether the partner can join on it.
   Settling: V567.
4. infra/object-store.tf:4                                         [report-flagged]    medium
   §5 PC-5 — aws_s3_bucket "exports" with no lifecycle configuration. Unproven link: whether a cleanup job deletes files.
5. (policy)                                                        Enabler             —
   No retention period is declared for exported files (UNDECLARED) — /data-fix asks before writing one.

Routed: 1 → security data-exposure-scan §6 (email in a log line) · 1 → documentation doc-drift-scan (a manifest sentence)
Verification: 14 candidates → 2 findings · 2 unconfirmed · 1 enabler · 3 hardening · 6 refuted (self-verified; precedents § 31, § 33, § 34)

Class coverage:
  §1 classification      checked (1a 2 files + 1b 11 → hardening: internal marts, effective +meta from dbt_project.yml)
  §2 erasure reach       checked (2a 4 tables · 2b 2 snapshots · 2c 2 → 2 findings)
  §3 pseudonymisation    checked (3 2 → 1 unconfirmed; 1 keyed HMAC refuted, precedent § 31)
  §4 lower environments  checked (4 1 → 0; the restore runs through pg_anonymizer)
  §5 stored exports      checked (5a 1 + 5b 1 + 5c 1 → 1 unconfirmed; the sheet push is the merchant's own data, § 34)
  §6 masking effective   N/A (no policy tags or masking policies)
```

`[report-with-fix]`: erase-and-scan or the dictionary oracle failed on a scratch target, or the fact is two-ended (the erasure list and the copy; the column and the absent classification), and the fix is local to the model, the handler, the hash call or the pipeline. `[report-flagged]`: one link is unproven (a cleanup job outside the repo, the partner's ability to join, the effective masking in the warehouse); the row names it and the settling oracle. The coverage block lists **all six** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 31 a keyed HMAC with the key in a KMS; § 32 erased subjects in rotating backups never restored without re-applying erasures; § 33 a hash used only as an internal join key; § 34 the subject's own access response, or the controller exporting its own data to its own destination.
- Synthetic seeds and a masked restore (not PC-4); a business contact address (not a subject's personal data); an aggregate with no identifier.

## When to run

- On any diff that adds a column to a model, snapshot, rollup or export mapper; touches an erasure handler; adds a dump/restore script, a bucket or a third-party push — `/audit-data-quality`'s analytical-PII signal.
- On every whole-repo `/audit-data-quality`, reporting all six §s; before a dataset is shared outside the team.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the copy, the column, the erasure list and the classification read with their `file:line` — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md). Under `/audit-data-quality` that is `@data-quality-auditor` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`.
- **Never print, copy or sample a personal value.** Probes report counts and column names; V565 seeds a synthetic subject; V567 hashes a public dictionary, never production values.
- **Never run an erasure, a restore or a build against a shared or production target.** Oracles run on duckdb, a throwaway container or a target the user confirmed is not production; a probe that cannot be isolated is `NOT-RUN`.
- **This skill writes nothing into the audited repo.** `find <root> -newer "$OUT/EXP.txt"` is empty at the end; a fix is `/data-fix`'s, and a retention period or a legal basis is the user's decision.
- **No `[report-with-fix]` without the V-oracle failing** or a two-ended fact. **Do not grade a class another skill owns** (§ Boundaries). **Do not print "personal data looks protected"** without the coverage block.

## Related

- `/audit-data-quality` dispatches this skill; `@data-quality-auditor` judges PC rows; `/data-fix` closes them with V565–V567 failing first.
- This pack: `derived-data-scan` (the rollups 0b reads), `extract-scan` (the export files 0d reads), `incremental-load-scan` §4 (deletes that never reach a warehouse table), `lineage-trace` (which marts a PII column flows into).
- database `schema-integrity-scan` §10, security `data-exposure-scan` §6 and `@data-privacy-reviewer`, infrastructure `dr-audit`, product `tracking-plan-scan`, documentation `doc-drift-scan`, when those packs are installed.

## Sources

From the data-engineering research (2026-10-19): EDPB Guidelines 01/2025 on pseudonymisation (2025-01-16, consultation; final text UNVERIFIED there) and commentary on EDPS v SRB C-413/23 P; ICO right to erasure (OGL v3.0); Databricks GDPR with Delta (VACUUM, REORG … APPLY (PURGE)); Snowflake tag-based masking; Databricks row filters and column masks; dbt BigQuery configs (`policy_tags`, `persist_docs`) (DE-B-30…35). The real-repo shapes (a delete trigger closing a rollup's erasure, a merchant's own-data sheet push) are from the batch-8 eval § 3 (read-only, 2026-10-19). Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
