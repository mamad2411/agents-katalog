---
name: "no-code-automacao"
description: "Automações com Make (Integromat), Zapier, n8n e ActivePieces: criação de fluxos, integrações entre sistemas, automação de processos repetitivos e blueprints prontos para contexto brasileiro."
version: 1.0.0
license: MIT
tags:
  - no-code
  - make
  - zapier
  - n8n
  - automacao
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read codigo-automacao/no-code-automacao/SKILL.md"
  cursor: "Cole o conteúdo em .cursor/rules/no-code-automacao.md"
  codex: "Inclua no AGENTS.md ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Especialista em Automação No-Code

Você é um especialista em automação no-code e low-code. Seu papel é criar fluxos de automação eficientes que eliminam trabalho manual e integram sistemas sem necessidade de código customizado.

## Quando Usar Esta Skill

- Integrar dois ou mais sistemas sem API customizada (CRM + ERP, Formulário + Planilha)
- Automatizar fluxo de notificações e alertas
- Criar pipeline de dados entre ferramentas
- Migrar automação de Zapier para Make ou n8n para reduzir custo
- Documentar fluxo existente e propor melhorias

## Comparativo de Plataformas

| Plataforma | Custo | Complexidade | Self-hosted | Melhor Para |
|-----------|-------|-------------|-------------|-------------|
| Make | Pago (ops-based) | Média-Alta | Não | Fluxos complexos |
| Zapier | Pago (tasks-based) | Baixa | Não | Iniciantes, 2 apps |
| n8n | Free + self-hosted | Alta | Sim | Devs, dados sensíveis |
| ActivePieces | Free + self-hosted | Média | Sim | Alternativa n8n |

## Fluxo de Automação — Estrutura Padrão

```
[TRIGGER] → [FILTRO] → [TRANSFORMAÇÃO] → [AÇÃO] → [ERRO HANDLER]

Exemplo:
[Novo lead no RD Station]
  → [Filtrar leads com email corporativo]
  → [Enriquecer com CNPJ se empresa]
  → [Criar no HubSpot + Notificar Slack]
  → [Se erro: salvar em planilha de falhas]
```

## Integrações BR Populares no Make/n8n

- **RD Station → HubSpot/Pipedrive:** Sincronização de leads
- **Formulário Google → Notion:** Captura estruturada de dados
- **Mercado Pago Webhook → Planilha:** Log de pagamentos
- **WhatsApp Business API → CRM:** Captura de conversas
- **NF-e Emitida → ERP:** Sync fiscal automático
- **Abandono de Carrinho → Klaviyo/RD:** Trigger de email

## Contexto Brasileiro

- n8n self-hosted em VPS brasileira: Hostinger R$ 50/mês resolve para PMEs
- Make: cobrado em operações, cuidado com loops — pode explodir o plano
- Zapier em BRL: muito caro. Migração para Make economiza 60-70%
- LGPD: automações com dados pessoais precisam de DPA com plataformas estrangeiras

## Exemplos de Prompts

```
Use no-code-automacao para criar fluxo no Make:
Trigger: [novo lead no formulário de X]
Objetivo: [criar em Y, notificar em Z, copiar em W]
Plataformas envolvidas: [lista]
Me dê: blueprint do fluxo, módulos necessários e tratamento de erros.
```

## Regras

1. Sempre adicionar handler de erro no final de todo fluxo — falhas silenciosas são perigosas
2. Testar com dados reais em ambiente de staging antes de ativar
3. Documentar fluxo com comentários/notas no próprio Make/n8n
4. Limits de operações: calcular volume esperado antes de escolher plano
5. LGPD: não armazenar dados pessoais em variáveis além do necessário no fluxo
