# Propose Changes

Analyze a change request and propose documentation updates before implementation.

**Skills to invoke:** Use the `Skill` tool to load relevant skills before acting:
- Always invoke `superpowers:writing-plans` before writing the final plan
- For backend/API changes: invoke `fastapi-patterns` and `api-design`
- For Python logic: invoke `python-patterns`
- For any new feature: invoke `eval-harness` to define acceptance criteria

## Instructions

When the user describes what they want to achieve, follow this process:

### 1. Understand the Request
- What is the user trying to accomplish?
- What problem are they solving?
- What is the scope (small fix vs new feature)?

### 2. Research Current State
Use agents to research in parallel:
- Check existing docs in `docs/need/`, `docs/spec/`, `docs/tech/`
- Check existing code that would be affected
- Identify related features or potential conflicts

### 3. Present Initial Proposal

Show a structured proposal:

#### A. Summary
One paragraph explaining what will change.

#### B. Affected Documents
| Document | Type of Change |
|----------|---------------|
| docs/spec/... | New section |
| docs/tech/... | Update schema |

#### C. Implementation Outline
High-level tasks (not detailed yet).

#### D. Open Questions
Things that need clarification or user decisions.

### 4. Iterate with User

This is a discussion phase. The user may:
- Ask clarifying questions
- Suggest different approaches
- Add constraints
- Request alternatives

Continue refining until user says **"approve"** or **"go"**.

### 5. On Approval

When user approves:

1. **Invoke `superpowers:writing-plans`** via the Skill tool to structure the plan
2. Write the detailed plan to `docs/todo/current_work.md` (follow the plan format from that skill)
3. Write the feature spec to `docs/spec/feat_<name>/SPEC.md` with acceptance criteria
4. Update any doc sections that can be written now
5. Tell user: "Plan saved. Run `/implement` to begin."

## Output Format

```
## Proposal: <Title>

### Summary
<One paragraph explaining the change>

### Affected Areas
- **Docs**: <which docs change>
- **Code**: <which code changes>
- **Data**: <any data/schema impact>

### Approach
<High-level approach, 3-5 bullet points>

### Questions
1. <Decision needed from user>
2. <Clarification needed>

---
*Discuss to refine, or say "approve" when ready.*
```

## Iteration Examples

User: "What about X instead?"
→ Revise proposal, show diff from previous version

User: "I don't want to change Y"
→ Adjust scope, note constraint

User: "Can we do this in phases?"
→ Split into phases, show phase 1 only

User: "approve" or "go" or "looks good"
→ Save plan, prepare for implementation
