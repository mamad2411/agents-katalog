---
name: self-service-portal
description: "Designs self-service portal structures with knowledge base, ticketing, account management, and resource libraries for customer independence."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Self-Service Portal

## When to Use This Skill

Use this skill when you need to:
- Design the structure and content architecture of a customer self-service portal
- Plan knowledge base, ticketing, account management, and resource library sections
- Reduce support volume by enabling customers to help themselves
- Create a portal information architecture before building or configuring a platform

**DO NOT** use this skill for building the portal technically, selecting software platforms, or writing individual help articles. This is for designing the portal structure and user experience.

---

## Core Principle

A SELF-SERVICE PORTAL SUCCEEDS WHEN CUSTOMERS PREFER IT OVER CONTACTING SUPPORT — THAT MEANS FAST ANSWERS, EASY NAVIGATION, AND A CLEAR PATH TO A HUMAN WHEN SELF-SERVICE IS NOT ENOUGH.

---

## Phase 1: Needs Assessment

Understand what customers need from self-service.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What product or service do you offer?" | No default |
| **Support volume** | "How many support requests do you handle per month?" | 20-50 |
| **Top self-service needs** | "What do customers ask that they could answer themselves?" | No default |
| **Current tools** | "What self-service resources exist today? (FAQ page, help docs)" | Minimal or none |
| **Platform** | "Where will the portal live? (Notion, Zendesk, custom site, WordPress)" | To be decided |
| **Customer tech level** | "How comfortable are your customers with self-service?" | Moderate |

**GATE: Confirm needs before designing the portal structure.**

---

## Phase 2: Information Architecture

Design the portal structure and navigation.

### Portal Sections

```
## Self-Service Portal Structure

### 1. Knowledge Base
   - Getting Started
     - [Setup guide]
     - [Quick start tutorial]
     - [First steps checklist]
   - How-To Guides
     - [Category 1: guides]
     - [Category 2: guides]
   - Troubleshooting
     - [Common issues]
     - [Error messages]
   - FAQ
     - [Billing questions]
     - [Account questions]
     - [Product questions]

### 2. Account Management
   - View/update account information
   - Billing history and invoices
   - Subscription management
   - Password reset

### 3. Support
   - Submit a support ticket
   - Check ticket status
   - Live chat (during business hours)
   - Emergency contact information

### 4. Resources
   - Video tutorials
   - Templates and downloads
   - Best practices guides
   - Release notes / What is new

### 5. Community (optional)
   - Discussion forum
   - Feature requests
   - Tips from other customers
```

### Navigation Design

```
## Portal Homepage Layout

**Search bar** (prominent, top of page)
"Search for answers..."

**Quick links** (4-6 most common actions)
[ Getting Started ] [ Submit Ticket ] [ Billing ] [ Account ]

**Popular articles** (auto-populated by view count)
1. [Most viewed article]
2. [Second most viewed]
3. [Third most viewed]

**Categories** (visual cards or icons)
[ Knowledge Base ] [ How-To Guides ] [ Troubleshooting ] [ Resources ]

**Still need help?** (always visible)
[Contact Support] button
```

**GATE: Present the information architecture for review.**

---

## Phase 3: Content Plan

Plan the content needed to populate the portal.

### Content Inventory

```
## Portal Content Plan

| Section | Article/Page | Priority | Status | Owner |
|---------|-------------|----------|--------|-------|
| Getting Started | Setup guide | HIGH | To write | [Name] |
| Getting Started | Quick start | HIGH | To write | [Name] |
| Troubleshooting | [Common issue 1] | HIGH | To write | [Name] |
| FAQ | Billing questions | MEDIUM | To write | [Name] |
| Resources | [Template 1] | LOW | To create | [Name] |
```

### Content Priority Order

1. **Launch essentials (Month 1):** Getting started guide, top 5 FAQ answers, support ticket form
2. **Core content (Month 2):** Troubleshooting guides for common issues, account management instructions
3. **Expansion (Month 3+):** Video tutorials, templates, best practices, community features

### Search Optimization

- Title every article with the exact words customers use to describe the problem
- Add tags and keywords that match common search queries
- Include synonyms (e.g., "login" and "sign in" should both find the same article)
- Surface popular articles on the homepage

---

## Phase 4: Measurement

Track portal performance and iterate.

### Success Metrics

```
## Portal Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Self-service resolution rate | 60%+ of issues | — |
| Search success rate (found what they needed) | 80%+ | — |
| Support ticket reduction | [X]% decrease from baseline | — |
| Portal satisfaction (post-visit survey) | 4+/5 | — |
| Most-searched terms with no results | 0 | — |
```

### Monthly Portal Review

1. What are the top search terms? Do articles exist for all of them?
2. Which articles have high views but low helpfulness ratings? (Rewrite needed)
3. What support tickets could have been self-service? (Content gap)
4. Are customers finding the portal? (Check traffic sources)

### Continuous Improvement

- Add new articles for every support question asked 3+ times
- Update articles when product changes affect instructions
- Remove or archive outdated content quarterly
- Test the search experience monthly — can you find answers in under 60 seconds?

---

## Anti-Patterns

- **Hard to find** — if customers cannot find the portal, it does not exist. Link it from every support email, product interface, and website footer.
- **No search** — customers will not browse categories. Search must work and work well.
- **Outdated content** — stale articles erode trust in the entire portal. Assign article owners and review dates.
- **No path to a human** — self-service without an escape hatch to support creates frustration. Always provide a contact option.
- **Launching empty** — a portal with 3 articles looks abandoned. Launch with at least 10-15 core articles.

---

## Recovery

- **Customers still contact support for documented issues:** The portal is hard to find or the articles are hard to understand. Audit both discoverability and readability.
- **Low portal traffic:** Add portal links in support auto-replies, onboarding emails, and product UI. Customers need to be trained to check self-service first.
- **User cannot create enough content:** Start with FAQ-style answers (short, direct). Full how-to guides can come later.
- **Search returns irrelevant results:** Improve article titles, add tags, and create articles for common searches that currently return nothing.
- **User has no budget for a portal platform:** A well-organized Notion page or Google Site is a viable free portal for small businesses.
