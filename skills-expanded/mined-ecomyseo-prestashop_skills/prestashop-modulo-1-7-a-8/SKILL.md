---
name: prestashop-modulo-1-7-a-8
description: Llevar un modulo de PrestaShop 1.7.x a 8.x. Lo que de verdad rompe no es PrestaShop sino el salto de PHP 7.4 a 8.1 que viene con el; mas las 8 clases y los 68 metodos publicos que 8.x quita, las 10 firmas que cambian (dos de ellas quitando parametros de EN MEDIO, que es lo que no avisa), las 5 constantes que dejan de definirse y los 218 hooks que llegan. Medido comparando los nucleos 1.7.8.11 y 8.2.8 en disco y actualizando tiendas reales. Invocar al adaptar, auditar o depurar un modulo escrito para 1.7.x que tiene que funcionar en 8.x, o cuando una tienda recien subida a 8.2 enseñe un 500 con el cuerpo vacio. De 8.x a 9.x esta prestashop-modulo-8-a-9.
---

# De un módulo de PrestaShop 1.7.x a 8.x

Medido comparando los núcleos **1.7.8.11 y 8.2.8** extraídos en disco, y actualizando
tiendas reales de 1.7.8 a 8.2 con sus doscientos y pico módulos encima.

La conclusión, antes de nada, porque cambia por dónde se empieza a mirar:

> **PrestaShop 8 apenas rompe nada. Lo que rompe es el PHP que viene con él.**

1.7.8 no pasa de **PHP 7.4**; 8.2 corre en **8.1**. El salto de versión de la tienda
arrastra un salto de versión del lenguaje, y ahí es donde está casi todo el daño. Un
módulo que lleva años funcionando puede caerse sin que nadie haya tocado una sola API de
PrestaShop.

Lo que cambia de 9.1 a 9.2 está en `prestashop-9-2`; de 8.x a 9.x, en
`prestashop-modulo-8-a-9`, donde **sí** desaparecen cosas a lo grande.

---

## 1. Lo primero: el salto es de PHP, no de PrestaShop

| | 1.7.8.11 | 8.2.8 |
|---|---|---|
| PHP que admite | 7.1.3 – **7.4** | 7.2.5 – 8.1+ |
| Clases del núcleo que desaparecen | — | **8** |
| Métodos públicos que desaparecen | — | **68** |
| Firmas que cambian | — | **10** (2 peligrosas) |
| Constantes que dejan de definirse | — | **5** |
| Hooks | 678 | **896** (llegan 218, **no se va ninguno**) |

Con esos números delante, el orden de trabajo es: **primero PHP 8, después la API**.

### Lo que PHP 8 se lleva por delante, y dónde está siempre

En una tienda real, `php -l` con 8.1 sobre **5.179 ficheros de módulos** encontró **16 con
error de sintaxis**, y uno estaba **en la pasarela de pago**. El patrón se repite:

> **Los módulos de transportista y de pago empaquetan librerías viejas** — TCPDF,
> implementaciones propias de SHA256, clientes XML-RPC — y ahí es donde vive la sintaxis
> muerta. No en el código del módulo: en su carpeta `lib/`.

| Qué | Por qué revienta | Cómo se escribe ahora |
|---|---|---|
| `$cadena{$i}` | Acceso a carácter con llaves: **retirado en PHP 8.0**. Un solo fichero de TCPDF traía **72** | `$cadena[$i]` |
| `$x =& new Foo()` | Asignación por referencia de un `new`: sintaxis de PHP 4, fatal | `$x = new Foo()` |
| `function x($a) { ... }` redeclarada | Antes aviso, ahora fatal | — |
| Argumentos que llegan `null` a un parámetro tipado | En 7.4 se convertía; en 8 es `TypeError` | comprobar antes, o tipo anulable |

Y los tres que **`php -l` no ve**, porque la sintaxis es perfecta:

* **Un método NO estático llamado como estático.** En PHP 5 y 7 era un aviso y la tienda
  seguía; **en PHP 8 es un `Error` fatal**. Es capaz de tumbar el front entero.
* **Estrechar la visibilidad de un método o propiedad heredados** (`protected function
  hydrate()` sobre un `public` del núcleo): error **al enlazar la clase**, no de sintaxis.
* **Una firma de override incompatible** con la del padre: igual, fatal al enlazar.

Los tres se ven **al cargar la clase**, así que una prueba que solo instale el módulo sale
en verde y la pantalla revienta después.

### `(array) $x` no es «un array o vacío»

`(array) false` es `array(0 => false)`, no un array vacío. El `foreach` entra una vez con
`false` dentro y, al leer la primera clave, PHP 8 avisa «Trying to access array offset on
value of type bool» y la petición muere con un **500**. Y devuelven `false` cuando no hay
nada, entre otras: `Db::executeS()`, `Product::searchByName()`, `Customer::getAddresses()`,
`glob()`, `json_decode()` con basura y `file()`.

```php
$filas = Db::getInstance()->executeS($sql);
foreach (is_array($filas) ? $filas : array() as $fila) { … }
```

**En una llamada AJAX ese 500 no se ve**: el JavaScript se lo traga, la lista se queda
vacía y la pantalla parece que funciona.

### `php -l` con **7.4**, no solo con la última

Si el módulo dice soportar 7.4 —y casi todos los de una 1.7.8 lo dicen—, hay que lintarlo
también con 7.4. Un `array_unshift((array) $x, ...)` es un **fatal de compilación** en 7.4
(«Only variables can be passed by reference») que impide activar el módulo, y en PHP 8 no
da error ninguno: simplemente no hace nada.

---

## 2. Lo que 8.x sí quitó

### Ocho clases desaparecen enteras

| Se va | Qué hacer |
|---|---|
| **`Attribute`** | Es la gorda: pasa a llamarse **`ProductAttribute`**. Cualquier `new Attribute(...)` o `Attribute::` de un módulo de combinaciones deja de existir |
| `Referrer` | Los afiliados salen del núcleo |
| `Windows` | — |
| `PhpEncryptionLegacyEngine` | Cifrado antiguo |
| `AdminAttributeGeneratorController`, `AdminPatternsController`, `AdminReferrersController`, `AdminSearchEnginesController` | Pantallas del back-office retiradas |

### Sesenta y ocho métodos públicos, de clases que siguen existiendo

Los que más aparecen en código de módulos:

| Se va | Recambio |
|---|---|
| `Tools::jsonEncode()` / `Tools::jsonDecode()` | `json_encode()` / `json_decode()` de PHP |
| `Tools::array_replace()` | `array_replace()` de PHP |
| `Tools::display404Error()` | el controlador decide el 404 |
| `Tools::getSafeModeStatus()`, `Tools::addonsRequest()`, `Tools::getCldr()` | — |
| **`Cart::getOrderShippingCost()`** | `getPackageShippingCost()` |
| `Cart::getTaxesAverageUsed()`, `Cart::addExtraCarriers()`, `Cart::checkDiscountValidity()` | — |
| **`Product::updateQuantity()`** | `StockAvailable::updateQuantity()` |
| `Product::getAttributeCombinaisons()` y toda la familia `*Combinaison*` | las versiones sin la grafía francesa |
| `Product::reinjectQuantities()`, `Product::getAttributesImpacts()` | — |
| **`Configuration::getInt()`** | **ojo: no devolvía un entero**, devolvía un array por idioma. Ver la trampa de abajo |
| `Cookie::isLogged()` / `isLoggedBack()` | `Context::getContext()->employee->isLoggedBack()` y equivalentes |
| `Validate::isPasswd()` | la validación del núcleo nuevo |
| `Hook::getRetroHookName()`, `Hook::getHookAliasList()` | los alias de hook de 1.6 se acabaron |
| `Media::getJqueryPath()` | — |
| `FrontController::addMedia()` / `removeMedia()` | `registerStylesheet()` / `registerJavascript()` |
| `Helper::renderModulesList()`, `AdminController::renderModulesList()` | — |
| `Shop::getTheme()` | `Context::getContext()->shop->theme->getName()` |
| `TaxRulesGroup::getTaxes()` / `getTaxesRate()`, `Tax::getProductTaxRateViaRules()` | — |
| `OrderPayment::getByOrderId()`, `OrderHistory::getLastOrderState()`, `OrderSlip::createOrderSlip()` | — |

**`Tools::displayPrice()` TODAVÍA EXISTE en 8.2.** Se va en 9.x. No hay que tocarlo en este
salto — y cambiarlo «de paso» es meter un riesgo que nadie ha pedido.

### Cinco constantes dejan de definirse

`_PS_HOST_MODE_` · `_PS_PEAR_XML_PARSER_PATH_` · `_PS_SWIFT_DIR_` · `_PS_TAASC_PATH_` ·
**`_PS_TCPDF_PATH_`**

La que pilla a más módulos es **`_PS_TCPDF_PATH_`**: cualquiera que generase PDF usando el
TCPDF del núcleo se queda sin ruta. Y un `if (!defined('X')) exit;` usando una constante
retirada **hace que el módulo salga al cargarse** y la página se quede en blanco, sin un
solo error.

---

## 3. Diez firmas cambian, y **dos** son las peligrosas

Ocho **añaden** parámetros al final: las llamadas de siempre siguen valiendo, y lo único
que rompe es un override con la firma vieja (fatal al enlazar la clase).

Las **dos que quitan parámetros de EN MEDIO** son otra cosa, porque **las llamadas siguen
siendo sintácticamente válidas y los argumentos se corren de sitio**:

```php
// 1.7.8    Tools::displayDate($date, $id_lang = null, $full = false, $separator = null)
// 8.2.8    Tools::displayDate($date, $full = false)

Tools::displayDate($fecha, $id_lang, true);   // el IDIOMA cae en $full
```

y en PHP 8 eso es `TypeError: Argument #2 ($full) must be of type bool, null given`. La
pantalla devuelve **HTTP 500 con el cuerpo vacío**, `php -l` pasa limpio y no lo ve ni el
detector de métodos retirados (el método sigue existiendo) ni el de firmas de override
(nadie lo declara). Medido: **110 llamadas** repartidas por las tiendas de una tanda, 106
de ellas a `displayDate`.

La otra es `Module::getModulesOnDisk($use_config, ~~$logged_on_addons~~, $id_employee)`.

| Método | 1.7.8.11 | 8.2.8 |
|---|---|---|
| **`Tools::displayDate`** | `$date, $id_lang, $full, $separator` | `$date, $full` |
| **`Module::getModulesOnDisk`** | `$use_config, $logged_on_addons, $id_employee` | `$use_config, $id_employee` |
| `Hook::unregisterHook` | `$hook_name` | `$hook_identifier` (solo el nombre) |
| `ImageManager::resize` | `$fileType` | `$destinationFileType` (solo el nombre) |
| `Customer::searchByName` | | `+ ?ShopConstraint $shopConstraint` |
| `Mail::sendMailTest` | | `+ 4 de DKIM` |
| `OrderInvoice::getInvoiceByNumber` | `$id_invoice` | `$invoiceNumber, $orderId = null` |
| `OrderReturn::getOrdersReturn` | | `+ int $idOrderReturn` |
| `Pack::deleteItems` | | `+ $refreshCache = true` |
| `Product::getPriceFromOrder` | | `+ int $customizationId` |

**A PHP le da igual cómo se llame un parámetro**: `$fileType` → `$destinationFileType` no
rompe nada por sí solo, pero sí rompe un **override** que copió la firma vieja… y al
comparar firmas hay que hacerlo **por cuántos parámetros son, no por el nombre**, o no se
encuentra ni uno.

---

## 4. Llegan 218 hooks y no se va ninguno

Nada que migrar: lo que el módulo enganchaba sigue existiendo. Lo que sí hay es sitio nuevo
donde engancharse, sobre todo las familias `actionAfterCreate*FormHandler` /
`actionAfterUpdate*FormHandler` (los formularios Symfony del back-office) y
`actionAdminMenuTabsModifier`.

Dos de los que llegan conviene conocerlos porque resuelven cosas que en 1.7 se hacían con
un override:

* **`actionAfterLoadRoutes`** — tocar las rutas sin tocar el núcleo.
* **`actionAdminMenuTabsModifier`** — reescribir el menú del back-office. Y por lo mismo:
  si después de actualizar **falta una sección entera del menú** y `ps_tab` está perfecta,
  el culpable es un módulo enganchado ahí.

---

## 5. Las trampas que solo se ven en ejecución

### El prefijo duplicado: una bomba con años de retraso

Todo el front de una tienda recién actualizada, caído con:

```
Fatal error: Uncaught PDOException: SQLSTATE[42S02]:
Table 'x.psxx_psxx_mimodulo_map' doesn't exist
```

Fíjate en el prefijo **repetido**. El módulo hacía:

```php
$tabla = _DB_PREFIX_ . 'mimodulo_map';
$db->insert($tabla, [...]);          // insert() AÑADE el prefijo otra vez
```

**No lo rompió la actualización.** El fallo solo salta cuando toca **insertar**, y antes
estaba todo cacheado. Al actualizar cambian las URL, se vacía la caché, se intenta la
primera inserción y revienta. Merece la pena pasarle el patrón a todos los módulos:

```bash
grep -rn -E "\->(insert|update|delete)\(\s*(_DB_PREFIX_\s*\.|\$\w*[Tt]abl\w*)" modules/
```

y **mirar cada coincidencia una por una**: los que usan el QueryBuilder de Doctrine pasan el
nombre completo a propósito y están bien.

### `Configuration::getInt()` nunca devolvió un entero

Llamaba a `getConfigInMultipleLangs()` y devolvía **un array por idioma**. Quien lo usara
creyendo que daba un número llevaba años con un bug latente; al quitarse el método, se nota.
**Regla general: un recambio que el núcleo sugiere no es un recambio equivalente hasta
comparar los dos cuerpos.**

### Un `include_once` sobre un `.sql`

```php
include_once dirname(__FILE__) . '/sql/install.sql';
```

**Imprime** el fichero, no lo ejecuta: la tabla no se crea nunca. No es de 8.x —rompe en
cualquier versión— pero es de lo que más aparece al revisar módulos viejos de golpe.

### Tablas creadas al abrir la configuración

Si las tablas se crean en `getContent()` y no en `install()`, cualquier otra pestaña abierta
antes da un 500. Se crean en `install()`.

---

## 6. Cómo auditar un módulo (o doscientos) sin ahogarse

Por orden, que importa:

1. **`php -l` con 8.1** sobre todo el árbol del módulo, **`lib/` y `vendor/` incluidos** —
   que es donde está la sintaxis muerta. Y también con **7.4** si el módulo dice soportarlo.
2. **Índice del núcleo de destino** (`classes/` y `controllers/`) con la **cadena de
   herencia resuelta**: un método heredado del padre **no** es un método retirado. Sin
   seguir la herencia, la mitad de los hallazgos son falsos. Al subir por la cadena hay que
   probar el nombre del padre **y** `<padre>Core` en cada nivel.
3. **Todo hallazgo se confirma contra el código del núcleo nuevo.** Lo que existe, se
   descarta.
4. **Llamadas estáticas a métodos que no lo son**, y al revés. Es fatal en PHP 8 y no lo ve
   ningún linter.
5. **Constantes**: los `define()` del núcleo viejo que el nuevo no tiene, descartando las
   que el propio módulo define.
6. **Firmas**: comparar **por número de parámetros**, nunca por nombre.
7. **Llamadas con la firma vieja** de un método que sigue existiendo (el caso
   `displayDate`): hay que buscarlas aparte, porque no caen en ninguna de las anteriores.

**Reescribir con el tokenizador de PHP, nunca con expresiones regulares.** Y al contar
argumentos de una llamada hay que enmascarar antes comentarios, cadenas y heredocs: una coma
dentro de una cadena inventa un argumento y «arreglar» eso es destrozar el código de un
cliente con una cuenta mal hecha.

---

## 7. Verificar: lo que una prueba ingenua da por bueno

* **Instalar no es probar.** Los fallos de PHP 8 que más duelen saltan **al cargar la
  clase** o al abrir una pantalla, no al instalar. Hay que abrir la configuración **y todas
  sus pestañas**, con `_PS_MODE_DEV_` activo (convierte los avisos en 500, que es lo que
  interesa ver).
* **Mirar DÓNDE acaba la petición, no sólo el código.** Un módulo que redirige deja un
  302 → 200 y la prueba anota «200» sin haber abierto nada. Solo cuenta si la URL final es
  la pedida.
* **Un 500 con el cuerpo vacío es la firma del `TypeError`.** No hay nada en pantalla y a
  veces nada en el registro del módulo: el fatal está en el `php_error_log` o en el registro
  del servidor.
* **Y en AJAX no se ve ni eso**: hay que mirar el **cuerpo de las respuestas 5xx**, no sólo
  la consola del navegador.
* **El front, con el tema del cliente.** Un tema de 1.7.8 suele arrastrar marcado de 1.6
  (`.product_list`, `a.product_img_link`) en vez del de Classic (`.product-miniature`): una
  prueba automática que busque los selectores modernos no encuentra nada y se queda sin
  ficha, sin carrito y sin checkout, dando por bueno que «no hay errores».

---

## 8. Y lo que pasa alrededor, que no es del módulo pero lo parece

* **Al actualizar, todos los módulos no nativos quedan apagados** (es lo que hace
  `--disable-non-native-modules=1`). Si no se vuelven a encender, el front sale sin tema y
  parece que la actualización ha roto la tienda. Hay que tener el inventario de **antes**
  para saber cuáles había que reencender.
* **El núcleo de una tienda vieja viene modificado**, siempre. Parches escritos deprisa que
  la actualización se lleva por delante: hay que compararlo con el núcleo original de su
  versión —**normalizando los fines de línea**, o un CRLF/LF da cientos de líneas de
  diferencia falsas— y volver a aplicar después lo que valga la pena.
* **Módulos duplicados con sufijo** (`mimodulo1`, `mimodulo_2`, `algo_1`) y carpetas de
  módulos nunca instalados con código roto dentro: ocupan, se analizan y ensucian cualquier
  auditoría. Se apartan antes de empezar.
* **Un módulo cifrado con ionCube para otra versión de PHP**, sólo con estar en `modules/`,
  **tumba la instalación de otros módulos**. Se aparta de la carpeta antes de probar.

---

## 9. De 1.7.x a 9.x de una vez: no se puede

Y no es una manía, es una cuenta. `autoupgrade` **arranca la tienda con el núcleo VIEJO**
para migrar la base, mientras los requisitos exigen el PHP del **NUEVO**. Hace falta un PHP
que valga para los dos:

```
1.7.8.11  admite PHP 7.1.3 – 7.4.99
9.2.0     exige  PHP 8.1   – 8.5.99        -> no se solapan
```

Con PHP 7.4 los requisitos rechazan el destino 9.x; con PHP 8.1 el `vendor/doctrine` que
trae 1.7.8 no compila y la tienda no llega a arrancar. **Hay que pasar por 8.2**, que sube
desde 7.4 y desde ahí ya se puede ir a 9.1 o directo a 9.2.
