---
name: hermes-skills-tap-workflow
description: "Use when authoring, publishing, or propagating Hermes or Claude Code skills through a GitHub tap repo - editing a skill at its canonical source, installing it into profiles, keeping installed copies from drifting, and avoiding known install pitfalls."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, skills, tap, github, publish, propagate, profiles]
    related_skills: [hermes-agent-skill-authoring]
---

# Hermes Skills Tap Workflow

Publicar una skill de Hermes como GitHub tap y propagarla a perfiles locales,
de forma que el repo sea la fuente canónica y las copias instaladas por perfil
sean las que se cargan.

**Caso de uso:** crear un monorepo de skills reutilizables y agregarlo como tap
a uno o varios perfiles.

## Estructura del repo tap

Layout que el proveedor de GitHub (GitHubSource, `tools/skills_hub_github.py`)
espera:

```
repo/
├── README.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        └── templates/...        # references/ y scripts/ son opcionales
```

- Cada skill es un subdirectorio de `skills/` con su `SKILL.md`.
- El path default del tap es `skills/` (el `add` lo usa por defecto).
- Nombres de carpetas que arrancan con `.` o `_` se saltan (no son skills).

## Crear el repo y conectarlo

```bash
# 1. Crear el repo (público o privado; skills son texto, público sirve para compartir)
gh repo create <owner>/<repo> --public --description "..."

# 2. Clonar, armar skills/<name>/SKILL.md (+ plantillas), README
cd ~ && gh repo clone <owner>/<repo>
mkdir -p <repo>/skills && cp -r <src-skill> <repo>/skills/
# author README con qué skills hay y cómo editar/propagar

# 3. Commit + push (paths EXPLÍCITOS, nunca git add -A: los guard de git lo bloquean)
cd <repo> && git add README.md skills/<name>/ && git commit -m "feat: add <name> skill tap" && git push -u origin main

# 4. Agregar el tap (perfil actual)
hermes skills tap add <owner>/<repo>

# 5. Por cada perfil adicional
hermes --profile <nombre> skills tap add <owner>/<repo>
```

## Verificar que el tap resuelve la skill

```bash
# El search NO cubre taps (busca el catálogo oficial).
# Usar inspect del identificador:
hermes skills inspect <owner>/<repo>/skills/<skill-name>
# debe mostrar Name/Description/Repo legibles (Trust: community).
```

`GitHubSource._list_skills_in_repo` usa `GET /repos/{repo}/contents/{path}` y
`inspect` por directorio — si `inspect` devuelve la skill, el layout es correcto.

## Propagar un cambio de skill (editar → push → re-instalar)

El tap es la FUENTE canónica. Las copias instaladas por perfil son las que se
cargan. Un cambio al repo NO llega solo a los perfiles.

1. Editar `skills/<name>/` en el repo.
2. Commit + push (paths explícitos).
3. Re-propagación a cada perfil:
   - `hermes skills install <owner>/<repo>/skills/<name>` (default), o
   - propagación manual: copiar la carpeta de la skill sobre el `skills/` del
     perfil, preservando `templates/`.

### La copia es el bug; el symlink es el fix

Para un tap PROPIO que se edita seguido, la copia instalada es deuda: cada push
exige re-instalar en cada perfil, y si no se hace, la copia drifta en silencio —
el mismo patrón "doc que drifta respecto al estado real" que el playbook enseña
a cazar. Un symlink elimina el paso: el cambio en el repo ES el cambio en el
perfil.

```bash
for s in /ruta/al/tap/skills/*/; do
  n=$(basename "$s")
  ln -sfn "$s" ~/.claude/skills/$n     # Claude Code
  ln -sfn "$s" ~/.hermes/skills/$n     # Hermes (perfil default)
done
```

Ambos loaders resuelven symlinks (verificado 2026-09-11: Hermes ya tenía 28
skills enganchadas así, y Claude Code levantó las descriptions editadas en vivo,
sin re-instalar). Reservar el install por copia para consumidores externos del
tap, que sí quieren una versión congelada.

**Evidencia de que la copia falla sola:** el día que se publicó este tap, 2 de 5
skills (incluida la insignia `empirical-project-playbook`) nunca llegaron al
perfil default — el repo decía que estaban publicadas y el perfil no las tenía.
Nadie lo notó porque nada falla: la skill simplemente no se carga nunca.
Presence ≠ utility, aplicado a la propagación.

## Pitfalls

- **`git add -A` está bloqueado** por los guards: usar paths explícitos.
- **`hermes skills search "x"` no cubre taps** — es del catálogo oficial. No
  usarlo para verificar un tap.
- **Los loops con `for p in ...` en un solo comando terminal pueden caer en el
  blocklist** (payload muy largo). Preferir varios comandos cortos o un solo
  path por llamada.
- **El sync de bundled skills de `hermes update` re-sincroniza los perfiles** —
  si una skill del default va a un tap, asegurarse de que el tap esté agregado
  en cada perfil que la use, o el update no la va a propagar.
- **Público vs privado**: skills son texto. Público facilita compartir; privado
  si es conocimiento propietario. Decidir explícitamente.
- **`hermes skills install` puede fallar con "Could not fetch from any source" aunque
  `inspect` resuelva y la skill esté commiteada.** (Visto 2026-09-11 con
  `data-medallion-architecture`; las dos anteriores instalaron bien.) El install resuelve
  vía skills.sh externo y es frágil a eso, no al contenido del repo. Workaround: propagación
  MANUAL — `mkdir -p ~/.hermes/skills/<name>` (y en cada `~/.hermes/profiles/<p>/skills/`),
  `cp -r <repo>/skills/<name>/SKILL.md <repo>/skills/<name>/templates …/`, preservando
  templates. Verificar con `ls` en el perfil. No reintentar el install en loop contra el
  mismo error de resolución.
