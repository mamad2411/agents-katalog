---
name: factual-discovery
description: Descubrimiento factual del sistema real antes de escribir una sola línea — stack, package manager, monorepo/workspaces, frameworks, ORM, base de datos, auth, design system, comandos de build/lint/test, la ruta y el componente reales, los endpoints, el DTO/modelo, los seeds y el baseline de errores en runtime. Usar al arrancar cualquier carril, feature o bug, antes de planificar o editar, y cada vez que estés por asumir cómo funciona algo en lugar de confirmarlo.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Descubrimiento factual

No modifiques funcionalidad hasta tener un mapa mínimo de evidencia del sistema real. La mayoría
de los errores caros nacen de asumir en vez de mirar. Trabajá con economía de contexto
(`context-thrift`) y muestreá patrones existentes (`native-code-patterns`) mientras descubrís.

## Cuándo aplica

- Al inicio de todo carril, feature o bug, antes de planificar.
- Cuando estás por decir "seguramente esto usa X" — confirmalo primero.
- Antes de crear cualquier pieza: puede que ya exista (`anti-hallucination-guard`).

## Regla

Un cambio de funcionalidad sin discovery previo es una apuesta. Durante discovery sólo se
permite el ajuste mínimo para poder arrancar el entorno, y sólo si se documenta.

## A. Repositorio y entorno

- `git status --short`, rama actual, commits locales sin publicar si importan.
- Monorepo/workspaces, lockfile, package manager real (no asumir).
- Scripts de `package.json`: build, lint, typecheck, test, e2e.
- Docker/compose si existe; `.env.example` (nunca imprimir secretos).

## B. Frontend

Localizá la definición de ruta, la página/vista, sus componentes hijos, el layout, el manejo de
estado/datos/formularios, el design system/UI kit, la arquitectura de estilos, los guards/permisos
y la i18n si existe.

## C. Backend

Localizá el controller/endpoint, el service/caso de uso, el DTO/validador, la entidad/modelo, el
repositorio, la fuente del esquema, los eventos/notificaciones y los tests que ya cubren la zona.

## D. Datos

Tablas/colecciones, claves, relaciones, índices, seeders, catálogos, constraints y estados/enums
implicados por el cambio.

## E. Runtime (baseline)

Arrancá sólo lo necesario y ejercitá la superficie que vas a cambiar **antes** de tocarla:

- Errores HTTP, errores de consola, assets faltantes, estado visual.
- Llamadas de red y la respuesta real relevante.
- Guardá este baseline: es contra lo que vas a comparar después.

## F. Salida del discovery

Resumí en una nota durable (no en el chat), lista para planificar:

- **Hechos** con archivo/línea que los respalda.
- **Contratos** reales (endpoints, DTOs, schema).
- **Baseline** de runtime.
- **Desconocidos** y **contradicciones** que encontraste.
- **Riesgos**.

## Anti-patrones

- Empezar a editar y "ver qué pasa".
- Asumir el ORM, el package manager o el patrón de un archivo sin abrir uno.
- Leer un archivo entero cuando alcanzaba un grep/rango — ver `context-thrift`.
- Confundir leer el código con verificar el comportamiento — eso es `evidence-and-verification`.

## Checklist

- [ ] Estado de git, workspaces, package manager y comandos reales confirmados.
- [ ] Ruta, componente, endpoint, DTO/modelo y datos implicados localizados con archivo/línea.
- [ ] Baseline de runtime capturado antes de editar.
- [ ] Desconocidos, contradicciones y riesgos anotados.
- [ ] Ninguna pieza nueva planificada sin antes buscar la existente.
