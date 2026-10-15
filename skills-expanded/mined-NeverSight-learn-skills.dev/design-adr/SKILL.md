---
name: design-adr
description: "Architecture Decision Records: formato ligero para documentar decisiones técnicas con contexto, alternativas consideradas y consecuencias. Actívala al tomar una decisión arquitectónica importante, o cuando el usuario diga 'ADR', 'decision record', 'por qué elegimos X', 'documentar decisión', 'arquitecture decision'."
---

# Design ADR — Architecture Decision Records

Las decisiones importantes merecen un párrafo, no un chat de Slack que nadie encontrará después.

---

## Formato ADR (ligero)

```markdown
# ADR-{NNNN}: {Título breve}

**Fecha:** {YYYY-MM-DD}
**Estado:** {Propuesto / Aceptado / Reemplazado por ADR-{NNNN} / Obsoleto}
**Decisores:** {nombres}

---

## Contexto

{Qué problema estamos resolviendo. Por qué hay que decidir ahora. Qué restricciones existen. 2-3 párrafos.}

---

## Decisión

{Elección concreta. Qué vamos a hacer. Una frase clara.}

> Ej: "Usaremos PostgreSQL como base de datos principal, con Redis para caché de sesiones."

---

## Consecuencias

### ✅ Positivo
- {Beneficio 1}
- {Beneficio 2}

### ❌ Negativo
- {Costo/riesgo 1}
- {Costo/riesgo 2}

---

## Alternativas consideradas

| Alternativa | Pros | Contras | Por qué se descartó |
|-------------|------|---------|-------------------|
| {Opción A} | ... | ... | ... |
| {Opción B} | ... | ... | ... |
```

---

## Cuándo escribir un ADR

Escribe ADR cuando la decisión:

- **Afecta la estructura del sistema** (elección de BD, ORM, framework, arquitectura)
- **Es costosa de revertir** (migrar de PostgreSQL a MongoDB no es trivial)
- **Tiene implicaciones cross-team** (el frontend y backend se acoplan a un contrato)
- **Va contra la intuición** ("usaremos SQLite en producción para este microservicio")
- **Alguien preguntará "por qué" en 6 meses**

No escribas ADR para:

- Qué versión de un paquete usar (eso es `package.json`)
- Dónde poner un archivo (eso es convención del proyecto)
- Decisiones triviales que no afectan arquitectura

---

## Ciclo de vida

```
Propuesto → Aceptado → (Reemplazado | Obsoleto)
```

- **Propuesto**: la decisión está en discusión. Puede haber varios ADR compitiendo.
- **Aceptado**: se aprobó y está vigente. Lo que el código refleja hoy.
- **Reemplazado por ADR-N**: una nueva decisión la dejó sin efecto. El ADR viejo queda como historia.
- **Obsoleto**: la decisión ya no aplica (ej: se migró de ese componente, el sistema cambió).

---

## Dónde guardarlos

```
docs/adr/
├── README.md          ← Índice de todos los ADR con status
├── 0001-usar-postgresql.md
├── 0002-jwt-auth.md
├── 0003-react-vite-antd.md
└── template.md
```

Índice (`README.md`):

```markdown
# Architecture Decision Records

| # | Título | Fecha | Estado |
|---|--------|------|--------|
| 0001 | Usar PostgreSQL como BD principal | 2026-06-01 | ✅ Aceptado |
| 0002 | JWT con refresh token para auth | 2026-06-03 | ✅ Aceptado |
| 0003 | React + Vite + Ant Design para frontend | 2026-06-05 | ✅ Aceptado |
| 0004 | Microservicios para el módulo de pagos | 2026-06-20 | ❌ Rechazado → ver ADR-0005 |
| 0005 | Pagos como módulo interno del monolito | 2026-06-21 | ✅ Aceptado |
```

---

## Workflow

1. **Identifica que se necesita un ADR** (por el contexto de la conversación o porque el usuario lo pide).
2. **Haz 2-3 preguntas clave** para llenar el contexto:
   - ¿Qué problema concreto estamos resolviendo?
   - ¿Hay restricciones? (costo, tiempo, experiencia del equipo, infraestructura)
   - ¿Qué alternativas se consideraron?
3. **Genera el ADR** con el formato estándar, incluyendo al menos 2 alternativas descartadas.
4. **Guarda el archivo** en `docs/adr/{NNNN}-{slug}.md`.
5. **Actualiza el índice** `docs/adr/README.md`.

---

## Lo que NO debe hacer

- No generar ADR sin preguntar primero qué alternativas consideró el equipo.
- No usar numeración autoincremental si ya existen ADR. Detectar el último número + 1.
- No escribir ADR de más de 1 página. Si necesita más, probablemente es un design doc, no un ADR.
- No forzar ADR para decisiones triviales.
