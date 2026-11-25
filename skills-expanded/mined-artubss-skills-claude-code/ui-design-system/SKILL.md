---
name: ui-design-system
description: Kit de ferramentas de sistema de design de UI para Designer de UI Sênior, incluindo geração de design tokens, documentação de componentes, cálculos de design responsivo e ferramentas de handoff para desenvolvimento. Use para criar sistemas de design, manter consistência visual e facilitar colaboração entre design e desenvolvimento.
---

# Sistema de Design de UI

Kit de ferramentas profissional para criar e manter sistemas de design escaláveis.

## Capacidades Principais
- Geração de design tokens (cores, tipografia, espaçamento)
- Arquitetura de sistema de componentes
- Cálculos de design responsivo
- Conformidade com acessibilidade
- Documentação de handoff para desenvolvimento

## Scripts Principais

### design_token_generator.py
Gera tokens de sistema de design completos a partir de cores da marca.

**Uso**: `python scripts/design_token_generator.py [brand_color] [style] [format]`
- Estilos: modern, classic, playful
- Formatos: json, css, scss

**Recursos**:
- Geração de paleta de cores completa
- Escala tipográfica modular
- Sistema de grid de espaçamento 8pt
- Tokens de sombra e animação
- Breakpoints responsivos
- Múltiplos formatos de exportação