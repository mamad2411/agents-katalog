---
name: specspine-extract
description: Use only to extract a minimal read-only architecture context handoff from a verified existing linked Markdown SpecSpine for a downstream feature, planning, review, SDD, or coding task that needs authoritative specification owners, decisions, constraints, evidence status, or blocking questions. Do not use for maintaining, debugging, testing, or implementing SpecSpine skills or tooling, generic repository work, or when no configured Spine root exists.
---

# SpecSpine Extract

Return the smallest source-grounded architecture handoff for one downstream
change. Do not modify the project or SpecSpine.

## Fast path

1. Resolve `<spine-root>` and documentation language from the request or
   project instructions; default the root to `specspine`.
2. Verify that the task is downstream architecture-context work and that
   `<spine-root>/README.md` exists. If either condition fails, stop without
   invoking the script because this skill is not applicable. A repository name
   or work on SpecSpine skills and tooling does not establish applicability.
3. Split the request into independently owned architecture targets. Form all
   query slices before using tools.
4. After applicability is established, invoke the bundled script exactly once:

```text
python3 <skill-root>/scripts/search_spine.py <spine-root> --queries-json '<compact-json>'
```

5. Produce the handoff directly from returned `DOCUMENT` blocks. Do not reread
   returned files. Read a file only when it is necessary and marked
   `DOCUMENT_OMITTED`.
6. If execution is unavailable, output is malformed, or a necessary slice is
   `no_match`, do not retry. Use the returned root `DOCUMENT`; read
   `<spine-root>/README.md` only if it was not returned, then follow only the
   links needed to fill the gap.

Read `<spine-root>/README.md` before searching only when the root,
documentation language, or system vocabulary cannot be resolved otherwise.
Resolve `<skill-root>` as this `SKILL.md` directory; never search for another
copy. Ranking, graph expansion, and output budget are fixed internal policy.

## Query

Use one slice per required owner, normally with 2–3 independent literal
features. Put synonyms for one feature in the same group. Use `should` only for
useful tie-breakers. Preserve exact paths, semantic IDs, API names, and
identifiers; write descriptive terms in the documentation language. Pass the
slices as the top-level JSON array shown below; never wrap it in an object.

```json
[
  {
    "id": "retry-owner",
    "must": [
      ["retry", "retries"],
      ["provider", "external provider"],
      ["timeout", "timed-out"]
    ],
    "should": [["backoff"]]
  }
]
```

`SLICE status=no_match` means no direct owner; its
`HIT origin=root_fallback` points to the included root index. Other slices and
their hits remain intact. `HIT origin=graph` is supporting context, not
automatically required. `DOCUMENT` is complete current Markdown.
`truncated=true` means at least one selected document was omitted. Protocol
paths are relative to `<spine-root>`; prepend the repository-relative
`<spine-root>/` when citing them in the handoff.

## Handoff

Use this order and omit empty sections:

```markdown
# Architecture context handoff
## Change intent
## Primary specification
## Required specifications
## Potentially affected specifications
## Architectural decisions and constraints
## Decision sources
## Relevant observations
## Unconfirmed inferences
## Blocking questions
## Expected architectural outcome
```

Name the canonical owner by declared responsibility. `Required` means needed
to understand the change safely; `Potentially affected` means possibly needing
later revision but not needed to establish the handoff. Cite paths relative to
the repository root. Preserve existing semantic IDs with their owner paths;
never invent IDs. Preserve conflicts, unconfirmed inferences, and unanswered
questions.

Use only the request and `<spine-root>` as architecture sources unless the user
authorizes others. Never add implementation tasks, filenames, acceptance
criteria, estimates, release scope, or inferred requirements. Never claim
code/spec conformance or silently answer a blocking question.
