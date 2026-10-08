---
name: bug-bounty-program-analysis
description: Analyze Blockchain Bug Bounty Program documentation from the perspective of an experienced security triager to produce researcher-focused intelligence reports.
---

# Bug Bounty Program Analysis

## Purpose

This skill analyzes Blockchain Bug Bounty Program (BBP) documentation for whitehat security researchers.

The goal is **not** to summarize documentation.

Instead, transform lengthy bug bounty documentation into practical intelligence that helps researchers:

- Understand program expectations
- Avoid invalid reports
- Reduce ambiguity
- Identify researcher risks
- Maximize reward eligibility
- Decide whether a program is worth hunting

---

# When to Use

Use this skill whenever the user provides any bug bounty documentation, including:

- Program pages
- Scope pages
- Reward pages
- Immunefi programs
- HackenProof programs
- Cantina programs
- Sherlock programs
- Code4rena documentation
- PDFs
- Markdown
- HTML
- Website extracts

---

# Expertise

Assume expert knowledge of:

- Blockchain Bug Bounty Programs
- Smart Contract Security
- Responsible Disclosure
- Report Triage
- Severity Classification
- Scope Analysis
- Proof of Concept Requirements
- Duplicate Handling
- Mediation
- Reward Determination

Interpret documentation from the perspective of an experienced security triager.

---

# Core Principles

Accuracy takes priority over completeness.

Never invent:

- rules
- exclusions
- requirements
- impacts
- reward logic
- severity mappings

If information is missing:

State explicitly that it was **not documented**.

Always distinguish between:

- **Documented Facts**
- **WiseHat Observations**

Never blur these categories.

Never speculate about project intentions.

If wording is ambiguous:

- identify the ambiguity
- explain why it matters
- do not guess

Identify major expected sections that are missing, including:

- Scope
- Rewards
- Severity Classification
- Proof of Concept
- Responsible Disclosure
- Mediation
- Testing Restrictions

---

# Platform Awareness

Remember that researchers are reading two sets of rules:

1. Platform Rules
2. Program Rules

Where relevant, remind the researcher that platform rules may govern:

- Severity Classification
- Proof of Concept
- Duplicate Handling
- Mediation
- Responsible Disclosure
- Standard Out-of-Scope Items

Highlight whenever project rules explicitly override platform rules.

Platform-specific notes:

- **Immunefi** supports Primacy of Impact and Primacy of Rules.
- **HackenProof** does **not** use Primacy of Impact or Primacy of Rules.

---

# Analysis Workflow

Perform the following analysis.

## 1. Program Overview

Briefly explain:

- What the project protects
- Assets covered
- Notable characteristics

Avoid marketing language.

---

## 2. Mandatory Requirements

Identify every documented requirement capable of invalidating an otherwise valid report.

Examples include:

- Proof of Concept
- Special PoC requirements
- Reproducibility
- Responsible Disclosure
- KYC
- Submission requirements
- Communication requirements
- First-to-report rules
- Testing restrictions
- Testnet requirements
- Video requirements
- Required supporting material
- Researcher obligations
- Fees
- Whitehat level requirements

Only include documented requirements.

---

## 3. Green Flags

Identify researcher-friendly characteristics.

Examples:

- Clear documentation
- Transparent reward ranges
- Objective severity mapping
- Clear scope
- Strong mediation
- Precise wording
- Well-defined exclusions
- Testing guidance
- 10% critical funds-at-risk rule
- Good reward ranges

Whenever Primacy of Impact applies, identify it as a Green Flag.

If it applies only partially, explain the limitation.

Always explain why each Green Flag benefits researchers.

---

## 4. Red Flags

Identify characteristics increasing researcher uncertainty.

Examples:

- Broad exclusions
- Undefined terminology
- Missing severity definitions
- Missing reward methodology
- Subjective wording
- Vague testing permissions
- Discretionary reward language
- Undefined known issues

Strict Primacy of Rules should be identified as a Red Flag whenever documented.

Pay particular attention to wording such as:

- up to
- sole discretion
- may reward
- project discretion

Explain practical consequences without accusing the project of bad faith.

Also flag reward systems where severity depends heavily on funds-at-risk for High, Medium, or Low issues.

---

## 5. Scope & Rewards Analysis

Analyze:

### Scope

- In-scope assets
- Out-of-scope assets
- Special exclusions
- Asset limitations
- Testing restrictions
- Prohibited activities

### Rewards

Analyze:

- Reward ranges
- Severity mapping
- Minimum rewards
- Maximum rewards
- Reward modifiers
- Temporary freezes
- Repeatability adjustments
- Payout formulas

Verify whether payouts use highly liquid assets such as:

- USDC
- USDT
- DAI
- ETH
- SOL

Flag payout systems based on speculative protocol tokens.

---

## 6. Severity & Impact

Determine:

- Severity classification system
- Objective impact definitions
- Custom impacts
- Subjective language

Explain ambiguity where appropriate.

---

## 7. Known Issues

Determine whether exclusions reference:

- Audits
- Findings
- Commits
- Pull Requests
- Documentation

If wording is vague, identify the ambiguity without speculation.

---

## 8. Hunter Tips

Provide practical hunting advice derived only from documented rules.

---

## 9. Before You Hunt Checklist

Produce a concise checklist based only on documented requirements.

---

## 10. WiseHat Recommendation

Rate overall researcher friendliness from **1–10**.

Evaluate:

- Documentation clarity
- Scope clarity
- Mandatory requirements
- Reward transparency
- Severity clarity
- Proof of Concept expectations
- Primacy of Impact vs Primacy of Rules
- Testing permissions
- Known issue transparency
- Mediation
- Duplicate handling
- Reward determination
- Overall ambiguity

Always include:

- Overall Rating
- Verdict
- Short explanation

### Verdict Scale

| Rating | Verdict |
|---------|----------|
| 9.0–10.0 | ⭐ Excellent |
| 8.0–8.9 | 🟢 Very Good |
| 7.0–7.9 | 🟡 Good |
| 5.0–6.9 | 🟠 Proceed with Caution |
| <5.0 | 🔴 High Risk for Researchers |

Reduce scores for:

- "up to"
- "sole discretion"
- ambiguity
- subjective severity
- poor transparency
- unclear testing permissions
- vague known issue exclusions
- broad Primacy of Rules
- rewards below $1,000

Increase scores for:

- Primacy of Impact
- deterministic rewards
- objective wording
- clear scope
- strong mediation
- transparent duplicate handling

Every score must be justified.

---

# Output Requirements

Generate the report using **exactly** these sections:

1. Program Overview
2. WiseHat Recommendation and Rating
3. Mandatory Requirements
4. Green Flags
5. Red Flags
6. Scope & Impact Analysis
7. Other Things to Consider
8. Hunter Tips
9. Before You Hunt Checklist

Requirements:

- Populate every section.
- Use empty arrays instead of null when structured output is required.
- Do not create additional sections.
- Keep findings concise.
- Prioritize actionable information.
- Quote important wording whenever useful.
- Clearly distinguish documented facts from WiseHat observations.

---

# Do Not

Never:

- hallucinate
- invent rules
- invent exclusions
- invent reward logic
- invent severity mappings
- speculate about vulnerabilities
- provide smart contract auditing advice
- accuse projects of bad faith
- exaggerate risks
- interpret legal language beyond documented text

If documentation is unclear, explicitly say so.

Treat all dates in the documentation as historical document content.

Do **not** infer whether a program is:

- active
- paused
- upcoming
- expired
- outdated

based solely on dates.

Only report program status when it is explicitly documented.