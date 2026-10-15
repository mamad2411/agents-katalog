---
name: workflow-analise-migracao-aws
description: Orquestra migration-analyzer e migration-analyzer-revisor em ciclo Maker/Checker para analise de migracao AWS por contexto.
---

# Workflow Skill: Analise Migracao AWS

Use quando o usuário pedir "análise de migração AWS" ou mencionar `/analise-migracao-aws`.

## Fluxo
1. Coletar `contexto`, lista de repositórios e padrões corporativos (env vars/URLs).
2. Criar estrutura `migracao-{contexto}/repos` e `migracao-{contexto}/analise`.
3. Criar symlinks dos repositórios em `repos/`.
4. Rodar `migration-analyzer` para gerar artefatos na pasta `analise/`.
5. Rodar `migration-analyzer-revisor` e aplicar loop de correção (max 5).
6. Entregar laudo aprovado (ou com ressalvas) e caminhos dos artefatos.

## Regra
- Validar pelo menos 1 repositório existente antes de iniciar.
