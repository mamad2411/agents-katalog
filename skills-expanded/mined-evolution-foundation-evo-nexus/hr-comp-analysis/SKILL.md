---
name: hr-comp-analysis
description: Analisa remuneração — benchmarking, posicionamento em faixas e modelagem de equity. Use quando precisar saber quanto pagar por um cargo, avaliar se uma oferta é competitiva, modelar uma concessão de equity, ou identificar outliers e riscos de retenção no time. Gatilhos: "quanto pagar a um [cargo]", "essa oferta é competitiva", "benchmark salarial".
argument-hint: "<cargo, nível ou dataset de remuneração>"
---

# HR — Comp Analysis

Analise dados de remuneração para benchmarking, posicionamento em faixas e planejamento. Ajuda a comparar remuneração com o mercado para contratações, retenção e planejamento de equity.

## O Que Preciso Saber

**Opção A: Análise de cargo único**
"Quanto pagar a um Engenheiro de Software Sênior em BH?"

**Opção B: Upload de dados de remuneração**
Faça upload de um CSV ou cole suas faixas salariais. Analisarei posicionamento, identificarei outliers e compararei com o mercado.

**Opção C: Modelagem de equity**
"Modele uma concessão de 5% de participação com cliff de 1 ano e vesting de 4 anos."

## Framework de Remuneração

### Componentes da Remuneração Total

#### Regime CLT
- **Salário base**: Remuneração mensal bruta
- **Benefícios obrigatórios**: FGTS (8%), férias + 1/3, 13° salário, INSS (variável por faixa)
- **Benefícios opcionais**: VR/VA, plano de saúde, PLR, VT ou ajuda de custo home office
- **Equity**: Participação societária (opções/phantom shares — menos comum em BR)
- **Bônus**: Participação nos Lucros e Resultados (PLR), conforme acordo coletivo ou individual

#### Regime PJ
- **Valor hora/projeto**: Negociado livremente
- **Nota fiscal**: Emitida pelo prestador
- **Benefícios**: Não há obrigatoriedade — negociados como valor bruto total
- **Custo empresa**: Sem encargos trabalhistas, mas com risco de vínculo empregatício se mal estruturado

### Variáveis-Chave
- **Cargo**: Função e especialização (backend, frontend, DevOps, PM, etc.)
- **Nível**: Júnior, Pleno, Sênior, Especialista, Líder
- **Localização**: BR (BH, SP, RJ) vs. remoto global — impacta referências
- **Estágio da empresa**: Startup early-stage vs. scale-up — equity mais relevante nos primeiros
- **Setor**: Tech/open source vs. enterprise — benchmarks diferentes

### Fontes de Dados
- **Pesquisa web**: Glassdoor BR, Levels.fyi (tech), pesquisas GPTW, Gupy/LinkedIn Salary Insights
- **Dados do usuário**: CSVs ou faixas fornecidas pelo Davidson
- Sempre indicar data e limitações da fonte

## Output

```markdown
## Análise de Remuneração: [Cargo/Escopo]
**Data:** [Data] | **Mercado de Referência:** [BR / Global / Remoto]

### Benchmarks de Mercado
| Percentil | Salário Base (CLT) | Equivalente PJ* | Total CLT (c/ encargos) |
|----------|-------------------|-----------------|------------------------|
| P25 | R$ [X]/mês | R$ [X]/mês | R$ [X]/mês |
| P50 | R$ [X]/mês | R$ [X]/mês | R$ [X]/mês |
| P75 | R$ [X]/mês | R$ [X]/mês | R$ [X]/mês |
| P90 | R$ [X]/mês | R$ [X]/mês | R$ [X]/mês |

*Estimativa PJ = CLT base ÷ 0,65 (compensa ausência de férias, 13°, FGTS)

**Fontes:** [Glassdoor BR, Levels.fyi, pesquisa web, dados fornecidos]
**Cuidado:** Dados podem ter defasagem de 6-12 meses. Valide com candidatos reais.

### Análise de Faixas (se dados fornecidos)
| Colaborador | Salário Atual | Mínimo da Faixa | Meio da Faixa | Máximo da Faixa | Posição |
|-------------|--------------|----------------|--------------|----------------|---------|
| [Nome] | R$ [X] | R$ [X] | R$ [X] | R$ [X] | [Abaixo/Na/Acima] |

### Modelagem de Equity
| Parâmetro | Valor |
|-----------|-------|
| Tipo | [Opções / Phantom Shares / Participação direta] |
| % concedido | [X]% |
| Cliff | [X meses] |
| Vesting | [X anos, linear/cliff] |
| Valuation de referência | R$ [X] (se disponível) |
| Valor estimado no P50 exit | R$ [X] |

### Custo Total para a Empresa
| Regime | Custo Mensal | Custo Anual |
|--------|-------------|-------------|
| CLT | R$ [X] (base + ~75% encargos e benefícios) | R$ [X] |
| PJ | R$ [X] (valor NF) | R$ [X] |

### Recomendações
- [Recomendações específicas de remuneração]
- [Considerações de equity se aplicável]
- [Riscos de retenção se identificados]
- [Posicionamento sugerido — abaixo/no/acima do mercado e por quê]
```

## Dicas

1. **Localização importa** — BH costuma ter custo ~15-25% abaixo de SP para tech. Remoto global pode demandar benchmarks em USD.
2. **Remuneração total, não só base** — Para CLT, inclua benefícios e encargos. Para PJ, compare o bruto recebido.
3. **Multiplier PJ** — Regra prática: valor PJ ≈ CLT bruto ÷ 0,65 para equivalência líquida.
4. **Confidencialidade** — Dados de remuneração são sensíveis. Resultados ficam na conversa.
5. **Equity em startup BR** — Phantom shares evitam complexidade societária. Consultar Thaís ou Vitor para estrutura legal adequada.
6. **PLR CLT** — Participação nos Resultados é negociada e não incide FGTS/INSS se bem estruturada. Consultar Samara.
