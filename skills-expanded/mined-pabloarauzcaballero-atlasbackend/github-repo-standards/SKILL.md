---
name: github-repo-standards
description: Estructura estándar de un repositorio de la casa en GitHub — contenido de `.github/` (plantilla de PR, issue forms, CODEOWNERS, workflows, dependabot.yml, release.yml), archivos de raíz (README, CONTRIBUTING, SECURITY, LICENSE, .gitattributes, .editorconfig), el repo `.github` de la organización para defaults compartidos, y los settings recomendados. Usar al crear un repo nuevo, al normalizar uno existente, al agregar una plantilla, o al decidir qué se comparte a nivel organización. Exigir que CODEOWNERS pida revisión es `github-branch-protection-rulesets`.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Estándar de repositorio en GitHub

Un repo de la casa se reconoce por su esqueleto: mismas plantillas, mismos dueños, mismos gates.
La protección de ramas vive en `github-branch-protection-rulesets`, la postura de seguridad en
`github-security-features` y los workflows en `github-actions-ci`. Esta skill cubre **qué archivos
existen, dónde van y cómo se configura el repo**.

> [!important] Las rutas de este documento están verificadas contra docs.github.com
> GitHub sólo reconoce los nombres y carpetas exactos. Un `CODEOWNERS` en el lugar equivocado
> no falla: simplemente no se aplica, y nadie se entera hasta que un PR se mergea sin revisión.

## 1. Árbol de referencia

```text
.github/
├── CODEOWNERS                      # o en raíz o en docs/ — ver §3
├── pull_request_template.md        # plantilla única de PR
├── PULL_REQUEST_TEMPLATE/          # (opcional) varias plantillas — carpeta en MAYÚSCULAS
│   └── hotfix.md
├── ISSUE_TEMPLATE/
│   ├── config.yml                  # chooser: enlaces externos y blank_issues_enabled
│   ├── 1-bug.yml                   # issue forms (YAML)
│   └── 2-feature.yml
├── dependabot.yml
├── release.yml                     # categorías de las release notes automáticas
└── workflows/
    ├── ci.yml
    └── security.yml
README.md
CONTRIBUTING.md
SECURITY.md
LICENSE                             # NO se puede heredar de la organización
CHANGELOG.md                        # si el repo se versiona
.gitignore
.gitattributes
.editorconfig
```

## 2. Plantillas

| Artefacto | Ruta exacta | Notas |
|---|---|---|
| Plantilla de PR | `pull_request_template.md` en raíz, `.github/` o `docs/` | El cuerpo lo define `github-pull-requests` |
| Varias plantillas de PR | `.github/PULL_REQUEST_TEMPLATE/<nombre>.md` | Carpeta en mayúsculas; se elige con el parámetro `template` en la URL |
| Issue forms | `.github/ISSUE_TEMPLATE/<nombre>.yml` | Los `.yml` se listan antes que los `.md`, alfanuméricamente |
| Chooser de issues | `.github/ISSUE_TEMPLATE/config.yml` | Un solo archivo; agrega enlaces externos y puede desactivar el issue en blanco |

- Prefijá con número para fijar el orden (`1-bug.yml`, `2-feature.yml`); con diez o más, rellená
  con cero (`01-…`). El detalle de los campos está en `github-issues-projects`.
- Las plantillas recién están disponibles **una vez mergeadas a la rama por defecto**. Probarlas
  desde una rama y concluir que "no funcionan" es el error clásico.

## 3. CODEOWNERS

- Ubicaciones válidas: `.github/`, la raíz o `docs/`. GitHub busca **en ese orden y usa la primera
  que encuentra** — tener dos es una fuente de confusión garantizada, dejá una sola.
- **Gana el último patrón que coincide**, no el primero. Ordená de lo general a lo específico.
- Sintaxis tipo gitignore, pero **sin** negación `!`, **sin** rangos `[ ]` y sin escapar `#`.
  Las rutas distinguen mayúsculas.
- Los usuarios y equipos listados necesitan acceso de escritura, o la asignación se ignora en silencio.

```text
*                       @org/plataforma
/apps/api/              @org/backend
/apps/web/              @org/frontend
/db/                    @org/datos @org/backend
/.github/workflows/     @org/plataforma
```

Para que CODEOWNERS **obligue** y no sólo sugiera, hace falta activar la revisión de code owners
en el ruleset (`github-branch-protection-rulesets`).

## 4. Dependabot y release notes

`.github/dependabot.yml` — claves de nivel superior `version: 2` y `updates:`. Por entrada:
`package-ecosystem` y `directory` (o `directories`) y `schedule.interval` son obligatorias;
`open-pull-requests-limit` (por defecto 5), `groups`, `allow`, `ignore`, `labels`, `assignees`,
`commit-message` y `cooldown` son opcionales. Agrupá para no ahogarte en PRs sueltos.

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule: { interval: "weekly" }
    open-pull-requests-limit: 5
    groups:
      dev-dependencies:
        dependency-type: "development"
```

`.github/release.yml` — configura las release notes automáticas:
`changelog.categories[]` con `title` y `labels` (ambas obligatorias) y `changelog.exclude`
con `labels` y/o `authors`. Las categorías se alimentan de las labels de los PRs, así que la
taxonomía de labels y el prefijo del título tienen que ser coherentes (`github-releases-versioning`).

## 5. Defaults de la organización

El repo especial `.github` de la organización aporta archivos por defecto a todos los repos que no
tengan el suyo. Se puede heredar: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`,
`SUPPORT.md` (en raíz, `.github/` o `docs/`), `FUNDING.yml` (sólo en `.github/`), las plantillas de
issue y PR con su `config.yml`, y los formularios de discusión en `.github/DISCUSSION_TEMPLATE`.

**El `LICENSE` no se hereda**: tiene que estar en cada repo, porque viaja con el clon o el paquete.

Regla de la casa: lo transversal (código de conducta, política de seguridad, cómo contribuir,
plantilla base de issues) vive en el repo `.github` de la organización; cada repo sólo sobrescribe
lo que de verdad es distinto.

## 6. Settings del repo

| Setting | Valor de la casa | Por qué |
|---|---|---|
| Automatically delete head branches | Activado | Settings → General → Pull Requests. Evita el cementerio de ramas; las reglas de protección pueden impedirlo |
| Métodos de merge | Sólo el que usa el repo | Ver la tabla de `github-pull-requests`; habilitar los tres invita a mezclar historias |
| Wiki | Desactivado | La documentación vive versionada con el código (`technical-docs-and-adr`) |
| Discussions | Sólo si hay quien las modere | Un foro abandonado es peor que no tenerlo |
| Topics | Siempre | Es cómo se encuentra el repo entre varios repos hermanos |
| Visibilidad | Privado salvo decisión explícita | Los repos con datos de salud no se vuelven públicos "para probar algo" |

## 7. Archivos de raíz que importan

- **README**: qué es, cómo se levanta local, comandos reales, dónde está el resto. Si sus comandos
  no funcionan copiados y pegados, está roto.
- **CONTRIBUTING**: flujo de ramas, convención de commits, cómo correr los tests, cómo se revisa.
- **SECURITY.md**: canal privado de reporte de vulnerabilidades (`github-security-features`).
- **`.gitattributes`**: normalización de saltos de línea y marcado de archivos generados como
  `linguist-generated` para sacarlos del diff. Crítico con Windows y Linux mezclados.
- **`.editorconfig`**: indentación y fin de archivo, para que el formateador no pelee con el editor.

## Anti-patrones

- `CODEOWNERS` en dos ubicaciones, o con patrones ordenados de específico a general.
- Plantillas creadas en una rama y nunca mergeadas a la default: no aparecen.
- `LICENSE` delegado a la organización: no se hereda.
- README que documenta comandos de hace seis meses (`anti-hallucination-guard`).
- Repo nuevo sin protección de rama "porque todavía es chico": nunca se agrega después.
- Habilitar wiki, discussions, projects y páginas "por las dudas", sin dueño.

## Checklist — repo nuevo

- [ ] `README`, `CONTRIBUTING`, `SECURITY.md`, `LICENSE`, `.gitignore`, `.gitattributes`, `.editorconfig`.
- [ ] `.github/pull_request_template.md` con la plantilla de la casa.
- [ ] `.github/ISSUE_TEMPLATE/` con al menos bug y feature, más `config.yml`.
- [ ] `CODEOWNERS` en **una** ubicación, de general a específico, con equipos que tengan escritura.
- [ ] `.github/dependabot.yml` con las ecologías reales del repo y grupos.
- [ ] `.github/release.yml` alineado con la taxonomía de labels.
- [ ] Workflow de CI verde y registrado como check requerido.
- [ ] Ruleset sobre la rama de integración; borrado automático de rama activado.
- [ ] Métodos de merge reducidos al que usa el repo; topics cargados.
- [ ] Secret scanning con push protection y Dependabot alerts activados.
- [ ] Verificado desde la rama por defecto que las plantillas aparecen al abrir un PR/issue.
