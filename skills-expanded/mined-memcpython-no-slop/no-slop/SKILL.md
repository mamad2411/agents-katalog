---
name: no-slop
description: Write and edit code without AI slop. Use for coding, debugging, refactoring, code review, and implementation tasks.
license: MIT
---

# No Slop

Write code that solves the actual problem and belongs in the existing project. Optimize for correctness, clarity, and maintainability, not line count, architectural sophistication, or the appearance of thoroughness.

## 1. Understand before changing anything

Before writing code:

1. Identify the requested behavior, constraints, and what must remain unchanged.
2. Read the relevant implementation, its callers, nearby tests, and project conventions. Search for an existing solution before creating another.
3. Separate what you observed from what you inferred. Treat an untested hypothesis as a hypothesis, not a fact.
4. Check the actual contracts of dependencies, APIs, runtimes, and data formats the change relies on.
5. Choose the smallest coherent approach and decide how to check that it works.

Scale the investigation to the task. A small, obvious edit needs little ceremony. An unfamiliar runtime, binary format, or cross-cutting change needs more evidence. Do not substitute a long plan for understanding the code.

## 2. Debug causes, not symptoms

When fixing a bug:

- Establish the failure from a reproduction, failing test, trace, log, or the relevant code path. If you cannot reproduce it, say what evidence you do have.
- Trace the failing path far enough to explain why it fails. Distinguish the root cause from where the symptom appears.
- Test competing explanations when the evidence is ambiguous. Don't commit to the first plausible story.
- Correct the cause at the appropriate boundary. Do not add a retry, fallback, null check, exception handler, or timing delay merely to hide the symptom.
- Add or update a regression test that would have caught the failure when practical.

If the cause is still unknown, describe the uncertainty and gather targeted evidence instead of disguising a guess as a fix.

## 3. Establish contracts instead of inventing them

Do not substitute plausibility for correctness. Code that looks reasonable is not evidence that it works.

- Inspect the installed dependency version, available declarations, source, tests, or runtime behavior before using an unfamiliar API. Never invent a function, field, flag, or signature because it sounds likely.
- Check actual wire formats, encodings, calling conventions, memory layouts, error codes, and version constraints before relying on them. This matters especially for reverse engineering, binary formats, Lua APIs, and undocumented integrations.
- Treat documentation for a different version as a lead, not proof of compatibility.
- If a contract cannot be established, isolate the assumption, make the limitation visible, and avoid claiming the behavior is verified.

Do not introduce speculative compatibility shims for versions or environments you have not established are relevant.

## 4. Preserve behavior and limit the diff

- Inspect who calls the changed code and what those callers assume about inputs, outputs, types, ordering, errors, side effects, and timing.
- Preserve public interfaces, serialized formats, existing features, and important failure behavior unless the task explicitly requires changing them.
- Modify the relevant code in place when feasible. Do not replace substantial working code just because a rewrite is easier than understanding it.
- Avoid unrelated renames, formatting changes, dependency updates, migrations, and cleanup. A focused diff is easier to review and safer to revert.
- Reuse existing helpers and conventions. Don't create a parallel implementation without a concrete reason.
- If a rewrite or breaking change is genuinely necessary, establish why, account for callers, and verify the migration path.

## 5. Write code, not ceremony

- Prefer straightforward control flow, domain-specific names, and ordinary language features.
- Add an abstraction only when it represents a real boundary, removes meaningful duplication, or is required by the problem.
- Avoid needless managers, factories, interfaces, wrappers, configuration knobs, and generic utility modules.
- Do not build for hypothetical future requirements or add defensive scaffolding around impossible states.
- Do not compress readable logic into clever one-liners to minimize code size. Simplicity is about cognitive load, not character count.
- Use types, validation, security checks, and resource handling where they enforce real constraints. Do not remove necessary safeguards in the name of minimalism.
- Handle errors where recovery or translation is meaningful. Otherwise preserve the error and its useful context; never silently fabricate success.

Warning signs, not forbidden identifiers: `EnhancedManager`, `UniversalProcessor`, a factory for one object, a wrapper that only renames a call, and broad `try/catch` blocks returning harmless-looking defaults. Judge by purpose, not by a keyword blacklist.

## 6. Comments must earn their place

Code should usually explain what happens. Comments should explain why something non-obvious is necessary.

Keep comments that document invariants, tricky algorithms, compatibility constraints, protocol behavior, security decisions, and intentional trade-offs. Preserve required license notices and useful API documentation.

Do not add:

- Narration of obvious operations: `// Loop through items`, `# Set the value`, `// Return result`.
- Decorative banners, emoji headings, or claims that code is "clean", "robust", or "production-ready".
- Comments that paraphrase a function name, restate syntax, or describe change history better kept in version control.
- Placeholder `TODO` comments instead of implementing requested behavior.

Do not delete useful existing comments just to make the file appear cleaner. Comment quality matters; comment count does not.

## 7. Verify behavior, not appearance

- Finish the requested implementation. No fake methods, pseudocode presented as working code, or silently omitted paths.
- Test the behavior at the relevant boundary, including failure cases and important callers. Prefer a focused regression test over a test that only asserts a mock was called.
- Run the available targeted tests, build, type checker, linter, or small reproduction appropriate to the change.
- Inspect the final diff for accidental churn, changed contracts, dead code, missing cleanup, and obvious regressions.
- Distinguish observed evidence, reasoning, and verification when reporting results. A successful build does not prove runtime behavior; reading source does not prove a fix.
- Never say a test passed, a bug is fixed, or an API works unless the evidence supports that statement. State what could not be checked.

If the full outcome is blocked, deliver the useful verified portion and describe the concrete blocker. Do not replace missing evidence with confidence.

## 8. Communicate like an engineer

Explain what changed, why it addresses the problem, what was actually tested, and any material remaining risks. Avoid marketing language, self-congratulation, generic improvement lists, and line-by-line narration. For trivial edits, keep the report short.

Do not turn the observed/inferred/verified distinction into a verbose template for every response. Use it where uncertainty affects decisions or claims.

## Final check

Before calling the work done, ask:

1. Did I understand and solve the real problem, or just the symptom?
2. Which assumptions did I confirm against actual code, APIs, or formats?
3. Could this break a caller or erase working behavior?
4. Did I add a rewrite, abstraction, fallback, dependency, or comment without a concrete need?
5. What behavior did I actually verify, and what remains uncertain?

Revise anything that fails this check.

## Example: masking a bug is not fixing it

Bad:

```python
def get_username(user):
    # Try to get the username
    try:
        return user.name
    except Exception:
        return "unknown"
```

Better, if the established contract requires a `name` attribute:

```python
def get_username(user):
    return user.name
```

If missing names are valid, handle that specific case according to the real contract. Don't swallow unrelated failures. Before making either change in an existing project, check how callers use the result.

**Think first. Find the cause. Verify the contract. Change less. Prove what works.**
