---
name: ollama-agent
description: Use when implementas o ajustas un agente Ollama en Nexus (src/nexus/agents/) — patrón make_chat_client(model, host) con StripUnsupportedOllamaOptions, instrucciones del agente como string explícito, binding de @tool, modelo por defecto qwen3:8b, consideraciones de num_ctx y streaming. Referencia src/nexus/llm/ y src/nexus/agents/recon.py.
---

# Skill: Ollama Agent

> Patrón canónico para construir agentes Ollama en Nexus. Todos los agentes usan `make_chat_client` de la factory central, no instancian `OllamaChatClient` directamente.

## Cuándo usar esta skill

- Implementas un nuevo agente en `src/nexus/agents/<agent>.py`.
- Ajustas el modelo, el host o las instrucciones de un agente existente.
- Añades tools a un agente o cambias su `approval_mode`.
- Depuras errores de handoff, streaming o `num_ctx` con Ollama.

## Factory central — `nexus.llm.make_chat_client`

**Nunca instancies `OllamaChatClient` directamente.** Usa siempre la factory:

```python
from nexus.llm import make_chat_client

client = make_chat_client(model="qwen3:8b", host=None)
```

Por qué la factory y no instanciación directa:
- DRY: todos los agentes comparten la misma configuración (incluyendo middleware).
- El middleware `StripUnsupportedOllamaOptions` se aplica automáticamente — sin él, los workflows de handoff revienten con `TypeError` en `ollama>=0.5.x`.
- Si se añade más middleware (telemetría, rate-limit), se toca un único sitio.

## StripUnsupportedOllamaOptions (middleware obligatorio)

El conector `agent_framework_ollama` marca `allow_multiple_tool_calls` como "no soportada" pero la pasa por error al cliente subyacente. `HandoffBuilder` fuerza esta key en cada agente clonado, lo que provoca `TypeError`. El middleware la filtra antes de que llegue al handler final.

Ya está registrado en `make_chat_client` — no hay que instanciarlo manualmente. Si en el futuro aparecen más keys incompatibles, se añaden a `StripUnsupportedOllamaOptions.UNSUPPORTED_KEYS` en `src/nexus/llm/middleware.py`.

## Modelo por defecto y configuración

```python
# src/nexus/config.py (referencia)
DEFAULT_MODEL = "qwen3:8b"     # modelo local por defecto
DEFAULT_HOST  = None            # None → http://localhost:11434 o $OLLAMA_HOST
```

El modelo se lee de `CONFIG` para que sea configurable sin tocar el código del agente:

```python
from nexus.config import CONFIG

client = make_chat_client(model=CONFIG.ollama_model, host=CONFIG.ollama_host)
```

## Patrón canónico de agente

```python
"""Agente <nombre> de Nexus.

<Descripción del propósito y fase del agente.>

Diseño:
- Agent único (no Workflow) para Fase 1. El LLM decide el orden de tools
  basándose en INSTRUCTIONS y en los findings que devuelve cada tool.
- `build_<agent>_agent()` separada de `run_<agent>()` para que la UI pueda
  suscribirse a eventos antes de lanzarlo.
- `run_<agent>()` es async, str-in → str-out.
"""

from __future__ import annotations

import asyncio

from agent_framework import Agent

from nexus.config import CONFIG
from nexus.llm import make_chat_client
from nexus.tools.<tool_a> import <tool_a>
from nexus.tools.<tool_b> import <tool_b>


# Instrucciones como string explícito (no f-string con variables volátiles).
# El agente recibirá target/contexto como argumento de entrada, no interpolado
# en las instrucciones — así INSTRUCTIONS es estable y no depende de runtime.
INSTRUCTIONS = (
    "Eres un agente de <rol> para un lab aislado de pentesting personal. "
    "TODO el tráfico va contra un lab Docker en 127.0.0.1.\n\n"
    "Dispones de las siguientes herramientas:\n"
    "- `<tool_a>(target)`: <descripción breve>.\n"
    "- `<tool_b>(target)`: <descripción breve>.\n\n"
    "Flujo recomendado:\n"
    "1. <paso 1>.\n"
    "2. <paso 2>.\n\n"
    "Reglas duras:\n"
    "- NO inventes resultados: cíñete a lo que devuelven las tools.\n"
    "- NO uses tools sobre targets fuera del lab (solo 127.0.0.1 / "
    "juice_shop / webgoat / dvna).\n"
    "- Si una tool falla, reporta el error y continúa con las que puedas."
)


def build_<agent>_agent() -> Agent:
    """Construye el agente sin lanzarlo.

    Útil para suscribirse a eventos antes de `asyncio.run()`.
    """
    client = make_chat_client(
        model=CONFIG.ollama_model,
        host=CONFIG.ollama_host,
    )
    return Agent(
        name="<agent>",
        instructions=INSTRUCTIONS,
        model=client,
        tools=[<tool_a>, <tool_b>],
    )


async def run_<agent>(task: str) -> str:
    """Lanza el agente con la tarea dada y devuelve el resultado.

    Args:
        task: descripción de la tarea (p. ej. "Haz recon de 127.0.0.1").

    Returns:
        Resultado del agente como string (resumen de findings).
    """
    agent = build_<agent>_agent()
    result = await agent.run(task)
    return str(result)


if __name__ == "__main__":
    print(asyncio.run(run_<agent>("Haz recon de 127.0.0.1")))
```

## Consideraciones de num_ctx y streaming

**num_ctx**: el contexto por defecto de Ollama es 2048 tokens, insuficiente para agentes con múltiples rondas de tool calls. Si el agente se queda sin contexto (el modelo empieza a "olvidar" findings anteriores), pasa `num_ctx` como opción:

```python
# Sólo si el agente maneja sesiones largas con muchos tool calls.
# Valor típico para qwen3:8b con historia de findings: 8192.
client = make_chat_client(model=CONFIG.ollama_model)
# num_ctx se pasa como opción al Agent, no a make_chat_client directamente.
```

**Streaming**: el conector soporta streaming, pero para agentes de recon/pentest el modo non-streaming es más sencillo de depurar. Usa streaming sólo si la UI necesita progreso en tiempo real (Task de UI live).

**Stripping de thinking-tags**: algunos modelos emiten `<think>...</think>` antes de la respuesta. Si el agente expone la salida directamente al usuario, filtra esos bloques antes de mostrarlos.

## Do's and Don'ts (con razón)

- DO: usa siempre `make_chat_client` — porque el middleware `StripUnsupportedOllamaOptions` es obligatorio y la factory lo aplica automáticamente.
- DO: escribe INSTRUCTIONS como string explícito (concatenación de strings o triple-quote) — porque las f-strings con variables de runtime hacen las instrucciones impredecibles y difíciles de testear.
- DO: separa `build_<agent>()` de `run_<agent>()` — porque la UI de Task #23 necesita suscribirse a eventos antes de lanzar.
- DO: prueba el agente con `qwen3:8b` local antes de proponer un modelo diferente — porque cambiar el modelo es una decisión arquitectónica (habla con el PM).
- DON'T: NO instancies `OllamaChatClient` directamente — porque el middleware no quedaría registrado y los handoffs reventarían.
- DON'T: NO añadas un modelo nuevo al stack sin pasar por el PM — es un cambio de configuración con impacto en recursos (RAM, velocidad).
- DON'T: NO ignores los guardrails de pentest-safety en las tools que el agente invoca — las tools ya los implementan, pero el agente no debe bypasearlos.

## Definition of Done

- [ ] Agente construido con `make_chat_client(model=CONFIG.ollama_model, host=CONFIG.ollama_host)`.
- [ ] INSTRUCTIONS como string explícito; sin f-string con variables volátiles.
- [ ] Tools vinculadas via parámetro `tools=[...]` del Agent.
- [ ] `build_<agent>_agent()` separada de `run_<agent>()`.
- [ ] Fallback gracioso si el agente no puede completar (captura de excepción → mensaje de error).
- [ ] Verificación `<60s`: `python -m pytest tests/test_<agent>.py -v` (con Ollama mockeado).

## Frontera
**Nunca commit/push/tag.** Añadir un modelo nuevo es decisión del PM (STOP y pregunta). Los guardrails de pentest están en `pentest-safety` (REFERENCIA). El patrón de tools que el agente invoca está en `tool-pattern` (REFERENCIA). Reporta `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED` con la salida de verificación literal.
