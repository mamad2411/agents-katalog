---
name: notion-task-patterns
description: "⚠️ DEPRECATED — Use Flyee API (bridge.py) para task management. Este skill é mantido apenas como referência histórica."
---

# ⚠️ DEPRECATED — Notion Task Patterns

> [!CAUTION]
> **Este skill foi DEPRECADO em 2026-03-14.**
>
> **Motivo:** Todos os workflows foram migrados para usar a Flyee API via `bridge.py`
> em vez de Notion MCP tools.
>
> **Substituto:** `.agent/flyee-bridge/bridge.py` — funções `create_task()`, `update_task()`,
> `list_tasks()`, `get_task()`.
>
> **Se você chegou aqui via referência em workflow:** A referência deveria ter sido
> atualizada para "Flyee API". Verifique o workflow de origem.

---

## Referência Rápida — Flyee API (Substituto)

```python
from bridge import create_task, update_task, list_tasks, get_task, load_config

config = load_config()

# Criar task
create_task(api_url=config["api_url"], api_key=config["api_key"],
            project_id=config["project_id"], task_type="implement_feature",
            name="Nome da Task", description="Descrição")

# Atualizar task
update_task(api_url=config["api_url"], api_key=config["api_key"],
            task_id="<id>", status="completed", result_status="success",
            output={"summary": "..."}, metrics={"time_spent": "2h"})

# Listar tasks
tasks = list_tasks(api_url=config["api_url"], api_key=config["api_key"],
                   project_id=config["project_id"])

# Buscar task
task = get_task(api_url=config["api_url"], api_key=config["api_key"],
                task_id="<id>")
```

---

> **CONTEÚDO ABAIXO MANTIDO COMO REFERÊNCIA HISTÓRICA.**
> Os templates de corpo por categoria (Feature, Bug, Melhoria, etc.) podem ser
> úteis como referência de formato, mas os API calls devem usar Flyee API.

---

# (HISTÓRICO) Notion Task Patterns

> ~~**Single Source of Truth** para todos os workflows que manipulam tasks no Notion.~~

---

## 🎯 PROPÓSITO

Garantir consistência em:

1. **Database Padrão** - Sempre usar "Tarefas"
2. **Validação de Schema** - Propriedades obrigatórias
3. **Formato de Corpo** - Template por categoria
4. **API Calls** - Exemplos padronizados
5. **Idioma** - Templates localizados para transparência com cliente

---

## 🌐 IDIOMA DAS TASKS (GATE PRÉ-CRIAÇÃO)

> [!IMPORTANT]
> **REGRA:** Antes de criar tasks, perguntar ao usuário o idioma preferido.
> O objetivo é **transparência com o cliente** - tasks devem ser compreensíveis.

### Pergunta Obrigatória (1x por Projeto)

```markdown
🌐 **Idioma das Tasks no Notion**

Para garantir transparência com o cliente, em qual idioma você prefere que as tasks sejam escritas?

- [ ] 🇧🇷 **Português** (recomendado para clientes brasileiros)
- [ ] 🇺🇸 **English** (recommended for international teams)

Essa escolha afeta:

- Títulos das seções (User Story, Acceptance Criteria, etc.)
- Descrições e critérios de aceite
- Comentários de progresso e conclusão
```

### Quando Perguntar

| Situação                                       | Ação                                         |
| ---------------------------------------------- | -------------------------------------------- |
| Novo projeto (`/new-project`, `/discovery`)    | ⭐ Perguntar na Phase 3 (antes do Breakdown) |
| Projeto existente sem preferência salva        | ⭐ Perguntar antes de criar primeira task    |
| Preferência já definida em PROJECT-PROGRESS.md | ✅ Usar idioma salvo                         |

### Salvar Preferência

Adicionar em `docs/PROJECT-PROGRESS.md`:

```markdown
## Configurações

| Configuração | Valor        |
| ------------ | ------------ |
| Idioma Tasks | 🇧🇷 Português |
```

---

## 🔴 DATABASE PADRÃO (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** TODOS os workflows DEVEM buscar o database com nome exato **"Tarefas"**.
> NÃO usar outros databases como "Daily", "Sprint", etc.

### Busca Obrigatória

```
Use: mcp_notion-mcp-server_API-post-search
query: "Tarefas"
filter: { "property": "object", "value": "data_source" }
```

### Validação do Nome

| Resultado da Busca   | Ação                            |
| -------------------- | ------------------------------- |
| Encontrou "Tarefas"  | ✅ Usar este database           |
| Encontrou outro nome | ❌ PARAR e perguntar ao usuário |
| Não encontrou nada   | ❌ PARAR e notificar usuário    |

### Mensagem se Database Incorreto

```markdown
⚠️ **DATABASE INCORRETO**

Esperado: "Tarefas"
Encontrado: "{nome_encontrado}"

O padrão do projeto exige que tasks sejam criadas no database "Tarefas".

**Opções:**

1. Criar database "Tarefas" no Notion
2. Confirmar que deseja usar "{nome_encontrado}" (não recomendado)
```

---

## 📋 PROPRIEDADES OBRIGATÓRIAS

> [!IMPORTANT]
> Antes de criar qualquer task, valide se o database possui estas propriedades.
> Se QUALQUER propriedade obrigatória estiver ausente, **PARE e notifique o usuário**.

### Na Criação da Task

| Propriedade      | Tipo         | Obrigatório   | Notas                                                |
| ---------------- | ------------ | ------------- | ---------------------------------------------------- |
| `Nome da tarefa` | title        | ✅ Sim        | Título da task — **SEM PREFIXOS** (ver regra abaixo) |
| `Status`         | status       | ✅ Sim        | Options: Não iniciado, Em andamento, Concluído       |
| `ID`             | unique_id    | ✅ Automático | Autoincremento do Notion (NÃO preencher na criação)  |
| `Categoria`      | multi_select | ✅ Sim        | Feature, Bug, Melhoria, Refatoração, Log             |
| `Prioridade`     | select       | ✅ Sim        | Alta, Média, Baixa                                   |
| `Épico`          | select       | ✅ Sim        | Módulo/Feature principal (1. Setup, 2. Auth, etc.)   |
| `Estimativa`     | number       | ✅ Sim        | **Horas estimadas** (obrigatório na criação)         |
| `% Progresso`    | number       | ✅ Sim        | Percentual de conclusão (0-100)                      |

### 🚫 REGRA DE NOMENCLATURA: SEM PREFIXOS (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Títulos de tasks NÃO devem conter prefixos como `[DOC]`, `[TDD]`,
> `[TEST]`, `[BUG]`, `[FEAT]`, `F1 —`, `F2 —` ou qualquer tag/numeração inventada.
> A **Categoria** (multi_select) já cumpre essa função. Duplicar no título é redundante.

| ❌ ERRADO                           | ✅ CORRETO                                     |
| ----------------------------------- | ---------------------------------------------- |
| `[DOC] F1 — Checkout e Onboarding`  | `Checkout e Onboarding`                        |
| `[TDD] Subscriptions — TDD Reverso` | `Subscriptions — TDD Reverso`                  |
| `[TEST] Testes Unitários`           | `Testes Unitários e Integração`                |
| `[BUG] Fix login timeout`           | `Fix login timeout`                            |
| `P0 Fix — PlanController auth`      | `PlanController sem JwtAuthGuard`              |
| `Bug Fix — modulesValue billing`    | `modulesValue=0 hardcoded (billing incorreta)` |

> [!WARNING]
> **📜 HISTÓRICO DE FALHAS:**
>
> - **(2026-02-18 v1):** 10 tasks criadas com prefixos `[DOC]`/`[TDD]`/`[TEST]` no título.
>   Causa: agente inventou prefixos para organizar, duplicando a Categoria.
> - **(2026-02-18 v2):** Tasks #11 e #12 criadas com prefixo `P0 Fix —` no título.
>   Causa: agente usou prioridade como prefixo. Info de prioridade pertence à propriedade
>   `Prioridade` (select), NÃO ao título. Inclui: `P0`, `P1`, `Bug Fix`, `Security Fix`, etc.

### Na Conclusão da Task

| Propriedade   | Tipo      | Obrigatório | Notas                                                        |
| ------------- | --------- | ----------- | ------------------------------------------------------------ |
| `Tempo Gasto` | rich_text | ✅ Sim      | **Tempo real gasto** (ex: "2h30m") - obrigatório ao concluir |

> [!CAUTION]
> **REGRA:** Ao marcar task como "Concluído", **DEVE** preencher `Tempo Gasto`.

### Propriedades Opcionais

| Propriedade        | Tipo   | Notas                                         |
| ------------------ | ------ | --------------------------------------------- |
| `Nível de esforço` | select | XS, S, M, L, XL                               |
| `Agente`           | select | backend-specialist, frontend-specialist, etc. |
| `Projeto`          | select | Nome do projeto                               |
| `Prazo`            | date   | Data limite                                   |
| `Responsável`      | people | Quem é responsável                            |

### Propriedades Automáticas (Read-Only)

> [!NOTE]
> Estas propriedades são **gerenciadas automaticamente** pelo Notion.
> **NÃO** inclua em chamadas de API - elas são read-only.

| Propriedade     | Tipo             | Comportamento                 |
| --------------- | ---------------- | ----------------------------- |
| `Criado em`     | created_time     | Preenchido ao criar página    |
| `Última edição` | last_edited_time | Atualizado a cada modificação |

---

## 🔄 CICLO DE VIDA DA TASK

### Fases e Propriedades Obrigatórias

| Fase          | Trigger                                                     | Propriedades Obrigatórias                |
| ------------- | ----------------------------------------------------------- | ---------------------------------------- |
| **Criação**   | `/discovery`, `/new-project`, `/new-task`, `/legacy-project` | `Estimativa` ✅                          |
| **Início**    | `/execute`, `/task-update start`                            | `Status` → "Em andamento"                |
| **Progresso** | `/task-update progress`                                     | Comentário de progresso                  |
| **Conclusão** | `/execute`, `/task-update done`                             | `Status` → "Concluído", `Tempo Gasto` ✅ |

### 🚨 GATE DE SYNC NOTION (OBRIGATÓRIO) ⭐

> [!CAUTION]
> **REGRA BLOQUEANTE:** Quando uma task ou épico é concluído localmente (testes passando, código funcionando),
> o agente **DEVE** atualizar o Notion **ANTES** de prosseguir para próxima task/épico.
> **NUNCA** deixar sync para depois - isso causa inconsistência e falta de transparência.

> [!WARNING]
> **📜 HISTÓRICO DE FALHAS (2026-02-06):**
>
> - **Gap detectado:** Agente ignorou sync após concluir tasks #11-#17
> - **Causa raiz:** Workflow referenciava skill mas não tinha chamadas MCP inline
> - **Correção aplicada:** Workflow `new-project.md` agora inclui PASSOS 1-4 com chamadas MCP explícitas
> - **Lição:** NUNCA apenas referenciar outra skill para ações críticas - incluir comandos inline

**Trigger:**

- Testes passando para uma task
- Épico completo (todas tasks do épico concluídas)
- Trabalho manual executado (refatoração, fix, etc.)

**Ação Obrigatória (sequencial):**

1. **Atualizar Status** → "Concluído"
2. **Preencher Tempo Gasto** → Ex: "2h30m"
3. **Adicionar % Progresso** → 100
4. **Adicionar Nota de Conclusão no Corpo** → Append block com resumo

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Concluído" } },
    "Tempo Gasto": { "rich_text": [{ "text": { "content": "{tempo}" } }] },
    "% Progresso": { "number": 100 }
  }
}
```

**Nota de Conclusão (append ao corpo da task):**

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    {
      "type": "divider",
      "divider": {}
    },
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
          {
            "type": "text",
            "text": { "content": "📋 {resumo da implementação}" }
          }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": { "content": "🧪 Testes: {X} novos ({arquivo}.test.tsx)" }
          }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "📁 Arquivos: {lista de arquivos modificados}"
            }
          }
        ]
      }
    }
  ]
}
```

**Mensagem Obrigatória ao Concluir Épico:**

```markdown
✅ **Épico X Completo**

📋 **Tasks concluídas:**
| ID | Task | Tempo |
|----|------|-------|
| #1 | {nome} | {tempo} |
| #2 | {nome} | {tempo} |

🔄 **Synced com Notion:** ✅
📍 **Próximo:** Épico Y - {nome}
```

> [!WARNING]
> **FALHA DETECTADA:** Épicos sendo marcados como "completos" sem atualizar Notion.
> Esta regra existe para EVITAR essa inconsistência.

### 🚨 GATE DE FINALIZAÇÃO (Pre-Start Check)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de iniciar qualquer nova task, o agente DEVE verificar
> se há tasks com Status="Em andamento". Se houver, PERGUNTAR ao usuário.

**Verificação obrigatória:**

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DATABASE_ID}",
  "filter": {
    "property": "Status",
    "status": { "equals": "Em andamento" }
  }
}
```

**Se encontrar tasks abertas:**

```
⚠️ TASK EM ANDAMENTO DETECTADA

📋 {nome da task}
📊 Status: Em andamento
⏱️ Tempo Gasto: (não preenchido)

Deseja:
1. Finalizar esta task primeiro (preencher Tempo Gasto)
2. Iniciar nova task mesmo assim
```

### Regras do Ciclo

1. **CRIAÇÃO:** `Estimativa` é **OBRIGATÓRIO** - não criar task sem este campo
2. **CONCLUSÃO:** `Tempo Gasto` é **OBRIGATÓRIO** - não marcar "Concluído" sem preencher
3. **GATE:** Verificar tasks abertas antes de iniciar nova

---

## 🛑 VALIDAÇÃO DE SCHEMA (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Este processo DEVE ser executado ANTES de criar qualquer task.
> NÃO pule esta validação em nenhuma circunstância.

### Processo de Validação (3 Passos)

**Passo 1 - Buscar Database:**

```
Use: mcp_notion-mcp-server_API-post-search
query: "Tarefas"
filter: { "property": "object", "value": "data_source" }
```

**Passo 2 - Recuperar Schema:**

```
Use: mcp_notion-mcp-server_API-retrieve-a-database
database_id: {DATABASE_ID}
```

**Passo 3 - Validar Propriedades:**

- Verificar se TODAS as propriedades obrigatórias existem
- Se QUALQUER uma estiver ausente → **PARAR**

### Mensagem de Erro OBRIGATÓRIA

Se propriedades estiverem ausentes, exibir:

```markdown
⚠️ **PROPRIEDADES AUSENTES** no database 'Tarefas':

| Propriedade | Tipo Esperado |
| ----------- | ------------- |
| {nome}      | {tipo}        |
| {nome}      | {tipo}        |

**Por favor, crie estas propriedades no Notion antes de continuar.**

🔗 [Abrir database no Notion]({notion_url})

---

**Instruções para criar propriedades:**

1. Abra o database "Tarefas" no Notion
2. Clique em "+" ao lado do último cabeçalho de coluna
3. Adicione cada propriedade com o tipo correto

**AGUARDANDO** confirmação após criar as propriedades...
```

> [!CAUTION]
> **NÃO prossiga** com criação de tasks até que TODAS as propriedades obrigatórias existam.
> O usuário DEVE confirmar que criou as propriedades antes de continuar.

---

## 📝 FORMATO DO CORPO POR CATEGORIA

### Detectar Categoria

| Categoria      | Trigger Keywords                                           | Formato               |
| -------------- | ---------------------------------------------------------- | --------------------- |
| `Feature`      | "nova", "criar", "implementar", "adicionar"                | User Story            |
| `Bug`          | "fix", "corrigir", "erro", "bug", "problema"               | Bug Report            |
| `Melhoria`     | "refactor", "melhorar", "otimizar", "limpar"               | Plano Técnico         |
| `Refatoração`  | "débito", "legacy", "modernizar"                           | Plano Técnico         |
| `Documentação` | "documentar", "TDD", "design system", "fluxo", "análise"   | Template Documentação |
| `Prototipação` | "protótipo", "stitch", "mockup", "wireframe", "UI", "tela" | Template Prototipação |
| `Log`          | trabalho retroativo                                        | Resumo Técnico        |

---

### 🎯 Template: FEATURE (User Story)

> **Usar o idioma definido pelo usuário em PROJECT-PROGRESS.md**

#### 🇧🇷 Português (PT-BR)

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "📖 História do Usuário" } }]
      }
    },
    {
      "paragraph": {
        "rich_text": [
          {
            "text": {
              "content": "Como **{persona}**, eu quero **{ação}**, para que **{benefício}**."
            }
          }
        ]
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "✅ Critérios de Aceite" } }]
      }
    },
    {
      "to_do": {
        "rich_text": [
          {
            "text": {
              "content": "Dado {contexto}, Quando {ação}, Então {resultado}"
            }
          }
        ],
        "checked": false
      }
    },
    {
      "to_do": {
        "rich_text": [
          {
            "text": {
              "content": "Dado {contexto}, Quando {ação}, Então {resultado}"
            }
          }
        ],
        "checked": false
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "⚠️ Casos Especiais" } }]
      }
    },
    {
      "bulleted_list_item": {
        "rich_text": [{ "text": { "content": "{caso especial 1}" } }]
      }
    },
    {
      "bulleted_list_item": {
        "rich_text": [{ "text": { "content": "{caso especial 2}" } }]
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "🔗 Referências" } }]
      }
    },
    {
      "paragraph": {
        "rich_text": [{ "text": { "content": "PRD: {link}\nTDD: {link}" } }]
      }
    }
  ]
}
```

#### 🇺🇸 English (EN)

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    {
      "heading_2": { "rich_text": [{ "text": { "content": "📖 User Story" } }] }
    },
    {
      "paragraph": {
        "rich_text": [
          {
            "text": {
              "content": "As a **{persona}**, I want to **{action}**, so that **{benefit}**."
            }
          }
        ]
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "✅ Acceptance Criteria" } }]
      }
    },
    {
      "to_do": {
        "rich_text": [
          {
            "text": {
              "content": "Given {context}, When {action}, Then {outcome}"
            }
          }
        ],
        "checked": false
      }
    },
    {
      "to_do": {
        "rich_text": [
          {
            "text": {
              "content": "Given {context}, When {action}, Then {outcome}"
            }
          }
        ],
        "checked": false
      }
    },

    {
      "heading_2": { "rich_text": [{ "text": { "content": "⚠️ Edge Cases" } }] }
    },
    {
      "bulleted_list_item": {
        "rich_text": [{ "text": { "content": "{edge case 1}" } }]
      }
    },
    {
      "bulleted_list_item": {
        "rich_text": [{ "text": { "content": "{edge case 2}" } }]
      }
    },

    {
      "heading_2": { "rich_text": [{ "text": { "content": "🔗 References" } }] }
    },
    {
      "paragraph": {
        "rich_text": [{ "text": { "content": "PRD: {link}\nTDD: {link}" } }]
      }
    }
  ]
}
```

---

### 🐛 Template: BUG

```
Use: mcp_notion-mcp-server_API-patch-block-children
block_id: {page_id}
children: [
  { "heading_2": { "rich_text": [{ "text": { "content": "🐛 Problema" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{descrição do bug}" } }] } },

  { "heading_2": { "rich_text": [{ "text": { "content": "📋 Passos para Reproduzir" } }] } },
  { "numbered_list_item": { "rich_text": [{ "text": { "content": "{passo 1}" } }] } },
  { "numbered_list_item": { "rich_text": [{ "text": { "content": "{passo 2}" } }] } },

  { "heading_2": { "rich_text": [{ "text": { "content": "✅ Critérios de Resolução" } }] } },
  { "to_do": { "rich_text": [{ "text": { "content": "{critério 1}" } }], "checked": false } },
  { "to_do": { "rich_text": [{ "text": { "content": "{critério 2}" } }], "checked": false } },

  { "heading_2": { "rich_text": [{ "text": { "content": "🔗 References" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "Related: #{task_id}" } }] } }
]
```

---

### 🔧 Template: MELHORIA / REFATORAÇÃO

```
Use: mcp_notion-mcp-server_API-patch-block-children
block_id: {page_id}
children: [
  { "heading_2": { "rich_text": [{ "text": { "content": "📋 Plano Técnico" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{descrição técnica}" } }] } },

  { "heading_2": { "rich_text": [{ "text": { "content": "✅ Checklist" } }] } },
  { "to_do": { "rich_text": [{ "text": { "content": "{item 1}" } }], "checked": false } },
  { "to_do": { "rich_text": [{ "text": { "content": "{item 2}" } }], "checked": false } },

  { "heading_2": { "rich_text": [{ "text": { "content": "📁 Arquivos Afetados" } }] } },
  { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{arquivo 1}" } }] } },
  { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{arquivo 2}" } }] } }
]
```

---

### 📝 Template: LOG (Retroativo)

```
Use: mcp_notion-mcp-server_API-patch-block-children
block_id: {page_id}
children: [
  { "heading_2": { "rich_text": [{ "text": { "content": "📋 Resumo" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{descrição do trabalho realizado}" } }] } },

  { "heading_2": { "rich_text": [{ "text": { "content": "📁 Arquivos Alterados" } }] } },
  { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{arquivo 1}" } }] } }
]
```

---

### 📄 Template: DOCUMENTAÇÃO (Análise/TDD/Design System/Testes)

> [!IMPORTANT]
> **Uso:** Para tasks de fases estruturadas (documentação de fluxos, TDD reverso, Design System, escrita de testes).
> Estas tasks garantem **transparência com o cliente** sobre trabalho de engenharia.

#### 🇧🇷 Português (PT-BR)

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    {
      "heading_2": { "rich_text": [{ "text": { "content": "📋 Objetivo" } }] }
    },
    {
      "paragraph": {
        "rich_text": [
          {
            "text": {
              "content": "{o que será documentado/criado e por que é necessário}"
            }
          }
        ]
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "✅ Critérios de Aceite" } }]
      }
    },
    {
      "to_do": {
        "rich_text": [
          {
            "text": {
              "content": "{critério 1 - ex: Fluxo X documentado com entrada, saída e dependências}"
            }
          }
        ],
        "checked": false
      }
    },
    {
      "to_do": {
        "rich_text": [
          {
            "text": {
              "content": "{critério 2 - ex: TDD validado com >= 75% completo}"
            }
          }
        ],
        "checked": false
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "📁 Artefatos Esperados" } }]
      }
    },
    {
      "bulleted_list_item": {
        "rich_text": [
          {
            "text": {
              "content": "{arquivo de saída - ex: docs/flows/auth/login.md}"
            }
          }
        ]
      }
    },
    {
      "bulleted_list_item": {
        "rich_text": [
          {
            "text": {
              "content": "{arquivo de saída - ex: docs/design/TDD-projeto-auth.md}"
            }
          }
        ]
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "🔗 Referências" } }]
      }
    },
    {
      "paragraph": {
        "rich_text": [
          {
            "text": {
              "content": "Módulo: {path}\nAnálise: docs/CODEBASE-{projeto}.md"
            }
          }
        ]
      }
    }
  ]
}
```

#### 🇺🇸 English (EN)

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    {
      "heading_2": { "rich_text": [{ "text": { "content": "📋 Objective" } }] }
    },
    {
      "paragraph": {
        "rich_text": [
          {
            "text": {
              "content": "{what will be documented/created and why it is necessary}"
            }
          }
        ]
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "✅ Acceptance Criteria" } }]
      }
    },
    {
      "to_do": {
        "rich_text": [
          {
            "text": {
              "content": "{criterion 1 - e.g.: Flow X documented with inputs, outputs and dependencies}"
            }
          }
        ],
        "checked": false
      }
    },
    {
      "to_do": {
        "rich_text": [
          {
            "text": {
              "content": "{criterion 2 - e.g.: TDD validated with >= 75% complete}"
            }
          }
        ],
        "checked": false
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "📁 Expected Artifacts" } }]
      }
    },
    {
      "bulleted_list_item": {
        "rich_text": [
          {
            "text": {
              "content": "{output file - e.g.: docs/flows/auth/login.md}"
            }
          }
        ]
      }
    },
    {
      "bulleted_list_item": {
        "rich_text": [
          {
            "text": {
              "content": "{output file - e.g.: docs/design/TDD-project-auth.md}"
            }
          }
        ]
      }
    },

    {
      "heading_2": { "rich_text": [{ "text": { "content": "🔗 References" } }] }
    },
    {
      "paragraph": {
        "rich_text": [
          {
            "text": {
              "content": "Module: {path}\nAnalysis: docs/CODEBASE-{project}.md"
            }
          }
        ]
      }
    }
  ]
}
```

---

### 🎨 Template: PROTOTIPAÇÃO (Stitch/Mockup)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Prototipação SEMPRE usa **1 TASK POR TELA**.
> NÃO criar uma única task para múltiplas telas.
> Cada tela = 1 task individual = 1 validação do cliente.

**Fluxo de Status:**

```
Não iniciado → Em andamento → Aguardando Aprovação → Concluído
                                    ↑
                            GATE DO CLIENTE
```

**Template do Corpo:**

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    {
      "heading_2": { "rich_text": [{ "text": { "content": "🎨 Protótipo" } }] }
    },
    {
      "paragraph": {
        "rich_text": [
          {
            "text": {
              "content": "Tela: {nome da tela}\nDispositivo: {Desktop/Mobile/Tablet}"
            }
          }
        ]
      }
    },

    { "heading_2": { "rich_text": [{ "text": { "content": "📸 Preview" } }] } },
    { "image": { "external": { "url": "{screenshot_url_do_stitch}" } } },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "✅ Critérios de Validação" } }]
      }
    },
    {
      "to_do": {
        "rich_text": [
          { "text": { "content": "Layout conforme Design System (MASTER.md)" } }
        ],
        "checked": false
      }
    },
    {
      "to_do": {
        "rich_text": [
          { "text": { "content": "Copy/textos conforme Content Strategy" } }
        ],
        "checked": false
      }
    },
    {
      "to_do": {
        "rich_text": [{ "text": { "content": "Hierarquia visual adequada" } }],
        "checked": false
      }
    },
    {
      "to_do": {
        "rich_text": [{ "text": { "content": "Responsividade adequada" } }],
        "checked": false
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "📝 Feedback do Cliente" } }]
      }
    },
    {
      "paragraph": {
        "rich_text": [{ "text": { "content": "(Aguardando revisão)" } }]
      }
    },

    {
      "heading_2": {
        "rich_text": [{ "text": { "content": "🔗 Referências" } }]
      }
    },
    {
      "paragraph": {
        "rich_text": [
          {
            "text": {
              "content": "Design System: design-system/{nome}/MASTER.md\nContent Strategy: docs/content/CONTENT-STRATEGY-{nome}.md"
            }
          }
        ]
      }
    }
  ]
}
```

**Ao marcar "Aguardando Aprovação" - Notificar Cliente:**

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [
    {
      "text": {
        "content": "🎨 **Protótipo pronto para validação**\n\n📋 Por favor, revise o protótipo acima e valide:\n✅ Layout e visual\n✅ Textos e copy\n✅ Hierarquia de informações\n\n📝 **Ações:**\n🟢 Aprovado? Marque status como 'Concluído'\n🔴 Ajustes necessários? Marque status como 'Recusado' e descreva nos comentários"
      }
    }
  ]
}
```

---

### 🔗 Vínculo: Prototipação → Implementação

> [!IMPORTANT]
> **REGRA:** Tasks de Prototipação e Implementação são SEPARADAS.
> Após aprovação do protótipo, a task de implementação (Feature) é liberada.

**Estrutura de Tasks:**

```
Task: "Header - Protótipo"        Task: "Header - Implementação"
├── Categoria: Prototipação       ├── Categoria: Feature
├── Status: Concluído             ├── Status: Não iniciado → Em andamento
└── Link para implementação ──────└── Link para protótipo
```

**No corpo da task de Implementação (Feature), adicionar referência:**

```json
{
  "paragraph": {
    "rich_text": [
      { "text": { "content": "🔗 Protótipo aprovado: #{id_task_prototipo}" } }
    ]
  }
}
```

**Query para verificar se protótipo foi aprovado antes de iniciar implementação:**

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DATABASE_ID}",
  "filter": {
    "and": [
      {
        "property": "Nome da tarefa",
        "title": { "contains": "{nome_tela} - Protótipo" }
      },
      { "property": "Status", "status": { "equals": "Concluído" } }
    ]
  }
}
```

> [!CAUTION]
> **BLOQUEADOR:** NÃO iniciar task de implementação sem protótipo correspondente com Status = "Concluído".

---

## 🔌 API TEMPLATES CENTRALIZADOS

> [!IMPORTANT]
> **SINGLE SOURCE OF TRUTH:** Todos os workflows DEVEM usar estes templates.
> Não duplique exemplos de API nos workflows - referencie esta skill.

---

### Status Values (CANÔNICOS)

| Status                   | Quando Usar                                          | Valor API                |
| ------------------------ | ---------------------------------------------------- | ------------------------ |
| **Não iniciado**         | Task criada, não começada                            | `"Não iniciado"`         |
| **Em andamento**         | Task em execução                                     | `"Em andamento"`         |
| **Aguardando Aprovação** | ⭐ Protótipo pronto, aguardando validação do cliente | `"Aguardando Aprovação"` |
| **Recusado**             | ❌ Cliente não aprovou (requer comentário)           | `"Recusado"`             |
| **Concluído**            | ✅ Task finalizada / Cliente aprovou                 | `"Concluído"`            |

> [!CAUTION]
> **REGRA:** Status `Recusado` **EXIGE** comentário do cliente com feedback.
> Agente DEVE analisar comentários, ajustar protótipo, e retornar para `Aguardando Aprovação`.

**Ciclo de Recusa:**

```
Recusado (com comentário)
        ↓
Agente analisa feedback
        ↓
Ajusta protótipo
        ↓
Atualiza task (novo preview)
        ↓
Status → Aguardando Aprovação
        ↓
Notifica cliente (comentário)
```

> [!NOTE]
>
> - `Última edição` → Atualizada **automaticamente** a cada modificação
> - `Criado em` → Preenchido **automaticamente** ao criar a página

---

### 🔍 Buscar Database

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "Tarefas",
  "filter": { "property": "object", "value": "data_source" }
}
```

### 🔎 Buscar Task por ID (PREFERIDO)

> [!TIP]
> **Método mais preciso:** Use busca por `unique_id` quando souber o ID da task.

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DATABASE_ID}",
  "filter": {
    "property": "ID",
    "unique_id": {
      "equals": 42
    }
  }
}
```

> [!CAUTION]
> **IMPORTANTE:** Use `"unique_id"` como tipo do filtro, **NÃO** `"number"`.

**Operadores disponíveis:**

| Operador                   | Uso                                 |
| -------------------------- | ----------------------------------- |
| `equals`                   | Buscar task específica por ID exato |
| `does_not_equal`           | Excluir task específica             |
| `greater_than`             | Tasks após ID X                     |
| `less_than`                | Tasks antes de ID X                 |
| `greater_than_or_equal_to` | Tasks a partir de ID X              |
| `less_than_or_equal_to`    | Tasks até ID X                      |

### 🔎 Buscar Task por Nome (Alternativa)

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "{Nome da Task}",
  "filter": { "property": "object", "value": "page" }
}
```

> [!NOTE]
> Busca por nome é menos precisa (pode retornar múltiplos resultados).
> Prefira busca por ID quando disponível.

### 📋 Validar Schema

```json
// Tool: mcp_notion-mcp-server_API-retrieve-a-database
{ "database_id": "{DATABASE_ID}" }
```

### ➕ CRIAR TASK (2 ETAPAS OBRIGATÓRIAS) ⭐

> [!CAUTION]
> **REGRA BLOQUEANTE:** Criação de tasks é um processo de **2 ETAPAS SEQUENCIAIS**.
> Uma task SÓ está completa após AMBAS as etapas. Pular ETAPA 2 = task incompleta.

---

#### ETAPA 1: Criar Página (Propriedades)

```json
// Tool: mcp_notion-mcp-server_API-post-page
{
  "parent": { "database_id": "{DATABASE_ID}" },
  "properties": {
    "Nome da tarefa": { "title": [{ "text": { "content": "{nome}" } }] },
    "Status": { "status": { "name": "Não iniciado" } },
    "Épico": { "select": { "name": "{N. Nome}" } },
    "Categoria": { "multi_select": [{ "name": "{categoria}" }] },
    "Prioridade": { "select": { "name": "Alta" } },
    "Estimativa": { "number": {horas} },
    "% Progresso": { "number": 0 }
  }
}
```

**⚠️ IMPORTANTE:** Salvar o `page_id` retornado (campo `id` na resposta) para ETAPA 2.

---

#### ETAPA 2: Adicionar Corpo (OBRIGATÓRIO)

> [!CAUTION]
> **IMEDIATAMENTE** após ETAPA 1, executar ETAPA 2. NÃO prosseguir para próxima task sem completar esta etapa.

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}", // ID retornado da ETAPA 1
  "children": [
    /* Template por categoria - ver seção TEMPLATES */
  ]
}
```

---

#### TEMPLATES POR CATEGORIA

**Feature (User Story):**

```json
[
  {
    "heading_2": { "rich_text": [{ "text": { "content": "📖 User Story" } }] }
  },
  {
    "paragraph": {
      "rich_text": [
        {
          "text": {
            "content": "As a **{persona}**, I want to **{action}**, so that **{benefit}**."
          }
        }
      ]
    }
  },
  {
    "heading_2": {
      "rich_text": [{ "text": { "content": "✅ Acceptance Criteria" } }]
    }
  },
  {
    "to_do": {
      "rich_text": [
        {
          "text": {
            "content": "Given {context}, When {action}, Then {outcome}"
          }
        }
      ],
      "checked": false
    }
  },
  {
    "heading_2": { "rich_text": [{ "text": { "content": "🔗 References" } }] }
  },
  {
    "paragraph": {
      "rich_text": [{ "text": { "content": "TDD: docs/design/TDD-{nome}.md" } }]
    }
  }
]
```

**Bug:**

```json
[
  { "heading_2": { "rich_text": [{ "text": { "content": "🐛 Problema" } }] } },
  {
    "paragraph": {
      "rich_text": [{ "text": { "content": "{descrição do bug}" } }]
    }
  },
  {
    "heading_2": {
      "rich_text": [{ "text": { "content": "📋 Passos para Reproduzir" } }]
    }
  },
  {
    "numbered_list_item": {
      "rich_text": [{ "text": { "content": "{passo 1}" } }]
    }
  },
  {
    "heading_2": {
      "rich_text": [{ "text": { "content": "✅ Critérios de Resolução" } }]
    }
  },
  {
    "to_do": {
      "rich_text": [{ "text": { "content": "{critério}" } }],
      "checked": false
    }
  }
]
```

**Log (Trabalho Retroativo):**

```json
[
  {
    "heading_2": {
      "rich_text": [{ "text": { "content": "📝 Resumo Técnico" } }]
    }
  },
  {
    "paragraph": {
      "rich_text": [{ "text": { "content": "{descrição técnica}" } }]
    }
  },
  {
    "heading_2": {
      "rich_text": [{ "text": { "content": "📁 Arquivos Afetados" } }]
    }
  },
  {
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "{arquivo}" } }]
    }
  }
]
```

---

> [!CAUTION]
> **REGRA BLOQUEANTE:** Criar múltiplas tasks com `API-post-page` e só depois adicionar corpos
> é **PROIBIDO**. O workflow **NÃO PODE PROSSEGUIR** enquanto houver tasks sem corpo.
> **CORRETO:** Para CADA task: ETAPA 1 → ETAPA 2 → próxima task.
> **Se ETAPA 2 falhar** (ex: erro de API, serialização), o agente DEVE resolver o erro
> e completar a ETAPA 2 **ANTES** de criar a próxima task ou avançar de fase.

> [!WARNING]
> **📜 HISTÓRICO DE FALHAS (2026-02-18):**
>
> - **Gap detectado:** 10 tasks criadas sem corpo — agente fez batch de ETAPA 1 para todas, pulou ETAPA 2
> - **Causa raiz:** Primeiro tentou `children` inline no `post-page` (erro 400 por serialização).
>   Ao refazer, criou todas as páginas sem corpo e avançou sem completar ETAPA 2.
> - **Correção aplicada:** Regra elevada de WARNING → CAUTION. Workflow não pode avançar sem corpos.

---

#### VERIFICAÇÃO DE CONCLUSÃO

Após criar todas as tasks, verificar:

```
[ ] Todas as tasks criadas com API-post-page
[ ] TODAS as tasks com corpo via API-patch-block-children
[ ] Template correto usado para cada categoria
```

---

## 🚨 GATE DE CONCLUSÃO DE FASE (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Uma fase que cria tasks no Notion SÓ pode ser marcada como "Concluída"
> após verificar que **100% das tasks** têm propriedades E corpo preenchidos.
> **NUNCA** avançar de fase sem completar esta verificação.

### Processo de Verificação (OBRIGATÓRIO)

**Antes de marcar qualquer fase como "Concluída":**

1. **Listar todas as tasks criadas na fase**
2. **Para CADA task, verificar:**
   - [ ] Propriedades obrigatórias preenchidas (Nome, Status, Épico, Categoria, Estimativa)
   - [ ] Corpo adicionado via `API-patch-block-children`
   - [ ] Corpo contém seções obrigatórias (User Story, Acceptance Criteria, References)

3. **Se QUALQUER task estiver incompleta → PARAR e completar antes de avançar**

### Query de Verificação

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DATABASE_ID}",
  "filter": {
    "property": "ID",
    "unique_id": {
      "greater_than_or_equal_to": {ID_INICIAL},
      "less_than_or_equal_to": {ID_FINAL}
    }
  }
}
```

Para cada task retornada, verificar se tem children/blocks:

```json
// Tool: mcp_notion-mcp-server_API-get-block-children
{
  "block_id": "{page_id}"
}
```

**Se `results` estiver vazio → task SEM corpo → INCOMPLETA**

### Mensagem de Erro OBRIGATÓRIA

Se encontrar tasks incompletas:

```markdown
⚠️ **FASE NÃO PODE SER CONCLUÍDA**

Encontrei {N} task(s) sem corpo preenchido:

| ID    | Nome   | Status       |
| ----- | ------ | ------------ |
| #{id} | {nome} | ❌ Sem corpo |

**Ação obrigatória:** Adicionar corpo a todas as tasks antes de avançar.
```

### Regras do Gate

1. **OBRIGATÓRIO** verificar TODAS as tasks antes de marcar fase como concluída
2. **NUNCA** atualizar PROJECT-PROGRESS.md para próxima fase sem completar verificação
3. **Se falhar**, completar tasks faltantes ANTES de prosseguir
4. **Log obrigatório** em PROJECT-PROGRESS.md: "Phase X: Verificação completa - N tasks"

---

### 🔄 Atualizar Status → Em Andamento

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Em andamento" } }
  }
}
```

### ✅ Atualizar Status → Concluído

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Concluído" } },
    "Tempo Gasto": { "rich_text": [{ "text": { "content": "{Xh}m" } }] }
  }
}
```

> [!CAUTION]
> **OBRIGATÓRIO:** `Tempo Gasto` deve ser preenchido ao concluir.

### 💬 Adicionar Comentário de Progresso

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [
    { "text": { "content": "🔄 **Progresso:** {descrição do avanço}" } }
  ]
}
```

### ✅ Comentário de Conclusão (RICO - OBRIGATÓRIO)

> [!IMPORTANT]
> **REGRA:** Ao concluir task, adicionar comentário rico para transparência com cliente.
> Use o idioma definido em PROJECT-PROGRESS.md.

#### 🇧🇷 Português (PT-BR)

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [
    {
      "text": {
        "content": "✅ **Task Concluída**\n\n📋 **O que foi feito:**\n• {descrição simples do que foi implementado}\n• {outra funcionalidade se aplicável}\n\n📁 **Arquivos modificados:**\n• {arquivo 1}\n• {arquivo 2}\n\n🔗 **Próximos passos:**\n• {task relacionada ou \"Nenhum - task independente\"}"
      }
    }
  ]
}
```

#### 🇺🇸 English (EN)

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [
    {
      "text": {
        "content": "✅ **Task Completed**\n\n📋 **What was done:**\n• {simple description of what was implemented}\n• {another feature if applicable}\n\n📁 **Files modified:**\n• {file 1}\n• {file 2}\n\n🔗 **Next steps:**\n• {related task or \"None - standalone task\"}"
      }
    }
  ]
}
```

> [!TIP]
> **Para transparência:** Use linguagem simples que o cliente entenda.
> Evite jargões técnicos quando possível.

## 🔄 PHASE TASK TRACKING (Padrão Compartilhado)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Toda atividade pós-análise em qualquer workflow estruturado
> DEVE ter tasks no Notion para **transparência com o cliente**.
> Trabalho executado sem task = trabalho invisível = falha de comunicação.

### Quando Aplicar

| Workflow          | Fases que DEVEM ter tasks                                                                 |
| ----------------- | ----------------------------------------------------------------------------------------- |
| `/legacy-project` | Phase 4 (Documentação), Phase 5 (TDD), Phase 5.5 (Design System), Phase 6 (Testes)        |
| `/new-project`    | Phase 2.5 (Design System), Phase 2.65 (Content), Phase 2.8 (Page Specs), Phase 4 (Testes) |

### Categorias por Tipo de Fase

| Tipo de Fase           | Categoria Notion | Épico Sugerido             |
| ---------------------- | ---------------- | -------------------------- |
| Documentação de fluxos | `Documentação`   | `{módulo} - Documentação`  |
| TDD Técnico/Reverso    | `Documentação`   | `{módulo} - TDD`           |
| Design System          | `Melhoria`       | `{módulo} - Design System` |
| Escrita de Testes      | `Melhoria`       | `{módulo} - Testes`        |
| Melhorias/Refatoração  | `Refatoração`    | `{módulo} - Melhorias`     |

### Processo: Breakdown de Fases (OBRIGATÓRIO)

**Executar ANTES de iniciar a primeira fase que gera artefatos.**

**Passo 1:** Discovery do database + validação de schema (ver seção "VALIDAÇÃO DE SCHEMA")

**Passo 2:** Perguntar idioma (se não definido — ver seção "IDIOMA DAS TASKS")

**Passo 3:** Criar 1 task por atividade planejada, usando:

- Propriedades: seguir seção "CRIAR TASK (2 ETAPAS OBRIGATÓRIAS)"
- Corpo: usar **Template Documentação** (ver seção acima)
- Categoria: conforme tabela "Categorias por Tipo de Fase"

**Exemplo para `/legacy-project` módulo `auth`:**

| #   | Task                                  | Categoria    | Épico                | Estimativa |
| --- | ------------------------------------- | ------------ | -------------------- | ---------- |
| 1   | Documentar fluxo: Login               | Documentação | auth - Documentação  | 2h         |
| 2   | Documentar fluxo: Register            | Documentação | auth - Documentação  | 2h         |
| 3   | TDD Reverso: auth                     | Documentação | auth - TDD           | 4h         |
| 4   | Design System: extração               | Melhoria     | auth - Design System | 3h         |
| 5   | Testes: Integration (fluxos críticos) | Melhoria     | auth - Testes        | 4h         |
| 6   | Testes: Unit (funções complexas)      | Melhoria     | auth - Testes        | 3h         |

### Gate: NOTION SYNC ao Final de Cada Fase (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Ao concluir QUALQUER fase, o agente DEVE executar
> os 4 passos abaixo ANTES de avançar para a próxima fase.
> Pular sync = Phase NÃO pode ser marcada como concluída.

**Passo 1 — Atualizar status da(s) task(s) da fase:**

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Concluído" } },
    "Tempo Gasto": { "rich_text": [{ "text": { "content": "{tempo_real}" } }] },
    "% Progresso": { "number": 100 }
  }
}
```

**Passo 2 — Adicionar nota de conclusão no corpo:**

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    { "divider": {} },
    {
      "callout": {
        "icon": { "type": "emoji", "emoji": "✅" },
        "rich_text": [{ "text": { "content": "Concluído em {data}" } }]
      }
    },
    {
      "bulleted_list_item": {
        "rich_text": [
          { "text": { "content": "📁 Artefato: {arquivo gerado}" } }
        ]
      }
    }
  ]
}
```

**Passo 3 — Adicionar comentário rico de conclusão:**

> Seguir seção "Comentário de Conclusão (RICO - OBRIGATÓRIO)" desta skill.

**Passo 4 — Verificar que TODAS as tasks da fase foram synced:**

> Seguir seção "GATE DE CONCLUSÃO DE FASE" desta skill.

### Checklist de Fase

```markdown
⚠️ VERIFICAÇÃO - Phase {N} Concluída?

[ ] Todas tasks da fase com Status = "Concluído"
[ ] Tempo Gasto preenchido em cada task
[ ] Nota de conclusão adicionada ao corpo de cada task
[ ] Comentário rico adicionado a cada task
[ ] PROJECT-PROGRESS.md atualizado

❌ Se QUALQUER item desmarcado → NÃO avançar para próxima fase
✅ TODOS marcados → Prosseguir
```

---

## 📚 DOCUMENTATION DATABASES (Padrão Compartilhado)

> [!IMPORTANT]
> **Propósito:** Dois databases Notion separados para **documentação orientada a públicos distintos**.
>
> - **"Documentação Técnica"** — para desenvolvedores: fluxos com código, diagramas Mermaid, atoms, contratos de API
> - **"Manual do Usuário"** — para usuário final e operadores: passo-a-passo visual, sem código
>   Diferente da "Tarefas" (que rastreia trabalho), as databases de documentação entregam **conhecimento**.

### Quando Aplicar

| Workflow          | Momento                                  | Databases               |
| ----------------- | ---------------------------------------- | ----------------------- |
| `/legacy-project` | Phase 8 (técnica) + Phase 8.5 (manual)   | Ambos                   |
| `/new-project`    | Phase 7.5 (técnica) + Phase 7.6 (manual) | Ambos                   |
| `/document`       | Fase 4 — após cross-reference            | Ambos (manual opcional) |
| `/new-task`        | Fase 0.5 — context check                 | Buscar em ambos         |

---

### 🔴 DATABASE 1: "Documentação Técnica"

> [!CAUTION]
> **REGRA BLOQUEANTE:** Buscar database com nome exato **"Documentação Técnica"**.
> NÃO usar "Docs", "Documentation", "Documentação", ou qualquer variação.

#### Busca Obrigatória

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "Documentação Técnica",
  "filter": { "property": "object", "value": "data_source" }
}
```

#### Se NÃO encontrar

```markdown
⚠️ **Database "Documentação Técnica" não encontrado.**

Para publicar a documentação técnica do projeto:

1. Crie um database **"Documentação Técnica"** no Notion com as propriedades listadas abaixo
2. Compartilhe o database com a integração (bot)
3. Confirme para continuar

**Propriedades obrigatórias:**

| Propriedade        | Tipo      | Descrição                                      |
| ------------------ | --------- | ---------------------------------------------- |
| Nome               | Title     | Nome do documento                              |
| Módulo             | Select    | Escopo (shop/, api/, admin/)                   |
| Tipo               | Select    | Fluxo, TDD, Design System, Testes, Arquitetura |
| Status             | Status    | Rascunho → Publicado → Atualizado              |
| Última Atualização | Date      | Data da última edição                          |
| Arquivo Local      | Rich Text | Path do arquivo no repositório                 |
| Tasks Relacionadas | Rich Text | IDs das tasks associadas                       |
```

---

### 📖 DATABASE 2: "Manual do Usuário"

> [!CAUTION]
> **REGRA BLOQUEANTE:** Buscar database com nome exato **"Manual do Usuário"**.
> NÃO usar "User Manual", "Guia", ou qualquer variação.

#### Busca Obrigatória

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "Manual do Usuário",
  "filter": { "property": "object", "value": "data_source" }
}
```

#### Se NÃO encontrar

```markdown
⚠️ **Database "Manual do Usuário" não encontrado.**

Para publicar guias acessíveis para usuários e operadores:

1. Crie um database **"Manual do Usuário"** no Notion com as propriedades listadas abaixo
2. Compartilhe o database com a integração (bot)
3. Confirme para continuar

**Propriedades obrigatórias:**

| Propriedade  | Tipo   | Descrição                                                  |
| ------------ | ------ | ---------------------------------------------------------- |
| Nome         | Title  | Título amigável do guia                                    |
| Seção        | Select | Autenticação, Compras, Checkout, Pedidos, Conta, Operações |
| Status       | Select | Rascunho, Publicado                                        |
| Público-alvo | Select | Usuário Final, Operador                                    |
```

---

### 📋 PROPRIEDADES OBRIGATÓRIAS — Database "Documentação Técnica"

| Propriedade            | Tipo Notion | Obrigatório | Exemplo                                      |
| ---------------------- | ----------- | ----------- | -------------------------------------------- |
| **Nome**               | `title`     | ✅          | "Fluxo: Checkout Guest"                      |
| **Módulo**             | `select`    | ✅          | `shop/`                                      |
| **Tipo**               | `select`    | ✅          | `Fluxo`                                      |
| **Status**             | `status`    | ✅          | `Publicado`                                  |
| **Última Atualização** | `date`      | ✅          | 2026-02-16                                   |
| **Arquivo Local**      | `rich_text` | ✅          | `docs/flows/shop/checkout/checkout-guest.md` |
| **Tasks Relacionadas** | `rich_text` | ⭐          | `#1.1, #1.2, #1.3`                           |

#### Valores de "Tipo"

| Valor           | Quando usar                                                  |
| --------------- | ------------------------------------------------------------ |
| `Fluxo`         | Documentação de fluxo funcional (Phase 4 legacy)             |
| `TDD`           | Technical Design Document (Phase 5 legacy / Phase 2 new)     |
| `Design System` | Tokens, cores, tipografia (Phase 5.5 legacy / Phase 2.5 new) |
| `Testes`        | Estratégia e cobertura (Phase 6 legacy / Phase 4 new)        |
| `Arquitetura`   | CODEBASE, visão geral do módulo                              |
| `PRD`           | Product Requirements Document (new-project)                  |

#### Valores de "Status"

| Status       | Significado                                       |
| ------------ | ------------------------------------------------- |
| `Rascunho`   | Doc criado mas incompleto                         |
| `Publicado`  | Doc completo e disponível para o cliente          |
| `Atualizado` | Doc existente que foi re-publicado com alterações |

---

### 📋 PROPRIEDADES OBRIGATÓRIAS — Database "Manual do Usuário"

| Propriedade      | Tipo Notion | Obrigatório | Exemplo                |
| ---------------- | ----------- | ----------- | ---------------------- |
| **Nome**         | `title`     | ✅          | "Como criar sua conta" |
| **Seção**        | `select`    | ✅          | `Autenticação`         |
| **Status**       | `select`    | ✅          | `Publicado`            |
| **Público-alvo** | `select`    | ✅          | `Usuário Final`        |

#### Valores de "Seção"

| Valor          | Abrange                                |
| -------------- | -------------------------------------- |
| `Autenticação` | Login, registro, senha, social login   |
| `Compras`      | Catálogo, busca, navegação             |
| `Checkout`     | Fluxos de compra, pagamento            |
| `Pedidos`      | Acompanhamento, devoluções, reembolsos |
| `Conta`        | Perfil, wishlist, avaliações           |
| `Operações`    | Guias administrativos/operador         |

#### Valores de "Público-alvo"

| Valor           | Quem lê                   |
| --------------- | ------------------------- |
| `Usuário Final` | Cliente da loja           |
| `Operador`      | Admin, suporte, operações |

---

### 📝 TEMPLATES DE CORPO — Por Tipo de Documento

> [!IMPORTANT]
> O conteúdo deve ser **COMPLETO** (não resumo). O cliente lê no Notion sem acessar o repositório.

#### Template: Fluxo

```json
// Blocos Notion para documento tipo "Fluxo"
[
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": { "rich_text": [{ "text": { "content": "📋 Visão Geral" } }] }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{descrição do fluxo}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "🔄 Diagrama do Fluxo" } }]
    }
  },
  {
    "object": "block",
    "type": "code",
    "code": {
      "rich_text": [{ "text": { "content": "{diagrama mermaid}" } }],
      "language": "mermaid"
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "🧩 Componentes Envolvidos" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{tabela de componentes}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "📜 Regras de Negócio" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{regras identificadas}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "✅ Casos de Teste" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        { "text": { "content": "{happy path + edge cases + error cases}" } }
      ]
    }
  },
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "heading_3",
    "heading_3": {
      "rich_text": [{ "text": { "content": "📜 Histórico de Atualizações" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": {
            "content": "| Data | Descrição | Tasks |\n|------|-----------|-------|\n| {data} | Publicação inicial | {tasks} |"
          }
        }
      ]
    }
  }
]
```

#### Template: TDD

```json
// Blocos Notion para documento tipo "TDD"
[
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "🎯 Contexto e Objetivo" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{contexto do módulo}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "🛠️ Stack Tecnológica" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{stack identificada}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "📦 Módulos e Dependências" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{módulos analisados}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "⚠️ Riscos e Débitos Técnicos" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{riscos identificados}" } }]
    }
  },
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "heading_3",
    "heading_3": {
      "rich_text": [{ "text": { "content": "📜 Histórico de Atualizações" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": {
            "content": "| Data | Descrição | Tasks |\n|------|-----------|-------|\n| {data} | Publicação inicial | {tasks} |"
          }
        }
      ]
    }
  }
]
```

#### Template: Design System

```json
// Blocos Notion para documento tipo "Design System"
[
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": { "rich_text": [{ "text": { "content": "🎨 Cores" } }] }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{paleta de cores}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": { "rich_text": [{ "text": { "content": "🔤 Tipografia" } }] }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{fontes e escalas}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "📐 Espaçamento e Grid" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{spacing tokens}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": { "rich_text": [{ "text": { "content": "🧩 Componentes" } }] }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{componentes base}" } }]
    }
  },
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "heading_3",
    "heading_3": {
      "rich_text": [{ "text": { "content": "📜 Histórico de Atualizações" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": {
            "content": "| Data | Descrição | Tasks |\n|------|-----------|-------|\n| {data} | Publicação inicial | {tasks} |"
          }
        }
      ]
    }
  }
]
```

#### Template: Testes

```json
// Blocos Notion para documento tipo "Testes"
[
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "📊 Cobertura Atual" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{métricas de cobertura}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "🧪 Estratégia de Testes" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        { "text": { "content": "{pirâmide: unit > integration > e2e}" } }
      ]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "✅ Cenários Cobertos" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "{lista de cenários}" } }]
    }
  },
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "heading_3",
    "heading_3": {
      "rich_text": [{ "text": { "content": "📜 Histórico de Atualizações" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": {
            "content": "| Data | Descrição | Tasks |\n|------|-----------|-------|\n| {data} | Publicação inicial | {tasks} |"
          }
        }
      ]
    }
  }
]
```

---

### 🔄 UPSERT — Atualizar Documentação Existente

> [!CAUTION]
> **REGRA:** Antes de criar uma nova página, SEMPRE verificar se já existe um doc com
> mesmo **Nome** + **Módulo** na database. Se existir → ATUALIZAR, não duplicar.
> **Aplica-se a AMBOS databases:** "Documentação Técnica" e "Manual do Usuário".

#### Processo de Verificação — Documentação Técnica

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DOC_TECNICA_DATABASE_ID}",
  "filter": {
    "and": [
      { "property": "Nome", "title": { "equals": "{nome_do_doc}" } },
      { "property": "Módulo", "select": { "equals": "{módulo}" } }
    ]
  }
}
```

#### Processo de Verificação — Manual do Usuário

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{MANUAL_DATABASE_ID}",
  "filter": {
    "property": "Nome",
    "title": { "equals": "{nome_do_guia}" }
  }
}
```

#### Se encontrar (UPDATE)

1. **Deletar** blocos antigos do corpo (exceto o histórico)
2. **Adicionar** novos blocos com conteúdo atualizado
3. **Atualizar propriedades:**
   - `Status` → "Atualizado" (técnica) ou manter "Publicado" (manual)
   - `Última Atualização` → data atual
   - `Tasks Relacionadas` → adicionar novas tasks (append, não substituir) — apenas técnica
4. **Adicionar entrada** no histórico de atualizações (apenas técnica):
   ```
   | {data} | {descrição da atualização} | {novas tasks} |
   ```
5. **Adicionar comentário** na página:
   ```json
   // Tool: mcp_notion-mcp-server_API-create-a-comment
   {
     "parent": { "page_id": "{page_id}" },
     "rich_text": [
       {
         "text": {
           "content": "🔄 Documentação atualizada\n\n📋 Alterações: {descrição}\n📅 Data: {data}\n🔗 Tasks: {IDs}"
         }
       }
     ]
   }
   ```

#### Se NÃO encontrar (CREATE)

Seguir processo normal: ETAPA 1 (criar página) → ETAPA 2 (adicionar corpo com template).

---

### 📜 HISTÓRICO DE ATUALIZAÇÕES (Obrigatório — Documentação Técnica)

> [!IMPORTANT]
> **TODO documento na database "Documentação Técnica" DEVE ter um bloco de histórico** no final.
> O histórico registra cada publicação/atualização com referência às tasks do trabalho realizado.
> **Nota:** O "Manual do Usuário" NÃO requer histórico técnico — apenas conteúdo acessível.

#### Formato

```markdown
📜 Histórico de Atualizações

| Data       | Descrição                                                 | Tasks Relacionadas |
| ---------- | --------------------------------------------------------- | ------------------ |
| 2026-02-16 | Publicação inicial — documentação do fluxo checkout guest | #1.1, #1.2         |
| 2026-03-01 | Atualizado com novos edge cases identificados             | #3.5               |
```

#### Regras

1. **Publicação inicial** — entrada com data + "Publicação inicial" + tasks das fases que geraram o doc
2. **Updates subsequentes** — adicionar linha com data + descrição + novas tasks
3. **Tasks referenciadas** — usar os IDs das tasks da database "Tarefas" que geraram/atualizaram o doc
4. **Nunca deletar histórico** — apenas append de novas entradas

---

### Processo: Publicação de Documentação Técnica

> Usado na Phase 8 do `/legacy-project` e Phase 7.5 do `/new-project`.

#### Passo 1: Discovery e Validação

1. Buscar database "Documentação Técnica" (ver seção "DATABASE 1" acima)
2. Validar schema (ver seção "PROPRIEDADES OBRIGATÓRIAS — Database Documentação Técnica" acima)
3. Se ausente → PARAR e notificar usuário

#### Passo 2: Coletar Artefatos Gerados

Listar todos os docs gerados nas fases anteriores:

| Fonte                                | Tipo          | Arquivo Local                           |
| ------------------------------------ | ------------- | --------------------------------------- |
| Phase 4 (legacy) / —                 | Fluxo         | `docs/flows/{módulo}/{fluxo}.md`        |
| Phase 5 (legacy) / Phase 2 (new)     | TDD           | `docs/design/TDD-{projeto}-{módulo}.md` |
| Phase 5.5 (legacy) / Phase 2.5 (new) | Design System | `design-system/MASTER.md`               |
| Phase 6 (legacy) / Phase 4 (new)     | Testes        | (relatório de cobertura)                |
| Phase 1 (legacy)                     | Arquitetura   | `docs/CODEBASE-{projeto}.md`            |
| Phase 1 (new)                        | PRD           | `docs/PRD-{nome}.md`                    |

#### Passo 3: Para cada artefato

1. Verificar upsert (doc já existe?)
2. Ler conteúdo completo do arquivo local
3. Criar/atualizar página Notion com template correto
4. Preencher propriedades (Nome, Módulo, Tipo, Status, Data, Arquivo Local, Tasks)
5. Adicionar entrada no histórico

#### Passo 4: Relatório de Publicação

```markdown
📚 **DOCUMENTAÇÃO TÉCNICA PUBLICADA - {módulo}**

| #   | Documento | Tipo   | Status                 | Notion |
| --- | --------- | ------ | ---------------------- | ------ |
| 1   | {nome}    | {tipo} | {Publicado/Atualizado} | 🔗     |
| ... | ...       | ...    | ...                    | ...    |

Total: {N} documentos publicados
✅ Devs podem consultar em: Notion → Database "Documentação Técnica"
```

---

### Processo: Publicação do Manual do Usuário

> Usado na Phase 8.5 do `/legacy-project` e Phase 7.6 do `/new-project`.
> Executado APÓS a publicação da Documentação Técnica.

#### Passo 1: Discovery e Validação

1. Buscar database "Manual do Usuário" (ver seção "DATABASE 2" acima)
2. Validar schema (ver seção "PROPRIEDADES OBRIGATÓRIAS — Database Manual do Usuário" acima)
3. Se ausente → PARAR e notificar usuário

#### Passo 2: Mapear Fluxos Técnicos → Guias de Usuário

Para cada fluxo publicado na Documentação Técnica, gerar versão acessível:

| Fluxos Técnicos                                                   | Guia do Usuário               | Público-alvo  | Seção        |
| ----------------------------------------------------------------- | ----------------------------- | ------------- | ------------ |
| login, register, social-login, otp-login                          | Como criar sua conta          | Usuário Final | Autenticação |
| password-recovery                                                 | Esqueci minha senha           | Usuário Final | Autenticação |
| catalog, search                                                   | Navegando e buscando produtos | Usuário Final | Compras      |
| checkout-standard, checkout-guest, checkout-digital, payment-flow | Finalizando sua compra        | Usuário Final | Checkout     |
| orders                                                            | Acompanhando seus pedidos     | Usuário Final | Pedidos      |
| refunds                                                           | Devoluções e reembolsos       | Usuário Final | Pedidos      |
| profile                                                           | Gerenciando seu perfil        | Usuário Final | Conta        |
| wishlist                                                          | Lista de desejos              | Usuário Final | Conta        |
| reviews                                                           | Deixando avaliações           | Usuário Final | Conta        |
| (admin: pedidos)                                                  | Gestão de Pedidos             | Operador      | Operações    |
| (admin: produtos)                                                 | Gestão de Produtos            | Operador      | Operações    |
| (admin: usuários)                                                 | Gestão de Usuários            | Operador      | Operações    |

#### Passo 3: Template de Corpo — Manual do Usuário

```json
// Blocos Notion para guia do usuário
[
  {
    "object": "block",
    "type": "callout",
    "callout": {
      "rich_text": [
        { "text": { "content": "{descrição simples em 1-2 frases}" } }
      ],
      "icon": { "emoji": "💡" }
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "📝 Passo a Passo" } }]
    }
  },
  {
    "object": "block",
    "type": "numbered_list_item",
    "numbered_list_item": {
      "rich_text": [
        { "text": { "content": "{passo 1 — linguagem simples, sem código}" } }
      ]
    }
  },
  {
    "object": "block",
    "type": "numbered_list_item",
    "numbered_list_item": {
      "rich_text": [{ "text": { "content": "{passo 2}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "💡 Dicas Importantes" } }]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "{dica útil 1}" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "❓ Problemas Comuns" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": {
            "content": "| Problema | Solução |\n|----------|---------|\n| {problema 1} | {solução 1} |"
          }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "divider",
    "divider": {}
  },
  {
    "object": "block",
    "type": "callout",
    "callout": {
      "rich_text": [
        {
          "text": {
            "content": "Precisa de ajuda? Entre em contato com o suporte."
          }
        }
      ],
      "icon": { "emoji": "🆘" }
    }
  }
]
```

> [!CAUTION]
> **REGRAS DO MANUAL DO USUÁRIO:**
>
> - ❌ NÃO incluir nomes de componentes React, hooks, atoms, ou paths de arquivo
> - ❌ NÃO usar diagramas Mermaid ou JSON de API
> - ❌ NÃO referenciar libs (jotai, react-query, yup, etc.)
> - ✅ Usar linguagem simples e direta ("Clique em...", "Digite seu...")
> - ✅ Focar em ações do usuário, não em implementação técnica
> - ✅ Incluir dicas práticas e soluções para problemas comuns

#### Passo 4: Relatório de Publicação

```markdown
📖 **MANUAL DO USUÁRIO PUBLICADO - {módulo}**

| #   | Guia   | Público-alvo | Seção   | Status    |
| --- | ------ | ------------ | ------- | --------- |
| 1   | {nome} | {público}    | {seção} | Publicado |
| ... | ...    | ...          | ...     | ...       |

Total: {N} guias publicados
✅ Usuários e operadores podem consultar em: Notion → Database "Manual do Usuário"
```

---

## 📋 CHECKLIST DE USO

### Para Tasks (Database "Tarefas")

Antes de criar/atualizar task:

- [ ] **Idioma definido** em PROJECT-PROGRESS.md (PT-BR ou EN)
- [ ] Database descoberto dinamicamente (não hardcoded)
- [ ] Schema validado com propriedades obrigatórias
- [ ] Categoria detectada corretamente
- [ ] **ETAPA 1:** Task criada via `API-post-page`
- [ ] **ETAPA 2:** Corpo adicionado via `API-patch-block-children` (OBRIGATÓRIO)
- [ ] Template correto usado para categoria (no idioma do projeto)

Ao concluir task:

- [ ] `Status` → "Concluído"
- [ ] `Tempo Gasto` preenchido
- [ ] **Comentário rico** adicionado (no idioma do projeto)

### Para Documentação Técnica (Database "Documentação Técnica")

Antes de publicar:

- [ ] Database "Documentação Técnica" descoberto e validado
- [ ] Verificação de upsert realizada (doc já existe?)
- [ ] Conteúdo completo lido do arquivo local
- [ ] Template correto usado para o tipo de documento
- [ ] Histórico de atualizações incluído no corpo
- [ ] Tasks relacionadas referenciadas

### Para Manual do Usuário (Database "Manual do Usuário")

Antes de publicar:

- [ ] Database "Manual do Usuário" descoberto e validado
- [ ] Verificação de upsert realizada (guia já existe?)
- [ ] Conteúdo escrito em linguagem acessível (sem código)
- [ ] Template de guia usado (passo-a-passo + dicas + problemas)
- [ ] Público-alvo definido (Usuário Final ou Operador)
- [ ] Seção definida corretamente

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow          | Operação                                                                    |
| ----------------- | --------------------------------------------------------------------------- |
| `/discovery`      | Criar tasks do TDD                                                          |
| `/new-task`        | Criar task de melhoria/bug + context check em ambos DBs                     |
| `/tdd breakdown`  | Criar tasks do breakdown                                                    |
| `/legacy-project` | Tasks (phases 3.5-7) + Doc Técnica (phase 8) + Manual (phase 8.5)           |
| `/log`            | Criar task retroativa                                                       |
| `/execute`        | Atualizar task existente                                                    |
| `/new-project`    | Tasks (breakdown + tracking) + Doc Técnica (phase 7.5) + Manual (phase 7.6) |
| `/task-update`    | Atualizar progresso                                                         |
| `/document`       | Publicar doc em ambos DBs (Fase 4)                                          |
