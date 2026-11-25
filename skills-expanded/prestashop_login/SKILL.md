---
name: prestashop_login
description: Cómo autenticar/loguear empleados (admin/back-office) y clientes (front) en PrestaShop 1.7, 8 y 9 desde código (módulos, endpoints AJAX standalone, passkeys/WebAuthn, 2FA/TOTP, login programático). Cubre la migración crítica del login admin a Symfony Security en PS9.
risk: high
source: community
date_added: '2026-05-24'
author: Ecom Experts
tags:
  - prestashop
  - login
  - authentication
  - symfony-security
  - webauthn
  - passkey
  - totp
  - 2fa
  - ps9
tools:
  - claude-code
  - antigravity
  - cursor
  - gemini-cli
  - codex-cli
---

# Login en PrestaShop 1.7 / 8 / 9

Guía para autenticar empleados (admin) y clientes (front) desde código. El cambio
GRANDE está en el **login admin de PS9**, que se migró a **Symfony Security** y rompe
todos los métodos legacy. El login de **clientes (front)** y el de **admin en PS ≤ 8**
NO cambiaron.

---

## 1. Diferencia clave PS ≤ 8 vs PS 9 (login ADMIN)

| Aspecto | PS 1.7 / 8 | PS 9 |
|---|---|---|
| Motor de login admin | Cookie legacy (`Cookie`) | **Symfony Security** (firewall `main`) |
| Hooks `actionAdminLoginControllerLoginBefore/After` | Existen | **ELIMINADOS** |
| `$cookie->id_employee = X; $cookie->write()` autentica | Sí | **NO** (cookie read-only para autorización) |
| Clase del user | `PrestaShopBundle\Security\Admin\Employee` (UserInterface) | `PrestaShopBundle\Entity\Employee\Employee` (Doctrine entity) |
| Fuente de verdad de la sesión | Cookie PS | Sesión Symfony (`PHPSESSID`) + token en `_security_main` |
| Requiere `EmployeeSession` Doctrine atada al token | No | **Sí** (sino logout "por seguridad") |

El login de **clientes (front)** es idéntico en todas las versiones (ver §5).

---

## 2. Login ADMIN en PS ≤ 8 (legacy) — sigue funcionando

```php
$employee = new Employee((int) $id_employee);
$cookie = Context::getContext()->cookie;
$cookie->id_employee   = (int) $employee->id;
$cookie->email         = $employee->email;
$cookie->profile       = (int) $employee->id_profile;
$cookie->passwd        = $employee->passwd;
$cookie->last_passwd_gen = $employee->last_passwd_gen;
$cookie->remote_addr   = (int) ip2long(Tools::getRemoteAddr());
if (class_exists('EmployeeSession')) {
    $cookie->registerSession(new EmployeeSession()); // PS 8.1+
}
$cookie->write();
$redirect = Context::getContext()->link->getAdminLink('AdminDashboard');
```

---

## 3. Login ADMIN en PS 9 — patrón CORRECTO (ticket + EventSubscriber)

> NO funciona: escribir `$_SESSION['_sf2_attributes']['_security_main']` a mano,
> ni `$cookie->id_employee`, ni bootear `AdminKernel` standalone (los servicios
> `security.*` NO son públicos: `$container->has('security.user_authenticator')`
> devuelve `false`). Todos acaban en **"Tu sesión se ha cerrado por motivos de
> seguridad"** (el `ContextListener::refreshUser` invalida el token).

El **único** método soportado es `UserAuthenticatorInterface::authenticateUser()`,
y SOLO se puede llamar **dentro de un request real** (no desde un script standalone).
Por eso el patrón es **ticket de un solo uso + EventSubscriber**:

### 3.1 Paso A — endpoint standalone emite un ticket (no autentica)
Tras validar credenciales (passkey/WebAuthn, etc.), NO toques la sesión Symfony.
Inserta un ticket en BD y redirige a una URL del admin con el token:

```php
$token = rtrim(strtr(base64_encode(random_bytes(32)), '+/', '-_'), '=');
Db::getInstance()->insert('mi_modulo_admin_tickets', [
    'token' => pSQL($token),
    'id_employee' => (int) $employee->id,
    'expires_at' => pSQL(date('Y-m-d H:i:s', time() + 30)), // TTL corto
    'used' => 0,
    'date_add' => pSQL(date('Y-m-d H:i:s')),
]);
// CRÍTICO: redirigir a /login (anónima, dentro del firewall main), NO a index.php.
$slug = trim(basename(rtrim((string) _PS_ADMIN_DIR_, DIRECTORY_SEPARATOR)), '/');
$redirect = rtrim(Tools::getShopDomainSsl(true), '/') . '/' . $slug . '/login?mi_ticket=' . rawurlencode($token);
```

### 3.2 Paso B — un EventSubscriber consume el ticket DENTRO del request

```php
// config/services.yml (solo PS9; en PS<=8 hay que BORRARLO o el container peta)
services:
    _defaults: { autowire: true, autoconfigure: true, public: false }
    Mi\Modulo\Security\MiAuthenticator: { autowire: true, public: false }
    Mi\Modulo\EventSubscriber\TicketSubscriber:
        autowire: true
        arguments: { $authenticator: '@Mi\Modulo\Security\MiAuthenticator' }
        tags: [{ name: kernel.event_subscriber }]
```

```php
final class TicketSubscriber implements EventSubscriberInterface
{
    public function __construct(
        private UserAuthenticatorInterface $userAuthenticator,
        private EmployeeProvider $employeeProvider,
        private MiAuthenticator $authenticator,           // AbstractAuthenticator, supports()=false
        private EntityManagerInterface $entityManager,
        private Security $security,
    ) {}

    public static function getSubscribedEvents(): array
    {
        // PRIORIDAD 4 = POR DEBAJO del firewall (prio 8). Si corres ANTES, el
        // ContextListener (que carga el token de sesión a prio 8) hace
        // setToken(null) y BORRA tu token recién creado → loop login infinito.
        return [KernelEvents::REQUEST => [['onRequest', 4]]];
    }

    public function onRequest(RequestEvent $event): void
    {
        if (!$event->isMainRequest()) return;
        $req = $event->getRequest();
        $token = (string) $req->query->get('mi_ticket', '');
        if ($token === '') return;
        $idEmployee = $this->consumeTicketAtomic($token); // valida + UPDATE used=1
        if (!$idEmployee) return;

        $email = (string) Db::getInstance()->getValue(
            "SELECT email FROM "._DB_PREFIX_."employee WHERE id_employee=".(int)$idEmployee." AND active=1"
        );
        $doctrineUser = $this->employeeProvider->loadUserByIdentifier($email);
        $req->attributes->set('_mi_email', $email); // para el authenticator

        // Login programático oficial Symfony:
        $this->userAuthenticator->authenticateUser($doctrineUser, $this->authenticator, $req);

        // CRÍTICO PS9: atar una EmployeeSession Doctrine al token. Sin esto, el
        // EmployeeSessionSubscriber del core hace logout "por seguridad".
        $sess = new EmployeeSession();
        $sess->setToken(sha1(uniqid('', true)));
        $doctrineUser->addSession($sess);
        $this->entityManager->persist($sess);
        $this->entityManager->flush();
        $tok = $this->security->getToken();
        if ($tok && class_exists(TokenAttributes::class)) {
            $tok->setAttribute(TokenAttributes::EMPLOYEE_SESSION, $sess);
        }

        // Cortocircuito SEGURO a prio 4: el ContextListener (prio 8 ya corrió)
        // persistirá el token en kernel.response aunque devolvamos respuesta.
        $slug = trim(basename(rtrim((string) _PS_ADMIN_DIR_, DIRECTORY_SEPARATOR)), '/');
        $event->setResponse(new RedirectResponse('/'.$slug.'/index.php?controller=AdminDashboard'));
    }
}
```

El authenticator auxiliar (no se ejecuta solo, solo lo usa `authenticateUser`):

```php
class MiAuthenticator extends AbstractAuthenticator implements InteractiveAuthenticatorInterface
{
    public function supports(Request $r): ?bool { return false; }  // nunca por el firewall
    public function authenticate(Request $r): Passport {
        return new SelfValidatingPassport(new UserBadge((string) $r->attributes->get('_mi_email','')));
    }
    public function onAuthenticationSuccess(Request $r, TokenInterface $t, string $f): ?Response { return null; }
    public function onAuthenticationFailure(Request $r, AuthenticationException $e): ?Response { return null; }
    public function isInteractive(): bool { return true; }
}
```

### 3.3 Las 3 reglas de oro (causas reales de fallo)
1. **services.yml** debe existir en PS9 **y** el container debe recompilarse
   (`Tools::clearSf2Cache()` o borrar `var/cache`) al crearlo/cambiarlo; si no, los
   subscribers no se registran y todo falla **en silencio** (sin error 500).
   En PS ≤ 8 ese services.yml debe **no existir** (referencia clases de Symfony
   6.x → el container peta). Genéralo/bórralo según `version_compare(_PS_VERSION_,'9.0.0','>=')`.
2. **Prioridad < 8** en el `kernel.request` del subscriber, y consumir el ticket
   en `/login` (anónima), NUNCA en `index.php` (protegida: el firewall rebota antes).
3. **EmployeeSession Doctrine atada al token** + usar `authenticateUser()`
   (no `Security::login()` con el `\Employee` legacy → `UnsupportedUserException`).

---

## 4. 2FA / TOTP gate en PS 9 (pantalla intermedia tras login)

Escucha `LoginSuccessEvent` para marcar la sesión pendiente, y `kernel.request`
(prio 5) para mostrar la pantalla del código. **NO redirijas a una URL inventada
tipo `index.php?totp_gate=1`: NO enruta en PS9 y cae en la welcome page de Symfony.**
En su lugar **muestra el formulario INLINE** (con `$event->setResponse(...)`) sobre la
propia petición del dashboard (que sí enruta), y que el form haga POST a la URI actual:

```php
public function onKernelRequest(RequestEvent $event): void {
    // ... exclusiones (/login, /logout, /modules/.., rutas del módulo) ...
    if ((int) $req->request->get('mi_totp_submit') === 1) {        // SUBMIT del código
        $event->setResponse($this->gateController->processSubmit($req));
        $event->stopPropagation(); return;
    }
    if ($session->get('totp_verified') === true) return;           // ya validado
    if (!$employeeTieneTotp) { $session->set('totp_verified', true); return; }
    // tiene TOTP y no validado → pintar el form INLINE sobre esta petición:
    $event->setResponse($this->gateController->renderForm($req));   // action = uri actual
    $event->stopPropagation();
}
```

**Campo "Código 2FA" en el formulario de login admin:**
- **PS ≤ 8**: el TOTP se valida DENTRO del form de login (hook `actionAdminLoginControllerLoginBefore`), así que SÍ hay que inyectar un campo "Código 2FA" en el formulario.
- **PS 9**: ese hook NO existe y el TOTP se valida en el gate intermedio post-login. El campo en el formulario es **redundante y confuso → quítalo en PS9** (no cargues el JS que lo inyecta). Gatea por `version_compare(_PS_VERSION_, '9.0.0', '>=')`.

> Resumen de la diferencia 2FA admin: **PS8 = código en el form de login**;
> **PS9 = pantalla intermedia (gate) tras el login**. NO mezclar; cada versión
> usa su mecanismo. PS8 no puede usar el gate Symfony (no tiene los subscribers).

---

## 5. Login de CLIENTES (front)

### 5.1 En un request NORMAL de PrestaShop (FrontController/controller)
El login nativo es simplemente:
```php
$customer = new Customer((int) $id_customer);
$this->context->updateCustomer($customer);             // establece la sesión + carrito
Hook::exec('actionAuthentication', ['customer' => $customer]);
Tools::redirect($this->context->link->getPageLink('my-account', true));
```
`updateCustomer()` es el método correcto: asocia el cliente al contexto, regenera la
sesión y recalcula el carrito. Hooks `actionAuthentication` / `actionCustomerLogoutAfter`
disponibles en todas las versiones.

### 5.2 ⚠️ CRÍTICO PS9: NO loguear al cliente desde un endpoint AJAX standalone
En **PS9 el front del cliente se autentica por la SESIÓN, NO por la cookie legacy**.
Escribir `$cookie->id_customer=...; $cookie->logged=1; $cookie->write();` desde un
`.php` standalone o un FrontController que hace `exit` **NO loguea** (se ve `logged=1`
en memoria pero el siguiente request da `is_logged=false` → **loop de login**). Síntoma
en log: `set_cookie_count=0` aunque `headers_sent=no` (Cookie::write no detecta cambios
o la sesión no se materializa con el exit).

**Solución (mismo patrón que el admin): ticket + request normal.**
1. El AJAX (que valida la passkey/credencial) **NO loguea**: inserta un ticket de un
   solo uso (p.ej. en una tabla `*_tokens` con `user_type='customer'`, TTL ~60s) y
   devuelve un redirect a un **FrontController GET** propio (`customer_login?t=TOKEN`).
2. Ese FrontController, en `init()`, valida/consume el ticket (DELETE atómico),
   `$this->context->updateCustomer($customer)` y `Tools::redirect(my-account)`. Como es
   un request NORMAL (no AJAX con exit), **la sesión PS9 sí se persiste**.

> Regla general PS9 (admin Y cliente): la sesión real se establece en el flujo nativo
> del kernel; un endpoint AJAX que hace `exit` NO la persiste. Para login programático,
> usa SIEMPRE el patrón **ticket de un solo uso → login en un request normal**.

### 5.2.bis Aplica a TODO login de cliente (passkey, TOTP, backup, recovery)
El patrón ticket→FrontController vale para cualquier autenticación de cliente que se
valide en AJAX: passkey, código TOTP (segundo factor por email+password), códigos de
backup, recuperación. En todos, tras verificar, NO escribas la cookie desde el AJAX:
emite el ticket y redirige al FrontController de login. Centraliza la función de
"login + redirect" para que devuelva la URL (ticket en PS9, my-account por cookie en
PS≤8) y que todos los flujos la usen.

### 5.3 Decisión de diseño
Si el cliente tiene TOTP activo, NO le pidas TOTP encima de la passkey: la passkey ya es
factor fuerte (entra directo, igual que el admin). Pedir TOTP tras passkey + hacer
`$cookie->logout()` mientras tanto deja al cliente deslogueado si el flujo no se completa.

### 5.4 ⚠️ El FrontController de login NO debe re-disparar `actionAuthentication`
El hook `actionAuthentication` del propio módulo 2FA suele hacer, si el cliente tiene
TOTP activo: `$cookie->logout()` + `Tools::redirect(authentication?totp=1)`. Por eso, en
el FrontController `customer_login` (al que se llega TRAS pasar el factor fuerte: passkey,
o TOTP/backup/recovery ya validado), haz SOLO `$context->updateCustomer($customer)` y el
redirect — **NO** `Hook::exec('actionAuthentication')`: lo re-dispararía y volvería a
pedir TOTP (y desloguearía). `updateCustomer()` por sí solo no dispara ese hook.
El flujo de login normal (email+contraseña) SÍ pasa por el AuthController de PS, que
dispara `actionAuthentication` y pide TOTP — correcto; tras validar el código se entra
por `customer_login` sin re-pedirlo.

---

## 6. Endpoints AJAX standalone en PS9 (.php fuera del routing)
- Define `_PS_ADMIN_DIR_` **ANTES** de `require config/config.inc.php` (sino PS hidrata
  contexto front en vez de admin y `$ctx->employee` queda vacío).
- Para IDENTIFICAR (no autorizar) al employee logueado: la cookie legacy a veces trae
  `id_employee`; si no, lee el email del blob serializado de la sesión Symfony nativa
  (`$_SESSION['_sf2_attributes']['_security_main']`, regex `s:5:"email";s:\d+:"([^"]+)"`)
  y resuelve `id_employee` por email en BD.
- Blinda el output JSON: `set_error_handler` que devuelva `true` + `ob_start()` +
  `register_shutdown_function` que descarte cualquier buffer que no empiece por `{`/`[`.
  PS9 emite muchos `Deprecated`/warnings que romperían `JSON.parse`.

---

## 6.bis WebAuthn (passkeys): challenge robusto e independiente del JS
- El `challenge` viaja DENTRO del `clientDataJSON` (estándar WebAuthn). NO dependas de
  que el JS reenvíe un `challengeId` aparte: si el JS está cacheado (CCC de PS) puede no
  enviarlo y el server recibe `challengeId=0` → "Attestation inválida" / "Invalid
  signature". En el server, si no llega el id, resuélvelo por el VALOR: decodifica el
  `challenge` del clientDataJSON (base64url → bin → `bin2hex`) y busca su fila en la
  tabla de challenges. Así funciona con cualquier versión del JS.
- En el LOGIN con passkey el usuario aún NO está identificado: `generateChallenge` NO
  debe exigir sesión; genera el reto SIN `user` (un challenge es solo un nonce). La
  identificación real ocurre al validar la firma (`verifyAssertion`). En el REGISTRO sí
  hace falta sesión (necesitas `user.id` para `navigator.credentials.create`).
- CCC (Parámetros avanzados → Rendimiento) cachea/combina los JS de módulos: tras editar
  un `.js` de módulo hay que vaciar caché o el navegador (incluso en incógnito) seguirá
  recibiendo el bundle viejo. Por eso conviene que el SERVER no dependa del JS.

## 7. Checklist de depuración login PS9
- ¿Aparece `onLoginSuccess`/subscriber en logs? NO → services.yml ausente o container
  no recompilado.
- ¿`login OK` pero rebota a `/login`? → token no persiste: subscriber a prioridad > 8,
  o ticket consumido en URL protegida.
- ¿"Tu sesión se ha cerrado por motivos de seguridad"? → falta EmployeeSession atada,
  o escribiste `_security_main` a mano.
- ¿Welcome page de Symfony? → redirigiste a una URL que no enruta (usa `/login` o
  `index.php?controller=...`, o pinta inline).
- ¿Cliente front entra y rebota a login (loop), `set_cookie_count=0`? → PS9 usa la
  SESIÓN, no la cookie legacy: loguea vía ticket + FrontController normal (§5.2), no
  desde el AJAX.
- ¿"Attestation inválida" / "challenge_id no encontrado: 0"? → el JS no envía
  `challengeId` (cacheado por CCC); resuelve el challenge por su valor desde
  clientDataJSON en el server (§6.bis).

## Fuentes
- devdocs.prestashop-project.org/9/modules/core-updates/9.0/
- PR #35983 (Migrate BO login to Symfony)
- Symfony 6.4 Security: programmatic login & authentication events.
