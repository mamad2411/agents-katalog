---
name: explainer
description: Crea explainers animados. Son videos explicativos hechos en HTML que se reproducen solos, con guion, una escena animada por bloque, subtítulos sincronizados, modo grabación y exportación a MP4. Sirve para vertical 9:16 (TikTok, Reels, Shorts), horizontal 16:9 (YouTube, clases, presentaciones), cuadrado 1:1 y 4:5. Antes de construir pregunta formato, voz, estilo visual, duración y tono, y guarda las respuestas como perfil. Usar SIEMPRE que el usuario pida "un explainer", "un video explicativo", "animated explainer", "explicame esto con una animación", "animá esta historia", "un reel animado", "un video animado para YouTube", o quiera convertir una noticia, un concepto, una clase, un producto o un dato en una animación para narrar, aunque no diga "explainer". No usar para gráficos estáticos, diapositivas ni edición de video filmado.
---

# Explainer animado

Este skill produce una página HTML autocontenida. La página se reproduce sola, escena por escena. Cada escena acompaña un bloque del guion. Quien narra graba su voz encima o graba la pantalla en modo grabación. El mismo HTML exporta un MP4 cuadro por cuadro.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `assets/plantilla.html` | Motor completo con un ejemplo de 4 escenas. Es la base de cada explainer nuevo. |
| `assets/ejemplos/planeta-vertical.html` | Explainer terminado de 70 s. Calibra densidad y calidad. Usa un motor anterior: no lo copies como base. |
| `references/formatos.md` | Zonas del cuadro, cámara y composición de cada formato. |
| `references/estilos.md` | Paletas, tipografías, reglas de trazo y tono del guion. |
| `references/escenas.md` | Patrones visuales que funcionan, errores frecuentes e íconos del motor. |
| `references/movimiento.md` | Números de movimiento y laboratorio de fotos. |
| `references/audio.md` | Sincronía con una voz ya grabada. |
| `scripts/simular.cjs` | Prueba la reproducción completa con Node, sin navegador. |
| `scripts/render.mjs` | Fotos, hoja de contacto y MP4. Necesita Playwright y ffmpeg. |
| `scripts/palabras.mjs` | Convierte una transcripción de Whisper en tiempos por palabra. |

En los comandos, `SKILL_DIR` es la carpeta de este archivo.

## Paso 0: entender el estilo

El mismo motor sirve para estilos muy distintos. Preguntá antes de investigar o escribir.

### Perfil guardado

1. Buscá `perfil.md` en `SKILL_DIR`.
2. Si existe, resumilo en una línea. Por ejemplo: "Vertical, Noche, la narrás vos, 60–90 s, karaoke".
3. Preguntá "¿Uso este perfil?". Si la respuesta es sí, salteá las preguntas.

### Preguntas

- Hacé todas las preguntas en una sola tanda.
- No preguntes lo que el pedido ya responde.
- Si tenés una herramienta de preguntas con opciones, como AskUserQuestion, usala. Admite 4 preguntas por llamada: usá dos llamadas.
- Sin esa herramienta, escribí un solo mensaje con preguntas numeradas, opciones y un default marcado. Aclará: "Respondé solo lo que quieras cambiar".

**Ronda 1:**

| # | Pregunta | Opciones |
|---|---|---|
| 1 | Formato | Vertical 9:16 (TikTok, Reels, Shorts) · Horizontal 16:9 (YouTube, clase, presentación) · Cuadrado 1:1 · Feed 4:5 |
| 2 | Voz | La grabo yo después · Ya tengo el audio grabado · Sin voz: el texto va en pantalla |
| 3 | Estilo visual | Noche · Papel · Pizarra · Plano color · Plano técnico · Tu marca: colores y tipografía propios |
| 4 | Duración | 30–45 s · 60–90 s · 2–3 min |

Describí cada estilo en una línea con los datos de `references/estilos.md`. Si la herramienta admite 4 opciones, nombrá Plano técnico y Tu marca en el texto de la pregunta: el usuario las elige con "Otro".

**Ronda 2, solo lo que falte:**

| # | Pregunta | Opciones |
|---|---|---|
| 5 | Tono del guion | Cercano y con humor · Claro y neutro · Formal · Imitá un texto mío |
| 6 | Subtítulos | Karaoke: resalta la palabra dicha · Simples · Sin subtítulos |
| 7 | Guion | Lo escribís vos · Uso el mío |
| 8 | Idioma y trato | Deducilo del pedido. Preguntá solo si no está claro: vos, tú, usted, inglés. |

Si elige "Imitá un texto mío", pedí que pegue un texto suyo. Si el usuario tiene un skill propio de escritura en su voz, usalo para el guion.

**Defaults** si responde "elegí vos": vertical 9:16, la grabo yo, Noche, 60–90 s, claro y neutro, karaoke, idioma del pedido.

### Guardar el perfil

Escribí `SKILL_DIR/perfil.md` con las respuestas:

```
formato: 9:16
voz: la grabo yo
estilo: Noche
duracion: 60–90 s
tono: cercano y con humor
subtitulos: karaoke
idioma: español rioplatense, voseo
referencia_de_voz: (texto pegado o nombre de un skill de escritura, opcional)
```

Si la carpeta es de solo lectura, mostrá el perfil en un bloque. Así el usuario lo pega la próxima vez.

## Qué cambia según la voz

| Voz | Guion | Subtítulos | Reloj |
|---|---|---|---|
| La grabo yo | Escrito para decirlo en voz alta | Karaoke o simples, con tiempo estimado | Estimado. Al grabar, resincronizá con `references/audio.md`. |
| Ya tengo el audio | La transcripción del audio | Exactos, palabra por palabra | El audio. |
| Sin voz | Frases cortas para leer | `simples`: son el texto del video | Estimado con `ritmo: 1.3`. |

## La regla central: la pantalla acompaña la voz

La gente escucha la voz. La pantalla no repite lo que dice la voz.

- No pongas títulos, rótulos, leyendas, chips de estado ni listas.
- Convertí cada concepto en un ícono o en una acción animada.
- Dejá solo el texto que funciona como ícono: años en una línea de tiempo, una fecha en un calendario, un nombre de archivo en una ventana.
- Usá como máximo 4 palabras en pantalla por escena, sin contar los subtítulos.
- Los subtítulos son el único texto real.

Por qué: un título compite con la voz. Nadie lee y escucha a la vez.

En un video sin voz, los subtítulos simples cumplen el papel de la voz. La regla sigue igual: el dibujo no repite el texto.

### Excepción: un prompt o un texto para copiar

Cuando la voz dicta un texto que el público va a copiar, ese texto va en pantalla.

- Escribilo dentro de una barra, palabra por palabra, cuando la voz lo dice. `F.words` trae cada palabra con su segundo.
- Pintá la palabra dicha con el color de acento.
- Ocultá los subtítulos de esa escena con `noSubs: true`.
- Debajo del texto, animá lo que hace cada instrucción.

## Cuadro completo

El dibujo toca los cuatro bordes del cuadro. Nunca lo encierres en una franja o en una caja con el resto vacío.

- El lado corto del cuadro mide 100 unidades de mundo. El origen es el punto de la cámara.
- `F.area` es la zona de acción. Ahí van el héroe y el evento de la palabra clave.
- Seguí dibujando detrás de los subtítulos hasta el borde: el suelo, el cuerpo, la continuación del objeto.
- Detrás de los subtítulos usá tonos oscuros. Si el dibujo es claro o cargado, llamá a `scrim()`.
- En vertical, apilá el sujeto de arriba abajo. En horizontal, repartilo de izquierda a derecha.

Las zonas exactas y la composición de cada formato están en `references/formatos.md`.

## El gancho: los primeros segundos

El gancho es lo más importante. Los primeros 10 segundos llevan el movimiento más fuerte.

- Hacé del cuadro 0 una composición terminada y llamativa. Es la miniatura.
- Usá movimientos de cámara grandes: un plano cerrado que se aleja, un foco, una implosión, una construcción en vivo.
- Cambiá de plano en cada palabra fuerte de la voz.
- Evitá íconos chicos quietos y diagramas de lado a lado en el gancho.
- Revisá el gancho con `--fotos gancho` antes que el resto.

### Prueba de cada escena

Antes de construir, pasá cada escena por dos preguntas:

1. ¿Se entiende mirando la animación y leyendo solo los subtítulos?
2. ¿Hay texto en pantalla que repite la voz?

Una escena que es una lista, un número grande, una cuenta regresiva o una leyenda falla la prueba. Rediseñala como una acción. `references/escenas.md` tiene los patrones.

## Flujo en dos pasos

Reconstruir una animación cuesta mucho más que corregir un texto. Por eso se aprueba primero el plan.

### Paso 1: investigación, guion y storyboard

1. **Investigá.** Buscá fuentes primarias. Verificá cada cifra. Distinguí lo confirmado de lo reportado. Guardá los links para el panel de fuentes. Sin búsqueda web, trabajá con el material del usuario y marcá cada dato dudoso con `[VERIFICAR]`.
2. **Escribí el guion** con el tono del perfil. Si el usuario trajo su guion, respetalo y solo partilo en bloques.
   - Primera frase: un gancho. Un dato con fecha, una paradoja, una pregunta que pica o una confesión.
   - Una idea por bloque. Cada bloque tiene de 1 a 3 frases.
   - Números concretos en lugar de "mucho" o "poco".
   - Una analogía física por cada concepto abstracto. Esa analogía se dibuja literal.
   - Un cierre que no resume: una imagen, un giro o una frase que vuele sola.
   - Evitá las fórmulas gastadas, como "no es X, es Y".
   - Escribilo para decirlo en voz alta. Leelo en voz baja antes de entregarlo.
3. **Calculá el largo.** La voz rinde unas 2,5 palabras por segundo.

   | Duración | Bloques | Palabras |
   |---|---|---|
   | 30–45 s | 5–6 | 80–110 |
   | 60–90 s | 7–9 | 160–220 |
   | 2–3 min | 12–18 | 300–450 |

   Para más de 3 minutos, proponé partirlo en capítulos de un explainer cada uno.
4. **Armá el storyboard.** Escribí una línea por escena con la acción visual. Cada línea responde cinco preguntas:
   - **Héroe:** ¿cuál es el único movimiento principal?
   - **Palabra clave:** ¿con qué palabra de la voz coincide?
   - **Escala:** ¿qué magnitud se compara con otra?
   - **Continuidad:** ¿qué elemento viene de la escena anterior y cómo se transforma?
   - **Imagen final:** ¿qué cuadro queda quieto y legible al terminar?
5. **Presentá guion y storyboard en el chat.** Esperá el OK. Si el usuario dice "hacelo directo", salteá la espera.

### Paso 2: construcción

1. Copiá `assets/plantilla.html` a la carpeta de trabajo con un nombre nuevo.
2. Completá `CONFIG`: `formato`, `subtitulos` y `ritmo`, según el perfil.
3. Aplicá el estilo: tokens de `:root`, link de fuentes y reglas de trazo de `references/estilos.md`.
4. Reemplazá el contenido. La sección "Qué tocar del motor" dice qué cambia.
5. Sincronizá cada evento clave con `F.at('palabra')`. Seguí la sección "Sincronía".
6. Aplicá los números de `references/movimiento.md`. Un héroe por plano. Los secundarios arrancan 150 ms después.
7. Simulá la reproducción:
   ```bash
   node SKILL_DIR/scripts/simular.cjs explainer.html
   ```
   El resultado tiene que ser `OK` sin avisos. Un aviso de `at()` indica una palabra que no está en la escena.
8. Corré el laboratorio de fotos, si hay Playwright:
   ```bash
   node SKILL_DIR/scripts/render.mjs explainer.html --fotos gancho
   node SKILL_DIR/scripts/render.mjs explainer.html --fotos finales
   ```
   - La primera vez, instalá las dependencias: `cd SKILL_DIR/scripts && npm install && npx playwright install chromium`.
   - Abrí `out/hoja.png` con Read. Describí cada cuadro como un espectador.
   - Comparalo con el storyboard. Pasá la lista de `references/formatos.md`.
   - Corregí con notas que nombran escena y segundo. Repetí hasta que cada escena pase.
   - Sin Playwright, salteá este paso y pedile al usuario que revise el resultado.
9. Entregá con la sección "Entrega".

## Qué tocar del motor

La plantilla está dividida en secciones numeradas.

**Conservá:** 3 Formatos, 4 Tokens y utilidades, 5 Lienzo y cámara, 6 Ayudantes, 7 Íconos, 10 a 12 Motor y contrato de render. También el CSS del cuadro, los subtítulos, el panel, el modo grabación y el interruptor de subtítulos.

**Reemplazá:**

- Sección 1 `CONFIG`: los valores del perfil.
- Sección 2: `SCRIPT` con un bloque por escena y `SAY` con la forma hablada de números y siglas. Por ejemplo, `'2018': 'dos mil dieciocho'`.
- Sección 8: los dibujos del tema. Borrá los del cielo.
- Sección 9 `SCENES`: un objeto por escena.
- El panel: `<title>`, título, "Qué es ilustración" y "Fuentes". Las aclaraciones de honestidad van ahí, nunca en el cuadro.
- Los tokens de `:root` y el link de fuentes, según el estilo.
- Los textos de la interfaz, al idioma del usuario.

### Una escena

```js
{
  alt: 'Descripción para lectores de pantalla.',
  cam: F => [[0, 0, 0, 1], [F.at('estadio'), 0, -20, 2.5]], // opcional: [t, x, y, zoom]
  noSubs: false,                                           // opcional
  draw(t, F) { /* dibujá en unidades de mundo */ }
}
```

`draw` recibe `t`, los segundos desde el inicio de la escena, y `F`:

| Campo | Qué es |
|---|---|
| `F.area` | Zona de acción: `x0`, `x1`, `y0`, `y1`, `cx`, `cy`, `w`, `h` y `s`, el lado menor. |
| `F.left`, `F.right`, `F.top`, `F.bottom` | Bordes del cuadro con zoom 1. |
| `F.subsTop`, `F.subsBottom` | Zona de subtítulos. |
| `F.vertical`, `F.horizontal`, `F.formato` | Formato actual, para componer distinto. |
| `F.at('palabra', n)` | Segundo en que la voz dice la n-ésima aparición de esa palabra. |
| `F.words` | Cada palabra de la escena con su inicio `s` y su fin `e`. |
| `F.g` | Tiempo global, para el movimiento ambiente. |
| `F.dur` | Duración de la escena. |

Medí todo con `F.area`. Así la escena se adapta a cualquier formato. La plantilla muestra el patrón con `axis(F)` y `viewer(F)`.

Ayudantes de dibujo: `bleed(color o [arriba, abajo], a)` pinta toda la pantalla. `fixed(fn)` dibuja sin cámara. `scrim(a)` oscurece la zona de subtítulos. `txt`, `line`, `rrect` y `dot` dibujan en unidades de mundo.

## Sincronía

- Anclá cada evento clave a una palabra con `F.at('palabra')`. No escribas segundos fijos para esos eventos.
- `F.at` funciona con tiempos estimados y con audio real. Al cambiar el audio, todo se mueve solo.
- Para un movimiento, sumá duraciones cortas a ese ancla. Por ejemplo, `seg(t, F.at('lamparita'), F.at('lamparita') + .4)`.
- La duración estimada de cada palabra es 0,1 s + 0,038 s por letra. Cada coma suma 0,17 s y cada punto 0,38 s.
- Dejá la última imagen de cada escena quieta y legible. Con `prefers-reduced-motion`, el motor muestra solo ese estado.
- Dentro de `draw`, nunca uses `Date.now`, `performance.now` ni `Math.random` sin semilla. Usá `rng(semilla)`. Así cada cuadro sale igual en la página, en las fotos y en el MP4.

Con una voz ya grabada, seguí `references/audio.md`.

## Entrega

1. **Publicá o abrí el HTML.**
   - Si tenés la herramienta `Artifact`, publicalo con `icon: "video"`. Antes, seguí lo que pida la herramienta. Avisá que el artifact es privado hasta que el usuario lo comparta.
   - En claude.ai, entregalo como artifact HTML.
   - Si no, guardalo y abrilo en el navegador: `open explainer.html` en macOS, `start explainer.html` en Windows, `xdg-open explainer.html` en Linux.
2. **Pegá el guion limpio en el chat**, un bloque por escena, listo para grabar.
3. **Explicá cómo grabar.** Modo grabación oculta los controles y arranca de cero. La tecla S oculta los subtítulos. La tecla H sale del modo.
4. **Exportá el MP4** si hay Node, Playwright y ffmpeg. Corré los dos renders en segundo plano:
   ```bash
   node SKILL_DIR/scripts/render.mjs explainer.html --fps 30
   node SKILL_DIR/scripts/render.mjs explainer.html --fps 30 --query bare=1 --nombre explainer-sin-subtitulos
   ```
   El lado corto sale en 1080 px. La versión sin subtítulos sirve para editar sobre la voz real. Para sumar la voz al MP4, seguí `references/audio.md`.
5. **Ofrecé dos cosas en una línea:** resincronizar con la voz grabada y armar otra versión en otro formato. Para previsualizar otro formato, agregá `?formato=16:9` a la URL. Después recomponé cada escena para ese formato.

## Idioma

- El guion y los subtítulos van en el idioma y el tono del perfil.
- Las respuestas en el chat van en el idioma del usuario.
- Traducí los textos del panel y de los botones al idioma del usuario.
