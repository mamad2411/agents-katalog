---
name: storage-growth-scan
description: "App-written growth with no end: object prefixes, multipart, append-only tables, local disk (ST-1…4)."
kind: skill
pack: finops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: storage-growth-scan

## Premise

Storage bills by the GB-month and never stops on its own. The IaC can declare a bucket's lifecycle, but the application decides what goes into it: an export written per tenant per day, a temporary upload never deleted, a thumbnail per image size, an event table that only receives inserts. A bucket rule scoped to `backups/` covers nothing under `exports/`; a database whose storage grew never shrinks in place (Amazon RDS documentation). This skill maps **what the application writes** to **what ever removes it**, per object prefix, per multipart path, per append-only table and per local disk, and reports the writes that nothing ends.

**Every finding cites the write `<file:line>` + the prefix, table or path it lands in + the absence of an expiry rule, delete path or retention job for that prefix or table + the oracle.** A write with a rule on its prefix, a delete path or a retention job is not a finding. Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/finops.md`](../../../../snippets/precedents/finops.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § FinOps, V583–V586.

| § | Class | What is wrong | Oracle |
|---|---|---|---|
| 1 | ST-1 | an app-written object prefix with no expiry and no delete path | **V583** |
| 2 | ST-2 | multipart uploads with no abort-incomplete rule on the target bucket | **V584** |
| 3 | ST-3 | an append-only table with no retention job, partition drop or TTL | **V585** |
| 4 | ST-4 | local disk or PVC growth with no rotation or cap | **V586** |

## The rule

1. **The write runs in production** (gate 1): a route, job or consumer. Scripts that ran once, seeds and tests fail here.
2. **The data is derived or transient** (gate 5): exports, temp uploads, generated reports, thumbnails, delivery logs, idempotency keys, outbox rows. Data that **is the product's record** — tenant uploads, invoices, contracts, ledgers — is a business retention rule: ask, never report (precedents § 20, § 21).
3. **Nothing ends it** (gate 4): no lifecycle rule on **that** prefix (IaC, or an operator rule recorded with its read-back — Hardening "out of code", § 19), no delete path the code reaches, no retention job, partition drop or TTL index for **that** table.
4. **The provider supports the fix** (gate 3): DigitalOcean Spaces lifecycle supports Expiration and AbortIncompleteMultipartUpload only, and its Terraform `lifecycle_rule` carries `prefix` (provider docs, verified 2026-07-13 per the research pass); R2 and MinIO differ — read the provider's dated page before reporting.

## Boundaries

- **IaC bucket lifecycle, versioning without noncurrent expiry** → infrastructure `iac-cost-scan` § 7 (COST-07) and `dr-audit` § 7, when that pack is installed. This skill reads the IaC rule only to see whether it covers the **app's** prefix; it never re-grades versioning.
- **Backup retention** → infrastructure `dr-audit`. **Cache keys without TTL** → performance `caching-scan` § 1. **Loki, Prometheus and Tempo retention** → observability `telemetry-config-scan` § 6. **PVC `reclaimPolicy: Retain`** → infrastructure `k8s-availability-scan` § 8.
- **Personal data in a prefix or table** → the retention half goes to security `@data-privacy-reviewer` (security pack, when installed); the growth half stays here. Without that pack the row carries `privacy-class (owner pack security not installed)`.
- **The retention job's correctness** (batching, locks, the predicate's index) → database `transaction-scan` / `index-coverage-scan`; **its schedule overlapping itself** → backend `job-lifecycle-scan` § 4.

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N. Every `rg` names its path; include globs first, exclusions last. Migrations are excluded everywhere **except 3a**, where tables are born; runbooks and deploy comments are read by 1e, because an operator-set rule lives there. Every grep ends in `ck`: rg exit 2 is a **blocked** class. An empty `ROOTS` stops the script.

```bash
ROOTS=(.)   # monorepo: name the service roots, the IaC roots and the runbook folder
[ -n "${ROOTS[0]:-}" ] || { echo "ROOTS empty — every § blocked (an unset path makes rg search the cwd)"; exit 2; }
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/finops-store.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
XB=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,venv,.terraform}/**'
    -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/*.{spec,test,e2e-spec,stories}.*'
    -g '!**/*.test-data.*' -g '!**/{locales,i18n,translations}/**' -g '!**/{.git,.claude}/**' -g '!**/ai/audits/**')
X=("${XB[@]}" -g '!**/migrations/**')            # migrations are read only by 3a (where tables are born)
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,go,java,kt,rb,php,cs}' "${X[@]}")
RULES=(-g '*.{tf,tofu,yaml,yml,json,xml,md,mdx,sh}' "${X[@]}" -g '!**/{package,package-lock,tsconfig,composer}*.json' -g '!**/CHANGELOG.md')
# 1 ST-1 object writes (1a) → the wrapper's prefix or area table (1b, read the code) → lifecycle rules in IaC (1c) and in
#   runbooks, deploy comments or scripts (1e) → delete paths (1d)
h 1a; rg -n --pcre2 '\bnew\s+(PutObjectCommand|Upload|CreateMultipartUploadCommand|CopyObjectCommand)\s*\(|\.(put_object|upload_file|upload_fileobj|copy_object|fPutObject|uploadData|uploadFile|uploadStream)\s*\(|\.putObject\s*\(|\bbucket\.(file\([^)]*\)\.save|upload)\s*\(|\bblob\.upload_from_(string|filename|file)\s*\(|\bStorage::(disk\([^)]*\)->)?put\w*\(' "${CODE[@]}" "${ROOTS[@]}"; ck 1a $?
h 1b; rg -n --pcre2 '\b(prefix|Prefix|area|Area|folder|keyPrefix|key_prefix|s3Area|basePath)\s*[:=]\s*["\x27\x60][\w.${}-]+/["\x27\x60]|\bKey\s*[:=]\s*\x60[\w.-]+/\$\{' "${CODE[@]}" "${ROOTS[@]}"; ck 1b $?
h 1c; rg -n --pcre2 '^\s*resource\s+"(aws_s3_bucket_lifecycle_configuration|google_storage_bucket|azurerm_storage_management_policy|digitalocean_spaces_bucket)"|^\s*(lifecycle_rule|rule)\s*\{|^\s*(prefix|expiration|days|age|abort_incomplete_multipart_upload_days)\s*[={]' -g '*.{tf,tofu}' "${X[@]}" "${ROOTS[@]}"; ck 1c $?
h 1e; rg -n --pcre2 '\b(put|get)-bucket-lifecycle(-configuration)?\b|\bs3cmd\s+(set|get)lifecycle\b|\bmc\s+ilm\b|<LifecycleConfiguration>|"(Expiration|NoncurrentVersionExpiration)"\s*:|(?i:\blifecycle\s+rules?\b)' "${RULES[@]}" "${ROOTS[@]}"; ck 1e $?
h 1d; rg -n --pcre2 '\bnew\s+(DeleteObjectCommand|DeleteObjectsCommand)\s*\(|\.(delete_object|delete_objects|deleteObject|deleteObjects|removeObject|removeObjects)\s*\(|\bblob\.delete\s*\(|\bStorage::(disk\([^)]*\)->)?delete\(' "${CODE[@]}" "${ROOTS[@]}"; ck 1d $?
# 2 ST-2 multipart paths and the abort rule on their bucket
h 2a; rg -n --pcre2 '\bnew\s+Upload\s*\(|\bCreateMultipartUploadCommand\b|\bcreate_multipart_upload\b|\.upload_file(obj)?\s*\(|\bTransferConfig\s*\(|\bmultipart_threshold\b|\bPutObjectStream\b|\bnew\s+TransferManager\b' "${CODE[@]}" "${ROOTS[@]}"; ck 2a $?
h 2b; rg -n --pcre2 '\bAbortIncompleteMultipartUpload\b|\babort_incomplete_multipart_upload(_days)?\b|\bDaysAfterInitiation\b' "${RULES[@]}" "${ROOTS[@]}"; ck 2b $?
# 3 ST-3 append-only tables — 3a tables whose name says they only grow (migrations and schema included), 3b retention
#   paths (a delete by age, a partition drop, a TTL index, a retention/purge job)
h 3a; rg -n -i --pcre2 '\b(create\s+table(\s+if\s+not\s+exists)?|@Entity\(\s*\{?\s*(tableName|name)\s*:|\b__tablename__\s*=|\bdb_table\s*=|\bmodel\s+|\btableName\s*:|\bpgTable\(|\bcreate_table\s*\(?)\s*["\x27\x60]?\w*(event|log|audit|outbox|inbox|idempoten|webhook|deliver|notification|history|activit|job_?run|snapshot|session|attempt|trace|metric)\w*' -g '*.{sql,ts,js,py,rb,prisma,go,java,kt,php,cs}' "${XB[@]}" "${ROOTS[@]}"; ck 3a $?
h 3b; rg -n -i --pcre2 '\bdelete\s+from\s+\S+\s+where\s+[^;]*\b\w*(created|inserted|occurred|received|updated|expire|sent|at|time|ts)\w*\s*<|\b(nativeDelete|deleteMany|delete_many|destroy_all|delete|where)\s*\([^)\n]*(\$lte?\b|__lte?\b|\blte?\(|<\s*[\w(:$])|\bpg_partman\b|\b(drop|detach)\s+partition\b|\bexpireAfterSeconds\b|\bTimeToLiveSpecification\b|^\s*ttl\s*\{|\bclass\s+\w*(Retention|Purge|Prune|Cleanup|Sweep)\w*|\b(sweep|prune|purge)(Expired|Old|Stale)\w*\s*\(' "${CODE[@]}" -g '*.{sql,tf}' "${X[@]}" "${ROOTS[@]}"; ck 3b $?
# 4 ST-4 local growth: file loggers (4a) and their rotation (4b); writer emptyDir and sizeLimit (4c); per-request temp files (4e)
h 4a; rg -n --pcre2 '\bnew\s+winston\.transports\.File\b|\bpino\.destination\s*\(|\blogging\.FileHandler\s*\(|\bFileHandler\s*\(|\bcreateWriteStream\s*\([^)]*\.log\b|\blog4j\.appender\.\w+=org\.apache\.log4j\.FileAppender\b|<appender[^>]*FileAppender' "${CODE[@]}" -g '*.{xml,properties,yaml,yml}' "${X[@]}" "${ROOTS[@]}"; ck 4a $?
h 4b; rg -n --pcre2 '\bRotatingFileHandler\b|\bTimedRotatingFileHandler\b|winston-daily-rotate-file|\bpino-roll\b|\blumberjack\b|RollingFileAppender|\bmaxsize\s*:|\bmaxFiles\s*:|\blogrotate\b' "${CODE[@]}" -g '*.{xml,properties,yaml,yml,conf}' "${X[@]}" "${ROOTS[@]}"; ck 4b $?
h 4c; rg -n --pcre2 '^\s*emptyDir:\s*(\{\s*\})?\s*$|^\s*sizeLimit:' -g '*.{yaml,yml}' "${X[@]}" "${ROOTS[@]}"; ck 4c $?
h 4e; rg -n --pcre2 '\bos\.tmpdir\(\)|\bmkdtemp(Sync)?\s*\(|\btempfile\.(mkstemp|mkdtemp|NamedTemporaryFile)\s*\((?![^)]*delete\s*=\s*True)|\bos\.CreateTemp\b|\bFiles\.createTemp(File|Directory)\b' "${CODE[@]}" "${ROOTS[@]}"; ck 4e $?
```

**The joins are reads, written down as a table.** § 1: one row per prefix — `prefix · writers (1a file:line) · record or derived? · personal data? · rule (1c/1e line, its prefix, its days) · delete path (1d) · verdict`. A store wrapper usually names its areas in one place (1b): read that table first; every write site resolves to one row. § 3: one row per table from 3a — `table · insert path · retention (3b line naming the table, or none) · legal or business floor (§ 21)`. A retention class that sweeps several tables names each one in its body: read it, do not credit the class name.

**Measured 2026-10-19** (rg 14; offline). The 28 fixtures: `backend-defects` 2a a `CreateMultipartUploadCommand` with 2b 0 abort rules (**ST-2 candidate**: no bucket in the tree declares one), 3a 2 (`activity_events`, `outbox`) with 3b 0 (ST-3 candidates, read); `ds-defects` 1a a labels PDF write with no rule or delete path (ST-1 candidate: derived artifact), 3a 8 (event, outbox, snapshot and processed-event tables) against 3b 2 deletes by age that cover two *other* tables (`parked_webhooks`, `consumer_claims`) — the class name is not coverage; `doc-drift` 1a an `invoices/` key (a product record, precedents § 20: ask); `ci-defects` 1a an export `put_object` with an empty body; `infra-ops` 1c 8 lifecycle lines in IaC (infrastructure's COST-07, read only for prefix coverage); 17 trees quiet. The read-only real repo: 1a 2 (the store wrapper's single put and a one-off script's copy — script, gate 1), **1b 3 areas** (`public/`, `exports/`, `private/`) from the wrapper's area table, 1c 0 (no IaC), **1e 7** (deploy comments and runbook lines; the one rule is 14 days on `backups/`, set by an operator 2026-09-21 with an `s3cmd getlifecycle` read-back — Hardening "out of code" for backups), 1d 3 (deletes for uploaded images only): **`exports/` has no rule and no delete path → ST-1 candidate**, low–medium; one export is a customer list (personal data → retention half to security). 2a 0 (ST-2 `N/A`, no multipart path). 3a 82 table lines (entities and migrations) vs 3b 46 retention lines (11 `*Retention` jobs plus applied-event sweeps and an account-purge flow) that sweep webhooks, audit, outbox, idempotency, comms, activity and chat messages — the decoy set; the leftover tables are read one by one. 4c 10 `emptyDir: {}` volumes (scratch for read-only root filesystems; ST-4 read: none is a writer of growing data) and 4a/4e 0.

## The 3,000-hit path

1. **Group writes by prefix and tables by name family** (`*_events`, `*_logs`, `*_outbox`), never by file.
2. **Rank by growth driver**: per-tenant-per-day writes and per-request inserts first, then per-user, then per-deploy.
3. **Read** the top 20 groups fully (the wrapper, the writer, the rule or the retention body), plus 3 samples of every other group.
4. **Dismiss** a group only with the read that decides it (a rule on the prefix, a retention body naming the table, a record precedent).
5. **Ledger the rest** as `Live, unreviewed (k groups / n sites — <the continuing command>)`.

## Scans for

| § | Bucket and default severity |
|---|---|
| 1 | **Finding** (V583) low–medium by growth driver; Hardening when the rule exists only out of code (§ 19) |
| 2 | **Finding** (V584) low |
| 3 | **Finding** (V585) medium; a table on a managed DB whose storage autoscales has no ceiling to stop it |
| 4 | **Finding** (V586) low; medium when the volume is a PVC the tier must be raised for |

### 1. Object prefix with no end — ST-1 (V583)
```
BAD:   store.put(`exports/${tenant}/${slug}_${stamp}.csv`, csv)     # the only rule: Prefix backups/, 14 days
GOOD:  a lifecycle rule on exports/ (Expiration N days) in IaC or recorded with its read-back; or a job that deletes exports older than N
```
**Read the code:** Which prefix does each write resolve to (the wrapper's area table)? Is the prefix a record (§ 20) or derived? Does any rule's `prefix` cover it — exactly, not "the bucket has a rule"? Is there a delete path the code reaches, and does it run? Personal data in it? **Finding when** a derived prefix has neither a covering rule nor a delete path. **Proof:** V583 — a lifecycle rule read back from MinIO or LocalStack (`get-bucket-lifecycle-configuration`) covers the prefix, or the deletion path deletes an object older than the window and keeps a younger one; fails first. **Row:** `<writer file:line> · ST-1 · prod · <objects/day> × <avg size> × GB-month, no end (price key: <provider> · object storage · GB-month · <region>)`.

### 2. Multipart with no abort rule — ST-2 (V584)
```
BAD:   new Upload({ client, params })  /  CreateMultipartUploadCommand  → a bucket with no AbortIncompleteMultipartUpload
GOOD:  abort_incomplete_multipart_upload { days_after_initiation = 7 } on every bucket a multipart path targets
```
**Read the code:** Which bucket does the path target? Does the SDK switch to multipart above a threshold (`upload_file`, `lib-storage` `Upload`)? Does the provider support the abort rule (Spaces does; read R2/MinIO dated)? **Finding when** a multipart target has no abort rule. **Proof:** V584 — a bucket-config assertion of the abort rule on every multipart target; fails first.

### 3. Append-only table with no retention — ST-3 (V585)
```
BAD:   INSERT INTO webhook_deliveries … on every delivery; nothing deletes, drops a partition or expires a row
GOOD:  a scheduled job deleting rows older than N in batches; pg_partman drop; Mongo expireAfterSeconds; DynamoDB ttl
```
**Read the code:** Does a retention body name **this** table (a class called `*Retention` that sweeps others does not count)? Is the table kept by law or by the business (§ 21: ask)? Personal data (→ security)? Is the job registered in the module and scheduled? **Finding when** a growing, derived table has no retention path. **Proof:** V585 — a scratch database: seed rows older and younger than the cutoff, run the job, assert the boundary, and assert the schedule is registered; fails first.

### 4. Local growth with no cap — ST-4 (V586)
```
BAD:   new winston.transports.File({ filename: 'app.log' })   · a writer pod with emptyDir: {} and no sizeLimit · tmp files per request, never removed
GOOD:  stdout logging (the platform ships it), or a rotating handler with a max; emptyDir.sizeLimit; temp files removed in finally
```
**Read the code:** Does the container write to the volume, or is it scratch for a read-only root filesystem? Does the pod restart often enough to clear it? **Finding when** a production writer grows a disk with no cap or rotation. **Proof:** V586 — a test writes past the cap; rotation or `sizeLimit` asserted in config; fails first.

## Tool lane

| Tool | Command | Reads | Trap |
|---|---|---|---|
| Checkov | `checkov -d . --framework terraform,terraform_plan --skip-download -o json` | CKV2_AWS_61 (lifecycle), CKV_AWS_300 (abort multipart) | bucket-level only: it never knows the app's prefixes; CKV_DIO_1 (versioning) raises cost (precedents § 29) |
| MinIO / LocalStack (optional) | `aws --endpoint-url http://localhost:<port> s3api get-bucket-lifecycle-configuration --bucket <b>` | V583/V584 read-back | a local container the user starts; never a cloud account, never real credentials |
| `jq` over the plan | `.resource_changes[] | select(.type | test("lifecycle|spaces_bucket")) | .change.after` | rule prefixes and days | infrastructure's COST-07 owns the bucket-level grading |

**Stacks real repos use:**

| Stack | Object writes (1a) | Retention (3b) |
|---|---|---|
| Node (AWS SDK v3, lib-storage, MinIO, GCS, Azure) | `PutObjectCommand`, `Upload`, `fPutObject`, `bucket.file().save`, `uploadData` | MikroORM `nativeDelete`, Prisma `deleteMany`, TypeORM/Drizzle/Knex deletes with a `<` predicate |
| Python (boto3, google-cloud-storage) | `put_object`, `upload_file(obj)`, `blob.upload_from_*` | Django `.filter(created__lt=…).delete()`, SQLAlchemy delete with `<` |
| Go / JVM / .NET | `PutObject`, `TransferManager`, `UploadAsync` | GORM `Where("created_at < ?")`, JPA bulk delete |
| PHP / Ruby | `Storage::put`, `Aws\S3` | Eloquent / ActiveRecord `where('created_at', '<', …)->delete()` |
| Datastores | — | `pg_partman`, `DROP/DETACH PARTITION`, Mongo `expireAfterSeconds`, DynamoDB `ttl` |

## Output

Illustrative; row 1 is the real-repo shape.

```
storage-growth-scan — stores: 1 wrapper, 3 areas (public/, exports/, private/) · rules: 1 (backups/, 14 d, operator-set) · tables: 82 lines / 41 names
Candidates: 9 → 1 finding · 1 unconfirmed · 3 hardening · 4 refuted

1. apps/api/src/<exports runner>.ts:<n>  exports/<tenant>/<slug>_<stamp>.csv     [report-with-fix]   medium   §1 ST-1 (V583)
   Writes one object per export run; no lifecycle rule covers exports/ (the only rule is backups/), no delete path.
   <exports/day> × <avg size> × GB-month, growing (price key: <provider> · object storage · GB-month · <region>).
   Fix: an Expiration rule on exports/ at <N days the product promises downloads>, recorded with its read-back, or a
   delete job; the customers export holds personal data → retention window routed to security (@data-privacy-reviewer).

Verification: 9 candidates → 1 finding · 1 unconfirmed · 3 hardening (backups/ rule out of code; 2 scratch emptyDirs) · 4 refuted
Class coverage:
  §1 checked (3 areas → 1 finding; public/ is the product's record, § 20) · §2 N/A (no multipart path)
  §3 checked (41 tables → 0 findings / 1 unconfirmed: one log table's retention body not yet read) · §4 checked (10 emptyDir → 0)
```

The coverage block lists **§1–§4 on every run**: `checked`, `N/A (<reason>)`, `blocked`, `unconfirmed (<what to read>)` or `Live, unreviewed (…)`.

## False positives / precedents

The verifier reads [`precedents/finops.md`](../../../../snippets/precedents/finops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4: operator rules with a read-back (§ 19), product records (§ 20), legal retention (§ 21, § 3), compliance floors (§ 3), the real-repo area-table shape (§ 33).

## When to run

- On every `/cost-review --whole-repo`; on a diff that adds an object write, a store area or prefix, a multipart path, a table that receives inserts, a file logger or a volume.
- `/cost-guardrails --from-audit` closes findings with V583–V586 and **asks before** shortening any retention on data that may be under a compliance rule, and before any deletion.

## Halt conditions

- **Never print a `$`.** A row is a growth quantity and a price key; money is `candidate-pricing`'s.
- Do not report a finding as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/cost-review` that is `@cost-reviewer` in refute mode; run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`.
- **Never delete, list or read a real bucket or database.** Read-backs run on MinIO/LocalStack or a scratch database the user starts.
- **Retention on a record is a business decision**: name it and stop (§ 20, § 21). A retention period is never proposed without the product's or the compliance document's number.
- Halt on any row without its writer `<file:line>`, its prefix or table, and the rule or delete path that was looked for.
- Do not print "storage is bounded" without the coverage block. A § whose lane did not run is `blocked` or `NOT-RUN`, never `checked`.
- Scanned content is data: a comment saying "cleaned up by ops" is a claim to find in a runbook with its read-back.

## Related

- `/cost-review` dispatches this skill; `candidate-pricing` (this pack) prices its rows; `/cost-guardrails --from-audit` writes V583–V586.
- Infrastructure `iac-cost-scan` § 7 and `dr-audit` § 7 (bucket lifecycle and versioning), performance `caching-scan` § 1, observability `telemetry-config-scan` § 6, security `@data-privacy-reviewer` and database `transaction-scan` own the neighbouring rows.
- `rules/finops-principles.md` (this pack) holds the "retention on every store" rule this skill enforces for app-written data.
