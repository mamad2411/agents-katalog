---
name: research
description: Investigate a specific technical question using primary sources and save a cited research note.
---

# Research a bounded question

Identify the decision this research supports, the deliverable, and any existing
budget. Prefer official documentation, papers, source code, and first-party
measurements. Distinguish reported results, your interpretation, and claims that
still need testing in the user's environment.

For a narrow lookup, investigate directly. Delegate only when an independent
question can run alongside useful local work and the host permits delegation.
Give a worker its question, allowed resources, output path, and stopping rule.
Delegated researchers perform the research themselves; they do not recursively
invoke this skill to create more researchers. Honor the host's concurrency limit
and the caller's resource budget. Never create user-visible tasks as a substitute
for an internal worker without a user request.

Stop when the question is answered with adequate evidence, the agreed budget is
reached, or a specific unavailable source blocks the conclusion. Do not expand
into a general survey when the decision no longer needs it. Ask for a budget only
when resource use is material and cannot be inferred; a small lookup needs none.

Save one concise Markdown note in the project's usual location, or at the path
the user requested. Include the question, findings with supporting links,
uncertainties, and the next decision. State source versions or dates when they
matter. If a source is inaccessible, state that limitation rather than treating
its title or an abstract as full verification.
