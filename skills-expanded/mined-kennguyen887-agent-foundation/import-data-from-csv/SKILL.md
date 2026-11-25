---
name: import-data-from-csv
description: Use when building a bulk CSV/spreadsheet import endpoint — streaming parse, per-row validation with a row-numbered error report, data normalization (Excel quotes, multi-format dates), atomic chunked upsert in a transaction, partial-success response, and fan-out to workers for large files. NestJS/TypeORM reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Import data from CSV

A bulk-import endpoint (members, products, locations, …) that ingests a CSV/spreadsheet and reports
exactly which rows failed. Examples NestJS/TS, neutral `listing` domain. principle → **▸ Example** →
**▸ Other stacks**.

## Core principle
**Validate per row; never all-or-nothing-silently.** Parse → validate each row → collect valid rows
AND a row-numbered error list → write the valid ones atomically → return a **partial-success report**
(N imported, M failed + why). The user must learn *which* row failed and *why*, not just "import failed".

## 1. Parse — streaming + normalized
- **Stream the CSV** (don't load a huge file fully into memory). Validate the **header row first**
  (required columns present) before processing data rows; skip empty rows.
  ```ts
  csv({ delimiter: 'auto', trim: true }).fromString(normalized)
    .on('header', (h) => assertRequiredHeaders(h))
    .subscribe((row, lineNo) => { /* §2 */ }, onError, () => resolve({ valid, errors }));
  ```
- **Normalize spreadsheet quirks** first: collapse Excel triple-quotes (`"""x"""` → `"x"`), trim
  cells, blank → `undefined`, upper-case headers for matching.
- **Parse dates defensively** — try a list of accepted formats, then timezone-normalize; if none
  match, record a row error (don't silently store an invalid/﻿shifted date):
  ```ts
  const d = ['DD/MM/YYYY','YYYY-MM-DD','D-MMM-YY'].map((f) => dayjs(v, f, true)).find((x) => x.isValid());
  return d ? d.tz(TZ) : null;   // null → row error
  ```

## 2. Validate each row → collect errors with row numbers
Map the row to a DTO and `validateSync` it (class-validator); on failure push a **structured row
error** (line number + key + flattened messages) and continue — don't abort the whole file:
```ts
const dto = mapRowToDto(row);
const errs = validateSync(dto, { whitelist: true });
if (errs.length) { rowErrors.push({ row: lineNo, key: dto.code, messages: flatten(errs) }); return; }
valid.push(dto);
```

## 3. Write valid rows atomically, in chunks
- Wrap the write in a transaction; **upsert in chunks of N** (don't build one giant statement) via the
  ORM's bulk upsert; **dedupe rows first** (Map by business key).
  ```ts
  for (const part of chunk(valid, 500)) await em.upsert(Listing, part, ['orgId', 'code']);
  ```
- Log an import-summary row (who, file, counts) for audit.

## 4. Respond with partial success
Return `{ imported: valid.length, failed: rowErrors.length, errors: rowErrors }` — a 200 **report**,
not a 400 that loses the detail. The client shows the user exactly which rows to fix.

## 5. Large files → fan out in controlled batches
Don't process a huge file inline — **chunk rows into batches and dispatch to workers**, grouping
batches to cap concurrency, with audit-friendly names:
```ts
const batches = chunk(rows, BATCH_SIZE);     // e.g. 100 rows/batch
const groups  = chunk(batches, GROUP_SIZE);  // e.g. 5 batches at a time → bounded concurrency
for (const group of groups)
  await dispatchBatch({ event: EVENT.bulkImport, payloadList: group.map((b, i) => ({ fileName: `${name}-part-${i}`, data: b })) });
```
Each batch job must be **idempotent** (see `background-jobs-and-caching` — DB-lock or Redis `SET NX`).
▸ *Other stacks:* same shape everywhere — stream-parse, per-row validate + error list, chunked bulk
upsert in a tx, partial-success report, fan out big files to a queue.

## Verification
- The endpoint returns a **per-row error report** (row number + reason), not a single opaque failure.
- Valid rows are written atomically and **in chunks** (no one-giant-insert, no per-row round trips).
- Header validated up front; dates parsed against an explicit format list; large files fan out to
  idempotent batch jobs.

## Related
- `background-jobs-and-caching` (batch jobs + idempotency) · `write-service-code` (transactions,
  validation) · `code-conventions`.
