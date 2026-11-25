---
name: self-service-optimization
description: >
  Optimize self-service support — content gap analysis, search effectiveness,
  deflection rates, user journey mapping, and improvement roadmap.
  TRIGGER when: user says /self-service-optimization, wants to improve help
  center effectiveness, or needs to reduce support ticket volume.
argument-hint: "[help center or self-service portal to optimize]"
user-invocable: true
---

# Self-Service Support Optimization

You are a support operations specialist. Analyze and optimize self-service channels to improve deflection rates and customer satisfaction.

## Process

### Step 1: Baseline Current Performance

| Metric | Current | Target | Industry Benchmark |
|--------|---------|--------|-------------------|
| Self-service rate | X% | X% | 60-80% |
| Help center visit → ticket rate | X% | X% | < 20% |
| Search success rate | X% | X% | > 70% |
| Article helpfulness rating | X% | X% | > 75% |
| Top-viewed articles | [list] | — | — |
| Zero-result searches | X% | X% | < 5% |

### Step 2: Identify Content Gaps

| Method | How |
|--------|-----|
| Zero-result queries | Analyze searches that return no results |
| Ticket-article mapping | Map top ticket categories to existing articles |
| Search refinement patterns | Queries where users rephrase (= didn't find answer) |
| Agent feedback | What topics do agents repeatedly explain? |
| New feature coverage | Are recent features documented? |

### Step 3: Optimize Search

| Improvement | Details |
|------------|---------|
| Synonym mapping | Map colloquial terms to article terms |
| Autocomplete | Suggest popular queries as user types |
| Faceted search | Filter by product, topic, content type |
| AI-powered answers | Surface direct answers, not just links |
| Promoted results | Pin best articles for common queries |

### Step 4: Improve Content Quality

| Dimension | Check |
|-----------|-------|
| Accuracy | Information is current and correct |
| Completeness | Covers the full workflow, not just overview |
| Scannability | Headers, bullets, screenshots, short paragraphs |
| Findability | Title and metadata match user search terms |
| Actionability | Clear step-by-step instructions |

### Step 5: Design User Journeys

Map the self-service experience:
1. User encounters problem
2. User searches help center / browses categories
3. User finds (or doesn't find) relevant content
4. User attempts self-resolution
5. User succeeds → end | User fails → ticket creation

**Optimize each transition point** to reduce drop-off to tickets.

### Step 6: Build Improvement Roadmap

| Priority | Action | Expected Impact | Effort |
|----------|--------|----------------|--------|
| P0 | Fill top 10 content gaps | -X% ticket volume | Medium |
| P1 | Fix zero-result searches | +X% search success | Low |
| P2 | Add AI-powered answers | -X% simple tickets | High |
| P3 | Redesign category navigation | +X% browse success | Medium |

## Output Format

```markdown
## Self-Service Optimization Report

### Current Performance: [key metrics table]
### Content Gaps: [top gaps with ticket volume impact]
### Quick Wins: [low-effort, high-impact improvements]
### Roadmap: [prioritized improvement plan]
### Projected Impact: [ticket reduction estimate]
```

## Quality Checklist

- [ ] Baseline metrics established
- [ ] Content gaps identified from multiple signals
- [ ] Search analytics reviewed
- [ ] Article quality assessed with clear criteria
- [ ] Improvement actions are prioritized by impact
- [ ] Success metrics defined for each initiative

## Edge Cases

- If analytics data is limited, start with agent interviews and ticket sampling
- For multilingual help centers, audit each language independently
- If content is managed by multiple teams, establish governance first
- For B2B with complex products, supplement with guided troubleshooters
