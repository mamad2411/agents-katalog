---
name: fuentes-requerimiento
description: Como la Mesa de Servicios recibe y normaliza un requerimiento desde CUALQUIER fuente - correo, documento (docx/pdf/xlsx), transcripcion o acta de reunion de Teams/Meet, audio o video de la reunion (transcripcion local con Whisper + ffmpeg), chat, notas de llamada o relato verbal - que se extrae de cada una, como se conserva la fuente original como evidencia, como se detectan contradicciones entre fuentes, y como queda el registro normalizado de la solicitud (solicitud.md) con lo entendido, lo que falta y lo que se contradice. Cargala al recibir material de un cliente o de mesa.
---

# Fuentes de requerimiento — recepcion y normalizacion (Mesa de Servicios)

Un cliente no entrega requerimientos: entrega señales dispersas — un correo con tres
pedidos mezclados, una reunion de 40 minutos donde lo importante se dijo en 2, un Excel con
"lo que necesitamos", un audio de WhatsApp. La recepcion convierte esas señales en UN
registro normalizado que diga con claridad: que se entendio, que falta, y que se contradice.
Nada se pierde (la fuente original se conserva) y nada se inventa (lo que no esta, se marca
como faltante, no se completa con suposiciones).

## Donde queda todo
```
.mesa/solicitudes/{ID}/
├── fuentes/            la materia prima tal cual llego (inmutable)
│   ├── 01-correo-{fecha}.eml|.md
│   ├── 02-reunion-{fecha}.transcripcion.md
│   ├── 03-reunion-{fecha}.mp4  (+ .transcripcion.md generada)
│   └── 04-adjunto-{nombre}.pdf
├── solicitud.md        el registro normalizado (lo que produce la recepcion)
├── preguntas.md        rondas de preguntas y respuestas (lo produce el analista)
└── documento/          el documento estandarizado y la propuesta (lo produce el redactor)
```
El `{ID}` nace provisional (`SOL-{fecha}-{n}`) y se reemplaza por el correlativo definitivo
(`BUG-2026-003`, `PRY-2026-014`, `CTZ-2026-007`) cuando el analista cierra el tipo.

## Por fuente: que es, como entra, que se extrae

### Correo
- **Entra:** el texto pegado, un `.eml` o un reenvio. Se guarda completo, con remitente, fecha,
  asunto y los adjuntos referenciados.
- **Se extrae:** quien pide (empresa y rol, no datos personales), que pide (puede haber VARIOS
  pedidos en un correo: se separan), contexto ("desde la semana pasada", "para el cierre de
  mes"), urgencia declarada, y adjuntos mencionados que NO llegaron (se marcan faltantes).
- **Trampa tipica:** el hilo de respuestas contradice el primer correo. Se lee el hilo
  completo y prevalece lo mas reciente, anotando el cambio.

### Documento (Word, PDF, Excel, presentacion)
- **Entra:** el archivo. Se lee completo (no solo la primera pagina); un Excel se revisa hoja
  por hoja, una presentacion lamina por lamina.
- **Se extrae:** objetivo declarado, alcance, listas de funcionalidades o casos, datos de
  ejemplo, pantallas o flujos descritos, restricciones (plazos, normativas), y lo que el
  documento da por sabido sin explicar (candidato a pregunta).
- **Trampa tipica:** documentos viejos reutilizados con partes que ya no aplican. Se pregunta
  la vigencia de cada seccion dudosa.

### Transcripcion o acta de reunion (Teams, Meet, Zoom)
- **Entra:** la transcripcion automatica que genera la herramienta, o el acta escrita. Se
  guarda tal cual, con fecha, asistentes por rol y duracion.
- **Se extrae:** decisiones (quien dijo que si a que), pedidos explicitos, compromisos de
  ambas partes, dudas que quedaron abiertas en la propia reunion, y ejemplos concretos que el
  cliente dio ("por ejemplo, cuando el proveedor manda la factura sin orden de compra...").
  Los ejemplos valen oro: son casos de uso reales.
- **Trampa tipica:** las transcripciones automaticas confunden nombres de productos y
  terminos del negocio (usa el `glosario.md` de faast-brain para corregir la lectura), y
  mezclan "lo que queremos" con "lo que descartamos". Se separa explicitamente lo descartado.

### Audio o video de la reunion (grabacion cruda)
- **Entra:** `.mp4`, `.m4a`, `.mp3`, `.wav`, `.webm`. Se transcribe LOCALMENTE (sin subir el
  archivo a ningun servicio externo):
  ```bash
  ffmpeg -i reunion.mp4 -vn -ac 1 -ar 16000 reunion.wav        # extraer audio
  whisper reunion.wav --language es --model medium --output_format txt --output_dir .   # transcribir
  ```
  (si `whisper` no esta: `/mesa-servicios:setup` lo instala; `ffmpeg` viene en el setup basico).
  La transcripcion generada se guarda junto al archivo como `.transcripcion.md` y a partir de
  ahi se trata como una transcripcion (seccion anterior). Si la grabacion es larga (> 1 h),
  se transcribe completa igual: no se "salta" nada; lo que se descarta se marca.
- **Trampa tipica:** audio de mala calidad produce transcripciones con huecos. Los huecos se
  marcan `[inaudible]` y, si cae en algo importante, es una pregunta para el cliente, no una
  suposicion.

### Chat, notas de llamada, relato verbal de mesa
- **Entra:** lo que el analista de mesa escribe o pega ("me llamo el cliente y me dijo...").
- **Se extrae:** lo mismo que un correo, con una diferencia: es de segunda mano. Se marca como
  tal y se pide confirmar al cliente lo que sea decisivo.

## El registro normalizado: `solicitud.md`
```markdown
# Solicitud {ID-provisional} — {titulo corto en negocio}

**Recibida:** {fecha} · **Por:** {quien de mesa} · **Cliente:** {empresa o TRANSVERSAL (por confirmar)}
**Fuentes:** 01-correo (2026-03-10), 02-reunion-teams (2026-03-11, 42 min), 04-adjunto "Requerimiento v2.docx"
**Tipo preliminar:** bug | proyecto | cotizacion | (por determinar)

## Lo que se entendio (en lenguaje de negocio)
{que pide el cliente y para que, como lo vive el negocio; si hay varios pedidos, uno por item}

## Ejemplos concretos que dio el cliente
- {caso real mencionado, con las palabras del cliente}

## Lo que falta (candidatos a pregunta)
- {dato, decision o alcance que ninguna fuente aclara}

## Contradicciones entre fuentes
- {el correo dice X; en la reunion se dijo Y} → prevalece {cual y por que}, confirmar

## Restricciones declaradas
- {plazos, normativa, dependencias, urgencia}

## Material faltante
- {adjunto mencionado que no llego, grabacion sin transcripcion, etc.}
```

## Reglas duras
- La fuente original es **inmutable** y se conserva: nunca se edita un correo o una
  transcripcion; se anota aparte.
- Lo que no esta en ninguna fuente **no se completa con suposiciones**: va a "Lo que falta".
- Se separa lo pedido de lo descartado, y lo decidido de lo "en el aire".
- Varios pedidos en una misma fuente → varios items (y, si son de naturaleza distinta,
  varias solicitudes).
- Audio y video se transcriben en la maquina; nunca se envian a servicios externos. Los
  archivos pesados no entran a git (`.mesa/solicitudes/*/fuentes/*.mp4` en `.gitignore`).
- Datos personales de personas (RUT, telefonos, correos personales) que aparezcan en las
  fuentes NO se copian al registro normalizado: se habla de empresa y rol.
