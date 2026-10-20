---
name: medication-prescription-safety
description: Gate de seguridad para software que toca medicamentos y recetas — prohíbe inferir, generar o completar dosis, contraindicaciones, interacciones o equivalencias; exige fuentes con procedencia y metadatos, unidades explícitas, recetas inmutables una vez emitidas con estados emitida/dispensada/anulada, y revisión clínica humana obligatoria. El contenido generado por IA jamás entra como contenido clínico. Usar al modelar catálogos de medicamentos, construir o revisar la receta electrónica, sembrar datos farmacológicos, escribir validaciones de dosis o mostrar información de un fármaco.
effort: high
---

# Seguridad en medicamentos y recetas

Un error en este módulo no es un bug de UI: puede dañar a una persona. La skill es de
**ingeniería** — el software **transporta y preserva** decisiones clínicas, no las toma. Todo
contenido farmacológico y toda regla clínica los define y valida un profesional responsable.
No des, ni dejes que el sistema dé, consejo médico.

## 1. Línea roja: qué nunca hace el software (ni el agente)

| Prohibido | Por qué | En su lugar |
|---|---|---|
| Inferir, calcular «por defecto» o autocompletar **dosis, frecuencia, vía o duración** | Una sugerencia plausible se acepta sin leer | Campo vacío que el prescriptor completa; ayudas solo desde fuente validada y visible |
| Generar o resumir **contraindicaciones, interacciones, efectos adversos, uso en embarazo/pediatría** | No hay forma de verificar lo generado | Mostrar texto de la fuente licenciada, con versión y fecha, o no mostrar nada |
| Declarar **equivalencias** o sustituciones entre productos | Es una decisión clínica/regulatoria | Relación cargada desde la fuente, nunca deducida por nombre o principio activo |
| Inventar medicamentos, presentaciones o códigos para «tener datos» | Dato ficticio presentado como real | Catálogo con procedencia — ver `seed-data-catalogs` |
| Usar salida de un LLM como contenido clínico, ni siquiera «para revisar después» | El borrador se vuelve definitivo | IA solo en tareas no clínicas del flujo; ver §6 |
| Corregir «errores obvios» de una receta existente | No sabés si es un error | Se reporta al responsable clínico |

Si un requisito pide algo de esta tabla, **frená**: registrá la ambigüedad y escalala
(`anti-hallucination-guard`, `requirements-and-acceptance`). No lo resuelvas por conveniencia.

## 2. Catálogo de medicamentos: solo con procedencia

1. Cada registro lleva: fuente, identificador en la fuente, versión/edición, fecha de obtención,
   licencia/condición de uso, y responsable que aprobó la carga.
2. Códigos contra terminología (la familia ATC u otra que defina el responsable clínico), como
   conceptos — ver `terminology-value-sets`. Licencias: verificar.
3. Distinguí niveles y no los mezcles: principio activo · producto/presentación comercial ·
   forma farmacéutica · concentración · envase. «Paracetamol» no es un producto dispensable.
4. Carga generada, idempotente, con ids estables; correcciones en el origen, nunca a mano en la
   base (`model-driven-schema`).
5. Retiro = inactivación. Una receta histórica debe seguir resolviendo el producto que nombró.
6. Actualización del catálogo = cambio planificado con diff revisado por el responsable clínico.
7. Sin fuente aprobada → el módulo no se siembra. Campo de texto libre explícitamente etiquetado
   como «no codificado» es preferible a un catálogo inventado.

## 3. Unidades y cantidades explícitas

```ts
// ❌ número pelado: ¿mg? ¿ml? ¿comprimidos? ¿por toma o por día?
{ dose: 5, frequency: 2 }

// ✅ valor + unidad codificada, y cada magnitud nombrada
{ doseQuantity: { value: '5', unit: Unit.Milligram },
  timing: { frequency: 2, period: { value: 1, unit: Unit.Day } },
  route: Route.Oral }
```

- Toda cantidad clínica es **valor + unidad**, con la unidad como concepto codificado (UCUM es la
  familia de referencia que usa FHIR; adopción: verificar con el responsable clínico).
- **Decimal exacto**, nunca `float`: mismo criterio que dinero (`typescript-standards`,
  `database-design`). Transportá como string decimal.
- **Cero conversión implícita** de unidades. Si hace falta convertir, es una función explícita,
  testeada con casos aprobados por el responsable clínico, y el valor original se conserva.
- UI: unidad siempre visible junto al número, sin ceros finales (`5` no `5.0`), con cero inicial
  (`0.5` no `.5`), sin abreviaturas ambiguas. Formato localizado solo para mostrar, nunca para
  almacenar — ver `frontend-forms-ux`, `frontend-i18n-l10n`.
- Validaciones de rango: solo las reglas entregadas por escrito por el responsable clínico, con
  versión. Un límite inventado «razonable» es una regla clínica inventada.

## 4. La receta es inmutable una vez emitida

Máquina de estados explícita (`state-machines-workflows`):

```
borrador ──emitir──▶ emitida ──dispensar──▶ dispensada (parcial | total)
                        │
                        ├──anular──▶ anulada   (motivo + autor; no se borra)
                        └──vencer──▶ vencida   (por vigencia)
```

1. **Borrador**: editable por su autor. **Emitida**: congelada; snapshot completo de lo prescripto
   (producto, concentración, cantidades, indicaciones, prescriptor, paciente, fecha, vigencia).
2. Cambiar una receta emitida = **anular + emitir nueva** con referencia a la anterior. Nunca
   `UPDATE`. Reforzalo en la base — ver `clinical-records` §3.
3. El snapshot guarda **código + display + versión** del producto al emitir: que el catálogo
   cambie no reescribe recetas viejas.
4. Emitir exige prescriptor autenticado y **habilitado** (matrícula/rol vigentes verificados en
   servidor) — `authz-access-control`, `authn-identity`. Requisitos formales de validez de una
   receta: validar con el responsable legal.
5. Dispensar y anular son transiciones **atómicas e idempotentes**: doble clic, reintento de red
   o dos farmacias simultáneas no producen doble dispensa — `concurrency-and-locking`.
6. Dispensa parcial: se registra cantidad entregada y saldo; el total dispensado no supera lo
   prescripto.
7. Cada transición genera evento de auditoría con actor y momento (`audit-trail-history`). La
   receta es parte del registro clínico: aplica todo `clinical-records`.
8. FHIR separa orden (`MedicationRequest`), entrega (`MedicationDispense`) y toma
   (`MedicationAdministration`): conservá esa separación aunque tu modelo sea propio — ver
   `healthcare-interoperability-fhir`.

## 5. Mostrar, buscar y compartir

- Buscar medicamentos: por nombre y por principio activo, sin tildes, sin corrección automática
  que sustituya lo tipeado por «lo más parecido» — ver `search-and-filtering`. Nombres parecidos
  se muestran diferenciados, no fusionados.
- Selección siempre explícita del usuario; nada preseleccionado.
- La receta de un paciente es PHI: minimización, consentimiento y registro de acceso — ver
  `data-privacy-phi`, `consent-management`. Funciones tipo «dónde conseguir mi receta» no envían
  el contenido de la receta a proveedores de mapas ni a terceros (`maps-geolocation`).
- Notificaciones sobre recetas: texto neutro, sin nombre del fármaco (`notifications-delivery`).
- Copy clínico (advertencias, instrucciones al paciente) lo redacta y aprueba el responsable
  clínico; el equipo lo versiona, no lo escribe.

## 6. IA y automatización

| Permitido | No permitido |
|---|---|
| Generar código, tests, migraciones, datos **sintéticos de estructura** claramente falsos | Poblar catálogos farmacológicos, dosis, interacciones |
| Normalizar formato de datos ya provenientes de la fuente, con diff revisado | «Completar» campos faltantes de la fuente |
| Asistir búsqueda sobre el catálogo aprobado | Recomendar un fármaco, dosis o sustitución |
| Redactar textos de UI no clínicos | Redactar advertencias o indicaciones clínicas |

Datos de prueba: productos y pacientes evidentemente ficticios y marcados como tales, jamás
mezclados con seeds reales — ver `test-data-management`.

## 7. Revisión clínica humana obligatoria

Requiere aprobación registrada (quién, cuándo, sobre qué versión) del responsable clínico:

- carga o actualización del catálogo de medicamentos y de unidades;
- cualquier regla de validación, alerta o cálculo con semántica clínica;
- textos clínicos mostrados a pacientes o profesionales;
- cambios en el flujo de emisión, dispensa o anulación.

Sin esa aprobación, el cambio no se declara terminado: queda BLOCKED, que es un veredicto legítimo
(`evidence-and-verification`).

## Anti-patrones

- `defaultDose` en el catálogo «para agilizar».
- Un `number` para la dosis y la unidad en el placeholder del input.
- `PATCH /prescriptions/:id` sobre una receta emitida.
- Interacciones cargadas desde una planilla sin origen.
- Seeds con nombres de fármacos reales y concentraciones inventadas.
- Autocompletado que reemplaza lo escrito por el fármaco «más probable».
- Borrar una receta anulada.

## Checklist

- [ ] Ningún valor clínico inferido, generado ni por defecto.
- [ ] Catálogo con fuente, versión, fecha, licencia y aprobación; niveles de producto diferenciados.
- [ ] Cantidades como decimal exacto + unidad codificada; sin conversiones implícitas.
- [ ] Receta emitida inmutable, con snapshot; corrección por anular + reemitir.
- [ ] Transiciones atómicas e idempotentes; dispensa no supera lo prescripto.
- [ ] Prescriptor habilitado verificado en servidor.
- [ ] Auditoría en cada transición y acceso; PHI minimizado; nada a terceros.
- [ ] Sin contenido clínico de IA; datos de prueba evidentemente ficticios.
- [ ] Aprobación clínica registrada para catálogo, reglas y textos.

## Evidencia / Definition of Done

Salida literal (`evidence-and-verification`):

1. **Intento de modificar una receta emitida** → rechazo de la API y de la base, pegados.
2. **Doble dispensa concurrente** (test de integración) → una sola prospera; comando y resumen —
   ver `integrity-testing`.
3. **Consulta de procedencia**: conteo de productos sin fuente/versión = 0 —
   `data-quality-validation`.
4. **Grep del diff** sin dosis, rangos ni textos clínicos escritos por el equipo o por IA.
5. **Registro de aprobación clínica** referenciado (quién, fecha, versión).
6. No cubierto, declarado. Sin aprobación clínica → BLOCKED, no PASS.
