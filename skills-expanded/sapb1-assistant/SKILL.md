---
name: sapb1-assistant
description: "SAP Business One (SAP B1 / B1) ERP assistant for consultants and integrators. Use for anything SAP Business One, including \"B1\", \"SBO\", table names (OINV, ORDR, OCRD, OITM), object type numbers, the DI API (SAPbobsCOM), UDOs, or the Service Layer/OData. Capabilities - (1) Object types: number, table, key and topic lookup. (2) SQL/schema: verified queries against bundled B1 10.0 and 9.3 dictionaries. (3) DI API: generate and review C# for connection, business objects/services, transactions, errors and user-defined objects from the bundled DI API 10.0 reference. (4) Service Layer: OData v4 endpoints, login/session, CRUD/actions, query options, ETags, batch, SQLQueries, FP2602 webhooks, and exact entity set, property, enum and action lookup from a bundled FP 2602 $metadata snapshot. (5) DI API vs Service Layer: which to choose, SAP's documented limitations of each, and porting code and names between them. Trigger on any SAP Business One question, casually phrased or not."
compatibility: "Runtime needs file read + grep over the bundled references. Refreshing references needs web access to the source sites, curl, and Python 3.10+ (scripts/ for the schema and the DI API reference, a documented procedure for the object list); none of that is needed to answer questions."
metadata:
  author: Francois Taljaard
  version: "2026.10.4"
  domain: SAP Business One ERP
---

# SAP Business One Assistant

> **Version disclaimer:** the bundled schema dictionaries cover **SAP Business One 10.0** (SAP's own reference, the default) and **9.3** only. Any other release, including later feature packs, can have tables and columns they lack, and a client's own user-defined tables and fields are never in them. State which version you used whenever you give SQL, and confirm any column that matters on the client's own database.

Reference-backed assistant for SAP Business One consultants and integrators. The rule that makes it
trustworthy: **every material claim comes from a bundled reference and is cited** — never from memory alone.
Object type numbers, table names and key columns are exactly the things a model guesses plausibly and wrongly.

## 1. Route the request

| Request looks like | Go to |
|---|---|
| "what's the object type for X", "what is object type N", "which table / primary key is behind N", "list the objects for sales / inventory / banking", UDO or DI API work that needs an object number | § 3 Object types |
| a view, query, report extract, "what table/field holds X", join, valid-value / status questions against B1 data | § 4 SQL / schema |
| generate, **review** or fix **C# against the DI API** (`SAPbobsCOM`): connect, create/update an invoice, order, business partner or item, read errors, transactions, UDFs/UDTs/UDOs, "what does this DI API property/method do", an enum value, "audit / clean up my integration" | § 5 DI API |
| Service Layer / REST / OData: login/session cookies, `/b1s/v2`, `$metadata`, entity reads/writes, actions, query options, paging, ETags, batch, UDF/UDT/UDO entities, attachments, `SQLQueries`, SQL views, FP2602 webhooks, Service Layer configuration or troubleshooting, "review my Service Layer code"; an exact Service Layer name - "which entity set / property / enum value / action is X", "what type is `Document.DocType`", "which action closes an order" | § 6 Service Layer (step 3 for exact names) |
| "DI API or Service Layer?", "can Service Layer do X like the DI API", "port this DI API code to Service Layer", "why is it `DocumentLines` here and `Document_Lines` there", architecture or platform choice for a new B1 integration | § 6 step 1 (`di-api-vs-service-layer.md`) |
| both — "build a view over sales orders and tell me the ObjType" | § 4, using § 3 for object numbers |

Anything else (UI API code, version and upgrade questions, how-to procedures) is a planned
capability, see `MAINTENANCE.md`. Say so, answer what you can with the caveat that it is not
reference-backed, and note that the skill could be extended.

## 2. Ground rules

- **Never write SQL or code that modifies B1 tables directly.** Direct writes bypass B1's business logic and
  corrupt integrity; the supported write paths are the application, the DI API and the Service Layer. Don't
  print the modifying statement even as an illustration of what not to run; describe it in words. **In the DI
  API (§ 5) and Service Layer (§ 6), writes through the supported API ARE the correct path**, but `Recordset.DoQuery` is
  for reading only: never use it to change B1 data, and never invent an object number, enum value or member.
- **Verify, then cite.** Quote the object number, table and key from `references/objects/object-types.md`
  and say that is where it came from. If a number or table isn't in the list, say it isn't in the list —
  don't fill the gap from memory.
- **Know the source's limits.** Rows marked `sap-di` in the object list are confirmed by SAP's own DI API 10.0
  reference (`BoObjectTypes`); the other rows come only from two community websites that state no B1 version.
  For a number without `sap-di` that will ship (UDO registration, Service Layer calls), tell the user to confirm
  it against SAP's reference for the client's version.
- **Match the client's version** when it changes the answer, and ask if you can't tell. The bundled schemas are
  **B1 10.0** (default) and **9.3**; use the folder matching the client, otherwise 10.0, and say which. 10.0 has
  246 more tables and about 5,300 more columns than 9.3, so a 9.3 client can lack columns 10.0 shows and a later
  release can have ones it lacks. A client's own user-defined tables and fields are never in either. Give the user
  a way to confirm a column on their own database before they rely on it.
- **Ask which database** (SQL Server or SAP HANA) before writing SQL: the dictionary records column types, not
  dialect, and the two dialects differ.
- If the user reports a fact the references lack or contradict, say the reference should be updated
  (`MAINTENANCE.md`) rather than silently preferring either.

## 3. Object types

1. **Pin the question**: number → table, table → number, or a topic search ("everything about bins"). Note
   whether the user wants one object or a list.
2. **Read** `references/objects/INDEX.md` for the sources, their reliability and the known issues, then grep
   `references/objects/object-types.md`. One line per object: `| ObjType | Table | Description | Primary Key | DI API | Src | Notes |`.
   - By number: `^| 17 |`
   - By table: `\| ORDR \|`
   - By topic: `(?i)bin|batch|serial` against the Description column
3. **Read the Notes column** on every row you use. It flags blank source data (209, 225-227), table-name
   conflicts between the sources and where SAP's DI API class names a different table. Don't present a flagged
   row as settled. The **DI API** column is the `BoObjectTypes` member to use in C# (§ 5); a blank there means
   SAP's enumeration has no member for that number.
4. **Watch for shared tables**: `ODRF` carries two object numbers (112 and 1179), so a table name alone is not
   a unique key.
5. **Deliver** the number, table, description and key as a short table, cite `object-types.md`, and add the
   source caveat from § 2 when the answer will end up in code. If the user's table or number is missing from
   the list, say so and offer to check SAP's documentation.

## 4. SQL / schema

Bundled dictionaries: `references/dictionary/10.0/` (**default**, 2,784 tables, from SAP's own `REFDB.chm`) and
`references/dictionary/9.3/` (2,546 tables, from erpref.com, for clients still on 9.3). Below, `<ver>` is the
folder you chose. `references/dictionary/INDEX.md` has the sources, counts, the 9.3 to 10.0 changes and known issues.
**9.3 lists composite-key columns in reversed order; take key order from 10.0.**

1. **Pin the requirement**: entities, columns, filters (open only? date range? which currency?) and the
   **grain** (one row per document / per line / per item). B1 documents split into a header table and row
   tables, so grain decides the join. If grain, open-vs-closed or the database (SQL Server / HANA) is
   ambiguous, ask — status fields are multi-valued and a wrong guess silently drops or duplicates rows.
2. **Find the tables** by grepping `references/dictionary/<ver>/table-index.md` (one line per table: name,
   description, module, column and index counts, `ObjType`, and the `File`, `Line` and `Lines` where its entry
   is). Header and row tables read as a family (e.g. an order and its lines); check both.
3. **Verify every column** by reading the table's entry: open `references/dictionary/<ver>/dict/<File>` from
   line `Line` for `Lines` lines (a line-range read; or grep `^# TABLE - ` in that file). Entries are bundled by
   module, so never read a whole file. Never emit a column you haven't seen there. Lines read
   `name type(len) description default=… [valid values] ->parent table`. The `Indexes:` block lists physical
   indexes; the **first one is the primary key** (usually named `PRIMARY`) — join and filter on it.
4. **Join through the `->PARENT` links and index columns**, not by name similarity. A `->` link names the table
   a column refers to; it doesn't give the parent's key column, so confirm that against the parent file's
   first index. The links are the source's own mapping, not enforced foreign keys: don't join on `->ADP1`
   (see § 7 Gotchas).
5. **Decode valid values from the bracketed `[…]` lists**, never from memory: status flags, document types,
   Y/N fields. Decode with CASE in the output and cite the values used in filters. Read the list on the exact
   table, since the same column name can carry different values on different tables. A column with no list,
   or a value with a blank label (`[0=, 1=]`), has no documented meaning — say so rather than inventing one.
6. **Object numbers**: where a column holds an object type number, resolve it through
   `references/objects/object-types.md` (§ 3) and cite that file.
7. **Deliver**: one ```sql block with the complete `CREATE VIEW` (or query) in the right dialect, then a short
   note on the tables used and why, the joins, the status filters in business terms, and explicit assumptions
   (grain, currency, which date field). Add a sanity-check `SELECT TOP 20 …` (or `LIMIT 20` on HANA) to run
   first, and say which schema version you used, so columns should be confirmed on the client's database.

Grep recipes (paths relative to the skill root): `(?i)bin` in `references/dictionary/<ver>/table-index.md` →
tables by topic. For "which tables carry a column" or "what points at the business partner table", grep the
bundles for the table headings and the column together, e.g. `^(# |  CardCode )` or `^(# |.*->OCRD$)` across
`references/dictionary/<ver>/dict/`: a matching field line belongs to the nearest `# TABLE - ` heading above it.

## 5. DI API development (C#)

Generate or review C# against the **DI API** (`SAPbobsCOM`): `Company` -> business objects and services. Scope is
this object library only, not the UI API, the Service Layer or DI Server. The reference is **DI API 10.0**
(10.00.190), which matches the default **10.0** schema dictionary; for a 9.3 client use the 9.3 folder and say so.

1. **Pin the request**: which object or document (invoice, order, business partner, item, UDO…), whether it is a
   **read** or a **create/update**, the B1 version and database (SQL Server / HANA), and what already exists
   (solution, connection handling). Ask when read-vs-write or the version changes the answer.
2. **Read** `references/diapi/INDEX.md`, then `references/diapi/di-api-guide.md`, and
   `references/diapi/common-mistakes.md` before writing code, so you produce the documented pattern and not the
   usual wrong one.
3. **Look up every class, member and enum you use** — never from memory. For "does it exist and what type is it",
   grep `references/diapi/api/members.md` (`Class.Member : VBType [R/W]`, one line each) and
   `references/diapi/enums/members.md` (`Enum.Member = Value`). For remarks, parameters and SAP's sample, find the
   class in `references/diapi/api/INDEX.md` (it gives the `File`, `Line` and `Lines` of each class) and read that
   range of `references/diapi/api/<File>`; enums the same way through `references/diapi/enums/INDEX.md`
   (`BoObjectTypes` holds the object numbers). Never read a whole bundle. An unfamiliar member gets looked up,
   not guessed.
4. **Verify table and column names** (for `Recordset` reads, field names, UDFs next to standard fields) in
   `references/dictionary/<ver>/` (§ 4) and say which version. A class's source table is in `api/INDEX.md`.
5. **Generate the documented pattern**: connect with the mandatory properties from configuration; check every
   return code and call `GetLastError` straight away; read lines in the order SAP's sample shows; wrap
   multi-object changes in `StartTransaction`/`EndTransaction`; `Marshal.ReleaseComObject` the `UserFieldsMD` /
   `UserTablesMD` / `UserObjectsMD` objects; disconnect in `finally`/`Dispose`.
6. **Examples are SAP's, labelled by language.** Prefer a `C# example`; a `VB example` is a pattern to translate
   (and a few SAP-labelled "C#" samples are really VB). Translate VB types with the table in the guide § 9.
7. **Deliver**: one ```csharp block, then a short note: which members and enums were verified in the reference,
   what is still unverified (for example a 10.0-only member on a 9.3 client, or a later feature pack), and the environment caveats from § 7.
   Offer a test plan or the matching read-only SQL (§ 4) as follow-ups.
8. **Reviewing an existing project** ("review / audit / clean up my DI API code"): run the greps in
   `references/diapi/review-checklist.md` over the whole tree before reading files, verify each flagged member in
   `api/members.md`, and report data-affecting defects first, then connection and COM lifetime, then the rest.
   Behaviours that look wrong but may be intended for the client go in a separate list to decide, not fix. For a
   restructuring, the guide § 12 describes a testable build-then-commit layout (practice, not SAP guidance).

## 6. Service Layer (REST / OData v4)

Generate or review integrations against the SAP Business One **Service Layer**. The bundled references cover
stable integration patterns for B1 10.0 plus explicit feature-pack boundaries, and a generated snapshot of one
**FP 2602** `/b1s/v2/$metadata` (`references/servicelayer/metadata/`) for exact entity set, property, enum and
action names.

1. **Choosing or porting?** For "DI API or Service Layer", "can Service Layer do X", a platform decision for a new
   integration, or porting DI API code, read `references/servicelayer/di-api-vs-service-layer.md` first: it holds
   SAP's own limitation list (no cross-request transactions, no `Recordset`, no XML import/export, restart after
   new UDO/UDF/UDT), the decision table, the side-by-side operation mapping and the naming differences. Ask the
   seven questions in its § 7 when the answer depends on them; label the practice rows as practice.
2. **Pin the client version and database** when they change the answer. For new integrations prefer **OData v4**
   at `/b1s/v2`; SAP deprecates OData v3 from FP 2405. Read `references/servicelayer/INDEX.md`, then
   `references/servicelayer/service-layer-guide.md`. Several query features (aggregation, `$crossjoin`, row-level
   filter, Semantic Layer views) are documented for HANA only, and SQL views for SQL Server only.
3. **Look up every exact name, never invent it.** Read `references/servicelayer/metadata/INDEX.md` once, then
   grep the flat indexes, one entry per line: `metadata/api/members.md` (`Type.Property : ODataType`, e.g.
   `^SAPB1\.BusinessPartner\.CardType `), `metadata/enums/members.md` (`Enum.Member = Value`),
   `metadata/operations/members.md` (`Action|Function Name(params) -> return`), `metadata/entity-sets.md` (entity
   set -> entity type and navigation bindings: `Orders`, `Invoices`, `Quotations` ... are all `SAPB1.Document`)
   and `metadata/operation-imports.md` (global endpoints such as `Login`). For a type's full entry (key, OpenType,
   navigation properties) take `File`/`Line`/`Lines` from `metadata/api/INDEX.md` (operations and enums likewise)
   and read only that range - never a whole bundle. The snapshot is **one FP 2602 company**: on another feature
   pack confirm names against the client's `/b1s/v2/$metadata` or SAP's change log for that pack and say so; a
   type with `Filtered properties: N` had customer UDFs removed, and UDFs, UDTs and UDOs are always client-specific.
   Never derive an entity or property name from a DI API class or collection name: Service Layer renames them
   (`di-api-vs-service-layer.md` § 6).
4. **Authenticate and preserve the session**: `POST /b1s/v2/Login`, then send back `B1SESSION` (mandatory) and
   `ROUTEID` (optional, keeps the load balancer sticky). The login response reports `SessionTimeout` in minutes
   (default 30). Reuse sessions: SAP calls login heavy. End an explicit session with `POST /b1s/v2/Logout`.
5. **Reads**: `$select` to keep payloads narrow; `$filter` with only the four documented functions (`startswith`,
   `endswith`, `contains`, `substringof`) and no arithmetic; follow the next link when a collection pages (page
   size 20 unless `Prefer: odata.maxpagesize` says otherwise). Use `$expand` only where metadata exposes the
   navigation property.
6. **Writes**: use the entity/action API (`POST`, `PATCH`, bound and global actions), never direct SQL against B1
   tables. `PATCH`, not `PUT`, for partial updates; read-only properties in a PATCH are silently ignored. For
   read-modify-write flows, retain the ETag and send `If-Match`; treat HTTP 412 as a concurrency conflict to
   re-read and reconcile, not a blind retry. Anything that must be atomic across objects goes in one `$batch`
   change set; if it needs branching between steps, say so and point to the DI API or a JavaScript extension.
7. **`SQLQueries`**: read `references/servicelayer/sql-queries.md`. Available from B1 10.0 FP 2011; named
   parameters; read-only; table and column allowlist; limited keyword and function set; `select *` rejected in the
   select list; separate authorization subjects.
8. **FP 2602 webhooks**: read `references/servicelayer/fp2602.md`. Do not propose webhooks on an earlier B1
   version, and keep the FP 2608 additions (`BizObjProps`, `FilterExpr`, formulas) off an FP 2602 system.
9. **Deliver**: code/request examples plus a short verification note: B1 version and database, OData version,
   which reference backed the protocol behaviour (with the guide page when it matters), which exact names were
   verified in the FP 2602 metadata snapshot, and which still require live `$metadata` confirmation (another
   feature pack, UDFs, UDOs).

## 7. Gotchas (things a careful engineer still gets wrong)

- **The schemas are B1 10.0 and 9.3 only.** Other releases and every client's user-defined tables and fields are
  absent; a column missing here isn't proof it's missing on the client's database. 9.3 to 10.0 added 246 tables,
  widened types (`MDP2.JrnlMemo` 50 to 254) and extended valid-value lists, so don't mix versions in one query.
- **9.3 key column order is reversed** against SAP's reference (`RDR1`: `LineNum, DocEntry` in 9.3,
  `DocEntry, LineNum` in 10.0). The column sets agree; use 10.0 for order.
- **Valid-value lists are per table.** `CANCELED` is `Y=Yes, N=No` on the sales order (`ORDR`) but also has
  `C=Cancellation` on the A/R invoice (`OINV`). A list can be partial too (`RDR1.BaseType` lists only
  `23=Sales Quotation` beside two blank labels), so treat it as "the values the source documents".
- **"Open" is not one column.** Documents carry `DocStatus` (`O`/`C`) and a separate `CANCELED` flag, and row
  tables carry their own `LineStatus`. Decide which the requirement means and say which you used.
- **`->ADP1` is not a join.** In 10.0, 955 of 1,279 `ObjType`/`ObjectType` columns are linked to `ADP1`
  (Object Settings - History). Resolve object numbers through `references/objects/object-types.md` instead.
  Links to `OACT`, `OOCR`, `OUSR`, `OCRD`, `OITM` and similar are genuine references (account, dimension, user,
  business partner, item). 24 links point at `OINM`/`OPMN`, which have no file.
- **Header and rows are separate tables** with a composite key on the row table (`RDR1`: `DocEntry, LineNum`).
  Joining header to rows on `DocEntry` alone is right; joining rows to rows without `LineNum` multiplies them.
- **Types are the source's, not SQL Server's.** `Num(19,6)`, `Int(11)` vs `Int(6)` (unexplained by the source)
  and `Identity(11)` are shown as given; the physical type on the client's database is the authority.
- **83 tables have a blank description** in 10.0 (84 have one equal to the table name in 9.3, e.g. `OSES`): the
  source gave nothing better.
- **`OSES`, `TAAS` and `TAASF` are the tables whose first index isn't named `PRIMARY`** (`PK_CODE`, `DUMMY`), which
  is why the rule is "first index".
- The object list behind `ObjType` comes from community websites and carries its own caveats (§ 2).

**DI API (§ 5):**
- **`Long` is `int`** in C#, and the reference prints Visual Basic signatures only; use the guide § 9 table and
  confirm anything unusual (`Integer`, `Variant`) in IntelliSense on the install.
- **Check the code, then call `GetLastError` immediately**; the error is lost on the next call. Business objects
  return a code, services throw `COMException`.
- **A failed call inside `StartTransaction` has already rolled back**; code that carries on is outside the
  transaction.
- **`Recordset.DoQuery` runs anything.** Reads only; writes go through business objects.
- **SAP's own samples are not all C#**: some blocks labelled C# are Visual Basic (tagged `vb` in `api/`).
- **Release `UserFieldsMD`/`UserTablesMD`/`UserObjectsMD` with `Marshal.ReleaseComObject`** after creating a UDF,
  table or UDO in .NET; SAP marks it IMPORTANT.
- **The DI API reference and the default schema are both 10.0.** 420 of the 438 source tables its classes name are
  in the 10.0 dictionary (404 in 9.3); the rest look like views or localization tables. Confirm columns on the
  client's database.
- **The interop can know more than the CHM.** `dst_MSSQL2022 = 17` exists in the 10.0 interop though the reference
  stops at 2019; parse `DbServerType` with `Enum.TryParse` and fail at connect time with the valid names.
- **A service `Add` posts the whole document.** Calling it inside the line loop posts one document per line
  (guide § 11, mistakes row 18).
- **`Lines.Add()` after the last line is tolerated**, not a bug: the DI API ignores the trailing empty line. Set
  `DocObjectCode` first on drafts and the base reference before `ItemCode`; those orders do matter (guide § 11).
- **`BaseType` is two kinds**: the object number on `Document_Lines`, `InvBaseDocTypeEnum` (InventoryTransferRequest
  = 5) on `StockTransfer_Lines` (mistakes row 23).

**Service Layer (§ 6):**
- **A valid `$batch` answers 202 on OData v3 but 200 on v4**, and a sub-request can still have failed: read every
  sub-response. A failure inside a change set returns one response for the whole change set (guide § 6).
- **A stale `If-Match` is HTTP 412 with SAP error -2039** ("Another user or another operation modified data"): re-read
  and reconcile, never resend the old payload (guide § 5).
- **`SQLQueries` rejects `select *` in the select list but accepts it inside an `EXISTS` subquery**, and rejects all
  DML with a parse error expecting `SELECT` (sql-queries.md § 3-4). The stored `SqlText` comes back normalized with
  bracketed (SQL Server) or double-quoted (HANA) identifiers; that is cosmetic, not a change of meaning.
- **Webhooks need FP 2602 and the Webhook Messenger Service running**; they are off per company until
  `CompanyService_UpdateAdminInfo` sets `EnableWebhook`. `BizObjProps`, `FilterExpr`, `ExtDataList` and the formula
  language are **FP 2608**. Delivery can duplicate after a retry and is ordered per company only, so receivers
  must be idempotent. SAP's own text disagrees on the retry policy (3 × 2 s versus 5 exponential); say so.
- **There is no transaction across Service Layer requests.** A `$batch` change set is the only atomic unit, the
  batch stops at the first failure, and there is no rollback call. Order-plus-delivery with logic in between is a
  DI API or JavaScript-extension job (di-api-vs-service-layer.md § 2-3).
- **New UDO/UDF/UDT metadata is invisible until Service Layer restarts**, even though the metadata entities
  created it. A deployment that creates and then uses a UDF in one run fails on Service Layer.
- **Service Layer names are not DI API names.** `Document_Lines` is `DocumentLines`, `InventoryGenEntry` is
  `InventoryGenEntries`, `BatchNumber.BatchNumber` is `BatchNumberProperty`. Look it up, never transliterate.
- **One type, many entity sets.** `Orders`, `Invoices`, `DeliveryNotes`, `Quotations`, `Drafts` and 21 more are all
  `SAPB1.Document` (`metadata/entity-sets.md`); the URL's entity set, not a property, decides the document type, and a
  bound action such as `Close` is declared once on the type and called on the set: `POST /b1s/v2/Orders(DocEntry)/Close`.
- **Absence from the metadata snapshot is not proof of absence.** It is one FP 2602 company; `OpenType: true` types
  accept UDFs that are never listed, `Filtered properties: N` marks removed customer UDFs, and a later feature pack
  can add properties (SAP's change log per pack). Say "not in the FP 2602 snapshot", not "does not exist".
- **`$filter` knows four functions and no arithmetic.** `tolower`, `year`, `add` and the like fail. Aggregation,
  `$crossjoin` and the row-level query service are documented for HANA; on SQL Server use `SQLQueries` or an
  exposed SQL view instead.
- **`SQLQueries` is allowlisted.** A table outside `b1s_sqltable.conf` fails with 702 and SAP says not to add
  tables; log tables and `SBO-COMMON` are never queryable. A normal user needs the query granted under
  *Service Layer SQL Query* (403 / -6006 otherwise).

## 8. Layout

```
references/objects/      INDEX.md, object-types.md (the reconciled list)
references/dictionary/   INDEX.md, 10.0/ and 9.3/ each with table-index.md + dict/<Module>.md (tables bundled by module)
references/diapi/        INDEX.md, di-api-guide.md (how-to), common-mistakes.md, review-checklist.md, api/ (INDEX.md + members.md + classes-NN.md bundles), enums/ (INDEX.md + members.md + enums-NN.md bundles)
references/servicelayer/ INDEX.md, service-layer-guide.md, di-api-vs-service-layer.md (choose / port), sql-queries.md, fp2602.md (webhooks), metadata/ (FP 2602 $metadata snapshot: INDEX.md, api/, entity-sets.md, operations/, operation-imports.md, enums/ - flat members.md indexes + bundles)
scripts/                 maintenance only (compile the 10.0 schema and the DI API reference from the SDK's CHMs; fetch + compile the 9.3 schema) — never needed to answer
evals/evals.json         test prompts per capability
MAINTENANCE.md           how to refresh the object list, the schema or the DI API reference, add a source, add a capability
```

Every `references/` folder has an `INDEX.md` with sources and verified dates per file — read it first, open
only what the request needs. The skill is limited to under 200 files, so large references are bundled and their
indexes give the file and line range of every entry.
