---
name: eda-script-pattern-curator
description: Capture and maintain reusable script-writing experience across wrappers, helpers, parsers, validators, and runtime shims so future script work can reuse proven patterns and avoid repeated anti-patterns.
---

# EDA Script Pattern Curator

## When to use

Use this skill when:
1. repeated script-writing lessons appear across infrastructure or execution helpers,
2. a new wrapper/helper is being considered and prior abstraction/runtime experience should be checked first,
3. script anti-patterns should be promoted into durable guidance,
4. infra work needs a place to persist coding lessons that are more specific than global governance but broader than one script.

## Scope Boundary

This skill owns:
- reusable script-writing patterns,
- wrapper and runtime lessons,
- abstraction triggers for when a one-off helper should become a shared tool,
- script-level anti-pattern capture.

It does not own:
- the tool catalog itself,
- domain experiment conclusions,
- generic artifact hygiene,
- final infrastructure workflow ownership.

## Expected Downstream Consumers

Typical consumers:
- `eda-infra-maintainer`
- `eda-method-implementer`
- `workflow-scoped-execution`
- `eda-context-accessor`

## Inputs

Provide or derive:
1. script or wrapper paths under discussion,
2. prior maintenance notes or logs,
3. tool-catalog search results,
4. runtime/environment constraints when relevant.

## Outputs

Emit the smallest useful set:
1. script-pattern note or SOP update,
2. concrete reuse/abstraction recommendation,
3. anti-pattern warning when applicable,
4. cross-links to related tools or wrappers.

## Hard rules

1. Do not create a new shared script just because two scripts look similar; require a clear reuse trigger.
2. Keep script-writing lessons separate from experiment-phenomenology lessons.
3. Tie every pattern or anti-pattern to concrete script evidence.
4. Prefer tool-catalog reuse over new wrapper proliferation.

## Operational References

1. Load `references/pattern-layers.md` when deciding how to separate raw script incidents from reusable patterns.
2. Load `references/integration-policy.md` when wiring script-pattern guidance into infra or execution workflows.
3. Use `docs/knowledge_base/templates/script_incident_template.md` and `docs/knowledge_base/templates/script_pattern_note_template.md` as the default artifact skeletons when no more specific script-pattern template already exists.
