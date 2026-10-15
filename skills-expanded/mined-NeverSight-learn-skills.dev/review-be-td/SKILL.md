---
name: review-be-td
description: "Review a Backend Technical Design (TD) from a frontend developer's perspective: verify the BE TD exposes everything the FE needs to implement the PRD, and surface gaps or mismatches before FE development begins. Use when the user shares a BE TD and wants to understand what APIs and data contracts the FE will get."
---

# Review BE TD (FE Perspective)

Read a Backend Technical Design as a **frontend developer**: check that the BE TD exposes the APIs, data shapes, and error states the FE needs to implement the PRD requirements. Surface anything missing or unclear that would block FE implementation.

## Execution Flow

### Step 1: Fetch All Documents

Use available tools and MCP servers to fetch:
- The BE TD content. Read all images embedded in it (diagrams, schema screenshots, flow charts).
- The PRD content. Read all images embedded in it (mockups, diagrams, screenshots) — they often contain requirements not written in the text.

After fetching the main PRD, scan it for references to other PRDs (linked URLs or named documents). For each referenced PRD, fetch its content and read all its images.

### Step 2: Understand the FE Repo Context

- Get a lightweight picture of what the current FE repo owns: pages, components, state management, API layer, key domain concepts.
- Scan recent MRs from the last 6 months to identify ongoing FE projects that may intersect with this BE TD. Use git and available repository tools and MCP servers for this.

### Step 3: Extract What the FE Needs from the Backend

From the PRD, identify all FE requirements (UI behavior, display logic, user interactions). For each, determine what the FE will need the backend to provide: data fields to display, actions to trigger, error/loading states to handle.

This becomes the checklist to evaluate the BE TD against in Step 4.

Focus only on the **API contract layer** of the BE TD — endpoints, request/response shapes, error codes, and pagination/filtering contracts. Skip internal BE implementation details such as database schema, internal service logic, caching strategy, infrastructure, or anything the FE never directly interacts with.

### Step 4: Evaluate the BE TD from the FE's Perspective

For each FE need identified in Step 3, check whether the BE TD's API contract satisfies it. Only keep track of:

- **Partial** — BE TD mentions it but the shape, error codes, or edge cases are not clearly defined for FE use.
- **Missing** — BE TD does not expose what the FE needs at all.

Discard fully covered items — do not record or mention them anywhere in the output.

Specifically check:

**Missing (in BE TD, required by PRD):**
- API endpoints the FE needs but the BE TD doesn't define (list, get, create, update, delete, actions)
- Response fields the PRD requires the UI to display but are absent from the BE TD's response shapes
- Error codes/states the FE needs to handle that the BE TD doesn't define
- Pagination, filtering, or sorting contracts the PRD implies but the BE TD omits

**Redundant (in BE TD, not required by PRD):**
- API endpoints the BE TD defines that no PRD requirement maps to
- Response fields returned by the BE TD that the PRD never requires the UI to display

**Existing API changes — compatibility and release sequencing:**
When the BE TD modifies an existing API (not a new endpoint), check:
- Is the change backward-compatible? (e.g. adding optional fields is safe; removing/renaming fields or changing response shape breaks existing FE code)
- If breaking: does the current FE code in the repo depend on the old contract? Check the repo context from Step 2.
- If there is a breaking change or the FE must update alongside the BE, raise a release sequencing concern: who deploys first, and is there a window where FE and BE are mismatched?
- If a versioned endpoint or feature flag is needed to avoid a breaking window, flag it.

Also check:
- Does the TD touch the same area as an ongoing FE project (MR from Step 2)? Flag the conflict and name the branch/MR.

### Step 5: Output the Report

---

## BE TD Review Report (FE Perspective)

### Summary
2–3 sentences. State what the BE TD covers and whether it gives the FE enough to implement the PRD requirements.

### FE Needs vs BE TD Coverage

Only list FE needs that are **Partial** or **Missing** — skip anything fully covered. This section is purely factual: state what is missing or incomplete, no questions. Use this format for each item:

**[Partial / Missing] FE Need**
- Gap: what is missing or unclear in the BE TD.

### Open Questions

Only raise questions that cannot be resolved by reading the BE TD or PRD — things that require a decision or clarification from the BE team. Do not repeat gaps already listed in the Coverage section above. Order by priority (blocking first, then high risk, then nice-to-have clarity). Use this format for each concern:

**[TD / PRD Section]** Question for the BE team.

---

## Tone & Style

- Use bullet points heavily — one idea per bullet, short sentence.
- Avoid long prose paragraphs. If a thought needs more than one sentence, break it into bullets.
- Be direct and concrete.
- Review from the FE's point of view only — do not critique BE architecture or implementation choices.
- Do NOT rewrite the TD or generate code — this skill is review only.
