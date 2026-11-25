---
name: review-spec
description: Review a requirements spec file for completeness, convention alignment, and ambiguities. Use when the user invokes /review-spec, says "review this spec", "check the spec", "what's missing from the spec", or "review spec NN" while a requirements file is open or named.
---

# Review Spec

Analyse a requirements spec file and produce structured feedback in chat. No files are written — this is a read-only critique pass.

<!--
SETUP — replace these tokens before using:
  {{SPEC_DIR}}         e.g. docs/specs/
  {{CONVENTIONS_DOC}}  e.g. CLAUDE.md
-->

## Instructions

1. **Resolve the target spec.**
   - A full file path → use directly.
   - A bare name or step number → look in `{{SPEC_DIR}}` for a matching file; if multiple match, ask.
   - No argument → use the file the user has open; if still ambiguous, ask.
   - If your project organizes specs into subtrees (e.g. `docs/api/requirements/` and `docs/ui/requirements/`), extend the resolver to disambiguate by subtree.

2. **Read inputs.**
   - Read the spec file in full.
   - Read [reference.md](reference.md) — it contains the canonical section list and the edge-case checklist.
   - Read `{{CONVENTIONS_DOC}}` — it has the project's rules you must cross-reference.

3. **Completeness check.**
   For each canonical section in `reference.md`, mark it as ✅ present, ⚠️ thin, or ❌ missing.

4. **Convention alignment check.**
   Work through every rule in `{{CONVENTIONS_DOC}}` and flag any spec instruction that conflicts with or omits a required convention. Be specific — name the rule and the spec line that violates it.

5. **Ambiguity & edge-case pass.**
   Run the edge-case checklist in `reference.md` and flag anything not addressed.

6. **If Context7 is configured** for this project (a `context7_*` tool is in the available tool list), use it sparingly for version-current framework API details when alignment depends on it. Skip otherwise.

7. **Output the review in chat** using this exact structure — do not write any files:

```
## Spec Review: <name>

### Completeness
- ✅ Purpose
- ✅ Requirements — Must Have
- ⚠️ Acceptance Criteria — present but not in Given/When/Then form
- ❌ Open Questions — missing

### Convention Alignment
- ✅ <rule from {{CONVENTIONS_DOC}}>
- ❌ <rule violated and where>

### Ambiguities & Edge Cases
- AC-2 has no measurable outcome
- "Should Have" item #3 overlaps with Must Have #1
- ...

### Open Questions to resolve before planning
- ...

### Suggested Additions
- Add an Out of Scope subsection clarifying that X is deferred
- ...
```

8. **Do not generate any code, plan files, or implementation details.** If the spec looks solid, end with: *"Spec looks ready — run `/create-plan` to generate the implementation plan."*

## Notes

- Be specific in every finding — reference the exact section or item name (e.g. "Must Have #3", "AC-2").
- "Thin" is not the same as "missing". A one-line Purpose is fine; a Requirements list of one vague bullet is thin.
- Skipping the convention alignment pass is not acceptable — it is the primary value of this skill.
