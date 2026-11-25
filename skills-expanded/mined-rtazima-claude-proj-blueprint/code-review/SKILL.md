---
name: code-review
description: Code review following project conventions. Activated when the user asks for a review, CR, or code revision.
allowed tools: Read, Grep, Glob
---

# Code Review

## Default checklist
1. **Correctness**: does the code do what it should?
2. **Tests**: coverage for happy path + edge cases
3. **Naming**: descriptive variables and functions
4. **Security**: no hardcoded secrets, inputs validated
5. **Performance**: no N+1 queries, no unnecessary loops
6. **Docs**: docstrings on public functions

## Active spec checklist
[SPEC] Add checklist items for each active spec module:
- Compliance: legal basis documented for personal data?
- Security: OWASP Top 10 verified?
- Observability: metrics and logs instrumented?
- Scalability: performance impact assessed?
- Accessibility: WCAG verified?
- [Add per active specs]

## Output format
- 🔴 Blocker — must fix before merge
- 🟡 Suggestion — recommended improvement
- 🟢 Nit — cosmetic, non-blocking

## Racionalizações comuns

| Racionalização | Realidade |
|---|---|
| "É só um refactor pequeno, não precisa de review" | Refactors pequenos introduzem bugs sutis. Review sempre. |
| "Os testes passam, então o código está correto" | Testes cobrem cenários escritos. Review encontra cenários não testados. |
| "Esse padrão é idiomático, não precisa comentar" | Idiomático pra quem? Docstring em função pública é obrigatório. |
| "Performance não importa agora, é MVP" | N+1 query em MVP vira incidente em produção. Revise sempre. |

## Red Flags

- Aprovou sem verificar se testes existem para os cenários alterados
- Ignorou warning de `any` type ou `@ts-ignore`
- Não verificou se secrets estão hardcoded
- Pulou checklist de spec ativo (segurança, compliance, etc.)

## References
- Conventions: see `CLAUDE.md` at the root
- ADRs: see `docs/architecture/`
- Specs: see `docs/specs/`
