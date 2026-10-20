---
name: project-tracking-patterns
description: Regras de atualização de progresso durante workflows. Atualização de PROJECT-PROGRESS.md, histórico, e Flyee sincronizado.
---

# Project Tracking Patterns

> **Single Source of Truth** para rastrear progresso durante workflows longos.

---

## 🎯 PROPÓSITO

Garantir que durante execução de workflows:
1. **Arquivo de progresso** seja atualizado a cada fase
2. **Histórico** seja registrado a cada ação
3. **Flyee** seja sincronizado após cada task
4. **Tasks individuais** sejam listadas e rastreadas

---

## 🔴 REGRAS OBRIGATÓRIAS

> [!CAUTION]
> **TODAS as regras abaixo são BLOQUEANTES.**
> O workflow NÃO pode prosseguir sem cumpri-las.

### 1. Atualização Após Cada Fase

**Quando:** Ao completar qualquer fase de um workflow

**Onde:** Arquivo de progresso (`PROJECT-PROGRESS.md`, `LEGACY-PROGRESS.md`, etc.)

**O que atualizar:**
- [ ] `Fase Atual` → Próxima fase
- [ ] Status da fase concluída → `✅ Concluído`
- [ ] Artefato gerado (se houver)
- [ ] `Última atualização` → Data/hora atual

```markdown
## Exemplo de atualização:

| Fase | Status | Artefato |
|------|--------|----------|
| 2. TDD Técnico | ✅ Aprovado | `docs/design/TDD-{nome}.md` |  ← ATUALIZADO
| 3. Breakdown | 🟡 Em Progresso | - |  ← NOVA FASE ATUAL
```

---

### 2. Registro no Histórico

**Quando:** Após QUALQUER ação significativa

**Formato:**
```markdown
| Data | Fase | Ação |
|------|------|------|
| 2026-02-02 12:30 | 3 | Breakdown iniciado |
| 2026-02-02 12:35 | 3 | 10 tasks criadas no Flyee |
| 2026-02-02 12:40 | 3 | Breakdown concluído |
```

**Ações que DEVEM ser registradas:**
- Início de fase
- Conclusão de fase
- Criação de artefatos
- Criação de tasks no Flyee
- Aprovações humanas
- Erros ou bloqueios

---

### 3. Atualização de Tasks Após Cada Item

**Quando:** Ao trabalhar em Phase 4 (Testes) ou Phase 5 (Implementação)

**Onde:** Seção `📝 Tasks` no arquivo de progresso

**Template:**
```markdown
## 📝 Tasks (Phase 4-5)

| # | Task | Teste | Código | Status |
|---|------|-------|--------|--------|
| 1 | Setup inicial | ✅ | ✅ | ✅ Completo |
| 2 | Auth básica | ✅ | 🟡 | 🟡 Em Progresso |  ← ATUALIZAR AQUI
| 3 | CRUD usuários | ⏳ | ⏳ | ⏳ Pendente |
```

---

### 4. Sincronização de Tarefas (OBRIGATÓRIO) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** As tarefas (Flyee ou Local) DEVEM ser atualizadas após cada épico/fase conforme a configuração de `Tracker de Tasks`.
> NÃO prosseguir para próximo épico sem sincronizar o respectivo tracker.

**Quando sincronizar:**
| Momento | Ação |
|---------|------|
| 🔴 **ANTES de escrever código** | **CRIAR TASK no Flyee (`bridge.py --create-task`)** |
| Ao iniciar implementação | Atualizar status → "Em Progresso" (`bridge.py --update-task`) |
| Ao finalizar a implentação | Excutar workflow genérico `/task-complete` |

> [!CAUTION]
> É estritamente proibido iniciar a codificação (Phase 5 do `/new-project` ou Phase 3 do `/new-task`) sem antes gerar um Task ID no Tracker. 

**Como sincronizar (Único caminho autorizado):**

**1. Via Bridge CLI (Criação e Atualização):**
```bash
# 1. CRIAR TASK (Obrigatório antes de codar)
python3 .agent/flyee-bridge/bridge.py --create-task \
  --name "Título descritivo" \
  --type implement_feature \
  --description "Breve descrição" \
  --priority normal

# 2. STATUS EM PROGRESSO
python3 .agent/flyee-bridge/bridge.py --update-task <task_id> --status running
```

> [!TIP]
> Bridge CLI auto-detects if `flyee.json` exists. If project is not connected to Flyee, it skips silently.

**2. Via Workflow (Conclusão - OBRIGATÓRIO):**
```markdown
# 3. FECHAMENTO DE TASK
Para concluir uma tarefa, invoque obrigatoriamente o workflow genérico:
`/task-complete`
(Ele cuidará do logging de execução, cobertura e fechamento no Flyee)
```

---

### 5. Gate de Sincronização por Épico 🔴

> [!CAUTION]
> **BLOQUEADOR:** Antes de iniciar próximo épico, verificar o **Modo de Tracking** do projeto:

#### Se Tracker = Flyee:
```markdown
## Checklist de Sincronização - Épico {N}

- [ ] Todas as tasks do épico atualizadas no Flyee
- [ ] Status correto (Concluído/Em Progresso)
- [ ] % Progresso atualizado
- [ ] Comentário de conclusão adicionado

> **SE NÃO SINCRONIZADO:** PARAR e sincronizar antes de prosseguir.
```

#### Se Tracker = Local (`docs/TASKS.md`):
```markdown
## Checklist de Sincronização - Épico {N}

- [ ] Todas as tasks do épico marcadas com `[x]` no arquivo `docs/TASKS.md`

> **SE NÃO SINCRONIZADO:** PARAR e atualizar arquivo antes de prosseguir.
```

**Mensagem obrigatória ao completar épico:**
```markdown
📊 **Épico {N} Concluído - Tracker Sync**

| Task ID | Status | % |
|---------|--------|---|
| {id} | ✅ | 100% |
| {id} | ✅ | 100% |

✅ Flyee sincronizado. Prosseguindo para Épico {N+1}.
```

---

### 6. Logging de Execução por Task 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** Ao completar verificação/execução de CADA task individual,
> você DEVE exibir o log de execução ANTES de prosseguir para a próxima task.

**Quando:** Após completar verificação ou execução de qualquer task

**Template OBRIGATÓRIO:**
```markdown
### ✅ Task {ID}: {Nome}

**Verificação:**
- ✅ {arquivo/componente verificado}
- ✅ {critério de aceitação atendido}
- ✅ {teste passando, se aplicável}

**Arquivos Relevantes:**
- `{caminho/arquivo1.ts}`
- `{caminho/arquivo2.tsx}`

**Ação Flyee:**
- Status: Não iniciado → Concluído
- Última edição: {timestamp automático}

**Tempo aproximado:** {X}min
```

**Exemplo Preenchido:**
```markdown
### ✅ Task 1.1: Setup Next.js 15 + App Router

**Verificação:**
- ✅ `package.json` contém `next@15.1.7`
- ✅ `src/app/layout.tsx` existe com App Router
- ✅ `npm run build` passa sem erros

**Arquivos Relevantes:**
- `package.json`
- `src/app/layout.tsx`
- `next.config.ts`

**Ação Flyee:**
- Status: Não iniciado → Concluído
- Última edição: 2026-02-03T14:15:00

**Tempo aproximado:** 2min
```

**Regras:**
1. **NUNCA** pular este log - mesmo para tasks simples
2. **SEMPRE** listar arquivos verificados/criados
3. **SEMPRE** incluir critérios de aceitação verificados
4. **ATUALIZAR** Flyee ANTES de prosseguir para próxima task

---

### 7. TASK SYNC — Template de Conclusão (Flyee) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** O ÚNICO caminho autorizado para concluir uma task no Flyee é
> o workflow `/task-complete`. Chamadas avulsas a `API-patch-page` SEM as etapas
> completas são **PROIBIDAS** — são a causa raiz das falhas v1-v4.

**Template canônico de nota de conclusão (Flyee API — `API-patch-block-children`):**

```json
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    {
      "type": "callout",
      "callout": {
        "icon": { "type": "emoji", "emoji": "✅" },
        "rich_text": [
          { "type": "text", "text": { "content": "Concluído em {data}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          { "type": "text", "text": { "content": "📋 {resumo da implementação}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          { "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          { "type": "text", "text": { "content": "📁 Arquivos: {lista de arquivos modificados}" } }
        ]
      }
    }
  ]
}
```

**Etapas obrigatórias do `/task-complete` (em ordem):**

1. Log de Execução exibido
2. Resumo de Execução (O que foi feito, Arquivos, Verificação, Decisões)
3. `API-patch-page` — Status → Concluído + % Progresso → 100 + Tempo Gasto
4. `API-patch-block-children` — Nota inline ✅ (template acima)
5. `API-create-a-comment` — Comentário rico de conclusão
6. Arquivo de progresso atualizado (LEGACY-PROGRESS.md / PROJECT-PROGRESS.md)
7. Histórico de ações atualizado
8. Mensagem de confirmação exibida

> [!CAUTION]
> 🚫 **ANTI-PATTERN (PROIBIDO):**
> ```
> API-patch-page isoladamente ← CAUSA RAIZ das falhas v1-v4
> ```
> ✅ **PADRÃO CORRETO:** Ler `.agent/workflows/task-complete.md` e executar TODAS as 8 etapas.

#### 🧠 Self-Check Anti-Bypass (OBRIGATÓRIO)

Antes de iniciar o próximo item (fluxo, task, fase), o agente DEVE responder:

```
❓ SELF-CHECK — Item anterior ({nome})

1. Executei `/task-complete` para a Task #{id}? → SIM/NÃO
2. Comentário de conclusão no Flyee? → SIM/NÃO
3. Arquivo de progresso atualizado? → SIM/NÃO

→ Se QUALQUER = NÃO → PARAR e completar ANTES de prosseguir
→ Se TODAS = SIM → Prosseguir
```

#### Historical Lessons — TASK SYNC

> 🔴 **FALHA v1 (api/):** 6 tasks (#27-#32) marcadas Concluído sem comentário, sem Tempo Gasto,
> sem nota de conclusão. O gate não estava listado na sequência de ações.

> 🔴 **FALHA v2 (subscriptions/):** 3 tasks (#1-#3) marcadas Concluído via `API-patch-page`
> (Status + % Progresso), mas SEM: comentário, Tempo Gasto, nota inline, nem update de progresso.
> **Causa raiz:** o gate era o último passo numa lista e o agente o pulou.

> 🔴 **FALHA v3 (subscriptions/ --resume):** Session seguinte NÃO executou `/task-complete`
> para tasks já concluídas. Fez apenas `API-patch-page` (Status + %) sem comentário, nota inline,
> nem update de progresso. **Causa raiz:** instrução era textual, agente não leu `task-complete.md`.

> 🔴 **FALHA v4 (admin/ --resume):** Mesmo com regra v3 escrita, agente fez chamadas diretas
> a `API-patch-page` por task, sem as 8 etapas completas. **Causa raiz:** `API-patch-page` não
> constava como gatilho no Task Completion Gate do GEMINI.md.

---

## 📋 CHECKLIST DE COMPLIANCE

Antes de prosseguir para próxima fase:

- [ ] Arquivo de progresso atualizado
- [ ] Histórico registrado
- [ ] Tasks individuais atualizadas (se aplicável)
- [ ] **🔴 Log de execução exibido para cada task**
- [ ] **🔴 Flyee sincronizado via `/task-complete` (OBRIGATÓRIO — ver seção 7)**

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Arquivo de Progresso |
|----------|---------------------|
| `/new-project` | `docs/PROJECT-PROGRESS.md` |
| `/legacy-project` | `docs/LEGACY-PROGRESS.md` |
| `/new-task` | `docs/NEW-TASK-PROGRESS.md` |
| `/discovery` | Tasks direto no Flyee |
| `/execute` | Task específica no Flyee |
