---
name: github-multirepo-coordination
description: Coordinación de un cambio que cruza varios repos hermanos (API, web, mobile, modelo) — orden de merge según dependencia de contrato, PRs vinculados entre repos, la misma rama en todos, reusable workflows con `workflow_call`, disparos cruzados con `repository_dispatch`, ventana de compatibilidad hacia atrás y verificación del contrato OpenAPI en CI. Usar al abrir un carril que toca más de un repo, al ordenar los merges, o al romper un contrato que otros consumen.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Coordinación entre repos hermanos

Un carril rara vez vive en un solo repo: toca el modelo, la API, la web y a veces la app móvil.
Git puro (ramas, commits, rebase) está en `git-workflow-multirepo`; la forma de cada PR, en
`github-pull-requests`. Esta skill cubre **el orden, el vínculo y la automatización entre repos**.

> [!important] El riesgo no es el código: es la ventana
> Entre que mergeás el productor del contrato y que despliegan los consumidores, el sistema corre
> con **dos versiones conviviendo**. Todo lo de acá existe para que esa ventana no rompa nada.

## 1. Identificar el grafo de dependencia

Antes de escribir una línea, escribí en el carril (`lane-authoring`) qué repos toca y quién
depende de quién. La dependencia es **de contrato**, no de importancia:

```text
modelo ──▶ API ──▶ web
                └─▶ mobile
API (OpenAPI) ──▶ cualquier consumidor generado
```

- **Productor**: el repo que publica el contrato (esquema, endpoint, evento, tipo generado).
- **Consumidor**: el que lo usa.
- Si dos repos se necesitan mutuamente para compilar, el contrato está mal cortado: partilo en
  una pieza que uno publica y el otro consume.

## 2. Orden de merge

1. **Primero el productor, después los consumidores.** El modelo antes que la API; la API antes
   que la web y la app.
2. El productor **sólo puede mergear cambios compatibles hacia atrás**. Si no lo son, va en dos
   pasos (§4).
3. Los consumidores no se mergean hasta que lo del productor está desplegado en el entorno donde
   corren sus tests de integración. Verde local contra una API vieja no prueba nada.
4. El despliegue sigue el mismo orden que el merge (`release-and-rollback`).
5. **Nunca al revés**: mergear la web que consume un endpoint que todavía no existe rompe la
   rama de integración de la web.

❌ Mergeo los tres PRs juntos "porque el carril está listo".
✅ Mergeo modelo → despliego → mergeo API → despliego → mergeo web y mobile.

## 3. Vincular los PRs

- **Una rama con el mismo nombre en todos los repos afectados** (`feat/agenda-bloqueos`). Es lo
  que permite encontrar los hermanos sin un tablero.
- En la descripción de cada PR, una sección fija con los enlaces cruzados y el orden:

```markdown
## Repos de este carril
Orden de merge: 1) modelo · 2) api · 3) web
- modelo: org/salud-model#84   ← este PR
- api:    org/salud-api#312
- web:    org/salud-web#198
Bloqueado por: org/salud-model#84
```

- Las palabras clave de cierre (`Closes #123`) **sólo funcionan dentro del mismo repo**; para un
  issue de otro repo usá la referencia completa `org/repo#123` y cerralo a mano.
- Un issue paraguas en el repo del carril, con los tres PRs enlazados, sirve de tablero
  (`github-issues-projects`).

## 4. Romper un contrato sin romper a nadie (expand / contract)

Nunca se borra y se agrega en el mismo merge. Tres pasos, cada uno desplegable solo:

| Paso | Productor | Consumidores |
|---|---|---|
| **Expand** | Agrega lo nuevo, mantiene lo viejo funcionando | Sin cambios; siguen andando |
| **Migrate** | — | Se mueven a lo nuevo, se mergean y despliegan |
| **Contract** | Borra lo viejo, sólo cuando nadie lo usa | — |

- Entre expand y contract tiene que pasar al menos un ciclo de despliegue completo de **todos**
  los consumidores, incluida la app móvil — que no se actualiza cuando vos querés, sino cuando
  el usuario actualiza. Para móvil, la ventana se mide en versiones publicadas, no en días.
- Marcá lo viejo como `deprecated` en el spec (`api-openapi-docs`) antes de borrarlo.
- El mismo patrón aplica al esquema de datos (`model-driven-schema`) y a los eventos
  (`async-messaging-events`).

## 5. Workflows compartidos

Un repo central (por ejemplo el `.github` de la organización o un `shared-workflows`) publica los
workflows reutilizables; los demás los llaman. Un solo lugar donde arreglar el pipeline.

El workflow reutilizable declara el disparador y sus entradas y salidas:

```yaml
# org/shared-workflows/.github/workflows/node-ci.yml
on:
  workflow_call:
    inputs:
      node-version: { type: string, required: true }
    outputs:
      coverage:
        value: ${{ jobs.test.outputs.coverage }}
```

El repo consumidor lo invoca desde `jobs.<id>.uses`, con la forma
`{owner}/{repo}/.github/workflows/{archivo}@{ref}`:

```yaml
jobs:
  ci:
    uses: org/shared-workflows/.github/workflows/node-ci.yml@v1
    with:
      node-version: "22"
    secrets: inherit        # o pasadas una por una
```

- **Fijá el `@ref`**: una etiqueta de versión o un SHA, nunca una rama móvil como `main`. Si no,
  un cambio en el repo central rompe el CI de cinco repos a la vez.
- Los secretos se pasan explícitos o con `secrets: inherit`. Heredar todo es cómodo y amplio;
  preferí explícito cuando el workflow es de un tercero (`github-security-features`).
- Las salidas se consumen con `needs.<job>.outputs.<nombre>`.

## 6. Disparos cruzados

Cuando un repo tiene que despertar a otro (regenerar clientes tras publicar un spec, redesplegar
un consumidor):

- `repository_dispatch` — se dispara con `POST /repos/{owner}/{repo}/dispatches`, con
  `event_type` (obligatorio, hasta 100 caracteres) y `client_payload` opcional (máximo 10
  propiedades de primer nivel y 65 535 caracteres en total). El workflow **corre siempre sobre la
  rama por defecto** del repo destino, no sobre la rama del que dispara: no lo uses para validar
  una rama.
- `workflow_dispatch` — para el disparo manual, con hasta 25 entradas de primer nivel.
- El payload se lee como `github.event.client_payload.<campo>`.
- Requiere un token con permiso de escritura sobre el repo destino; usá una GitHub App o un token
  fine-grained acotado, no un PAT clásico personal (`github-security-features`).

## 7. Verificar el contrato en CI

- El productor publica el spec OpenAPI como artefacto en cada build.
- El consumidor corre un check que compara el spec contra el que tiene fijado y **falla si cambió
  de forma incompatible**. Ese check es el que protege la ventana del §4.
- Detección de breaking changes y linting del spec: `api-openapi-docs`.
- Los tests de contrato propiamente dichos viven en `integrity-testing`.

## Anti-patrones

- Mergear los PRs hermanos "todos juntos al final" y descubrir el orden en producción.
- Apuntar un reusable workflow a `@main`.
- Borrar el campo viejo en el mismo PR que agrega el nuevo.
- Asumir que la app móvil se actualiza al mismo tiempo que la web.
- Usar `repository_dispatch` para probar una rama (corre sobre la default).
- Un PR que toca tres repos porque el workspace está montado como uno solo: se pierde la revisión
  por dueño y la reversión por repo.
- Ramas con nombres distintos en cada repo: nadie encuentra a los hermanos.

## Checklist

- [ ] Los repos afectados y el grafo de dependencia están escritos en el carril.
- [ ] Misma rama en todos los repos; PRs enlazados con el orden de merge explícito.
- [ ] El cambio de contrato es compatible hacia atrás, o está cortado en expand/migrate/contract.
- [ ] Lo viejo quedó marcado como deprecado antes de programar su borrado.
- [ ] Los consumidores se mergean recién con el productor ya desplegado.
- [ ] Los reusable workflows están fijados a una versión o SHA, con secretos acotados.
- [ ] El check de contrato OpenAPI corre en los consumidores y falla ante incompatibilidad.
- [ ] Considerada la ventana de la app móvil en versiones publicadas.
- [ ] Orden de despliegue y plan de rollback acordados antes del primer merge.
