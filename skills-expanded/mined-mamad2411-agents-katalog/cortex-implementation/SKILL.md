---
name: cortex-implementation
description: >
  Guía paso a paso para implementar un agente Cortex en Atom desde cero o migrar
  un flow de Flowbuilder/Smarton existente. Usar siempre que alguien mencione:
  implementar Cortex, montar un agente en Atom Agent Builder, migrar Smartons a
  Cortex, configurar un bot conversacional educativo/comercial en Atom, o cuando
  el usuario comparta un JSON de flow y quiera pasarlo a Cortex. Cubre análisis
  previo del flow, configuración global, diseño del prompt, code tools de
  normalización, bases de conocimiento, conexiones en Flowbuilder y testing.
---

# Guía de Implementación Cortex en Atom

## Visión general del proceso

```
1. Análisis previo (flow JSON + conversaciones)
2. Configuración Global (instrucciones, pauta, etapas, campos)
3. Diseño del nodo Cortex (prompt + KB + code tools)
4. Conexiones en Flowbuilder (downstream logic)
5. Testing y ajustes
```

---

## 1. ANÁLISIS PREVIO

Antes de tocar el canvas, extraer del JSON del flow existente:

### Del JSON del flow (metadata export de Atom)
```python
# Nodos clave a identificar:
# - app.Smarton: cuántos hay, qué campos capturan, qué KBs usan
# - app.Formatter: qué normalizaciones hacen (programa, país, etc.)
# - app.HttpV2: endpoints y body de peticiones HTTP
# - app.Asignation: grupos/asesores asignados
# - app.Tag: etiquetas usadas
# - app.Stage: etapas del funnel
# - app.ConversionApi: eventos Meta CAPI
# - app.SaveField: campos guardados (ej: Salesforce ID)
# - app.Conditional: lógica de bifurcación
# - app.Typification: tipificaciones usadas
```

**Checklist de análisis:**
- [ ] ¿Cuántos Smartons hay y qué campos captura cada uno?
- [ ] ¿Qué Formatters existen y qué normalizan?
- [ ] ¿Hay HTTP requests? ¿Qué campos usan como input?
- [ ] ¿Hay SaveField de integraciones externas (Salesforce, HubSpot)?
- [ ] ¿Hay ConversionApi? ¿Qué eventos?
- [ ] ¿Qué tags se aplican en cada path (éxito, abandono, interés)?
- [ ] ¿Cuáles son las etapas y cuándo se asignan?

### De las conversaciones reales
Analizar el CSV de conversaciones para detectar:
- Frases que hacen fallar al bot ("solo te puedo ayudar con...")
- Programas/productos mencionados que no están en KB
- Tipificaciones por defecto altas (>50% = problema)
- Patrones de abandono

### El JSON exportado puede tener bugs de datos propios — no es la fuente de verdad definitiva
Visto en producción: el mismo catálogo (nombre→código de un listado de sedes) hardcodeado
en 3 Formatters distintos del mismo flow, **sin coincidir entre sí** para varias entradas
— y con un código duplicado entre dos entradas distintas dentro de la copia
"mayoritaria". El bot en producción probablemente ya estaba usando el código equivocado
en algunos casos, silenciosamente. Antes de migrar un catálogo así a una KB de Cortex:
- Diffear todas las copias del mismo catálogo si aparece más de una vez en el JSON.
- Si hay discrepancia, no elegir una copia "porque parece más reciente" — confirmar con
  el cliente o con la fuente autoritativa (ver siguiente punto).
- Marcar explícitamente en la KB/code tool qué valores están confirmados y cuáles no
  (ej. un flag `confirmado: true/false` por fila), para que el prompt no los use a ciegas
  para una acción irreversible (crear una cita real, por ejemplo).

**Cuando exista una colección de Postman, documentación de API, o acceso directo al
canvas real de FlowBuilder, priorizar esa fuente por sobre reconstruir specs desde el
JSON exportado** — el JSON puede estar desactualizado o ya tener el bug de arriba. Ojo
al leer el canvas real: la numeración de nodos ("Petición HTTP #1", "#2", "#3"...) es
orden de creación, no tiene relación con qué función cumple cada uno — abrir cada nodo y
confirmar la URL antes de asumir cuál es cuál. Una etiqueta "DEPRECADO" en un nodo suele
referirse al *tipo de componente* (ej. "Petición HTTP" v1 vs "HttpV2"), no
necesariamente a que ese endpoint específico esté fuera de uso — confirmar antes de
descartarlo.

---

## 2. CONFIGURACIÓN GLOBAL

### Instrucciones Generales
Solo va tono, idioma y restricciones globales. La lógica de conversación va en el nodo.

```
[NOMBRE DEL BOT] es el [ROL] de [EMPRESA].

TONO Y ESTILO
- [Formal/Cercano/Profesional]: [descripción]
- Idioma: español latinoamericano neutro. Tuteo (tú/te/tu). Nunca voseo.
- Usar el nombre del usuario en cuanto esté disponible.
- Máximo 3-4 oraciones por mensaje.
- Emojis con moderación: máximo 1 por mensaje.

LO QUE NUNCA HACE
- Inventar datos que no están en la base de conocimiento.
- Hacer más de 2 preguntas en el mismo mensaje.
- Responder [casos específicos del cliente que deben evitarse].
```

### Reconocimiento de Pauta
Activar si el cliente usa Click-to-WhatsApp Ads de Meta.

Prompt de pauta:
```
Usá la información del anuncio para personalizar el primer mensaje.
Mencioná directamente el producto/servicio del anuncio. No preguntes
"¿en qué puedo ayudarte?" — ya sabés qué le interesó. Arrancá
confirmando el interés y ofreciendo el siguiente dato más relevante.
```

### Etapas del Funnel
Configurar en orden. Cada una requiere nombre en Atom + condición en lenguaje natural.

**No asumir el orden por cómo aparecen listadas en el JSON del flow viejo o en cualquier
plantilla — cada etapa trae un campo `order` explícito (`attrs.data.stage.order` en el
export) y hay que leerlo siempre.** Pasó en producción: se listaron las etapas en el
orden de aparición ("Awareness, Lead, MQL, Opportunity, SQL") y el cliente lo detectó de
inmediato porque el `order` real tenía Opportunity **después** de SQL, no antes —
Opportunity resultó ser una etapa de gestión activa post-handoff que el bot nunca debía
marcar. Un error de este tipo en las Condiciones de Finalización haría que el propio bot
avance una etapa que le corresponde solo al asesor humano.

| Etapa | Condición típica |
|---|---|
| Awareness | Primera consulta, sin interés concreto aún |
| Lead | Mostró interés en un producto/programa específico |
| MQL | Perfil calificado, cumple requisitos del producto |
| SQL | Datos completos capturados, listo para asesor/compra |

(Puede haber etapas posteriores a SQL, como Opportunity, que pertenecen al ciclo del
asesor humano después del handoff — confirmar con el `order` real de la cuenta si el bot
debe llegar hasta ahí o detenerse antes.)

### Etiquetas
Crear las que correspondan al cliente. Típicas:
- `Interesado` — mostró interés concreto
- `Datos completos` — capturó todos los campos requeridos
- `ABANDONO` — dejó de responder antes de completar
- `Exploración` — solo quería info, sin intención de compra
- `SAC` — derivado a servicio al cliente
- Tags por categoría de producto (ej: `MA Ejecutivas`, `Open Programs`)

### Tipificaciones
Máximo 15. Deben responder preguntas de negocio. Ejemplos:
- `Interesado - [Categoría A]`
- `Interesado - [Categoría B]`
- `MQL Calificado`
- `No califica`
- `No interesado`
- `Solo información`
- `Alumni / Ya apliqué`

**Las tipificaciones y las Condiciones de Finalización las evalúa el propio nodo (la IA
del agente), no un asesor humano al cerrar el chat.** Es el mismo mecanismo que las
tipificaciones nativas tipo "Consulta Resuelta x Bot": una condición en lenguaje natural
en el panel del nodo, evaluada automáticamente. Al proponer una tipificación nueva (ej.
para medir un evento de conversión), escribir la condición para que la evalúe la IA
("El cliente especificó X y fue derivado a Y"), no diseñarla asumiendo un paso manual
humano.

### Campos a Identificar y Guardar (Global)
Son opcionales — se capturan si el usuario los menciona. NO bloquean el flujo.
Agregar todos los campos de contacto: nombre, apellido, email, país, cargo, empresa, etc.
Los campos obligatorios van en el nodo individual.

**Son independientes de cualquier nodo** — no hace falta que el prompt de un nodo
puntual los mencione para que se capturen; el propio panel de Atom lo aclara ("Define qué
información debe identificar y guardar el agente si el cliente la menciona durante la
conversación"), es transversal a toda la conversación. No asumir que un campo global "no
está conectado" solo porque no aparece referenciado en el prompt de un nodo — confirmar
directamente en el panel de Configuración Global antes de reportarlo como bug.

**La descripción de cada campo tiene un tope de 200 caracteres** (el nombre del campo es
un input separado, sin ese límite). Si el campo necesita enumerar una lista larga de
valores válidos (ej. 10 categorías de producto), esa lista no entra en la descripción —
dejar la descripción corta ("ver instrucciones del Agente de [X]") y poner la enumeración
completa en el prompt del nodo Cortex relevante, que tiene 10,000 caracteres de margen.

**Bug visto en producción — campos de sistema (`first_name`/`last_name`/`email`/
`phone`) se auto-completan mal cuando están marcados como reconocibles acá.** Caso real:
el bot preguntó "¿para qué vehículo la necesitas (modelo y año)?", el cliente respondió
"Hilux 2018", y el sistema guardó `first_name: "Hilux"` / `last_name: "2018"` — tomó la
respuesta a una pregunta de producto como si fuera el nombre, solo porque tenía forma de
dos palabras. En otra prueba del mismo nodo, en vez de mal-asignar, directamente **pidió
proactivamente** nombre y apellido aunque el prompt del nodo decía "máximo 2 datos, no
pidas más" — sugiere que el reconocimiento global de estos campos puede operar por
encima de las instrucciones de minimización de datos del nodo.

**Mitigación (agregar siempre que el nodo tenga estos campos de sistema activos):** una
regla explícita en el prompt, ej.:
```
Nunca guardes first_name/last_name a partir de una respuesta que no sea explícitamente
el nombre del cliente. Un modelo de vehículo, una marca, un año o cualquier dato de
producto NUNCA es un nombre, aunque tenga formato de dos palabras.
```
Esto reduce el riesgo pero no está confirmado que lo elimine del todo — si el problema
persiste después de esta regla, es señal de que la causa es la extracción automática de
campos de sistema a nivel plataforma, no algo controlable 100% desde el prompt. Reportar
como bug de producto en ese caso, no seguir iterando el prompt indefinidamente.

### Recuperación por Inactividad
Para educación/consultoría: 3 intentos, timeouts de 3h / 6h / 12h.

- **Intento 1** (3h): Retomar mencionando el producto específico de interés. Tono suave, sin urgencia.
- **Intento 2** (6h): Ofrecer alternativa de bajo compromiso (folleto, link, agendar llamada).
- **Intento 3** (12h): Usar mensaje de cierre exacto del cliente anterior si existe, o: `"Daremos por finalizada la conversación por el momento. Si más adelante deseas retomar, estaré aquí para ayudarte. ¡Hasta luego! 👋"`

**Confirmado por el equipo de producto de Atom:** Cortex ya no tiene el concepto de
"ramas" de Flowbuilder — el recupero se adapta según el momento conversacional en el que
está el usuario, no según una rama específica. Si el caso de uso necesita un recupero
**distinto por sitio/rama puntual del flujo** (no solo por etapa del funnel), eso todavía
**no se puede configurar nativamente en Cortex** — hay que resolverlo en Flowbuilder.
Detectarlo temprano si el flow viejo tenía recuperos diferenciados por rama.

### Zona Horaria
Usar la zona del país principal de operación del cliente. **La fecha/hora actual que el
prompt puede referenciar (para instrucciones tipo "hoy es...") se toma automáticamente de
esta configuración — no existe una variable de sistema tipo `{{fecha_actual}}` separada,
ni hace falta declararla; alcanza con configurar bien la zona horaria acá.**

---

## 3. NODO CORTEX

### El prompt es UN SOLO campo de texto, con límite de 10,000 caracteres

El nodo Cortex de Atom no tiene campos separados por sección — es un único textarea. Las
"secciones" de abajo son subtítulos (`#`) dentro de ese mismo texto, no UI distinta.
**Draftear, contar caracteres, y recién entonces entregarlo** — un primer borrador
completo con las 7 secciones fácilmente pasa los 10,000 (visto en producción: 10,257,
tuvo que comprimirse a ~6,900 sin perder lógica, solo acortando prosa). Al comprimir:
sacar redundancia entre secciones (ej. "nunca inventes precios" repetido en ROL y en
CAPACIDADES), no sacar reglas.

**Las Condiciones de Finalización NO van dentro de este texto** — a pesar de que el
listado de abajo las incluya como 7ma sección, en la práctica es una configuración
**separada** en la UI de Atom (cada condición es un par Nombre/Condición en su propio
panel, fuera del campo de prompt). Diseñarlas junto con el resto del prompt está bien,
pero al momento de cargarlas en Atom van en su lugar correspondiente, no pegadas al
final del texto del prompt.

### Anatomía del Prompt (6 secciones — Condiciones de Finalización va aparte, ver arriba)

```
# ROL Y OBJETIVO
[Quién es el bot, qué hace, qué NO hace]

# CONTEXTO
[Info de la empresa, categorías de productos/servicios, sedes]

# CAPACIDADES Y HERRAMIENTAS
[Bases de conocimiento disponibles, qué puede y qué no puede responder]

# FLUJO DE CONVERSACIÓN
[Pasos ordenados: saludo → identificar interés → informar → calificar → capturar datos → cierre]

# NORMALIZACIÓN Y GUARDADO DE CAMPOS
[Instrucciones para invocar code tools antes de guardar campos]

# VERIFICACIÓN DE CAMPOS
[No repetir preguntas ya respondidas. Validar formato de email y datos numéricos]

# LÍMITES DE MENSAJERÍA
[Max mensajes consecutivos, no decir "claro/entendido", consolidar info]
```

### Cuando el nodo cubre varias líneas de negocio con distintos requisitos

Si distintas ramas de la conversación necesitan datos distintos (ej. Taller necesita
placa/fecha/hora, Ventas solo necesita modelo), **toda la bifurcación va en el prompt**
(sección FLUJO DE CONVERSACIÓN, una sub-rama por línea) — nunca en "Campos a Consultar"
(ver más abajo, sección obligatorios por nodo), porque esos campos se piden **siempre,
para cualquier rama, sin condición posible**. Poner ahí un campo que solo aplica a una
línea rompe todas las demás.

### Instrucciones Generales (Global) vs. prompt del nodo — no son independientes

Las Instrucciones Generales (Configuración Global) se aplican **siempre, sobre cualquier
nodo**, incluso si el prompt del nodo describe un alcance más chico. Si se arma una
versión simplificada del prompt de un nodo para una prueba puntual (por ejemplo, aislar
un solo caso de uso mientras se depuran bugs), y las Instrucciones Generales todavía
describen el alcance completo del bot, esa descripción más amplia se va a filtrar en los
saludos igual. Al simplificar un nodo para testear, evaluar si también hace falta
achicar temporalmente las Instrucciones Generales, o aceptar el filtrado como limitación
conocida de la prueba.

### Saludo inicial
**Crítico:** El primer mensaje debe combinar saludo + pregunta orientadora. Nunca solo "Hola, ¿en qué puedo ayudarte?".
- Si viene de pauta: mencionar directamente el producto del anuncio.
- Si es orgánico: saludar + pregunta de orientación en el mismo mensaje.

### Captura de datos
Para más de 3 campos: usar formato de lista (bullets), no conversacional.
Si el cliente tiene WhatsApp Flows habilitado: activar para captura de formulario (mejor UX).

**Validaciones a incluir siempre en el prompt:**
- Email: verificar formato con @ y dominio antes de guardar.
- Números (años de experiencia, edad): pedir valor numérico exacto si la respuesta es ambigua.

### Campos a Consultar (obligatorios por nodo)
Solo los que bloquean el avance. Típicamente:
- Nombre
- Email
- Producto/programa de interés
- Campos de calificación (ej: años de experiencia para programas ejecutivos)

**Regla:** si el campo aplica solo a cierta categoría, indicarlo explícitamente en el prompt.

**Confirmado en Atom (no es solo una suposición del prompt): un campo listado acá se
pregunta SIEMPRE, para toda la conversación, sin excepción posible por rama.** El aviso
de la propia UI lo dice literal: *"Todos los campos que el cliente debe proporcionar
serán requeridos para avanzar."* No hay forma de condicionarlo desde este panel. Si el
nodo cubre más de una línea de negocio y cada una necesita campos distintos, la solución
NO es esta lista — es (a) dejarla vacía o con lo mínimo común a todas las líneas, y (b)
que el prompt (sección FLUJO DE CONVERSACIÓN) pida cada dato en el momento justo según
la rama, guardándolo vía "Campos a Identificar y Guardar" (opcional, global) en lugar de
declararlo obligatorio acá.

### Condiciones de Salida (Fin)
Típicamente 3 condiciones mínimas:
1. **Calificado / Asignar a asesor** — datos completos + perfil validado
2. **Solo información** — recibió info, no quiso dar datos
3. **No califica** — no cumple requisitos; ofrecer alternativa antes de cerrar

**No cerrar apenas se completan los campos obligatorios — confirmar y avisar la
transferencia antes de salir.** Visto en producción (caso Finesa, marcado explícitamente
por el equipo de producto como "valioso para todos"): un agente que salía apenas
recolectaba nombre+email, sin despedida ni aviso, porque la condición de salida solo
decía "cuando haya recopilado los datos con éxito". La condición de salida hacia
"Calificado/Asignar a asesor" debería exigir las 3 cosas en conjunto:
- Que los datos obligatorios se hayan recopilado (nombrarlos explícitamente).
- Que el cliente haya confirmado si desea algo más o no.
- Que el agente haya avisado que va a transferir/derivar.

**Los ejemplos dentro del prompt también son instrucciones — no solo el texto
prescriptivo.** Mismo caso Finesa: el agente pedía el teléfono aunque no era campo
obligatorio ni estaba pedido explícitamente en las instrucciones — la causa era que el
teléfono aparecía en un ejemplo de conversación dentro del prompt. Al revisar un prompt
por comportamiento no deseado, revisar también los bloques de ejemplo, no solo las
reglas.

### Formatos de Respuesta
- **Botones**: activar. Para preguntas con 2-3 opciones cerradas.
- **Lista**: activar. Para presentar múltiples opciones de productos.
- **Carrusel**: solo si hay imágenes cargadas en KB por cada ítem.

**Problema frecuente — mensaje duplicado:** Si el agente genera texto + componente (lista/botones) en el mismo turno, Cortex los renderiza como 2 mensajes. Solución: agregar en la descripción de ejecución del formato: *"Cuando uses este formato, no incluyas texto introductorio separado — el texto y el componente son un solo mensaje."*

**WhatsApp Flows — el texto del botón que abre el formulario no es configurable
directamente.** Cortex toma automáticamente los primeros ~20 caracteres del texto del
mensaje que acompaña al formulario como texto del botón (reportado independientemente en
dos clientes distintos, Dycar y una cuenta de Open English, ambos con el mismo síntoma:
el botón sale con un texto largo/cortado en vez de algo corto tipo "Responder").
**Workaround confirmado por el equipo:** redactar el mensaje que acompaña al WA Flow de
forma que sus primeros ~20 caracteres sean exactamente el texto deseado para el botón —
ej. si el mensaje empieza con *"Completa tus datos para continuar con tu proceso."*, el
botón queda "Completa tus datos...". Reportado como bug/mejora a producto, pero mientras
tanto usar el workaround en vez de esperar el fix.

---

## 4. CODE TOOLS DE NORMALIZACIÓN

### Patrón general
Cuando el flow anterior usaba Formatters para normalizar campos, reemplazarlos con Code Tools en Cortex. Cada tool:
1. Recibe el valor raw del campo como `params.campo`
2. Normaliza: `toLowerCase()` + quitar acentos (NFD) + quitar no-alfanuméricos
3. Busca en un mapping objeto
4. Guarda con `await setField("keyword_del_campo", valorNormalizado)`
5. Retorna `{ success, valorNormalizado, message }`

**Importante:** El keyword del campo debe coincidir exactamente con el `{{client.keyword}}` de Atom.

### Tool: normalizar_programa (o producto)
```javascript
async function main(params){
  const mapping = {
    // alias: "Nombre Oficial Completo"
    "emba": "Executive Master in Business Administration (EMBA)",
    // ... resto del mapping
  };

  function normalizeString(str) {
    return str.toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]/g, '');
  }

  const normalized = normalizeString(params.programa);
  const oficial = mapping[normalized];

  if (oficial) {
    await setField("programa_academico", oficial);
    return { success: true, programa_oficial: oficial, message: "Identificado: " + oficial };
  } else {
    await setField("programa_academico", params.programa);
    return { success: false, programa_oficial: params.programa, message: "No encontrado: " + params.programa };
  }
}
```

### Tool: normalizar_tipo (categoría)
Clasifica el valor normalizado en categorías fijas para bifurcación en Flowbuilder.
```javascript
async function main(params){
  const categoriaA = ["Producto A1", "Producto A2"];
  const categoriaB = ["Producto B1", "Producto B2"];

  const input = params.programa || "";

  if (categoriaA.includes(input)) {
    await setField("tipo_programa", "Categoría A");
    return { success: true, tipo: "Categoría A" };
  } else if (categoriaB.includes(input)) {
    await setField("tipo_programa", "Categoría B");
    return { success: true, tipo: "Categoría B" };
  } else {
    await setField("tipo_programa", "Otro");
    return { success: true, tipo: "Otro" };
  }
}
```

### Tool: normalizar_pais
```javascript
async function main(params){
  const mapping = {
    // aliases en español e inglés → ISO code
    "costarica": "CR", "panama": "PA", "colombia": "CO",
    // ... resto del mapping
  };

  let normalized = params.Pais.toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]/g, '');

  const iso = mapping[normalized];

  // Lista de países LATAM — el resto → "Overseas"
  const latam = ["CR","PA","CO","MX","GT","HN","NI","SV","BZ","EC",
                 "PE","BO","PY","UY","AR","CL","VE","BR","CU","DO",
                 "PR","HT","JM","TT","BB","BS","GY","SR"];

  const finalPais = iso && latam.includes(iso) ? iso : "Overseas";

  await setField("pais_de_origen", finalPais);
  return { success: true, pais_iso: finalPais, message: "País: " + finalPais };
}
```

**Notas:**
- El problema más común al cargar code tools en Atom: el editor envuelve el código en `function main(params){}` automáticamente. Pegar solo el contenido interior, sin redeclarar la función.
- Si el editor muestra `// const mapping = ...` (comentado), usar el botón "Generar con IA" para generar el esqueleto correcto y luego reemplazar el mapping.
- Siempre probar con al menos 2 casos en el botón "Probar script" antes de guardar.
- Verificar en "Llamadas SDK" que aparezca `setField(...)` correctamente.
- **Convención recomendada para scripts nuevos:** `async function main(params) {...}` (con `await` en las llamadas asíncronas). El patrón histórico `function main(params){...}` sin `async` sigue viéndose en producción y funciona en el runtime de Atom — no es un error que rompa el script — pero la skill oficial de Atom para Code Tools (`atom-cortex-code-tool-builder`, ver sección 4a) lo marca como patrón a no usar como plantilla para código nuevo. Adoptarlo por consistencia hacia adelante, no por necesidad de arreglar algo roto.

---

## 4a. REGLAS TRANSVERSALES PARA ESCRIBIR CODE TOOLS (de la skill oficial de Atom)

Diego Pereda compartió `atom-cortex-code-tool-builder`, una skill de Claude Code hecha
por el equipo de Atom, enfocada específicamente en escribir/depurar el JavaScript de una
Code Tool (no en el proceso de implementación completo — para eso sigue sirviendo esta
skill). Si la tarea es diseñar o corregir el código de una Code Tool puntual, especialmente
una que integra con una API externa (CRM, ERP, HubSpot, Salesforce, etc.), usar esa skill
directamente para el detalle línea por línea. Acá quedan solo las reglas transversales que
todo implementador de Cortex debería conocer aunque no abra esa skill:

- **`setField()` y `return` son cosas distintas.** `setField()` persiste el valor en un
  campo de Cortex; `return` solo devuelve el resultado de la ejecución del script. Si un
  requisito dice "guardar en un campo", no alcanza con incluir el valor en el `return`.
- **Nunca inventar información técnica crítica** (endpoints, tokens, IDs, pipeline/stage
  IDs, nombres de properties, estructuras de respuesta, reglas de negocio). Si falta un
  dato indispensable, usar un placeholder claramente identificado (ej. `"TU_TOKEN_AQUI"`)
  y pedir solo ese dato puntual — no reconstruir la integración a partir de suposiciones.
- **No reutilizar IDs, endpoints ni reglas de negocio de un cliente para otro** solo
  porque funcionaron ahí — cada integración (HubSpot, Salesforce, Syonet, un CRM propio)
  tiene su propio pipeline, stage, properties y reglas de prioridad.
- **Separar éxito HTTP de éxito funcional.** Un HTTP 200 no garantiza que la operación de
  negocio haya funcionado — la API puede responder 200 con `{ "success": false }` o un
  indicador propio. Validar ambos niveles cuando el contrato de la API lo permita.
- **No usar `results[0]` arbitrariamente** cuando una búsqueda puede devolver varios
  registros y existen reglas de negocio para elegir uno (pipeline, prioridad, fecha,
  estado) — definir el criterio de selección explícitamente.
- **No retornar el objeto completo de la respuesta ni del error** (`return response` /
  `return error`) — devolver solo los campos necesarios y serializables.
- **Evaluar idempotencia solo si existe un riesgo real de duplicados** (leads, citas,
  pedidos) y solo si hay un identificador o estado real que permita reconocer una
  ejecución previa — no inventar la estrategia.
- **Al recopilar los detalles de una integración con un usuario no técnico**, no pedir de
  entrada todos los datos técnicos juntos (URL, endpoints, auth, schemas). Primero
  identificar el sistema/plataforma; si es una plataforma conocida (HubSpot, Salesforce,
  Google), resolver lo estándar por documentación pública y preguntar solo lo específico
  de esa cuenta (ej. el nombre interno de una property); si es una API propia o
  desconocida, pedir un CURL, una request de Postman o documentación real antes de
  construir.

---

## 4b. HTTP REQUEST vs CODE TOOL — ambos pueden llamar servicios externos, no son la misma herramienta

**Corregido 2026-08-13:** esta sección antes decía, citando una doc interna de Notion,
que "Code Tool no sale a la red" y que llamar una API externa solo era posible desde HTTP
Request. Eso quedó contradicho por `atom-cortex-code-tool-builder` (la skill oficial de
Atom para Code Tools, ver 4a) y por 3 integraciones reales de producción que documenta
(Saludsa/HubSpot, Autoshow/Syonet, Turbi/HubSpot) — todas Code Tools que sí llaman APIs
externas. Confirmado con Emily: usar esta versión, no la de Notion.

**Code Tool con llamadas HTTP:** dentro del script de una Code Tool, las llamadas a
servicios externos se hacen con una función `http()` disponible en el runtime:
```javascript
const response = await http({
  url: "https://api.example.com/resource",
  method: "POST",
  headers: { "Authorization": "Bearer TU_TOKEN_AQUI", "Content-Type": "application/json" },
  data: { value: params.value }
});
```
No están disponibles `fetch`, `axios`, `require()` ni `XMLHttpRequest` — usar siempre
`http()`. Esto habilita, dentro de un solo script, patrones que antes se pensaban
imposibles sin HTTP Request: encadenar varias llamadas (A devuelve datos que B necesita),
buscar/crear/actualizar, múltiples sistemas en secuencia, compensación si un paso
posterior falla, todo sin tener que crear un campo-puente por cada valor transitorio
(ver plantillas en `atom-cortex-code-tool-builder/references/02_...PLANTILLAS.md`).

**Entonces, ¿cuándo usar HTTP Request (el componente de UI) en vez de una Code Tool?**
HTTP Request sigue siendo la opción más simple para **una sola llamada declarativa**,
configurada sin código (Canvas → Nodo Cortex → Herramientas → HTTP Request), donde las
"variables" son campos de guardado del nodo/cuenta que se insertan escribiendo `/` en
URL/headers/body. Para lógica más compleja en un solo paso (buscar-y-decidir,
encadenar llamadas, idempotencia, orquestar más de un sistema), una Code Tool evita tener
que crear un campo real por cada valor transitorio entre llamadas — que sigue siendo
necesario si se resuelve todo con HTTP Request nodos separados.

**Manejo de errores en HTTP Request (el componente de UI):** hay un toggle de "Manejo de
códigos de respuesta" (por defecto 200,201,204 como éxito) y un toggle de timeout —
activar ambos para integraciones reales. Ninguno distingue "la API respondió 200 pero con
datos vacíos" (ej. una placa/cliente no registrado — caso de negocio válido, no un error)
de una falla real — esa distinción hay que resolverla en el prompt o en el código de la
Code Tool, no en la configuración de la herramienta.

**Guardar la respuesta funciona igual en ambas herramientas:** "Probar API/script desde
aquí" ejecuta con valores de ejemplo, y desde el JSON de respuesta se mapea cada
propiedad a un campo — clic sobre el valor abre el formulario de mapeo, con opción de
crear el campo ahí mismo sin salir del editor. El mapeo no es automático: hay que
declarar explícitamente cada valor a guardar.

---

## 4c. LIMITACIONES DE PLATAFORMA CONOCIDAS (confirmar antes de prometer al cliente)

Estas son limitaciones confirmadas por el equipo de producto de Atom (canal
`#cortex-implementación`), no suposiciones — pero pueden cambiar de sprint a sprint, así
que conviene reconfirmar el estado si el caso de uso depende fuerte de alguna:

- **Calendario — un solo mailbox.** La integración de calendario de Cortex hoy solo
  soporta un mailbox del lado del cliente. Si el caso de uso necesita agenda por persona
  (ej. cada vendedor/asesor con su propio Outlook, para que el bot agende directamente en
  el calendario del asesor que le corresponde), esto **no está soportado todavía**.
  Cuándo importa: cualquier flow donde el paso final es "agendar cita con la persona X" y
  hay más de una persona con calendario propio (equipo de ventas, asesores, médicos,
  etc.), no solo agenda única compartida. Detectarlo en el análisis previo (paso 1) si el
  flow viejo ya asignaba dinámicamente un asesor antes de agendar.
- **Ubicación/GPS no reconocida nativamente** (confirmado 2026-08-12: "no reconoce").
  Si el caso de uso quiere sugerir la sede más cercana a partir de la ubicación que
  comparte el usuario por WhatsApp, no funciona todavía en Cortex — en ese momento el
  equipo de producto indicó que entraba en el próximo sprint, así que reconfirmar el
  estado actual antes de diseñar el flujo asumiendo que ya funciona.
- **"Solicitud de información de contacto" de WhatsApp (contact request) no soportada.**
  Confirmado por producto: "todavía no soportamos ese tipo de msj para solicitud de
  contacto". Workaround: ponerlo como paso de Flowbuilder **antes** de entrar al nodo
  Cortex, no dentro del nodo.
- **Bases de conocimiento — reportado que ya no se soporta PDF** (reporte de un
  implementador, sin confirmación de producto en el hilo). A diferencia de los tres
  puntos de arriba, esto contradice lo que dice la sección 5 más abajo (que sí lista PDF
  como formato válido para Documento Estático) — **verificar subiendo un PDF de prueba
  antes de asumir cualquiera de las dos versiones**, no confiar en ninguna de las dos
  fuentes a ciegas hasta reconfirmar en el editor real.

---

## 5. BASES DE CONOCIMIENTO

### Búsqueda en catálogo con múltiples coincidencias
Si una consulta contra la tabla dinámica puede matchear más de un ítem (ej. un modelo con
varias versiones/trims), el prompt debe instruir mostrar **todas** las coincidencias, no
solo la primera — idealmente con el atributo que las distingue (ej. rango de precio: "3
versiones, desde $114,000 a $134,990"). Mostrar solo el primer resultado silenciosamente
descarta opciones válidas y genera fricción cuando el cliente preguntaba por otra versión.

### Tabla Dinámica (catálogo de productos/servicios)
Usar cuando hay múltiples ítems con atributos similares (programas, productos, servicios).
- Formato: Excel (.xlsx) con una fila por ítem
- Columnas clave: nombre completo, aliases/siglas, tipo/categoría, modalidad, características, URL
- **Los aliases son críticos**: incluir cómo los usuarios realmente escriben el producto, no solo el nombre oficial
- Frecuencia de actualización: Mensual (para catálogos que no cambian seguido)

### Documento Estático (FAQs, políticas, info institucional)
Usar para información que no cambia frecuentemente: preguntas frecuentes, políticas, descripciones institucionales.
- Formato: .docx o .pdf
- Organizar por categorías con encabezados claros
- Formato Q&A: `P: [pregunta]\nR: [respuesta]`

### Regla de oro
Si el dato puede cambiar (precios, fechas, disponibilidad), NO cargarlo en KB. En el prompt indicar: *"Para [dato], derivar al asesor."*

---

## 6. CONEXIONES EN FLOWBUILDER

### El agente Cortex es un componente dentro de un flow de Flowbuilder, no algo aparte
El número de WhatsApp se sigue conectando normalmente a un flow de Flowbuilder — no hay
una conexión directa "número → Cortex". El orden es: crear el agente en Cortex primero,
después armar (o editar) el flow en Flowbuilder agregando el componente del agente, y ese
flow es el que queda conectado al número.

### Reglas de conexión del nodo Agente (confirmadas, reportadas como bug de plataforma)
- **Agente → Condicional inmediatamente después: el condicional puede enrutar mal** (por
  defecto cae en la rama "Otro" aunque el campo que compara sí tenga el valor correcto —
  visto con campos de tipo país y de tipo sede en dos clientes distintos, UMICET y Quick
  Learning, confirmado por el equipo de producto como el mismo bug en ambos casos).
  **Workaround confirmado:** insertar un componente de **Mensaje** entre el nodo Agente y
  el Condicional — esto hace que el enrutamiento funcione correctamente. Si un
  condicional after-Cortex enruta siempre a la rama por defecto pese a que el campo tiene
  el valor esperado, este es el primer workaround a probar antes de asumir que el prompt
  o la normalización están mal.
- **Agente → Evaluador de Respuesta no se puede conectar directamente** (mismo
  comportamiento que Smarton → Evaluador, tampoco permitido). El sentido válido es el
  inverso: **Evaluador de Respuesta → Agente** sí funciona. Si se necesita lógica de
  evaluación después del agente, resolverlo con un Condicional, no intentando conectar el
  agente directo a un Evaluador.

### Checklist completo post-Cortex
**NO saltarse ningún componente del flow anterior.** Inventariar todo antes de armar el nuevo flow.

Componentes típicos que van después del nodo Cortex:

**Path "Calificado / Asignar":**
- [ ] Tag de categoría (ej: "MA Ejecutivas", "Open Programs")
- [ ] Tag "Datos completos" o equivalente
- [ ] Etapa SQL
- [ ] **Conversion API** (evento tipo InitiateCheckout o Lead)
- [ ] HTTP request (si hay routing dinámico de asesores)
- [ ] Condicional por tipo/categoría → diferentes grupos de asignación
- [ ] **SaveField de integraciones** (Salesforce ID, HubSpot ID, etc.)
- [ ] Asignación (dinámica o específica)

**Path "Solo información / Cierre":**
- [ ] Tag "Exploración" o equivalente
- [ ] Tipificación
- [ ] Mensaje de cierre
- [ ] Fin de flujo

**Path "No califica":**
- [ ] Tipificación
- [ ] Mensaje con alternativa (ej: producto más accesible)
- [ ] Tag "ABANDONO" si corresponde
- [ ] Fin de flujo

### HTTP de asignación dinámica
Si el flow anterior usaba HTTP para hacer match asesor/producto+país:
- El body del HTTP debe usar `{{client.campo}}` en lugar de `{{flow_field.campo}}`
- Los valores en `lista_elementos` deben coincidir exactamente con lo que guardan las code tools
- Si la tool guarda ISO de país, el HTTP debe tener ISO. Si guarda nombre, el HTTP debe tener nombre.
- Actualizar el body del HTTP sin cambiar el endpoint ni la lógica de n8n.

---

## 7. TESTING

### Casos a probar siempre

| Caso | Input de prueba | Lo que validar |
|---|---|---|
| Happy path ejecutivo | Nombre de maestría/producto premium → años de exp → datos | Tipificación correcta, asesor asignado correcto |
| Happy path residencial | Producto para perfiles junior | No pide cargo/empresa si no aplica |
| Programa que antes fallaba | Producto que daba error en el flow viejo | Bot responde con info correcta |
| Producto nuevo (no en KB) | Producto recientemente lanzado | No alucina, deriva a asesor |
| País fuera de región | País que va a "Overseas" | Asignación al grupo correcto |
| Email inválido | "emily at gmail com" | Pide corrección antes de guardar |
| Solo info | Consulta → sin dar datos | Tipificación "Solo información" |
| No califica | Perfil que no cumple requisitos | Ofrece alternativa, cierra amablemente |

### Antes de dar por funcional una integración: probar dentro de una conversación completa, no solo aislada
Un HTTP Request de Cortex puede probarse exitosamente en modo aislado ("Probar API"
dentro de Configuraciones avanzadas) y aun así fallar cuando se invoca en medio de una
conversación simulada real — visto en producción (cliente Yen Car, push a CRM), sin causa
raíz confirmada por el equipo al momento del reporte. No dar por cerrada una integración
solo porque la prueba aislada del HTTP pasó — correr también la conversación completa en
el simulador antes de marcarla como lista.

### El simulador del nodo Cortex y el simulador/número real de Flowbuilder no siempre coinciden
Reportado y confirmado como comportamiento no intencional por el equipo de producto
("debería verse igualmente"): formatos como listas de opciones o botones pueden verse
bien en el simulador propio del editor de Cortex y no reflejarse igual al probar desde
Flowbuilder o desde un número conectado. No confiar solo en el simulador aislado de
Cortex para dar por buena una funcionalidad — probar también con un número de WhatsApp
conectado (aunque sea uno de prueba de otra cuenta, duplicando la plantilla) antes de
confirmar al cliente.

### Publicar y guardar
- **Guardar seguido, no acumular muchos cambios antes de guardar** — un error de "no me
  deja guardar" visto por varios implementadores se resolvió guardando cada pocos
  cambios en lugar de esperar a tener muchos acumulados.
- **Una vez publicado un flujo, hay que volver a Publicar (no alcanza con Guardar) cada
  vez que se hacen cambios** para que el simulador y las evaluaciones reflejen la versión
  nueva — confirmado por producto: "una vez publicado no se puede dar a guardar" en el
  sentido de dejar cambios pendientes sin publicar y esperar que se vean.
- **Si falla la publicación con un error poco claro, volver a intentar publicar con el
  inspector del navegador (F12) abierto** — ahí se ve el motivo real. Las dos causas más
  comunes confirmadas: pasarse del límite de 10,000 caracteres del prompt (ver sección
  3), o tener un campo de información agregado en el nodo pero no seleccionado/mapeado.
- **Error de "similitud" al publicar:** ocurre cuando dos condicionales (o condiciones de
  finalización) tienen redacciones demasiado parecidas entre sí. Fix confirmado:
  reformular el texto de una de las dos para diferenciarlas más, no cambiar la lógica.

### Bugs frecuentes y fixes

| Síntoma | Causa | Fix |
|---|---|---|
| HTTP se ejecuta múltiples veces | Ramas convergentes al mismo nodo HTTP | Duplicar el nodo HTTP por cada rama |
| Tipo de producto clasificado mal | Nombre en code tool no coincide exactamente con lo que guarda normalizar_programa | Verificar strings exactos en los arrays de normalizar_tipo |
| Mensaje duplicado (texto + componente) | Agente genera texto Y lista/botón en el mismo turno | Agregar instrucción en descripción de ejecución del formato |
| `mapping is not defined` en code tool | El editor comentó el `const mapping` con `//` | Usar "Generar con IA" para regenerar el esqueleto |
| Bot pide datos que el usuario ya dio | Campos capturados globalmente pero no validados en el nodo | Agregar instrucción de verificación previa al prompt |
| Cargo/empresa pedidos innecesariamente | Campos obligatorios no diferenciados por tipo de producto | Separar instrucción por categoría en el prompt |
| Bot guarda un dato de producto (modelo, marca, año) como first_name/last_name | Campos de sistema con reconocimiento automático global, dispara ante cualquier respuesta con forma de nombre | Regla explícita en el prompt (ver sección 2, Campos a Identificar y Guardar) — si persiste, es bug de plataforma, no de prompt |
| Bot pide zona/sede en una línea que no la necesita | El prompt generalizó la lógica de una línea con múltiples sedes (ej. Llantas) a otra que tiene una sola cola de asignación | Aclarar explícitamente en el prompt cuáles líneas SÍ necesitan sede y cuáles no, en vez de una regla genérica |
| Tipificación de un flujo (ej. "Inicio de Cita") aparece en un cierre de otro flujo (ej. derivación a Ventas) | Las Condiciones de Finalización no están suficientemente acotadas a la rama que las dispara | En cada condición de finalización, aclarar explícitamente a qué rama/sub-flujo aplica exclusivamente |
| Condicional después del Agente enruta siempre a la rama por defecto | Bug de plataforma confirmado (ver sección 6) | Insertar un componente de Mensaje entre el Agente y el Condicional |
| WA Flow: el botón sale con texto largo/cortado en vez del texto corto deseado | Cortex toma los primeros ~20 caracteres del mensaje que acompaña el formulario como texto del botón | Redactar el mensaje para que sus primeros ~20 caracteres sean el texto deseado del botón |
| Campos guardados por el Agente no persisten al pasar a Flowbuilder | Bug abierto, sin causa raíz confirmada al momento del reporte (cliente Dycar) | Reportar como bug a producto; no asumir que es un error del prompt propio hasta descartar esto |
| Cortex envía un mensaje interactivo (botones) aunque esté desactivado y sin referencia en el prompt | Bug abierto, sin causa raíz confirmada al momento del reporte (cliente Dycar) | Reportar como bug a producto; revisar igual el prompt de config global por si acaso, pero no asumir que ahí está la causa |

---

## 8. REFERENCIAS

Para implementaciones con casos similares al de INCAE:
- Flow con catálogo de programas educativos: ver `references/incae-case.md`
- Mapping completo de países LATAM (ISO + aliases en español): disponible en la code tool `normalizar_pais`
- Template de prompt para institución educativa: ver sección 3 de este skill

---

> **Nota para el PM/CSM:** Este skill captura el proceso completo de implementación de Cortex. Para cada cliente nuevo, el paso 1 (análisis previo del JSON) es el más crítico — define todo lo que no se puede saltear en los pasos siguientes.
