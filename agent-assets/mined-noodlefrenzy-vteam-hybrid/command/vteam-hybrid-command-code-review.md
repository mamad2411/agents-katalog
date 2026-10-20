<!-- agent-notes: { ctx: "multi-lens code review + migration + API compat + perf", deps: [docs/methodology/personas.md, .claude/agents/code-reviewer.md, docs/performance-budget.md, docs/security/threat-model.md], state: active, last: "grace@2026-02-15" } -->
Run a multi-perspective code review on the current changes.

This combines three persona lenses from the v-team (see `docs/methodology/personas.md`), plus situational checks for migrations, API changes, and performance. Review the staged/unstaged changes or the most recent commits and apply each lens.

---

## Lens 1: Vik (Simplicity, Maintainability & Performance)

Review through the eyes of a veteran engineer asking "could a junior understand this at 2am during an incident?"

- Unnecessary complexity or abstraction?
- Clever code that should be obvious code?
- N+1 queries or hidden performance issues?
- Concurrency risks?
- Naming that obscures intent?
- Is the code organized so that the next person can find things?
- **Performance:** Does this change affect a hot path? Check against `docs/performance-budget.md` if it exists. Flag allocation patterns in loops, bundle size impacts, resource leaks.

---

## Lens 2: Tara (Test Quality & Coverage)

Review through the eyes of a testing expert:

- Are the new/changed code paths covered by tests?
- Are unhappy paths and edge cases tested?
- Do tests verify behavior or implementation details? (Prefer behavior.)
- Is the test pyramid balanced? (Too many e2e? Not enough unit?)
- Are test names descriptive enough to serve as documentation?
- Any flaky test risks (timing, ordering, external dependencies)?
- **Test strategy alignment:** Does coverage match `docs/test-strategy.md` if it exists?

---

## Lens 3: Pierrot (Security Surface)

Review through the eyes of a security and compliance expert:

- Auth or authorization changes? Are they correct?
- User input being handled safely? (Injection, XSS, SSRF?)
- Secrets or credentials exposed?
- New dependencies introduced? Any known vulnerabilities or license issues?
- Data handling changes? (PII, encryption, logging sensitive data?)
- New attack surface exposed? If so, does `docs/security/threat-model.md` need updating?

---

## Situational Checks (apply when relevant)

### Migration Safety (if the diff includes schema/data changes)

Invoke Archie's migration safety review:

- Is this migration reversible?
- Is it backward-compatible with the currently running version?
- Does it preserve existing data?
- What's the performance impact on production-sized tables?
- Flag any migration that fails these checks as **Critical**.

### API Contract Compatibility (if the diff changes an API surface)

Invoke Archie's API lens:

- Does this change break any existing consumers?
- If breaking: is it properly versioned? Is there a deprecation timeline?
- Does the API spec (OpenAPI, GraphQL schema, protobuf) reflect the change?

---

## Output

Organize findings by lens and severity:

- **Critical** — Must fix before merging. Security vulnerabilities, data loss risks, broken functionality.
- **Important** — Should fix. Maintainability issues, missing test coverage for key paths, potential performance problems.
- **Suggestion** — Consider fixing. Style, naming, minor improvements.

If no issues found for a lens, say so explicitly — a clean bill of health is useful information.

---

## Review Document

For non-trivial reviews (M-sized or larger changes, Critical/Important findings, new patterns, or anything with teaching value), write a review document to `docs/code-reviews/{{date}}-<topic>.md`. These serve as learning artifacts for early-career developers.

The document should include context, all findings with explanations of *why* they matter (not just what's wrong), and a **Lessons** section with generalizable takeaways. See the code-reviewer agent definition for the full template.

When in doubt about whether a review is "large enough" to document — document it. The cost of an extra doc is low; the cost of lost knowledge is high.

---

## Tracking Artifact

After the review is complete, produce `docs/tracking/YYYY-MM-DD-<topic>-review.md` summarizing the review findings (Critical/Important/Suggestion counts), key issues found, and resolution status. If a full review document was written to `docs/code-reviews/`, link to it. Use the standard tracking format from `docs/process/tracking-protocol.md`. Set **Prior Phase** to the most recent implementation artifact for this topic (if any).
