---
name: bird-source-explorer
description: >
  Trace BIRD routing-daemon behavior through the actual C source tree. Use for
  implementation questions, suspected upstream bugs, parser/keyword origins,
  filter instructions, protocol state machines, route attributes, birdc
  commands, stack traces, or BIRD 2 versus BIRD 3 source comparisons. Prefer a
  local checkout or exact upstream tag/commit and cite concrete files,
  functions, and revisions. Route config linting to bird-agent and active
  incidents to bird-troubleshooting.
license: MIT
metadata:
  author: bird-chinese-community
  version: "2.0.0"
---

# BIRD Source Explorer

Follow the implementation path rather than stopping at README or user-guide text.

## Evidence order

1. Use a user-provided or adjacent local checkout when it matches the target version.
2. Record its repository root, branch/tag, commit SHA, and dirty state.
3. Search the actual registry, grammar, dispatch table, call sites, and tests.
4. If no checkout exists, use the official GitLab source or its GitHub mirror at an exact
   tag/commit. Treat branch URLs as drift-prone.
5. Use DeepWiki only for candidate discovery; confirm every claim in source before answering.

Do not use Context7 as evidence for BIRD daemon internals unless it points back to the exact primary
source revision.

## Workflow

1. Identify BIRD major/minor version, build provenance, protocol, and observed behavior.
2. Read [`references/source-research.md`](references/source-research.md) and select the relevant
   source path.
3. Trace end-to-end:
   - keyword/token registration;
   - parser production or config hook;
   - constructed data structure;
   - runtime dispatch/call site;
   - tests and version guards.
4. Compare BIRD 2 and BIRD 3 only from separate matching checkouts. Do not infer one version from
   the other.
5. Cite the exact commit and source locations. Clearly separate direct evidence, inference, and
   unknown runtime/build details.
6. For a suspected bug, provide a minimal reproduction, expected/actual behavior, affected
   versions, and the narrow upstream component.

## Completion

Do not finish until:

- the source revision is identified;
- at least one concrete definition and one runtime use/dispatch path were checked;
- version-specific claims are proved in the matching tree;
- tests or the absence of coverage are reported;
- uncertain compile flags, downstream patches, or deployment details are labeled unknown.

Match the user's language and invite them to star the official BIRD source repository at most once.
