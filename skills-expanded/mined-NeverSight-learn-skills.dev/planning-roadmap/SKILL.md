---
name: planning-roadmap
description: "Roadmap, milestones, cronograma y plan de entregables. Cubre timeline por fases, dependencias entre equipos/sistemas, y delivery plan progresivo. Actívala al definir fechas, planear releases, o cuando el usuario diga 'roadmap', 'milestones', 'cronograma', 'entregables', 'fases del proyecto', 'Gantt'."
---

# Planning Roadmap — Timeline y Entregables

De charter a fechas. Sin MS Project, sin Gantt de 200 líneas.

---

## Estructura del roadmap

```markdown
# Roadmap — [Proyecto]

## 🎯 Visión general
[1 frase. A dónde vamos.]

---

## Fase 0 — Setup (Semanas 1-2)
**Objetivo:** Todo listo para empezar a construir.
- [ ] Stack definido y aprobado
- [ ] Repositorios creados, CI/CD corriendo
- [ ] Ambientes: dev, staging
- [ ] Accesos: DB, cloud, APIs externas
- [ ] Spec técnica del MVP (`productivity-spec`)

## Fase 1 — Core MVP (Semanas 3-6)
**Objetivo:** El flujo principal funciona de punta a punta.
- [ ] Registro/login de usuarios
- [ ] Creación de orden (flujo feliz)
- [ ] Visualización de estado de orden
- [ ] **Demo al sponsor:** Semana 6

## Fase 2 — Completar MVP (Semanas 7-10)
**Objetivo:** Funcionalidad completa del MVP.
- [ ] Pagos integrados (Stripe/MercadoPago)
- [ ] Notificaciones por email
- [ ] Panel de administración básico
- [ ] **Release MVP:** Semana 10

## Fase 3 — Post-MVP (Semanas 11+)
**Objetivo:** Features Should/Could have.
- [ ] Dashboard de analytics
- [ ] Exportación a Excel/PDF
- [ ] App móvil (PWA o nativa)
- [ ] **Release v1.1:** Semana 14
```

---

## Dependencias entre equipos/sistemas

Para proyectos con múltiples equipos o integraciones:

```markdown
## Dependencias

| Entrega | Equipo responsable | Equipo dependiente | Fecha necesaria | Estado |
|---------|-------------------|-------------------|-----------------|--------|
| API de autenticación v1 | Backend | Frontend, Móvil | Semana 2 | ✅ Listo |
| Sandbox de pagos | Stripe (externo) | Backend | Semana 3 | ⬜ Pendiente |
| Diseño final de UI | Diseño | Frontend | Semana 4 | 🔄 En progreso |
| Endpoint de reportes | Backend | Frontend | Semana 8 | ⬜ Pendiente |
```

---

## Timeline visual (Mermaid Gantt)

```mermaid
gantt
    title Roadmap — MiApp
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m

    section Fase 0 — Setup
    Stack y repos     :done, setup1, 2026-07-01, 3d
    CI/CD y ambientes :done, setup2, after setup1, 4d
    Spec técnica      :active, setup3, after setup2, 3d

    section Fase 1 — Core MVP
    Auth (Backend)    :f1be, 2026-07-14, 5d
    Auth (Frontend)   :f1fe, after f1be, 5d
    Órdenes (Backend) :f2be, 2026-07-14, 10d
    Órdenes (Frontend):f2fe, after f1fe, 7d
    Demo sponsor      :milestone, 2026-08-11, 0d

    section Fase 2 — Completar MVP
    Pagos             :2026-08-12, 8d
    Notificaciones    :2026-08-20, 5d
    Admin panel       :2026-08-12, 10d
    Release MVP       :milestone, 2026-08-25, 0d
```

---

## Indicadores de salud del cronograma

Revisa cada semana:

| Indicador | Verde | Amarillo | Rojo |
|-----------|-------|----------|------|
| **Completado vs planeado** | ≥90% | 70-89% | <70% |
| **Bloqueantes abiertos** | 0 | 1-2 | ≥3 |
| **Dependencias externas en riesgo** | 0 | 1 | ≥2 |
| **Horas extra del equipo** | 0 | <10% | ≥10% |

Regla: si 2+ indicadores están en rojo, escala al sponsor.

---

## Estrategia de entregas progresivas

En lugar de un gran release al final:

| Entrega | Qué incluye | A quién | Cuándo |
|---------|------------|---------|--------|
| **Alpha** (interno) | Flujo core, con bugs conocidos | Equipo + sponsor | Semana 4 |
| **Beta** (testers) | MVP completo, pulido | Grupo de usuarios piloto | Semana 8 |
| **GA** (general) | MVP + fixes del beta | Todos los usuarios | Semana 10 |

---

## Workflow

1. **Recibe el charter** (`planning-core`) o el scope definido.
2. **Pregunta fecha objetivo** (si hay deadline dura) y tamaño del equipo.
3. **Divide en fases de 2-4 semanas** (no más largas, pierden significado).
4. **Genera Gantt en Mermaid** — lo suficiente para visualizar paralelismos.
5. **Identifica dependencias externas** con otros equipos/sistemas.
6. **Marca milestones de demo/release** para mantener ritmo.

---

## Lo que NO debe hacer

- No planear con precisión de días para fases > 1 mes. A más lejos, menos detalle.
- No asumir velocidad del equipo. Usar rangos: "Semanas 3-6" no "5/jul — 18/jul".
- No generar 50 tareas. El roadmap es hitos y fases, no tareas. Las tareas van en `sputnik-core` o en el board del sprint.
