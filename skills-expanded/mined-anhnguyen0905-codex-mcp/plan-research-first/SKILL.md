---
name: plan-research-first
description: Research-first planning — search for existing implementations, libraries, and in-repo patterns before designing anything new. Adopt proven solutions over net-new code.
---

# Research First

Never design from a blank page. Cheapest code is code you don't write; second cheapest follows a pattern that already works.

## Order of research (stop at the first sufficient hit)

1. **This codebase** — Is there an existing feature that does 80% of this? Follow its structure, naming, error handling, and test style exactly. Grep for similar routes/components/services before inventing new ones.
2. **Installed dependencies** — Does a library already in package.json/pyproject/go.mod solve it? Prefer using what's installed over adding anything.
3. **Package registries** (npm/PyPI/crates/Go modules) — For utility problems (dates, validation, parsing, retries), a battle-tested library beats hand-rolled code. Check: weekly downloads, last release date, open issues, license.
4. **Reference implementations** — `gh search code`/`gh search repos` and official docs for how others solved the same problem; port the approach, not the code.

## What to record in PLAN.md

For each significant choice: what was found, what was chosen, and why the alternatives lost — one line each. This stops the "why didn't we just use X?" review round. Record any **new dependency** under PLAN.md's *Risk & blast radius* (with license + maintenance status), and reflect a reused in-repo pattern in the *Contracts* / *Component → files* sections so the backlog slices along it.

## Guardrails

- New dependency = a decision the user should see in the plan, with license and maintenance status noted.
- Do NOT hand-roll: crypto, auth/session logic, date/timezone math, parsers for standard formats (CSV/YAML/JWT), retry/backoff. Libraries exist and get these right.
- Do NOT add a dependency for something under ~20 lines of obvious code (left-pad rule).
- Version-check assumptions: confirm API shapes against the installed version's docs, not memory.
