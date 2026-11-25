---
name: clickup-group-progress
description: Acompanha e registra no ClickUp o andamento e planejamento de desenvolvimento de um grupo/projeto informado pelo usuário (não necessariamente “Nexus”) usando o MCP do ClickUp. Use quando o usuário pedir “status do <grupo>”, “o que mudou”, “o que está em progresso”, “blockers/risco”, “próximos itens”, “planejar feature”, “criar/update tarefas” ou “sincronizar contexto” com ClickUp — mesmo sem mencionar explicitamente “ClickUp”.
---

# ClickUp + Grupo: andamento e planejamento

## Objetivo
Usar o MCP do ClickUp para:
- **ver** o andamento do desenvolvimento do grupo informado pelo usuário (o que está em progresso, bloqueios e próximos itens);
- **planejar** novas funcionalidades (épicos/features → tarefas/subtarefas, prioridades e critérios de aceite);
- **registrar** no ClickUp o contexto técnico do trabalho, sempre indicando **módulo/arquivo/função** em foco.

## Regras obrigatórias de reporte (sempre cumprir)

Antes de qualquer atualização no ClickUp, produzir um “cartão de contexto” e reutilizá-lo em descrições/comentários:

```markdown
### Contexto técnico (obrigatório)
- App: <grupo informado pelo usuário>
- Módulo/arquivo: `<caminho/do/arquivo>`
- Função/classe: `<nome>`
- Escopo: `<1 frase>`
- Evidência: `<link/commit/PR> (se houver)`
```

Se o usuário não fornecer o grupo/projeto explicitamente (embora ele tenha dito que vai passar o nome), ou se não for possível inferir com alta confiança:
- App: `não identificado ainda`

Se a tarefa/épico-alvo no ClickUp não puder ser identificada com alta confiança (ex.: múltiplos matches sem contexto suficiente), não criar/atualizar/comentar no ClickUp: devolva a síntese ao usuário e solicite qual item deve ser atualizado.

## Feedback verbose ao usuário (obrigatório)

Sempre que a skill **criar/atualizar/comentar** no ClickUp (ou quando decidir **não** executar por falta de confiança), retornar uma confirmação explícita para o usuário, incluindo o que foi feito e o que não foi feito.

Formato obrigatório (ajuste os valores conforme o que o MCP retornar):

```markdown
### Confirmação de execução no ClickUp (verbose)
- Grupo: <grupo informado pelo usuário>
- Ação realizada:
  - Criados (N): <títulos/nomes> (ex.: <task_id> - <title>)
  - Atualizados (N): <títulos/nomes> (ex.: <task_id> - <title>)
  - Comentados (N): <títulos/nomes> (ex.: <task_id> - <title>)
- Local/Lista usada para criação (se aplicável):
  - List: <list_name> (id: <list_id>)
- Busca/identificação (para transparência):
  - Termos usados: <termos>
  - Itens candidatos: <quantidade>
- Não executado (se houver):
  - Motivo: <por que não deu para identificar com alta confiança / qual dado faltou>
  - O que preciso do usuário: <pergunta objetiva>
```

Regras de consistência:
- Se nenhum item foi criado/atualizado/comentado (por exemplo, por baixa confiança), preencher a seção como “Não executado” e retornar a síntese + a pergunta objetiva para destravar.
- Sempre que possível, inclua `task_id` (ou o identificador que o MCP retornar) junto do título para facilitar auditoria.

## Descoberta do “lugar do grupo” no ClickUp

1. **Encontrar por busca global (padrão)**:
   - Usar `clickup_search` com palavras-chave baseadas no grupo:
     - nome do grupo (exato e, quando útil, variações simples);
     - e termos genéricos de engenharia/roadmap: `roadmap`, `feature`, `epic`, `bug`, `blocker`, `backend`, `frontend`, `infra`, `release`.
   - Preferir filtrar `asset_types: ["task", "doc"]` quando o objetivo for status/backlog (se o MCP disponibilizar esses filtros no seu schema).

2. **Mapear a hierarquia (somente se necessário)**:
   - Se a busca não esclarecer onde ficam as listas/pastas do grupo, usar `clickup_get_workspace_hierarchy` com `max_depth: 2`.
   - Quando já houver `space_ids` conhecidos, limitar por `space_ids`.

3. **Trabalhar com listas conscientemente**:
   - Para criar tarefas, **nunca adivinhar a lista**: obter o `list_id` via `clickup_get_list` (por `list_name` ou `list_id`) antes de criar.
   - Registrar no texto qual lista foi usada (nome do list e/ou id quando disponível).

## Fluxo: “Ver andamento do desenvolvimento”

Quando o usuário pedir status:

1. **Coletar itens recentes**:
   - Usar `clickup_search` para retornar tarefas relevantes ao grupo e ordenar por `updated_at desc` quando suportado.
   - Se o usuário citar responsáveis, usar `filters.assignees` quando disponível; caso precise resolver nomes → usar `clickup_find_member_by_name` ou `clickup_resolve_assignees` (se existir no seu MCP).

2. **Gerar síntese objetiva (para o usuário)** e opcionalmente registrar no ClickUp:
   - **Em progresso**: top 5 tarefas mais recentemente atualizadas e com status ativo (quando houver informação de status);
   - **Bloqueios/risco**: itens com dependências, falta de definição, ou divergências claras no texto/descrição;
   - **Próximos**: 3 itens recomendados com justificativa curta.

3. **Registrar “status do dia” no ClickUp (quando solicitado ou quando fizer sentido)**:
   - Preferir `clickup_create_task_comment` na tarefa/épico raiz do grupo (ou na tarefa principal do candidato mais alinhado).
   - Se nenhum candidato for suficientemente adequado, não comentar no ClickUp e apenas devolver a síntese ao usuário.

O comentário deve começar com **Contexto técnico (obrigatório)** e terminar com:

```markdown
### Status
- Progresso: `<o que avançou>`
- Próximo passo: `<próxima ação>`
- Bloqueios: `<se houver>`
```

## Fluxo: “Planejar novas funcionalidades”

Quando o usuário pedir planejamento/roadmap:

1. **Normalizar a demanda**:
   - Transformar a solicitação em objetivo, não-objetivos, requisitos funcionais, requisitos não-funcionais, riscos e critérios de aceite.

2. **Propor decomposição**:
   - Criar um épico/tarefa-mãe (feature) e subtarefas por componente (backend, frontend, banco, infra, testes).
   - Para cada subtarefa: objetivo, entregável, critérios de aceite e “Contexto técnico (obrigatório)” (mesmo que inicial com `não identificado ainda`).

3. **Materializar no ClickUp**:
   - Criar/atualizar tarefas usando:
     - `clickup_create_task` (para novas tarefas) e
     - `clickup_update_task` (para ajustar descrição/prioridade/datas/status).
   - Para notas de refinamento, decisões e trade-offs, usar `clickup_create_task_comment`.

## Convenções de texto para tarefas do grupo

### Nome de tarefa (padrão)
Usar prefixos consistentes:
- `FEAT - ...` para funcionalidade
- `FIX - ...` para correção
- `TECH - ...` para débito técnico/refactor
- `CHORE - ...` para infra/rotina

### Descrição (padrão mínimo)

```markdown
### Contexto técnico (obrigatório)
- App: <grupo informado pelo usuário>
- Módulo/arquivo: `<caminho/do/arquivo>`
- Função/classe: `<nome>`
- Escopo: `<1 frase>`
- Evidência: `<link/commit/PR> (se houver)`

### Objetivo
<texto>

### Critérios de aceite
- [ ] <critério 1>
- [ ] <critério 2>

### Notas
<dependências, riscos, decisões>
```

## Ferramentas do MCP do ClickUp (as principais)
- `clickup_search`: busca global para localizar tarefas/docs e capturar “o que mudou”
- `clickup_get_workspace_hierarchy`: entender Spaces/Folders/Lists quando a busca não for suficiente
- `clickup_get_list`: resolver `list_id` por nome antes de criar tarefas
- `clickup_create_task` / `clickup_update_task`: criar/ajustar tarefas
- `clickup_create_task_comment`: registrar status, decisões, evidências e sempre o **módulo/função**
- (Opcional) `clickup_start_time_tracking` / `clickup_stop_time_tracking`: iniciar/parar apontamento quando o usuário pedir

## Exemplos de gatilhos
- “Mostra o andamento do grupo X no ClickUp” → usar fluxo de andamento + síntese
- “Planeja a feature Y para o grupo X” → decompor e criar tarefas/subtarefas + critérios de aceite
- “Atualiza a tarefa Z com o que foi feito hoje” → comentar na tarefa com o template e **módulo/função**
