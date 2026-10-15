---
name: clickup-nexus-progress
description: Acompanha e registra no ClickUp o andamento do desenvolvimento do Nexus (em progresso, bloqueios e próximos passos) e apoia planejamento/roadmap, backlog e priorização usando o MCP do ClickUp. Use quando o usuário pedir “status do Nexus”, “o que mudou”, “o que está em progresso”, “blockers/risco”, “próximos itens”, “planejar feature”, “criar/update tarefas” ou “sincronizar contexto” com ClickUp — mesmo sem mencionar explicitamente “ClickUp”.
---

# ClickUp + Nexus: andamento e planejamento

## Objetivo

Usar o MCP do ClickUp para:

- **ver** o andamento do desenvolvimento do Nexus (o que está em progresso, bloqueios, próximos itens);
- **planejar** novas funcionalidades (épicos/features → tarefas/subtarefas, prioridades e critérios de aceite);
- **registrar** no ClickUp o contexto técnico do trabalho, sempre indicando **módulo/arquivo/função** em foco.

## Regras obrigatórias de reporte (sempre cumprir)

Antes de qualquer atualização no ClickUp, produzir um “cartão de contexto” e reutilizá-lo em descrições/comentários:

```markdown
### Contexto técnico (obrigatório)
- App: Nexus
- Módulo/arquivo: `<caminho/do/arquivo>`
- Função/classe: `<nome>`
- Escopo: `<1 frase>`
- Evidência: `<link/commit/PR> (se houver)`
```

Se o usuário não fornecer o módulo/função explicitamente:
- inferir a partir do diff/arquivos tocados na sessão; ou
- se ainda não for possível, registrar como:
  - **Módulo/arquivo**: `não identificado ainda`
  - **Função/classe**: `não identificado ainda`

Se a tarefa/épico-alvo no ClickUp não puder ser identificada com alta confiança (ex.: múltiplos matches sem contexto suficiente), não criar/atualizar/comentar no ClickUp: devolva a síntese para o usuário e solicite qual item deve ser atualizado.

## Feedback verbose ao usuário (obrigatório)

Sempre que a skill **criar/atualizar/comentar** no ClickUp (ou quando decidir **não** executar por falta de confiança), retornar uma confirmação explícita para o usuário, incluindo o que foi feito e o que não foi feito.

Formato obrigatório (ajuste os valores conforme o que o MCP retornar):

```markdown
### Confirmação de execução no ClickUp (verbose)
- App: Nexus
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

## Descoberta do “lugar do Nexus” no ClickUp

1. **Encontrar por busca global** (padrão):
   - Usar `clickup_search` com palavras-chave como: `nexus`, `Nexus`, `backend`, `frontend`, `infra`, `roadmap`, `bug`, `feature`.
   - Preferir filtrar `asset_types: ["task", "doc"]` quando o objetivo for status/backlog.

2. **Mapear a hierarquia** (somente se necessário):
   - Se a busca não esclarecer onde ficam as listas/pastas do Nexus, usar `clickup_get_workspace_hierarchy` com `max_depth: 2` e limitar por `space_ids` quando já conhecidos.

3. **Trabalhar com listas conscientemente**:
   - Para criar tarefas, **nunca adivinhar a lista**: obter o `list_id` via `clickup_get_list` (por `list_name` ou `list_id`) e registrar no texto qual lista foi usada.

## Fluxo: “Ver andamento do desenvolvimento”

Quando o usuário pedir status, usar este protocolo:

1. **Coletar itens recentes**:
   - `clickup_search` por `asset_types: ["task"]`, ordenando por `updated_at desc`.
   - Se o usuário citar responsáveis, usar `filters.assignees` (IDs) quando disponíveis; se precisar resolver nomes → usar `clickup_find_member_by_name` ou `clickup_resolve_assignees`.

2. **Gerar síntese objetiva** (para o usuário) e opcionalmente registrar no ClickUp:
   - **Em progresso**: top 5 tarefas mais recentemente atualizadas e com status ativo.
   - **Bloqueios/risco**: itens com dependências, falta de definição, ou divergências.
   - **Próximos**: 3 itens recomendados com justificativa curta.

3. **Registrar “status do dia” no ClickUp** (quando solicitado ou quando fizer sentido):
   - Preferir `clickup_create_task_comment` na tarefa/épico raiz do Nexus (ou na tarefa principal da iniciativa atual).
   - Se não for possível identificar essa tarefa-alvo com confiança, comentar na tarefa Nexus mais recentemente atualizada dentre os candidatos retornados pela `clickup_search`.
   - Se nenhum candidato for suficientemente adequado, não comentar no ClickUp e apenas devolver a síntese ao usuário.
   - O comentário deve começar com **Contexto técnico (obrigatório)** e terminar com:

```markdown
### Status
- Progresso: `<o que avançou>`
- Próximo passo: `<próxima ação>`
- Bloqueios: `<se houver>`
```

## Fluxo: “Planejar novas funcionalidades”

Quando o usuário pedir planejamento/roadmap:

1. **Normalizar a demanda**:
   - Transformar a solicitação em: objetivo, não-objetivos, requisitos funcionais, requisitos não-funcionais, riscos e critérios de aceite.

2. **Propor decomposição**:
   - Criar um épico/tarefa-mãe (feature) e subtarefas por componente (backend, frontend, banco, infra, testes).
   - Para cada subtarefa: objetivo, entregável, critérios de aceite, e “Contexto técnico (obrigatório)” (mesmo que inicial com `não identificado ainda`).

3. **Materializar no ClickUp**:
   - Criar/atualizar tarefas usando:
     - `clickup_create_task` (para novas tarefas) e
     - `clickup_update_task` (para ajustar descrição/prioridade/datas/status).
   - Para notas de refinamento, decisões e trade-offs, usar `clickup_create_task_comment`.

## Convenções de texto para tarefas do Nexus

### Nome de tarefa (padrão)

Usar prefixos consistentes:
- `FEAT - ...` para funcionalidade
- `FIX - ...` para correção
- `TECH - ...` para débito técnico/refactor
- `CHORE - ...` para infra/rotina

### Descrição (padrão mínimo)

```markdown
### Contexto técnico (obrigatório)
- App: Nexus
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

- `clickup_search`: busca global para localizar tarefas/docs e capturar “o que mudou”.
- `clickup_get_workspace_hierarchy`: entender Spaces/Folders/Lists quando a busca não for suficiente.
- `clickup_get_list`: resolver `list_id` por nome/ID antes de criar tarefas.
- `clickup_create_task` / `clickup_update_task`: criar/ajustar tarefas.
- `clickup_create_task_comment`: registrar status, decisões, evidências, e sempre o **módulo/função**.
- (Opcional) `clickup_start_time_tracking` / `clickup_stop_time_tracking`: iniciar/parar apontamento quando o usuário pedir.

## Exemplos de uso (gatilhos)

- “Mostra o andamento do Nexus no ClickUp” → usar fluxo de andamento + síntese.
- “Planeja a feature X” → decompor e criar tarefas/subtarefas + critérios de aceite.
- “Atualiza a tarefa Y com o que foi feito hoje” → comentar na tarefa com o template e **módulo/função**.
- “Atualiza a tarefa Y com o que foi feito hoje” → comentar na tarefa com o template e **módulo/função**.
