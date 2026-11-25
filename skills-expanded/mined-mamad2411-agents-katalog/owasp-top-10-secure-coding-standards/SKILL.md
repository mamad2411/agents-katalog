---
name: owasp-top-10-secure-coding-standards
description: >
  Guides understanding the OWASP Top 10 web application security risk
  categories, applying secure coding practices that prevent each category,
  and mapping which categories automated SAST/DAST tooling can and cannot
  reliably detect. Use when a user asks to "explain the OWASP Top 10",
  "review this code against OWASP standards", "why didn't our scanner
  catch this vulnerability", "add secure coding guidelines for [injection /
  broken access control / etc.]", "map OWASP categories to our SAST/DAST
  tool rules", or "figure out what our scanning stack is missing". Distinct
  from the sast-integration and dast-integration skills, which cover tool
  setup and pipeline mechanics — this skill focuses on the security
  categories themselves and their coverage boundaries, including
  business-logic flaws no automated scanner reliably finds.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: standards-and-compliance-frameworks
  maturity: stable
---

# OWASP Top 10 Secure Coding Standards

## Purpose

The OWASP Top 10 is a periodically updated (most recently 2021, with the
next major revision expected on OWASP's normal multi-year cadence) awareness
document ranking the most critical web application security risk
categories, based on real-world incidence and exploitability/impact data
contributed by the security community. It is not itself a testing
methodology or a checklist that guarantees secure code — it is a shared
vocabulary for categories of things that go wrong. This skill guides
applying secure coding practices that address each category during
development, and — the part teams most often get wrong — understanding
precisely which categories automated SAST (static analysis) and DAST
(dynamic/runtime analysis) tooling can reliably detect versus which ones
(most notably broken access control and business-logic flaws) require human
threat-modeling and testing because no scanner can infer intended
application behavior from code or traffic alone. A codebase that is "clean"
per SAST/DAST scan results has had certain risk categories tested, not all
ten, and definitely not custom business-logic abuse.

## When to use

- A user asks to explain or apply the OWASP Top 10 to a specific
  codebase, PR, or design.
- Reviewing code or a design for a specific risk category (e.g. "check
  this endpoint for broken access control" or "does this query have an
  injection risk").
- Investigating why an automated scanner (SAST/DAST) did not catch a
  vulnerability that was later found in review, pentest, or production —
  most often because the flaw is in a category tooling structurally
  cannot detect (e.g. an authorization check that's syntactically present
  but logically wrong).
- Building or updating secure-coding guidelines/training material for a
  team.
- Deciding what additional coverage (manual code review, threat modeling,
  pentest) is needed beyond existing SAST/DAST scanning.
- Triaging a SAST or DAST finding and needing to know which OWASP
  category it maps to and how confident the tool can realistically be for
  that category.

## Prerequisites & environment

- Familiarity with the application's architecture, authentication/
  authorization model, and data flows — several OWASP Top 10 categories
  (especially broken access control) can only be meaningfully assessed
  with knowledge of intended behavior, not just code patterns.
- Existing or planned SAST tooling (see
  [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md))
  and DAST tooling (see
  [dast-integration](../../../devsecops/skills/dast-integration/SKILL.md))
  — this skill assumes those pipelines exist or are being built, and
  focuses on what categories they cover.
- Know which OWASP Top 10 edition is the reference — category names and
  numbering changed meaningfully between the 2017 and 2021 editions (e.g.
  "Broken Access Control" moved to #1 in 2021; "Insecure Deserialization"
  was folded into a broader "Software and Data Integrity Failures"
  category; "Server-Side Request Forgery (SSRF)" was added as its own
  category in 2021). Cite the edition explicitly when referencing a
  category number.
- Understand the categories are **not** a complete application security
  program by themselves — OWASP also publishes the more exhaustive
  Application Security Verification Standard (ASVS) and the OWASP Testing
  Guide for teams that need deeper coverage than the Top 10's
  awareness-level framing.

## Step-by-step guidance

1. **Identify which OWASP Top 10 edition applies** (2021 is current as of
   this writing) and use its category list and numbering consistently in
   any findings or guidelines produced.
2. **For a code/design review, walk each relevant category deliberately**
   rather than relying purely on intuition — the "Common pitfalls" section
   below covers why intuition-only review under-indexes on categories
   like broken access control and SSRF.
3. **Apply the category-specific secure coding practice** (see the table
   below) at the point of writing or reviewing code — e.g. parameterized
   queries for injection, centralized authorization middleware checked
   per-request for access control, rather than ad hoc per-endpoint logic.
4. **Map any SAST/DAST finding to its OWASP category** before triaging
   severity — this contextualizes the finding for developers who know
   OWASP category names better than a tool's internal rule ID.
5. **Identify coverage gaps deliberately**: for categories where
   automated tooling is weak (broken access control, business-logic
   abuse, some SSRF variants, insecure design), schedule manual code
   review, threat modeling, or a targeted pentest rather than assuming
   "the scanner would have caught it."
6. **Track category coverage over time**, not just finding count — a
   dashboard showing "0 open findings" from a scanner that only exercises
   3 of the 10 categories well is misleading; report coverage per
   category, including "not automatable — covered by manual review on
   [cadence]."
7. **Feed confirmed findings back into secure coding guidelines and
   linter/SAST custom rules** where the pattern is codifiable (e.g. a
   custom Semgrep rule for a recurring injection pattern specific to the
   codebase), closing the loop between finding and prevention.
8. **Where this feeds compliance work**, note that OWASP Top 10 coverage
   is commonly cited as supporting evidence for PCI-DSS Requirement 6
   (secure application development) and NIST CSF `PR.PS`/`ID.RA` — see
   [security-compliance-mapping-soc2-iso-pci-nist](../security-compliance-mapping-soc2-iso-pci-nist/SKILL.md)
   for how to represent that mapping accurately, without overclaiming that
   OWASP alignment alone satisfies a framework requirement.

## Best practices

- Treat category numbering as edition-specific and say so — "A01:2021"
  is meaningfully different from a 2017-era "A1" reference; mixing them
  in the same document confuses readers and undermines precision.
- Push authorization checks into a single, centrally-reviewed layer
  (middleware, policy engine, framework-level guard) rather than
  scattering per-endpoint `if user.role == ...` checks — broken access
  control is consistently the most commonly reported category and the
  hardest for tooling to catch because the "correct" answer is
  business-specific.
- Parameterize all data-layer queries and use framework-provided
  escaping for output contexts (HTML, SQL, shell, LDAP, XML) rather than
  hand-rolled sanitization — most injection-category findings are
  eliminated structurally this way, not by review discipline alone.
- Don't rely on a single tool type: SAST catches code-pattern issues at
  rest, DAST catches runtime/request-response issues, and neither
  reliably validates that an authorization decision is *correct* for the
  business — combine both plus targeted manual review/pentest for
  categories where tooling is weak.
- Version and pin dependencies with SCA scanning as part of addressing
  "Vulnerable and Outdated Components" — this category overlaps with
  supply-chain practices; don't treat it as covered just because SAST/DAST
  ran, since neither typically inventories third-party library versions
  as their primary job.
- Log security-relevant events (auth failures, access-control denials,
  input validation failures) with enough detail to support both
  detection and later forensic/audit needs — this addresses "Security
  Logging and Monitoring Failures" directly and is also evidence
  commonly requested for SOC 2/ISO 27001/PCI-DSS log-monitoring criteria.
- Revisit the guideline set when OWASP publishes a new Top 10 edition —
  category boundaries shift (e.g. deserialization getting folded into
  "Software and Data Integrity Failures" in 2021) and a stale reference
  can miss newly emphasized risk (e.g. SSRF's addition as its own category
  in 2021 reflecting real-world incidence growth).

## Common pitfalls

- **Symptom:** The team reports "zero OWASP Top 10 findings" based purely
  on SAST/DAST scan results, and treats the application as broadly secure.
  **Fix:** Explicitly state which categories the scanning stack actually
  covers well (typically injection, some cryptographic failures, known-
  vulnerable components, some misconfiguration) versus which it
  structurally cannot (broken access control logic errors,
  business-logic abuse, most insecure-design issues) — "zero findings"
  from automated tooling is a claim about tooling coverage, not about the
  whole Top 10.
- **Symptom:** A business-logic flaw — e.g. a checkout flow that lets a
  user apply the same discount code unlimited times, or an API that lets
  User A cancel User B's order by guessing an ID — ships to production
  because no SAST/DAST finding flagged it, and the team is surprised.
  **Fix:** These are Broken Access Control / Insecure Design category
  issues that require a human who understands intended business rules to
  find — schedule manual review or targeted abuse-case testing for
  authorization and business-logic flows specifically; do not expect
  automated tooling to infer "should User A be able to do this."
- **Symptom:** A DAST scan is run against a staging environment seeded
  with a single admin-level test account, so authorization-boundary
  issues (a low-privilege user accessing an admin endpoint) never surface
  because the scanner only ever tests as one user.
  **Fix:** Configure DAST (and manual testing) with multiple accounts at
  different privilege levels and explicitly test cross-account/cross-role
  access, which is where most real broken-access-control vulnerabilities
  live.
- **Symptom:** A recurring injection-pattern finding is fixed one occurrence
  at a time in code review, but the same pattern keeps reappearing in new
  PRs because there's no systemic prevention.
  **Fix:** Once a pattern recurs, encode it as a custom SAST rule (e.g. a
  Semgrep rule matching the specific unsafe API usage) so it's caught
  automatically going forward instead of relying on reviewer memory each
  time.
- **Symptom:** Security logging exists but only captures generic
  "request completed" entries with no distinction between successful and
  failed authentication/authorization attempts, so an actual attack
  pattern (repeated 403s from one account) goes unnoticed until a much
  later manual investigation.
  **Fix:** Log security-relevant *outcomes* explicitly (auth success/
  failure, access-control denial with the resource and requesting
  identity, input-validation rejection) and alert on anomalous patterns —
  this is the actual intent of the "Security Logging and Monitoring
  Failures" category, not just having logs at all.

## Worked example

Illustrative mapping of OWASP Top 10 (2021 edition) categories to secure
coding practice and typical SAST/DAST tooling coverage:

| OWASP Top 10 (2021) category | Secure coding practice | Typical SAST rule type | Typical DAST coverage | Tooling coverage confidence |
|---|---|---|---|---|
| A01: Broken Access Control | Centralized authorization layer; deny-by-default; per-object ownership checks | Rare/limited — some rules flag missing auth decorators/annotations | Can find some role-based bypass if scanner is configured with multiple privilege-level accounts | **Low** — mostly requires manual review/threat modeling |
| A02: Cryptographic Failures | Use vetted libraries; enforce TLS 1.2+; never roll custom crypto; proper key management (see [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md)) | Rules for weak algorithms (MD5/SHA1 for security use), hardcoded keys, disabled cert validation | Can detect weak TLS config, missing HSTS | **Medium-High** for known-bad patterns |
| A03: Injection (SQL, NoSQL, OS command, LDAP) | Parameterized queries/prepared statements; framework-level output encoding; input allow-listing | Strong — taint-tracking rules for unsanitized input reaching a sink | Strong — active injection payloads against forms/params | **High** |
| A04: Insecure Design | Threat modeling during design; abuse-case test cases; secure design patterns/reference architectures | Very limited — SAST reviews code, not design intent | Very limited | **Low** — inherently a design/review-time activity |
| A05: Security Misconfiguration | Hardened default configs (see [container-image-hardening](../../../devsecops/skills/container-image-hardening/SKILL.md), [cis-benchmarks-hardening](../cis-benchmarks-hardening/SKILL.md)); no default credentials; minimal error verbosity in prod | Some — IaC/config scanning rules | Can detect verbose error messages, exposed debug endpoints, default credentials | **Medium** |
| A06: Vulnerable and Outdated Components | Dependency pinning, SCA scanning, patch SLAs (see [supply-chain-security-slsa-sbom](../../../devsecops/skills/supply-chain-security-slsa-sbom/SKILL.md)) | N/A for SAST proper — this is SCA's job, often bundled alongside SAST tools | Can sometimes fingerprint outdated library versions from responses | **High**, but only if SCA is actually running — not a SAST/DAST-native category |
| A07: Identification and Authentication Failures | Strong password/session policy, MFA, secure session token generation, rate-limit login attempts | Some rules for weak session config, missing lockout | Can test for credential stuffing resistance, session fixation, missing rate limiting | **Medium** |
| A08: Software and Data Integrity Failures | Verify signatures/checksums on dependencies and CI artifacts, avoid insecure deserialization of untrusted data | Rules for unsafe deserialization APIs | Limited — mostly a build/supply-chain-time concern | **Medium** for deserialization patterns, **Low** for CI/CD integrity overall |
| A09: Security Logging and Monitoring Failures | Log auth/authz outcomes with identity + resource; centralize logs; alert on anomalies | Rare — not typically a code-pattern SAST checks well | Can sometimes detect absence of logging indirectly (e.g. no lockout after repeated failures) | **Low** — mostly a design/ops verification |
| A10: Server-Side Request Forgery (SSRF) | Allow-list outbound destinations; disable unnecessary URL-fetching features; validate/normalize user-supplied URLs before use | Some rules for unsanitized URL passed to HTTP client | Can actively probe for SSRF via out-of-band callback payloads | **Medium** |

Illustrative finding triage using the table: a DAST scan flags "session
token does not expire after logout" — mapped to **A07: Identification and
Authentication Failures**. Because this category is only medium-confidence
for automated tooling, the team additionally schedules a manual review of
the session-invalidation logic (not just the single flagged endpoint) rather
than closing the finding once the one instance is patched.

Illustrative coverage summary reported alongside a "0 open SAST/DAST
findings" dashboard: "Automated tooling provides high-confidence coverage
for A03 (Injection) and A06 (Vulnerable Components); medium confidence for
A02, A05, A07, A10; low confidence for A01 (Broken Access Control), A04
(Insecure Design), and A09 (Logging/Monitoring) — these three are covered
instead by quarterly manual authorization review and design-time threat
modeling, tracked separately in `<REVIEW_TRACKER_PLACEHOLDER>`."

## Cross-references

- [security-compliance-mapping-soc2-iso-pci-nist](../security-compliance-mapping-soc2-iso-pci-nist/SKILL.md) — mapping OWASP-aligned secure coding evidence to PCI-DSS Requirement 6 and NIST CSF, without overclaiming certification.
- [cloud-well-architected-framework-review](../cloud-well-architected-framework-review/SKILL.md) — where application-layer OWASP findings roll up into a workload's broader security-pillar review.
- [cis-benchmarks-hardening](../cis-benchmarks-hardening/SKILL.md) — infrastructure/platform-level hardening that complements application-layer OWASP practices (e.g. A05 Security Misconfiguration at the host/container level).
- [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md) — tool setup, tuning, and triage mechanics for static analysis referenced throughout this skill's coverage table.
- [dast-integration](../../../devsecops/skills/dast-integration/SKILL.md) — tool setup and pipeline mechanics for dynamic scanning referenced throughout this skill's coverage table.
- [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md) — key/credential handling underlying A02 (Cryptographic Failures) prevention.
- [supply-chain-security-slsa-sbom](../../../devsecops/skills/supply-chain-security-slsa-sbom/SKILL.md) — SBOM/provenance practices underlying A06 and A08 prevention.
- [container-image-hardening](../../../devsecops/skills/container-image-hardening/SKILL.md) — hardened defaults underlying A05 (Security Misconfiguration) prevention at the container level.
