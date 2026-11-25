---
description: Audit implementation against project constitution principles
tags: [feature, validation, constitution, compliance]
---

# Validate Against Constitution

Audit the implemented feature against the project constitution to ensure compliance with foundational principles.

## Instructions

You are auditing feature implementation for constitution compliance before declaring the feature complete.

### Step 1: Load Constitution

Read: `specs/.specify/memory/constitution.md`

Extract core principles (typically 3-7 principles per project).

Example from Birdmate:
```markdown
## Core Principles

I. Natural Language First
II. Accurate Bird Taxonomy
III. Test-First & Field-Validated
IV. Observability & Audit Trail
V. API First
```

### Step 2: Audit Each Principle

For each principle, evaluate implementation compliance.

## Audit Template

```markdown
# Constitution Compliance Audit

**Feature**: [Feature Name]
**Feature ID**: [ID]
**Audit Date**: [Timestamp]
**Auditor**: Feature Lead

## Principle-by-Principle Analysis

### Principle I: [Principle Name]

**Constitution Statement**:
[Quote the exact principle from constitution.md]

**Compliance Status**: ✅ Compliant | ⚠️ Partial | ❌ Non-Compliant

**Evidence**:
- [Specific file/code demonstrating compliance]
- [Test showing principle upheld]
- [Documentation reference]

**Findings**:
[Detailed assessment of how well implementation follows this principle]

**Violations** (if any):
- [Specific instance where principle was violated]
- [Impact of violation]
- [Remediation required]

**Recommendations**:
- [Action to improve compliance]

---

### Principle II: [Next Principle]

[Repeat structure]
```

## Example Audit

```markdown
# Constitution Compliance Audit: Bird Search Feature

**Feature**: Natural Language Bird Search
**Feature ID**: 001-bird-search
**Audit Date**: 2025-12-24
**Auditor**: Feature Lead

## Overall Compliance: ⚠️ Partial (4/5 principles compliant)

---

### Principle I: Natural Language First

**Constitution Statement**:
> "Every search interface MUST accept human-readable descriptions (color, size, behavior, habitat, song characteristics) as first-class input. Bird data enrichment and index design are driven by user-query patterns, not technical convenience. No query syntax required—plain English only."

**Compliance Status**: ✅ Compliant

**Evidence**:
- `frontend/src/components/SearchBox.tsx` - Plain text input, no special syntax
- `backend/src/search/nlp-parser.ts` - Parses natural language queries
- Integration tests use plain English: "red chest with grey back"
- No query syntax documented or required

**Findings**:
Implementation fully embraces natural language. Search accepts free-form text and interprets color, size, and behavior patterns without requiring structured input.

**Test Coverage**:
- 12 test cases with natural language queries
- Tests cover color descriptors, behavior patterns, habitat descriptions
- All pass with accurate results

**Violations**: None

**Recommendations**: None - principle fully upheld

---

### Principle II: Accurate Bird Taxonomy

**Constitution Statement**:
> "All bird records MUST reference authoritative taxonomic sources (eBird, Cornell Lab taxonomy, or equivalent). When conflicting data exists across sources, flag ambiguity to the user; never silently merge or prioritize sources without documentation. Synonyms and regional names are cross-referenced for discoverability."

**Compliance Status**: ⚠️ Partial

**Evidence**:
- `src/data/taxonomy.ts` - Loads eBird taxonomy (authoritative)
- `src/data/birds.json` - 487 bird records with eBird IDs
- Database schema includes `taxonomy_source` field

**Findings**:
Primary taxonomy correctly sourced from eBird. However, synonym cross-referencing is incomplete.

**Violations**:
1. **Synonym Support Missing**
   - Spec mentions cross-referencing regional names
   - Implementation: Only scientific + common English names
   - Impact: Users searching "robin" in Europe get North American Robin
   - Example: European Robin (Erithacus rubecula) not distinguished from American Robin (Turdus migratorius)

2. **Ambiguity Flagging Not Implemented**
   - Constitution requires flagging conflicting data
   - Implementation: Returns first match only
   - Impact: Users don't know when name is ambiguous

**Recommendations**:
1. **Critical**: Implement synonym mapping (eBird has this data)
2. **Important**: Add ambiguity detection and user notification
3. Add field `common_names: string[]` to bird records
4. Create follow-up story: US-004 Synonym Support

---

### Principle III: Test-First & Field-Validated

**Constitution Statement**:
> "TDD mandatory: Write tests covering query intent → User approves expected results → Run tests (fail) → Implement → Tests pass. Integration tests simulate real field conditions (e.g., 'red head, yellow eye' must match breeding-plumage variants). Searches tested against curated queries from actual birdwatchers."

**Compliance Status**: ⚠️ Partial

**Evidence**:
- TDD followed: 85% test coverage
- `tests/integration/search-real-queries.test.ts` - 24 real-world test cases
- All user stories had tests written first

**Findings**:
Strong TDD discipline during development. However, field validation is missing.

**Violations**:
1. **No Field Validation**
   - Constitution requires testing with "actual birdwatchers"
   - Implementation: Tested by developers only
   - Impact: May not handle real-world query patterns
   - Example: No validation that "sounds like a drum roll" matches Pileated Woodpecker

**Recommendations**:
1. **Before Launch**: Get 3-5 birdwatchers to test search
2. Capture their queries and results
3. Add queries to integration test suite
4. Document field validation in AGENTS.md

---

### Principle IV: Observability & Audit Trail

**Constitution Statement**:
> "Every search query logged with user intent, normalized description, and top-3 results returned. Logging MUST include: query timestamp, user location (optional), results matched, confidence scores. Failed or ambiguous queries tracked for future index improvements. No PII logged without explicit consent."

**Compliance Status**: ✅ Compliant

**Evidence**:
- `backend/src/logging/search-logger.ts` - Structured logging
- Elasticsearch integration stores search audit trail
- Log format includes all required fields:
  ```json
  {
    "timestamp": "2025-12-24T10:30:00Z",
    "query": "red chest grey back",
    "normalized": ["red", "chest", "grey", "back"],
    "results": [
      { "id": "robin", "confidence": 0.95 },
      { "id": "rosefinch", "confidence": 0.78 }
    ],
    "user_location": null,
    "session_id": "abc123"
  }
  ```

**Findings**:
Comprehensive logging implemented. No PII captured (location is opt-in).

**Violations**: None

**Recommendations**: 
- Add dashboard for analyzing failed queries (future enhancement)

---

### Principle V: API First

**Constitution Statement**:
> "Ship as web application with RESTful API backend; UI MUST accept plain text input (search box), API returns JSON (structured). API endpoints designed for composability and external integrations. Dependencies kept minimal; use embedded bird database (JSON or lightweight DB) unless scale demands external service."

**Compliance Status**: ✅ Compliant

**Evidence**:
- `contracts/api.openapi.yml` - Full REST API spec
- `POST /api/search` endpoint accepts `{ query: string }`
- Returns JSON: `{ birds: [...], confidence: number }`
- Frontend consumes API, doesn't access database directly
- SQLite used (lightweight, embedded)

**Findings**:
Clean API-first architecture. Frontend and backend properly separated.

**Violations**: None

**Recommendations**:
- Document API rate limits (future consideration)
- Add API versioning if schema changes expected

---

## Summary

### Compliance Overview

| Principle | Status | Critical Issues |
|-----------|--------|-----------------|
| I. Natural Language First | ✅ Compliant | None |
| II. Accurate Taxonomy | ⚠️ Partial | Synonym support missing |
| III. Test-First | ⚠️ Partial | No field validation |
| IV. Observability | ✅ Compliant | None |
| V. API First | ✅ Compliant | None |

**Overall**: ⚠️ 3/5 Fully Compliant, 2/5 Partial

### Critical Action Items

1. **Implement Synonym Cross-Referencing** (Principle II)
   - Blocking for v1.0 launch
   - Estimated effort: 1 story (US-004)
   
2. **Conduct Field Validation** (Principle III)
   - Required before production launch
   - Get 3-5 birdwatchers to test
   - 1-2 days

### Post-Launch Improvements

1. Add ambiguity detection for conflicting bird names
2. Build failed-query analytics dashboard

## Sign-Off

- [ ] All critical violations addressed
- [ ] Partial compliance items have mitigation plan
- [ ] Constitution amendments proposed if needed
- [ ] Feature Lead approval

**Status**: [Ready for Launch | Needs Work | Blocked]

**Auditor**: [Name]
**Date**: [Date]
```

## Audit Checklist

For each principle:
- ✅ Quote exact wording from constitution
- ✅ Provide specific code/file evidence
- ✅ Identify violations with impact assessment
- ✅ Recommend remediation actions
- ✅ Classify severity (Critical | Important | Minor)

## When to Run This Audit

- **Before feature launch**: Mandatory full audit
- **After all stories merged**: Comprehensive review
- **When constitution updated**: Re-audit affected features
- **During retrospective**: Learn from compliance gaps

---

**Remember**: Constitution is non-negotiable. Either comply or amend constitution with rationale.
