---
name: prestashop-carrier-seur
description: API de SEUR tal y como la usa el módulo oficial seur 2.5.26 de PrestaShop. Endpoints REST reales, OAuth2 password, las claves exactas de ps_configuration donde el comerciante ya tiene puestas sus credenciales, la tabla de 433 códigos de situación, etiquetas en PDF/ZPL y las trampas del código. Usar al integrar SEUR, al leer sus credenciales desde otro módulo o al consultar el seguimiento de un envío SEUR.
---

# SEUR — API real, leída del módulo oficial

**Fuente:** `seur`, versión **2.5.26**
(`seur/config.xml:5`), autor Seur, desarrollado por Ebolution.
**Solo lectura: no se modifica ni un byte de ese módulo.**

El módulo convive con dos generaciones de API. La **v2 (REST/JSON sobre `seur.io`) es la viva**;
las URL SOAP `ws.seur.com` siguen guardadas en configuración pero el flujo de alta, etiqueta y
seguimiento va por REST.

---

## 1. Endpoints reales

Todos salen de `seur/seur.php:236-267` (los `Configuration::updateValue` del `install()`), y los
mismos valores se reescriben en `seur/upgrade/upgrade-2.3.0.php`, `upgrade-2.3.9.php`,
`upgrade-2.5.18.php` y `upgrade-2.5.19.php`.

### 1.1 REST v2 — producción

| Qué hace | Clave de configuración | URL | Método |
|---|---|---|---|
| Token OAuth2 | `SEUR2_URLWS_TOKEN` | `https://servicios.api.seur.io/pic_token` | POST (form-urlencoded) |
| **Seguimiento** | `SEUR2_URLWS_E` | `https://servicios.api.seur.io/pic/v1/tracking-services/simplified` | **GET** (`classes/Expedition.php:43`) |
| Alta de expedición | `SEUR2_URLWS_ET` | `https://servicios.api.seur.io/pic/v1/shipments` | POST (`classes/Label.php:385`) |
| Modificar expedición | `SEUR2_URLWS_SHIPMENT_UPDATE` | `https://servicios.api.seur.io/pic/v1/shipments/update` | — |
| Añadir bultos | `SEUR2_URLWS_UPDATE_SHIPMENTS_ADD_PARCELS` | `https://servicios.api.seur.io/pic/v1/shipments/addpack` | — |
| **Etiquetas** | `SEUR2_URLWS_LABELS` | `https://servicios.api.seur.io/pic/v1/labels` | **GET** (`classes/Label.php:326`) |
| Recogidas | `SEUR2_URLWS_PICKUP` | `https://servicios.api.seur.io/pic/v1/collections` | — |
| Anular recogida | `SEUR2_URLWS_PICKUP_CANCEL` | `https://servicios.api.seur.io/pic/v1/collections/cancel` | — |
| Puntos de recogida | `SEUR2_URLWS_PICKUPS` | `https://servicios.api.seur.io/pic/v1/pickups` | — |
| Brexit: facturas | `SEUR2_URLWS_BREXIT_INV` | `https://servicios.api.seur.io/pic/v1/brexit/invoices` | — |
| Brexit: partidas | `SEUR2_URLWS_BREXIT_TARIF` | `https://servicios.api.seur.io/pic/v1/brexit/tariff-item` | — |

### 1.2 Entorno de PRUEBAS

No hay una clave de configuración aparte. El módulo cambia el dominio **en caliente** dentro de
`sendCurl()` cuando existe la constante `USE_API_PRE` (`seur/classes/SeurLib.php:707-710`):

```php
if (defined('USE_API_PRE') && USE_API_PRE) {
    $url = str_replace('https://servicios.api.seur.io', 'https://servicios.apipre.seur.io', $url);
}
```

Es decir: **pre = el mismo camino, cambiando `api` por `apipre`**. Ejemplos que aparecen
comentados en el código: `https://servicios.apipre.seur.io/pic_token` (`SeurLib.php:669`) y
`https://servicios.apipre.seur.io/pic/v1/tracking-services/simplified` (`Expedition.php:20`).

### 1.3 Geolabel (API intermedia, aún registrada)

`seur/seur.php:253-255`:

```
SEUR2_URLWS_ADD_SHIP     https://api.seur.com/geolabel/api/shipment/addShipment
SEUR2_URLWS_SHIP_LABEL   https://api.seur.com/geolabel/api/shipment/getLabel
SEUR2_URLWS_ET_GEOLABEL  https://api.seur.com/geolabel/swagger-ui.html#/add-shipment-controller
```

### 1.4 SOAP heredado (v1) — sigue registrado, ya no es el camino principal

`seur/seur.php:236-240`:

```
SEUR2_URLWS_SP  https://ws.seur.com/WSEcatalogoPublicos/servlet/XFireServlet/WSServiciosWebPublicos?wsdl
SEUR2_URLWS_R   https://ws.seur.com/webseur/services/WSCrearRecogida?wsdl
SEUR2_URLWS_A   https://ws.seur.com/webseur/services/WSConsultaAlbaranes?wsdl
SEUR2_URLWS_M   http://cit.seur.com/CIT-war/services/DetalleBultoPDFWebService?wsdl
```

**NO CONFIRMADO:** los nombres de las operaciones SOAP de estos WSDL no aparecen en el código del
módulo 2.5.26; el flujo actual no los invoca.

### 1.5 Página pública de seguimiento

`seur/seur.php:1164` y `:1832`:

```
https://www.seur.com/livetracking/pages/seguimiento-online.do?segOnlineIdentificador=<referencia>&segOnlineFecha=DD-MM-AAAA
```

La fecha es obligatoria, con ese formato exacto, montada troceando la fecha del pedido.

---

## 2. Autenticación

**OAuth2 con `grant_type=password`**, cinco datos. `seur/classes/SeurLib.php:662-694`:

```
POST  https://servicios.api.seur.io/pic_token
Accept: */*
Content-Type: application/x-www-form-urlencoded

grant_type=password&client_id=…&client_secret=…&username=…&password=…
```

**Cuidado con el cuerpo:** el módulo lo monta como un array de trozos y lo une con `&`
(`SeurLib.php:678-684` + `:720`), **sin `urlencode`**. Una contraseña con `&` o `+` rompe la
petición. En código nuevo, usar `http_build_query()`.

La respuesta trae `access_token` y `expires_in`. El módulo lo cachea **por tienda** en
`ps_configuration` y protege la renovación con un `flock` sobre
`_PS_CACHE_DIR_.'seur_token.lock'` (`SeurLib.php:604-655`), releyendo dentro del bloqueo por si
otra petición ya lo renovó.

Las llamadas posteriores llevan:

```
Accept: */*
Content-Type: application/json
Authorization: Bearer <access_token>
```

Además del token, **el seguimiento necesita el NIF del comercio y el CCC**, ver §5.

---

## 3. Claves EXACTAS de `ps_configuration`

Esto es lo que permite a un módulo nuevo reutilizar las credenciales que el comerciante ya tiene
puestas. Lista literal, tal cual se lee en el código.

### 3.1 Credenciales de la API (`SeurLib.php:668-674`, `:827-837`)

```
SEUR2_API_CLIENT_ID
SEUR2_API_CLIENT_SECRET
SEUR2_API_USERNAME
SEUR2_API_PASSWORD
```

`SeurLib::isAPIConfigured()` (`:827`) considera el módulo configurado si las **cuatro** están y no
están vacías. Misma comprobación vale para un módulo nuevo.

### 3.2 Token en caché (`SeurLib.php:607-608`, `:632-633`)

```
SEUR2_TOKEN_API              se guarda POR TIENDA (id_shop)
SEUR2_TOKEN_API_EXPIRES_AT   timestamp de caducidad
```

Se leen y escriben con `Configuration::get('SEUR2_TOKEN_API', null, null, $idShop)`. Un módulo
nuevo puede **reaprovechar ese token** en lugar de pedir otro.

### 3.3 Datos del comercio

```
SEUR2_MERCHANT_NIF_DNI     NIF/DNI — OBLIGATORIO en la consulta de seguimiento
SEUR2_MERCHANT_COMPANY
SEUR2_MERCHANT_FIRSTNAME
SEUR2_MERCHANT_LASTNAME
SEUR2_MERCHANT_USER
SEUR2_MERCHANT_PASS
SEUR2_MERCHANT_CLICKCOLLECT
SEUR2_D_EORI / SEUR2_R_EORI    EORI de destinatario y remitente (aduanas)
```

### 3.4 URL de servicio

```
SEUR2_URLWS_TOKEN  SEUR2_URLWS_E   SEUR2_URLWS_ET   SEUR2_URLWS_LABELS
SEUR2_URLWS_SHIPMENT_UPDATE   SEUR2_URLWS_UPDATE_SHIPMENTS_ADD_PARCELS
SEUR2_URLWS_PICKUP  SEUR2_URLWS_PICKUP_CANCEL  SEUR2_URLWS_PICKUPS
SEUR2_URLWS_BREXIT_INV  SEUR2_URLWS_BREXIT_TARIF
SEUR2_URLWS_ADD_SHIP  SEUR2_URLWS_SHIP_LABEL  SEUR2_URLWS_ET_GEOLABEL
SEUR2_URLWS_SP  SEUR2_URLWS_R  SEUR2_URLWS_A  SEUR2_URLWS_M     (SOAP heredado)
```

**Léelas de configuración, no las escribas a mano en el módulo nuevo.** Si SEUR cambia un camino,
el comerciante lo cambia en un sitio y funcionan los dos módulos.

### 3.5 Estados de pedido a los que se mapea cada grupo

```
SEUR2_STATUS_IN_TRANSIT            SEUR2_STATUS_DELIVERED
SEUR2_STATUS_INCIDENCE             SEUR2_STATUS_CONTRIBUTE_SOLUTION
SEUR2_STATUS_RETURN_IN_PROGRESS    SEUR2_STATUS_AVAILABLE_IN_STORE
```

### 3.6 Resto de opciones (por si hay que respetarlas)

```
SEUR2_SETTINGS_PRINT_TYPE      1=PDF, 2=ZPL, 3=A4_3
SEUR2_SETTINGS_LABEL_REFERENCE_TYPE
SEUR2_SETTINGS_PICKUP          SEUR2_SETTINGS_COD y su familia (COD_RATE, COD_MIN, COD_MAX,
                               COD_FEE_MIN, COD_FEE_PERCENT, COD_DETAILED_TAXES)
SEUR2_AUTO_CREATE_LABELS       SEUR2_AUTO_CREATE_LABELS_PAYMENTS_METHODS_AVAILABLE
SEUR2_AUTO_CALCULATE_PACKAGES  SEUR2_BULK_ASSIGN_CARRIER
SEUR2_UPDATE_SHIPMENT_CRON     SEUR2_UPDATE_SHIPMENT_INTERVAL   SEUR2_NEXT_TICK
SEUR2_CRON_KEY                 SEUR2_GOOGLE_API_KEY
SEUR2_NACIONAL_PRODUCT / _SERVICE     SEUR2_INTERNACIONAL_PRODUCT / _SERVICE
SEUR2_PICKUP_PRODUCT / _SERVICE (y las variantes _FRIO, _INT, _INT_FRIO, _INT_NOEUR, …)
SEUR2_FREE_PRICE  SEUR2_FREE_WEIGTH  SEUR2_TARIC
SEUR2_RETURNS_SITE_URL  SEUR2_ACTIVE_RETURNS_SITE_LINK
SEUR2_SENDED_ORDER  SEUR2_SENDED_IN_MANIFEST  SEUR2_CAPTURE_ORDER
SEUR2_RECALCULATE_SHIPMENT_COST  SEUR2_PRODS_REFS_IN_COMMENTS  SEUR2_MAP_RELOAD_CONFIG
```

Hay además un juego **heredado sin el `2`** (`SEUR_WS_USERNAME`, `SEUR_WS_PASSWORD`,
`SEUR_URLWS_*`, `SEUR_NACIONAL_PRODUCT`, `SEUR_TRANSCAR_*`, `SEUR_Configured`,
`SEUR_CONFIGURATION_OK`, `SEUR_PRINTER_NAME`…) del módulo de la época de PrestaShop 1.5/1.6.
**Un módulo nuevo debe leer las `SEUR2_*`; las `SEUR_*` solo como respaldo.**

### 3.7 Lo que NO está en `ps_configuration`: el CCC

El código de cliente y la franquicia están en **`ps_seur2_ccc`** (`seur/sql/install.php:29-49`):

```
id_seur_ccc, cit, ccc, nombre_personalizado, franchise, street_type, street_name,
street_number, staircase, floor, door, post_code, town, state, country, phone, email,
e_devoluciones, url_devoluciones, is_default, id_shop
```

Se lee con `SeurLib::getMerchantData($id_seur_ccc)` (`SeurLib.php:88-98`), que por defecto usa
`id_seur_ccc = 1`. Puede haber **varios CCC** (nacional e internacional) y `SeurLib::getCCC()`
(`:101-121`) elige según el país de destino.

---

## 4. Detectar el módulo

```php
if (Module::isInstalled('seur') && Module::isEnabled('seur')
    && Configuration::get('SEUR2_API_CLIENT_ID')
    && Configuration::get('SEUR2_API_CLIENT_SECRET')
    && Configuration::get('SEUR2_API_USERNAME')
    && Configuration::get('SEUR2_API_PASSWORD')) {
    // credenciales SEUR reutilizables
}
```

Nombre en `ps_module`: **`seur`** (`seur/config.xml:3`).

---

## 5. Seguimiento

`seur/classes/Expedition.php:15-56`. Es un **GET** con los parámetros en la cadena de consulta
(`SeurLib::sendCurl()` hace `http_build_query()` cuando la acción es `GET`, `SeurLib.php:735-739`).

```
GET https://servicios.api.seur.io/pic/v1/tracking-services/simplified
    ?ref=<referencia del pedido>
    &refType=REFERENCE
    &idNumber=<SEUR2_MERCHANT_NIF_DNI>
    &accountNumber=<ps_seur2_ccc.ccc>
    &businessUnit=<ps_seur2_ccc.franchise>
Authorization: Bearer <token>
```

**La consulta va por REFERENCIA del pedido, no por número de expedición.** Es lo que manda el
módulo: `'refType' => 'REFERENCE'` (`Expedition.php:37`) con `SeurLib::getOrderReference($order)`
(`commands/UpdateShipmentsStatus.php:99-107`).

Respuesta: objeto con `data[]`. Se usa el **primer** elemento, `data[0]`, y de él:

- `eventCode` — el código de situación (`UpdateShipmentsStatus.php:115-116`)
- `description` — texto que se guarda en el pedido (`:150`)

Si viene `errors` o no viene `data`, es error aunque el HTTP sea 200 (`Expedition.php:44-48`).

### 5.1 La tabla de códigos de situación: 433 filas en `ps_seur2_status`

`seur/sql/install.php:194-205` crea la tabla y mete **433 filas** con tres columnas:
`id_status`, `cod_situ`, `grupo`.

El `eventCode` que devuelve el API se **trocea con una expresión regular**
(`UpdateShipmentsStatus.php:114-124`):

```php
preg_match('/(.)(.)([0-9]*)/', $cod_situacion, $matches, PREG_OFFSET_CAPTURE);
$tipo_situ = $matches[2][0];   // SEGUNDO carácter
$cod_situ  = $matches[3][0];   // la parte numérica
```

y se busca así (`classes/SeurOrder.php:179-187`):

```sql
SELECT * FROM ps_seur2_status WHERE cod_situ LIKE '%<tipo><cod a 3 dígitos con ceros>'
```

Es decir, `cod_situ` tiene la forma **letra + letra + 3 dígitos**: `LC002`, `II721`, `LI566`,
`SC845`, `LD221`, `LK…`, `LM…`, `LX…`, `SK…`, `SW…`, `SX…`, `LJ…`, `LL…`, `LO…`, `LR…`, `LS…`,
`LT…`, `IS…`.

**Reparto real de las 433 filas por grupo** (contado sobre `seur/sql/install.php`):

| `grupo` | Filas | Estado de pedido al que va |
|---|---|---|
| `EN TRÁNSITO` | 143 | `SEUR2_STATUS_IN_TRANSIT` |
| `ENTREGADO` | 89 | `SEUR2_STATUS_DELIVERED` |
| `INCIDENCIA` | 61 | `SEUR2_STATUS_INCIDENCE` |
| `DOCUMENTACIÓN RECTIFICADA` | 59 | `SEUR2_STATUS_IN_TRANSIT` (comparte destino) |
| `APORTAR SOLUCIÓN` | 39 | `SEUR2_STATUS_CONTRIBUTE_SOLUTION` |
| `DEVOLUCIÓN EN CURSO` | 8 | `SEUR2_STATUS_RETURN_IN_PROGRESS` |
| `DISPONIBLE PARA RECOGER EN TIENDA` | 7 | `SEUR2_STATUS_AVAILABLE_IN_STORE` |
| `MULTIPARCEL` | 1 | ninguno (no está en el `switch`) |
| `CLASSIC` | 1 | ninguno (no está en el `switch`) |

El `switch` que mapea grupo → estado de pedido está en `classes/SeurOrder.php:209-231`.
**Los grupos `MULTIPARCEL` y `CLASSIC` no tienen caso**: caen fuera y `$id_status_order` se queda
sin definir (aviso de PHP 8 al llegar al `if` de la línea 233).

Muestra de códigos reales (`seur/sql/install.php:206-…`):

| `cod_situ` | `grupo` |
|---|---|
| `LC001`, `LC002`, `LC003`, `LC004`, `LC005`, `LC006`, `LC101` | EN TRÁNSITO |
| `LC845`, `LC860`, `SC845`, `SC883`, `SC999`, `SC001` | EN TRÁNSITO |
| `LD221`, `LD223`, `LD846`, `LD841`, `II718`, `II740` | EN TRÁNSITO |
| `II701` | DEVOLUCIÓN EN CURSO |
| `II717`, `II719`, `II721`, `II722`, `II731`, `II732`, `II741`–`II762` | APORTAR SOLUCIÓN |
| `LI452`, `LI456`, `LI457`, `LI460`, `LI566`, `LI567` | EN TRÁNSITO |
| `LI717`–`LI732` | APORTAR SOLUCIÓN |

**La tabla completa está en `seur/sql/install.php` a partir de la línea 205.** Si hace falta el
mapa entero, se lee de ahí: es la única copia fiable y viene del propio SEUR.

### 5.2 Terminología

`tipo_situ` (la **segunda** letra) marca la familia: `C` = circulación, `D` = entrega, `I` =
incidencia. La **primera** letra (`L`, `S`, `I`, `X`…) el módulo la descarta: solo se queda con la
segunda y con el número. Consecuencia real: `LC002` y `SC002` son la misma fila para el módulo.

---

## 6. Etiquetas

`seur/classes/Label.php:300-368`. Es un **GET** con el cuerpo en la cadena de consulta.

```
GET https://servicios.api.seur.io/pic/v1/labels
    ?code=<shipmentCode>&type=<PDF|ZPL|A4_3>&entity=EXPEDITIONS
    [&templateType=Z4_TWO_BODIES]     ← solo cuando type=A4_3
Authorization: Bearer <token>
```

El tipo sale de `SEUR2_SETTINGS_PRINT_TYPE` a través de `PrinterType` (`classes/PrinterType.php:9-24`):

| Valor | Constante | `type` que se manda |
|---|---|---|
| `1` | `PRINTER_TYPE_PDF` | `PDF` |
| `2` | `PRINTER_TYPE_ETIQUETA` | `ZPL` |
| `3` | `PRINTER_TYPE_A4_3` | `A4_3` + `templateType: Z4_TWO_BODIES` |

Respuesta: `data[]`, un elemento por etiqueta. De cada uno (`Label.php:334-339`):

- **PDF** → campo `pdf`, en **base64**; el módulo hace `base64_decode()` y lo escribe como `.pdf`.
- **ZPL** → campo `label`, en texto plano; se escribe como `.txt`.

Se guardan en `modules/seur/files/deliveries_labels/`, con el nombre del pedido y sufijo `_2`,
`_3`… a partir de la segunda (`Label.php:341-347`).

Alta previa de la expedición (`Label.php:375-395`): **POST** a `SEUR2_URLWS_ET` con JSON. De la
respuesta se usan `data.shipmentCode`, `data.ecbs` y `data.parcelNumbers` (`:349-351`), que se
guardan en `ps_seur2_order` (`SeurLib.php:381-390`).

---

## 7. Número de seguimiento

- Lo que se escribe en el pedido es `ps_orders.shipping_number`, vía
  `$order->setWsShippingNumber()`, **recortado a 64 caracteres** (`SeurLib.php:393-398`).
- Lo detallado queda en `ps_seur2_order`: `expeditionCode`, `ecbs` y `parcelNumbers` (estos dos
  como listas unidas por `-`), y `label_files`.

**NO CONFIRMADO:** el módulo no valida ni describe en ningún sitio la longitud ni el prefijo del
`shipmentCode`, así que **no se puede adivinar un envío SEUR a partir del número**. Para saber si
un pedido es de SEUR hay que mirar su `id_carrier` contra `ps_seur2_carrier` o el
`external_module_name = 'seur'` del transportista.

---

## 8. Trampas vistas en este código

1. **El cuerpo del token no va codificado.** `SeurLib.php:678-684` monta `'password=' . $password`
   y lo une con `&`. Una contraseña con `&`, `+` o `%` rompe la autenticación sin decir por qué.
2. **`sendCurl` con `GET` mete los datos en la URL.** Si se le pasa un array grande (el caso de
   `/labels` y `/tracking-services/simplified`), todo va en la cadena de consulta.
3. **Verificación TLS desactivada**: `CURLOPT_SSL_VERIFYHOST` y `CURLOPT_SSL_VERIFYPEER` a `false`
   (`SeurLib.php:750-751`). No copiarlo.
4. **HTTP 200 con error dentro.** Se comprueba `isset($response->errors)` / `->error`
   (`Label.php:387-394`, `Expedition.php:44`). El código HTTP no dice nada.
5. **Mensaje de error roto por precedencia de operadores**: `Expedition.php:45` hace
   `'TRACKING Error: '.isset($response->errors[0]->detail)?? ''`. La concatenación se evalúa antes
   que `isset`, así que el mensaje que sale es basura. Al diagnosticar, no fiarse de ese texto:
   mirar el registro de `SeurLib::log()`.
6. **El seguimiento va por referencia del pedido, no por expedición.** Si la referencia del pedido
   cambia, el seguimiento deja de encontrar nada.
7. **`MULTIPARCEL` y `CLASSIC` no tienen estado de pedido asignado** (§5.1).
8. **La clave de la caché del token es por tienda.** En multitienda, leer siempre con `id_shop`.
9. **`SEUR2_API_CLIENT_SECRET` se usa como «secreto» de una URL pública del front**
   (`seur/seur.php:884-889`: `getModuleLink('seur','updateshipments',['secret' => …])`). Es decir,
   el client_secret de la API viaja en una URL del back-office. **No repetir ese patrón**: para un
   cron, token propio (`SEUR2_CRON_KEY` ya existe para eso).

---

## 9. Fragmento PHP listo para copiar (estructura legacy, sin Composer, cURL nativo)

Consulta el seguimiento de un pedido reutilizando las credenciales que el módulo `seur` ya tiene.

```php
<?php
/**
 * Seguimiento SEUR reutilizando la configuracion del modulo oficial 'seur'.
 * Sin Composer, sin namespace, cURL nativo.
 */
if (!defined('_PS_VERSION_')) {
    exit;
}

class MiSeurTracking
{
    /** Token OAuth2, reaprovechando el que el modulo 'seur' ya tenga en cache. */
    public static function getToken()
    {
        $idShop = (int) Context::getContext()->shop->id;

        $token = (string) Configuration::get('SEUR2_TOKEN_API', null, null, $idShop);
        $exp = (int) Configuration::get('SEUR2_TOKEN_API_EXPIRES_AT', null, null, $idShop);
        if ($token !== '' && $exp > (time() + 60)) {
            return $token;
        }

        $clientId = Configuration::get('SEUR2_API_CLIENT_ID');
        $clientSecret = Configuration::get('SEUR2_API_CLIENT_SECRET');
        $username = Configuration::get('SEUR2_API_USERNAME');
        $password = Configuration::get('SEUR2_API_PASSWORD');
        if (!$clientId || !$clientSecret || !$username || !$password) {
            return false;
        }

        $url = Configuration::get('SEUR2_URLWS_TOKEN');
        if (!$url) {
            $url = 'https://servicios.api.seur.io/pic_token';
        }

        // http_build_query, NO la concatenacion a pelo del modulo oficial.
        $body = http_build_query(array(
            'grant_type' => 'password',
            'client_id' => $clientId,
            'client_secret' => $clientSecret,
            'username' => $username,
            'password' => $password,
        ));

        $ch = curl_init();
        curl_setopt_array($ch, array(
            CURLOPT_URL => $url,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $body,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 20,
            CURLOPT_HTTPHEADER => array(
                'Accept: */*',
                'Content-Type: application/x-www-form-urlencoded',
            ),
        ));
        $raw = curl_exec($ch);
        $err = curl_error($ch);
        curl_close($ch);

        if ($err || $raw === false || $raw === '') {
            return false;
        }

        $json = json_decode($raw, true);
        if (!is_array($json) || empty($json['access_token'])) {
            return false;
        }

        $expiresIn = isset($json['expires_in']) ? (int) $json['expires_in'] : 3600;
        Configuration::updateValue('SEUR2_TOKEN_API', $json['access_token'], false, null, $idShop);
        Configuration::updateValue('SEUR2_TOKEN_API_EXPIRES_AT', time() + $expiresIn, false, null, $idShop);

        return $json['access_token'];
    }

    /** CCC y franquicia del comercio (tabla ps_seur2_ccc del modulo oficial). */
    public static function getMerchantData($idSeurCcc = 1)
    {
        $fila = Db::getInstance(_PS_USE_SQL_SLAVE_)->getRow(
            'SELECT `ccc`, `franchise`
               FROM `' . _DB_PREFIX_ . 'seur2_ccc`
              WHERE `id_seur_ccc` = ' . (int) ($idSeurCcc > 0 ? $idSeurCcc : 1)
        );

        return is_array($fila) ? $fila : array();
    }

    /**
     * Devuelve el ultimo evento del envio, o false.
     * OJO: SEUR consulta por REFERENCIA del pedido, no por numero de expedicion.
     *
     * @return array|false  array('eventCode' => 'LC002', 'description' => '...')
     */
    public static function getEstado($referenciaPedido, $idSeurCcc = 1)
    {
        $token = self::getToken();
        if (!$token) {
            return false;
        }

        $merchant = self::getMerchantData($idSeurCcc);
        if (empty($merchant['ccc'])) {
            return false;
        }

        $url = Configuration::get('SEUR2_URLWS_E');
        if (!$url) {
            $url = 'https://servicios.api.seur.io/pic/v1/tracking-services/simplified';
        }

        $url .= '?' . http_build_query(array(
            'ref' => $referenciaPedido,
            'refType' => 'REFERENCE',
            'idNumber' => Configuration::get('SEUR2_MERCHANT_NIF_DNI'),
            'accountNumber' => $merchant['ccc'],
            'businessUnit' => isset($merchant['franchise']) ? $merchant['franchise'] : '',
        ));

        $ch = curl_init();
        curl_setopt_array($ch, array(
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 20,
            CURLOPT_HTTPHEADER => array(
                'Accept: */*',
                'Content-Type: application/json',
                'Authorization: Bearer ' . $token,
            ),
        ));
        $raw = curl_exec($ch);
        $err = curl_error($ch);
        curl_close($ch);

        if ($err || $raw === false || $raw === '') {
            return false;
        }

        // HTTP 200 NO significa que haya ido bien: el error viene dentro.
        $json = json_decode($raw, true);
        if (!is_array($json) || !empty($json['errors']) || empty($json['data'][0])) {
            return false;
        }

        $evento = $json['data'][0];

        return array(
            'eventCode' => isset($evento['eventCode']) ? $evento['eventCode'] : '',
            'description' => isset($evento['description']) ? $evento['description'] : '',
        );
    }

    /**
     * Traduce un eventCode al grupo de SEUR usando la tabla del modulo oficial.
     * Devuelve 'EN TRANSITO', 'ENTREGADO', 'INCIDENCIA'... o false.
     */
    public static function getGrupo($eventCode)
    {
        if (!preg_match('/^(.)(.)([0-9]+)$/', (string) $eventCode, $m)) {
            return false;
        }

        $busca = $m[2] . str_pad($m[3], 3, '0', STR_PAD_LEFT);

        return Db::getInstance(_PS_USE_SQL_SLAVE_)->getValue(
            'SELECT `grupo` FROM `' . _DB_PREFIX_ . 'seur2_status`
              WHERE `cod_situ` LIKE "%' . pSQL($busca) . '"'
        );
    }
}
```

Uso:

```php
$estado = MiSeurTracking::getEstado('PEDIDO-1234');
if ($estado !== false) {
    $grupo = MiSeurTracking::getGrupo($estado['eventCode']);  // 'ENTREGADO', 'EN TRÁNSITO'...
}
```

---

## 10. Qué NO se ha podido confirmar leyendo el código

- **Operaciones de los WSDL heredados** (`ws.seur.com`, `cit.seur.com`): las URL están registradas
  pero el módulo 2.5.26 no las invoca; los nombres de operación no aparecen.
- **Estructura del JSON de alta de expedición** (`/pic/v1/shipments`): el cuerpo se monta en
  `Label.php` a partir de datos del pedido a lo largo de cientos de líneas; no hay un esquema
  escrito. Para replicarlo hay que leer `seur/classes/Label.php` entero.
- **Formato del `shipmentCode`** (longitud, prefijo): no se valida en ningún sitio.
- **Códigos de error del API** (los `errors[].detail`): no hay tabla en el módulo.
- **Puntos de recogida** (`/pic/v1/pickups`) y **recogidas** (`/pic/v1/collections`): las URL están
  confirmadas, la forma de la petición no se ha revisado en esta lectura.
