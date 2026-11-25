---
name: security-validate
description: "Verify OWASP ASVS 5.0.0 security assessment coverage, retest vulnerability fixes and reconcile code, scan and manual evidence. Use after security changes or when checking application audit completeness."
---

# Validate an application security remediation and assessment evidence

## Scope

Use for post-change security verification or checking an ASVS evidence ledger. Structural coverage checks do not establish that controls actually work. Keep the review limited to explicitly authorized systems and tools.

## Procedure

1. Resolve target ASVS 5.0.0 level and assessment boundary using `../security-diagnose/references/standard-selection.md`; distinguish frontend evidence from server, identity or deployment evidence.
2. Check every selected ASVS requirement against `../security-diagnose/references/asvs/5.0.0/index.json`; confirm full official requirement meaning through `../security-diagnose/references/asvs/5.0.0/source-access.md` and record pass/fail, not applicable, not tested, and needs-manual-verification outcomes. Do not treat unavailable requirement text as a pass.
3. Use existing independent SAST, SCA, secret-scanning, configuration and authorized dynamic/manual tests for the changed failure modes. Pin tool versions, save invocation scope, methods and reproducible evidence.
4. Test negative and abuse cases as well as normal operation; verify remediation did not regress expected authentication, tenancy isolation, data safety or availability.
5. Use distribution-side `scripts/check_security_audit.py` for structural completeness when accessible; otherwise validate by the bundled index and report gaps. Do not claim security certification or completed penetration testing.

## Outcomes

Distinguish report format valid, coverage complete, requirements actually verified and any independent assurance or signoff. All are different states. Missing evidence is neither success nor failure; report it as unknown and follow the consuming organization’s policy.
