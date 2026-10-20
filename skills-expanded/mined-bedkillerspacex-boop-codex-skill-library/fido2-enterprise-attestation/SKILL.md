---
name: fido2-enterprise-attestation
description: >
  Plan and implement FIDO2/WebAuthn enterprise attestation: attestation conveyance,
  packed/TPM/Android key formats, MDS/metadata service, allowlists of AAGUIDs and
  attestation root certificates, and privacy tradeoffs. Use when enterprises require
  proof that authenticators are company-approved hardware keys on owned RPs, or when
  reviewing attestation verification code and policy.
---

# FIDO2 Enterprise Attestation

## Scope And Authorization

- **In scope:** relying parties (RPs) and authenticator policies you own; lab authenticators; authorized reviews.
- **Out of scope:** extracting attestation private keys from devices, forging vendor attestations, or attacking third-party RPs.
- Attestation can identify device models—handle as sensitive inventory data.
- Redact attestation certificates and user handles from public tickets.
- Pair RP code with `code-quality-standards`.

## When To Use

- Requiring **enterprise-approved** security keys (YubiKey, Titan, etc.) for workforce login.
- Implementing WebAuthn `attestation` conveyance (`none`, `indirect`, `direct`, `enterprise`).
- Verifying attestation statements (packed, TPM, android-key, apple) against roots/MDS.
- Building AAGUID allow/deny lists and continuous policy updates.
- Deciding when attestation is mandatory vs optional for consumer vs enterprise RPs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic OAuth/JWT API auth | `api-auth-and-jwt-abuse` |
| FedCM browser federation | `fedcm-basics` |
| Account takeover methodology | `account-takeover-methodology` |
| Secrets management | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Notes |
| --- | --- |
| Attestation | Proof about authenticator properties at registration time |
| AAGUID | Authenticator model identifier (16 bytes) |
| Conveyance | Whether browser/RP receives attestation statement |
| MDS | FIDO Metadata Service — vendor capabilities and status |
| Enterprise attestation | Vendor/enterprise modes that may return uniquely identifying attestation |
| Verification | Signature chain to trusted roots; match policy (FIPS, biometric, etc.) |

## Conveyance choices

| Mode | Effect | Typical use |
| --- | --- | --- |
| `none` | No attestation (privacy-friendly) | Consumer RPs |
| `indirect` | Anonymized/possibly browser-mediated | Rare intermediate |
| `direct` | Full attestation statement to RP | Enterprise device control |
| `enterprise` | Enterprise attestation when supported | Strict workforce deployments |

## Workflow

### 1. Confirm scope and success criteria

1. Define which authenticator classes are allowed (hardware-bound, USB/NFC/BLE, platform vs roaming).
2. Success: unapproved software authenticators rejected at registration; approved keys register; verification failures logged.
3. Legal/privacy review if attestation uniquely identifies tokens.

### 2. Inventory RP WebAuthn policy

```javascript
// Registration options sketch
navigator.credentials.create({
  publicKey: {
    rp: { id: "sso.example.com", name: "Example SSO" },
    user: { id: userIdBytes, name: email, displayName: name },
    challenge: challengeBytes,
    pubKeyCredParams: [{ alg: -7, type: "public-key" }, { alg: -257, type: "public-key" }],
    authenticatorSelection: {
      authenticatorAttachment: "cross-platform",
      residentKey: "preferred",
      userVerification: "required",
    },
    attestation: "direct", // or "enterprise" when supported
    // extensions: { ... enterprise attestation extensions per current WebAuthn level }
  },
});
```

1. Confirm server libraries support attestation verification (not only storing `none`).
2. Inventory existing credentials missing attestation (legacy).

### 3. Establish trust anchors and MDS

1. Load FIDO MDS blobs or vendor root certificates per policy.
2. Maintain AAGUID allowlist from procurement (approved models).
3. Track revocation/status reports (compromised firmware flags in MDS).

```text
# Ops checklist
# - Scheduled job to refresh MDS
# - Alert if MDS stale > N days
# - Change control for AAGUID allowlist edits
```

### 4. Verify attestation on registration

1. Parse attestation object: `authData`, `fmt`, `attStmt`.
2. Validate `rpIdHash`, flags (AT, UV as required), AAGUID.
3. Verify `attStmt` signature chain for `fmt` (packed/TPM/…).
4. Enforce policy: AAGUID ∈ allowlist; attestation root trusted; UV required if policy says so.
5. Store credential public key + AAGUID + attestation result metadata (not necessarily full cert chain forever—define retention).

```python
# Pseudocode — use a maintained WebAuthn server library in production
def register(attestation_object, client_data_json, expected_challenge, policy):
    parsed = verify_attestation(attestation_object, client_data_json, expected_challenge)
    if parsed.aaguid not in policy.allowed_aaguids:
        raise PolicyError("authenticator_not_allowed")
    if not parsed.attestation_trusted:
        raise PolicyError("attestation_untrusted")
    save_credential(parsed.credential_id, parsed.public_key, parsed.aaguid)
```

### 5. Verify with evidence

1. Register approved hardware key → success.
2. Register disallowed software authenticator (lab) → rejected.
3. Tamper attestation signature in unit test → rejected.
4. Expired MDS / missing root → fail closed or explicit degraded mode with alert.

### 6. Observe and harden

1. Metrics: registration success by AAGUID, attestation failures by reason.
2. Alert on sudden surge of unknown AAGUIDs (probing or policy gap).
3. Authentication ceremony: attestation usually registration-time; do not assume every auth returns attestation.

### 7. Hand off

1. Document conveyance mode, allowlist process, MDS refresh, exception path (break-glass keys).
2. Train helpdesk on supported key models.
3. Apply `code-quality-standards` for RP verification code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Policy | Explicit AAGUID + root trust | Accept any attestation `fmt` without chain check |
| Privacy | Enterprise-only RP; retention limits | Log full certs in SIEM forever without need |
| Conveyance | `direct`/`enterprise` when required | `none` but claim hardware proof |
| Fail mode | Deny unknown devices | Soft-allow on verify errors |
| Libraries | Maintained WebAuthn libs | Hand-rolled ASN.1 crypto only |
| Lifecycle | MDS refresh automation | One-time root PEM from 2019 |

## Output Checklist

- [ ] RP policy and conveyance mode documented
- [ ] Trust anchors / MDS refresh process in place
- [ ] AAGUID allowlist with owners
- [ ] Verification implemented via sound library + tests
- [ ] Allowed vs denied authenticators evidenced
- [ ] Privacy/retention of attestation data decided
- [ ] Metrics and stale-MDS alerts
- [ ] Break-glass procedure documented
- [ ] `code-quality-standards` applied

## Rules

- Owned RPs and authorized labs only.
- Attestation verification failures must not be silently ignored if policy requires hardware proof.
- Distinguish registration attestation from ongoing authentication assertions.
- Treat enterprise attestation identifiers as sensitive inventory.
- Keep focus on FIDO2/WebAuthn attestation—not general password policy.
