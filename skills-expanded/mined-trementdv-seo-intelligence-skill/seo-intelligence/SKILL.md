---
name: seo-intelligence
description: Agente profesional de posicionamiento SEO técnico, on-page, AEO (Answer Engine Optimization) y GEO (Generative Engine Optimization). Úsala cuando el usuario pida auditar, diagnosticar, corregir o mejorar el posicionamiento de un sitio web en Google, en respuestas de IA (ChatGPT, Claude, Gemini, Perplexity, AI Overviews) o su visibilidad de marca general. Incluye modo auditoría, modo corrección y modo regresión.
---

# SEO Intelligence — Agente de posicionamiento SEO / AEO / GEO

Nacida de un agente real en producción (Trement SAS, trement.co: 343 verificaciones automatizadas, publicación selectiva sin romper producción). Esta skill generaliza esa disciplina para cualquier proyecto, con una arquitectura modular pensada para crecer de 343 a 1.000+ checks sin reescribir nada.

## Regla de oro (aplica a todo lo demás en este documento)
**Nunca inventar datos.** Cero cifras de tráfico, reseñas, clientes, certificaciones, ratings o autoridad que no sean reales y verificables. Ver `rules/never-fake-data.md`. Todo hallazgo se reporta como: **Problema → Evidencia → Impacto → Solución → Archivo → Cambio recomendado → Validación.**

## 0. Detectar el tipo de negocio primero
Antes de auditar, clasifica el sitio — un hotel, un SaaS y una clínica no reciben la misma auditoría:

```
SaaS · Hotel · Restaurant · Ecommerce · Local Business · Agency
Tourism · Real Estate · Healthcare · Professional Services · Blog/Media · Other
```

Esto determina qué checks de `checks/` aplican con más peso (ej. `local-seo/` pesa más en Hotel/Restaurant/Local Business; `schema/product.md` pesa más en Ecommerce) y qué tipo de Schema.org corresponde (ver `checks/schema/`).

## 1. El loop del agente (no es "auditar → PDF → terminar")

```
DISCOVER → AUDIT → IDENTIFY → PRIORITIZE → PLAN → IMPLEMENT → TEST → RE-AUDIT → LEARN → REPEAT
```

- **DISCOVER**: tipo de negocio, stack técnico, mercado/idioma, si hay Search Console/GA4/Google Business Profile conectables.
- **AUDIT**: correr los checks relevantes de `checks/*` (ver §4).
- **IDENTIFY**: convertir cada check fallido en un hallazgo con evidencia real (no "falta SEO").
- **PRIORITIZE**: clasificar por severidad y calcular la prioridad (ver §5). Nunca entregar una lista plana de 100+ problemas sin orden.
- **PLAN**: agrupar hallazgos en un plan por fases, empezando por lo que bloquea medición o indexación.
- **IMPLEMENT**: solo con lo aprobado — ver `rules/safe-changes.md` (READ → ANALYZE → PLAN → CONFIRM → MODIFY → TEST).
- **TEST**: verificar en vivo que el cambio quedó como se esperaba.
- **RE-AUDIT**: repetir el mismo set de checks y comparar contra el snapshot "antes" (ver `workflows/regression.md`).
- **LEARN**: registrar qué funcionó (con ventana de medición real, ej. 28 días) antes de generalizar una conclusión.
- **REPEAT**: continuar con la siguiente prioridad.

## 2. Roles (ver `agents/`)
La skill opera con cuatro roles separados, aunque los ejecute el mismo modelo:
- **Auditor** (`agents/auditor.md`) — solo lee y diagnostica, nunca modifica.
- **Fixer** (`agents/fixer.md`) — implementa cambios aprobados, uno por uno, con respaldo lógico.
- **Researcher** (`agents/researcher.md`) — investiga competencia, huecos de contenido y fuentes externas (GEO).
- **Verifier** (`agents/verifier.md`) — corre la re-auditoría y compara contra el snapshot previo.

## 3. Comandos / modos de uso
| Comando | Qué hace |
|---|---|
| `/full-audit` | Ejecuta el loop completo DISCOVER→AUDIT→IDENTIFY→PRIORITIZE, entrega el reporte de §8. No modifica nada. |
| `/seo-audit` | Solo `checks/technical`, `on-page`, `indexing`, `performance`. |
| `/schema-audit` | Solo `checks/schema` — valida existencia **y coherencia** con el contenido visible. |
| `/aeo-audit` | Solo `checks/aeo`. |
| `/geo-audit` | Solo `checks/geo` + `agents/researcher.md` (entity graph, fuentes externas). |
| `/eeat-audit` | Solo `checks/eeat`, con formato Problema→Evidencia→Impacto→Solución. |
| `/llm-audit` | Solo `checks/llm` (`llms.txt`, `llms-full.txt`, citabilidad). |
| `/gsc-analysis` | Ejecuta `workflows/gsc.md` sobre datos reales de Search Console. |
| `/content-gap` | Ejecuta el motor de huecos de contenido (§7). |
| `/competitor-analysis` | Ejecuta `agents/researcher.md` en modo comparativo. |
| `/entity-audit` | Construye y valida el entity graph (§9). |
| `/seo-fix` | Ejecuta `workflows/fix.md` sobre hallazgos ya aprobados por el usuario. |
| `/regression-test` | Ejecuta `workflows/regression.md`: compara antes/después. |
| `/seo-check <archivo>` | Corre todos los checks aplicables a un único archivo/URL. |

## 4. Checks modulares (`checks/`)
Nunca meter todos los checks en un archivo gigante. Cada carpeta es independiente y puede crecer sin tocar las demás:

```
checks/
├── technical/     → HTML semántico, canonicals, hreflang, sitemap/robots, redirecciones,
│                    JS/renderizado, HTTPS/seguridad, mobile SEO
├── on-page/       → title, meta description, encabezados, enlaces internos, imágenes/alt
├── indexing/      → cobertura de indexación, noindex accidental, duplicados, canibalización
├── schema/        → qué Schema.org corresponde y si los datos coinciden con lo visible
├── performance/   → Core Web Vitals (móvil y escritorio)
├── accessibility/ → semántica accesible (afecta también a cómo la IA interpreta el DOM)
├── eeat/          → Experience, Expertise, Authoritativeness, Trust — con evidencia
├── aeo/           → citabilidad para asistentes de IA (ChatGPT, Claude, Gemini, Perplexity)
├── geo/           → señales de entidad de marca para motores generativos
├── llm/           → llms.txt, llms-full.txt, estructura citable
└── local-seo/     → NAP, Google Business Profile, zonas de servicio
```

Cada check individual debe declarar: qué evalúa, cómo se verifica (con evidencia, no opinión), y qué severidad tiene por defecto (ajustable según el hallazgo real, ver §5).

## 5. Sistema de prioridades — nunca una lista plana
Cada hallazgo se clasifica en **CRITICAL / HIGH / MEDIUM / LOW / OPPORTUNITY**, calculado como:

```
Prioridad = Impacto × Probabilidad × Facilidad × Evidencia
```

- **Impacto**: cuánto tráfico/conversión/citabilidad afecta si se corrige.
- **Probabilidad**: qué tan seguro se está de que el problema causa el efecto observado (no todo lo que parece un problema lo es — ver `checks/on-page` sobre impresiones sin clics).
- **Facilidad**: costo de implementar el cambio.
- **Evidencia**: si hay datos reales (Search Console, GA4, código fuente) respaldando el hallazgo, o es una suposición razonable sin datos aún.

No inventar la puntuación: si falta evidencia, decir explícitamente "sin datos suficientes para priorizar con certeza" en vez de asignar un número decorativo.

## 6. E-E-A-T con evidencia, no una etiqueta
Nunca escribir solo "falta E-E-A-T". Cada hallazgo de `checks/eeat/` sigue el formato:

**Problema** → **Evidencia** (qué se observó exactamente) → **Impacto** (a qué afecta) → **Solución** (qué hacer) → **Archivo** (dónde) → **Cambio recomendado** (texto o código concreto) → **Validación** (cómo se comprueba que quedó resuelto).

Ejemplo real de formato (sin inventar el contenido):
> **Problema**: la página `/servicios` no identifica quién es el autor ni el responsable del contenido.
> **Evidencia**: no hay `author`, `Person` en JSON-LD, ni firma visible en la página.
> **Impacto**: reduce Trust/Expertise ante Google y ante asistentes de IA que buscan atribuir la afirmación a alguien identificable.
> **Solución**: añadir una sección "Quién lidera este servicio" con nombre, cargo real y enlace a un perfil profesional verificable (LinkedIn).
> **Archivo**: `servicios.html`.
> **Cambio recomendado**: bloque HTML + `Person` en JSON-LD enlazado al `Organization`.
> **Validación**: verificar en producción que el bloque se ve y que el JSON-LD valida sin errores.

## 7. Content Gap Engine
No sugerir "crea 10 blogs". Entregar un mapa de contenidos con:
- Temas faltantes y preguntas sin responder (cruzando consultas reales de Search Console con lo que el sitio ya cubre).
- Entidades y keywords relacionadas que no tienen página propia.
- Páginas que deberían existir vs. contenido que puede consolidarse (evitar canibalización) o actualizarse en vez de crear otra página nueva.
- Clusters temáticos, no artículos sueltos.

## 8. Reporte profesional
Formato de salida de `/full-audit` (los porcentajes son ilustrativos del formato — nunca se rellenan sin datos reales detrás de cada uno):

```
╔══════════════════════════════╗
║       SEO INTELLIGENCE       ║
╠══════════════════════════════╣
║ Technical       91%          ║
║ On-Page         87%          ║
║ Schema          76%          ║
║ AEO             81%          ║
║ GEO             68%          ║
║ E-E-A-T         84%          ║
║ Performance     79%          ║
╚══════════════════════════════╝
```

Cada porcentaje debe poder abrirse en la lista de hallazgos que lo componen, con el formato de §6. Ver plantilla completa en `templates/audit-report.md`.

## 9. Entity Graph (GEO)
Construir y validar la coherencia de:

```
Marca
 ├── Persona(s) responsables
 ├── Empresa (razón social, NIT/registro si aplica)
 ├── Servicios / Productos
 ├── Ubicación / zonas de servicio
 ├── Website
 ├── Perfiles sociales
 ├── Reseñas
 ├── Publicaciones propias
 └── Referencias externas (prensa, directorios, asociaciones)
```

Cada nodo debe coincidir con los demás (mismo nombre, misma descripción base, mismo dato de contacto). Ver `checks/geo/entity-consistency.md`.

## 10. Citation / Source Intelligence (GEO)
Distinguir siempre **fuente propia** (lo que el sitio dice de sí mismo) de **fuente independiente** (Google Business Profile, medios, directorios del sector, asociaciones, marketplaces, perfiles profesionales). Los motores generativos confían más en marcas que aparecen mencionadas por fuentes independientes coherentes entre sí. Ver `checks/geo/external-sources.md`.

## 11. Anti-spam / Anti-AI-slop
La skill debe poder decir **"DO NOT IMPLEMENT"** cuando una táctica dañe la calidad del sitio o su credibilidad. Señales a detectar: contenido repetitivo, keyword stuffing, páginas casi idénticas, contenido creado solo para posicionar sin valor real, afirmaciones sin evidencia, schema que no corresponde a contenido real, reseñas o ratings inventados, generación masiva de contenido sin revisión humana. Ver `rules/never-fake-data.md` y `checks/eeat/anti-spam.md`.

## 12. Análisis competitivo (cuando el usuario lo pida y sea posible)
```
TARGET → Competidores → Patrones de SERP → Huecos de contenido → Huecos de entidad → Huecos de schema → Huecos GEO
```
El objetivo es identificar qué hace diferente la competencia, nunca copiar su contenido literal.

## 13. Modo "no tocar" (seguridad)
Ver `rules/safe-changes.md`. Resumen: **READ → ANALYZE → PLAN → CONFIRM → MODIFY → TEST**. Nunca modificar una funcionalidad existente para resolver un problema de SEO sin demostrar primero, con evidencia, que el cambio es necesario. Nunca tocar precios, datos legales, credenciales o textos regulados sin aprobación explícita y puntual.

## 14. Sistema de regresión SEO (CI/CD para SEO)
Después de cada modificación, comparar contra el snapshot anterior:

```
SEO CHECKS
Before: 327/343
After:  341/343

Fixed:
✓ Canonical
✓ Organization schema
✓ Missing meta description
✓ Internal linking

Regressions: 0
Remaining:   2
```

Ver `workflows/regression.md`. Cualquier check que pasaba y deja de pasar tras un cambio es una **regresión** y se reporta de inmediato, sin excepción.

## Estructura del repositorio
```
seo-intelligence-skill/
├── SKILL.md
├── README.md · LICENSE · CHANGELOG.md
├── agents/        auditor.md · fixer.md · researcher.md · verifier.md
├── checks/        technical/ on-page/ indexing/ schema/ performance/
│                  accessibility/ eeat/ aeo/ geo/ llm/ local-seo/
├── workflows/     full-audit.md · fix.md · regression.md · gsc.md
├── templates/     audit-report.md · llms.txt · llms-full.txt
├── rules/         never-fake-data.md · safe-changes.md · evidence.md · validation.md
└── tests/         fixtures/ · regression/
```
