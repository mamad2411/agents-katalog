---
name: data-quality-validation
description: Gate de calidad de datos por consultas de verificación — conteos esperados, huérfanos, duplicados, nulos indebidos, rangos y formatos, jerarquías rotas, reconciliación entre sistemas e invariantes de negocio expresadas en SQL, corridas antes y después de cada carga. Usar después de cargar seeds o un dataset, tras aplicar un parche de esquema o un backfill, al validar un restore, cuando "los números no cuadran", y antes de declarar una carga o migración de datos como correcta. Incluye plantillas de queries.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Validación de calidad de datos

"Cargó sin error" no dice nada sobre si los datos están bien. Esta skill convierte la calidad
de datos en un conjunto de consultas que devuelven **cero filas cuando todo está sano**, y en
un antes/después alrededor de cada operación que mueve datos. Complementa a
`integrity-testing` (tests automatizados de constraints y transacciones): esto es el control
sobre los **datos ya cargados**.

## 1. Principios

1. **Toda verificación es una query cuyo resultado sano es vacío** (o un número esperado
   declarado de antemano). Así se automatiza y no admite interpretación.
2. **El valor esperado se escribe antes de correr**, con su origen (manifiesto del dataset,
   conteo de la fuente, DDL). Mirar el número y decidir después que "está bien" no es verificar.
3. **Solo lectura.** Esta skill detecta; no arregla. El arreglo va en el generador o la fuente
   (`seed-data-catalogs`, `model-driven-schema`), nunca con `UPDATE`/`DELETE` manual.
4. Si una invariante se puede garantizar con una constraint, **va como constraint**
   (`database-design` §2). La query queda para lo que el motor no puede expresar, para datos
   previos a la constraint y para cruces entre sistemas.
5. Corré contra una réplica o fuera de pico si la tabla es grande; una validación no debe
   degradar producción.

## 2. Antes / después

Alrededor de toda carga, parche, backfill o restore:

```sql
-- foto: conteo por tabla del schema afectado (exacto, no estimado)
SELECT 'catalog.cities' AS t, count(*) FROM catalog.cities
UNION ALL SELECT 'catalog.regions', count(*) FROM catalog.regions;
```

- Guardá la foto **antes**, corré la operación, tomá la foto **después**, y explicá cada delta:
  `después − antes == insertados reportados por el cargador`. Un delta sin explicación es un
  hallazgo, aunque no haya habido error.
- Para detectar cambios de contenido sin cambio de conteo, comparar una huella por tabla:

```sql
SELECT md5(string_agg(t::text, '|' ORDER BY t.city_id)) FROM catalog.cities t;
```

  (útil en catálogos chicos y en verificación de restore; caro en tablas grandes).

## 3. Plantillas

**Huérfanos** — hijos cuyo padre no existe (FK ausente, deshabilitada o diferida):

```sql
SELECT c.city_id, c.region_id
  FROM catalog.cities c
  LEFT JOIN catalog.regions r ON r.region_id = c.region_id
 WHERE c.region_id IS NOT NULL AND r.region_id IS NULL;
```

**Duplicados por clave natural** — lo que una `UNIQUE` debería impedir:

```sql
SELECT region_id, lower(trim(name)) AS k, count(*)
  FROM catalog.cities
 GROUP BY 1, 2 HAVING count(*) > 1;
```

**Nulos y vacíos indebidos** — incluye el string vacío y el espacio, que `NOT NULL` deja pasar:

```sql
SELECT count(*) FILTER (WHERE name IS NULL)        AS nulos,
       count(*) FILTER (WHERE btrim(name) = '')    AS vacios
  FROM catalog.cities;
```

**Rangos, formatos y fechas imposibles:**

```sql
SELECT appointment_id FROM scheduling.appointments
 WHERE ends_at <= starts_at OR starts_at < timestamptz '1900-01-01';

SELECT account_id FROM billing.invoices WHERE total < 0 OR total <> round(total, 2);
```

**Valores fuera de su catálogo** — columna de concepto que apunta a un concepto de otro value set:

```sql
SELECT a.appointment_id, a.status_concept_id
  FROM scheduling.appointments a
 WHERE NOT EXISTS (SELECT 1 FROM terminology.value_set_members m
                    WHERE m.value_set_code = 'appointment_status'
                      AND m.concept_id = a.status_concept_id);
```

(nombres de tablas ilustrativos: usá los del modelo del proyecto; ver `terminology-value-sets`).

**Jerarquías: ciclos y profundidad** en un árbol autorreferente:

```sql
WITH RECURSIVE t AS (
  SELECT node_id, parent_id, ARRAY[node_id] AS path, false AS cycle
    FROM catalog.nodes WHERE parent_id IS NOT NULL
  UNION ALL
  SELECT n.node_id, n.parent_id, t.path || n.node_id, n.node_id = ANY(t.path)
    FROM catalog.nodes n JOIN t ON n.node_id = t.parent_id WHERE NOT t.cycle
) SELECT DISTINCT path FROM t WHERE cycle;
```

**Solapamientos** — dos reservas del mismo recurso que se pisan (lo que un `EXCLUDE` impediría):

```sql
SELECT a.appointment_id, b.appointment_id
  FROM scheduling.appointments a
  JOIN scheduling.appointments b
    ON a.resource_id = b.resource_id AND a.appointment_id < b.appointment_id
   AND tstzrange(a.starts_at, a.ends_at) && tstzrange(b.starts_at, b.ends_at);
```

## 4. Invariantes de negocio en SQL

Escribí cada regla del dominio como una query de violaciones. Ejemplos de forma:

| Invariante | Query de violación |
|---|---|
| Todo asiento contable balancea | `GROUP BY entry_id HAVING sum(debit) <> sum(credit)` (`accounting-double-entry`) |
| Un estado terminal no tiene transiciones posteriores | join de historial con `occurred_at > closed_at` (`state-machines-workflows`) |
| Todo acceso a un expediente tiene base legal vigente | anti-join acceso ↔ consentimiento (`data-privacy-sensitive`) |
| Toda fila de tenant tiene `tenant_id` y coincide con el de su padre | join padre-hijo con `tenant_id` distinto (`multi-tenancy`) |
| Tabla append-only no tiene filas modificadas | ver `audit-trail-history` |

Guardá estas queries versionadas junto al modelo, una por archivo o en una suite con nombre por
regla. Una invariante que solo vive en la cabeza de alguien no se verifica.

## 5. Reconciliación entre sistemas

Cuando el mismo hecho vive en dos lugares (base ↔ índice de búsqueda, base ↔ proveedor de pagos,
base ↔ archivo exportado, origen ↔ destino de una migración):

1. Definí cuál es la **fuente de verdad**. La reconciliación reporta contra ella.
2. Compará en tres niveles, del más barato al más caro: conteo → suma de control de una columna
   numérica o huella por lotes → diferencia fila a fila por clave (`EXCEPT` en ambos sentidos).
3. Reportá tres conjuntos: solo en A, solo en B, en ambos con contenido distinto.
4. Fijá el corte temporal (`WHERE updated_at <= :corte`) o vas a reportar como diferencia lo
   que está en tránsito.

```sql
(SELECT id, amount FROM staging.payments_src EXCEPT SELECT id, amount FROM billing.payments)
UNION ALL
(SELECT id, amount FROM billing.payments EXCEPT SELECT id, amount FROM staging.payments_src);
```

## 6. Operación

- Las queries corren como **suite**: un script que ejecuta todas, imprime `regla | violaciones` y
  sale con código distinto de cero si alguna no es cero (`python-tooling-standards`).
- Se ejecuta en CI contra la base reconstruida, y después de toda carga en entornos compartidos.
- Un hallazgo se clasifica: `GENERADOR` (corregir y recargar), `FUENTE` (dataset defectuoso:
  escalar, no parchear), `ESQUEMA` (falta constraint), `ESPERADO` (la regla estaba mal: corregir
  la regla, con justificación).
- Nunca "bajes el umbral" para que pase. Si hay 3 huérfanos conocidos y aceptados, se listan por
  ID con su justificación; la regla sigue exigiendo cero fuera de esa lista.
- Las salidas pueden contener PII: reportá IDs y conteos, no contenido (`data-privacy-sensitive`).

## Anti-patrones

- Validar con `count(*) > 0`: prueba que hay algo, no que está bien.
- Estimar conteos con estadísticas del catálogo del motor para una igualdad exacta.
- Decidir el número esperado después de ver el resultado.
- Arreglar el hallazgo con SQL manual y no tocar el generador.
- Suite que solo corre cuando alguien se acuerda.

## Checklist

- [ ] Valores esperados declarados antes de correr, con su origen.
- [ ] Foto antes y después; cada delta explicado por el reporte del cargador.
- [ ] Huérfanos, duplicados, nulos/vacíos, rangos y pertenencia a catálogo: 0 violaciones.
- [ ] Jerarquías sin ciclos ni hijos sin padre.
- [ ] Invariantes de negocio del módulo tocado ejecutadas.
- [ ] Reconciliación en ambos sentidos si hay dos sistemas, con corte temporal fijo.
- [ ] Hallazgos clasificados; ninguno resuelto con SQL manual.

## Evidencia / Definition of Done

Para afirmar "datos verificados" pegá **literal**: (1) la tabla `regla | esperado | obtenido` de
la suite completa, (2) las fotos de conteo antes y después con el reporte del cargador al lado,
(3) para cada hallazgo, IDs afectados y clasificación, (4) qué tablas o reglas **no** se
cubrieron. Sin esa salida, el estado es "cargado", no "verificado": ver
`evidence-and-verification`.
