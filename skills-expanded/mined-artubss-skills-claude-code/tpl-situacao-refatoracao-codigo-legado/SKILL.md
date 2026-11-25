---
name: tpl-situacao-refatoracao-codigo-legado
description: Template do pack (situacao/01-refatoracao-codigo-legado.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/01-refatoracao-codigo-legado.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Refactoring Legacy Code

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/01-refatoracao-codigo-legado.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when you need to safely improve the structure of existing code without changing its observable behavior. This applies to: removing dead code, extracting functions, renaming for clarity, adding types to untyped JavaScript, splitting god objects/files, or paying down technical debt incrementally. NOT for rewrites from scratch.

## OBJECTIVES
- Improve code health without breaking functionality
- Increase test coverage before and during refactoring
- Make changes that are reviewable and reversible
- Leave code better than you found it (Boy Scout Rule)
- Document decisions along the way

## APPROACH RULES

1. **Test before you touch.** If there are no tests for a piece of code, write characterization tests first — tests that capture current behavior, even if that behavior is wrong.

2. **Strangler Fig Pattern.** Never do big-bang rewrites. Create the new implementation alongside the old, redirect traffic gradually, then delete the old code. Never leave both running indefinitely.

3. **One concern per commit.** Each commit should do exactly one thing: rename, extract, move, or simplify. Never mix refactoring with behavior changes in the same commit.

4. **Red-Green-Refactor.** If adding tests: write a failing test → make it pass → refactor. Never skip the red phase.

5. **Preserve the public interface.** Refactoring internal logic is safe. Changing method signatures or return shapes is a breaking change — handle it separately.

6. **Adding TypeScript types to JS:** Start at the leaf nodes (utility functions) and work inward toward the core. Use `unknown` instead of `any`. Enable `strict: true` in tsconfig from day one — do not plan to "add strict later."

7. **The Boy Scout Rule.** Leave every file you touch slightly better than you found it. Never make it worse. Even a simple rename or extracted constant counts.

8. **Refactor vs Rewrite decision:** Refactor if the logic is fundamentally sound but messy. Rewrite if the logic is broken or the architecture cannot support future requirements. Default to refactoring — rewrites almost always take 3× longer than estimated.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| A function over 50 lines | Extract sub-functions with descriptive names. Each function should do one thing. |
| A file over 300 lines | Identify natural module boundaries and split. Keep the original file as a re-export barrel temporarily. |
| Magic numbers or strings | Extract to named constants at the top of the file or a `constants.ts` file |
| Deeply nested conditionals (3+ levels) | Apply early return / guard clause pattern to invert the logic |
| Any `// TODO` or `// HACK` comment | Create a GitHub Issue for it, then fix it in this PR if it's in scope |
| `any` type in TypeScript | Replace with the correct type. If unknown, use `unknown` and add a type guard |
| Duplicate logic in 3+ places | Extract to a shared utility. Do not extract if only 2 occurrences — wait for the third |
| A class doing 5+ unrelated things | Apply Single Responsibility — split into separate classes/modules |
| No error handling in async code | Add try/catch with explicit error types. Never swallow errors silently |
| Commented-out code | Delete it. Git history exists for a reason |

## DO NOT

- **DO NOT** refactor and add features in the same branch/PR
- **DO NOT** rename a public API or database column without a deprecation path
- **DO NOT** turn a refactoring PR into a feature PR ("while I'm here...")
- **DO NOT** remove code you don't understand without understanding it first
- **DO NOT** use `any` as a shortcut when adding TypeScript — it defeats the purpose
- **DO NOT** assume tests are passing just because CI passed before — run them locally
- **DO NOT** do a big-bang refactor of an entire module in one PR — split into layers
- **DO NOT** delete old code until the new code is verified in production (Strangler Fig)

## OUTPUT FORMAT

For each refactoring session, produce:

1. **Summary of changes** — bullet list of what was changed and why
2. **Before/After snippets** — for each significant change, show old code vs new code
3. **Test coverage delta** — lines/branches covered before vs after
4. **Open items** — things noticed but intentionally left for follow-up issues
5. **Risks** — any changes that could have non-obvious side effects

Example commit message format:
```
refactor(auth): extract token validation to pure function

- Moved token parsing logic from AuthMiddleware into validateToken()
- Added unit tests for all token edge cases
- No behavior change — same logic, same error messages

Refs: #342
```

## QUALITY GATES

- [ ] All existing tests pass after every commit (not just at the end)
- [ ] No new `any` types introduced in TypeScript files
- [ ] Every extracted function has a JSDoc comment or is self-documenting by name
- [ ] No file is left longer than it was before the PR (or is justified in description)
- [ ] Test coverage did not decrease
- [ ] PR contains zero feature changes — pure refactoring only
- [ ] `git diff --stat` shows reasonable file count (not 50+ files in one PR)
- [ ] Peer reviewed by someone who knows the original code
- [ ] No dead code (unreachable branches, unused variables) remains
- [ ] CHANGELOG / tech debt tracker updated if applicable
