---
name: authn-identity
description: Autenticación e identidad para la API NestJS y sus clientes web/mobile — OAuth 2.x/OIDC con authorization code + PKCE, sesiones vs JWT y dónde guardar tokens, rotación de refresh tokens, hashing de contraseñas según OWASP, MFA, recuperación de cuenta sin enumeración de usuarios, verificación de email/teléfono, links con token de un solo uso y alta de usuario/profesional con verificación. Usar al diseñar o revisar login, registro, reset de contraseña, emisión de tokens, cierre de sesión o cualquier flujo que decida QUIÉN es el actor.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Autenticación e identidad

Responde una sola pregunta: **¿quién es el actor y cómo lo probó?** Qué puede hacer ese
actor es `authz-access-control`. El marco general (OWASP Top 10, secretos, headers) vive en
`security-guardrails`; acá está el detalle de los flujos.

## 1. Elegir el mecanismo

| Cliente | Mecanismo | Dónde vive la credencial |
|---|---|---|
| Web propia con SSR / mismo sitio | Sesión de servidor o token en cookie | Cookie `HttpOnly` + `Secure` + `SameSite` |
| SPA contra API en otro origen | Authorization code + PKCE, idealmente vía BFF | Cookie `HttpOnly` del BFF; nunca en `localStorage` |
| App mobile | Authorization code + PKCE con navegador del sistema | Almacenamiento seguro del SO (Keychain / Keystore) |
| Servicio a servicio | Client credentials | Secret manager |

- **Nunca guardes tokens ni identificadores de sesión en `localStorage`**: OWASP lo desaconseja
  porque cualquier JavaScript de la página los lee — un solo XSS se lleva la sesión. Una cookie
  `HttpOnly` no es legible desde JS. `sessionStorage` reduce la persistencia, no el riesgo de XSS.
- Cookie de sesión ⇒ necesitás defensa CSRF (`SameSite` + token anti-CSRF en mutaciones).
- JWT no es "más seguro" que una sesión: es **sin estado**, y por eso no se puede revocar
  sin agregar estado (lista de revocación o versión de sesión). Si necesitás cierre de sesión
  inmediato —en salud lo necesitás—, asumí ese estado desde el diseño.

## 2. OAuth 2.x / OIDC — reglas de RFC 9700 (Security BCP)

1. Flujo **authorization code con PKCE** siempre. Clientes públicos **deben** usar PKCE; para
   confidenciales es recomendado; el servidor de autorización debe soportarlo.
2. **Prohibido** el grant de contraseña (resource owner password credentials): RFC 9700 dice
   MUST NOT. El implicit grant (`response_type=token`) no se usa.
3. `redirect_uri` con **coincidencia exacta** de string (única excepción: puerto en `localhost`
   de apps nativas). Nada de comodines ni prefijos.
4. Access tokens de **vida corta**, restringidos por audiencia (`aud`) y por alcance mínimo.
5. Refresh tokens de clientes públicos: **rotación** o sender-constrained (DPoP / mTLS).
6. OIDC: validá `iss`, `aud`, `exp`, `nonce` y la firma del ID token contra el JWKS del emisor.
   El ID token identifica al usuario ante el cliente; **no** es credencial para tu API.

## 3. Validación de JWT en la API

- Fijá el algoritmo esperado en el verificador; nunca aceptes el `alg` que trae el token
  (ataques `none` y confusión HS/RS).
- Validá firma, `exp`, `iss`, `aud`. Un JWT decodificado sin verificar es input de usuario.
- El payload es legible por cualquiera: sin PII ni datos clínicos, solo identificadores.
- En NestJS: guard global por `APP_GUARD` y **excepción explícita** con un decorador `@Public()`
  (`SetMetadata` + `reflector.getAllAndOverride`). Una ruta nueva nace autenticada.

```ts
// ✅ autenticado por defecto; lo público se declara, no se olvida
providers: [{ provide: APP_GUARD, useClass: AuthGuard }]

@Public()
@Post('auth/login')
login(@Body() dto: LoginDto) { /* ... */ }
```

## 4. Rotación de refresh tokens y cierre de sesión

1. Cada uso del refresh token emite uno nuevo e invalida el anterior.
2. Guardá los refresh tokens **hasheados**, agrupados por *familia* (una por login/dispositivo).
3. **Detección de reuso**: si llega un refresh ya rotado, alguien lo copió ⇒ revocá la familia
   entera y forzá login. No lo trates como error benigno.
4. Cierre de sesión = revocar la familia. **Cierre global** = revocar todas las familias del
   usuario; ofrecelo en ajustes y ejecutalo solo al cambiar contraseña, email o MFA.
5. Para que el cierre sea efectivo con JWT: access token corto + `sessionVersion` en el usuario
   que el guard compara, o lista de revocación con TTL igual a la vida del token.
6. Listá sesiones activas (dispositivo, última actividad) para que el usuario pueda cortarlas.

## 5. Contraseñas (OWASP Password Storage Cheat Sheet)

- **Argon2id** es la primera opción. Mínimo: 19 MiB de memoria, 2 iteraciones, paralelismo 1
  (`m=19456, t=2, p=1`); equivalentes: `m=47104,t=1` · `m=12288,t=3` · `m=9216,t=4` · `m=7168,t=5`.
- Sin Argon2id: **scrypt** (`N=2^17, r=8, p=1` o equivalentes). **bcrypt** solo en sistemas
  legados: work factor ≥ 10 y ojo con el límite de **72 bytes** de entrada.
- Exigencia FIPS-140: PBKDF2-HMAC-SHA256 con 600 000 iteraciones.
- Calibrá el costo en tu hardware real y revisalo periódicamente; los números son pisos.
- Migración de hashes viejos: re-hashear en el próximo login exitoso, o envolver el hash viejo
  con el nuevo algoritmo hasta entonces. Nunca dejar un MD5/SHA "porque ya estaba".
- Pepper opcional: fuera de la base (secret manager), nunca junto al hash.
- Política: longitud mínima razonable, sin reglas de composición arbitrarias, permitir pegar
  y gestores de contraseñas, chequear contra listas de contraseñas filtradas.

## 6. MFA (OWASP MFA Cheat Sheet)

- Preferí factores **resistentes a phishing**: passkeys / FIDO2 / WebAuthn. TOTP es la
  alternativa de bajo costo. **SMS no** para aplicaciones con PII o de alto valor (NIST
  SP 800-63B-4 lo marca como autenticador restringido: SIM-swap, SS7). Email como factor
  depende de la seguridad de una casilla que suele no tener MFA.
- Exigilo en el login y **re-exigilo** (step-up) en: cambio de contraseña, cambio de email,
  desactivar MFA, elevar a sesión administrativa y acciones de alto riesgo del dominio.
- Entregá **códigos de recuperación de un solo uso** al activar MFA, guardados hasheados.
- El reset de MFA es el camino de ataque preferido: exige verificación de identidad más fuerte
  que el login, queda auditado y notifica al usuario por el canal anterior.

## 7. Recuperación de cuenta sin enumeración

1. **Misma respuesta** exista o no la cuenta ("Si el correo está registrado, te enviamos…").
2. **Mismo tiempo de respuesta**: encolá el envío; no hagas trabajo extra solo si existe.
3. Mismo cuidado en login ("credenciales inválidas", sin distinguir usuario de contraseña) y
   en registro (no revelar "ese email ya existe" a un anónimo: avisá por email al titular).
4. Rate limit **por cuenta y por IP**; no bloquees la cuenta como castigo (es un DoS al usuario).
5. Tras el reset: **no** autologuear; pedir login normal. Invalidar sesiones existentes (o
   ofrecerlo). Notificar por email que la contraseña cambió.
6. Construí la URL desde configuración, nunca desde el header `Host` del request.

## 8. Tokens de propósito único (reset, verificación, invitación, acciones por link)

- Generados con CSPRNG (`crypto.randomBytes`), largos; en base se guarda **solo el hash**.
- Atados a **un propósito**, un sujeto y, si aplica, un recurso. Un token de verificación de
  email no sirve para resetear contraseña.
- **Un solo uso**: se marca consumido en la misma transacción que aplica el efecto.
- Vencimiento corto y proporcional al riesgo; al emitir uno nuevo se invalidan los anteriores.
- El link **identifica** la acción, no autoriza al que hace clic: una acción sensible abierta
  desde un email pide sesión del actor correcto (ver `authz-access-control`).
- Cuidado con prefetch de clientes de correo: el GET muestra una pantalla, el **POST** confirma.

## 9. Alta y verificación

- **Usuario**: cuenta creada en estado *no verificado* con capacidades mínimas; email y/o
  teléfono verificados con token de un solo uso antes de habilitar acciones sensibles. Cambiar
  el email exige verificar el nuevo **y** notificar al viejo.
- **Profesional** (rol con privilegios sobre datos de terceros): el rol **no se autoasigna**.
  Alta = solicitud con credenciales profesionales → revisión → aprobación registrada con quién
  y cuándo. Hasta entonces la cuenta opera como usuario común. Estados explícitos
  (`pendiente` / `aprobado` / `rechazado` / `suspendido`), modelados según `state-machines-workflows`.
- Identidad ≠ perfil: una persona, una identidad, varios roles/organizaciones (`multi-tenancy`).

## 10. Abuso y registro

- Rate limit en login, registro, reset y verificación. En NestJS: `@nestjs/throttler`
  (`ThrottlerModule.forRoot`, `ttl` en milisegundos, `@Throttle({ default: { limit, ttl } })`).
  El storage por defecto es **en memoria**: con más de una instancia necesitás un
  `ThrottlerStorage` compartido (Redis) o el límite se multiplica por instancia.
- Auditá: login ok/fallido, reset solicitado/completado, cambio de factor, revocaciones,
  reuso de refresh. Sin contraseñas ni tokens en el log (`backend-observability`).

## Anti-patrones

- Token en `localStorage` "porque es una SPA". JWT de larga vida sin revocación.
- "El email no existe" en el reset. Autologin después del reset.
- Rol profesional/admin elegible en el formulario de registro.
- Comparar tokens con `===` sobre texto plano guardado en la base.
- Desactivar MFA con solo la contraseña. SMS como único segundo factor en datos de salud.

## Checklist

- [ ] Authorization code + PKCE; sin password grant ni implicit; `redirect_uri` exacto.
- [ ] Ningún token en `localStorage`; cookies `HttpOnly`/`Secure`/`SameSite` + anti-CSRF.
- [ ] JWT: algoritmo fijo, `iss`/`aud`/`exp` validados, payload sin PII.
- [ ] Guard global + `@Public()` explícito.
- [ ] Refresh con rotación, hash en base, detección de reuso y revocación por familia.
- [ ] Cierre de sesión global efectivo (versión de sesión o lista de revocación).
- [ ] Argon2id con parámetros ≥ mínimo OWASP; plan de migración de hashes legados.
- [ ] MFA con step-up en acciones sensibles; códigos de recuperación; reset de MFA endurecido.
- [ ] Reset/login/registro sin enumeración, con tiempo uniforme y rate limit por cuenta e IP.
- [ ] Tokens de un solo uso: hasheados, por propósito, con vencimiento, consumo transaccional.
- [ ] Rol profesional solo por aprobación auditada.
- [ ] Throttler con storage compartido si hay más de una instancia.
