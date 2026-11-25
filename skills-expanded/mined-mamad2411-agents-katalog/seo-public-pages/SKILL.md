---
name: seo-public-pages
description: SEO técnico de páginas públicas (directorios, perfiles, landing) — SSR/prerender para HTML indexable, títulos y meta description por ruta, datos estructurados schema.org (JSON-LD), sitemap y robots.txt, URLs canónicas, Open Graph/Twitter para compartir, e i18n con hreflang. Usar al crear o revisar cualquier página pública que deba aparecer en buscadores o verse bien al compartirse, y para decidir qué se prerenderiza y qué se sirve on-demand.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# SEO de páginas públicas

Solo aplica a lo **público** (directorios de profesionales, perfiles, landing). El área
logueada no se indexa. Un buscador necesita HTML con contenido en la primera respuesta, una
URL estable por recurso, y metadatos que describan la página.

## 1. HTML indexable: SSR o prerender

- El contenido debe estar en el HTML de la primera respuesta, no aparecer recién tras hidratar.
  Serví las rutas públicas con SSR o prerenderizadas (`RenderMode.Prerender`/`Server`; ver
  el modo de render que corresponda). Una landing de marketing se sirve estática por defecto.
- Nada de contenido crítico detrás de una interacción o de un `@defer` que el crawler no dispara.
- Un `<h1>` por página, jerarquía de headings coherente, enlaces `<a href>` reales (no `click`).

## 2. Título y meta por ruta

Cada ruta setea su propio `<title>` y `<meta name="description">` con el contenido real de esa
página (nombre del profesional, especialidad, ciudad), no un texto genérico del sitio. En
Angular, usá los servicios `Title` y `Meta` en un resolver o en el componente.

```typescript
private title = inject(Title);
private meta = inject(Meta);

setSeo(p: Profile) {
  this.title.setTitle(`${p.fullName} — ${p.specialty} en ${p.city}`);
  this.meta.updateTag({ name: 'description', content: p.summary.slice(0, 155) });
}
```

## 3. Datos estructurados (JSON-LD)

Agregá schema.org en JSON-LD para que el buscador entienda la entidad (p.ej. `Physician`,
`MedicalOrganization`, `BreadcrumbList`). El JSON-LD debe reflejar lo que se ve en la página;
no marques datos falsos o no visibles.

```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Physician","name":"...","medicalSpecialty":"...","address":{...}}
</script>
```

## 4. Canónicas, sitemap, robots

- **URL canónica** (`<link rel="canonical">`) por página, para que variantes con parámetros no
  se traten como duplicados. Una URL estable por recurso (ver `frontend-navigation-ia`).
- **sitemap.xml** generado con las URLs públicas indexables; actualizado cuando cambian.
- **robots.txt** que permite lo público y bloquea lo privado/duplicado; referenciá el sitemap.
- Ojo con contenido delgado o duplicado (miles de perfiles casi vacíos): `noindex` los que no
  aporten, para no diluir el sitio.

## 5. Compartir: Open Graph y Twitter Cards

Metadatos `og:title`, `og:description`, `og:image`, `og:url` (y `twitter:card`) por página,
para que el enlace se vea bien en redes y chat. La imagen debe existir y tener tamaño adecuado.

## 6. i18n y rendimiento

- Con varios idiomas, `hreflang` entre las variantes y canónica por idioma (ver `frontend-i18n-l10n`).
- El rendimiento es factor de ranking: Core Web Vitals dentro de umbral, imágenes optimizadas,
  poco JS en páginas de contenido (ver `frontend-performance`).

## Anti-patrones

- Página pública que renderiza el contenido solo en el cliente (crawler ve HTML vacío).
- Mismo `<title>`/description para todas las rutas.
- JSON-LD con datos que no están en la página.
- Sin canónica: variantes con `?utm=...` indexadas como duplicados.
- Datos sensibles o privados en una página indexable (consentimiento primero; ver `data-privacy-sensitive`).

## Checklist

- [ ] Rutas públicas con SSR/prerender; contenido en el primer HTML.
- [ ] `<title>` y meta description propios y descriptivos por ruta.
- [ ] JSON-LD schema.org que refleja el contenido visible.
- [ ] Canónica por página; sitemap.xml y robots.txt correctos.
- [ ] Open Graph/Twitter con imagen válida.
- [ ] hreflang si hay idiomas; Core Web Vitals en verde.
- [ ] Nada privado/datos sensibles en páginas indexables.
