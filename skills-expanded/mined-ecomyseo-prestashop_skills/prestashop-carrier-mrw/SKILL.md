---
name: prestashop-carrier-mrw
description: API SOAP de MRW (SAGEC) tal y como la usan los módulos oficiales mrwcarrier 8.0.7 y mrwtracking 3.8.1 de PrestaShop. Endpoints .asmx reales de producción y pruebas, la cabecera SOAP AuthInfo, las claves exactas de ps_configuration y la tabla de abonados donde el comerciante ya tiene puestas sus credenciales, seguimiento, etiquetas PDF y las trampas del código. Usar al integrar MRW, al leer sus credenciales desde otro módulo o al consultar el estado de un envío MRW.
---

# MRW — API real, leída de los módulos oficiales

**Fuente:** `mrwcarrier` (versión
**8.0.7**, `config.xml:5`) y `…\mrwtracking\` (versión **3.8.1**, `config.xml:5`), ambos de MRW
IBERIA. **Solo lectura: no se modifica ni un byte.**

MRW se reparte en **dos módulos**:

| Módulo | Qué hace | Web service |
|---|---|---|
| `mrwcarrier` | Crea envíos, pide etiquetas, consulta puntos de recogida, consulta estados | `sagec.mrw.es/MRWEnvio.asmx` + `trackingservice.mrw.es/TrackingService.svc` |
| `mrwtracking` | Solo seguimiento nacional | `seguimiento.mrw.es/swc/wssgmntnvs.asmx` |

Toda la API es **SOAP 1.1 sobre `.asmx`** (SAGEC, *Servicio Automatizado de Generación de
Envíos*). Los módulos la llaman con la extensión `SoapClient` de PHP leyendo el WSDL, **no con
XML a pelo**.

---

## 1. Endpoints reales

### 1.1 Envíos y etiquetas — SAGEC

`mrwcarrier/mrwcarrier.php:2720-2725`, `:4407-4413`, `:6679-6687`,
`mrwcarrier/controllers/admin/AdminMrwCarrierController.php:345-353`, `:423-431`:

| Entorno | URL | WSDL |
|---|---|---|
| **Producción** (`MRWCARRIER_ENTORNO = 'mrw_pro'`) | `https://sagec.mrw.es/MRWEnvio.asmx` | `https://sagec.mrw.es/MRWEnvio.asmx?WSDL` |
| **Pruebas** (`= 'mrw_pre'`) | `https://sagec-test.mrw.es/MRWEnvio.asmx` | `https://sagec-test.mrw.es/MRWEnvio.asmx?WSDL` |

El módulo construye la URL como `$url . '?WSDL'` (`mrwcarrier.php:2726`).

**Operaciones confirmadas en el código:**

| Operación | Devuelve | Dónde |
|---|---|---|
| `TransmEnvio` | `TransmEnvioResult` → `Estado`, `Mensaje`, `NumeroSolicitud`, `NumeroEnvio` | `mrwcarrier.php:2753`, `:2766-2796` |
| `TransmEnvioInternacional` | `TransmEnvioInternacionalResult` → los mismos campos | `mrwcarrier.php:2908`, `:2921-2951` |
| `EtiquetaEnvio` | **`GetEtiquetaEnvioResult`** → `Estado`, `Mensaje`, `EtiquetaFile` | `mrwcarrier.php:4428`, `:4435-4442`, `:6742` |
| `EtiquetaEnvioInternacional` | **`GetEtiquetaEnvioInternacionalResult`** → los mismos campos | `AdminMrwCarrierController.php:481-487`, `mrwcarrier.php:6833` |
| `GetPointsByCP` | `GetPointsByCPResult` (puntos de recogida por código postal) | `mrwcarrier/ajax_locations.php:339-345` |

> **El nombre de la operación y el del resultado NO coinciden.** Se llama a `EtiquetaEnvio` y el
> nodo de respuesta es `GetEtiquetaEnvioResult`. Es así en el WSDL de MRW; no es una errata del
> módulo.

Para `GetPointsByCP` el WSDL exige los nodos anidados con su espacio de nombres explícito
(`ajax_locations.php:329-339`), y por eso el módulo usa `SoapVar`:

```
GetPointsByCP → request → Point → CodigoPostal      (todos en xmlns http://www.mrw.es/)
```

El WSDL que usa esa llamada está escrito en minúsculas: `https://sagec.mrw.es/mrwenvio.asmx?WSDL`
(`ajax_locations.php:305`). Es el mismo servicio.

### 1.2 Seguimiento — TrackingService (usado por `mrwcarrier`)

`mrwcarrier/mrwcarrier.php:7352-7357`:

| Entorno | Servicio | WSDL |
|---|---|---|
| Producción | `https://trackingservice.mrw.es/TrackingService.svc/TrackingServices` | `https://trackingservice.mrw.es/TrackingService.svc?wsdl` |
| Pruebas | `https://trackingservice-test.mrw.es/TrackingService.svc/TrackingServices` | `https://trackingservice-test.mrw.es/TrackingService.svc?wsdl` |

Operación: **`GetEnvios`** (`mrwcarrier.php:7392`).

### 1.3 Seguimiento — wssgmntnvs (usado por `mrwtracking`)

`mrwtracking/mrwtracking.php:121` (valor por defecto de `MRWTRACKING_WS_TRACKING`):

```
https://seguimiento.mrw.es/swc/wssgmntnvs.asmx        (+ '?WSDL', mrwtracking.php:761)
```

Operación: **`SeguimientoNumeroEnvioMRWNacional`** (`mrwtracking.php:787`).

**NO CONFIRMADO:** no hay entorno de pruebas para este servicio en el código.

### 1.4 Páginas públicas de seguimiento

- `https://www.mrw.es/seguimiento_envios/MRW_historico_nacional.asp?enviament=@`
  — es la `url` del transportista, con `@` como marcador
  (`mrwcarrier/mrwcarrier.php:43`, `mrwtracking/mrwtracking.php:1025`)
- `https://www.mrw.es/seguimiento/envio-historico.asp?envio=<numero>`
  (`mrwcarrier/mrwcarrier.php:5126`)
- Buscador de franquicias:
  `https://www.mrw.es/oficina_transporte_urgente/MRW_buscador_franquicia.asp`
  (`mrwcarrier.php:2260`)

---

## 2. Autenticación

**Cabecera SOAP `AuthInfo` en el espacio de nombres `http://www.mrw.es/`**, con cinco campos.
`mrwcarrier/mrwcarrier.php:3335-3341` y `:2749`:

```php
$cabeceras = array(
    'CodigoFranquicia'   => $rowSubscriber['agency'],      // Obligatorio
    'CodigoAbonado'      => $rowSubscriber['subscriber'],  // Obligatorio
    'CodigoDepartamento' => $rowSubscriber['department'],  // Opcional
    'UserName'           => $rowSubscriber['user'],        // Obligatorio
    'Password'           => $rowSubscriber['password'],    // Obligatorio
);
$header = new SoapHeader('http://www.mrw.es/', 'AuthInfo', $cabeceras);
$clientMRW->__setSoapHeaders($header);
```

Los comentarios de «Obligatorio» / «Opcional» son del propio módulo.

**Los dos servicios de seguimiento NO usan `AuthInfo`:** meten las credenciales **en los
parámetros** de la operación.

- `TrackingService.GetEnvios` (`mrwcarrier.php:7380-7388`): `login`, `pass`, `codigoIdioma`
  (`'3082'` = español de España), `tipoFiltro` (`'0'`), `valorFiltroDesde`, `valorFiltroHasta`,
  `tipoInformacion` (`'0'`).
- `SeguimientoNumeroEnvioMRWNacional` (`mrwtracking.php:845-852`): `Franquicia`, `Cliente`,
  `Password`, `NumeroMRW`, `Referencia`, `Agrupado` (`0`).

**No hay token ni OAuth.** La contraseña viaja en cada petición.

---

## 3. Claves EXACTAS de configuración

### 3.1 `mrwcarrier` — prefijo `MRWCARRIER_`

El prefijo se construye en `mrwcarrier/mrwcarrier.php:44`:
`$this->rename = strtoupper($this->name) . '_';`

Lista literal de claves (todas con el prefijo `MRWCARRIER_`):

```
MRWCARRIER_ENTORNO                  'mrw_pre' | 'mrw_pro'
MRWCARRIER_FRANQUICIA               código de franquicia
MRWCARRIER_ABONADO                  código de abonado
MRWCARRIER_USUARIO                  usuario SAGEC
MRWCARRIER_PASSWORD                 contraseña SAGEC
MRWCARRIER_URLWEBSERVICE            URL del WS
MRWCARRIER_CARRIER_ID_MRW           id(s) del transportista MRW creado al instalar
MRWCARRIER_SERVICE_MRW              servicio nacional por defecto
MRWCARRIER_SERVICE_MRW_INT          servicio internacional por defecto
MRWCARRIER_BEFORE_SENDING_MRW       estado de pedido que dispara el envío
MRWCARRIER_AFTER_SENDING_MRW        estado al que pasa el pedido tras enviarlo
MRWCARRIER_LAST_EXECUTE_MRW         marca de tiempo de la última ejecución
MRWCARRIER_ACTIVE_DEBUG_MRW         '0' | '1'
MRWCARRIER_ACCEPTANCE_TERMS_MRW
MRWCARRIER_ALLOW_POINT_DELIVERY     entrega en Point
MRWCARRIER_DEFAULT_SLOT_MRW         franja horaria por defecto
MRWCARRIER_DNI_REQUIRED_MRW
MRWCARRIER_MAIL_WHENSENT_MRW
MRWCARRIER_MESSAGE_TYPE_MRW
MRWCARRIER_MULTITRANS_MRW
MRWCARRIER_TICKET_MRW
MRWCARRIER_GESTION_BULTOS
MRWCARRIER_AGRUPAR_BULTOS
MRWCARRIER_DESGLOSE_BULTOS
MRWCARRIER_CRON_TOKEN               token del cron de estados
```

Referencias: `mrwcarrier.php:48-65`, `:103-111`, y los `Configuration::updateValue` de
`displayFrmConfig()`.

### 3.2 IMPORTANTE: las credenciales VIVAS están en `ps_mrwcarrier_subs`

El módulo es **multiabonado**. Las claves `MRWCARRIER_FRANQUICIA`, `_ABONADO`, `_USUARIO` y
`_PASSWORD` son el juego heredado; lo que realmente se manda en la cabecera `AuthInfo` sale de la
tabla `ps_mrwcarrier_subs` (`mrwcarrier.php:447-462`):

```sql
CREATE TABLE ps_mrwcarrier_subs (
    id_subscriber  int(11) AUTO_INCREMENT,
    id_shop        int(11) DEFAULT 1,
    id_name        varchar(25),
    environment    varchar(10),    -- 'mrw_pre' | 'mrw_pro'
    agency         varchar(10),    -- CodigoFranquicia
    subscriber     varchar(10),    -- CodigoAbonado
    department     varchar(100),   -- CodigoDepartamento
    user           varchar(100),   -- UserName
    password       varchar(100),   -- Password  (EN CLARO, sin cifrar)
    service        varchar(5),
    service_int    varchar(5),
    is_default     varchar(1) DEFAULT 'S',
    date           DATE
)
```

Se lee con `getHeaderConfigMRW()` (`mrwcarrier.php:3317-3344`), que busca el abonado del pedido en
`ps_mrwcarrier_mrw` y, si no lo encuentra, cae en `getDefaultSubscriber($id_shop)`
(`:3066-3071`). **Un módulo nuevo debe leer de esa tabla, no de `ps_configuration`.**

La contraseña está **en claro**. No hace falta descifrar nada, pero tampoco se debe volcar a un
registro.

### 3.3 Tabla de envíos: `ps_mrwcarrier_mrw`

`mrwcarrier.php:377-392`:

```sql
id_mrwcarrier_mrw, id_shop, order_id, send_num_mrw (VARCHAR 100 = NÚMERO DE ENVÍO),
params_mrw, date, print, cant, subscriber, service, saturday, agency,
backReturn, mrw_warehouse, mrw_slot
```

### 3.4 `mrwtracking` — prefijo `MRWTRACKING_`

`mrwtracking/mrwtracking.php:25`, `:121-123`, `:136-141`:

```
MRWTRACKING_WS_TRACKING     por defecto https://seguimiento.mrw.es/swc/wssgmntnvs.asmx
MRWTRACKING_FRANQUICIA
MRWTRACKING_ABONADO
MRWTRACKING_PASSWORD        (sin usuario: este WS solo pide franquicia + cliente + contraseña)
MRWTRACKING_ACTIVE_DEBUG
MRWTRACKING_FLG_ENTREGADO   1 = al detectar «entregado», pasa el pedido al estado 5
```

Tabla propia: `ps_mrwtracking_tracking` (`mrwtracking.php:58-72`) con
`id_order`, `num_expedicion`, `estado`, `file_firma`, `json_response`, `date_updated`.

**Precedente de reutilización entre módulos:** `mrwtracking` lee una clave de `mrwcarrier`,
`Configuration::get('MRWCARRIER_AFTER_SENDING_MRW')` (`mrwtracking.php:602`). Exactamente lo que
un módulo nuevo debería hacer con las credenciales.

---

## 4. Detectar el módulo

```php
if (Module::isInstalled('mrwcarrier') && Module::isEnabled('mrwcarrier')) {
    $abonado = Db::getInstance(_PS_USE_SQL_SLAVE_)->getRow(
        'SELECT `environment`, `agency`, `subscriber`, `department`, `user`, `password`
           FROM `' . _DB_PREFIX_ . 'mrwcarrier_subs`
          WHERE `id_shop` = ' . (int) Context::getContext()->shop->id . '
            AND `is_default` = "S"'
    );
}
```

Nombres en `ps_module`: **`mrwcarrier`** y **`mrwtracking`** (`config.xml:3` de cada uno).

Para saber si un `id_carrier` es de MRW: `Configuration::get('MRWCARRIER_CARRIER_ID_MRW')`
(`mrwcarrier.php:103`; puede contener varios id).

---

## 5. Seguimiento

### 5.1 Vía `TrackingService.GetEnvios` (lo que usa `mrwcarrier`)

`mrwcarrier/mrwcarrier.php:7344-7470`.

```php
$params = array(
    'login'            => $usuario,
    'pass'             => $contrasena,
    'codigoIdioma'     => '3082',        // español de España
    'tipoFiltro'       => '0',
    'valorFiltroDesde' => $numeroEnvio,
    'valorFiltroHasta' => $numeroEnvio,  // el mismo: consulta de un solo envío
    'tipoInformacion'  => '0',
);
$response = $client->GetEnvios($params);
```

La respuesta **no tiene una forma estable**: el módulo prueba tres estructuras
(`mrwcarrier.php:7414-7447`):

1. `GetEnviosResult → Seguimiento → Abonado → SeguimientoAbonado → Seguimiento[] → EstadoDescripcion`
2. `GetEnviosResult → Seguimiento → Seguimiento[] → EstadoDescripcion`
3. `GetEnviosResult → Seguimiento → EstadoDescripcion`

Se queda con el **último** elemento del array (`end($seguimientos)`).

**Mapeo de estado** (`mrwcarrier.php:7449-7455`): solo hay dos resultados.

| `EstadoDescripcion` (en mayúsculas) | Devuelve |
|---|---|
| `ENTREGADO` | `'ENTREGADO'` |
| cualquier otra cosa | `'EN_TRANSITO'` |

Si en `MensajeSeguimiento` viene el texto `No se encontraron resultados`, el módulo también lo
da por `EN_TRANSITO` (`:7457-7462`).

### 5.2 Vía `SeguimientoNumeroEnvioMRWNacional` (lo que usa `mrwtracking`)

`mrwtracking/mrwtracking.php:758-830`.

```php
$params = array(
    'Franquicia' => Configuration::get('MRWTRACKING_FRANQUICIA'),
    'Cliente'    => Configuration::get('MRWTRACKING_ABONADO'),
    'Password'   => Configuration::get('MRWTRACKING_PASSWORD'),
    'NumeroMRW'  => $numeroEnvio,
    'Referencia' => 'PEDIDO-' . $id_order,
    'Agrupado'   => 0,
);
$r = $client->SeguimientoNumeroEnvioMRWNacional($params);
```

Respuesta: `SeguimientoNumeroEnvioMRWNacionalResult` con

- `Estado` — **0 = la petición ha fallado, 1 = OK** (`mrwtracking.php:799`, `:807`)
- `Mensaje` — texto del error
- `Envio` → `Numero`, `Estado`, `EstadoDescripcion`, `FechaEntrega`, `HoraEntrega`

**Código de estado del envío** (`mrwtracking.php:586`, `:642`):

| `Envio->Estado` | Significado |
|---|---|
| `'00'` | **ENTREGADO** — el módulo guarda el seguimiento como definitivo y, si `MRWTRACKING_FLG_ENTREGADO = 1`, pone el pedido en el estado **5** (`$this->finalStatus`, `mrwtracking.php:26`) |
| cualquier otro | en curso — se vuelve a consultar en la siguiente pasada |

**NO CONFIRMADO:** la tabla completa de códigos de `Envio->Estado` de MRW. El código solo
distingue `'00'`. No hay ninguna otra lista en ninguno de los dos módulos. Lo único que se
aprovecha además es el texto `EstadoDescripcion`, que se guarda en mayúsculas en
`ps_mrwtracking_tracking.estado`.

---

## 6. Etiquetas

Operación **`EtiquetaEnvio`** (nacional) / **`EtiquetaEnvioInternacional`**.
`mrwcarrier/mrwcarrier.php:4531-4545` y `AdminMrwCarrierController.php:376-408`:

```php
$params = array(
    'request' => array(
        'NumeroEnvio'            => $numeros,      // uno o varios, separados
        'SeparadorNumerosEnvio'  => ',',
        'FechaInicioEnvio'       => '',            // o 'd/m/Y'
        'FechaFinEnvio'          => '',
        'TipoEtiquetaEnvio'      => '0',
        'ReportTopMargin'        => '1100',        // internacional: '20'
        'ReportLeftMargin'       => '650',         // internacional: '20'
    ),
);
$r = $client->EtiquetaEnvio($params);
// $r->GetEtiquetaEnvioResult->Estado:  0 = error (mirar ->Mensaje), 1 = OK
// $r->GetEtiquetaEnvioResult->EtiquetaFile = el PDF
```

**Formato: PDF.** El campo del WSDL es `base64Binary`, y **`SoapClient` ya lo descodifica**: el
módulo escribe `EtiquetaFile` directamente en el fichero, sin `base64_decode`
(`mrwcarrier.php:6865-6874`, `generateLabelsPDF()`). Si se construye el SOAP a mano con cURL,
**hay que descodificar el base64 uno mismo**.

Con varios pedidos, el módulo pide una sola llamada con los números unidos por `,`, guarda
`MRWNacLabels.pdf` y `MRWIntLabels.pdf` y, si hay de los dos tipos, los mete en un ZIP
(`AdminMrwCarrierController.php:239-296`).

Hay además una URL de etiqueta por navegador que se monta con
`&NumSol=<NumeroSolicitud>&Us=<UserName>&NumEnv=<NumeroEnvio>` (`mrwcarrier.php:2794-2795`).

---

## 7. Número de seguimiento

De `TransmEnvio` sale `TransmEnvioResult->NumeroEnvio` (`mrwcarrier.php:2796`), y el módulo lo
escribe en **tres sitios** (`mrwcarrier.php:3092`, `:3109`, `:3167`):

```
ps_mrwcarrier_mrw.send_num_mrw     varchar(100)
ps_orders.shipping_number
ps_order_carrier.tracking_number   (solo si pasa Validate::isTrackingNumber(), :3166)
```

**NO CONFIRMADO:** el formato (longitud, prefijo) del `NumeroEnvio`. Los módulos no lo validan ni
lo describen. **No se puede adivinar que un número es de MRW solo mirándolo.**

---

## 8. Trampas vistas en este código

1. **La extensión SOAP de PHP es obligatoria.** Los dos módulos lo comprueban con
   `class_exists('SoapClient')` y avisan en pantalla si falta (`mrwcarrier.php:1102`,
   `mrwtracking.php:267`). Sin ella no funciona nada.
2. **Nombre de operación ≠ nombre del resultado.** `EtiquetaEnvio` → `GetEtiquetaEnvioResult`.
3. **`Estado` invertido respecto a lo intuitivo.** En MRW **0 = error** y **1 = OK**
   (`mrwcarrier.php:2770`, `:2787`; `mrwtracking.php:799`, `:807`). El HTTP siempre es 200.
4. **La respuesta de `GetEnvios` cambia de forma.** Tres estructuras posibles; hay que probarlas
   todas o el estado se pierde en silencio (`mrwcarrier.php:7414-7447`).
5. **`GetPointsByCP` exige `SoapVar` con espacio de nombres explícito.** Pasar un array llano no
   funciona: el WSDL espera `GetPointsByCP → request → Point → CodigoPostal` con
   `xmlns="http://www.mrw.es/"` en cada nodo (`ajax_locations.php:329-339`).
6. **TLS sin verificar** en el cliente de seguimiento: `verify_peer` y `verify_peer_name` a
   `false` en el `stream_context` (`mrwcarrier.php:7367-7370`).
7. **Códigos postales recortados por país** antes de mandarlos: `PT` a 4 dígitos, `ES` a 5
   (`mrwcarrier.php:3357-3360`). Si se manda el código postal portugués completo (`1234-567`),
   MRW lo rechaza.
8. **`checkMrwShipmentStatus` devuelve `false` si falta cualquiera de los tres datos**
   (`mrwcarrier.php:7346-7348`), sin decir cuál.
9. **`$rowSubscriber` puede no existir.** `getHeaderConfigMRW()` (`:3317`) usa `$rowSubscriber`
   sin comprobar que `getDefaultSubscriber()` haya devuelto algo: si no hay ningún abonado por
   defecto, en PHP 8 salta un aviso y viajan cabeceras vacías → «usuario o contraseña
   incorrectos» que no tiene nada que ver con la contraseña.
10. **La contraseña está en claro en `ps_mrwcarrier_subs.password`.** No volcarla a ningún
    registro ni a ninguna respuesta AJAX.

---

## 9. Fragmento PHP listo para copiar (estructura legacy, sin Composer)

Consulta el estado de un envío MRW reutilizando el abonado que el módulo `mrwcarrier` ya tiene
configurado. Usa `SoapClient`, que es una **extensión de PHP**, no una dependencia de Composer.

```php
<?php
/**
 * Seguimiento MRW reutilizando la configuracion del modulo oficial 'mrwcarrier'.
 * Sin Composer, sin namespace. SoapClient es una extension de PHP, no una dependencia.
 */
if (!defined('_PS_VERSION_')) {
    exit;
}

class MiMrwTracking
{
    /**
     * Abonado por defecto de la tienda, desde la tabla del modulo oficial.
     * Devuelve array con environment, agency, subscriber, department, user, password.
     */
    public static function getAbonado($idShop = null)
    {
        if ($idShop === null) {
            $idShop = (int) Context::getContext()->shop->id;
        }

        $fila = Db::getInstance(_PS_USE_SQL_SLAVE_)->getRow(
            'SELECT `environment`, `agency`, `subscriber`, `department`, `user`, `password`
               FROM `' . _DB_PREFIX_ . 'mrwcarrier_subs`
              WHERE `id_shop` = ' . (int) $idShop . '
                AND `is_default` = "S"'
        );

        if (!is_array($fila) || empty($fila['user'])) {
            // Sin abonado por defecto en esta tienda: probamos el primero que haya.
            $fila = Db::getInstance(_PS_USE_SQL_SLAVE_)->getRow(
                'SELECT `environment`, `agency`, `subscriber`, `department`, `user`, `password`
                   FROM `' . _DB_PREFIX_ . 'mrwcarrier_subs`
                  ORDER BY `id_subscriber` ASC'
            );
        }

        return is_array($fila) ? $fila : array();
    }

    /** Numero de envio MRW de un pedido (tabla del modulo oficial). */
    public static function getNumeroEnvio($idOrder)
    {
        $numero = Db::getInstance(_PS_USE_SQL_SLAVE_)->getValue(
            'SELECT `send_num_mrw` FROM `' . _DB_PREFIX_ . 'mrwcarrier_mrw`
              WHERE `order_id` = ' . (int) $idOrder
        );

        return $numero ? (string) $numero : '';
    }

    /**
     * Estado del envio via TrackingService.GetEnvios.
     *
     * @return string|false 'ENTREGADO', 'EN_TRANSITO' o false si no se pudo consultar
     */
    public static function getEstado($numeroEnvio)
    {
        if (!class_exists('SoapClient')) {
            return false;   // la extension SOAP de PHP no esta activa
        }

        $numeroEnvio = trim((string) $numeroEnvio);
        if ($numeroEnvio === '') {
            return false;
        }

        $abonado = self::getAbonado();
        if (empty($abonado['user']) || empty($abonado['password'])) {
            return false;
        }

        $wsdl = (isset($abonado['environment']) && $abonado['environment'] === 'mrw_pro')
            ? 'https://trackingservice.mrw.es/TrackingService.svc?wsdl'
            : 'https://trackingservice-test.mrw.es/TrackingService.svc?wsdl';

        try {
            $client = new SoapClient($wsdl, array(
                'trace' => true,
                'exceptions' => true,
                'soap_version' => SOAP_1_1,
                'connection_timeout' => 10,
            ));
        } catch (SoapFault $e) {
            return false;
        }

        try {
            $respuesta = $client->GetEnvios(array(
                'login' => $abonado['user'],
                'pass' => $abonado['password'],
                'codigoIdioma' => '3082',
                'tipoFiltro' => '0',
                'valorFiltroDesde' => $numeroEnvio,
                'valorFiltroHasta' => $numeroEnvio,
                'tipoInformacion' => '0',
            ));
        } catch (SoapFault $e) {
            return false;
        }

        $descripcion = self::extraerDescripcion($respuesta);
        if ($descripcion === null) {
            return false;
        }

        return (Tools::strtoupper($descripcion) === 'ENTREGADO') ? 'ENTREGADO' : 'EN_TRANSITO';
    }

    /**
     * La respuesta de GetEnvios llega con TRES estructuras distintas segun el caso.
     * Hay que probarlas todas o el estado se pierde sin un solo error.
     */
    private static function extraerDescripcion($respuesta)
    {
        $result = null;
        if (is_object($respuesta) && isset($respuesta->GetEnviosResult)) {
            $result = $respuesta->GetEnviosResult;
        } elseif (is_array($respuesta) && isset($respuesta['GetEnviosResult'])) {
            $result = (object) $respuesta['GetEnviosResult'];
        }

        if (!$result || !isset($result->Seguimiento)) {
            return null;
        }

        $wrapper = is_array($result->Seguimiento) ? $result->Seguimiento[0] : $result->Seguimiento;

        // 1) Abonado -> SeguimientoAbonado -> Seguimiento[]
        if (isset($wrapper->Abonado)) {
            $abonado = is_array($wrapper->Abonado) ? $wrapper->Abonado[0] : $wrapper->Abonado;
            if (isset($abonado->SeguimientoAbonado)) {
                $sa = is_array($abonado->SeguimientoAbonado)
                    ? $abonado->SeguimientoAbonado[0]
                    : $abonado->SeguimientoAbonado;
                if (isset($sa->Seguimiento)) {
                    $lista = is_array($sa->Seguimiento) ? $sa->Seguimiento : array($sa->Seguimiento);
                    $ultimo = end($lista);

                    return isset($ultimo->EstadoDescripcion) ? trim((string) $ultimo->EstadoDescripcion) : null;
                }
            }
        }

        // 2) Seguimiento -> Seguimiento[]
        if (isset($wrapper->Seguimiento)) {
            $lista = is_array($wrapper->Seguimiento) ? $wrapper->Seguimiento : array($wrapper->Seguimiento);
            $ultimo = end($lista);

            return isset($ultimo->EstadoDescripcion) ? trim((string) $ultimo->EstadoDescripcion) : null;
        }

        // 3) EstadoDescripcion directo
        if (isset($wrapper->EstadoDescripcion)) {
            return trim((string) $wrapper->EstadoDescripcion);
        }

        return null;
    }
}
```

Uso:

```php
$numero = MiMrwTracking::getNumeroEnvio(1234);
$estado = $numero ? MiMrwTracking::getEstado($numero) : false;   // 'ENTREGADO' | 'EN_TRANSITO' | false
```

---

## 10. Qué NO se ha podido confirmar leyendo el código

- **Tabla completa de códigos de estado de MRW.** El código solo distingue `Envio->Estado == '00'`
  (entregado) y el texto `EstadoDescripcion == 'ENTREGADO'`. No hay ninguna lista de códigos en
  ninguno de los dos módulos.
- **Formato del `NumeroEnvio`**: no se valida ni se describe.
- **`SOAPAction` y espacio de nombres para llamar por cURL** a `wssgmntnvs.asmx` y a
  `TrackingService.svc`: los módulos usan `SoapClient` con el WSDL, así que esos datos no aparecen
  en el código. El único espacio de nombres confirmado es `http://www.mrw.es/`, y solo para la
  cabecera `AuthInfo` de `MRWEnvio.asmx`.
- **Estructura completa del `TransmEnvio`**: `getParamsMRW()` monta decenas de campos a lo largo
  de cientos de líneas de `mrwcarrier.php`. Para replicarlo hay que leer esa función.
- **Entorno de pruebas de `seguimiento.mrw.es`**: no aparece.
- **Códigos de error de SAGEC**: solo llega el texto de `Mensaje`; no hay tabla.
