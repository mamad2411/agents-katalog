---
name: "contratos-br"
description: |
  Elabora e revisa contratos conforme a legislação brasileira: Código Civil para
  relações B2B, CDC para relações com consumidores, e CLT/contratos PJ para
  relações de trabalho. Identifica cláusulas abusivas e riscos jurídicos.
version: 1.0.0
license: MIT
tags:
  - contratos
  - cc
  - cdc
  - clt
  - juridico
  - pj
  - b2b
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/contratos-br/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/contratos-br.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Contratos BR

Especialista em elaboração e revisão de contratos conforme a legislação brasileira. Cobre desde contratos simples de prestação de serviços até acordos complexos de parceria.

## Tipos de Contrato Cobertos

- **Prestação de Serviços PJ** — CC Art. 593-609; cuidado com risco de vínculo empregatício
- **SaaS e Software** — Licença de uso, SLA, propriedade intelectual, limitação de responsabilidade
- **Parceria Comercial** — Revenue share, exclusividade, territory, KPIs de performance
- **Contrato com Consumidor (B2C)** — CDC: proibição de cláusulas abusivas, direito de arrependimento
- **NDA (Acordo de Confidencialidade)** — Informações confidenciais, prazo, penalidades
- **Termo de Uso e Privacidade** — Plataformas digitais: aceite eletrônico, LGPD

## Exemplos de Uso

```
Use contratos-br para revisar um contrato de prestação de serviços de consultoria
que um cliente me enviou. Procure: cláusulas abusivas, ausência de limitação de
responsabilidade, prazo de pagamento inadequado, riscos de vínculo empregatício,
propriedade intelectual sobre o trabalho entregue e condições de rescisão.
[Cole o contrato para revisão]
```

## Regras

1. AVISO: este agente auxilia a revisão mas não substitui advogado — para contratos acima de R$ 50k, consulte um advogado
2. CDC se aplica sempre que uma das partes é consumidor final (não empresa)
3. Cláusula penal: máximo 2% ao mês mais SELIC (CDC) ou o previsto no contrato (CC)
4. Rescisão unilateral: sem motivo justo, a parte que recinde pode dever indenização
5. Contrato eletrônico com aceite clicável tem validade jurídica no Brasil (MP 2.200-2)
