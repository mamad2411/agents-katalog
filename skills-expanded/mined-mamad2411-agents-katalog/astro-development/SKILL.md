---
name: astro-development
description: Desarrollo de la landing en Astro — arquitectura de islas y directivas `client:*` (`load`/`idle`/`visible`/`only`), colecciones de contenido tipadas, salida estática vs on-demand (`output` y `prerender`), manejo de assets y cero JS por defecto. Usar al construir o modificar la landing/sitio de marketing, al agregar una isla interactiva, al modelar contenido en colecciones, o al decidir qué va en Astro y qué en la app Angular.
---

# Astro — landing y sitio de contenido

Astro es para sitios centrados en contenido (landing, marketing, blog): renderiza a HTML y
envía **cero JavaScript por defecto**. La app de producto (con estado, auth, datos) vive en
Angular; Astro es la vitrina rápida.

## 1. Cuándo Astro y cuándo la app Angular

| Va en Astro | Va en la app Angular |
|---|---|
| Landing, precios, "sobre nosotros", blog | Áreas logueadas, agenda, ficha clínica |
| Contenido mayormente estático | Estado rico, formularios complejos, datos en vivo |
| Prioridad SEO + carga instantánea | Interacción intensa y sesión |

No reconstruyas el producto en Astro ni metas la landing dentro de la SPA: cada uno donde rinde.

## 2. Islas y directivas `client:*`

Los componentes `.astro` no envían JS. Solo las "islas" (componentes de framework con una
directiva `client:*`) se hidratan, y solo esas. Elegí la directiva por urgencia real:

```astro
---
import Newsletter from '../components/Newsletter.jsx';
import Faq from '../components/Faq.svelte';
---
<Newsletter client:visible />   <!-- hidrata al entrar en viewport -->
<Faq client:idle />             <!-- hidrata cuando el navegador está ocioso -->
```

| Directiva | Hidrata | Usar para |
|---|---|---|
| `client:load` | En cuanto carga la página | Interacción crítica visible de entrada |
| `client:idle` | Cuando el navegador queda ocioso | Interacción no urgente |
| `client:visible` | Al entrar al viewport | Islas más abajo en la página |
| `client:only="<fw>"` | Solo en cliente, sin render en servidor | Componentes que dependen del navegador |

Regla: la mínima hidratación posible. Todo lo que no sea interactivo queda como HTML estático.

## 3. Colecciones de contenido

Modelá el contenido (posts, features, testimonios) como colecciones tipadas con un esquema.
Ganás validación en build y tipos al consultarlas.

```typescript
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
const posts = defineCollection({
  schema: z.object({ title: z.string(), date: z.date(), draft: z.boolean().default(false) }),
});
export const collections = { posts };
```

Consultá con `getCollection('posts')` y filtrá los `draft` en producción.

## 4. Salida estática vs on-demand

- Por defecto Astro genera un sitio **estático** en build: lo ideal para la landing.
- Si necesitás render on-demand (SSR) en algunas rutas, configurás `output: 'server'` con un
  adaptador y marcás las páginas estáticas con `export const prerender = true`. Mantené
  estático todo lo que pueda serlo.
- La estrategia de deploy (build estático servido, o Node para SSR) la fija `coolify-deployment`.

## 5. Assets y rendimiento

- Poné imágenes en el pipeline de assets de Astro para optimización y tamaños responsivos;
  no referencies binarios grandes sin procesar.
- Como el JS por defecto es cero, el rendimiento sale casi gratis: no lo arruines metiendo
  islas `client:load` innecesarias. Verificá Core Web Vitals (`frontend-performance`).
- SEO: aprovechá el HTML estático para títulos, meta y JSON-LD por página (ver `seo-public-pages`).

## Anti-patrones

- Marcar todo con `client:load` (mata la ventaja de Astro).
- Contenido en archivos sueltos sin esquema en vez de colecciones tipadas.
- SSR global cuando el sitio podía ser estático.
- Duplicar la app de producto o la sesión en la landing.
- Imágenes sin optimizar fuera del pipeline de assets.

## Checklist

- [ ] Solo las islas realmente interactivas llevan `client:*`, con la directiva mínima.
- [ ] Contenido en colecciones con esquema; borradores filtrados en producción.
- [ ] Estático por defecto; `prerender` explícito si hay `output: 'server'`.
- [ ] Imágenes por el pipeline de assets; Core Web Vitals en verde.
- [ ] SEO por página resuelto (ver `seo-public-pages`).
- [ ] La frontera Astro/Angular respetada.
