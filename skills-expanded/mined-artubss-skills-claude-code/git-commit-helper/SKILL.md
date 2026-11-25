---
name: Git Commit Helper
description: Gere mensagens de commit descritivas analisando diffs do git. Use quando o usuário pedir ajuda para escrever mensagens de commit ou revisar mudanças preparadas.
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "echo \"[$(date)] Git Commit Helper: Analyzed git diff for commit message\" >> ~/.claude/git-commit-helper.log"
---

# Git Commit Helper

## Início rápido

Analise as mudanças preparadas e gere uma mensagem de commit:

```bash
# Visualize mudanças preparadas
git diff --staged

# Gere mensagem de commit baseada nas mudanças
# (Claude analisará o diff e sugerirá uma mensagem)
```

## Formato da mensagem de commit

Siga o formato de conventional commits:

```
<type>(<scope>): <description>

[corpo opcional]

[rodapé opcional]
```

### Tipos

- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Mudanças na documentação
- **style**: Mudanças no estilo do código (formatação, ponto-e-vírgula faltantes)
- **refactor**: Refatoração de código
- **test**: Adição ou atualização de testes
- **chore**: Tarefas de manutenção

### Exemplos

**Commit de funcionalidade:**
```
feat(auth): add JWT authentication

Implement JWT-based authentication system with:
- Login endpoint with token generation
- Token validation middleware
- Refresh token support
```

**Correção de bug:**
```
fix(api): handle null values in user profile

Prevent crashes when user profile fields are null.
Add null checks before accessing nested properties.
```

**Refatoração:**
```
refactor(database): simplify query builder

Extract common query patterns into reusable functions.
Reduce code duplication in database layer.
```

## Analisando mudanças

Revise o que está sendo commitado:

```bash
# Mostra arquivos alterados
git status

# Mostra mudanças detalhadas
git diff --staged

# Mostra estatísticas
git diff --staged --stat

# Mostra mudanças para arquivo específico
git diff --staged path/to/file
```

## Diretrizes para mensagens de commit

**FAÇA:**
- Use modo imperativo ("adicionar funcionalidade" e não "adicionada funcionalidade")
- Mantenha a primeira linha com menos de 50 caracteres
- Capitalize a primeira letra
- Sem ponto ao final do resumo
- Explique POR QUÊ, não apenas O QUÊ no corpo

**NÃO FAÇA:**
- Use mensagens vagas como "atualizar" ou "corrigir coisas"
- Inclua detalhes técnicos de implementação no resumo
- Escreva parágrafos na linha de resumo
- Use tempo passado

## Commits de múltiplos arquivos

Ao commitar múltiplas mudanças relacionadas:

```
refactor(core): restructure authentication module

- Move auth logic from controllers to service layer
- Extract validation into separate validators
- Update tests to use new structure
- Add integration tests for auth flow

Breaking change: Auth service now requires config object
```

## Exemplos de escopo

**Frontend:**
- `feat(ui): add loading spinner to dashboard`
- `fix(form): validate email format`

**Backend:**
- `feat(api): add user profile endpoint`
- `fix(db): resolve connection pool leak`

**Infrastructure:**
- `chore(ci): update Node version to 20`
- `feat(docker): add multi-stage build`

## Mudanças quebradas (breaking changes)

Indique claramente as mudanças quebradas:

```
feat(api)!: restructure API response format

BREAKING CHANGE: All API responses now follow JSON:API spec

Previous format:
{ "data": {...}, "status": "ok" }

New format:
{ "data": {...}, "meta": {...} }

Migration guide: Update client code to handle new response structure
```

## Fluxo de trabalho com template

1. **Revise mudanças**: `git diff --staged`
2. **Identifique o tipo**: É feat, fix, refactor, etc.?
3. **Determine o escopo**: Qual parte da base de código?
4. **Escreva o resumo**: Descrição breve em modo imperativo
5. **Adicione o corpo**: Explique por quê e qual o impacto
6. **Anote mudanças quebradas**: Se aplicável

## Assistente de commit interativo

Use `git add -p` para staging seletivo:

```bash
# Prepare mudanças interativamente
git add -p

# Revise o que está preparado
git diff --staged

# Commit com mensagem
git commit -m "type(scope): description"
```

## Emendando commits

Corrija a mensagem do último commit:

```bash
# Emende apenas a mensagem de commit
git commit --amend

# Emende e adicione mais mudanças
git add forgotten-file.js
git commit --amend --no-edit
```

## Melhores práticas

1. **Commits atômicos** - Uma mudança lógica por commit
2. **Teste antes de commitar** - Garanta que o código funciona
3. **Referencie issues** - Inclua números de issues se aplicável
4. **Mantenha o foco** - Não misture mudanças não relacionadas
5. **Escreva para humanos** - Você mesmo lerá isso no futuro

## Checklist de mensagem de commit

- [ ] O tipo é apropriado (feat/fix/docs/etc.)
- [ ] O escopo é específico e claro
- [ ] O resumo tem menos de 50 caracteres
- [ ] O resumo usa modo imperativo
- [ ] O corpo explica POR QUÊ, não apenas O QUÊ
- [ ] Mudanças quebradas estão claramente marcadas
- [ ] Números de issues relacionadas estão inclusos