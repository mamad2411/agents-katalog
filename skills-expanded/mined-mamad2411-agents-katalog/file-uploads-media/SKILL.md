---
name: file-uploads-media
description: Gate de subida y manejo de archivos e imágenes en la API NestJS — validar tipo real por magic bytes y tamaño, almacenar fuera de la app en object storage, nombres no adivinables, servir por URL firmada con autorización, procesar (thumbnails, reencode) fuera del request, escaneo antivirus y tratar los adjuntos con las reglas de datos sensibles. Usar al crear o revisar cualquier endpoint que reciba un archivo (foto de perfil, documento, adjunto de ficha, comprobante), al servir un archivo subido, o al diseñar dónde y cómo se guardan los medios.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Subida y manejo de archivos y medios

Un endpoint de upload es superficie de ataque de primera: ejecución de contenido, agotamiento de
disco, acceso a archivos ajenos, malware. Tratalo como entrada hostil. Complementa
`security-guardrails` (visión general) y `data-privacy-sensitive` (un adjunto de expediente es un dato sensible).

## 1. Validación de la subida

- **Tamaño**: límite duro en el body parser / interceptor **antes** de bufferizar todo en
  memoria. Límite por tipo de archivo y por endpoint. Rechazá con 413.
- **Tipo real por contenido, no por extensión ni por `Content-Type`**: ambos los controla el
  cliente. Leé los *magic bytes* (con una librería tipo `file-type`) y validá contra una
  **allowlist** de tipos esperados (`image/png`, `image/jpeg`, `application/pdf`…). Nunca una
  denylist.

```ts
// ✅ el tipo lo decide el contenido, contra una lista blanca
const detected = await fileTypeFromBuffer(file.buffer);   // magic bytes
if (!detected || !ALLOWED_MIME.has(detected.mime)) throw new UnsupportedMediaTypeException();
// ❌ confiar en lo que dijo el cliente
if (file.mimetype === 'image/png') save(file);            // falsificable
```

- Coherencia extensión ↔ contenido detectado. Renombrá vos el archivo; no uses el nombre del
  cliente para nada del filesystem (path traversal: `../../etc/...`).
- Imágenes: reencodealas (§4) para descartar payloads escondidos en metadatos. PDFs y ofimática:
  tratalos como potencialmente maliciosos → escaneo (§5), nunca ejecutar ni renderizar en el servidor sin sandbox.
- SVG es HTML ejecutable: si lo aceptás, sanitizalo y servilo con `Content-Disposition:
  attachment` o desde un dominio aislado; nunca inline en tu origen.

## 2. Almacenamiento — fuera de la app

- Guardá los binarios en **object storage** (S3-compatible), no en el filesystem del contenedor
  (efímero en despliegues tipo Coolify) ni en la base.
- En la base guardás solo **metadatos**: `id`, `owner`/`tenant`, `content_type` detectado,
  `size`, `checksum`, `storage_key`, `created_by`, timestamps, y el vínculo al recurso.
- **Nombre/clave no adivinable**: UUID/hash, nunca `foto_1.jpg` ni el nombre original ni un id
  secuencial. Adivinable = enumerable.
- Bucket **privado por defecto**. Nada público salvo assets deliberadamente públicos, y esos en
  otro bucket. Cifrado en reposo activado.
- Separá por tenant en la clave (`{tenant}/{recurso}/{uuid}`) y validá el tenant al leer
  (`multi-tenancy`).

## 3. Servir con autorización — URL firmada

- El acceso a un archivo pasa por **tu** control de acceso, igual que cualquier recurso: quién
  pide, tiene relación con ese recurso (`authz-access-control`, y para clínicos la relación de
  atención + `data-privacy-sensitive`).
- Dos patrones: (a) proxy — tu API valida y hace stream desde el storage; simple, pero carga tu
  API; (b) **URL prefirmada** de vida corta — tu API autoriza y devuelve una URL temporal al
  storage. Preferí (b) para archivos grandes/frecuentes.
- La URL firmada vence pronto (minutos), es de un solo recurso y no se loguea con el token
  (`data-privacy-sensitive`: nada sensible en URLs que queden en logs/historial).
- Subida directa del cliente al storage: **URL prefirmada de PUT** con `content-type` y tamaño
  máximo fijados por el servidor; validá y registrá el objeto en un webhook/confirmación
  posterior. No dejes objetos huérfanos sin metadatos.

## 4. Procesamiento fuera del request

- Thumbnails, reencode, extracción de texto, marca de agua: en un **job en background**
  (`background-jobs-scheduling`), no en el request de subida. El request solo valida, guarda el
  original y encola.
- Imágenes con `sharp`: `resize` con límites máximos, `toFormat`/`toBuffer` a un formato seguro,
  descartando metadatos EXIF (que pueden traer geolocalización del paciente — privacidad).
- Límites de dimensiones y de píxeles totales: una imagen "pequeña" en bytes puede ser
  gigapíxeles y agotar memoria (decompression bomb). Fijá topes.
- Estado del medio: `uploaded → scanning → ready → failed`; la UI muestra "procesando"
  (`frontend-ux-states`). No sirvas un derivado hasta `ready`.

## 5. Escaneo antivirus/malware

- Todo archivo que un usuario podrá descargar (adjuntos, documentos) pasa por **escaneo**
  (p. ej. ClamAV como servicio) antes de quedar `ready`. Verificá integración y actualización de firmas.
- Hasta que pase el escaneo, el archivo está en cuarentena y no se sirve.
- Positivo ⇒ borrar/aislar, registrar, avisar. Nunca servir un archivo no escaneado "porque el usuario espera".

## 6. Adjuntos de expediente = datos sensibles

- Una radiografía, un PDF de laboratorio o una foto de una lesión son datos de salud: aplican
  **todas** las reglas de `data-privacy-sensitive` y `audit-trail-history` (inmutabilidad, auditoría de
  cada acceso, retención, borrado).
- Registrá cada **lectura** de un adjunto clínico en el rastro de auditoría (`audit-trail-history`).
- Datos de prueba: nunca subas archivos con datos personales reales a entornos de desarrollo (`test-data-management`).

## 7. Ciclo de vida

- Borrado: al eliminar el recurso dueño, borrá (o marcá para borrar) el objeto; evitá huérfanos
  que acumulan costo y riesgo. Para clínicos, seguí la política de retención, no borres a lo loco.
- Reconciliación periódica objeto ↔ metadato: objetos sin fila y filas sin objeto son bugs.
- Cuotas por tenant/usuario para que el storage no crezca sin control.

## Evidencia / DoD

Antes de declarar listo un endpoint de upload, pegá:
- Prueba de que un archivo con extensión falsificada (`.png` que es un ejecutable) es **rechazado** por magic bytes.
- Prueba de que un usuario sin relación con el recurso recibe 403 al pedir el archivo (y la URL firmada vencida ya no sirve).
- Salida que muestre que el original se guardó con clave no adivinable en bucket privado y que el derivado se generó en background.
- Para adjuntos clínicos: entrada de auditoría registrada en el acceso.

## Anti-patrones

- Confiar en `Content-Type`/extensión; denylist en vez de allowlist.
- Guardar en el filesystem del contenedor o en la base; usar el nombre original del cliente.
- Bucket público; claves adivinables/secuenciales; servir sin chequear autorización.
- Procesar la imagen en el request; no descartar EXIF; sin tope de píxeles.
- Servir sin escanear; datos sensibles o token en la URL; no auditar el acceso a los adjuntos.

## Checklist

- [ ] Tamaño limitado antes de bufferizar; allowlist de tipos por magic bytes; nombre propio.
- [ ] Original en object storage privado y cifrado, clave no adivinable, por tenant.
- [ ] Solo metadatos en la base; acceso servido por URL firmada corta con autorización.
- [ ] Reencode/thumbnails/OCR en background; EXIF descartado; tope de dimensiones y píxeles.
- [ ] Escaneo antivirus antes de `ready`; cuarentena mientras tanto.
- [ ] Adjuntos sensibles con sus reglas: auditoría de acceso, retención, inmutabilidad.
- [ ] Sin objetos huérfanos; cuotas por tenant; reconciliación periódica.
- [ ] Evidencia de rechazo de tipo falso, de 403 a no autorizado y de generación en background pegada.
