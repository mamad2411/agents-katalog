---
name: tracker-hub-agent-bootstrap
description: Crear, configurar, documentar, auditar y verificar agentes en cualquier instancia de Tracker Hub o Banhaia Hub siguiendo las plantillas canónicas (doc madre + bootstrap 7-fases + driver matrix + security defaults + verificación). Usá este skill SIEMPRE que el usuario quiera crear, modificar, auditar o documentar un agente sobre tracker-hub, aunque NO mencione "skill", "plantilla" o "bootstrap". Aplicalo también cuando te pidan configurar un workflow autónomo con LLM, conectar un bot externo (Slack/Telegram/Chatwoot/WhatsApp) a tracker-hub, diagnosticar por qué un agente sale con output vacío o no llama tools, decidir entre langchain_ollama / cli / anthropic / openai, configurar un coder con worktree aislado y require_approval, definir security_config / mcp_tools_allowlist / blocked_tools, o auditar el inventario de agentes existente. Cubre los 7 pasos — discovery, workspace, docs operativos, doc madre, tracker_create_agent, bindings, verificación.
---

# Tracker Hub Agent Bootstrap

> **Para qué sirve este skill**: bootstrapear un agente nuevo en cualquier instancia de Tracker Hub
> siguiendo las plantillas canónicas. El agente que lo lee es responsable de hacer discovery primero,
> escribir el doc madre antes que el agente técnico, configurar `provider_config` correcto según
> driver, bindear workspace con rol `owner`, verificar con smoke test, y dejar el inventario
> actualizado por nombre + ID.

---

## TL;DR — flujo recomendado (7 fases)

1. **Discovery** — `tracker_search`, `tracker_list_agents`, `tracker_list_workspaces`, `tracker_search_documents`. Si hay un agente con el mismo propósito → parar y reportar al humano.
2. **Workspace/dominio** — crear `workspace` + `module`s + `user`s si no existen. Anotar todos los IDs.
3. **Docs operativos** — `folder` del dominio + guía operativa + perfiles individuales (uno por humano relevante).
4. **Doc madre** — copiar plantilla de `references/doc-madre-template.md`, completar 11 secciones, crear `Agente {tipo} — {nombre}` + doc memoria. Linkear al workspace.
5. **Agente técnico** — `tracker_create_agent` con la plantilla JSON del driver elegido (ver `references/provider-config.md`). `system_prompt` **referencia el doc madre por ID, NO duplica contenido**.
6. **Bindings** — `tracker_bind_agent_workspace` con `role:'owner'` (obligatorio, sin esto los tools scope-filtered devuelven vacío). Opcional: tool bindings, cron jobs, event triggers, messaging contacts (`authorized:1`).
7. **Verificación** — `tracker_run_agent` con input de prueba, `tracker_get_agent_run` para inspeccionar, validar header `[langchain_ollama: <model>, tools:N, num_ctx:N, history:N]` en `error_output`. Completar los IDs reales en el doc madre.

---

## Driver default

`langchain_ollama` + `qwen2.5:7b` + `temperature:0.1` + `num_ctx:8192` + `timeout_ms:120000` + `concurrency:1`.

CLI (`claude`, `codex`, `gemini`) **solo para coders pesados** con `working_dir` válido y `use_worktree:true`. APIs pagas (`anthropic`, `openai`) solo cuando se necesita modelo grande con razonamiento fuerte.

Decisión completa: [`references/driver-matrix.md`](./references/driver-matrix.md).

---

## Provider config — 3 modos operativos

| Modo | Flags | Cuándo |
|------|-------|--------|
| **Static KB** | `disable_tools:true, include_content:true` | Bots externos (Chatwoot, WhatsApp), KB chica determinista |
| **Dynamic MCP** | `disable_tools:false, include_content:false, num_ctx:16384` | KBs grandes, agente busca on-demand |
| **Híbrido** | `disable_tools:false, include_content:true, num_ctx:16384+` | Asistentes multi-turn con KB embebida y tools de búsqueda |

Plantilla JSON completa por driver: [`references/provider-config.md`](./references/provider-config.md).

---

## Security defaults (obligatorios)

```json
"security_config": {
  "block_on_injection": true,
  "log_inputs": true,
  "blocked_tools": ["tracker_delete_*"]
}
```

Para agentes externos (que reciben input de Slack/Telegram/Chatwoot/WhatsApp): `block_on_injection:true` siempre. Para agentes con write: agregar `allowed_tools` allowlist explícito si vas a permitir mutaciones puntuales.

Detalle completo: [`references/security-defaults.md`](./references/security-defaults.md).

---

## Filtrado real de tools (gotcha crítico)

**Para `langchain_ollama`**: el filtro que ve el modelo es `provider_config.mcp_tools_allowlist` / `mcp_tools_denylist`. `allowed_tools` a nivel del agente **NO filtra lo que el modelo ve**; opera en otra capa.

```json
"provider_config": {
  "mcp_tools_allowlist": [
    "tracker_list_items", "tracker_get_item", "tracker_create_item", "tracker_update_item",
    "tracker_search", "tracker_search_documents", "tracker_get_document",
    "tracker_list_modules", "tracker_get_workspace"
  ]
}
```

Tools curados del driver `langchain_ollama` (23): 20 read + 3 write (`tracker_create_item`, `tracker_update_item`, `tracker_update_item_status`). Si necesitás otros write tools, escalá a `cli` driver o pedile al humano.

---

## Verificación post-creación

Después de `tracker_run_agent`, **siempre** inspeccionar el run:

```
tracker_get_agent_run run_id=<id>
```

Validar:
- `exit_code` = 0
- `output` no vacío (si está vacío con exit_code 0 → bump `num_ctx` a `16384`)
- `error_output` arranca con `[langchain_ollama: <modelo>, tools: <n>, num_ctx: <n>, history: <n>]`
- `tools: 0` confirma `disable_tools: true`; si esperabas tools, está mal config.
- Si el agente debía llamar tools y no las llamó → driver mal elegido (`ollama` simple no tiene tool-calling, usar `langchain_ollama`).

Checklist completo: [`references/verification.md`](./references/verification.md).

---

## Memoria — modelo de 2 capas

- **Tracker Hub (canónico, persistente)**: un doc `{Agente} — Memoria` por agente. <200 líneas. Update via `tracker_update_document` al final del ciclo. **Sobrevive** a reinstalaciones, otros runners, auditorías.
- **Filesystem (scratch, ephemeral)**: `.tracker-hub/agents/{agent_id}/` con `memory.md`, `notes/`, `cache/`, `runs/{run_id}/`. Descartable; el agente debe funcionar aunque esté vacío.

Regla de promoción: si una nota del scratch se usa 2-3 veces → consolidar al doc memoria → limpiar scratch.

Detalle: [`references/memory-model.md`](./references/memory-model.md).

---

## CLI coders — worktree lifecycle

Solo para `type:"cli"` (claude/codex/gemini). Activá con `provider_config.use_worktree:true`. El run trabaja en `agent-run/{runId}` en una worktree aislada con identidad git propia. Estrategias:

- **`worktree_strategy:"persistent"`** (default): si la branch tiene commits, worktree + branch persisten para review humano. Si no, ambos se borran.
- **`worktree_strategy:"ephemeral"`**: worktree dir siempre se borra; branch sobrevive si tiene commits.

Para gates humanos: `provider_config.require_approval:true` → al terminar con cambios, status pasa a `awaiting_approval` y manda notificación. Continuación: `context.continuation = { prev_run_id: "<id>" }` reusa el branch del run anterior.

---

## Anti-checklist (errores frecuentes)

Estos son los errores que **siempre** hay que evitar. Detalle con síntomas y fixes en [`references/pitfalls.md`](./references/pitfalls.md):

- Crear el agente técnico **antes** que el doc madre.
- Hardcodear contenido del prompt en lugar de referenciar el doc madre por ID.
- Olvidar `tracker_bind_agent_workspace` (tools devuelven vacío silenciosamente).
- Usar `allowed_tools` agent-level esperando que filtre lo que el modelo ve (no lo hace para `langchain_ollama`).
- Especificar un `model` que no está descargado en el host Ollama (`ollama list` para verificar).
- `num_ctx:8192` con KB > 10k chars → output vacío + exit_code 0. Bumpear a 16384.
- Tags genéricos (`general`, `test`) — no permiten discovery posterior.
- Skipar la verificación post-creación.
- Dejar `messaging_contacts.authorized:0` y esperar que los webhooks funcionen.
- Crear agentes duplicados (sin discovery previo).
- Referenciar otros docs/agentes por nombre solamente (sin ID hex16).

---

## Cuándo invocarme (señales para triggerear)

- "Crear un agente para X" / "agregar un bot a tracker-hub" / "configurar un asistente"
- "Bootstrappear un workspace nuevo con agente"
- "El agente no llama tools" / "el output sale vacío" / "diagnosticar agente"
- "Auditar agentes" / "revisar inventario" / "mantener docs de agentes"
- "Cambiar de Claude a Ollama" / "elegir driver" / "qué modelo usar"
- "Configurar Slack/Telegram/Chatwoot con un agente"
- "Coder agent con worktree" / "approval flow" / "auto-merge"
- "Por qué el agente no ve los workspaces" / "scope vacío"

---

## Plantilla mínima `tracker_create_agent` (langchain_ollama)

```json
{
  "name": "{Nombre legible}",
  "type": "langchain_ollama",
  "category": "assistant",
  "description": "Ver doc madre {doc_madre_id}",
  "timeout_ms": 120000,
  "concurrency": 1,
  "system_prompt": "Sos {Nombre}. Tu rol y reglas están definidos en el documento canónico '{Título doc madre}' (`{doc_madre_id}`) y tu memoria operativa en '{Título memoria}' (`{doc_memoria_id}`). Antes de cualquier acción, validá esos documentos. {Instrucciones específicas breves, 1-2 oraciones}",
  "provider_config": {
    "host": "http://localhost:11434",
    "model": "qwen2.5:7b",
    "temperature": 0.1,
    "num_ctx": 8192,
    "disable_tools": false,
    "include_content": false,
    "mcp_tools_allowlist": [
      "tracker_list_items", "tracker_get_item", "tracker_create_item", "tracker_update_item",
      "tracker_search", "tracker_search_documents", "tracker_get_document",
      "tracker_list_modules", "tracker_get_workspace"
    ]
  },
  "security_config": {
    "block_on_injection": true,
    "log_inputs": true,
    "blocked_tools": ["tracker_delete_*"]
  },
  "tags": ["{dominio}", "{categoria}"]
}
```

Variantes por driver (cli coder, ollama simple, anthropic, openai) en [`references/provider-config.md`](./references/provider-config.md).

---

## Bindings obligatorios después de crear

```
tracker_bind_agent_workspace agent_id=<id> workspace_id=<wid> role=owner
```

Sin esto, los tools scope-filtered (`tracker_list_items`, `tracker_get_workspace`) devuelven vacío. **Es la causa más común de "el agente no ve nada"**.

Opcionales según caso:
- `tracker_bind_agent_tool` — bindear herramientas externas (gh, npm, etc).
- `tracker_create_cron` — schedule recurrente.
- `tracker_create_agent_trigger` — evento → agente.
- `tracker_create_messaging_contact` con `authorized:1` — webhooks Slack/Telegram/Chatwoot.

---

## Recetas express por categoría

### Asistente conversacional (chat + tools)
- Driver: `langchain_ollama`
- Modo: Híbrido (`include_content:true` + tools on)
- KB: 2-5 docs canónicos por `kb_doc_ids`
- num_ctx: 16384 (o 65536 si KB grande)

### Bot externo (Chatwoot/WhatsApp) con KB estática
- Driver: `langchain_ollama`
- Modo: Static KB (`disable_tools:true, include_content:true`)
- Integración: `integrations.config.user_api_token` (NO `api_token` — bot tokens no leen mensajes)
- Output: `tracker-hub` backend strippea markdown antes de POST (WhatsApp)

### PM / Reviewer / Auditor
- Driver: `langchain_ollama` o `cli` codex (`model_reasoning_effort:high`)
- Memoria persistente: doc memoria + `tracker_get_document` al inicio, `tracker_update_document` al final
- Output: app + view (NO Slack walls)

### Coder pesado
- Driver: `cli` (claude/codex)
- `working_dir`: ruta válida del repo
- `provider_config.use_worktree:true`
- `provider_config.injection_profile:"claude"|"codex"|"gemini"`
- `provider_config.require_approval:true` para gates humanos (recomendado)
- Para autonomous: agregar `--dangerously-skip-permissions` o equivalente en `args`
- system_prompt: `"Sos {Nombre}. Modo AUTÓNOMO — NUNCA preguntar, NUNCA plan mode. Leé CLAUDE.md, implementá, commit con mensaje descriptivo."`

---

## Referencias cruzadas

- [`references/doc-madre-template.md`](./references/doc-madre-template.md) — las 11 secciones canónicas (copiar y completar)
- [`references/driver-matrix.md`](./references/driver-matrix.md) — cuándo usar qué driver
- [`references/provider-config.md`](./references/provider-config.md) — plantillas JSON por driver + 3 modos
- [`references/security-defaults.md`](./references/security-defaults.md) — block_on_injection, allowlist, mínima exposición
- [`references/verification.md`](./references/verification.md) — smoke test post-creación + interpretación del header diagnóstico
- [`references/memory-model.md`](./references/memory-model.md) — 2 capas: tracker-hub canónico + .tracker-hub/agents/{id}/ scratch
- [`references/pitfalls.md`](./references/pitfalls.md) — anti-checklist completo con síntomas y fixes

Skills hermanos en este repo:
- `tracker-hub-apps-builder` — para fase 6 (Surface): apps JSX como salida del agente.
- `tracker-hub-views-builder` — para dashboards/kioskos que el agente alimenta.

---

## 8 reglas de oro

1. **Tracker Hub es la única fuente de verdad** (el filesystem es scratch).
2. **Documentar antes de crear** (doc madre + memoria antes de `tracker_create_agent`).
3. **Referenciar por nombre + ID hex16** — solo nombre es un bug.
4. **No duplicar** — siempre `tracker_search`, `tracker_list_agents`, `tracker_search_documents` antes de crear.
5. **Mínima exposición** — `mcp_tools_allowlist` en `provider_config`, NO `allowed_tools` agent-level.
6. **Output operativo a apps/views**, no a Slack dumps.
7. **Verificar después de crear** — smoke run + leer `error_output`.
8. **Driver default = `langchain_ollama`**. CLI solo para coders pesados.
