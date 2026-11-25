---
name: video-lanzamiento
description: Manual de video de lanzamiento del equipo de Marketing, la pieza mas critica del plugin - lenguaje cinematografico concreto para mostrar software REAL como un keynote de Apple, un reveal de Ferrari, Bugatti o Pagani o un comercial de perfume - estructura del keynote (apertura emocional, problema, un capitulo por parte del desglose, prueba y resultados, cierre y llamado), clips de 6-15 s por parte, teaser y version muda, tipos de plano y movimientos de camara virtual, reveals de producto (luz que recorre, macro de detalle, giro 3D, desarmado parte por parte), transiciones con proposito, curvas de easing y duraciones, tiempos de lectura, montaje al beat, color, tipografia cinetica, sonido con licencia y -14 LUFS, subtitulos, especificaciones de entrega por formato, captura limpia a tamaño real con Playwright y normalizar_video.py, produccion con HyperFrames (blueprints, keyframes, audio, media-use, CLI) y QA cuadro a cuadro con qa_video.py. Cargala antes de guionizar, producir o revisar cualquier video.
---

# Video de lanzamiento — cine para producto real

El video es lo que el CEO ve primero y lo que se reenvia. Si parece un slideshow animado, toda la
propuesta parece barata. Este manual es la vara: lenguaje de los grandes lanzamientos aplicado al
producto REAL de FAAST, con especificaciones y control de calidad de productora.

## 1. Referentes y que tomar de cada uno (el lenguaje, nunca la marca)
| Referente | Tomar | No tomar |
|---|---|---|
| Keynotes / films de producto de Apple | objeto en el vacio, luz que descubre, una idea por plano, cifra a pantalla completa, silencio antes del dato, producto siempre nitido | su musica, sus frases, sus tipografias, su logo |
| Reveals de Ferrari, Bugatti, Pagani | macro del detalle antes del todo, desarmado "exploded view", giro lento del objeto, cifra tecnica como poesia, golpe sonoro en el corte | sonidos de motor grabados, logos, rojo Ferrari como cita |
| Comerciales de perfume (Chanel, Dior) | tres planos y una palabra, ritmo lento y seguro, textura y luz, marca al final | modelos, sensualidad fuera de contexto financiero |
| Titulos de Saul Bass, Buck, ManvsMachine | tipografia protagonista, geometria, transiciones que significan | estilos firmados copiados |
| Demos de Stripe, Linear, Arc | interfaz real explicada en una secuencia, cursor con intencion, camara que sigue la consecuencia | sus UIs |

## 2. Estructura
### Keynote (2-4 min, lo fija el brief)
| Bloque | Duracion | Que pasa | Blueprint HyperFrames tipico |
|---|---|---|---|
| Apertura emocional | 6-12 s | negro → luz → un detalle macro → marca; no explica, intriga | `logo-assemble-lockup`, `titlecard-reveal` |
| Problema | 15-30 s | la tension con una cifra con fuente; el costo de seguir igual | `kinetic-type-beats`, `dataviz-countup` |
| **Capitulo por parte** (×N) | 20-40 s c/u | titulo del capitulo → revelacion → como funciona (pantalla real) → resultado (cifra/antes-despues) | `device-surface-showcase`, `camera-journey`, `cursor-ui-demo`, `zoom-out-workspace-reveal`, `comparison-split` |
| Prueba / resultados | 15-25 s | benchmark, cifras de marca citadas, todas las partes juntas | `grid-card-assemble`, `dataviz-countup`, `constellation-hub` |
| Hoja de ruta | 8-15 s | lo que viene, honesto | `spatial-pan-stations` |
| Cierre y llamado | 6-10 s | frase central + marca + siguiente paso | `logo-assemble-lockup`, `cta-morph-press` |

### Clip por parte (6-15 s) — para usar suelto
`0-2 s` gancho (detalle macro o palabra) → `2-9 s` revelacion de la parte en su pantalla real →
`9-12 s` cifra con nota → `12-15 s` marca + llamado. Se entiende sin sonido. Formatos 16:9, 9:16 y 1:1
reencuadrados. Opcional: **pieza extendida por parte** (30-45 s) = el capitulo como pieza autonoma.

### Teaser (15-30 s)
Solo macros de 3-5 partes, sin explicar, ritmo creciente, cierre de marca con fecha o llamado.

### Version muda
Mismo montaje con subtitulos quemados y texto en pantalla autosuficiente (LinkedIn en autoplay, salas
sin audio).

## 3. Planos y movimientos de camara virtual (software real)
| Plano / movimiento | Descripcion | Uso | Herramienta |
|---|---|---|---|
| Revelacion por luz | la pantalla emerge de negro con una luz que la recorre en diagonal | portada de cada capitulo | transiciones de luz (`css-light`), mascaras |
| Macro / punch-in | zoom lento hasta un detalle real (boton, cifra, estado) a 2-4x | el momento clave | `hyperframes-keyframes` punch-in, capturas 2x |
| Push-in | acercamiento continuo y suave | foco, tension | keyframes camara |
| Pull-out / zoom-out revelador | de un detalle al todo | "esto vive dentro de..." | `zoom-out-workspace-reveal` |
| Orbita / giro 3D | la pantalla en perspectiva gira 8-20° | elegancia, cambio de capitulo | keyframes 3D depth |
| Desarmado ("exploded view") | la interfaz se separa en capas en profundidad (encabezado, tarjetas, tabla, accion) y se vuelve a armar | presentar una parte pieza por pieza | capas de la captura recortadas + 3D depth |
| Recorrido guiado | grabacion real del flujo, con camara que sigue la consecuencia | "como funciona" | `cursor-ui-demo`, `camera-journey` |
| Dispositivo heroe | la pantalla en un marco sobrio flotando con sombra suave | introducir una parte | `device-surface-showcase` |
| Split antes / despues | pantalla dividida o barrido entre proceso viejo y nuevo | resultado | `comparison-split` |
| Cifra a pantalla completa | numero gigante, unidad pequeña, nota | resultado | `dataviz-countup`, `kinetic-type-beats` |
| Paneo por estaciones | camara lateral por varias partes | hoja de ruta, resumen | `spatial-pan-stations` |
| Respiro | 1-2 s de negro o color de marca | entre capitulos | corte / disolucion |

## 4. Transiciones con proposito
- **Corte seco en el beat**: la transicion por defecto. Lo demas se justifica.
- **Disolucion lenta**: paso de tiempo o cambio de tono (problema → solucion).
- **Match cut / whip**: de un elemento a otro con la misma forma o posicion (la cifra del problema se
  convierte en la cifra del resultado).
- **Luz / blur**: revelacion o salida elegante de un capitulo.
- **Push 3D**: avanzar al siguiente capitulo "dentro" del producto.
- Prohibidas: cubo, estrellas, barridos de colores, zoom de PowerPoint, transiciones distintas en cada corte.

## 5. Easing y duraciones
| Movimiento | Duracion | Curva |
|---|---|---|
| Entrada de elemento | 400-800 ms | ease-out suave (p. ej. cubic-bezier(0.16, 1, 0.3, 1)) |
| Salida | 250-500 ms | ease-in |
| Revelacion de producto | 1,2-2,0 s | ease-in-out lento |
| Push-in / orbita | 3-6 s | lineal o ease-in-out muy suave (continuo) |
| Punch-in a detalle | 600-900 ms + sosten ≥ 1,5 s | ease-out |
| Tipografia cinetica | 300-600 ms por palabra/bloque | ease-out, sin rebote |
Sin rebotes ni elasticos en piezas financieras (salvo micro-detalles); springs muy amortiguados.

## 6. Tiempos de lectura
- Minimo por cartela: **0,4 s por palabra + 1 s** (una cartela de 5 palabras: ≥ 3 s en pantalla).
- Cifra con unidad y nota: ≥ 2,5 s.
- Subtitulos: ≤ 42 caracteres por linea, ≤ 2 lineas, ≥ 1,2 s por subtitulo, ~17 caracteres/s maximo.
- Nunca dos textos compitiendo en el mismo plano.

## 7. Montaje al beat y ritmo
- Elegir musica antes de montar; marcar beats (`npx hyperframes beats`) y cortar en el pulso.
- BPM orientativo: 70-90 elegante (keynote), 100-120 energico (clips, teaser).
- Curva de energia: apertura contenida → sube en las partes → pico en la prueba → resuelve en el cierre.
- Silencio de 0,5 s antes de la cifra mas importante.

## 8. Color y luz
- Paleta: neutros profundos (negro carbon, grafito) o blanco infinito + el acento de marca (verde del
  isotipo, ver `marca-faast`).
- Grade/LUT solo sobre el ENTORNO; la interfaz del producto y el logo conservan sus colores exactos.
- Luz de estudio: un key lateral suave, reflejo sutil bajo la pantalla, nada de lens flares baratos.

## 9. Tipografia cinetica
Tipografias de la marca con licencia; titulares de capitulo grandes con tracking levemente negativo;
cifras con numerales tabulares; efectos de texto de `hyperframes-animation` (revelado por mascara,
linea por linea, sustitucion de palabra en el beat); contraste AA siempre; zona segura (5% del borde;
9:16 con 250 px libres arriba y abajo).

## 10. Sonido
- Musica con licencia que cubra el uso (web, sala, redes, pauta) — `media-use` la resuelve con registro
  de procedencia; nada con derechos sin licencia; nada que imite un tema conocido.
- Sound design: un golpe grave en revelaciones, ticks sutiles en cifras, aire/ambiente en macros; nada
  de "whoosh" en cada corte.
- Voz en off (opcional): grabada o TTS con licencia; ducking de la musica (`hyperframes-audio`); la voz
  no lee el texto en pantalla.
- **Loudness**: integrada **-14 LUFS ±1**, true peak **≤ -1 dBTP** (web/redes). Normalizar en dos
  pasadas con `loudnorm` (receta en `media-use`):
  `ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -` → segunda pasada con
  los valores medidos.

## 11. Especificaciones de entrega
| Formato | Resolucion | fps | Codec | Bitrate video | Audio |
|---|---|---|---|---|---|
| Keynote master | 3840x2160 | 30 (60 con scroll de UI largo) | H.264 High yuv420p (H.265 para archivo) | 35-50 Mbps | AAC 48 kHz 320 kbps, -14 LUFS, TP ≤ -1 |
| Keynote envio/web | 1920x1080 | 30 | H.264 High yuv420p | 10-16 Mbps | idem |
| Clip / teaser 16:9 | 1920x1080 | 30 | H.264 | 8-12 Mbps | idem |
| 9:16 | 1080x1920 | 30 | H.264 | 8-10 Mbps | idem + subtitulos quemados |
| 1:1 | 1080x1080 | 30 | H.264 | 6-8 Mbps | idem + subtitulos quemados |
| Version muda | = original | 30 | H.264 | = | sin audio, subtitulos quemados |
| Poster | tamaño del formato | — | PNG | — | — |
Limites de cada plataforma: verificarlos vigentes con fuente y fecha antes de exportar. Plantilla:
`templates/video/especificacion-entrega.md`.

## 12. Captura del material real (tamaño real, nitido)
**Capturas fijas**: `browser_resize` 1920x1080 → `browser_take_screenshot` (2x para macro y 4K); datos
ficticios; sin cursor, toasts, banners ni barras.

**Grabaciones** — secuencia obligatoria (Playwright comparte una sola captura por pagina; si la traza
arranca antes que el video, el video sale chico en la esquina con relleno gris):
1. Navegador limpio (`browser_close` si ya hubo video o traza en la sesion).
2. `browser_resize` al viewport exacto.
3. `browser_start_video` con `size` = viewport exacto.
4. `browser_video_hide_actions` (marketing no lleva superposicion de acciones).
5. Traza solo si se necesita, SIEMPRE despues del video.
6. Recorrido lento y seguro con `browser_video_chapter` por paso.
7. `browser_stop_tracing` y `browser_stop_video`; un video por sesion de navegador.
8. Verificar: `python3 scripts/normalizar_video.py {archivo}.webm` (en esta skill) → **OK**. Si sale
   RELLENO o REPARADO, **se regraba** (para marketing la version reparada no sirve: pierde nitidez).

**Nitidez**: una grabacion 1080p nunca se escala a pantalla completa en un master 4K; va dentro de un
marco a ≤ 100% de su tamaño nativo, o se usan capturas 2x para los planos grandes.

## 13. Produccion con HyperFrames
1. `hyperframes` (entrada) → `product-launch-video` (Paso 0 setup `hyperframes.json` + `BRIEF.md` → 1
   captura → 2 `frame.md` → 3 `STORYBOARD.md` + `SCRIPT.md` → 3.1 audio → 4 diseño por frame → 5 frames
   `compositions/frames/NN-*.html` + `index.html` → 6 render). Puertas del usuario en 0, 3 y 6.
2. Proyecto en `.marketing/campanas/{ID}/piezas/video/{proyecto}/` (nunca en un repo).
3. Un capitulo = una sub-composicion (`hyperframes-core`); los clips reutilizan la del capitulo.
4. Catalogo antes de escribir movimiento: `npx hyperframes catalog --query "..."` (en ingles).
5. Camara con `hyperframes-keyframes`; blueprints y transiciones de `hyperframes-animation`; diseño,
   tipografia y beats con `hyperframes-creative`; mezcla con `hyperframes-audio`; musica, SFX, voz,
   LUT y subtitulos con `media-use`.
6. `npx hyperframes lint` (iterar) → `npx hyperframes check` (gate) → `npx hyperframes preview
   --background` (aprobar) → `npx hyperframes render --quality draft|high --output ...`.
`STORYBOARD.md` (formato de `hyperframes-core`): frontmatter `format: 1920x1080`, `duration`,
`message`, `arc: Apertura → Problema → P01 … Pnn → Prueba → Hoja de ruta → Cierre`, `audience`; un
`## Frame N — {titulo}` por plano/beat con `duration`, `transition_in`, `scene`, `voiceover`, `poster`.

## 14. Preproduccion (orden y entregables)
Concepto (1 frase + 3 referencias) → tratamiento (1 pagina) → guion por parte
(`templates/video/guion-parte.md`) → storyboard cuadro a cuadro con duracion por plano
(`templates/video/storyboard-parte.md`) → **animatic** (render draft en tiempo real con la musica) →
aprobacion. Nada se produce sin animatic aprobado.

## 15. QA cuadro a cuadro
```bash
python3 scripts/qa_video.py entregas/keynote-ceo-16x9-1080p-v1.mp4 --spec 1920x1080 --duracion 190 --fps 30
python3 scripts/qa_video.py entregas/ --spec 1080x1920          # todos los verticales
python3 scripts/qa_video.py entregas/keynote-...-muda-v1.mp4 --muda
```
Mide codec, resolucion, fps, duracion (±0,5 s), bitrate, loudness y true peak, negros y congelados, y
extrae 12 fotogramas + hoja de contactos en `{video}-qa/`. Luego se revisan los fotogramas de cada
capitulo con `templates/video/checklist-qa-video.md`: producto nitido y a tamaño completo, textos
completos y legibles, marca correcta, ningun dato real. Una falla bloquea la entrega.

## 16. Accesibilidad
Subtitulos siempre; version muda; nada de destellos de mas de 3 por segundo; contraste AA en texto
sobreimpreso; piezas web animadas con alternativa `prefers-reduced-motion` (fundido simple o imagen fija).

## 17. Anti-patrones (lo que hace que se vea barato)
Slideshow animado (capturas que entran y salen con fundido, sin camara ni ritmo) · transiciones de
PowerPoint · texto que no se alcanza a leer · voz que lee el texto · musica generica de banco sin
intencion · capturas borrosas, chicas, pixeladas o con relleno gris · UI de fantasia (hologramas,
dashboards inventados) · stock footage generico · lens flares y particulas de plantilla · logo
deformado o recoloreado · copiar logos, sonidos, musica o claims de los referentes · render final sin
aprobacion.
