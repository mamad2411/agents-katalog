---
name: environment-secrets-config
description: Gate de configuración y secretos según 12-factor — config por entorno en variables, validación de env al arrancar (fallar si falta), sin secretos en el repo, el bundle del front ni logs, jerarquía de `.env`, `.env.example` documentado, rotación y dónde viven los secretos en CI y Coolify. Usar al agregar una variable de entorno, al leer config en código, al preparar el deploy de un servicio, al revisar un `.env` que se coló en git, o antes de dar por lista la config de un entorno.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Configuración y secretos

La config cambia entre entornos; el código, no. Todo lo que difiere entre dev, staging y
producción —URLs, credenciales, flags— vive en el entorno, no en el fuente (12-factor, factor
III). Un secreto en el repo es un secreto comprometido. Verificado contra 12factor.net.

## 1. Config vs código

- **Config** = todo lo que varía por entorno (host de base, credenciales, claves de terceros,
  nivel de log, feature flags). Va en variables de entorno.
- **Código** = igual en todos los entornos. Si tenés un `if (env === 'production')` decidiendo
  lógica de negocio, casi siempre es una variable de config disfrazada.
- Prueba ácida: **¿podrías hacer público el repo ahora mismo sin filtrar ninguna credencial?**
  Si la respuesta es no, hay secretos donde no deberían estar.

## 2. Validar el entorno al arrancar — fallar temprano

Nunca leas `process.env.X` disperso por el código con un default silencioso. Validá **todo** el
entorno al bootstrap y **abortá** si algo falta o no tipa. Un servicio que arranca sin su
config y falla en la primera request es peor que uno que no arranca.

```typescript
// NestJS: ConfigModule con schema; la app no levanta si el env es inválido
ConfigModule.forRoot({
  validate: (raw) => envSchema.parse(raw),   // zod: lanza y detiene el arranque
  isGlobal: true,
});
```

- Sin defaults para secretos (una `JWT_SECRET` con default es una puerta abierta).
- Tipá y coaccioná: los puertos son números, los flags son booleanos, las URLs se parsean.
- El error de validación dice **qué** variable falta, nunca **su valor**.

## 3. Prohibiciones

- ❌ Secretos commiteados (`.env`, claves, `*.pem`, tokens). Van en `.gitignore` **antes** del
  primer commit. Si ya se coló uno: rotarlo (ya está comprometido) y limpiar la historia.
- ❌ Secretos en el **bundle del front**. Todo lo que llega al navegador es público: una API key
  "de frontend" es una API key filtrada. El front solo lleva config pública (URL de la API,
  claves publicables por diseño). Ver `frontend-security`.
- ❌ Secretos en **logs, trazas, mensajes de error o URLs** (query string queda en access logs e
  historial). Ver `data-privacy-sensitive` y `backend-observability`.
- ❌ El mismo secreto en varios entornos: dev, staging y prod tienen credenciales distintas.

## 4. Jerarquía de `.env` y el ejemplo versionado

- Versioná **`.env.example`** con **todas** las claves, valores de ejemplo NO sensibles y un
  comentario por variable (para qué es, formato, si es obligatoria). Es el contrato de config.
- `.env` (real, con secretos) va en `.gitignore`.
- Precedencia típica de más específico a más general: variable ya exportada en el shell/CI >
  `.env.local` (overrides personales, ignorado) > `.env`. No dependas de un orden mágico:
  documentá el que uses.
- Un `.env.example` desactualizado rompe a quien clona. Cada variable nueva entra al ejemplo en
  el mismo commit que la introduce.

## 5. Dónde viven los secretos por entorno

| Entorno | Dónde | Regla |
|---|---|---|
| Local | `.env` en la máquina | Nunca sale del disco; datos de prueba, no de producción |
| CI | Secrets/variables del proveedor | `secrets` para lo sensible, `vars` para lo público; permiso mínimo (ver `github-actions-ci`) |
| Producción/staging | Gestor de secretos del deploy (Coolify) | Marcados como secreto; distintos por entorno (ver `coolify-operations`) |

- Preferí **OIDC/identidades de corta duración** a secretos de larga vida cuando la plataforma lo
  permita (ver `github-actions-ci`).
- Distinguí **build-time vs runtime**: un secreto de runtime que se inyecta en build queda
  horneado en la imagen. Ver `dockerfile-production`.

## 6. Rotación

- Todo secreto tiene dueño y se puede rotar sin downtime (soportá dos válidos durante la
  ventana de rotación).
- Rotá **ante sospecha o filtración, ya**, no "cuando haya tiempo".
- Un secreto que apareció en git, en un log o en un chat **está comprometido**: rotarlo, no
  borrarlo y hacer de cuenta que no pasó.

## Evidencia / DoD

Para declarar la configuración de un servicio o entorno "lista", pegá:
- Salida de un grep de secretos sobre el árbol y la historia reciente, **vacía**:
  `git grep -nEi '(secret|password|api[_-]?key|token|BEGIN [A-Z ]*PRIVATE KEY)'` y, para lo ya
  commiteado, un escaneo con una herramienta de secret scanning (ver `github-security-features`).
- Prueba de que **falta una variable obligatoria hace fallar el arranque**: la salida del intento
  con el env incompleto mostrando el error de validación (sin exponer valores).
- `.env.example` con todas las claves que el código lee (diff clave-a-clave contra las variables
  referenciadas).
- Confirmación de que el bundle del front no contiene ningún secreto (grep del build).

## Checklist

- [ ] Config por entorno en variables; nada de config en el código.
- [ ] Validación de env al arrancar que aborta ante faltante/ inválido, sin exponer valores.
- [ ] `.env` en `.gitignore`; `.env.example` versionado y completo, una línea por variable.
- [ ] Cero secretos en repo, historia, bundle del front, logs, trazas o URLs.
- [ ] Secretos distintos por entorno, en el gestor de cada uno, con permiso mínimo.
- [ ] Cada secreto tiene dueño y plan de rotación; los filtrados se rotan de inmediato.
