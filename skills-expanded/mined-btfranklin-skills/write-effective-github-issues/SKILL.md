---
name: write-effective-github-issues
description: "Write, revise, or review GitHub issues for AI agents. Use when asked to draft a ticket, improve an issue, or clarify its scope and acceptance criteria. Explain product value, architecture, implementation, and sufficient verification. Do not use to implement an issue or review code."
---

# Write Effective GitHub Issues

Explain the product benefit, define the outcome, and propose an implementation, in that order. Specify the evidence required to complete the work.

## Establish the context

Read the request and the relevant repository instructions. Inspect the product context, affected code, existing patterns, and required checks when available. Read an existing issue and relevant discussion before revising it. Respect the repository issue template.

Investigate only enough to identify the intended outcome, a feasible approach, and required constraints. Stop research when more detail would not change those decisions. Do not perform a repository audit or implement the change to write its issue.

Separate verified facts, proposed decisions, and unresolved questions. Do not invent product strategy, code locations, commands, or test results. Ask a focused question when missing information changes the purpose, scope, or architectural decision. Continue independent drafting while awaiting the answer. Mark the issue as a draft if an unresolved decision prevents implementation.

## Write the issue

Use a specific title that identifies the intended change. Use the sections below as the default structure. Adapt their headings to the repository template while preserving their purpose and approximate order. Always include a section that explains product value.

Scale detail to the task. A small correction can use short paragraphs. Include conclusions and evidence that affect implementation. Omit the research history and generic engineering advice.

### Why: Product value

Explain the current problem, who it affects, and the benefit of solving it. Connect the change to the larger product goal when the available context supports that connection. State the immediate benefit when broader strategy is unknown.

For internal technical work, explain the effect on a relevant product concern, such as reliability, delivery speed, operating cost, or maintainability. Make the connection specific. Avoid unsupported claims that a change improves quality or scalability.

### What: Outcome and architectural approach

Describe the resulting behavior and its scope. Explain how the change fits the system. Identify responsible components, interfaces, data flow, and constraints only where they affect a decision.

Propose the simplest coherent design that meets the goal. Explain choices that affect behavior, compatibility, or maintenance. Discuss an alternative only when the tradeoff helps the implementer assess the proposal.

Keep component responsibilities and interfaces clear so future changes remain practical. Add flexibility only when a known requirement justifies it. Do not require speculative abstractions, extension systems, compatibility layers, or future features. Separate possible future work from required work.

State which changes are outside scope when an agent could reasonably mistake them for required work.

### How: Implementation proposal

Give a concrete starting point. Include verified code locations, patterns to reuse, likely changes, and dependencies when useful. Specify a sequence only when order matters.

Distinguish required behavior and constraints from suggested methods. Use explicit terms such as "Required" and "Proposed" where the distinction could be unclear. Permit a better implementation that preserves the required outcome and constraints. Resolve decisions about required product behavior before presenting the issue as ready to implement.

Avoid line-by-line instructions, full patches, and rigid internal naming unless they are necessary to preserve an existing contract. Link to precise sources instead of copying large documents or logs. Keep enough context in the issue to explain why each source matters.

### Validation and completion

Include acceptance cases, required checks, validation limits, and a completion rule. Keep these parts brief for small changes.

**Acceptance cases:** Describe observable outcomes. For each case, specify:

- Starting condition or relevant input.
- Action or trigger.
- Expected result.
- Verification method, such as an existing test, a focused regression test, or a manual check.

Use a compact table or a short list. Each case must support a required outcome or address a concrete risk. Reuse existing coverage when it already demonstrates the result. Do not require a new automated test for every case.

Include the main success case and relevant regression or failure cases. Avoid an exhaustive test matrix. Include failure, recovery, authorization, concurrency, or persistence cases only when the affected behavior or a known risk makes them necessary.

**Required checks:** Name the applicable repository checks and any focused verification. Use verified commands when available. Preserve mandatory checks and review gates. Report missing setup as a blocker to the affected check; do not invent a command or claim a pass.

**Validation limits:** Identify checks that add little value for this issue. Keep validation limits separate from changes that are outside scope. Select only relevant examples from this list:

- Duplicate tests for behavior that existing tests adequately cover.
- Tests that repeat internal implementation details without checking behavior.
- Speculative input combinations unrelated to supported use or a concrete risk.
- Broad performance, security, or compatibility investigations unrelated to the change.
- New test infrastructure for a change that existing tools can verify.
- Repeated successful checks without a relevant change or an unresolved concern.

Do not use these limits to dismiss a known defect or omit required verification. Do not use arbitrary time limits or test counts as substitutes for sufficient evidence.

**Completion rule:** State that implementation is complete when the acceptance cases pass, required checks and review gates are satisfied, and no known defect prevents the intended outcome. After that point, stop testing and investigation. Expand validation only when a failure, relevant code change, or concrete unresolved risk justifies it. State why the extra check is needed and what result will resolve the concern. Rerun affected checks after a correction; repeat broader checks only when required or justified by the change.

Instruct the implementer to report any required check that cannot run and the reason. Missing verification does not count as a pass. Keep unrelated findings outside the issue unless they prevent its outcome.

## Review and deliver

Review the draft once against these questions:

- Can an agent explain why the work matters to the product?
- Can it identify the required outcome and constraints without guessing?
- Can it distinguish required behavior from the proposed implementation?
- Does every acceptance case have an observable result and a verification method?
- Does it know which work adds value, which work is outside scope, and when to stop?

Correct concrete gaps. Remove repeated material and details that do not change a decision. Do not start repeated review or proof cycles without a specific unresolved problem.

Use short, direct sentences and active voice. Put one instruction in each sentence. Use one term for one concept. Use "must" for requirements and imperative verbs for recommendations. Do not use "should", contractions, idioms, or promotional language. Preserve exact identifiers, commands, and relevant quoted user text.

Return the issue title and body for a drafting request. Create or update the GitHub issue only when the user authorizes that action. An issue-writing request does not authorize implementation. When revising an existing issue, preserve supported requirements and decisions unless the user changes them.
