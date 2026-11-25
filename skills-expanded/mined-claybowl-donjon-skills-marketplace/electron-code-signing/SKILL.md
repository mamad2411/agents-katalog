---
name: electron-code-signing
description: >
  This skill should be used when the user needs to code-sign or notarize an
  Electron desktop app for macOS or Windows distribution. Triggers on phrases
  like "sign my electron app", "notarize electron", "apple developer cert",
  "code signing certificate", "windows EV cert", "EV code signing",
  "macos notarization", "notarize app", "unidentified developer warning",
  "SmartScreen warning", "signing in CI", or "my app is flagged as untrusted
  by macOS / Windows".
version: 0.1.0
---

# Electron Code Signing

## When this skill is loaded

The user is preparing to distribute an Electron app outside a trusted distribution channel (i.e., not an internal deploy) and needs to sign the binary so users' OS trust checks don't block or scare them off. Signing is **required** for `electron-updater` to work silently on macOS — unsigned updates abort.

## TL;DR by platform

| Platform | Cert type | Typical cost | Setup time | Required for auto-update? |
|---|---|---|---|---|
| macOS | Apple Developer ID Application | $99/yr (Apple Developer Program) | 1–3 business days | **Yes, hard requirement** |
| Windows | EV Code Signing (DigiCert / Sectigo / SSL.com) | $300–500/yr | 2–5 days (hardware token ships) | Recommended; OV certs cause SmartScreen delays |
| Linux | None required; optional GPG sig | $0 | Hours | No |

## macOS — the two-step gate

Two steps must happen in strict order:

1. **Code sign** the app with a Developer ID Application certificate (using `@electron/osx-sign`, wrapped by electron-builder).
2. **Notarize** the signed app — upload to Apple, Apple scans for malware, Apple returns a ticket, you "staple" the ticket to the binary (also wrapped by electron-builder).

**Without step 1:** macOS shows "Apple could not verify this app is free of malware." Users right-click to open. Users do not buy this.
**Without step 2:** Same outcome since macOS 10.15 (Catalina) — notarization is a hard gate for apps distributed outside the Mac App Store.

### The certificate chain

1. Enroll in the [Apple Developer Program](https://developer.apple.com/programs/) ($99/year). Requires a D-U-N-S number for orgs (Apple provides one free); or use your personal Apple ID for solo dev.
2. In Xcode (or Apple Developer portal) → Certificates → create a **Developer ID Application** certificate. Download, double-click to install into Keychain.
3. Export the cert **and its private key** from Keychain as a `.p12` file. Set a strong password; you'll need it in CI.

### The notarization credentials

Notarization uses app-specific passwords, not your Apple ID password directly.

1. Go to [appleid.apple.com](https://appleid.apple.com/) → Sign-In and Security → App-Specific Passwords → generate one labeled "electron-notarize".
2. Your `APPLE_ID` is your Apple ID email.
3. Your `APPLE_TEAM_ID` is a 10-character string from Apple Developer portal → Membership.
4. Your `APPLE_APP_SPECIFIC_PASSWORD` is the one you just generated.

All three go into GitHub Actions secrets for CI notarization.

See `references/macos-deep-dive.md` for a full CI workflow YAML.

## Windows — pick your pain

Three real paths, ranked by ease:

### Path 1: Cloud code signing service (EASIEST)

Services like **SignPath**, **Certum SimplySign**, **DigiCert KeyLocker**, or **SSL.com eSigner** host the hardware token for you. You send the binary; they sign it; CI gets the signed binary back.

Cost: $150–400/yr. Best for solo devs and small teams.
Tradeoff: You trust the service with signing on your behalf.

### Path 2: Self-hosted EV token

You buy an EV Code Signing cert from DigiCert / Sectigo. They ship you a USB hardware token. You have to plug that physical token into a Windows machine to sign.

Cost: $300–500/yr for the cert; you also need a Windows CI runner capable of accessing the USB token (hosted GitHub runners cannot — you need self-hosted).
Tradeoff: Full control, immediate SmartScreen reputation. Physical token = physical security requirement.

### Path 3: Standard (OV) Code Signing cert

Cheaper ($80–150/yr), no hardware token required. But SmartScreen Filter still warns users until your cert builds reputation (weeks to months). Not recommended for new apps.

## The CI signing dance — short version

**macOS CI:**
1. Base64-encode your `.p12` and put it in `MAC_CERTIFICATE` GH Actions secret.
2. Add `MAC_CERTIFICATE_PASSWORD`, `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID`.
3. In the Mac runner, create a temporary keychain, import the `.p12`, set default-keychain.
4. Run `electron-builder --mac`. It detects the Developer ID cert, signs, notarizes, and staples — all in one go.

**Windows CI with SignPath (Path 1):**
1. Create a SignPath project for the app.
2. Add `SIGNPATH_ORG_ID`, `SIGNPATH_PROJECT_SLUG`, `SIGNPATH_SIGNING_POLICY_SLUG`, `SIGNPATH_API_TOKEN` to GH secrets.
3. CI builds unsigned installer → uploads to SignPath → downloads signed installer → uploads to GitHub Release. SignPath provides a reusable GH Action.

## Rookie mistakes

1. **Forgetting `hardenedRuntime: true` in electron-builder config.** Notarization will reject otherwise.
2. **Missing entitlements file.** Electron needs JIT entitlement (`com.apple.security.cs.allow-jit`). Scaffold has this; don't delete it.
3. **Notarization timeout fatalism.** Apple's queue varies 5 min to 2 hours. Don't assume failure under 30 min.
4. **Expired cert mid-release.** Set a calendar reminder for renewal 45 days before expiry. Nothing torches a release more reliably than an expired cert.
5. **Signing on a non-Mac runner for macOS.** Mac binaries must be signed on macOS (hosted `macos-latest` works). Linux `osslsigncode` does NOT work for Mac.
6. **Leaking the p12 password.** Never echo or log it in CI output. Use `::add-mask::` in GH Actions.
7. **Not checking the final signed binary.** Run `codesign -dvvv YourApp.app` and `spctl -a -t exec -vvv YourApp.app` on the artifact before publishing.

## Cost reality check

- Solo indie app, Mac + Windows: **~$400–500/year** all-in (Apple $99 + SignPath $300 or Certum cheaper).
- Mac only: **$99/year**.
- Enterprise with existing org cert infrastructure: often **$0** additional if they can share certs; ask before buying.

## References

- `references/macos-deep-dive.md` — full Mac signing + notarization CI walkthrough with YAML
- `references/windows-deep-dive.md` — Windows EV cert, SignPath integration, SmartScreen reputation
