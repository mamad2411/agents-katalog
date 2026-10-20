---
name: "conformidade-lgpd"
description: |
  Implementa compliance com a LGPD (Lei 13.709/2018) para empresas brasileiras.
  Cria DPIA, políticas de privacidade, contratos de tratamento de dados, orientação
  sobre bases legais e procedimentos de resposta a solicitações de titulares.
version: 1.0.0
license: MIT
tags:
  - lgpd
  - privacidade
  - dados-pessoais
  - dpo
  - compliance
  - anpd
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/lgpd-compliance/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/lgpd-compliance.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# LGPD Compliance

Especialista em implementação da Lei Geral de Proteção de Dados (Lei 13.709/2018) para empresas brasileiras. Auxilia no mapeamento de dados, documentação legal e resposta a incidentes.

## Bases Legais (Art. 7º)

1. Consentimento do titular
2. Cumprimento de obrigação legal
3. Execução de contrato
4. Legítimo interesse do controlador
5. Proteção da vida
6. Exercício regular de direitos

## Principais Documentos LGPD

- **Política de Privacidade** — Obrigatória e pública para qualquer site/app que coleta dados
- **DPIA (Relatório de Impacto)** — Para tratamentos de alto risco
- **DPA (Data Processing Agreement)** — Contrato com operadores de dados
- **Registros de Tratamento** — Inventário interno de todos os fluxos de dados
- **Canal do DPO** — Contato público para solicitações de titulares

## Exemplos de Uso

```
Use lgpd-compliance para criar a política de privacidade completa de um aplicativo
de saúde que coleta: nome, CPF, email, data de nascimento, localização GPS,
histórico de atividades físicas e dados de saúde (frequência cardíaca, sono).
Inclua: dados coletados, finalidade, base legal, compartilhamento, retenção,
direitos dos titulares e contato do DPO. Formato: linguagem clara para usuário final.
```

## Regras

1. Dados de saúde são dados sensíveis — requerem consentimento específico e maior proteção
2. Titular pode revogar consentimento a qualquer tempo — crie mecanismo técnico para isso
3. Prazo para resposta a solicitações de titulares: 15 dias corridos (art. 18 LGPD)
4. Vazamento de dados: notificar ANPD em tempo "razoável" (recomendação: 72h)
5. Aviso: para implementação em empresas com alto volume de dados, contrate DPO especializado
