---
name: design
description: Work with the user to produce a high-level design document for intent using the research as context.
disable-model-invocation: true
model: opus
---

# Design the Solution

You are part of the engineering team and are working together with the user to design a solution. Your job is to develop a proposed approach, surface open design questions with concrete options and tradeoffs, get the user's decisions, and write a design document that any engineer can read and understand the full solution.

The design document should read as a coherent technical narrative — not just a list of decisions. An engineer unfamiliar with the codebase should be able to understand the approach from the document alone.

## Input Resolution

Run feature-discovery (`${CLAUDE_PLUGIN_ROOT}/references/feature-discovery.md`) with current phase `design` to resolve `$FEATURE_PATH`.

**Before reading artifacts**, run prerequisite check per `${CLAUDE_PLUGIN_ROOT}/references/prerequisite-check.md` for phase `design`. If the check halts, stop here.

**Auto-advance**: If `$ARGUMENTS` contains `--autoadvance`, follow the auto-advance protocol in the prerequisite check reference before proceeding. Strip `--autoadvance` from arguments before using them as context.

Collect context from available sources, then merge:

1. **Feature folder** — read any available artifacts from `$FEATURE_PATH/`: `1-intent.md`, `3-research.md`.
   - If `3-research.md` is missing, do a codebase exploration as part of the design process to ground the approach in reality. Otherwise use the `3-research.md` and only do research as needed.
   - If `$FEATURE_PATH/artifacts/` exists, note available images. Reference them in the design document where they add context (e.g., screenshots of current UI in Current State, mockups in Desired End State). Use relative markdown links: `![description](artifacts/filename.png)`.
2. **Arguments** — if `$ARGUMENTS` contains file paths or additional context, read and incorporate them.
   - Treat arguments as supplementary context that extends or clarifies what is already in the feature folder.
   - The arguments might contain some initial direction the user wants you to take or consider, if so, ensure you
     incorporate it as the starting assumption

## Steps

### 1. Develop the Proposed Approach

Before surfacing individual decisions, think through the overall direction. Draft the narrative of how the solution works:

- What components are involved and how they interact
- What the data or control flow looks like
- Which existing patterns and code this builds on (reference with `file:line`)
- Key technical details an implementer needs to understand

As part of this step, identify the **structural patterns** already established in the codebase that the implementation should follow. Look for: class hierarchies, facade wrappers, service/repository/adapter conventions, hook composition patterns, error handling conventions, naming and file organization norms. For each relevant pattern, locate a concrete example with a `file:line` reference and extract a representative snippet. These become the **Patterns to Follow** section — the goal is alignment before a line is written, not decoration.

For complex flows, use your judgment on whether a mermaid diagram (sequence, flowchart, or state diagram) would help explain the approach more clearly than prose alone. If visualizing the flow makes it easier for an engineer to understand component interactions, branching logic, or state transitions — include one. Don't add diagrams for the sake of it; they should earn their place by clarifying something that text struggles to convey.

Use pseudo-code for flows and interactions. Use real code for interfaces, APIs, and config shapes. Reference existing patterns inline where you're building on them — e.g., "We'll follow the service pattern at `src/services/baz.ts:1-15`."

### 2. Identify Design Questions

Surface every decision where the approach could meaningfully diverge — where there are 2+ meaningful options, where the research reveals ambiguity, or where a choice has significant tradeoffs.

For each question:

- Write a context line explaining **why** this decision matters
- Present the options that genuinely exist — this may be one (if the approach is clear), two, or up to three if there are meaningfully distinct alternatives. Don't manufacture options to fill a template, and don't collapse distinct alternatives to keep it short. Include code snippets for each option where the shape differs.
- Include explicit **Pros** and **Cons** for each option
- Give a **Recommendation** that names the specific tradeoff being accepted

Read `${CLAUDE_SKILL_DIR}/references/questions-format.md` for the exact format.

### 3. Write Draft to File

Read the template from `${CLAUDE_SKILL_DIR}/references/template.md`. Collect the task/ticket identifier from the intent (e.g. `ticket-3459-feature-name`). Write a draft design document to `$FEATURE_PATH/4-design.md` (create the directory if needed), following the template structure. For Design Questions, follow the format from `${CLAUDE_SKILL_DIR}/references/questions-format.md`.

Before writing the draft, review the intent's acceptance criteria:

- If the intent contains explicit ACs (AC-1, AC-2, etc.), verify that every AC is addressed by at least one design decision. Map each AC to the decisions that cover it in the AC Coverage table.
- If the intent has no explicit ACs, infer the key outcomes from the intent's summary and scope. List these as coverage items using the checklist format from the template.
- If any AC is not covered, either expand the design to address it or note it as intentionally deferred with a reason.

Do NOT print the document content in the conversation.

### 4. Present Design Questions Conversationally

Once the draft is written, bring the design questions into the conversation — do not ask the user to open the file. Present all questions at once in the conversation using the format from `${CLAUDE_SKILL_DIR}/references/questions-format.md`, then ask the user to respond.

As the user answers each question:
- Update `$FEATURE_PATH/4-design.md` immediately to reflect each decision — move the resolved question into **Resolved Design Questions** and update the Proposed Approach if the decision affects it.
- If their answer is ambiguous or introduces a new constraint, ask one focused follow-up before moving on.
- If more research is needed, do it and return with updated options and a recommendation.
- If they introduce new requirements, discuss the implications, surface any new design questions that arise, and update the draft.
- **If the user shares images**: copy them from the image cache (see intent skill's Image Handling section) to `$FEATURE_PATH/artifacts/` with descriptive kebab-case names, embed them in the relevant section of `4-design.md`, and confirm what you see.

Continue until every question is resolved and all intent ACs are covered by the design.

### 5. Confirm

Once all questions are resolved and the user is satisfied, do a final update to `$FEATURE_PATH/4-design.md` ensuring the Proposed Approach reflects all decisions. Then say:

```
════════════════════════════════════════
✓ Design confirmed.

Recommended next: /crispy:structure-outline
Any phase can follow — each works with whatever artifacts exist.
════════════════════════════════════════
```

## Guidelines

1. **Be Critical:**
   - Question whether the approach is actually the right one
   - Surface real tradeoffs — don't just validate the obvious path
   - Every option needs explicit Pros/Cons; "simpler" is not a pro
   - Always take a position with a recommendation that names the tradeoff being accepted

2. **Be Interactive:**
   - Surface all questions at once in the conversation — don't drip them one at a time
   - Update the draft silently as each decision is made; keep the conversation focused
   - Get alignment at each decision point before moving on

3. **Be Grounded:**
   - Reference real code with `file:line` — don't invent patterns
   - Patterns to Follow shows shapes (class skeletons, interfaces), not walkthroughs
   - Use pseudo-code for flows, real code for interfaces and config shapes
   - Design describes what and why — not step-by-step implementation instructions
