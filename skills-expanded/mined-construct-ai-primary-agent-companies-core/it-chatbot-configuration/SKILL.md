---
title: IT Chatbot Configuration
description: Skill for chatbot setup, prompt tuning, state-aware assistant configuration, and discipline integration for the ConstructAI platform
frequency: Per chatbot deployment or update
success_rate: 90%
tags:
  - it-operations
  - chatbot-configuration
  - prompt-tuning
  - conversational-ai
  - discipline-integration
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/prompts/02050_AI-NATIVE-INFORMATION-TECHNOLOGY-PROMPT.md
  - docs_construct_ai/skills/domainforge_ai/voice-command-integration/SKILL.md
---

# IT Chatbot Configuration

## Overview

This skill covers chatbot configuration and management for the ConstructAI platform. It encompasses chatbot setup, state-aware assistant configuration, prompt tuning, discipline integration, knowledge base management, and conversational flow design. Primary agent: 02050-009 ChatBot Engineer. Supporting skills: `domainforge_ai/voice-command-integration`.

## Triggers

- New discipline page needs chatbot integration
- Existing chatbot requires performance tuning
- Conversational flow update needed
- Knowledge base update required
- New chat type (document, agent, workspace) needs configuration
- User feedback indicates conversation quality issues

## Prerequisites

- Chatbot infrastructure deployed and accessible
- Discipline domain knowledge available
- ChatbotBase component integrated in page
- LLM configuration established
- Knowledge base or vector database available for RAG

## Steps

### Step 1: Chatbot Type Assessment
- Identify chat type needed (document, agent, upsert, workspace)
- Determine discipline context and code
- Identify user roles and permissions
- Review existing chatbot implementations for similar disciplines

### Step 2: State-Aware Configuration
- Configure chatbot to detect page state (agents, upsert, workspace)
- Define state-specific system prompts
- Define state-specific capability boundaries
- Configure state transition handling
- Test state detection accuracy

### Step 3: Prompt Configuration
- Select appropriate system prompt template
- Inject discipline-specific context (domain knowledge, glossary)
- Configure assistant name and persona
- Define response boundaries (what chatbot can and cannot do)
- Add safety boundaries from domain knowledge

### Step 4: Knowledge Base Integration
- Configure RAG pipeline connection
- Select relevant document collections for discipline
- Configure retrieval parameters (top-k, similarity threshold)
- Test retrieval accuracy with sample queries

### Step 5: Conversation Flow Design
- Design greeting and initial prompt
- Design response structure for common query types
- Design error handling (no results, ambiguous query, out of scope)
- Design escalation path to human when needed

### Step 6: Testing & Validation
- Test with sample queries for each state
- Test with out-of-scope queries — verify boundary enforcement
- Test with ambiguous queries — verify clarification requests
- Test state transitions — verify chatbot adapts correctly
- Test knowledge retrieval — verify RAG accuracy

### Step 7: Monitoring & Tuning
- Configure conversation tracking and analytics
- Configure user feedback collection
- Identify low-quality conversation patterns
- Tune prompts, retrieval parameters, and boundaries
- Update knowledge base with new information

## Success Criteria

- Chatbot correctly detects page state and adapts response
- System prompt includes discipline-specific context
- RAG retrieval returns relevant results 90%+ of the time
- Out-of-scope queries handled with appropriate escalation
- Conversation boundaries enforced
- User feedback collected and incorporated

## Common Pitfalls

1. **Incorrect state detection**: Ensure state detection logic covers all page states
2. **Overconfident responses**: Configure uncertainty disclosure when knowledge is incomplete
3. **Missing boundaries**: Explicitly define what chatbot cannot do (modify data, approve deployments)
4. **Knowledge base staleness**: Schedule regular knowledge base updates
5. **Retrieval accuracy**: Tune top-k and similarity threshold per discipline
6. **No fallback**: Always provide human escalation path

## Cross-References

- `it-agent-coordination/SKILL.md` — Multi-agent chatbot orchestration
- `it-documentation-generation/SKILL.md` — Knowledge base document generation
- `domainforge_ai/voice-command-integration/SKILL.md` — Voice integration patterns

## Usage

Apply this skill when configuring chatbots for new discipline pages, tuning existing chatbot performance, or updating conversational flows and knowledge bases.

## Metrics

- **State Detection Accuracy**: 95%+ correct state identification
- **RAG Retrieval Accuracy**: 90%+ relevant results in top-3
- **Response Quality Score**: 85%+ of responses rated satisfactory by users
- **Boundary Enforcement**: 100% of out-of-scope queries handled appropriately
- **Escalation Success**: 90%+ of escalated issues resolved by human within SLA