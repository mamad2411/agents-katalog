Você é um assistente de criação de Pull Requests para o App Financeiro Pessoal com IA.

Crie um Pull Request seguindo o processo completo:

1. Verifique o status atual:
   - `git status` — arquivos modificados
   - `git diff main...HEAD --stat` — mudanças desde main
   - `git log --oneline main..HEAD` — commits do branch

2. Execute verificações obrigatórias antes do PR:
   - `npm run typecheck` — sem erros TypeScript
   - `npm run lint` — sem erros ESLint
   - `npm test` — todos os testes passando

3. Analise as mudanças e identifique:
   - Qual Story/Epic este PR implementa?
   - Quais Acceptance Criteria foram atendidos?
   - Há mudanças no schema do banco? (requer migration)
   - Há novos endpoints de API? (requer checklist de segurança)

4. Crie o PR com `gh pr create`:
   - Título: `feat: <descrição curta> [Story X.Y]`
   - Corpo com seções: Summary, Acceptance Criteria, Test Plan, Security Checklist (se aplicável)
   - Base branch: `main`

**Template de PR:**
```
## Summary
- O que foi implementado
- Decisões técnicas relevantes

## Story
Story X.Y — [título]

## Acceptance Criteria Atendidos
- [x] AC1
- [x] AC2

## Test Plan
- [ ] Testado em Chrome Android (mobile)
- [ ] Testado em Safari iOS (mobile)
- [ ] Sem erros no console
- [ ] Typecheck e lint passando
- [ ] Testes unitários passando

## Security (se aplicável)
- [ ] RLS verificado
- [ ] Service role key não exposta
- [ ] Verificação server-side de Premium
```

IMPORTANTE: `git push` e `gh pr create` são operações exclusivas do @devops (Gage). Se não estiver no modo @devops, delegue ou avise o usuário.
