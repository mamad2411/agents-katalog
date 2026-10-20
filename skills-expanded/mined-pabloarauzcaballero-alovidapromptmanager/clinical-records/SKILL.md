---
name: clinical-records
description: Gate de diseño del registro clínico electrónico — autoría y marca de tiempo confiables, inmutabilidad con enmiendas y adendas en vez de edición destructiva, versionado, firma y cierre de nota, visibilidad por relación de atención, adjuntos, trazabilidad de cada acceso y prohibición de borrado físico. Usar al modelar o tocar notas clínicas, evoluciones, diagnósticos, resultados, recetas, adjuntos o cualquier entidad que forme parte de la historia clínica, y al revisar un endpoint que las cree, modifique, liste o exporte.
effort: high
---

# Registro clínico

Skill de **ingeniería**. Qué constituye legalmente la historia clínica, cuánto se conserva, quién
es su custodio y qué firma es válida son definiciones del responsable legal/clínico — ver
`regulatory-compliance-mapping`. Acá está el diseño que permite cumplirlas: un registro que se
puede **defender**, porque muestra quién escribió qué, cuándo, y qué cambió después.

## 1. Propiedades que el diseño garantiza

| Propiedad | Significa | Se rompe cuando… |
|---|---|---|
| **Atribuible** | Cada entrada tiene autor real, rol y organización | Se escribe con cuenta compartida o «en nombre de» sin registrarlo |
| **Contemporáneo** | Se distingue cuándo ocurrió el hecho de cuándo se registró | Hay un solo timestamp editable |
| **Íntegro** | Lo firmado no cambia; lo que cambia deja rastro | `UPDATE` sobre la nota |
| **Completo** | Las correcciones conviven con el original | Se sobrescribe o se borra |
| **Disponible y reservado** | Lo ve quien atiende, y nadie más | Cualquier rol clínico ve a cualquier paciente |

## 2. Autoría y tiempo

1. `author` sale del contexto autenticado del servidor, **nunca** del body. Igual `organization`
   y `tenant` (`multi-tenancy`).
2. Actuar por otro (transcripción, asistente, residente supervisado) se modela: `author`,
   `recordedBy`, `supervisedBy`. No se falsea el autor.
3. Dos tiempos como mínimo, ambos en UTC con zona de origen conservada:
   - `occurredAt` — cuándo pasó el hecho clínico (lo informa el profesional, puede ser pasado).
   - `recordedAt` — cuándo se escribió (lo pone el servidor, no se edita).
   Registro tardío es legítimo; **ocultarlo** no.
4. Reloj del servidor, no del cliente. Ver `typescript-standards` para tipos de fecha.

## 3. Inmutabilidad: enmienda y adenda, no edición

Ciclo de vida de una entrada — modelalo como máquina de estados explícita
(`state-machines-workflows`):

```
borrador ──firmar──▶ firmada ──enmendar──▶ enmendada (nueva versión; la anterior queda)
                        │
                        ├──adenda──▶ (entrada hija que agrega, no reemplaza)
                        └──anular──▶ ingresada por error (visible como tal, con motivo)
```

- **Borrador**: editable solo por su autor; no es parte del registro compartido. Definí con el
  responsable clínico si caduca o se descarta.
- **Firmada**: inmutable. Cualquier cambio posterior es una operación nueva.
- **Enmienda**: corrige contenido. Crea versión N+1 que referencia a la N, con autor, fecha y
  **motivo obligatorio**. La versión N sigue consultable.
- **Adenda**: agrega información sin alterar el original. Entrada hija enlazada.
- **Ingresada por error**: marca de estado con motivo; la entrada no desaparece, se muestra
  tachada/etiquetada. Es el mismo criterio que usa HL7 FHIR con `entered-in-error` en sus recursos.

```ts
// ❌ la historia anterior deja de existir
note.content = dto.content;
await em.flush();

// ✅ versión nueva, original intacto, motivo y autor registrados
const amended = note.amend({ content: dto.content, reason: dto.reason, author: actor });
em.persist(amended); // note.supersededBy = amended; note queda inmutable
await em.flush();
```

Refuerzo en la base, no solo en el servicio: restricciones o triggers que rechacen `UPDATE` de
contenido y `DELETE` sobre entradas firmadas; permisos de tabla sin `DELETE` para el rol de
aplicación — ver `database-design` y `audit-trail-history`.

## 4. Versionado y concurrencia

- Cada entrada tiene `version` monotónica y enlace `supersedes`/`supersededBy`. La vista por
  defecto muestra la vigente **y señala** que hay historial.
- Edición concurrente de un borrador: locking optimista por versión de fila; el conflicto se le
  muestra al usuario, no se resuelve con «último gana» — ver `concurrency-and-locking`.
- Firmar es una transición atómica: o queda firmada con su hash/sello, o sigue borrador.
- Plantillas y formularios estructurados: guardá la **versión de la plantilla** con la que se
  capturó. Cambiar la plantilla no reinterpreta registros viejos.
- Conceptos codificados (diagnóstico, procedimiento): guardá código + sistema + versión + display
  mostrado al momento — ver `terminology-value-sets`.

## 5. Firma y cierre

1. Firmar = acto explícito del autor autenticado, con re-autenticación o factor adicional si la
   política lo exige (`authn-identity`).
2. Se sella: autor, rol, momento, y un hash del contenido canónico para detectar alteración.
3. Qué tipo de firma tiene validez legal: **validar con el responsable legal**. El diseño debe
   permitir enchufar el mecanismo sin rehacer el modelo.
4. Co-firma/supervisión como estados propios, no como campo libre.
5. Notas sin firmar al cierre del encuentro: visibles en un tablero de pendientes; no se firman
   solas por un job.

## 6. Quién ve qué — relación de atención

- Rol clínico **no alcanza**. El acceso exige una relación vigente con el paciente: encuentro,
  cita, pertenencia al equipo tratante, derivación, o consentimiento explícito. Sin relación →
  denegado, o break-glass — ver `consent-management` y `authz-access-control`.
- La relación tiene vigencia: termina la atención, termina el acceso rutinario.
- Segmentos de mayor reserva (los define el responsable clínico/legal): soportalos con etiquetas
  de sensibilidad por entrada evaluadas en la política de acceso, no con pantallas separadas.
- El paciente accede a su registro según política; administración y soporte **no** por defecto.
- Listados clínicos minimizan campos — ver `data-privacy-phi`.

## 7. Adjuntos

- Son parte del registro: mismas reglas de autoría, inmutabilidad, relación de atención y registro
  de acceso. Un adjunto «reemplazado» es una versión nueva.
- Almacenamiento privado, acceso por URL firmada de vida corta emitida **después** de autorizar;
  nunca bucket público ni id adivinable.
- Validación de tipo y tamaño, análisis de contenido, y metadatos (EXIF, autor del documento)
  tratados como PII — ver `file-uploads-media`.
- Guardá hash del archivo para demostrar integridad.

## 8. Trazabilidad y no-borrado

1. **Cada lectura, creación, enmienda, firma, anulación, impresión y export** genera un evento de
   auditoría: actor, paciente, entrada, acción, momento, origen, base del acceso. El evento no
   contiene el contenido clínico — ver `audit-trail-history`.
2. Distinguí **procedencia** (quién produjo el dato y cómo llegó) de **auditoría** (quién hizo qué
   con él). FHIR los separa en `Provenance` y `AuditEvent`; conviene la misma separación.
3. **Sin borrado físico** de entradas clínicas desde la aplicación. Retiro = cambio de estado.
   Solicitudes de supresión del titular y fin de plazo de conservación: proceso formal definido
   con el responsable legal, ejecutado por un procedimiento controlado y registrado.
4. Soft delete genérico **no** sirve acá: una nota «eliminada» que desaparece de la vista es una
   edición destructiva con otro nombre. Usá los estados de §3.
5. Backups y restauración conservan la cadena de versiones — ver `backup-restore-dr`.

## Anti-patrones

- `PATCH /notes/:id` que pisa el contenido de una nota firmada.
- `authorId` aceptado desde el cliente.
- Un único `updatedAt` como toda la historia del registro.
- Importaciones masivas que entran sin autor ni procedencia.
- Contenido clínico generado o resumido por IA guardado como si lo hubiera escrito el profesional
  — ver `medication-prescription-safety` §6.
- Reportes o exports que leen directo de la tabla saltándose política de acceso y auditoría.

## Checklist

- [ ] Autor, organización y tenant desde el contexto del servidor.
- [ ] `occurredAt` y `recordedAt` separados; `recordedAt` no editable.
- [ ] Estados borrador / firmada / enmendada / ingresada por error como máquina explícita.
- [ ] Enmienda y adenda crean registros nuevos con motivo; el original permanece.
- [ ] La base rechaza `UPDATE` de contenido y `DELETE` sobre entradas firmadas.
- [ ] Firma atómica con sello de autor, momento y hash.
- [ ] Acceso por relación de atención vigente + consentimiento; break-glass disponible y auditado.
- [ ] Adjuntos privados, versionados, con URL firmada y registro de acceso.
- [ ] Evento de auditoría en lectura, escritura, firma, anulación y export.
- [ ] Versión de plantilla y de terminología guardadas con la entrada.
- [ ] Retención y supresión definidas con el responsable legal.

## Evidencia / Definition of Done

Salida literal, no paráfrasis (`evidence-and-verification`):

1. **Intento de edición de una nota firmada** → respuesta de rechazo pegada, y el `UPDATE`/`DELETE`
   directo contra la base fallando por la restricción.
2. **Enmienda**: consulta que muestre versión N y N+1 coexistiendo, con motivo y autor.
3. **Prueba negativa de acceso**: profesional del mismo rol sin relación de atención → denegado.
4. **Eventos de auditoría** generados por leer, enmendar y exportar (filas literales).
5. **Adjunto**: URL sin firma o vencida → denegada.
6. Tests de integración de estas invariantes en verde, con el comando y su resumen pegados —
   ver `integrity-testing`. Lo no ejercitado, declarado «no cubierto».
