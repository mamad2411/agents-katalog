---
name: prestashop-9-2
description: Que cambia de verdad en PrestaShop 9.2 respecto a 9.1: el checkout de una pagina que ahora viene en el nucleo, las seis firmas que cambian, las tres condiciones de producto nuevas, los 46 hooks que llegan y las 10 tablas nuevas. Medido comparando los nucleos 9.1.5 y 9.2.0 en disco, no leido de la documentacion. Invocar al actualizar una tienda a 9.2, al adaptar un modulo de pago o de transporte al checkout de una pagina, al usar las extra properties, o cuando algo del checkout deje de funcionar despues de actualizar. Para llevar un modulo de 8.x a 9.x esta prestashop-modulo-8-a-9; para temas, prestashop-tema-hummingbird.
---

# PrestaShop 9.2

Todo lo de aquí está **medido comparando los dos núcleos extraídos en disco**, el de 9.1.5
y el de 9.2.0, uno al lado del otro; no copiado de la documentación. Cuando algo sale de las
devdocs, se dice.

Dos cosas viven en otro skill, porque son otro trabajo: llevar un módulo de **8.x a 9.x** es
`prestashop-modulo-8-a-9`, y los **temas hijo de Hummingbird**, `prestashop-tema-hummingbird`.

## Lo primero, y es una buena noticia: 9.2 no quita nada

| | 9.1.5 → 9.2.0 |
|---|---|
| métodos estáticos retirados | **0** |
| métodos de instancia retirados | **0** |
| constantes `define()` retiradas | **0** |
| rutas de Symfony retiradas | **0** (698 → 753) |
| hooks retirados | **0** (1111 → 1157) |
| renombres oficiales de hook | **0** |
| columnas de la base que se van | **0** |

Es una versión menor y se nota: **un módulo que funciona en 9.1 no se cae en 9.2 por nada
de lo de arriba.** Los pasos del motor que buscan métodos retirados, clases movidas,
constantes o columnas perdidas van a salir vacíos, y eso es lo correcto.

Lo que sí cambia está en tres sitios: el **checkout**, las **firmas** de seis métodos y
las **condiciones de producto**.

## 1. El checkout de una página, en el núcleo

9.2 trae `modules/ps_onepagecheckout` **dentro del paquete**. Cambia una cosa de fondo:

> **La página ya no se recarga.** El listado de transportes y el de formas de pago se
> rehacen por AJAX cuando el cliente cambia la dirección o el transportista.

Eso rompe, en silencio y con la página en 200, a dos clases de módulo.

### Pago que se envía solo (`setBinary(true)`)

Botones inteligentes, campos alojados, redirecciones. Antes el formulario del checkout se
enviaba y después iba el pago. Ahora hay que pedirle al checkout que guarde **antes**:

```js
window.ps_onepagecheckout.submitBeforePayment()
  .then(() => { /* aquí el pago */ });
```

**Si no se hace:** el cliente, la dirección y el transportista elegido no se guardan antes
de que el pago se lleve al cliente fuera. Pedidos a medias, sin un error en ningún sitio.

Un caso real: **`ps_checkout`**, el módulo de pago de la propia PrestaShop, es binario, y
en una tienda en producción no llamaba a `submitBeforePayment`.

### Interfaz propia que hay que volver a montar

Un mapa de puntos de recogida, un calculador de portes, un campo extra. Al rehacerse la
sección por AJAX, lo que el módulo había montado **desaparece**:

```js
prestashop.on('opcPaymentMethodsUpdated', () => { montarMisBotones(); });
prestashop.on('opcCarriersUpdated',       () => { montarMiMapa(); });
```

Los cinco avisos que manda el checkout, **comprobados en el código del módulo**, no en las
devdocs:

`opcCarriersLoading` · `opcCarriersUpdated` · `opcCarrierSelected` · `opcCarriersFailed` ·
`opcPaymentMethodsUpdated`

### Cómo se sabe si un módulo es de transporte

**No por `getOrderShippingCost`.** Medido sobre dos módulos de transporte a medida que
pintan el calculador de portes en tiendas en producción: **ninguno de los dos lo declara.**
Lo que los delata es que enganchan los hooks del paso de transporte:

`displayBeforeCarrier` · `displayAfterCarrier` · `displayCarrierExtraContent` ·
`actionCarrierProcess` · `displayCarrierList` · `actionValidateStepComplete` ·
`actionSubmitCustomerAddressForm` · `actionValidateCustomerAddressForm`

Esto **se avisa, no se arregla**: cada módulo monta su interfaz a su manera y escribirle el
remonte sería inventarse su código.

> *(Lo comprueba un guion personal, no incluido en este repositorio: busca los módulos de
> pago binarios que no llaman a `submitBeforePayment()` y los que pintan algo en el paso de
> transporte sin escuchar `opcCarriersUpdated` / `opcPaymentMethodsUpdated`.)*

## 2. Seis firmas que cambian, y ninguna quita nada

Todas **añaden parámetros opcionales al final**, así que las llamadas siguen valiendo. Lo
que sí rompe es un **override** de una de ellas con la firma vieja: eso es un fatal **al
enlazar la clase**, no de sintaxis, así que `php -l` pasa limpio y no se ve hasta que algo
carga esa clase.

> *(Lo caza un guion personal, no incluido en este repositorio: compara cada declaración de
> los `override/` y de los módulos con la firma del método en el núcleo de destino, y avisa
> de las que no cuadran.)*

### Y ese fatal MATA AL `autoupgrade`, así que hay que arreglarlo ANTES de actualizar

Medido el 30/09/2026 en una tienda en producción, que no pudo saltar a 9.2 y murió a los
6,6 minutos con **36.700 ficheros ya copiados y la base todavía en 9.1.5**:

```
Fatal error: Declaration of ImageManager::resize($sourceFile, $destinationFile, ...)
must be compatible with ImageManagerCore::resize(..., string $imageFitment = ImageFitment::FIT)
  override/classes/ImageManager.php línea 42
```

**No es que el arreglo no exista: es que llegaba tarde.** `autoupgrade` copia los ficheros
y después **arranca la tienda con el núcleo NUEVO** para migrar la base (paso
`UpdateDatabase`); el override con la firma vieja revienta ahí, antes de que se pueda
reparar nada. La reparación tiene que ir **delante del salto**.

Y se puede adelantar sin romper la tienda de la versión de partida, porque **PHP deja que
una clase hija declare más parámetros opcionales que su padre**:

```
9.1  el padre tiene 12  ->  el hijo declara 13, el último opcional  -> vale
9.2  el padre tiene 13  ->  el hijo declara 13                      -> vale
```

Dos cosas que hay que hacer bien al adelantarla:

* **El valor por defecto se escribe como LITERAL**, nunca la constante del núcleo nuevo:
  `ImageFitment::FIT` se escribe **`'fit'`**, porque esa clase **no existe en 9.1** y
  copiarla tal cual deja el override sin poder cargarse — justo lo que se intentaba evitar.
* **Los parámetros se comparan por CUÁNTOS SON, no por cómo se llaman.** A PHP le da igual
  el nombre; el override de un cliente casi nunca copia los del núcleo (llamaba `$fileType`
  a lo que el núcleo llama `$destinationFileType`). Comparando nombres, el detector decía
  «0 declaraciones» en la tienda que tenía el fallo delante.

### Ficheros ya en 9.2 y base en 9.1.5 NO siempre es un callejón sin salida

Es el estado en que queda una tienda cuando el salto muere después de copiar. La regla
conocida dice que ahí `autoupgrade` contesta `Versions are identical` y no migra nunca,
porque saca la versión de origen de los **ficheros**. Cierto, **pero solo cuando no
encuentra estado**:

```php
// UpgradeContainer::getCurrentPrestaShopVersion()
if ($this->getUpdateState()->isInitialized()) {      // = existe state_update.var
    return $this->getUpdateState()->getCurrentVersion();
}
return $this->getPrestaShopConfiguration()->getPrestaShopVersion();
```

Mientras `<admin>/autoupgrade/state_update.var` viva, dentro sigue puesto
`currentVersion = "9.1.5"` y **se puede continuar**: `update:start … --action=<el último
que autoupgrade dejó escrito en su registro>`. Lo que mata la tienda es **borrar ese
estado** por reflejo.

Los dos estados se distinguen midiendo, no opinando:

| estado | cómo se reconoce | qué se hace |
|---|---|---|
| **rancio** | su `currentVersion` **no** es la de la base: es de otro intento | se tira; si no, `autoupgrade` se cree una versión que la tienda no tiene |
| **a medias** | `currentVersion` == la de la base, `destinationVersion` == la que se pide, los ficheros ya son los de destino y el `backlog` de `filesToUpgrade.list` está **vacío** | se conserva y se continúa con `--action` |

Si lo que se quedó a medias es la **copia de ficheros** (backlog con cosas dentro), esto no
aplica: eso sí hay que rehacerlo desde el ZIP del cliente.

| método | qué se le añade |
|---|---|
| `AddProductToOrderCommand::toExistingInvoice` | `?int $shipmentId`, `?int $carrierId`, `?bool $isVirtual` |
| `AddProductToOrderCommand::withNewInvoice` | `?int $shipmentId`, `?int $carrierId`, `?bool $isVirtual` |
| `Connection::isBot` | `$userAgent = null` |
| `ImageManager::resize` | `string $imageFitment = ImageFitment::FIT` |
| `StockMovement::createEditionMovement` | `array $apiClientIds`, `array $apiClientNames` |
| `StockMovement::createOrdersMovement` | `array $apiClientIds`, `array $apiClientNames` |

## 3. Condiciones de producto: tres valores nuevos

A `new`, `used` y `refurbished` se suman **`open_box`**, **`damaged`** y
**`new_with_defects`** (devdocs). Un módulo que compare la condición contra una lista
cerrada —un `switch`, un `in_array`— se deja fuera productos sin decir nada.

## 4. Lo que llega nuevo (46 hooks) y no rompe nada

Ninguno es obligatorio; son puntos donde engancharse.

* **Checkout**: `actionCheckoutBuildProcess`.
* **Front**: `displayCartBelowSummary`, `displayOrderDetailProductLine`,
  `displaySubcategories`.
* **Extra properties** (16 hooks `*ExtraPropertyDefinition*`): campos extra en productos,
  combinaciones, clientes y pedidos **sin tabla propia**, y salen solos en el
  back-office, el front y la API. Está marcado `@experimental` en el propio núcleo: sirve
  para sustituir tablas a medida, pero no para construir encima todavía.
* **Envíos** (`*FulfillShipment*`), **accesos rápidos**, **reglas de impuestos**,
  **plantillas de correo**, **devoluciones** y **países**: pantallas que terminan de
  migrarse a Symfony, cada una con su familia de hooks de rejilla y formulario.

## 5. La base: 10 tablas nuevas, ninguna que se vaya

Nuevas: `extra_property_definition`, `extra_property_definition_shop`, y ocho de B2B
(`b2b_role`, `business_entity`, `customer_b2b`…). Columnas nuevas en `cart_rule`
(`total_quantity`), `image_type` (`image_fitment`), `order_return_detail` (`cancelled`),
`order_return_state` (`is_cancelling_return`) y `shipment` (`deleted`).

El **B2B mejorado** va detrás de la bandera `improved_b2b`, en beta y apagada: las devdocs
dicen expresamente que su esquema va a cambiar y que no se construya encima.

## 6. Cosas sueltas que conviene saber

* **Servicios del módulo**: ahora se pueden dar por versión —
  `services.php` → `services-9.2.yml` → `services-9.yml` → `services.yml`—, y el
  `services.yml` de siempre sigue valiendo.
* **JSON-LD en el núcleo**: los datos estructurados se pasan como array por
  `actionFrontControllerSetVariables` y los pinta el tema.
* **La carpeta `install/` se borra sola** al terminar la instalación.
* **Órdenes de consola nuevas**, y una es muy útil aquí:
  `prestashop:employee:create-admin` crea un administrador sin tocar la base a mano;
  también `prestashop:module:list`, `prestashop:employee:change-password` y
  `prestashop:htaccess:generate`.

## Cómo se actualiza una tienda a 9.2

**En peldaños, y la escalera es esta:**

```
8.2  ->  9.1  ->  9.2
```

De 1.7.8.11 a 9.2 son los tres saltos; de 8.2.8, dos; de 9.1.5, uno. **De 1.7.x a 9.x de una
vez no se puede** y está medido por los dos lados: con PHP 7.4
`update:check-requirements` rechaza el destino 9.x, y con PHP 8.1 el `vendor/doctrine` que
trae 1.7.8 no compila, así que `update:start` no llega a arrancar la tienda para migrarla.

PHP: 9.2 pide **8.1 como mínimo** y admite hasta 8.5.

> *(Aquí lo encadena un motor propio, no incluido en este repositorio: monta la copia del
> cliente en local, da los saltos que falten y repara lo que cada uno rompe.)*

## Lo que conviene automatizar

Estas comprobaciones están escritas como guiones propios que **no se publican aquí**; lo que
sí vale la pena llevarse es **qué comprueban**, porque son las que encontraron los fallos de
este documento:

| qué comprueba | en dos líneas |
|---|---|
| El checkout de una página | Marca los módulos de **pago binario** que no llaman a `submitBeforePayment()` y los que pintan interfaz en el paso de transporte sin escuchar `opcCarriersUpdated` / `opcPaymentMethodsUpdated`. Avisa; no reescribe el módulo. |
| Los avisos del propio checkout | Busca los cinco nombres de evento **dentro del módulo del paquete 9.2.0**. Si PrestaShop los renombra en 9.3, salta la comprobación en vez de quedarse callada. |
| Las firmas de los overrides | Compara cada declaración con la del método en el núcleo de destino y avisa de las que no cuadran, **antes** de actualizar. |
| La escalera de versiones | Que los saltos que salen sean `8.2 → 9.1 → 9.2` según de dónde se venga, y que nunca se proponga `1.7.x → 9.x` directo. |

**Un aviso que no se queda callado cuando cambia el núcleo vale el doble que uno que
acierta hoy.** Las tres primeras se comprueban contra el código de 9.2.0 en disco, no contra
una lista escrita a mano: cuando PrestaShop cambie el nombre, la comprobación falla y se
entera alguien.
