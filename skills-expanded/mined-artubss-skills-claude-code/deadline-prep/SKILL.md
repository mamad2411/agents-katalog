---
name: deadline-prep
description: Gera um esboço de demo estruturado a partir do histórico de alterações da sua sessão e git history. Lê .claude/critical_log_changes.csv e git log para produzir talking points prontos para apresentação em demos de fim de dia, standups ou prazos de entrega.
---

# Deadline Prep

Gera um esboço de demo estruturado a partir do seu trabalho na sessão. Combina o CSV do change log (do hook change-logger) com o histórico do git para criar talking points prontos para apresentação.

## Workflow

### Step 1: Coletar fontes de dados

**Change log** (fonte primária se disponível):
- Leia `.claude/critical_log_changes.csv` se existir
- Parse das colunas: timestamp, tool, file_path, action, details
- Agrupe por: arquivos criados, arquivos modificados, comandos executados

**Git history** (sempre disponível):
```bash
git log --oneline --since="today 00:00"
git diff --stat HEAD~10 2>/dev/null || git diff --stat
```

Se o CSV não existir, volte para o modo somente git e anote isso na saída.

### Step 2: Analisar e categorizar alterações

Agrupe todas as alterações em categorias:

| Categoria | Sinais |
|-----------|--------|
| **Features entregues** | Novos arquivos, novas rotas, novos componentes, commits `feat` |
| **Correções de bugs** | Arquivos modificados com commits `fix`, mudanças de tratamento de erro |
| **Refatores** | Arquivos renomeados, mudanças estruturais, commits `refactor` |
| **Config/Setup** | package.json, tsconfig, CI/CD, mudanças Docker |
| **Testes** | Arquivos de teste criados ou modificados |
| **Documentação** | README, docs, comentários |

### Step 3: Gerar o esboço da demo

Crie um documento markdown estruturado:

```markdown
# Demo Outline — [Data]

## O que entreguei
- **[Nome da Feature/Fix]**: Uma frase explicando o que faz e por que importa
- **[Nome da Feature/Fix]**: Uma frase explicando o que faz e por que importa
- **[Nome da Feature/Fix]**: Uma frase explicando o que faz e por que importa

## Decisões de Arquitetura
- **[Decisão]**: Por que escolhi essa abordagem em vez de alternativas
- **[Decisão]**: Tradeoff que fiz e o raciocínio

## O que faria a seguir
1. **[Prioridade 1]**: Por que este é o passo mais importante
2. **[Prioridade 2]**: O que isso desbloquearia
3. **[Prioridade 3]**: Melhoria interessante de se ter

## Métricas da Sessão
- Arquivos modificados: X
- Linhas: +Y / -Z
- Commits: N
- Arquivos-chave: `path/to/important/file.ts`, `path/to/other.ts`
- Janela de tempo: HH:MM - HH:MM
```

### Step 4: Salvar e apresentar

Salve o esboço em `.claude/demo-outline.md`.

Imprima o esboço completo no terminal para que você possa revisar imediatamente.

## Dicas

- Execute isso 30 minutos antes do seu deadline para ter tempo de revisar e adicionar contexto pessoal
- A seção "Decisões de Arquitetura" é o que os revisores mais se importam — adicione contexto sobre os tradeoffs
- "O que faria a seguir" mostra que você pensa além da tarefa imediata
- Edite o esboço gerado para adicionar sua própria voz e qualquer contexto que o log tenha perdido
- Funciona melhor com o hook `change-logger` instalado, mas funciona apenas com git history também