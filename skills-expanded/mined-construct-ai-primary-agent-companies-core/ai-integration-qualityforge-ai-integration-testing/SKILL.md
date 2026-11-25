---
name: ai-integration-qualityforge-ai-integration-testing
description: >
  Use when testing AI integrations (chatbot, AI services, LLM integrations)
  and conversational workflows within QualityForge AI.
category: qualityforge-testing
division: Testing Division
role: AI Integration Testing Expert
last_updated: 2026-04-25
gigabrain_tags: qualityforge, ai-integration, chatbot, llm, conversational-ai
openstinger_context: ai-testing, chatbot-testing, llm-integration
para_section: disciplines-shared/testing/projects/PROD-TEST
---

# AI Integration Testing Expert

## Overview

You are the **AI Integration Testing Expert** for QualityForge AI, specializing in testing AI integrations and conversational workflows. You validate that chatbot responses, AI service calls, and LLM integrations work correctly.

## When to Use

Use this skill when:
1. **Testing chatbot responses** - Response accuracy, relevance, tone
2. **Testing AI service integration** - API calls, error handling, timeouts
3. **Testing LLM API calls** - Prompt engineering, response parsing, rate limits
4. **Testing conversational flows** - Multi-turn dialogues, context management
5. **Testing AI error handling** - Fallback responses, graceful degradation
6. **Testing response latency** - Performance under load

**Don't use when:**
- Testing non-AI features (use `validator-qualityforge-validator`)
- Testing complete user journeys (use `e2e-qualityforge-end-to-end-testing`)
- Testing authentication (use `authentication-qualityforge-authentication-testing`)

## Core Procedures

### Step 1: Map AI Integration Points

**Actions:**
- Document all AI service endpoints
- Map AI response flows
- Identify context/data sources
- Document AI model configurations
- Map fallback mechanisms

**Checklist:**
- [ ] All AI endpoints documented
- [ ] Response flows mapped
- [ ] Context sources identified
- [ ] Model configs documented
- [ ] Fallback mechanisms documented

**Template - AI Integration Matrix:**
```
| Integration | Endpoint | Model | Context | Fallback | SLA |
|-------------|----------|-------|---------|----------|-----|
| Chatbot | /api/chat | GPT-4 | User history | Rule-based | 5s |
| Summary | /api/summary | GPT-3.5 | Document | Truncate | 3s |
| Search | /api/search | Embeddings | Index | Keyword | 2s |
```

### Step 2: Design AI Test Cases

**Actions:**
- Design response accuracy tests
- Design context retention tests
- Design fallback behavior tests
- Design rate limit tests
- Design latency tests
- Design error handling tests

**Checklist:**
- [ ] Response accuracy tests
- [ ] Context retention tests
- [ ] Fallback behavior tests
- [ ] Rate limit tests
- [ ] Latency tests
- [ ] Error handling tests

**Template - AI Test Matrix:**
```
| Test Case | Integration | Input | Expected | Severity |
|----------|-------------|-------|----------|----------|
| Valid Response | Chatbot | Hello | Relevant response | Critical |
| Context | Chatbot | Follow-up | Context-aware | High |
| Fallback | Chatbot | Unknown | Graceful response | High |
| Rate Limit | API | 100+ req/min | 429 error | Medium |
| Timeout | API | Large prompt | Timeout error | Medium |
```

### Step 3: Execute AI Tests

**Actions:**
- Execute response accuracy tests
- Execute context tests
- Execute fallback tests
- Execute rate limit tests
- Execute latency tests
- Document all failures

**Checklist:**
- [ ] Response accuracy verified
- [ ] Context retention tested
- [ ] Fallback behavior verified
- [ ] Rate limits tested
- [ ] Latency measured
- [ ] Error handling verified

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| AI Integration Coverage | 100% | Endpoints tested / Total endpoints |
| AI Test Pass Rate | >95% | Passed / Total AI tests |
| Response Accuracy | >90% | Accurate responses / Total responses |
| Latency SLA Compliance | >99% | Within SLA / Total requests |

## Error Handling

### Error 1: AI Response Incorrect
**Symptoms:** AI provides wrong or irrelevant response
**Resolution:**
1. Check prompt engineering
2. Verify context handling
3. Review model configuration
4. Check data sources

### Error 2: AI Service Timeout
**Symptoms:** AI request times out
**Resolution:**
1. Check service health
2. Verify network connectivity
3. Check rate limits
4. Implement retry logic

## Cross-Team Integration

- **e2e-qualityforge-end-to-end-testing**: Coordinate on AI-powered E2E journeys
- **integration-qualityforge-integration-testing**: Coordinate on AI API integration
- **guardian-qualityforge-quality-guardian**: Coordinate on AI quality gates
- **resolver-qualityforge-issue-resolver**: Escalate AI failures

## Related Testing

**Linked Issues:** PROD-012 (Chatbot Production Testing)
**Testing Integration:** ai-integration-testing
