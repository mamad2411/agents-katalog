---
name: shorts-animados-3d
description: >-
  Crea shorts verticales animados de dos estilos, caricatura 2D en un mundo 3D
  con Three.js y Remotion, o animación 3D realista con Blender. Úsala cuando
  pidan la skill de shorts de LuisPa, un video como el de Alejandro o el puente,
  o animaciones realistas como las de puntadas en Blender.
---

# Shorts animados 3D (three.js + Remotion)

## Primero: elige el estilo y acompaña a la persona

Cuando alguien abra la skill por primera vez o no haya elegido un estilo, explica de forma breve que este paquete incluye dos caminos y muestra los dos ejemplos **antes de pedir que elija**:

1. **Animación 3D realista con Blender**: escenas creadas con modelos, materiales, luces y cámara 3D, por ejemplo animaciones explicativas de anatomía. El ejemplo muestra una herida con puntadas: avisa antes de mostrarlo. [Ver imagen](ejemplos/animacion-realista.png) · [Ver video de Blender](ejemplos/video-blender-puntadas.mp4) (vista previa de 9 s, sin audio).
2. **Caricatura animada**: personajes planos de caricatura en escenarios 3D coloridos. Se crea con código usando Three.js y Remotion. [Ver imagen](ejemplos/animacion-caricatura.jpg) · [Ver video de Alejandro Magno](ejemplos/video-alejandro-caricatura.mp4) (vista previa de 9,8 s con audio).

Si el entorno permite mostrar imágenes o reproducir videos, muestra ambos ejemplos directamente en el chat; de lo contrario, proporciona enlaces o rutas completas a los archivos locales para que la persona los abra. No afirmes que se mostraron o reprodujeron si el entorno no pudo hacerlo. Pregunta «¿Cuál estilo quieres: realista con Blender o caricatura?» y espera la respuesta antes de instalar o preparar herramientas. Si ya indicó claramente el estilo, respétalo y evita volver a preguntar.

Habla en español sencillo. Pregunta una cosa por vez cuando la persona sea principiante, explica cualquier término técnico y acompaña la instalación sin asumir que sabe programar. Comprueba sistema operativo, programas disponibles y requisitos de la ruta elegida; explica las opciones y posibles costos antes de que el usuario elija proveedores externos de voz u otros servicios. No solicites claves en el chat. El paquete contiene plantillas, no un video terminado ni un proyecto que funcione automáticamente al descargarlo.

Después pide la idea y la duración. Ayuda a preparar y revisar guion, voz y escenas; genera avances y deja espacio para que la persona indique correcciones. Continúa hacia el render y verifica que se haya producido un MP4 con imagen y audio cuando las herramientas y recursos estén disponibles. No prometas calidad o resultado automático: si falta algo, explica qué está pendiente y cómo resolverlo. Sigue `realista/REALISTA.md` solo para Blender; para caricatura sigue el proceso de abajo.

### Entrega sencilla en Mac y Windows

Estas instrucciones son para ti, Claude: acompaña a la persona sin obligarla a leer archivos técnicos. Detecta su sistema operativo y pregúntale dónde quiere guardar el proyecto (por ejemplo, una carpeta de su Escritorio); usa la ubicación real que te indique, sin suponer que el Escritorio se llama `Desktop` ni que está fuera de OneDrive o iCloud. Conserva juntos los archivos necesarios, la narración, el proyecto editable y la salida, sin copiar credenciales ni archivos ajenos. Si ya entregó guion o audio, úsalos y no se los vuelvas a pedir. Avisa si falta algo imprescindible.

Para Windows prepara en la carpeta elegida un `RENDERIZAR.bat`; para Mac, un `RENDERIZAR.command` ejecutable. Adáptalo al proyecto y al motor seleccionado: Blender para realista; Remotion para caricatura. Al hacer doble clic debe comprobar que existen los programas y archivos requeridos, iniciar el render, indicar el progreso, detenerse y mostrar el error si algo falla, y conservar la ventana abierta con la ruta del resultado. Usa rutas relativas al propio proyecto y admite espacios. No borres proyectos ni cuadros existentes; evita mezclar cuadros de renders distintos. Crea el MP4 final con la narración cuando exista y comprueba imagen, audio y duración. Si hay un problema no lo anuncies como terminado.

En Blender detecta y prueba la GPU disponible: Metal en Mac; OptiX o CUDA para NVIDIA en Windows, HIP para AMD y OneAPI para Intel, según soporte real de la versión de Blender. Confirma en el registro el dispositivo que realmente se usa; si no funciona, explica la causa y ofrece CPU, sin afirmar que la GPU funcionó. La exportación de Remotion es distinta: no garantices que toda la codificación use la tarjeta gráfica. Antes de entregar el lanzador, ejecuta una prueba pequeña cuando el entorno lo permita; si no puedes probarlo en el sistema del usuario, dilo claramente. El tiempo para preparar y renderizar varía, no prometas diez minutos.

Skill de **Crea con LuisPa**, en español. Está basada en la skill gratuita
[claude-animated-shorts](https://github.com/mromidev/claude-animated-shorts) de Mr omi (licencia MIT): el motor,
las plantillas del puente y los reportes de medición son de él. Lo nuevo de esta versión: todo en español, el short
de Alejandro Magno como segundo ejemplo completo (batalla, multitudes enormes, cámara lenta, brasas), la herramienta
para medir cualquier short a 30 cuadros por segundo y las reglas que salieron de corregir ese short.

Ejemplos probados:
- **Alejandro Magno en Gaugamela** (`plantillas/alejandro/`, composición `Alejandro`, 1080x1920, 30 fps, 9.8 s).
  Guion en `plantillas/alejandro/GUION_alejandro.md`.
- **El puente que se cayó por una canción** (`plantillas/puente/`, 67 s, en inglés), de Mr omi.

El estilo se estudió midiendo 20 shorts de un canal de referencia (`referencias/`). Esos cuadros son **solo para
estudiar el estilo**:
- Nunca copies sus guiones, personajes ni tomas. Historia, personajes y voz siempre son tuyos.
- No subas ni publiques sus videos. No digas el nombre del canal en la voz ni en la descripción.


## Shorts 3D realistas (Blender)
Si piden que se vea **real** (piel, heridas, puntadas, cuerpo humano, «render de Blender»), NO uses three.js:
sigue `realista/REALISTA.md`. Ahí está el proceso, cada pieza (piel, herida, hilo, vello, luz), los errores que ya
salieron y cómo bajar el tiempo de render. Hay dos ejemplos completos: `realista/blender/puntadas_brazo/` (9 s) y
`realista/blender/puntadas_pierna/` (31 s). La cámara se mide con `realista/herramientas/camara_fase.py`.

## Reglas del estilo
- Voz en español, una sola voz pareja, de corrido: 3.2–3.8 palabras por segundo, casi sin silencios.
- Sin subtítulos en la versión principal (el estilo de referencia sale sin ellos). Si quieres una versión con
  subtítulos, hazla aparte.
- Nada de recuadros, subrayados ni flechas encima de los personajes. Una cifra importante (p. ej. «47,000») va
  discreta, arriba del cuadro, sin tapar a nadie.
- Los chistes y datos son hechos reales investigados, con su fuente.
- Mezcla: voz al frente; música y efectos de 5 a 10 dB abajo; -14 LUFS al final.
- Exporta vertical 1080x1920 (o 1440x2560 con `--scale 1.3333`).
- Guarda después de cada paso. Una vez aprobado el guion, hazlo de corrido.

## Proceso
1. **Tema y datos.** Una historia real y sorprendente con causa y efecto que se pueda ver, más una comparación
   cotidiana que la explique. Escribe los datos con su fuente arriba del `GUION.md`.
   - Si las cifras varían (fuentes antiguas contra historiadores modernos), usa la estimación moderna y dilo así.
2. **Guion** (fórmula de `referencias/BIBLIA_DE_ESTILO.md`):
   - **Gancho:** el dato absurdo en una sola frase, sin introducción.
   - **Lugar y época:** año, lugar, orgullo.
   - **Escalada:** tres o cuatro momentos, cada uno más grande.
   - **El momento en que se rompe.**
   - **Doble línea seca:** «Por suerte… / Por desgracia…».
   - **Explicación** con una comparación cotidiana, entrando con un giro fijo («Fíjate…»).
   - **Consecuencia** y **remate** con sorpresa. El video termina en la última palabra.
   - Nunca describas con la voz lo que ya se está viendo.
3. **Voz.** Graba o genera `voz.wav` y saca los tiempos por palabra a `palabras.json` (cualquier
   transcriptor con tiempos por palabra). Corrige los tiempos a mano: todo se sincroniza con ese archivo.
4. **Plan de tomas** en `story.ts`. Copia la plantilla más parecida (`plantillas/alejandro/` para batallas y
   multitudes, `plantillas/puente/` para pueblo y personajes que caminan) a `src/videos/<nombre>/` y regístrala en
   `src/Root.tsx` (ver `plantillas/alejandro/Root_ejemplo.tsx`).
   - `SHOTS`: cada toma con sus cuadros a/b y sus llaves de cámara `{f, pos, look, fov, glide}`.
   - `XFADE`: fundido de 6 cuadros cuando cambia el lugar.
   - Cada reacción en pantalla cae 0–3 cuadros antes de su palabra. Anota los cuadros de cada palabra arriba de
     `story.ts`.
5. **Mundo.**
   - `lights.ts`: luces y paleta de cielo/niebla por tipo de luz.
   - `shade.ts`: sombreado de dos tonos.
   - `paint.ts`: texturas pintadas con Canvas2D (suelo, nubes, madera, piedra), con las uniones pintadas oscuras.
   - `world.ts`: cielo, niebla del color del horizonte, poses por cuadro. En Alejandro también: suelo quemado,
     humo, flechas encendidas clavadas, montañas con nieve y brasas flotando (`Points`).
6. **Personajes.**
   - `toon.ts`: la API de dibujo `Pen` (lienzo 600x1000, pies en y = 975, cabezas de frijol, extremidades de
     palito, contorno ciruela de grosor variable, librería de caras).
   - En Alejandro se agregaron vistas de frente (`horseFront`, `rideFront`, `chariotFront`), caballo, elefante,
     carro de guerra, la opción de alzar armas y la cara de grito.
   - Multitudes: `troop.ts` + `crowd.ts` dibujan miles de soldados en un atlas y los reparten en el campo
     (100 mil dibujos, cada uno en su lugar). Todos los personajes van en la capa `NOINK`.
   - `cardshade.ts`: los personajes reciben la luz de la escena (no brillan solos) y proyectan sombra.
7. **Post** (`Alex.tsx`/`Bridge.tsx` + `ink.ts` + `lensblur.ts` + `grade.ts`). Orden: tinta → desenfoque →
   bloom → mapeo de tono NEUTRAL → corrección de color (MSAA 4). Todo valor en píxeles escala con alto / 1920.
8. **Sonido.**
   - Opción A (puente): todo sintetizado con `plantillas/audio/` (efectos y música original bajo la voz).
   - Opción B (Alejandro): efectos grabados de tu biblioteca con licencia, colocados para que su pico caiga en
     su cuadro (`plantillas/alejandro/mezcla_ejemplo.py`). Un fuego que crepita de fondo, whoosh en cada
     movimiento de cámara, impacto en cada cifra, whoosh lento y grave en la cámara lenta.
   - Nada de pops de burbuja repetidos ni efectos de caricatura baratos.
   - Fija los tiempos de la imagen antes de hacer el sonido.
9. **Revisión del look.** Saca fotos sueltas: `node plantillas/scripts/fotos.mjs out/x_ 20,100,200 0.5`.
   Ponlas junto a cuadros de `referencias/cuadros/` con `python plantillas/scripts/sbs_sheet.py` y revisa.
10. **Medición.** Mide tu render igual que la referencia:
    `python herramientas/medir_30fps.py out/video.mp4 out/medida`. Saca hojas de 60 cuadros, cortes, % de cuadros
    con la cámara en movimiento, brillo, contraste y saturación. Meta: cámara moviéndose en más del 80 % de los
    cuadros y 0–1 cortes duros.
11. **Render final.**
    `npx remotion render src/index.ts <Composición> out/video.mp4 --codec h264 --crf 16`
    y junta el audio con `-map 0:v:0 -map 1:a:0` (Remotion escribe una pista de audio muda).
    Revisa cada cuadro con `python plantillas/scripts/short_qa.py final.mp4 out/qa shots.json`.

## Lo que aprendimos con Alejandro (revísalo en cada short nuevo)
- **La primera versión siempre sale «bonita, de día de campo».** Si la historia es una guerra, que se vea guerra:
  luz naranja de humo, suelo quemado, flechas ardiendo, carros rotos. Nada de un ambiente feliz.
- **La toma aérea muy alta (570 m) se ve como puro ruido.** Para que se entienda el tamaño de un ejército, baja la
  cámara y ponla alta *detrás* de un bando mirando al otro (en Alejandro: `[0,60,-110] → [0,0,90]`, fov 58).
- **Un ejército enorme nunca debe terminar dentro del cuadro.** Si se le ve el final, se ve chico.
- **Presenta a cada protagonista de frente**, pasa la cámara enfrente de él y métela entre su gente; luego sube
  para enseñar cuántos son. Al pasar, sus soldados alzan las armas y gritan (la primera fila primero).
- **Cámara lenta en el momento fuerte**: el reloj del mundo corre al 22 % (`worldF` en `story.ts`), con un sonido
  grave y lento. Entra y sale suave.
- **Brasas de fuego flotando** cerca de la cámara dan profundidad y vida a cualquier toma de batalla.
- **La cámara nunca se queda quieta**: cada pausa lleva un acercamiento lento. Un tramo de 12 cuadros sin
  movimiento se ve como video trabado.
- **Antes de renderizar, revisa cuadros sueltos de cada toma**: cámaras atoradas dentro de una casa, árboles
  verde azulado, una cadena o un objeto justo enfrente de las caras.
- **Pide que lo compare contra la referencia por áreas** (color, tinta, luz y sombra, texturas, personajes,
  profundidad, movimiento) con números, no con opiniones. Una opinión no la puedes recrear; un número, sí.

## Valores finales del look (del puente, después de 4 rondas de revisión)
- **Luz** (`lights.ts`, sol fijo por toma y relativo a la cámara):
  - día: az 75 / el 48, luz [1.58,1.5,1.33], sombra [.30,.29,.36], tinte frío SOLO en la sombra; cielo #3e7fd2 →
    horizonte #b8d0ec; niebla = horizonte, 25→300 m.
  - atardecer: sol bajo a contraluz (az 6 / el 7), luz #FFB36B ×1.5, sombras violeta-azul (nunca cafés), cielo
    #ffc47c → #8a6f8a.
- **Tinta** (`ink.ts`): #030303, 5.1 px de cerca (6 m) → 3.3 px de lejos (90 m) a 1080x1920. Los personajes no
  llevan la tinta del mundo: traen su propio contorno ciruela.
- **Desenfoque** (`lensblur.ts` + `dofAt`): primeros planos 12–16 px, planos medios 10–12, tomas abiertas 0.
  Enfoque en los ojos de la primera fila.
- **Personajes:** cabeza de frijol (alto/ancho .94), contorno ciruela #241726, ojos a .26 del ancho, sin
  chapitas; adultos de 3.5 cabezas; parpadeo cada 0.5–2.3 s; sombra de contacto bajo los pies.
- **Cámara:** cortes solo en saltos grandes; lo demás, deslizamientos suaves (smootherstep) de 18–40 cuadros;
  sacudidas en impactos que cambian de signo cada cuadro y se apagan en 7; giros de 4–4.6°.
- **Color de referencia:** brillo mediano de día ~.57, sin negros aplastados (p5 ~.23), saturación alta.
- **Grano de película: apagado.** La referencia no tiene, y multiplica el tamaño del archivo.

## Cuando no se parece a la referencia (ciclo de comparación con agentes)
1. **Mide primero la referencia.** Un agente por área (movimiento, profundidad, texturas, personajes, luz,
   contornos, color), cada uno escribe números en `referencias/reportes_en/<área>.md` (ya vienen hechos).
2. **Un dueño por archivo.** Copia el proyecto a una caja de arena por agente
   (`src/videos/<nombre>_{cam,world,mat,char,post}`). Dueños:
   - cam: `story.ts` · world: `world.ts`, `lights.ts`, `shade.ts`, `grade.ts` · mat: `paint.ts`, `build.ts` ·
     char: `toon.ts`, `cast.ts`/`troop.ts`, `cardshade.ts` · post: `ink.ts`, `Alex.tsx`/`Bridge.tsx`, `lensblur.ts`.
   Cada agente solo toca sus archivos en su copia. Así no se rompen el trabajo entre ellos.
3. **Junta** con `python plantillas/scripts/bridge_merge.py`, corre `npx tsc --noEmit` y vuelve a sincronizar
   todas las copias antes de la siguiente ronda.
4. **Verifica** con un agente nuevo: hojas lado a lado, calificación de 0 a 10 por área y una lista de arreglos
   con número de cuadro. Cada arreglo va al dueño de ese archivo.

## Trampas conocidas
- Los modelos del kit de naturaleza de Kenney salen color verde azulado: recolorea por nombre de material.
- Las cámaras terminan dentro de las casas: quita todo lo que tape un rayo de la cámara.
- Si la tinta va en el mismo paso que el desenfoque, el desenfoque la borra. La tinta va en su propio paso, antes.
- Los valores en píxeles del post deben escalar con la resolución (las fotos de prueba van a 0.5).
- **Disco:** cada bundle de Remotion copia `public/` a la carpeta temporal y no lo borra. Renderiza con
  `TEMP`/`TMP` apuntando a un disco grande y borra los `remotion-webpack-bundle-*` cuando termines el proyecto.
- Archivos `.ts` de prueba dentro de `out/` rompen `tsc`: nómbralos `.txt`.
- Un columpio con una sola cuerda que se pierde detrás del niño se ve como un ahorcado: siempre dos cuerdas.
- Objetos a menos de ~2 m del lente se ven como manchas enormes en la orilla: revisa cada objeto cerca de la cámara.
- Un arbusto cortado por la orilla del cuadro se ve como «pelota verde»: que se reconozca o que no esté.
- Banderas: usa la correcta de la época y el lugar.
