---
name: planning-core
description: "Guía principal de planeación de software: project charter, alcance, MVP slicing (MoSCoW), ágil liviano y estimación de alto nivel. Incluye el modo compacto de 1 página. Úsala al iniciar proyecto, planear sprint 0 o 'project charter'."
---

# Planning Core — Planeación de Proyecto

Guía de planeación esencial. Cubre lo mínimo para arrancar un proyecto con claridad, sin burocracia innecesaria. Basado en principios ágiles + sentido común.

---

## Project Charter (1-pager)

Todo proyecto debe caber en una hoja. Si no, no está claro.

Nota: las mini-secciones de Stakeholders, Hitos y Riesgos de abajo son un resumen de una página; para el detalle completo (matriz RACI, roadmap por fases, matriz de riesgos), cargar también `planning-stakeholders`, `planning-roadmap` y `planning-risk` respectivamente.

```markdown
# [Nombre del Proyecto]

## 🎯 Objetivo
[Una frase. Qué problema resuelve, para quién.]

## 📦 Alcance (MVP)
- [Funcionalidad 1]
- [Funcionalidad 2]
- [Funcionalidad 3]

## 🚫 Fuera de alcance (explícito)
- [Lo que NO se hará en esta fase]

## 👥 Stakeholders clave
| Rol | Persona/Equipo | Interés |
|-----|---------------|---------|
| Sponsor | [nombre] | Aprueba presupuesto |
| Product Owner | [nombre] | Define prioridades |
| Tech Lead | [nombre] | Decisiones técnicas |

## 📅 Hitos principales
| Hito | Fecha | Entregable |
|------|-------|-----------|
| Kickoff | [fecha] | Charter aprobado |
| MVP | [fecha] | Funcionalidad core en staging |
| Release | [fecha] | En producción |

## ⚠️ Riesgos top 3
1. [Riesgo] — Mitigación: [acción]
2. [Riesgo] — Mitigación: [acción]
3. [Riesgo] — Mitigación: [acción]

## 💰 Recursos
- Equipo: [N devs] + [N diseño/QA]
- Presupuesto: [$ o horas]
- Infraestructura: [cloud/on-premise]
```

---

## Alcance y MVP slicing

### MoSCoW prioritization

| Categoría | Significado | % del esfuerzo |
|-----------|------------|----------------|
| **Must have** | Sin esto no hay producto | ~60% |
| **Should have** | Importante, no crítico | ~20% |
| **Could have** | Nice to have, si sobra tiempo | ~15% |
| **Won't have** (ahora) | Explícitamente fuera de esta fase | ~5% (documentar) |

### Cómo cortar MVP

1. **Define el problema core.** ¿Qué hace el usuario hoy que duele? Resuelve solo eso.
2. **Un usuario, un flujo.** MVP = un tipo de usuario hace una cosa de punta a punta.
3. **Corta features, no calidad.** Un feature menos, no un feature a medias.
4. **Pregunta "¿qué pasa si NO lo hacemos?"** Si la respuesta es "nada crítico", fuera del MVP.

```markdown
## MVP Scope
✅ Usuario se registra con email
✅ Crea una orden básica (1 producto, sin variantes)
✅ Ve estado de su orden
❌ Dashboard de analytics
❌ Multi-moneda
❌ App móvil
```

---

## Metodología ágil liviana

### Ceremonies mínimas que sí sirven

| Ceremonia | Frecuencia | Duración | Propósito real |
|-----------|-----------|----------|---------------|
| **Daily** | Diario | 10 min | ¿Bloqueos? No reporte de status. |
| **Sprint Planning** | Cada 1-2 semanas | 30-60 min | ¿Qué cabe en este sprint? |
| **Sprint Review** | Fin de sprint | 20-30 min | Demo de lo construido. |
| **Retro** | Fin de sprint | 20-30 min | ¿Qué mejorar como equipo? |

Lo que NO necesitas en un equipo < 6 personas: refinement separado (va en planning), daily de 30 min, grooming multi-hora.

### User stories efectivas

```
Como [tipo de usuario],
quiero [acción],
para [beneficio].

Criterios de aceptación:
- [ ] Dado [contexto], cuando [acción], entonces [resultado]
- [ ] Dado [contexto], cuando [acción], entonces [resultado]
```

---

## Estimación de alto nivel

Antes de entrar a detalle (que cubre `sputnik-core`), haz un sizing rápido:

| Tamaño | Significado | Rango |
|--------|------------|-------|
| **S** | 1-3 días | Tarea simple, bien entendida |
| **M** | 1-2 semanas | Feature con algunas incógnitas |
| **L** | 2-4 semanas | Módulo completo, varias integraciones |
| **XL** | > 1 mes | Demasiado grande → dividir |

Regla: si todo es M o L, el proyecto está bien dimensionado. Si hay XL, partir. Si todo es S, probablemente hay detalle innecesario.

---

## Roles (equipo pequeño, < 8 personas)

| Rol | Responsabilidad | ¿Quién lo hace típicamente? |
|-----|----------------|----------------------------|
| Product Owner | Qué se construye y en qué orden | Cliente o stakeholder designado |
| Tech Lead | Cómo se construye, estándares técnicos | Dev más senior |
| Delivery Lead | Que el equipo no se atasque, facilitación | Puede ser el mismo Tech Lead |
| Team | Construir, testear, deployar | Desarrolladores |

En equipos de 2-4 personas, no multipliques roles. Una persona puede ser PO + Tech Lead.

---

## Workflow de la skill

1. **Recibe la necesidad** del usuario ("planear proyecto X", "definir MVP de Y").
2. **Haz preguntas mínimas para llenar el charter** — en un solo mensaje si es posible:
   - ¿Cuál es el problema que resuelve?
   - ¿Quién es el usuario final?
   - ¿Hay fecha límite o presupuesto?
   - ¿Stack definido o por definir?
3. **Genera el charter 1-pager** con las 7 secciones.
4. **Identifica gaps y suposiciones** y preséntalos breve (sin iterar como `productivity-spec`, solo listar).
5. **Entrega el charter** y pregunta si se necesita detalle en stakeholders, riesgos o roadmap → derivar a sub-skills.

---

## Lo que NO debe hacer

- No generar documentación extensa. Un charter es 1 página.
- No asumir metodología rígida (Scrum completo, SAFe). Por defecto, ágil liviano.
- No estimar en horas/hombre detallado. Eso va en `sputnik-core`.
- No diseñar arquitectura. Eso va en `design-core`.
- No reemplazar al PO. Las decisiones de alcance las valida el usuario.

---

## Modo compacto (charter de 1 página, para agentes)

Cuando el usuario pida "plan this", "project charter", "MVP scope" o el consumidor sea un agente, genera el charter en una pasada, **máximo 1 página, tablas sin prosa**:

```
# Project Charter: [Nombre]

## Objective
[Una frase: problema + usuario.]

## MVP Scope (Must)
- [Feature]

## Out of Scope (Won't — explícito)
- [Exclusión]

## Actors
| Actor | Device | Access |

## Modules
| Module | Responsibility | Priority | Phase |

## Roadmap
| Phase | Duration | Features | Depends On |

## Top Risks
| Risk | Type | Probability | Impact | Mitigation |

## Stack (inferido/sugerido)
| Layer | Tech | Why |

## Key Decisions (ADR candidates)
| Decision | Options | Choice | Rationale |

## Undefined
- [ ] [Gap que requiere decisión]
```

Reglas: preguntar máximo 2 cosas en un solo mensaje; IDs `ORD-01`; prioridad `P0|P1|P2`; duraciones en semanas; sin teoría de metodología, sin roles, sin presupuesto salvo petición explícita.
