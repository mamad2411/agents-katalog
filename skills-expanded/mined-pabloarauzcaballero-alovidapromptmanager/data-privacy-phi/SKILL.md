---
name: data-privacy-phi
description: Gate de privacidad para software que toca datos personales y de salud (PII/PHI) — clasificación de datos, minimización por vista y endpoint, PHI fuera de logs/trazas/URLs/analytics/errores, cifrado, enmascarado, retención y borrado, datos de prueba sintéticos, seudonimización vs anonimización, acceso con registro y exportes. Usar al diseñar o revisar cualquier endpoint, DTO, query, log, seed, export, integración con terceros o pantalla que muestre datos de pacientes, profesionales o usuarios, y como checklist obligatorio en cada PR que los toque.
effort: high
---

# Privacidad de datos personales y de salud (PII / PHI)

Skill de **ingeniería**: controles técnicos y patrones de diseño. No es asesoría legal. Qué norma
aplica, qué base legal ampara un tratamiento y qué plazos de retención corresponden lo define el
responsable legal/de privacidad de la empresa — ver `regulatory-compliance-mapping`. Ante la duda,
tratá el dato como sensible.

## 1. Clasificá antes de tocar

Todo campo nuevo entra al sistema con una clase. Sin clase, no se mergea.

| Clase | Qué es | Ejemplos | Trato mínimo |
|---|---|---|---|
| **Público** | Publicable por decisión del titular o del negocio | Nombre profesional en un directorio público, especialidad | Igual validar que el titular lo publicó |
| **Interno** | Operativo, sin persona identificable | Configuración, catálogos, métricas agregadas | Control de acceso normal |
| **PII** | Identifica o hace identificable a una persona | Nombre, documento de identidad, correo, teléfono, dirección, geolocalización, foto, IP | Minimizar, enmascarar, fuera de logs |
| **PHI / dato de salud** | Dato personal sobre la salud física o mental, incluida la prestación de servicios de salud | Diagnóstico, nota clínica, receta, resultado, cita con especialidad, cobertura de seguro, adjunto clínico | Todo lo de PII + acceso por relación de atención, registro de cada acceso, consentimiento |
| **Secreto** | Credencial o material criptográfico | Tokens, claves, contraseñas, cadenas de conexión | Nunca en código, logs ni repos — ver `environment-secrets-config` |

- El dato de salud es **categoría especial** en los marcos de referencia más usados (p. ej. GDPR art. 9
  lo lista junto a datos genéticos y biométricos; HIPAA lo regula como PHI). Usalos como vara de
  diseño aunque no te apliquen formalmente; la aplicabilidad la confirma el responsable legal.
- **Inferencias cuentan**: «tiene cita con oncología» es dato de salud aunque no haya diagnóstico.
  Un mensaje de notificación, un nombre de archivo o un asunto de correo pueden revelar PHI.
- Documentá la clase donde viva el modelo de datos (ver `model-driven-schema`), no en un wiki aparte.

## 2. Minimización por vista y por endpoint

1. Cada endpoint devuelve **solo los campos que esa vista usa**. Prohibido serializar la entidad
   ORM entera; siempre un DTO de salida explícito por caso de uso.
2. Listados y búsquedas: campos de identificación mínimos. El detalle clínico se pide aparte, con
   su propia autorización (`authz-access-control`) y, si corresponde, consentimiento
   (`consent-management`).
3. Mass assignment y over-fetching son fugas: DTO de entrada con lista blanca; `select`/`fields`
   explícitos en la query, no `SELECT *` hacia un serializador.
4. Lo que el frontend oculta sigue viajando: si el rol no debe verlo, **el servidor no lo envía**.
5. En SSR, el estado transferido al cliente es visible en el HTML: no incluyas PHI que la vista
   no renderiza (`angular-ssr-hydration`).

```ts
// ❌ expone columnas clínicas, internas y futuras sin que nadie lo decida
return this.em.find(Patient, { tenant });

// ✅ contrato explícito: lo que no está en el DTO no sale
return patients.map((p) => ({ id: p.id, displayName: p.displayName, initials: p.initials }));
```

## 3. Dónde NO puede aparecer PII/PHI

| Superficie | Regla |
|---|---|
| **Logs y trazas** | Identificadores opacos (id interno, correlation id). Nunca nombre, documento, diagnóstico, cuerpo de request/response clínico, ni tokens. Redacción en el logger, no a criterio de cada autor — ver `backend-observability` |
| **URLs y query strings** | Quedan en historial, proxies, `Referer` y logs de acceso. Nada de documento, correo o términos clínicos en la ruta; usá ids opacos y cuerpo de request |
| **Mensajes de error** | Al cliente, problem details sin datos del registro; el detalle va al log ya redactado — ver `error-handling-contract` |
| **Analytics / RUM / monitoreo de errores** | Sin PHI en eventos, breadcrumbs, nombres de pantalla ni grabaciones de sesión. Scrubbing antes de enviar — ver `frontend-error-monitoring` |
| **Notificaciones** | Push, SMS y asunto de correo se ven en pantalla bloqueada: texto neutro + deep link autenticado — ver `notifications-delivery` |
| **Almacenamiento del cliente** | Nada de PHI en `localStorage`, caché HTTP compartida ni capturas de pantalla de tests subidas a terceros |
| **Prompts y herramientas de IA/terceros** | PHI real no se pega en chats, issues, PRs, tickets ni servicios externos sin acuerdo de tratamiento vigente |
| **Repos** | Ni dumps, ni fixtures con datos reales, ni capturas con pacientes reales |

## 4. Cifrado y enmascarado

- **En tránsito**: TLS en todo salto, incluidos servicio↔base y servicio↔servicio interno.
- **En reposo**: cifrado de volumen/base y de backups como piso. Para campos de máxima
  sensibilidad, evaluá cifrado a nivel de campo con gestión de claves separada de los datos.
- No inventes criptografía: primitivas y librerías estándar, rotación de claves planificada —
  ver `security-guardrails`.
- **Enmascarado** en UI y exportes por defecto (`****1234`), con revelado explícito, autorizado
  y registrado.
- Hash ≠ anonimización: un hash sin sal de un documento de identidad se revierte por fuerza bruta.

## 5. Seudonimización vs anonimización

| | Seudonimizado | Anonimizado |
|---|---|---|
| Definición operativa | No atribuible a una persona **sin información adicional** guardada aparte | No re-identificable por ningún medio razonable |
| ¿Sigue siendo dato personal? | **Sí** — se protege igual | No, si la anonimización es real |
| Uso típico | Analítica interna, entornos de prueba derivados | Estadísticas publicables, datasets abiertos |
| Riesgo | La tabla de correspondencia es el activo crítico | Re-identificación por combinación de cuasi-identificadores (fecha de nacimiento + zona + sexo) |

- Quitar el nombre **no** anonimiza. Evaluá cuasi-identificadores, celdas chicas en agregados y
  texto libre.
- Referencia de método: HIPAA describe dos vías de des-identificación (determinación de experto y
  *safe harbor* por remoción de identificadores listados, 45 CFR 164.514). Afirmar que un dataset
  «es anónimo» requiere validación del responsable de privacidad, no del autor del script.

## 6. Retención y borrado

1. Cada clase de dato tiene plazo de retención y criterio de borrado **definidos por el
   responsable legal** y registrados; el código los implementa, no los decide.
2. El registro clínico suele tener obligación de conservación: «borrar» puede ser bloquear,
   restringir o seudonimizar — ver `clinical-records`. No hagas borrado físico por defecto.
3. El borrado alcanza réplicas, cachés, índices de búsqueda, colas, exportes y, según política,
   backups (`backup-restore-dr`).
4. Jobs de purga idempotentes, con registro de qué se purgó (ids, no contenido) — ver
   `background-jobs-scheduling`.

## 7. Datos de prueba y entornos

- **Producción nunca baja a dev/test/staging.** Datos sintéticos generados con semilla
  determinista — ver `seed-data-catalogs` y `test-data-management`.
- Sintético ≠ real disfrazado: no mezcles nombres reales con diagnósticos inventados.
- **Nunca expongas un entorno con datos personales por túneles o servicios de terceros**
  (dev tunnels, pastebins, acortadores, capturas subidas a herramientas externas). Probá en local.
- Catálogos «reales» (instituciones, medicamentos) se distinguen de datos de personas: los
  primeros llevan procedencia, los segundos son siempre sintéticos.

## 8. Acceso con registro y exportes

- Todo acceso de lectura a PHI se registra: quién, qué registro, cuándo, desde dónde, con qué
  propósito/relación — ver `audit-trail-history`. El log de acceso no contiene el PHI leído.
- Exportes (CSV, PDF, reportes): autorización propia, mínimo de columnas, registro del evento,
  caducidad del archivo, enlace firmado de un solo propósito — ver `file-uploads-media`.
- Soporte y administración no ven PHI por defecto; el acceso excepcional sigue el patrón
  break-glass de `consent-management`.

## Anti-patrones

- `logger.debug(JSON.stringify(req.body))` en un endpoint clínico.
- «Lo filtra el front.» — el dato ya salió.
- Búsqueda pública que confirma si una persona es paciente.
- Copia de la base productiva «solo para reproducir un bug».
- Campo de texto libre sin clasificar donde termina cayendo de todo.
- Ids secuenciales adivinables en recursos clínicos (ver IDOR en `security-guardrails`).

## Checklist por PR

- [ ] Cada campo nuevo tiene clase asignada y documentada.
- [ ] DTO de salida explícito; ningún endpoint serializa la entidad completa.
- [ ] Cero PII/PHI en logs, trazas, URLs, errores al cliente, analytics y notificaciones.
- [ ] Autorización por relación de atención y, si aplica, consentimiento verificado en servidor.
- [ ] Acceso de lectura a PHI registrado.
- [ ] Seeds/fixtures/capturas solo con datos sintéticos.
- [ ] Exportes con autorización, columnas mínimas y registro.
- [ ] Retención/borrado del dato nuevo definidos con el responsable legal.
- [ ] Ningún servicio de terceros recibe PHI sin acuerdo vigente.

## Evidencia / Definition of Done

Para afirmar «cumple privacidad» pegá salida literal, no paráfrasis:

1. **Respuesta real** del endpoint (p. ej. `curl` contra el entorno local) mostrando que solo
   viajan los campos del DTO.
2. **Búsqueda de fugas en logs**: ejecutá el flujo y pegá el resultado de buscar en la salida de
   logs un valor sintético conocido (documento, nombre, diagnóstico de prueba) → cero coincidencias.
3. **Prueba negativa de acceso**: usuario sin relación/consentimiento recibe 403/404, con la
   respuesta pegada — ver `api-testing` y `security-testing`.
4. **Registro de acceso** generado por la lectura autorizada (fila o evento literal).
5. **Grep del diff** sin datos personales reales en seeds, fixtures ni snapshots.
6. Lo no verificado se declara como «no cubierto». Ver `evidence-and-verification`.
