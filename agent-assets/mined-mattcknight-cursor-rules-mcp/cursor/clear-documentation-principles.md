---
description: Clear Documentation Principles - Principles of clear, uncluttered technical documentation based on analysis of high-quality enterprise architecture documents
alwaysApply: false
---

# Clear Documentation Principles

## Overview

This document captures the principles of clear, uncluttered technical documentation based on analysis of high-quality enterprise architecture documents.

**Purpose:** Establish writing standards that produce documentation that is easy to read, understand, and act upon.

---

## Core Principles

### 1. Clarity Over Completeness

Write for understanding, not for documentation sake.

**✅ DO:**
```markdown
[Company] seeks a partner to fully manage and be contractually responsible 
for [business function] between [stakeholder groups].
```

**❌ DON'T:**
```markdown
As per the strategic initiative outlined in the Q3 2025 roadmap, 
stakeholders have identified that [Company], being a leading [industry] 
company in the [space], is seeking to establish a partnership...
```

**Principle:** One clear sentence beats three verbose ones.

---

### 2. Minimize Metadata Clutter

Keep document headers clean. No metadata blocks.

**✅ DO:**
```markdown
# [Feature Name]

**Jira Initiative:** [JIRA-XXXXX](link)

## Introduction
This document outlines the architecture proposal...
```

**❌ DON'T:**
```markdown
# [Feature Name]

**Date:** November 4, 2025
**Version:** v1.0
**Author:** Development Team
**Status:** Draft
**Reviewers:** Architecture Team, Security Team
**Approvers:** [Pending]
**Classification:** Internal
**Last Modified:** November 4, 2025

## Document History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | Oct 1 | ... | Initial draft |
...
```

**Principle:** Put the Jira link in context. Skip everything else. Git handles version control.

---

### 3. No Status Footers

Documents should end cleanly, not with administrative metadata.

**✅ DO:**
```markdown
## What is Out of Scope?

1. Feature X (future phase)
2. Feature Y (not requested)

---

*Document source: [Source attribution]*
```

**❌ DON'T:**
```markdown
---

**Document Status:** Ready for Review
**Version:** v1.0
**Last Updated:** November 1, 2025
**Prepared By:** Development Team
**Reviewed By:** Architecture Team, Security Team
**Approved By:** [Pending Review]

**Reference Documents:**
- Solution Architecture
- Technical Design
```

**Principle:** Git commit history shows who/when. Document should focus on content.

---

### 4. Diagrams First, Text Second

Show, then explain. Don't explain, then show.

**✅ DO:**
```markdown
## Proposed Architecture

[DIAGRAM HERE]

Key components include:
- Component 1: Purpose
- Component 2: Purpose
- Component 3: Purpose
```

**❌ DON'T:**
```markdown
## Proposed Architecture

The proposed architecture consists of several key components. First, 
we have Component 1 which serves as a central hub. This component 
includes multiple APIs including public and internal. The public 
API is designed for external parties while the internal API...

[DIAGRAM HERE]
```

**Principle:** Diagram communicates faster. Text adds detail.

---

### 5. Short, Direct Sentences

Cut filler words. Use active voice. Be specific.

**✅ DO:**
```markdown
Service stores information.
```

**❌ DON'T:**
```markdown
The Service is responsible for the storage and management of 
information data.
```

**✅ DO:**
```markdown
Dev completion: September 15th, 2025
Go-live: October 15th, 2025
```

**❌ DON'T:**
```markdown
The development team anticipates that development activities 
will be substantially complete by approximately mid-September 
of 2025, with production deployment targeted for mid-October.
```

**Principle:** Every word must earn its place.

---

### 6. Business Language First

Lead with business value, follow with technical details.

**✅ DO:**
```markdown
## Business Need

[Company] seeks a partner to fully manage [business function] between 
[stakeholders], streamlining [process]. [Company] gains [benefit] 
and [outcome], enabling growth.

## Technical Solution

Service exposes REST APIs for:
1. Function 1
2. Function 2
```

**❌ DON'T:**
```markdown
## Technical Solution

The Service microservice will be implemented using [Technology] 
with RESTful APIs exposing endpoints for CRUD operations on 
entities stored in [Database]...

## Business Need

This enables [Company]'s business objectives around [function].
```

**Principle:** Executives read top sections. Engineers read full document.

---

### 7. Explicit Scope Boundaries

Always state what's IN and what's OUT.

**✅ DO:**
```markdown
## Functional Requirements

- Enhance [process]
- Extend [system] with [feature]

## What is Out of Scope?

1. Feature X (future phase)
2. Feature Y (not requested)
```

**❌ DON'T:**
```markdown
## Scope

This project will handle various aspects of the [process] 
workflow as they relate to the [initiative].
```

**Principle:** Ambiguity kills projects. Be explicit.

---

### 8. Concrete Numbers and Dates

Avoid vague quantifiers. Use real data.

**✅ DO:**
```markdown
## Performance Requirements

- Current load: [Number] transactions/year
- Future load: [Number]+ transactions/year
- API response time: < 2 seconds SLA
- Availability: 99.9% uptime
```

**❌ DON'T:**
```markdown
## Performance Requirements

- System must handle significant transaction volume
- API should respond quickly
- High availability required
```

**Principle:** Specific numbers enable planning and validation.

---

### 9. Consistent Section Structure

Use patterns readers can learn.

**✅ DO:**
```markdown
## Component Name

[DIAGRAM]

### Purpose
What it does.

### Technical Details
- Tech stack item 1
- Tech stack item 2

### API Endpoints
**POST** `/endpoint`
[Details]

---
```

**Pattern Recognition:** Each component follows same structure.

---

### 10. Horizontal Rules for Visual Breaks

Use `---` to separate major sections, creating visual breathing room.

**✅ DO:**
```markdown
## Business Need

Content here.

---

## Timelines

Content here.

---

## Architecture

Content here.
```

**❌ DON'T:**
```markdown
## Business Need
Content here.
## Timelines
Content here.
## Architecture
Content here.
```

**Principle:** White space improves readability.

---

### 11. Bold Titles: Separate Line, Not Inline

Bold titles or labels must be on their own line, not inline with the content.

**✅ DO:**
```markdown
**Decision:**

Database-driven feature flags editable via Admin UI

**Rationale:**

Enables toggle without code deployment and safe rollback.
```

**❌ DON'T:**
```markdown
**Decision**: Database-driven feature flags editable via Admin UI

**Rationale**: Enables toggle without code deployment and safe rollback.
```

**Principle:** Bold titles on separate lines are easier to scan. Inline titles create visual clutter.

---

### 12. No Bold Text Within Sentences

Avoid bold text in the middle of sentences unless explicitly required.

**✅ DO:**
```markdown
Services are bypassed for zero dollar transactions (no external calls).
Document generation is selective (Cover Letter, EOB, 835 only).
```

**❌ DON'T:**
```markdown
Services are **bypassed** for zero dollar transactions (no external calls).
Document generation is **selective** (Cover Letter, EOB, 835 only).
```

**EXCEPTION - Labeled List Items:**
```markdown
**Rationale (Architectural Trade-off):**
- **Ideal**: [Option 1]
- **Reality**: [Constraint]
- **Pragmatic**: [Solution]
```

This pattern is acceptable for structured list items with labels because:
- The labels are consistently formatted (all bold, all start with colon)
- The pattern aids in scanability of structured information
- The labels are not mid-sentence, they're list item prefixes

**Principle:** Bold text within prose creates visual noise. Reserve bold for headings, labels, and emphasis only when explicitly needed.

---

## Writing Style Rules

### Sentence Length

**Target:** 15-25 words per sentence average.

**✅ Examples:**
- "Service stores information." (3 words)
- "[Company] seeks a partner to fully manage processing." (8 words)
- "[Company] wants a strategic partnership to gain unique data access." (11 words)

### Paragraph Length

**Target:** 2-4 sentences per paragraph.

**✅ Example:**
```markdown
Service is a new component for [purpose]. It stores [data] 
and [function]. It acts as a [role] to [stakeholders]. 
Future expansion will include [features].
```

### Word Choice

**Prefer:**
- Simple over complex: "use" not "utilize"
- Active over passive: "System calls API" not "API is called by system"
- Concrete over abstract: "store in database" not "persist to data layer"
- Direct over hedged: "is" not "might be" or "could be"

**Replace:**
| Instead of | Use |
|------------|-----|
| "leverage" | "use" |
| "utilize" | "use" |
| "facilitate" | "enable" |
| "in order to" | "to" |
| "due to the fact that" | "because" |
| "at this point in time" | "now" |
| "is responsible for the storage of" | "stores" |
| "provides the capability to" | "enables" or "allows" |

---

## Document Structure Pattern

```markdown
# [Feature Name]

**Jira:** [LINK]

---

## Table of Contents

---

## Introduction
Brief, 1-2 sentences.

---

## Business Need
Why this matters (business language).

---

## Timelines
Concrete dates.

---

## Requirements
What we're building.

---

## Current Architecture
Where we are (with diagram).

---

## Proposed Architecture
Where we're going (with diagram).

### Component 1
Detail.

### Component 2
Detail.

---

## Data Flows
How information moves (with diagrams).

---

## What is Out of Scope
What we're NOT building.

---

*Source attribution*
```

---

## Checklist: Is Your Document Clear?

Run through this before finalizing:

### Structure
- [ ] Title is clear and specific
- [ ] Jira link in Introduction (not metadata header)
- [ ] No metadata block at top (Date, Version, Author, Status)
- [ ] No status footer at bottom
- [ ] Horizontal rules (`---`) separate major sections
- [ ] Table of contents if document > 10 sections

### Language
- [ ] Sentences average 15-25 words
- [ ] Paragraphs are 2-4 sentences
- [ ] Active voice used ("System calls" not "is called")
- [ ] Simple words ("use" not "utilize")
- [ ] No filler phrases ("in order to" → "to")
- [ ] Concrete numbers and dates (not "soon" or "many")

### Content Flow
- [ ] Business need stated before technical solution
- [ ] Current state shown before proposed state
- [ ] High-level before detailed
- [ ] What's IN scope and what's OUT scope explicit

### Diagrams
- [ ] Diagrams appear before text explanations
- [ ] Each diagram has a purpose (flow, architecture, data)
- [ ] Colors indicate system categories (if applicable)
- [ ] Labels are clear (not A, B, C)
- [ ] Progressive complexity (simple → detailed)

### Technical Details
- [ ] API endpoints include HTTP method and path
- [ ] Tech stack explicitly listed
- [ ] Performance numbers specific
- [ ] Error handling described
- [ ] Authentication/authorization clear

### Completeness
- [ ] Business value articulated
- [ ] Timelines with dates
- [ ] Integration points identified
- [ ] Data described
- [ ] Out of scope explicit

---

## Remember

✅ **Clear beats clever**  
✅ **Simple beats sophisticated**  
✅ **Direct beats diplomatic**  
✅ **Every word must earn its place**  
✅ **Diagrams communicate faster than text**  
✅ **Business language first, technical details second**  
✅ **Explicit scope boundaries prevent confusion**  
✅ **Concrete numbers enable planning**
