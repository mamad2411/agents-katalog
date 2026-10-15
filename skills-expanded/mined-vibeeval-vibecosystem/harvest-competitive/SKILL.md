---
name: harvest-competitive
description: Competitive intelligence - extract features, pricing, tech stack from competitor sites
allowed-tools: [Bash, Read, Write, WebFetch, WebSearch]
keywords: [competitive, analysis, competitor, pricing, features, comparison, intelligence, benchmark]
---

# Harvest Competitive

Automated competitive intelligence gathering. Extract and compare features, pricing, technology stacks, and market positioning from competitor websites.

## Usage

```bash
# Analyze a single competitor
/harvest-competitive https://competitor.com

# Compare multiple competitors
/harvest-competitive https://a.com https://b.com https://c.com --compare

# Focus on specific aspect
/harvest-competitive https://competitor.com --focus pricing
/harvest-competitive https://competitor.com --focus features
/harvest-competitive https://competitor.com --focus tech-stack
```

## Output

```markdown
# Competitive Analysis: [Company]
> Source: [URLs]
> Date: [timestamp]

## Product Overview
[What they do, target market, positioning]

## Features
| Feature | Status | Notes |
|---------|--------|-------|
| Feature A | Yes | [details] |
| Feature B | No | - |

## Pricing
| Plan | Price | Key Limits |
|------|-------|-----------|
| Free | $0 | [limits] |
| Pro | $X/mo | [limits] |

## Technology Stack (detected)
- Frontend: [framework]
- Backend: [inferred from headers/scripts]
- CDN: [provider]
- Analytics: [tools]

## Strengths & Weaknesses
### Strengths
- [strength 1]

### Weaknesses
- [weakness 1]

## Comparison Matrix (multi-competitor)
| Aspect | Us | Competitor A | Competitor B |
|--------|-----|-------------|-------------|
| Feature X | Yes | Yes | No |
| Price | $X | $Y | $Z |
```

## Integration

- **growth**: Market positioning, feature gaps
- **designer**: UI/UX patterns from competitors
- **architect**: Technical approach comparison
- **business-analyst**: Feature gap analysis

## Rules

- Only use publicly available information
- No login-wall bypassing
- Respect robots.txt
- Date-stamp all data (competitive info ages fast)
- Flag uncertainty: "detected" vs "confirmed"
