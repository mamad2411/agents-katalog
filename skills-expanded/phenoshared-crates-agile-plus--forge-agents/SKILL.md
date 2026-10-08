# AI-DD Crutch: AGENTS.md Drift Guard

## Rule: `agents_md_drift`

### Severity
FAIL (blocks commit)

### Trigger
A staged file is listed in AGENTS.md as a **do-not-touch zone** (marked with
`DO_NOT_TOUCH` or `AI_EXEMPT`) but the diff does not include a corresponding
WORKLOG.md row referencing that file.

### Do-not-touch zones

| File / Pattern | Rationale |
|----------------|-----------|
| `Cargo.lock` | Generated; managed by `cargo update` only |
| `crates/*/Cargo.toml` `version` field | Managed by `release-plz` |
| `.github/workflows/*.yml` SHA pins | Managed by `dependabot` or manual security audit |
| `SECURITY.md` | Org-level policy; changes require security review |
| `deny.toml` | Supply-chain policy; changes require audit |

### Required WORKLOG.md format

When touching a do-not-touch zone, the commit must include a WORKLOG.md entry
with:

```markdown
| task_id | file | rationale | reviewer |
|---------|------|-----------|----------|
| V3-042  | `Cargo.lock` | bump tokio for RUSTSEC-2026-XXXX | @security |
```

### Verification

```bash
pheno-vibecoding-guard run --check agents_md_drift
```
