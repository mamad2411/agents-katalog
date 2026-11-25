---
name: prestashop-transportistas-espana
description: Índice de los seis transportistas españoles integrados en PrestaShop (SEUR, MRW, GLS/ASM, Correos y Correos Express, Envialia). Dice cuál tiene API, de qué tipo, qué credenciales pide y DÓNDE las guarda cada módulo oficial, para que un módulo nuevo reutilice las credenciales que el comerciante ya tiene puestas en vez de pedírselas otra vez. Invocar SIEMPRE el primero cuando haya que hablar con un transportista, adivinar el transportista de un número de seguimiento, o leer credenciales ya configuradas en la tienda.
---

# Transportistas de España en PrestaShop — índice

Todo lo que hay aquí sale de **leer los seis módulos oficiales reales** que el usuario tiene en
`transportes`. Cada dato lleva su fichero y su
línea. Lo que no se ha podido confirmar leyendo ese código está marcado como **NO CONFIRMADO**.

> **Los módulos de `transportes\` son de solo lectura.** Son del usuario y están en producción:
> se leen para saber cómo hablar con cada transportista, **nunca se modifican**.

> **Esto es material de CONSULTA.** No es autoridad sobre estructura de carpetas ni convenciones.
> Si algo choca con el `CLAUDE.md` del proyecto, gana el `CLAUDE.md`.

---

## 1. Tabla resumen

| Transportista | Módulo (`ps_module.name`) | Versión leída | ¿API? | Tipo | Autenticación | Skill |
|---|---|---|---|---|---|---|
| **SEUR** | `seur` | 2.5.26 | Sí | **REST/JSON** (v2) + SOAP heredado (v1) | OAuth2 `password`: client_id + client_secret + usuario + contraseña → Bearer | `prestashop-carrier-seur` |
| **MRW** | `mrwcarrier` (+ `mrwtracking`) | 8.0.7 / 3.8.1 | Sí | **SOAP 1.1** (`.asmx`) | Cabecera SOAP `AuthInfo`: franquicia + abonado + departamento + usuario + contraseña | `prestashop-carrier-mrw` |
| **GLS / ASM** | `glsshipping` | 3.7.20 | Sí | **SOAP 1.2** (`.asmx`, XML a pelo por cURL) | **Un solo GUID** (`uidcliente`), sin usuario ni contraseña | `prestashop-carrier-gls` |
| **Correos** | `correosoficial` | 3.0.0 | Sí | **REST/JSON** | OAuth2 `client_credentials` → Bearer + `client_id`/`client_secret` de la app fijos en cabecera | `prestashop-carrier-correos` |
| **Correos Express (CEX)** | `correosoficial` (mismo módulo) | 3.0.0 | Sí | **REST/JSON** | **HTTP Basic** (usuario + contraseña CEX) | `prestashop-carrier-correos` |
| **Envialia** | `envialiacarrier` | 1.0.10 | Sí | **SOAP 1.1** (RemObjects, XML a pelo por cURL) | Login que devuelve un **id de sesión** que viaja en `ROClientIDHeader` | `prestashop-carrier-envialia` |

**Los seis tienen API.** Ninguno se limita a enlaces de seguimiento.

Los dos módulos de MRW se reparten el trabajo: `mrwcarrier` crea envíos y etiquetas,
`mrwtracking` solo consulta estados y **lee una clave de configuración de `mrwcarrier`**
(`MRWCARRIER_AFTER_SENDING_MRW`, `mrwtracking.php:602`) — precedente real de reutilización de
configuración entre módulos, que es justo lo que este skill busca.

---

## 2. LO IMPORTANTE: dónde está guardada cada credencial

Un módulo nuevo **no tiene que volver a pedirle las credenciales al comerciante**. Si el módulo
oficial del transportista ya está instalado, están aquí.

### 2.1 En `ps_configuration` (se leen con `Configuration::get()`)

**SEUR** — `seur/classes/SeurLib.php:668-674`, valores por defecto en `seur/seur.php:236-267`:

```
SEUR2_API_CLIENT_ID          client_id de la API
SEUR2_API_CLIENT_SECRET      client_secret de la API
SEUR2_API_USERNAME           usuario de la API
SEUR2_API_PASSWORD           contraseña de la API
SEUR2_TOKEN_API              Bearer en caché (por tienda)
SEUR2_TOKEN_API_EXPIRES_AT   caducidad del Bearer (timestamp)
SEUR2_MERCHANT_NIF_DNI       NIF del comercio (obligatorio al consultar el seguimiento)
SEUR2_URLWS_TOKEN            URL del token
SEUR2_URLWS_E                URL de seguimiento
SEUR2_URLWS_ET               URL de alta de expedición
SEUR2_URLWS_LABELS           URL de etiquetas
```

El **CCC/franquicia** NO está en `ps_configuration`: está en la tabla `ps_seur2_ccc`
(`seur/classes/SeurLib.php:93-97`, campos `ccc` y `franchise`).

**MRW (`mrwcarrier`)** — prefijo `MRWCARRIER_`, construido en `mrwcarrier/mrwcarrier.php:44`
como `strtoupper($this->name) . '_'`:

```
MRWCARRIER_ENTORNO             'mrw_pre' | 'mrw_pro'
MRWCARRIER_FRANQUICIA
MRWCARRIER_ABONADO
MRWCARRIER_USUARIO
MRWCARRIER_PASSWORD
MRWCARRIER_CARRIER_ID_MRW      id(s) del transportista MRW
MRWCARRIER_ACTIVE_DEBUG_MRW
MRWCARRIER_BEFORE_SENDING_MRW  estado de pedido que dispara el envío
MRWCARRIER_AFTER_SENDING_MRW   estado al que pasa después
MRWCARRIER_CRON_TOKEN
MRWCARRIER_ALLOW_POINT_DELIVERY
MRWCARRIER_SERVICE_MRW / MRWCARRIER_SERVICE_MRW_INT
```

**OJO:** esas claves de `ps_configuration` son el juego *heredado*. El juego **vivo** está en la
tabla `ps_mrwcarrier_subs` (multiabonado), ver §2.2.

**MRW (`mrwtracking`)** — prefijo `MRWTRACKING_` (`mrwtracking/mrwtracking.php:25`):

```
MRWTRACKING_WS_TRACKING    por defecto https://seguimiento.mrw.es/swc/wssgmntnvs.asmx (:121)
MRWTRACKING_FRANQUICIA
MRWTRACKING_ABONADO
MRWTRACKING_PASSWORD
MRWTRACKING_ACTIVE_DEBUG
MRWTRACKING_FLG_ENTREGADO
```

**GLS** — `glsshipping/glsshipping.php:114-129`, `:1007-1038`:

```
GLS_GUID     LA credencial (uidcliente). Por defecto 15F9A8B5-82AC-4094-99F7-9FD58FD43E9E,
             que es el GUID DE PRUEBAS (:114, :263)
GLS_URL      https://www.asmred.com/websrvs/ecm.asmx?wsdl (:115)
GLS_RCS      Retorno Copia Sellada (:571)
GLS_DORIG    departamento de origen (:590)
GLS_VSEC     valor asegurado (:596)
GLS_SENDER_NAME / GLS_SENDER_ADDRESS / GLS_SENDER_CITY / GLS_SENDER_CP / GLS_SENDER_COUNTRY
GLS_SERVICIO_SELECCIONADO_GLS10 / _GLS14 / _GLS24 / _BUSPAR / _GLSECO / _GLSEBP /
GLS_SERVICIO_SELECCIONADO_GLSSHOPDELINT / _GLSPARCEL   (listas de id_carrier separadas por ';')
GLS_STATUS_SEND / GLS_STATUS_COMPLETED / GLS_STATUS_FAILED
GLS_UPDATE_ORDER_STATUS_SEND / _COMPLETED / _FAILED
GLS_STATE_UPDATE_DAYS / GLS_STATE_UPDATE_FREQUENCY / GLS_CRON_TIME / GLS_DISABLE_STATE_UPDATE
```

**Correos** — en `ps_configuration` solo hay **una** clave
(`correosoficial/classes/Apis/CorreosOficialRest.php:41`):

```
CORREOS_OFICIAL_SANDBOX_MODE   1 = entorno PRE, 0 = PRO
```

Todo lo demás está en tablas propias, ver §2.2.

**Envialia** — `ps_configuration` guarda solo opciones de negocio, **ninguna credencial**.
Claves (prefijo en minúsculas, tal cual): `envialia_bultos`, `envialia_conf_tar`,
`envialia_ecomm_24`, `envialia_ecomm_72`, `envialia_ecomm_ee`, `envialia_ecomm_ww`,
`envialia_env_grat_int`, `envialia_env_grat_pen`, `envialia_estado_pedido`, `envialia_etiqueta`,
`envialia_imp_eti_a4`, `envialia_rem_prev*`, `envialia_seg_red`, `envialia_tarifa_impo`,
`envialia_tarifa_peso`, `envialia_tar_marg`, `envialia_tar_impuesto`.
Las credenciales están en `ps_envialia_config`, ver §2.2.

### 2.2 En tablas propias del módulo (NO en `ps_configuration`)

| Transportista | Tabla | Campos que importan |
|---|---|---|
| **SEUR** | `ps_seur2_ccc` | `cit`, `ccc`, `franchise`, `is_default`, `id_shop` (`seur/sql/install.php:29-49`) |
| **SEUR** | `ps_seur2_order` | `expeditionCode`, `ecbs`, `parcelNumbers`, `label_files` (`SeurLib.php:381-390`) |
| **SEUR** | `ps_seur2_status` | 433 filas `id_status` / `cod_situ` / `grupo` (`seur/sql/install.php:194-205`) |
| **MRW** | `ps_mrwcarrier_subs` | `environment`, `agency`, `subscriber`, `department`, `user`, `password`, `service`, `service_int`, `is_default`, `id_shop` (`mrwcarrier/mrwcarrier.php:447-462`) |
| **MRW** | `ps_mrwcarrier_mrw` | `order_id`, `send_num_mrw` (número de envío), `subscriber`, `service` (`:377-392`) |
| **GLS** | `ps_gls_envios` | `id_envio_order`, `codigo_envio` (código de barras), `url_track`, `num_albaran`, `current_state`, `state_history` (`glsshipping/sql/install.php:28-46`) |
| **Correos** | `ps_correos_oficial_codes` | `CorreosClientID`, `CorreosSecretID`, `CorreosUser`, `CorreosPassword`, `CorreosContract`, `CorreosCustomer`, `CorreosKey`, `CorreosOv2Code`, `CEXCustomer`, `CEXUser`, `CEXPassword`, `id_shop` (`correosoficial/models/CorreosOficialCode.php:66-86`) |
| **Correos** | `ps_correos_oficial_configuration` | pares `name`/`value`/`type`/`id_shop` (`correosoficial/models/CorreosOficialConfig.php:28-36`) |
| **Envialia** | `ps_envialia_config` | `V_COD_AGE` (agencia), `V_COD_CLI` (cliente), `V_COD_CLI_DEP` (departamento), `BL_PASS` (**BLOB cifrado con AES**), `V_URL_WEB`, `V_ID_SESION`, `V_URL_SEG` (`envialiacarrier/sql/install.sql:72-81`) |
| **Envialia** | `ps_envialia_envio` | `id_order`, `V_COD_AGE_CARGO`, `V_COD_AGE_ORI`, `V_ALBARAN`, `V_GUID` (`install.sql:16-24`) |

**Dos credenciales están CIFRADAS y no se leen con un `SELECT` a secas:**

- **Envialia**: `BL_PASS` va con `AES_ENCRYPT`/`AES_DECRYPT` de MySQL y la clave es una constante
  del módulo, `CONST_TOKEN` en `envialiacarrier/clases/ModuleConst.php:15`. Se descifra en SQL:
  `CAST(AES_DECRYPT(BL_PASS, "<CONST_TOKEN>") AS CHAR)` (`clases/EnvialiaConfig.php:13-14`).
- **Correos**: `CorreosPassword`, `CorreosSecretID` y `CEXPassword` llevan el prefijo `psenc:` y
  se descifran con `PhpEncryptionCore(_NEW_COOKIE_KEY_)`, la clave de cookies de la propia tienda
  (`classes/CorreosOficialCrypto.php:79-120`). Fuera de esa tienda no se pueden descifrar.

---

## 3. Detectar que un módulo de transportista está instalado y activo

Lo mismo para los seis; solo cambia el nombre:

```php
if (Module::isInstalled('glsshipping') && Module::isEnabled('glsshipping')) {
    $guid = Configuration::get('GLS_GUID');
}
```

`Module::isEnabled()` respeta la tienda del contexto. Si hace falta comprobarlo sin instanciar
nada (por ejemplo desde un cron), vale un `SELECT`:

```php
$activo = (int) Db::getInstance()->getValue(
    'SELECT ms.id_module
       FROM `'._DB_PREFIX_.'module` m
       JOIN `'._DB_PREFIX_.'module_shop` ms ON ms.id_module = m.id_module
      WHERE m.name = "glsshipping" AND ms.id_shop = '.(int) Context::getContext()->shop->id
);
```

Y para saber si un `id_carrier` concreto es de ese transportista, cada módulo tiene su forma:

| Transportista | Cómo se reconoce su transportista |
|---|---|
| GLS | `ps_carrier.external_module_name = 'glsshipping'`, o el `id_carrier`/`id_reference` dentro de las listas `GLS_SERVICIO_SELECCIONADO_*` separadas por `;` (`glsshipping.php:2928-2952`) |
| MRW | `MRWCARRIER_CARRIER_ID_MRW` (`mrwcarrier.php:103`) |
| Envialia | tabla `ps_envialia_tipo_serv`, columna `ID_CARRIER` (`sql/install.sql:91-94`) |
| SEUR | tabla `ps_seur2_carrier` / `external_module_name = 'seur'` |
| Correos | tabla `ps_correos_oficial_carriers_products` |

---

## 4. Adivinar el transportista por el número de seguimiento

Solo con lo que se puede **confirmar en el código**:

| Transportista | Dónde se guarda | Forma del número | Confirmado en |
|---|---|---|---|
| **Correos** | `ps_order_carrier.tracking_number` | **2 letras + 10 a 30 alfanuméricos** (`PQ4G…`, `PY43B4072…`). La expresión del propio módulo es `/([A-Z]{2}[A-Z0-9]{10,30})/i` | `classes/Cron/TrackingCronService.php:371` |
| **Correos Express** | igual | `codUnico` de cada bulto; **formato no descrito en el código** | `Apis/CorreosOficialCEXRest.php:476` |
| **GLS / ASM** | `ps_order_carrier.tracking_number` y `ps_gls_envios.codigo_envio` | el `codbarras` que devuelve `GrabaServicios`; `varchar(50)`; **formato no descrito en el código** | `glsshipping.php:1870-1874`, `:2080` |
| **MRW** | `ps_orders.shipping_number` + `ps_order_carrier.tracking_number` + `ps_mrwcarrier_mrw.send_num_mrw` | `NumeroEnvio` del WS; `varchar(100)`; **formato no descrito en el código** | `mrwcarrier.php:2796`, `:3092`, `:3109` |
| **SEUR** | `ps_orders.shipping_number` (recortado a 64) + `ps_seur2_order.expeditionCode` / `ecbs` / `parcelNumbers` | `shipmentCode` del API; **formato no descrito en el código** | `classes/SeurLib.php:392-397`, `classes/Label.php:349-351` |
| **Envialia** | `ps_order_carrier.tracking_number` = **`V_COD_AGE_CARGO` + `V_ALBARAN` concatenados** | agencia (hasta 6) + albarán (hasta 10) | `lib/WebService.php:1259`, `:1263-1266` |

**NO CONFIRMADO:** no hay en ninguno de los seis módulos una tabla de prefijos ni una longitud
fija que permita distinguir a ciegas SEUR de MRW de GLS. Lo único fiable es **mirar el
`id_carrier` del pedido** y resolver el transportista con la tabla de §3. La única pista real es
la de Correos (dos letras iniciales), y ni siquiera es exclusiva suya.

---

## 5. Resumen de endpoints (detalle en cada skill)

| Transportista | Producción | Pruebas |
|---|---|---|
| SEUR (v2 REST) | `https://servicios.api.seur.io/pic/v1/…` + token en `https://servicios.api.seur.io/pic_token` | `https://servicios.apipre.seur.io/…` (sustitución en `SeurLib.php:707-710`) |
| SEUR (geolabel) | `https://api.seur.com/geolabel/api/shipment/…` | — |
| MRW envíos | `https://sagec.mrw.es/MRWEnvio.asmx?WSDL` | `https://sagec-test.mrw.es/MRWEnvio.asmx?WSDL` |
| MRW seguimiento | `https://trackingservice.mrw.es/TrackingService.svc?wsdl` y `https://seguimiento.mrw.es/swc/wssgmntnvs.asmx` | `https://trackingservice-test.mrw.es/TrackingService.svc?wsdl` |
| GLS | `https://wsclientes.asmred.com/b2b.asmx` (y `https://www.asmred.com/websrvs/ecm.asmx?wsdl`) | **no hay entorno de pruebas**: se usa el GUID de pruebas contra producción |
| Correos | `https://api1.correos.es/logistics/tradeinout/api/v1` · token `https://apioauthcid.correos.es/Api/Authorize/token` | `https://api1.correospre.es/…` |
| Correos Express | `https://www.cexpr.es/wspsc/…` | `https://www.test.cexpr.es/wspsc/…` |
| Envialia | `<V_URL_WEB>/SOAP`, por defecto `ws.envialia.com/SOAP` | **no hay entorno de pruebas en el código** |

---

## 6. Trampas que valen para todos

1. **HTTP 200 no significa que haya salido bien.** Los cinco transportistas devuelven el error
   dentro del cuerpo con código 200: SEUR en `errors[]`, MRW en `…Result->Estado == 0`, GLS en
   `Servicios/Envio/Resultado/@return != 0`, Correos en `shipments[0].validationErrorCount > 0`,
   Envialia en `intCodError`. Comprobar siempre el cuerpo, nunca solo el código HTTP.
2. **`Db::executeS()` devuelve `false` cuando no hay filas.** `foreach ((array) $filas)` entra una
   vez con `false` dentro y revienta en PHP 8. Siempre `is_array($x) ? $x : array()`.
3. **Todos desactivan la verificación TLS** (`CURLOPT_SSL_VERIFYPEER => false`). Está en el código
   de los cinco. No copiarlo a ciegas en un módulo nuevo.
4. **Multitienda:** SEUR (`ps_seur2_ccc.id_shop`), MRW (`ps_mrwcarrier_subs.id_shop`) y Correos
   (`ps_correos_oficial_codes.id_shop`) guardan credenciales **por tienda**. GLS y Envialia no:
   son globales. Leer siempre con el `id_shop` en la mano.
5. **No lanzar barridos sobre pedidos antiguos.** Los cron de estos módulos ya limitan la ventana
   (GLS con `GLS_STATE_UPDATE_DAYS`, Correos con `SGAOrderStatusTrackingDays`). Un módulo nuevo que
   consulte seguimientos tiene que hacer lo mismo: ventana de 24 h como máximo si de ahí sale un
   correo o un aviso al cliente.

---

## 7. A qué skill ir

- `prestashop-carrier-seur` — SEUR
- `prestashop-carrier-mrw` — MRW (`mrwcarrier` y `mrwtracking`)
- `prestashop-carrier-gls` — GLS / ASM
- `prestashop-carrier-correos` — Correos y Correos Express
- `prestashop-carrier-envialia` — Envialia
