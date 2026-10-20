---
name: "produto-ecommerce"
description: "Skills para lançamento de produtos digitais, estratégias PLG, operações de e-commerce e métricas SaaS com contexto do mercado brasileiro. Use quando precisar de playbooks de lançamento, análise de churn, precificação em R$, operações de marketplace BR ou métricas de produto."
version: 1.0.0
license: MIT
tags:
  - produto
  - ecommerce
  - saas
  - plg
  - churn
  - lancamento
  - marketplace
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read produto-ecommerce/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/produto-ecommerce.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Produto, E-commerce & SaaS (Nível PODEROSO)

Skills completas para lançamento de produtos digitais, estratégias de crescimento, operações de e-commerce e métricas SaaS adaptadas ao mercado brasileiro. Do pré-lançamento ao pós-venda, cobrindo Mercado Livre, Shopee, Amazon BR e integrações com pagamentos PIX/Boleto. Focado em resultados mensuráveis e playbooks replicáveis para o contexto nacional.

## Início Rápido

### Claude Code
```
/read produto-ecommerce/lancamento-produto/SKILL.md
/read produto-ecommerce/estrategia-plg/SKILL.md
/read produto-ecommerce/analise-de-churn/SKILL.md
/read produto-ecommerce/operacoes-ecommerce/SKILL.md
/read produto-ecommerce/precificacao-saas/SKILL.md
/read produto-ecommerce/roadmap-de-produto/SKILL.md
/read produto-ecommerce/upsell-e-crosssell/SKILL.md
/read produto-ecommerce/estrategia-marketplace/SKILL.md
/read produto-ecommerce/abandono-de-carrinho/SKILL.md
/read produto-ecommerce/analitica-de-produto/SKILL.md
```

### Cursor
Adicione em `.cursor/rules/produto-ecommerce.md`:
```
Você é um especialista em produto digital e e-commerce para o mercado brasileiro.
Contexto: PIX, Boleto, marketplaces BR (Mercado Livre, Shopee, Magalu, Amazon BR).
Métricas sempre em R$. Considere sazonalidade BR (Black Friday, Dia das Mães, etc).
```

### Codex
Inclua no `AGENTS.md`:
```
## Especialista em Produto BR
Consulte produto-ecommerce/ para estratégias de lançamento, PLG, churn e e-commerce.
Sempre adapte métricas para R$ e considere regulamentações brasileiras (NF-e, LGPD).
```

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Lançamento de Produto | `lancamento-produto/` | Playbook pré, durante e pós-lançamento |
| Estratégia PLG | `estrategia-plg/` | Trial, freemium, expansão e viralidade |
| Análise de Churn | `analise-de-churn/` | Diagnóstico, cohort e retenção |
| Operações E-commerce | `operacoes-ecommerce/` | Catálogo, frete, checkout, devoluções BR |
| Precificação SaaS | `precificacao-saas/` | Tiers, annual vs monthly, testes de preço em R$ |
| Roadmap de Produto | `roadmap-de-produto/` | RICE, ICE, Now/Next/Later |
| Upsell & Cross-sell | `upsell-e-crosssell/` | Expansão de receita na base de clientes |
| Estratégia Marketplace | `estrategia-marketplace/` | Mercado Livre, Amazon, Shopee, Magalu BR |
| Abandono de Carrinho | `abandono-de-carrinho/` | Email, WhatsApp, retargeting |
| Analítica de Produto | `analitica-de-produto/` | DAU, MAU, NPS, retention, feature adoption |

## Exemplos de Uso

### Lançamento de Produto
```
Use a skill de lancamento-produto e crie um playbook completo para o lançamento
do meu SaaS de gestão financeira para MEIs. Tenho lista de espera de 800 pessoas
e quero fazer o lançamento na próxima segunda-feira.
```

### PLG Strategy
```
Atue como especialista em PLG e analise meu produto de automação de NF-e.
Quero implementar um modelo freemium. Defina os limites do plano gratuito,
gatilhos de conversão e a jornada de expansão para R$ 497/mês.
```

### Análise de Churn
```
Meu SaaS tem 18% de churn mensal. Use a skill de churn-analysis para
diagnosticar as causas prováveis e me dê um plano de 90 dias para
reduzir para menos de 5%.
```

### Precificação SaaS
```
Use pricing-saas para criar 3 tiers de preço para minha plataforma de
agendamentos para clínicas. Tenho custos de infraestrutura de R$ 8/cliente/mês
e quero margem bruta de pelo menos 70%.
```

### Marketplace
```
Quero vender meu produto de skincare no Mercado Livre e Shopee.
Use marketplace-strategy para criar a estratégia de entrada, precificação
competitiva e operação logística com envio de SP para todo o Brasil.
```

### Recuperação de Carrinho
```
Tenho e-commerce de suplementos com 73% de abandono de carrinho.
Use cart-abandonment para criar sequência completa: email D+1, D+3,
WhatsApp D+2 e retargeting no Meta Ads para o mercado brasileiro.
```

## Contexto Brasileiro

### Pagamentos e Checkout
- **PIX:** Principal método no Brasil (70%+ das transações digitais). Implementar PIX instantâneo com QR Code dinâmico
- **Boleto:** Ainda relevante para B2B e classes C/D. Vencimento padrão 3 dias úteis
- **Parcelamento:** Cultura do parcelamento em até 12x sem juros é diferencial competitivo
- **Gateway:** Mercado Pago, PagSeguro, Stripe BR, Asaas, Iugu, Pagar.me

### Logística e Frete
- **Correios:** Base da maioria dos pequenos e-commerces. SEDEX e PAC como padrão
- **Fretes alternativos:** Jadlog, Total Express, Azul Cargo, Loggi
- **Frete grátis:** Gatilho de conversão fundamental. Calcular ponto de equilíbrio
- **Reversa:** LGPD obriga política de troca/devolução. Prazo legal: 7 dias CDC

### Fiscal e Regulatório
- **NF-e / NFC-e:** Obrigatório em vendas físicas e digitais acima de certos valores
- **DIFAL:** Diferencial de alíquota ICMS em vendas interestaduais para consumidor final
- **LGPD:** Consentimento para remarketing e comunicações. Política de privacidade obrigatória

### Sazonalidade Brasileira
| Período | Oportunidade |
|---------|-------------|
| Dia das Mães (mai) | Presente feminino, serviços |
| Dia dos Namorados (jun) | Joias, experiências, moda |
| Black Friday (nov) | Todos os segmentos — maior volume do ano |
| Natal (dez) | Presentes, eletros, moda |
| Dia das Crianças (out) | Brinquedos, games, entretenimento |

### Marketplaces Brasileiros
| Marketplace | Posição | Comissão Média | Diferencial |
|-------------|---------|----------------|-------------|
| Mercado Livre | #1 BR | 10-20% | Base enorme, reputação seller |
| Shopee | Crescimento acelerado | 3-14% | Menor comissão inicial, gamificação |
| Amazon BR | Top 3 | 8-15% | Prime, FBA, confiança internacional |
| Magalu | Top 5 | 12-18% | Forte em eletro e regiões CDE |

## Configuração de Harness

### Claude Code — CLAUDE.md Global
Adicione ao seu `~/.claude/CLAUDE.md`:
```markdown
## Especialista em Produto & E-commerce BR
Quando trabalhar em produto digital, e-commerce ou SaaS:
- Sempre considere contexto brasileiro: PIX, Boleto, parcelamento, marketplaces BR
- Métricas de produto sempre em R$ com contexto de mercado nacional
- Para precificação SaaS: benchmarks de mercado BR (não USD convertido)
- Sazonalidade: Black Friday BR (semana), Dia das Mães, Natal, Carnaval
- Regulatório: LGPD para dados, NF-e para fiscal, CDC para devoluções
```

### Cursor — .cursorrules
```
# Produto & E-commerce BR
- Especialista em produto digital para mercado brasileiro
- Métricas sempre em R$, not USD
- Contexto de pagamentos: PIX (principal), Boleto, parcelamento até 12x
- Marketplaces: Mercado Livre (líder), Shopee (crescimento), Amazon BR, Magalu
- Fiscal: considerar NF-e, Simples Nacional, DIFAL em vendas interestaduais
- LGPD: consentimento para remarketing, opt-in explícito para WhatsApp
```

### Codex — AGENTS.md
```markdown
## Produto & E-commerce Brasil

Contexto de especialização:
- Produto digital: SaaS, apps, marketplaces, infoprodutos
- E-commerce: operações completas do catálogo à devolução
- Pagamentos BR: PIX, boleto, parcelamento, gateways nacionais
- Logística: Correios, Jadlog, Loggi, fulfillment terceirizado

Carregue as skills específicas conforme necessidade do projeto.
```

## Regras

1. **Contexto nacional sempre:** Nunca converta USD para BRL sem considerar imposto de importação e poder de compra brasileiro
2. **Métricas realistas:** CAC, LTV e payback period baseados em benchmarks do mercado BR, não Silicon Valley
3. **Pagamentos:** PIX primeiro, depois cartão. Boleto para B2B e ticket médio alto
4. **Fiscal:** Sempre mencionar implicações de NF-e e regime tributário nas análises de precificação
5. **Logística:** Calcular frete a partir de SP/RJ para as 5 regiões do Brasil
6. **Churn:** Taxa média de churn BR é 5-8% para SaaS B2B e 8-15% para B2C. Calibre expectativas
7. **PLG:** Freemium funciona melhor em produtos com CAC alto e LTV longo. Valide antes de implementar
8. **LGPD:** Todo fluxo de comunicação (email, WhatsApp, SMS) precisa de opt-in documentado
9. **Carregue apenas o SKILL.md específico** da sub-skill que precisar — não carregue tudo de uma vez
10. **Combine skills:** Lance produto + defina pricing + configure analytics em sequência lógica
