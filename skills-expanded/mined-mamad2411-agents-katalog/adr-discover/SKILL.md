---
name: adr-discover
description: Inspeccionar un proyecto existente para descubrir decisiones arquitectónicas implícitas y proponer ADRs candidatos. Usar cuando el usuario quiera auditar un repositorio en busca de decisiones no documentadas, pida "descubrir ADRs", "qué decisiones arquitectónicas tiene este proyecto", "busca ADRs en el repo", "analiza la arquitectura del proyecto" o cualquier variante que implique explorar el código/estructura para inferir decisiones relevantes que merezcan un ADR. Activar también cuando el usuario llegue a un proyecto nuevo y quiera entender qué decisiones ya se tomaron, aunque no mencione explícitamente "ADR".
---

# Skill: Descubrir ADRs en un proyecto existente

Analiza la estructura y el código de un repositorio para identificar **decisiones arquitectónicas implícitas** — elecciones de tecnología, patrones, convenciones o compromisos que están vivos en el código pero nunca se documentaron formalmente.

El output es una **lista priorizada de ADRs candidatos**. El usuario decide cuáles crear; el skill luego invoca `adr-manage` para cada uno aprobado.

---

## Fase 1 — Orientación inicial

Antes de inspeccionar, determinar el alcance:

1. **Leer `.agents/MEMORY.md`** (si existe) para entender el stack y contexto ya conocido.
2. **Leer `docs/adr/`** para listar los ADRs ya existentes — nunca proponer un candidato que duplique uno existente (`Accepted`, `Proposed` o `Draft`).
3. Si el usuario no indicó ruta, asumir raíz del repositorio actual.

---

## Fase 2 — Inspección del proyecto

Explorar en este orden, acumulando señales:

### 2a. Estructura de carpetas
```bash
find . -maxdepth 3 -type d | grep -v node_modules | grep -v .git | grep -v __pycache__
```
Inferir: monorepo vs monolito, separación por capas/dominios, presencia de módulos, microservicios, etc.

### 2b. Manifiestos de dependencias
Leer **todos** los que apliquen según el stack detectado:

| Ecosistema | Archivos a leer |
|---|---|
| Node / JS / TS | `package.json`, `package-lock.json`, `tsconfig.json` |
| Python | `pyproject.toml`, `requirements.txt`, `setup.cfg`, `Pipfile` |
| JVM | `pom.xml`, `build.gradle`, `build.gradle.kts` |
| .NET | `*.csproj`, `*.sln` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |

Señales clave a extraer:
- Framework web principal (Express, FastAPI, Spring, etc.)
- ORM / cliente de base de datos
- Bus de mensajes / queue
- Herramientas de test
- Bundler / transpilador
- Librerías de autenticación / autorización
- Clientes de servicios cloud

### 2c. Código fuente — patrones arquitectónicos
Buscar evidencia de patrones en el código:

```bash
# Detectar estructura de capas
find src -type d | head -30

# Buscar patrones de diseño comunes
grep -r "Repository\|Service\|Controller\|Handler\|UseCase\|Interactor" src --include="*.ts" --include="*.py" --include="*.java" -l 2>/dev/null | head -20

# Detectar uso de inyección de dependencias
grep -r "inject\|Injectable\|@Autowired\|provide\|container" src -l 2>/dev/null | head -10
```

### 2d. ADRs existentes
```bash
ls docs/adr/*.md 2>/dev/null || echo "No hay ADRs"
```
Para cada ADR existente, leer solo el título y la sección `## Decisión` (no cargar el documento completo si hay muchos).

---

## Fase 3 — Identificación de candidatos

Para cada señal encontrada, evaluar si amerita un ADR usando estos criterios:

**Incluir como candidato si:**
- Es una elección no obvia entre varias alternativas reales (ej: Redux vs Zustand, REST vs GraphQL)
- Tiene consecuencias que afectan a múltiples partes del sistema
- Sería costoso revertir sin una razón documentada
- Un desarrollador nuevo podría cuestionarla razonablemente

**Excluir si:**
- Ya está cubierta por un ADR existente
- Es la opción por defecto obvia del stack (ej: usar Jest en un proyecto CRA)
- Es una decisión de implementación, no arquitectónica

### Categorías típicas a buscar

| Categoría | Ejemplos de señales |
|---|---|
| **Lenguaje / runtime** | TypeScript strict, versión de Node/Python, uso de Deno/Bun |
| **Arquitectura general** | Capas (controller/service/repo), DDD, hexagonal, CQRS |
| **Persistencia** | Elección de BD, ORM vs query builder, estrategia de migraciones |
| **API / protocolo** | REST vs GraphQL vs tRPC, versioning de API |
| **Autenticación** | JWT vs sesiones, proveedor OAuth, manejo de refresh tokens |
| **Estado / UI** | Gestión de estado global, SSR vs CSR, design system |
| **Testing** | Estrategia de tests (unit/integration/e2e), mocking approach |
| **Observabilidad** | Logger elegido, estrategia de errores, tracing |
| **Modularidad** | Monorepo strategy, barrel exports, límites de módulo |
| **CI/CD** | Pipeline elegido, estrategia de deploy, feature flags |

---

## Fase 4 — Presentación de candidatos

Mostrar la lista al usuario en este formato:

```
## ADRs Candidatos Descubiertos

### 🟢 Alta prioridad (decisiones con amplio impacto)

**[C-01] Uso de TypeScript en modo strict**
- Evidencia: `tsconfig.json` con `"strict": true`
- Por qué es una decisión: afecta toda la experiencia de desarrollo y la curva de onboarding
- ADR existente: ninguno

**[C-02] Arquitectura en capas (Controller → Service → Repository)**
- Evidencia: estructura de carpetas `src/controllers/`, `src/services/`, `src/repositories/`
- Por qué es una decisión: define los límites de responsabilidad en todo el sistema
- ADR existente: ninguno

### 🟡 Media prioridad (decisiones relevantes, alcance acotado)

**[C-03] Uso de Prisma como ORM**
- Evidencia: `@prisma/client` en `package.json`, carpeta `prisma/`
- Por qué es una decisión: alternativa a TypeORM, Drizzle, Sequelize — no es la única opción
- ADR existente: ninguno

### ⚪ Baja prioridad (convenciones, menor impacto)

**[C-04] ESLint + Prettier para linting y formato**
- Evidencia: `.eslintrc.js`, `.prettierrc`
- Por qué es una decisión: establece el estándar de calidad de código del equipo
- ADR existente: ninguno

---
Total: X candidatos encontrados. ¿Cuáles quieres documentar como ADR?
```

Tras mostrar la lista, preguntar:

> "¿Cuáles candidatos quieres crear como ADR? Puedes indicarlos por código (C-01, C-03…), por rango (C-01 a C-04), o decir 'todos los de alta prioridad'."

---

## Fase 5 — Creación de ADRs aprobados

Por cada candidato aprobado por el usuario:

1. Invocar el skill `adr-manage` pasando como contexto:
   - El título sugerido
   - La evidencia encontrada (como contexto para la sección `## Contexto`)
   - La decisión inferida
   - Las alternativas implícitas detectadas (si las hay)

2. Dejar que `adr-manage` ejecute su flujo completo (incluyendo preguntar decisores, estado, etc.).

3. Una vez creado cada ADR, continuar con el siguiente candidato aprobado.

---

## Notas de comportamiento

- **No inventar decisiones.** Si la evidencia es ambigua, mencionar la incertidumbre en la columna "Evidencia" y marcarlo como baja prioridad.
- **No proponer ADRs triviales.** "Usamos Git" no es un ADR.
- **No repetir trabajo.** Si ya existe un ADR que cubre la decisión, omitir el candidato y mencionarlo en un pie de página: "X decisiones omitidas por estar ya documentadas."
- **Priorizar calidad sobre cantidad.** Mejor 4 candidatos sólidos que 12 rellenos.
- **Idioma:** seguir la convención de `.agents/MEMORY.md`; si no existe, usar el idioma del mensaje del usuario.