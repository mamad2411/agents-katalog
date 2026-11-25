---
name: text-sentiment
description: Analyze sentiment of text using LLM classification (positive/negative/neutral)
---

# Text Sentiment Analysis

Analyze sentiment of text using LLM classification (positive/negative/neutral)

## When to Use

- User wants to analyze sentiment
- User wants to sentiment analysis
- Keywords: sentiment, nlp, analysis, text

## Required Parameters

- **text** (string): Text to analyze

## Output

- **sentiment** (string): positive, negative, or neutral
- **confidence** (number): Confidence score 0-1
- **explanation** (string): Brief explanation

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `classify` -> 4 steps -> Exit: `ret_ok`, `ret_fail`
