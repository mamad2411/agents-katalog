---
name: model-driven-schema
description: Gate del esquema dirigido por modelo — el diagrama es la única fuente de verdad y el cambio fluye en una sola dirección (modelo → DDL generado → base → entidades ORM). Usar al agregar o quitar tablas, columnas, claves, índices o constraints; al tocar un generador; al ver síntomas de deriva (tabla ausente, columna ausente, nulabilidad divergente, conteos que no cuadran); antes de cualquier tentación de ALTER manual; y al decidir entre este enfoque y migraciones versionadas.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Esquema dirigido por modelo

La deriva entre capas es el fallo más caro de esta arquitectura: el código compila, el ORM
arranca, y el error aparece en la primera consulta que toca la columna que no existe. Esta
skill fija la dirección del cambio y cómo detectar que alguien la violó. Cómo se escribe el
modelo: `data-modeling-plantuml`. Qué es un buen esquema: `database-design`.

## 1. Las cuatro capas y la dirección única

```text
modelo (diagramas)        ← FUENTE DE VERDAD. Nada por encima.
   │  generador de DDL
   ▼
DDL generado (SQL)        ← salida. Nunca se edita a mano.
   │  aplicación por el camino oficial
   ▼
base de datos             ← materialización del DDL.
   │  generador de entidades
   ▼
entidades ORM             ← salida. Nunca se escriben a mano "para que compile".
```

1. **El cambio baja, siempre.** Si la base y el modelo discrepan, gana el modelo y la base se
   corrige desde él. Si una entidad y la base discrepan, la entidad se regenera. Nunca al revés.
2. **Temperatura cero:** ninguna capa inferior inventa lo que el modelo no declara — ni una
   columna, ni un tipo, ni una FK, ni un valor de catálogo.
3. **Todo defecto se corrige en el generador** (o en el modelo), jamás en su salida. Un arreglo
   manual sobrevive hasta la próxima regeneración y después desaparece en silencio.
4. La sincronización automática de esquema del ORM contra una base compartida queda **apagada**:
   es un vector de cambio en la dirección prohibida (la app creando lo que el modelo no declara).

## 2. Prohibiciones

| Prohibido | Por qué | En su lugar |
|---|---|---|
| Editar un `.sql` generado | La próxima generación lo pisa | Corregir modelo o generador |
| `ALTER TABLE` interactivo contra la base | Nadie más lo tiene; no se reproduce | Parche generado (§3) |
| `UPDATE`/`DELETE` para "arreglar" datos de carga | El defecto sigue en el generador | `seed-data-catalogs` |
| Entidad ORM escrita a mano | Diverge del DDL sin que nadie lo note | Regenerar |
| `CREATE TABLE` fuera del directorio de salida | Esquema fantasma fuera del modelo | Guard en CI (§4) |

## 3. Parches: el vehículo, no la corrección

Sobre una base viva no siempre se puede reconstruir. El parche incremental es legítimo si:

- Se **deriva del cambio del modelo** (idealmente lo emite el generador como diff entre DDL
  anterior y nuevo); nunca se redacta primero el parche y después "se acomoda" el modelo.
- Vive en un directorio propio, con nombre ordenable (`AAAA-MM-DD_descripcion.sql`), es
  idempotente (`IF NOT EXISTS`, guardas) y se aplica con una herramienta, no tipeado.
- Respeta expand/contract y los locks de `database-design` §5.
- **Invariante de convergencia:** base reconstruida desde cero == base vieja + parches. Si no
  son idénticas, el parche o el generador están mal. Probalo (§6).

## 4. Detección de deriva por frontera

| Frontera | Cómo se detecta | Esperado |
|---|---|---|
| modelo ↔ DDL | Regenerar todo sobre un árbol limpio y `git diff` | Diff vacío si no cambió el modelo |
| DDL ↔ base | Conteos de tablas/FKs/índices del DDL vs catálogo del motor | Igualdad **exacta** |
| base ↔ ORM | Verificador al arrancar y en CI: metadatos del ORM vs `information_schema` | Cero diferencias |
| datos | Huérfanos y conteos (`data-quality-validation`) | 0 huérfanos |

- Diff no vacío en la primera frontera sin haber tocado el modelo ⇒ alguien editó la salida a
  mano ⇒ revertir a lo generado. Esto exige generadores deterministas (`python-tooling-standards`).
- "Casi coincide" no existe: una igualdad de conteos que deja de ser exacta es deriva.
- Guard de CI: fallar si aparece `CREATE TABLE`/`ALTER TABLE` fuera de los directorios de DDL
  generado y de parches.

Categorías mínimas que el verificador base ↔ ORM debe reportar, con estos nombres:

| Tipo de deriva | Consecuencia |
|---|---|
| `tabla-ausente` | Toda consulta a la entidad falla |
| `columna-ausente` | Falla todo `SELECT` que la proyecte |
| `columna-obligatoria-no-mapeada` | Todo `INSERT` del ORM viola `NOT NULL` |
| `nulabilidad-divergente` | Falla al escribir, no al leer: el bug aparece tarde |

Consultas para localizar el faltante:

```sql
SELECT table_schema, count(*) FROM information_schema.tables
 WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog','information_schema')
 GROUP BY 1 ORDER BY 1;

SELECT column_name, is_nullable, data_type, column_default
  FROM information_schema.columns
 WHERE table_schema = :s AND table_name = :t ORDER BY ordinal_position;

-- PostgreSQL trunca identificadores a 63 bytes EN SILENCIO: dos nombres largos pueden colisionar
SELECT conname FROM pg_constraint WHERE length(conname) = 63;
```

No compares tipos como texto crudo (`int4` vs `integer`, `timestamptz` vs
`timestamp with time zone` son sinónimos): normalizá antes o vas a reportar deriva falsa.

## 5. Runbook — "hay deriva"

1. **DDL ≠ modelo** → regenerar y diffear. Si el modelo no cambió, revertir la edición manual.
2. **Base ≠ DDL** → ¿falta aplicar un parche? ¿alguien hizo `ALTER` a mano? ¿la app sincronizó
   esquema sola? Aplicar el parche faltante o reconstruir limpio y recargar datos.
3. **Entidades ≠ base** → regenerar entidades. Si persiste, el defecto está **aguas arriba**: hay
   entidades que el DDL nunca creó ⇒ corregir generador de DDL o modelo, no el ORM.
4. **Huérfanos > 0** → corregir el generador de datos y recargar. Nunca un `DELETE` manual.

En todos los casos: identificar la frontera **antes** de tocar nada, y subir hasta la capa
más alta que esté mal. Arreglar abajo lo que está roto arriba garantiza que vuelva.

## 6. Modelo como fuente vs migraciones versionadas

| Criterio | Modelo → DDL generado | Migraciones versionadas |
|---|---|---|
| Fuente de verdad | El diagrama (estado deseado) | La secuencia de cambios (historia) |
| Base nueva | Se genera completa, en un paso | Se reproduce toda la historia |
| Producción con datos y sin ventana | Requiere parches disciplinados | Es su caso natural |
| Riesgo típico | Deriva si alguien toca la salida | El modelo real solo existe "sumando" migraciones |
| Conviene cuando | Esquema grande, en diseño activo, reconstruible | Esquema estable con datos que no se pueden recrear |

No son excluyentes: modelo como fuente **más** parches generados es un híbrido válido mientras
se cumpla la invariante de convergencia del §3. Lo que no es válido es tener dos fuentes de
verdad. La elección se declara en el CLAUDE.md del proyecto.

## Anti-patrones

- "Lo arreglo en la base y después actualizo el modelo." Después es nunca.
- Regenerar entidades para tapar una tabla que el DDL jamás creó.
- Un parche escrito a mano que el generador no reproduce en una reconstrucción limpia.
- Verificador de deriva que solo loguea un warning que nadie lee: debe **fallar** el arranque en
  CI y en entornos no productivos.
- Declarar "propagado" tras regenerar una sola capa.

## Checklist

- [ ] El cambio empezó en el modelo; ninguna salida generada se editó a mano.
- [ ] Se regeneraron **todas** las capas afectadas: DDL, constraints, entidades, catálogos/seeds.
- [ ] Regeneración sobre árbol limpio da diff vacío salvo lo esperado por el cambio.
- [ ] Parche (si aplica) idempotente, derivado del modelo, y convergente con reconstrucción limpia.
- [ ] Verificador base ↔ ORM sin diferencias; conteos DDL ↔ base exactos.
- [ ] Guard de CI contra DDL fuera de los directorios permitidos en verde.

## Evidencia / Definition of Done

Para afirmar "cambio de esquema propagado" pegá la salida **literal** de:

1. `git diff --stat` tras regenerar: solo archivos esperados por el cambio del modelo.
2. El verificador base ↔ ORM: línea de "sin deriva" o el listado completo por tipo.
3. Conteos de tablas y FKs del DDL generado junto a los del catálogo del motor.
4. Si hubo parche: aplicación sin error **y** comparación contra una reconstrucción limpia.
5. Lo no cubierto, declarado explícitamente (capas o entornos no ejercitados).

Leer el diff no es verificar. Ver `evidence-and-verification`.
