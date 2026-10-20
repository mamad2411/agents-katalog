---
name: data-privacy-sensitive
description: Gate de privacidad para software que toca datos personales, financieros y biométricos (PII) — clasificación de datos, minimización por vista y endpoint, datos sensibles fuera de logs/trazas/URLs/analytics/errores, cifrado, enmascarado, retención y borrado, datos de prueba sintéticos, seudonimización vs anonimización, acceso con registro y exportes. Usar al diseñar o revisar cualquier endpoint, DTO, query, log, seed, export, integración con terceros o pantalla que muestre datos de un cliente, de un comercio o del personal interno, y como checklist obligatorio en cada PR que los toque.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Privacidad de datos personales, financieros y biométricos (PII)

Skill de **ingeniería**: controles técnicos y patrones de diseño. No es asesoría legal. Qué norma
aplica, qué base legal ampara un tratamiento y qué plazos de retención corresponden lo define el
responsable legal/de cumplimiento — ver `regulatory-compliance-mapping`. Ante la duda, tratá el
dato como sensible.

## 1. Clasificá antes de tocar

Todo campo nuevo entra al sistema con una clase. Sin clase, no se mergea.

| Clase | Qué es | Ejemplos | Trato mínimo |
|---|---|---|---|
| **Público** | Publicable por decisión del titular o del negocio | Nombre comercial de un comercio, rubro, dirección de sucursal | Igual validar que el titular lo publicó |
| **Interno** | Operativo, sin persona identificable | Configuración, catálogos, métricas agregadas | Control de acceso normal |
| **PII** | Identifica o hace identificable a una persona | Nombre, documento de identidad, correo, teléfono, dirección, geolocalización, foto, IP | Minimizar, enmascarar, fuera de logs |
| **Financiero / biométrico** | Dato patrimonial o rasgo físico usado para identificar | Extracto bancario, ingresos, deuda, capacidad de pago, score y resultado de una evaluación de riesgo, número de cuenta o tarjeta, imagen del carnet, selfie, huella facial | Todo lo de PII + acceso por rol **y** por relación con el titular, registro de cada acceso, base legal explícita |
| **Secreto** | Credencial o material criptográfico | Tokens, claves, contraseñas, cadenas de conexión | Nunca en código, logs ni repos — ver `environment-secrets-config` |

- El dato biométrico es **categoría especial** en los marcos de referencia más usados (p. ej. GDPR
  art. 9 lista datos genéticos y biométricos junto a los de salud). Usalos como vara de diseño
  aunque no te apliquen formalmente; la aplicabilidad la confirma el responsable legal.
- **Inferencias cuentan**: «solicitud rechazada por sobreendeudamiento» es un dato patrimonial
  aunque no lleve ninguna cifra. Un mensaje de notificación, un nombre de archivo o un asunto de
  correo pueden revelar el dato sin nombrarlo.
- Documentá la clase donde viva el modelo de datos (ver `model-driven-schema`), no en un wiki aparte.

## 2. Minimización por vista y por endpoint

1. Cada endpoint devuelve **solo los campos que esa vista usa**. Prohibido serializar la entidad
   ORM entera; siempre un DTO de salida explícito por caso de uso.
2. Listados y búsquedas: campos de identificación mínimos. El detalle patrimonial (extracto,
   ingresos, score) se pide aparte, con su propia autorización (`authz-access-control`) y su base
   legal (ver §3).
3. Mass assignment y over-fetching son fugas: DTO de entrada con lista blanca; `select`/`fields`
   explícitos en la query, no `SELECT *` hacia un serializador.
4. Lo que el frontend oculta sigue viajando: si el rol no debe verlo, **el servidor no lo envía**.
5. En SSR, el estado transferido al cliente es visible en el HTML: no incluyas datos sensibles que
   la vista no renderiza.

```ts
// ❌ expone columnas financieras, internas y futuras sin que nadie lo decida
return this.repo.findAll({ where: { tenantId } });

// ✅ contrato explícito: lo que no está en el DTO no sale
return clientes.map((c) => ({ id: c.id, displayName: c.displayName, estado: c.estado }));
```

## 3. Dónde NO puede aparecer PII

| Superficie | Regla |
|---|---|
| **Logs y trazas** | Identificadores opacos (id interno, correlation id). Nunca nombre, documento, monto, score, cuerpo de request/response con datos del titular, ni tokens. Redacción en el logger, no a criterio de cada autor — ver `backend-observability` |
| **URLs y query strings** | Quedan en historial, proxies, `Referer` y logs de acceso. Nada de documento, correo, monto ni id de imagen adivinable en la ruta; usá ids opacos y cuerpo de request |
| **Imágenes y adjuntos** | Carnet, selfie y comprobantes **nunca por URL pública**: se sirven autenticados y por bytes, con enlace firmado de un solo propósito — ver `file-uploads-media` |
| **Mensajes de error** | Al cliente, problem details sin datos del registro; el detalle va al log ya redactado — ver `error-handling-contract` |
| **Analytics / RUM / monitoreo de errores** | Sin datos sensibles en eventos, breadcrumbs, nombres de pantalla ni grabaciones de sesión. Scrubbing antes de enviar — ver `frontend-error-monitoring` |
| **Notificaciones** | Push, SMS y asunto de correo se ven en pantalla bloqueada: texto neutro + deep link autenticado. Nunca el monto, el resultado de la evaluación ni el documento — ver `notifications-delivery` |
| **Almacenamiento del cliente** | Nada de datos sensibles en `localStorage`, caché HTTP compartida ni capturas de pantalla de tests subidas a terceros |
| **Prompts y herramientas de IA/terceros** | Datos personales reales no se pegan en chats, issues, PRs, tickets ni servicios externos sin acuerdo de tratamiento vigente. Incluye los modelos que evalúan documentos: lo que se les manda sale de la casa |
| **Repos** | Ni dumps, ni fixtures con datos reales, ni capturas con clientes reales |

## 4. Cifrado y enmascarado

- **En tránsito**: TLS en todo salto, incluidos servicio↔base y servicio↔servicio interno.
- **En reposo**: cifrado de volumen/base y de backups como piso. Para campos de máxima
  sensibilidad, evaluá cifrado a nivel de campo con gestión de claves separada de los datos.
- No inventes criptografía: primitivas y librerías estándar, rotación de claves planificada —
  ver `security-guardrails`.
- **Enmascarado** en UI y exportes por defecto (`****1234`), con revelado explícito, autorizado
  y registrado.
- Hash ≠ anonimización: un hash sin sal de un documento de identidad se revierte por fuerza bruta,
  porque el espacio de documentos es chico y enumerable.

## 5. Seudonimización vs anonimización

| | Seudonimizado | Anonimizado |
|---|---|---|
| Definición operativa | No atribuible a una persona **sin información adicional** guardada aparte | No re-identificable por ningún medio razonable |
| ¿Sigue siendo dato personal? | **Sí** — se protege igual | No, si la anonimización es real |
| Uso típico | Analítica interna, entornos de prueba derivados | Estadísticas publicables, datasets abiertos |
| Riesgo | La tabla de correspondencia es el activo crítico | Re-identificación por combinación de cuasi-identificadores (fecha de nacimiento + zona + monto) |

- Quitar el nombre **no** anonimiza. Evaluá cuasi-identificadores, celdas chicas en agregados y
  texto libre.
- Una cifra rara re-identifica sola: en un tablero, un único crédito de ese monto en esa sucursal
  señala a una persona. Agregá con mínimos de celda.
- Afirmar que un dataset «es anónimo» requiere validación del responsable de privacidad, no del
  autor del script.

## 6. Retención y borrado

1. Cada clase de dato tiene plazo de retención y criterio de borrado **definidos por el
   responsable legal** y registrados; el código los implementa, no los decide.
2. El expediente de un crédito y los asientos contables suelen tener obligación de conservación:
   «borrar» puede ser bloquear, restringir o seudonimizar — ver `audit-trail-history`. No hagas
   borrado físico por defecto.
3. El borrado alcanza réplicas, cachés, índices de búsqueda, colas, exportes, el almacén de
   objetos y, según política, backups (`backup-restore-dr`). Una imagen borrada de la base y viva
   en el bucket no está borrada.
4. Jobs de purga idempotentes, con registro de qué se purgó (ids, no contenido) — ver
   `background-jobs-scheduling`.

## 7. Datos de prueba y entornos

- **Producción nunca baja a dev/test/staging.** Datos sintéticos generados con semilla
  determinista — ver `seed-data-catalogs` y `test-data-management`.
- Sintético ≠ real disfrazado: no mezcles nombres reales con montos inventados, ni carnets reales
  de conocidos «para probar el OCR».
- **Nunca expongas un entorno con datos personales por túneles o servicios de terceros**
  (dev tunnels, pastebins, acortadores, capturas subidas a herramientas externas). Probá en local.
- Catálogos «reales» (bancos, monedas, divisiones administrativas) se distinguen de datos de
  personas: los primeros llevan procedencia, los segundos son siempre sintéticos.

## 8. Acceso con registro y exportes

- Todo acceso de lectura a un dato sensible se registra: quién, qué registro, cuándo, desde dónde,
  con qué propósito/relación — ver `audit-trail-history`. El log de acceso no contiene el dato leído.
- Exportes (CSV, PDF, reportes): autorización propia, mínimo de columnas, registro del evento,
  caducidad del archivo, enlace firmado de un solo propósito — ver `file-uploads-media`.
- Soporte y administración no ven datos sensibles por defecto; el acceso excepcional sigue el
  patrón break-glass: motivo obligatorio, alcance acotado, caducidad y alerta al dueño del dato.

## Anti-patrones

- `logger.debug(JSON.stringify(req.body))` en el endpoint que recibe el extracto bancario.
- «Lo filtra el front.» — el dato ya salió.
- Búsqueda pública que confirma si una persona tiene una solicitud en curso.
- Copia de la base productiva «solo para reproducir un bug».
- Imagen del carnet servida por URL pública porque «el id es un uuid, nadie lo adivina».
- Campo de texto libre sin clasificar donde termina cayendo de todo.
- Ids secuenciales adivinables en recursos con datos del titular (ver IDOR en `security-guardrails`).

## Checklist por PR

- [ ] Cada campo nuevo tiene clase asignada y documentada.
- [ ] DTO de salida explícito; ningún endpoint serializa la entidad completa.
- [ ] Cero PII en logs, trazas, URLs, errores al cliente, analytics y notificaciones.
- [ ] Autorización por rol **y** por relación con el titular, verificada en servidor.
- [ ] Acceso de lectura a datos sensibles registrado.
- [ ] Imágenes y adjuntos servidos autenticados, nunca por URL pública.
- [ ] Seeds/fixtures/capturas solo con datos sintéticos.
- [ ] Exportes con autorización, columnas mínimas y registro.
- [ ] Retención/borrado del dato nuevo definidos con el responsable legal.
- [ ] Ningún servicio de terceros —modelos incluidos— recibe datos sensibles sin acuerdo vigente.

## Evidencia / Definition of Done

Para afirmar «cumple privacidad» pegá salida literal, no paráfrasis:

1. **Respuesta real** del endpoint (p. ej. `curl` contra el entorno local) mostrando que solo
   viajan los campos del DTO.
2. **Búsqueda de fugas en logs**: ejecutá el flujo y pegá el resultado de buscar en la salida de
   logs un valor sintético conocido (documento, nombre, monto de prueba) → cero coincidencias.
3. **Prueba negativa de acceso**: usuario sin relación con el titular recibe 403/404, con la
   respuesta pegada — ver `api-testing` y `security-testing`.
4. **Registro de acceso** generado por la lectura autorizada (fila o evento literal).
5. **Grep del diff** sin datos personales reales en seeds, fixtures ni snapshots.
6. Lo no verificado se declara como «no cubierto». Ver `evidence-and-verification`.
