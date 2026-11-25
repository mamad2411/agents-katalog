---
name: Research
description: Investigate documentation, APIs, or prior art and return a cited, decision-ready brief. Use when the answer depends on external facts or an unfamiliar codebase.
---

# Research

Research ends with a decision the user can act on — not a pile of links.

## 1. Define the question

- Restate the concrete question in one sentence.
- List what would make the answer actionable: version constraints, runtime, budget, deadline, compatibility.
- Separate facts that must be verified from preferences.

## 2. Gather

- Prefer primary sources: official docs, source code, release notes, specifications.
- Use `web_fetch` on specific documentation pages, not search-result fragments.
- For local code, trace definitions and call sites; cite `path:line`.
- Record publication dates and versions. A 2022 answer may be stale.
- For conflicting sources, note the conflict rather than averaging it away.

## 3. Synthesize

- Lead with the answer in 2–3 sentences.
- Support with a short evidence table: claim → source → date/version.
- Name tradeoffs and the conditions under which the recommendation flips.
- Mark uncertainty explicitly. Distinguish "documented" from "inferred".
- Include exact commands or code only when verified.

## 4. Deliver

- Link every external claim.
- Keep quotes short.
- Offer the next concrete step.
- If the sources are insufficient, say so and state what evidence is missing.

## Guardrails

- Never invent URLs, versions, benchmarks, or quotes.
- Do not treat a marketing page as independent evidence.
- Avoid exfiltrating private repository content to external services unless the user asked.
