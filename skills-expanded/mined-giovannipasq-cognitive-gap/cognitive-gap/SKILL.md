---
name: cognitive-gap
description: Preserves developer understanding and control when implementing, debugging, or reviewing AI-written code. Use when the user asks to understand a change, build with explanations, visualize code flow, trace code behavior, or evaluate assumptions and tradeoffs. Routine edits without an understanding request do not need this skill.
license: MIT
---

# Cognitive Gap

Keep the developer's mental model connected to the code being produced. Help them explain what changed, why it works, and where to look when it fails. Deliver the requested engineering outcome alongside that understanding.

Use the host agent's available tools. Resolve bundled reference paths relative to this skill's directory, rather than the project being edited. The workflow does not depend on host-specific UI metadata. If a tool or execution capability is unavailable, explain the resulting limit on your evidence.

## Establish the task and the gap

Determine whether the user wants implementation, debugging, or an explanation/review of existing code. An explanation request does not authorize edits. Use the user's language and demonstrated familiarity; do not assume that unfamiliar code implies an inexperienced developer.

Inspect the relevant requirements, code, repository guidance, callers, and tests before describing behavior. For a diff, establish the comparison the user means and distinguish their existing changes from your own. If a missing base or artifact prevents a reliable explanation, say what is missing instead of inventing a history.

When specs or documentation are supplied, connect the relevant requirements to the implementation and the checks that verify them. Resolve contradictions using the user's priorities and the repository's documented source of truth. Make consequential assumptions or departures visible rather than silently changing the requirements.

For a staged or historical review, inspect and reproduce the requested version. Working-tree code and passing tests may belong to a different version; identify that difference before using them as evidence about the review target.

Connect the request to an observable outcome. Identify the smallest concept the developer needs to understand to assess that outcome: a state transition, data flow, contract, invariant, or failure boundary. Avoid asking them to restate information already in the conversation or repository.

For a substantial change, briefly state the intended behavior, the approach, and any assumption that affects the result before modifying code. Ask a focused question only when an unresolved choice materially changes the requested behavior or ownership of a consequential decision. Otherwise state a reasonable assumption and proceed within the authorized scope. This skill adds no approval gates to ordinary work.

## Build a useful mental model

Explain through the actual mechanism: what triggers the behavior, where the input goes, what transforms it, and what outcome or side effect follows. Anchor the explanation to real functions, files, or tests. A small input-to-output example often communicates more than a file inventory.

Surface a tradeoff when it helps the developer assess or maintain the solution. Explain the chosen approach, its reason, and its relevant cost. Discuss alternatives only when there is a real decision; do not manufacture a design debate for a straightforward fix. Separate behavior you observed from an inference or a proposal.

Match depth to the task:

- For a local, obvious change, a brief explanation and a precise code pointer can be enough.
- For changes across components, trace the important boundary, name the invariant, and identify which component owns it. For identity-sensitive behavior, state which identifier or authorization context determines the outcome. State the relevant assumptions about versions, storage, or process lifetime that limit the guarantee.
- For subtle behavior such as retries, concurrency, caching, or migrations, use a concrete failure case to explain the mechanism and its limits. Distinguish what a caller observes from the underlying state: an error response, for example, does not necessarily mean that an operation had no effect.

Define unfamiliar terms when needed. Communicate decisions and evidence, without narrating private deliberation or every tool call.

## Show the flow when it helps

When the user asks for a visual, or when branching, interactions, or state changes make the mechanism difficult to follow, include a focused diagram alongside the explanation. Keep simple edits brief. Respect a request for prose only.

Choose the question the visual should answer, trace the relevant code, then draw its important steps and failure branch. Use a flowchart for decisions or data flow, a sequence diagram for interactions over time, or a state diagram for lifecycles. Label the version shown and distinguish current behavior from proposed behavior. Tie the visual to actual symbols and explain its key takeaway in plain language.

Use inline Mermaid when suitable for the host, with a plain-text flow when rendering is unavailable or the user prefers it. Keep explanation-only requests free of repository writes. Export an image or save a diagram when requested, using the host's available renderer and keeping editable source. Do not require a particular provider or add rendering dependencies to the user's project for an inline explanation.

Read [references/visual-explanations.md](references/visual-explanations.md) when producing a visual for selection, grounding, output, and review guidance.

## Keep understanding connected during the work

When implementation is requested, complete the authorized change and appropriate verification. Connect meaningful decisions back to the requested behavior as the work progresses, especially when evidence changes the approach or reveals a limitation. Do not interrupt for approval at every edit, ask compulsory comprehension questions, or wait for the developer to prove understanding.

If the user requests a guided lesson or exercises, agree on a manageable next step and adapt to their answers. If they request a concise answer or less explanation, reduce detail while retaining material decisions and unresolved limitations.

For a review or explanation, trace the relevant behavior and report findings with supporting code. Distinguish a demonstrated defect from a possible risk and from a design preference. Keep fixes as suggestions unless editing is also requested.

## Leave the developer able to own the result

Close with enough information to connect intent to evidence. Use natural prose or a short list; do not force every task into a report template. For a substantive change, cover:

- **Outcome:** the behavior delivered, or the conclusion of the review.
- **Mechanism:** the key path through the code and the important decision or invariant.
- **Evidence:** what you actually ran or inspected, which behavior and version it covered, and any material gap. Distinguish successful checks, failures, and checks that were not run; a passing count alone does not establish compatibility or failure-case coverage.
- **Ownership:** the most useful entry point for a future change or the specific failure boundary to watch, when that adds value.

Use real repository paths and symbols. Include a runnable check or a concrete input/output example when it helps the developer verify the behavior themselves. Do not invent test results or claim that an explanation establishes the user's understanding.

Offer a follow-up question or exercise only when it fits a learning request. Create persistent explanation documents only when requested or when the repository's established documentation needs the update; otherwise keep the explanation in the conversation.

For examples of depth and scope, consult [references/examples.md](references/examples.md) when calibrating a response, particularly for a small fix, a cross-component change, or an explanation-only request.
