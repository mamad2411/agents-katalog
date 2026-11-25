---
name: follow-lib-qrcode
description: Use qrcode to create QR codes — PNG/SVG/dataURL server-side or client-side
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test
  - follow-lib-otplib

---

## Goal

Use qrcode to create QR codes — PNG/SVG/dataURL server-side or client-side

## Scope

Use when the task involves this library/tool — setup, usage, debugging, or best practices (lib qrcode)

- Covers: QR code generation — PNG/SVG/dataURL/terminal output server-side, in the browser, or via CLI (`qrcode` command — see [cli](references/cli.md))
- Not covered: TOTP/2FA logic — use `/follow-lib-otplib` to create the `otpauth://` URI, then render the QR with this skill
- Latest: `qrcode@1.5.4` (verified 2026-09-13)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Use `QRCode.toDataURL()`, `toBuffer()`, `toString(type: svg)` per output
1. Set `errorCorrectionLevel` (M/Q/H for a logo overlay)
1. For API responses use `toBuffer` + `new Response(new Uint8Array(buf))`
1. Don't embed large data — QR has a limited capacity (~4KB binary)

### 2. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib qrcode)

## Rules

- Pick the output by consumer: dataURL for `<img>`, buffer for download
- Set margin/width so it actually scans (at least margin=2)
- Test a real scan before shipping

- Use `/run-verify` if needed
- Use `/run-test` if needed
- Use `/follow-lib-otplib` if the QR is an `otpauth://` TOTP enrollment

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib qrcode)
- No known security/performance pitfalls (lib qrcode)
- Lint, typecheck, tests pass
