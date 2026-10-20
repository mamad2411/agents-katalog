---
name: harness-upgrade
description: Actualiza el harness coe-harness de este repo (skills, hooks, settings, scripts de checks, workflows) a la última versión publicada, sin pisar nada que hayas editado tú. Actívate cuando el usuario pida actualizar, upgradear o traer la última versión del harness (ej. "actualiza el harness", "hay una versión nueva del harness", "upgradea el harness").
---

# /harness-upgrade

Una sola instrucción del usuario dispara todo el flujo: buscar la versión nueva,
aplicarla, borrar lo que ya no se usa y mergear lo que corresponda de los `.new`.
No hace falta que el usuario pida cada paso por separado.

## Qué hacer

1. **Estado actual.** Corre:

   ```
   npx -y github:soutec-dev/coe-harness#v1 status
   ```

   Si ya está en la última versión y no hay archivos obsoletos ni `.new`
   pendientes, avisa eso en una línea y termina — no hay nada más que hacer.

2. **Diagnóstico en seco**, siempre antes de tocar nada:

   ```
   npx -y github:soutec-dev/coe-harness#v1 upgrade --dry-run --prune
   ```

   El plan distingue dos grupos de obsoletos: los que se pueden borrar sin
   preguntar (contenido del harness, intacto desde que lo escribió) y los que tú
   editaste (exigen revisión, nunca se borran solos). Usa ese plan para armar el
   resumen del paso 3 — no le pidas OK al usuario todavía.

3. Aplica directo, sin esperar confirmación intermedia:

   ```
   npx -y github:soutec-dev/coe-harness#v1 upgrade --prune
   ```

   Esto actualiza los archivos que no editaste, deja `.new` al lado de los que sí
   editaste y **borra sin preguntar** los obsoletos que nunca tocaste. Los
   obsoletos que sí editaste **no se borran solos**: quedan reportados para que
   los revises en el paso 4. El mismo `upgrade` reaplica la branch protection de
   `main` en GitHub si `gh` está autenticado.

4. **Si el upgrade dejó archivos `.new`**, es porque el harness cambió una
   sección que tú también habías editado. Revisa cada uno:

   ```
   git diff --no-index CLAUDE.md CLAUDE.md.new
   ```

   Mergea por hunk, nunca el archivo entero:
   - Hunks en secciones propias del harness (reglas de Git, "Secretos y datos
     sensibles", Language, Behavior expectations, y equivalentes en otros archivos
     gestionados) → toma la versión del `.new`.
   - Hunks en secciones que el usuario llenó (Contexto, Reglas técnicas
     críticas, contenido específico del proyecto) → conserva el original, **sin
     tocarlo**.
   - Si un hunk es ambiguo, conserva el original y avísalo en el reporte final
     en vez de decidir por tu cuenta.

   Borra el `.new` después de mergear. Nunca copies un `.new` entero encima del
   original sin pasar por esta revisión hunk por hunk.

5. **Reporte final.** Avísale al usuario, en un resumen corto:
   - versión anterior → versión nueva.
   - qué se borró sin preguntar (obsoletos sin editar).
   - qué obsoletos editados quedaron pendientes de revisión (con la ruta).
   - qué `.new` se mergearon y qué se preservó de lo suyo en cada uno.
   - cualquier archivo que se saltó por stack (ver sección de abajo).
   - si la branch protection de `main` se reaplicó o quedó pendiente (y por qué).
   - si el upgrade sumó o cambió hooks en `.claude/settings.json` (por ejemplo
     `reglas-pr`): que **reinicie Claude Code** para que los cargue — los hooks
     se leen al iniciar la sesión, no en caliente.

   Si no hubo nada relevante que avisar más allá de "actualizado a la última
   versión", con esa línea alcanza.

## Fijar la versión

`#v1` es el tag móvil de la serie: recibe parches y minors sin que nadie haga
nada, y nunca un breaking. Es código que se ejecuta en la máquina al actualizar,
así que un proyecto que exija fijar versiones (auditoría, entornos regulados)
usa `#vX.Y.Z` en los tres comandos de arriba y lo sube a mano cuando decida; el
historial de versiones está en el CHANGELOG del harness.

## Único punto donde SÍ hay que parar

- Un obsoleto que el usuario editó no se borra sin que él lo apruebe. Repórtalo
  en el paso 5 y pregúntale si quiere que lo borres.
- Un hunk ambiguo de un `.new` no se resuelve solo: se deja como está y se
  reporta.

Fuera de esos casos, el flujo completo corre sin pedir OK intermedio — para
eso es "una sola instrucción".

## Tag-release fuera de Node

El harness solo distribuye `scripts/tag-release.mjs` y
`.github/workflows/tag-release.yml` en repos donde detecta Node (`package.json`).
Si el `init`/`upgrade` reporta *"No se instalaron por stack"* para esos dos
archivos, es tu trabajo escribirlos a mano para el stack real del proyecto — no
hay variantes empaquetadas por lenguaje: el contrato es siempre el mismo y tú lo
adaptas mejor que un template genérico.

1. **Fuente de versión**: lee el SemVer del archivo que ese stack usa para
   versionar (`pyproject.toml`/`setup.cfg` en Python, `Cargo.toml` en Rust, el
   `.csproj` en .NET, etc.). Si no hay una fuente de versión obvia, para y
   pregunta — no inventes un esquema.
2. **Tags**: crea el tag anotado e inmutable `vX.Y.Z` (falla si no es SemVer
   válido) y mueve a la fuerza el tag móvil de la major, `vX`, al mismo commit.
3. **Idempotencia**: si `vX.Y.Z` ya existe, no falla ni duplica — solo lo
   reporta y sale en 0. El tag móvil sí se reasigna siempre.
4. **Disparo**: workflow de GitHub Actions en `pull_request` `closed` con
   `base: main`, condicionado a `github.event.pull_request.merged == true`,
   usando el runtime del stack detectado (no `actions/setup-node` si el
   proyecto no es Node). Es el único workflow extra permitido además de los que
   instala el harness, porque reemplaza a uno de ellos.
5. **Nunca crea el GitHub Release**: eso lo sigue haciendo el coordinador a
   mano.

Usa `scripts/tag-release.mjs` y `.github/workflows/tag-release.yml` (el ejemplo
Node del propio harness) como referencia del contrato, no como plantilla a
copiar literal.

Si el `upgrade` marca esos archivos como `obsoleto` (porque el stack del
proyecto cambió), reemplázalos por la variante de tu stack en el mismo
momento — no dejes el script Node muerto en el repo.

## Qué NO hacer

- No corras `upgrade --force`. Pisa lo que el usuario escribió.
- No borres un obsoleto editado sin su OK explícito.
- No edites `.claude/harness.json` a mano. Es el lockfile: lo gestiona el CLI.
- No toques `.datos-autorizados` ni agregues `coe:no-secreto` como parte del
  upgrade: no son archivos del harness, son decisiones del usuario.
