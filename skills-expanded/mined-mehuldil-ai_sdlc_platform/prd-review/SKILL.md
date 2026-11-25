# /project:prd-review

**Interactive PRD Review & Gap Analysis**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:prd-review AB#123
/project:prd-review AB#123 --role=backend
/project:prd-review AB#123 --post-comments
```

## What This Does

1. **Loads PRD** from ADO work item
2. **Detects gaps** (missing sections, unclear requirements)
3. **Asks role-specific questions** (perspective-based review)
4. **Generates feedback** with suggested fixes
5. **Captures user notes** in chat for ADO comment
6. **Posts gaps as ADO comments** on the work item (user confirms)

## Interactive Flow

```
User: /project:prd-review AB#123

Claude: 🎯 PRD Review & Gap Analysis

Review from which perspective?
  [1] Product (goals, personas, success metrics)
  [2] Backend (architecture, APIs, data model)
  [3] Frontend (UI flows, user experience)
  [4] QA (test coverage, edge cases)
  [5] All perspectives

User: [2]

✅ COMPLETE SECTIONS:
  • Overview & Goals (clear)
  • User Personas (5 defined)
  • Feature Capabilities (8)
  • NFR Targets (documented)

⚠️ GAPS (Backend perspective):

1. Missing: API Contract Details
   Impact: Can't estimate development effort
   Fix: Define REST endpoints, request/response schemas, error codes
   Priority: BLOCKING (needed before architecture review)

2. Unclear: Async Processing Strategy
   Need: Decision on Kafka/async vs synchronous
   Impact: Architecture differs significantly
   Fix: Specify async requirements per API endpoint
   Priority: BLOCKING

3. Missing: Data Model
   Need: Entity diagrams, table schemas, relationships
   Impact: Database design depends on this
   Fix: Create ER diagram and normalize schema
   Priority: BLOCKING

4. Partial: Error Handling Strategy
   Current: Generic "error states" mentioned
   Need: Specific error codes (e.g., PHONE_INVALID, OTP_EXPIRED)
   Fix: Define error taxonomy with codes + messages
   Priority: MAJOR

5. Missing: Rate Limiting & Security
   Need: API rate limits, auth strategy, validation rules
   Impact: Affects service design
   Fix: Document security requirements + limits
   Priority: MAJOR

BLOCKING items: 3 (API contract, async decision, data model)
MAJOR items: 2 (error handling, security)

What would you like to do with these gaps?
  [1] Add blocking items to PRD now
  [2] Post all gaps as ADO comment on AB#123
  [3] Let me add notes first, then post as comment
  [4] Proceed anyway (risky)

User: [3]

Add your notes for each gap (type in chat):

User: "API contract — need OpenAPI 3.1 spec before arch review.
       Async strategy — discuss in next tech sync.
       Data model — DBA to draft ER diagram by Friday."

✓ Captured your notes.

POST COMBINED COMMENT TO ADO?
  [1] Yes, post gaps + my notes as comment on AB#123
  [2] Edit comment first
  [3] Just save locally
  [4] Cancel

User: [1]

✓ Posted PRD review comment to AB#123 with 5 gaps + user notes
✓ Tagged story: blocked:prd-review
✓ Saved review to .sdlc/memory/prd-review-AB#123.md

GATE G1 STATUS: ⚠️ INCOMPLETE

Gate G1 requires:
  • PRD sections complete ✗ (3 gaps identified)
  • AC stubs present ✓
  • No blocking gaps ✗ (3 blocking gaps)

Status: BLOCKED (gaps posted as comment on AB#123)

PM should:
  1. Review gap comment on AB#123
  2. Complete missing information per the notes
  3. Update PRD work item
  4. Tag as `ready:pre-grooming` when done
```

## CLI Mode

```bash
# Interactive
$ sdlc skill prd-review AB#123 --role=backend

# Auto-post (no confirmation)
$ sdlc skill prd-review AB#123 --role=backend --post-comments

# Batch review across sprint
$ sdlc skill prd-review AB#123 AB#456 AB#789 --post-to-ado
```

## Skill: prd-gap-analyzer

Validates PRD against template (10 required sections):
- Section completeness (all sections present)
- Product type & data policy declaration
- NFR specificity check (p95 latency, error rate, throughput, etc.)
- Success metrics quality (targets + guardrails)
- Acceptance criteria quality (binary, grouped by feature)
- User flows completeness (happy path + edge cases)
- Analytics event schema + drop-off tracking
- License risk scanning (AGPL, GPL detection)
- Cross-pod dependency detection
- Design asset links (Figma, prototypes)
- Open questions audit (all have owners)
- Risk register completeness (probability, impact, mitigation)

## ADO Comment Posting (Gaps)

For identified gaps, posts a **single structured comment** on the work item:
- **Format:** Gap # | Type (BLOCKING/MAJOR) | Description | User Notes
- **Tag added:** `blocked:prd-review`, `claude:generated`
- **No follow-up tasks created** — gaps are tracked via ADO comments
- **User notes:** Captured from chat input before posting

## G1 Gate Clear Conditions

Gate G1 is CLEAR when:
- Epic has no `blocked:prd-review` tag
- All gaps in the posted comment are resolved (PM confirms in reply comment)

## When Status = READY

PM manual actions (3 steps):
1. **Add comment on the Epic:** `G1 Ready`
2. **Update tags:** Remove `blocked:prd-review`, Add `ready:pre-grooming`
3. **Notify TPM** to schedule grooming

> Tag removal and gate sign-off are human actions per rules/guardrails.md

## Next Commands

- `/project:grooming AB#123 --type=master` - Generate master stories
- `/project:architecture-review AB#123` - Architecture feasibility
- `/project:gate-check AB#123` - Check gate status

---

## Model & Token Budget
- **Model Tier:** Sonnet (gap detection + analysis)
- Input: ~2K tokens (PRD content + template)
- Output: ~1.5K tokens (gap analysis + ADO comment)

