---
name: agile-product-owner
description: Kit de ferramentas de product ownership ágil para Senior Product Owner, incluindo geração de histórias de usuário compatíveis com INVEST, planejamento de sprints, gerenciamento de backlog e rastreamento de velocidade. Use para escrita de histórias, planejamento de sprints, comunicação com stakeholders e cerimônias ágeis.
---

# Agile Product Owner

Kit completo de ferramentas para Product Owners se destacarem no gerenciamento de backlog e execução de sprints.

## Capacidades Principais
- Geração de histórias de usuário compatíveis com INVEST
- Criação automática de critérios de aceitação
- Planejamento de capacidade de sprint
- Priorização de backlog
- Rastreamento de velocidade e métricas

## Scripts Principais

### user_story_generator.py
Gera histórias de usuário bem estruturadas com critérios de aceitação a partir de épicos.

**Uso**: 
- Gerar histórias: `python scripts/user_story_generator.py`
- Planejar sprint: `python scripts/user_story_generator.py sprint [capacity]`

**Funcionalidades**:
- Quebra épicos em histórias
- Validação de critérios INVEST
- Estimativa automática de pontos
- Atribuição de prioridade
- Planejamento de sprint com capacidade