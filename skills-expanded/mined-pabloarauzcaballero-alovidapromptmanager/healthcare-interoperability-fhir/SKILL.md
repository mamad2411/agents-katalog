---
name: healthcare-interoperability-fhir
description: HL7 FHIR como referencia de modelado e intercambio en software de salud — recursos núcleo (Patient, Practitioner, Organization, Encounter, Appointment, Observation, Condition, MedicationRequest, Consent, Coverage, Claim), referencias, identificadores, CodeableConcept/Coding, perfiles y extensiones, y mapeo modelo interno ↔ FHIR por capa anticorrupción sin acoplar el dominio. Usar al diseñar una entidad clínica nueva, al exponer o consumir una integración con otro sistema de salud, al nombrar conceptos del dominio, y para decidir cuándo NO adoptar FHIR internamente.
effort: high
---

# Interoperabilidad en salud con HL7 FHIR

FHIR es un estándar de HL7 para **intercambio** de información de salud: recursos con forma
definida, API REST y un sistema de terminología. Usalo para dos cosas: como **vocabulario de
referencia** al modelar (no reinventes lo que la comunidad ya discutió) y como **contrato de
borde** al integrar. No es, por defecto, tu esquema de base de datos.

> Verificado contra `hl7.org/fhir` (R5, v5.0.0). Muchas implementaciones y guías nacionales usan
> **R4**; nombres y elementos cambian entre versiones. Antes de integrar, confirmá la versión y la
> guía de implementación del otro extremo en la doc oficial.

## 1. Recursos núcleo y para qué sirve cada uno

| Recurso | Representa | Se confunde con |
|---|---|---|
| `Patient` | La persona que recibe atención | El usuario de la app (son cosas distintas: un usuario puede no ser paciente) |
| `RelatedPerson` | Familiar/representante vinculado a un paciente | Otro `Patient` |
| `Practitioner` | El profesional como persona | `PractitionerRole` |
| `PractitionerRole` | El profesional **en** una organización, con especialidad, lugar y horario | — (es donde vive «atiende cardiología en la clínica X») |
| `Organization` | Institución, aseguradora, grupo médico, departamento | `Location` |
| `Location` | Lugar físico donde se presta servicio | `Organization` |
| `HealthcareService` | Servicio ofrecido por una organización en un lugar | — (útil para directorios) |
| `Schedule` / `Slot` | Agenda de un recurso / franja reservable | `Appointment` |
| `Appointment` | Reserva de una atención futura, con participantes | `Encounter` |
| `Encounter` | La interacción de atención que efectivamente ocurre | `Appointment` (la cita es el plan; el encuentro, el hecho) |
| `Observation` | Medición o hallazgo: signos vitales, laboratorio, respuestas | `Condition` |
| `Condition` | Problema, diagnóstico o situación de salud | `Observation` |
| `MedicationRequest` | Orden/prescripción: suministro + instrucciones | `MedicationDispense` (entrega), `MedicationAdministration` (toma), `MedicationStatement` (reporte) |
| `Consent` | Decisión del paciente sobre uso/divulgación, tratamiento o investigación | Un flag de términos y condiciones |
| `Coverage` | Cobertura de seguro o pago de un beneficiario | `Claim` |
| `Claim` / `ClaimResponse` | Solicitud de pago/autorización a un pagador / su respuesta | `Coverage` |
| `DocumentReference` | Puntero a un documento o adjunto clínico | El binario en sí |
| `Provenance` / `AuditEvent` | Origen y autoría del dato / quién accedió o hizo qué | Entre sí — ver `clinical-records` §8 |
| `CodeSystem` / `ValueSet` / `ConceptMap` | Terminología — ver `terminology-value-sets` | Enums del lenguaje |

Antes de inventar una entidad clínica, buscá el recurso equivalente y leé su sección de
*boundaries*: ahí está resuelta la mitad de las discusiones de modelado
(`anti-hallucination-guard`).

## 2. Tipos de dato que hay que entender

**`Identifier`** — identificador de negocio (documento, matrícula, nº de póliza). Elementos:
`use`, `type`, `system`, `value`, `period`, `assigner`. `system` es el **espacio de nombres** que
hace único al `value`. Un mismo paciente tiene varios. No es el `id` lógico del recurso en el
servidor.

**`Reference`** — enlace entre recursos. Elementos: `reference`, `type`, `identifier`, `display`.
- *Literal*: URL relativa (`Patient/123`) o absoluta.
- *Lógica*: solo `identifier`, cuando conocés el identificador de negocio pero no la URL.
- *Versionada*: `Observation/1x2/_history/2`, útil para auditoría y procedencia.
- *Contenida*: recurso inline referenciado como `#p1`; solo si no tiene identidad propia.

**`Coding`** — un código de un sistema: `system`, `version`, `code`, `display`, `userSelected`.
**`CodeableConcept`** — un concepto: `coding` (0..*) + `text`. Permite varios códigos
equivalentes para el mismo concepto y conserva lo que el usuario vio/escribió.

```json
{
  "coding": [{ "system": "<uri-del-code-system>", "code": "<codigo>", "display": "<display>" }],
  "text": "texto tal como lo eligió o escribió el usuario"
}
```

Reglas: `code` sin `system` no significa nada; `display` no es la clave; guardá `version` cuando
la terminología evoluciona.

## 3. Perfiles, extensiones y guías

- **Perfil**: `StructureDefinition` que **restringe** un recurso base (cardinalidad más estricta,
  value sets obligatorios, elementos *must-support*). No puede romper las reglas del base,
  renombrar elementos ni agregar elementos base nuevos.
- **Extensión**: el mecanismo oficial para datos que el base no contempla. Se identifica por URL
  y declara en qué contexto aplica. Usala en vez de campos ad-hoc.
- **Guía de implementación (IG)**: conjunto coherente de perfiles, extensiones y value sets
  publicado como unidad (por país, red o caso de uso). Si tu contraparte sigue una IG, **esa** es
  la especificación, no el FHIR base.
- Un recurso declara conformidad en `meta.profile`; un servidor publica lo que soporta en su
  `CapabilityStatement`. Pedilo antes de integrar.
- Validá contra el perfil con un validador FHIR en CI, no a ojo (herramienta: verificar en la doc
  oficial la vigente para tu versión).

## 4. Mapeo interno ↔ FHIR sin acoplar el dominio

Arquitectura: **capa anticorrupción** en el borde. El dominio no importa tipos FHIR.

```
dominio + ORM  ◀──▶  mapper (puro, testeado)  ◀──▶  DTO FHIR  ◀──▶  API / cliente FHIR
```

1. Un mapper por recurso, **función pura** en ambos sentidos, con tests de ida y vuelta
   (`unit-testing`). Nada de lógica de negocio adentro.
2. **Tabla de mapeo** como documento versionado: campo interno ↔ elemento FHIR ↔ value set ↔
   pérdida de información. Lo que no mapea se declara, no se descarta en silencio
   (`technical-docs-and-adr`).
3. **Identidad**: tu id interno **no** es un `Identifier` de negocio. Exponé ids opacos como `id`
   lógico y los identificadores reales en `identifier` con su `system`.
4. **Terminología**: traducí conceptos internos a códigos estándar vía mapeo explícito
   (`ConceptMap` o tabla equivalente), conservando el original en `text`.
5. **Entrada desde terceros**: validá estructura y perfil, tratá todo como no confiable
   (`security-guardrails`), guardá la **procedencia** y no pises datos locales de mayor confianza.
   El narrativo HTML de un recurso no puede llevar contenido activo: sanealo igual antes de
   renderizar (`frontend-security`).
6. **Seguridad**: FHIR no define el control de acceso; lo ponés vos. Consentimiento y relación de
   atención se evalúan antes de serializar — ver `consent-management`, `authz-access-control`,
   `data-privacy-phi`. Una búsqueda FHIR es tan peligrosa como cualquier listado.
7. Versioná el contrato de integración y detectá cambios incompatibles — ver `api-openapi-docs`.

```ts
// ❌ el dominio habla FHIR: cada cambio de versión del estándar rompe el núcleo
class Appointment { participant: fhir.AppointmentParticipant[]; }

// ✅ el dominio habla su idioma; el borde traduce
export const toFhirAppointment = (a: Appointment): FhirAppointmentDto => ({ /* mapeo puro */ });
```

## 5. Cuándo NO adoptar FHIR internamente

| Situación | Decisión |
|---|---|
| Sin integración externa a la vista | Usalo como referencia de nombres y límites; no implementes API FHIR |
| Modelo relacional con invariantes fuertes (agenda, contabilidad, concurrencia) | Esquema propio normalizado (`database-design`); FHIR solo en el borde |
| Necesitás consultas analíticas o transaccionales eficientes | Guardar JSON FHIR como fuente primaria lo complica; mapeá |
| El estándar no cubre tu concepto de negocio | Modelo propio + extensión **solo** si hay que intercambiarlo |
| Una contraparte exige una IG concreta | Implementá **esa** IG en el borde, completa y validada, no «FHIR en general» |
| El equipo quiere «ser FHIR-nativo» sin caso de uso | No. Costo alto, beneficio nulo hasta que exista un interlocutor |

Señales de adopción sana: nombres de conceptos alineados, identificadores con `system`, conceptos
codificados, separación cita/encuentro y orden/dispensa, mappers testeados.

## Anti-patrones

- Llamar `Patient` al usuario de la app y mezclar credenciales con datos demográficos.
- Un solo campo `documento` sin `system`: imposible distinguir tipos ni emisores.
- Guardar solo el `display` de un diagnóstico.
- Campos propios metidos en el JSON sin extensión declarada.
- Exponer un endpoint de búsqueda FHIR sin filtro por tenant, relación ni consentimiento.
- Asumir R5 cuando la contraparte habla R4 (o al revés).
- Inventar recursos o elementos «de memoria»: verificá en `hl7.org/fhir` para la versión acordada.

## Checklist

- [ ] Versión de FHIR e IG de la contraparte confirmadas por escrito.
- [ ] Recurso equivalente buscado antes de crear una entidad clínica nueva.
- [ ] El dominio no depende de tipos FHIR; existe capa de mapeo.
- [ ] Tabla de mapeo versionada con pérdidas declaradas.
- [ ] Identificadores con `system`; conceptos con `system` + `code` (+ `version`).
- [ ] Validación contra perfil automatizada en CI.
- [ ] Control de acceso, consentimiento y minimización aplicados antes de serializar.
- [ ] Entrada externa validada, saneada y con procedencia registrada.

## Evidencia / Definition of Done

Salida literal (`evidence-and-verification`):

1. **Salida del validador FHIR** contra el perfil acordado para un recurso generado por el mapper.
2. **Tests de ida y vuelta** del mapper en verde (comando + resumen).
3. **Request/response real** contra el sandbox de la contraparte o un servidor de prueba, con
   datos sintéticos — nunca PHI real (`data-privacy-phi` §7).
4. **Prueba negativa**: consulta FHIR de un actor sin relación/consentimiento → denegada.
5. Enlace a la tabla de mapeo y a la decisión de arquitectura. No cubierto, declarado.
