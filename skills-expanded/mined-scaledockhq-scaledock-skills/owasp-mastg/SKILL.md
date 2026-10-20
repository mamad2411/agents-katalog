---
name: owasp-mastg
description: >-
  OWASP MASTG: test iOS and Android app security with the Mobile Application Security Testing Guide. Covers OWASP MASTG. Use when testing mobile application security. Triggers: MASTG.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWASP MASTG

The OWASP Mobile Application Security Testing Guide (MASTG) v2.0.0: the pass and fail criteria of its atomic tests (MASTG-TEST ids), each mapped to a MASVS category and a MASWE weakness, read from the project's Markdown source at the v2.0.0 release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Mobile security tester, reviewer or developer of an iOS or Android app.
- Target version: OWASP MASTG (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **MASTG-TEST-0300.** "The test case fails if the sensitive data is not encrypted before being written to private storage or the Keychain API isn't used to store the sensitive data."
2. **MASTG-TEST-0233.** "The test case fails if any HTTP URLs are confirmed to be used for communication."
3. **MASTG-TEST-0242.** "The test case fails if no `networkSecurityConfig` is set, or any relevant domain does not enable certificate pinning."
4. **MASTG-TEST-0338.** "The test case fails if the app uses data loaded from local storage (`SharedPreferences`, files, or databases) in a security-relevant decision without verifying its integrity and authenticity beforehand."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Every finding names its MASTG-TEST id, its MASWE weakness and the MAS profile it was tested against.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `owasp-masvs`, `owasp-mobile-top-10`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [MASTG-TEST-0200: Files Written to External Storage (Android, MASWE-0007)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0200.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0207: Runtime Storage of Unencrypted Data in the App Sandbox (Android, MASWE-0006)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0207.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0216: Sensitive Data Not Excluded From Backup (Android, MASWE-0004)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0216.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0300: References to APIs for Storing Unencrypted Data in Private Storage (iOS, MASWE-0006)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0300.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0297: Sensitive Data Exposure Through Logging APIs (iOS, MASWE-0001)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0297.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0204: Insecure Random API Usage (Android, MASWE-0027)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0204.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0208: Insufficient Key Sizes (Android, MASWE-0009)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0208.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0233: Hardcoded HTTP URLs (Android, MASWE-0050)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0233.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0234: Missing Implementation of Server Hostname Verification with SSLSockets (Android, MASWE-0052)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0234.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0242: Missing Certificate Pinning in Network Security Configuration (Android, MASWE-0047)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0242.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0396: References to URLSessionDelegate Bypassing Certificate Validation (iOS, MASWE-0052)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0396.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0326: References to APIs Allowing Fallback to Non-Biometric Authentication (Android, MASWE-0045)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-AUTH/MASTG-TEST-0326.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0270: References to APIs Detecting Biometric Enrollment Changes (iOS, MASWE-0046)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0270.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0226: Debuggable Flag Enabled in the AndroidManifest (Android, MASWE-0067)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0226.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0225: Usage of Insecure APK Signature Key Size (Android, MASWE-0104)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0225.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0324: References to Root Detection Mechanisms (Android, MASWE-0097)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0324.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0338: References to Storage Integrity Check APIs (Android, MASWE-0105)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0338.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
- [MASTG-TEST-0206: Undeclared PII in Network Traffic Capture (Android, MASWE-0108)](https://raw.githubusercontent.com/OWASP/owasp-mastg/v2.0.0/tests-beta/android/MASVS-PRIVACY/MASTG-TEST-0206.md): OWASP Flagship Project guide, Tag v2.0.0 (2026-06-30), checked 2026-10-06.
