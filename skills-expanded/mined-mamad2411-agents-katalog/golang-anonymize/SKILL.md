---
name: golang-anonymize
description: >
  Anonymize and pseudonymize data in Go pipelines: k-anonymity helpers, hashing
  with pepper, tokenization, log redaction, and reversible vs irreversible modes.
  Use for owned datasets under legal/privacy authorization.
---

# Golang Anonymize

## Research grounding

Runbook for **data anonymization/pseudonymization in Go**—ETL jobs, analytics
exports, test fixtures, and log pipelines—aligned with privacy engineering
practice (not legal advice). Skill id: `golang-anonymize`.

## Scope And Authorization

- **In scope:** datasets you are allowed to process; privacy-reviewed purposes.
- **Out of scope:** stripping protections to re-identify people without authority.
- Prefer irreversible transforms for public/share exports; document residual risk.
- Redact real PII from tickets; use synthetic examples.
- Pair with `code-quality-standards` and privacy counsel where required.

## When To Use

- Building Go export jobs that must leave production free of direct identifiers.
- Creating safe-ish fixtures from prod samples.
- Redacting structured logs (`slog` attributes) before ship.
- Focus tokens: **golang, anonymize**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Secrets management | `secrets-management-hygiene` |
| Access control to data | `golang-access-control` |
| Backup encryption | `golang-airgap-backup` / backup skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Technique | Use when | Notes |
| --- | --- | --- |
| Suppression | Rare IDs | Drop column/field |
| Generalization | Ages, ZIP | Buckets (age 30–39) |
| Hashing + pepper | Join keys across systems | HMAC-SHA256; pepper in KMS |
| Tokenization | Need reversibility under control | Vault/format-preserving |
| Noise/DP | Aggregate stats | Privacy budget expertise needed |
| Structured redaction | Logs/traces | Field allowlists |
| Pitfalls | Naive MD5 email; quasi-identifiers re-identify |

## Workflow

### 1. Confirm scope and success criteria

1. Data owner, lawful basis/purpose, recipient, authorization.
2. Success: no direct identifiers in export sample review; documented residual risk.
3. Classify fields: direct ID, quasi-ID, sensitive, public.

### 2. Inventory

1. Schemas (DB, events, logs) and join keys.
2. Downstream consumers and re-identification incentives.
3. Existing pepers/token vaults.

### 3. Baseline

1. Sample N records (authorized); list violating fields.
2. Record current export path and ACLs.

### 4. Implement Go transforms

```go
func HMACPseudonym(pepper []byte, value string) string {
	m := hmac.New(sha256.New, pepper)
	_, _ = m.Write([]byte(value))
	return hex.EncodeToString(m.Sum(nil))
}

func RedactEmail(s string) string {
	// keep domain for ops if policy allows: a***@example.com
	parts := strings.SplitN(s, "@", 2)
	if len(parts) != 2 {
		return "[redacted]"
	}
	return "***@" + parts[1]
}

// slog replace attr example concept: drop authorization headers
```

1. Pepper/keys from KMS; never hardcode; rotate with dual-write if joins must survive.
2. Apply same transform version tag in export metadata (`anon_profile=v3`).
3. Do not log preimages.
4. For test data: prefer full synthetic generation over weak anonymization when possible.

### 5. Verify with evidence

```bash
go test ./internal/anon/... -count=1
go test ./... -race -count=1
govulncheck ./...
```

1. Automated scanners: email/phone/CC regex on export → zero hits (or justified).
2. Join test: same input → same pseudonym within version; different pepper → different.
3. Access review: who can reverse tokens.

### 6. Observe and harden

1. Metrics: records processed, redaction hits, failed rows.
2. Periodic re-ID risk review when new quasi-IDs appear.
3. Alert on export jobs writing outside approved buckets.

### 7. Hand off

1. Document field map (source → transform → risk).
2. Key custody for peppers/tokenization.
3. Legal/privacy sign-off link.

## Field decision table

| Field | Default |
| --- | --- |
| email, phone, national ID | remove or tokenize |
| user_id internal | HMAC with pepper if needed for joins |
| IP | truncate / drop last octet (policy) |
| free text | drop or NER redact |
| amounts | keep if aggregate policy ok |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Hash | HMAC + KMS pepper | unsalted MD5 |
| Export | Profile versioned | Ad-hoc script on laptop |
| Logs | Allowlist fields | Log full request bodies |
| Legal | Purpose-limited | “Anonymized” public dump of quasi-IDs |
| Topic fidelity | Go anonymization | Generic go test only |

## Output Checklist

- [ ] Purpose, owner, authorization recorded
- [ ] Field classification complete
- [ ] Transforms implemented with key custody
- [ ] Automated PII scan on sample export clean
- [ ] Residual re-ID risk documented
- [ ] Metrics and access controls on exports
- [ ] `code-quality-standards` applied

## Rules

- Authorized privacy work only; not legal advice.
- Prefer minimization over clever anonymization.
- Focus on `golang-anonymize`.
- Never commit peppers or raw PII samples to git.
