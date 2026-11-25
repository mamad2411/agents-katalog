---
name: indexeddb
description: >-
  Indexed Database API: This document defines APIs for a database of records holding simple values and hierarchical objects. Covers Indexed Database API 2.0, Indexed Database API 3.0 (track preview). Use when storing structured data in IndexedDB. Triggers: IndexedDB, IDBDatabase.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Indexed Database API

This document defines APIs for a database of records holding simple values and hierarchical objects. Each record consists of a key and some value. Moreover, the database maintains indexes over records it stores. An application developer directly uses an API to locate records either by their key or by using an index. A query language can be layered on this API. An indexed database can be implemented using a persistent B-tree data structure.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when storing structured data in IndexedDB.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Indexed Database API 2.0 (default); Indexed Database API (legacy: read and upgrade, never author); Indexed Database API 3.0 (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **2.1.1. Database Connection.** "If this occurs the user agent must run the steps to close a database connection with the connection and with the forced flag set."
3. **2.2.1. Object Store Handle.** "Multiple handles may be associated with the same object store in different transactions , but there must be only one object store handle associated with a particular object store within a transaction ."
4. **2.3. Values.** "User agents must support any serializable object ."
5. **2.6.1. Index Handle.** "Multiple handles may be associated with the same index in different transactions , but there must be only one index handle associated with a particular index within a transaction ."
6. **2.7.1. Transaction Lifetime.** "The implementation must allow requests to be placed against the transaction whenever the active flag is set."
7. **2.7.1. Transaction Lifetime.** "Until the transaction is started the implementation must not execute these requests; however, the implementation must keep track of the requests and their order."
8. **2.7.1. Transaction Lifetime.** "If an attempt is made to place a request against a transaction when that transaction is not active , the implementation must reject the attempt by throwing a " TransactionInactiveError " DOMException ."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Indexed Database API 2.0](https://www.w3.org/TR/IndexedDB-2/): Recommendation, IndexedDB-2 REC-IndexedDB-2-20180130 (Recommendation, 2018-01-30), checked 2026-10-06.
- [Indexed Database API](https://www.w3.org/TR/IndexedDB/): Recommendation, IndexedDB WD-IndexedDB-3-20250813 (Recommendation, 2015-01-08), checked 2026-10-06.
- [Indexed Database API 3.0](https://www.w3.org/TR/IndexedDB-3/): Working Draft, IndexedDB-3 WD-IndexedDB-3-20250813 (Working Draft, 2025-08-13), checked 2026-10-06.
