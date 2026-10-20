---
name: tool-pattern
description: Use when añades o mantienes una tool de pentest en Nexus (src/nexus/tools/<tool>/{__init__.py,core.py,tool.py,rules.py} + tests/test_<tool>.py) — aplica el patrón canónico con lógica pura en core.py, wrapper @tool en tool.py normalizando a Finding + persist vía storage/repo.save_many, reglas deterministas en rules.py, timeouts httpx, errores graciosos, y guardrails pentest-safety (allowlist + HITL).
---

# Skill: Tool Pattern

> Plantilla canónica para una tool de pentest en Nexus. Un módulo aislado por herramienta. Cada tool es robusta, no rompe el agente, y respeta los guardrails de pentest-safety.

Contrato de error: las tools **nunca lanzan hacia arriba**. Devuelven findings o una lista vacía graciosa. El agente reportero lee de la DB de findings, no del resultado en memoria.

## Cuándo usar esta skill

- Añades una nueva tool en `src/nexus/tools/<tool>/`.
- Mantienes/arreglas una tool existente (timeout, fallback, reglas de severidad).
- Revisas que una tool cumple el patrón antes de pasársela al agente.

## GUARDRAIL CRÍTICO — pentest-safety antes de código

**Añadir una tool que no valide la allowlist es una violación de pentest-safety (STOP).** Antes de escribir la tool:

1. Confirma que el target se validará contra la allowlist del lab.
2. Determina si la acción es de lectura (recon/enumeración) o intrusiva (explotación, actuación).
3. Si es intrusiva: la tool debe usar `approval_mode="always_require"` y el agente emite PLAN antes de ejecutar.
4. Documenta el nivel de intrusión en el docstring de `core.py` y en el ADR (`plans/DECISIONS.md`).

Si no puedes verificar el scope -> DETENTE y reporta al PM. No implementes a ciegas.

## Estructura de ficheros

```
src/nexus/tools/<tool>/
    __init__.py    # re-export del @tool para que el agente lo importe limpio
    core.py        # lógica pura: target → list[Finding]; sin IO de DB ni LLM
    tool.py        # wrapper @tool: valida allowlist, llama a core, persiste, serializa
    rules.py       # reglas deterministas de severidad; sólo dicts + regex, sin IO
tests/
    test_<tool>.py # tests unitarios: core + rules en aislamiento; tool con mocks
```

Sigue el patrón existente de `src/nexus/tools/http_probe/` como referencia canónica.

## Patrón canónico

### core.py — lógica pura

```python
"""Lógica pura de <tool>: <descripción de entrada/salida>.

Decisiones de diseño:
- Sin side-effects de IO de red más allá de la propia probe.
- httpx timeout explícito: nunca bloquear indefinidamente.
- Errores de red → finding informativo, no excepción.
- verify=False sólo para targets del lab con certs self-signed.
"""

from __future__ import annotations

import httpx

from nexus.models.finding import Finding
from nexus.tools.<tool>.rules import (
    check_<rule_a>,
    check_<rule_b>,
)

DEFAULT_TIMEOUT = 10.0  # segundos; igual que http_probe


def probe(target: str, *, timeout: float = DEFAULT_TIMEOUT) -> list[Finding]:
    """Ejecuta <tool> contra el target y devuelve findings.

    Args:
        target: host:puerto o URL del target del lab.
        timeout: timeout total en segundos.

    Returns:
        list[Finding]. Nunca lanza — devuelve finding de error si falla.
    """
    try:
        # ... lógica de la probe ...
        findings: list[Finding] = []
        findings.extend(check_<rule_a>(target, ...))
        findings.extend(check_<rule_b>(target, ...))
        return findings
    except Exception as ex:
        return [
            Finding(
                tool="<tool>",
                category="<categoria>",
                severity="info",
                title=f"Error ejecutando <tool> contra {target}",
                description=f"No se pudo completar la probe: {ex}.",
                target=target,
                evidence=f"{type(ex).__name__}: {ex}",
            )
        ]
```

### tool.py — wrapper @tool

```python
"""Wrapper @tool de <tool> para Agent Framework.

El LLM ve <tool>(target: str) -> str. Internamente:
- Valida allowlist (pentest-safety).
- Llama a core.probe(target) → list[Finding].
- Persiste en la DB (best effort).
- Serializa a JSON con resumen por severidad.
"""

from __future__ import annotations

import json
from collections import Counter

from agent_framework import tool

from nexus.models.finding import Finding
from nexus.storage import make_engine, save_many
from nexus.tools.<tool>.core import probe

# Allowlist del lab (pentest-safety regla 1).
_LAB_ALLOWLIST = {
    "127.0.0.1",
    "localhost",
    "juice_shop",
    "dvwa",
    "webgoat",
    "dvna",
}


def _target_allowed(target: str) -> bool:
    """Devuelve True si el target está en la allowlist del lab."""
    host = target.split(":")[0].split("/")[-1].lower()
    return host in _LAB_ALLOWLIST


def _count_by_severity(findings: list[Finding]) -> dict[str, int]:
    return dict(Counter(f.severity for f in findings))


# approval_mode="never_require" para recon; "always_require" para exploits.
@tool(approval_mode="never_require")
def <tool>(target: str) -> str:
    """<Descripción para el LLM>.

    USO SÓLO EN LAB AISLADO. Valida allowlist antes de ejecutar.

    Args:
        target: host:puerto o URL del target (p. ej. "127.0.0.1:3000").

    Returns:
        JSON con: {"target": "...", "count": N, "by_severity": {...}, "findings": [...]}
    """
    # Guardrail pentest-safety: bloquear targets fuera del lab.
    if not _target_allowed(target):
        return json.dumps({
            "error": "TARGET_NOT_ALLOWED",
            "message": (
                f"El target '{target}' no está en la allowlist del lab. "
                "Sólo se permiten targets de test: 127.0.0.1, localhost, "
                "juice_shop, dvwa, webgoat, dvna."
            ),
        }, ensure_ascii=False)

    findings = probe(target)

    persist_error: str | None = None
    if findings:
        try:
            engine = make_engine()
            save_many(engine, findings)
        except Exception as ex:  # noqa: BLE001
            persist_error = f"{type(ex).__name__}: {ex}"

    payload: dict = {
        "target": target,
        "count": len(findings),
        "by_severity": _count_by_severity(findings),
        "findings": [f.to_dict() for f in findings],
    }
    if persist_error:
        payload["persist_error"] = persist_error
    return json.dumps(payload, ensure_ascii=False)
```

### rules.py — reglas deterministas

```python
"""Reglas deterministas para <tool>.

Ninguna regla consulta el LLM ni la DB. Sólo inputs estructurados + regex.
Severidades: critical | high | medium | low | info.
"""

from __future__ import annotations

import re

from nexus.models.finding import Finding


def check_<rule>(target: str, data: dict) -> list[Finding]:
    """Detecta <condición> y asigna severidad determinista.

    Lógica de severidad:
        - critical: <cuándo>
        - high:     <cuándo>
        - medium:   <cuándo>
        - low:      <cuándo>
        - info:     <cuándo>
    """
    findings: list[Finding] = []
    # ... lógica ...
    return findings
```

### Reglas del patrón (Do / Don't con razón)

- DO: `httpx timeout=DEFAULT_TIMEOUT` en toda request — porque un target lento no puede bloquear al agente indefinidamente.
- DO: validar allowlist en `tool.py` antes de llamar a `core.py` — porque la validación debe ser lo primero que ejecuta el wrapper, antes de cualquier IO.
- DO: devolver finding de error gracioso en `core.py` ante cualquier fallo — porque el agente debe seguir ejecutando otras tools aunque una falle.
- DO: `approval_mode="always_require"` para acciones intrusivas (exploits, actuadores) — porque pentest-safety exige HITL antes de ejecutar.
- DO: persistir findings vía `storage/repo.save_many` (best effort, con captura de error) — porque el agente reportero lee de la DB.
- DON'T: NO lances excepciones hacia arriba desde `core.py` — porque tumbaría el ciclo del agente.
- DON'T: NO pongas lógica de severidad en `core.py` — vive en `rules.py` para que sea testeable de forma aislada.
- DON'T: NO consultes el LLM ni la DB desde `core.py` ni `rules.py` — son capas de lógica pura.

## Checklist de Definition of Done

- [ ] Allowlist validada en `tool.py` antes de cualquier IO.
- [ ] `approval_mode` correcto: `"never_require"` para recon, `"always_require"` para exploits.
- [ ] `core.py` con timeout explícito y error gracioso (nunca lanza).
- [ ] `rules.py` con lógica determinista de severidad (sólo dicts + regex).
- [ ] Findings persistidos vía `storage/repo.save_many` (best effort).
- [ ] `__init__.py` re-exporta la función `@tool` para import limpio en el agente.
- [ ] `tests/test_<tool>.py` cubre: core con mock HTTP, rules en aislamiento, tool con allowlist bloqueada.
- [ ] Verificación `<60s`: `python -m pytest tests/test_<tool>.py -v`.

## Frontera
**Nunca hagas commit, push ni tag.** Haces el trabajo, lo verificas y lo reportas; sólo el PM integra. Si no llegas a un estado que pasa la verificación en 2 intentos -> reporta `BLOCKED`. La disciplina de TDD está en `superpowers:test-driven-development` (REFERENCIA). Los guardrails de seguridad están en `pentest-safety` (REFERENCIA).
