---
name: test-case-design-techniques
description: Diseño sistemático de casos de prueba — partición de equivalencia, análisis de valores límite, tabla de decisión, transición de estados, combinatorio pairwise, casos positivos y negativos, criterio de cobertura funcional y trazabilidad requisito → caso. Usar al planificar qué probar de una feature, endpoint o formulario, al convertir criterios de aceptación en casos concretos, o cuando "probé algo" pero no hay forma de saber qué quedó sin cubrir.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Técnicas de diseño de casos

Elegir casos "a ojo" deja huecos y duplica esfuerzo. Estas técnicas convierten un requisito en un
conjunto de casos **mínimo y suficiente**. Qué probar en qué nivel (unit/integración/E2E) lo decide
`qa-strategy`; los valores concretos salen de `edge-case-data-catalog`; el riesgo prioriza cuáles.

## 1. Partición de equivalencia
Dividí el espacio de entrada en clases donde el sistema debería comportarse igual, y probá **un
representante por clase** (no cien de la misma).
- Ejemplo — edad para una regla que aplica de 18 a 65: clases `<18`, `18–65`, `>65`. Tres casos, no treinta.
- Clases válidas e inválidas por separado. Cada clase inválida, en su propio caso (para no enmascarar).

## 2. Valores límite (BVA)
Los bugs se concentran en los bordes de cada clase. Para un rango `[min, max]` probá:
`min-1, min, min+1, max-1, max, max+1`.
- Aplicá a números, longitudes de string, tamaños de colección, fechas, montos.
- Complementa la partición: la partición dice "qué clases", el límite "qué valores de cada borde".

## 3. Tabla de decisión
Cuando la salida depende de varias condiciones combinadas, tabulá.

| Rol | Es dueño | Consentimiento | ¿Puede ver ficha? |
|---|---|---|---|
| médico | sí | — | sí |
| médico | no | sí | sí |
| médico | no | no | no |
| admin | — | — | no |

- Una fila = un caso. Colapsá filas donde una condición es indiferente (`—`).
- Cubre combinaciones que "a ojo" se olvidan (el médico no dueño sin consentimiento).

## 4. Transición de estados
Para entidades con ciclo de vida (cita, cotización, solicitud): tomá la máquina de
`state-machines-workflows` y derivá casos.
- Un caso por **transición válida** (que ocurra y persista).
- Un caso por **transición inválida** (que se rechace, sin efecto).
- Caminos: recorrido feliz completo, y al menos un intento de salto de estado.

## 5. Combinatorio (pairwise)
Cuando hay muchos parámetros independientes, probar todas las combinaciones explota. Pairwise cubre
todos los **pares** de valores con una fracción de los casos: atrapa la mayoría de los defectos por
interacción sin el costo del producto cartesiano. Usá una herramienta pairwise; documentá qué
combinaciones quedaron fuera y por qué.

## 6. Positivos y negativos
- **Positivo**: entrada válida → resultado esperado.
- **Negativo**: entrada inválida o no autorizada → rechazo correcto, mensaje claro, sin efecto lateral.
- Los negativos de autorización son obligatorios en API (otro usuario/tenant/rol): ver `api-testing`.

## Cobertura funcional (qué medir)
- Cada criterio de aceptación tiene ≥1 caso positivo y sus negativos relevantes.
- Cada regla de negocio de la tabla de decisión, cubierta.
- Cada transición de estado, cubierta.
- La cobertura de líneas/ramas es señal, no objetivo (ver `unit-testing`, `qa-strategy`).

## Trazabilidad requisito → caso
Mantené una matriz `REQ → caso(s) → resultado`. Sirve para:
- ver qué requisito no tiene ningún caso (hueco);
- ver qué caso no mapea a ningún requisito (¿sobra o falta el requisito?);
- reportar cobertura al cerrar (ver `test-plan-authoring`, `qa-evidence-reporting`).

## Anti-patrones
- Muchos casos de la misma clase de equivalencia y ninguno del borde.
- Solo camino feliz; cero negativos.
- Combinar todo con todo cuando pairwise bastaba (suite lenta e inmantenible).
- Casos sin resultado esperado explícito.

## Checklist
- [ ] Entradas particionadas; un representante por clase.
- [ ] Valores límite (min±1, max±1) cubiertos.
- [ ] Reglas combinadas tabuladas en tabla de decisión.
- [ ] Transiciones válidas e inválidas cubiertas si hay estados.
- [ ] Cada criterio de aceptación mapeado a casos (matriz de trazabilidad).
- [ ] Negativos de validación y de autorización incluidos.
