---
name: anti-hallucination-techniques
description: Use when verifying AI-generated content, validating claims, checking source credibility, implementing evidence-based reasoning, and preventing AI hallucinations. Includes source verification, fact-checking, and validation frameworks. Based on information verification best practices and AI safety guidelines.
license: MIT
---

# Anti-Hallucination Techniques Skill — Doc Researcher

## Overview

This skill provides comprehensive guidance for preventing and detecting AI hallucinations. It covers source verification, evidence-based reasoning, fact-checking techniques, and validation frameworks following information verification best practices and AI safety guidelines.

## When to Use

**Use this skill when:**

- Verifying AI-generated content accuracy
- Checking source credibility and citations
- Validating claims with evidence
- Implementing evidence-based reasoning
- Detecting and correcting hallucinations
- Fact-checking technical documentation
- Validating code examples
- Checking API documentation accuracy
- Verifying configuration examples
- Validating architectural diagrams
- Checking mathematical calculations
- Validating statistical claims
- Verifying historical facts
- Checking product specifications
- Validating legal or compliance information
- Checking financial data
- Verifying medical or health information
- Validating scientific claims
- Checking technical specifications
- Verifying geographic information
- Validating dates and times
- Checking names and proper nouns
- Validating contact information

**Do NOT use this skill when:**

- Writing application business logic (use domain-driven skill)
- Designing database schemas (use database-design skill)
- Writing API endpoint specifications (use api-design skill)
- Performing security audits (use security-auditor skill)
- Writing SQL queries (use sql-best-practices skill)
- Designing multi-page website layouts (use design-system skill)
- Analyzing deployment configurations (use deployment skill)
- Writing documentation (use documentation-best-practices skill)

## Hallucination Types

### Common Hallucination Patterns

```
┌─────────────────────────────────────────────────────────────┐
│              Hallucination Types                            │
├─────────────────────────────────────────────────────────────┤
│  1. Factual Hallucinations                                  │
│     - Incorrect dates, names, numbers                       │
│     - False historical claims                               │
│     - Misrepresented statistics                             │
│                                                              │
│  2. Technical Hallucinations                                │
│     - Incorrect API usage                                   │
│     - Fake function signatures                              │
│     - Non-existent libraries                                │
│                                                              │
│  3. Logical Hallucinations                                  │
│     - Invalid reasoning                                     │
│     - False cause-effect relationships                      │
│     - Contradictory statements                              │
│                                                              │
│  4. Source Hallucinations                                   │
│     - Fake citations                                        │
│     - Non-existent URLs                                     │
│     - Fabricated sources                                    │
│                                                              │
│  5. Pseudo-Quantification                                   │
│     - Made-up statistics                                    │
│     - Unsubstantiated percentages                           │
│     - False measurements                                    │
└─────────────────────────────────────────────────────────────┘
```

## Source Verification Framework

### CREDIBLE Checklist

```
┌─────────────────────────────────────────────────────────────┐
│              CREDIBLE Checklist                             │
├─────────────────────────────────────────────────────────────┤
│  C - Currency: Is the information current?                  │
│  R - Relevance: Is the information relevant?                │
│  E - Expertise: Does the author have expertise?             │
│  D - Diversity: Are multiple perspectives included?         │
│  I - Independence: Is the source independent?               │
│  E - Evidence: Is evidence provided?                        │
└─────────────────────────────────────────────────────────────┘
```

### Source Evaluation Matrix

```
┌─────────────────────────────────────────────────────────────┐
│              Source Evaluation                              │
├─────────────────────────────────────────────────────────────┤
│  Source Type          │  Reliability  │  Notes                  │
│  ────────────────────┼───────────────┼───────────────────────│
│  Peer-reviewed journal│  ★★★★★        │  High credibility       │
│  Government website   │  ★★★★☆        │  High credibility       │
│  Industry association │  ★★★★☆        │  Generally reliable     │
│  Corporate website    │  ★★★☆☆        │  May be biased          │
│  Blog/Personal site   │  ★★☆☆☆        │  Verify claims          │
│  Social media         │  ★☆☆☆☆        │  High hallucination     │
│  Unknown source       │  ☆☆☆☆☆        │  Unverifiable           │
└─────────────────────────────────────────────────────────────┘
```

## Evidence-Based Reasoning

### Claim Validation Framework

```
┌─────────────────────────────────────────────────────────────┐
│              Claim Validation Process                       │
├─────────────────────────────────────────────────────────────┤
│  1. Identify the claim                                      │
│     - What is being asserted?                               │
│     - What are the implications?                            │
│                                                              │
│  2. Find supporting evidence                                │
│     - Primary sources (original research)                   │
│     - Secondary sources (reviews, summaries)                │
│     - Tertiary sources (encyclopedias, textbooks)           │
│                                                              │
│  3. Evaluate the evidence                                   │
│     - Source credibility                                    │
│     - Methodology quality                                   │
│     - Consistency with other sources                        │
│                                                              │
│  4. Check for counter-evidence                              │
│     - Alternative explanations                              │
│     - Contradictory findings                                │
│     - Limitations and caveats                               │
│                                                              │
│  5. Draw a conclusion                                       │
│     - Strength of evidence                                  │
│     - Confidence level                                      │
│     - Uncertainty statements                                │
└─────────────────────────────────────────────────────────────┘
```

### Evidence Levels

```
┌─────────────────────────────────────────────────────────────┐
│              Evidence Hierarchy                             │
├─────────────────────────────────────────────────────────────┤
│  Level 1: Systematic reviews and meta-analyses              │
│  Level 2: Randomized controlled trials (RCTs)               │
│  Level 3: Cohort studies                                    │
│  Level 4: Case-control studies                              │
│  Level 5: Case reports and expert opinion                   │
│  Level 6: Anecdotal evidence                                │
└─────────────────────────────────────────────────────────────┘
```

## Fact-Checking Techniques

### Reverse Image Search

```
1. Extract image from content
2. Upload to reverse image search (Google, TinEye)
3. Check source and date of original image
4. Verify context matches current usage
5. Look for manipulated versions
```

### URL Verification

```
1. Check domain authority
2. Verify HTTPS and SSL certificate
3. Check for suspicious characters in URL
4. Verify domain registration information
5. Check for known phishing patterns
```

### Quote Verification

```
1. Search exact quote in quotes
2. Check original source
3. Verify context
4. Look for misattribution
5. Check for paraphrasing
```

## Validation Frameworks

### TRUST Framework

```
┌─────────────────────────────────────────────────────────────┐
│              TRUST Framework                                │
├─────────────────────────────────────────────────────────────┤
│  T - Traceability: Can the claim be traced to a source?     │
│  R - Reproducibility: Can the claim be verified?            │
│  U - Uncertainty: Is uncertainty acknowledged?              │
│  S - Source: Is the source credible?                        │
│  T - Timeliness: Is the information current?                │
└─────────────────────────────────────────────────────────────┘
```

### FAIR Principles

```
┌─────────────────────────────────────────────────────────────┐
│              FAIR Principles                                │
├─────────────────────────────────────────────────────────────┤
│  Findable: Information can be found                   (F)   │
│  Accessible: Information can be accessed              (A)   │
│  Interoperable: Information can be integrated         (I)   │
│  Reusable: Information can be reused                  (R)   │
└─────────────────────────────────────────────────────────────┘
```

## Real-World Impact

**Before this skill:**

- Unverified AI claims
- Incorrect information presented as fact
- Fake citations and sources
- Technical inaccuracies
- Misleading statistics

**After this skill:**

- Verified, evidence-based content
- Proper source citations
- Accurate technical information
- Transparent uncertainty statements
- Reliable documentation

## Cross-References

- **`documentation-best-practices`** - For accurate documentation
- **`context7-docs`** - For up-to-date documentation
- **`analyzing-projects`** - For project analysis

## References

- [Information Verification Best Practices](https://www.poynter.org/)
- [AI Safety Guidelines](https://arxiv.org/)
- [Fact-Checking Handbook](https://www.poynter.org/fact-checking/)
- [Evidence-Based Medicine](https://www.bmj.com/)
