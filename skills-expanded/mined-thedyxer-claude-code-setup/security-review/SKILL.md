---
name: security-review
description: Review code for exploitable security flaws when the user requests a security assessment or changes authentication, authorization, secrets, untrusted input, or sensitive data flows.
---

# Security review

Identify assets, trust boundaries, entry points, and privileges relevant to the requested area. Trace untrusted data through validation, authorization, storage, and output. Check concrete paths for injection, access control bypass, secret exposure, unsafe file or network access, and insecure defaults. Verify a finding against the code and, where practical, a safe local reproduction.

Report only actionable findings with file locations, exploit preconditions, impact, and a targeted fix. Separate confirmed findings from hypotheses. Do not claim a full audit from a partial review. For a requested fix, make the smallest effective change and verify the original exploit path and normal behavior.
