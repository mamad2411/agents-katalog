---
name: validate-with-security-review
description: Validate a PR diff for security vulnerabilities, secret leakage, unsafe trust boundaries, and operational security pitfalls. Use during a validation cycle or when another skill needs a focused security review.
---

# Validate with security review

Read [the shared validation contract](../validate/validation-contract.md). The caller supplies `RUN_DIR` containing `context.json` and `changes.json`.

## Trace changed trust boundaries

Read the complete three-dot diff, then inspect callers, sinks, configuration, and tests around every security-relevant changed path. Trace untrusted input to its use and identity/authorization data to every protected action. Check applicable concerns: authentication and authorization, tenant isolation, input validation and injection, XSS and unsafe redirects, SSRF and outbound requests, path traversal and file access, deserialization, cryptography and token/session handling, secrets and sensitive data in code/logs/errors, dependency or supply-chain changes, rate limiting/resource exhaustion, and insecure defaults or production configuration.

Ground each report in an exploitable path or a concrete leak/pitfall in the diff. State preconditions, impact, and a specific mitigation. Do not report hypothetical risks that the surrounding code demonstrably prevents.

Write `security-review.json` atomically as the contract's finding array. Use `blocking` for an exploitable high-impact flaw or credential exposure, `important` for a credible security defect, and `minor` for a bounded hardening concern.

**Done when:** every changed security boundary has been traced through its relevant source, controls, and sink, and `security-review.json` is a valid JSON array with evidence for every finding.
