# AGENTS

Read first:
- `README.md`
- `docs/TERMINOLOGY.md`
- `docs/SPECS.md`
- `docs/WORKFLOWS.md`
- `docs/TBPS.md`
- `docs/ENGINEERING.md`
- `docs/PUBLIC-DOCS.md`
- `docs/GUARDRAILS.md`
- `docs/agent-context/project-context.md`

Guide-system metadata:
- `.guide-profile.json` records planning traceability only; ordinary implementation agents must use the localized documents above rather than external guide repositories.

When changing workflows:
- update `docs/workflows/` first
- keep `.github/workflows/` synchronized

When introducing terminology:
- update `docs/TERMINOLOGY.md`

When introducing recurring execution patterns:
- add or update a document in `docs/tbps/`

When changing public package/API behavior:
- update `public-docs/`
- update `docs/specs/PublicApi.md`
- keep `public-docs/api-baselines/` synchronized via `./eng/public-api.sh`

When running validation:
- use `./eng/check.sh` as canonical completion gate
- use `./eng/release-check.sh <version>` for release readiness
- do not run benchmarks or long-running tests by default
