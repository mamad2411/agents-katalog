---
name: "mule-build-error-triage"
description: "Diagnose and fix MuleSoft/Maven build failures: mule-maven-plugin config, dependency/connector versions, secure-properties key, MUnit failures, runtime BOM. Use when a Mule build fails."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# Mule Build Error Triage

## Triage order
1. **Toolchain:** JDK 17, Maven present; `mule-maven-plugin` and Mule runtime BOM versions resolve (check `mule-artifact.json` minMuleVersion).
2. **Dependencies/connectors:** missing connector (e.g. HTTP) -> add dependency; version conflicts -> align via parent/BOM.
3. **Secure properties:** decryption fails -> the runtime key (`-M-Dmule.key` / `${runtime.property}`) is missing/wrong.
4. **Properties:** missing `${...}` placeholder -> add to `<env>-properties.yaml`/shared.
5. **MUnit failures:** read the assertion; fix flow or mock (see munit-test-stabilization).
6. **Packaging:** `mvn clean package` errors -> check `packaging=mule-application` + plugin config.

Fix the smallest failing slice; re-run `mvn clean verify`. Never disable tests to pass.
