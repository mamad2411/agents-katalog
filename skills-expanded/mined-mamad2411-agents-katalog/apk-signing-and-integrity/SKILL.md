---
name: apk-signing-and-integrity
description: >
  Authorized APK signing-scheme and integrity assessment: APK Signature Scheme
  v1/v2/v3/v4, cert lineage, apksigner verification, split/AAB notes, and app-side
  integrity or repack detection patterns. Use when reviewing how an owned or lab
  Android package is signed, re-signed, or self-checks integrity — not for
  distributing pirated or fraudulently re-signed third-party apps.
---

# APK Signing And Integrity

## Scope And Authorization

- **In scope:** APKs/AABs you build, own, or assess under written authorization (labs, CTF, internal mobile apps).
- **Out of scope:** Re-signing third-party apps for piracy, malware distribution, or unauthorized store fraud.
- Treat keystores, upload keys, and Play App Signing enrollment as high-value secrets.
- Prefer non-production keystores for experiments; never reuse production upload keys in CI logs.
- Pair any CI/signing automation with `code-quality-standards` and `secrets-management-hygiene`.

## When To Use

- Verifying which signature schemes (v1 JAR / v2 / v3 / v4) an APK uses and whether they verify cleanly.
- Comparing signing cert fingerprints across builds, channels, or “official vs suspect” lab samples.
- Diagnosing install failures (`INSTALL_PARSE_FAILED_NO_CERTIFICATES`, signature mismatch on update).
- Reviewing app-side integrity checks (signature hash pin, SafetyNet/Play Integrity handoff, anti-repack).
- Signing/aligning release builds with `apksigner` / `jarsigner` / `zipalign` in owned pipelines.
- Understanding lineage (v3 rotation) and split-APK / AAB → APK signing implications.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SSL pinning / MITM on mobile traffic | `mobile-ssl-pinning-bypass` (authorized only) |
| General Android reverse engineering | `binary-re/static-analysis` or mobile RE skills |
| Play Integrity / device attestation deep dive | attestation-specific skill if present; else document here lightly only |
| Secrets storage for keystores in vaults | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| v1 (JAR) | `META-INF/*.RSA|DSA|EC` + MANIFEST; required for some old paths; alone is weaker |
| v2 | Whole-file APK Signing Block; verified before install; preferred baseline |
| v3 | Key rotation / lineage; signed proof of cert succession |
| v4 | Incremental install friendly (fs-verity style) with `.idsig`; pair with v2/v3 |
| Tooling | `apksigner`, `aapt`/`aapt2`, `keytool`, `jarsigner`, `zipalign`, bundletool |
| Integrity | Pin signing cert SHA-256 in app only as one layer; prefer server + Play Integrity |

## Signature Scheme Matrix

| Scheme | What is signed | Notes |
| --- | --- | --- |
| v1 | ZIP entries via MANIFEST | Mutable after-sign risks if used alone on modern Android |
| v2 | APK contents + central directory | Required path for modern install verification |
| v3 | Same as v2 + lineage attribute | Use when rotating signing keys without reinstall gap |
| v4 | Companion `.idsig` | Speeds adb incremental; still need v2/v3 on the APK |

## Workflow

### 1. Confirm scope and success criteria

1. Record package name, versionCode/versionName, channel (debug/release/internal), authorization.
2. Success examples: `apksigner verify` exit 0; expected cert SHA-256 matches release inventory; v2+ present for target API; no unexpected extra signers.
3. Identify production keystore owners and break-glass for lost upload keys (Play App Signing).

### 2. Inventory the package and certs

```bash
APK=app-release.apk
# Schemes + certs
apksigner verify --verbose --print-certs "$APK"
# Package identity
aapt dump badging "$APK" | head -n 20
# Optional: list signers / digests
keytool -printcert -jarfile "$APK"
```

1. Capture **Subject**, **SHA-256** of signing cert(s), and whether multiple signers exist.
2. For AABs: note that Play may re-sign with app signing key; local upload key ≠ what devices see if enrolled.
3. For split APKs: verify each split and base share the same signer set.

### 3. Baseline before re-sign or policy change

1. Store current `apksigner verify --print-certs` output and file hash (`sha256sum`) of the release artifact.
2. Export cert-only (public) fingerprint sheet for app config / MDM allowlists — never export private keys to tickets.
3. Note minSdk / targetSdk: v2 required for install on modern Android when targeting recent APIs.

### 4. Sign, align, and rotate correctly (owned builds)

**Align then sign (release-style):**

```bash
zipalign -p -f 4 app-unsigned.apk app-aligned.apk
apksigner sign --ks release.jks --ks-key-alias release \
  --out app-release.apk app-aligned.apk
apksigner verify --verbose app-release.apk
```

**Explicit scheme selection (example: v2+v3):**

```bash
apksigner sign --ks release.jks --ks-key-alias release \
  --v1-signing-enabled true \
  --v2-signing-enabled true \
  --v3-signing-enabled true \
  --v4-signing-enabled true \
  --out app-release.apk app-aligned.apk
```

**v3 key rotation lineage (conceptual):**

1. Generate new key; build lineage with `apksigner rotate` / lineage tools per current SDK docs.
2. Sign with new key + attach lineage proving old → new.
3. Verify lineage prints as expected; test upgrade install from old-signed build to new-signed build.

1. Prefer **Play App Signing**: upload key signs AAB; Google holds app signing key.
2. CI: inject keystore from secret store; never commit `.jks`/`.keystore` or passwords.
3. Debug keystores are not production evidence — label them clearly.

### 5. App-side integrity patterns (defensive, owned apps)

| Check | Good practice | Weak / avoid alone |
| --- | --- | --- |
| Signing cert pin | Compare runtime `PackageManager` signatures to expected SHA-256 | Hardcoded only, no server signal |
| Installer package | Expect Play / MDM installer where applicable | Trusting installer alone |
| Play Integrity / SafetyNet | Server validates verdict + nonce | Client-only boolean |
| DEX / resource hash | Tamper-evident for offline CTF labs | Fragile across Play optimizations |

1. Prefer server-side binding of integrity tokens to session/account.
2. Expect repackers to patch local checks — design for detection/telemetry, not absolute prevention.
3. Document false-positive risk after legitimate key rotation.

### 6. Verify with evidence

```bash
apksigner verify --verbose --print-certs app-release.apk
# Expect: Verified using v2 and/or v3; cert SHA-256 matches inventory
sha256sum app-release.apk
# Install test on lab device/emulator (owned)
adb install -r app-release.apk
# Upgrade path: install old, then new; must not fail SIGNATURE_MISMATCH when lineage correct
```

1. For multi-signer / sharedUserId legacy: document why second cert exists.
2. Diff certs between CI artifact and store-downloaded APK when Play App Signing is on (expected difference if comparing upload vs signing key).
3. Keep redacted fingerprints in the change ticket.

### 7. Hand off

1. Record cert inventory, scheme requirements, and keystore rotation owners.
2. Add CI step: `apksigner verify` must pass before promote.
3. Link Play Console App Signing page ownership and recovery contacts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Schemes | v2+ (and v3 if rotating) on modern targets | v1-only release APK |
| Keys | HSM/Play-held app signing; upload key in vault | Debug keystore in git |
| Verify | `apksigner verify --print-certs` evidence | “It installs on my phone” |
| Rotation | v3 lineage + upgrade tests | New cert without plan → forced uninstall |
| Integrity | Server-validated attestation + pin | Client-only `if (tampered) exit` |
| Scope | Own/lab packages | Re-sign third-party apps for redistribution |

## Output Checklist

- [ ] Scope, package IDs, channel, authorization recorded
- [ ] Baseline cert fingerprints and schemes captured
- [ ] `apksigner verify` (verbose + print-certs) clean for release artifact
- [ ] Align → sign order correct; v2/v3/v4 choices documented
- [ ] Split/AAB/Play App Signing implications noted
- [ ] App-side integrity design reviewed (not sole control)
- [ ] Keystore/secret handling meets org policy
- [ ] Upgrade/re-sign tests executed on lab devices
- [ ] CI gate and owners documented
- [ ] `code-quality-standards` applied if pipeline code shipped

## Rules

- Authorized packages and labs only; no fraudulent re-signing of third-party software.
- Never commit private keys or keystore passwords; redact cert details only when policy requires (public certs are usually shareable).
- Prefer platform + store integrity signals over brittle client-only checks.
- Keep this skill on signing schemes, cert lineage, and integrity verification; route traffic interception and deep RE elsewhere.
- Evidence over assumptions: always keep `apksigner` output for the exact artifact hash you ship.
