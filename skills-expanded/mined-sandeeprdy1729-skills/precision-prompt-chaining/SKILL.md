---
name: precision-prompt-chaining
description: >
  Multi-step prompt chaining skill where each step's output becomes the next
  step's input, with explicit rules, constraints, and reference tokens between
  steps. Activates when the user needs to build a complex pipeline of dependent
  Claude calls — research → outline → draft → edit → publish — where downstream
  steps must be constrained by upstream outputs without hallucination or drift.
  Designs chains with named output variables, explicit pass rules, validation
  gates between steps, and failure recovery conditions.
  Use when user says: build a chain, multi-step prompt, pipeline of prompts, chain
  these steps, step by step with outputs, connect prompts, feed output into next
  prompt, automate a workflow, prompt pipeline, chained calls, sequential reasoning,
  dependent steps, chain of thought at scale, compound prompt.
  Do NOT activate for: single-turn questions, simple back-and-forth conversation,
  cases where one prompt is sufficient for the task.
  First response: "Prompt Chain Builder active. Describe the full workflow you
  want to automate — input, end goal, and any steps you've already identified.
  I'll design the chain architecture."
license: Apache 2.0
---

# Precision Prompt Chaining

Most "multi-step" prompting is just a list of instructions in one message. That's
not chaining. Real chaining is architecture: named outputs that become typed inputs,
explicit contracts between steps, validation gates that catch drift before it
propagates, and recovery logic for when a step produces garbage.

The failure mode is context pollution — by step 4, the model has forgotten the
constraints from step 1 and is happily hallucinating. This skill prevents that by
making the reference explicit at each step and using output tokens that the next
prompt must satisfy.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/design <workflow>` | Design the full chain architecture for a described workflow |
| `/step <n> <description>` | Write the prompt for a specific step in the chain |
| `/validate <step> <output>` | Check whether a step's output satisfies its contract |
| `/gate <step>` | Write the validation gate between two steps |
| `/vars` | Show all named output variables currently defined in the chain |
| `/inject <var> <value>` | Manually inject a variable value into the chain context |
| `/debug <step> <bad-output>` | Diagnose why a step's output drifted from spec |
| `/recover <step>` | Write a recovery prompt for when a step produces invalid output |
| `/compress <step>` | Summarize a step's output to only what downstream steps need |
| `/full-chain` | Output the complete chain as executable prompts, in order |
| `/dry-run` | Simulate the chain with mock data to expose weak steps |

---

## HIGH-LEVEL WORKFLOW

```text
User describes an end-to-end workflow
    │
    ├─ Phase 1: Chain Decomposition
    │     Break into atomic steps, each with one responsibility
    │
    ├─ Phase 2: Contract Definition
    │     Define named output variables and their format requirements
    │
    ├─ Phase 3: Step Prompts
    │     Write each step's prompt with explicit input references
    │
    ├─ Phase 4: Validation Gates
    │     Insert checks between steps that catch drift early
    │
    ├─ Phase 5: Recovery Logic
    │     Define what happens when a gate fails
    │
    └─ Phase 6: Compression
          Strip each step's output to only what downstream steps need
```

---

## PHASE 1 — CHAIN DECOMPOSITION

### Decomposition rules

1. **One responsibility per step.** A step that "researches and outlines" is two steps.
2. **Steps must be sequentially dependent.** If two steps don't depend on each other, they can run in parallel — design them that way.
3. **Name every step.** Steps are referenced by name in downstream prompts, not by position.
4. **Identify the single output** of each step. Multiple outputs = the step needs splitting.

### Decomposition format

```text
STEP: [step-name]
  INPUT:  {variable_name} (from step: [source-step] | from user)
  TASK:   [one sentence: what this step does]
  OUTPUT: {variable_name} — [format description]
  GATE:   [what must be true for output to pass to next step]
```

### Common chain patterns

| Pattern | Steps | Use case |
| --- | --- | --- |
| **Research → Synthesize → Write** | 3 | Article, report, long-form |
| **Extract → Validate → Transform** | 3 | Data pipeline, migration |
| **Plan → Critique → Revise → Finalize** | 4 | Strategy, code, documents |
| **Intake → Classify → Route → Execute** | 4 | Support triage, content moderation |
| **Brainstorm → Rank → Develop → Evaluate** | 4 | Product ideation, engineering design |
| **Analyze → Hypothesize → Test → Report** | 4 | Research, debugging, auditing |

---

## PHASE 2 — CONTRACT DEFINITION

Every step in the chain is a contract. The prompt is the spec. The output is the
delivery. Downstream steps treat the output as a dependency, not a suggestion.

### Variable naming rules

- Use `{SNAKE_CASE}` for variables referenced across steps
- Suffix with type: `{OUTLINE_LIST}`, `{SUMMARY_TEXT}`, `{SCORE_NUMBER}`, `{DECISION_BOOL}`
- A variable undefined in the current step context cannot be referenced

### Contract definition format

```text
CONTRACT: {VARIABLE_NAME}
  Producer:    [step that creates this]
  Consumers:   [steps that read this]
  Format:      [exact format — markdown list, JSON object, plain text, etc.]
  Max length:  [token or word limit]
  Must contain: [required elements]
  Must not contain: [forbidden content — opinions, caveats, links, etc.]
```

### Anti-drift rules

| Rule | Rationale |
| --- | --- |
| Never pass a full previous response to the next step | Downstream model reads everything — including its own drift |
| Strip step outputs to the defined contract before injecting | 80% of downstream hallucination comes from noise in upstream context |
| Re-state the original goal at every step | Each prompt is a fresh model context; it has forgotten the user's intent |
| Use explicit reference tokens: "Using ONLY {VAR}, ..." | Prevents the model from augmenting with its own knowledge mid-chain |
| End every step prompt with a format enforcement clause | The last instruction wins; put format requirements last |

---

## PHASE 3 — STEP PROMPT TEMPLATE

Every step prompt follows the same structure:

```text
## Context
You are performing step [N] of a [N]-step pipeline.
Your job in this step: [one sentence].

## Inputs
{VARIABLE_FROM_PREVIOUS_STEP}

## Instructions
[Specific instructions for this step only.]

Using ONLY the content in the inputs above — do not add information from your
own knowledge unless explicitly instructed.

## Output Format
[Exact format specification — schema, headers, length limit, etc.]

Output NOTHING except the formatted result. No preamble. No explanation.
```

### Step prompt rules

- **Re-state the goal from step 1** in every step that produces final-facing content
- **Reference variables by exact name** in curly braces: "Summarize {RESEARCH_NOTES} into..."
- **Specify maximum length** for every output — token creep accumulates across steps
- **Forbid caveats in output** unless the step is a critique step
- **End with format constraint** — the last sentence determines compliance most reliably

---

## PHASE 4 — VALIDATION GATES

A validation gate is a lightweight check prompt inserted between two steps. It prevents
bad output from propagating downstream, where it becomes expensive to fix.

### Gate prompt template

```text
## Gate Check: [step-name] → [next-step-name]

Review the following output from step [step-name]:

{STEP_OUTPUT}

Answer ONLY with PASS or FAIL, followed by one sentence.

PASS if ALL of the following are true:
  - [contract requirement 1]
  - [contract requirement 2]
  - [contract requirement 3]

FAIL if ANY of the following are true:
  - [failure condition 1]
  - [failure condition 2]
```

### Gate failure handling

| Failure type | Recovery action |
| --- | --- |
| Format invalid | Re-run the step with stricter format instruction |
| Content missing | Re-run with explicit instruction to include missing element |
| Hallucination detected | Re-run with explicit instruction: "Base answer ONLY on {INPUT_VAR}" |
| Output too long | Run a compression step before passing to gate |
| Contradicts upstream output | Re-run with both conflicting outputs and explicit resolution instruction |

---

## PHASE 5 — COMPRESSION

Long step outputs contaminate downstream context. Before passing an output to the
next step, compress it to only what the downstream step actually consumes.

### Compression prompt template

```text
Below is the output of [step-name]. Extract ONLY the following elements,
discarding everything else:

[element 1]: {description}
[element 2]: {description}

Output as:
{ELEMENT_1}: [content]
{ELEMENT_2}: [content]

Do not explain. Do not add context. Output nothing else.
```

### Compression rules

- Compress after every step that produces more than 500 words
- Name the compression output as a new variable: `{STEP_NAME_COMPRESSED}`
- Downstream steps reference the compressed version, not the raw output
- Never compress a critique step — critique value is in the detail

---

## OUTPUT FORMAT

When `/design` or `/full-chain` is called, output:

```text
CHAIN: [workflow name]
STEPS: [N]
VARIABLES: [list of all named variables]

─── STEP 1: [name] ───────────────────────────────────────
INPUT:  (user)
OUTPUT: {VARIABLE_NAME}
PROMPT:
[full step prompt]

GATE → STEP 2:
[full gate prompt]

─── STEP 2: [name] ───────────────────────────────────────
INPUT:  {VARIABLE_NAME}
OUTPUT: {VARIABLE_NAME_2}
PROMPT:
[full step prompt]
...
```
