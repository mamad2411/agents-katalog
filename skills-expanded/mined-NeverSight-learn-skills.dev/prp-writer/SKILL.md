---
name: prp-writer
description: Guides creation of Product Requirements Prompts (PRPs) - comprehensive requirement documents that serve as the foundation for AI-assisted development
license: MIT
metadata:
  author: gustavog-gutierrez
  version: "1.0"
allowed-tools: Read, Edit, Write
triggers:
  - prp-writer
  - prp writer
  - product requirements prompt
  - create PRP
  - generate requirements
  - AI-assisted development requirements
---

# PRP Generator (Product Requirements Prompt)

## Overview

The PRP Generator helps you create comprehensive Product Requirements Prompts - structured documents that capture everything needed to build a product feature or system. PRPs are optimized for AI-assisted development, providing clear requirements that both humans and AI can understand.

**Core Purpose:** Transform vague ideas into actionable, complete requirements.

## When to Use This Skill

Use PRP Generator when:

- Starting a new product or major feature
- Requirements are unclear or scattered
- Need to communicate requirements to development team
- Using AI assistants for implementation
- Transitioning from discovery to development
- Onboarding new team members to a project

## Key Capabilities

- Structure requirements into 12 standardized sections
- Identify project complexity pattern (A, B, C)
- Extract user stories in Jobs-to-be-Done format
- Define success criteria and metrics
- Document functional and non-functional requirements
- Capture constraints, risks, and assumptions
- Clarify what's in and out of scope

## Workflow

### The 12-Section PRP Structure

A complete PRP contains these 12 sections:

1. **Project Overview**
2. **Problem Statement**
3. **Success Criteria**
4. **User Stories (Jobs-to-be-Done)**
5. **Functional Requirements**
6. **Non-Functional Requirements**
7. **Technical Constraints**
8. **Data Requirements**
9. **UI/UX Requirements**
10. **Risks & Assumptions**
11. **Out of Scope**
12. **Open Questions**

Let's dive into each:

---

### 1. Project Overview

**Purpose:** High-level context and pattern classification

**What to Include:**

- Project name and one-sentence description
- Pattern classification (A, B, or C)
- Timeline estimate
- Target users
- Business context

**Example:**

```
Project: Domain Workflow Assistant
Pattern: C (AI-Native System)
Timeline: 10-12 weeks
Users: Primary operators + end users
Context: Reduce repetitive manual work by 40% while maintaining task quality
```

---

### 2. Problem Statement

**Purpose:** Clearly define the problem being solved

**Template:**

```
[User type] faces [problem] when [situation].
This causes [negative outcome].
We know this because [evidence].
```

**Example:**

```
Primary operators face long response times when end users request recurring workflow help. This causes user dissatisfaction and operator burnout handling repetitive inquiries.

We know this because:
- 60% of requests are recurring "How do I..." questions
- Average response time is 4 hours
- Operator surveys show 70% of time spent on repetitive questions
- NPS dropped from 45 to 38 in past 6 months
```

---

### 3. Success Criteria

**Purpose:** Define measurable outcomes

**Structure:**

- Primary metric (North Star)
- Secondary metrics
- Minimum success thresholds

**Example:**

```
Primary Metric:
- Reduce support ticket volume by 40% within 3 months of launch

Secondary Metrics:
- 80% of common questions answered by AI without escalation
- <2 second response time for AI answers
- >4.0/5.0 user satisfaction rating with AI responses
- 50% reduction in agent time spent on common questions

Minimum Success:
- 30% ticket reduction + 4.0/5.0 satisfaction
```

---

### 4. User Stories (Jobs-to-be-Done)

**Purpose:** Capture user needs in job-to-be-done format

**Template:**

```
When [situation], I want to [action], so I can [outcome].
```

**Example:**

```
End-User Stories:
1. When I have a billing question, I want instant answers, so I can resolve issues without waiting.
2. When I'm setting up my account, I want step-by-step guidance, so I don't get stuck.
3. When I need to reset my password, I want a simple self-service flow, so I don't need to contact support.

Agent Stories:
1. When a complex issue arrives, I want context from the AI conversation, so I can help efficiently.
2. When training new agents, I want the AI to handle basics, so I can focus on teaching advanced topics.
3. When end users escalate, I want interaction history, so I don't ask redundant questions.
```

---

### 5. Functional Requirements

**Purpose:** What the system must do

**Categories:**

- Core features (P0 - must have)
- Important features (P1 - should have)
- Nice-to-have (P2 - could have)

**Example:**

```
P0 (Core - MVP):
- FR-001: System answers common questions from knowledge base
- FR-002: System escalates to human when confidence is low (<70%)
- FR-003: Agents can see full conversation history
- FR-004: System tracks conversation satisfaction ratings

P1 (Important - Post-MVP):
- FR-005: System learns from agent corrections
- FR-006: System handles multi-turn conversations with context
- FR-007: Agents can override AI suggestions

P2 (Nice-to-have - Future):
- FR-008: System proactively suggests help articles
- FR-009: System detects dissatisfied end users
- FR-010: Multi-language support
```

---

### 6. Non-Functional Requirements

**Purpose:** How the system should perform

**Categories:**

- Performance
- Security
- Scalability
- Reliability
- Usability

**Example:**

```
Performance:
- NFR-001: Response time <2 seconds for 95th percentile
- NFR-002: Handle 100 concurrent conversations
- NFR-003: Knowledge base search <500ms

Security:
- NFR-004: End-user data encrypted at rest and in transit
- NFR-005: SOC2 Type II compliance
- NFR-006: Role-based access control (RBAC)
- NFR-007: Audit logs for all AI responses

Scalability:
- NFR-008: Support 10,000 conversations/day at launch
- NFR-009: Scale to 100,000 conversations/day within 6 months

Reliability:
- NFR-010: 99.9% uptime SLA
- NFR-011: Graceful degradation if AI service unavailable

Usability:
- NFR-012: Agents can use with <10 minutes training
- NFR-013: WCAG 2.1 AA accessibility compliance
```

---

### 7. Technical Constraints

**Purpose:** Technology limitations and requirements

**What to Include:**

- Existing systems to integrate with
- Technology stack requirements
- Infrastructure constraints
- Budget limitations
- Timeline constraints

**Example:**

```
Integrations:
- Must integrate with the existing system of record
- Must use the organization's approved identity provider
- Must emit logs and metrics to the existing observability platform

Technology Stack:
- Backend: Approved backend runtime for the project
- AI model: Approved model provider or self-hosted model
- Retrieval/index layer: Approved search, database, or vector index
- Frontend: Existing UI framework or platform standard

Infrastructure:
- Deploy on the existing hosting or runtime environment
- Use existing CI/CD and release pipelines

Budget:
- AI/service usage budget: TBD monthly maximum
- Infrastructure budget: TBD monthly maximum

Timeline:
- MVP must launch within 10 weeks
- Full feature set within 16 weeks
```

---

### 8. Data Requirements

**Purpose:** What data is needed and how it's managed

**Structure:**

- Data sources
- Data models
- Data privacy
- Data retention

**Example:**

```
Data Sources:
- Knowledge base articles (500+ source documents)
- Historical workflow records (2 years)
- Product or process documentation
- Public or internal FAQ pages

Data Models:
- Interactions: id, end_user_id, operator_id, messages[], status, satisfaction_rating
- Messages: id, sender, text, timestamp, ai_confidence
- Knowledge: id, title, content, embeddings, category, last_updated

Data Privacy:
- PII must be redacted before AI processing
- Conversation data retained for 90 days
- Analytics data aggregated and anonymized
- GDPR right-to-delete compliance

Data Security:
- Encrypt end-user data at rest (AES-256)
- Encrypt in transit (TLS 1.3)
- Role-based access to conversation data
```

---

### 9. UI/UX Requirements

**Purpose:** How users interact with the system

**What to Include:**

- User flows
- Interface requirements
- Design constraints
- Accessibility needs

**Example:**

```
End-User Interface:
- Chat widget in bottom-right corner
- Typing indicators and response time estimates
- Clear "Talk to a human" button always visible
- Conversation history accessible for 30 days

Operator Interface:
- Side panel showing AI suggestions
- One-click "Accept AI answer" button
- Edit AI answer before sending
- Flag incorrect responses for retraining
- Dashboard showing AI performance metrics

User Flows:
1. End user asks question → System retrieves answer → Displays with confidence
2. Low confidence → Auto-escalate to operator → Operator sees full context
3. Operator corrects response → System logs correction for improvement

Design Constraints:
- Match existing brand colors
- Mobile-responsive design
- WCAG 2.1 AA compliant
- Support keyboard navigation
```

---

### 10. Risks & Assumptions

**Purpose:** Identify potential blockers and dependencies

**Structure:**

- Risks with mitigation plans
- Assumptions to validate
- Dependencies on external factors

**Example:**

```
Risks:
1. AI hallucination risk
   - Mitigation: Confidence thresholds, human review for low confidence

2. Knowledge base quality risk
   - Mitigation: Content audit before launch, SME review of top 100 articles

3. User adoption risk (operators do not rely on assisted output)
   - Mitigation: Gradual rollout, agent training, show accuracy metrics

4. API cost overruns
   - Mitigation: Aggressive caching, token limits, usage monitoring

Assumptions:
1. End users will accept assisted responses (validate with beta test)
2. Knowledge base is accurate and up-to-date (audit required)
3. 80% of questions can be answered with existing knowledge
4. Approved AI/service latency is acceptable (<2s)

Dependencies:
1. Access to system-of-record API (approval required)
2. Knowledge base export from source repository
3. AI/service quota increase if current limits are insufficient
4. Operator availability for training and feedback
```

---

### 11. Out of Scope

**Purpose:** Explicitly state what WON'T be built

**Why Important:** Prevents scope creep and sets expectations

**Example:**

```
Out of Scope for MVP:
- Voice/phone support integration (post-MVP)
- Multi-language support (Phase 2)
- Integration with CRM system (future)
- Custom AI model training unless explicitly required
- Mobile app (web only initially)
- Proactive workflow initiation (on-demand assistance only)
- Sentiment analysis dashboard (future analytics)
- Agent performance scoring (v2 feature)

Explicitly NOT Building:
- Custom LLM training (too expensive)
- Real-time translation (complexity vs. value)
- Video call integration (different project)
```

---

### 12. Open Questions

**Purpose:** Document unknowns that need answers

**Structure:**

- Question
- Who can answer
- When answer needed by
- Impact if not answered

**Example:** `Q1: What error rate is acceptable for assisted responses? Who: product owner and domain owner. Deadline: before target architecture approval. Impact: Determines confidence thresholds and escalation flow.`

---

## Examples

Use compact PRPs for bounded Pattern A changes and full-depth PRPs for AI-heavy Pattern C systems. For Pattern C, define model, retrieval, orchestration, evaluation, latency, token budget, privacy, fallback, and human escalation requirements explicitly.

## Best Practices

- Start with the problem before naming solutions.
- Make success criteria measurable.
- Use Jobs-to-be-Done stories to capture user intent.
- State out-of-scope items explicitly.
- Track open questions with owner, deadline, and impact.
- Update the PRP as constraints and evidence change.
- Validate with product, engineering, design, and security stakeholders when relevant.

## Common Pitfalls

- Writing implementation choices instead of behavioral requirements.
- Using vague success criteria such as "better UX" or "fast".
- Omitting non-functional requirements.
- Assuming hidden knowledge instead of documenting it.
- Applying Pattern C complexity to Pattern A work.

## Deliverables

A complete PRP document containing all 12 sections, a pattern classification, measurable outcomes, explicit scope boundaries, tracked open questions, and stakeholder-ready requirements.

## Success Metrics

The PRP is ready when developers can build from it without repeated clarification, stakeholders agree on scope, risks are visible, open questions have owners, and the selected pattern matches the project complexity.
