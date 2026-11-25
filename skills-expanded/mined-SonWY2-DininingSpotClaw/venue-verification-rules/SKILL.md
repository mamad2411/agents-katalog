---
name: venue-verification-rules
description: Verifies whether restaurants truly fit group dining conditions. Use when Claude must judge headcount feasibility, room or hall availability, buyout options, budget fit, corkage, and source confidence.
compatibility: Claude Code or Claude with web-access or search capability.
metadata:
  author: oai
  version: 1.0.0
  category: verification
---

# Venue Verification Rules

## Instructions

### Source priority
1. official website or official menu
2. reservation platform detail page
3. local map or listing page
4. secondary review content

### Field interpretation
- 인원:
  - exact numeric support → 확인됨
  - vague group support → 추정됨
- 룸:
  - distinguish room from semi-private wording
- 대관:
  - distinguish partial buyout vs full buyout
- 가격:
  - distinguish course vs a la carte
- 콜키지:
  - 가능 / 프리 / 병당 비용 / 미기재

### Output labels
- 확인됨
- 추정됨
- 미확인
