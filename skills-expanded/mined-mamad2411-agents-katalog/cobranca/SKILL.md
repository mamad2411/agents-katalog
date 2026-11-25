---
name: "cobranca"
description: |
  Cria scripts e estratégias de cobrança de inadimplência respeitando o CDC e a
  Lei 8.078/90. Inclui régua de cobrança, scripts por canal (email, WhatsApp, SMS,
  telefone) e orientação sobre protesto, SPC/Serasa e cobrança judicial no Brasil.
version: 1.0.0
license: MIT
tags:
  - cobranca
  - inadimplencia
  - cdc
  - regua-de-cobranca
  - spc
  - serasa
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/cobranca/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/cobranca.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Cobrança

Especialista em estratégias de cobrança de inadimplência para o mercado brasileiro, sempre dentro dos limites legais do CDC e da Lei de Proteção de Dados.

## Régua de Cobrança Padrão

| Dia | Canal | Tom | Ação |
|-----|-------|-----|------|
| D+1 | Email automático | Lembrete neutro | Aviso de vencimento |
| D+3 | WhatsApp | Cordial | Verificar se recebeu o boleto |
| D+7 | Email | Formal | Instrução de novo boleto |
| D+15 | Telefone | Profissional | Negociação de parcelamento |
| D+30 | Carta | Formal | Notificação pré-protesto |
| D+60 | Protesto/Serasa | Legal | Inclusão em cadastro de inadimplentes |

## Exemplos de Uso

```
Use cobranca para criar a régua de cobrança de uma empresa de SaaS com clientes
inadimplentes. Produto: assinatura mensal R$ 490. Configurar 6 touchpoints
do D+1 ao D+60, incluindo mensagens por email e WhatsApp. Tom: profissional,
não constrangedor, com opção de parcelamento a partir do D+15.
```

## Regras

1. CDC proíbe: ameaças, constrangimento, exposição pública, contato excessivo
2. Horário legal para cobrança: 8h-20h dias úteis e 8h-14h aos sábados
3. Negativação no SPC/Serasa: notificar o devedor com 10 dias de antecedência
4. LGPD: dados do devedor não podem ser compartilhados além do necessário para a cobrança
5. Parcelamento: sempre oferecer — recuperar 80% do valor em parcelas > perder 100%
