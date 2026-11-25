---
name: prestashop-modulo-8-a-9
description: Llevar un modulo de PrestaShop 8.x a 9.x. Los metodos, las constantes y las librerias de vendor que 9 quito, las trampas de los recambios que el propio nucleo sugiere, las tres cosas del nucleo que cortan la instalacion sin avisar, como auditar muchos modulos sin ahogarse en falsos positivos y como verificarlo en una 9.2 de verdad. Medido comparando 8.2.8 con 9.2.0 sobre una auditoria de 91 modulos. Invocar al adaptar, auditar o depurar un modulo escrito para 8.x que tiene que funcionar en 9.x. Lo que cambia de 9.1 a 9.2 esta en prestashop-9-2.
---

# De un módulo de PrestaShop 8.x a 9.x

Lo que 9.x **sí quitó**, y cómo saberlo sin ahogarse en falsos positivos.

Medido comparando los núcleos **8.2.8 y 9.2.0** extraídos en disco, sobre una auditoría de
**91 módulos** propios: **1 de cada 3 no pasaba**, y casi siempre por lo mismo. Un módulo
escrito para 8.x salta una versión mayor, y ahí sí desaparecen cosas — al contrario que de
9.1 a 9.2, donde no desaparece ninguna (eso está en `prestashop-9-2`).

Lo que se comprueba aquí vale para cualquier 9.x; donde se mide contra una versión concreta,
se dice cuál.

## 1. Lo que 9.x quitó, y por qué el módulo revienta al abrir la pantalla y no al instalar

### Métodos que ya no existen

| en 8.x | en 9.x | se escribe |
|---|---|---|
| `Tools::displayPrice()` | no existe | `Context::getContext()->getCurrentLocale()->formatPrice($precio, $iso)` |
| `Tools::link_rewrite()` | no existe | `Tools::str2url()` |
| `Tools::displayNumber()` | no existe | `->getCurrentLocale()->formatNumber()` |
| `Tools::getBrightness()` | no existe | `(new ColorBrightnessCalculator())->isBright()` (de instancia, no estático) |
| `Tools::generateIndex()` | no existe | `PrestashopAutoload::getInstance()->generateIndex()` |
| `Tools::stripslashes()` | no existe | **la cadena tal cual** (ver la trampa de abajo) |
| `Tools::cleanNonUnicodeSupport()` | no existe | el patrón tal cual (en 8.x ya no hacía nada) |
| `$this->l()` en `AdminController` / `ModuleAdminController` | no existe | `$this->module->l(...)` o `$this->trans(...)` |
| `$this->ajaxDie()` (en `Controller`) | no existe | `$this->ajaxRender($x); exit;` |
| `$this->addJquery()` (en `Controller`) | no existe | quitarlo en el back-office, donde jQuery ya va cargado |

Los tres de los controladores rompen **al abrir la pantalla**, no al instalar:
«Attempted to call an undefined method». Una prueba que solo instala sale en verde.

### Las trampas de los recambios

* **`Tools::stripslashes()` NO era el `stripslashes()` de PHP.** En 8.x devolvía la cadena
  **sin tocarla**, y su propio aviso de obsoleto dice «use PHP's stripslashes instead».
  Hacer caso al aviso **cambia el comportamiento**: se comen barras de datos que nunca se
  tocaron. Recambio: nada, la variable tal cual.
* **`Configuration::getInt()`** (1.7, quitado ya en 8.0) **no devolvía un entero**: llamaba
  a `getConfigInMultipleLangs()` y devolvía un array por idioma.
* Regla general: **un recambio que el núcleo nombra no es un recambio equivalente** hasta
  comparar los dos cuerpos.

### Constantes que ya no se definen

25 `define()` de 8.2.8 no están en 9.2.0, entre ellas `_CAN_LOAD_FILES_`,
`_PS_PRICE_COMPUTE_PRECISION_`, `_PS_PRICE_DISPLAY_PRECISION_`, `_PS_PROD_IMG_DIR_` y
`ALL_CARRIERS`.

* **`if (!defined('_CAN_LOAD_FILES_')) exit;`** como guarda: en 9.x el módulo **sale al
  cargarse** y la página queda en blanco. Se cambia por `_PS_VERSION_`.
* Alias que sí existen: `_PS_PROD_IMG_DIR_` → `_PS_PRODUCT_IMG_DIR_`,
  `ALL_CARRIERS` → `Carrier::ALL_CARRIERS`. Las de precisión se definen en el módulo con
  su valor de 8.2.8.
* **Una tienda ACTUALIZADA puede funcionar por casualidad**: el motor de actualización
  vuelve a definir esas constantes en `config/`. En una 9.2 **instalada de cero** no están,
  y el módulo que «iba bien» en la tienda actualizada revienta en la nueva.

### Librerías que 8.x traía en `vendor/` y 9.x no

Comparando `vendor/composer/installed.json` de 8.2.8 y 9.2.0 salen **21 paquetes** que ya
no vienen. El que hace daño es **Guzzle** (ya falta en 9.1.5):

* `new \GuzzleHttp\Client` en 9.x es un **`Error`** («Attempted to load class»), **no una
  `Exception`**: el `catch (\Exception $e)` que lo rodeaba no lo recoge y la pantalla da 500.
* Recambio: **cURL nativo** (`curl_init` / `curl_setopt` / `curl_exec`), que además es lo
  que manda la regla de cero dependencias de Composer.
* Al comparar paquetes, **`symfony/symfony` (8.x) se parte en `symfony/form`,
  `symfony/http-foundation`…** en 9.x: el espacio de nombres del paquete viejo desaparece,
  pero la clase sigue. Se da por cubierta si **algún espacio de 9.2 es prefijo** del nombre
  completo de la clase, no si coincide la clave.

### Tres cosas del núcleo que cortan la instalación sin avisar

* **`ps_versions_compliancy`** se rellena antes de comparar (`Module.php:293-306`):
  `'max' => '9'` pasa a `9.999.999.999` y vale; **`'9.0'` pasa a `9.0.999.999` y bloquea la
  9.2**; `'8.99.99'` también. Y un módulo que no declara nada tiene `max = _PS_VERSION_`.
* **Hook registrado sin su método**: con `_PS_MODE_DEV_` activo, `Hook.php:611` **lanza una
  excepción y corta la instalación a medias** (a veces antes de crear las tablas); sin modo
  desarrollo solo lo apunta en el registro. Todo `registerHook('x')` lleva su `hookX()`.
* **Un override de una clase que 9.x ya no tiene se IGNORA en silencio**
  (`Module::getOverrides()`, `Module.php:3599`: solo cuenta si existe `<Clase>Core`). El
  módulo se instala y esa parte no hace nada.

### Overrides de módulo: el fichero NO vive donde parece

`addOverride()` **copia o fusiona los métodos** en `/override/classes/...`. Dentro de un
fichero de `override/` del módulo:

* **nada de `__DIR__`**: al ejecutarse, `__DIR__` es la carpeta `/override` de la tienda;
* **nada de `require_once` arriba del fichero**: la fusión solo se lleva los métodos. Si un
  método necesita algo, el `require_once _PS_MODULE_DIR_ . '<modulo>/...'` va **dentro del
  método**.

## 2. Cómo auditar muchos módulos sin ahogarse en falsos positivos

Lo que funcionó, por orden, sobre 91 módulos:

1. **Índice del núcleo de 9.2.0** (`classes/` y `controllers/`) con la **cadena de herencia
   resuelta**: un método heredado de un padre no es «método retirado». Sin seguir la
   herencia, la mitad de los hallazgos eran falsos. Al subir por la cadena hay que probar el
   nombre del padre **y** `<padre>Core` en cada nivel.
2. **Todo hallazgo se confirma contra el código de 9.2.0.** Lo que existe se descarta.
3. **Constantes**: los `define()` de 8.2.8 que 9.2.0 no tiene, descartando las que el propio
   módulo define.
4. **Librerías**: los paquetes de `vendor/` que desaparecen, cubiertos por prefijo (ver arriba).
5. **Plantillas**: fuera los `{include}` dentro de comentarios `{* … *}` **de varias
   líneas**, las plantillas `_14.tpl`…`_17.tpl` que el módulo solo elige en esas versiones y
   las que pinta **otro** módulo (eso es un aviso, no un bloqueo). Y leer la plantilla desde
   la carpeta real del módulo: si se lee de una copia que ya no existe, cada lectura fallida
   se convierte en «plantilla que no existe».
6. **Sintaxis**: `php -l` con **8.1**, que es el mínimo de 9.x. Un módulo que se declara solo
   para 9.x puede llevar sintaxis de PHP 8 (propiedades en el constructor) y lintarlo con
   7.4 da un falso bloqueo.

**Reescritura con el tokenizador de PHP, nunca con expresiones regulares.** Y los recambios
que no son una línea (los métodos quitados) van a un fichero de compatibilidad del propio
módulo con el **cuerpo de 8.2.8**, probado contra el núcleo 9.2 **arrancado de verdad**
(con el kernel de Symfony cargado), no contra stubs.

## 3. Verificar en una 9.2 de verdad: lo que una prueba ingenua da por bueno

Instalar y abrir la configuración y **todas** las pestañas del módulo, con `_PS_MODE_DEV_`
activo (convierte los avisos en 500, que es lo que interesa ver). Y además:

* **Mirar DÓNDE acaba la petición, no solo el código.** Un módulo de seguridad que filtra el
  back-office por IP redirigía **todas** las configuraciones al panel: 302 → 200, y la prueba
  anotaba «configurar 200» sin haber abierto ninguna. Solo cuenta si la URL final es la
  pedida, o la pestaña propia del módulo (un `getContent()` que redirige ahí es legítimo);
  acabar en `AdminDashboard` o `AdminLogin` es fallo.
* **El texto de la página puede contener la frase de error**: un registro de cambios que
  dice «corregido "Undefined array key…"» dispara el detector con la página en 200. Se
  descarta a mano, apuntando la página y la frase exactas.
* **Una pantalla lenta no es una pantalla rota**: la que tarda más que el límite del
  verificador se abre aparte y se mide.
* **Un módulo cifrado con ionCube para otra versión de PHP**, solo con estar en `modules/`,
  **tumba la instalación de OTROS módulos** («Only files produced by the PHP 8.2 ionCube
  Encoder can run on PHP 8.2»). Se aparta de la carpeta antes de probar.
* **Idempotencia de los arreglos a mano**: si el texto nuevo **contiene** al viejo (añadir
  métodos delante de uno que ya existía), la guarda es «¿ya está el texto nuevo?», nunca
  «¿falta el viejo?». Si no, la segunda pasada lo duplica: `Cannot redeclare`.

Al instalar salen también fallos que **no son de 9.2** y rompen en cualquier versión; merece
la pena buscarlos por patrón en todos los módulos a la vez:

* `include_once '.../sql/install.sql'`: **imprime** el fichero, no lo ejecuta. La tabla no
  se crea nunca.
* Tablas que solo se crean al abrir la configuración: cualquier otra pestaña abierta antes
  da 500. Se crean en `install()`.
* `pSQL()` o `(int)` envolviendo un **trozo** de SQL (`pSQL($where)`, `(int) $whereFecha`)
  en vez de un valor: comillas escapadas o un `0`, y la consulta rota.
* Una plantilla que lee claves de un array que llega vacío cuando falla un servicio externo:
  en modo desarrollo, 500. Valores por defecto con `array_merge()`.
* `protected function hydrate(array $row)` redefiniendo `ObjectModel::hydrate()`: menos
  visibilidad y otra firma, fatal al cargar la clase.
