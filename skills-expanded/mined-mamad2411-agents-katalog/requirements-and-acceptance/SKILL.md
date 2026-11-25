---
name: requirements-and-acceptance
description: Cómo convertir un pedido vago en criterios de aceptación verificables antes de escribir código — formato dado-cuando-entonces, Definition of Ready, matriz de trazabilidad requisito→evidencia, alcance IN/OUT y registro de ambigüedades sin adivinar. Usar al recibir cualquier requisito, historia o bug; al detectar una frase ambigua en el backlog; al decidir si algo está listo para implementar; y al definir qué evidencia probará que un criterio se cumplió. Para fijar el resultado observable antes de arrancar y dirimir si algo está hecho, ver `outcome-first`.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Requisitos y criterios de aceptación

Un requisito que no se puede verificar no está terminado de escribir. El trabajo empieza
convirtiendo el pedido en criterios observables; recién ahí se planifica. Complementa a
`outcome-first` (define el resultado) y a `anti-hallucination-guard` (no inventar lo faltante).

## Cuándo aplica

- Al recibir un pedido, historia, épica o reporte de bug.
- Cuando una frase del backlog es ambigua, contradictoria o "obvia".
- Antes de estimar, planificar o cortar en slices.

## 1. De pedido a criterio verificable

Cada requisito se expresa como uno o más criterios en formato **dado-cuando-entonces**:

```
DADO   un doctor con agenda publicada
CUANDO bloquea la franja 10:00–11:00 del martes
ENTONCES esa franja deja de aparecer como disponible para nuevas solicitudes
Y       las solicitudes ya aceptadas en esa franja no se alteran
```

- Cada criterio es booleano: se cumple o no, sin interpretación.
- Cubrí el camino feliz **y** los negativos/límite relevantes (sin permiso, dato inválido,
  concurrencia). Ver `edge-case-data-catalog`.
- Numerá: `REQ-<id>-<n>`, para trazar contra evidencia.

## 2. Alcance IN / OUT

Antes de arrancar, escribí explícitamente qué está dentro y qué queda afuera. Lo que no está
en IN no se implementa "de paso" — ver `scope-discipline`. Un OUT explícito evita el scope creep
y las discusiones de cierre.

## 3. Registro de ambigüedades (no adivinar)

- Si el pedido es ambiguo, **registralo como ambigüedad**; no lo resuelvas por lo que sea más
  fácil de construir ni cambies la semántica del requisito.
- Intentá resolver por evidencia primero (código, runtime, contrato). Si no se puede, marcá
  el criterio `AMBIGUOUS` y escalá la pregunta concreta. No implementes sobre una suposición
  presentada como hecho.

## 4. Definition of Ready

Un requisito está **listo para implementar** cuando:

- [ ] Tiene criterios de aceptación verificables (dado-cuando-entonces).
- [ ] Alcance IN/OUT declarado.
- [ ] Ambigüedades resueltas o marcadas y escaladas.
- [ ] Dependencias identificadas.
- [ ] Se sabe qué evidencia probará cada criterio.

Si no cumple, no está listo: no arranques, resolvé el Ready primero.

## 5. Matriz de trazabilidad

Mantené la relación requisito → evidencia, para que el cierre sea mecánico:

| Criterio | Estado | Archivos | Evidencia de cierre |
|---|---|---|---|
| REQ-42-1 | SATISFIED | api/…, web/… | test `bloqueo.e2e`, respuesta 200 pegada |
| REQ-42-2 | PARTIAL | web/… | falta estado de error |

Estados: `SATISFIED | PARTIAL | MISSING | AMBIGUOUS | BLOCKED`.

## 6. Definition of Done

Un requisito está **hecho** cuando todos sus criterios están `SATISFIED` con evidencia
observable pegada (ver `evidence-and-verification`), no cuando "el código está escrito".
UI cambiada sin backend/persistencia no es "hecho".

## Anti-patrones

- Criterios que empiezan con "el sistema debería ser rápido/intuitivo/robusto" — no son verificables.
- "Ya se entiende" como sustituto de escribir el criterio.
- Resolver una ambigüedad en silencio eligiendo lo más cómodo.
- Cerrar por "lo implementé" sin evidencia por criterio.

## Checklist

- [ ] Cada requisito tiene criterios dado-cuando-entonces booleanos y numerados.
- [ ] Camino feliz + negativos/límite cubiertos.
- [ ] IN/OUT explícito.
- [ ] Ambigüedades registradas, no adivinadas.
- [ ] Matriz requisito→evidencia lista para el cierre.
- [ ] Definition of Ready cumplida antes de codear; Definition of Done antes de cerrar.
