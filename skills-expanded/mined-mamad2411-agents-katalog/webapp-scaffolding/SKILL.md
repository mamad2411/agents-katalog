# Webapp Scaffolding

## Purpose
Scaffolds new React web applications using Turborepo generators.

## Role
Frontend Developer

## Phase
Development

## Triggered By
New frontend app needed (Architect decides if MFE or standalone).

## Inputs
- Architect's MFE/standalone decision (from `technical-assessment`)

## Rule
ALWAYS use generator — NEVER scaffold manually. Command: `bun turbo gen → select webapp type`.

## Process

### Types (Architect decides during planning)
- `standalone`: regular React app (`apps/web/{name}/`)
- `mfe-remote`: Module Federation remote (`apps/mfe/{name}/`)
- `mfe-host`: Module Federation host (`apps/web/{name}/` with remotes)

### Generator Creates
- Rsbuild config (`rsbuild.config.ts`)
- File-based routing setup
- `shared/` folder structure
- `modules/` folder structure
- Storybook configuration
- `docker-compose.yml` (for local dev)
- Helm chart (for Kubernetes deployment)
- `.env.example`

After scaffolding: run `environment-configuration` before starting development.

## Outputs
Scaffolded web app ready for module development.

## Quality Gates
- [ ] Generator used (not manual file creation)
- [ ] Correct type selected (matches Architect's decision)
- [ ] environment-configuration run after scaffolding

## References
- `.claude/skills/frontend-developer/environment-configuration/SKILL.md`
- `.claude/skills/frontend-developer/module-federation-setup/SKILL.md`
- `.claude/skills/solution-architect/technical-assessment/SKILL.md`
