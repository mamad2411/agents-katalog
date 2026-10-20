# Copilot Instructions

Primary repository docs:
- `docs/TERMINOLOGY.md`
- `docs/SPECS.md`
- `docs/ENGINEERING.md`
- `docs/PUBLIC-DOCS.md`
- `docs/GUARDRAILS.md`
- `docs/workflows/`
- `docs/tbps/`

Guide-system metadata lives in `.guide-profile.json` for planning and documentation-sync traceability only. Ordinary implementation work must use localized Fletched documentation and must not require copied guide documents or external guide repositories.

Use `./eng/check.sh` as the standard gate and `./eng/release-check.sh <version>` for release readiness.
