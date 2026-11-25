---
name: golang-bimi-notes
description: >
  Operational notes for BIMI (Brand Indicators for Message Identification) with
  Go mail-related services: DMARC pre-reqs, VMC/CMC, DNS records, and validation.
  Use for owned domains under authorization.
---

# Golang BIMI Notes

## Research grounding

Runbook for **BIMI** setup and operations when mail sending/receiving components
or validators are implemented or automated in **Go**, or when Go services own the
domain brand program. Skill id: `golang-bimi-notes`.

## Scope And Authorization

- **In scope:** domains and mail infrastructure you own.
- **Out of scope:** spoofing other brands’ BIMI; unauthorized DNS changes.
- BIMI requires solid DMARC—do not skip authentication base.
- Pair with email-auth skills if present; `code-quality-standards` for validators.

## When To Use

- Publishing BIMI TXT and hosted SVG logos for owned brands.
- Building Go checks for BIMI/DMARC/DKIM/SPF posture.
- Preparing Verified Mark Certificate (VMC) evidence packs.
- Focus tokens: **golang, bimi, notes**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General DNS/email security program | org email-auth runbooks |
| Abuse prevention on HTTP APIs | `golang-abuse-prevention` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Prerequisite | Notes |
| --- | --- |
| SPF | Aligned sending sources |
| DKIM | Signing outbound |
| DMARC | `p=quarantine/reject` preferred for BIMI participation |
| BIMI TXT | `default._bimi.example.com` → `v=BIMI1; l=https://...svg` |
| Logo | SVG Tiny PS requirements; HTTPS |
| VMC/CMC | Needed for many mailbox providers’ checkmark |
| Go | Generators/validators; MTA hooks rarely pure Go—focus DNS+HTTPS hosting |

## Workflow

### 1. Confirm scope and success criteria

1. Domains, brand owners, authorization for DNS/certs.
2. Success: DMARC enforced; BIMI record valid; logo fetches; provider support tested.
3. Rollback DNS TTL plan.

### 2. Inventory

1. Sending sources (ESP, on-prem, Go notifiers).
2. Current SPF/DKIM/DMARC via DNS queries.
3. Logo asset ownership.

### 3. Baseline

```bash
# Authorized checks on your domain
dig +short TXT default._bimi.example.com
dig +short TXT _dmarc.example.com
```

1. DMARC aggregate reports review (policy readiness).
2. Fix SPF/DKIM alignment gaps first.

### 4. Implement BIMI

1. Host SVG at HTTPS URL with strong TLS; cacheable.
2. Publish BIMI TXT; optionally `a=` authority evidence location.
3. Obtain VMC if targeting Gmail/etc. enhanced indicators; store cert securely.
4. Go automation sketch:

```go
// Fetch and basic-validate BIMI assertion record + logo URL reachability
func CheckBIMI(ctx context.Context, domain string) error {
	// lookup TXT default._bimi.<domain>
	// parse v=BIMI1; ensure l= https URL
	// HTTP GET logo with size/type checks
	return nil
}
```

5. Ensure Go transactional mailers sign DKIM and use aligned From domains.

### 5. Verify with evidence

```bash
go test ./internal/mailauth/... -count=1
dig +short TXT default._bimi.example.com
curl -fsSI https://brand.example/bimi/logo.svg
# Send test messages to supporting mailbox providers you control
```

1. DMARC `pct=100` reject/quarantine stable before claiming BIMI success.
2. Logo meets BIMI SVG profile (validator tools).
3. Document provider-specific display results.

### 6. Observe and harden

1. Monitor DMARC failure rates after BIMI publish.
2. Alert on logo URL downtime (BIMI degrades).
3. Renew VMC before expiry; calendar reminder.

### 7. Hand off

1. DNS + cert owners documented.
2. Brand guidelines for logo updates (re-validation).
3. Link to incident response if domain spoofing rises.

## Record examples (illustrative)

```text
default._bimi.example.com TXT "v=BIMI1; l=https://www.example.com/bimi/logo.svg; a=https://www.example.com/bimi/vmc.pem"
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Order | DMARC enforce then BIMI | BIMI on `p=none` only forever |
| Logo | Spec-compliant SVG HTTPS | Random PNG on HTTP |
| Sending | Aligned DKIM/SPF | Forwarding-broken unaligned From |
| Topic fidelity | BIMI for owned domains | Generic go test only |

## Output Checklist

- [ ] Domains authorized and inventoried
- [ ] SPF/DKIM/DMARC ready
- [ ] BIMI TXT + logo published
- [ ] VMC process if required
- [ ] Validation evidence (dig/curl/tests)
- [ ] Monitoring for logo/DMARC
- [ ] Owners and renewal calendar

## Rules

- Only for brands you own.
- Focus on `golang-bimi-notes`.
- Authentication first, indicators second.
- Protect VMC private materials.
