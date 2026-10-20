---
name: planning-risk
description: "Identificación y mitigación de riesgos: matriz probabilidad × impacto, riesgos técnicos/de negocio/externos y plan de mitigación. Úsala con 'riesgos del proyecto', 'risk matrix', 'mitigación' o 'qué puede salir mal'."
disable-model-invocation: true
---

# Planning Risk — Identificación y Mitigación

Si no identificaste qué puede salir mal, ya salió mal.

---

## Tipos de riesgo

| Tipo | Ejemplos |
|------|----------|
| **Técnico** | Stack nuevo para el equipo, integración con API sin documentación, deuda técnica del sistema legacy, performance con carga real |
| **Negocio** | Cambio de prioridades del sponsor, falta de adopción por usuarios, regulación nueva |
| **Externo** | Dependencia de proveedor (API se cae), rotación de personal clave, fecha límite impuesta sin consulta |
| **Organizacional** | Equipo sin experiencia en el dominio, dependencia entre equipos, falta de entornos (staging, QA) |

---

## Matriz probabilidad × impacto

```
Probabilidad
    Alta  │ 🟡 Medio      🔴 Crítico    🔴 Crítico
          │
  Media   │ 🟢 Bajo       🟡 Medio      🔴 Crítico
          │
   Baja   │ ⚪ Trivial    🟢 Bajo       🟡 Medio
          │
          └────────────────────────────────────
            Bajo          Medio          Alto
                        Impacto
```

### Criterios

| Probabilidad | Significado |
|-------------|------------|
| Alta (>60%) | Ya pasó en proyectos similares, o hay señales tempranas |
| Media (20-60%) | Puede pasar, hay factores de riesgo presentes |
| Baja (<20%) | Poco probable pero posible |

| Impacto | Significado |
|---------|------------|
| Alto | Atrasa el proyecto >30% o bloquea el lanzamiento |
| Medio | Atrasa 1-2 semanas o reduce alcance significativamente |
| Bajo | Atrasa <1 semana o afecta un nice-to-have |

---

## Tabla de riesgos

| # | Riesgo | Tipo | Probabilidad | Impacto | Nivel | Mitigación | Contingencia |
|---|--------|------|-------------|---------|-------|-----------|-------------|
| 1 | API del banco sin sandbox para testear | Técnico | Alta | Alto | 🔴 Crítico | Pedir acceso anticipado, pedir credentials semana 1 | Mock de la API con MSW para desarrollar mientras |
| 2 | Sponssor cambia prioridad a mitad del sprint | Negocio | Media | Alto | 🔴 Crítico | Sprint de 1 semana (no 2), demo frecuente | Buffer de 20% en el roadmap para absorber cambios |
| 3 | Dev clave se va de vacaciones 2 semanas | Organizacional | Alta | Medio | 🟡 Medio | Documentar decisiones en ADR, pair programming previo | Backup asignado, alcance reducido esa quincena |
| 4 | El ORM no soporta la feature de SQL que necesitamos | Técnico | Baja | Medio | 🟡 Medio | Probar con un spike técnico en semana 1 | Raw SQL como escape hatch |
| 5 | Usuarios no adoptan la nueva UI | Negocio | Media | Medio | 🟡 Medio | User testing temprano con prototipo clickeable | Rollback a UI anterior, iterar con feedback |

---

## Plan de respuesta

Cada riesgo 🔴 Crítico debe tener:

```markdown
### Riesgo: [título]
- **Dueño:** [quién monitorea este riesgo]
- **Disparador:** [señal que indica que el riesgo se materializó]
- **Mitigación:** [qué hacemos AHORA para reducir probabilidad o impacto]
- **Contingencia:** [qué hacemos SI OCURRE]
- **Revisión:** [frecuencia con que se reevalúa — ej: cada sprint planning]
```

---

## Registro de riesgos materializados

Documenta los riesgos que se volvieron realidad. Sirve para la retro y para no repetirlos.

```markdown
## Riesgos materializados este sprint
| Riesgo | Impacto real | Lección aprendida |
|--------|-------------|-------------------|
| API del banco sin sandbox | Atrasó 3 días el módulo de pagos | Para integraciones externas, spike antes de estimar |
```

---

## Workflow

1. **Recibe el charter** o contexto del proyecto (desde `planning-core` o directo del usuario).
2. **Brainstorming guiado** — haz 3-5 preguntas para descubrir riesgos:
   - ¿Qué parte del stack es nueva para el equipo?
   - ¿Hay dependencias externas? (APIs, proveedores, otros equipos)
   - ¿Hay fecha límite dura? (regulatorio, evento, contrato)
   - ¿Alguien clave se va de vacaciones o tiene sobrecarga?
   - ¿Qué pasó en el proyecto anterior que no queremos repetir?
3. **Genera la tabla de riesgos** con las 5 columnas.
4. **Para cada riesgo 🔴, escribe plan de respuesta** completo.
5. **Pregunta:** ¿Hay riesgos que no consideré?

---

## Lo que NO debe hacer

- No listar más de 10 riesgos. Si hay más, prioriza top 10.
- No incluir riesgos genéricos inútiles ("el proyecto podría atrasarse").
- No alarmar sin mitigación. Todo riesgo lleva acción.
- No olvidar riesgos de negocio/externos. No todo es técnico.
