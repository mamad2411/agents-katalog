---
name: bias-detection
description: Use when writing or reviewing code that makes decisions about people — pricing, scoring, ranking, filtering, access control, or content moderation. Detects discriminatory logic and unfair algorithmic patterns.
invoke_when: Use when generating code that scores, ranks, filters, prices, recommends, or classifies people or user-generated content. Also invoke during code review of any decision-making logic that affects users differently.
---

# Bias Detection

## Core Rule

**Code that makes decisions about people must be auditable, explainable, and free from proxy discrimination.** This applies to pricing algorithms, recommendation engines, content moderation, access control, scoring systems, search ranking, and any logic where different users can receive different outcomes.

## High-Risk Code Patterns

Flag these patterns immediately when they appear in decision-making code:

### 1. Protected Attribute Usage

Direct use of protected attributes in decision logic:

```typescript
// BAD — direct discrimination
function calculateRate(user: User): number {
  if (user.gender === 'female') return baseRate * 1.2;  // FLAG
  if (user.age > 60) return baseRate * 1.5;              // FLAG
  if (user.zipCode === '10451') return baseRate * 1.8;   // FLAG — proxy for race/income
  return baseRate;
}

// GOOD — decision based on relevant behavioral attributes
function calculateRate(account: Account): number {
  const riskScore = calculateRiskFromBehavior(account.history);
  return baseRate * riskMultiplier(riskScore);
}
```

### 2. Proxy Variable Detection

Variables that correlate with protected attributes:

| Proxy Variable | Correlates With | Why It's Risky |
|---------------|----------------|---------------|
| Zip code / postal code | Race, income | Redlining by another name |
| First name / last name | Race, ethnicity, gender | Name-based discrimination |
| Language preference | National origin, ethnicity | Exclusion of non-dominant groups |
| Device type / browser | Income, age | Economic discrimination |
| School / university name | Race, socioeconomic status | Educational elitism |
| Profile photo analysis | Race, gender, age, disability | Visual discrimination |

When any of these appear in scoring, ranking, or pricing logic — flag for review.

### 3. Threshold Bias

Hard-coded thresholds that disproportionately affect groups:

```typescript
// BAD — arbitrary threshold without justification
function isEligible(user: User): boolean {
  return user.creditScore > 720;  // FLAG — threshold disproportionately excludes certain demographics
}

// BETTER — document threshold justification and measure impact
function isEligible(user: User): boolean {
  // Threshold: 650 based on default rate analysis (see decision doc #1234)
  // Disparate impact tested quarterly — last review 2026-01-15
  return user.creditScore > CREDIT_THRESHOLD;
}
```

### 4. Training Data Assumptions

Code that embeds assumptions from biased data:

```typescript
// BAD — hardcoded assumption from biased historical data
const DEFAULT_SALARY = role === 'engineer' ? 120000 : 65000;

// BAD — gendered defaults
const title = user.name.endsWith('a') ? 'Ms.' : 'Mr.';

// GOOD — no assumptions about defaults; let the user specify
const title = user.preferredTitle ?? '';
```

## Bias Categories to Check

### Decision Fairness
- **Equal treatment**: Same inputs produce same outputs regardless of group membership
- **Equal opportunity**: Qualified individuals from all groups have equal chance of positive outcome
- **Demographic parity**: Positive outcomes distributed proportionally across groups (when applicable)

### Content Moderation Bias
- Moderation rules must not disproportionately flag content from specific cultural or linguistic groups
- Keyword blocklists must be reviewed for cultural bias
- Automated content decisions must have human appeal paths

### Search and Ranking Bias
- Default sort orders must not systematically disadvantage any group
- Search algorithms must not de-rank results based on proxy attributes
- Recommendation systems must measure and report diversity metrics

### Pricing and Access Bias
- Dynamic pricing must not correlate with protected attributes
- Feature gating must not create discriminatory access patterns
- Rate limiting must be uniform across demographic groups

## Implementation Guardrails

### 1. Decision Logging

Every automated decision about a person must be loggable:

```typescript
interface DecisionLog {
  decisionType: string;       // 'pricing' | 'eligibility' | 'ranking' | 'moderation'
  inputFeatures: string[];    // which features were used (NOT their values for PII reasons)
  outcome: string;            // the decision made
  modelVersion: string;       // which version of the logic made this decision
  timestamp: string;
  appealable: boolean;        // can the user challenge this decision?
}
```

### 2. Disparate Impact Testing

For any scoring or classification system, implement a test:

```typescript
it('pricing does not show disparate impact by zip code', () => {
  const results = ZIP_CODES_BY_DEMOGRAPHIC.map(zip => ({
    zip,
    price: calculatePrice({ ...baseUser, zipCode: zip }),
  }));

  const groupAAvg = average(results.filter(r => GROUP_A_ZIPS.includes(r.zip)).map(r => r.price));
  const groupBAvg = average(results.filter(r => GROUP_B_ZIPS.includes(r.zip)).map(r => r.price));

  // Four-fifths rule: ratio must be > 0.8
  expect(Math.min(groupAAvg, groupBAvg) / Math.max(groupAAvg, groupBAvg)).toBeGreaterThan(0.8);
});
```

### 3. Explainability Requirement

Decision-making code must support explanation:

```typescript
// Every decision function should have an explain variant
function calculateEligibility(user: User): { eligible: boolean; reasons: string[] } {
  const reasons: string[] = [];

  if (user.accountAge < 30) reasons.push('Account less than 30 days old');
  if (user.verificationStatus !== 'verified') reasons.push('Identity not verified');

  return {
    eligible: reasons.length === 0,
    reasons,
  };
}
```

## Regulatory Context

| Regulation | Requirement | Applies When |
|-----------|-------------|-------------|
| EU AI Act | High-risk AI systems require bias audits, transparency, human oversight | Scoring, hiring, credit, law enforcement |
| ECOA (US) | Cannot discriminate in credit decisions | Any credit/lending logic |
| Fair Housing Act | Cannot use protected attributes in housing decisions | Real estate, rental platforms |
| GDPR Art. 22 | Right to explanation for automated decisions | Any automated decision affecting EU residents |
| NYC Local Law 144 | Bias audits required for automated employment tools | Hiring, promotion, recruiting algorithms |

## Code Review Checklist

- [ ] No protected attributes (gender, race, age, religion, disability) in decision logic
- [ ] Proxy variables identified and justified or removed
- [ ] Hard-coded thresholds documented with justification and impact analysis
- [ ] Decision logging implemented for user-affecting automated decisions
- [ ] Disparate impact test exists for scoring/classification systems
- [ ] Explainability: users can understand why a decision was made about them
- [ ] Content moderation rules reviewed for cultural/linguistic bias
- [ ] Default values do not encode demographic assumptions
- [ ] Appeal/override mechanism exists for automated decisions
