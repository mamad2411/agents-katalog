---
name: prestashop-carrier-envialia
description: API SOAP de Envialia (ECOMM / RemObjects) tal y como la usa el módulo oficial envialiacarrier 1.0.10 de PrestaShop. Endpoint real, login con id de sesión en ROClientIDHeader, la tabla ps_envialia_config con la contraseña cifrada con AES_ENCRYPT de MySQL, sincronización de estados, etiquetas PDF en base64 y las trampas del código (URL sin esquema, ficheros en ISO-8859-1, tracking_number que puede ser una URL entera). Usar al integrar Envialia, al leer sus credenciales desde otro módulo o al consultar el estado de un envío Envialia.
---

# Envialia — API real, leída del módulo oficial

**Fuente:** `envialiacarrier`, versión
**1.0.10** (`config_es.xml:5`), autor Dinaprise para Envialia, integrando el sistema **ECOMM**.
**Solo lectura: no se modifica ni un byte.**

Es **SOAP 1.1** sobre un servidor **RemObjects** (`WebServService___*`, `LoginWSService___*`,
`ROClientIDHeader`). El módulo monta el XML como cadena y lo manda con cURL; parsea la respuesta
con `SimpleXMLElement` + XPath sobre el prefijo `v1`. **Ninguna extensión más allá de cURL y
SimpleXML.**

> **Aviso de codificación:** los ficheros PHP de este módulo están en **ISO-8859-1**, no en UTF-8.
> Los comentarios y las cadenas con tildes se ven rotos al leerlos como UTF-8. No es corrupción de
> disco: es la codificación original. Cuidado al citar o copiar cadenas de ahí.

---

## 1. Endpoint real

**No hay una URL fija: la configura el comerciante.** Se guarda en
`ps_envialia_config.V_URL_WEB`, y el valor que se siembra al instalar es
(`envialiacarrier/sql/install.sql:89`):

```sql
INSERT INTO `PREFIX_envialia_config` (`V_URL_WEB`, `V_ID_SESION`) VALUES ("ws.envialia.com", "");
```

La URL final la monta `WebService::getURLWS()` (`lib/WebService.php:86-102`) añadiendo `/SOAP`:

```
ws.envialia.com   →   ws.envialia.com/SOAP
```

> **Trampa nº 1, y es un fallo del módulo:** `getURLWS()` calcula bien
> `'http://' . $url` en el primer `if`, y **el segundo `if` lo pisa** con `$url . '/SOAP'`,
> perdiendo el `http://`. El resultado que se le pasa a cURL es `ws.envialia.com/SOAP`, **sin
> esquema**. Funciona porque cURL supone `http://` cuando falta, pero significa que **el módulo
> habla por HTTP en claro, no por HTTPS**, salvo que el comerciante escriba `https://…` a mano en
> la configuración — y ni así, porque el segundo `if` también lo pisaría. En código nuevo, montar
> la URL correctamente y forzar HTTPS.

**NO CONFIRMADO: no hay entorno de pruebas.** No aparece ninguna URL de PRE en el módulo.

### URL de seguimiento

La **devuelve el propio login**: el campo `strURLDetSegEnv` de la respuesta de `LoginCli2` /
`LoginDep2` se guarda en `ps_envialia_config.V_URL_SEG` (`lib/WebService.php:63-67`).

Es una plantilla con dos marcadores, `{GUID}` y `{FECHA}`, que se sustituyen en SQL
(`lib/WebService.php:1238-1241`):

```sql
REPLACE(REPLACE(ec.V_URL_SEG, "{GUID}", ee.V_GUID), "{FECHA}", DATE_FORMAT(ee.D_FECHA, "%d/%m/%Y"))
```

**NO CONFIRMADO:** la forma literal de esa URL. No está en el código: la da Envialia en cada login.

---

## 2. Operaciones SOAP confirmadas

Espacio de nombres del cuerpo: **`http://tempuri.org/`** (RemObjects).
Sobre del SOAP: `http://schemas.xmlsoap.org/soap/envelope/` (SOAP 1.1).

| Operación | Para qué | Dónde |
|---|---|---|
| `LoginWSService___LoginCli2` | Login **sin** departamento | `lib/WebService.php:28-32` |
| `LoginWSService___LoginDep2` | Login **con** departamento | `lib/WebService.php:42-47` |
| `WebServService___GrabaEnvio8` | Alta de expedición | `lib/WebService.php:271` |
| `WebServService___GrabaEnvioMasivo` | Alta en lote | `lib/generaEnvioBultosMasivo.php` |
| `WebServService___BorraEnvio` | Anular expedición | `lib/WebService.php:462` |
| `WebServService___BorraEnvioMasivo` | Anular en lote | `lib/WebService.php` (§ borraEnvioMasivo) |
| `WebServService___ConsEtiquetaEnvio6` | **Etiqueta** de un envío | `lib/WebService.php:538` |
| `WebServService___ConsEtiquetaEnvioMasiva` | Etiquetas en lote | `lib/WebService.php:616` |
| `WebServService___ConsEstadoEnvioMasivo` | **Seguimiento** (estados en lote) | `lib/WebService.php:686` |

Cabecera HTTP: `Content-Type: text/xml` (`lib/WebService.php:1207`).

---

## 3. Autenticación: login que devuelve un id de sesión

`lib/WebService.php:18-74`. **Dos operaciones según haya o no departamento.**

Sin departamento (`$strDepto` vacío):

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <LoginWSService___LoginCli2>
      <strCodAge>AGENCIA</strCodAge>
      <strCliente>CLIENTE</strCliente>
      <strPass>CONTRASEÑA</strPass>
    </LoginWSService___LoginCli2>
  </soap:Body>
</soap:Envelope>
```

Con departamento:

```xml
<LoginWSService___LoginDep2>
  <strCodAge>AGENCIA</strCodAge>
  <strCodCli>CLIENTE</strCodCli>          <!-- OJO: strCodCli, no strCliente -->
  <strDepartamento>DEPARTAMENTO</strDepartamento>
  <strPass>CONTRASEÑA</strPass>
</LoginWSService___LoginDep2>
```

> El nombre del campo del cliente **cambia entre las dos operaciones**: `strCliente` en `LoginCli2`
> y `strCodCli` en `LoginDep2` (`:29` frente a `:44`). Equivocarse ahí da un error de autenticación
> que no dice nada.

Respuesta:

- `//v1:strSesion` — **el id de sesión**, una cadena con llaves, tipo `{XXXXXXXX-…}`. El módulo lo
  reconoce precisamente por eso: `strpos($strSesion, '{')` (`:446-450`).
- `//v1:strURLDetSegEnv` — plantilla de la URL de seguimiento.
- `//faultcode` / `//faultstring` — si hay error, el fallo SOAP.

Los dos valores se guardan con `EnvialiaConfig::setSesionYUrlSeg()` (`clases/EnvialiaConfig.php:38-42`).

**El id de sesión viaja en la cabecera SOAP de todas las demás llamadas**
(`lib/WebService.php:265-269`):

```xml
<soap:Header>
  <ROClientIDHeader xmlns="http://tempuri.org/">
    <ID>{ID-DE-SESION}</ID>
  </ROClientIDHeader>
</soap:Header>
```

**Y caduca.** El módulo maneja la caducidad de una forma muy concreta, que hay que copiar
(`lib/WebService.php:470-481`): manda la petición, y **si la respuesta trae `//faultcode`,
vuelve a hacer login, sustituye el id de sesión dentro del XML ya montado y reintenta una vez**:

```php
if ($manejadorXml->xpath('//faultcode')) {
    $strNewSesion = self::login(...);
    $xmlNew = str_replace('<ID>' . $strSesion . '</ID>', '<ID>' . $strNewSesion . '</ID>', $xml);
    $respuesta = self::peticionPost($strUrlWebService, $xmlNew);
    $manejadorXml = new SimpleXMLElement($respuesta);
}
```

---

## 4. Dónde están las credenciales

### 4.1 En `ps_configuration`: NINGUNA credencial

`ps_configuration` solo guarda opciones de negocio, con el prefijo `envialia_` **en minúsculas**:

```
Bultos          envialia_bultos  envialia_bultos_fijo_num  envialia_bultos_var_num
Servicios       envialia_ecomm_24  envialia_ecomm_72  envialia_ecomm_ee  envialia_ecomm_ww
Envío gratis    envialia_env_grat_pen  envialia_env_grat_pen_imp_min  envialia_env_grat_pen_tipo_serv
                envialia_env_grat_int  envialia_env_grat_int_imp_min  envialia_env_grat_int_tipo_serv
Tarifas         envialia_conf_tar  envialia_tarifa_peso  envialia_tarifa_impo
                envialia_tar_marg  envialia_tar_impuesto  envialia_tar_imp_fijo  envialia_tar_imp_mani
                envialia_imp_tar_peso  envialia_imp_tar_impo
Etiqueta        envialia_etiqueta  envialia_imp_eti_a4  envialia_eti_ajustar
                envialia_eti_alto  envialia_eti_ancho  envialia_perm_imp_eti
Remitente       envialia_rem_prev  envialia_rem_prev_nom  envialia_rem_prev_dir
                envialia_rem_prev_cp  envialia_rem_prev_pob
Otros           envialia_estado_pedido  envialia_env_obs  envialia_ref_prod
                envialia_perm_grab_pedido  envialia_seg_red
```

### 4.2 Las credenciales: tabla `ps_envialia_config`

`envialiacarrier/sql/install.sql:72-81`:

```sql
CREATE TABLE PREFIX_envialia_config (
  id_envialia_config INT AUTO_INCREMENT PRIMARY KEY,
  V_COD_AGE      VARCHAR(6)    -- código de AGENCIA
  V_COD_CLI      VARCHAR(5)    -- código de CLIENTE
  V_COD_CLI_DEP  VARCHAR(40)   -- DEPARTAMENTO (puede ir vacío)
  BL_PASS        BLOB          -- CONTRASEÑA, cifrada con AES_ENCRYPT de MySQL
  V_URL_WEB      VARCHAR(250)  -- URL del web service, sin '/SOAP'
  V_ID_SESION    VARCHAR(40)   -- id de sesión en curso
  V_URL_SEG      VARCHAR(250)  -- plantilla de la URL de seguimiento ({GUID}, {FECHA})
)
```

**Hay una sola fila.** Los `UPDATE` de `EnvialiaConfig` no llevan `WHERE`
(`clases/EnvialiaConfig.php:26-35`), así que la configuración es **global, no por tienda**.

### 4.3 Descifrar la contraseña

`clases/EnvialiaConfig.php:12-24`:

```sql
SELECT V_COD_AGE, V_COD_CLI, V_COD_CLI_DEP, V_URL_WEB, V_URL_SEG, V_ID_SESION,
       CAST(AES_DECRYPT(BL_PASS, "<CONST_TOKEN>") AS CHAR) AS BL_PASS
  FROM ps_envialia_config
```

`CONST_TOKEN` es una constante del módulo, definida en
**`envialiacarrier/clases/ModuleConst.php:16`**. Está escrita en claro en el código; no es una
clave derivada de la tienda, así que **la contraseña se puede descifrar desde cualquier módulo**
del mismo PrestaShop sin más que leer esa constante:

```php
require_once _PS_MODULE_DIR_ . 'envialiacarrier/clases/ModuleConst.php';   // define CONST_TOKEN
```

(Es `AES_ENCRYPT` de MySQL, ECB de 128 bits sin sal. No es criptografía seria; es ofuscación.
Un módulo nuevo **no debería** guardar así una contraseña.)

### 4.4 Otras tablas

`envialiacarrier/sql/install.sql`:

| Tabla | Para qué |
|---|---|
| `envialia_envio` | `id_order`, `V_COD_AGE_CARGO`, `V_COD_AGE_ORI`, `V_ALBARAN`, `V_GUID`, `D_FECHA` (`:16-24`) |
| `envialia_estado` | `id_order_state` ↔ `V_COD_TIPO_EST` — **la rellena el comerciante a mano** (`:64-70`) |
| `envialia_tipo_serv` | `V_COD_TIPO_SERV`, `ID_CARRIER`, `V_DES`, `T_INT`, `T_EUR` (`:1-8`) |
| `envialia_zonas`, `envialia_tarifa_pesos`, `envialia_tarifa_importes` (+ `_base`), `envialia_cp` | tarifas |

---

## 5. Detectar el módulo

```php
if (Module::isInstalled('envialiacarrier') && Module::isEnabled('envialiacarrier')) {
    require_once _PS_MODULE_DIR_ . 'envialiacarrier/clases/ModuleConst.php';
    $conf = Db::getInstance(_PS_USE_SQL_SLAVE_)->getRow(
        'SELECT V_COD_AGE, V_COD_CLI, V_COD_CLI_DEP, V_URL_WEB, V_ID_SESION, V_URL_SEG,
                CAST(AES_DECRYPT(BL_PASS, "' . pSQL(CONST_TOKEN) . '") AS CHAR) AS BL_PASS
           FROM `' . _DB_PREFIX_ . 'envialia_config`'
    );
}
```

Nombre en `ps_module`: **`envialiacarrier`** (`config_es.xml:3`).

Para saber si un `id_carrier` es de Envialia, la tabla `ps_envialia_tipo_serv` (`sql/install.sql:91-94`):

| `V_COD_TIPO_SERV` | Servicio | Internacional | Europa |
|---|---|---|---|
| `E24` | servicio E-Comm 24 | 0 | 0 |
| `E72` | servicio E-Comm 72 | 0 | 0 |
| `EEU` | E-COMM EUROPE EXPRESS | 0 | 1 |
| `EWW` | E-COMM WORLDWIDE | 1 | 1 |

```php
$esEnvialia = (bool) Db::getInstance(_PS_USE_SQL_SLAVE_)->getValue(
    'SELECT 1 FROM `' . _DB_PREFIX_ . 'envialia_tipo_serv` WHERE `ID_CARRIER` = ' . (int) $idCarrier
);
```

---

## 6. Seguimiento — `ConsEstadoEnvioMasivo`

`lib/WebService.php:649-740`. **Es una consulta en LOTE, no de uno en uno.**

Se le pasa un XML de envíos **escapado como texto** dentro de `<strEnvios>`. El XML es
(`controllers/admin/AdminEnvialiaEnvioController.php:176-182`, `:373-379`):

```xml
<ENVIOS>
  <ENVIO V_COD_AGE_CARGO="000123" V_COD_AGE_ORI="000123" V_ALBARAN="1234567890" />
  <ENVIO ... />
</ENVIOS>
```

y se escapa con `WebService::parseaXML()` (`lib/WebService.php:1213-1232`) antes de meterlo:
`&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `'` → `&apos;`, `"` → `&quot;`, y **las vocales
acentuadas se sustituyen por vocales sin tilde** (en bytes ISO-8859-1).

Petición:

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" …>
  <soap:Header>
    <ROClientIDHeader xmlns="http://tempuri.org/"><ID>{SESION}</ID></ROClientIDHeader>
  </soap:Header>
  <soap:Body>
    <WebServService___ConsEstadoEnvioMasivo>
      <strEnvios>&lt;ENVIOS&gt;&lt;ENVIO … /&gt;&lt;/ENVIOS&gt;</strEnvios>
    </WebServService___ConsEstadoEnvioMasivo>
  </soap:Body>
</soap:Envelope>
```

Respuesta: `//v1:strEstados`, **otra vez un XML dentro de un texto**, que el módulo vuelve a cargar
con `SimpleXMLElement` (`:707`). Dentro hay nodos `<ENV_ESTADOS …/>` con atributos
(`:711-721`):

```
V_COD_AGE_CARGO   V_COD_AGE_ORI   V_ALBARAN   V_COD_TIPO_EST
```

`V_COD_TIPO_EST` es **el código de estado de Envialia**, `varchar(4)`.

### 6.1 Códigos de estado

**NO CONFIRMADO: no existe ninguna tabla de códigos de Envialia en el módulo.** La tabla
`ps_envialia_estado` se crea **vacía** (`sql/install.sql:64-70`, ni un `INSERT`) y es el
**comerciante quien introduce a mano cada equivalencia** en el back-office, en la pantalla
«Estados» del módulo: un campo de texto de 4 caracteres llamado *«Código estado envialia»* y un
desplegable con los estados de pedido de PrestaShop
(`controllers/admin/AdminEnvialiaEstadoController.php:77-85`).

El módulo controla que no haya duplicados (`:126-139`) y aplica la equivalencia con un `UPDATE`
directo sobre `ps_orders.current_state` (`lib/WebService.php:713-720`):

```sql
UPDATE ps_orders
   SET current_state = (SELECT ee.id_order_state FROM ps_envialia_estado ee
                         WHERE ee.V_COD_TIPO_EST = '<codigo>')
 WHERE id_order = (SELECT een.id_order FROM ps_envialia_envio een
                    WHERE een.V_COD_AGE_CARGO = '…' AND een.V_COD_AGE_ORI = '…'
                      AND een.V_ALBARAN = '…')
   AND EXISTS (SELECT … FROM ps_envialia_estado WHERE V_COD_TIPO_EST = '<codigo>')
```

y después inserta a mano una fila en `ps_order_history` (`:721-727`).

**Consecuencia para un módulo nuevo:** los códigos de Envialia hay que sacarlos de la propia tabla
`ps_envialia_estado` del comerciante (que es la única fuente) o pedírselos a Envialia. No hay lista
ni en el código ni en el SQL.

### 6.2 La ventana de sincronización

`CONST_DIAS_SINC = 10` (`clases/ModuleConst.php:19`). La sincronización automática solo mira los
envíos de los **últimos 10 días** (`AdminEnvialiaEnvioController.php:170-172`).

### 6.3 Mensajes de error que devuelve esa función

Textos literales de `lib/WebService.php:733-740`:

| Texto | Cuándo |
|---|---|
| `Envios no encontrados.` | hay `strEstados` pero sin `ENV_ESTADOS` dentro |
| `Error al conectar con el servidor.` | no llega `strEstados`, o no hay sesión |
| `No ha configurado la url de conexión.` | `V_URL_WEB` vacía |

---

## 7. Etiquetas — `ConsEtiquetaEnvio6`

`lib/WebService.php:498-580`:

```xml
<WebServService___ConsEtiquetaEnvio6>
  <strCodAgeOri>AGENCIA</strCodAgeOri>
  <strAlbaran>ALBARAN</strAlbaran>
  <strBulto></strBulto>
  <boPaginaA4>0</boPaginaA4>          <!-- 1 si envialia_imp_eti_a4 == 1 -->
  <intNumEtiqImpresasA4>0</intNumEtiqImpresasA4>
  <strFormato>PDF</strFormato>
</WebServService___ConsEtiquetaEnvio6>
```

Respuesta: `//v1:strEtiqueta` con el **PDF en base64**. Si no viene ese nodo, la función devuelve
la cadena `'0'` (`:581-585`) — **no `false`**, la cadena `'0'`.

Tratamiento del PDF (`lib/WebService.php:367-372`):

```php
$decoded = base64_decode($strEtiqueta);
$decoded = EnvialiaEtiquetaFormato::ajustar($decoded);   // recorta/ajusta según envialia_eti_alto/_ancho
file_put_contents('../modules/EnvialiaCarrier/etiquetas/' . $strSesion . '.pdf', $decoded);
```

> La ruta lleva **`EnvialiaCarrier` con mayúsculas** y es **relativa** (`../modules/…`). En Linux,
> con la carpeta real en minúsculas, eso no existe. Es un fallo del módulo; en código nuevo,
> `_PS_MODULE_DIR_ . 'envialiacarrier/…'`.

En lote: `ConsEtiquetaEnvioMasiva` con el mismo `<ENVIOS>` escapado en `<strEnvios>`
(`lib/WebService.php:605-646`).

---

## 8. Alta de expedición — `GrabaEnvio8`

`lib/WebService.php:263-344`. Campos obligatorios y notables:

```
strCodAgeCargo  strCodAgeOri     ← los dos, la MISMA agencia
strAlbaran      ← vacío al dar de alta; lo asigna Envialia
dtFecha         strCodTipoServ   ← E24 | E72 | EEU | EWW
strCodCli       strCodCliDep
strNomOri  strDirOri  strPobOri  strCPOri  strTlfOri
strNomDes  strDirDes  strPobDes  strCPDes  strTlfDes
intDoc=0   intPaq=<bultos>   dPesoOri   dAltoOri  dAnchoOri  dLargoOri
dReembolso   dValor=0  dAnticipo=0  dCobCli=0
strObs   boSabado=0  boRetorno=0  boGestOri=0  boGestDes=0  boAnulado=0  boAcuse=0
strRef   strCodPais  strDesMoviles  strDesDirEmails
boInsert=1
strCampo3=<id_order>          ← el módulo mete aquí el id del pedido
strCampo4=<referencias de los artículos con cantidades>
```

Respuesta (`lib/WebService.php:341-354`):

- `//v1:strAlbaranOut` — **el número de albarán**
- `//v1:dtFecHoraAltaOut` — fecha y hora del alta
- `//v1:strGuidOut` — GUID del envío; el módulo **le quita las llaves** `{` y `}` antes de
  guardarlo (`:351-353`)

Y se inserta la fila en `ps_envialia_envio` (`:356-360`).

---

## 9. Número de seguimiento

`WebService::actualizaSeguimiento()` (`lib/WebService.php:1234-1268`) escribe
`ps_order_carrier.tracking_number`, y **lo que escribe depende de una opción**:

| `envialia_seg_red` | Qué se guarda en `tracking_number` |
|---|---|
| `0` | **Una URL entera**: `V_URL_SEG` con `{GUID}` y `{FECHA}` ya sustituidos |
| distinto de `0` | `V_COD_AGE_CARGO` + `V_ALBARAN` concatenados (agencia hasta 6 + albarán hasta 10) |

> **Trampa gorda:** con la opción por defecto, **`tracking_number` NO es un número: es una URL de
> seguimiento completa**. Un módulo que dé por hecho que ahí hay un código se encontrará un
> `https://…` de 200 caracteres. Para tener el número de verdad, leer
> `ps_envialia_envio.V_ALBARAN`.

**NO CONFIRMADO:** el formato del `V_ALBARAN` más allá de su tipo, `VARCHAR(10)`. El módulo no lo
valida.

---

## 10. Trampas vistas en este código

1. **`getURLWS()` pierde el esquema** y deja la petición en HTTP en claro (§1). Fallo real del
   módulo.
2. **`EnvialiaConfig::getConfig()` puede devolver una variable sin definir.**
   `clases/EnvialiaConfig.php:17-22` hace `foreach ($resultado as $result) { }` — un bucle vacío
   solo para quedarse con la última fila — y luego `return $result;`. Si `executeS()` devuelve
   `false` (tabla vacía), en PHP 8 eso es un aviso de variable indefinida y un `return null`, y
   todo lo que venga detrás falla con «Trying to access array offset on value of type null».
   **Es el patrón que prohíbe el `CLAUDE.md`**: `executeS()` devuelve `false`, no un array vacío.
3. **El nombre del campo del cliente cambia entre `LoginCli2` y `LoginDep2`** (§3).
4. **La sesión caduca sin avisar.** El único síntoma es un `//faultcode` en la respuesta. Hay que
   implementar el reintento con relogin (§3) o las llamadas fallan al azar.
5. **XML anidado dos veces.** `<strEnvios>` y `strEstados` llevan XML escapado dentro de un
   elemento de texto. Hay que escapar al mandar y volver a parsear al recibir.
6. **`parseaXML()` quita las tildes** sustituyendo bytes ISO-8859-1 (`lib/WebService.php:1219-1229`).
   Si el módulo nuevo trabaja en UTF-8, esas sustituciones no encajan y las tildes llegan rotas a
   Envialia. Hay un `utf8_decode()` suelto antes de una de las llamadas
   (`lib/WebService.php:1100`), lo que confirma que el servicio espera **ISO-8859-1**.
   `utf8_decode()` está **obsoleto desde PHP 8.2**: usar
   `mb_convert_encoding($s, 'ISO-8859-1', 'UTF-8')`.
7. **`ImprimeEnvio()` devuelve la cadena `'0'` en caso de error**, no `false`. Un
   `if (!$r)` funciona por casualidad; un `if ($r === false)` no.
8. **La ruta de las etiquetas es relativa y con mayúsculas** (`../modules/EnvialiaCarrier/…`):
   no funciona en Linux (§7).
9. **La contraseña está en un BLOB con `AES_ENCRYPT` y la clave en claro en el código**
   (`clases/ModuleConst.php:16`). No es protección; no copiar el patrón.
10. **SQL sin `pSQL()`.** `setConfigAcceso()` y compañía interpolan directamente
    (`clases/EnvialiaConfig.php:26-31`), y la sincronización de estados mete los atributos del XML
    de respuesta dentro del `UPDATE` sin escapar (`lib/WebService.php:713-727`). En código nuevo,
    `pSQL()` siempre.
11. **`tracking_number` puede ser una URL entera** (§9).
12. **Configuración global, no por tienda.** Los `UPDATE` de `ps_envialia_config` no llevan `WHERE`
    (`clases/EnvialiaConfig.php:26-35`): una sola fila para todas las tiendas.
13. **`Db::getInstance(_PS_USE_SQL_SLAVE_)` para escrituras.** `setConfigAcceso()` y `setSesion()`
    (`:29`, `:35`) hacen `UPDATE` sobre la conexión de **solo lectura**. Con una réplica de verdad
    detrás, eso falla o escribe donde no debe.
14. **El módulo pinta JavaScript con `echo` dentro de la lógica del web service**
    (`lib/WebService.php:378-400`) para lanzar la impresión. En una llamada AJAX o en un cron eso
    contamina la respuesta.

---

## 11. Fragmento PHP listo para copiar (estructura legacy, sin Composer, cURL nativo)

```php
<?php
/**
 * Seguimiento de Envialia reutilizando la configuracion del modulo oficial
 * 'envialiacarrier'. Sin Composer, sin namespace, cURL nativo + SimpleXML.
 */
if (!defined('_PS_VERSION_')) {
    exit;
}

class MiEnvialiaTracking
{
    const NS_TEMPURI = 'http://tempuri.org/';

    /**
     * Configuracion del modulo oficial, con la contrasena ya descifrada.
     * BL_PASS va con AES_ENCRYPT de MySQL y la clave es CONST_TOKEN del modulo.
     */
    public static function getConfig()
    {
        $modConst = _PS_MODULE_DIR_ . 'envialiacarrier/clases/ModuleConst.php';
        if (!file_exists($modConst)) {
            return array();
        }
        require_once $modConst;   // define CONST_TOKEN
        if (!defined('CONST_TOKEN')) {
            return array();
        }

        $fila = Db::getInstance(_PS_USE_SQL_SLAVE_)->getRow(
            'SELECT `V_COD_AGE`, `V_COD_CLI`, `V_COD_CLI_DEP`, `V_URL_WEB`, `V_ID_SESION`, `V_URL_SEG`,
                    CAST(AES_DECRYPT(`BL_PASS`, "' . pSQL(CONST_TOKEN) . '") AS CHAR) AS `BL_PASS`
               FROM `' . _DB_PREFIX_ . 'envialia_config`'
        );

        // getRow() devuelve false si no hay fila: NUNCA (array) $fila.
        return is_array($fila) ? $fila : array();
    }

    /**
     * URL del servicio. El modulo oficial pierde el esquema aqui; nosotros no.
     */
    public static function getUrlWs($urlConfigurada)
    {
        $url = trim((string) $urlConfigurada);
        if ($url === '') {
            return '';
        }
        if (stripos($url, 'http://') !== 0 && stripos($url, 'https://') !== 0) {
            $url = 'https://' . $url;
        }
        if (substr(Tools::strtolower($url), -5) !== '/soap') {
            $url = rtrim($url, '/') . '/SOAP';
        }

        return $url;
    }

    /** POST del sobre SOAP. */
    private static function peticionPost($url, $xml)
    {
        $ch = curl_init();
        curl_setopt_array($ch, array(
            CURLOPT_URL => $url,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $xml,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_HTTPHEADER => array('Content-Type: text/xml'),
        ));
        $r = curl_exec($ch);
        $err = curl_error($ch);
        curl_close($ch);

        return ($err || $r === false || $r === '') ? false : $r;
    }

    /**
     * Login. Devuelve el id de sesion (entre llaves) o false.
     * OJO: el campo del cliente se llama distinto con y sin departamento.
     */
    public static function login(array $conf)
    {
        $url = self::getUrlWs(isset($conf['V_URL_WEB']) ? $conf['V_URL_WEB'] : '');
        if ($url === '') {
            return false;
        }

        $age = htmlspecialchars((string) $conf['V_COD_AGE'], ENT_XML1, 'UTF-8');
        $cli = htmlspecialchars((string) $conf['V_COD_CLI'], ENT_XML1, 'UTF-8');
        $pass = htmlspecialchars((string) $conf['BL_PASS'], ENT_XML1, 'UTF-8');
        $dep = trim((string) $conf['V_COD_CLI_DEP']);

        if ($dep === '') {
            $cuerpo = '<LoginWSService___LoginCli2>'
                . '<strCodAge>' . $age . '</strCodAge>'
                . '<strCliente>' . $cli . '</strCliente>'
                . '<strPass>' . $pass . '</strPass>'
                . '</LoginWSService___LoginCli2>';
        } else {
            $cuerpo = '<LoginWSService___LoginDep2>'
                . '<strCodAge>' . $age . '</strCodAge>'
                . '<strCodCli>' . $cli . '</strCodCli>'
                . '<strDepartamento>' . htmlspecialchars($dep, ENT_XML1, 'UTF-8') . '</strDepartamento>'
                . '<strPass>' . $pass . '</strPass>'
                . '</LoginWSService___LoginDep2>';
        }

        $xml = '<?xml version="1.0" encoding="utf-8"?>'
            . '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
            . ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            . ' xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
            . '<soap:Body>' . $cuerpo . '</soap:Body></soap:Envelope>';

        $respuesta = self::peticionPost($url, $xml);
        if ($respuesta === false) {
            return false;
        }

        $doc = @simplexml_load_string($respuesta);
        if (!$doc || $doc->xpath('//faultcode')) {
            return false;
        }

        $sesion = $doc->xpath('//v1:strSesion');

        return empty($sesion[0]) ? false : (string) $sesion[0];
    }

    /**
     * Estados de un lote de envios.
     *
     * @param array $envios array de array('V_COD_AGE_CARGO','V_COD_AGE_ORI','V_ALBARAN')
     * @return array|false  array('<albaran>' => '<V_COD_TIPO_EST>')
     */
    public static function getEstados(array $envios)
    {
        if (empty($envios)) {
            return array();
        }

        $conf = self::getConfig();
        if (empty($conf['V_COD_AGE'])) {
            return false;
        }

        $url = self::getUrlWs($conf['V_URL_WEB']);
        $sesion = trim((string) $conf['V_ID_SESION']);
        if ($sesion === '' || strpos($sesion, '{') === false) {
            $sesion = self::login($conf);
            if ($sesion === false) {
                return false;
            }
        }

        $lista = '<ENVIOS>';
        foreach ($envios as $e) {
            $lista .= '<ENVIO V_COD_AGE_CARGO = "' . $e['V_COD_AGE_CARGO']
                . '" V_COD_AGE_ORI = "' . $e['V_COD_AGE_ORI']
                . '" V_ALBARAN = "' . $e['V_ALBARAN'] . '" />';
        }
        $lista .= '</ENVIOS>';

        // El servicio espera ISO-8859-1. utf8_decode esta obsoleto desde PHP 8.2.
        if (function_exists('mb_convert_encoding')) {
            $lista = mb_convert_encoding($lista, 'ISO-8859-1', 'UTF-8');
        }
        $listaEscapada = htmlspecialchars($lista, ENT_QUOTES | ENT_XML1, 'ISO-8859-1');

        $xml = self::montarSobre($sesion, $listaEscapada);
        $respuesta = self::peticionPost($url, $xml);
        if ($respuesta === false) {
            return false;
        }

        $doc = @simplexml_load_string($respuesta);

        // La sesion caduca: si hay faultcode, relogin y UN reintento.
        if (!$doc || $doc->xpath('//faultcode')) {
            $nueva = self::login($conf);
            if ($nueva === false) {
                return false;
            }
            $respuesta = self::peticionPost($url, self::montarSobre($nueva, $listaEscapada));
            if ($respuesta === false) {
                return false;
            }
            $doc = @simplexml_load_string($respuesta);
            if (!$doc) {
                return false;
            }
        }

        $estados = $doc->xpath('//v1:strEstados');
        if (empty($estados[0])) {
            return false;
        }

        // Dentro viene OTRO XML.
        $interno = @simplexml_load_string((string) $estados[0]);
        if (!$interno) {
            return false;
        }

        $salida = array();
        $nodos = $interno->xpath('//ENV_ESTADOS');
        foreach (is_array($nodos) ? $nodos : array() as $nodo) {
            $salida[(string) $nodo['V_ALBARAN']] = (string) $nodo['V_COD_TIPO_EST'];
        }

        return $salida;
    }

    private static function montarSobre($sesion, $listaEscapada)
    {
        return '<?xml version="1.0" encoding="utf-8"?>'
            . '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
            . ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            . ' xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
            . '<soap:Header><ROClientIDHeader xmlns="' . self::NS_TEMPURI . '">'
            . '<ID>' . $sesion . '</ID>'
            . '</ROClientIDHeader></soap:Header>'
            . '<soap:Body><WebServService___ConsEstadoEnvioMasivo>'
            . '<strEnvios>' . $listaEscapada . '</strEnvios>'
            . '</WebServService___ConsEstadoEnvioMasivo></soap:Body></soap:Envelope>';
    }

    /** Envios de un pedido, desde la tabla del modulo oficial. */
    public static function getEnviosDePedido($idOrder)
    {
        $filas = Db::getInstance(_PS_USE_SQL_SLAVE_)->executeS(
            'SELECT `V_COD_AGE_CARGO`, `V_COD_AGE_ORI`, `V_ALBARAN`
               FROM `' . _DB_PREFIX_ . 'envialia_envio`
              WHERE `id_order` = ' . (int) $idOrder
        );

        return is_array($filas) ? $filas : array();
    }
}
```

Uso:

```php
$envios = MiEnvialiaTracking::getEnviosDePedido(1234);
$estados = MiEnvialiaTracking::getEstados($envios);
// $estados = array('1234567890' => 'E10', ...)
// Para saber que significa cada codigo: tabla ps_envialia_estado del comerciante.
```

---

## 12. Qué NO se ha podido confirmar leyendo el código

- **La lista de códigos `V_COD_TIPO_EST` de Envialia.** No existe en el módulo: la tabla
  `ps_envialia_estado` se crea vacía y la rellena el comerciante a mano. Es el único transportista
  de los seis que no trae ninguna tabla de estados.
- **La URL de seguimiento** (`V_URL_SEG`): la da el propio login, no está en el código. Solo se
  sabe que lleva los marcadores `{GUID}` y `{FECHA}` en formato `d/m/Y`.
- **Entorno de pruebas**: no aparece ninguna URL de PRE.
- **Formato del `V_ALBARAN`**: solo el tipo, `VARCHAR(10)`.
- **Códigos de error generales** del web service: lo único tabulado son los tres del borrado
  (`lib/WebService.php:13-16`): `1` = el envío no existe, `2` = el usuario no tiene permiso para
  borrarlo, `3` = la fecha está fuera del rango permitido. Del resto de operaciones solo llega
  `intCodError` sin tabla.
- **WSDL del servicio**: el módulo no lo consulta nunca (monta el XML a mano), así que no hay
  esquema de los tipos ni lista completa de operaciones.
- **Diferencia entre `GrabaEnvio8` y `GrabaEnvioMasivo`** en cuanto a campos: el masivo se monta en
  `lib/generaEnvioBultosMasivo.php`; no se ha revisado en esta lectura.
