---
name: shopify-headless-middleware
description: use this skill to facilitate ai-sdlc and mob programming sessions for shopify headless ecommerce, middleware api, and integration use cases. trigger this skill when the user asks to design, analyze, extend, test, or workshop ecommerce features such as discounts, customer segmentation, pricing, checkout, loyalty, inventory, oms/erp integrations, storefront api flows, admin api usage, or middleware architecture.
---

# Shopify Headless Middleware AI-SDLC Skill

Use this skill to guide AI-assisted SDLC activities for Shopify Headless, middleware APIs, and commerce integrations.

## Core Purpose

Help teams move from business use case to collaborative design, implementation planning, testing, and delivery using mob programming and AI-assisted SDLC practices.

## Default Output Structure

When the user provides a use case, produce:

1. Business objective
2. Customer and stakeholder context
3. Mob programming participants
4. Domain discovery questions
5. Architecture approach
6. API design
7. Data model or payload examples
8. Business rules
9. Testing strategy
10. Edge cases and risks
11. Mob session agenda
12. Implementation checklist

## Reference Routing

Use the relevant reference file based on the user's topic:

- Discount segmentation: `references/discount-segmentation.md`
- Checkout customization: `references/checkout-customization.md`
- Inventory synchronization: `references/inventory-sync.md`
- OMS/ERP integration: `references/oms-erp-integration.md`

## Mob Programming Participants

Recommend participants based on the use case:

- Product Owner
- Shopify Architect
- Middleware/API Developer
- Frontend Developer
- QA Engineer
- DevOps/SRE Engineer
- Security Engineer when authentication, customer data, payments, or PII are involved
- Business/Marketing stakeholder when discounts, promotions, loyalty, or segmentation are involved

## Standard Mob Session Agenda

### 1. Use Case Framing

Clarify:

- What customer problem are we solving?
- Which customer types are affected?
- Which Shopify capabilities are involved?
- Which middleware services are involved?
- What are the business rules?

### 2. Domain Discovery

Identify:

- Customer segments
- Cart states
- Pricing rules
- Discount eligibility
- Shopify data sources
- External systems
- API consumers
- Checkout impact

### 3. Architecture Discussion

Cover:

- Headless frontend responsibility
- Middleware responsibility
- Shopify responsibility
- Cache responsibility
- Integration responsibility
- Logging and observability responsibility

### 4. API Design

Define:

- Endpoint name
- Request payload
- Response payload
- Authentication requirements
- Error handling
- Rate limits
- Caching behavior

### 5. Rule Definition

Capture rules in this format:

```text
IF <condition>
AND <optional condition>
THEN <business outcome>
```

### 6. Test Planning

Include:

- Happy path
- Guest customer
- Logged-in customer
- VIP customer
- Wholesale customer
- Invalid customer session
- Shopify API failure
- Middleware timeout
- Cache miss
- Conflicting rules

### 7. Implementation Checklist

End with a clear engineering delivery checklist.

## Output Style

Be practical, architecture-focused, and implementation-ready.

Prefer:

- Tables
- API examples
- Rule examples
- Testing checklists
- Clear separation of business rules and technical design

Avoid:

- Generic agile explanations
- Overly theoretical content
- Long motivational content
