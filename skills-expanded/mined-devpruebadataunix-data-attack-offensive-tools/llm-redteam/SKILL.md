---
name: llm-redteam
description: Red teaming de aplicaciones LLM siguiendo OWASP Top 10 for LLM — prompt injection (directa/indirecta), excessive agency, fuga de system prompt y RAG/vector poisoning. Úsala cuando el activo en scope sea un chatbot, asistente, agente con herramientas o pipeline RAG.
---

# Red teaming de aplicaciones con LLM (OWASP LLM Top 10)

Línea de servicio emergente: evaluar la seguridad de aplicaciones que incorporan modelos de
lenguaje. El riesgo NO está en el modelo aislado sino en **cómo la app lo conecta** a datos,
herramientas y usuarios. No necesita infraestructura nueva: es metodología + prueba reproducible.

## Cuándo usarla
Cuando el scope incluya un endpoint de chat/IA, una API de agente, o un buscador/asistente con
recuperación (RAG). La ejecuta el agente `ai-security`.

## Vectores (OWASP LLM)
- **LLM01 Prompt Injection — directa:** anula el system prompt (cambio de rol, "ignora…"),
  ofuscación (otros idiomas, base64, delimitadores, payload splitting).
- **LLM01 Prompt Injection — indirecta:** esconde instrucciones en contenido que el LLM
  ingiere (página web, PDF, documento RAG, correo); se disparan al procesarlo.
- **LLM07 System Prompt Leakage / LLM02 Sensitive Info:** extrae instrucciones, claves o
  datos de otras sesiones/tenants.
- **LLM06 Excessive Agency:** si el LLM usa herramientas (funciones, shell, API), encadena una
  acción no autorizada — inyección de parámetros, tool shadowing, confused deputy.
- **LLM05 Insecure Output Handling:** la salida del LLM llega a un sink sin sanear → XSS (DOM),
  SQLi/RCE (intérprete). Puente a explotación web clásica.
- **LLM08 Vector/Embedding Weaknesses:** envenenamiento del índice RAG, manipulación de la
  recuperación, fuga cruzada entre contextos.

## Cómo probar
- Manualmente vía el endpoint de chat/API (curl/proxy): un payload por vector, registrando
  prompt + respuesta. Itera variando ofuscación.
- Para inyección indirecta: coloca el payload en una fuente que el sistema recupere (si el RoE
  lo permite) y observa el efecto diferido.
- Para excessive agency: mapea las herramientas del agente y busca la que tenga efecto lateral.

## Evidencia y alcance
- **Sin fuente no se explota:** el finding es el intercambio (prompt enviado + respuesta que
  prueba el fallo). Guárdalo como `evidence`/`reproduction` en `contracts/engagement.json`.
- Mapea a `contracts/finding.schema.json` con `owasp: LLMxx`. `status` real solo con prueba.
- No exfiltres datos reales; demuestra con un dato testigo. Acciones con efecto real pasan por
  el gate humano del bot (tiers en `bot/intel/risk.py`).
