---
name: search-and-filtering
description: Búsqueda y filtrado de listados en la API sobre PostgreSQL — normalización con unaccent y pg_trgm, full-text de Postgres, filtros componibles y seguros (sin SQL dinámico inseguro ni orden inyectable), paginación por cursor estable con orden determinista, y no exponer datos de personas antes del consentimiento. Usar al construir un endpoint de listado o buscador, al agregar filtros u ordenamiento, al implementar autocompletado o "buscar por nombre", o al diagnosticar una búsqueda lenta, con resultados inestables entre páginas o que filtra datos que no debería.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Búsqueda y filtrado

Un listado con búsqueda es tres problemas juntos: **relevancia** (que encuentre), **seguridad**
(que no inyecte ni exponga de más) y **rendimiento** (que escale con el dataset). La base de
índices y planes está en `postgresql-advanced`; acá está cómo se arma el endpoint.

## 1. Normalización y coincidencia

- Texto de personas/catálogos en español: normalizá acentos y mayúsculas. `unaccent` +
  `lower()` para que "José" matchee "jose". Aplicá la **misma** normalización al indexar y al consultar.
- Coincidencia parcial / tolerante a typos: `pg_trgm` (`ILIKE '%x%'`, o `similarity()`/`%`
  operador) con índice **GIN** sobre la expresión normalizada. Sirve para autocompletar y
  "buscar por nombre".
- Búsqueda de texto largo (contenido, descripciones): full-text de Postgres —`tsvector` +
  `tsquery`, `to_tsvector('spanish', ...)`, ranking con `ts_rank`, índice GIN sobre el `tsvector`.
- Elegí una: trigram para nombres/campos cortos y prefijos; full-text para documentos. No las
  mezcles sin razón.

```sql
-- ✅ índice que respalda la búsqueda por nombre normalizada
CREATE INDEX idx_person_name_trgm ON person USING gin (lower(unaccent(full_name)) gin_trgm_ops);
-- consulta que usa ese índice
WHERE lower(unaccent(full_name)) LIKE lower(unaccent($1)) || '%';
```

Toda búsqueda que se pone en producción tiene un `EXPLAIN (ANALYZE)` que muestra que **usa el
índice**, no un seq scan (`postgresql-advanced`).

## 2. Filtros componibles y seguros

- Construí el `WHERE` con el **query builder del ORM** o consultas parametrizadas. **Jamás**
  concatenes valores del cliente en el SQL.
- El campo por el que se filtra/ordena viene de una **allowlist** en el servidor, no del string
  crudo del cliente. `sort=name` se mapea a una columna conocida; `sort=; DROP...` no existe en el mapa.

```ts
// ✅ campo de orden contra allowlist → columna real
const SORTABLE = { name: 'full_name', createdAt: 'created_at' } as const;
const col = SORTABLE[dto.sort ?? 'createdAt'];
if (!col) throw new BadRequestException('sort inválido');
// ❌ orden inyectable
qb.orderBy(`${dto.sort} ${dto.dir}`);   // dto.sort y dto.dir vienen del cliente
```

- Validá cada filtro con el DTO (tipo, rango, enum). `dir` solo `asc|desc`.
- Filtros opcionales: aplicá solo los presentes; no generes `WHERE 1=1 AND ...` con basura.
- El filtro de **tenant** no es opcional ni viene del cliente: lo pone el contexto siempre
  (`multi-tenancy`). Un buscador es una fuga clásica de datos entre organizaciones.

## 3. Paginación por cursor (estándar de la casa)

Offset (`LIMIT/OFFSET`) se degrada en datasets grandes y **salta o repite** filas cuando el
conjunto cambia entre páginas. Usá cursor.

- Ordená por una clave **determinista y única**: la columna de orden **+** un desempate único
  (`created_at, id`). Sin el desempate, dos filas con igual `created_at` rompen el cursor.
- El cursor codifica los valores de la última fila de la página; la siguiente pide "después de
  eso" (keyset):

```sql
-- ✅ keyset: estable aunque se inserten filas entremedio, y usa índice (created_at, id)
WHERE (created_at, id) < ($lastCreatedAt, $lastId)
ORDER BY created_at DESC, id DESC
LIMIT $pageSize + 1;   -- el +1 dice si hay página siguiente
```

- Cursor **opaco** (base64) y validado al recibir; no expongas el offset ni datos internos.
- El orden del listado y el del cursor son el mismo, siempre; cambiar el orden invalida cursores viejos.
- `pageSize` con tope máximo del servidor.

## 4. No exponer antes del consentimiento

"Buscar personas" es sensible (`data-privacy-sensitive`):

- Los buscadores de personas devuelven solo lo que el actor tiene derecho a ver **en ese
  contexto**. Un directorio público muestra lo que el profesional/entidad aceptó publicar; no la ficha.
- Antes del consentimiento/relación de atención, la búsqueda no revela datos clínicos ni de
  contacto privados. Devolvé el mínimo (nombre público, especialidad), no todo el registro.
- Cuidado con **inferencia por filtros**: permitir filtrar pacientes por diagnóstico o por
  medicación puede exponer condición de salud aunque no muestres el campo. Restringí esos filtros
  por rol y auditá su uso.
- Respuesta mínima por vista (`authz-access-control`): el listado devuelve campos de listado, no
  la entidad entera.

## 5. Rendimiento y forma de la respuesta

- Cada combinación de filtro+orden que se ofrece debe tener índice que la respalde, o una razón
  documentada de por qué el seq scan es aceptable (tabla chica).
- No traigas relaciones que el listado no muestra (N+1 y payload gordo:
  `code-efficiency`). Proyectá solo lo necesario.
- `count` total exacto es caro en tablas grandes: preferí "hay más" (el `+1` del keyset) o un
  conteo aproximado; el count exacto, solo si el negocio lo exige.
- Autocompletado: `debounce` en el cliente, longitud mínima de query, límite chico de
  resultados, y cacheá catálogos estables (`caching-strategy`) — nunca cachees resultados con
  datos por-usuario.

## Anti-patrones

- Concatenar valores del cliente en SQL; ordenar por un string crudo del cliente.
- Normalizar distinto al indexar y al consultar (el índice no se usa).
- `LIKE '%x%'` sin índice trigram sobre tablas grandes; búsqueda sin `EXPLAIN`.
- Offset para paginar catálogos grandes; cursor sin desempate único.
- Filtro de tenant que viene del cliente o se olvida; buscador que devuelve la entidad completa.
- Permitir filtrar personas por atributos clínicos sin control ni auditoría.

## Checklist

- [ ] Normalización (`unaccent`+`lower`) idéntica al indexar y consultar; índice GIN/trigram o full-text que la respalda.
- [ ] `EXPLAIN (ANALYZE)` muestra uso de índice, no seq scan, en el dataset esperado.
- [ ] Filtros y orden por allowlist mapeada a columnas; DTO valida tipos/rangos; `dir` acotado.
- [ ] Tenant impuesto por contexto, nunca por el cliente.
- [ ] Paginación por cursor keyset con orden determinista (`col, id`) y cursor opaco validado; `pageSize` con tope.
- [ ] La búsqueda de personas respeta consentimiento/relación y devuelve el mínimo.
- [ ] Filtros que podrían inferir datos clínicos están restringidos por rol y auditados.
- [ ] Sin N+1; proyección mínima; catálogos estables cacheados, resultados por-usuario no.
