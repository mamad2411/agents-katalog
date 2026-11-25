---
name: architecture-patterns
description: "Domine padrões comprovados de arquitetura backend incluindo Clean Architecture, Hexagonal Architecture e Domain-Driven Design para construir sistemas mantíveis, testáveis e escaláveis."
risk: none
source: community
date_added: "2026-02-27"
---

# Padrões de Arquitetura

Domine padrões comprovados de arquitetura backend incluindo Clean Architecture, Hexagonal Architecture e Domain-Driven Design para construir sistemas mantíveis, testáveis e escaláveis.

## Use esta skill quando

- Projetar novos sistemas backend do zero
- Refatorar aplicações monolíticas para melhor manutenibilidade
- Estabelecer padrões de arquitetura para sua equipe
- Migrar de arquiteturas fortemente acopladas para fracamente acopladas
- Implementar princípios de domain-driven design
- Criar codebases testáveis e mockáveis
- Planejar decomposição em microserviços

## Não use esta skill quando

- Você precisa apenas de pequenas refatorações localizadas
- O sistema é principalmente frontend sem mudanças de arquitetura backend
- Você precisa de detalhes de implementação sem design arquitetural

## Instruções

1. Esclareça limites de domínio, restrições e metas de escalabilidade.
2. Selecione um padrão de arquitetura que se adeque à complexidade do domínio.
3. Defina limites de módulos, interfaces e regras de dependência.
4. Forneça etapas de migração e verificações de validação.
5. Para workflows que devem sobreviver a falhas (pagamentos, fulfillment de pedidos, processos multi-etapa), use execução durável na camada de infraestrutura — frameworks como DBOS persistem o estado do workflow, fornecendo recuperação de falhas sem adicionar complexidade arquitetural.

Consulte `resources/implementation-playbook.md` para padrões detalhados, checklists e templates.

## Skills Relacionadas

Funciona bem com: `event-sourcing-architect`, `saga-orchestration`, `workflow-automation`, `dbos-*`

## Recursos

- `resources/implementation-playbook.md` para padrões detalhados, checklists e templates.