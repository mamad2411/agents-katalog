---
name: domain-driven-design
description: "Planeje e roteirize trabalho de Domain-Driven Design desde modelagem estratégica até implementação tática e padrões de arquitetura orientada a eventos."
risk: safe
source: self
tags: "[ddd, domain, bounded-context, architecture]"
date_added: "2026-02-27"
---

# Domain-Driven Design

## Use this skill when

- Você precisa modelar um domínio de negócio complexo com limites explícitos.
- Você quer decidir se DDD completo vale a complexidade adicional.
- Você precisa conectar decisões de design estratégico a padrões de implementação.
- Você está planejando CQRS, event sourcing, sagas ou projeções a partir de necessidades do domínio.

## Do not use this skill when

- O problema é CRUD simples com baixa complexidade de negócio.
- Você só precisa de correções localizadas de bugs.
- Não há acesso a conhecimento de domínio e nenhum especialista de produto proxy.

## Instructions

1. Execute uma verificação de viabilidade antes de se comprometer com DDD completo.
2. Produza artefatos estratégicos primeiro: subdomínios, bounded contexts, glossário de linguagem.
3. Roteirize para skills especializadas com base na tarefa atual.
4. Defina critérios de sucesso e evidências para cada etapa.

### Viability check

Use DDD completo apenas quando pelo menos dois destes forem verdadeiros:

- Regras de negócio são complexas ou mudam rapidamente.
- Múltiplos times estão causando colisões de modelos.
- Contratos de integração são instáveis.
- Auditoria e invariantes explícitos são críticos.

### Routing map

- Modelo estratégico e limites: `@ddd-strategic-design`
- Integrações cross-context e tradução: `@ddd-context-mapping`
- Modelagem de código tática: `@ddd-tactical-patterns`
- Separação leitura/escrita: `@cqrs-implementation`
- Histórico de eventos como fonte de verdade: `@event-sourcing-architect` e `@event-store-design`
- Workflows de longa duração: `@saga-orchestration`
- Modelos de leitura: `@projection-patterns`
- Decision log: `@architecture-decision-records`

Se templates forem necessários, abra `references/ddd-deliverables.md`.

## Output requirements

Sempre retorne:

- Escopo e suposições
- Etapa atual (estratégica, tática ou orientada a eventos)
- Artefatos explícitos produzidos
- Riscos abertos e recomendação do próximo passo

## Examples

```text
Use @domain-driven-design to assess if this billing platform should adopt full DDD.
Then route to the right next skill and list artifacts we must produce this week.
```

## Limitations

- Esta skill não substitui workshops diretos com especialistas de domínio.
- Ela não fornece geração de código específica do framework.
- Ela não deve ser usada como justificativa para over-engineer sistemas simples.