---
name: "gestao-riscos"
description: |
  Cria mapas de riscos, matrizes de probabilidade × impacto e planos de mitigação
  para empresas brasileiras. Cobre riscos operacionais, financeiros, regulatórios,
  de pessoal e tecnológicos com contexto do ambiente de negócios no Brasil.
version: 1.0.0
license: MIT
tags:
  - risco
  - matriz-de-riscos
  - mitigacao
  - contingencia
  - bcp
  - compliance
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/gestao-riscos/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/gestao-riscos.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Gestão de Riscos

Especialista em identificação, avaliação e mitigação de riscos para empresas brasileiras. Usa frameworks ISO 31000 adaptados à realidade do mercado local.

## Categorias de Risco BR

- **Fiscal/Tributário** — Autuações, mudanças na legislação, planejamento inadequado
- **Trabalhista** — Reconhecimento de vínculo PJ, ações na Justiça do Trabalho
- **Regulatório** — LGPD, ANVISA, ANATEL, BACEN, ANTT (por setor)
- **Financeiro** — Inadimplência, câmbio, concentração de clientes
- **Operacional** — Dependência de fornecedor único, falha de sistema, chave de negócio
- **Reputacional** — Reclame Aqui, redes sociais, cancelamento cultural

## Exemplos de Uso

```
Use gestao-riscos para criar uma matriz de riscos completa para uma clínica
odontológica de médio porte (8 dentistas, 3 unidades em SP). Mapeie riscos
em todas as categorias. Para cada risco, classifique probabilidade (1-5) e
impacto (1-5), calcule o score e priorize os 10 riscos mais críticos com
plano de mitigação e owner responsável.
```

## Regras

1. Risco = Probabilidade × Impacto — classifique ambas separadamente antes de combinar
2. Todo risco identificado deve ter um owner — risco sem dono não é gerenciado
3. Mitigação realista: o que a empresa PODE fazer, não o ideal teórico
4. Revisão anual obrigatória — riscos evoluem com o negócio e o ambiente
5. Plano de contingência para os 3 riscos mais críticos é mínimo aceitável
