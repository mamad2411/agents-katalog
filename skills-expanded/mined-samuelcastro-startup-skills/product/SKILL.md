---
name: product
description: Guide founders through product documentation, planning, and execution. Use when a founder says "help me write a PRD", "create a product roadmap", "write user stories", "prioritize features", "scope this feature", "product requirements", "acceptance criteria", "what should we build next", or needs to articulate product vision for teams or investors.
---

# Product Planning & Documentation

Guide founders from product idea through PRD, roadmap, and user stories to execution-ready specifications.

## Workflow

### 1. Diagnose Current Need

Ask: "What product documentation do you need?"

| Need | Signals | Next Step |
|------|---------|-----------|
| **PRD/Spec** | "Help me write a PRD", "spec out this feature" | → Step 2: Write PRD |
| **Roadmap** | "Prioritize features", "what should we build next" | → Step 3: Build Roadmap |
| **User Stories** | "Write user stories", "acceptance criteria" | → Step 4: Write User Stories |
| **Vision Doc** | "Product strategy", "investor deck product section" | → Step 5: Product Vision |
| **All of the above** | New product, starting from scratch | → Start with Step 2 |

### 2. Write the PRD

A PRD articulates the "what" and "why"—not the "how." Engineering and design determine solutions.

**Lenny Rachitsky's Three-Step Framework:**
1. Crystallize the problem you're solving
2. Align on the problem with team/stakeholders
3. Keep referring back to the problem throughout

**PRD Structure (Kevin Yien/Square Template):**

See `references/prd-templates.md` for complete templates.

**Core Sections:**

| Section | Purpose | Key Questions |
|---------|---------|---------------|
| **Problem Alignment** | Why we're doing this | What problem? Why does it matter? What evidence? |
| **Goals** | What success looks like | Measurable + immeasurable goals |
| **Non-Goals** | What we're NOT doing | Explicit scope boundaries |
| **Solution Alignment** | What we're building | Key features, flows, logic |
| **Launch Plan** | How we ship | Milestones, dates, criteria |

**Problem Statement Template:**
```
[Target user] struggles with [problem] because [root cause].
We believe [solution approach] will work because [evidence/insight].
```

**Critical Rules:**
- Don't continue past Problem Alignment until ALL contributors are aligned
- Keep it to one page if possible (Paul Adams/Intercom: "The longer the doc, the less it gets read")
- Link out to detailed specs, don't embed everything
- Define Non-Goals as clearly as Goals—this prevents scope creep

**PRD Quality Checklist:**
- [ ] Problem is clear in 1-2 sentences
- [ ] Evidence/customer insights support the problem
- [ ] Goals are specific and measurable
- [ ] Non-goals explicitly defined
- [ ] Success criteria are testable
- [ ] All contributors have signed off on problem before solution

### 3. Build the Roadmap

Roadmaps communicate strategy and vision—they are NOT execution plans.

**Kevin Yien's Roadmapping Maxims:**
- Don't think about what to build WHILE making the roadmap
- Focus on "high conviction big bets," not 25 small items
- Build roadmap AFTER you identify OKRs, not before
- Have specific target numbers, not "low/medium/high impact"
- Build in wiggle room—roadmap items should drive 110%+ of OKR

See `references/roadmap-prioritization.md` for framework details.

**Prioritization Framework Selection:**

| Framework | Best For | How It Works |
|-----------|----------|--------------|
| **RICE** | Data-driven teams, comparing many ideas | Score: (Reach × Impact × Confidence) ÷ Effort |
| **MoSCoW** | MVP definition, stakeholder alignment | Must-have, Should-have, Could-have, Won't-have |
| **Value vs. Effort** | Quick decisions, visual thinkers | 2×2 matrix plotting value against effort |
| **Cost of Delay** | Time-sensitive decisions | Revenue/value lost by waiting |
| **Opportunity Scoring** | Jobs-to-be-done approach | Importance vs. satisfaction gap |

**RICE Scoring (Intercom Method):**

| Factor | Definition | Scoring |
|--------|------------|---------|
| **Reach** | How many users affected per time period | Actual number (e.g., 500 users/month) |
| **Impact** | Effect on individual users | 3=Massive, 2=High, 1=Medium, 0.5=Low, 0.25=Minimal |
| **Confidence** | How sure are you | 100%=High, 80%=Medium, 50%=Low |
| **Effort** | Person-months to complete | Whole numbers (e.g., 2 person-months) |

**Formula:** `RICE Score = (Reach × Impact × Confidence) ÷ Effort`

**MoSCoW Definitions:**
- **Must-Have:** Product literally won't work without it. Non-negotiable.
- **Should-Have:** Important but not critical. Can ship without temporarily.
- **Could-Have:** Nice to have. Build if time permits.
- **Won't-Have:** Explicitly out of scope. May reconsider later.

**Roadmap Format Options:**
- **Now/Next/Later:** Good for early stage, avoids false precision on dates
- **Quarterly:** Standard for growth stage, ties to OKRs
- **Timeline:** Visual Gantt-style, good for stakeholder communication

### 4. Write User Stories

User stories capture requirements from the user's perspective, enabling conversation between product and engineering.

**Standard Format:**
```
As a [user type],
I want [action/goal],
So that [benefit/outcome].
```

**The 3 C's (Ron Jeffries):**
1. **Card:** The written story—brief placeholder for conversation
2. **Conversation:** Discussion that reveals details and context
3. **Confirmation:** Acceptance criteria that define "done"

See `references/user-stories.md` for complete framework.

**INVEST Criteria (Bill Wake):**

Every good user story should be:

| Criterion | Meaning | Why It Matters |
|-----------|---------|----------------|
| **I**ndependent | Can be built without depending on other stories | Flexible prioritization |
| **N**egotiable | Details can evolve through conversation | Enables collaboration |
| **V**aluable | Delivers clear value to user | Keeps focus on outcomes |
| **E**stimable | Team can estimate size | Enables planning |
| **S**mall | Completable in one sprint | Reduces risk |
| **T**estable | Has clear acceptance criteria | Defines "done" |

**Writing Acceptance Criteria:**

Use Given/When/Then format (BDD style):
```
Given [precondition/context],
When [action is taken],
Then [expected result].
```

**Example:**
```
User Story:
As a customer, I want to filter products by price range
so that I can find items within my budget.

Acceptance Criteria:
- Given I am on the product listing page
- When I set min price to $50 and max price to $100
- Then only products priced between $50-$100 are displayed
- And the filter values persist when I navigate back
- And I can clear filters to see all products again
```

**Story Splitting Techniques:**

When stories are too big, split by:
- **Workflow steps:** Registration → Onboarding → First action
- **Business rules:** Happy path → Edge cases → Error handling
- **Data types:** Text → Images → Video
- **Operations:** Create → Read → Update → Delete
- **User types:** Admin → Power user → Basic user
- **Platforms:** Web → Mobile → API

**Common Story Smells:**
- Too many acceptance criteria (>5-7) → Split the story
- Technical tasks disguised as stories → Reframe around user value
- "And" in the middle → Probably multiple stories
- Can't demo to stakeholder → Not valuable enough

### 5. Product Vision Document

For communicating product strategy to investors, board, or new team members.

**One-Page Product Vision:**

```markdown
## [Product Name] Vision

**Mission:** [One sentence—why the product exists]

**Target User:** [Specific persona with key characteristics]

**Problem:** [The pain point in user's words]

**Solution:** [How we solve it differently]

**Key Value Proposition:** [Why users choose us over alternatives]

**North Star Metric:** [Single metric that captures value delivery]

**Current State:**
- Users: [Number]
- Key metric: [Value]
- Stage: [MVP/Growth/Scale]

**12-Month Vision:**
[What the product looks like in a year—paint the picture]

**Key Bets:**
1. [Bet 1]: [Hypothesis and expected outcome]
2. [Bet 2]: [Hypothesis and expected outcome]
3. [Bet 3]: [Hypothesis and expected outcome]
```

## Deliverables

### 1. PRD Document

Create using `docx` skill with structure from `references/prd-templates.md`:
- Problem Alignment section with evidence
- Goals and Non-Goals
- Key Features (prioritized)
- Key Flows (visual or written)
- Key Logic (edge cases, business rules)
- Launch Plan with milestones
- Operational checklist
- Changelog for updates

### 2. Prioritized Roadmap

Create using `xlsx` skill:
- Feature/initiative list with descriptions
- RICE scores (or chosen framework scores)
- Priority ranking
- Time horizon (Now/Next/Later or quarters)
- Dependencies flagged
- Owner assigned

### 3. User Stories with Acceptance Criteria

Format options:
- Markdown file organized by epic
- Spreadsheet with columns: ID, Story, Acceptance Criteria, Priority, Estimate
- Individual story cards

Each story includes:
- User story in standard format
- 3-7 acceptance criteria in Given/When/Then
- Priority (MoSCoW or numerical)
- Estimate (story points or t-shirt size)

### 4. Product Vision One-Pager

Create using `docx` or markdown:
- Mission statement
- Target user profile
- Problem/solution summary
- North star metric
- Current state snapshot
- 12-month vision narrative
- Key strategic bets

## Anti-Patterns to Avoid

**PRD Mistakes:**
- Writing the solution before aligning on the problem
- PRD becomes 20+ pages nobody reads
- No explicit Non-Goals (leads to scope creep)
- Skipping stakeholder alignment signatures
- Treating PRD as static (it's a living document)

**Roadmap Mistakes:**
- Using roadmap as execution plan (too granular)
- Committing to specific dates too early
- No clear prioritization framework
- Building what's loudest, not most valuable
- Roadmap doesn't connect to OKRs/strategy

**User Story Mistakes:**
- Stories written by PM in isolation (no conversation)
- Technical tasks instead of user value
- Vague acceptance criteria ("works correctly")
- Stories too large to complete in sprint
- Missing the "so that" (the why)

## Reference Files

- `references/prd-templates.md` — Kevin Yien, Lenny, Intercom templates with examples
- `references/roadmap-prioritization.md` — RICE, MoSCoW, and other frameworks in detail
- `references/user-stories.md` — INVEST criteria, story splitting, acceptance criteria patterns

## Integration with Other Skills

- Use `idea-validation` skill first if problem not validated
- Use `business-model` skill for pricing/monetization sections
- Use `fundraising` skill for investor-facing product narrative
- Use `docx` skill for PRD document creation
- Use `xlsx` skill for roadmap spreadsheets
- Use `pptx` skill for product review presentations

---

*Adapted from [Linas Beliūnas's](https://linas.substack.com/p/onepersonunicorn) **The One-Person Unicorn** founder skill set.*
