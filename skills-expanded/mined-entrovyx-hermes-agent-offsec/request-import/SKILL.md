---
name: request-import
description: "Import HAR exports or raw Burp/Caido HTTP requests into an offensive request map. Use as /request-import <path> to extract endpoints, methods, parameters, cookies, auth hints, and deep-hunt candidates."
sources: field_recon
report_count: 50
---

# Request Import Mode

Use this mode when the operator invokes `/request-import <file.har|raw-request.txt>`.

This mode turns captured traffic into attack planning material. It is not a passive parser; it should produce endpoint intelligence, object families, parameters, role/state clues, and suggested `/deep-hunt` routes.

## Required Behavior

1. Resolve the user-provided file path.
2. Run the parser:

```bash
python skills/offsec/meta/request-import/scripts/har_burp_mapper.py "<path>"
```

3. If a target dossier exists, write or merge the output into:

```text
.offsec/campaigns/<target-slug>/request-map.md
```

4. Use the parsed map to recommend concrete manual attack modes.

## What To Extract

For each request:
- method
- URL/path
- host
- query parameters
- body parameters
- content type
- auth artifacts
- cookies
- object ID candidates
- state-changing behavior
- response status if HAR contains it
- source file/request index

## Offensive Classification

Tag routes as:
- `auth/recovery`
- `invite/onboarding`
- `billing/credits/refunds`
- `graphql`
- `import/upload/parser`
- `export/attachment/preview`
- `role/ownership`
- `support/admin`
- `ai/rag`
- `webhook/integration`
- `generic-api`

## Output Contract

Return:
- request count
- top endpoint clusters
- high-risk parameters
- object ID candidates
- auth/cookie artifacts observed
- recommended `/deep-hunt` modes
- recommended `/attack-chain` candidates

