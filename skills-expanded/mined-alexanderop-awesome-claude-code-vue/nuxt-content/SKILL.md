---
name: nuxt-content
description: Use when answering questions about OR implementing features with Nuxt Content (queries, MDC components, document-driven mode), especially when uncertain about current API - Nuxt Content is frequently updated with breaking changes, so fetch current documentation from llms.txt before responding to ensure accuracy over training data
---

# Nuxt Content Documentation Reference

## Overview

**Nuxt Content evolves rapidly. Training data is stale. Fetch current docs FIRST, implement/answer SECOND.**

Core principle: https://content.nuxt.com/llms.txt is the source of truth for ALL Nuxt Content questions AND implementations, regardless of how simple the task seems or how confident you feel about the API.

## When to Use

Use this skill for ANY question OR implementation task about:
- Nuxt Content queries (`queryContent`, `where`, operators)
- MDC (Markdown Components) syntax
- Document-driven mode
- Content rendering components
- API references
- Version-specific features
- Troubleshooting Nuxt Content issues

**Especially use when:**
- Implementing a feature using Nuxt Content
- Not confident about current API syntax
- Aware training data might be stale
- About to write code involving Nuxt Content
- User mentions "Nuxt Content" and you need to take action

## Mandatory Workflow

**Step 1: Fetch Documentation with Targeted Extraction**

**CRITICAL:** Use targeted WebFetch prompts that extract ONLY the specific sections needed. Do NOT ask for full documentation dumps.

```
Use WebFetch on: https://content.nuxt.com/llms.txt

Prompt format:
"Extract ONLY the documentation for [specific API/feature/concept].

Include:
- API syntax with parameters
- Code examples
- Version-specific notes
- Common gotchas

Exclude everything else. Return a concise summary."
```

**Why targeted extraction matters:**
- Full docs are 50k+ tokens
- Targeted extraction returns 1-3k tokens
- 20-50x context savings vs full dump
- Faster responses, cleaner context

**Exception for reusing:** Reuse docs from same conversation ONLY if ALL conditions met:
- You already fetched docs for this topic in this conversation AND
- The previous fetch explicitly covered the SAME specific API/feature/concept AND
- You can answer the new question completely with the previous result AND
- Less than 10 minutes have passed

**When in doubt, fetch again with targeted prompt.** Be specific about what to extract.

**Step 2: Answer Using Extracted Documentation**

- Use extracted documentation as PRIMARY source
- Reference training data only to supplement or provide context
- Include links to relevant docs sections
- Cite what came from llms.txt vs. general knowledge

**NO EXCEPTIONS to targeted fetch:** Fetch docs even when:
- User says "quick question"
- Question seems simple
- You feel confident about the answer
- User mentions they already looked at docs
- It's a yes/no question
- It's a version confirmation
- You're late in the conversation

## Red Flags - STOP and Dispatch Subagent First

If you're thinking ANY of these thoughts, STOP. Dispatch subagent to fetch docs FIRST:

**Question-answering red flags:**
- "This is a straightforward question I know"
- "User needs this fast"
- "Fetching docs would take extra time"
- "Low risk if I'm wrong"
- "I can fetch later if needed"
- "They already looked at docs"
- "This feature is mature, my knowledge is current"
- "Just need to confirm what I know"

**Implementation red flags:**
- "I'll implement based on what I know"
- "This seems straightforward to implement"
- "Let me write the code quickly"
- "I know how queryContent works"
- "I remember the MDC syntax"
- "I've used Nuxt Content before" (in training data)
- "I can update if the code fails"
- "Just need to write simple query code"

**Context-bloat red flags (CRITICAL):**
- "I'll fetch the full documentation"
- "Let me get all the docs to be thorough"
- "I'll load llms.txt completely"
- "Better to have all the info"
- "Generic WebFetch prompt is fine"

**ABSOLUTELY FORBIDDEN:** Fetching full documentation dump. This bloats context with 50k+ tokens.

**REQUIRED:** Use targeted WebFetch prompts that extract ONLY the specific section needed (1-3k tokens).

**All of these mean: Use targeted extraction. Specify EXACTLY what to extract. No full dumps.**

## Why Training Data Fails

Nuxt Content v3 introduced breaking changes. API evolves. Features change. Your training data is from January 2025 - documentation is updated continuously.

**Real examples from testing:**
- Agent suggested `$contains` without checking current operator syntax
- Agent confirmed MDC without verifying v3-specific changes
- Agent provided query patterns without checking current API

Every case: Agent was confident. Every case: Should have fetched docs.

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|----------------|-----|
| Answer from memory | Confidence in training data | Fetch llms.txt with targeted extraction first |
| Skip docs for "simple" questions | Assume simplicity = accuracy | Simple questions need current docs too - fetch targeted |
| Postpone fetching | "Can fetch if wrong" | Wrong answers waste user time - fetch first |
| Trust version knowledge | "Feature is mature" | Mature features still change - verify with docs |
| Cite "official docs say" | User mentioned docs | Fetch to verify what docs actually say |
| Fetch full documentation | "Better to be thorough" | Targeted extraction (1-3k tokens) vs full dump (50k+ tokens) |
| Generic WebFetch prompt | Laziness | Specify EXACTLY what section to extract |

## Quick Reference

**Every Nuxt Content interaction:**
1. Use WebFetch on https://content.nuxt.com/llms.txt with TARGETED prompt
2. Extract ONLY relevant sections (not full docs)
3. Use extracted info as primary source
4. Provide answer/implementation based on extracted docs
5. Supplement with training knowledge only if needed
6. Cite source (docs vs. general knowledge)

**Targeted WebFetch prompt template:**
```
"Extract ONLY the documentation for [specific API/feature/concept] from Nuxt Content.

Include:
- API syntax with parameters
- Code examples
- Version-specific notes
- Common gotchas

Exclude everything else. Return a concise summary (1-3k tokens max)."
```

**Context savings:** Targeted extraction (1-3k tokens) vs full dump (50k+ tokens) = 20-50x savings

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "User needs fast answer/implementation" | Fast wrong answer wastes more time than slow correct answer |
| "I know this from training" | Training data is stale; Nuxt Content v3 has breaking changes |
| "Straightforward question/implementation" | Simple tasks still need current API syntax |
| "Low risk if wrong" | Wrong answer/code blocks user; high cost to be wrong |
| "They already looked at docs" | Verify what docs actually say - might have misread |
| "Feature is mature" | Mature features get updates and deprecations |
| "Can fetch later if needed" | Fetch now = right first time; fetch later = wasted round trip |
| "Just confirming what I know" | Confirmation requires checking source, not memory |
| "I'll implement then test" | Implementing wrong API = debugging time for user |
| "I can update if it fails" | Test-fix cycle wastes time; fetch docs first prevents failures |
| "I'll fetch all the docs to be thorough" | Full dump = 50k+ tokens; targeted extraction = 1-3k tokens |
| "Generic WebFetch prompt is fine" | Targeted prompt extracts only what's needed; saves 20-50x context |
| "The docs are small enough" | llms.txt is 50k+ tokens; always use targeted extraction |

## Real-World Impact

**Without this skill:** Agents provide outdated API syntax, wrong operator names, incorrect version information, implement features with stale APIs based on training data, blow up context with full documentation dumps.

**With this skill:** Agents fetch current documentation with targeted extraction before answering OR implementing, provide accurate syntax, cite correct version info, save user debugging time, keep conversation context efficient.

**Context savings:** Targeted extraction (1-3k tokens) vs full dump (50k+ tokens) = 20-50x savings per interaction

**Time cost:** Targeted fetch adds 5-10 seconds. User debugging incorrect information or broken implementations adds 5-30 minutes. Always fetch with targeted extraction first.
