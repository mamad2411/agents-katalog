---
name: directories-public-profiles
description: Diseño de directorios públicos y perfiles (doctores, entidades de salud) — qué es público vs privado, consentimiento antes de exponer, perfil verificado, búsqueda y filtrado, SEO de perfiles, exposición de datos mínimos y control del dueño sobre su propia visibilidad. Usar al construir o revisar un directorio público, la ficha pública de un profesional o institución, la búsqueda de esas fichas, o cualquier endpoint que muestre datos de una persona a usuarios no autenticados.
---

# Directorios públicos y perfiles — reglas de diseño

Un directorio público de personas de salud es una superficie sensible: publica datos reales de
gente real ante cualquiera. La regla que manda todo: **nada se hace público sin consentimiento y
sin verificación**.

## 1. Público vs privado: lista blanca, no lista negra

- Definí **explícitamente qué campos son públicos** (lista blanca). Todo lo demás es privado por
  defecto. Nunca al revés ("público salvo estos"): un campo nuevo no debe filtrarse por olvido.
- El endpoint público devuelve un **DTO público** distinto del interno; no serialices la entidad
  completa (ver `authz-access-control`, respuesta mínima; `data-privacy-phi`).
- Datos que casi nunca van en público: documento de identidad, email/teléfono personales,
  dirección exacta, y por supuesto cualquier dato clínico. Un contacto profesional publicado es
  una decisión consciente del dueño, no el default.

## 2. Consentimiento antes de exponer

- Aparecer en el directorio es **opt-in explícito y revocable** (ver `consent-management`). Revocar
  saca la ficha del índice **de inmediato**, incluidas cachés y resultados de búsqueda.
- El consentimiento tiene alcance: puede aceptar aparecer con nombre y especialidad pero no con
  foto o teléfono. Respetá el alcance por campo.

## 3. Perfil verificado

- Un directorio de salud sin verificación es un riesgo. Marcá el estado de verificación del
  profesional/entidad y no publiques como "verificado" lo que no lo está (ver
  `anti-hallucination-guard`: no afirmar lo que no se comprobó).
- Los títulos, especialidades y matrículas se modelan como conceptos codificados con procedencia,
  no texto libre inventado (ver `terminology-value-sets`, `seed-data-catalogs`).

## 4. Control del dueño

- El dueño del perfil controla su visibilidad y sus datos: puede editar, ocultar campos, pausar la
  publicación o eliminarse del directorio. Es su dato.
- Toda edición de lo que se muestra queda auditada (ver `audit-trail-history`).

## 5. Búsqueda y filtrado

- La búsqueda pública solo consulta e indexa **campos públicos y consentidos**. No permitas
  filtrar/ordenar por un campo privado aunque no se muestre: eso lo filtra igual.
- Búsqueda por nombre/especialidad/ubicación con normalización (acentos, mayúsculas) e índices
  adecuados (ver `search-and-filtering`, `postgresql-advanced` para `pg_trgm`/`unaccent`).
- Cuidado con la **enumeración**: paginación acotada, rate limiting y sin exponer identificadores
  internos que permitan raspar toda la base (ver `security-guardrails`).

## 6. SEO de perfiles

- Los perfiles públicos suelen querer indexarse en buscadores: URLs estables y legibles (slug),
  títulos y meta descripción por perfil, datos estructurados, renderizado en servidor
  (ver `seo-public-pages`, y `angular-ssr-hydration` para no filtrar datos privados en el HTML).
- Un perfil despublicado o revocado debe dejar de ser indexable (noindex / 404/410) y salir del
  sitemap. Coordiná con la caché del CDN.

## Anti-patrones

- Serializar la entidad completa en el endpoint público (lista negra de campos).
- Publicar sin opt-in, o que revocar no saque la ficha de caché/índice/buscador.
- Mostrar "verificado" sin verificación real.
- Permitir filtrar/ordenar la búsqueda por campos privados.
- URLs con id interno secuencial que invitan al scraping masivo.
- SSR que mete datos privados en el HTML servido.

## Checklist

- [ ] Lista blanca de campos públicos; DTO público separado del interno.
- [ ] Aparecer es opt-in revocable, con alcance por campo; revocar limpia caché e índice al instante.
- [ ] Estado de verificación real; títulos/especialidades como conceptos con procedencia.
- [ ] El dueño puede editar, ocultar, pausar y eliminarse; cambios auditados.
- [ ] Búsqueda solo sobre campos públicos y consentidos; normalizada e indexada.
- [ ] Anti-enumeración: paginación acotada, rate limiting, sin ids internos expuestos.
- [ ] SEO con URLs estables y SSR sin datos privados; despublicar quita del índice y del sitemap.
