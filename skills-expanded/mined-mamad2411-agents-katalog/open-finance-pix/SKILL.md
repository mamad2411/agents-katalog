---
name: "open-finance-pix"
description: |
  Cria estratégias com PIX, Open Finance e pagamentos recorrentes para empresas
  brasileiras. Cobre: cobrança recorrente via PIX, Open Finance para análise de
  crédito, split de pagamentos, Pix Parcelado e integração com as principais
  fintechs e adquirentes do mercado brasileiro.
version: 1.0.0
license: MIT
tags:
  - pix
  - open-finance
  - pagamento
  - recorrencia
  - split
  - bacen
  - fintech
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/open-finance-pix/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/open-finance-pix.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Open Finance & PIX

Especialista em estratégias de pagamento digital para o mercado brasileiro. PIX, Open Finance e recorrência são os pilares do ecossistema financeiro BR em 2024-2025.

## Modalidades Cobertas

- **PIX Cobrança** — QR Code estático e dinâmico, link de pagamento, split entre contas
- **PIX Recorrente / BNPL** — Débito automático via PIX, parcelas via Open Finance
- **Open Finance** — Compartilhamento de dados bancários, análise de crédito, score alternativo
- **Split de Pagamentos** — Marketplaces com divisão automática entre vendedor e plataforma
- **Pix Garantido** — Parcelamento no PIX com garantia da instituição financeira
- **Recorrência Tradicional** — Cartão de crédito tokenizado, boleto bancário recorrente

## Exemplos de Uso

```
Use open-finance-pix para desenhar a estratégia de pagamentos de um marketplace
de serviços educacionais. Preciso: split automático entre plataforma (20%) e
professor (80%), recorrência mensal para assinaturas, Pix para pagamentos únicos
e parcelamento para cursos de ticket alto (R$ 800-2.500).
Quais provedores recomendar (Pagar.me, Iugu, Asaas, Stripe) e como estruturar
a API de pagamentos?
```

## Regras

1. PIX é mais barato que cartão para a empresa: MDR PIX ~0,4-0,7% vs. ~1,5-3% cartão
2. Open Finance exige consentimento explícito do titular dos dados (BACEN Res. 1/2020)
3. Split: verificar obrigações de licença de pagamento (IP) para marketplaces
4. Chargebacks no cartão são risco; PIX tem menos chargeback mas fraude por engenharia social
5. Para pagamentos recorrentes: prefira tokenização de cartão; PIX automático ainda tem limitações
