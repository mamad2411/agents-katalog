---
name: prestashop-carrier-correos
description: API REST de Correos (P3/CorreosID) y de Correos Express (CEX) tal y como las usa el módulo oficial correosoficial 3.0.0 de PrestaShop. Endpoints reales de producción y PRE, OAuth2 client_credentials y HTTP Basic, la tabla ps_correos_oficial_codes donde están cifradas las credenciales del comerciante, el mapa de 692 códigos de evento a cinco estados, etiquetas PDF/ZPL/XML y las trampas del código. Usar al integrar Correos o Correos Express, al leer sus credenciales desde otro módulo o al consultar el seguimiento de un envío.
---

# Correos y Correos Express — API real, leída del módulo oficial

**Fuente:** `correosoficial`, versión
**3.0.0** (`config.xml:5`), autor Grupo Correos. **Solo lectura: no se modifica ni un byte.**

Un solo módulo integra **dos transportistas con dos API completamente distintas**:

| | **Correos** (P3 / CorreosID) | **Correos Express** (CEX) |
|---|---|---|
| Protocolo | REST/JSON | REST/JSON |
| Autenticación | OAuth2 `client_credentials` → Bearer | HTTP Basic |
| Clase | `CorreosOficialRest` | `CorreosOficialCEXRest` |
| Quién elige | `CorreosOficialApiRouter::…` según `payload['company']` (`'Correos'` \| `'CEX'`) y el remitente del pedido (`classes/CorreosOficialApiRouter.php:89-147`) |

Hay una tercera clase, `CorreosOficialSGARest`, para el almacén (SGA), que comparte URL y forma de
autenticación con la de Correos.

> **Aviso de estructura:** este módulo trae `src/`, `vendor/` y `composer.json`. Es del fabricante.
> **Un módulo propio NO debe copiar esa estructura** — manda el `CLAUDE.md` del proyecto:
> estructura legacy, sin Composer. Todo lo de aquí se puede hacer con `curl` nativo.

---

## 1. Endpoints reales

### 1.1 Correos (P3) — `classes/Apis/CorreosOficialRest.php:44-57`

El entorno lo decide **una sola clave**, `CORREOS_OFICIAL_SANDBOX_MODE`: `1` → PRE, `0` → PRO
(`classes/Apis/CorreosOficialRest.php:41-43`).

| Qué hace | PRO | PRE (sandbox) |
|---|---|---|
| Token | `https://apioauthcid.correos.es/Api/Authorize/token` | `https://azam-t-correosid-a0-svc-netcore-oauthservices-01.azurewebsites.net/Api/Authorize/token` |
| API de logística | `https://api1.correos.es/logistics/tradeinout/api/v1` | `https://api1.correospre.es/logistics/tradeinout/api/v1` |
| API de seguimiento | `https://api1.correos.es/support/track/api/v1` | `https://api1.correospre.es/support/track/api/v1` |

> La URL de token de PRE es un `azurewebsites.net`. La «buena» (`https://apioauthcid.correospre.es/Api/Authorize/Token`)
> está **comentada** en el código (`:46`). Es decir: en sandbox el módulo habla contra un Azure de
> Correos, no contra el dominio de Correos.

**Rutas sobre `urlApi`** (todas confirmadas por las llamadas a `requestRestCall()`):

| Ruta | Método | Para qué | Línea |
|---|---|---|---|
| `/preregister/delivery` | POST | Alta de expedición | `:585`, `:1138` |
| `/preregister/delivery/annulment` | POST | Anular expedición | `:710` |
| `/labels/print/labels` | POST | Etiquetas (y CN23) | `:1207`, `:1245` |
| `/labels/print/documents` | POST | Documentación de aduanas | `:1247` |
| `/requests` | POST | Alta de recogida | `:822` |
| `/requests/cancel/<id>` | POST | Anular recogida | `:862` |
| `/requests/<id>` | POST | Consultar recogida | `:907` |
| `/terminals/homepaqs?postalCode=<cp>` | GET | Buscar HomePaq | `:1358` |
| `/units/operative-unit` | — | Oficinas (se menciona en la traza, `:231`) | `:231` |
| **`/track/search-continuous-trace/<numero>`** | **GET** | **Seguimiento** | `:1479` |

### 1.2 Correos Express (CEX) — `classes/Apis/CorreosOficialCEXRest.php`

Cada llamada elige su URL a mano según el entorno:

| Qué hace | PRO | PRE |
|---|---|---|
| Grabar envío | `https://www.cexpr.es/wspsc/apiRestGrabacionEnviok8s/json/grabacionEnvio` | `https://www.test.cexpr.es/wspsc/apiRestGrabacionEnviok8s/json/grabacionEnvio` |
| **Seguimiento** | `https://www.cexpr.es/wspsc/apiRestSeguimientoEnviosk8s/json/seguimientoEnvio` | `https://www.test.cexpr.es/wspsc/apiRestListaEnvios/json/listaEnvios` |
| Etiqueta | `https://www.cexpr.es/wspsc/apiRestEtiquetaTransporte/json/etiquetaTransporte` | `https://www.test.cexpr.es/wspsc/apiRestEtiquetaTransporte/json/etiquetaTransporte` |
| Grabar recogida | `https://www.cexpr.es/wsps/apiRestGrabacionRecogidaEnviok8s/json/grabarRecogida` | `https://www.test.cexpr.es/wsps/apiRestGrabacionRecogidaEnviok8s/json/grabarRecogida` |
| Anular recogida | `https://www.cexpr.es/wsps/apiRestGrabacionRecogidaEnviok8s/json/anularRecogida` | `https://www.test.cexpr.es/wsps/apiRestGrabacionRecogidaEnviok8s/json/anularRecogida` |
| Consultar recogida | `https://www.cexpr.es/wspsc/apiRestSeguimientoRecogidak8s/json/seguimientoRecogida` | `https://www.test.cexpr.es/wsps/apiRestSeguimientoRecogidak8s/json/seguimientoRecogida` |
| Oficinas | `https://www.cexpr.es/wspsc/apiRestOficina/v1/oficinas/listadoOficinasCoordenadas` | (la misma) |
| PUDO | `https://www.cexpr.es/wspsc/apiRestInterfacePuntosEntrega/json/consultPudo` | `https://www.test.cexpr.es/wspsc/apiRestInterfacePuntosEntrega/json/consultPudo` |

Líneas: `:119-121`, `:231-233`, `:493-495`, `:536-538`, `:606-608`, `:806-808`, `:842-844`,
`:932-937`. **Ojo**: `wspsc` y `wsps` alternan según el servicio; no es una errata.

> **En PRE el seguimiento apunta a `apiRestListaEnvios/json/listaEnvios`, no a
> `seguimientoEnvio`** (`:806-809`). Son dos servicios distintos con dos respuestas distintas.

### 1.3 Páginas públicas de seguimiento

- Correos: `https://www.correos.es/es/es/herramientas/localizador/envios/detalle?tracking-number=@`
  (`classes/CorreosOficialReturnsMail.php:229`)
- Correos Express: `https://s.correosexpress.com/c?n=@` (`:235`) y `https://s.correosexpress.com/`
  (`:187`)

---

## 2. Autenticación

### 2.1 Correos (P3) — OAuth2 `client_credentials`

`classes/Apis/CorreosOficialRest.php:74-140`:

```
POST  https://apioauthcid.correos.es/Api/Authorize/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=<CorreosClientID del comercio>
&client_secret=<CorreosSecretID descifrado>
&scope=AP3 LBS RCG
```

El `scope` es literalmente `'AP3 LBS RCG'` (`:101`), codificado con `PHP_QUERY_RFC3986`.

Respuesta: `access_token` (OAuth2 estándar) o, en algunas versiones, `idToken` — el módulo acepta
los dos (`:127`). El token es un JWT y se cachea **en memoria del proceso**, indexado por
`md5($clientId)` (`:30`, `:77-81`), comprobando la caducidad con `isJwtExpired()`.

> **Aviso explícito del propio código** (`:26-32`): *«Never store this JWT in `$_SESSION`: that
> array is Symfony's employee session (CSRF / BO login). Writing it there can invalidate admin
> tokens mid-request.»* Es decir: **no guardar el token en la sesión de PrestaShop**.

Cada llamada al API lleva (`:168-198`):

```
client_id: <valor fijo de la app del módulo, en base64 en el código>
client_secret: <valor fijo de la app del módulo, en base64 en el código>
Content-Type: text/plain
Accept: application/json
Authorization: Bearer <access_token>
```

**Sí: `Content-Type: text/plain` aunque el cuerpo sea JSON.** Está así en `:171`, y las llamadas
funcionan. No «corregirlo» sin probar.

El `client_id` / `client_secret` de las **cabeceras** son de la aplicación del módulo, fijos y
codificados en base64 dentro del código (`CorreosOficialRest.php:169-170`, y el `client_id` en
claro en `CorreosOficialSGARest.php:15`). No son del comerciante; los del comerciante son los que
van en el cuerpo del token.

### 2.2 Correos Express — HTTP Basic

`classes/Apis/CorreosOficialCEXRest.php:77-91`:

```php
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
curl_setopt($ch, CURLOPT_USERPWD, $client['CEXUser'] . ':' . $cexPassword);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/json',
    'Content-Length: ' . strlen(json_encode($data)),
));
```

Sin token, sin OAuth. Usuario y contraseña en cada petición.

---

## 3. Dónde están las credenciales del comerciante

### 3.1 En `ps_configuration`: UNA sola clave

```
CORREOS_OFICIAL_SANDBOX_MODE    1 = PRE, 0 = PRO
```

(`classes/Apis/CorreosOficialRest.php:41`, `CorreosOficialCEXRest.php:44`,
`CorreosOficialSGARest.php`). **Nada más.**

### 3.2 Las credenciales: tabla `ps_correos_oficial_codes`

`models/CorreosOficialCode.php:66-86`. Columnas literales:

```
id
customer_code      código de cliente (si tiene 8 dígitos, se le antepone '99', :91-98)
company            'Correos' | 'CEX'   (varchar 7)
CorreosContract
CorreosCustomer
CorreosKey
CorreosUser
CorreosPassword    CIFRADO   (varchar 1024)
CorreosOv2Code
CorreosClientID    client_id de CorreosID
CorreosSecretID    CIFRADO   (varchar 1024) — es el client_secret
CEXCustomer        codigoCliente de Correos Express
CEXUser
CEXPassword        CIFRADO   (varchar 1024)
id_shop
```

Lectura: `CorreosOficialCode::getAllCodes($id_shop)` (`:102-120`).

**El cifrado** (`classes/CorreosOficialCrypto.php:79-120`):

- Prefijo `psenc:` + `PhpEncryptionCore(_NEW_COOKIE_KEY_)`.
- `_NEW_COOKIE_KEY_` es la clave de cookies **de esa tienda**. Fuera de ella no se descifra nada.
- Hay un formato heredado sin prefijo (`isLegacyEncrypted()`, `:22-42`) que también se acepta.
- `decrypt()` devuelve el valor tal cual si no parece cifrado (`:118`), así que sirve para los dos
  formatos y para valores en claro.

Para un módulo nuevo: **llamar a `CorreosOficialCrypto::decrypt()` del propio módulo oficial**
(está en el espacio de nombres `CorreosOficial\Classes`), o replicar
`(new PhpEncryptionCore(_NEW_COOKIE_KEY_))->decrypt(substr($v, 6))` tras quitar el prefijo `psenc:`.
`PhpEncryptionCore` es una clase **del núcleo de PrestaShop**, no de Composer.

### 3.3 La configuración: tabla `ps_correos_oficial_configuration`

`models/CorreosOficialConfig.php:28-36` — pares `name` / `value` / `type` / `id_shop`.
Se lee con `CorreosOficialConfig::getValueByName($name, $id_shop)` (`:46-75`), que si no encuentra
la fila de esa tienda **cae a la primera fila que haya de cualquier tienda** (`:66-72`). En
multitienda eso puede devolver el valor de otra tienda sin avisar.

**Lista literal de los `name` que usa el módulo** (extraídos de todas las llamadas a
`getValueByName`):

```
Estados de envío → id_order_state
  ShipmentPreregistered   ShipmentInProgress   ShipmentDelivered
  ShipmentCanceled        ShipmentReturned
Seguimiento automático
  ActivateAutomaticTracking   CronInterval   CronLastExecutionTime
Etiqueta
  DefaultLabel   ChangeLogoOnLabel   UploadLogoLabels   LabelObservations
  LabelAlternativeText   ShowLabelData   CustomerAlternativeText
Dimensiones y peso por defecto
  ActivateDimensionsByDefault   DimensionsByDefaultHeight
  DimensionsByDefaultLarge      DimensionsByDefaultWidth
  ActivateWeightByDefault       WeightByDefault   DefaultPackages
Aduanas
  UseProductCustomsData   DefaultCustomsDescription   CountryOriginByDefault
  CountryFeatureId   HSFeatureId   MappedHsFeature   MappedOriginFeature
  ShippCustomsReference
Tarifas
  Tariff   TariffByDefault   TariffDescription   TariffRadio
SGA (almacén)
  ActivateSGA   SGACustomer   SGAOwner   SGAStore   SGAProcessStatus
  SGAUpdateStock   SGAOrderUpdateStock   SGAStockCronInterval
  SGAStockCronLastExecutionTime   SGAOrderStatusCronInterval
  SGAOrderStatusTracking   SGAOrderStatusTrackingCronInterval
  SGAOrderStatusTrackingCronLastExecutionTime   SGAOrderStatusTrackingDays
  SGAOrderStatusTrackingEX   SGAOrderStatusTrackingPE   SGAOrderStatusTrackingError
  SGA_STATUS_OK   SGA_STATUS_KO   SGA_STATUS_CANCELLED   SGA_STATUS_PREPARE
Otros
  ActivateMarketplace   CashOnDeliveryMethod   BankAccNumberAndIBAN
  GoogleMapsApi   GDPR   UseModuleFeatures   CorreosModify
  AgreeToAlterReferences   ShowShippingStatusProcess
```

### 3.4 Resto de tablas del módulo

`correos_oficial_carriers_products`, `correos_oficial_codes_actives`,
`correos_oficial_customs_description`, `correos_oficial_orders`,
`correos_oficial_pickups_returns`, `correos_oficial_products`,
`correos_oficial_products_shop`, `correos_oficial_requests`, `correos_oficial_returns`,
`correos_oficial_saved_orders`, `correos_oficial_saved_returns`, `correos_oficial_senders`,
`correos_oficial_sga_orders_log`, `correos_oficial_sga_orders_status`,
`correos_oficial_ws_status`.

`correos_oficial_ws_status` es la tabla heredada con **692 filas** de códigos de evento; el módulo
3.0.0 ya no la consulta en ejecución: la convirtió en el array constante de `StatusMapper`
(`classes/Cron/StatusMapper.php:21-33`).

---

## 4. Detectar el módulo

```php
if (Module::isInstalled('correosoficial') && Module::isEnabled('correosoficial')) {
    $idShop = (int) Context::getContext()->shop->id;
    $codigos = Db::getInstance(_PS_USE_SQL_SLAVE_)->executeS(
        'SELECT * FROM `' . _DB_PREFIX_ . 'correos_oficial_codes` WHERE `id_shop` = ' . $idShop
    );
    $codigos = is_array($codigos) ? $codigos : array();   // executeS devuelve false si no hay filas
}
```

Nombre en `ps_module`: **`correosoficial`** (`config.xml:3`).

**Cómo saber si un contrato de Correos sirve** (`classes/CorreosOficialApiRouter.php:153-157`):

```php
$clientId = trim((string) $codigo['CorreosClientID']);
$sirve = ($clientId !== '' && strtolower($clientId) !== 'n/a');
```

Si no lo tiene, el contrato **está sin migrar a CorreosID** y el API P3 lo rechaza. El módulo da
ese error literal: *«The contract needs migration to CorreosID before it can be used.»*
(`:102`, `:113`).

---

## 5. Seguimiento

### 5.1 Correos (P3)

`classes/Apis/CorreosOficialRest.php:1469-1516`:

```
GET  <urlApi>/track/search-continuous-trace/<numero urlencode>
Authorization: Bearer <token>
```

Antes de mandarlo, el módulo **quita todos los espacios** del número
(`preg_replace('/\s+/', '', trim(...))`, `:1477`).

Respuesta: **un array**, se usa `[0]`, y de ahí:

- `events[]` — cada uno con `eventCode` (`StatusMapper.php:31-33`)
- `error.codError` / `error.desError`

Códigos de retorno que el módulo da por buenos: `codError` igual a `'0'` o `'3'` (`:1506-1509`).
Y si ya vienen `events`, los devuelve aunque el error parezca raro (`:1502-1504`).

### 5.2 Correos Express

`classes/Apis/CorreosOficialCEXRest.php:805-834`:

```json
POST https://www.cexpr.es/wspsc/apiRestSeguimientoEnviosk8s/json/seguimientoEnvio
{ "codigoCliente": "<CEXCustomer>", "dato": "<numero>", "idioma": "ES" }
```

Respuesta (documentada en `classes/Cron/TrackingCronService.php:386-393`):

```
codigoRetorno            int     200 = OK
mensajeRetorno           objeto
  ->estadoEnvios         array
    [N]->codigoEstado    int     ← el código
    [N]->descripcionEstado string
```

Se coge el **último** elemento de `estadoEnvios` (`TrackingCronService.php:343-350`: `end()`).

### 5.3 El mapa de códigos: `StatusMapper`

`classes/Cron/StatusMapper.php`. Convierte las **692 filas** de la tabla heredada
`correos_oficial_ws_status` en un array constante en PHP, sin consultas.

**Cinco estados semánticos** (`:38-42`), cada uno con su clave en
`ps_correos_oficial_configuration` (`:46-53`):

| Estado | Clave de configuración | Estado de pedido por defecto |
|---|---|---|
| `preregistered` | `ShipmentPreregistered` | 900 |
| `in_progress` | `ShipmentInProgress` | 904 |
| `delivered` | `ShipmentDelivered` | 903 |
| `canceled` | `ShipmentCanceled` | 901 |
| `returned` | `ShipmentReturned` | 902 |

**Terminales** (no se vuelve a consultar): `delivered`, `canceled`, `returned` (`:56-61`).

**Cómo funciona el mapa** (`:63-71`): el array `EVENT_MAP` **solo lista las excepciones**.
Cualquier código que no esté en él es `in_progress`. Claves numéricas = `codigoEstado` de CEX y
códigos numéricos heredados de Correos; claves alfanuméricas = `eventCode` del P3.

Muestra real de códigos, sacados del propio array:

| Estado | Códigos numéricos (CEX / heredados) | `eventCode` del P3 (muestra) |
|---|---|---|
| **PRERREGISTRADO** | `1` | `A020000R`, `A090000V`, `A150000R`, `O040000R`, `SR01000V`, `SR05000V`, `SR070B0R`, `SR080A0R`, `SR09000R`, `X010000V`, `X240000V`, `Z010PF0R`, `Z130000R` |
| **ENTREGADO** | `12` | `A170000V`, `E010670V`, `H010710V`, `H300030V`…`H300070V`, `I010000V`, `I010110V`…`I010130V`, `I010400V`, `I011010V`…`I011030V`, `I01E030V`, `I01H010V`…`I01H230V`, `I240300V`, `R010750V`, `X090030R`, `X120000V`, `X290030R`, `X340000V`, `X350000V`, `X380000V` |
| **ANULADO** | `13`, `14`, `15`, `16`, `19`, `31` | `A040000R`, `A060000R`, `E070000R`, `E130000R`, `E140000R`, `E150000R`, `E230000R`, `E23E500R`, `E310000R`… |
| **DEVUELTO** | — | (resto del array) |
| **EN CURSO** | todo lo demás | todo lo demás |

**La lista completa está en `correosoficial/classes/Cron/StatusMapper.php`.** Es el mapa oficial
de Correos y ahí se lee entero; no tiene sentido copiarlo a mano.

### 5.4 Cómo se elige qué API consultar

`classes/Cron/TrackingCronService.php:113`: recorre `['Correos', 'CEX']` y para cada uno busca sus
pedidos. El `eventCode` sale de `getOrderStatusP3()` o de `fetchCEXEventCode()` según el tipo
(`:191-192`).

---

## 6. Etiquetas

### 6.1 Correos (P3)

`classes/Apis/CorreosOficialRest.php:1195-1236`:

```json
POST <urlApi>/labels/print/labels
{
  "application": "PRS",
  "documentationType": 1,          // 0 = ambos, 1 = etiqueta, 2 = CN23
  "print": {
    "labelOrderType": 2,
    "labelFormat": 2,              // 1 = XML, 2 = PDF, 3 = ZPL
    "labelPrintMode": 2,           // 1 = A4, 2 = térmica
    "labelPrintInitialPosition": 1,
    "shipments": [ … ]
  }
}
```

Respuesta: campo `pdf` en **base64**; el módulo hace `base64_decode()` (`:1224`).
La documentación de aduanas (CN23) va por `/labels/print/documents` (`:1247`).

### 6.2 Correos Express

`classes/Apis/CorreosOficialCEXRest.php:860-921`:

```json
POST https://www.cexpr.es/wspsc/apiRestEtiquetaTransporte/json/etiquetaTransporte
{
  "keyCli": "<customer_code>",
  "nenvio": "<exp_number>",
  "posicionEtiqueta": 0,
  "tipo": 1,                       // 1 = térmica/adhesiva, 3 = 3 por A4
  "logoCliente": ""
}
```

Respuesta: `listaEtiquetas[]` con cada etiqueta en **base64**
(`array_map('base64_decode', $listaEtiquetas)`, `:919`), más `codErr` / `desErr`.
`codErr` distinto de `'0'` es error (`:898-912`); visto en el código: **`-10`**.

### 6.3 Constantes de etiqueta

`config/label_constants.php:10-34`:

```
LABEL_TYPE_ADHESIVE   = 0     LABEL_FORMAT_STANDAR = 0
LABEL_TYPE_HALF       = 1     LABEL_FORMAT_3A4     = 1
LABEL_TYPE_THERMAL    = 2     LABEL_FORMAT_4A4     = 2
CEX_LABEL_THERMAL_ADHESIVE = 1
CEX_LABEL_3A4              = 3
```

En pantalla solo se ofrecen «Térmica» y «Adhesiva»: «Medio folio» está comentado (`:48-51`).

---

## 7. Número de seguimiento

- Correos: `shipments[0].shipmentCode`, o si no hay, `packages[0].packageCode`
  (`CorreosOficialRest.php:668-671`). Cada bulto tiene su `packageCode` (`:662`).
- CEX: `listaBultos[N].codUnico` (`CorreosOficialCEXRest.php:476`, `:796`).
- Se escribe en `ps_order_carrier.tracking_number`.

**Formato CONFIRMADO para Correos** (`classes/Cron/TrackingCronService.php:371`):

```php
preg_match('/([A-Z]{2}[A-Z0-9]{10,30})/i', $normalized, $m)
```

**Dos letras seguidas de 10 a 30 alfanuméricos.** Ejemplos reales que aparecen en el código:
`PQ4G…` (`:358`) y `PY43B40720207850128042X` (`CorreosOficialRest.php:1559`).

Antes de comparar, el módulo **limpia el número** (`TrackingCronService.php:357-375`): quita un
prefijo `Expedición:`, `Envío:`, `tracking:` o `localizador:` (con o sin tilde), quita los espacios
y lo pasa a mayúsculas. Hace falta porque los pedidos de marketplace llegan con el número dentro de
una frase.

**NO CONFIRMADO:** el formato del `codUnico` de Correos Express.

---

## 8. Trampas vistas en este código

1. **HTTP 200 con error dentro.** El alta devuelve 200 con `shipments[0].validationErrorCount > 0`
   y sin `packages` (`CorreosOficialRest.php:626-640`). Hay que comprobarlo explícitamente.
2. **`Content-Type: text/plain` con cuerpo JSON** en las llamadas a P3 (`:171`). Es así a
   propósito; no cambiarlo sin probar.
3. **`CORREOS_BASE_LOCATION` no está definida en ningún sitio.** Se usa en
   `CorreosOficialRest.php:1565` (método `location()`, que llama `getOrderStatus()`) y **no hay ni
   un `define()` de esa constante en todo el módulo**. En PHP 8 eso es un `Error: Undefined
   constant` fatal. Solo se llega por el camino heredado (`getOrderStatus`, `:1519`); el camino
   vivo es `getOrderStatusP3()`. **No usar `getOrderStatus()` como referencia.**
4. **Las credenciales están cifradas con la clave de cookies de la tienda.** Un volcado de la base
   de datos llevado a otra tienda no sirve: hay que volver a introducirlas.
5. **`getValueByName()` cae a otra tienda.** Si no encuentra la fila de `id_shop`, devuelve la
   primera que haya de cualquier tienda (`models/CorreosOficialConfig.php:66-72`). En multitienda
   se puede leer la configuración de la tienda de al lado sin enterarse.
6. **El código de cliente de 8 dígitos lleva `99` delante.** `normalizeCustomerCode()`
   (`models/CorreosOficialCode.php:95-102`) antepone `'99'` cuando tiene exactamente 8 caracteres.
   Si un módulo nuevo lo manda sin normalizar, Correos no lo reconoce.
7. **El mensaje de error de CEX viene en ISO-8859-1.** El módulo lo convierte a UTF-8 a mano
   (`CorreosOficialCEXRest.php:886`). Sin esa conversión, las tildes salen rotas.
8. **TLS sin verificar** en las dos API (`CorreosOficialRest.php:213`,
   `CorreosOficialCEXRest.php:84`).
9. **En PRE el seguimiento de CEX apunta a otro servicio** (`listaEnvios` en vez de
   `seguimientoEnvio`, `:806-808`), con otra respuesta. Lo que funcione en pruebas puede no valer
   en producción.
10. **Contratos sin migrar a CorreosID.** Si `CorreosClientID` está vacío o vale `n/a`, el API P3
    no se puede usar (`CorreosOficialApiRouter.php:153-157`). Hay que comprobarlo antes de intentar
    nada.
11. **Timeout de 15 segundos** en P3 (`CorreosOficialRest.php:92`, `:210`). En un cron con muchos
    pedidos, hay que contar con eso.
12. **No meter el JWT en `$_SESSION`** — aviso del propio código, §2.1.

---

## 9. Fragmento PHP listo para copiar (estructura legacy, sin Composer, cURL nativo)

```php
<?php
/**
 * Seguimiento de Correos (P3) reutilizando las credenciales del modulo oficial
 * 'correosoficial'. Sin Composer, sin namespace, cURL nativo.
 * PhpEncryptionCore es del NUCLEO de PrestaShop, no de Composer.
 */
if (!defined('_PS_VERSION_')) {
    exit;
}

class MiCorreosTracking
{
    const PREFIJO_CIFRADO = 'psenc:';

    /** @var array token en memoria del proceso, indexado por md5(clientId) */
    private static $tokenCache = array();

    /** Contratos del comercio guardados por el modulo oficial. */
    public static function getCodigos($company = 'Correos', $idShop = null)
    {
        if ($idShop === null) {
            $idShop = (int) Context::getContext()->shop->id;
        }

        $filas = Db::getInstance(_PS_USE_SQL_SLAVE_)->executeS(
            'SELECT * FROM `' . _DB_PREFIX_ . 'correos_oficial_codes`
              WHERE `id_shop` = ' . (int) $idShop . '
                AND `company` = "' . pSQL($company) . '"'
        );

        // executeS() devuelve FALSE si no hay filas: (array) false seria array(0 => false).
        return is_array($filas) ? $filas : array();
    }

    /** Descifra un secreto guardado por el modulo oficial. */
    public static function descifrar($valor)
    {
        if ($valor === null || $valor === '') {
            return '';
        }

        $valor = (string) $valor;
        if (strpos($valor, self::PREFIJO_CIFRADO) !== 0) {
            return $valor;   // valor en claro o formato heredado que no sabemos tratar
        }
        if (!defined('_NEW_COOKIE_KEY_') || !_NEW_COOKIE_KEY_) {
            return '';
        }

        try {
            $enc = new PhpEncryptionCore(_NEW_COOKIE_KEY_);

            return (string) $enc->decrypt(Tools::substr($valor, Tools::strlen(self::PREFIJO_CIFRADO)));
        } catch (Exception $e) {
            return '';
        }
    }

    public static function esSandbox()
    {
        return (int) Configuration::get('CORREOS_OFICIAL_SANDBOX_MODE', 0) === 1;
    }

    public static function urlApi()
    {
        return self::esSandbox()
            ? 'https://api1.correospre.es/logistics/tradeinout/api/v1'
            : 'https://api1.correos.es/logistics/tradeinout/api/v1';
    }

    public static function urlToken()
    {
        return self::esSandbox()
            ? 'https://azam-t-correosid-a0-svc-netcore-oauthservices-01.azurewebsites.net/Api/Authorize/token'
            : 'https://apioauthcid.correos.es/Api/Authorize/token';
    }

    /** Bearer de CorreosID. NUNCA guardarlo en $_SESSION. */
    public static function getToken($clientId, $clientSecret)
    {
        $clave = md5((string) $clientId);
        if (isset(self::$tokenCache[$clave])) {
            return self::$tokenCache[$clave];
        }

        $ch = curl_init();
        curl_setopt_array($ch, array(
            CURLOPT_URL => self::urlToken(),
            CURLOPT_CUSTOMREQUEST => 'POST',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 15,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_POSTFIELDS => http_build_query(array(
                'grant_type' => 'client_credentials',
                'client_id' => $clientId,
                'client_secret' => $clientSecret,
                'scope' => 'AP3 LBS RCG',
            ), '', '&', PHP_QUERY_RFC3986),
            CURLOPT_HTTPHEADER => array('Content-Type: application/x-www-form-urlencoded'),
        ));
        $raw = curl_exec($ch);
        $err = curl_error($ch);
        curl_close($ch);

        if ($err || $raw === false || $raw === '') {
            return false;
        }

        $json = json_decode($raw, true);
        if (!is_array($json)) {
            return false;
        }

        $token = isset($json['access_token'])
            ? $json['access_token']
            : (isset($json['idToken']) ? $json['idToken'] : null);

        if (!$token) {
            return false;
        }
        self::$tokenCache[$clave] = $token;

        return $token;
    }

    /** Limpia el numero como hace el modulo oficial (pedidos de marketplace). */
    public static function normalizarNumero($numero)
    {
        $n = trim((string) $numero);
        if ($n === '') {
            return '';
        }
        $n = preg_replace('/^(expedici[oó]n|env[ií]o|tracking|localizador)\s*:\s*/iu', '', $n);
        $n = preg_replace('/\s+/', '', $n);
        if (!is_string($n) || $n === '') {
            return '';
        }
        if (preg_match('/([A-Z]{2}[A-Z0-9]{10,30})/i', $n, $m)) {
            return Tools::strtoupper($m[1]);
        }

        return Tools::strtoupper($n);
    }

    /**
     * Ultimo eventCode del envio, o false.
     * Camino VIVO: /track/search-continuous-trace (NO getOrderStatus, que usa
     * una constante inexistente y revienta en PHP 8).
     *
     * @return string|false
     */
    public static function getUltimoEventCode($numeroSeguimiento, $codigo = null)
    {
        if ($codigo === null) {
            $codigos = self::getCodigos('Correos');
            if (empty($codigos[0])) {
                return false;
            }
            $codigo = $codigos[0];
        }

        $clientId = isset($codigo['CorreosClientID']) ? trim((string) $codigo['CorreosClientID']) : '';
        if ($clientId === '' || Tools::strtolower($clientId) === 'n/a') {
            return false;   // contrato sin migrar a CorreosID
        }

        $clientSecret = self::descifrar(isset($codigo['CorreosSecretID']) ? $codigo['CorreosSecretID'] : '');
        if ($clientSecret === '') {
            return false;
        }

        $token = self::getToken($clientId, $clientSecret);
        if (!$token) {
            return false;
        }

        $numero = self::normalizarNumero($numeroSeguimiento);
        if ($numero === '') {
            return false;
        }

        $ch = curl_init();
        curl_setopt_array($ch, array(
            CURLOPT_URL => self::urlApi() . '/track/search-continuous-trace/' . urlencode($numero),
            CURLOPT_CUSTOMREQUEST => 'GET',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 15,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_HTTPHEADER => array(
                'Content-Type: text/plain',   // si, text/plain: es lo que espera el API
                'Accept: application/json',
                'Authorization: Bearer ' . $token,
            ),
        ));
        $raw = curl_exec($ch);
        $err = curl_error($ch);
        curl_close($ch);

        if ($err || $raw === false || $raw === '') {
            return false;
        }

        $json = json_decode($raw, true);
        if (!is_array($json) || !isset($json[0])) {
            return false;
        }

        $eventos = isset($json[0]['events']) && is_array($json[0]['events']) ? $json[0]['events'] : array();
        if (empty($eventos)) {
            return false;
        }

        $ultimo = end($eventos);

        return isset($ultimo['eventCode']) ? (string) $ultimo['eventCode'] : false;
    }
}
```

Uso, apoyándose en el mapa oficial de códigos del propio módulo:

```php
$evento = MiCorreosTracking::getUltimoEventCode('PQ4G1234567890');
if ($evento !== false) {
    // Traducir con el mapa del modulo oficial (classes/Cron/StatusMapper.php):
    // 'preregistered' | 'in_progress' | 'delivered' | 'canceled' | 'returned'
}
```

---

## 10. Qué NO se ha podido confirmar leyendo el código

- **Formato del `codUnico` de Correos Express** (longitud, prefijo): no se valida.
- **Tabla de códigos de error de P3** (los `error[].errorCode` / `description`): no hay lista; solo
  llega el texto.
- **Códigos de error de CEX** más allá de los vistos: `18005` (lo inventa el módulo cuando la
  respuesta no es un array, `CorreosOficialCEXRest.php:877`), `-10` (`:901`) y `401`
  (credenciales, `:59-64`). No hay tabla.
- **Esquema completo del alta de expedición** (`/preregister/delivery`): el cuerpo se monta a lo
  largo de cientos de líneas de `CorreosOficialRest.php`; no hay esquema aparte.
- **Los `client_id`/`client_secret` fijos de la aplicación** (`:169-170`) son de Correos, no del
  comerciante. Están en base64 en el código; no se reproducen aquí.
- **Significado individual de los 692 códigos de evento.** `StatusMapper` los agrupa en cinco
  estados, pero no dice qué significa cada uno. La descripción legible viene en
  `descripcionEstado` (CEX) o en el propio evento (P3), no en una tabla del módulo.
- **`correos_oficial_ws_status`**: la tabla existe y se crea al instalar, pero el módulo 3.0.0 ya
  no la consulta. Si hace falta el texto de cada código, ahí está.
