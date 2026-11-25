---
name: dining-query-planner
description: Builds search queries for restaurant and company dinner venue scouting. Use when Claude needs to search by area, headcount, budget, room, private booking, buyout, cuisine, corkage, parking, or business-dinner tone.
compatibility: Claude Code or Claude with web-access or search capability.
metadata:
  author: oai
  version: 1.0.0
  category: dining-research
---

# Dining Query Planner

## Instructions
Convert user requirements into diversified query sets.

### Query expansion rules
- Expand area into district, station, and neighborhood variants
- Expand headcount into phrases such as:
  - 25명 가능
  - 단체 25명
  - 25인 룸
  - 25명 대관
- Expand budget into a small range window
- Split corkage into:
  - 콜키지
  - 콜키지 프리
  - 주류 반입
- Create separate exclusion terms

### Output
- primary_queries
- expansion_queries
- verification_queries
- exclusion_terms
