---
name: self-critique-verification
description: Mandatory self-auditing rubric to catch hallucinations, unverified numbers, code syntax discrepancies, and logical gaps before returning final answers.
license: MIT
---

# Self-Critique & Verification Rubric

Every agent output must pass this internal audit checklist before submission. If any check fails, the model must revise its response immediately.

## Pre-Response Verification Protocol

Before finalizing any response, execute this 5-point adversarial self-check:

### 1. The Fact & Citation Check (Anti-Hallucination)
- [ ] Did I cite any specific benchmark number, latency measurement, or percentage?
  - **Rule**: If YES, does each number have an identifiable citation (`[Author, Year, arXiv/DOI/PMID]`)?
  - **Rule**: If a number cannot be verified against a source, replace it with an explicit parameter placeholder or mark it `[Estimated - pending empirical validation]`.
- [ ] Are all paper titles and authors actual published works, rather than synthetic or amalgamated titles?

### 2. Code & Implementation Sanity Check
- [ ] Do tensor dimensions match across all matrix multiplications?
- [ ] Are all imports declared and verified to exist in the target package environment?
- [ ] Is there any incomplete pseudo-code or placeholder like `# TODO: implement this`?
  - **Rule**: Every code block must be fully copy-paste executable.

### 3. Instruction & Requirement Audit
- [ ] Re-read the initial user prompt word for word.
- [ ] Did I answer the exact question asked, or did I drift into adjacent generalities?
- [ ] Are all explicit constraints (e.g., zero cost, specific template, file paths) satisfied?

### 4. Adversarial Red Teaming
- [ ] Imagine a hostile reviewer reading this output:
  - What is the weakest claim made?
  - What assumption could be completely false in production?
- [ ] Add explicit caveats, failure modes, or boundary condition disclosures for any identified vulnerabilities.

### 5. Final Output Actionability Gate
- [ ] Can a junior engineer or an automated runner take this output and execute without confusion?
- [ ] Are paths absolute or unambiguously relative to workspace root?
