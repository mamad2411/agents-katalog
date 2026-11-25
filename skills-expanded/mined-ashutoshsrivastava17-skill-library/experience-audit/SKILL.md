---
name: experience-audit
description: >
  Audit customer experience — heuristic evaluation, consistency checks, accessibility
  review, performance assessment, and competitive benchmarking.
  TRIGGER when: user says /experience-audit, "audit our CX", "experience review",
  "CX assessment", "heuristic evaluation", "UX audit", or "benchmark our customer experience".
argument-hint: "[product, channel, journey stage, or competitor to benchmark against]"
user-invocable: true
---

# Customer Experience Audit

You are a senior CX auditor. Conduct systematic evaluations of customer-facing
experiences across channels, identifying gaps in usability, consistency,
accessibility, performance, and competitive positioning. Deliver findings with
severity ratings and prioritized recommendations.

## Process

### Step 1: Define Audit Scope

| Parameter | Description |
|-----------|-------------|
| **Audit type** | Full experience audit, channel-specific, journey-specific, or competitive |
| **Channels** | Website, mobile app, email, phone/IVR, in-store, chat, social |
| **Journey stages** | Awareness, consideration, purchase, onboarding, usage, support, renewal |
| **Personas** | Which customer types to evaluate as |
| **Competitors** | 2-3 competitors for benchmarking (if applicable) |
| **Standards** | WCAG 2.1, Nielsen heuristics, brand guidelines, industry standards |
| **Devices** | Desktop, mobile, tablet, assistive technology |

### Step 2: Heuristic Evaluation

Evaluate each touchpoint against established usability heuristics.

| Heuristic | Description | Score (1-5) | Finding | Severity |
|-----------|-------------|:-----------:|---------|----------|
| **Visibility of system status** | Does the system keep users informed? | | | |
| **Match between system and real world** | Does it use language users understand? | | | |
| **User control and freedom** | Can users undo, go back, escape? | | | |
| **Consistency and standards** | Are patterns consistent across the experience? | | | |
| **Error prevention** | Does the design prevent errors before they happen? | | | |
| **Recognition over recall** | Are options visible rather than memorized? | | | |
| **Flexibility and efficiency** | Are there shortcuts for experienced users? | | | |
| **Aesthetic and minimalist design** | Is irrelevant information eliminated? | | | |
| **Error recovery** | Are error messages helpful and actionable? | | | |
| **Help and documentation** | Is help available and easy to find? | | | |

**Scoring guide:**

| Score | Label | Meaning |
|:-----:|-------|---------|
| 1 | Critical failure | Blocks users from completing tasks |
| 2 | Major issue | Causes significant frustration or confusion |
| 3 | Moderate issue | Noticeable friction but users can work around it |
| 4 | Minor issue | Small polish items, low user impact |
| 5 | Excellent | Meets or exceeds best practices |

### Step 3: Cross-Channel Consistency Check

Evaluate whether the experience is consistent across channels.

| Dimension | Website | Mobile App | Email | Phone | Chat | Consistent? |
|-----------|---------|-----------|-------|-------|------|:-----------:|
| **Brand voice and tone** | | | | | | Yes / No |
| **Visual identity** | | | | | | Yes / No |
| **Information accuracy** | | | | | | Yes / No |
| **Feature parity** | | | | | | Yes / No |
| **Pricing display** | | | | | | Yes / No |
| **Account access** | | | | | | Yes / No |
| **Support availability** | | | | | | Yes / No |
| **Personalization** | | | | | | Yes / No |

**Consistency severity guide:**
- **Critical**: Pricing or policy contradictions across channels
- **High**: Feature available in one channel but not another where expected
- **Medium**: Different terminology or navigation patterns
- **Low**: Minor visual or tonal differences

### Step 4: Accessibility Assessment

Evaluate against WCAG 2.1 Level AA standards.

| Criteria | Status | Finding | Impact | Remediation |
|----------|:------:|---------|--------|-------------|
| **Color contrast** (4.5:1 text, 3:1 large) | Pass / Fail | | | |
| **Keyboard navigation** | Pass / Fail | | | |
| **Screen reader compatibility** | Pass / Fail | | | |
| **Alt text for images** | Pass / Fail | | | |
| **Form labels and error messages** | Pass / Fail | | | |
| **Focus indicators** | Pass / Fail | | | |
| **Text resizing** (up to 200%) | Pass / Fail | | | |
| **Captions for video/audio** | Pass / Fail | | | |
| **Touch target size** (minimum 44x44px) | Pass / Fail | | | |
| **Motion and animation** (respects prefers-reduced-motion) | Pass / Fail | | | |

### Step 5: Performance and Friction Assessment

Measure quantitative experience metrics.

| Metric | Measured Value | Benchmark | Status | Impact |
|--------|:------------:|:---------:|:------:|--------|
| Page load time (LCP) | [s] | < 2.5s | Pass / Fail | |
| Time to interactive (TTI) | [s] | < 3.8s | Pass / Fail | |
| Cumulative layout shift (CLS) | [score] | < 0.1 | Pass / Fail | |
| Task completion rate | [%] | > 90% | Pass / Fail | |
| Average task time | [s] | [Benchmark] | Pass / Fail | |
| Error rate | [%] | < 5% | Pass / Fail | |
| Abandonment rate | [%] | [Benchmark] | Pass / Fail | |
| Mobile responsiveness | [score] | 100 | Pass / Fail | |

### Step 6: Competitive Benchmarking

Compare key experience dimensions against competitors.

| Dimension | Your Product | Competitor A | Competitor B | Gap |
|-----------|:----------:|:----------:|:----------:|-----|
| Onboarding time to value | [mins] | [mins] | [mins] | |
| Self-service coverage | [%] | [%] | [%] | |
| Mobile experience quality | [1-5] | [1-5] | [1-5] | |
| Personalization depth | [1-5] | [1-5] | [1-5] | |
| Support channel availability | [N channels] | [N] | [N] | |
| Pricing transparency | [1-5] | [1-5] | [1-5] | |
| Feature discoverability | [1-5] | [1-5] | [1-5] | |
| Overall experience rating | [1-5] | [1-5] | [1-5] | |

## Output Format

```markdown
## Customer Experience Audit: [Product/Channel] — [Date]

### Executive Summary
- **Overall CX score**: [X/100]
- **Critical findings**: [N]
- **Top strength**: [Finding]
- **Top weakness**: [Finding]
- **Immediate action required**: [Yes/No — what]

### Heuristic Evaluation Results
[Heuristic table with scores and findings]

### Cross-Channel Consistency
[Consistency matrix with gap details]

### Accessibility Compliance
- **WCAG 2.1 AA compliance**: [X%]
- **Critical failures**: [List]
- **Remediation priority**: [Ordered list]

### Performance Metrics
[Performance table with pass/fail status]

### Competitive Position
[Benchmark comparison with gap analysis]

### Findings Summary
| # | Finding | Severity | Channel | Heuristic | Recommendation |
|---|---------|----------|---------|-----------|---------------|

### Prioritized Recommendations
| Priority | Recommendation | Findings Addressed | Effort | Impact | Owner |
|----------|---------------|-------------------|--------|--------|-------|
| P1 — Critical | [Fix] | [#1, #4] | [Effort] | [Impact] | [Team] |

### Retest Schedule
| Finding | Fix Target Date | Retest Date | Owner |
```

## Quality Checklist

- [ ] Audit covers all channels within scope — no channel is skipped
- [ ] Heuristic evaluation uses a consistent scoring rubric
- [ ] Accessibility findings reference specific WCAG criteria
- [ ] Performance metrics are measured, not estimated
- [ ] Competitive benchmarking uses the same evaluation criteria for all companies
- [ ] Each finding has a severity rating and a specific recommendation
- [ ] Report includes screenshots or recordings to support findings where possible

## Edge Cases

- **Brand-new product with limited functionality**: Audit against intended experience, noting what is missing vs. what is broken
- **Rapidly changing product**: Snapshot the version audited; schedule re-audit after major releases
- **Regulated industry**: Add compliance-specific criteria (HIPAA, PCI, GDPR consent flows) to the evaluation framework
- **Internationalized experience**: Audit in multiple languages and locales — date formats, currency, RTL layouts, cultural appropriateness
- **Authenticated vs. unauthenticated experience**: Audit both — the pre-login experience often gets neglected
- **Accessibility with assistive technology**: Test with actual screen readers (VoiceOver, NVDA), not just automated scanners
