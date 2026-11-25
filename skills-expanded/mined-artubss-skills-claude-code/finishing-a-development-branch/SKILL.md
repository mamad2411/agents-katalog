---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finalizando uma Branch de Desenvolvimento

## Visão Geral

Guie a conclusão do trabalho de desenvolvimento apresentando opções claras e executando o fluxo escolhido.

**Princípio central:** Verificar testes → Apresentar opções → Executar escolha → Limpar.

**Anuncie no início:** "Estou usando a skill finishing-a-development-branch para completar este trabalho."

## O Processo

### Etapa 1: Verificar Testes

**Antes de apresentar opções, verifique se os testes passam:**

```bash
# Executar suite de testes do projeto
npm test / cargo test / pytest / go test ./...
```

**Se os testes falharem:**
```
Testes falhando (<N> falhas). Deve-se corrigir antes de completar:

[Mostrar falhas]

Não é possível prosseguir com merge/PR até que os testes passem.
```

Pare. Não prossiga para a Etapa 2.

**Se os testes passarem:** Prossiga para a Etapa 2.

### Etapa 2: Determinar Branch Base

```bash
# Tentar branches base comuns
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Ou pergunte: "Esta branch foi criada a partir de main - isso está correto?"

### Etapa 3: Apresentar Opções

Apresente exatamente estas 4 opções:

```
Implementação completa. O que você gostaria de fazer?

1. Fazer merge de volta para <base-branch> localmente
2. Fazer push e criar um Pull Request
3. Manter a branch como está (vou lidar depois)
4. Descartar este trabalho

Qual opção?
```

**Não adicione explicações** - mantenha as opções concisas.

### Etapa 4: Executar Escolha

#### Opção 1: Fazer Merge Localmente

```bash
# Mudar para branch base
git checkout <base-branch>

# Atualizar
git pull

# Fazer merge da branch de feature
git merge <feature-branch>

# Verificar testes no resultado do merge
<comando de teste>

# Se os testes passarem
git branch -d <feature-branch>
```

Depois: Limpar worktree (Etapa 5)

#### Opção 2: Fazer Push e Criar PR

```bash
# Fazer push da branch
git push -u origin <feature-branch>

# Criar PR
gh pr create --title "<título>" --body "$(cat <<'EOF'
## Resumo
<2-3 bullets do que mudou>

## Plano de Teste
- [ ] <passos de verificação>
EOF
)"
```

Depois: Limpar worktree (Etapa 5)

#### Opção 3: Manter Como Está

Relatar: "Mantendo branch <nome>. Worktree preservada em <caminho>."

**Não limpe a worktree.**

#### Opção 4: Descartar

**Confirme primeiro:**
```
Isso vai deletar permanentemente:
- Branch <nome>
- Todos os commits: <lista-de-commits>
- Worktree em <caminho>

Digite 'descartar' para confirmar.
```

Aguarde a confirmação exata.

Se confirmado:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Depois: Limpar worktree (Etapa 5)

### Etapa 5: Limpar Worktree

**Para Opções 1, 2, 4:**

Verificar se está em worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

Se sim:
```bash
git worktree remove <caminho-worktree>
```

**Para Opção 3:** Manter worktree.

## Referência Rápida

| Opção | Merge | Push | Manter Worktree | Limpar Branch |
|-------|-------|------|-----------------|----------------|
| 1. Fazer merge localmente | ✓ | - | - | ✓ |
| 2. Criar PR | - | ✓ | ✓ | - |
| 3. Manter como está | - | - | ✓ | - |
| 4. Descartar | - | - | - | ✓ (force) |

## Erros Comuns

**Pular verificação de testes**
- **Problema:** Fazer merge de código quebrado, criar PR com falhas
- **Solução:** Sempre verificar testes antes de oferecer opções

**Perguntas abertas**
- **Problema:** "O que faço agora?" → ambíguo
- **Solução:** Apresentar exatamente 4 opções estruturadas

**Limpeza automática de worktree**
- **Problema:** Remover worktree quando você pode precisar dela (Opções 2, 3)
- **Solução:** Limpar apenas para Opções 1 e 4

**Sem confirmação para descartar**
- **Problema:** Deletar trabalho acidentalmente
- **Solução:** Exigir confirmação digitada "descartar"

## Sinais de Alerta

**Nunca:**
- Prosseguir com testes falhando
- Fazer merge sem verificar testes no resultado
- Deletar trabalho sem confirmação
- Fazer força de push sem solicitação explícita

**Sempre:**
- Verificar testes antes de oferecer opções
- Apresentar exatamente 4 opções
- Obter confirmação digitada para Opção 4
- Limpar worktree apenas para Opções 1 & 4

## Integração

**Chamada por:**
- **subagent-driven-development** (Etapa 7) - Após todas as tarefas completarem
- **executing-plans** (Etapa 5) - Após todos os batches completarem

**Funciona com:**
- **using-git-worktrees** - Limpa a worktree criada por aquela skill