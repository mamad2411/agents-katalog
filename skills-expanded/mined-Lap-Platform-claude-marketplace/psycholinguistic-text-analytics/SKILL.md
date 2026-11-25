---
name: psycholinguistic-text-analytics
description: "Psycholinguistic Text Analytics API skill. Use when working with Psycholinguistic Text Analytics for communication, emotion, ekman-emotion. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Psycholinguistic Text Analytics
API version: 1.0

## Auth
ApiKey x-api-key in header

## Base URL
https://api.symanto.net

## Setup
1. Set your API key in the appropriate header
3. POST /communication -- create first communication

## Endpoints

8 endpoints across 8 groups. See references/api-spec.lap for full details.

### communication
| Method | Path | Description |
|--------|------|-------------|
| POST | /communication | Communication & Tonality |

### emotion
| Method | Path | Description |
|--------|------|-------------|
| POST | /emotion | Emotion Analysis |

### ekman-emotion
| Method | Path | Description |
|--------|------|-------------|
| POST | /ekman-emotion | Emotion Analysis |

### personality
| Method | Path | Description |
|--------|------|-------------|
| POST | /personality | Personality Traits |

### sentiment
| Method | Path | Description |
|--------|------|-------------|
| POST | /sentiment | Sentiment Analysis |

### topic-sentiment
| Method | Path | Description |
|--------|------|-------------|
| POST | /topic-sentiment | Extracts topics and sentiments and relates them. |

### brand-recommendation
| Method | Path | Description |
|--------|------|-------------|
| POST | /brand-recommendation | Predicts whether a phrase is a promoter, detractor or indifferent |

### language-detection
| Method | Path | Description |
|--------|------|-------------|
| POST | /language-detection | Language Detection |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a communication?" -> POST /communication
- "Create a emotion?" -> POST /emotion
- "Create a ekman-emotion?" -> POST /ekman-emotion
- "Create a personality?" -> POST /personality
- "Create a sentiment?" -> POST /sentiment
- "Create a topic-sentiment?" -> POST /topic-sentiment
- "Create a brand-recommendation?" -> POST /brand-recommendation
- "Create a language-detection?" -> POST /language-detection
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
