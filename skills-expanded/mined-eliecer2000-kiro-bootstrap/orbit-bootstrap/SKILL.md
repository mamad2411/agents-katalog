---
name: orbit-bootstrap
description: Orbit bootstrap process, artifact resync, project profile resolution and workspace initialization. Use when bootstrapping a new project, resyncing artifacts or resolving project profiles.
---

# Orbit Bootstrap

Skill para el proceso de bootstrap interactivo de Orbit, resincronización de artefactos, resolución de perfiles de proyecto, gestión de conflictos, políticas de sesión y flujo completo de inicialización de workspaces.

## Principios fundamentales

- Orbit es el agente principal de bootstrap y resincronización del framework.
- El bootstrap ejecuta el pipeline real (`install.sh`) antes de crear código o scaffolding.
- El perfil de proyecto se resuelve internamente a partir de preguntas de negocio y stack, nunca pidiendo el ID crudo al usuario.
- Ningún artefacto se copia manualmente. Todo pasa por el pipeline del framework.
- El scaffolding de la aplicación comienza solo después de que el bootstrap haya terminado y los artefactos del perfil estén presentes.

## Flujo de bootstrap

```
1. Detectar contexto (HOME vs proyecto existente)
2. Preguntar si desea preparar el entorno
3. Si acepta → Resolver perfil de proyecto (wizard)
4. Ejecutar pipeline: install.sh --resync-project
   4a. Session Gates
   4b. Detect Or Select Profile
   4c. Validate Environment (+ auto-install de herramientas de sistema)
   4d. Load Orbit Artifacts
   4e. Install Project Tooling (linters, formatters, test runners)
   4f. Write Project State
5. Verificar artefactos generados
6. Actualizar .orbit-project.json
7. Listo para scaffolding
```

## Instalación de herramientas

El pipeline distingue dos niveles de herramientas:

### Herramientas de sistema (paso 4c - Validate Environment)

Validadas y auto-instaladas si faltan (controlado por `ORBIT_AUTO_INSTALL_TOOLS`, default `yes`):

| Herramienta | Método de instalación |
|---|---|
| `git` | brew / apt / xcode-select |
| `node` / `npm` | brew / apt / nvm |
| `python3` | brew / apt |
| `aws` | brew / awscli installer |
| `terraform` | brew / apt |
| `pnpm` | npm / corepack |
| `yarn` | corepack / npm |

Cada perfil define sus validaciones requeridas. Todos los perfiles validan `git` como dependencia base.

### Herramientas de proyecto (paso 4e - Install Project Tooling)

Instaladas automáticamente como devDependencies según el campo `tooling` del perfil:

| Runtime | Package Manager | Herramientas típicas |
|---|---|---|
| TypeScript/JavaScript | npm / pnpm / yarn / bun | eslint, prettier, vitest, typescript |
| Python | uv / poetry / pip3 | ruff, black, pytest, mypy |
| none (Terraform) | — | Solo herramientas de sistema |

El package manager se detecta automáticamente por lockfile (`pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`). Si no hay lockfile, usa `npm` por defecto.

Si no existe `package.json` (Node.js) o `pyproject.toml` (Python), se inicializa automáticamente antes de instalar.

## Comando de bootstrap

```bash
ORBIT_BOOTSTRAP_DECISION=yes \
ORBIT_HOME_DECISION=no \
ORBIT_PROJECT_PROFILE_ID=<profile-id> \
ORBIT_REMOTE_SKILL_DECISION=no \
~/.kiro/orbit/install.sh --resync-project "<ruta-objetivo>"
```

### Variables de entorno del pipeline

| Variable | Valores | Descripción |
|---|---|---|
| `ORBIT_BOOTSTRAP_DECISION` | `yes` / `no` | Si el usuario acepta preparar el entorno |
| `ORBIT_HOME_DECISION` | `yes` / `no` | Si se crea carpeta de proyecto desde HOME |
| `ORBIT_PROJECT_PROFILE_ID` | ID del perfil | Perfil resuelto por el wizard |
| `ORBIT_REMOTE_SKILL_DECISION` | `yes` / `no` | Si se instalan skills remotas recomendadas |

## Resolución de perfil de proyecto

El perfil se resuelve con un wizard basado en 4 dimensiones:

1. **Workload**: ¿Qué tipo de aplicación? (API backend, full-stack, infraestructura, shared library)
2. **Runtime**: ¿Qué lenguaje? (TypeScript, JavaScript, Python)
3. **Provisioner**: ¿Cómo se provisiona la infra? (CDK, Terraform, Amplify)
4. **Framework**: ¿Qué framework frontend? (React, Vue, Nuxt — solo para full-stack)

### Perfiles disponibles

| Perfil ID | Workload | Runtime | Provisioner |
|---|---|---|---|
| `aws-backend-api-typescript` | API Backend | TypeScript | CDK |
| `aws-backend-api-python` | API Backend | Python | CDK |
| `aws-backend-api-javascript` | API Backend | JavaScript | CDK |
| `aws-backend-lambda-typescript` | Lambda | TypeScript | CDK |
| `aws-backend-lambda-python` | Lambda | Python | CDK |
| `aws-backend-lambda-javascript` | Lambda | JavaScript | CDK |
| `aws-infra-cdk-typescript` | Infraestructura | TypeScript | CDK |
| `aws-infra-terraform` | Infraestructura | HCL | Terraform |
| `aws-amplify-react` | Full-stack | TypeScript | Amplify |
| `aws-amplify-vue` | Full-stack | TypeScript | Amplify |
| `aws-amplify-nuxt` | Full-stack | TypeScript | Amplify |
| `aws-shared-lib-typescript` | Shared Library | TypeScript | - |
| `aws-shared-lib-python` | Shared Library | Python | - |
| `aws-shared-lib-javascript` | Shared Library | JavaScript | - |

## Verificación post-bootstrap

Después del bootstrap, verificar que existen:

```
.kiro/
├── .orbit-project.json     # Metadata del proyecto
├── agents/                 # Agentes del perfil
├── steering/               # Steering files del perfil
├── skills/                 # Skills del perfil
└── hooks/                  # Hooks del perfil
```

Si alguno falta, el bootstrap no se completó correctamente. Ejecutar resync.

## Reglas de sesión

1. Si el usuario rechaza el bootstrap, no volver a preguntar en la sesión actual.
2. Si el contexto es HOME, preguntar una sola vez si desea crear carpeta de proyecto.
3. Si acepta crear carpeta, prepararla y continuar el flujo desde esa ruta.
4. Si el perfil es ambiguo, resolver con el wizard (nunca pedir el ID crudo).
5. Ninguna skill remota se instala sin confirmación explícita del usuario.
6. Al terminar, actualizar `.orbit-project.json`.
7. No improvisar bootstrap manual ni saltarse la copia de artefactos.
8. El scaffolding comienza solo después del bootstrap exitoso.
9. El bootstrap resuelve un perfil de proyecto de Orbit, no un perfil de AWS CLI.

## Resincronización

Usar resync cuando:
- Se actualizó el framework y se necesitan nuevos artefactos.
- Se cambió el perfil del proyecto.
- Se detectan artefactos faltantes o desactualizados.

El comando es el mismo que el bootstrap, ejecutado sobre un proyecto existente.

## Conflictos de artefactos

- Si un artefacto local fue modificado por el usuario y el framework trae una versión nueva, el pipeline debe detectar el conflicto.
- Estrategia: preservar cambios del usuario, aplicar actualizaciones del framework donde no hay conflicto.
- Artefactos que nunca se sobreescriben: código de aplicación del usuario.
- Artefactos que siempre se actualizan: steering, skills, hooks, agents del perfil.

## Lo que Orbit NO debe hacer durante bootstrap

- ❌ Pedir perfil de AWS CLI, credenciales, access keys o account ID.
- ❌ Ejecutar `aws sts get-caller-identity` (solo si el usuario pide desplegar).
- ❌ Pedir el `project-profile-id` crudo al usuario.
- ❌ Crear código o scaffolding antes de que el bootstrap termine.
- ❌ Instalar skills remotas sin confirmación.
- ❌ Improvisar copiando archivos manualmente en lugar de usar el pipeline.

## Checklist de bootstrap

- [ ] Contexto detectado (HOME vs proyecto).
- [ ] Usuario confirmó preparar entorno.
- [ ] Perfil resuelto con wizard (workload, runtime, provisioner, framework).
- [ ] Pipeline ejecutado con `install.sh --resync-project`.
- [ ] Artefactos verificados (.orbit-project.json, agents, steering, skills, hooks).
- [ ] `.orbit-project.json` actualizado.
- [ ] Listo para scaffolding.
