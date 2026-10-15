---
name: alder-discover-business-questions
description: Use Alder Structural Discovery to find grounded questions about confirmed current work before a Problem is known. Use for "Alderで今の業務の見直しどころを探して" or "ProblemはまだないのでAlderで業務構造を見て". Read-only inquiry; do not infer Pain or propose Optimization candidates. Not design-quality review or functional-condition discovery.
license: MIT
---

# Discover questions about current business structure

Read the bundled [Optional Structural Discovery](references/optimization-review.md#optional-structural-discovery-before-a-problem-is-known) section in full. It is the authority for this separate inquiry. Do not fetch newer guidance or require a manually supplied Alder document.

Read project instructions and the whole relevant current-state Business Design, including connected Activities, Objects, roles, timing and Results. Find the design from the request, declared path or conventional `docs/business-design/`; ask only when unreadable or ambiguous. Record its revision and confirmation basis. If the design does not faithfully establish a relationship needed for inquiry, return a plain design-confirmation question to authoring/quality review. Do not count that incomplete relationship as an improvement observation.

For a few grounded observations, separate Structural Observation, Evidence, Why it may matter, Unknowns and Question. Preserve checks with different purposes even if they share a person, time or Object. A structural relationship alone establishes no actual burden, error, delay, cost, Problem, Pain, benefit or optimum. Do not introduce nonexistent work or a maintained intermediate artifact. Zero observations is valid; people may reject or defer every question.

Keep this inquiry read-only. Do not rewrite Business Design, produce Optimization Candidates/Extreme perspectives, implement changes or update review states. Only an actual human-confirmed operational Problem and Pain level can enter Optimization Review; record/confirm that input in Business Design through the design loop first. If a known Problem was supplied and improvement proposals were requested, use the separate `alder-optimize-business` workflow rather than replacing it with this inquiry.

Return the grounded questions or a brief zero-result explanation, unresolved design confirmations, the installed Alder version from `../../plugin.json`, input revision and [authority provenance](references/provenance.json). Include plugin commit when known. Discovery does not make a business decision.
