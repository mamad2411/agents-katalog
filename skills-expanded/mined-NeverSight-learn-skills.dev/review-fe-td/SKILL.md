---
name: review-fe-td
description: Review a Frontend Technical Design (TD) against its PRD and BE TD to verify UI requirement coverage, API contract alignment, and surface gaps before FE implementation begins. Use when the user shares a FE TD and wants to validate it against the product requirements and backend design.
---

# Review FE TD

Review a Frontend Technical Design as a **frontend developer**: verify every FE requirement from the PRD is addressed, confirm the FE TD correctly consumes the BE API contracts, surface gaps or inconsistencies, and raise open questions that must be resolved before implementation starts.


## Execution Flow

### Step 1: Fetch All Documents

Use available tools and MCP servers to fetch the FE TD content. Read all images embedded in it (component diagrams, flow charts).

If `prd` is not provided, scan the FE TD for a link or reference to the PRD and use that. If `be_td` is not provided, scan the FE TD for a link or reference to the BE TD and use that.

Then fetch:
- The PRD content. Read all images embedded in it (mockups, diagrams, screenshots) — they often contain requirements not written in the text.
- The BE TD content. Read all images embedded in it.

After fetching the main PRD, scan it for references to other PRDs (linked URLs or named documents). For each referenced PRD, fetch its content and read all its images.

### Step 2: Understand the Repo Context

- Get a lightweight picture of what the current FE repo owns: pages, components, state management, API layer, key domain concepts.
- Scan recent MRs from the last 6 months to identify ongoing projects: their purpose, the areas of the codebase they touch, and their current status. Use git and available repository tools and MCP servers for this.

### Step 3: Extract In-Scope FE Requirements

Identify all PRD requirements that are the frontend's responsibility (UI behavior, user-facing flows, display logic, interactions, routing). Discard out-of-scope items. This becomes the checklist against which the FE TD is evaluated in Step 4.

### Step 4: Evaluate TD Coverage

For each in-scope FE requirement from Step 3, determine whether the FE TD addresses it:

- **Covered** — TD explicitly describes the design that satisfies this requirement.
- **Partial** — TD mentions it but leaves behavior, edge cases, or display conditions unspecified.
- **Missing** — TD does not address it at all.

**PRD traceability — every FE TD behavior must map to the PRD:**
- For every new or updated UI behavior described in the FE TD, verify it is backed by a PRD requirement. Flag any behavior the FE TD introduces that has no corresponding PRD requirement.

**UI behavior vs. API behavior alignment:**
- Does each UI action (button click, form submit, filter change, etc.) correctly map to the API call the BE TD defines for that action?
- Does the UI's loading, success, and error states match what the BE TD's API actually returns?
- Does the FE TD reflect the correct trigger conditions (e.g. when to call an API, what parameters to send) as implied by both the PRD flow and the BE TD contract?
- Does the FE TD call the correct API endpoints, request parameters, and response fields from the BE TD?
- Does the FE TD make assumptions about API behavior that contradict or are absent from the BE TD?

**Repo convention alignment:**
Using the repo context from Step 2, check whether the FE TD's design follows established patterns in this codebase:
- Does it reuse existing components, hooks, or utilities where the repo already has them, or does it propose duplicating them?
- Does it follow the repo's state management patterns (store structure, action naming, selector conventions)?
- Does it follow the repo's API layer patterns (how services/hooks are structured and named)?
- Does it follow the repo's routing and page structure conventions?
- Does it follow the repo's file and folder naming conventions?
Flag deviations as concerns — not to block the TD, but so the author can align before implementation.

**Ongoing project conflicts:**
- Does the TD touch the same area as an ongoing project (MR from Step 2)? Flag the conflict and name the branch/MR.

### Step 5: Output the Report

---

## FE TD Review Report

### Summary
2–3 sentences maximum. State what the TD covers and the overall verdict (complete, partially complete, or has gaps).

### BE–FE Alignment

Only list mismatches or uncertainties that can be identified by reading both TDs — factual discrepancies, no questions. Omit this section if fully aligned. Use this format for each item:

**[Area]** Factual description of the mismatch between FE TD and BE TD.

### Open Questions

Only raise questions that require a decision or clarification — things that cannot be resolved by reading the TDs or PRD alone. Do not repeat mismatches already listed in BE–FE Alignment above. Focus on convention deviations, missing design decisions, or unclear technical approach. Do not raise concerns about product requirements (those belong in `/review-prd`). Order by priority (blocking first, then high risk, then nice-to-have clarity). Use this format:

**[TD Section]** Question for the author to clarify.

---

## Tone & Style

- Use bullet points heavily — one idea per bullet, short sentence.
- Avoid long prose paragraphs. If a thought needs more than one sentence, break it into bullets.
- Be direct and concrete.
- Do not second-guess FE implementation choices unless they contradict a PRD requirement or the BE TD contract.
- Do NOT rewrite the TD or generate code — this skill is review only.
