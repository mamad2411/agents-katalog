---
name: using-git-worktrees
description: Use quando iniciando trabalho em feature que precisa isolamento do workspace atual ou antes de executar planos de implementação - cria git worktrees isoladas com seleção inteligente de diretório e verificação de segurança
---

# Usando Git Worktrees

## Visão Geral

Git worktrees criam workspaces isolados compartilhando o mesmo repositório, permitindo trabalhar em múltiplas branches simultaneamente sem fazer switch.

**Princípio central:** Seleção sistemática de diretório + verificação de segurança = isolamento confiável.

**Anuncie no início:** "Estou usando a skill using-git-worktrees para configurar um workspace isolado."

## Processo de Seleção de Diretório

Siga esta ordem de prioridade:

### 1. Verificar Diretórios Existentes

```bash
# Verificar em ordem de prioridade
ls -d .worktrees 2>/dev/null     # Preferido (oculto)
ls -d worktrees 2>/dev/null      # Alternativa
```

**Se encontrado:** Use esse diretório. Se ambos existem, `.worktrees` vence.

### 2. Verificar CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**Se preferência especificada:** Use sem perguntar.

### 3. Perguntar ao Usuário

Se nenhum diretório existe e nenhuma preferência em CLAUDE.md:

```
Nenhum diretório de worktree encontrado. Onde devo criar as worktrees?

1. .worktrees/ (local ao projeto, oculto)
2. ~/.config/superpowers/worktrees/<nome-projeto>/ (localização global)

Qual você prefere?
```

## Verificação de Segurança

### Para Diretórios Locais ao Projeto (.worktrees ou worktrees)

**DEVE verificar se diretório está ignorado antes de criar worktree:**

```bash
# Verificar se diretório está ignorado (respeita .gitignore local, global e sistema)
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**Se NÃO estiver ignorado:**

Conforme regra de Jesse "Corrija coisas quebradas imediatamente":
1. Adicione linha apropriada ao .gitignore
2. Commit da mudança
3. Prossiga com criação da worktree

**Por que crítico:** Evita acidentalmente fazer commit do conteúdo da worktree ao repositório.

### Para Diretório Global (~/.config/superpowers/worktrees)

Nenhuma verificação de .gitignore necessária - fora do projeto inteiramente.

## Passos de Criação

### 1. Detectar Nome do Projeto

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Criar Worktree

```bash
# Determinar caminho completo
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Criar worktree com nova branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Executar Setup do Projeto

Auto-detectar e executar setup apropriado:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verificar Baseline Limpo

Executar testes para garantir que worktree inicia limpa:

```bash
# Exemplos - use comando apropriado para o projeto
npm test
cargo test
pytest
go test ./...
```

**Se testes falharem:** Reportar falhas, perguntar se deve prosseguir ou investigar.

**Se testes passarem:** Reportar pronto.

### 5. Reportar Localização

```
Worktree pronta em <caminho-completo>
Testes passando (<N> testes, 0 falhas)
Pronto para implementar <nome-feature>
```

## Referência Rápida

| Situação | Ação |
|----------|------|
| `.worktrees/` existe | Use (verifique ignorado) |
| `worktrees/` existe | Use (verifique ignorado) |
| Ambos existem | Use `.worktrees/` |
| Nenhum existe | Verificar CLAUDE.md → Perguntar usuário |
| Diretório não ignorado | Adicionar ao .gitignore + commit |
| Testes falham durante baseline | Reportar falhas + perguntar |
| Sem package.json/Cargo.toml | Pular instalação de dependências |

## Erros Comuns

### Pular verificação de ignore

- **Problema:** Conteúdo da worktree fica rastreado, polui git status
- **Solução:** Sempre use `git check-ignore` antes de criar worktree local ao projeto

### Assumir localização do diretório

- **Problema:** Cria inconsistência, viola convenções do projeto
- **Solução:** Siga prioridade: existente > CLAUDE.md > perguntar

### Prosseguir com testes falhando

- **Problema:** Não consegue distinguir bugs novos de problemas pré-existentes
- **Solução:** Reportar falhas, obter permissão explícita para prosseguir

### Hardcodificar comandos de setup

- **Problema:** Quebra em projetos usando ferramentas diferentes
- **Solução:** Auto-detectar de arquivos do projeto (package.json, etc.)

## Exemplo de Workflow

```
Você: Estou usando a skill using-git-worktrees para configurar um workspace isolado.

[Verificar .worktrees/ - existe]
[Verificar ignorado - git check-ignore confirma .worktrees/ está ignorado]
[Criar worktree: git worktree add .worktrees/auth -b feature/auth]
[Executar npm install]
[Executar npm test - 47 passando]

Worktree pronta em /Users/jesse/myproject/.worktrees/auth
Testes passando (47 testes, 0 falhas)
Pronto para implementar feature de auth
```

## Red Flags

**Nunca:**
- Criar worktree sem verificar se está ignorada (local ao projeto)
- Pular verificação de baseline de testes
- Prosseguir com testes falhando sem perguntar
- Assumir localização do diretório quando ambíguo
- Pular verificação de CLAUDE.md

**Sempre:**
- Seguir prioridade de diretório: existente > CLAUDE.md > perguntar
- Verificar se diretório está ignorado para local ao projeto
- Auto-detectar e executar setup do projeto
- Verificar baseline de testes limpo

## Integração

**Chamada por:**
- **brainstorming** (Fase 4) - OBRIGATÓRIA quando design é aprovado e implementação segue
- Qualquer skill precisando de workspace isolado

**Funciona com:**
- **finishing-a-development-branch** - OBRIGATÓRIA para limpeza após trabalho completo
- **executing-plans** ou **subagent-driven-development** - Trabalho acontece nesta worktree