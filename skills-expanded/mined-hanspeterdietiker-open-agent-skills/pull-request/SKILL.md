---
name: pull-request
description: Use when the user asks to open, create, or draft a pull request, or runs /pull-request in any GitHub repository - abrir PR, criar pull request, gh pr create.
license: MIT
metadata:
  author: hanspeterdietiker
  based-on: conventional-commits skill (this repository) + https://www.conventionalcommits.org/en/v1.0.0/
---

# Pull Request

Cria pull requests bem documentados com o GitHub CLI (`gh`) em qualquer repositório.

## Uso
```
/pull-request [opcional: labels separadas por vírgula, ex. "bug,ui"] [opcional: draft] [opcional: base=<branch>]
```

## Fluxo
1. **Pré-checagens**
   - `gh auth status` falhou → peça ao usuário para rodar `! gh auth login` e pare.
   - Mudanças não commitadas → avise; ofereça commitar com a skill `conventional-commits` antes.
   - `gh pr view --json url` já retorna um PR desta branch → mostre o link e pergunte se é para atualizar em vez de criar outro.
2. **Descobrir a branch base** (não presuma `main`): argumento `base=` → senão `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`.
3. **Analisar o histórico:** `git log --oneline <base>..HEAD` e `git diff --stat <base>...HEAD`. Leia os diffs relevantes, não só as mensagens.
4. **Título**
   - 1 commit → use a mensagem dele.
   - Vários → resumo no formato conventional commits (`feat(scope): ...`), ≤ 72 caracteres, no idioma do histórico do repo.
5. **Labels**
   - Inferir pelos prefixos dos commits: `feat` → `enhancement`, `fix` → `bug`, `docs` → `documentation`, `perf` → `performance`, `test` → `tests`, `ci`/`build` → `ci`.
   - Juntar com as labels passadas no argumento.
   - Manter só as que existem: `gh label list --limit 200`. Label inexistente faz o `gh pr create` falhar; informe as descartadas.
6. **Referências de issue:** colete IDs do nome da branch, dos commits e do argumento: Jira (`[A-Z][A-Z0-9]+-\d+`, ex. `PROJ-41`) ou GitHub (`#41` → `Closes #41`). Nenhum encontrado → pergunte ao usuário; se não houver, omita a seção.
7. **Corpo:** use o template do repo se existir (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`, `docs/pull_request_template.md`). Senão, use o template abaixo. Grave em arquivo temporário.
8. **Publicar:** `git push -u origin HEAD` se a branch não tiver upstream, depois:
   ```
   gh pr create --base <base> --title "<título>" --body-file <arquivo> [--label "<l1>,<l2>"] [--draft]
   ```
9. Retornar a URL do PR.

## Template padrão
```markdown
## Summary
Resumo curto do que muda e por quê.

## Changes
- Mudanças específicas, agrupadas por área

## Testing
Como validar (comandos, passos manuais, cenários).

## Refs
- PROJ-41 / Closes #41

## Screenshots
(se aplicável; remova a seção se não houver)

## Checklist
- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Labels aplicadas
- [ ] Sem breaking changes (ou descritas acima)
```

## Regras fixas
- **Sem atribuição de IA:** nada de "Generated with Claude Code", `Co-Authored-By: Claude` ou link de sessão no título ou no corpo.
- Marque no checklist só o que foi de fato verificado; o resto fica `[ ]`.
- Não faça force-push nem altere a branch base.

## Créditos / Credits

- **Autor / Author:** [hanspeterdietiker](https://github.com/hanspeterdietiker).
- **Baseado em / Based on:** a skill [`conventional-commits`](../conventional-commits/SKILL.md) deste repositório (padrões de título, tipos e referências de issue) e a especificação [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
- **Sub-skill opcional / Optional sub-skill:** [`conventional-commits`](../conventional-commits/SKILL.md) — para commitar mudanças pendentes antes de abrir o PR.
