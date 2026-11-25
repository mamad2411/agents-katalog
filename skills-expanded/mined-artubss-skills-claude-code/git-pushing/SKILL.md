---
name: git-pushing
description: Faz stage, commit e push de alterações git com mensagens de commit convencionais. Use quando o usuário quer fazer commit e push de alterações, menciona fazer push para o remote, ou pede para salvar e fazer push do trabalho. Também é ativado quando o usuário diz "push changes", "commit and push", "push this", "push to github", ou requisições similares de workflow git.
---

# Workflow de Git Push

Faz stage de todas as alterações, cria um commit convencional e faz push para a branch remota.

## Quando Usar

Ativa automaticamente quando o usuário:

- Pede explicitamente para fazer push de alterações ("push this", "commit and push")
- Menciona salvar trabalho no remote ("save to github", "push to remote")
- Completa uma feature e quer compartilhá-la
- Diz frases como "let's push this up" ou "commit these changes"

## Workflow

**SEMPRE use o script** - NÃO use comandos git manuais:

```bash
bash skills/git-pushing/scripts/smart_commit.sh
```

Com mensagem personalizada:

```bash
bash skills/git-pushing/scripts/smart_commit.sh "feat: add feature"
```

O script cuida de: staging, mensagem de commit convencional, footer do Claude, push com flag -u.