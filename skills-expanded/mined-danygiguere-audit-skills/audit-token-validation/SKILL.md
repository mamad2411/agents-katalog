---
name: audit-token-validation
description: Inbound token and webhook verification checklist. Use when code verifies JWTs, API keys, signed URLs, or webhook signatures — decode-without-verify, alg confusion, missing exp/aud/iss checks, kid/JWKS handling, HMAC over raw body, replay windows.
---

Read `../audit/references/access-data-security/token-validation.md` and apply
its checklist to the code the user specified (or the current diff if none was
given). If the target is larger than a diff — a module, service, or whole repo —
follow `../audit/references/methodology/scope.md` first. Verify each candidate
with `../audit/references/methodology/verify.md` before reporting. Report
surviving findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
