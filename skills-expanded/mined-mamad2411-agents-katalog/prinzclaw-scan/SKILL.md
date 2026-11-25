---
name: prinzclaw-scan
description: Scans public statements for verifiable promises with time anchors and numeric metrics
tools: [web_fetch, rss_parser]
---

# Scan Skill — T (Tension)

## Purpose
Extract verifiable promises from public statements by powerful figures.

## When to Use
When given a quote or statement from a public figure, use this skill to determine if it contains a verifiable promise.

## How It Works

### Input
- Entity name and handle
- Quote/statement text
- Source URL (optional)
- Timestamp (defaults to now)

### Analysis Criteria
A promise is **verifiable** if it contains at least TWO of:
1. **Time anchor**: "within 6 months", "by 2026", "next quarter", "in 30 days"
2. **Numeric metric**: "$2", "50,000 jobs", "15% growth", "reduce to $X"
3. **Binary outcome**: "will not sign", "will never do", "I guarantee X won't happen"

### Filtering Rules
Reject statements that are:
- Vague slogans without specifics
- Political rhetoric without measurable outcomes
- Emotional expressions without facts
- Pure opinions without evidence

### Output
Returns a structured promise object:
```json
{
  "id": "SHA-256 hash",
  "entity": "Name",
  "promise_text": "exact quote",
  "source_url": "https://...",
  "promise_date": "2026-03-16",
  "expiry_date": "2026-09-16",
  "verifiable_metric": "price < $2.00",
  "data_source_for_verification": "https://eia.gov/...",
  "status": "PENDING"
}
```

## Usage in TACO Pipeline
The scan skill is the first stage. Its output feeds directly into the analyze skill for contradiction detection.
