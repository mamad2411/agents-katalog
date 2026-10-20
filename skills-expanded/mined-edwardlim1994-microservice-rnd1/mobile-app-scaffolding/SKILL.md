# Mobile App Scaffolding

## Purpose
Scaffolds new React Native Expo mobile applications using Turborepo generators.

## Role
Mobile Developer

## Phase
Development

## Triggered By
New mobile app needed.

## Inputs
- Architect's mobile app requirement

## Process
Framework: React Native Expo. Development: Expo web mode in Coder (agent cannot run native simulator).

`bun turbo gen → mobile app`

Mobile module generator in development — until ready: follow existing mobile app module structure manually. Same generator principle as frontend: never scaffold manually once the generator is available.

## Outputs
Scaffolded mobile app ready for module development.

## Quality Gates
- [ ] Generator used once available (manual structure-following only until then)
- [ ] Expo web mode confirmed working for local development
- [ ] Structure mirrors established mobile app pattern

## References
- `.claude/skills/frontend-developer/webapp-scaffolding/SKILL.md`
- `.claude/skills/mobile-developer/module-scaffolding/SKILL.md`
