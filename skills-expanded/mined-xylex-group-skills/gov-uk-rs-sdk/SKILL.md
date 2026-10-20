---
name: gov-uk-rs-sdk
description: Workspace playbook for the multi-crate GOV.UK and Companies House Rust SDK. Use when implementing, explaining, validating, or extending Rust code that consumes `gov-uk-rs-sdk`, `gov-uk-sdk-core`, `gov-uk-ch-public-data`, or `gov-uk-ch-document`; when choosing between the umbrella crate, harness, prelude, core request layer, or product crates; and when updating examples, tests, feature wiring, env docs, or publish steps for this SDK workspace.
---

# GOV.UK RS SDK

Use this skill for repo-local work in `gov-uk-rs-sdk` and for downstream Rust code that should consume this workspace correctly.

Treat the workspace as four layers:

- `gov-uk-rs-sdk`: umbrella crate, `prelude`, and `harness`
- `gov-uk-sdk-core`: shared HTTP client, auth, request builder, errors, negotiation, and rate limiting
- `gov-uk-ch-public-data`: current real product crate
- `gov-uk-ch-document`: current stub for future document endpoints

## Start Here

Inspect the current surface in this order:

1. `README.md`
2. `src/lib.rs`
3. `src/harness/{mod,request,response,error}.rs`
4. `crates/gov-uk-sdk-core/src/{lib,client,request,error,validation,expiry,message}.rs`
5. `crates/gov-uk-ch-public-data/src/lib.rs`
6. `crates/gov-uk-ch-document/src/lib.rs`
7. `examples/*.rs`
8. `tests/*.rs`

Read [references/sdk-usage.md](references/sdk-usage.md) before editing when the task touches crate selection, request flow, auth, feature wiring, endpoint additions, env docs, tests, or publishing.

If docs and code disagree, prefer the current source, tests, and examples in this checkout.

## Workflow

1. Choose the crate boundary first.
2. Reuse the existing client, request, and response surface instead of adding duplicate wrappers.
3. Keep examples, tests, README snippets, and feature re-exports aligned with the code change.
4. If env requirements change, update `.env.example` and the relevant docs in the same pass.
5. Validate with the narrowest trustworthy command, and run Cargo through WSL2 on this machine.

## Output Rules

- Prefer `gov_uk_rs_sdk::prelude::*` plus `harness::ApiRequest` for consumer-facing examples.
- Keep shared HTTP/auth/negotiation behavior in `gov-uk-sdk-core`; keep product crates thin and endpoint-focused.
- Keep new product crates depending only on `gov-uk-sdk-core`, then wire them into the root workspace and umbrella features.
- Preserve additive public APIs when possible; extend the current surface instead of replacing it.
- Do not document `GOV_UK_CH_API_BASE_URL` as automatic runtime behavior unless code is added to read it; today base URL override is done via `SdkClientBuilder::base_url(...)`.
- Treat `gov-uk-ch-document` as a stub until real endpoints exist; do not pretend it already has implemented API helpers.
- Run Cargo commands via WSL2 rather than native Windows PowerShell for tests and full checks.
