---
name: seo-basico
description: Revisa y corrige el SEO básico de un sitio construido o en línea - title y meta description por página, un h1, lang, canonical, Open Graph, imágenes sin alt, enlaces internos rotos, títulos repetidos, robots.txt y sitemap - y explica cómo avisar a los buscadores. Úsalo cuando la persona pida revisar el SEO, preparar el sitio para Google o Bing, mejorar cómo se ve un link compartido, o antes de publicar.
argument-hint: "[carpeta del build | URL del sitio]"
---

# SEO básico

No prometes posiciones. Te aseguras de que **los buscadores puedan leer y entender cada página**
y de que un link compartido se vea bien. Eso es lo que un sitio de diseñador suele tener mal.

## 1. Revisa
- Sitio local: `npm run build` y luego
  `node ${CLAUDE_SKILL_DIR}/scripts/seo.mjs --dist dist` (o la carpeta de salida del framework).
- Sitio publicado: `node ${CLAUDE_SKILL_DIR}/scripts/seo.mjs --url https://tusitio.com --max 40`.

El script reporta por página: `title` (30–60 caracteres), `meta description` (70–160), un solo
`h1`, `lang`, `canonical`, Open Graph (`og:title`, `og:description`, `og:image` con URL
absoluta), imágenes sin `alt`, enlaces sin texto, enlaces internos rotos y `noindex` donde no
corresponde; y en el sitio: títulos o descripciones repetidos, `robots.txt` (que exista, que no
bloquee todo y que apunte al sitemap) y sitemap (y que no use `example.com`).

## 2. Corrige en la fuente, no en el HTML generado
- Busca el componente que arma el `<head>` (en Astro, un `Seo.astro` o el layout; en Next.js,
  `metadata` o `generateMetadata`) y corrige ahí.
- **Title:** «Qué es esta página · Marca». Único por página.
- **Description:** lo que la persona encontrará, en una frase con la palabra que buscaría. No
  repitas el title.
- **Open Graph:** imagen de 1200×630 px con URL absoluta; sin ella el link se comparte sin
  imagen.
- **Canonical:** URL absoluta de la versión oficial de cada página.
- **Sitemap:** en Astro, `@astrojs/sitemap` con `site` configurado en `astro.config` (tu dominio
  real, no `example.com`). En `public/robots.txt`: `Sitemap: https://tusitio.com/sitemap-index.xml`.
- Las páginas internas (catálogo `/componentes`, 404, borradores) llevan
  `<meta name="robots" content="noindex">` y no van en el sitemap.
- **Textos de los títulos y descripciones:** si existe el skill `ux-writing-es`, pásalos por su
  script.

## 3. Contenido (lo que más pesa y el script no mide)
Revisa y comenta, sin reescribir sin permiso:
- ¿Cada página responde una pregunta concreta de alguien? ¿El `h1` lo dice?
- ¿Los casos de un portafolio tienen texto real (contexto, problema, proceso, resultado) o solo
  imágenes? Google no lee imágenes de texto.
- ¿Hay enlaces internos entre páginas relacionadas?

## 4. Avisar a los buscadores (solo si la persona lo pide, después de publicar)
- **Google:** Search Console → agregar la propiedad → enviar el sitemap.
- **Bing (y por extensión los buscadores que usan su índice):** IndexNow. Genera una clave
  (8–128 caracteres: letras, números y guiones), publícala en `public/<clave>.txt` con la clave
  como único contenido y, ya publicada, envía las URLs:
  ```bash
  curl -X POST https://api.indexnow.org/indexnow -H "Content-Type: application/json; charset=utf-8" \
    -d '{"host":"tusitio.com","key":"<clave>","keyLocation":"https://tusitio.com/<clave>.txt","urlList":["https://tusitio.com/"]}'
  ```
  Respuesta 200 o 202 = recibido. **Pide confirmación antes de enviar**: es una llamada a un
  servicio externo.

## 5. Informe
| Página | Problema | Corrección (archivo:línea) | Hecho |
|---|---|---|---|

Vuelve a correr el script después de corregir y muestra el resumen final.
