---
name: daily-meeting-update
description: "Gerador interativo de atualizações de daily standup/reunião. Use quando o usuário menciona 'daily', 'standup', 'scrum update', 'status update', 'o que fiz ontem', 'preparar para reunião', 'atualização matinal' ou 'sincronização de time'. Extrai atividade do GitHub, Jira e histórico de sessões Claude Code. Realiza entrevista com 4 perguntas (ontem, hoje, bloqueadores, tópicos de discussão) e gera atualização formatada em Markdown."
user-invocable: true
---

# Daily Meeting Update

Gere uma atualização de daily standup/reunião através de uma **entrevista interativa**. Nunca assuma que ferramentas estão configuradas—pergunte antes.

---

## Fluxo de trabalho

```
INÍCIO
  │
  ▼
┌─────────────────────────────────────────────────────┐
│ Fase 1: DETECTAR & OFERECER INTEGRAÇÕES             │
│ • Verificar: Histórico Claude Code? gh CLI? jira CLI? │
│ • Claude Code → Extrair resumo da sessão de ontem   │
│   → Usuário seleciona itens relevantes via multiSelect │
│ • GitHub/Jira → Perguntar ao usuário, extrair se aprovado │
│ • Extrair dados AGORA (antes da entrevista)         │
├─────────────────────────────────────────────────────┤
│ Fase 2: ENTREVISTA (com contexto)                   │
│ • Mostrar dados extraídos como contexto             │
│ • Ontem: "Vi que você fez merge do PR #123, mais algo?" │
│ • Hoje: No que você vai trabalhar?                  │
│ • Bloqueadores: Algo te bloqueando?                 │
│ • Tópicos: Algo para discutir no fim da reunião?    │
├─────────────────────────────────────────────────────┤
│ Fase 3: GERAR ATUALIZAÇÃO                           │
│ • Combinar respostas da entrevista + dados de ferramentas │
│ • Formatar como Markdown limpo                      │
│ • Apresentar ao usuário                             │
└─────────────────────────────────────────────────────┘
```

---

## Fase 1: Detectar & Oferecer Integrações

### Passo 1: Detecção Silenciosa

Verificar integrações disponíveis **silenciosamente** (suprimir erros, não mostrar ao usuário):

| Integração | Detecção |
|-------------|----------|
| **Histórico Claude Code** | Diretório `~/.claude/projects` existe com arquivos `.jsonl` |
| GitHub CLI | `gh auth status` bem-sucedido |
| Jira CLI | Comando `jira` existe |
| Atlassian MCP | Ferramentas `mcp__atlassian__*` disponíveis |
| Git | Dentro de um repositório git |

### Passo 2: Oferecer Integrações GitHub/Jira (se disponíveis)

> **Usuários Claude Code:** Use a ferramenta `AskUserQuestionTool` para todas as perguntas nesta fase.

**GitHub/Git:**

Se `HAS_GH` ou `HAS_GIT`:

```
"Detectei que você tem GitHub/Git configurado. Quer que eu extraia sua atividade recente (commits, PRs, reviews)?"

Opções:
- "Sim, extrai as informações"
- "Não, vou fornecer tudo manualmente"
```

Se sim:

```
"Quais repositórios/projetos devo verificar?"

Opções:
- "Apenas o diretório atual" (se dentro de um repositório git)
- "Vou listar os repositórios" → usuário fornece lista
```

**Jira:**

Se `HAS_JIRA_CLI` ou `HAS_ATLASSIAN_MCP`:

```
"Detectei que você tem Jira configurado. Quer que eu extraia seus tickets?"

Opções:
- "Sim, extraia meus tickets"
- "Não, vou fornecer tudo manualmente"
```

### Passo 3: Extrair Dados GitHub/Jira (se aprovado)

**GitHub/Git** — Para cada repositório aprovado:
- Commits do usuário desde ontem
- PRs abertos/mesclados pelo usuário
- Reviews feitos pelo usuário

**Jira** — Tickets atribuídos ao usuário, atualizados nas últimas 24h

**Insight importante**: Armazenar resultados para usar como contexto na entrevista da Fase 2.

### Passo 4: Oferecer Histórico Claude Code

Esta integração captura tudo o que você trabalhou com Claude Code — útil para lembrar trabalhos que não estão em git ou Jira.

**Detecção:**
```bash
ls ~/.claude/projects/*/*.jsonl 2>/dev/null | head -1
```

**Se histórico Claude Code existe, pergunte:**

```
"Posso também extrair seu histórico de sessões Claude Code de ontem. Isso ajuda a lembrar trabalho que não está em git/Jira (pesquisa, debugging, planejamento). Quer que eu verifique?"

Opções:
- "Sim, extraia minhas sessões Claude Code"
- "Não, tenho tudo que preciso"
```

**Se sim, execute o script de resumo:**

```bash
python3 ~/.claude/skills/daily-meeting-update/scripts/claude_digest.py --format json
```

**Depois apresente sessões com multiSelect:**

Use `AskUserQuestionTool` com `multiSelect: true` para deixar usuário escolher itens relevantes:

```
"Aqui estão suas sessões Claude Code de ontem. Selecione as relevantes para seu standup:"

Opções (multiSelect):
- "Corrigir bug de autenticação (backend-api)"
- "Implementar fluxo OAuth (backend-api)"
- "Atualizar estilos da homepage (frontend-app)"
- "Pesquisar provedores de pagamento (docs)"
```

**Insight importante:** Usuário seleciona quais sessões são relacionadas a trabalho. Projetos pessoais ou experimentos podem ser excluídos.

**NÃO execute o script de resumo quando:**
- Usuário diz explicitamente "Não" ao histórico Claude Code
- Usuário diz que vai fornecer tudo manualmente
- Diretório `~/.claude/projects` não existe

**Se script de resumo falhar:**
- Fallback: Pule integração Claude Code silenciosamente, prossiga com entrevista
- Problemas comuns: Python não instalado, sem sessões de ontem, erros de permissão
- NÃO bloqueie o fluxo do standup — o script é suplementar, não obrigatório

---

## Fase 2: Entrevista (com contexto)

> **Usuários Claude Code:** Use a ferramenta `AskUserQuestionTool` para conduzir a entrevista. Isso oferece melhor UX com opções estruturadas.

**Use dados extraídos como contexto** para fazer perguntas mais inteligentes.

### Pergunta 1: Ontem

**Se dados foram extraídos**, mostre primeiro:

```
"Aqui está o que encontrei de sua atividade:
- Merge do PR #123: fix login timeout
- 3 commits em backend-api
- Review do PR #456 (aprovado)

Trabalhou em mais algo ontem que eu possa ter perdido?"
```

**Se nenhum dado foi extraído:**

```
"No que você trabalhou ontem/desde o último standup?"
```

Se resposta do usuário for vaga, pergunte mais:
- "Pode detalhar mais sobre X?"
- "Completou algo específico?"

### Pergunta 2: Hoje

```
"No que você vai trabalhar hoje?"

Opções:
- [Entrada de texto - usuário escreve livremente]
```

**Se dados de Jira foram extraídos**, você pode sugerir:

```
"Vi que você tem esses tickets atribuídos:
- PROJ-123: Implementar fluxo OAuth (Em Progresso)
- PROJ-456: Corrigir bug de pagamento (To Do)

Vai trabalhar em algum deles hoje?"
```

### Pergunta 3: Bloqueadores

```
"Tem algum bloqueador ou impedimento?"

Opções:
- "Sem bloqueadores"
- "Sim, tenho bloqueadores" → acompanhamento para detalhes
```

### Pergunta 4: Tópicos para Discussão

```
"Tem algum tópico que quer trazer no fim do daily?"

Opções:
- "Não, nada a discutir"
- "Sim" → acompanhamento para detalhes

Exemplos de tópicos:
- Decisão técnica que precisa de input
- Alinhamento com outro time
- Pergunta sobre priorização
- Anúncio ou informação para o time
```

---

## Fase 3: Gerar Atualização

Combine todas as informações em Markdown limpo:

```markdown
# Daily Update - [DATA]

## Ontem
- [Itens da entrevista]
- [Itens do GitHub/Jira se extraídos]

## Hoje
- [Itens da entrevista]

## Bloqueadores
- [Bloqueadores ou "Sem bloqueadores"]

## PRs & Reviews (se extraído do GitHub)
- [PRs abertos]
- [PRs mesclados]
- [Reviews realizados]

## Jira (se extraído do Jira)
- [Tickets atualizados]

## Tópicos para Discussão
- [Tópicos ou "Nenhum"]

---
*Links:*
- [Links de PR]
- [Links de tickets]
```

---

## Princípios Principais

1. **Entrevista é primária** — Ferramentas complementam, não substituem contexto humano
2. **Consentimento antes de acesso** — Sempre pergunte antes de extrair de qualquer integração
3. **Perguntas conscientes** — Mostre dados extraídos durante entrevista para disparar memória ("Vi que você fez merge do PR #123...")

---

## Referência Rápida

| Fase | Ação | Ferramenta |
|------|------|-----------|
| 1. Detectar & Oferecer | Verificar gh/jira/histórico claude, perguntar ao usuário, extrair dados | Bash (silencioso), AskUserQuestionTool* |
| 2. Entrevista | Fazer 4 perguntas com contexto | AskUserQuestionTool* |
| 3. Gerar | Formatar Markdown | Texto de saída |

*Apenas Claude Code: Use a ferramenta `AskUserQuestionTool` para perguntas estruturadas.

### Script de Resumo Claude Code

```bash
# Obter sessões de ontem como JSON
python3 ~/.claude/skills/daily-meeting-update/scripts/claude_digest.py --format json

# Obter sessões de hoje
python3 ~/.claude/skills/daily-meeting-update/scripts/claude_digest.py --date today --format json

# Filtrar para projeto específico
python3 ~/.claude/skills/daily-meeting-update/scripts/claude_digest.py --project ~/my-app --format json
```

---

## Exemplo de Sessão

```
Claude: "Vamos preparar seu daily! Detectei GitHub configurado. Quer que eu extraia sua atividade recente?"
Usuário: "Sim"

Claude: "Quais repositórios devo verificar?"
Usuário: "backend-api e frontend-app"

[Claude extrai dados do GitHub silenciosamente]

Claude: "Posso também extrair seu histórico de sessões Claude Code de ontem. Quer que eu verifique?"
Usuário: "Sim"

[Claude executa script de resumo, obtém 5 sessões]

Claude: "Aqui estão suas sessões Claude Code de ontem. Selecione as relevantes para seu standup:"
  ☑ Corrigir bug de timeout de autenticação (backend-api)
  ☑ Implementar fluxo OAuth (backend-api)
  ☐ Atualizar blog pessoal (blog) - [usuário desseleciona projeto pessoal]
  ☑ Pesquisar provedores de pagamento (docs)
  ☐ Debugar falhas em testes (experiments)

Usuário: [seleciona 3 itens relevantes]

Claude: "Aqui está o que encontrei de sua atividade:
- Merge do PR #120: fix login timeout
- Aberto PR #125: feat: add OAuth flow
- Review do PR #123 (aprovado), PR #456 (changes requested)
- 5 commits em backend-api
- [Do Claude Code] Corrigir bug de timeout de autenticação
- [Do Claude Code] Implementar fluxo OAuth
- [Do Claude Code] Pesquisar provedores de pagamento

Trabalhou em mais algo ontem que eu possa ter perdido?"
Usuário: "Não, cobre tudo"

Claude: "No que você vai trabalhar hoje?"
Usuário: "Continuar com o recurso OAuth e fazer deploy para staging"

Claude: "Tem algum bloqueador?"
Usuário: "Não"

Claude: "Tem algum tópico para trazer no fim do daily?"
Usuário: "Sim, quero discutir a arquitetura do novo módulo de pagamentos"

[Claude gera atualização]
```

---

## Exemplo de Saída

```markdown
# Daily Update - 2026-01-22

## Ontem
- Trabalhou em feature de autenticação
- Pesquisa em provedores de pagamento
- Merge do PR #120 (fix: login timeout)
- Aberto PR #125 (feat: add OAuth flow)

## Hoje
- Continuar com feature OAuth
- Deploy para staging

## Bloqueadores
- Sem bloqueadores

## PRs & Reviews
- **Aberto:** PR #125 - feat: add OAuth flow
- **Mesclado:** PR #120 - fix: login timeout
- **Reviews:** PR #123 (aprovado), PR #456 (changes requested)

## Tópicos para Discussão
- Arquitetura do novo módulo de pagamentos

---
*Links:*
- https://github.com/org/repo/pull/125
- https://github.com/org/repo/pull/120
```

---

## Anti-Padrões

| Evite | Por quê (Conhecimento Especialista) | Faça Instead |
|------|-------------------------------------|-------------|
| Executar gh/jira sem perguntar | Usuários podem ter repositórios pessoais visíveis, ou estar em contexto de projeto sensível que não querem exposto | Sempre pergunte primeiro, deixe usuário escolher repositórios |
| Assumir diretório atual é único projeto | Desenvolvedores frequentemente trabalham em 2-5 repositórios simultaneamente (frontend, backend, infra) | Pergunte "Em quais projetos você está trabalhando?" |
| Pular entrevista mesmo com dados de ferramentas | Ferramentas capturam O QUE aconteceu mas perdem POR QUÊ e contexto (pesquisa, reuniões, planejamento) | Entrevista é primária, ferramentas complementam |
| Gerar atualização antes de todas 4 perguntas | Usuário pode ter bloqueador crítico ou tópico de discussão que muda a narrativa | Complete entrevista, depois gere |
| Incluir mensagens de commit brutas | Mensagens de commit são frequentemente crípticas ("fix", "wip") e não contam a história | Resuma em resultados legíveis por humanos |
| Pedir dados depois da entrevista | Mostrar contexto durante entrevista torna perguntas mais inteligentes ("Vi que você fez merge do PR #123, mais algo?") | Extraia dados primeiro, depois entreviste com contexto |

---

## NUNCA

- **NUNCA assuma que ferramentas estão configuradas** — Muitos devs têm gh instalado mas não autenticado, ou jira CLI apontando para instância errada
- **NUNCA pule pergunta "Tópicos para Discussão"** — Esta é frequentemente a parte mais valiosa do standup que ferramentas não conseguem capturar
- **NUNCA gere mais de 15 bullets** — Standup deve levar <2 minutos para ler; atualizações longas perdem a audiência
- **NUNCA inclua números de ticket/PR sem contexto** — "PROJ-123" não significa nada; sempre inclua título ou resumo
- **NUNCA extraia dados de repositórios que usuário não aprovara explicitamente** — Mesmo que consiga ver outros repositórios, respeite limites