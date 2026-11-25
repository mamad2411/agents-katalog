---
name: dnssec-deployment-basics
description: >
  Deploy and operate DNSSEC on zones you own or are authorized to manage: key models
  (KSK/ZSK or CSK), signing algorithms, DS publication at the parent, chain-of-trust
  validation, key rollover, NSEC/NSEC3, and failure triage. Use when enabling DNSSEC,
  fixing BOGUS/SERVFAIL after signing, publishing or rotating DS/CDS/CDNSKEY, planning
  algorithm or key rollovers, choosing NSEC vs NSEC3, or verifying resolver validation
  for org-owned DNS — not for attacking third-party zones.
---

# DNSSEC Deployment Basics

## Scope And Authorization

- **In scope:** Zones and DNS providers you own or operate under contract.
- **Out of scope:** Breaking DNSSEC on third-party domains; unauthorized AXFR.
- Prefer staging/child zone first; parent DS changes are high impact.
- Protect private keys (HSM/KMS/provider); never commit them.
- Pair with `dns-latency-triage`, `dmarc-spf-dkim-hardening` (records still need signing), and `secrets-management-hygiene`.

## When To Use

- Enabling DNSSEC on corporate or product domains.
- Fixing validating resolvers returning SERVFAIL (BOGUS).
- Publishing/updating DS at registrar after key rollover.
- Choosing algorithms (e.g. ECDSA P-256, ED25519 where supported).
- Planning KSK/ZSK or CSK rollovers without outage.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Email SPF/DKIM/DMARC content | `dmarc-spf-dkim-hardening` |
| DoH privacy | `dns-over-https-basics` |
| DNS rebinding | defense/attacks skills |
| Registrar business process only | registrar runbook |
| Code quality baseline | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| RRSIG | Signature over RRset |
| DNSKEY | Public keys in zone |
| DS | Hash of KSK at parent—chain of trust |
| KSK / ZSK | Key- / zone-signing keys (classic split) |
| CSK | Combined signing key model |
| NSEC/NSEC3 | Authenticated denial of existence |
| AD flag | Authenticated Data (validating resolver) |
| BOGUS | Validation failure → often SERVFAIL |

## Workflow

### 1. Confirm scope and success criteria

1. Zone name, DNS hoster, registrar (parent DS), algorithm policy, rollover owners.
2. Success: chain validates from root; public resolvers set AD; no BOGUS; DS matches KSK; monitoring on.
3. Maintenance window for DS publish/remove.

### 2. Inventory and readiness

```bash
dig example.com DNSKEY +dnssec
dig example.com DS +dnssec
dig example.com A +dnssec @1.1.1.1
# Check DS at parent
dig DS example.com @$(dig NS com +short | head -1)
```

1. Ensure all authoritative NS serve consistent signed data.
2. TTLs and multi-provider: multi-signer needs careful CDS/CDNSKEY or coordinated keys.

### 3. Enable signing on authoritative

1. Provider UI or software (BIND `dnssec-policy`, Knot, PowerDNS, cloud DNS “DNSSEC on”).
2. Prefer modern algorithms supported by your parent and resolvers (e.g. 13/ECDSAP256SHA256 or 15/ED25519 when ecosystem allows).
3. Choose NSEC vs NSEC3 (NSEC3 for zone walking privacy tradeoffs; many public zones use NSEC OK).
4. Wait until all auth NS serve DNSKEY + RRSIGs.

### 4. Publish DS at parent

1. Export DS (key tag, algorithm, digest type, digest) from DNSKEY KSK.
2. Enter at registrar/parent; wait for parent propagation.
3. Optional CDS/CDNSKEY automation if parent supports (registry-dependent).

```bash
# Verify chain
dig example.com A +dnssec +multi
delv example.com A 2>/dev/null   # if available
```

1. Confirm AD bit from validating resolvers.
2. Online checkers you trust as secondary signal only.

### 5. Rollover procedures (high level)

| Rollover | Idea |
| --- | --- |
| ZSK | Pre-publish new ZSK → sign → wait → remove old (timing via TTLs) |
| KSK | Dual KSK → DS add new → wait → remove old DS → retire old KSK |
| Algorithm | Follow RFCs/provider wizards carefully—easy to BOGUS |

1. Never remove DS before new chain is live and propagated.
2. Track key tag and calendar; dual-control for DS changes.

### 6. Failure triage

| Symptom | Checks |
| --- | --- |
| SERVFAIL only on validating resolvers | Signatures expired, wrong DS, partial NS unsigned |
| Intermittent | Multi-NS inconsistency; clock skew on signer |
| After rollover | DS mismatch; old RRSIG TTL still cached |
| Latency up | Larger responses; TCP fallback; `dns-latency-triage` |

```bash
dig example.com A @8.8.8.8 +dnssec
dig example.com DNSKEY +multi
dig example.com RRSIG +multi
```

1. Emergency: some orgs remove DS to go insecure—treat as security incident with approval (validation disabled).

### 7. Operate and hand off

1. Monitor signature expiry, DS match, and SERVFAIL rates.
2. Calendar next rollover; document provider-specific steps.
3. Secure key material; audit who can change DS at registrar (MFA!).
4. After enable: re-check mail/HTTPS unrelated records still correct.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| DS | Match live KSK; wait propagate | Delete DS mid-rollover |
| Keys | HSM/provider secure | DNSKEY private in email |
| Multi-NS | All signed consistently | One NS unsigned |
| Algo | Modern supported | Broken/deprecated only |
| Monitor | Expiry alerts | Set and forget |
| Emergency | Ticketed insecure | Panic DS delete often |

## Output Checklist

- [ ] Zone/provider/registrar owners listed
- [ ] Signing enabled on all auth NS
- [ ] DS published and validated (AD bit)
- [ ] Algorithm and NSEC mode documented
- [ ] Rollover runbook written
- [ ] Monitoring for BOGUS/expiry
- [ ] Key custody and registrar MFA verified
- [ ] Multi-signer issues addressed if any
- [ ] Post-change resolve tests pass
- [ ] Residual risk noted

## Rules

- Parent DS is production-critical—change carefully.
- Protect private keys; dual control on DS.
- Validate with multiple resolvers before declaring success.
- Owned/authorized zones only.
- Focus on DNSSEC deploy/ops, not email content or rebinding.
