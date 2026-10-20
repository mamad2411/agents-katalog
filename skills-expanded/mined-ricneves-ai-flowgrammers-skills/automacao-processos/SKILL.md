---
name: "automacao-processos"
description: |
  Identifica oportunidades de automação e cria fluxos de trabalho com Make (Integromat),
  Zapier, n8n e ferramentas nativas. Foca em operações, RH e atendimento com as
  ferramentas mais utilizadas no mercado brasileiro de PMEs e startups.
version: 1.0.0
license: MIT
tags:
  - automacao
  - make
  - zapier
  - n8n
  - processos
  - operacoes
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read operacoes-rh/automacao-processos/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/automacao-processos.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Automação de Processos

Especialista em automação de operações para empresas brasileiras. Identifica o que automatizar, com qual ferramenta e como implementar.

## Ferramentas por Perfil

| Ferramenta | Perfil | Custo | Ideal para |
|------------|--------|-------|-----------|
| Make (Integromat) | Visual, avançado | A partir de $9/mês | Fluxos complexos com lógica |
| Zapier | Visual, simples | A partir de $20/mês | Integrações rápidas entre apps |
| n8n | Dev-friendly, auto-hospedado | Gratuito (self-hosted) | Times técnicos, dados sensíveis |
| Power Automate | Microsoft 365 | Incluído no M365 | Empresas no ecossistema Microsoft |

## Processos Mais Automatizados em PMEs BR

- Onboarding de colaboradores (criar contas, enviar docs)
- Notificações de boletos vencidos e lembretes de pagamento
- Qualificação de leads (formulário → CRM → Slack/WhatsApp)
- Relatórios periódicos (exportar → formatar → enviar)
- Atualização de planilhas após vendas no CRM

## Exemplos de Uso

```
Use automacao-processos para mapear e automatizar o processo de admissão de
novo colaborador na empresa. Ferramentas disponíveis: Make, Slack, Google Workspace,
Notion e BambooHR. O processo atual: RH manda email manual para TI criar conta,
para facilities preparar mesa, e para gestor preparar onboarding. Leva 3 dias.
Meta: automatizar para que tudo aconteça em 2 horas após aprovação no ATS.
```

## Regras

1. Documentar o processo manual antes de automatizar — automação de caos gera caos mais rápido
2. Começar pequeno: automatize a tarefa mais repetitiva e de menor risco primeiro
3. Sempre ter um fallback manual — o que acontece se a automação falhar?
4. LGPD: dados pessoais em automações precisam de análise de segurança e minimização
5. n8n self-hosted para dados sensíveis (CPF, dados financeiros) — evite cloud de terceiros
