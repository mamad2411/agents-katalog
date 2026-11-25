---
name: sputnik-retro
description: "Retrospectiva de estimación del equipo Sputnik. Compara puntos estimados vs horas reales en Jira, calcula precisión, identifica patrones de sub/sobre-estimación por capa y genera recomendaciones. Úsala al final de cada sprint o cuando el usuario pida 'retrospectiva de estimación', 'comparar estimado vs real', o 'cómo mejorar las estimaciones'."
disable-model-invocation: true
metadata:
  requires-devkits: auto-detect
---

# Sputnik Retro — Estimado vs Real

Compara la estimación de `sputnik-core` contra el tiempo real registrado en Jira. Cierra el ciclo de estimación con datos.

---

## Workflow

### Paso 1: Obtener datos

```bash
# Opción A: desde Jira (preferido)
# Usa search_jira_issues con JQL del sprint cerrado
sprint = "Sprint 12" AND project = SPK

# Opción B: input manual
# El usuario pega la tabla de estimación original + datos reales
```

Para cada issue obtén:

| Dato | Fuente |
|------|--------|
| **Puntos estimados** | `sputnik-core` (tabla original) o campo Story Points en Jira |
| **Horas reales** | `timeoriginalestimate` o `timespent` en Jira (si usan time tracking). Si no hay time tracking, usar `status` (¿se completó en el sprint? ¿hubo re-trabajo?) |
| **Capa** | Label (`sql`, `backend`, `frontend`) o inferir del summary |
| **Tipo de actividad** | Extraer del summary: "Se realiza SP", "Se crea Pantalla", etc. |
| **¿Dividido?** | Issues con `[DIVISION]` en el summary |

### Paso 2: Calcular precisión

```typescript
interface EstimationAccuracy {
  issueKey: string;
  estimatedPoints: number;
  estimatedHours: number;        // puntos * 2 (conversión estándar)
  actualHours: number;           // de Jira time tracking o inferido
  variance: number;              // actualHours - estimatedHours
  accuracy: 'under' | 'accurate' | 'over';
  // accurate: ±25% del estimado
  // under: real > 125% estimado (se subestimó)
  // over: real < 75% estimado (se sobreestimó)
}
```

### Paso 3: Agrupar hallazgos

#### Por capa

| Capa | Issues | Pts Est. | Hrs Est. | Hrs Reales | Precisión |
|------|--------|----------|----------|------------|-----------|
| SQL | 12 | 25 | 50 | 62 | 80% (subestimado 24%) |
| Backend | 8 | 18 | 36 | 30 | 83% (sobreestimado 17%) |
| Frontend | 15 | 28 | 56 | 70 | 80% (subestimado 25%) |

#### Por tipo de actividad

| Tipo | Precisión | Patrón |
|------|-----------|--------|
| `Se realiza SP` | 72% | Subestimado. SPs con transacción requieren 3.5h en vez de 2h por punto. |
| `Se crea Pantalla FrontEnd` | 78% | Subestimado. Pantallas con formulario + tabla consistentemente toman más. |
| `Se crea Consulta BackEnd` | 95% | Muy preciso. GETs simples se estiman bien. |

#### Por patrón de división

```
Tareas divididas [DIVISION]:
  - 60% de las divisiones fueron correctas (cada sub-tarea tomó lo estimado)
  - 25% pudieron ser una sola tarea (las 3 partes tomaron 4h total vs 12h estimadas)
  - 15% necesitaban más división (una sub-tarea de 3pts tomó 12h)
```

### Paso 4: Generar recomendaciones

```
📊 Recomendaciones para el próximo sprint:

1. SQL: Subir SPs con transacción de 2pts → 3pts
   Evidencia: 6/8 SPs con BEGIN TRAN/ROLLBACK tomaron >4h reales.

2. Frontend: Pantallas con ProTable + Drawer de 2pts → 3pts
   Evidencia: 4/5 pantallas con formulario lateral tomaron >6h.

3. Backend: GETs sin lógica se mantienen en 1pt ✅
   Evidencia: 10/10 endpoints GET simples dentro del estimado.

4. División: No dividir tareas de <2pts
   Evidencia: 3 tareas de 1pt divididas en 3 partes resultaron en over-engineering.
```

### Paso 5: Actualizar criterios de `sputnik-core`

Si el usuario confirma, actualiza los criterios de estimación en `sputnik-core`:

```
- SPs con transacción: ahora 3pts (antes 2pts)
- Pantallas con formulario + tabla: ahora 3pts (antes 2pts)
- No dividir tareas de 1pt
```

### Paso 6: Reporte final

Genera un markdown con:

1. **Resumen ejecutivo**: % de precisión global, tendencia vs sprint anterior
2. **Tabla por capa**: estimado vs real con % precisión
3. **Top 5 subestimaciones**: issues que más se desviaron (horas)
4. **Top 5 sobreestimaciones**: issues donde se "regalaron" horas
5. **Recomendaciones**: ajustes concretos para `sputnik-core`
6. **Gráfico de tendencia** (ASCII): precisión por sprint

```
Precisión por sprint:
  Sprint 10  ████████░░  82%
  Sprint 11  █████████░  88%
  Sprint 12  ██████████  91%  ← mejorando
```

---

## Lo que NO debe hacer

- No asumir horas reales si Jira no tiene time tracking. Preguntar al usuario o usar señales proxy (comentarios, commits, re-aperturas).
- No cambiar los criterios de `sputnik-core` sin confirmación del usuario.
- No comparar contra otros equipos (esta skill es para mejorar al equipo Sputnik, no para rankings).
