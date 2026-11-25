---
name: prestashop-tema-hummingbird
description: Crear un tema hijo de Hummingbird para PrestaShop 9.1 / 9.2 y los modulos que lo acompanan. Activacion del tema (por que falla prestashop:theme:enable y como se hace), las capas CSS de Hummingbird, lo que el JavaScript del nucleo repinta en la ficha y en las tarjetas de listado, el ZIP con dependencies, las cachees que tapan un despliegue y como probarlo. Medido montando temas hijo completos sobre 9.1.5 y 9.2.0. Invocar al montar o depurar un tema hijo de Hummingbird, o un modulo que pinte en su portada, su pie o sus tarjetas de producto.
---

# Temas hijo de Hummingbird (9.1 / 9.2) y sus módulos

Medido montando temas hijo completos —portada, listados, ficha— sobre **9.1.5** (Hummingbird
2.0.0) y **9.2.0** (2.1.2). Casi nada de esto está en la documentación: sale de que la
pantalla no salía, o salía y se rompía al cambiar de combinación.

Lo que cambia entre 9.1 y 9.2 está en `prestashop-9-2`.


Medido montando temas hijo completos (portada, listados, ficha) sobre 9.1.5 y 9.2.0.

## Instalación y activación

* **El instalador oficial de 9.2 renombra la carpeta `admin` al azar.** Si se le cambia el
  nombre después, el contenedor de Symfony sigue apuntando a la vieja: hay que borrar
  `var/cache` **con el servidor parado**.
* **`prestashop:theme:enable` falla en 9.x** («Cannot build Language context»). Se activa desde
  PHP: arrancar `AdminKernel`, pedir
  `PrestaShop\PrestaShop\Core\Context\ContextBuilderPreparer` →
  `prepareLanguageId((int) Configuration::get('PS_LANG_DEFAULT'))`, poner un `Employee` en el
  contexto y llamar al gestor de temas.
* **Activar un tema por consola deja el contenedor desfasado**: otros módulos del back-office
  dan 500 en sus rutas hasta que se vacía `var/cache` con el servidor parado.
* **Al cambiar de tema, PrestaShop desengancha módulos** que el tema nuevo no declara (por
  ejemplo `blockwishlist` de `displayFooter`): todo lo que tenga que quedar enganchado va en
  `global_settings.hooks.modules_to_hook` del `theme.yml`.

## El tema hijo

* `parent: hummingbird` + `assets: use_parent_assets: true`. `assets/css/custom.css` y
  `assets/js/custom.js` los carga el núcleo como `theme-custom` con prioridad 1000.
* `compatibility: from: 9.1.0 / to: ~9.2.0` funciona: 9.1.5 trae Hummingbird 2.0.0 y 9.2.0 la
  2.1.2. Diferencia encontrada: en la 2.0.0 la miniatura activa de la galería no se marca al
  deslizar; se sincroniza desde el JS del hijo con el evento `slid.bs.carousel`.
* **Hummingbird usa `@layer`.** Las reglas del hijo (sin capa) ganan a las normales del padre,
  pero **un `!important` sin capa pierde contra las utilidades `!important` de la capa
  `utilities`** de Bootstrap. Donde el padre pone utilidades (`py-4`,
  `justify-content-center`…), se sobrescribe la plantilla, no se pelea con CSS.
* `:has()` sirve para cosas como una cabecera transparente solo en la portada con imagen
  grande: `body#index:has(.hero):not(.scrolled) #header { … }`.
* **Ficha de producto**: todo lo que `core.js` repinta al cambiar de combinación tiene que
  seguir dentro de `.js-product-container` con su clase: `.js-product-prices`,
  `.js-product-add-to-cart`, `.js-product-details` (si no se enseña, se deja oculto: `core.js`
  lee su `data-product`), `.js-images-container`, `.js-product-variants`,
  `.js-product-additional-info`. `#quantity_wanted` puede ser un `hidden` con `min`.
* **Miniaturas de listado**: `blockwishlist` mete su corazón en `.thumbnail-container` dentro de
  `.js-product-miniature`. Sin esa clase su JS revienta y, con el JS combinado (CCC), **corta
  todo el JS del tema que va detrás**.
* **Datos extra en las tarjetas**: `actionPresentProductListing` con
  `$params['presentedProduct']->appendArray([...])`. Los productos que un módulo presenta él
  mismo (un carrusel dentro de `displayHome`) no pasan por ese gancho: hay que añadírselo a mano.
* **Traducción oficial es-ES de 9.2.0 rota**: `Subcategories for %s` → `Subcategorías de %s%`.
  En PHP 8 `vsprintf` lanza `ValueError` y **toda categoría con subcategorías da un 500 en
  blanco** (también con Hummingbird sin tocar). Se corrige desde el tema con
  `translations/es-ES/ShopThemeCatalog.es-ES.xlf` con la cadena buena: el catálogo del tema se
  carga después del núcleo y la pisa.
* **Cachés que tapan un despliegue**: CCC, Smarty sin recompilar y catálogos de traducción. Tras
  copiar ficheros: `var/cache/*/smarty`, `var/cache/*/translations` y
  `themes/<tema>/assets/cache`.

## El ZIP del tema

* `dependencies/modules/<modulo>/` dentro del ZIP: el gestor de temas los copia a `modules/` al
  importar y los instala al activar (con `global_settings.modules.to_enable`). El `index.php`
  de `dependencies/modules/` **no** sustituye al de `modules/`.
* `ThemeManager::install()` falla si la carpeta del tema ya existe: para probar la importación
  de verdad, apartar antes el tema y sus módulos.

## Módulos que acompañan al tema

* **Ficha V2, pestaña propia**: hijo de la raíz en `actionProductFormBuilderModifier`, guardado
  en `actionAfterUpdateProductFormHandler` con `form_data['<pestaña>']`. **Nunca**
  `'mapped' => false`.
* **`Configuration::updateValue($k, $v, true)` pasa por `purifyHTML()`** y guarda «&» como
  «&amp;»: la tienda lo enseña tal cual. `true` solo para HTML de verdad. Con `false` **no** se
  pierden los saltos de línea: `Db::escape()` escapa antes del `nl2br` + `strip_tags`.
* **Las clases de `classes/` de otro módulo no están cargadas** fuera de sus pantallas:
  `require_once` en el constructor si `!class_exists($c, false)`. Con solo `class_exists()` la
  función se salta en silencio.
* **Subidas de imagen propias**: `ImageManager::isRealImage($tmp, null, [mimes])` + extensión
  permitida + tamaño; carpeta pública bajo `_PS_IMG_DIR_` con `index.php` y un `.htaccess` que
  no deja ejecutar nada; en la configuración solo el nombre del fichero.
* **Menú principal** (`ps_mainmenu`): `MOD_BLOCKTOPMENU_ITEMS` con `CAT<n>`, `CMS<n>`, `PRD<n>`,
  `LNK<n>`; su caché vive en `_PS_CACHE_DIR_ . 'ps_mainmenu'` y hay que borrarla al cambiarlo.
* **Lista de enlaces** (`ps_linklist`): el contenido de cada bloque es un JSON con las claves
  `cms`, `product`, `static` y `category`; los enlaces legales de debajo del pie son un bloque en
  `displayFooterAfter`.
* **Constructores visuales** (Creative Elements, Crazy Elements, iqitelementor…): se detectan por
  el nombre del módulo, si está activo (`active` + `Module::isEnabled`), en qué ganchos de
  portada/pie está y sus tablas (`ce\_%`, `crazy%`, `iqit\_elementor%`). Si hay uno activo, la
  portada y el pie son suyos: no se tocan.
* La URL legacy `index.php?controller=AdminModules&configure=<modulo>&token=…` sigue valiendo
  en 9.x (redirige a su pantalla).

## Probarlo

* **El primer acceso al back-office tras vaciar la caché reconstruye el contenedor**: puede
  tardar minutos. Calentar con una petición antes de la prueba y subir el tiempo de espera.
* Los interruptores del HelperForm en 9.x se pintan como `ps-switch`: su `<label for>` no se
  puede pulsar; en una prueba se marca el `radio` directamente.
* El autocompletado del buscador (`ps_searchbar`) puede tardar varios segundos con la máquina
  cargada: esperar al resultado, no un tiempo fijo.
* La prueba de guardado de un formulario lleva siempre un texto con «&» y relee la base.
