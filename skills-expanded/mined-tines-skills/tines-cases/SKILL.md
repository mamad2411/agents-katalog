---
name: tines-cases
description: Working with Tines Cases from a 3B workflow or chat — creating, updating, listing, and managing cases with their comments, subscribers, and activities, plus the Records store cases draw on. Use this whenever you’re asked to open, update, close, search, or manage a Tines case, to work with Tines records, or to call the Tines API for anything case- or record-related.
license: Apache-2.0
compatibility: Tines 3B
---

# Working with Tines Cases

Tines Cases is Tines’ investigation and case-management surface, and Records is the structured-data store alongside it. You reach both through the same **Tines Stories** connector (identifier `tines`) that covers the rest of the Tines API.

## Find the connector first

Before writing any call, use the `searchConnectors` tool with the identifier `tines` to find an existing “Tines Stories” connector. Reuse it if one exists. Only if none is found, prompt the user to create one with the `connectStepToApp` tool.

## Read the endpoint doc before you write the call

Payloads have non-obvious fields, so fetch the specific endpoint doc and follow it rather than guessing. The API index the connector points you at links a per-endpoint markdown doc for every case operation and sub-resource (comments, records, subscribers, activities, and so on), and for every record operation. For a conceptual overview of how Cases works, see `https://www.tines.com/docs/cases/overview/`.

Flag ambiguity rather than guessing silently.

## Records

Records are structured, queryable tables: a record type defines typed fields, and each record is a row of field values. They stand on their own, and a record can additionally be linked to one or more cases, e.g., when it’s evidence in an investigation. Records live under `records`, their schemas under `record_types`, and a case’s linked records under `cases/<case_id>/records`.

For a conceptual overview, see `https://www.tines.com/docs/records/`. Before writing record calls, read `https://www.tines.com/llm/stories/docs/api/records/best-practices.md` — it covers aggregate queries, pagination, filters, rate limits, retention, and linking records to cases.

## Base path

Cases and records live under `{TINES_URL}/api/…`. Prefer the newest API version an endpoint offers, and don’t fall back to an older version just because the connector’s connection test happens to hit one. Versions vary by endpoint — some case-related operations sit under the newer version while others are still on the older one — so check the endpoint doc for the current version of each call rather than assuming a single base path.
