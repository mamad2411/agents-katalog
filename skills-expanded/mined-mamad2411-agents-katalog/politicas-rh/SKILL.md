---
name: "politicas-rh"
description: |
  Cria políticas internas de RH, código de conduta e handbook do colaborador para
  empresas brasileiras. Todas as políticas são alinhadas à CLT, LGPD e boas práticas
  de gestão de pessoas, com linguagem acessível e aplicável ao cotidiano.
version: 1.0.0
license: MIT
tags:
  - politicas
  - handbook
  - codigo-conduta
  - rh
  - clt
  - compliance
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read operacoes-rh/politicas-rh/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/politicas-rh.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Políticas de RH

Especialista em criação de políticas internas e handbook do colaborador para empresas brasileiras. Políticas claras previnem conflitos e alinham expectativas.

## Políticas Mais Solicitadas

- **Home Office / Trabalho Remoto** — Elegibilidade, equipamentos, ajuda de custo (CLT art. 75-D)
- **Benefícios Flexíveis** — Regras de uso de Gympass, cartão benefício, day off
- **Política de Férias** — Agendamento, coletivas, abono pecuniário
- **Código de Conduta** — Comportamentos esperados, situações de conflito, denúncia
- **Uso de Tecnologia e Redes Sociais** — Uso pessoal de equipamentos corporativos
- **Diversidade e Inclusão** — Compromisso formal, canais de denúncia
- **Política de Horas Extras** — Banco de horas vs. pagamento; regras do acordo coletivo

## Exemplos de Uso

```
Use politicas-rh para criar a política de home office de uma startup de 22 pessoas.
A empresa tem modelo híbrido: 2 dias presenciais obrigatórios por semana para todos.
Para home office, a empresa oferece R$ 150/mês de ajuda de custo e empréstimo de
cadeira ergonômica. Inclua: quem é elegível, regras de disponibilidade, uso de
ferramentas, e o que acontece se não comparecer ao dia presencial.
```

## Regras

1. Ajuda de custo home office: art. 75-D CLT — deve ser acordada em contrato, não caracteriza salário
2. Banco de horas: precisa de acordo coletivo ou individual por escrito (não vale só combinar)
3. Código de conduta: comunicar formalmente a todos e ter confirmação de recebimento
4. Políticas discriminatórias (faixa etária, estado civil, etc.) são ilegais no Brasil
5. Revisar políticas anualmente e sempre que houver mudança legislativa relevante
