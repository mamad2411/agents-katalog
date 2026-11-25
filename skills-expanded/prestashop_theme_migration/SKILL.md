---
name: prestashop_theme_migration
description: Adaptar/migrar o auditar un tema de PrestaShop (classic, hijo de classic o tema propio) entre versiones 1.7.0 → 1.7.8.11 → 8.0 → 8.1 → 8.2 → 9.0 → 9.1 → 9.2. Prioriza dos cosas: arreglar errores críticos (checkout, registro, plantillas rotas) y aplicar las mejoras de SEO y rendimiento que el tema se está perdiendo (JSON-LD, canonical, WebP/AVIF, lazy loading, Core Web Vitals), descartando el ruido de paridad cosmética con classic. Contiene el diff real del tema classic versión a versión a nivel de patch, los breaking changes de Smarty, la línea temporal de features y el protocolo de verificación del proceso de compra. Cubre también el tema Hummingbird (Bootstrap 5, tema por defecto en instalaciones nuevas desde 9.1) y cuándo NO conviene migrar a él. Usar al subir de versión una plantilla hecha para 1.7.x/8.x, auditar un tema tras un upgrade, diagnosticar una plantilla rota, decidir entre classic y Hummingbird, o saber en qué versión se introdujo un cambio del tema.
risk: high
source: analysis
date_added: '2026-07-24'
author: Ivan C.
tags:
  - prestashop
  - theme
  - smarty
  - migration
  - classic-theme
  - hummingbird
  - bootstrap5
  - webp
  - checkout
---

# Migración de temas PrestaShop entre versiones

## Regla de oro

**Ningún cambio puede romper la maquetación ni la funcionalidad existente.**
El proceso de compra (carrito → dirección → envío → pago → confirmación) es
intocable: es lo último que se toca y lo primero que se verifica. Ante la duda
entre "modernizar" y "no romper", **no romper gana siempre**.

## Prioridades

El objetivo de una migración **no** es que el tema se parezca a classic. Es que
(a) nada esté roto y (b) la tienda venda y posicione mejor que antes. Todo lo que
no sirva a una de esas dos cosas es ruido.

Cuatro capas, en este orden:

1. **Bloqueantes** — lo que impide que la plantilla renderice (errores de Smarty,
   variables inexistentes). Sin esto la tienda está caída.
2. **Errores críticos** — lo que renderiza pero no funciona, o funciona mal, y
   cuesta dinero: checkout, registro, combinaciones, filtros, JS roto.
3. **SEO y rendimiento** — JSON-LD, canonical, WebP/AVIF, lazy loading,
   dimensiones de imagen. **Es un entregable, no un extra opcional.**
4. **Paridad cosmética con classic** — el resto. Casi siempre **no vale la pena**
   y suele ser el grueso del diff. Ver "Qué no tocar".

**Las capas 1 y 2 van primero siempre**, y se verifican con un pedido real antes
de seguir. Pero una migración que se queda ahí está a medias: la capa 3 es donde
está el valor que el cliente percibe, y hay que planificarla y presupuestarla
desde el principio, no dejarla como "ya lo veremos".

Al auditar un tema, **informar siempre de la capa 3 aunque nadie la haya pedido**,
con su coste estimado. Un tema de 1.7.6 en PrestaShop 8 típicamente no tiene
datos estructurados modernos, ni WebP, ni lazy loading: son tres mejoras grandes
que el cliente normalmente no sabe que le faltan.

Dentro de la capa 3, el orden y los porqués están en `references/seo.md`. Resumen:
dimensiones de imagen **antes** que `loading="lazy"`; JSON-LD completo o nada; y
`<picture>` solo si se puede tocar el JS.

⚠️ **Algo que parece capa 3 puede ser capa 2: el contenido invisible.** Cuando el
tema no pinta un campo que el cliente ya ha rellenado, eso no es una mejora
pendiente, es contenido roto. El caso típico es la descripción adicional de
categoría de 8.0 (`seo.md` § 2): el comerciante la escribe, la guarda, y no sale
nunca. Antes de clasificar, comprobar si el campo tiene datos.

## Mapa versión de PrestaShop → versión del tema

Hasta 1.7.8.11 el tema vivía en el repo principal (`themes/classic`, siempre
declarado como `version: 1.0.0`). Desde 8.0 vive en un repo aparte,
[PrestaShop/classic-theme](https://github.com/PrestaShop/classic-theme), y entra
por Composer. **Ojo al nombre**: el repositorio se llama `classic-theme`, pero el
paquete Composer es **`prestashop/classic`**.

Desde 9.0 el paquete incluye además un **segundo tema, Hummingbird**
(`prestashop/hummingbird`), que pasa a ser el tema por defecto **de las
instalaciones nuevas** a partir de 9.1. Ver la sección "Hummingbird" más abajo
antes de sacar conclusiones de esa columna.

| PrestaShop | Tema classic | Hummingbird | Por defecto | Bootstrap (classic) | jQuery |
|---|---|---|---|---|---|
| 1.7.0.x | 1.0.0 | — | classic | 4.0.0-alpha.2 | 2.x |
| 1.7.1 – 1.7.7 | 1.0.0 | — | classic | 4.0.0-alpha.5 | 2.x |
| 1.7.8.x | 1.0.0 | — | classic | 4.0.0-alpha.5 | 3.5.1 |
| 8.0.x | 2.0.6 | — | classic | 4.0.0-alpha.5 | 3.5.1 |
| 8.1.x | 2.1.1 | (aparte, 1.x) | classic | 4.0.0-alpha.5 | 3.5.1 |
| **8.2.0** | **2.1.3** | (aparte, 1.x) | classic | 4.0.0-alpha.5 | 3.5.1 |
| 8.2.1 – 8.2.7 | 2.2.0 | (aparte, 1.x) | classic | 4.0.0-alpha.5 | 3.5.1 |
| 9.0.0 | 3.0.2 | v1.0.0 | classic | 4.0.0-alpha.5 | 3.7.1 |
| 9.0.1 | 3.0.3 | v1.0.1 | classic | 4.0.0-alpha.5 | 3.7.1 |
| 9.0.2 | 3.0.4 | v1.0.1 | classic | 4.0.0-alpha.5 | 3.7.1 |
| 9.0.3 | 3.0.5 | v1.0.1 | classic | 4.0.0-alpha.5 | 3.7.1 |
| 9.1.0 – 9.1.1 | 3.1.1 | **v2.0.0** | **hummingbird** ¹ | 4.0.0-alpha.5 | 3.7.1 |
| 9.1.2 – 9.1.4 | 3.1.2 | **v2.0.0** | **hummingbird** ¹ | 4.0.0-alpha.5 | 3.7.1 |
| 9.2.0-beta.1 | 3.1.2 | v2.1.0-beta.2 | **hummingbird** ¹ | 4.0.0-alpha.5 | 3.7.1 |

¹ **Solo en instalaciones nuevas.** Toda tienda que llegue actualizando desde
8.x o 9.0.x **conserva el tema que tenía**. Es el caso mayoritario y es el que
cubre el resto de este skill.

Versiones resueltas del `composer.lock` de cada tag. Para comprobarlo sin
adivinar:

```bash
curl -sL https://raw.githubusercontent.com/PrestaShop/PrestaShop/<TAG>/composer.lock \
 | jq -r '.packages[] | select(.type=="prestashop-theme") | .name+"="+.version'
```

⚠️ **El tema cambia dentro de la misma minor.** No basta con saber que la tienda
es "9.0" o "8.2": hay que mirar el patch. Cuatro trampas concretas:

- **8.2.0 lleva 2.1.3, no 2.2.0.** Es la única 8.2.x que se queda en la rama
  2.1.x. La política de contraseñas en `password-new.tpl` y el arreglo responsive
  de `contact.tpl` entran en 8.2.**1**.
- **El multi-envío no es exclusivo de 9.1**: llega en el tema 3.0.4, o sea
  PrestaShop **9.0.2**. Ver `breaking-changes.md`.
- **`3.0.6` y `3.1.0` son tags huérfanos**: existen en GitHub pero **nunca se
  distribuyeron en ningún ZIP de PrestaShop**. Si un `theme.yml` declara esas
  versiones, es una instalación manual, no un core estándar.
- **El campo `version:` de `theme.yml` miente.** classic 3.0.3 y 3.0.4 declaran
  ambos `3.0.2`; Hummingbird v1.0.0 declara `0.2.0`. Datar por contenido.

### Estado de las ramas (a 24-07-2026)

- Última estable de 8.x: **8.2.7** (2026-06-04).
- Última estable de 9.x: **9.1.4** (2026-06-04).
- **No existe PrestaShop 9.2 estable.** El único tag 9.2 es `9.2.0-beta.1`
  (2026-07-22); feature freeze el 9-jul-2026. Todo lo que se diga de 9.2 aquí
  sale del beta y **hay que revalidarlo cuando salga la estable**.
- **No existe classic-theme 3.2.x.** Último tag de classic: **3.1.2**
  (2026-05-11). Su `theme.yml` declara `from: 9.0.0`, `to: ~` (sin tope
  superior) en toda la rama 3.x.

### Lo que NO cambia entre 9.1 y 9.2

Sirve para no perder tiempo auditando de más:

| Componente | 9.1.4 | 9.2.0-beta.1 |
|---|---|---|
| PHP (`composer.json`) | `>=8.1` | `>=8.1` |
| Symfony | `~6.4.0` | `~6.4.0` |
| **Smarty** | v4.5.5 | **idéntico** |
| jQuery | 3.7.1 + migrate 3.4.0 | idéntico |
| `framework` de classic | `bootstrap-v4.0.0-alpha.5` | idéntico |
| `{extends}`, `{block}`, `parent:`, `{hook}`, `{widget}` | sin cambios | sin cambios |
| Overrides de módulo (`themes/<tema>/modules/…`) | sin cambios | sin cambios |
| `custom.css` / `custom.js` (prioridad 1000) | sin cambios | sin cambios |
| Herencia padre/hijo (`use_parent_assets`) | sin cambios | sin cambios |

⚠️ **PrestaShop no usa Smarty 5 en ninguna versión publicada.** Verificado en el
`composer.lock`: 8.2.7 → **v4.3.4**, 9.0.0 → **v4.5.5**, 9.1.4 y 9.2.0-beta.1 →
v4.5.5. El salto de sintaxis que obliga a `{else if}` → `{elseif}` es de **9.0**
y ocurre **dentro de Smarty 4** (4.3 → 4.5), no en un cambio de major. Buscar
guías de "migración a Smarty 5" lleva a documentación que no aplica.

**Bootstrap no ha cambiado nunca en classic**: sigue siendo 4.0.0-alpha.5 desde
1.7.1 hasta 9.2. Un tema basado en classic no necesita reescribir su grid ni sus
clases al subir de versión. Es la mejor noticia de toda la migración y conviene
decírselo al usuario pronto, porque el miedo habitual es justo ese.

Desde 9.0 el `theme.yml` declara además `framework: 'bootstrap-v4.0.0-alpha.5'`.

⚠️ **Esto vale para classic, no para Hummingbird.** Hummingbird 2.x es
**Bootstrap 5.3.3**, y ahí sí hay que reescribir el grid, las utilidades y los
`data-*` enteros. Es la diferencia que convierte "migrar a Hummingbird" en un
rediseño y no en una migración. Ver `references/hummingbird.md` § 4.

### ⚠️ Está congelado en una *alpha*, y eso tiene consecuencias

`4.0.0-alpha.5` **no es Bootstrap 4**. Usa nombres de clase que se renombraron
antes de la versión estable y que hoy no existen en ningún Bootstrap moderno.
Verificado en classic 9.1.1:

| Clase en classic (alpha.5) | Equivalente en BS4 estable | Usos en classic 9.1.1 |
|---|---|---|
| `col-xs-12` | `col-12` | 22 ficheros |
| `hidden-sm-down` | `d-none d-md-block` | 18 |
| `card-block` | `card-body` | 18 |
| `float-xs-left` / `float-xs-right` | `float-left` / `float-right` | 22 |

Tres reglas que se derivan de esto:

- **Nunca "actualizar Bootstrap"** en un tema de PrestaShop. Subir a 4.6 o a 5
  rompe la maquetación entera y además desalinea el tema del core y de todos los
  módulos, que siguen emitiendo markup alpha. No es una mejora pendiente: es una
  reescritura del tema.
- **No pegar snippets de Bootstrap moderno.** El HTML copiado de la documentación
  actual o de cualquier tutorial no funcionará. Copiar siempre de classic.
- Si aparece `col-12` o `card-body` en un tema, alguien ha mezclado versiones y
  ahí probablemente ya hay maquetación rota.

Para comprobar la correspondencia en cualquier tag sin tener que adivinar:

```bash
git show <tag>:composer.lock | grep -A2 'classic-theme/tree'
```

## Hummingbird: el tema por defecto desde 9.1 (con matices que importan)

Es la pregunta que llega siempre al hablar de PrestaShop 9, casi siempre mal
planteada. **En su formulación literal —"en PS 9 hay que usar Hummingbird en vez
de classic"— es falsa.**

| Afirmación | Veredicto |
|---|---|
| "En PS 9 **hay que** usar Hummingbird" | **falso como obligación** |
| "En PS 9.0 el tema por defecto es Hummingbird" | **falso** — es classic |
| "En PS 9.1+ el tema por defecto es Hummingbird" | **cierto, solo en instalaciones NUEVAS** |
| "Hay que instalarlo aparte" | **falso** — va en el paquete desde 9.0 |
| "Classic está deprecado" | **cierto pero acotado** — *for new development*, desde 9.1 |
| "Classic dejará de funcionar en PS 9" | **falso / sin evidencia** |
| "Existe guía oficial de migración classic → Hummingbird" | **falso** — la URL da 404 |
| "Migrar classic → Hummingbird es una migración" | **falso — es una reescritura** |

Verbatim de <https://devdocs.prestashop-project.org/9/themes/>:

> "Starting from PrestaShop 9.1, Hummingbird is the default theme."
> "The Classic theme is deprecated for new development starting from PrestaShop
> 9.1. It remains available for backward compatibility but will not receive new
> features."

Y de `/9/modules/core-updates/9.1/`:

> "Existing installations upgrading from 9.0.x keep their current theme.
> Hummingbird is only set as default for fresh installations."

**No hay ningún anuncio de fecha de eliminación de classic.** Sigue empaquetado,
mantenido (3.1.2, mayo 2026) y con `to: ~` en su `theme.yml`.

### La formulación correcta, que es la que hay que trasladar al cliente

> Classic sigue siendo la referencia correcta para **migrar un tema existente**.
> Hummingbird es la referencia correcta para **empezar un tema nuevo**.

### Cuándo SÍ y cuándo NO

**SÍ**: tienda nueva o rediseño ya presupuestado · obligación de accesibilidad
(EAA) · se desarrollan módulos o temas para el Marketplace · tema propio poco
personalizado · PS 9.2 con One Page Checkout.

**NO** (quedarse en classic): el tema es comercial · hay muchos módulos de
terceros de front · el objetivo inmediato es subir de versión sin incidencias ·
la tienda ya está en 9.x y funciona · no hay toolchain Node/SCSS/TS ni quien la
mantenga · el objetivo es 8.x, o 8.x y 9.x a la vez.

### La regla práctica

> Si cambiar de tema obliga a reescribir el CSS, el JS y el marcado —y siempre
> obliga—, no es una migración: es un **rediseño**. Preséntalo y presupuéstalo
> como tal. Si el negocio no quiere pagar un rediseño ahora, **la respuesta
> correcta es quedarse en classic**.

### Tres bulos que hay que desmontar antes de que lleguen al presupuesto

Medidos, no opinados:

- **"Añade JSON-LD, WebP/AVIF y lazy loading que classic no tiene."** Falso.
  Classic tiene los mismos tres `_partials/microdata/*-jsonld.tpl`, y `<picture>`
  con WebP/AVIF y `loading="lazy"` desde 8.1.
- **"Bundle CSS más ligero."** Falso: `theme.css` **345 KB vs 190 KB** (+82 %).
- **"Elimina jQuery."** A medias: del código del tema sí, pero `themes/core.js`
  lo sigue cargando (~140 KB) porque Hummingbird no declara
  `theme_settings.core_scripts: false`.

Lo que **sí** gana de verdad: accesibilidad (`aria-live` 9 vs 0,
`:focus-visible` 33 vs 0…), `srcset`/`sizes` reales, y `fetchpriority="high"` en
la portada de producto **eliminando el `loading="lazy"` que classic pone sobre el
LCP**. De Core Web Vitals **no hay ni un benchmark público riguroso**.

Todo el detalle —tablas de renombrados Bootstrap, capa de compatibilidad,
arquitectura JS, temas hijo, compatibilidad de módulos, coste de migración— en
`references/hummingbird.md`.

## Dónde está el detalle

Consultar el fichero de referencia que corresponda; no hace falta leerlos todos:

- `references/breaking-changes.md` — **capas 1 y 2**. Rupturas versión a versión
  con el antes/después exacto. Resuelve el 90 % de los errores críticos.
- `references/checkout.md` — errores críticos del proceso de compra y el
  checklist de verificación obligatorio. Leer siempre antes de tocar el checkout.
- `references/seo.md` — **capa 3**. Cambios con impacto SEO ordenados por
  importancia (JSON-LD, canonical, Open Graph, Core Web Vitals) y su checklist.
  Leer siempre al auditar, aunque el encargo no mencione SEO.
- `references/images.md` — capa 3. WebP/AVIF, `<picture>`, lazy loading,
  `fetchpriority` y el JS de intercambio de imágenes, que es donde está la trampa.
- `references/timeline.md` — matriz de en qué versión aparece cada plantilla y
  cada feature, y correspondencia exacta tema ↔ PrestaShop a nivel de patch.
- `references/hummingbird.md` — todo lo de Hummingbird: emparejamiento de
  versiones, Bootstrap 4-alpha.5 → 5.3.3, capa de compatibilidad, arquitectura
  JS, temas hijo, módulos, SEO real y criterios de decisión. Leer **antes** de
  aceptar cualquier encargo de "pasar el tema a Hummingbird".

## Cómo reconocer para qué versión está hecha una plantilla

Antes de tocar nada, datar la plantilla. Estos marcadores son inequívocos:

| Si encuentras… | La plantilla es de… |
|---|---|
| `itemscope itemtype="https://schema.org/Product"` en `catalog/product.tpl` | ≤ 1.7.7 |
| `_partials/microdata/product-jsonld.tpl` | ≥ 1.7.8 |
| `$product.canonical_url` en las miniaturas | ≤ 1.7.7 |
| `loading="lazy"` y `js-product-add-to-cart` | ≥ 1.7.8 |
| `id="payment-form"` (genérico) | ≤ 1.7.8.11 |
| `id="payment-{$option.id}-form"` | ≥ 8.0 |
| `data-minlength` / `field-password-policy` | ≥ 8.0 |
| `category-footer.tpl` / `$category.additional_description` | ≥ 8.0 |
| `<picture>` con `sources.webp` / `sources.avif` | ≥ 8.1 |
| `$product_manufacturer->name` (objeto, con flecha) | ≤ 8.2 |
| `$product_manufacturer.name` + `$category.cover` | ≥ 9.0 |
| `{else if}` (con espacio) | ≤ 8.2 — **rompe en 9.0** |
| `$is_multishipment_enabled` | ≥ 9.1 |
| `- ~` en `modules_to_hook` del `theme.yml` | ≥ 9.1 (tema 3.1.0) |
| `{block name='breadcrumb_list'}` / `breadcrumb_items` | ≥ 9.1.2 (tema 3.1.2) |
| `{if !empty($structured_data)}` en `head.tpl` | ≥ 9.2 (JSON-LD del core) |
| `$is_one_page_checkout_enabled` | ≥ 9.2 |
| `.one-page-checkout`, `#opc-form`, `#opc-pay-button` | ≥ 9.2 (`ps_onepagecheckout`) |
| condición `open_box` / `damaged` / `new_with_defects` | ≥ 9.2 |
| `data-ps-component` / `data-ps-action` / `data-ps-target` | **Hummingbird**, no classic |
| `data-bs-toggle` / `visually-hidden` / `btn-close` / `form-select` | Bootstrap 5 → **Hummingbird** |
| `templates/components/` o `_partials/preload.tpl` | **Hummingbird** |
| `catalog/brands.tpl` presente **y** sin `manufacturers.tpl` | **Hummingbird** |

Cruzar siempre con el `theme.yml` del tema (`meta.compatibility.from`), pero
fiarse más del contenido: el `theme.yml` de los temas comerciales suele estar
sin actualizar o mentir directamente.

⚠️ **El campo `version:` del `theme.yml` tampoco es fiable en los temas
oficiales**: classic 3.0.3 y 3.0.4 declaran ambos `3.0.2`, y Hummingbird v1.0.0
declara `0.2.0`. Datar por contenido o por la versión de PrestaShop, nunca por
ese campo.

## Procedimiento de migración

### 0. ¿Migrar a mano o actualizar el tema del proveedor?

Plantearlo **antes** de empezar, porque a veces ahorra el proyecto entero.

Si el tema es comercial (Leotheme, Warehouse, Panda…), lo primero es mirar si el
proveedor ha publicado una versión para la rama destino. Si existe, suele salir
más a cuenta que migrar plantilla a plantilla — y encima queda soportado.

El coste de esa vía está en las personalizaciones: al actualizar el tema se
pierden todos los cambios hechos sobre sus ficheros. Hay que inventariarlos antes
(`git log` sobre la carpeta del tema ayuda si estuvo versionado) y decidir cuáles
merece la pena rehacer.

Regla aproximada: si el tema está muy personalizado, migrar a mano; si está casi
virgen, actualizar. En la duda, comparar el tema instalado con el ZIP original
del proveedor — si apenas difieren, actualizar es lo sensato.

### 1. Establecer la línea base

Obtener el classic de **origen** y el de **destino** para diffear contra ellos.
Para 8.0+ el repo del tema es independiente:

```bash
git clone --filter=blob:none https://github.com/PrestaShop/classic-theme.git
git -C classic-theme archive -o out.tar <tag>   # 2.0.6 | 2.1.1 | 2.2.0 | 3.0.2 | 3.1.1
```

Para 1.7.x, `themes/classic` dentro del repo `PrestaShop/PrestaShop` en el tag
correspondiente.

En Windows/PowerShell, `git archive | tar -x` **corrompe el binario**: hay que
escribir el `.tar` a disco y extraerlo en un segundo paso.

El diff útil no es tema-cliente contra classic-destino (demasiado ruido: el tema
cliente tiene su propio diseño). Es **classic-origen contra classic-destino**:
eso da la lista exacta de cambios que hay que trasladar al tema del cliente.

### 1.bis. Ver cómo se puede tocar el JS y el CSS de este tema

La pregunta útil no es "¿tiene `_dev`?" sino **"¿este cambio hay que añadirlo o
hay que modificar lo que ya existe?"**. Son dos vías muy distintas.

#### Añadir: siempre se puede, sin compilar nada

El core registra estos dos ficheros **en todos los temas**, sin declararlos en
`theme.yml` (verificado en `FrontController.php` de 8.2.7, líneas 979 y 989):

```php
registerStylesheet('theme-custom', '/assets/css/custom.css', ['priority' => 1000]);
registerJavascript('theme-custom', '/assets/js/custom.js',  ['priority' => 1000]);
```

Prioridad 1000 = van los últimos. El CSS gana por orden ante igual
especificidad, y el JS se ejecuta **después** del `theme.js` del tema.

Para casi todo lo de la capa 3 esto basta: `updateSources` para `<picture>`,
handlers extra, ajustes de estilo. **No hace falta `_dev` ni reconstruir nada.**

#### Modificar lo existente: ahí sí hacen falta fuentes

Cambiar una función que ya está dentro del `theme.js` compilado, o tocar
variables SCSS, requiere las fuentes. Y hay que buscarlas donde las tenga *ese*
tema, no donde las tiene classic: los temas comerciales usan sus propias carpetas
(`development/`, `dev/`, `src/`, `sass/`…), y un `_dev` vacío **no significa que
no haya fuentes** — hay que mirar el árbol entero antes de concluir nada.

Si de verdad no hay fuentes, aún queda margen: desde `custom.js` se puede
desactivar un handler del tema (`.off()`) y sustituirlo por otro. Es más frágil,
pero rara vez es un callejón sin salida.

Si hay fuentes, comprobar que **compilan**: los `_dev` de época 1.7.x usan
`node-sass`, que necesita compilación nativa y no funciona en las versiones
actuales de Node. Classic no migró a `sass` (Dart) hasta el tema 2.2.1 y 3.0.x.

#### Lo que sí hay que avisar al cliente

Si el tema es comercial y se editan sus ficheros compilados, esos cambios **se
pierden cuando el proveedor publique una actualización**. Todo lo que se pueda
meter en `custom.js` / `custom.css` sobrevive. Es razón suficiente para preferir
esa vía aunque sea algo más incómoda.

### 2. Inventariar qué sobreescribe el tema

Solo importan las plantillas que el tema realmente sobreescribe. Si el tema es
hijo de classic y no tiene su propio `catalog/_partials/miniatures/product.tpl`,
ese fichero lo hereda ya corregido y no hay nada que hacer.

Revisar también `modules/` dentro del tema: los overrides de plantillas de
módulos (`ps_shoppingcart`, `ps_customersignin`, `ps_contactinfo`…) se olvidan
siempre y son causa habitual de roturas silenciosas tras el upgrade.

### 🔴 Los maquetadores duplican las plantillas del tema

Antes de editar una plantilla, preguntarse **quién la pinta de verdad**. Los
temas con maquetador (ApPageBuilder, Creative Elements, JX Page Builder…) traen
sus propias copias de las miniaturas de producto, y **son esas las que se usan**
en home, listados y bloques. Editar `catalog/_partials/miniatures/product.tpl` no
cambia nada, y el síntoma es desconcertante: subes el cambio, vacías caché, y el
HTML sigue igual.

Peor aún: suelen ser **varias copias** del mismo markup, una por "perfil" o
layout guardado, con nombres opacos (`plist1537113400.tpl`). Hay que parchearlas
todas o el cambio se aplicará en unas páginas sí y en otras no.

Localizarlas siempre por markup, nunca por ruta:

```bash
# coger una clase distintiva del HTML real de la web y buscarla entera
grep -rl "thumbnail product-thumbnail" <tema>/ modules/
```

Y confirmar contra el HTML de producción: si el markup servido no coincide
exactamente con la plantilla que ibas a editar, es que la pinta otra.

### 3. Aplicar por capas

Bloqueantes → errores críticos → SEO/rendimiento, según
`references/breaking-changes.md` y `references/seo.md`. Un commit por capa como
mínimo, para poder revertir una sin perder las otras.

Las capas 1 y 2 suelen ser **pocos ficheros**: en un tema real de 1.7.6 sobre
PrestaShop 8.2, dos o tres. La capa 3 es la que tiene volumen. Si el listado de
"cosas a arreglar" tiene 90 entradas, casi seguro se ha colado la capa 4.

## Qué no tocar

El error más caro de una migración es perseguir paridad con classic. Un tema
comercial tiene diseño propio: la mayoría del diff contra classic es cabecera de
licencia y cambios cosméticos que **no aplican**. Descartar de entrada:

- **Añadir clases `js-*` a un tema legacy que funciona.** El core declara los
  selectores duales (`.product-actions, .js-product-actions`) con ámbito `.row`,
  así que el marcado antiguo sigue resolviendo. Verificado en 8.2.7. Tocar 150
  plantillas para esto es trabajo sin resultado. Ver `breaking-changes.md` § 1.7.8.
- **Reescribir el grid.** Bootstrap no ha cambiado desde 1.7.1.
- **Reordenar markup o renombrar clases** para parecerse a classic.
- **Cambios de PS 9** (presenters, sintaxis de Smarty, multi-envío) en una tienda
  que se queda en 8.x. Única excepción: `{else if}` → `{elseif}`, que es gratis,
  funciona igual en Smarty 3/4 y adelanta trabajo. Hacerlo siempre.
- **Pasar el tema a Hummingbird "ya que estamos" en un upgrade de versión.** Son
  dos proyectos distintos y sumarlos multiplica el riesgo. Subir de versión
  manteniendo classic, estabilizar, y evaluar el tema aparte. Ver
  `references/hummingbird.md` § 12.
- **Actualizar Bootstrap en un tema hijo de classic para "acercarlo" a
  Hummingbird.** No hay camino intermedio: o el tema es alpha.5 o es 5.3.3.
  Mezclar deja el tema desalineado del core y de todos los módulos a la vez.
- **Limpiar carpetas muertas** (`_partials_old` y similares). Riesgo sin ganancia.
- **Los datos estructurados que ya funcionan.** Si el tema emite microdatos
  válidos, no se migran a JSON-LD: Google soporta ambas sintaxis. Solo se **añade
  lo que falte**, cuidando de no describir la misma entidad dos veces. Ver
  `seo.md` § 1.
- **Los emails del tema.** Si el tema trae `mails/<iso>/*.html`, se quedan como
  están. Verificado en 8.2.7: `Mail::getTemplateBasePath()` sigue dando prioridad
  a `themes/<tema>/mails/` sobre el core, y entre 1.7.6 y 8.2.7 **no se añadió ni
  se eliminó ninguna plantilla de correo** (51 en ambas). Que el tema solo
  sobreescriba algunas y el resto caigan al core es normal y funciona.

Regla práctica: si un cambio no arregla algo roto ni mejora SEO/rendimiento,
**no se hace**. Y si el cliente lo pide igualmente, va en un commit aparte.

### 4. Verificar

El checklist completo está en `references/checkout.md`. Como mínimo, y sin
excepciones, **hacer un pedido real de principio a fin** en el entorno migrado,
con y sin cliente registrado.

## Formato del informe de auditoría

Al auditar un tema, entregar siempre estas cinco secciones, en este orden:

1. **Datación** — de qué versión es el tema, con los marcadores que lo prueban.
2. **Lo que NO está roto** — antes que los problemas. Evita alarmar de más y
   suele ser la mayor parte. Aquí van Bootstrap, los selectores duales del core y
   lo que el tema ya tenga correcto.
3. **Errores críticos** — capas 1 y 2, con `fichero:línea` y el impacto concreto
   en negocio ("el bloque de registro no se muestra nunca"), no en abstracto.
4. **SEO y rendimiento** — capa 3, con lo que falta y lo que cuesta. **Nunca
   omitir esta sección**, aunque el encargo fuera solo "arréglame esto".
5. **Qué no tocaría** — explícito, con el porqué. Es lo que protege el
   presupuesto y evita que la migración se convierta en una reescritura.

Cada punto debe decir si está **verificado** o si hace falta probarlo en la
tienda. Muchas cosas no se pueden determinar leyendo plantillas.

**Si la tienda es (o va a ser) 9.1+, añadir una sexta sección: `classic o
Hummingbird`.** Una recomendación explícita, con el porqué, aunque nadie haya
preguntado — porque si no lo planteas tú lo planteará un competidor, y casi
siempre mal. En la mayoría de casos la recomendación correcta es **quedarse en
classic** y decirlo sin rodeos, pero hay que argumentarlo, no omitirlo. Criterios
en `references/hummingbird.md` § 12.

## Notas de trabajo

- **No inventar variables.** Si no consta que una variable exista en la versión
  destino, comprobarlo en el classic de esa versión antes de usarla. Las
  variables de plantilla de PrestaShop no están documentadas de forma fiable y
  el presenter cambia entre versiones sin previo aviso.
- **Blindar los accesos nuevos.** Al añadir algo que solo existe en la versión
  destino, envolverlo en `{if isset($x)}` o `{if !empty($x)}` si el tema debe
  seguir funcionando en versiones anteriores. Es lo que hace el propio classic
  con `$is_multishipment_enabled` en 9.1.
- **Los `{block}` son API pública.** Renombrar o eliminar un `{block name='…'}`
  rompe los temas hijos y algunos módulos que extienden bloques. Añadir sí,
  quitar no.
- **Las clases `js-*` son contrato con el JavaScript del tema**, no decoración.
  Quitar una `js-product-add-to-cart` o una `js-thumb` rompe la actualización
  dinámica de la ficha de producto sin dar ningún error visible. Ver
  `references/breaking-changes.md` § 1.7.8.
- **Vaciar caché de Smarty** tras cada tanda de cambios, y comprobar con
  `PS_DEBUG_MODE` activado para que los errores de plantilla se vean.
