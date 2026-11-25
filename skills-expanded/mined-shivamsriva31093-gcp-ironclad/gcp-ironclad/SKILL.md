---
name: gcp-ironclad
description: Use when securing API keys in GCP, hardening Gemini/Vertex API access against fraud, preventing leaked-key abuse, setting up spend guardrails on Google Cloud, or auditing API key restrictions across a GCP organization. Triggers on phrases like "secure GCP keys", "gemini api fraud", "gcp ironclad", "harden gcp project", "lock down google cloud api keys".
---

# GCP API-Key Ironclad — Driver

## Overview

Orchestrates the full audit-and-harden flow for GCP API keys. Runs two READ-ONLY sub-skills in parallel, gates on an "active spike" check, then runs two APPLY sub-skills, then assembles a single markdown + JSON final report. Every applied change is idempotent and reversible.

## When to Use

- After any suspected leaked-key incident, to confirm cleanup and lock down what's left.
- As a recurring hygiene pass (every 30 days, say) on a GCP organization.
- For a new GCP user who wants strong defaults established once and verifiable.

## Inputs / flags

| Flag | Default | Meaning |
|---|---|---|
| `--dry-run` | off | Run every phase, mutate nothing |
| `--confirm-each` | off | Prompt y/n before every applied action |
| `--lookback-days` | 60 | Anomaly-scan window |
| `--threshold-pct` | 200 | Anomaly threshold (% over 7d rolling avg) |
| `--active-spike-multiple` | 10 | Multiple above baseline in last 24h that triggers the halt |

## Phases

### Phase 0 — Discover scope

```bash
SESSION_DIR="/tmp/gcp-ironclad/$(date -u +%Y-%m-%dT%H-%M-%SZ)"
mkdir -p "${SESSION_DIR}"
gcloud auth application-default print-access-token >/dev/null   # ADC sanity check
USER=$(gcloud config get-value account)
gcloud projects list --format=json > "${SESSION_DIR}/raw-projects.json"
gcloud billing accounts list --format=json > "${SESSION_DIR}/raw-billing.json"

jq -n --arg u "$USER" \
      --slurpfile p "${SESSION_DIR}/raw-projects.json" \
      --slurpfile b "${SESSION_DIR}/raw-billing.json" '
{
  schemaVersion: 1,
  generatedAt: (now | strftime("%Y-%m-%dT%H:%M:%SZ")),
  user: $u,
  projects: $p[0],
  billingAccounts: $b[0]
}' > "${SESSION_DIR}/scope.json"

export SESSION_DIR
```

### Phase 1 — Read-only audits (parallel)

Invoke both sub-skills via the `Skill` tool, passing `SESSION_DIR` in env. They may run in parallel because they write distinct files:

> Use `Skill` tool with name `gcp-credentials-audit`.
> Use `Skill` tool with name `gcp-cost-anomaly-scan`.

After both return, both `${SESSION_DIR}/audit.json` and `${SESSION_DIR}/anomalies.json` must exist.

### Phase 2 — Active-spike gate

```bash
ACTIVE=$(jq '[.anomalies[] | select(.activeIn24h == true and .multipleOver >= '"${ACTIVE_SPIKE_MULTIPLE:-10}"')] | length' "${SESSION_DIR}/anomalies.json")
if [ "${ACTIVE}" -gt 0 ]; then
  echo "🚨 Active spike detected (${ACTIVE} project(s) >${ACTIVE_SPIKE_MULTIPLE:-10}× baseline in last 24h). HALTING before Phase 3."
  HALT=1
fi
```

If `HALT=1`, skip Phase 3 entirely and proceed directly to Phase 4 (the report will explain).

### Phase 3 — Apply (sequential)

If not halted:

> Use `Skill` tool with name `gcp-spend-guardrails`.
> Then use `Skill` tool with name `gcp-key-restrictions`.

After both, `${SESSION_DIR}/guardrails-applied.json` and `${SESSION_DIR}/key-restrictions.json` must exist.

### Phase 4 — Consolidate report

Render `${HOME}/.claude/skills/gcp-ironclad/final-report.template.md` against the merged data from all phase JSONs. Write:
- Markdown report: `${HOME}/.claude/reports/gcp-ironclad-$(date -u +%Y-%m-%dT%H-%M-%SZ).md`
- JSON companion: `${HOME}/.claude/reports/gcp-ironclad-$(date -u +%Y-%m-%dT%H-%M-%SZ).json`

Print the executive-summary section inline so the user sees the key numbers without opening the report.

## Idempotency

The driver itself is stateless. All idempotency lives in the APPLY sub-skills (each one gates on "current state ≠ desired state"). Running the driver twice in succession on a clean environment should yield two reports both showing zero changes.

## Errors

- If Phase 0 fails (no ADC, no project access), abort with the exact command to fix.
- If any sub-skill returns a non-empty `errors[]`, surface those in §1 of the report but do not abort.
- Two concurrent driver runs each get their own `SESSION_DIR`; no shared state.

## See also

- Suite README: `~/.claude/skills/gcp-ironclad/README.md`
- Spec (full design): `docs/superpowers/specs/2026-05-24-gcp-api-key-ironclad-skill-design.md`
