---
name: go-package-boundaries
description: Use when a Go change creates, splits, merges, or relocates packages, adds a responsibility, or changes import direction or ownership. Applies to libraries, CLIs, and services; local expression edits with unchanged responsibilities do not need this skill.
---

# Go package boundaries

Choose the smallest boundary that gives related behavior a clear owner and reduces demonstrated coupling. Package names, source size, and architecture labels do not establish that need.

Inspect the affected packages, imports, actual consumers, module Go version, and requested behavior. Describe each affected package's responsibility in a sentence. Trace which callers need the operation and which details change independently. Use project conventions where they fit this evidence; do not infer a release or ownership policy.

Before moving code, distinguish these choices:

- **Same package, new file:** improve navigation when code shares invariants and changes together. File boundaries do not isolate imports or visibility.
- **New package:** isolate a cohesive capability, independently evolving implementation, or actual reusable protocol. Name the consumer and change pressure that justify its dependency edge.
- **New interface:** establishes a substitutable contract, not implementation ownership. Concrete storage or outbound protocol code can remain coupled to an operation package even after interfaces are introduced. When separate maintenance is required, give those implementations an appropriate package and compose them outside the operation.

For new ingress, identify the reusable operation beneath HTTP, CLI, RPC, or worker handling. Keep its validation and sequencing available to every caller. Let ingress translate inputs and outcomes. Separate ingress packages only when reuse, independent evolution, or dependency isolation warrants them; a second caller alone does not require a layer per component.

Keep concrete adapter imports out of the operation they implement. Commands or another existing composition root connect the operation and implementations. Put representation details with the code that owns that representation. Resolve cycles by reexamining responsibility or the actual consumer contract, rather than introducing an undifferentiated `common` package. A reusable technical capability is valid when actual consumers justify it.

Read [package maps](references/package-maps.md) when choosing a split or comparing project shapes. Adapt the examples to the code; they are alternatives, not templates.

Implement only the necessary movement. Preserve supported public imports, APIs, wire/file bytes, and failure ordering unless the task explicitly changes them. Run affected behavior tests and relevant build/import checks, respecting the supported Go version. Report the package decision, its evidence, resulting dependency direction, and verification limits.

This skill owns placement and import direction. Consumer-visible contracts and compatibility are the API-contract decision; interface necessity and resource ownership are the composition decision. Check those boundaries when relevant without requiring additional skills or turning a local edit into a repository redesign.
