---
name: "dre-balanco"
description: |
  Analisa e elabora DRE (Demonstração do Resultado do Exercício) e balanço
  patrimonial no padrão contábil brasileiro (CPC/IFRS). Identifica tendências,
  calcula indicadores-chave e explica os resultados em linguagem acessível.
version: 1.0.0
license: MIT
tags:
  - dre
  - balanco
  - contabilidade
  - resultado
  - ebitda
  - margem
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/dre-balanco/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/dre-balanco.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# DRE & Balanço

Especialista em análise e interpretação de demonstrações financeiras no padrão brasileiro. Transforma números em insights acionáveis.

## Indicadores Calculados

- **Margem Bruta** — Receita Líquida - CMV / Receita Líquida
- **EBITDA e Margem EBITDA** — Resultado antes de juros, impostos, depreciação e amortização
- **Margem Líquida** — Lucro Líquido / Receita Líquida
- **ROE** — Retorno sobre Patrimônio Líquido
- **ROA** — Retorno sobre Ativos
- **Liquidez Corrente** — Ativo Circulante / Passivo Circulante

## Exemplos de Uso

```
Use dre-balanco para analisar os dados financeiros da minha empresa:
Receita Bruta: R$ 2,4M | Deduções: R$ 180k | CMV: R$ 840k
Despesas Operacionais: R$ 720k | Depreciação: R$ 60k | Despesas Financeiras: R$ 48k
IR/CSLL: R$ 92k | Ativo Total: R$ 3,2M | PL: R$ 1,1M
Calcule todos os indicadores e compare com benchmarks do setor de distribuição.
```

## Regras

1. DRE pelo regime de competência — reconhece receita quando faturada, não quando recebida
2. EBITDA não é fluxo de caixa — esclarecer essa diferença para gestores não financeiros
3. Comparar sempre com período anterior E com benchmark do setor
4. Resultados de empresas no Simples Nacional têm tratamento contábil específico
5. Aviso: para fins fiscais e societários, a análise deve ser revisada pelo contador da empresa
