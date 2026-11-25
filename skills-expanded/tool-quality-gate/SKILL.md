---
name: tool-quality-gate
description: "Validación pre-deploy cero-config para proyectos web. Detecta stack, configura tests cuando faltan, ejecuta build, variables de entorno, seguridad, tests y lint, y devuelve un score 0-100 con acciones concretas. Úsala antes de desplegar, hacer push, validar una app, preparar un proyecto arnes en nivel PRO o revisar si el código está listo para producción."
---

# Quality Gate

Validación pre-deploy para proyectos web, pensada para operadores no técnicos que necesitan una respuesta clara: **¿puedo subir esto o no?**

La skill se basa en prácticas TDD y pre-deploy, simplificadas para makers. No pretende sustituir una auditoría profesional, pero sí bloquear errores obvios antes de producción.

Si construyes con `arnes`, usa `tool-quality-gate` especialmente en nivel PRO antes del despliegue. Si aparecen hallazgos de seguridad, cruza también con `tool-seguridad-ia`.

---

## Modo de ejecución

Al activarse, decide el modo:

- **No hay setup de tests** (`vitest.config`, tests o hooks ausentes) → ejecuta **SETUP** y luego **CHECK**.
- **Ya hay testing configurado** → ejecuta **CHECK** directamente.
- **El usuario pide configurar tests** → ejecuta **SETUP**.
- **El usuario va a desplegar o hacer push** → ejecuta **CHECK** antes de continuar.

---

## SETUP

Se ejecuta una vez por proyecto. Objetivo: dejar una base mínima de validación sin romper trabajo existente.

### Paso 1 — Detectar stack

Lee `package.json` y la estructura del proyecto:

- Framework: Next.js App Router, Next.js Pages, React/Vite, Node, etc.
- Base de datos: Supabase, Prisma, ninguna.
- Destino de despliegue: Vercel, Netlify, otro.
- Configuración de tests ya existente.

Si hay configuración parcial, intégrala. No sobrescribas tests ni hooks del usuario.

### Paso 2 — Instalar dependencias

Instala solo lo necesario según el stack. Usa `references/install-configs.md` para paquetes y plantillas.

Paquetes base:

- `vitest` + `jsdom` para unit/integration tests.
- `husky` + `lint-staged` para hooks.
- `@playwright/test` solo si hay páginas interactivas que merecen E2E.

### Paso 3 — Crear configuración

Crea, si faltan:

- `vitest.config.ts`
- `vitest.setup.ts`
- hooks Husky `pre-commit` / `pre-push`
- scripts en `package.json`

El hook `pre-push` debe ejecutar build y tests para bloquear pushes rotos.

### Paso 4 — Generar tests mínimos

Para cada API route (`app/api/**/route.ts`), genera tests para:

1. **200** — caso feliz.
2. **400** — body/parámetros inválidos.
3. **401** — sin autenticación, si la ruta usa auth.
4. **403** — permisos insuficientes, si hay roles.
5. **404** — recurso no encontrado.
6. **500** — fallo simulado de base de datos o dependencia.

Para cada página (`app/**/page.tsx`), genera un test básico de render o de función de carga cuando sea Server Component.

Ubica tests junto al archivo fuente: `route.test.ts`, `page.test.tsx`.

### Paso 5 — Reportar setup

Resume qué se configuró, cuántos tests se generaron y ejecuta un primer CHECK.

---

## CHECK

Pipeline de 5 fases, score total 100.

### Fase 1 — Build (30 puntos)

Ejecuta `npm run build`.

- Pasa → 30/30.
- Falla → 0/30 y bloquea el resto si el fallo impide evaluar.

Traduce errores técnicos a lenguaje accionable: archivo, línea probable y cambio recomendado.

### Fase 2 — Variables de entorno (20 puntos)

Escanea referencias a `process.env.X` e `import.meta.env.X` y verifica `.env.local` o `.env`.

Comprueba:

- Variables críticas presentes.
- Variables públicas con prefijo correcto (`NEXT_PUBLIC_` en Next.js).
- Sin credenciales hardcodeadas en código fuente.

### Fase 3 — Seguridad (15 puntos)

Busca errores comunes:

- Credenciales o strings largos sospechosos en fuente.
- Variables server usadas en cliente.
- API routes privadas sin auth.
- CORS demasiado permisivo.
- Supabase service role en frontend.

Para una revisión más profunda, deriva a `tool-seguridad-ia` o `tool-web-security-audit` según el caso.

### Fase 4 — Tests (25 puntos)

Ejecuta `npx vitest run`.

- Todo pasa → 25/25.
- Parcial → score proporcional.
- No hay tests → 12/25 y recomienda SETUP.

Explica fallos con causa probable y siguiente acción.

### Fase 5 — Lint (10 puntos)

Ejecuta `npx next lint` o `npx eslint .` según el stack.

---

## Informe

Formato recomendado:

```text
QUALITY GATE — INFORME

Score: XX/100

Build .............. XX/30
Env vars ........... XX/20
Seguridad .......... XX/15
Tests .............. XX/25
Lint ............... XX/10

VEREDICTO: ...
```

Veredictos:

- **90-100**: listo para producción.
- **75-89**: funciona, pero hay avisos que conviene revisar.
- **50-74**: riesgo medio; arreglar los puntos rojos antes de subir.
- **0-49**: no desplegar hasta corregir bloqueadores.

Después del score, lista cada acción con severidad, impacto en puntos, problema y fix concreto.

---

## Intercepción de deploy

Si el usuario dice "deploy", "sube esto", "push a producción", "Vercel", "vamos a subir", "git push", "ship it" o equivalente, ejecuta CHECK primero.

- Score >= 75 → se puede continuar, mencionando avisos.
- Score 50-74 → pregunta si prefiere arreglar antes de subir.
- Score < 50 → recomienda bloquear despliegue y resolver críticos.

---

## Estilo de comunicación

- Responde siempre en español.
- Traduce output técnico a lenguaje humano.
- No muestres logs crudos sin interpretación.
- No preguntes qué testear si puedes inferirlo del proyecto.
- Si no hay tests, genera una base en vez de limitarte a señalarlo.

Skill original de Angel Aparicio (IA Masters Academy), adaptada para iamasters-os.
