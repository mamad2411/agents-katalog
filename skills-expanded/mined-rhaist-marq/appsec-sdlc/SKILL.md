---
name: appsec-sdlc
description: "Covers secure SDLC architecture: pipeline gates, SAST vs DAST vs IAST vs SCA (what each finds and misses, where), OWASP SAMM and ASVS, and software supply chain (SBOM, SLSA, signing). Use when the user asks which application-security testing to adopt, how to build a secure development lifecycle, how to measure AppSec maturity with SAMM, verify against ASVS, or secure third-party code and dependencies. (Rolling it out in CI/CD: devsecops.)"
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# AppSec & Secure SDLC

Application security is a property of the **pipeline**, not a scan at the end. Bugs get exponentially cheaper to fix the earlier you catch them, so the architecture goal is to **push each check to the leftmost point it can run** and gate there. The other half is the supply chain: most of your code is someone else's, so you must know _what_ you ship and _how_ it was built.

## Secure SDLC gates (shift-left, gate where it's cheapest)

One enforcing gate per phase. A gate that only warns is not a gate.

- **Design**: threat model the feature (`load_skill threat-modeling`). Output: security requirements + abuse cases. Cheapest fixes live here.
- **Code**: IDE/pre-commit linting, secret scanning, SAST on the diff. Fast feedback or developers route around it.
- **Build/CI**: SAST (full), SCA on dependencies, IaC scanning, **secret scanning**, generate SBOM + provenance. The primary enforcing gate.
- **Test/Staging**: DAST / IAST against a running build, integration-level auth tests.
- **Release**: sign artifacts, verify provenance, policy-as-code gate (block on critical + known-exploited).
- **Runtime/Prod**: WAF/RASP, ASPM correlation, feedback to the next threat model.

Rules: **gate on exploitable/known-exploited, not raw severity count**; a wall of low-confidence highs trains developers to ignore the gate. Make checks fast and low-false-positive at the left; tolerate slower, deeper checks further right. Break the build only on what you'll actually act on.

## SAST vs DAST vs IAST vs SCA: what each finds and misses

The four are complementary; none is sufficient alone. Match the tool to the bug class and the pipeline stage.

| Tool     | Sees                            | Stage          | Finds well                                                  | Misses / weakness                                                    |
| -------- | ------------------------------- | -------------- | ----------------------------------------------------------- | -------------------------------------------------------------------- |
| **SAST** | Source / bytecode (white-box)   | Code / CI      | Injection, XSS, insecure crypto, taint flows in _your_ code | Runtime/config/auth-logic bugs; **noisy, high false-positive**       |
| **SCA**  | Dependency manifests + graph    | Code / CI      | Known-CVE vuln deps, license risk, transitive pulls         | Zero-days; custom code; whether the vuln path is reachable           |
| **DAST** | Running app (black-box)         | Test / staging | Real exploitable runtime, auth, config, injection           | No code location; poor coverage of unreached paths; slow             |
| **IAST** | Running app + instrumented code | Test (in QA)   | Runtime bugs _with_ code location, low FP                   | Needs instrumentation + exercising the code (test coverage gates it) |

- **SAST** = breadth + early, pays in false positives. Tune ruthlessly or it gets ignored.
- **SCA** = mandatory; your dependencies are most of your attack surface. Prefer SCA that does **reachability** analysis (is the vulnerable function actually called?) to cut noise.
- **DAST** = truth (it actually exploits) but late and location-blind. The web-app pentest mirror (SQLi, XSS, SSRF).
- **IAST** = SAST accuracy + DAST realism, but only covers what your tests exercise.
- **ASPM** (Application Security Posture Management) sits _above_ these: it ingests SAST/DAST/SCA/IaC findings, dedupes, correlates with runtime/reachability, and surfaces only exploitable risk. It manages scanners, it is not a scanner. Reach for it when uncorrelated scanner noise is the bottleneck. (Cloud-infra analog: `load_skill cloud-security`.)

## OWASP SAMM & ASVS: maturity vs verification

Two OWASP standards, two different jobs. Use them together.

- **SAMM** (Software Assurance Maturity Model, **v2** current as of 2026, `https://owaspsamm.org`): measures **process maturity** of your AppSec _program_ across 5 business functions (Governance, Design, Implementation, Verification, Operations) / 15 practices, scored at maturity levels 1 to 3. Use it to assess and build the program roadmap (same Current→Target gap method as `load_skill gap-analysis`).
- **ASVS** (Application Security Verification Standard, **v5.0** current, May 2025: `https://owasp.org/www-project-application-security-verification-standard/`): a **verification checklist** of concrete security requirements across levels L1/L2/L3 (rising assurance). Use it as the requirement set you test _against_, which turns "is it secure" into a checkable list.
- Pairing: **SAMM tells you how good your process is; ASVS tells you whether a given app meets requirements.** SAMM for the program, ASVS per-application. Verify both versions are still current before citing.

## Software supply chain (you ship other people's code)

Two questions: **what's in it** (SBOM) and **how was it built / can I trust it** (provenance, SLSA, signing).

- **SBOM** (Software Bill of Materials): machine-readable inventory of every component + version + license (formats: **SPDX**, **CycloneDX**). Generate it in CI per build; it's what lets you answer "are we affected by CVE-X" in minutes, not weeks (the Log4Shell lesson). An SBOM you don't ingest/query is shelfware.
- **SLSA** (Supply-chain Levels for Software Artifacts, OpenSSF: `https://slsa.dev`; **v1.2** current, 2025): a graded framework for **build integrity + provenance**. Now split into a **Build track** (below) and a **Source track** (v1.2 promoted it from experimental to approved; grades version-control history integrity + enforced code review). Build track:
  - **L1**: produce provenance (releases traceable to how they were built).
  - **L2**: signed provenance on a hosted/protected build platform.
  - **L3**: hardened, isolated builds with non-falsifiable provenance and protected signing secrets.
  - Targets the "tampered build / poisoned pipeline" threat (SolarWinds class). Verify the spec level definitions are current.
- **Signing + verification**: sign artifacts and _verify on the consuming side_ (Sigstore/cosign for keyless signing; in-toto attestations). Signing you don't verify at deploy buys nothing: **enforce verification at the release gate.**
- **Dependency hygiene**: pin/lock versions, verify checksums, prefer an internal proxy/registry, watch for typosquats and dependency-confusion (internal-name packages must resolve internally first).

## Where to enforce

- The build/CI stage is the single highest-leverage enforcing gate: SAST, SCA, secret scan, SBOM, provenance all converge there.
- Verify signatures + provenance at the **release** gate, not at build (build can be tampered).
- Map AppSec findings to controls with `load_skill control-mapping` (CWE → ISO/NIST/CIS); feed unfixed risk to `load_skill risk-assessment`.
- Design-phase requirements come from `load_skill threat-modeling`: close the loop by turning threats into ASVS-style tested requirements.

## Rules

- Gate on exploitable/known-exploited, not severity counts: noise kills the gate's credibility.
- No single scanner is sufficient: SAST+SCA in CI, DAST/IAST in test, ASPM to correlate.
- An SBOM you can't query and a signature you don't verify are both theater.
- Tune SAST false positives aggressively; an ignored gate is worse than no gate.
