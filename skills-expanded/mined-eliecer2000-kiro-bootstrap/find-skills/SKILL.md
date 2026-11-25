---
name: find-skills
description: Discover, search and install skills from the open agent ecosystem. Use when looking for external skills, browsing the skills marketplace, or installing new capabilities via npx skills CLI.
---

# Find Skills

Skill obligatoria para descubrir, buscar e instalar skills del ecosistema abierto de agentes. Permite a cualquier agente de Orbit localizar capacidades adicionales bajo demanda usando el CLI `npx skills`.

## Cuándo usar esta skill

Usar cuando:

- El usuario pregunta "cómo hago X" y X podría tener una skill existente.
- El usuario dice "busca una skill para X" o "hay alguna skill que haga X".
- El usuario quiere extender las capacidades del agente con herramientas, templates o workflows.
- Se necesita funcionalidad especializada fuera del catálogo local de Orbit.
- El usuario menciona un dominio específico (React, testing, deployment, design, etc.).

## Qué es el Skills CLI

El CLI `npx skills` es el package manager del ecosistema abierto de skills para agentes. Las skills son paquetes modulares que extienden las capacidades del agente con conocimiento especializado, workflows y herramientas.

### Comandos clave

```bash
# Buscar skills interactivamente o por keyword
npx skills find [query]

# Instalar una skill desde GitHub u otras fuentes
npx skills add <package>

# Instalar globalmente sin confirmación
npx skills add <owner/repo@skill> -g -y

# Verificar actualizaciones
npx skills check

# Actualizar todas las skills instaladas
npx skills update

# Inicializar una skill nueva
npx skills init <nombre>
```

### Directorio de skills

Explorar skills disponibles en: https://skills.sh/

## Proceso de búsqueda

### Paso 1: Entender la necesidad

Identificar:
1. El dominio (React, testing, design, deployment, AWS, etc.)
2. La tarea específica (escribir tests, crear animaciones, revisar PRs)
3. Si es una tarea común que probablemente tenga una skill existente

### Paso 2: Consultar el leaderboard

Antes de ejecutar búsqueda CLI, revisar el [leaderboard de skills.sh](https://skills.sh/) para skills populares y probadas. El leaderboard rankea por instalaciones totales.

Fuentes populares:
- `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs)
- `anthropics/skills` — Frontend design, document processing (100K+ installs)
- `ComposioHQ/awesome-claude-skills` — Integraciones y automatización

### Paso 3: Buscar con el CLI

```bash
npx skills find [query]
```

Ejemplos:
- "cómo optimizo mi app React?" → `npx skills find react performance`
- "necesito ayuda con PR reviews" → `npx skills find pr review`
- "quiero crear un changelog" → `npx skills find changelog`
- "necesito patrones serverless" → `npx skills find aws serverless`

### Paso 4: Verificar calidad antes de recomendar

NO recomendar una skill solo por aparecer en resultados. Verificar:

1. **Instalaciones** — Preferir skills con 1K+ installs. Precaución con menos de 100.
2. **Reputación de la fuente** — Fuentes oficiales (`vercel-labs`, `anthropics`, `microsoft`, `aws`) son más confiables.
3. **GitHub stars** — Repositorio con <100 stars requiere escepticismo.
4. **Fecha de actualización** — Skills sin actualizar en >6 meses pueden estar desactualizadas.

### Paso 5: Presentar opciones al usuario

Incluir:
1. Nombre de la skill y qué hace
2. Conteo de instalaciones y fuente
3. Comando de instalación
4. Link para más información

Ejemplo de respuesta:
```
Encontré una skill que puede ayudar: "react-best-practices" de Vercel Engineering
con guías de optimización de rendimiento para React y Next.js. (185K installs)

Para instalarla:
npx skills add vercel-labs/agent-skills@react-best-practices

Más info: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### Paso 6: Instalar si el usuario acepta

```bash
npx skills add <owner/repo@skill> -g -y
```

El flag `-g` instala a nivel global (usuario) y `-y` omite confirmaciones.

## Categorías comunes de skills

| Categoría        | Queries de ejemplo                           |
|------------------|----------------------------------------------|
| Web Development  | react, nextjs, typescript, css, tailwind     |
| Testing          | testing, jest, playwright, e2e               |
| DevOps           | deploy, docker, kubernetes, ci-cd            |
| Documentation    | docs, readme, changelog, api-docs            |
| Code Quality     | review, lint, refactor, best-practices       |
| Design           | ui, ux, design-system, accessibility         |
| Cloud / AWS      | aws, serverless, lambda, cdk, terraform      |
| Productivity     | workflow, automation, git                    |

## Integración con Orbit

### Política de instalación

Orbit usa la política `confirm-before-install` para skills remotas. El flujo es:

1. El agente identifica la necesidad de una skill externa.
2. Busca usando `npx skills find`.
3. Presenta la opción al usuario con detalles de calidad.
4. Solo instala tras confirmación explícita del usuario.
5. La skill se registra en el `remoteSkillsAllowlist` del proyecto si aplica.

### Comando de instalación Orbit

```bash
npx skills add <package> -g -y
```

### Cuando no se encuentran skills

1. Reconocer que no se encontró una skill existente.
2. Ofrecer ayudar directamente con las capacidades generales del agente.
3. Sugerir crear una skill propia si es una tarea recurrente:

```bash
npx skills init mi-skill-custom
```

## Tips para búsquedas efectivas

1. Usar keywords específicos: "react testing" es mejor que solo "testing".
2. Probar términos alternativos: si "deploy" no funciona, probar "deployment" o "ci-cd".
3. Revisar fuentes populares primero: muchas skills vienen de `vercel-labs/agent-skills` o `ComposioHQ/awesome-claude-skills`.
4. Combinar dominio + tarea: "aws lambda optimization" es más preciso que "aws".

## Anti-patrones

- ❌ Instalar skills sin verificar calidad ni reputación.
- ❌ Instalar skills sin confirmación del usuario.
- ❌ Recomendar skills con <100 instalaciones sin advertencia.
- ❌ Ignorar skills locales de Orbit cuando ya cubren la necesidad.
- ❌ Buscar skills para tareas triviales que el agente ya sabe hacer.
- ❌ No verificar compatibilidad con el agente/IDE actual.
