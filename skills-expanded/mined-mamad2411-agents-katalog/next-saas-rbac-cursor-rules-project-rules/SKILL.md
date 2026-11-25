# Project Rules Index

Este arquivo serve como índice para todas as regras do projeto SaaS RBAC.

## Arquivos de Regras

### Documentação Core
- **`memory.mdc`**: Regras de memória e aprendizado - **DEVE SER LIDO PRIMEIRO**
- **`project.mdc`**: Preferências do projeto e padrões de código
- **`self.mdc`**: Log de erros e correções aprendidas

### Documentação Técnica
- **`api.mdc`**: Documentação completa de todos os endpoints da API
- **`database-schema.mdc`**: Schema do banco de dados e padrões de query

### Agentes Especialistas
- **`expert-software-engineer.mdc`**: Diretrizes para implementação e qualidade de código
- **`expert-solution-architect.mdc`**: Padrões arquiteturais e coerência do sistema
- **`expert-system-design.mdc`**: Design de sistemas escaláveis e distribuídos

## Fluxo de Trabalho Recomendado

1. **Antes de cada requisição**: Ler `memory.mdc` e `project.mdc`
2. **Durante desenvolvimento**: Consultar arquivos relevantes (`api.mdc`, `database-schema.mdc`)
3. **Após cada requisição**: Atualizar documentação se necessário
4. **Ao encontrar erros**: Registrar em `self.mdc`

## Referência Rápida

- **Criar/modificar API**: Consultar `api.mdc` antes e atualizar depois
- **Operações de banco**: Consultar `database-schema.mdc` antes e atualizar depois
- **Decisões arquiteturais**: Seguir `expert-solution-architect.mdc`
- **Otimizações de performance**: Seguir `expert-system-design.mdc`
- **Implementação de código**: Seguir `expert-software-engineer.mdc`

