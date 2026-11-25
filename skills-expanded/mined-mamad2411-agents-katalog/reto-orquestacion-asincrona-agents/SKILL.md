# Contrato de trabajo para agentes

Este archivo gobierna cualquier agente que modifique este repositorio. El objetivo es producir cambios pequeños, comprensibles y verificables sin atribuir al agente, al autor o a la estructura de carpetas capacidades que la evidencia no demuestra.

## Orden de lectura

1. `README.md`: propósito, ejecución y demostración humana.
2. Este `AGENTS.md`: proceso obligatorio y límites.
3. `docs/changes/README.md`: formato de un paquete de cambio.
4. El paquete activo bajo `docs/changes/<fecha>-<slug>/`.
5. Solo después, los archivos técnicos afectados.

[METODOLOGIA] Carga contexto de forma progresiva. No leas todo `backend/` y `frontend/` si el cambio solo afecta un contrato o componente. Usa `docs/TRACEABILITY.md` para localizar implementación y prueba.

## Flujo obligatorio para cambios

No edites código antes de completar las cuatro primeras fases.

### 1. Validar lo entendido

- Resume el objetivo, el comportamiento esperado y lo que queda fuera.
- Inspecciona primero el estado Git, estas instrucciones y los archivos implicados.
- Distingue hechos observados, inferencias y supuestos.
- Si el pedido es solo diagnóstico o explicación, permanece en lectura.

### 2. Intake

- Crea o actualiza `docs/changes/<fecha>-<slug>/intake.md`.
- Pregunta únicamente por decisiones que cambien materialmente el resultado.
- Si no hay preguntas bloqueantes, registra los supuestos y continúa.
- No inventes requisitos, credenciales, datos personales ni decisiones de negocio.

### 3. Plan

- Registra en `plan.md` archivos previstos, secuencia, riesgos, pruebas y condición de parada.
- Para cambios de comportamiento, publicación, migraciones o acciones destructivas, solicita aprobación explícita antes de ejecutar.
- Una corrección o documentación ya autorizada puede continuar si el alcance está cerrado y es reversible.

### 4. Spec

- Define en `spec.md` el comportamiento observable, invariantes, casos borde, fuera de alcance y criterios de aceptación.
- Si cambia una API o estado persistido, especifica contrato HTTP/SQL y compatibilidad.
- Una spec no es código ni prueba de que el cambio funciona.

### 5. Ejecución

- Implementa el cambio mínimo que satisface la spec.
- Conserva la separación `domain → application → infrastructure → api` en backend.
- Mantén separados snapshot autoritativo, intención y proyección optimista en frontend.
- Comenta el porqué de concurrencia, reconciliación o decisiones no obvias; no describas sintaxis evidente.
- No cambies una prueba solo para obtener verde. Si la prueba era incorrecta, documenta la causa y conserva o refuerza la expectativa funcional.

### 6. Evidencia y cierre

- Registra en `evidence.md` comandos ejecutados, resultados, fallos encontrados y gaps.
- Ejecuta primero la prueba más cercana; después, cuando aplique, `./scripts/verify.sh`.
- No declares éxito por compilación parcial, contenedor levantado o UI visible.
- Antes de publicar: `git diff --check`, revisión de privacidad, estado Git y lectura remota del SHA.

## Comandos de autoridad

```bash
./scripts/new-change.sh nombre-del-cambio
./scripts/check-agentic-workflow.sh
./scripts/verify.sh
./scripts/demo-schedules.sh
```

Docker es la autoridad reproducible. Java, Maven, Node y PostgreSQL locales son opcionales.

## Límites y honestidad

- La estructura de carpetas orienta el contexto; no garantiza razonamiento correcto ni calidad del código.
- Loom facilita I/O bloqueante; PostgreSQL y el `UPDATE` condicional preservan la integridad.
- Este repo demuestra un método asistido para comprender, implementar y validar. No demuestra que su autor pueda reconstruir todo de memoria o programarlo manualmente sin herramientas.
- Si Java 21, Spring o PostgreSQL son nuevos para quien trabaja, explica los conceptos, consulta fuentes primarias cuando sea necesario y valida cada hipótesis con pruebas ejecutables.
- No publiques el PDF original, contenido privado de NotebookLM, rutas locales, secretos ni PII.

[PEDAGOGIA] Ante un fallo, parte del requisito, reproduce la prueba aislada, explica la causa en lenguaje simple y solo después ejecuta el gate completo.

[INFERENCIA] Esta adaptación toma de ICM la separación de contexto y los puntos de revisión humana, pero mantiene el código en sus módulos técnicos para no duplicar ni esconder la fuente real.

[SUPUESTO] `AGENTS.md` es el nombre estándar y versionado solicitado como “agent.md”; no se mantiene un duplicado con nombre singular que pueda divergir.

[NEUROCIENCIA] N/A. No se usan afirmaciones neurocientíficas para justificar el proceso.
