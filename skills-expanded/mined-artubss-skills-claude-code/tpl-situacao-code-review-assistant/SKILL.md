---
name: tpl-situacao-code-review-assistant
description: Template do pack (situacao/05-code-review-assistant.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/05-code-review-assistant.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Systematic Code Review

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/05-code-review-assistant.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when conducting or receiving code reviews — Pull Requests, Merge Requests, or any structured review of proposed changes. The goal is not to find fault but to improve code quality, catch bugs before production, share knowledge, and maintain consistency. Reviews should be efficient, constructive, and focused on the code, not the author.

## OBJECTIVES
- Catch correctness bugs, logic errors, and edge cases before merge
- Identify security, performance, and reliability concerns
- Verify the change meets acceptance criteria and has adequate tests
- Maintain codebase consistency and shared ownership
- Give feedback that the author can act on immediately

## APPROACH RULES

1. **Review the diff, not the author.** Keep all feedback about the code. Use "this function" not "you wrote." Frame feedback as questions when uncertain.

2. **Review in layers, not in one pass.** First pass: understand the change at a high level (read the PR description, tests, then code). Second pass: correctness and logic. Third pass: style, naming, and consistency.

3. **Distinguish blocking from non-blocking.**
   - `[BLOCKING]` — Must be fixed before merge (bugs, security, test failures, missing tests for critical paths)
   - `[SUGGESTION]` — Would improve quality but doesn't block merge (naming, minor refactoring)
   - `[QUESTION]` — Seeking understanding, not requesting a change
   - `[NIT]` — Purely stylistic, author's discretion

4. **PR size matters.** A PR over 400 lines of changed code is hard to review effectively. If asked to review a large PR, flag it and suggest splitting it. Review large PRs in sections, not all at once.

5. **Check the tests first.** If there are no tests for new behavior, that's the most important thing to flag. Understanding the tests usually clarifies the intent of the code.

6. **Verify acceptance criteria.** Does the code actually do what the ticket/story asked for? Is there a way to verify it manually?

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| No tests for new logic | `[BLOCKING]` Request tests. Specify which cases need coverage: happy path, error cases, edge cases |
| A function over 40 lines | `[SUGGESTION]` Ask what each section does. Often leads to natural extraction. |
| Complex conditional logic | `[QUESTION]` Ask the author to explain the logic. If they can't quickly, it needs refactoring |
| Hardcoded values (URLs, IDs, magic numbers) | `[BLOCKING]` or `[SUGGESTION]` depending on production risk. Ask: what happens when this changes? |
| Missing error handling | `[BLOCKING]` — unhandled Promise rejections, bare `catch` blocks, ignored return codes |
| Security-sensitive code (auth, crypto, user input) | Always block. Tag as `[SECURITY]`. Apply full OWASP pattern review |
| Duplicate code that already exists | `[SUGGESTION]` Point to the existing utility. No need to duplicate. |
| `console.log` or debug code | `[BLOCKING]` — never merge debug artifacts to main |
| Commented-out code | `[BLOCKING]` — delete it or explain why it's staying |
| Missing or incorrect type annotations | `[SUGGESTION]` in typed codebases or `[BLOCKING]` if types are a team standard |

## Review Checklist

**Correctness**
- [ ] Does the code implement what the ticket/story describes?
- [ ] Are edge cases handled? (empty arrays, null values, zero, negative numbers, max values)
- [ ] Are there off-by-one errors in loops or array access?
- [ ] Are async operations awaited? Are race conditions possible?
- [ ] Are error paths tested, not just the happy path?

**Security**
- [ ] Is user input validated and sanitized before use?
- [ ] Are SQL/NoSQL queries parameterized?
- [ ] Are secrets hardcoded anywhere?
- [ ] Are authorization checks present on all new endpoints?

**Performance**
- [ ] Are there obvious N+1 query patterns?
- [ ] Are large datasets paginated?
- [ ] Are expensive operations cached where appropriate?

**Readability**
- [ ] Do names explain intent? (verbs for functions, nouns for variables)
- [ ] Are comments explaining WHY, not WHAT?
- [ ] Is the complexity justified by requirements?

**Tests**
- [ ] Do tests cover happy path, error cases, and edge cases?
- [ ] Are tests testing behavior, not implementation details?
- [ ] Would the tests catch the bug if someone broke the code?

## DO NOT

- **DO NOT** approve a PR you don't understand — ask questions until you do
- **DO NOT** request changes on style if the team has a linter that handles it
- **DO NOT** leave a review open more than 24 hours without at minimum a comment
- **DO NOT** re-review already-addressed items — trust that the author fixed what was asked
- **DO NOT** use review to teach a whole new paradigm — suggest a separate tech talk instead
- **DO NOT** pile on if another reviewer already flagged the same issue — add a "+1 on the above"
- **DO NOT** approve PRs with failing CI — never assume "it's probably fine"

## OUTPUT FORMAT

For each review, structure comments as:

```
[BLOCKING] The `getUser` function does not handle the case where `userId` is undefined.
If `userId` is undefined, the database query will return unintended results.

Suggestion:
if (!userId) throw new Error('userId is required')
```

For a PR summary comment:

```
## Review Summary

**Overall:** Approve with minor changes / Request changes

**Highlights:**
- Clean separation between service and controller layer
- Good error handling in the webhook handler

**Blocking Issues (2):**
- Missing auth check on DELETE /api/posts/:id
- No test for the rate limiting logic

**Suggestions (3):**
- Extract the email template to a separate file
- `processData` function could be named more specifically
- Missing JSDoc on the public-facing `UserService` class
```

## QUALITY GATES

- [ ] Every `[BLOCKING]` comment has an explicit suggestion for how to fix it
- [ ] PR description was read before reviewing the code
- [ ] Tests were read before the implementation code
- [ ] Review submitted within SLA (default: 24 business hours)
- [ ] All existing CI checks were green before starting review
- [ ] No style/formatting comments that a linter should catch
- [ ] Author acknowledged or responded to all blocking items before approval
- [ ] Second reviewer requested for security-sensitive or architecturally significant changes
