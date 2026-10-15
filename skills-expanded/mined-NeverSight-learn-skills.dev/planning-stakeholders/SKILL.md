---
name: planning-stakeholders
description: "Mapeo de stakeholders, matriz RACI, plan de comunicación y análisis de impacto. Actívala al identificar interesados del proyecto, definir responsabilidades, o cuando el usuario diga 'stakeholders', 'RACI', 'matriz de comunicación', 'análisis de impacto', 'quién decide qué'."
---

# Planning Stakeholders — Mapeo y Comunicación

Identifica quién importa, quién decide, y cómo mantenerlos informados.

---

## Mapa de stakeholders

### Matriz influencia × interés

```
        Alto interés
            │
    ┌───────┴───────┐
    │  Mantener      │  Gestionar
    │  informados    │  de cerca
    │                │
Baja ───────────────────── Alta
influencia          influencia
    │                │
    │  Monitorear    │  Mantener
    │                │  satisfechos
    └───────┬───────┘
            │
        Bajo interés
```

| Stakeholder | Rol | Influencia | Interés | Estrategia |
|------------|-----|-----------|---------|------------|
| Sponsor | Aprueba presupuesto | Alta | Alto | Gestionar de cerca — reporte semanal |
| Usuarios finales | Usan el sistema | Baja | Alto | Mantener informados — demo mensual |
| Equipo de infra | Provee servidores | Alta | Bajo | Mantener satisfechos — avisar con tiempo |
| Soporte | Atiende tickets | Baja | Bajo | Monitorear — informar en release |

---

## Matriz RACI

Para cada entregable o decisión grande:

| Actividad / Decisión | **R**esponsable | **A**prueba | **C**onsultado | **I**nformado |
|---------------------|-----------------|-------------|----------------|---------------|
| Definir alcance MVP | Product Owner | Sponsor | Tech Lead | Equipo |
| Elegir stack técnico | Tech Lead | Product Owner | Equipo | Sponsor |
| Aprobar diseño UI | Diseñador | Product Owner | Usuarios (test) | Tech Lead |
| Deploy a producción | Tech Lead | Product Owner | — | Equipo, Soporte |
| Priorizar bugs | Product Owner | — | Tech Lead, Soporte | Equipo |

**Reglas RACI:**
- Una sola **A** por fila (quien firma).
- La **R** puede ser quien ejecuta, la **A** quien responde.
- Si una fila tiene múltiples **A**, la decisión no tiene dueño claro.

---

## Plan de comunicación

| Qué se comunica | A quién | Frecuencia | Canal | Formato |
|----------------|---------|-----------|-------|---------|
| Avance del sprint | Sponsor, PO | Semanal | Email/Slack | 3 bullets: logros, bloqueos, próximo |
| Cambios de alcance | Sponsor | Cuando ocurran | Reunión 15 min | Qué cambia, por qué, impacto en fecha |
| Release notes | Usuarios, Soporte | Por release | Email/Changelog | Qué cambió, qué arreglaron |
| Riesgos nuevos | Sponsor, PO | Inmediato | Mensaje directo | Riesgo + plan de mitigación |
| Demo de avance | Usuarios (grupo test) | Quincenal | Reunión 30 min | Mostrar, no explicar. Recoger feedback. |

---

## Análisis de impacto

Cuando algo cambia (alcance, fecha, stack), evalúa impacto en 4 dimensiones:

| Dimensión | Pregunta |
|-----------|----------|
| **Alcance** | ¿Agrega/quita funcionalidad? ¿Afecta MVP? |
| **Tiempo** | ¿Atrasa/adelanta milestones? ¿Cuánto? |
| **Costo** | ¿Requiere más recursos? ¿Licencias? |
| **Calidad** | ¿Afecta criterios de aceptación? ¿Métricas no funcionales? |

Para cada cambio, registra en una línea:

```markdown
⚠️ Cambio: Agregar pasarela de pago PayPal
   Alcance: +1 feature (Should have)
   Tiempo: +1 semana (MVP se mueve del 15/jul al 22/jul)
   Costo: $0 (ya tenemos cuenta PayPal business)
   Calidad: Sin impacto
   ✅ Aprobado por: Sponsor (05/jun)
```

---

## Workflow

1. **Recibe contexto del proyecto** (idealmente desde `planning-core`).
2. **Identifica stakeholders** con el usuario: nombres, roles, nivel de involucramiento.
3. **Genera matriz influencia × interés** + **matriz RACI** para las decisiones clave.
4. **Propón plan de comunicación** mínimo.
5. **Entrega todo en un solo documento** estructurado.

---

## Lo que NO debe hacer

- No asumir nombres de stakeholders. Preguntar o dejar placeholders `[nombre]`.
- No generar matrices con 20+ filas. Si el proyecto es chico (< 5 personas), RACI de 5-6 filas.
- No imponer canales (Slack vs Teams vs email). Preguntar qué usan.
