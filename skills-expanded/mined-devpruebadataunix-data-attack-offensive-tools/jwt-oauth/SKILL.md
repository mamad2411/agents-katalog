---
name: jwt-oauth
description: Ataques a JWT y flujos OAuth 2.0 / OIDC — alg=none, confusión RS256→HS256, claves de firma débiles, redirect_uri abierto, robo de tokens y abuso de scopes. Úsala cuando el activo en scope use JWT como sesión/autorización o SSO basado en OAuth/OIDC.
---

# JWT y OAuth/OIDC ofensivos

Los tokens son omnipresentes en APIs y SSO modernos; su seguridad depende de detalles de
implementación que fallan a menudo. Validar la firma y el flujo de autorización es el núcleo.

## Cuándo usarla
Cuando veas `Authorization: Bearer eyJ…` (JWT), endpoints `/.well-known/openid-configuration`,
`/oauth/authorize`, `/token`, o parámetros `redirect_uri`, `state`, `code`, `id_token`.

## Técnicas (con MITRE)
- **alg=none** (T1550.001): cambia el header a `{"alg":"none"}` y elimina la firma.
- **Confusión RS256→HS256**: firma con la clave pública como secreto HMAC si el server no fija alg.
- **Clave de firma débil**: crackea el HMAC offline (diccionario) y forja tokens.
- **Inyección por cabecera (`jwk`/`jku`/`kid`/`x5u`)**: incrusta tu clave pública en `jwk`, apunta `jku`
  a un JWKS que tú alojas, o abusa de `kid` (path traversal a un fichero conocido, o SQLi) para que el
  server verifique con una clave que TÚ controlas y aceptar tokens forjados.
- **Claims sin validar**: manipula `sub`, `role`, `scope`, `exp`; confusión de audiencia (`aud`).
- **OAuth**: `redirect_uri` abierto/parcial → robo de `code`/`token`; falta de `state` → CSRF;
  `response_type=token` (implicit) filtra el token en el fragmento; PKCE ausente.

## Herramientas (suite del repo)
- Manipulación/forja/replay del token: **JWT Editor** (extensión de Burp, automatiza `jwk`/`jku`/alg
  confusion), **`jwt_tool`** (batería de comprobaciones + explotación), o proxy manual (lo cubre `web-exploit`).
- Crackeo del secreto HMAC: `hashcat` modo 16500 (JWT) — tier **sensitive** (pide aprobación).
- Descubrimiento del flujo OAuth: `recon-suite` (`httpx`/`katana`) sobre los endpoints `.well-known`.

## Evidencia y alcance
- Prueba mínima: un token forjado/manipulado que el servidor **acepta** (respuesta autenticada),
  o el `code`/`token` capturado vía `redirect_uri` — guárdalo como `evidence`.
- Mapea a `contracts/finding.schema.json` (`cvss_vector`, `evidence`, `reproduction`).
- **Sin fuente no se explota**: un `alg=none` "posible" es candidato hasta que el server lo acepte.
