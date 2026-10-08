---
name: federal-register-doc-fetch
description: Retrieve bounded official FederalRegister.gov document metadata through the Tiangong CLI, optionally filtered by publication date, term, agency, type, topic, docket, or RIN. Use to identify notices, proposed rules, final rules, or presidential documents; do not use for document bodies, docket comments, legal interpretation, current-force determinations, or compliance advice.
---

# Federal Register Document Metadata

Use the CLI-owned `federal-register.documents` capability. This Skill supplies
intent routing and result-use boundaries only; the CLI owns source discovery,
input/output schemas, HTTP behavior, pagination, limits, validation, and
receipts.

## Before running

1. Read `references/tiangong-data-requirement.json`.
2. Use the caller- or workspace-resolved stable CLI. The requirement declares
   compatible capability and operation contract majors; it does not select a
   package build.
3. Run `data describe` with that same CLI. Continue only when the capability
   ID and required contract majors match, and copy the exact current
   capability/operation versions from that response into the run request.

```bash
tiangong-ai data describe federal-register.documents --json
```

Use the returned Discovery Metadata to confirm current source coverage,
restrictions, `provides`, and `doesNotProvide`. Prefer another source when the
task needs full text, docket attachments, public comments, or legal analysis.

## Prepare the request

Build a `tiangong.data.run-request.v1` envelope and replace the two version
placeholders with the exact versions from the same `data describe` response. Prefer a publication date
and a narrowing filter for evidence questions. An empty `input` is allowed only
for a bounded newest-document listing under explicit runtime limits:

```json
{
  "schemaVersion": "tiangong.data.run-request.v1",
  "capabilityId": "federal-register.documents",
  "capabilityVersion": "<describe.manifest.capabilityVersion>",
  "operationId": "search",
  "operationVersion": "<describe.manifest.operations[0].operationVersion>",
  "limits": {
    "maxPages": 2,
    "maxRecords": 100
  },
  "input": {
    "term": "clean air",
    "publicationDate": {
      "from": "2026-01-01",
      "to": "2026-03-31"
    },
    "agencies": ["environmental-protection-agency"],
    "documentTypes": ["RULE", "PRORULE"],
    "order": "newest",
    "pageSize": 100
  }
}
```

Use the operation input schema returned by the same `data describe` response for current agency,
document type, topic, docket, RIN, ordering, and page-size semantics under
`input`. Optional top-level `limits` may only reduce the operation's published
page, record, response-size, or timeout limits; they cannot raise them. Do not
invent provider slugs or broaden the publication window without the user's
intent.

## Run

```bash
tiangong-ai data run federal-register.documents search \
  --input /absolute/path/to/request.json --json
```

The command emits a `tiangong.data.run-result.v1` envelope. Preserve its
`contract`, `warnings`, `errors`, and `receipt` with `data` when handing the
result to another workflow.

## Result boundaries

- Treat `partial` and truncation stop reasons as incomplete coverage; report
  the page or record limit instead of implying an exhaustive search.
- Treat `blocked` as no usable business result and surface the structured
  errors instead of silently changing filters or limits.
- Returned URLs are metadata links, not proof that document bodies were
  retrieved or reviewed. Preserve citation, comment-close, raw-text, XML, and
  Regulations.gov link fields when the provider supplies them.
- Verify legally consequential claims against an official edition and qualified
  legal guidance. This Skill does not determine current legal force.
- Cross-source comparison and research evidence admission belong to the caller
  or Auto Research, not this atomic Skill.

## Reference

- `references/tiangong-data-requirement.json`: stable capability requirement; it is not a package lock.
