---
name: static-analysis-linting
description: Análisis estático de la casa — ESLint con flat config y typescript-eslint con reglas type-aware, Prettier separado del linter, autofix seguro vs manual, lint-staged/husky, reglas que importan vs ruido, y la prohibición de silenciar reglas con `eslint-disable` sin justificación. Usar al montar o migrar la config de lint de un repo, al agregar o desactivar una regla, al integrar el lint al pre-commit y al CI, o cuando el lint tira mil warnings que nadie mira.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Análisis estático — el compilador que atrapa lo que `tsc` no ve

El linter no reemplaza a `tsc`: lo complementa. `tsc` valida tipos; ESLint valida
patrones (promesas sin await, `any` implícito, imports muertos, código sospechoso).
Con reglas *type-aware* el linter también razona sobre tipos y atrapa bugs reales.

## 1. Flat config + typescript-eslint con tipos

La config moderna es `eslint.config.mjs` (flat config, un array de bloques). Para
type-aware linting (verificado en typescript-eslint.io):

```js
// eslint.config.mjs
import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  js.configs.recommended,
  tseslint.configs.recommendedTypeChecked, // ✅ reglas que usan información de tipos
  {
    languageOptions: {
      parserOptions: { projectService: true }, // habilita el servicio de tipos, sin listar tsconfigs a mano
    },
  },
  { ignores: ['dist/', 'coverage/', '**/*.generated.ts'] },
);
```

`recommendedTypeChecked` es más lento (TS analiza el proyecto antes de lintear) pero
atrapa lo que vale: `no-floating-promises`, `no-misused-promises`,
`no-unsafe-*`. En una API con async por todos lados, esas reglas pagan solas su costo.

## 2. Prettier NO es un linter — separalos

- **Prettier**: formato (comillas, comas, ancho). Corre aparte (`prettier --check` /
  `--write`). Es la etapa 1 del gate.
- **ESLint**: calidad y bugs. No le pongas reglas de formato.
- Para que no choquen, que ESLint no tenga reglas estilísticas de formato (con la config
  de arriba no las trae). No mezcles responsabilidades: un archivo mal formateado lo
  arregla Prettier, no una regla de lint.

## 3. Autofix: seguro vs manual

- `--fix` seguro y automatizable: imports ordenados, comillas, `prefer-const`, quitar
  imports sin uso. Corren solos en `lint-staged`.
- **Nunca** autofix a ciegas de reglas que cambian semántica (algunas sugerencias de
  `no-floating-promises` agregan `void`). Revisá el diff del fix como cualquier cambio.

## 4. Pre-commit rápido, CI completo

```jsonc
// package.json → lint-staged: solo lo staged, en segundos
"lint-staged": {
  "*.{ts,html}": ["eslint --fix", "prettier --write"]
}
```

Enganchalo con husky (`pre-commit`). El hook es feedback local y salteable; el CI
lintea **todo** sin `--fix` y bloquea (ver `code-quality-gates`). En CI usá
`--max-warnings=0`: o la regla es error, o no existe.

## 5. `eslint-disable`: la excepción con nombre y apellido

Desactivar una regla es una decisión de ingeniería, no un atajo:

```ts
// ❌ silencia y esconde: nadie sabe por qué
// eslint-disable-next-line
const x = data as any;

// ✅ regla puntual + motivo verificable
// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment -- SDK sin tipos, validado por zod abajo (issue #142)
const raw = sdk.fetch();
```

Reglas: `disable` de una regla específica (nunca la línea entera), en una sola línea
(no `disable` de archivo), con comentario `--` que explica el porqué. Un `disable`
sin motivo es un `any` disfrazado — lo caza `anti-hallucination-guard`.

## 6. Reglas: señal vs ruido

- Arrancá de `recommended` + `recommendedTypeChecked`. No inventes 200 reglas el día uno.
- Subí a `error` lo que atrapa bugs; sacá lo que solo genera ruido estilístico.
- Reglas propias del proyecto (naming de archivos, imports prohibidos entre capas con
  `no-restricted-imports`) codifican la arquitectura: valen oro.
- Lint de commits (commitlint + Conventional Commits) alimenta el changelog
  (ver `github-releases-versioning`).

## Anti-patrones
- Mezclar Prettier dentro de ESLint y pelear configuraciones eternamente.
- 10 000 warnings tolerados: warning que no bloquea = regla que no existe.
- `eslint-disable` de archivo entero al inicio de un módulo "problemático".
- Config sin `projectService`/type info: perdés la mitad del valor.
- Ejecutar lint solo local: sin CI, el que no tiene el hook mergea cualquier cosa.

## Checklist
- [ ] Flat config con `recommendedTypeChecked` y `projectService: true`.
- [ ] Prettier corre separado; ESLint no tiene reglas de formato.
- [ ] `lint-staged` + husky en local; CI con `--max-warnings=0` que bloquea.
- [ ] Cada `eslint-disable` es de regla puntual, en una línea, con motivo `--`.
- [ ] Hay reglas que protegen las fronteras de arquitectura del proyecto.
- [ ] commitlint activo si el changelog se genera de los commits.
