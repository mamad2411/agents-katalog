---
name: arch-discover
description: Inspeccionar un proyecto existente para descubrir decisiones arquitectónicas implícitas y las reglas/convenciones vivas que están en vigor, y proponer los ADR y estándares candidatos que las documentarían. Usar cuando el usuario quiera auditar un repositorio en busca de decisiones o normas no documentadas, pida "descubrir ADRs", "descubrir estándares", "qué decisiones arquitectónicas tiene este proyecto", "qué convenciones sigue el código", "analiza la arquitectura del proyecto" o cualquier variante que implique explorar el código/estructura para inferir arquitectura relevante que merezca documentarse. Activar también cuando el usuario llegue a un proyecto nuevo y quiera entender qué decisiones y reglas ya existen, aunque no mencione explícitamente "ADR" o "estándar".
license: MIT
---

# Skill: Descubrir arquitectura en un proyecto existente

Analiza la estructura y el código de un repositorio para identificar **arquitectura implícita** —
elecciones de tecnología, patrones, convenciones o compromisos que están vivos en el código pero
nunca se documentaron formalmente.

Cada hallazgo se traduce en artefactos de dos tipos (ver el skill `arch-manage` para la distinción completa):

- Un **ADR** — la *decisión* histórica: por qué se eligió algo. Todo hallazgo relevante produce un ADR candidato.
- Un **requisito** dentro de un **estándar de dominio** — la *regla viva* que el código sigue hoy (`docs/standards/`). El estándar es **amplio** (un **dominio técnico o funcional** entero: *Testing Standards*, *API Standards*…; un aspecto de arquitectura, no un dominio de negocio/DDD) y agrupa varios requisitos; cada requisito se redacta con RFC 2119/8174 (MUST/SHOULD/MAY…). Un hallazgo que es una norma continua y verificable propone **un requisito**, dentro del estándar de dominio que le corresponde (agrupándolo con otros del mismo dominio). La unidad verificable fina —el **criterio de cumplimiento** (`CR-XXX`), que pertenece a un requisito pero vive en la tabla única del estándar— la propone `arch-manage` al crear el artefacto, para que el usuario elija cuáles crear; en descubrimiento basta con proponer el requisito y su regla.

Ejemplo: detectar "unit tests con PHPUnit" y "e2e con Playwright" son **dos decisiones** (dos ADR),
pero **un solo estándar de dominio** *Testing Standards* con **dos requisitos** («Unit testing»,
«E2E testing»). En cambio detectar "hubo una migración de Webpack a Vite" es una decisión histórica
(**ADR** sin criterio de cumplimiento): no hay una norma continua que cumplir, solo un hecho.

El output es una **lista priorizada de candidatos**, agrupando los requisitos por estándar de dominio.
El usuario decide cuáles documentar; el skill luego invoca `arch-manage` para cada uno aprobado, que
crea el ADR y —cuando aplique— añade su requisito al estándar de dominio (creándolo o ampliándolo).
Este skill es **autocontenido**: cuando se invoca (directamente o como subagente desde otro skill,
p. ej. `arch-init`), corre sus cinco fases hasta el final, incluida la creación de los artefactos
aprobados — nadie más los vuelve a crear después.

---

## Resolución de idioma

Decidir el idioma de los mensajes al usuario y de lo que se le pasa a `arch-manage` en este orden;
detenerse en el primer paso que aplique:

1. Si en el contexto de la sesión existe una preferencia de idioma del usuario, usarla.
2. Si hay una preferencia registrada en `.agents/MEMORY.md` (línea `preferred language: <código>`), usarla.
3. Si no, usar el idioma del mensaje del usuario y preguntar si desea persistir esa preferencia en `.agents/MEMORY.md`.
4. Si no se puede inferir, **preguntar** qué idioma prefiere; no decidir el idioma por cuenta propia.

---

## Fase 1 — Orientación inicial

Antes de inspeccionar, determinar el alcance:

1. **Leer `AGENTS.md`** (si existe, sección `## Stack tecnológico`) y **`.agents/MEMORY.md`** (si existe, idioma y contexto operativo) para entender lo ya conocido — el stack vive solo en `AGENTS.md`, no se duplica en `MEMORY.md`.
2. **Leer `docs/adr/` y `docs/standards/`** para listar los artefactos ya existentes — nunca proponer un candidato que duplique un ADR o estándar existente (en cualquier estado).
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

### 2d. Artefactos existentes
```bash
ls docs/adr/*.md docs/standards/*.md 2>/dev/null || echo "No hay ADRs ni estándares"
```
Para cada uno, leer solo lo clave (`## Decisión` de los ADR; el `title`/`domain` y los requisitos `## <…>` de los estándares); no cargar el documento completo si hay muchos.

---

## Fase 3 — Identificación de candidatos

Para cada señal encontrada, evaluar si amerita documentarse usando estos criterios:

**Incluir como candidato si:**
- Es una elección no obvia entre varias alternativas reales (ej: Redux vs Zustand, REST vs GraphQL)
- Tiene consecuencias que afectan a múltiples partes del sistema
- Sería costoso revertir sin una razón documentada
- Un desarrollador nuevo podría cuestionarla razonablemente

**Excluir si:**
- Ya está cubierta por un ADR o por un requisito de estándar existente
- Es la opción por defecto obvia del stack (ej: usar Jest en un proyecto CRA)
- Es una decisión de implementación, no arquitectónica

### Clasificar cada candidato: ¿fija un requisito? ¿de qué dominio técnico/funcional?

Por cada candidato, además de la decisión (ADR), determinar si hay una **regla viva** que documentar como **requisito** dentro de un **estándar de dominio**:

- **Decisión + requisito** — el código sigue hoy una norma continua y verificable (p. ej. "las APIs son GraphQL", "el dominio no importa infraestructura", "unit tests con PHPUnit"). Proponer el ADR **y** el requisito, indicando **a qué estándar de dominio pertenece** (agrupándolo con otros candidatos del mismo dominio bajo un solo estándar).
- **Solo decisión (ADR)** — una elección histórica o puntual sin una regla continua que cumplir (una migración ya ejecutada, la adopción inicial de un runtime). Proponer solo el ADR.

**Agrupar por dominio:** varios candidatos del mismo dominio se consolidan en **un** estándar. P. ej. "unit tests con PHPUnit" + "e2e con Playwright" + "cobertura ≥ 80%" → un estándar *Testing Standards* con tres requisitos.

### Categorías / dominios típicos a buscar

Leer [`references/functional-domains.md`](references/functional-domains.md) para el catálogo completo
de los nueve **dominios funcionales canónicos** (los mismos que usa `arch-manage`) y clasificar cada
candidato en uno de ellos — proponer un dominio nuevo solo si de verdad no encaja en ninguno.

---

## Fase 4 — Presentación de candidatos

Leer [`references/candidate-presentation.md`](references/candidate-presentation.md) para el formato
exacto (con ejemplo) en el que se muestra la lista al usuario, agrupada por prioridad (🔴 alta / 🟡
media / ⚪ baja) e indicando a qué estándar de dominio aportaría cada requisito. Al final de la lista,
preguntar con la herramienta de preguntas estructuradas cuáles documentar (esa referencia trae la
pregunta exacta y sus opciones).

---

## Fase 5 — Creación de los artefactos aprobados

Por cada candidato aprobado por el usuario:

1. Invocar el skill `arch-manage` pasando como contexto:
   - El título sugerido de la decisión
   - La evidencia encontrada (como contexto para el `## Contexto` del ADR)
   - La decisión inferida
   - **Si fija un requisito:** el enunciado de la regla en lenguaje RFC 2119 y **el estándar de dominio** al que pertenece (para que `arch-manage` cree o amplíe ese estándar)
   - Las alternativas implícitas detectadas (si las hay)
   - Los **Decisores** y el **idioma**, acordados una sola vez para todo el lote, de modo que `arch-manage` no vuelva a preguntar lo mismo por cada artefacto

2. Dejar que `arch-manage` ejecute su flujo completo: crea el ADR y, cuando corresponda, añade el requisito al estándar de dominio (creándolo o ampliándolo), **propone los criterios de cumplimiento candidatos con su mecanismo de verificación para que el usuario elija cuáles crear**, escribe los seleccionados como `CR-XXX` con su `Enfoque` (bloqueante/warning), enlaza `emits` (a nivel de CR) / `source_adrs` y crea las fitness functions elegidas. En lote, esa propuesta y selección se presenta **una sola vez para todos los candidatos aprobados** (una tabla con columna `Estándar`), no una por artefacto.

3. **Agrupar por dominio en el lote:** procesar juntos los candidatos del mismo dominio para que sus requisitos caigan en el **mismo** estándar (no crear un estándar por candidato).

   **Propuesta de criterios, una sola vez para el lote.** Los ADR y los bloques de requisito se crean candidato a candidato, pero la **propuesta y selección de los criterios de cumplimiento** (con su mecanismo de verificación) se acumula y se presenta **al final del lote**, en una sola tabla con columna `Estándar`, con una única tanda de preguntas. No lanzar la selección por cada candidato.

4. Una vez creado cada artefacto, continuar con el siguiente candidato aprobado.

Este skill no deja candidatos "aceptados pero pendientes de crear": todo lo que el usuario aprueba en
la Fase 4 queda creado al final de la Fase 5, en la misma ejecución. Un skill que invoque `arch-discover`
como subagente (p. ej. `arch-init`) debe dejarlo correr hasta aquí — no hay un modo que se detenga antes.

---

## Notas de comportamiento

- **No inventar decisiones ni reglas.** Si la evidencia es ambigua, mencionar la incertidumbre en "Evidencia" y marcarlo como baja prioridad.
- **No proponer artefactos triviales.** "Usamos Git" no es un ADR.
- **No repetir trabajo.** Si ya existe un ADR o un requisito de estándar que cubre el hallazgo, omitir el candidato y mencionarlo en un pie de página: "X hallazgos omitidos por estar ya documentados."
- **Distinguir decisión de regla, y agrupar por dominio.** No todo ADR fija un requisito; proponer requisito solo cuando hay una norma continua y verificable. Consolidar los requisitos del mismo dominio en un solo estándar (no un estándar por regla).
- **Priorizar calidad sobre cantidad.** Mejor 4 candidatos sólidos que 12 rellenos.

---

## Archivos del skill (contexto progresivo)

Este `SKILL.md` contiene el flujo completo de las cinco fases. El catálogo de dominios y el formato de
presentación están en `references/`; **leerlos solo cuando la fase correspondiente lo pida**:

- [`references/functional-domains.md`](references/functional-domains.md) — catálogo de los 9 dominios funcionales canónicos. Leer en la Fase 3, al clasificar el dominio de cada candidato.
- [`references/candidate-presentation.md`](references/candidate-presentation.md) — formato y ejemplo completo para presentar la lista de candidatos al usuario. Leer en la Fase 4.
