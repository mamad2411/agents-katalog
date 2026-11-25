---
name: tool-zoom-summary
description: "Genera un resumen HTML interactivo de una reunión de Zoom. Descarga transcripción VTT + chat via API, identifica los temas tratados, y produce un documento branded con timestamps clickables, recursos compartidos y mini-resumen. Usar cuando el usuario pida 'resumen zoom', 'resumen de la reunión', 'zoom summary', '/zoom', o tras una clase / call recurrente que el operador documenta semanalmente."
triggers:
  - "resumen zoom"
  - "resumen de la reunion"
  - "zoom summary"
  - "/zoom"
alwaysActive: false
---

# tool-zoom-summary

## Overview

Genera un HTML interactivo premium a partir de una reunión de Zoom. Descarga la transcripción VTT y el chat TXT via Zoom API, identifica los temas tratados, y genera un documento visual con timestamps clickables, recursos compartidos y mini-resumen para publicación en comunidad.

## Pre-requisitos

Antes de invocar esta skill, el operador necesita:

1. **Cliente Zoom API configurado** — credenciales OAuth en `.env` del repo. Variables esperadas:
   - `ZOOM_ACCOUNT_ID`
   - `ZOOM_CLIENT_ID`
   - `ZOOM_CLIENT_SECRET`

2. **Script descargador** — el operador necesita un script local que sepa hablar con la Zoom API (listar grabaciones, descargar VTT + chat). Ejemplo de interfaz esperada:
   ```bash
   node tools/zoom-api.mjs --list --days 7
   node tools/zoom-api.mjs --download MEETING_UUID --output /tmp/zoom-summary
   ```
   Si el script no existe en el repo, la skill avisa y para. El operador puede generar el script con `automation-n8n-builder` o pedirlo a Claude antes de continuar.

3. **Brand assets** — el HTML hereda colores y voz del `brand-context/` del repo. Si no hay brand-context, usa el esquema neutro por defecto en `references/color_schemes.md`.

4. **Tipos de reunión recurrentes (opcional)** — si el operador tiene clases/calls semanales con nombres predecibles, definir su mapping en `brand-context/meeting-types.md` con:
   - Patrón del topic en Zoom (ej. "contiene 'café' o 'camal'")
   - Nombre canónico de la reunión
   - Carpeta de salida
   - Esquema de color a usar

## References

- `references/color_schemes.md` — Esquemas de color sugeridos por tipo de reunión
- `references/html_template_guide.md` — Estructura HTML, CSS variables, JS interactivo

## Execution Flow

### PHASE 1: FETCH — Obtener grabaciones de Zoom

```bash
node tools/zoom-api.mjs --list --days 7
```

Si el usuario proporciona un meeting ID concreto, usar ése directamente. Si no:

**CRÍTICO: filtrar PRIMERO por título del topic, después escoger la más reciente.**

La lista de meetings devuelve TODAS las grabaciones. Debes:
1. Parsear el JSON de output y obtener el array `meetings`.
2. **Filtrar** por el tipo objetivo (ver mapping en `brand-context/meeting-types.md` si existe).
3. De la lista filtrada, escoger la más reciente por `start_time`.
4. Si NO hay coincidencias → avisar al usuario, listar lo disponible.

**Si se invoca por cron (scheduled task):**
- El prompt del cron especifica qué tipo buscar.
- Hacer match por título de topic, no solo por fecha.
- Si no hay coincidencia en últimos 7 días → salir sin generar nada. Nunca generar HTML de una reunión equivocada.

**Si se invoca manualmente (/zoom):**
- Si solo hay una reunión candidata hoy → usarla.
- Si hay varias o ambigüedad → mostrar lista con topics y horarios, preguntar.

### PHASE 2: DETECT — Identificar tipo de reunión

Match el campo `topic` de Zoom (case-insensitive) contra el mapping de `brand-context/meeting-types.md`.

Si no hay mapping configurado, preguntar al operador qué tipo es y qué esquema de color quiere.

**NUNCA procesar una reunión cuyo topic no coincide con el tipo esperado.**

### PHASE 3: DOWNLOAD — Descargar transcripción y chat

```bash
node tools/zoom-api.mjs --download MEETING_UUID --output /tmp/zoom-summary
```

Esto guarda:
- `/tmp/zoom-summary/transcript.vtt` — Transcripción VTT completa
- `/tmp/zoom-summary/chat.txt` — Mensajes de chat
- `/tmp/zoom-summary/metadata.json` — Meeting info, share URL, etc.

Leer los tres archivos. Si `processing: true`, avisar al usuario y sugerir reintentar en 15 min.

### PHASE 4: ANALYZE — Procesar contenido

#### 4a. Parse VTT Transcript
- Dividir por doble salto de línea.
- Extraer rangos de timestamp y convertir a segundos.
- Extraer nombres de speaker (patrón: "Name: text").
- Fusionar segmentos consecutivos del mismo speaker dentro de 5 segundos.

#### 4b. Parse Chat
- Extraer timestamp, sender, recipient, message.
- Identificar URLs compartidas (regex: `https?://[^\s]+`).
- Agrupar URLs por contexto/tema cuando sea posible.

#### 4c. Topic Analysis
A partir de la transcripción parseada, identificar **4-8 temas distintos**:
- Agrupar por cambios temáticos en la conversación.
- Para cada tema determinar:
  - Título (corto, descriptivo)
  - Emoji apropiado
  - Timestamps de inicio/fin (para badge de duración)
  - 3-5 puntos clave con detalles expandibles
  - Citas notables si aparece alguna potente
  - URLs relacionadas del chat (si se compartieron durante ese tema)

#### 4d. Mini-resumen
Generar 3-4 bullet points resumiendo la sesión para un post de comunidad:
- Formato: emoji + frase corta por bullet.
- Foco en qué aprendieron / qué se decidió / qué herramientas se mostraron.

#### 4e. Resources
Compilar todas las URLs del chat en grupos categorizados:
- Tools / plataformas (ej: claude.ai, github.com)
- Artículos / contenido (blog posts, videos)
- Otros enlaces
- Incluir quién lo compartió y contexto breve.

### PHASE 4.5: GLOSSARY PASS — Corregir términos de STT (OBLIGATORIO)

Las transcripciones automáticas confunden términos técnicos. **ANTES de identificar topics o generar nada**, cargar el glosario del operador si existe:

```
Read brand-context/glossary.json
```

Si no existe `brand-context/glossary.json`, copiar `brand-context/glossary-template.json` como punto de partida y pedir al operador que confirme o amplíe términos propios.

Procedimiento:

1. **Aplicar replacements con `confidence=high`** automáticamente.
   Ejemplos comunes de errores STT en castellano técnico:
   - "Cloud" → "Claude"
   - "rack" → "RAG" (en contexto de AI, no de servidores)
   - "super base" / "supa base" → "Supabase"
   - "N8n" → "n8n"
   - Nombres de personas con confusión fonética (revisar contra glossary).

2. **Para términos con `caveat`**, verificar contexto antes de reemplazar.

3. **Detectar términos nuevos sospechosos** que no estén en el glosario:
   - Homófonos de herramientas conocidas
   - Nombres propios poco comunes con mayúsculas
   - Siglas o acrónimos deletreados raro
   - Listarlos como "Dudas detectadas" y **preguntar al usuario** antes de generar HTML.

4. **Cuando el usuario confirme** un término nuevo, actualizar `brand-context/glossary.json` añadiendo el alias.

5. **Si la tarea es autónoma (cron)** y no se puede preguntar:
   - Aplicar solo `confidence=high`.
   - Para dudas críticas, usar el nombre más probable según contexto y añadir nota al final del HTML: "Nota: algunos términos fueron autocorregidos. Revisar antes de publicar."

**Regla de oro:** nunca generar HTML con un homófono donde debería ir un término técnico real.

### PHASE 4f: TIMESTAMP URL — Detectar Loom u otra plataforma

Si el operador suele subir las grabaciones a una plataforma externa (Loom, YouTube, Vimeo) para enlazar timestamps:

1. **Buscar en el chat** una URL con el patrón configurado (`loom.com/share/`, `youtu.be/`, etc.).
2. **Si no se encuentra**, preguntar al usuario por la URL.
3. **Si no hay URL externa**, usar la `share_url` de Zoom como fallback.

Formato de timestamps según plataforma:
- Loom: `LOOM_URL?t=XmYs` (ej. `?t=10m35s`)
- YouTube: `YT_URL&t=635s`
- Zoom share: solo deeplink, sin timestamp granular.

### PHASE 5: GENERATE — Construir HTML

Usando `references/html_template_guide.md` como guía estructural:

1. Cargar el template HTML del operador si existe (`brand-context/templates/zoom-summary.html`). Si no, usar el genérico de `references/`.
2. Aplicar las CSS variables del esquema de color seleccionado.
3. Construir todas las secciones: hero, nav-timeline, topic sections con talking points, resources, footer.
4. Timestamps como links clickables al URL detectado en Phase 4f.
   - **Formato del texto visible**: literalmente la etiqueta de tiempo `M:SS` o `H:MM:SS`. NUNCA "Ver", "Ver timestamp" o similares.
5. **Footer / marca de agua**: usar la marca del operador desde `brand-context/`. **No incluir** "Generado con Claude Code" ni mencionar herramientas IA en el HTML público.
6. JavaScript: fade-in observer, scroll tracking, talking point toggles.
7. **No incluir mini-summary en el HTML** — se entrega como texto en chat (ver Phase 7).

### PHASE 6: SAVE — Guardar archivo

Output folder según el tipo de reunión configurado en `brand-context/meeting-types.md`. Si no hay tipo, preguntar al usuario o usar `projects/zoom-summary/<YYYY-MM-DD>-<topic-slug>/`.

Filename: `{type-kebab}-DD-mes-YYYY.html` o el formato que el operador haya definido.

Después de guardar:
1. Confirmar el path al usuario.
2. Entregar los bloques de texto de Phase 7 en chat.
3. Limpiar `/tmp/zoom-summary/`.

### PHASE 7: ENTREGABLES DE TEXTO — Siempre por chat, nunca en el HTML

Generar estos 3 bloques como texto en el chat después de guardar el HTML:

#### 7a. 5 Títulos para publicación (máx. 50 caracteres cada uno)
- Al menos 3 centrados en lo que se vio en la sesión (no genéricos).
- Estilo: directo, con gancho, orientado a valor.
- Recomendar los mejores 1-2 con breve justificación.

#### 7b. Resumen estructurado para descripción del vídeo

Estructura sugerida (el operador puede sobrescribirla con un template en `brand-context/templates/zoom-summary-description.md`):

```
# Resumen estructurado de la clase

## Objetivo de la clase
[2-3 párrafos narrativos: qué se aprende y por qué importa. Tono directo, orientado al valor.]

## ¿Qué te llevas de esta clase?
- [Bullet corto en infinitivo o "Cómo..."]
- [...]
(7-10 bullets)

## ¿Qué se trabaja durante la clase?

### 1. Título del tema
- Sub-bullet con detalle concreto
- Sub-bullet con detalle concreto

### 2. Título del tema
- Sub-bullet
- Sub-bullet

[Mínimo 5 secciones numeradas, una por tema.]

## Herramientas, plataformas o recursos mencionados
- Herramienta 1
- Herramienta 2
[Lista simple, sin descripción.]

## Ideas, aprendizajes o reflexiones clave
- Insight accionable en una línea
- Insight accionable en una línea
[7-10 ítems.]
```

#### 7c. Mini-resumen para post de comunidad
- Crear hype para que la gente quiera ver la grabación.
- Texto plano con emojis si encaja con el brand voice del operador.
- Incluir los temas más llamativos con gancho.
- 4-6 párrafos o bullets cortos.
- CTA final hacia la grabación.

## Edge Cases

- **Grabación aún procesando**: avisar, sugerir reintento en 15 min.
- **No hay grabación hoy**: listar grabaciones recientes, dejar que el usuario elija.
- **Múltiples grabaciones el mismo día**: mostrar lista con topics y horas, preguntar.
- **No hay chat file**: generar HTML sin la sección de resources.
- **No hay transcript**: no se puede continuar — informar al usuario.
- **Reunión corta (<15 min)**: puede que solo haya 1-2 temas, ajustar secciones.

## Quality Checklist

Antes de guardar el HTML, verificar:
- [ ] Todo el CSS usa variables (sin colores hardcodeados del esquema).
- [ ] Todos los timestamps enlazan al URL correcto con `?t=` o `&t=`.
- [ ] La sección Resources incluye todas las URLs del chat.
- [ ] El nav-timeline coincide en número con las secciones de tema.
- [ ] **NO hay mini-summary en el HTML** (va como texto en chat).
- [ ] Footer correcto con nombre de la reunión, fecha y hora.
- [ ] Texto en el idioma del operador (`brand-context/`).
- [ ] Responsive: `clamp()` para fuentes, `auto-fit` para grids.
- [ ] **GLOSSARY PASS aplicado**: grep el HTML final por homófonos típicos.
- [ ] Términos nuevos confirmados con el usuario (si no es cron).
- [ ] Glosario actualizado con los términos confirmados en esta sesión.

## Skills relacionadas en el OS

- **`marketing-brand-voice`** — para asegurar que el HTML respeta la voz del operador.
- **`tool-humanizer`** — pasar el resumen de la descripción por humanizer antes de publicar.
- **`tool-visual-explainer`** — alternativa si el operador quiere un HTML standalone más visual y menos estructurado.
- **`automation-n8n-builder`** — para automatizar el cron de descarga de grabaciones recurrentes.
