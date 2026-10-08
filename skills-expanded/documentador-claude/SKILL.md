# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LaTeX documentation for **Proyecto Atlas**, a Smart City platform for the municipality of San Lorenzo de El Escorial (Spain), aligned with the **UNE 178104:2017** standard. Documentation is written in **Spanish**.

This repo contains:
- `manualTecnico/` — Technical architecture manual (active)
- `manualAdministracion/` — Administration manual (pending)

## Building Documents

```bash
# Compile (run twice for TOC and cross-references to resolve)
cd manualTecnico && pdflatex main.tex && pdflatex main.tex

# Automatic recompilation on changes
latexmk -pdf manualTecnico/main.tex

# Clean build artifacts
latexmk -C manualTecnico/main.tex
```

Build artifacts to ignore: `*.aux`, `*.log`, `*.toc`, `*.out`, `*.lof`, `*.lot`, `*.fls`, `*.fdb_latexmk`, `*.synctex.gz`, `*.pdf`

## Auto-generated LaTeX content

Some sections are generated programmatically from source repos. **Never edit generated files by hand.**

| Script | Genera | Fuente |
|---|---|---|
| `node scripts/generate-ontology-latex.js` | `manualTecnico/capitulos/03-modulos/ontologia-generada.tex` | `atlas-messaging-ontology/schemas/**/*.json` |

Run these scripts before compiling when the source repo has changed. The generated files are committed to the repo so the manual compiles without needing the source repos present.

## Document Structure

```
manualTecnico/
├── main.tex                               # Raíz: paquetes, portada, \include de capítulos
├── abstract/abstract.tex                  # Resumen ejecutivo
├── imagenes/                              # Imágenes externas (PNG, PDF)
└── capitulos/
    ├── 01-introduccion/introduccion.tex   # Contexto, UNE 178104, objetivos, tecnologías
    ├── 02-arquitectura/arquitectura.tex   # Visión general, patrones, diagramas TikZ
    ├── 03-modulos/
    │   ├── modulos.tex                    # Microservicios y librerías de infraestructura
    │   └── ontologia-generada.tex         # GENERADO — catálogo de etiquetas AMQP
    ├── 04-infraestructura/infraestructura.tex  # RabbitMQ, MariaDB, Valkey, Ollama, NGINX
    ├── 05-despliegue/despliegue.tex       # Kubernetes on-premise y Azure, entornos
    └── 06-desarrollo/desarrollo.tex      # Guía para extender la plataforma

scripts/
└── generate-ontology-latex.js            # Genera ontologia-generada.tex desde schemas JSON
```

Cada capítulo vive en su propia subcarpeta. Se incluyen desde `main.tex` con `\include{capitulos/XX-nombre/nombre}`. Si un capítulo crece, sus secciones pueden extraerse a ficheros separados usando `\input{}`.

## LaTeX Conventions

- **Diagramas**: usar **TikZ** preferentemente para todos los diagramas (arquitectura, flujos, topología de red). Evitar imágenes externas salvo fotografías o capturas de pantalla.
- **Paquetes cargados en main.tex**: `babel` (español), `listings` (código con coloreado JSON/bash), `booktabs`+`tabularx`+`longtable` (tablas), `amssymb` (`\checkmark`), `hyperref` (enlaces en color `atlasblue`), `fancyhdr` (cabeceras).
- **Color corporativo**: `atlasblue` definido como RGB(0,83,156).
- **Etiquetas**: prefijos por tipo — `\label{cap:nombre}`, `\label{sec:nombre}`, `\label{fig:nombre}`, `\label{tab:nombre}`.
- **Secciones pendientes**: marcar con `% TODO: descripción` para facilitar seguimiento.

## Working Mechanics

El usuario guía qué sección o capítulo escribir en cada sesión. El flujo habitual es:
1. El usuario indica qué parte desarrollar (ej. "escribe la sección de RabbitMQ")
2. Consultar los repositorios del ecosistema Atlas (ver abajo) para obtener datos técnicos reales
3. Escribir contenido preciso y técnico en LaTeX, con diagramas TikZ donde sea relevante
4. Los capítulos esqueleto tienen secciones `% TODO:` que sirven de guía

## Atlas Platform Architecture (reference for writing)

### Ecosistema de repositorios

Los repositorios fuente están en el directorio padre `../`:

| Repositorio | Tecnología | Propósito |
|---|---|---|
| `atlas-api` | Node.js + Fastify 5 | API Gateway REST, puerto 3000 |
| `atlas-cms` | Strapi 5 + MariaDB + Valkey | CMS headless, puerto 1337 |
| `atlas-calendar-scrapping` | Node.js | Scraping de eventos de múltiples fuentes |
| `atlas-service-ollama` | Node.js + Ollama | Microservicio IA: LLM, OCR, embeddings |
| `atlas-messaging-ontology` | JSON Schema + Node.js | Registro centralizado de schemas de mensajes |
| `ferimer-queue-manager` | amqplib | Abstracción RabbitMQ (RPC y Fire-and-Forget) |
| `ferimer-endpoints-manager` | Node.js + AJV | Carga dinámica de endpoints en Fastify |
| `ferimer-database-manager` | MariaDB driver | Abstracción de base de datos |

### Patrones de comunicación (RabbitMQ)

- **RPC** (request-response): `atlas-api` → RabbitMQ → microservicio receiver
- **Fire-and-Forget**: eventos unidireccionales entre servicios
- Clases del queue-manager: `AMQP_RPC_Emitter/Receiver`, `AMQP_FireAndForget_Emitter/Receiver`
- Conversión de tags a routing keys por broker: `:` → `.` (RabbitMQ/Kafka), `:` → `/` (MQTT)

### Ontología de mensajes

Tag format: `<domain>:<category>:<action>[:<subtype>]` — sólo minúsculas, sin guiones.

Dominios activos (v0.0.6): `tools:ai:llm`, `tools:ai:embedding`, `tools:ai:translation`, `tools:ocr:image:file`, `tools:ocr:image:url`

El catálogo completo está en `atlas-messaging-ontology/docs/TAGS.md` (generado con `npm run generate-docs` en ese repo).

### Arquitectura de despliegue (dos entornos Kubernetes)

**On-premise — CPD Ayuntamiento de San Lorenzo de El Escorial:**
- Hardware: 3 servidores físicos + cajón de discos + SAI + tarjetas GPU
- Cluster Kubernetes para microservicios internos y procesamiento IA
- **RabbitMQ interno**: comunicación inter-microservicios (vhost `/atlas`)
- **RabbitMQ IoT + módulo MQTT**: recibe datos de sensores, cámaras y dispositivos IoT distribuidos por la ciudad
- Servicios de IA local con Ollama sobre GPU (modelos: `gemma3`, `deepseek-ocr`, embeddings)
- Proxy inverso: **NGINX**

**Cloud — VPS Azure:**
- Cluster Kubernetes para servicios de cara al público
- Web de turismo, CMS (Strapi), APIs públicas
- **RabbitMQ cloud**: comunicaciones con el CMS y servicios Azure
- Proxy inverso: **NGINX**

Todos los microservicios se despliegan como pods **stateless y desacoplados**. El estado persiste en MariaDB, Valkey o almacenamiento externo, nunca en el pod.

### Infraestructura de soporte

| Servicio | Tecnología | Entorno | Puerto |
|---|---|---|---|
| Base de datos | MariaDB 11.x | Ambos | 3306 |
| Caché | Valkey 8 (Redis-compat.) | Ambos | 6379 |
| Message broker | RabbitMQ 3.x | Ambos (3 instancias) | 5672 |
| IoT/MQTT broker | RabbitMQ + plugin MQTT | On-premise | 1883 |
| IA local | Ollama | On-premise | 11434 |
| Proxy inverso | NGINX | Ambos | 80/443 |
