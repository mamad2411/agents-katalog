---
name: terminology-value-sets
description: Gate de terminología — todo catálogo cerrado (estados, tipos, especialidades, sexo, monedas, divisiones administrativas, diagnósticos) se modela como concepto codificado contra un servidor terminológico, nunca como enum de lenguaje ni label hardcodeado. Cubre code system vs value set vs concept, columnas `*_concept_id`, código vs display, versionado, value sets estáticos vs dinámicos, i18n del display y validación de pertenencia. Usar antes de crear un enum, un catálogo, un `select` de opciones fijas o un `switch` sobre un tipo, y al sembrar o traducir catálogos.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Terminología y value sets

En un sistema de salud casi todo lo que parece «un enum» es en realidad **terminología**: tiene
dueño, versiones, traducciones, jerarquía y equivalencias con estándares externos. Tratarlo como
constante del código produce catálogos duplicados, datos históricos ilegibles e integraciones
imposibles.

**Regla de la casa**: un catálogo cerrado es un *value set* de *conceptos*; la columna que lo
referencia es `*_concept_id`. El cómo exacto (tablas, generadores, archivos de definición) lo fija
el CLAUDE.md del proyecto.

## 1. Vocabulario (no lo mezcles)

| Término | Qué es | Analogía |
|---|---|---|
| **Code system** | Declara un conjunto de conceptos con sus códigos y significado. Tiene dueño y versión | El diccionario |
| **Concept** | Una unidad de significado dentro de un code system: `system` + `code` (+ `display`) | Una entrada del diccionario |
| **Value set** | Selección de conceptos, de uno o más code systems, **para un contexto de uso** | La lista de palabras admitidas en un campo |
| **Binding** | La atadura de un campo a un value set | «Este campo solo acepta esta lista» |
| **Concept map** | Relación entre conceptos de un conjunto y otro | El diccionario bilingüe |
| **Definición vs expansión** | Las reglas que dicen qué entra / la lista concreta resultante en un momento dado | La consulta vs su resultado |

El vocabulario viene de HL7 FHIR (`CodeSystem`, `ValueSet`, `ConceptMap`), pero la mecánica no es
exclusiva de salud: sirve igual para monedas, estados de solicitud o divisiones administrativas.
Un concepto puede pertenecer a muchos value sets; un value set
no «posee» conceptos.

## 2. Antes de crear: buscá el que ya existe

Aplicá `anti-hallucination-guard`. Secuencia obligatoria:

1. Buscá en el servidor terminológico por significado, no por nombre exacto (sinónimos, otro
   idioma, singular/plural).
2. Buscá value sets que ya contengan esos conceptos con otro recorte.
3. ¿Existe un estándar externo que lo cubra? Preferilo a un code system local.
4. Solo si nada sirve: code system local, con dueño, definición por concepto y decisión registrada
   (`technical-docs-and-adr`).

**Prohibido el catálogo paralelo**: una segunda tabla `specialties` «para esta pantalla», un
`const STATUSES = [...]` en el front, o un JSON de opciones en mobile. Si el front necesita la
lista, la pide al mismo origen.

## 3. Modelado

```sql
-- ❌ texto libre o enum nativo: sin versión, sin traducción, sin equivalencias
status text check (status in ('PENDIENTE','APROBADA','RECHAZADA'))

-- ✅ referencia a concepto; la pertenencia al value set se valida aparte
status_concept_id bigint not null references terminology.concept (id)
```

1. La columna se llama `<rol>_concept_id` y tiene **FK real** al concepto — ver `database-design`.
2. La FK garantiza que el concepto existe; **no** que pertenezca al value set del campo. Eso se
   valida en el servicio (§6) y, donde el motor lo permita, con restricción o trigger.
3. En el código, el tipo es un id de marca o un objeto concepto, no un `string` suelto —
   ver `typescript-standards`.
4. La lógica de negocio compara por **código estable**, resuelto una vez y cacheado; jamás por
   `display` ni por id numérico hardcodeado.

```ts
// ❌ se rompe al traducir, corregir una tilde o resembrar
if (request.status.display === 'Aprobada') { ... }
if (request.statusConceptId === 4312) { ... }

// ✅ código estable del concepto, con nombre en un único lugar
if (request.status.is(RequestStatus.Approved)) { ... }
```

5. Transiciones entre conceptos de estado son una máquina de estados, no un `update` libre —
   ver `state-machines-workflows`.

## 4. Código vs display

| | Código | Display |
|---|---|---|
| Para | Máquinas, lógica, integraciones | Personas |
| Estabilidad | Inmutable una vez publicado | Cambia (ortografía, idioma, preferencia) |
| Unicidad | Única dentro de su `system` | No garantizada |
| Se persiste en el registro | Siempre (vía concepto) | Como **copia histórica** cuando el registro es clínico o legal |

- Un código retirado se marca inactivo; **no se reutiliza** con otro significado ni se borra.
- En registros clínicos guardá además el display mostrado y la versión: lo que el profesional vio
  es parte del registro — ver `audit-trail-history`.

## 5. Versionado

1. Code systems y value sets tienen versión. Una expansión es válida **para una versión**.
2. Cambios compatibles: agregar concepto, agregar traducción, agregar sinónimo. Incompatibles:
   cambiar significado de un código, reutilizarlo, sacarlo de un value set con datos vigentes.
3. Retirar un concepto: `inactive` + sucesor si lo hay. Los datos históricos siguen resolviendo.
   Los formularios ofrecen solo activos; las vistas de lectura muestran también inactivos.
4. Actualizar una terminología externa es un cambio planificado: diff de conceptos, impacto sobre
   datos existentes, mapeo de retirados — ver `dependency-management`.
5. La carga es generada, idempotente y con ids estables — ver `seed-data-catalogs` y
   `model-driven-schema`. Se corrige en el origen, nunca a mano en la base.

## 6. Value sets estáticos vs dinámicos

| | Estático | Dinámico |
|---|---|---|
| Quién lo define | Modelo/terminología, en tiempo de diseño | La aplicación o sus usuarios, en runtime |
| Ejemplos | Estados de un flujo, sexo, divisiones administrativas, especialidades | Etiquetas de una organización, motivos configurables por tenant |
| Ciclo | Versionado, revisado, sembrado | CRUD con autorización y auditoría |
| Documentación | Definición por concepto obligatoria | Reglas de quién crea y con qué alcance |
| Riesgo | Rigidez | Proliferación y duplicados: exigí normalización y búsqueda previa |

**Validación de pertenencia** (equivalente a `$validate-code` en un servicio terminológico FHIR):
toda entrada que traiga un concepto se valida en servidor contra el value set **del campo**, en
la versión vigente, y que esté activo. Un concepto válido de otro value set es un input inválido
— error de validación, no 500 (`error-handling-contract`). En multi-tenant, los dinámicos se
validan además contra el tenant (`multi-tenancy`).

## 7. i18n del display

- Las traducciones son **designaciones** del concepto (idioma + uso), no columnas
  `name_es`/`name_en` ni archivos de i18n del front. La UI traduce su chrome; la terminología
  traduce sus conceptos — ver `frontend-i18n-l10n`.
- Fallback explícito de idioma; nunca mostrar el código crudo al usuario.
- Ordená por display en el idioma activo con la colación correcta, no por código.
- Búsqueda de conceptos: sinónimos, sin tildes, por prefijo — ver `search-and-filtering`.
  Catálogos grandes se sirven paginados/por búsqueda, nunca la expansión completa al cliente.

## 8. Estándares externos (solo como familias)

SNOMED CT (clínica general), LOINC (laboratorio y observaciones), ICD/CIE (clasificación de
enfermedades), ATC (clasificación de medicamentos). **Licencias, ediciones nacionales y
condiciones de uso: verificar** con el responsable legal y con el organismo emisor antes de
incorporarlos o redistribuirlos. Registrá procedencia: fuente, versión, fecha, licencia.
No cargues terminología clínica desde fuentes no oficiales ni generada por IA — ver
el catálogo que fije el `CLAUDE.md` del repo.

## Anti-patrones

- `enum Status { ... }` en TypeScript como fuente de verdad de un catálogo de negocio.
- `switch` sobre strings de display.
- Un `<select>` con opciones escritas en la plantilla.
- La misma lista definida en API, web y mobile por separado.
- Crear «Otro» en vez de modelar el concepto faltante (o `text` libre acompañando al concepto
  cuando «otro» es legítimo).
- Borrar un concepto referenciado por datos históricos.

## Checklist

- [ ] Se buscó concepto/value set existente antes de crear (evidencia de la búsqueda).
- [ ] Columna `*_concept_id` con FK; tipo fuerte en el código.
- [ ] Lógica por código estable; cero comparaciones por display o id literal.
- [ ] Pertenencia al value set validada en servidor (activo, versión, tenant).
- [ ] Conceptos nuevos con definición, dueño y procedencia; decisión registrada.
- [ ] Retiro por inactivación; históricos siguen resolviendo.
- [ ] Traducciones como designaciones; fallback definido.
- [ ] Web y mobile consumen el mismo origen; sin listas duplicadas.
- [ ] Licencia de terminologías externas verificada.

## Evidencia / Definition of Done

Salida literal (`evidence-and-verification`):

1. **Búsqueda previa**: consulta y resultado que muestran que el concepto/value set no existía (o
   cuál se reutilizó).
2. **Request con concepto ajeno al value set** → respuesta de validación rechazada, pegada.
3. **Grep del diff** sin enums de catálogo, displays en condicionales ni ids de concepto literales.
4. **Carga idempotente**: segunda ejecución del sembrado sin inserciones nuevas.
5. **Registro histórico** con concepto inactivo que sigue mostrando su display.
6. No cubierto, declarado.
