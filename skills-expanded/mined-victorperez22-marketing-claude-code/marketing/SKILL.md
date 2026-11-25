# Marketing Claude Code — Orquestador Principal

Sistema de analisis y generacion de contenido de marketing para Claude Code. Pensado para emprendedores, agencias y solopreneurs que necesitan auditar webs, generar copy, diagnosticar funnels, preparar propuestas para clientes y disenar estrategia — todo desde la terminal.

## Tabla de comandos

| Comando                             | Que hace                                                 | Output                         |
| ----------------------------------- | -------------------------------------------------------- | ------------------------------ |
| `/marketing auditoria <url>`        | Auditoria completa de marketing (subagentes en paralelo) | AUDITORIA-MARKETING.md         |
| `/marketing rapido <url>`           | Snapshot de marketing en 60 segundos                     | Salida por terminal            |
| `/marketing copy <url>`             | Genera copy optimizado para cualquier pagina             | Terminal + COPY-SUGERENCIAS.md |
| `/marketing emails <tema/url>`      | Genera secuencias de email                               | SECUENCIAS-EMAIL.md            |
| `/marketing redes <tema/url>`       | Calendario de contenido para redes sociales              | CALENDARIO-REDES.md            |
| `/marketing ads <url>`              | Copy y creatividades para campanas de ads                | CAMPANAS-ADS.md                |
| `/marketing funnel <url>`           | Analisis y optimizacion del funnel de ventas             | ANALISIS-FUNNEL.md             |
| `/marketing competidores <url>`     | Inteligencia competitiva                                 | INFORME-COMPETIDORES.md        |
| `/marketing landing <url>`          | Analisis CRO de landing page                             | LANDING-CRO.md                 |
| `/marketing lanzamiento <producto>` | Playbook de lanzamiento                                  | PLAYBOOK-LANZAMIENTO.md        |
| `/marketing propuesta <cliente>`    | Propuesta comercial para cliente                         | PROPUESTA-CLIENTE.md           |
| `/marketing informe <url>`          | Informe de marketing en Markdown                         | INFORME-MARKETING.md           |
| `/marketing informe-pdf <url>`      | Informe de marketing en PDF                              | INFORME-MARKETING.pdf          |
| `/marketing seo <url>`              | Auditoria SEO de contenido                               | AUDITORIA-SEO.md               |
| `/marketing marca <url>`            | Analisis de voz de marca y guidelines                    | VOZ-MARCA.md                   |

## Logica de routing

Cuando el usuario invoca `/marketing <comando>`, rutea a la sub-skill correspondiente.

### Auditoria completa (`/marketing auditoria <url>`)

Comando estrella. Lanza **5 subagentes en paralelo** que analizan la web de forma simultanea:

1. **marketing-contenido** → Calidad de contenido, messaging, efectividad del copy
2. **marketing-conversion** → CRO, funnels, landing pages, flujos de registro
3. **marketing-competencia** → Posicionamiento competitivo, panorama del mercado
4. **marketing-seo** → SEO tecnico, arquitectura del sitio, rendimiento
5. **marketing-estrategia** → Estrategia global, pricing, oportunidades de crecimiento

**Metodologia de scoring (Marketing Score 0-100):**

| Categoria                   | Peso | Que mide                                                       |
| --------------------------- | ---- | -------------------------------------------------------------- |
| Contenido y Mensaje         | 25%  | Calidad del copy, value props, claridad, persuasion            |
| Optimizacion de Conversion  | 25%  | CTAs, formularios, friccion, social proof, urgencia            |
| SEO y Descubrimiento        | 15%  | SEO on-page, SEO tecnico, estructura de contenido              |
| Posicionamiento Competitivo | 15%  | Diferenciacion, conciencia de mercado, paginas de alternativas |
| Marca y Confianza           | 10%  | Consistencia de marca, senales de confianza, social proof      |
| Crecimiento y Estrategia    | 10%  | Pricing, referral, retencion, expansion                        |

**Por que priorizamos Conversion sobre SEO:** la mayoria de webs B2B en Espana viven de trafico de pago + outbound, no de SEO organico. Fixar conversion tiene impacto directo en revenue a corto plazo; mover SEO requiere meses.

**Marketing Score compuesto** = media ponderada de las 6 categorias.

### Snapshot rapido (`/marketing rapido <url>`)

Evaluacion rapida de 60 segundos. **No** lanzar subagentes. En su lugar:

1. Hacer WebFetch de la homepage
2. Evaluar: claridad del headline, fuerza del CTA, value proposition, senales de confianza, preparacion mobile
3. Devolver un scorecard breve con los 3 mejores puntos y los 3 fixes prioritarios
4. Limitar el output a menos de 30 lineas

### Comandos individuales

Para el resto (`/marketing copy`, `/marketing emails`, etc.), rutear a la sub-skill correspondiente en `skills/marketing-<comando>/SKILL.md`.

## Deteccion del tipo de negocio

Antes de ejecutar cualquier analisis, identifica el tipo de negocio:

- **SaaS/Software** → Foco en: conversion trial-a-paid, onboarding, paginas de features, tiers de pricing
- **E-commerce** → Foco en: fichas de producto, abandono de carrito, upsells, resenas
- **Agencia/Servicios** → Foco en: casos de exito, portfolio, formularios de contacto, senales de confianza
- **Negocio local** → Foco en: Google Business Profile, SEO local, resenas, como llegar
- **Creator/Curso** → Foco en: lead magnets, captura de email, testimonios, comunidad
- **Marketplace** → Foco en: mensaje a dos lados, balance oferta/demanda, mecanismos de confianza

## Estandares de output

Todos los outputs deben cumplir:

1. **Accionable sobre teorico** — Cada recomendacion debe ser suficientemente especifica para implementarse tal cual
2. **Priorizado** — Siempre ordenado por impacto (Alto/Medio/Bajo)
3. **Revenue-focused** — Cada sugerencia conecta con resultados de negocio
4. **Con ejemplos** — Incluir antes/despues del copy, no solo consejos
5. **Listo para cliente** — Los informes deben poderse presentar al cliente sin reescribir

## Salida a fichero

Guardar los outputs detallados como Markdown en el directorio actual:

- Nombres descriptivos: `AUDITORIA-MARKETING.md`, `INFORME-COMPETIDORES.md`, etc.
- Cabecera con URL, fecha y score global
- Estructura con headers y tablas claras
- Resumen ejecutivo al principio en informes para cliente

## Referencias cruzadas entre skills

Muchas skills funcionan mejor encadenadas:

- `/marketing auditoria` invoca todos los subagentes y produce el analisis mas completo
- `/marketing propuesta` puede apoyarse en resultados de auditoria si estan disponibles
- `/marketing informe` e `/marketing informe-pdf` compilan todos los datos de analisis disponibles
- `/marketing copy` mejora si antes se ha corrido `/marketing marca` para fijar la voz
- `/marketing emails` aprovecha insights de `/marketing funnel` si existen
