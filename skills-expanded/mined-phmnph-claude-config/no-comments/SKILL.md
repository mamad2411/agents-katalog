---
name: no-comments
description: Remove stale or redundant comments when requested, or when changed comments obscure the code's behavior.
---

# Review comments in scope

Inspect the requested files or relevant changed comments. This is an optional
cleanup pass, not a required stage before every commit, push, or PR.

Remove dead code and prose that only narrates an obvious implementation. Keep
useful explanations of intent, domain assumptions, numerical reasoning,
compatibility constraints, and required license or tool directives. Confirm that
a claim is stale before deleting it; uncertainty alone is not evidence.

A small diff can be reviewed directly. For a substantial independent pass, a
permitted subagent can load $comment-sicko and report findings in the given scope.
It must not edit the code or delegate again. Inspect its evidence before applying
accepted changes.

Do not remove a suppression or constraint comment until the underlying issue is
resolved or the directive is demonstrably obsolete. Inspect history or callers
when needed to establish that. An architectural concern discovered here can be
reported separately; comment cleanup does not authorize an unrelated redesign.

Apply authorized, supported edits and run checks affected by directive changes.
Report material deletions, retained unresolved constraints, and any follow-up.
