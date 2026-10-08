---
name: pt-social-contributions
description: "Utilize esta skill sempre que for solicitada a abordar contribuições para a Segurança Social de trabalhadores independentes em Portugal. Acione perante expressões como \"Segurança Social trabalhador independente\", \"contribuições independente Portugal\", \"declaração trimestral SS\", \"rendimento relevante\", ou qualquer questão sobre obrigações contributivas de um cliente trabalhador independente em Portugal. Abrange a taxa de 21,4% sobre o rendimento relevante (com coeficiente de 70% para serviços e 20% para comércio na Categoria B simplificada), a declaração trimestral, a isenção dos primeiros 12 meses e as escalas baseadas no IAS. LEIA SEMPRE esta skill antes de qualquer trabalho relativo a contribuições para a Segurança Social em Portugal. Trigger also on: \"Portuguese social contributions\", \"Segurança Social self-employed\", \"quarterly declaration Portugal\", \"IAS contribution base\", \"trabalhador independente rate\"."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: PT
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/pt-social-contributions"
  tax_year: 2025
  obligation: SSC
---

# Portugal — Segurança Social do Trabalhador Independente — Skill v2.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Secção 1 — Referência rápida

| Campo | Valor |
|---|---|
| País | Portugal (República Portuguesa) |
| Autoridade | DGSS (Direção-Geral da Segurança Social) / ISS (Instituto da Segurança Social) para contribuições; AT (Autoridade Tributária e Aduaneira) para impostos |
| Legislação principal | Código Contributivo (Lei n.º 110/2009, art. 139.º a 170.º) |
| Legislação complementar | Decreto Regulamentar n.º 1-A/2011; atualizações anuais por Portaria |
| Taxa do trabalhador independente | 21,4% |
| Taxa do empresário em nome individual | 25,2% |
| Rendimento relevante — serviços (coeficiente Categoria B) | 70% do bruto |
| Rendimento relevante — comércio/bens (coeficiente Categoria B) | 20% do bruto |
| IAS (Indexante dos Apoios Sociais), 2025 | €522,50 |
| Contribuição mínima mensal | €20,00 |
| Base máxima mensal (12 × IAS) | €6.270,00 |
| Primeiros 12 meses | Isenção de contribuições |
| Periodicidade da declaração | Trimestral |
| Periodicidade do pagamento | Mensal (entre o dia 10 e o dia 20) |
| Moeda | EUR apenas |
| Contribuidor | Open Accountants |
| Validado por | Pendente — requer validação por contabilista certificado português |
| Data de validação | Pendente |

---

## Secção 2 — Inputs obrigatórios e catálogo de recusas

### Inputs obrigatórios

Antes de qualquer cálculo, DEVE obter:

1. **Tipo de atividade** — trabalhador independente, empresário em nome individual ou profissional liberal?
2. **Rendimento bruto trimestral (rendimento relevante)** — proveniente da declaração trimestral.
3. **Ano de início de atividade** — primeiros 12 meses isentos de contribuições.
4. **Existe atividade por conta de outrem em simultâneo?** — pode aplicar-se taxa reduzida ou isenção.
5. **Categoria do rendimento** — prestação de serviços vs venda de bens (comércio)?
6. **O cliente tem contabilidade organizada?** — afeta o cálculo do rendimento relevante.

**Se o tipo de rendimento (serviços vs bens) for desconhecido, PARE. O coeficiente de rendimento relevante difere.**

### Catálogo de recusas

**R-PT-SOC-1 — Trabalhador transfronteiriço da UE.** Acionador: o cliente é residente em Portugal e presta serviços noutro Estado-Membro da UE. Mensagem: "A segurança social transfronteiriça exige análise do certificado A1 ao abrigo do Regulamento (CE) n.º 883/2004. Escalar para consultor qualificado."

**R-PT-SOC-2 — Taxas reduzidas para pensionistas.** Acionador: trabalhador independente pensionista pergunta sobre taxa contributiva reduzida. Mensagem: "As taxas contributivas para pensionistas requerem confirmação junto da Segurança Social (DGSS/ISS). Sinalizar para revisor."

### Proibições

- NUNCA aplicar 21,4% diretamente ao rendimento bruto — o coeficiente de rendimento relevante (70% para serviços, 20% para comércio) tem de ser aplicado primeiro.
- NUNCA esquecer a isenção dos primeiros 12 meses para novos trabalhadores independentes.
- NUNCA ignorar a contribuição mínima mensal de €20 — mesmo com rendimento zero, este mínimo aplica-se após o período de isenção.
- NUNCA confundir a taxa do trabalhador independente (21,4%) com a taxa do empresário em nome individual (25,2%).
- NUNCA apresentar o rendimento da declaração trimestral como base contributiva — tem de ser convertido para mensal.
- NUNCA esquecer de aplicar o limite máximo de 12 × IAS (€6.270,00 em 2025).
- NUNCA afirmar que as contribuições NÃO são dedutíveis fiscalmente — SÃO dedutíveis em sede de IRS.
- NUNCA aconselhar sobre a isenção por acumulação de atividade sem verificar o limiar de 4 × IAS.

---

## Secção 3 — Cálculo do rendimento relevante

**Legislação:** Código Contributivo, art. 162.º

### Sem contabilidade organizada (Categoria B simplificada)

| Tipo de rendimento | % de rendimento relevante |
|---|---|
| Prestação de serviços | 70% do bruto |
| Produção e venda de bens (comércio) | 20% do bruto |
| Misto (serviços + bens) | Aplicar cada % à respetiva categoria |

### Com contabilidade organizada

Rendimento relevante = lucro líquido efetivo apurado pelos registos contabilísticos.

### Conversão de trimestral para mensal

```
rendimento_relevante_trimestral = soma do rendimento relevante dos 3 meses do trimestre
rendimento_relevante_mensal = rendimento_relevante_trimestral / 3
```

---

## Secção 4 — Taxas, base contributiva e limites (2025)

**Legislação:** Código Contributivo, art. 163.º e 168.º

### Taxas contributivas (TSU — Taxa Social Única)

| Categoria | Taxa |
|---|---|
| Trabalhador independente | 21,4% |
| Trabalhador independente — primeiros 12 meses (isenção total) | 0% (alternativamente 15% em regimes específicos) |
| Empresário em nome individual (com trabalhadores) | 25,2% |

### Limites da base contributiva

| Limite | Montante |
|---|---|
| Contribuição mínima mensal | €20,00 |
| Base máxima mensal (12 × IAS) | €6.270,00 |
| IAS de referência (2025) | €522,50 |

```
base_mensal = min(rendimento_relevante_mensal, 6.270,00)
contribuição_mensal = max(20,00, base_mensal × 21,4%)
```

### Escalões de base contributiva

A base contributiva é determinada por escalões indexados ao IAS, revistos **trimestralmente** com base no rendimento relevante apurado nos três meses anteriores. A Segurança Social comunica o escalão aplicável após cada declaração trimestral.

---

## Secção 5 — Etapas de cálculo

### Etapa 5.1 — Declaração trimestral

| Período da declaração | Período de rendimento abrangido | Prazo de entrega |
|---|---|---|
| Janeiro | Out–Dez (ano anterior) | Final de janeiro |
| Abril | Jan–Mar | Final de abril |
| Julho | Abr–Jun | Final de julho |
| Outubro | Jul–Set | Final de outubro |

### Etapa 5.2 — Calcular o rendimento relevante mensal

```
SE apenas_serviços (sem contabilidade organizada):
    rendimento_relevante = bruto_trimestral × 70% / 3
SENÃO SE apenas_bens:
    rendimento_relevante = bruto_trimestral × 20% / 3
SENÃO SE misto:
    rendimento_relevante = (bruto_serviços × 70% + bruto_bens × 20%) / 3
SENÃO SE contabilidade_organizada:
    rendimento_relevante = lucro_líquido_trimestral / 3
```

### Etapa 5.3 — Aplicar limites e calcular

```
base_mensal = min(rendimento_relevante, 6.270,00)
contribuição_mensal = max(20,00, base_mensal × 21,4%)
```

### Etapa 5.4 — As contribuições aplicam-se ao trimestre seguinte

A declaração trimestral determina as contribuições devidas nos 3 meses subsequentes. A base contributiva é, assim, revista **trimestralmente**.

---

## Secção 6 — Calendário de pagamentos, isenções e dedutibilidade fiscal

### Calendário de pagamentos

| Obrigação | Prazo |
|---|---|
| Pagamento mensal da contribuição | Entre o dia 10 e o dia 20 de cada mês |
| Meios de pagamento | Débito direto, Multibanco ou portal da Segurança Social Direta |

Atraso no pagamento: juros à taxa legal e potencial perda de prestações sociais.

### Isenções

**Primeiros 12 meses:** os novos trabalhadores independentes estão isentos de contribuições durante os primeiros 12 meses de atividade. Em determinados regimes transitórios, pode aplicar-se uma taxa reduzida de 15% em vez da isenção total — confirmar com o ISS.

**Isenção por acumulação com trabalho dependente:** se o trabalhador independente exercer também atividade por conta de outrem e o empregador descontar pelo menos sobre a base contributiva mínima:
- Se o rendimento por conta de outrem ≥ IAS: as contribuições do trabalhador independente podem ser reduzidas ou isentas.
- Se o rendimento como trabalhador independente ≥ 4 × IAS (€2.090,00 em 2025): a isenção NÃO se aplica.

### Dedutibilidade fiscal

| Questão | Resposta |
|---|---|
| As contribuições para a Segurança Social são dedutíveis? | SIM — ao rendimento bruto em sede de IRS |
| Classificação | Deduções da Categoria B |
| Quando são dedutíveis? | No ano em que são pagas |

---

## Secção 7 — Contabilidade organizada e recibos verdes

### Trabalhador independente com contabilidade organizada

Rendimento relevante = lucro líquido efetivo (e não o coeficiente presumido). Se o lucro líquido for negativo, aplica-se igualmente a contribuição mínima de €20. Confirmar a metodologia de apuramento do lucro com o contabilista certificado. Sinalizar para revisor.

### Rendimentos por recibos verdes

Estes rendimentos SÃO rendimentos de trabalhador independente. Aplica-se a regra-padrão do coeficiente de 70% do rendimento relevante. Todos os montantes faturados em recibos verdes são reportados na declaração trimestral.

---

## Secção 8 — Registo de casos-limite

### EC1 — Primeiro ano de atividade
**Situação:** O cliente abriu atividade em março de 2025.
**Resolução:** Isento de contribuições até fevereiro de 2026 (12 meses). Primeira declaração trimestral devida em abril de 2026. As contribuições começam a partir do mês seguinte à primeira declaração.

### EC2 — Rendimento de serviços abaixo da contribuição mínima
**Situação:** O cliente presta serviços com rendimento bruto trimestral de €1.000.
**Resolução:** Rendimento relevante = €1.000 × 70% / 3 = €233,33/mês. Contribuição calculada = €233,33 × 21,4% = €49,93/mês (acima do mínimo de €20).

### EC3 — Rendimento muito elevado
**Situação:** O cliente aufere €30.000/trimestre em serviços.
**Resolução:** Rendimento relevante = €7.000/mês. Limitado a €6.270,00 (12 × IAS). Contribuição mensal = €6.270,00 × 21,4% = €1.341,78.

### EC4 — Misto de serviços e bens
**Situação:** O cliente aufere €6.000 de serviços e €15.000 de bens no trimestre.
**Resolução:** Rendimento relevante = (€6.000 × 70% + €15.000 × 20%) / 3 = €2.400/mês. Contribuição = €2.400 × 21,4% = €513,60.

### EC5 — Acumulação com trabalho dependente, isenção aplicável
**Situação:** Cliente com vencimento de €1.200/mês por conta de outrem e prestação de serviços trimestral de €2.000 como independente.
**Resolução:** Rendimento relevante como independente = €466,67/mês (inferior a 4 × IAS). Aplica-se a isenção por acumulação. Contribuições = €0.

---

## Secção 9 — Protocolo de escalonamento para revisor

Quando uma situação exige juízo do revisor:

```
SINALIZAÇÃO PARA REVISOR
Nível: T2
Cliente: [nome]
Situação: [descrição]
Questão: [o que é ambíguo]
Opções: [tratamentos possíveis]
Recomendação: [tratamento mais provavelmente correto e fundamentação]
Ação requerida: Contabilista certificado qualificado deve confirmar antes de aconselhar o cliente.
```

Quando uma situação está fora do âmbito da skill:

```
ESCALONAMENTO NECESSÁRIO
Nível: T3
Cliente: [nome]
Situação: [descrição]
Questão: [fora do âmbito da skill]
Ação requerida: Não aconselhar. Encaminhar para contabilista certificado qualificado. Documentar a lacuna.
```

---

## Secção 10 — Bateria de testes

### Teste 1 — Serviços padrão, escalão intermédio
**Input:** Bruto trimestral de serviços €9.000, sem trabalho dependente, atividade já estabelecida.
**Output esperado:** Rendimento relevante = €2.100/mês. Contribuição = €449,40/mês. Anual: €5.392,80.

### Teste 2 — Aplicação da contribuição mínima
**Input:** Bruto trimestral de serviços €1.500.
**Output esperado:** Rendimento relevante = €350/mês. Contribuição calculada = €350 × 21,4% = €74,90/mês (acima do mínimo de €20).

### Teste 3 — Aplicação da base máxima
**Input:** Bruto trimestral de serviços €30.000.
**Output esperado:** Rendimento relevante = €7.000/mês. Limitado a €6.270,00. Contribuição = €1.341,78/mês.

### Teste 4 — Primeiro ano isento
**Input:** Atividade aberta há 4 meses, bruto trimestral €12.000.
**Output esperado:** Isento (dentro dos primeiros 12 meses). Contribuições = €0.

### Teste 5 — Rendimento apenas de comércio (bens)
**Input:** Bruto trimestral de venda de bens €20.000, sem trabalho dependente.
**Output esperado:** Rendimento relevante = €1.333,33/mês. Contribuição = €285,33/mês.

### Teste 6 — Acumulação com trabalho dependente, isenção aplicável
**Input:** Vencimento por conta de outrem €1.500/mês, prestação de serviços trimestral €2.000 como independente.
**Output esperado:** Rendimento relevante como independente = €466,67/mês (inferior a 4 × IAS). Aplica-se isenção. Contribuições = €0.

### Teste 7 — Empresário em nome individual
**Input:** Empresário em nome individual com trabalhadores, serviços trimestrais €15.000.
**Output esperado:** Taxa = 25,2%. Rendimento relevante = €3.500/mês. Contribuição = €882,00/mês.

---

## Aviso legal

Esta skill e os respetivos outputs são fornecidos apenas para fins informativos e de cálculo, não constituindo aconselhamento fiscal, jurídico ou financeiro. A Open Accountants e os seus contribuidores não aceitam qualquer responsabilidade por erros, omissões ou consequências decorrentes da utilização desta skill. Todos os outputs devem ser revistos e validados por um profissional qualificado (contabilista certificado, revisor oficial de contas, advogado fiscalista ou equivalente licenciado na jurisdição aplicável) antes de qualquer entrega ou ato baseado nos mesmos.

A versão mais atualizada e verificada desta skill é mantida em [openaccountants.com](https://openaccountants.com). Inicie sessão para aceder à versão mais recente, solicitar revisão profissional por um contabilista licenciado e acompanhar atualizações à medida que a legislação fiscal evolui.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/pt-social-contributions) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
