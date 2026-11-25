---
name: content-generation
version: 1.0.0
description: Generate structured content artifacts meeting defined requirements for purpose, audience, and quality
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - file:write
    - content:generate
  requires_approval: false
---

# Content Generation

Generate structured content artifacts — documents, reports, proposals, specifications, templates — meeting defined requirements for purpose, audience, format, and quality.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `generate_content` is invoked, you (the agent) follow the methodology below using your writing and reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `synthesis/content-generation` in its skill list.

## When to Use

- Creating a document, report, proposal, or specification from scratch
- Transforming raw data or notes into a polished artifact
- Producing content that must meet specific format and quality requirements
- Generating multiple variants of content for different audiences
- Creating templates or frameworks for repeated use

## Methodology

### 1. Gather Requirements

Before writing a single word, clarify:
- **Purpose**: What should this content accomplish? (inform, persuade, instruct, document)
- **Audience**: Who will read this? What do they already know? What do they need?
- **Format**: What type of artifact? (report, proposal, spec, email, guide, template)
- **Tone**: Formal, conversational, technical, executive?
- **Length**: Expected size (brief paragraph, 1-pager, full document)
- **Key points**: What must be included? What must NOT be included?
- **Constraints**: Style guides, templates, regulatory requirements?

### 2. Create an Outline

Structure the content before drafting:
- Identify 3-7 major sections based on purpose and format
- Order sections for logical flow (context → detail → action)
- For each section, note 2-4 key points to cover
- Verify the outline covers all required key points
- Check: does the structure serve the audience's needs?

### 3. Draft

Write the content following the outline:
- **Lead with the most important information** — don't bury the conclusion
- **One idea per paragraph** — each paragraph earns its place
- **Use concrete language** — specifics over generalities
- **Match audience level** — adjust vocabulary and detail to the reader
- **Include evidence** — claims are supported by data, examples, or citations
- **Use formatting** — headings, lists, tables, and emphasis to aid scanning

### 4. Review

Evaluate the draft against requirements:

**Completeness check:**
- Does it address the stated purpose?
- Are all required key points covered?
- Is anything important missing?

**Audience check:**
- Is the language appropriate for the audience?
- Is the level of detail right (not too shallow, not too deep)?
- Would the audience understand this without additional context?

**Quality check:**
- Is the structure logical and easy to follow?
- Are claims supported by evidence?
- Is the tone consistent throughout?
- Are there redundancies or filler that can be removed?

### 5. Refine

Polish the content:
- Cut ruthlessly — if a sentence doesn't serve the purpose, remove it
- Strengthen weak language — replace hedging with confident statements (when warranted)
- Improve transitions between sections
- Verify formatting is consistent
- Check for factual accuracy

## Output Format

The output format depends on the artifact type. Use the structure that best serves the purpose:

**Report:**
```
# [Title]

## Executive Summary
[Key takeaway in 2-3 sentences]

## [Section 1]
[Content]

## [Section 2]
[Content]

## Conclusions / Recommendations
[Actionable outcomes]
```

**Proposal:**
```
# [Title]

## Problem Statement
[What needs to be solved]

## Proposed Solution
[What you're proposing]

## Benefits
[Why this solution]

## Approach
[How it will be done]

## Requirements
[What's needed]

## Next Steps
[Immediate actions]
```

**Specification:**
```
# [Title]

## Overview
[What this specifies]

## Requirements
### Functional Requirements
[What it must do]

### Non-Functional Requirements
[How well it must do it]

## Constraints
[Limitations]

## Acceptance Criteria
[How to verify]
```

**Guide / How-To:**
```
# [Title]

## Prerequisites
[What you need before starting]

## Steps
1. [Step with explanation]
2. [Step with explanation]

## Troubleshooting
[Common issues and solutions]
```

## Quality Criteria

- Content serves its stated purpose
- Audience can understand and act on it without additional context
- Structure is logical and scannable
- Claims are supported by evidence
- Tone is consistent and appropriate
- No filler, redundancy, or unnecessary hedging
- Formatting enhances readability

## Common Mistakes

- **Writing without clear requirements**: Always clarify purpose and audience first
- **Burying the lead**: Put the most important information first, not last
- **Writing for yourself instead of the audience**: Match vocabulary and depth to the reader
- **Including everything you know**: Include what the audience needs, not everything you found
- **Inconsistent tone**: Mixing formal and casual, or technical and executive, within one document
- **Skipping the outline**: Drafting without structure produces disorganized content
- **Not cutting**: First drafts are always too long. Revision means removal.
- **Format without substance**: Pretty formatting doesn't fix thin content

## Completion

Content generation is complete when:
- The artifact serves its stated purpose
- All required key points are covered
- The audience can understand and act on the content
- The format matches the artifact type
- Review checklist items pass
- Content has been refined (first drafts are never final)
