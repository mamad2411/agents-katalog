---
name: create-product-spec
version: 3.0.0
description: >
  Genera y optimiza fichas técnicas estandarizadas de producto a partir de Google Docs.
  Usa esta skill cuando el usuario quiera crear una ficha técnica nueva a partir de un documento de proveedor,
  reformatear una ficha existente sin formato, estandarizar información de un producto,
  o mejorar/optimizar una ficha técnica ya creada.
  También aplica cuando mencione "ficha", "ficha técnica", "producto nuevo", "datos del proveedor",
  "reformatear ficha", "optimizar ficha", o cualquier variación de "necesito documentar este producto".
  Esta skill NO se encarga de compartir, mover archivos ni enviar notificaciones — su único propósito
  es generar el documento con formato profesional.
metadata:
  openclaw:
    category: "recipe"
    domain: "ecommerce"
    requires:
      bins: ["gws", "python3", "curl"]
      skills: ["gws-docs", "gws-drive"]
---

# Ficha Técnica de Producto

> **PREREQUISITOS:** Las skills `gws-docs` y `gws-drive` deben estar disponibles.

Esta skill tiene un único propósito: **generar y optimizar fichas técnicas de producto**. Toma información de un Google Doc (documento de proveedor, ficha sin formato, evaluación de producto, etc.) y produce un Google Doc profesional con tablas, imágenes e información estructurada, listo para uso interno por los equipos de compras, logística y listing.

No se encarga de compartir documentos, mover archivos a carpetas específicas ni enviar notificaciones. Esas son responsabilidades de otras skills o del usuario.

## Modos de uso

### Modo 1: Crear ficha nueva
A partir de un documento fuente (proveedor, evaluación, notas), genera una ficha técnica desde cero con formato profesional.

### Modo 2: Optimizar ficha existente
A partir de una ficha técnica ya creada pero sin formato o con formato deficiente, la reformatea y estructura según el estándar definido aquí. Lee el documento existente, extrae toda la información, y genera un nuevo documento con el formato correcto.

## Parámetros de entrada

El usuario proporciona un valor (como URL o ID):

| Parámetro | Descripción |
|-----------|-------------|
| `DOCUMENTO_FUENTE` | Google Doc ID o URL del documento fuente (proveedor, ficha existente, etc.) |

Extrae el ID de las URLs si el usuario pega enlaces completos. El Doc ID es la cadena entre `/d/` y `/edit` en URLs de Google Docs. El Folder ID es la cadena después de `/folders/`.

### Carpeta destino de la ficha técnica

La ficha generada se crea dentro de una carpeta en Google Drive. Por defecto se usa:

**Carpeta por defecto:** `1XDpCRHI_xtel7BWlOpzl1_bBHFG5ZAac`
(URL: `https://drive.google.com/drive/folders/1XDpCRHI_xtel7BWlOpzl1_bBHFG5ZAac`)

Si el usuario especifica una carpeta diferente, usa esa en su lugar. Después de crear el documento, muévelo a esta carpeta con:

```bash
gws drive files update --params '{"fileId":"NEW_DOC_ID","addParents":"FOLDER_ID","supportsAllDrives":true}'
```

### Shared Drives

La carpeta por defecto está en un Shared Drive. Todas las operaciones de Drive (`files.get`, `files.list`, `files.update`, `permissions.create`, etc.) deben incluir `"supportsAllDrives":true` en los params. Para búsquedas (`files.list`), incluir también `"corpora":"allDrives","includeItemsFromAllDrives":true`. Sin estos flags, los archivos en Shared Drives devuelven 404.

### Carpeta de imágenes

Las imágenes extraídas se suben a una carpeta centralizada en Google Drive llamada **"Fotos para fichas técnicas"**. Al inicio del flujo, busca esta carpeta en Drive (incluyendo Shared Drives). Si no existe, créala. Usa siempre esta carpeta para todas las imágenes de todas las fichas.

### Tipografía

La fuente predefinida de todas las fichas técnicas es **Geist**. Si Google Docs no tiene Geist disponible, el sistema usará la fuente de fallback más cercana, pero la instrucción siempre debe especificar Geist.

El tamaño de texto normal por defecto es **10pt** (no 11pt que es el default de Google Docs). Los títulos y headings **no se tocan** — deben mantener sus tamaños nativos (H1=20pt, H2=16pt, H3=14pt, etc.).

**Cómo aplicar correctamente:** Usar `builder.apply_global_style()` del script `build_spec.py`, que internamente:
1. Aplica 10pt + Geist a todo el documento con `updateTextStyle`
2. Restaura los tamaños de los headings (H1=20pt, H2=16pt, H3=14pt) que fueron pisados por el paso 1
3. Restaura tamaños explícitos (ej. título a 22pt, subtítulo a 11pt)
4. Minimiza los párrafos vacíos preservados por `insertTable` (a 1pt, sin spacing) para eliminar saltos de línea no deseados entre títulos y tablas

**IMPORTANTE — No usar `spacer()` entre secciones.** Los headings ya tienen `spaceAbove`/`spaceBelow` integrado. Insertar `spacer()` (un `\n` extra) entre un heading y el contenido siguiente crea un salto de línea visible no deseado. El builder maneja automáticamente la eliminación del párrafo preservado que `insertTable` genera antes de cada tabla.

## Reglas de contenido (no negociables)

Estas reglas existen porque la ficha es un documento de referencia interna — cualquier dato inventado puede causar errores en compras, logística o listings que cuestan dinero real.

1. **Preservar toda la información.** La ficha debe contener toda la información del documento fuente — no se recorta, no se resume, no se simplifica. Se puede optimizar ligeramente la redacción (claridad, ortografía) pero el contenido informativo debe ser idéntico al original. Si el documento fuente tiene 15 campos de packaging, la ficha tiene 15 campos de packaging.
2. **Cero invención.** Campo sin dato en la fuente → `—`. Nunca estimes ni inferir valores.
3. **Cero suposiciones.** Dato ambiguo o contradictorio → `[⚠️ Verificar con proveedor]` con explicación breve.
4. **Unidades originales.** Reporta exactamente como aparecen. No conviertas cm↔mm, kg↔g, etc.
5. **Respetar estructura de la fuente.** Si hay una tabla de packaging, genera una. Si hay dos, genera dos.
6. **Idioma.** Documento final en español. Todo texto en otro idioma (EN, ZH, o cualquier otro) se traduce al español y se marca con `[Trad. del EN]`, `[Trad. del ZH]`, etc. Esto aplica a todos los campos sin excepción: nombres de producto, descripciones, respuestas de proveedor, notas técnicas, etc.
7. **Secciones ausentes.** Si una sección no existe en la fuente, incluye el encabezado con `[Sin datos en documento fuente]`.
8. **Datos contradictorios.** Incluye ambos valores y marca `[⚠️ Dato contradictorio - verificar]`.
9. **Productos vs. variantes.** Si el documento tiene múltiples productos *no relacionados*, genera una ficha separada por cada uno — **nunca omitas un tab**. Si el documento tiene **múltiples tabs** donde cada tab es una variante del mismo producto (ej. distinto tamaño, color o configuración del mismo artículo), genera **una sola ficha de familia** con las secciones compartidas unificadas y una sección "Variantes" que compara los campos que difieren. La clave para distinguir: si los tabs comparten proveedor, material, marca y descripción general pero difieren en ASIN, tamaño, color o SKU, son variantes. **IMPORTANTE:** Cuando los tabs son productos no relacionados (distinto modelo, distinto motor, distinta funcionalidad), debes generar una ficha completa e independiente para CADA tab. No proceses solo uno y descartes los demás — cada producto del documento debe tener su propia ficha.

## Flujo de ejecución

Ejecuta estos pasos en orden. Cada paso incluye los comandos exactos para el `gws` CLI.

### Paso 0 · Localizar o crear la carpeta de imágenes

Antes de empezar, busca la carpeta **"Fotos para fichas técnicas"** en Drive:

```bash
gws drive files list --params '{"q":"name=\"Fotos para fichas técnicas\" and mimeType=\"application/vnd.google-apps.folder\" and trashed=false","fields":"files(id,name)"}'
```

Si no existe, créala:

```bash
gws drive files create --json '{"name":"Fotos para fichas técnicas","mimeType":"application/vnd.google-apps.folder"}'
```

Guarda el `FOLDER_ID` de esta carpeta — se usará para todas las imágenes.

### Paso 1 · Leer el documento fuente

```bash
gws docs documents get --params '{"documentId":"DOC_ID","includeTabsContent":true}'
```

El JSON de respuesta es grande (~200-300KB). Procesa con Python para extraer datos de **todos los tabs**:

1. **Contar tabs:** `len(tabs)` en la respuesta.
2. **Para cada tab**, extraer:
   - `tabs[i].tabProperties.title` → nombre de la variante (ej. "Balance small", "Balance XL")
   - **Texto:** recorre `tabs[i].documentTab.body.content[]` → para cada `paragraph`, concatena los `textRun.content` de sus elements. Para cada `table`, recorre `tableRows[].tableCells[].content[]` extrayendo texto de cada celda.
   - **Imágenes:** NO extraer de la API de Docs (`inlineObjects` / `positionedObjects`), ya que es incompleta — hay imágenes (Google Drawings, imágenes pegadas, etc.) que no aparecen en ninguno de los dos. Las imágenes se extraen en el Paso 2 mediante HTML export.
   - **Título del producto:** el primer párrafo de texto significativo del tab.

3. **Determinar modo:**
   - Si `len(tabs) == 1` → **modo single** (producto individual). Procesa normalmente.
   - Si `len(tabs) > 1` → evaluar si son variantes o productos no relacionados:
     - **Son variantes** si comparten proveedor, material, marca y descripción general pero difieren en ASIN, tamaño, color o SKU → **modo family**.
     - **No son variantes** si son productos completamente distintos → generar fichas separadas.

4. **En modo family**, clasificar campos:
   - Extraer los mismos campos de cada tab en una lista de diccionarios.
   - Para cada campo, comparar valores entre variantes:
     - Valor **idéntico** en todos los tabs → campo **compartido** (va a `shared_specs`)
     - Valor **distinto** en al menos un tab → campo **por variante** (va a `variants.fields`)
   - Campos inherentemente por variante (siempre van a `variants.fields` aunque sean iguales): ASIN, Unique ID (UID), Color / Forma, Tamaño del Producto.
   - **Normalizar nombres de campo entre tabs.** Los tabs pueden usar nombres ligeramente distintos para el mismo campo (ej. "UID" vs "Unique ID", "ASIN /" vs "ASIN"). Al comparar valores entre tabs, normaliza los nombres para emparejar correctamente los campos equivalentes. Si un campo existe en un tab pero no en otro (después de normalizar), incluirlo igualmente con el valor del tab que lo tiene y `—` para el que no.
   - **Principio: en caso de duda, poner en la tabla de variantes.** Es mejor mostrar una fila redundante que ocultar una diferencia.

### Paso 2 · Extraer, subir y publicar imágenes

La API de Docs (`inlineObjects`, `positionedObjects`) no captura todas las imágenes del documento — hay tipos (Google Drawings, imágenes pegadas, etc.) que no aparecen. El método confiable es **exportar el documento como HTML** via Drive API, que contiene todas las imágenes visibles como data URIs base64.

**Paso 2a · Exportar como HTML:**

```bash
gws drive files export --params '{"fileId":"DOC_ID","mimeType":"text/html"}' -o /tmp/doc_export.html
```

**Paso 2b · Extraer imágenes del HTML con Python:**

```python
import re, base64, hashlib

with open("/tmp/doc_export.html", encoding="utf-8", errors="replace") as f:
    html = f.read()

imgs = re.findall(r'<img[^>]+src="(data:([^;]+);base64,([^"]+))"', html)

seen_hashes = set()
unique_images = []
for _, mime, b64_data in imgs:
    raw = base64.b64decode(b64_data)
    h = hashlib.md5(raw).hexdigest()
    if h not in seen_hashes:
        seen_hashes.add(h)
        ext = "jpg" if "jpeg" in mime else "png"
        path = f"/tmp/product_img_{len(unique_images)}.{ext}"
        with open(path, "wb") as f:
            f.write(raw)
        unique_images.append(path)
```

Esto deduplica automáticamente imágenes repetidas entre tabs (misma imagen en varios tabs genera el mismo hash).

**Paso 2c · Subir a Drive y hacer públicas:**

```bash
# Por cada imagen única extraída:
gws drive +upload /tmp/product_img_N.ext --parent FOLDER_ID --name "producto_img_N.ext"
# Anotar el file ID

gws drive permissions create --params '{"fileId":"FILE_ID","supportsAllDrives":true}' --json '{"role":"reader","type":"anyone"}'
```

La URL pública para `insertInlineImage` es: `https://drive.google.com/uc?export=view&id=FILE_ID`

### Paso 3 · Crear el documento destino

```bash
gws docs documents create --json '{"title":"Ficha Técnica — NOMBRE_PRODUCTO"}'
```

Guarda el `documentId` de la respuesta.

### Paso 4 · Escribir el contenido formateado

Genera las requests de `batchUpdate` usando el script Python `scripts/build_spec.py` (ver sección de referencia técnica más abajo). El script toma como entrada los datos extraídos y produce el JSON de requests.

El script soporta dos modos: `single` (producto individual) y `family` (familia de variantes). El modo se determina en el Paso 1 y se pasa al script a través del JSON de datos.

**Estructura del documento (modo single):**

1. **Título** — HEADING_1, centrado, azul (#2F5496), 22pt
2. **Marketplace** — Cursiva gris, centrado
3. **Imagen del producto** — Imágenes inline centradas (las subidas en Paso 2)
4. **Especificaciones técnicas** — Tabla 2 columnas con estos campos siempre presentes:

   | Campo estándar |
   |---|
   | ASIN |
   | Unique ID |
   | Modelo fabricación |
   | Proveedor |
   | Correo proveedor |
   | Marca producto |
   | Definición de nombre |
   | Productos similares mismo proveedor |
   | Color / Forma |
   | Personalización logo |
   | Material |
   | Tamaño del Producto |
   | Imágenes reales |
   | Link manuales |
   | Link imágenes del producto |
   | Link packaging |

   **Imágenes reales:** Celda destinada a contener el enlace (hipervínculo clicable) hacia la carpeta de fotos reales del producto recibido (no renders ni imágenes de marketing). En los documentos fuente, este campo suele aparecer como un hipervínculo con texto visible "Link" — se debe extraer la URL del hipervínculo (`textStyle.link.url`), no el texto visible. Si el documento fuente incluye un enlace o referencia a imágenes reales, insertarlo aquí. Si no hay dato, dejar `—`.

   **Link manuales:** Celda destinada a contener el enlace (hipervínculo clicable) hacia los manuales del producto (instrucciones de uso, fichas de seguridad, etc.). Si el documento fuente incluye un enlace o referencia a manuales, insertarlo aquí. Si no hay dato, dejar `—`.

   **Link imágenes del producto:** Celda destinada a contener el enlace (hipervínculo clicable) hacia la carpeta o repositorio de imágenes del producto (fotos de alta resolución, renders, lifestyle, etc.). Si el documento fuente incluye un enlace o referencia a imágenes, insertarlo aquí. Si no hay dato, dejar `—`.

   **Link packaging:** Celda destinada a contener el enlace (hipervínculo clicable) hacia la documentación o carpeta de packaging del producto (diseños de caja, etiquetas, artes finales, etc.). Si el documento fuente incluye un enlace o referencia a packaging, insertarlo aquí. Si no hay dato, dejar `—`.

   Los cuatro campos de enlaces deben ser hipervínculos funcionales dentro del Google Doc (usar `updateTextStyle` con `link.url`), no texto plano de URLs. **IMPORTANTE:** En los documentos fuente, los enlaces suelen estar embebidos como hipervínculos en texto genérico (ej. la celda muestra "Link" pero tiene un `textStyle.link.url` con la URL real). Siempre extraer la URL del hipervínculo, no solo el texto visible de la celda.

   Campos adicionales del documento fuente que encajen en formato tabla (clave-valor) se añaden en una segunda tabla bajo heading "Campos adicionales".

   **Información extendida (fuera de tabla):** Es habitual que los documentos fuente contengan bloques de información que no encajan en un campo clave-valor simple — por ejemplo, "Otras características", descripciones técnicas detalladas, notas de uso, etc. Esta información se presenta como un sub-apartado (HEADING_3) dentro de la sección de Especificaciones técnicas, con el contenido en viñetas (bullet list). Cada punto en viñeta conserva el nombre/título en bold seguido de la descripción. Esto permite preservar toda la información sin forzarla en celdas de tabla donde no cabe cómodamente.

   Ejemplo:
   ```
   ### Otras características
   • Anti-bacterias: Tiene una resistencia efectiva a la oxidación...
   • Saludable: Su superior no metal hace que nunca se oxide...
   ```

5. **Packaging** — Adaptar según disponibilidad de datos:
   - **Datos completos:** Tabla 4a (empaque individual/cartón) + Tabla 4b (logística/materiales)
   - **Datos parciales:** Una sola tabla con los campos disponibles
   - **Sin datos:** `[Sin datos de packaging — solicitar al proveedor]`

6. **Dudas, consultas e incidencias** — Esta sección recoge toda la comunicación y problemas documentados con el proveedor. Es importante analizar el contenido del documento fuente para clasificar correctamente cada entrada:

   - **Consultas al proveedor:** Preguntas técnicas o comerciales dirigidas al proveedor. Se presentan con la pregunta en bold azul y la respuesta en texto normal con prefijo "—". Preguntas sin respuesta: `[Pendiente de respuesta]`.
   - **Incidencias reportadas:** Problemas, errores o defectos detectados por el equipo (ej. "llegó con piezas erróneas", "mala durabilidad del color"). No son preguntas sino registros de problemas. Se presentan en una tabla con columnas "Incidencia" y "Detalle/Estado".
   - **Solicitudes de mejora:** Peticiones al proveedor para mejorar aspectos del producto (ej. "mejorar el filo"). Se incluyen en la tabla de incidencias con su estado.

   Analiza el tono y contenido de cada entrada para determinar su tipo. Una frase como "Mejorar el filo de todos los elementos" es una solicitud de mejora, no una pregunta. "¿Cuál es el MOQ?" sí es una consulta. "Set ha llegado con pcs erróneas" es una incidencia.

   Si el documento tiene ambos tipos, crea dos sub-apartados (HEADING_3): "Consultas al proveedor" y "Incidencias y solicitudes de mejora". Si solo hay uno de los dos tipos, usa un solo apartado con el nombre correspondiente.

7. **Imágenes contextuales** — Si hay imágenes de uso, problemas técnicos, etc., insertarlas junto al contenido relacionado.

8. **Documento(s) de referencia** — Sección al final del documento con heading "Documentos de referencia". Presenta los enlaces a los documentos originales usados como fuente de información en una tabla con dos columnas: "Documento" (nombre descriptivo) y "Enlace" (URL clicable). Esto permite que el usuario siempre pueda acceder a los datos originales.

   Ejemplo de tabla:

   | Documento | Enlace |
   |---|---|
   | Evaluación de proveedor — Nombre Producto | [Abrir documento](https://docs.google.com/document/d/DOC_ID/edit) |

   - Si el documento fuente es una ficha antigua, el nombre debe ser descriptivo (ej. "Ficha técnica anterior — Producto X")
   - Si son múltiples documentos de referencia, incluir una fila por cada uno
   - Los enlaces deben ser hipervínculos funcionales dentro del Google Doc (usar `updateTextStyle` con `link.url`)

**Estructura del documento (modo family):**

En modo family, la estructura cambia para unificar información compartida y separar las diferencias por variante:

1. **Título** — Nombre de la familia de producto (ej. "Balance Pad"), NO el nombre de una variante específica. HEADING_1, centrado, azul (#2F5496), 22pt.
2. **Marketplace** — Cursiva gris, centrado (compartido).
3. **Imagen del producto** — Imagen representativa de la familia. Si cada variante tiene imagen distinta, usar la del primer tab o una representativa.
4. **Especificaciones técnicas** — Tabla 2 columnas SOLO con campos **compartidos** (idénticos en todas las variantes). Mismos campos estándar que en modo single, pero solo los que no difieren entre variantes. Campos típicamente compartidos: Proveedor, Correo proveedor, Marca producto, Material, Personalización logo, Modelo fabricación, Link manuales, Link imágenes, Link packaging.
5. **Variantes** — Tabla N+1 columnas con campos que **difieren** entre variantes. Primera columna "Campo" (fondo gris), columnas siguientes nombradas con el título de cada variante (del tab). Header azul con texto blanco. Usar `builder.variants_table(names, fields)`. Campos típicamente por variante: ASIN, Unique ID, Color / Forma, Tamaño del Producto, Peso, dimensiones de packaging.
6. **Packaging** — Si los datos de packaging son idénticos entre variantes: tabla 2 columnas normal. Si difieren: tabla comparativa multi-columna (usar `variants_table`).
7. **Dudas, consultas e incidencias** — Igual que modo single (compartido a nivel familia).
8. **Documento(s) de referencia** — Igual que modo single.

**Estructura de datos JSON para el script:**

El JSON que se pasa a `build_spec.py` tiene claves en inglés. La clave `mode` determina el flujo:

**Modo single:**
```json
{
  "mode": "single",
  "title": "Nombre del producto",
  "marketplace": "amazon.es",
  "product_images": [["url", 200, 150]],
  "specs": [["ASIN", "B0DQQ8R9SQ"], ["Material", "TPE"]],
  "additional_fields": [["campo", "valor"]],
  "usage_image": {"url": "...", "w": 300, "h": 200},
  "packaging_4a": [["campo", "valor"]],
  "packaging_4b": [["campo", "valor"]],
  "questions": [
    {"question": "Pregunta?", "answer": "Respuesta", "image": {"url": "...", "w": 300, "h": 200}}
  ],
  "translated_questions": [{"question": "Q?", "answer": "A"}]
}
```

**Modo family:**
```json
{
  "mode": "family",
  "family_title": "Balance Pad",
  "marketplace": "amazon.es",
  "product_images": [["url", 200, 150]],
  "shared_specs": [["Material", "TPE"], ["Proveedor", "Phoebe"]],
  "additional_fields": [["campo", "valor"]],
  "variants": {
    "names": ["Small Azul", "Small Negro", "XL Azul", "XL Negro"],
    "fields": [
      ["ASIN", ["B0DQQ8R9SQ", "B0DQQ6YCW2", "B0DQQ7LXL1", "B0DQQ77VTY"]],
      ["Unique ID", ["B3J4K-W2J-J6", "H1R6Y-T9N-Z3", "O2X1I-Z3E-K9", "G1F2S-S7R-M1"]],
      ["Tamaño", ["40x33x5 cm", "40x33x5 cm", "50x40x6 cm", "50x40x6 cm"]],
      ["Peso", ["0.27 kg", "0.27 kg", "0.5 kg", "0.5 kg"]]
    ],
    "images": {
      "Small Azul": [["url", 200, 150]]
    }
  },
  "packaging_4a": [["campo", "valor"]],
  "packaging_4b": [["campo", "valor"]],
  "questions": [
    {"question": "Pregunta?", "answer": "Respuesta"}
  ],
  "translated_questions": [{"question": "Q?", "answer": "A"}]
}
```

Cuando `mode` está ausente, se asume `"single"`.

**Envío del batchUpdate:**

El JSON puede exceder el límite de argumentos del shell (~32KB). Divide en lotes de 80-100 requests:

```bash
# Generar JSON completo
python3 scripts/build_spec.py ARGS > all_requests.json

# Dividir en partes
python3 -c "
import json
with open('all_requests.json') as f: data = json.load(f)
reqs = data['requests']
size = 90
for i in range(0, len(reqs), size):
    part = reqs[i:i+size]
    with open(f'part{i//size}.json','w') as f: json.dump({'requests':part},f,ensure_ascii=False)
"

# Enviar cada parte
for p in part*.json; do
  gws docs documents batchUpdate --params '{"documentId":"NEW_DOC_ID"}' --json "$(cat $p)"
done
```

### Paso 5 · Mover la ficha a la carpeta destino

Mueve el documento generado a la carpeta destino (por defecto `1XDpCRHI_xtel7BWlOpzl1_bBHFG5ZAac`, salvo que el usuario indique otra):

```bash
gws drive files update --params '{"fileId":"NEW_DOC_ID","addParents":"FOLDER_ID"}'
```

### Resultado final

Al terminar, muestra al usuario:
- El enlace al documento generado: `https://docs.google.com/document/d/NEW_DOC_ID/edit`
- Un resumen de campos marcados con `[⚠️]` que requieren verificación con el proveedor
- El número de imágenes procesadas

## Referencia técnica: Google Docs API tables

El manejo de tablas en Google Docs API tiene particularidades críticas que causan errores si no se respetan. Esta sección documenta las fórmulas exactas derivadas de prueba empírica.

### Cómo funciona insertTable

Cuando llamas `insertTable` en un índice `I`:
- El párrafo existente en `I` se **preserva** (no se reemplaza)
- La tabla se crea en `I + 1`
- Se añade un párrafo trailing después de la tabla

Por tanto:
```
table_start = I + 1          (NO I)
idx_advance = 1 + table_struct_size
table_struct_size = 2 + rows × (1 + 2 × cols)
```

### Índice de párrafo de una celda

Para insertar texto en la celda `(row, col)` de una tabla que empieza en `table_start` con `cols` columnas:

```
para_idx = table_start + 3 + row × (1 + 2 × cols) + 2 × col + cumulative_offset
```

Donde `cumulative_offset` es la suma de `len(text)` de todo el texto insertado en celdas anteriores (en orden de lectura: `(0,0)`, `(0,1)`, ..., `(R-1, C-1)`).

### Verificación empírica

Para una tabla 2×2 insertada en índice 6:
```
table_start = 7
Cell(0,0) para = 10    → 7 + 3 + 0 + 0 = 10  ✓
Cell(0,1) para = 12    → 7 + 3 + 0 + 2 = 12  ✓
Cell(1,0) para = 15    → 7 + 3 + 5 + 0 = 15  ✓
Cell(1,1) para = 17    → 7 + 3 + 5 + 2 = 17  ✓
```

### Estilo de tablas

```python
# Header azul con texto blanco
{"updateTableCellStyle": {
    "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": {"red": 0.184, "green": 0.329, "blue": 0.588}}}},
    "fields": "backgroundColor",
    "tableRange": {"tableCellLocation": {"tableStartLocation": {"index": TABLE_START}, "rowIndex": 0, "columnIndex": 0}, "rowSpan": 1, "columnSpan": 2}
}}

# Columna izquierda gris claro (filas de datos)
{"updateTableCellStyle": {
    "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": {"red": 0.918, "green": 0.925, "blue": 0.941}}}},
    "fields": "backgroundColor",
    "tableRange": {"tableCellLocation": {"tableStartLocation": {"index": TABLE_START}, "rowIndex": 1, "columnIndex": 0}, "rowSpan": NUM_DATA_ROWS, "columnSpan": 1}
}}

# Ancho fijo de columna izquierda
{"updateTableColumnProperties": {
    "tableStartLocation": {"index": TABLE_START}, "columnIndices": [0],
    "tableColumnProperties": {"widthType": "FIXED_WIDTH", "width": {"magnitude": 170, "unit": "PT"}},
    "fields": "widthType,width"
}}
```

### Inserción de imágenes inline

```python
{"insertInlineImage": {
    "uri": "https://drive.google.com/uc?export=view&id=FILE_ID",
    "location": {"index": IDX},
    "objectSize": {"width": {"magnitude": W_PT, "unit": "PT"}, "height": {"magnitude": H_PT, "unit": "PT"}}
}}
# Avance de índice: idx += 1 (la imagen ocupa 1 posición)
```

## Checklist de validación

Antes de finalizar, verifica:

- [ ] Todos los datos provienen exclusivamente del documento fuente
- [ ] Los campos vacíos tienen "—", no valores inventados
- [ ] Las unidades de medida son exactas respecto al original
- [ ] La estructura de packaging refleja los datos disponibles (sin tablas vacías de más)
- [ ] Las respuestas del proveedor son textuales, sin parafraseo
- [ ] Todos los campos `[⚠️]` tienen justificación
- [ ] Las imágenes se extrajeron via HTML export (no solo de inlineObjects/positionedObjects)
- [ ] Las imágenes se deduplicaron por hash antes de subirlas
- [ ] Las imágenes se subieron a la carpeta "Fotos para fichas técnicas"
- [ ] La sección "Documentos de referencia" incluye enlaces funcionales a todos los documentos fuente
- [ ] La ficha se movió a la carpeta destino correcta
- [ ] El documento final tiene formato profesional consistente (títulos, tablas, colores)
- [ ] (Modo family) Los campos compartidos están en la tabla de 2 columnas, NO en la tabla de variantes
- [ ] (Modo family) Los campos que difieren están en la tabla de variantes, NO en la tabla compartida
- [ ] (Modo family) Los nombres de variantes coinciden con los títulos de los tabs del documento fuente
