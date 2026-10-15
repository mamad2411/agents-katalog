---
name: piensa-brand-docs
description: >-
  Construye documentos visuales de marca de Piensa Digital AI como artifacts HTML
  editables que se exportan a PDF o imagen con calidad de imprenta. Estética dark
  premium (negros/grises tipo Vercel, acentos violeta+mint, glassmorfismo, tipografía
  Montserrat+Inter). Usá esta skill SIEMPRE que se pida crear un informe, reporte,
  documento, one-pager, propuesta, dossier, carátula, placa o pieza gráfica "de Piensa
  Digital AI" o "con la estética de la agencia" — aunque no digan la palabra "skill" ni
  "template". También cuando pidan un PDF o imagen "que se vea profesional / de marca /
  como el informe de Sanz Clima", o cuando haya que mantener coherencia visual entre
  documentos de la agencia. El contenido es dinámico; el diseño (fondos, fuentes, logo,
  cards, headers/footer, colores) es fijo y lo aporta la skill.
---

# Piensa Brand Docs

Genera documentos con la identidad visual de **Piensa Digital AI**: un sistema de diseño
dark, premium y consistente, empaquetado para que sólo cambie el **contenido**. El output
es un **único HTML autocontenido** que la persona abre en su navegador para editar textos,
y desde una **barra de herramientas** exporta a **PDF** o a **imagen** (PNG/JPG).

## Por qué está armado así (leé esto, te ahorra errores)

- **Los fondos son imágenes rasterizadas**, no degradados CSS. Un degradado vectorial se
  ve distinto en cada visor de PDF (Acrobat lo satura y hace banding; PDFium lo dibuja
  lento). Una imagen se ve idéntica en todos lados. Los fondos de marca ya están horneados
  para A4 en `assets/backgrounds/a4/`. Para otros tamaños se re-hornean (ver más abajo).
- **El documento final incrusta TODO** (fuentes, fondos, logo, Tailwind, librería de
  export) como data URIs. Así funciona offline y — clave — permite exportar imágenes del
  lado del cliente sin que el navegador bloquee el canvas por seguridad ("tainted canvas").
- **Flujo dev → build**: editás un HTML liviano que referencia `./assets/...` (fácil de
  leer y modificar); un script lo compila incrustando todo. Nunca edites el archivo final
  gigante a mano.
- **El texto es siempre vectorial** en el PDF (nítido y seleccionable). Sólo el fondo es
  imagen.
- **Todos los scripts son Node.js, sin dependencias externas** (sólo `fs`/`path`/`http` de
  la librería estándar). Esto es a propósito: como la skill se instala vía `npx skills add`,
  Node ya está garantizado en la máquina — no hay que asumir que la persona tiene Python
  instalado, ni pedirle que instale nada. La única excepción es `bake-backgrounds.js`
  (sólo hace falta para tamaños que no sean A4), que necesita un navegador Chromium
  instalado — ver el paso 3.

## Identidad visual (resumen)

- **Fondo dark** neutro (negros/grises, sin tinte azul). Acentos de marca: **violeta**
  `#7400b8` / `#7b3fe4` / `#e1b6ff` y **mint** `#42e2b8` / `#62fbd0`.
- **Tipografía**: Montserrat (títulos/display) + Inter (texto). Embebidas.
- **Bloques/cards**: glassmorfismo (blur 16px + saturación), borde fino `rgba(255,255,255,.08)`,
  esquina redondeada 14px, línea superior en gradiente opcional para destacados.
- **Tags/pills**, **badges numéricos** (estilo Supabase: borde fino mint + interior apagado),
  **bullets** en gradiente, **encabezado corrido** y **pie** con texto a la izquierda y
  numeración a la derecha.

El catálogo completo de tokens y componentes (con el código de cada bloque) está en
**`references/design-system.md`**. Leelo antes de armar bloques que no estén en el template.

## Flujo de trabajo

### 1. Entender el pedido (preguntar tamaño y orientación)
Antes de generar, definí el **lienzo**. Si la persona no lo aclara, **preguntá** tamaño y
orientación. Aceptá píxeles ("1080x1350") o prosa ("para Instagram", "para LinkedIn",
"carta/Letter", "apaisado"). **Default: A4 vertical** (como el informe de Sanz Clima).
Tamaños útiles (px @96dpi):

| Uso | Ancho×Alto | Nota |
|---|---|---|
| A4 vertical (default) | 794 × 1123 | fondos ya horneados en `assets/backgrounds/a4` |
| A4 apaisado | 1123 × 794 | re-hornear fondos |
| Carta / Letter | 816 × 1056 | re-hornear |
| Instagram post | 1080 × 1080 | social, `--scale 1` |
| Instagram story / vertical | 1080 × 1350 | social, `--scale 1` |
| LinkedIn / X imagen | 1200 × 675 | social, `--scale 1` |

También definí: **¿lleva portada?** (los reportes sí; una placa suelta quizás no) y
**cuántas páginas/hojas** aproximadamente.

### 2. Preparar la copia de trabajo
Copiá `template.html` (está en la raíz de la skill) y la carpeta `assets/` a una carpeta de
salida (p.ej. junto al proyecto del usuario). El template referencia `./assets/...`, así que
`assets/` tiene que quedar como carpeta hermana del HTML de trabajo.

```
salida/
├── working.html         # copia de template.html — acá editás
└── assets/              # copia de la carpeta assets/ de la skill
```

### 3. (Sólo si el tamaño NO es A4) hornear los fondos
```bash
node scripts/bake-backgrounds.js --width <W> --height <H> --count <N> --scale <S> --out salida/assets/backgrounds/custom
```
Usá `--scale 1.5` para tamaños tipo papel (más nitidez), `--scale 1` para social ya grande.
Luego, en `working.html`, apuntá las reglas `#page-N { background-image: url("./assets/backgrounds/custom/bgN.png") }`
y actualizá `--page-w` / `--page-h` en `:root` y el `@page { size: ... }`.

Este script necesita un navegador Chromium (Chrome, Edge o Chromium) instalado en la máquina
para rasterizar el degradado — es el único requisito externo real de toda la skill. Si no lo
encuentra, lo dice claramente en la consola. En Windows casi nunca falta (viene Edge de
fábrica); si igual faltara y el documento es tamaño papel, usá directamente los fondos ya
horneados en `assets/backgrounds/a4/` sin necesidad de este paso.

### 4. Editar el contenido (la estructura NO es rígida)
`template.html` trae **dos hojas de ejemplo** (portada + una página de contenido con los
bloques más comunes) para que no arranques de una hoja en blanco. **No es un molde a llenar
tal cual** — es un punto de partida. El documento real puede necesitar 1 página o 12, con
una portada o sin ella, con grillas de comparación en vez de listas, con 2 secciones por
hoja en vez de 1, etc. Armá la estructura que el contenido pida, combinando los bloques de
**`references/design-system.md`** (ahí está cada componente suelto: cards, pills, badges
numéricos, grillas, bloque de firma, encabezado corrido...) o creando variaciones nuevas que
respeten los mismos tokens.

Lo que **sí** hay que mantener siempre (esto es lo que hace que se vea "de Piensa Digital AI"
sea cual sea la estructura):
- Los tokens de color, tipografía (Montserrat+Inter) y glassmorfismo.
- Una `<div class="page-wrap">` + checkbox de selección por cada hoja (para que el PDF
  pagine bien y la descarga de imágenes funcione).
- La barra de herramientas y el bloque `<script>` **intactos** — ahí vive toda la lógica
  de edición, zoom, exportación y colores.

Reemplazá los placeholders `{{...}}` que uses, borrá los que no, y ajustá numeración de
páginas y footers. Mirá **`references/example-report.html`** para ver un documento real
completo (el informe Sanz Clima) — es la mejor guía de cómo se ve terminado, aunque su
estructura de 2 páginas es sólo uno de los muchos layouts posibles.

Reglas de oro de layout: A4 entra ~1 bloque destacado + 1 sección con 3-4 cards por hoja.
No amontonar; si sobra contenido, agregá una hoja. Cada hoja es una `<article class="page-container">`
independiente para que el PDF mantenga los saltos de página.

### 5. Compilar el documento final (SIEMPRE, sin que lo pidan)
Este paso es **parte de entregar el documento**, no opcional. Apenas termines de editar el
contenido, corré el build automáticamente y entregá el archivo compilado:
```bash
node scripts/build-document.js salida/working.html salida/Documento.html
```
Esto incrusta todo (fuentes, fondos, logo, Tailwind, librería de export) y produce el HTML
autocontenido (pesa varios MB por los fondos: es normal y esperado). **Entregá
`Documento.html`** — nunca el `working.html`, porque sin los assets al lado se ve sin estilos
y la descarga de imágenes no funciona (el navegador bloquea el canvas con archivos externos).

### 6. Previsualizar/verificar SIEMPRE por localhost, nunca con file://
Si necesitás abrir el documento en un navegador para revisarlo vos mismo (por ejemplo con una
herramienta de automatización/screenshot antes de entregarlo), **serví la carpeta por HTTP**:
```bash
node scripts/serve.js salida/ 8080
```
y abrí `http://localhost:8080/Documento.html` (o `working.html` mientras editás). **No abras
el archivo con `file://`.** Dos razones concretas:
- Las herramientas de navegador automatizado (Playwright y similares) suelen **bloquear
  `file://` por seguridad** — la carga falla o queda en blanco, no es un bug del documento.
- Mientras trabajás sobre `working.html` (antes del build), el navegador puede negarse a
  cargar sus referencias relativas a `./assets/...` bajo `file://` según la configuración de
  seguridad; por HTTP siempre funciona.
`serve.js` no tiene dependencias (sólo Node), corré el comando en segundo plano y seguí
trabajando. Esto es sólo para TU verificación — la persona que reciba `Documento.html` sí
puede abrirlo con doble clic normalmente en su propio navegador (es autocontenido, no
depende de ningún servidor).

### 7. Exportar (lo hace la persona desde la barra)
- **Descargar PDF**: botón blanco → diálogo del navegador → *Guardar como PDF · Márgenes:
  Ninguno · Gráficos de fondo: ✓*. Texto vectorial, fondo imagen, idéntico en todo visor.
- **Descargar imágenes**: elegir formato (**PNG 1x** default, PNG 2x, PNG 3x, o **JPG**
  —menor calidad—) y, si se quiere, tildar **"Solo selecc."** para bajar sólo las hojas
  marcadas con su checkbox. Cada hoja se baja como una imagen.

## Barra de herramientas (qué incluye)
Zoom escalonado 50→200% (default 100%) · Márgenes (guías) · Selector de formato de imagen +
selección de páginas · Descargar imágenes · Descargar PDF · Colores de texto (muestras +
personalizado) · Restablecer (vuelve al color/gradiente original). *No* incluye "alternar
gradiente" (se quitó a propósito).

## Recursos que puede aportar el usuario
Cualquier archivo que la persona deje en **`resources/`** (una imagen, un logo alternativo,
un ícono, un gráfico) está disponible para usar en el documento. Cuando el pedido mencione
"usá la imagen que dejé", "poné este logo", etc., buscá en `resources/`, copiá el archivo a
`salida/assets/` y referencialo desde `working.html` (el build lo incrustará). Para cambiar
el **logo** por defecto, reemplazá `assets/logo.png` (o apuntá el `<img>` de la portada al
recurso nuevo). Ver `resources/README.md`.

## Estructura de la skill
```
piensa-brand-docs/
├── SKILL.md
├── template.html             # esqueleto editable (copialo junto con assets/)
├── references/
│   ├── design-system.md      # tokens + código de cada componente/bloque
│   └── example-report.html   # documento real (Sanz Clima) como guía
├── assets/
│   ├── fonts.css             # Inter + Montserrat + iconos, embebidos
│   ├── logo.png              # logo de marca
│   ├── lib/                  # tailwind.js + html-to-image.js (offline)
│   └── backgrounds/
│       ├── a4/ bg1..bg4.png  # fondos horneados A4 (1.5x)
│       └── _source.html      # generador de fondos (lo usa bake-backgrounds.js)
├── scripts/                  # todo Node.js puro, cero dependencias externas
│   ├── build-document.js     # working.html + assets → HTML autocontenido (SIEMPRE)
│   ├── bake-backgrounds.js   # hornea fondos a cualquier tamaño (sólo si no es A4)
│   └── serve.js               # servidor estático mínimo, para previsualizar por localhost
└── resources/                # dropzone: el usuario deja acá imágenes/logos a usar
```

## Iteración
Todo es iterable en el mismo chat: si piden otro color de sección, otro tipo de bloque,
mover el pie, etc., editá `working.html` y recompilá. Los estilos raramente cambian, pero
cuando cambien, tocá el `<style>` del template (o de la copia) y volvé a compilar.
