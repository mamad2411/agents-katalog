---
name: insurance-workflows
description: Diseño de flujos de seguros de salud — coberturas y planes, pólizas y afiliaciones, solicitudes con su ciclo (enviada, en revisión, aprobada, rechazada), verificación de elegibilidad, autorizaciones previas, relación con facturación y reclamos, y trazabilidad de documentos. Usar al modelar o tocar seguros, coberturas, pólizas, solicitudes de autorización, elegibilidad, reclamos o cualquier flujo donde una aseguradora aprueba, cubre o paga una prestación.
---

# Flujos de seguros — reglas de diseño

Skill de ingeniería. Las reglas de cobertura, copagos, deducibles y obligaciones regulatorias
dependen del país y del contrato con cada aseguradora: **validá con el responsable de seguros/legal**
qué se cubre y bajo qué condiciones. Acá va cómo se modelan las entidades y los estados sin
inventar coberturas.

## 1. Entidades núcleo (nómbralas como el dominio real)

- **Aseguradora** (payer/organización): un catálogo real, con procedencia; no inventes
  aseguradoras ficticias (ver `seed-data-catalogs`).
- **Plan / cobertura**: qué prestaciones cubre, límites, vigencia. Las prestaciones cubiertas se
  modelan como conceptos codificados, no strings sueltos (ver `terminology-value-sets`).
- **Póliza / afiliación**: vincula a una persona con un plan por un periodo, con su número de
  afiliado. Alinea con el recurso `Coverage` de FHIR (ver `healthcare-interoperability-fhir`).
- **Solicitud / autorización**: pedido de aprobación de una prestación bajo una cobertura.
- **Reclamo (claim)**: cobro de una prestación ya realizada; alinea con `Claim` de FHIR.

No colapses estas entidades: una autorización previa no es un reclamo, y una póliza no es un plan.

## 2. Ciclo de la solicitud

Máquina de estados explícita (ver `state-machines-workflows`):

`draft` → `submitted` → `under_review` → (`approved` | `rejected` | `needs_info`) ; y `cancelled`.

- Cada transición registra actor, fecha, motivo y documento de respaldo.
- `needs_info` permite volver a `submitted` con lo pedido; no reabras `approved`/`rejected` sin
  un flujo formal.
- Los plazos (SLA de respuesta) se calculan; el vencimiento es un estado derivado, no un olvido.

## 3. Elegibilidad

- Verificar elegibilidad = ¿la persona tiene una cobertura **vigente** que incluye esta prestación
  a esta fecha? Es una consulta con fecha, no un booleano guardado.
- La respuesta de elegibilidad es un **snapshot con fecha**: guardala si la decisión depende de
  ella, porque la cobertura puede cambiar después.
- Si la elegibilidad la resuelve la aseguradora por integración, tratá su respuesta como frontera
  externa: envolvela, versioná el contrato y no propagues su formato por todo el sistema
  (ver `async-messaging-events` para integraciones).

## 4. Autorización previa

- Algunas prestaciones requieren autorización **antes** de realizarse. El flujo clínico debe poder
  bloquear o advertir cuando falta (regla de negocio en el servidor).
- La autorización aprobada tiene alcance y vigencia: una prestación, una cantidad, un rango de
  fechas. No la trates como cheque en blanco.

## 5. Relación con facturación y clínica

- Una prestación autorizada y realizada genera un **reclamo** hacia la aseguradora y, del lado
  del paciente, la parte no cubierta (copago/deducible) va a facturación
  (ver `quotations-billing`, `accounting-double-entry`).
- El vínculo prestación clínica ↔ autorización ↔ reclamo ↔ factura debe ser rastreable de punta a
  punta. La prestación clínica en sí es parte de la historia (ver `clinical-records`): no la
  modifiques para "cuadrar" con el seguro.

## 6. Documentos y trazabilidad

- Las solicitudes y reclamos llevan adjuntos (informes, órdenes, respuestas del payer): almacenamiento
  seguro y validado (ver `file-uploads-media`), nunca PHI en logs (ver `data-privacy-phi`).
- Todo cambio de estado y toda comunicación con la aseguradora queda en el rastro
  (ver `audit-trail-history`).

## Anti-patrones

- Colapsar póliza, plan, autorización y reclamo en una sola tabla.
- Elegibilidad como booleano guardado en el perfil en vez de consulta con fecha.
- Inventar coberturas, copagos o aseguradoras para "completar" datos.
- Tratar una autorización como permiso ilimitado.
- Modificar la prestación clínica para que encaje con lo que el seguro cubre.

## Checklist

- [ ] Entidades separadas: aseguradora, plan/cobertura, póliza, solicitud/autorización, reclamo.
- [ ] Prestaciones cubiertas como conceptos codificados; aseguradoras/planes con datos reales y procedencia.
- [ ] Ciclo de estados explícito con actor, fecha, motivo y respaldo por transición; SLA calculado.
- [ ] Elegibilidad como consulta con fecha; snapshot guardado si la decisión depende de él.
- [ ] Autorización con alcance y vigencia; el flujo clínico advierte si falta.
- [ ] Trazabilidad prestación ↔ autorización ↔ reclamo ↔ factura completa.
- [ ] Adjuntos seguros; sin PHI en logs; cambios auditados.
