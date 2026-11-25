---
name: code-complexity-metrics
description: Métricas de complejidad como señal para dirigir el esfuerzo — complejidad ciclomática y cognitiva, longitud de función/archivo/parámetros, profundidad de anidamiento, acoplamiento y cohesión, con umbrales que marcan dónde mirar (no dogmas) y foco en la tendencia por encima del valor absoluto. Usar al elegir qué refactorizar primero, al configurar reglas de complejidad en el linter, al revisar un archivo que "da miedo tocar", o al justificar con datos por qué un módulo necesita trabajo.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Métricas de complejidad — un termómetro, no un juez

Las métricas no dicen "este código es malo": dicen "acá hay riesgo, mirá". Sirven para
**priorizar** el trabajo de `clean-code`, `solid-principles` y `refactoring-safely`, no
para reemplazar el criterio. Un número alto es una pregunta, no una sentencia.

## 1. Las métricas que importan

| Métrica | Qué mide | Señal de alerta (ajustá en el CLAUDE.md) |
|---|---|---|
| Ciclomática | nº de caminos independientes (ifs, loops, `&&`, `case`) | ~10+ por función |
| Cognitiva (Sonar) | qué tan difícil es de *entender* para un humano | ~15+ por función |
| Longitud de función | líneas | ~40+ |
| Parámetros | nº de argumentos | 4+ (ver `clean-code`) |
| Anidamiento | profundidad de bloques | 3+ niveles |
| Acoplamiento (fan-in/out) | de cuántos módulos depende / cuántos dependen de él | outlier del repo |

Ciclomática vs cognitiva: una cadena `switch` plana tiene ciclomática alta pero es
fácil de leer (cognitiva baja); tres `if` anidados con `&&` tienen cognitiva alta aunque
la ciclomática no explote. Para decidir "¿esto se entiende?", pesa más la cognitiva.

## 2. Umbral = señal, no límite duro

```ts
// eslint.config.mjs → marca funciones para revisar, no rompe el build por 1 de más
rules: { 'complexity': ['warn', 10] }
```

- El umbral dispara una **revisión**, no un rechazo automático. Una función con
  ciclomática 12 que es un `switch` exhaustivo y claro puede quedarse (con `disable`
  justificado, ver `static-analysis-linting`).
- No conviertas la métrica en objetivo: si premiás "ciclomática baja", la gente parte
  funciones en pedazos sin sentido para engañar al número (ley de Goodhart).

## 3. La tendencia manda sobre el valor absoluto

Un repo heredado con complejidad alta no se arregla de un día para otro. Lo que se
gobierna es la **dirección**:

- ¿La complejidad del módulo sube o baja con cada PR? (ver trinquete en `code-quality-gates`).
- ¿El código nuevo entra por debajo del umbral aunque el viejo esté por encima?
- Regla del boy scout: la función que tocás sale un poco más simple de lo que entró.

## 4. Hotspots: churn × complejidad

Lo más rentable de refactorizar no es lo más complejo, es lo complejo **que además
cambia seguido**. Un archivo horrible que nadie toca en dos años no es urgente; uno
complejo que se edita cada semana quema tiempo en cada PR y esconde bugs.

```bash
# ✅ archivos con más commits en el último tiempo = candidatos si además son complejos
git log --since="6 months ago" --name-only --pretty=format: \
  | grep '\.ts$' | sort | uniq -c | sort -rn | head -20
```

Cruzá esa lista con la complejidad medida: la intersección es tu backlog de refactor.

## 5. Qué hacer con un hotspot

1. Cubrilo con tests de caracterización antes de tocarlo (`refactoring-safely`).
2. Bajá anidamiento con *early return* / cláusulas de guarda.
3. Extraé el cuerpo de cada rama a una función con nombre (baja cognitiva sin partir a lo bruto).
4. Si un `switch` por tipo se repite, es polimorfismo esperando nacer (`solid-principles`).
5. Registrá lo que no alcanzás a hacer como deuda visible (`technical-debt-management`).

## Anti-patrones
- Convertir el umbral en gate duro y que el equipo trocee funciones para burlarlo.
- Perseguir la métrica global de un repo heredado y frustrarse.
- Medir complejidad e ignorar el churn: refactorizás lo que no molesta a nadie.
- Reportar un número sin acción concreta al lado.

## Checklist
- [ ] Elegiste 2–3 métricas con umbral de señal, definido en el CLAUDE.md del proyecto.
- [ ] El umbral dispara revisión, no rechazo ciego; las excepciones van justificadas.
- [ ] Mirás tendencia y código nuevo, no solo el absoluto del repo.
- [ ] Priorizás por hotspot (churn × complejidad), no por complejidad sola.
- [ ] Cada hotspot reportado sale con una acción concreta o una entrada de deuda.
