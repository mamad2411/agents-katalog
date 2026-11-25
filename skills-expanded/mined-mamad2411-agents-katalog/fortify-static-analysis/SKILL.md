---
name: fortify-static-analysis
description: >
  Guides deep, tool-specific use of OpenText (formerly Micro Focus)
  Fortify Static Code Analyzer (SCA) and Fortify Audit Workbench for
  enterprise, on-premises static analysis — the translate/scan build
  workflow, Fortify Security Rulepacks, audit workbench triage (Not an
  Issue / Reliability / Suspicious), and how Fortify's on-prem,
  build-integrated model differs operationally from cloud-native SAST.
  Use when the user asks to "run a Fortify scan", "configure sourceanalyzer
  for a build", "triage findings in Fortify Audit Workbench", "integrate
  Fortify with Jenkins/Azure DevOps", "reduce Fortify SCA false positives",
  or "compare Fortify against SonarQube/Semgrep for enterprise
  compliance". Fortify-specific depth on the translate/scan model and
  enterprise workflow; for the general SAST concept see sast-integration
  in the devsecops domain.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# Fortify Static Analysis

## Purpose

Fortify Static Code Analyzer (SCA) is an enterprise, historically
on-premises-first SAST engine built around a two-phase model — a
**translate** phase that parses source into an intermediate
representation matching the target language's actual build (not just a
text/regex scan), and a **scan** phase that runs deep interprocedural
dataflow and control-flow analysis against that representation using
vendor-maintained Security Rulepacks. This buys genuinely deep
taint-tracking (following untrusted input across function and even
file boundaries) at the cost of needing to mirror the real build
process closely, materially slower scans than a lightweight pattern
matcher, and an audit workflow (Fortify Audit Workbench, or its
web-based counterpart in Fortify Software Security Center/SSC) built
around human triage of findings into confirmed categories rather than a
lightweight suppress-and-move-on model. Organizations reach for Fortify
specifically for compliance-driven and regulated environments (defense,
finance, government) where an auditable, enterprise-supported on-prem
tool with a mature audit trail is a requirement, not just a preference
— understanding that trade-off is the core of using it well.

## When to use

- The user asks to "run a Fortify scan" or configure the
  `sourceanalyzer` translate/scan build steps for a project.
- The user needs to integrate Fortify into Jenkins, Azure DevOps, or
  another enterprise CI system, uploading results to Fortify Software
  Security Center (SSC) for centralized tracking.
- The user is triaging findings in Fortify Audit Workbench and needs to
  understand the difference between marking something "Not an Issue,"
  "Reliability Issue," "Bad Practice," or a confirmed "Suspicious"/
  "Exploitable" vulnerability.
- The user's Fortify translate phase fails or produces incomplete
  results for a compiled-language project (Java, C/C++, .NET) and needs
  the build to be mirrored more faithfully.
- The user is comparing Fortify against a cloud-native SAST tool
  (Semgrep, SonarQube, CodeQL) for a regulated or on-premises-mandated
  environment, and needs the concrete operational differences (not just
  a feature checklist).
- The user needs to justify or track compliance evidence (e.g. for an
  audit) that static analysis was run and findings were triaged by a
  human, which Fortify's audit workflow is specifically built to
  produce.

## Prerequisites & environment

- Fortify Static Code Analyzer license and installation (on-premises
  server or, more recently, Fortify on Demand/ScanCentral for
  cloud-hosted scanning of the same engine) — current major versions
  are commonly referred to by year-based releases; confirm the
  installed `sourceanalyzer -version` against your organization's
  supported version before assuming CLI flag compatibility across
  versions.
- A build environment that can actually compile the target project —
  Fortify's translate phase for compiled languages (Java, C/C++, .NET)
  needs to observe a real build (or a close proxy of one) to resolve
  types and build accurate dataflow; interpreted languages (JavaScript,
  Python) translate more directly from source without a compile step.
- Fortify Audit Workbench (desktop) or Fortify Software Security Center
  (SSC, the server-based centralized results/triage/reporting
  platform) for reviewing scan results — a raw `.fpr` (Fortify Project
  Results) file is not intended to be read directly.
- Current Fortify Security Rulepacks (vendor-updated rule content,
  analogous to a SAST tool's ruleset) — kept current via Fortify's
  update mechanism (`fortifyupdate` or equivalent), since stale
  rulepacks miss newer vulnerability patterns and language/framework
  versions.
- CI/CD integration plugin matching the platform (Fortify Jenkins
  plugin, Azure DevOps extension, or a generic CLI invocation) and a
  service account/token with permission to publish results to SSC.
- Enough build-time budget: a full translate+scan on a large monorepo
  is measured in tens of minutes to hours, not seconds — plan CI
  scheduling accordingly (see Common pitfalls).

## Step-by-step guidance

1. **Clean any prior build artifacts**, then run the **translate**
   phase, mirroring the real build as closely as possible:
   ```bash
   # Java (Maven) example
   sourceanalyzer -b checkout-service -clean
   sourceanalyzer -b checkout-service mvn -f pom.xml clean compile
   ```
   For C/C++, translate must wrap the actual compiler invocation so
   Fortify observes real preprocessor/include behavior:
   ```bash
   sourceanalyzer -b checkout-native -clean
   sourceanalyzer -b checkout-native gcc -c src/*.c -Iinclude
   ```
   For .NET:
   ```bash
   sourceanalyzer -b checkout-service -clean
   sourceanalyzer -b checkout-service msbuild CheckoutService.sln /t:rebuild
   ```

2. **Run the scan phase**, producing an `.fpr` results file:
   ```bash
   sourceanalyzer -b checkout-service -scan -f checkout-service.fpr
   ```

3. **Upload results to Fortify Software Security Center (SSC)** for
   centralized triage and trend tracking rather than emailing `.fpr`
   files around:
   ```bash
   fortifyclient uploadFPR \
     -file checkout-service.fpr \
     -application "checkout-service" \
     -applicationVersion "main" \
     -url https://<fortify-ssc-host>/ssc \
     -authtoken "${FORTIFY_SSC_TOKEN}"
   ```

4. **Wire translate/scan/upload into CI** (Jenkins declarative example;
   Azure DevOps uses the equivalent extension tasks):
   ```groovy
   pipeline {
     agent any
     stages {
       stage('Fortify Translate') {
         steps {
           sh 'sourceanalyzer -b checkout-service -clean'
           sh 'sourceanalyzer -b checkout-service mvn -f pom.xml clean compile'
         }
       }
       stage('Fortify Scan') {
         steps {
           sh 'sourceanalyzer -b checkout-service -scan -f checkout-service.fpr'
         }
       }
       stage('Publish to SSC') {
         steps {
           sh '''
             fortifyclient uploadFPR -file checkout-service.fpr \
               -application "checkout-service" -applicationVersion "main" \
               -url $FORTIFY_SSC_URL -authtoken $FORTIFY_SSC_TOKEN
           '''
         }
       }
     }
   }
   ```

5. **Triage in Fortify Audit Workbench (or SSC's web audit view)**,
   using Fortify's specific triage taxonomy rather than a generic
   "dismiss" action:
   - **Exploitable** — confirmed real vulnerability; track to fix.
   - **Suspicious** — likely real but needs further investigation
     before confirming.
   - **Not an Issue** — analyzed and determined to be a false positive
     or non-exploitable in context; requires a rationale comment.
   - **Bad Practice / Reliability Issue** — a real code-quality concern
     but not a security vulnerability per se.
   Every non-"Exploitable" triage decision should carry a short audit
   comment — this triage history is itself often the compliance
   artifact an audit is looking for, not just the final finding count.

6. **Tune Security Rulepacks and add custom rules** for
   organization-specific sinks/sources (e.g. an internal logging
   wrapper that should be treated as a sensitive-data sink) using
   Fortify's custom rule authoring (XML-based rule definitions) rather
   than accepting only vendor-shipped rule coverage.

7. **Set a build-breaker threshold** in CI based on triaged severity
   (Critical/High confirmed-Exploitable count), not raw finding count
   — Fortify's default output includes many Suspicious/Not-Yet-Audited
   findings that should not, by themselves, block a build before human
   triage has had a chance to run.

8. **Re-scan incrementally where supported** (Fortify's incremental
   analysis features vary by version and language) to keep scan time
   manageable on a large codebase — a full clean translate+scan on
   every commit is often impractical; consider a full scan on a nightly
   or release-gate cadence with a lighter/faster complementary tool
   (e.g. [sonarqube-code-quality-and-security](../sonarqube-code-quality-and-security/SKILL.md)
   or a Semgrep-based check per
   [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md))
   running on every PR for faster feedback.

## Best practices

- Mirror the real build exactly in the translate phase — a translate
  step that doesn't match the actual compiler/build tool invocation
  (wrong classpath, missing include paths, an incomplete Maven profile)
  silently produces an incomplete or misleading scan, not an error you'll
  necessarily notice.
- Budget for Fortify's audit workflow as a first-class, ongoing
  activity, not a one-time gate — its differentiator versus a
  lightweight SAST tool is the structured human-triage audit trail; a
  team that never triages just accumulates an ever-growing pile of
  Not-Yet-Audited findings with none of Fortify's actual value realized.
- Keep Security Rulepacks current on a defined update cadence — an
  enterprise on-prem install does not auto-update the way a SaaS SAST
  tool does, so stale rulepacks are a real and easy-to-miss risk.
- Reserve Fortify's full scan for a nightly/release-gate cadence on
  large codebases, and pair it with a fast, lightweight SAST tool for
  per-PR feedback — see
  [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md)
  for that faster-feedback pattern; Fortify's deep interprocedural
  analysis is not typically fast enough to be the only per-PR gate on a
  large monorepo.
- Treat Fortify's deep dataflow strength as complementary to, not a
  replacement for, breadth-oriented tools —
  [sonarqube-code-quality-and-security](../sonarqube-code-quality-and-security/SKILL.md)
  or a multi-language SAST tool often covers more ecosystems/frameworks
  out of the box with less setup, while Fortify goes deeper on the
  languages it fully supports.
- Never treat a clean Fortify scan as covering the whole security
  program — it is source-level static analysis only; pair it with
  [owasp-zap-dast-configuration](../owasp-zap-dast-configuration/SKILL.md)
  for runtime behavior and
  [trivy-vulnerability-scanning](../trivy-vulnerability-scanning/SKILL.md)
  for third-party dependency CVEs, neither of which Fortify SCA
  analyzes.

## Common pitfalls

- **Symptom:** The scan phase completes almost instantly and reports
  suspiciously few findings for a large codebase.
  **Fix:** The translate phase likely failed silently or only
  partially translated the codebase (a build error, missing
  dependency, or wrong working directory during translate). Check the
  translate log for errors/warnings and confirm the file count
  translated roughly matches the expected source tree size before
  trusting scan results — a broken translate produces a technically
  successful but nearly-empty scan, not an obvious failure.

- **Symptom:** Fortify Audit Workbench shows thousands of
  Not-Yet-Audited findings and the team's response is to bulk-suppress
  entire categories to make the number manageable.
  **Fix:** Bulk-suppressing a whole rule category discards genuine
  findings along with noise. Instead, prioritize triage by Fortify's
  built-in priority order (Critical/High confirmed first), triage in
  batches by rule category with a subject-matter reviewer for that
  category, and use custom rule tuning (step 6) to reduce a specific
  noisy rule's false-positive rate rather than disabling it outright.

- **Symptom:** CI pipeline time balloons after adding Fortify, with the
  translate+scan step taking 45+ minutes on every commit.
  **Fix:** Move the full translate+scan to a nightly or release-gate
  schedule instead of every commit, and use a faster, lighter SAST tool
  for per-PR feedback (see
  [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md)),
  reserving Fortify's deeper analysis for a cadence where its runtime
  cost is acceptable.

- **Symptom:** A finding marked "Not an Issue" during triage reappears
  as a new, separate finding after the next scan, forcing the same
  triage decision repeatedly.
  **Fix:** This typically happens when the underlying code location
  shifts enough (refactor, line-number drift) that Fortify's finding
  fingerprinting treats it as new rather than matching the previously
  audited instance — review triage decisions on a schedule after major
  refactors specifically, and confirm SSC's audit history is being
  carried forward correctly between scans rather than treating each
  `.fpr` upload as fully independent.

- **Symptom:** A C/C++ project's translate phase fails with missing
  header/include errors that don't occur in the normal build.
  **Fix:** The `sourceanalyzer` wrapper needs the identical include
  paths, defines, and compiler flags as the real build — confirm the
  translate command is invoked with the same environment/build wrapper
  (e.g. through the actual `make`/`cmake` invocation rather than a
  hand-simplified compile command) so Fortify observes exactly what the
  real compiler sees.

## Worked example

A financial-services team with an on-premises Java monorepo integrates
Fortify SCA into Jenkins with a nightly full scan and SSC-based audit
workflow, alongside a faster per-PR Semgrep gate for quick feedback.

Jenkinsfile (nightly full scan stage, abbreviated from step 4):
```groovy
stage('Fortify Full Scan (nightly)') {
  when { triggeredBy 'TimerTrigger' }
  steps {
    sh 'sourceanalyzer -b payments-core -clean'
    sh 'sourceanalyzer -b payments-core mvn -f pom.xml clean compile'
    sh 'sourceanalyzer -b payments-core -scan -f payments-core.fpr'
    sh '''
      fortifyclient uploadFPR -file payments-core.fpr \
        -application "payments-core" -applicationVersion "main" \
        -url $FORTIFY_SSC_URL -authtoken $FORTIFY_SSC_TOKEN
    '''
  }
}
```

Sample confirmed finding in SSC after audit:
```
Category: SQL Injection
Priority: Critical
Status: Exploitable (audited by: j.rivera, 2026-07-15)
File: src/main/java/com/example/payments/LedgerDao.java:112
Analyzer trace: HTTP Request Parameter "accountId" (Source)
  -> LedgerController.getBalance() line 44
  -> LedgerService.fetchLedger() line 61
  -> LedgerDao.rawQuery() line 112 (Sink: java.sql.Statement.executeQuery)
```
Remediation: replace `Statement` with a `PreparedStatement` and bind
`accountId` as a parameter; re-run the translate+scan and confirm the
finding transitions to "Fixed" in SSC's audit history rather than
reappearing as a new, separately-audited finding.

## Cross-references

- [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md) —
  the tool-agnostic SAST concept, and specifically the faster
  lightweight-scanner-for-PR-feedback pattern meant to pair with
  Fortify's slower, deeper full scans.
- [sonarqube-code-quality-and-security](../sonarqube-code-quality-and-security/SKILL.md) —
  a broader-coverage, faster, more cloud-native alternative worth
  running alongside Fortify rather than choosing exclusively one or the
  other in most enterprise stacks.
- [owasp-zap-dast-configuration](../owasp-zap-dast-configuration/SKILL.md) —
  runtime testing that catches issues no static analyzer, including
  Fortify, can see from source alone.
- [trivy-vulnerability-scanning](../trivy-vulnerability-scanning/SKILL.md) —
  covers third-party dependency and container CVEs, which Fortify SCA
  does not analyze (Fortify Software Composition Analysis is a separate
  product/module from Fortify SCA's static source analysis).
