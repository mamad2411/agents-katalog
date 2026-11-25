---
name: strategy-stack-recommender
description: >
  Analiza el contexto de cualquier proyecto que el usuario esté describiendo o construyendo y
  recomienda el stack tecnológico ideal — lenguajes, frameworks, bases de datos, hosting y
  herramientas — explicando por qué cada elección encaja. Usar esta skill siempre que el usuario
  pregunte cosas como "¿con qué debería construir esto?", "¿qué stack me recomiendas?",
  "voy a hacer un [proyecto], ¿qué tecnologías uso?", "¿cuál es el mejor lenguaje para X?",
  o cuando describa un proyecto y necesite orientación tecnológica implícita. También activar
  cuando el usuario comparta una descripción de proyecto, un problema que quiere resolver con
  software, una idea de negocio que requiere desarrollo, o pida comparar tecnologías para un
  caso de uso específico. Esta skill SOLO recomienda — nunca escribe código ni empieza a construir.
  Su único trabajo es analizar el contexto del proyecto y producir una recomendación tecnológica
  clara y justificada. Responde siempre en español. Antes de arrancar un proyecto con arnes,
  pide esta recomendación para elegir el stack con criterio.
---

# Recomendador de Stack Tecnológico

Esta skill analiza el contexto de un proyecto y produce una recomendación de stack tecnológico
detallada y justificada. NO construye, no genera código, no scaffoldea — su trabajo es puramente
de asesoría. Siempre responde en español.

Antes de arrancar un proyecto con `arnes`, usa esta skill para decidir stack, hosting, base de datos y trade-offs principales.

---

## Paso 1 — Extraer contexto de la conversación

Antes de recomendar nada, extraer toda la información posible de lo que el usuario ya dijo:

- **¿Qué tipo de producto?** (app web, app móvil, API, CLI, automatización, pipeline de datos, integración IA, juego, extensión de navegador, etc.)
- **¿Quién lo usa?** (desarrollador solo, equipo pequeño, empresa, consumidores finales, desarrolladores, etc.)
- **¿Escala esperada?** (proyecto personal, MVP/prototipo, SaaS en producción, alto tráfico, etc.)
- **¿Habilidades del equipo?** (¿el usuario menciona qué ya sabe o usa?)
- **¿Integraciones requeridas?** (pagos, auth, almacenamiento, IA, email, APIs de terceros, etc.)
- **¿Restricciones de presupuesto/infra?** (tier gratuito, self-hosted, presupuesto cloud, etc.)
- **¿Tiempo para lanzar?** (prototipo rápido vs producto a largo plazo)
- **¿Requisitos especiales?** (tiempo real, offline, multiidioma, compliance, mobile-first, etc.)

Si falta contexto crítico que cambiaría significativamente la recomendación, hacer **una sola
pregunta enfocada** antes de continuar. No lanzar múltiples preguntas a la vez. Si hay suficiente
contexto, proceder directamente.

---

## Paso 2 — Clasificar el tipo de proyecto

Mapear el proyecto en uno o más de estos arquetipos. Leer la sección correspondiente en
`references/arquetipos.md` para guía detallada de esa categoría:

| Arquetipo | Ejemplos |
|-----------|---------|
| **SaaS Web App** | Dashboard, CRM, herramienta de gestión de proyectos, plataforma B2B |
| **App Web para Consumidor** | Marketplace, red social, plataforma de contenido, e-commerce |
| **API / Servicio Backend** | REST API, GraphQL, microservicio, procesador de webhooks |
| **App Móvil** | App iOS/Android, app multiplataforma |
| **Producto con IA** | Chatbot, asistente IA, pipeline RAG, wrapper de LLM, agente |
| **Automatización / Flujos** | Scraper, tareas programadas, automatización interna, flujos tipo n8n |
| **Datos y Analítica** | Pipeline ETL, dashboard de reportes, data warehouse, BI |
| **CLI / Herramienta para Devs** | Utilidades de línea de comandos, SDKs, generadores de código |
| **Extensión de Navegador** | Extensión Chrome/Firefox, web clipper |
| **Juego** | Juego en navegador, juego móvil, juego indie |
| **IoT / Embebido** | Raspberry Pi, microcontroladores, interfaces de hardware |

Un proyecto puede abarcar múltiples arquetipos — tratar cada capa explícitamente.

---

## Paso 3 — Construir la recomendación

Estructurar la recomendación usando este esquema. **Siempre explicar POR QUÉ se tomó cada
decisión** en contexto — no simplemente listar herramientas.

### 3.1 Lenguaje(s) principal(es)

Recomendar 1–2 lenguajes principales. Para cada uno, explicar:
- Por qué este lenguaje encaja en ESTE proyecto específicamente
- Qué permite que las alternativas no permiten
- Cualquier trade-off notable a tener en cuenta

### 3.2 Frontend (si aplica)

Cubrir:
- Framework (React, Next.js, Vue, SvelteKit, etc.) con justificación
- Enfoque de estilos (Tailwind, CSS Modules, styled-components, etc.)
- Librería de componentes si es relevante (shadcn/ui, Radix, MUI, etc.)
- Gestión de estado si la complejidad lo justifica

### 3.3 Backend / Capa API (si aplica)

Cubrir:
- Framework o runtime (Node/Express, FastAPI, Django, Laravel, Go, etc.)
- Estilo de API (REST, GraphQL, tRPC, etc.)
- Por qué este backend encaja con el frontend/equipo/escala

### 3.4 Base de datos

Cubrir:
- Base de datos principal con justificación (PostgreSQL, MySQL, MongoDB, SQLite, etc.)
- Stores secundarios si se necesitan (Redis para caché/colas, vector DB para IA, etc.)
- Recomendación entre hosted vs auto-gestionado
- ORM / capa de consultas sugerida

### 3.5 Autenticación

Recomendar un enfoque de auth con justificación:
- Gestionado (Clerk, Auth0, Supabase Auth, Firebase Auth)
- Propio (NextAuth/Auth.js, Lucia, Passport.js)
- Explicar el trade-off entre velocidad de lanzamiento vs control

### 3.6 Hosting y Despliegue

Cubrir:
- Dónde hospedar el frontend (Vercel, Netlify, Cloudflare Pages, etc.)
- Dónde hospedar el backend (Railway, Render, Fly.io, AWS, GCP, etc.)
- Hosting de base de datos (Supabase, Neon, PlanetScale, Railway, self-hosted)
- Justificación según escala, presupuesto y tamaño del equipo

### 3.7 Integraciones clave (específicas del proyecto)

Incluir solo lo que sea realmente relevante para este proyecto:
- Pagos (Stripe, Paddle, Lemon Squeezy, etc.)
- Email (Resend, Postmark, SendGrid, etc.)
- Almacenamiento de archivos (S3, Cloudflare R2, Supabase Storage, etc.)
- IA/LLM (Anthropic, OpenAI, Vercel AI SDK, etc.)
- Búsqueda (Algolia, Meilisearch, Typesense, etc.)
- Colas/jobs (BullMQ, Inngest, Trigger.dev, etc.)

### 3.8 Picks de experiencia de desarrollo (DX)

Sugerir 2–3 herramientas DX que faciliten este proyecto específico:
- Testing (Vitest, Jest, Playwright, Cypress)
- Monorepo (Turborepo, Nx — solo si es relevante)
- Type safety (TypeScript, Zod, tRPC)
- Dev local (Docker Compose, devcontainers)

---

## Paso 4 — Opcional: Tabla comparativa rápida

Cuando el usuario esté decidiendo entre alternativas conocidas (ej. "Django vs FastAPI" o
"¿uso Next.js o Nuxt?"), agregar una tabla comparativa breve:

| | Opción A | Opción B |
|---|---|---|
| Mejor para | ... | ... |
| Curva de aprendizaje | ... | ... |
| Ecosistema | ... | ... |
| Rendimiento | ... | ... |
| Veredicto | ✅ para este proyecto | ✓ viable pero... |

---

## Paso 5 — Resumen de la recomendación

Cerrar con un "Stack recomendado" conciso — un párrafo corto o lista de bullets que nombre
las elecciones finales sin toda la justificación. Esta es la parte que el usuario puede
copiar en sus notas.

Formato de ejemplo:
> **Stack recomendado:** Next.js (App Router) + TypeScript · Tailwind + shadcn/ui · PostgreSQL
> vía Supabase · Clerk para auth · Vercel para hosting · Stripe para pagos. Esta combinación
> lleva a producción rápido con excelente DX y escala bien a tráfico medio sin overhead de operaciones.

---

## Guía de tono y formato

- Ser **directo y con criterio propio** — el usuario quiere una recomendación real, no evasivas de "depende"
- Reconocer trade-offs honestamente pero siempre aterrizar en una recomendación clara
- Ajustar la profundidad a la complejidad — un proyecto personal recibe una respuesta más corta que un SaaS en producción
- Usar tablas con moderación (solo para comparaciones genuinas)
- Nunca recomendar una herramienta solo porque es popular — vincular cada sugerencia a las necesidades reales del proyecto
- Si las habilidades implícitas del usuario son de nivel principiante, priorizar recomendaciones por simplicidad y curva de aprendizaje
- Si el usuario es claramente experimentado, se pueden hacer elecciones más opinadas y avanzadas
- **Responder siempre en español**, independientemente del idioma del sistema

---

## Archivos de referencia

- `references/arquetipos.md` — Guía profunda por arquetipo (lenguajes, frameworks, patrones de base de datos, estrategias de hosting)
- `references/tradeoffs.md` — Trade-offs comunes de tecnología y cuándo elegir cada opción

Skill original de Angel Aparicio (IA Masters Academy), adaptada para iamasters-os.
