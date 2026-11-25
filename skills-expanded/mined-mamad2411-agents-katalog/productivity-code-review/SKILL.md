---
name: productivity-code-review
description: Realiza una revisión exhaustiva de código en cualquier proyecto. Analiza seguridad, mejoras, optimizaciones, sugerencias y críticas — usando los dev-kits del stack para reglas específicas. Ejecuta escaneo automático de dependencias (npm audit, pip-audit, dotnet list package) y análisis estático (eslint, ruff, mypy). Genera un reporte en formato tabla con checkboxes (✅/⬜) como archivo CODE_REVIEW.md en la raíz del proyecto, con sección Quick Wins para arreglos de <30 min. Usar cuando el usuario pida "review", "analizar el proyecto", "auditar código", "code review", "revisa el proyecto", "security review", o quiera evaluar la calidad de su código.
requires-devkits: auto-detect
---

# Productivity Code Review — Auditoría de Proyecto

## Propósito

Realizar una auditoría completa de código fuente cubriendo **5 categorías**: Seguridad, Mejoras, Optimizaciones, Sugerencias y Críticas. El resultado se entrega como un archivo `CODE_REVIEW.md` en la raíz del proyecto con formato tabla y checkboxes para seguimiento de correcciones.

---

## Instrucciones del Agente

### Fase 1: Descubrimiento del Proyecto

1. Explora la estructura del proyecto con `find`/`ls` (excluyendo `node_modules`, `.git`, `bin`, `obj`, etc.)
2. Identifica el stack tecnológico: lenguaje, framework, base de datos, dependencias clave
3. **Detecta y carga los dev-kits relevantes** según el stack:
   - `.csproj` / `*.sln` → cargar `dotnet-core`, `dotnet-security`, `dotnet-performance`
   - `Program.cs` con `WebApplication` → cargar `aspnet-core`
   - `package.json` con `react` → cargar `react-core`, `react-performance`, `react-components`
   - `package.json` con `next` → cargar `react-core`, `react-architecture`
   - `package.json` con `antd` / `@ant-design/pro-components` → cargar `react-antdesign`
   - `package.json` con `express` / `fastify` → cargar `nodejs-core`, `nodejs-express`
   - `pyproject.toml` con `fastapi` → cargar `python-core`, `python-fastapi`
   - `prisma/schema.prisma` → cargar `nodejs-database` o `python-database` según stack
   - `*.csproj` con `Microsoft.EntityFrameworkCore.SqlServer` → cargar `sql-server-core`
   - `*.csproj` con `Npgsql` → cargar `postgresql-core`
   - `Dockerfile` + `k8s/` → cargar `devops-docker`, `devops-kubernetes`
   - `.github/workflows/` → cargar `devops-cicd`
   Las reglas de estos dev-kits guían el análisis (ej: `dotnet-security` define qué verificar en JWT, CORS, etc.)
4. Lee los archivos de configuración principales (`package.json`, `*.csproj`, `pom.xml`, `appsettings*.json`, `.env` files, `Dockerfile`, etc.)
5. Lee los archivos de entrada (`Program.cs`, `index.js`, `main.py`, etc.)
5. **Análisis estático automático**: Si el proyecto tiene linters/type-checkers configurados, ejecútalos y reporta hallazgos:
   - Node.js: `npx eslint . --format json` (si `.eslintrc` existe), `npx tsc --noEmit` (errores de tipo)
   - Python: `uv run ruff check . --output-format json` (si `ruff` en deps), `uv run mypy src/ --no-error-summary` (errores de tipo)
   - .NET: `dotnet build --no-restore` (warnings de compilación), `dotnet format --verify-no-changes` (estilo)
   Los resultados se integran en las categorías Mejoras (lint) y Optimizaciones (type errors).
6. Lee al menos el 80% de los archivos de código fuente (controladores, servicios, modelos, vistas, scripts)

### Fase 2: Análisis por Categoría

Analiza cada archivo contra estas **5 categorías obligatorias**:

#### 🔴 Seguridad (Security Issues)
Busca activamente vulnerabilidades:
- **Autenticación/Autorización**: falta de auth, bypasses, sesiones inseguras, tokens hardcodeados, backdoors de debug
- **Inyección**: SQL injection, command injection, XSS, path traversal
- **Configuración insegura**: CORS demasiado permisivo, secrets en texto plano, HTTP en vez de HTTPS, cabeceras de seguridad faltantes (CSP, HSTS, X-Frame-Options)
- **Exposición de datos**: logs con datos sensibles, stack traces al usuario, información en el DOM
- **CSRF**: falta de anti-forgery tokens en POST
- **Dependencias**: CDNs externos sin SRI, paquetes desactualizados, dependencias de preview/beta en producción
- **Criptografía**: hashing débil, falta de encryptión, claves hardcodeadas
- **Escaneo automático de vulnerabilidades**: Ejecutar el comando de auditoría según el stack:
  - Node.js: `npm audit --json` (parsear advisories con severity high/critical)
  - Python: `uv run pip-audit --format json` (parsear vulnerabilities)
  - .NET: `dotnet list package --vulnerable` (parsear salida)
  Reportar CVEs reales en la tabla de Seguridad con el CVE ID cuando exista.

#### 🛠️ Mejoras (Improvements)
Problemas de calidad de código y mantenibilidad:
- **Tipado débil**: uso excesivo de `object`, `dynamic`, `var`, `any`
- **Código duplicado**: lógica repetida en múltiples lugares
- **Nombrado inconsistente**: mezcla de idiomas, convenciones rotas, typos
- **Código muerto**: métodos vacíos/stub, imports no usados, archivos basura
- **Falta de documentación**: sin Swagger, sin README, sin comentarios XML
- **Manejo de errores**: catch vacíos, throw sin contexto, falta de logging estructurado
- **Mala separación de responsabilidades**: lógica de negocio en controladores, vistas con queries

#### ⚡ Optimizaciones (Optimizations)
Oportunidades de performance:
- **Consultas N+1**: múltiples llamadas a BD en loops
- **Falta de caché**: datos catálogo/estáticos sin `IMemoryCache` o Redis
- **Operaciones costosas repetidas**: reflection, serialización, DataTable→objeto manual
- **Carga de recursos**: duplicación de scripts/CSS, sin bundling/minificación, Font Awesome completo vs subset
- **Consultas sin paginación**: SELECT * sin LIMIT/OFFSET
- **Operaciones síncronas bloqueantes**: falta de async/await en I/O
- **Over-fetching**: endpoints que retornan más datos de los necesarios

#### 💡 Sugerencias (Suggestions)
Recomendaciones proactivas no críticas:
- Migración tecnológica (ej: DataTable → Dapper/EF Core)
- Adopción de patrones arquitectónicos (CQRS, MediatR, Repository)
- Herramientas de monitoreo (Application Insights, Serilog, health checks)
- Mejoras de DX (hot reload, .editorconfig, linters)
- Modularización de frontend (ES6 modules, componentes)
- API versioning, compresión, HATEOAS
- Pruebas unitarias/integración

#### 🗣️ Críticas (Criticism)
Problemas estructurales profundos:
- Versiones preview/beta en producción
- Anti-patrones arquitectónicos (DataTable como contrato, God objects)
- Dependencias de DLLs propietarias sin source
- Mock/testing code mezclado con producción
- Deuda técnica severa que compromete escalabilidad
- Mezcla de idiomas que dificulta colaboración
- Acoplamiento fuerte entre capas

### Fase 3: Clasificación por Severidad

Cada hallazgo debe llevar **una y solo una** etiqueta de severidad:

| Etiqueta | Criterio |
|----------|----------|
| 🔴 **Crítico** | Vulnerabilidad explotable, crash, pérdida de datos, puerta trasera, o bloquea el desarrollo/despliegue |
| 🟡 **Alto** | Impacto significativo en seguridad/performance/mantenibilidad, debería resolverse en este sprint |
| 🟢 **Medio** | Code smell, violación de buenas prácticas, deuda técnica que puede esperar 1-2 sprints |
| ⚪ **Bajo** | Cosmético, preferencia estilística, mejora "nice to have" |

3. **Quick Wins** (arreglos de <30 min con alto impacto):
   Top 5 cosas que el equipo puede corregir hoy mismo.

### Fase 4: Generación del Reporte

Crea el archivo `CODE_REVIEW.md` en la raíz del proyecto con esta estructura exacta:

```markdown
# 🔍 Code Review — [Nombre del Proyecto]

> **Fecha:** [YYYY-MM-DD]
> **Revisor:** AI Code Review
> **Stack:** [Lenguaje + Framework + BD]

---

## 📊 Resumen

| Categoría | Total | 🔴 Crítico | 🟡 Alto | 🟢 Medio | ⚪ Bajo |
|-----------|-------|-----------|---------|----------|---------|
| Seguridad | N | N | N | N | N |
| Mejoras | N | N | N | N | N |
| Optimizaciones | N | N | N | N | N |
| Sugerencias | N | N | N | N | N |
| Críticas | N | N | N | N | N |
| **TOTAL** | **N** | **N** | **N** | **N** | **N** |

---

## ⚡ Quick Wins (< 30 min cada uno)

| # | Archivo | Problema | Acción | ✅ |
|---|---------|----------|--------|----|
| 1 | `path/file.ts:10` | Descripción breve | Acción concreta de <30 min | ⬜ |

---

## 🔴 Seguridad (Security Issues)

| # | Severidad | Archivo / Ubicación | Problema | Recomendación | ✅ |
|---|-----------|---------------------|----------|----------------|---|
| 1 | 🔴 Crítico | `path/to/file.cs:42` | Descripción concisa del problema | Acción correctiva específica | ⬜ |

... (todas las filas necesarias)

---

## 🛠️ Mejoras (Improvements)

| # | Severidad | Archivo / Ubicación | Problema | Recomendación | ✅ |
|---|-----------|---------------------|----------|----------------|---|
| ... | ... | ... | ... | ... | ⬜ |

---

## ⚡ Optimizaciones (Optimizations)

| # | Severidad | Archivo / Ubicación | Problema | Recomendación | ✅ |
|---|-----------|---------------------|----------|----------------|---|
| ... | ... | ... | ... | ... | ⬜ |

---

## 💡 Sugerencias (Suggestions)

| # | Severidad | Área | Sugerencia | ✅ |
|---|-----------|------|------------|----|
| ... | ... | ... | ... | ⬜ |

---

## 🗣️ Críticas (Criticism)

| # | Severidad | Crítica | Detalle | ✅ |
|---|-----------|---------|---------|----|
| ... | ... | ... | ... | ⬜ |

---

## 📋 Plan de Acción Recomendado

### Fase 1 — Inmediato (Sprint actual)
1. ✅ Acción concreta
2. ⬜ Acción concreta

### Fase 2 — Corto plazo (1-2 sprints)
3. ⬜ ...

### Fase 3 — Mediano plazo (3-4 sprints)
...

### Fase 4 — Largo plazo
...

---

> **Nota:** Este reporte es generado automáticamente. Revisar cada hallazgo antes de actuar.
```

### Fase 5: Resumen al Usuario

Al finalizar, presenta un resumen ejecutivo:

1. Total de hallazgos por categoría y severidad
2. Top 5 problemas más graves (Críticos)
3. Ruta del archivo generado
4. Recordatorio de que cada hallazgo tiene un checkbox ✅ para seguimiento

---

## Reglas Estrictas

- **5 categorías obligatorias**: Siempre incluye Seguridad, Mejoras, Optimizaciones, Sugerencias, Críticas
- **Tablas con checkboxes**: Cada fila debe terminar con `| ⬜ |` para seguimiento
- **Severidad única**: Cada hallazgo tiene una y solo una severidad (🔴🟡🟢⚪)
- **Archivo concreto**: Cada hallazgo referencia archivo y línea específicos (`path/to/file.ext:N`)
- **Recomendación accionable**: Cada hallazgo incluye qué hacer para resolverlo (no solo describir el problema)
- **Plan de acción**: Agrupa las correcciones en fases temporales (Inmediato → Corto → Mediano → Largo plazo)
- **Nunca inventes problemas**: Solo reporta hallazgos que realmente observaste en el código
- **No repitas hallazgos**: Si el mismo problema aparece en múltiples archivos, consolida en un solo row mencionando todos los archivos
- **Sé específico**: Usa nombres reales de variables, métodos, clases, y valores observados en el código

---

## Ejemplo de Flujo

**Usuario:** "Revisa el proyecto y dime problemas de seguridad, mejoras y optimizaciones"

**Agente:**
1. Explora estructura con `find` y `ls`
2. Lee archivos clave (config, entry point, controladores, servicios, modelos)
3. Analiza cada archivo contra las 5 categorías
4. Clasifica por severidad
5. Genera `CODE_REVIEW.md` con tablas + checkboxes
6. Notifica al usuario:

```
✅ Análisis completado: 75 hallazgos encontrados

📊 Resumen:
- 🔴 Seguridad: 14 issues (10 críticos)
- 🛠️ Mejoras: 15 issues (2 críticos)
- ⚡ Optimizaciones: 13 issues (4 críticos)
- 💡 Sugerencias: 18 recomendaciones
- 🗣️ Críticas: 15 observaciones

🔴 Top 5 críticos:
1. CORS AllowAnyOrigin en Program.cs:43
2. Sin autenticación real — login vía query string
3. Backdoor de debug (empleado 964669)
4. Reflection en cada SP para mapear parámetros
5. Sin anti-forgery tokens en POST

📁 Reporte guardado en: CODE_REVIEW.md
Cada hallazgo tiene un checkbox ✅ para marcar al corregirlo.
```

---

## Notas de Implementación

- Lee todos los archivos fuente relevantes; no asumas problemas sin evidencia
- Si el proyecto ya tiene un `CODE_REVIEW.md` previo, pregunta si debe reemplazarlo o actualizarlo
- Adapta el nivel de detalle al tamaño del proyecto (un script de 100 líneas no necesita el mismo rigor que un monolito de 50k líneas)
- Prioriza hallazgos de seguridad sobre todo lo demás
- Si encuentras un `docs/optimizacion-checklist.md` u otro reporte previo, intégralo como referencia pero no dupliques hallazgos
- Usa emojis de severidad consistentemente: 🔴 🟡 🟢 ⚪
- El archivo generado debe ser inmediatamente útil: abrirlo en VS Code debe permitir marcar checkboxes y hacer tracking visual
