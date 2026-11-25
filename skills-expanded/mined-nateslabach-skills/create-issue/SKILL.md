---
name: create-issue
description: Craft a single, high-quality GitHub issue from a developer's description of a bug, unexpected behavior, or desired enhancement. Walks through reproduction, codebase exploration, and structured drafting so the issue is actionable on arrival. Use when user wants to file an issue, report a bug, request a feature, or document a problem they've encountered.
---

# Create Issue

Turn a developer's rough description of a problem or idea into a single, well-structured GitHub issue that is actionable the moment someone reads it.

This skill produces **one issue at a time**.

## Principles

### Actionable on arrival

A good issue lets someone start working without asking follow-up questions. Every issue must answer: what happened (or what should happen), how to see it, and how to know it's fixed.

### Behavioral, not procedural

Describe **what** the system does vs what it should do. Avoid file paths and line numbers — they go stale within hours. Name types, interfaces, and behavioral contracts instead.

### Honest about unknowns

If reproduction is intermittent, say so. If the root cause is unclear, say so. An honest "cause unknown, here's what I've ruled out" is more useful than a guess that sends someone down the wrong path.

## Process

### 1. Understand the problem

Work from whatever the developer tells you. Ask clarifying questions **one at a time** — don't dump a questionnaire. Focus on:

- **What happened** — the actual behavior they observed
- **What they expected** — the behavior they wanted
- **When it started** — did it work before? What changed?
- **How often** — every time, sometimes, once?

If the developer passes an issue reference, error message, stack trace, or log output, use that as your starting point instead of asking them to re-describe it.

Stop asking when you have enough to write a clear description. Two or three targeted questions is usually enough — don't grill beyond what the issue needs.

### 2. Explore the codebase

If you have access to the codebase, explore the area relevant to the problem. Look for:

- The domain vocabulary used in this area (use the project's `CONTEXT.md` glossary if one exists)
- Existing tests that cover the behavior
- Related issues or TODOs in the code
- ADRs that explain decisions in this area

Use what you find to write the issue in the project's own language, not the developer's paraphrase.

### 3. Attempt reproduction (bugs only)

For bug reports, trace the relevant code path and run existing tests if possible. Do not claim a reproduction you didn't actually observe — an honest "could not reproduce" is more useful than a fabricated one.

Report what you find:

- **Reproduced** — describe the exact steps and what you observed
- **Partially reproduced** — you saw related behavior but not the exact symptom
- **Could not reproduce** — describe what you tried

A confirmed reproduction with a code path makes a dramatically stronger issue. But a failed reproduction is still valuable — note it in the issue so the next person doesn't repeat your work.

### 4. Classify

Determine the issue type:

- **Bug** — something is broken or behaving contrary to its documented/intended behavior
- **Enhancement** — new capability or improvement to existing behavior

A thing that "works" but produces wrong results is a bug, not an enhancement. If the distinction is genuinely unclear from the description alone, ask rather than guess — misfiling an enhancement as a bug skews labeling and metrics.

### 5. Draft the issue

Write the issue using the template below. Present the draft to the developer and ask:

- Does this accurately describe the problem?
- Is anything missing or overstated?

Iterate until the developer approves.

### 6. Publish

Attempt to post the approved issue to the issue tracker using an available tool (e.g. `gh` CLI or GitHub MCP). Apply the agreed labels. Report back the issue number and URL.

If no publishing tool is available, output the final issue body as a fenced markdown block so the developer can paste it manually:

````markdown
[issue body here]
````

## Issue body template

### Bug

**Summary**

One or two sentences: what is broken, and what is the impact.

**Current behavior**

What the system does now. Be specific — include error messages, wrong outputs, or unexpected states. Paste stack traces or logs in a code block if available.

**Expected behavior**

What the system should do instead. Reference documented behavior, type contracts, or prior working behavior if applicable.

**Steps to reproduce**

1. Step one
2. Step two
3. Step three

**Environment** *(include only fields relevant to this bug)*

- Runtime:
- OS:
- Browser / client:
- Relevant config:

**Frequency:** Every time / Intermittent (~X% of attempts) / Once

**Investigation notes**

What has been explored so far: code paths traced, hypotheses tested, things ruled out. Omit this section if no investigation has been done.

**Acceptance criteria**

- Criterion 1
- Criterion 2

---

### Enhancement

**Summary**

One or two sentences: what capability is missing or what improvement is proposed.

**Motivation**

Why this matters. Describe the user problem or workflow gap — not the solution. If this came from a real scenario, describe it.

**Proposed behavior**

What the system should do. Describe the end-to-end behavior from the user's perspective. Mention key interfaces or types that would be involved if they already exist in the codebase.

**Alternatives considered**

Other approaches and why they are less suitable. Omit if there is genuinely only one reasonable approach.

**Open questions**

Design decisions or unknowns that should be resolved before implementation begins. Omit if none.

**Acceptance criteria**

- Criterion 1
- Criterion 2
- Criterion 3

## Operating rules

- Ask clarifying questions one at a time — never more than one per message
- Do not skip the draft-and-review loop even if the developer says "just file it"
- Never publish without explicit developer approval of the draft
- Do not add file paths or line numbers to the issue body
- If you cannot reproduce a bug, say so — do not fabricate or imply a reproduction
- Output a copyable markdown block any time publishing fails or no tool is available

## What makes a bad issue

Avoid these — they waste everyone's time:

- **Vague symptoms:** "it's broken" / "doesn't work" / "something is wrong with X"
- **Solution-first:** jumps to "add a flag" or "change the config" without stating the problem
- **Stale references:** file paths, line numbers, or commit SHAs that will drift within days
- **Missing reproduction:** "I saw an error" with no steps, environment, or frequency
- **Kitchen-sink scope:** five different problems bundled into one issue

If the developer's description falls into any of these, the grilling in Step 1 should fix it before the issue is written.
