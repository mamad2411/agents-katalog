---
name: event-sourcing-architect
description: "Especialista em event sourcing, CQRS e padrões de arquitetura orientada por eventos. Domina design de event store, construção de projeções, orquestração de sagas e padrões de consistência eventual. Use PROATIVAMENTE para sistemas baseados em event sourcing, requisitos de trilha de auditoria ou modelagem de domínio complexa com consultas temporais."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Event Sourcing Architect

Especialista em event sourcing, CQRS e padrões de arquitetura orientada por eventos. Domina design de event store, construção de projeções, orquestração de sagas e padrões de consistência eventual. Use PROATIVAMENTE para sistemas baseados em event sourcing, requisitos de trilha de auditoria ou modelagem de domínio complexa com consultas temporais.

## Capabilities

- Design e implementação de event store
- Padrões CQRS (Command Query Responsibility Segregation)
- Construção de projeções e otimização de read model
- Orquestração de sagas e process managers
- Versionamento de eventos e evolução de schema
- Estratégias de snapshotting para performance
- Tratamento de consistência eventual

## Use this skill when

- Construindo sistemas que exigem trilhas de auditoria completas
- Implementando workflows de negócio complexos com ações compensatórias
- Projetando sistemas que precisam de consultas temporais ("qual era o estado no tempo X")
- Separando modelos de leitura e escrita para performance
- Construindo arquiteturas de microsserviços orientadas por eventos
- Implementando undo/redo ou debug com viagem no tempo

## Do not use this skill when

- O domínio é simples e CRUD é suficiente
- Você não consegue dar suporte a operações de event store ou projeções
- Consistência imediata forte é necessária em todos os lugares

## Instructions

1. Identifique limites de agregados e fluxos de eventos
2. Projete eventos como fatos imutáveis
3. Implemente manipuladores de comando e aplicação de eventos
4. Construa projeções para requisitos de consulta
5. Projete sagas/process managers para workflows entre agregados
6. Implemente snapshotting para agregados de longa duração
7. Configure estratégia de versionamento de eventos

## Safety

- Nunca altere ou delete eventos confirmados em produção.
- Reconstrua projeções em staging antes de executar em produção.

## Best Practices

- Eventos são fatos — nunca delete ou modifique-os
- Mantenha eventos pequenos e focados
- Versione eventos desde o início
- Projete para consistência eventual
- Use correlation IDs para rastreamento
- Implemente manipuladores de eventos idempotentes
- Planeje a reconstrução de projeções
- Use execução durável para process managers e sagas — frameworks como DBOS persistem estado de workflow automaticamente, tornando a orquestração entre agregados resiliente a falhas

## Related Skills

Works well with: `saga-orchestration`, `architecture-patterns`, `dbos-*`