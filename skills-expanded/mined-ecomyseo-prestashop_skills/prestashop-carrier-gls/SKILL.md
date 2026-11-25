---
name: prestashop-carrier-gls
description: API SOAP de GLS España (ASM / asmred) tal y como la usa el módulo oficial glsshipping 3.7.20 de PrestaShop. Endpoints b2b.asmx reales, autenticación por GUID único, las claves exactas de ps_configuration donde el comerciante ya tiene puesto su GUID, la tabla de servicios y horarios, GetExpCli para el seguimiento, etiquetas PDF en base64 y las trampas del código. Usar al integrar GLS/ASM, al leer su GUID desde otro módulo o al consultar el estado de un envío GLS.
---

# GLS España (ASM / asmred) — API real, leída del módulo oficial

**Fuente:** `glsshipping`, versión
**3.7.20** (`config.xml:5`), autor GLS. **Solo lectura: no se modifica ni un byte.**

Es **SOAP 1.2** contra `asmred.com`. El módulo **no usa `SoapClient`**: monta el XML como cadena y
lo manda con cURL (`CURLOPT_POSTFIELDS` + `Content-Type: text/xml; charset=UTF-8`), y parsea la
respuesta con `simplexml_load_string()` + XPath. Eso hace que sea el más fácil de replicar en un
módulo legacy: **no hace falta ninguna extensión más que cURL y SimpleXML**.

---

## 1. Endpoints reales

| Qué hace | URL | Dónde |
|---|---|---|
| **Endpoint que de verdad se usa** | `https://wsclientes.asmred.com/b2b.asmx` | `glsshipping.php:1693`, `AdminGlsshippingController.php:426` |
| Seguimiento (con `?op=`) | `https://wsclientes.asmred.com/b2b.asmx?op=GetExpCli` | `glsshipping.php:2774` |
| URL configurable (valor por defecto) | `https://www.asmred.com/websrvs/ecm.asmx?wsdl` | `glsshipping.php:115`, `:269` |
| Etiqueta por navegador | `https://www.asmred.com/Extranet/public/ecmLabel.aspx?codbarras=<cod>&uid=<GUID>` | `glsshipping.php:1953-1955`, `:2478` |
| Seguimiento público del cliente | `https://mygls.gls-spain.es/e/<codigoBarras>/<cpDestino>/<isoIdioma>` | `glsshipping.php:2039` |

> **Trampa gorda:** la clave `GLS_URL` guarda `https://www.asmred.com/websrvs/ecm.asmx?wsdl`, pero
> el código la **ignora** y la pisa a pelo justo después de leerla:
> ```php
> $URL = Configuration::get('GLS_URL', null, null, $id_shop);   // :1687
> $URL = str_replace("http://", "https://", $URL);              // :1690
> $URL = 'https://wsclientes.asmred.com/b2b.asmx';              // :1693  ← siempre
> ```
> Lo mismo en el seguimiento (`:2774`) y en `collect()` (`AdminGlsshippingController.php:426`).
> **Cambiar `GLS_URL` no cambia nada.** Un módulo nuevo debe apuntar a `wsclientes.asmred.com`.

**NO CONFIRMADO: no hay entorno de pruebas.** No aparece ninguna URL de PRE en el módulo. GLS
distingue pruebas de producción **por el GUID**: el que trae de fábrica
(`15F9A8B5-82AC-4094-99F7-9FD58FD43E9E`, `glsshipping.php:114`) es el GUID de pruebas, según su
propia descripción en pantalla (`:263`): *«El GUID por defecto […] es para hacer pruebas. […]
solicite su GUID a su Agencia GLS.»*

### Operaciones confirmadas

Todas en el espacio de nombres **`http://www.asmred.com/`**:

| Operación | Para qué | Dónde |
|---|---|---|
| `GrabaServicios` | Dar de alta la expedición y recibir el código de barras y la etiqueta | `glsshipping.php:1710` |
| `GetExpCli` | Consultar el estado de una expedición | `glsshipping.php:2788-2793` |
| `EnviaCorreoAgencia` | Avisar a la agencia de la recogida (cierre del día) | `AdminGlsshippingController.php:432-436` |

---

## 2. Autenticación

**Un solo dato: el GUID.** No hay usuario, contraseña ni token.

- En `GrabaServicios` viaja como atributo del nodo raíz:
  `<Servicios uidcliente="<GUID>">` (`glsshipping.php:1713`).
- En `GetExpCli` y en `EnviaCorreoAgencia` viaja como elemento:
  `<uid><GUID></uid>` (`glsshipping.php:2791-2793`, `AdminGlsshippingController.php:434`).
- En la etiqueta por navegador, como parámetro: `&uid=<GUID>` (`glsshipping.php:1955`).

Cabecera HTTP obligatoria: `Content-Type: text/xml; charset=UTF-8` (`glsshipping.php:1812`).
Sin ella, GLS devuelve un fallo SOAP.

---

## 3. Claves EXACTAS de `ps_configuration`

Todas son globales salvo donde se indique (varias se leen con `$id_shop`, así que **hay que pasar
el `id_shop`** — ver §8.6).

### 3.1 La credencial

```
GLS_GUID     ← LA credencial. Por defecto '15F9A8B5-82AC-4094-99F7-9FD58FD43E9E' (de PRUEBAS)
GLS_URL      https://www.asmred.com/websrvs/ecm.asmx?wsdl  (se guarda pero NO se usa, ver §1)
GLSSHIPPING_LIVE_MODE
```

Referencias: `glsshipping.php:114-115`, `:262-269`, `:1007-1008`, `:1687-1688`.

### 3.2 Remitente

```
GLS_SENDER_NAME
GLS_SENDER_ADDRESS
GLS_SENDER_CITY
GLS_SENDER_CP
GLS_SENDER_COUNTRY
GLS_EMAIL
```

### 3.3 Opciones del envío

```
GLS_RCS         Retorno Copia Sellada (0/1)          glsshipping.php:571
GLS_DORIG       departamento de origen               :590
GLS_VSEC        valor asegurado                      :596
GLS_RETORNO     retorno
GLS_COD         contrareembolso
GLS_INCOTERM    incoterm para EBP fuera de la UE
GLS_SERVICE_DEFAULT
GLS_DEF_PESO    peso por defecto
GLS_BULTOS  GLS_FIJO_BULTOS  GLS_NUM_FIJO_BULTOS  GLS_NUM_ARTICULOS
GLS_APLI4       etiquetas múltiples en Apli4         :977
GLS_MULEBP  GLS_BPESPT  GLS_SDI_COUNTRIES  GLS_OPEN_CARRIER
GLS_ENVIAR_MAIL
```

### 3.4 Qué transportistas son de GLS

Cada una guarda **una lista de `id_carrier` separada por `;`** (`glsshipping.php:2928-2952`):

```
GLS_SERVICIO_SELECCIONADO_GLS10
GLS_SERVICIO_SELECCIONADO_GLS14
GLS_SERVICIO_SELECCIONADO_GLS24
GLS_SERVICIO_SELECCIONADO_BUSPAR
GLS_SERVICIO_SELECCIONADO_GLSECO
GLS_SERVICIO_SELECCIONADO_GLSEBP
GLS_SERVICIO_SELECCIONADO_GLSSHOPDELINT
GLS_SERVICIO_SELECCIONADO_GLSPARCEL
GLS_VALID_CARRIERS
```

Se comparan **tanto contra `id_carrier` como contra `id_reference`**, porque PrestaShop crea un
`id_carrier` nuevo cada vez que se edita un transportista.

### 3.5 Estados de pedido y actualización automática

```
GLS_STATUS_SEND                 estado al grabar el envío
GLS_STATUS_COMPLETED            estado al entregar
GLS_STATUS_FAILED               estado si no se entrega
GLS_UPDATE_ORDER_STATUS_SEND        1 = aplicar GLS_STATUS_SEND
GLS_UPDATE_ORDER_STATUS_COMPLETED   1 = aplicar GLS_STATUS_COMPLETED
GLS_UPDATE_ORDER_STATUS_FAILED      1 = aplicar GLS_STATUS_FAILED
GLS_DISABLE_STATE_UPDATE
GLS_STATE_UPDATE_DAYS           ventana de días hacia atrás que consulta el cron
GLS_STATE_UPDATE_FREQUENCY
GLS_CRON_TIME
GLS_DATE_UPDATE  GLS_DATE_CLIENTDATA_UPDATE  date_collect
```

### 3.6 Tarifas

```
GLS_CSV_RATES  GLS_CSV_RATES_TYPE  GLS_SHOW_CSV
```

### 3.7 Tabla propia: `ps_gls_envios`

`glsshipping/sql/install.php:28-46`:

```sql
id_envio, id_envio_order (UNIQUE = id_order), current_state, state_history (JSON),
codigo_envio (varchar 50 = CÓDIGO DE BARRAS), url_track, num_albaran,
codigo_barras (RUTA del PDF en disco, no el código), bultos, retorno, rcs,
peso, vsec, dorig, observaciones, fecha
```

> **`codigo_barras` NO es el código de barras: es la ruta del fichero PDF** en
> `modules/glsshipping/PDF/` (`glsshipping.php:2060-2065`, `:2066`). El código de barras está en
> `codigo_envio`. Nombre desafortunado, pero es así.

---

## 4. Detectar el módulo

```php
if (Module::isInstalled('glsshipping') && Module::isEnabled('glsshipping')) {
    $guid = Configuration::get('GLS_GUID');
    // ¿está usando todavía el GUID de pruebas?
    $esPruebas = ($guid === '15F9A8B5-82AC-4094-99F7-9FD58FD43E9E');
}
```

Nombre en `ps_module`: **`glsshipping`** (`config.xml:3`).

Para saber si un `id_carrier` es de GLS hay dos caminos, los dos en el módulo:

1. `ps_carrier.external_module_name = 'glsshipping'` (`glsshipping.php:2757`).
2. El `id_carrier` **o** el `id_reference` dentro de alguna lista `GLS_SERVICIO_SELECCIONADO_*`
   (`glsshipping.php:2957-2985`, función `isCarrierGLS()`).

---

## 5. Seguimiento — `GetExpCli`

`glsshipping.php:2763-2903`. Petición:

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                 xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetExpCli xmlns="http://www.asmred.com/">
      <codigo>CODIGO_DE_BARRAS</codigo>
      <uid>GUID</uid>
    </GetExpCli>
  </soap12:Body>
</soap12:Envelope>
```

Se manda por POST a `https://wsclientes.asmred.com/b2b.asmx?op=GetExpCli` con
`Content-Type: text/xml; charset=UTF-8`.

Respuesta — el módulo la lee con XPath registrando el prefijo `asm` para
`http://www.asmred.com/` (`glsshipping.php:2824-2836`):

```
//asm:GetExpCliResponse/asm:GetExpCliResult
  //expediciones/exp
    //expediciones/exp/codestado               ← el estado, un entero
    //expediciones/exp/tracking_list/tracking  ← histórico
        tipo     'ESTADO' | 'INCIDENCIA' | otros (se descartan)
        codigo
        evento   texto
        fecha    'd/m/Y H:i:s'
```

El módulo se queda con los **10 últimos** eventos ordenados por fecha y los guarda como JSON en
`ps_gls_envios.state_history` (`:2856-2866`).

### 5.1 Códigos de estado (`codestado`)

**Lo único CONFIRMADO en el código:**

| `codestado` | Qué hace el módulo | Dónde |
|---|---|---|
| **`7`** | **ENTREGADO.** Si `GLS_UPDATE_ORDER_STATUS_COMPLETED = 1`, pone el pedido en `GLS_STATUS_COMPLETED` | `glsshipping.php:2881-2889` |
| cualquier otro | Si `GLS_UPDATE_ORDER_STATUS_FAILED = 1`, pone el pedido en `GLS_STATUS_FAILED` | `:2890-2900` |
| **`-10`** | Sin datos: el módulo salta ese envío (`continue`) sin tocar nada | `:2879` |
| **`7, 8, 5, 10, 12, 15, 17`** | **Estados finales.** El cron excluye de la consulta cualquier envío que ya esté en uno de ellos | `:2759` |

La consulta del cron (`glsshipping.php:2750-2761`) es:

```sql
... AND e.fecha BETWEEN (CURDATE() - INTERVAL <GLS_STATE_UPDATE_DAYS> DAY) AND (CURDATE() + INTERVAL 1 DAY)
    AND e.codigo_envio != ""
    AND (e.current_state IS NULL OR e.current_state NOT IN (7,8,5,10,12,15,17))
    AND o.current_state NOT IN (<GLS_STATUS_COMPLETED>)
```

**NO CONFIRMADO: la tabla completa de `codestado` con su significado.** El módulo no la tiene: lo
único que distingue es `7` (entregado), `-10` (sin datos) y el conjunto de estados finales. El
resto los mete todos en el mismo saco de «fallido», que es una simplificación del propio módulo,
no de GLS.

*De la documentación pública (fuera del código, [omatech/gls-tracker](https://github.com/omatech/gls-tracker)):*
en el `tracking_list`, una entrada con `tipo = ESTADO` y `codigo = 5` marca una expedición
**anulada**; y los estados que devuelve el servicio se describen como `GRABADO`, `EN REPARTO` y
`ENTREGADO`. **Esto viene de la web, no del código del módulo**, y no cubre los demás `codestado`.

---

## 6. Etiquetas

No hay una llamada aparte: **la etiqueta viene dentro de la respuesta de `GrabaServicios`**. Se
pide con este nodo en la petición (`glsshipping.php:1791-1793`):

```xml
<DevuelveAdicionales>
  <Etiqueta tipo="PDF"></Etiqueta>
</DevuelveAdicionales>
```

Y se recoge así (`glsshipping.php:1874-1875`):

```
//Servicios/Envio/Etiquetas/Etiqueta     ← PDF en BASE64
//Servicios/Envio/@codbarras             ← código de barras (atributo)
//Servicios/Envio/Resultado/@return      ← 0 = OK, distinto de 0 = ERROR
//Servicios/Envio/Errores/Error          ← texto del error
//Servicios/Envio/Referencias/Referencia[@tipo="N"]   ← número de albarán
```

El PDF se descodifica con `base64_decode()` y se escribe en `modules/glsshipping/PDF/`
(`glsshipping.php:2055-2065`). La carpeta tiene que existir y ser escribible; si no, el módulo
imprime los permisos en pantalla (`:1885-1893`).

También se puede abrir la etiqueta ya grabada en el navegador:

```
https://www.asmred.com/Extranet/public/ecmLabel.aspx?codbarras=<codigo_envio>&uid=<GLS_GUID>
```

---

## 7. Tabla de servicios y horarios

`glsshipping.php:1367-1396` y `:1404-1445`. Cada servicio comercial es un par
`<Servicio>` + `<Horario>`:

| Nombre en el módulo | `<Servicio>` | `<Horario>` |
|---|---|---|
| `GLS10` | `1` | `0` |
| `GLS14` | `1` | `2` |
| `GLS24` | `1` | `3` |
| `BUSPAR` (BusinessParcel) | `96` | `18` |
| `ECONOMY` | `37` | `18` |
| `EUROBUSINESSPARCEL` (EBP) | `74` | `3` |
| `SHOPDELINT` | `74` | `19` |
| `PARCELS` (ParcelShop) | `1` | `19` |

**Regla especial:** si el servicio es `74` (EBP) y el peso es **menor de 3 kg**, el módulo cambia
el servicio a **`76`** (`glsshipping.php:1704`):

```php
if ($servicio == 74 && $gls_peso_origen < 3) $servicio = 76;
```

Con `74` o `76` e incoterm mayor que 0, la petición lleva `<Aduanas><Incoterm>` en lugar de
`<Retorno>` (`:1725-1734`).

Códigos de país: **numéricos** para el remitente (`351` para Portugal, `glsshipping.php:1680`) e
**ISO alfabético** para el destinatario (`<Pais>' . $gls_pais . '</Pais>` con `iso_code`, `:1755`).
No son el mismo formato en los dos extremos.

---

## 8. Trampas vistas en este código

1. **`GLS_URL` no se usa.** Ver §1. Cambiar la configuración no cambia el destino.
2. **HTTP 200 con error dentro.** Hay que mirar `Servicios/Envio/Resultado/@return`; si no es `0`,
   la expedición NO se ha grabado (`glsshipping.php:1836-1841`).
3. **El módulo guarda los errores en `$_SESSION["ultimoErrorGLS"]`** (`:1834-1840`). En una
   petición AJAX o en un cron eso no existe y se pierde. En un módulo nuevo, el error va al
   registro del módulo.
4. **`codigo_barras` de `ps_gls_envios` es una RUTA de fichero**, no el código (§3.7).
5. **`GetExpCli` se llama con `curl_multi`** para varios pedidos a la vez (`:2765`, `:2806`). Si se
   copia, hay que cerrar los manejadores: el módulo lo hace en `:2822-2823`.
6. **Multitienda a medias.** `grabarServicios()` lee con `$id_shop`
   (`Configuration::get('GLS_URL', null, null, $id_shop)`, `:1687-1688`), pero el cron de estados
   lee **sin** `id_shop`: `Configuration::get('GLS_GUID')` (`:2763`) y
   `Configuration::get('GLS_UPDATE_ORDER_STATUS_COMPLETED')` (`:2881`). En multitienda, el cron usa
   el GUID de la tienda del contexto para envíos de todas.
7. **XML montado por concatenación de cadenas.** El módulo mete los textos libres en `<![CDATA[…]]>`
   (nombre, dirección, observaciones), pero **los números y los códigos no van escapados**. En
   código nuevo, `htmlspecialchars()` en todo lo que no sea CDATA.
8. **TLS sin verificar**: `CURLOPT_SSL_VERIFYPEER => false` en las tres llamadas
   (`:1804`, `:2771`, `AdminGlsshippingController.php:440`).
9. **`CURLOPT_CONNECTTIMEOUT => 5` y sin `CURLOPT_TIMEOUT`.** Si asmred acepta la conexión y luego
   se queda pensando, la petición se puede eternizar. En código nuevo, poner `CURLOPT_TIMEOUT`.
10. **La recogida (`EnviaCorreoAgencia`) no comprueba la respuesta.** Solo la escribe en el
    registro (`AdminGlsshippingController.php:450-453`). Si falla, nadie se entera.
11. **El teléfono y el móvil se rellenan el uno con el otro** si falta alguno
    (`glsshipping.php:1699-1700`). Si faltan los dos, viajan vacíos y GLS lo rechaza.

---

## 9. Fragmento PHP listo para copiar (estructura legacy, sin Composer, cURL nativo)

```php
<?php
/**
 * Seguimiento GLS/ASM reutilizando el GUID del modulo oficial 'glsshipping'.
 * Sin Composer, sin namespace, cURL nativo + SimpleXML.
 */
if (!defined('_PS_VERSION_')) {
    exit;
}

class MiGlsTracking
{
    const ENDPOINT = 'https://wsclientes.asmred.com/b2b.asmx';
    const NS_ASM = 'http://www.asmred.com/';
    const NS_SOAP12 = 'http://www.w3.org/2003/05/soap-envelope';

    /** Estados que GLS da por finales: no hace falta volver a consultar. */
    const ESTADOS_FINALES = array(7, 8, 5, 10, 12, 15, 17);

    const ESTADO_ENTREGADO = 7;
    const ESTADO_SIN_DATOS = -10;

    /** GUID del comercio, tal como lo guarda el modulo oficial. */
    public static function getGuid($idShop = null)
    {
        if ($idShop === null) {
            $idShop = (int) Context::getContext()->shop->id;
        }

        $guid = Configuration::get('GLS_GUID', null, null, $idShop);

        return $guid ? (string) $guid : '';
    }

    /** Codigo de barras (numero de seguimiento) de un pedido. */
    public static function getCodigoEnvio($idOrder)
    {
        $codigo = Db::getInstance(_PS_USE_SQL_SLAVE_)->getValue(
            'SELECT `codigo_envio` FROM `' . _DB_PREFIX_ . 'gls_envios`
              WHERE `id_envio_order` = ' . (int) $idOrder
        );

        return $codigo ? (string) $codigo : '';
    }

    /**
     * Consulta GetExpCli.
     *
     * @return array|false  array('codestado' => int, 'eventos' => array)
     */
    public static function getEstado($codigoEnvio, $idShop = null)
    {
        $codigoEnvio = trim((string) $codigoEnvio);
        $guid = self::getGuid($idShop);
        if ($codigoEnvio === '' || $guid === '') {
            return false;
        }

        $xml = '<?xml version="1.0" encoding="utf-8"?>'
            . '<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            . ' xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
            . ' xmlns:soap12="' . self::NS_SOAP12 . '">'
            . '<soap12:Body>'
            . '<GetExpCli xmlns="' . self::NS_ASM . '">'
            . '<codigo>' . htmlspecialchars($codigoEnvio, ENT_XML1, 'UTF-8') . '</codigo>'
            . '<uid>' . htmlspecialchars($guid, ENT_XML1, 'UTF-8') . '</uid>'
            . '</GetExpCli>'
            . '</soap12:Body></soap12:Envelope>';

        $ch = curl_init();
        curl_setopt_array($ch, array(
            CURLOPT_URL => self::ENDPOINT . '?op=GetExpCli',
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $xml,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HEADER => false,
            CURLOPT_FORBID_REUSE => true,
            CURLOPT_FRESH_CONNECT => true,
            CURLOPT_CONNECTTIMEOUT => 5,
            CURLOPT_TIMEOUT => 20,   // el modulo oficial NO lo pone: ponlo tu
            CURLOPT_HTTPHEADER => array('Content-Type: text/xml; charset=UTF-8'),
        ));
        $respuesta = curl_exec($ch);
        $error = curl_error($ch);
        curl_close($ch);

        if ($error || $respuesta === false || $respuesta === '') {
            return false;
        }

        // HTTP 200 no garantiza nada: hay que mirar el cuerpo.
        $doc = @simplexml_load_string($respuesta, null, 0, self::NS_SOAP12);
        if (empty($doc)) {
            return false;
        }
        $doc->registerXPathNamespace('asm', self::NS_ASM);

        $result = $doc->xpath('//asm:GetExpCliResponse/asm:GetExpCliResult');
        if (empty($result[0])) {
            return false;
        }

        $exp = $result[0]->xpath('//expediciones/exp');
        if (empty($exp[0])) {
            return false;
        }

        $codestado = $exp[0]->xpath('//expediciones/exp/codestado');
        if (empty($codestado[0])) {
            return false;
        }

        $eventos = array();
        $lista = $exp[0]->xpath('//expediciones/exp/tracking_list/tracking');
        foreach (is_array($lista) ? $lista : array() as $item) {
            $tipo = isset($item->tipo[0]) ? (string) $item->tipo[0] : '';
            if (!in_array($tipo, array('ESTADO', 'INCIDENCIA'), true)) {
                continue;
            }
            $eventos[] = array(
                'date' => isset($item->fecha[0]) ? (string) $item->fecha[0] : '',   // d/m/Y H:i:s
                'type' => $tipo,
                'code' => isset($item->codigo[0]) ? (string) $item->codigo[0] : '',
                'text' => isset($item->evento[0]) ? (string) $item->evento[0] : '',
            );
        }

        return array(
            'codestado' => (int) $codestado[0],
            'eventos' => $eventos,
        );
    }

    public static function estaEntregado($codestado)
    {
        return (int) $codestado === self::ESTADO_ENTREGADO;
    }

    public static function esEstadoFinal($codestado)
    {
        return in_array((int) $codestado, self::ESTADOS_FINALES, true);
    }
}
```

Uso:

```php
$codigo = MiGlsTracking::getCodigoEnvio(1234);
$estado = $codigo ? MiGlsTracking::getEstado($codigo) : false;
if ($estado !== false && MiGlsTracking::estaEntregado($estado['codestado'])) {
    // entregado
}
```

---

## 10. Qué NO se ha podido confirmar leyendo el código

- **Tabla completa de `codestado`.** Solo hay `7` (entregado), `-10` (sin datos) y la lista de
  estados finales `7,8,5,10,12,15,17`. El significado de `8`, `10`, `12`, `15` y `17` **no
  aparece**. Lo que sí se sabe por la web (no por el código) es que en `tracking_list` un
  `tipo=ESTADO` con `codigo=5` es una expedición anulada.
- **Códigos del `tracking_list`** (`<codigo>` de cada evento): no hay tabla.
- **Entorno de pruebas**: no existe en el módulo; se usa el GUID de pruebas contra producción.
- **Esquema completo de `GrabaServicios`**: el XML se monta en `glsshipping.php:1707-1794`; ahí
  está todo, pero no hay un esquema aparte ni documentación de qué campos son obligatorios.
- **Códigos de error de `Errores/Error`**: llega solo el texto.
- **Formato del `codbarras`** (longitud, prefijo): no se valida. Columna `varchar(50)`.
- **Qué operaciones ofrece `ecm.asmx`** (la URL guardada en `GLS_URL`): el módulo nunca la llama.

Sources: [omatech/gls-tracker](https://github.com/omatech/gls-tracker/blob/master/README.md)
