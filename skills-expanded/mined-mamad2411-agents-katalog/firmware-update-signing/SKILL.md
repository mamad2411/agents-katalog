---
name: firmware-update-signing
description: >
  Design and review firmware update signing and verification: key hierarchy, signature
  algorithms, anti-rollback counters, secure boot chain alignment, update package format,
  and failure modes. Use when implementing or auditing OTA/USB update authenticity on
  owned devices and authorized product security reviews—not for bypassing third-party
  update protection without authorization.
---

# Firmware Update Signing

## Scope And Authorization

- **In scope:** devices, update servers, and signing pipelines you own or are authorized to assess.
- **Out of scope:** forging vendor updates, stealing production signing keys, or unauthorized downgrade attacks against third parties.
- Protect signing keys as tier-0 secrets; use HSMs for production.
- Redact private keys and production certs from tickets.
- Pair code/IaC with `code-quality-standards`.

## When To Use

- Building or reviewing **signed OTA/USB firmware** packages.
- Ensuring bootloaders verify signatures before install/boot.
- Anti-rollback (monotonic version/security counters).
- Aligning secure boot, dm-verity/fs integrity, and update client checks.
- Incident response after suspected malicious update (owned fleet).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| First-pass firmware unpack | `firmware-analysis-basics` |
| Binary RE of updater binary | `binary-re/static-analysis` |
| General secrets rotation | `secrets-management-hygiene` |
| Mobile app pinning | `mobile-ssl-pinning-bypass` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Intent |
| --- | --- |
| Authenticity | Image from trusted publisher (sig verify) |
| Integrity | Bytes unmodified |
| Freshness / anti-rollback | No install of older vulnerable version |
| Confidentiality (optional) | Encrypt image for IP; not a substitute for signing |
| Key custody | Offline root; online limited subkeys; rotation |

## Threats

| Threat | Mitigation |
| --- | --- |
| Unsigned image accepted | Mandatory verify before flash |
| Strip signature / parse bug | Strict parser; fail closed |
| Downgrade to vuln version | Monotonic version + rollback protect fuses/counters |
| Compromised transport only | TLS helps privacy/integrity in transit but **signing** still required end-to-end |
| Dev keys in prod devices | Separate PKI; disable debug unlock |
| Key theft from CI | HSM/KMS; dual control; short-lived job identity |

## Workflow

### 1. Confirm scope and success criteria

1. Device class, boot ROM capabilities, existing secure boot state.
2. Success: modified image rejected; correctly signed image accepted; older version rejected when policy requires.
3. Define algorithm suite (e.g. ed25519, ECDSA-P256, RSA-3072+) and encoding (raw, CMS, custom TLV).

### 2. Inventory update chain

```text
Signing system → artifact repo → device downloader → verifier → installer → reboot → bootloader verify
```

1. Where is public key stored (ROM, efuse, rpmb, A/B slot metadata)?
2. Is verification in bootloader, userspace, or both?
3. Map package format: header, payload, signature blob, cert chain.

### 3. Baseline failure cases (lab devices)

1. Flip one payload bit → must fail.
2. Re-sign with wrong key → fail.
3. Truncate signature → fail.
4. Downgrade package → fail if anti-rollback enabled.
5. Valid sign → success path.

### 4. Implement or harden verification

```python
# Pseudocode verifier — use vetted crypto libs only
def verify_update(pkg: bytes, pubkey, min_version: int) -> bytes:
    header, payload, sig = parse(pkg)  # strict lengths
    if header.version < min_version:
        raise RollbackError()
    if not raw_verify(pubkey, header.canonical_bytes + payload, sig):
        raise AuthError()
    return payload
```

```text
# Ops signing (illustrative)
# hash payload → sign in HSM → attach sig → publish
# Never export raw private key to general CI disks
```

1. Verify **before** any flash of untrusted regions; avoid TOCTOU (verify then flash without re-fetch).
2. Pin algorithms; reject `none`/unknown alg IDs.
3. If cert chains used: validate chain, time (with care for offline devices), revocation strategy.
4. Anti-rollback storage must be non-user-resettable (efuse/RPMB/TEE), not only a file on writable userdata.
5. A/B updates: confirm both slots covered; prevent rollback slot activation without policy.

### 5. Align with secure boot

1. Bootloader signature verification should not be weaker than OTA client.
2. Document whether userspace OTA is bypassable by writing raw flash—if so, hardware root of trust is mandatory.
3. Debug unlock procedures audited and logged.

### 6. Verify with evidence

| Test | Result |
| --- | --- |
| Bit-flip payload | Reject + error metric |
| Wrong key | Reject |
| Downgrade | Reject |
| Official build | Accept + boot |
| Key rotation dual-sign window | Documented |

```bash
# Lab: compare hashes and attempt install via owned update tool only
sha256sum good.bin evil.bin
```

### 7. Observe and hand off

1. Metrics: verify_fail_total, rollback_reject_total, update_success.
2. Alert on fleet-wide verify failures (bad rollout or attack).
3. Runbook for key compromise (revoke, freeze updates, re-provision strategy).
4. Apply `code-quality-standards` for verifier code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Crypto | Modern sig + vetted lib | Homegrown hash compare only |
| Keys | HSM root offline | PEM in GitHub Actions plaintext |
| Rollback | Hardware counter | version.txt on SD card |
| Transport | TLS + signed payload | HTTPS only, no image sig |
| Fail mode | Brick-safe recover signed only | Accept unsigned “for recovery” always |
| Evidence | Lab reject tests | “We sign builds” without device verify |

## Output Checklist

- [ ] Chain of trust diagram complete
- [ ] Algorithms and package format documented
- [ ] Key custody and rotation documented
- [ ] Verifier fail-closed behavior evidenced
- [ ] Anti-rollback mechanism reviewed
- [ ] Secure boot alignment assessed
- [ ] Incident/compromise runbook exists
- [ ] Metrics/alerts defined
- [ ] `code-quality-standards` applied

## Rules

- Owned/authorized devices only.
- Signing without on-device verification is theater.
- Protect signing keys as production crown jewels.
- Do not assist unauthorized bypass of update authentication.
- Hand unpack/analysis to `firmware-analysis-basics`; keep this skill on authenticity of updates.
