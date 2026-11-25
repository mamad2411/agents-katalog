---
name: worktree-guide
description: Guia interativo para desenvolvimento paralelo com Ghostty, git worktrees e Lazygit. Use ao configurar fluxos de trabalho com múltiplas tarefas ou aprender o sistema de worktrees.
license: MIT
metadata:
  author: claude-code-templates
  version: "1.0"
---

Guie o usuário através de fluxos de trabalho de desenvolvimento paralelo usando painéis do terminal Ghostty, git worktrees e Lazygit. Esta é tanto uma experiência de aprendizado quanto uma referência prática.

---

## Verificação Inicial

Antes de começar, detecte o ambiente do usuário:

```bash
git rev-parse --is-inside-work-tree 2>&1 && echo "GIT_OK" || echo "NOT_GIT"
```

**Se não for um repositório git:**
> Este não é um repositório git. Navegue para um projeto git primeiro e depois volte a `/worktree-guide`.

Verifique se estamos em um worktree ou no repositório principal:
```bash
git worktree list
pwd
```

Anote o contexto para orientação posterior.

---

## Fase 1: Bem-vindo e Detecção de Contexto

Exiba com base no ambiente:

**Se estiver no repositório principal:**
```
## Guia de Desenvolvimento Paralelo com Worktree

Bem-vindo! Vou guiá-lo através da configuração e uso de worktrees paralelos para desenvolvimento com múltiplas tarefas.

┌─────────────────────────────────────────────────────────────┐
│  Terminal Ghostty                                           │
│  ┌──────────────────────┬──────────────────────┐           │
│  │                      │                      │           │
│  │   Claude (Tarefa 1)  │   Claude (Tarefa 2)  │           │
│  │   claude/login-page   │   claude/fix-auth-bug │           │
│  │                      │                      │           │
│  ├──────────────────────┴──────────────────────┤           │
│  │              Lazygit (monitoramento)        │           │
│  └─────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘

**Seu fluxo de trabalho:**
1. Criar worktrees → `/worktree-init`
2. Abrir painéis Ghostty → `Cmd+D` / `Cmd+Shift+D`
3. Executar Claude em cada painel → `cd <worktree> && claude`
4. Entregar quando concluído → `/worktree-deliver`
5. Limpar → `/worktree-cleanup`

O que você gostaria de fazer?
```

Use AskUserQuestion:
- "Aprender o fluxo completo" — Começar pela Fase 2
- "Apenas mostrar atalhos de teclado" — Pular para Quick Reference
- "Criar worktrees agora" — Sugerir `/worktree-init`
- "Outra coisa" — Perguntar o que precisa

**Se já estiver em um worktree:**
```
## Status do Worktree

Você já está dentro de um worktree! Deixe-me verificar seu status.
```

Em seguida, execute o equivalente a `/worktree-check` e forneça orientação contextual.

---

## Fase 2: Essenciais do Ghostty

**EXPLICAR:**
```
## Gerenciamento de Painéis Ghostty

O sistema de painéis do Ghostty é perfeito para desenvolvimento paralelo. Aqui estão os atalhos de teclado essenciais:
```

**MOSTRAR:**
```
┌─────────────────────────────────────────────────────────────┐
│                    ATALHOS DO GHOSTTY                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DIVISÃO                                                    │
│  ─────────                                                  │
│  Cmd+D           Dividir painel para a direita              │
│  Cmd+Shift+D     Dividir painel para baixo                  │
│                                                             │
│  NAVEGAÇÃO                                                  │
│  ─────────                                                  │
│  Cmd+Alt+←/→/↑/↓ Mover foco entre painéis                   │
│  Cmd+[/]         Ciclar entre painéis                       │
│                                                             │
│  DIMENSIONAMENTO                                            │
│  ─────────                                                  │
│  Cmd+Shift+E     Igualar tamanhos de todos os painéis       │
│  Cmd+Shift+F     Alternar zoom (painel em tela cheia)       │
│                                                             │
│  FECHAMENTO                                                 │
│  ─────────                                                  │
│  Cmd+W           Fechar painel atual                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

**Dica profissional:** Use Cmd+Shift+F para ampliar um painel quando precisar de foco, depois pressione novamente para voltar à visualização multi-painel.
```

**PAUSA** - "Pronto para aprender sobre Lazygit? (Ou pular para fluxo de trabalho)"

---

## Fase 3: Essenciais do Lazygit

**EXPLICAR:**
```
## Lazygit para Monitorar Worktrees

Lazygit oferece uma visão geral visual de todos os seus worktrees e suas alterações. Execute-o a partir do seu repositório principal para monitorar tudo.
```

**MOSTRAR:**
```
┌─────────────────────────────────────────────────────────────┐
│                    ATALHOS DO LAZYGIT                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WORKTREES (navegue para painel Worktrees)                  │
│  ─────────                                                  │
│  w              Alternar para painel de worktrees (ou criar) │
│  Enter          Alternar para worktree selecionado           │
│  n              Criar novo worktree                          │
│  d              Deletar worktree (com confirmação)           │
│                                                             │
│  ARQUIVOS & STAGING                                         │
│  ─────────                                                  │
│  Space          Fazer stage/unstage de arquivo              │
│  a              Fazer stage de todos os arquivos             │
│  Enter          Ver diff do arquivo (com Delta highlighting) │
│                                                             │
│  COMMITS                                                    │
│  ─────────                                                  │
│  c              Fazer commit das alterações em stage         │
│  C              Fazer commit com editor                      │
│  A              Amend do último commit                       │
│                                                             │
│  SINCRONIZAÇÃO                                              │
│  ─────────                                                  │
│  P              Push                                         │
│  p              Pull                                         │
│  f              Fetch                                        │
│                                                             │
│  GERAL                                                      │
│  ─────────                                                  │
│  ?              Ajuda (contextual)                           │
│  q              Sair / voltar                                │
│  Tab            Alternar painéis                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

**Fluxo de monitoramento:**
1. Abrir lazygit no repositório principal (ou painel Ghostty dedicado)
2. Pressionar `w` para ver todos os worktrees
3. Usar Enter para acessar alterações de qualquer worktree
4. Pressionar `q` para voltar à lista de worktrees
```

**PAUSA** - "Pronto para o passo a passo completo do fluxo de trabalho?"

---

## Fase 4: Fluxo de Trabalho Completo (Guiado)

**EXPLICAR:**
```
## Fluxo de Trabalho Completo de Desenvolvimento Paralelo

Vou guiá-lo através do ciclo completo. Faremos passo a passo.
```

### Passo 4.1: Criar Worktrees

**EXPLICAR:**
```
### Passo 1: Criar Worktrees

Primeiro, defina as tarefas que você deseja trabalhar em paralelo. O comando `/worktree-init` cria um worktree para cada tarefa.
```

**FAZER:** Mostrar exemplo de comando:
```
Exemplo de uso:

/worktree-init add user authentication | fix login bug | improve dashboard performance

Isso cria:
├── ../worktrees/<repo>/claude-add-user-authentication/
├── ../worktrees/<repo>/claude-fix-login-bug/
└── ../worktrees/<repo>/claude-improve-dashboard-performance/
```

### Passo 4.2: Abrir Painéis Ghostty

**EXPLICAR:**
```
### Passo 2: Abrir Painéis Ghostty

Agora divida seu terminal em painéis—um para cada tarefa, mais opcionalmente um para monitoramento com Lazygit.
```

**FAZER:**
```
1. Pressione Cmd+D para dividir para a direita (primeiro worktree)
2. Pressione Cmd+D novamente (segundo worktree)
3. Opcionalmente pressione Cmd+Shift+D em qualquer painel para Lazygit abaixo

Layout resultante:
┌──────────┬──────────┬──────────┐
│ Tarefa 1 │ Tarefa 2 │ Tarefa 3 │
│ claude   │ claude   │ claude   │
├──────────┴──────────┴──────────┤
│           lazygit              │
└────────────────────────────────┘
```

### Passo 4.3: Trabalhar em Cada Painel

**EXPLICAR:**
```
### Passo 3: Trabalhar Independentemente

Em cada painel:
1. cd para o caminho do worktree (a partir da saída dos comandos)
2. Execute `claude` para iniciar uma sessão Claude
3. Use `/worktree-check` a qualquer momento para verificar em qual tarefa está trabalhando
4. Trabalhe normalmente—Claude não sabe sobre outros painéis
```

### Passo 4.4: Entregar Trabalho Concluído

**EXPLICAR:**
```
### Passo 4: Entregar Quando Concluído

Quando terminar uma tarefa em qualquer painel, use `/worktree-deliver` para:
1. Revisar suas alterações
2. Criar um commit
3. Fazer push para remote
4. Criar um pull request
```

### Passo 4.5: Limpar

**EXPLICAR:**
```
### Passo 5: Limpar Após Merge

Depois que seus PRs forem mesclados no GitHub:
1. Volte ao repositório principal (não em um worktree)
2. Execute `/worktree-cleanup --all`
3. Remove worktrees e branches mesclados
```

---

## Fase 5: Solução de Problemas

**MOSTRAR:**
```
## Solução de Problemas

### "Não tenho certeza de qual worktree estou"

Execute `/worktree-check` — mostra sua branch, tarefa e status.

Alternativamente:
$ git branch --show-current    # Mostra claude/<name>
$ pwd                          # Mostra o caminho do worktree

---

### "Tenho alterações não confirmadas e quero alternar tarefas"

**Opção 1:** Fazer commit de work-in-progress
$ git add . && git commit -m "wip: progresso no recurso"

**Opção 2:** Fazer stash das alterações (temporário)
$ git stash push -m "wip: estacionando alterações"

Então no outro painel, continue trabalhando. Volte depois com:
$ git stash pop

---

### "Acidentalmente comecei a trabalhar no worktree errado"

1. Fazer stash de suas alterações: `git stash push -m "trabalho feito no lugar errado"`
2. Navegar para o worktree correto
3. Aplicar o stash: `git stash pop`

---

### "Meu worktree tem conflitos de merge"

1. Execute `git fetch origin` para obter as últimas versões
2. Execute `git rebase origin/main` (ou merge se preferir)
3. Resolva conflitos no seu editor
4. `git add .` depois `git rebase --continue`

---

### "Quero abandonar um worktree"

A partir do repositório principal:
$ git worktree remove ../worktrees/repo/claude-<name> --force
$ git branch -D claude/<name>

Nota: Force é necessário se houver alterações não confirmadas.

---

### "/worktree-deliver falhou no push"

Geralmente significa que a branch remota não existe ainda ou há um conflito.

Tente:
$ git push -u origin HEAD

Se houver conflito com remote, faça pull primeiro:
$ git pull --rebase origin claude/<name>

---

### "O caminho do worktree não existe mais"

O worktree foi provavelmente deletado manualmente. Limpe o estado git:
$ git worktree prune
```

---

## Fase 6: Cartão de Referência Rápida

**MOSTRAR:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REFERÊNCIA RÁPIDA DO WORKTREE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  COMANDOS                                                                   │
│  ─────────                                                                  │
│  /worktree-init <tarefa1> | <tarefa2>    Criar worktrees para tarefas para. │
│  /worktree-check                         Mostrar status & tarefa atual      │
│  /worktree-deliver                       Commit, push e criar PR            │
│  /worktree-cleanup --all                 Remover worktrees e branches mescladas │
│  /worktree-cleanup --dry-run             Visualizar o que seria limpo       │
│                                                                             │
│  GHOSTTY                                                                    │
│  ─────────                                                                  │
│  Cmd+D              Dividir direita  │  Cmd+Shift+E    Igualar painéis     │
│  Cmd+Shift+D        Dividir baixo    │  Cmd+Shift+F    Alternar zoom       │
│  Cmd+Alt+Arrows     Navegar         │  Cmd+W          Fechar painel       │
│                                                                             │
│  LAZYGIT                                                                    │
│  ─────────                                                                  │
│  w                  Painel worktrees │  Space          Stage/unstage       │
│  Enter              Ver diff         │  c              Commit              │
│  P                  Push             │  ?              Ajuda               │
│                                                                             │
│  GIT (manual)                                                               │
│  ─────────                                                                  │
│  git worktree list                   Listar todos os worktrees             │
│  git worktree add -b claude/name path Criar worktree manualmente           │
│  git worktree remove path            Remover um worktree                   │
│  git worktree prune                  Limpar refs de worktree obsoletos     │
│                                                                             │
│  FLUXO DE TRABALHO                                                          │
│  ─────────                                                                  │
│  1. /worktree-init tarefas...        Criar worktrees                       │
│  2. Cmd+D (dividir painéis)          Abrir painéis Ghostty                 │
│  3. cd <path> && claude              Iniciar Claude em cada                │
│  4. /worktree-deliver                PR quando concluído                    │
│  5. /worktree-cleanup                Limpar após merge                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Limitações de Segurança

- **Nunca executar comandos destrutivos** sem confirmação (worktree remove, branch delete)
- **Sempre verificar localização** antes de sugerir operações com worktree
- **Se o usuário parecer perdido**, ofereça `/worktree-check` primeiro
- **Nunca deletar com força** branches que não estão mescladas
- **Não assumir que as ferramentas estão instaladas** — verificar disponibilidade do lazygit ao sugerir
- **Respeitar o ritmo do usuário** — não se apressar pelas seções se ele quiser praticar
- **Manter o cartão de referência disponível** — oferecer exibi-lo sempre que relevante