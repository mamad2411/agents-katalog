---
name: jira
description: Use quando o usuário menciona issues do Jira (ex: "PROJ-123"), pergunta sobre tickets, quer criar/visualizar/atualizar issues, verificar status do sprint ou gerenciar seu workflow no Jira. Ativa em palavras-chave como "jira", "issue", "ticket", "sprint", "backlog" ou padrões de chaves de issue.
---

# Jira

Interação em linguagem natural com Jira. Suporta múltiplos backends.

## Detecção de Backend

**Execute esta verificação primeiro** para determinar qual backend usar:

```
1. Verifique se a CLI jira está disponível:
   → Execute: which jira
   → Se encontrado: USE CLI BACKEND

2. Se não houver CLI, verifique Atlassian MCP:
   → Procure por tools mcp__atlassian__*
   → Se disponível: USE MCP BACKEND

3. Se nenhum estiver disponível:
   → GUIE O USUÁRIO PARA CONFIGURAÇÃO
```

| Backend | Quando Usar | Referência |
|---------|-------------|-----------|
| **CLI** | Comando `jira` disponível | `references/commands.md` |
| **MCP** | Tools Atlassian MCP disponíveis | `references/mcp.md` |
| **Nenhum** | Nenhum disponível | Guia para instalar CLI |

---

## Referência Rápida (CLI)

> Pule esta seção se estiver usando o backend MCP.

| Intenção | Comando |
|----------|---------|
| Visualizar issue | `jira issue view ISSUE-KEY` |
| Listar minhas issues | `jira issue list -a$(jira me)` |
| Minhas em andamento | `jira issue list -a$(jira me) -s"In Progress"` |
| Criar issue | `jira issue create -tType -s"Summary" -b"Description"` |
| Mover/transicionar | `jira issue move ISSUE-KEY "State"` |
| Atribuir a mim | `jira issue assign ISSUE-KEY $(jira me)` |
| Desatribuir | `jira issue assign ISSUE-KEY x` |
| Adicionar comentário | `jira issue comment add ISSUE-KEY -b"Comment text"` |
| Abrir no navegador | `jira open ISSUE-KEY` |
| Sprint atual | `jira sprint list --state active` |
| Quem sou eu | `jira me` |

---

## Referência Rápida (MCP)

> Pule esta seção se estiver usando o backend CLI.

| Intenção | Tool MCP |
|----------|----------|
| Buscar issues | `mcp__atlassian__searchJiraIssuesUsingJql` |
| Visualizar issue | `mcp__atlassian__getJiraIssue` |
| Criar issue | `mcp__atlassian__createJiraIssue` |
| Atualizar issue | `mcp__atlassian__editJiraIssue` |
| Obter transições | `mcp__atlassian__getTransitionsForJiraIssue` |
| Transicionar | `mcp__atlassian__transitionJiraIssue` |
| Adicionar comentário | `mcp__atlassian__addCommentToJiraIssue` |
| Buscar usuário | `mcp__atlassian__lookupJiraAccountId` |
| Listar projetos | `mcp__atlassian__getVisibleJiraProjects` |

Veja `references/mcp.md` para padrões MCP completos.

---

## Gatilhos

- "criar um ticket no jira"
- "mostre-me PROJ-123"
- "listar meus tickets"
- "mover ticket para concluído"
- "o que tem no sprint atual"

---

## Detecção de Chave de Issue

Chaves de issue seguem o padrão: `[A-Z]+-[0-9]+` (ex: PROJ-123, ABC-1).

Quando um usuário menciona uma chave de issue na conversa:
- **CLI:** `jira issue view KEY` ou `jira open KEY`
- **MCP:** `mcp__atlassian__jira_get_issue` com a chave

---

## Workflow

**Criando tickets:**
1. Pesquise contexto se o usuário referencia código/tickets/PRs
2. Draftar conteúdo do ticket
3. Revisar com o usuário
4. Criar usando o backend apropriado

**Atualizando tickets:**
1. Busque detalhes da issue primeiro
2. Verifique status (cuidado com tickets em andamento)
3. Mostre mudanças atuais vs propostas
4. Obtenha aprovação antes de atualizar
5. Adicione comentário explicando as mudanças

---

## Antes de Qualquer Operação

Pergunte-se:

1. **Qual é o estado atual?** — Sempre busque a issue primeiro. Não assuma que status, responsável ou campos são o que o usuário pensa que são.

2. **Quem mais será afetado?** — Verifique observadores, issues vinculadas, epics pai. Uma "edição simples" pode notificar 10 pessoas.

3. **Isso é reversível?** — Transições podem ter portões de mão única. Alguns workflows requerem estados intermediários. Edições de descrição não têm desfazer.

4. **Tenho os identificadores corretos?** — Chaves de issue, IDs de transição, IDs de conta. Nomes de exibição não funcionam para atribuição (MCP).

---

## NUNCA

- **NUNCA transicione sem buscar status atual** — Workflows podem exigir estados intermediários. "A Fazer" → "Concluído" pode falhar silenciosamente se "Em Andamento" for necessário primeiro.

- **NUNCA atribua usando nome de exibição (MCP)** — Apenas IDs de conta funcionam. Sempre chame `lookupJiraAccountId` primeiro, ou a atribuição falha silenciosamente.

- **NUNCA edite descrição sem mostrar original** — Jira não tem desfazer. O usuário deve ver o que está substituindo.

- **NUNCA use `--no-input` sem todos os campos obrigatórios (CLI)** — Falha silenciosamente com erros crípticos. Verifique campos obrigatórios do projeto primeiro.

- **NUNCA assuma que nomes de transição são universais** — "Concluído", "Fechado", "Completo" variam por projeto. Sempre obtenha transições disponíveis primeiro.

- **NUNCA modifique em lote sem aprovação explícita** — Cada mudança de ticket notifica observadores. 10 edições = 10 tempestades de notificação.

---

## Segurança

- Sempre mostre o comando/tool call antes de executá-lo
- Sempre obtenha aprovação antes de modificar tickets
- Preserve informações originais ao editar
- Verifique atualizações após aplicar
- Sempre suplemente problemas de autenticação claramente para que o usuário possa resolvê-los

---

## Nenhum Backend Disponível

Se nem CLI nem MCP estiverem disponíveis, guie o usuário:

```
Para usar Jira, você precisa de um destes:

1. **jira CLI** (recomendado):
   https://github.com/ankitpokhrel/jira-cli

   Instalar: brew install ankitpokhrel/jira-cli/jira-cli
   Configurar: jira init

2. **Atlassian MCP**:
   Configure em suas configurações MCP com credenciais Atlassian.
```

---

## Mergulho Profundo

**CARREGUE referência quando:**
- Criando issues com campos complexos ou conteúdo multilinhas
- Construindo queries JQL além de filtros simples
- Solucionando erros ou problemas de autenticação
- Trabalhando com transições, vinculação ou sprints

**NÃO carregue referência para:**
- Operações simples de visualização/listagem (Referência Rápida acima é suficiente)
- Verificações de status básicas (`jira issue view KEY`)
- Abrir issues no navegador

| Tarefa | Carregar Referência? |
|--------|-----------------|
| Visualizar issue única | Não |
| Listar meus tickets | Não |
| Criar com descrição | **Sim** — CLI precisa do padrão `/tmp` |
| Transicionar issue | **Sim** — precisa de ID de transição de workflow |
| Busca JQL | **Sim** — para queries complexas |
| Vincular issues | **Sim** — limitação MCP, precisa de script |

Referências:
- Padrões CLI: `references/commands.md`
- Padrões MCP: `references/mcp.md`