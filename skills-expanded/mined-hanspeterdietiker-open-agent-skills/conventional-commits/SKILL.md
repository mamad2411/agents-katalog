---
name: conventional-commits
description: Use when the user asks to commit, create a commit, write a commit message, or runs /commit or /conventional-commits in any git repository - commit, commitar, mensagem de commit, conventional commits.
license: MIT
metadata:
  author: hanspeterdietiker
  based-on: https://www.conventionalcommits.org/en/v1.0.0/
---

# Conventional Commits

Cria commits no padrão [Conventional Commits 1.0](https://www.conventionalcommits.org/) em qualquer repositório.

## Uso
```
/conventional-commits [opcional: dica de escopo ou contexto]
```

## Fluxo
1. **Ler o estado:** `git status`, `git diff --staged`, `git log -n 10 --oneline`.
   - Nada staged → mostre os arquivos alterados e pergunte o que entra. Nunca rode `git add -A` / `git add .` sem confirmação (evita `.env`, binários, lixo).
   - Mudanças sem relação entre si → proponha dividir em mais de um commit.
2. **Seguir as regras do repo, se existirem:** `commitlint.config.*`, `.commitlintrc*`, `.czrc`, ou seção `commitlint` no `package.json`. Elas prevalecem sobre este guia (tipos, escopos, tamanho).
3. **Imitar o histórico:** idioma (pt/en), estilo de escopo e uso de IDs de issue vistos no `git log`.
4. **Gerar a mensagem** (formato abaixo).
5. **Commitar via arquivo** para preservar quebras de linha em qualquer shell (bash, PowerShell, cmd):
   ```
   git commit -F <arquivo-temporario>
   ```
6. Mostrar `git log -1 --stat` como confirmação.

## Formato
```
<type>(<scope>)!: <descrição>

[corpo opcional: o porquê da mudança, linhas até 72 colunas]

[rodapés opcionais]
```

| Regra | Detalhe |
|-------|---------|
| Descrição | imperativo, minúscula, sem ponto final, ≤ 72 caracteres no cabeçalho inteiro |
| Escopo | opcional; módulo/pasta afetada (`auth`, `api`, `docs`). Omita se a mudança for transversal |
| Breaking change | `!` após o tipo/escopo **e** rodapé `BREAKING CHANGE: <o que quebrou>` |
| Issue | ID detectado no nome da branch ou informado pelo usuário → rodapé `Refs: PROJ-41` (Jira) ou `Closes #41` (GitHub) |

## Tipos
| Tipo | Quando |
|------|--------|
| `feat` | nova funcionalidade |
| `fix` | correção de bug |
| `docs` | só documentação |
| `style` | formatação, sem mudar lógica |
| `refactor` | reestruturação sem mudar comportamento |
| `perf` | melhoria de desempenho |
| `test` | testes novos ou ajustados |
| `build` | build, dependências |
| `ci` | pipelines de CI |
| `chore` | manutenção que não se encaixa acima |
| `revert` | reverte commit anterior |

## Regras fixas
- **Sem atribuição de IA:** nada de `Co-Authored-By: Claude`, "Generated with Claude Code" ou link de sessão na mensagem.
- Nunca `--no-verify`. Se um hook falhar, corrija a causa e crie um commit **novo** (não use `--amend` no commit anterior).
- Não faça push, a menos que o usuário peça.

## Exemplo
```
feat(auth): add password reset flow

Users had no way to recover access without contacting support.

- add forgot password form
- send verification email with expiring token
- add POST /auth/reset endpoint

Refs: PROJ-41
```

## Créditos / Credits

- **Autor / Author:** [hanspeterdietiker](https://github.com/hanspeterdietiker).
- **Baseado em / Based on:** especificação [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
