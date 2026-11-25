---
name: swift-comments-that-matter
license: MIT
description: Review and write Swift comments and DocC symbol documentation. Use to preserve API contracts, explain non-obvious intent or lifecycle constraints, and remove redundant implementation commentary. Applies to comment-focused work, not general Swift refactoring or concurrency migrations.
---

# Swift Comments That Matter

Write documentation that helps consumers use an API and maintainers change it safely.

## Choose The Kind Of Documentation

- Symbol documentation (`///`) describes observable behavior, useful parameters,
  results, errors, and usage constraints. It can serve public APIs or internal
  APIs documented for the team; it need not reveal a hidden risk to be useful.
- Implementation commentary (`//`) explains a decision, invariant, trade-off, or
  failure mode that naming, types, and control flow do not make clear.
- DocC articles explain broader concepts or workflows. Documentation extension
  files can supplement a symbol without changing its source.

Do not delete useful API summaries just because types or tests express behavior.
Do not add internal commentary when no context would be lost without it.

Comments consumed by tools or required notices are not ordinary prose. Preserve
lint/formatter directives, generator markers, and license/copyright headers during
editorial cleanup. If a change to one is explicitly in scope, check its syntax,
placement, and affected region against the relevant configuration or generator;
do not remove it merely because it lacks explanatory value.

## Review Or Rewrite

1. Inspect the comment and enough implementation, callers, tests, or maintained
   references to assess its claims. Distinguish an existing contract from an
   explanation you are inferring.
2. Prefer expressing enforceable contracts in code and checking behavior with
   tests. Still explain *why* an explicit boundary must be preserved when the
   compiler cannot capture that intent.
3. Refactor within the authorized scope. In comment-only work, report code bugs
   or proposed refactors separately rather than changing behavior or documenting
   a bug as intentional.
4. Choose a recommendation and write only the useful final text, or recommend
   deletion. Use `no → bad → good → best` only for teaching or explicit comparison.

Read [decision rules](docs/decision-rules.md) for the full flow and teaching model.

## Evidence And Recommendations

Use `keep`, `refactor`, `encode`, `test`, `move-to-DocC`, or `delete` when supported
by evidence. Use `needs-evidence` when a claim cannot be confirmed or disproved
from the available context. Missing evidence alone is not grounds for deletion.
Preserve the uncertain text provisionally and state what reference or owner could
resolve it; do not invent business reasons, issues, measurements, or guarantees.

For each actionable review finding, give the location, recommendation, reason,
and final text when justified. Identify evidence gaps when they affect the
recommendation. Return actionable findings by default; report unchanged comments
only when useful or when the user requests a complete inventory. Separate verified
errors, optional wording improvements, and unresolved evidence gaps.

## Writing Rules

- Be concise, direct, and specific to the code's contract or decision.
- Avoid boilerplate such as “This function…” and line-by-line narration; improve
  wording without treating a stylistic opening as a correctness failure.
- Use section labels only when they help scan real constraints. `Ownership:` and
  similar labels are prose conventions, not dedicated DocC directives.
- Tie workarounds and performance claims to evidence or a meaningful revisit
  condition. Do not turn hypothetical examples into factual project guarantees.
- Keep compiler-visible boundaries and useful API documentation. Neither replaces
  the other, and a test can verify a contract without explaining why it matters.

## Read Only What The Task Needs

- Review checks and rubric: [checklist](docs/checklist.md).
- Symbol summaries, markup, generated symbols, and rendered checks:
  [DocC guidance](docs/docc-guidance.md).
- Task ownership, cooperative cancellation, cleanup, isolation settings, and
  intentional annotations: [concurrency contracts](docs/concurrency-contracts.md).
- Common low-signal patterns: [review red flags](docs/review-red-flags.md).
- Wording anchors and negative controls: [golden examples](docs/golden-examples.md).
- Domain examples: [examples index](examples/README.md). Read a matching example
  rather than loading the whole catalog.
- Authoring examples for this package: [example constraints](docs/example-constraints.md).
- Broader rationale and tone: [principles](docs/principles.md) and [context](docs/context.md).

For version-sensitive advice, check the project's compiler, language mode, SDK,
deployment targets, and relevant feature flags before adopting new syntax or
execution assumptions. An announcement or successful type-check is not proof of
runtime availability or behavior.
