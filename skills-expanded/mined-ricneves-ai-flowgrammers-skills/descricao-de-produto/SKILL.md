---
name: "descricao-de-produto"
description: |
  Cria descrições de produto de alta conversão para e-commerce e marketplaces
  brasileiros (Mercado Livre, Shopee, Amazon BR, VTEX). Inclui SEO de marketplace,
  título otimizado, bullet benefits e ficha técnica estruturada.
version: 1.0.0
license: MIT
tags:
  - produto
  - e-commerce
  - marketplace
  - mercado-livre
  - shopee
  - amazon-br
  - descricao
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read conteudo-copy/product-description/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/product-description.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Product Description

Especialista em descrições de produto para e-commerce e marketplaces brasileiros. Combina SEO de marketplace com copywriting de benefícios para maximizar visibilidade e conversão.

## Estrutura por Marketplace

### Mercado Livre
- Título: até 60 chars com palavra-chave principal
- Bullet points: 5-8 benefícios em linguagem de vantagem
- Descrição: 500-1.500 chars com keywords secundárias
- Ficha técnica: completa para algoritmo de busca

### Shopee
- Título: até 100 chars — inclua variações da palavra-chave
- Descrição: formato visual com emojis aceitos
- Destacar: tempo de envio, avaliações e política de devolução

### Loja própria (VTEX/Nuvemshop/Tray)
- Descrição longa: 300-600 palavras orientadas a benefícios
- Specs técnicas: separadas em aba/accordion
- SEO: meta title, meta description, alt text das imagens

## Exemplos de Uso

```
Use product-description e crie a descrição completa para um liquidificador
de 1.000W para venda no Mercado Livre. Destaque: motor de alta potência,
copo de aço inox, 10 velocidades, garantia de 2 anos. Preço: R$ 249,90.
Inclua título otimizado e 6 bullet points de benefício.
```

## Regras

1. Benefícios > Features — "Processa gelo em 5 segundos" > "Motor de 1.000W"
2. Sempre mencione garantia, prazo de entrega e política de troca
3. Use palavras-chave naturalmente — sem keyword stuffing no marketplace
4. Ficha técnica completa melhora posicionamento no algoritmo do ML e Shopee
5. Inclua variações de busca no título para capturar mais tráfego orgânico
