---
alwaysApply: true
---

# Projeto

Aplicação para registro de progressão de carga em academia.

## Regras

- Sempre utilizar TypeScript.
- Nunca utilizar any.
- Utilizar Server Actions antes de criar APIs.
- Utilizar Prisma para acesso ao banco.
- Validar entradas com Zod.
- Componentes devem ser pequenos.
- Evitar lógica de negócio em componentes React.
- Regras de negócio devem ficar em services.
- Acesso ao banco deve ficar em repositories.

## Estrutura

modules/
actions/
services/
repositories/
validations/
components/

## Banco

A fonte da verdade é o schema Prisma.

## MVP

O foco é:

- treinos
- exercícios
- séries
- carga
- repetições
- histórico

Não implementar funcionalidades fora do MVP sem solicitação explícita.

# Git Workflow

Toda feature implementada deve:

1. Respeitar o escopo do roadmap.
2. Não alterar funcionalidades não relacionadas.
3. Passar pelo lint e typecheck.
4. Gerar uma sugestão de commit utilizando Conventional Commits.

Formato:

type(scope): descrição

Exemplos:

feat(workouts): create workout CRUD

feat(exercises): add exercise creation flow

feat(sessions): register workout sets

feat(progress): add weight progression chart

fix(workouts): validate workout name

refactor(repositories): extract prisma queries

docs(architecture): update module structure
