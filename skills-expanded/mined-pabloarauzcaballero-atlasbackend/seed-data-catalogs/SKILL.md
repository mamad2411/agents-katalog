---
name: seed-data-catalogs
description: Estándar para seeds y catálogos — cargas idempotentes con IDs estables (la segunda corrida inserta 0), datos REALES con procedencia registrada (fuente, URL, fecha, licencia), prohibición de datos ficticios presentados como reales, jerarquías padre-hijo, datasets grandes por importación y datos de demo separados. Usar al crear o actualizar un catálogo (regiones, ciudades, especialidades, aseguradoras, instituciones, monedas, medicamentos), al escribir un seeder o generador de datos, al corregir un dato cargado, o cuando un requisito pide "datos reales".
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Seeds y catálogos

Un catálogo mal sembrado contamina todo lo que lo referencia y no se nota hasta producción.
Esta skill fija cómo se obtienen, generan y cargan los datos de referencia. La verificación
posterior a la carga es `data-quality-validation`; el esquema que los recibe,
`model-driven-schema`.

## 1. Tres clases de dato — no las mezcles

| Clase | Origen | Quién lo cambia | Ejemplo |
|---|---|---|---|
| **Catálogo oficial** | Organismo o estándar externo | Solo una nueva versión de la fuente | División administrativa, códigos de moneda, terminología clínica |
| **Catálogo interno** | Decisión de la casa | Un cambio revisado en el repo | Estados de un flujo, tipos de notificación |
| **Dato aportado por usuario** | La aplicación en runtime | El usuario | Una clínica que se registra |

- Cada fila sabe a qué clase pertenece (columna u origen separado). Un usuario nunca edita un
  catálogo oficial; una recarga de catálogo nunca pisa un dato de usuario.
- Conjuntos cerrados de valores van como conceptos de catálogo, no como enums en código: ver
  `terminology-value-sets`.

## 2. Datos reales: procedencia obligatoria

1. Si el requisito pide datos reales, la fuente es institucional, un estándar publicado o un
   dataset ya aprobado por el responsable del dominio. **Nunca texto generado.**
2. Todo dataset lleva su manifiesto de procedencia junto al archivo:

```yaml
dataset: administrative_areas
source_name: <organismo que lo publica>
source_url: <url exacta del recurso>
retrieved_at: 2026-09-19
source_version: <edición / fecha de publicación>
license: <licencia o condición de uso>
transform: normalización de mayúsculas; sin filas agregadas ni inferidas
checksum_sha256: <hash del archivo crudo>
```

3. **Prohibido** presentar como real un dato ficticio o inferido: universidades, aseguradoras,
   especialidades, instituciones, direcciones. Si no hay fuente, el catálogo queda **vacío con
   un TODO y la fuente pendiente**, no relleno de inventos.
4. **Datos clínicos** (medicamentos, dosis, contraindicaciones, interacciones, relaciones
   título → especialidad): jamás se completan ni se "corrigen" por inferencia. Exigen dataset
   con evidencia y validación de quien es dueño funcional de ese catálogo.
5. Verificá que la licencia permite el uso y la redistribución que vas a hacer. Si no está
   clara, escalá; no la asumas.

## 3. IDs estables

- El ID de una fila de catálogo **no cambia nunca** entre corridas, entornos ni versiones: otras
  tablas, URLs, caches y exportes lo referencian.
- Derivá el ID de forma determinista desde la clave natural (p. ej. UUID v5 sobre
  `namespace + código`), o fijalo en el dataset. **No** uses autoincrementales ni UUID aleatorios
  generados en cada corrida.
- La clave natural (código oficial, o `padre + nombre normalizado`) lleva constraint `UNIQUE`: es
  lo que hace posible el upsert y detecta duplicados.
- Reemplazar IDs existentes solo con un plan de remapeo de todas las referencias, revisado.

## 4. Idempotencia

La carga se puede correr N veces con el mismo resultado que una.

```sql
-- carga inicial: no pisa lo existente
INSERT INTO catalog.cities (city_id, region_id, code, name)
VALUES (:id, :region_id, :code, :name)
ON CONFLICT (city_id) DO NOTHING;

-- modo refresco: propaga correcciones del generador
INSERT INTO catalog.cities (city_id, region_id, code, name)
VALUES (:id, :region_id, :code, :name)
ON CONFLICT (city_id) DO UPDATE
  SET name = EXCLUDED.name, region_id = EXCLUDED.region_id;
```

- **Prueba obligatoria:** dos corridas consecutivas; la segunda reporta `insertados: 0`.
- Ojo con la trampa: con `DO NOTHING`, una **corrección** en el dataset no llega a una base ya
  poblada. Necesitás un modo de refresco explícito, y saber cuál estás corriendo.
- Prohibido `TRUNCATE` + reinserción como estrategia de actualización sobre datos que otras
  tablas referencian o que existen en producción.
- Carga dentro de una transacción por dataset: o entra entero o no entra.
- El cargador imprime conteos por tabla (leídos, insertados, actualizados, omitidos). Una carga
  muda no se puede verificar.

## 5. Corregir en el generador, nunca en la base

Dato mal cargado ⇒ se corrige el dataset o el generador, se regenera y se recarga en modo
refresco. Un `UPDATE` manual sobrevive hasta la próxima reconstrucción y después vuelve el
error, en silencio. Lo mismo para archivos de seed **generados**: no se editan a mano.

## 6. Jerarquías

- Región → ciudad, grupo → subgrupo, árbol de coberturas: el padre se carga antes que el hijo,
  con FK real y `ON DELETE RESTRICT`.
- El hijo referencia al padre por **clave estable**, no por posición ni por nombre suelto.
- No inventes relaciones que la fuente no declara. Si el dataset trae hijos sin padre
  resoluble, la carga **aborta** listándolos; no los cuelga de un padre "Otros".
- Árboles de profundidad variable: `parent_id` autorreferente + verificación de ciclos y
  huérfanos tras la carga.
- Probá los selects dependientes de la UI (elegir región filtra ciudades) contra los datos cargados.

## 7. Datasets grandes

- Miles de filas no se escriben como literales en código ni en un `.sql` de cientos de MB en el
  repo. Se **importan** desde el archivo fuente (CSV/JSON) con un cargador, por lotes o `COPY`.
- El archivo crudo se conserva sin tocar (con su checksum); la normalización es un paso
  reproducible aparte. Así se puede auditar qué cambió la casa respecto de la fuente.
- Actualizar a una nueva edición de la fuente = nuevo manifiesto + diff de altas/bajas/cambios
  revisado por un humano. Las bajas se marcan inactivas, no se borran si hay referencias.
- Si el dataset no debe vivir en git (tamaño, licencia), el repo guarda manifiesto, checksum y
  el script de obtención.

## 8. Datos de demo y de prueba: separados

| Conjunto | Contenido | ¿Producción? |
|---|---|---|
| Referencia | Catálogos oficiales e internos | Sí |
| Demo / mock | Personas, turnos, historias **sintéticas** | **Nunca** |
| Fixtures de test | Mínimos y deterministas por test | Nunca (`test-data-management`) |

- Directorios y comandos distintos. El cargador de demo **falla duro** si detecta entorno
  productivo; no alcanza con "acordarse" de no correrlo.
- Los datos de demo son sintéticos e inequívocamente falsos. Nunca copies datos reales de
  personas a un entorno de desarrollo: `data-privacy-sensitive`.
- Demo no es "real": no lo cites como tal en una demo al cliente ni en un reporte.

## Anti-patrones

- Catálogo "real" escrito de memoria o generado por un modelo de lenguaje.
- IDs que cambian en cada reconstrucción y rompen referencias en otros entornos.
- Seeder ad-hoc dentro de una feature, fuera del mecanismo oficial de carga.
- Arreglar un typo con `UPDATE` en la base compartida.
- Mezclar datos de demo con catálogos en el mismo archivo o comando.
- Borrar filas de catálogo con referencias vivas en vez de inactivarlas.

## Checklist

- [ ] Clase del dato identificada (oficial / interno / usuario).
- [ ] Manifiesto de procedencia completo: fuente, URL, fecha, versión, licencia, checksum.
- [ ] Ningún valor inventado o inferido; lo que falta quedó vacío con TODO.
- [ ] IDs deterministas y estables; clave natural con `UNIQUE`.
- [ ] Segunda corrida consecutiva inserta 0; existe modo refresco para correcciones.
- [ ] Jerarquías con FK, padres antes que hijos, sin huérfanos ni ciclos.
- [ ] Dataset grande importado desde archivo, crudo conservado.
- [ ] Demo separado y bloqueado en producción.
- [ ] Verificación post-carga ejecutada (`data-quality-validation`) con salida pegada.
