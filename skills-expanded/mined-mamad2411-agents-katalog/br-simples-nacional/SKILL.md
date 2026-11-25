---
name: br-simples-nacional
description: "> [PT-BR] Use esta skill sempre que for solicitado tratar do Simples Nacional brasileiro ou do regime MEI. Acione com expressões como \"Simples Nacional\", \"MEI\", \"microempreendedor individual\", \"DAS\", \"DASN-SIMEI\", \"anexo Simples\", \"tabela do Simples\", \"Fator R\", ou qualquer dúvida sobre o regime unificado de tributação para micro e pequenas empresas no Brasil. Cobre o DAS mensal fixo do MEI, as tabelas progressivas do Simples Nacional (Anexos I-V), os limites de faturamento, o Fator R, as declarações anuais e a interação com a Reforma Tributária 2026 (CBS/IBS). SEMPRE leia esta skill antes de tocar em qualquer trabalho de Simples Nacional ou MEI no Brasil. — [EN] Use this skill whenever asked about the Brazilian Simples Nacional or MEI regime. Triggers include \"Simples Nacional\", \"MEI\", \"DAS\", \"DASN-SIMEI\", \"Anexo Simples\", \"Fator R\", and any question on the unified tax regime for Brazilian micro and small businesses."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: BR
  category: international
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/br-simples-nacional"
  tax_year: 2025
  obligation: OTHER
  reviewed_by: "pending depends_on: - income-tax-workflow-base"
---

# Brasil — Simples Nacional — Skill v2.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Seção 1 — Referência rápida

| Campo | Valor |
|---|---|
| País | Brasil |
| Tributo | Tributo unificado do Simples Nacional (DAS) que engloba IRPJ, CSLL, PIS, COFINS, CPP, ICMS, ISS, IPI |
| Moeda | Apenas BRL |
| Ano-base | Ano-calendário |
| Legislação principal | Lei Complementar 123/2006 (Estatuto Nacional da Microempresa) |
| Legislação complementar | Resoluções CGSN; LC 155/2016; EC 132/2023; LC 214/2025; LC 227/2026 |
| Autoridade fiscal | Receita Federal do Brasil (RFB); Comitê Gestor do Simples Nacional (CGSN) |
| Portal de entrega | Portal do Simples Nacional (www8.receita.fazenda.gov.br/SimplesNacional) |
| Prazo de entrega | DAS até o dia 20 do mês seguinte; DEFIS até 31 de março; DASN-SIMEI até 31 de maio |
| Colaborador | Open Accountants Community |
| Validação | Pendente — exige assinatura de contador brasileiro (registrado no CRC) |
| Versão da skill | 2.1 |

### Limites de faturamento

| Categoria | Faturamento anual máximo |
|---|---|
| MEI | R$ 81.000 (TBC — há propostas para elevar a R$ 144.913,41 ainda não promulgadas) |
| Microempresa (ME) | R$ 360.000 |
| Empresa de Pequeno Porte (EPP) | R$ 4.800.000 |
| Sublimite ICMS/ISS | R$ 3.600.000 |

### DAS-MEI mensal (2025)

| Atividade | INSS (5% do salário mínimo) | ICMS | ISS | Total |
|---|---|---|---|---|
| Comércio/Indústria | R$ 75,90 | R$ 1,00 | -- | R$ 76,90 |
| Serviços | R$ 75,90 | -- | R$ 5,00 | R$ 80,90 |
| Comércio + Serviços | R$ 75,90 | R$ 1,00 | R$ 5,00 | R$ 81,90 |

Baseado no salário mínimo de R$ 1.518,00 vigente em 2025.

### Fórmula da alíquota efetiva

Alíquota Efetiva = (RBT12 x Alíquota Nominal - Parcela a Deduzir) / RBT12

### Defaults conservadores

| Ambiguidade | Default |
|---|---|
| Tipo de entidade desconhecido | ME (não MEI — mais conservador) |
| CNAE desconhecido | Anexo V (alíquotas mais altas) |
| Folha desconhecida para Fator R | Fator R < 28% (permanece no Anexo V) |
| Faixa de faturamento desconhecida | Faixa mais alta aplicável |

---

## Seção 2 — Insumos obrigatórios e catálogo de recusas

### Insumos obrigatórios

**Mínimo viável** — tipo de entidade (MEI/ME/EPP), receita bruta dos últimos 12 meses (RBT12), tipo de atividade (CNAE), receita do mês corrente.

**Recomendado** — folha de salários (para o Fator R), unidade da federação de registro, histórico de pagamentos do DAS.

**Ideal** — dados completos do PGDAS-D, receita segregada por atividade, confirmação da classificação por Anexo, DEFIS do exercício anterior.

### Catálogo de recusas

**R-BR-S1 — Transição por exclusão.** "Receita superior a R$ 4.800.000. O cliente está excluído do Simples Nacional. Deve migrar para Lucro Presumido ou Lucro Real. Escalar para contador qualificado."

**R-BR-S2 — Lucro Presumido / Lucro Real.** "Esta skill cobre apenas o Simples Nacional e o MEI. Os demais regimes possuem métodos de apuração distintos."

**R-BR-S3 — Regras estaduais específicas de ICMS.** "Regras estaduais detalhadas de ICMS para empresas acima do sublimite exigem conhecimento estadual específico. Escalar."

**R-BR-S4 — Regime híbrido CBS/IBS com creditamento.** "A opção pelo regime híbrido do art. 21-A da LC 123/06 (introduzido pela LC 214/2025) exige análise da composição da clientela B2B versus B2C e simulação de impacto. Escalar para contador para decisão definitiva."

---

## Seção 3 — Biblioteca de padrões de transações

### 3.1 Padrões de receita

| Padrão | Tratamento | Notas |
|---|---|---|
| VENDA, RECEITA, PIX RECEBIDO | Incluir no RBT12 | Receita bruta para definição de faixa |
| NF-E EMITIDA, NFS-E EMITIDA | Incluir no RBT12 | Receita por emissão de nota fiscal |
| MERCADO LIVRE, MARKETPLACE | Incluir no RBT12 | Vendas em plataformas |
| EXPORTAÇÃO | Incluir no RBT12 | O teste de limite inclui exportações |
| DEVOLUÇÃO, CANCELAMENTO | Deduzir da receita | Reduz a receita bruta |
| TRANSFERÊNCIA PRÓPRIA | EXCLUIR | Movimentação interna |

### 3.2 Padrões de pagamento de tributos

| Padrão | Tratamento | Notas |
|---|---|---|
| DAS, SIMPLES NACIONAL | Pagamento unificado | Engloba todos os tributos |
| DAS-MEI, DASN | Pagamento fixo do MEI | Valor fixo mensal |
| ICMS FORA SIMPLES | ICMS apartado | Acima do sublimite ou ICMS-ST |
| ISS FORA SIMPLES | ISS apartado | Acima do sublimite |
| INSS PATRONAL | INSS patronal apartado | Apenas Anexo IV |
| CBS/IBS APARTADO (2026+) | Recolhimento separado fora do DAS | Apenas no regime híbrido do art. 21-A LC 123/06 |

### 3.3 Padrões de definição de Anexo

| Atividade CNAE | Anexo típico | Notas |
|---|---|---|
| Comércio, varejo | Anexo I | Venda de mercadorias |
| Indústria, manufatura | Anexo II | Inclui IPI |
| Serviços gerais, manutenção | Anexo III | Verificar Fator R para atividades do V |
| Limpeza, segurança, construção | Anexo IV | Sem CPP no DAS |
| Consultoria em TI, serviços profissionais | Anexo V (ou III se Fator R >= 28%) | Fator R é crítico |

---

## Seção 4 — Exemplos resolvidos

### Exemplo 1 — DAS mensal do MEI (Serviços)

**Entrada:** MEI prestando serviços de TI. Salário mínimo R$ 1.518.

**Cálculo:**
- INSS: 5% x 1.518 = R$ 75,90
- ISS: R$ 5,00
- Total DAS: R$ 80,90/mês

### Exemplo 2 — Simples Nacional, Anexo I Comércio

**Entrada:** RBT12 = R$ 500.000. Receita do mês = R$ 45.000.

**Cálculo:**
- Faixa 3 (360.001 a 720.000)
- Alíquota efetiva = (500.000 x 9,50% - 13.860) / 500.000 = 6,728%
- DAS = 45.000 x 6,728% = R$ 3.027,60

### Exemplo 3 — Anexo V com Fator R >= 28%

**Entrada:** Empresa de consultoria, RBT12 = R$ 400.000. Folha dos últimos 12 meses = R$ 130.000.

**Cálculo:**
- Fator R = 130.000 / 400.000 = 32,5% (>= 28%)
- Aplica-se Anexo III em vez do V
- Faixa 3: alíquota efetiva = (400.000 x 13,50% - 17.640) / 400.000 = 9,09%

### Exemplo 4 — Excesso de receita no MEI (dentro de 20%)

**Entrada:** MEI com receita anual de R$ 90.000 (11,1% acima do limite).

**Classificação:**
- Excesso = R$ 9.000
- DAS complementar sobre o excesso pelas alíquotas do Simples ME
- Migração para ME a partir de janeiro do ano seguinte

---

## Seção 5 — Regras de Tier 1 (quando os dados são claros)

### 5.1 Elegibilidade do MEI

**Legislação:** LC 123/2006, Arts. 18-A a 18-E

Receita anual máxima R$ 81.000. Máximo de 1 empregado. Vedado a profissões regulamentadas. Vedado a sócio de outra empresa. Vedado ter filiais.

### 5.2 Anexos do Simples Nacional

**Legislação:** LC 123/2006, Anexos I-V (com redação dada pela LC 155/2016)

Anexo I: Comércio (4,00% -- 19,00%). Anexo II: Indústria (4,50% -- 30,00%). Anexo III: Serviços I (6,00% -- 33,00%). Anexo IV: Serviços II — limpeza/segurança/construção (4,50% -- 33,00%, sem CPP no DAS). Anexo V: Serviços profissionais (15,50% -- 30,50%).

### 5.3 Regra do Fator R

**Legislação:** LC 123/2006, Art. 18, § 5º-J

Para atividades do Anexo V, se o Fator R (razão folha/receita dos últimos 12 meses) >= 28%, a atividade passa a ser tributada pelo Anexo III.

### 5.4 Sublimite de ICMS/ISS

Se a receita ultrapassar R$ 3.600.000 mas permanecer abaixo de R$ 4.800.000: os tributos federais continuam no DAS do Simples, mas ICMS e ISS são recolhidos FORA do Simples às alíquotas normais estaduais/municipais.

### 5.5 Regra especial do Anexo IV

O Anexo IV NÃO inclui a CPP (INSS patronal) no DAS. O INSS patronal deve ser recolhido em separado (20% sobre a folha).

---

## Seção 6 — Catálogo Tier 2 (exige julgamento do revisor)

### 6.1 Cálculo do Fator R

Exige dados precisos de folha, incluindo pró-labore, salários, FGTS, INSS e 13º salário. Sinalizar para o revisor.

### 6.2 Atividades em múltiplos Anexos

A receita deve ser segregada por atividade. A receita de cada atividade é tributada pelo respectivo Anexo, mas o RBT12 para definição de faixa é a receita TOTAL. Sinalizar para o revisor.

### 6.3 Sublimite ultrapassado

Receita acima de R$ 3.600.000: aumento significativo de complexidade. Sinalizar para contador.

### 6.4 MEI próximo do teto

Receita próxima de R$ 81.000: se ultrapassar em mais de 20%, o MEI é convertido retroativamente em ME a partir de janeiro. Deve contratar contador.

### 6.5 Decisão entre Simples cheio e regime híbrido CBS/IBS (a partir de 2026)

Sinalizar para o revisor sempre que o cliente tiver clientela predominantemente B2B com interesse no creditamento de CBS/IBS. A opção pelo art. 21-A da LC 123/06 implica recolhimento apartado de CBS+IBS e exige simulação comparativa.

---

## Seção — Simples Nacional e a Reforma Tributária 2026

### Marco legal

- **EC 132/2023** — Emenda Constitucional que institui o IVA dual brasileiro (CBS federal + IBS subnacional) e extingue gradualmente PIS, COFINS, ICMS e ISS.
- **LC 214/2025** — Lei Complementar que regulamenta a CBS e o IBS, define fato gerador, base de cálculo, não cumulatividade plena, regimes específicos e a opção do art. 21-A da LC 123/06 para optantes do Simples Nacional.
- **LC 227/2026** — Segunda fase da regulamentação, em vigor a partir de janeiro de 2026, com início efetivo da cobrança simbólica.

### MEI permanece isento

O **MEI permanece isento** de IBS/CBS. Continua recolhendo seus tributos via **DAS-MEI**, que unifica INSS + ISS/ICMS no valor fixo mensal. Não há qualquer alteração estrutural para o MEI em 2026 e não há repasse de créditos de IBS/CBS aos seus clientes.

### Simples Nacional (ME/EPP) — duas opções a partir de 2026

O **Simples Nacional para ME e EPP continua existindo**. Em 2026, o optante pode escolher entre dois caminhos:

**(a) Permanecer integralmente no Simples (caminho padrão).** O DAS continua a ser o recolhimento único. IBS e CBS já estão embutidos no DAS, **sem créditos transferíveis aos clientes**. É a opção mais simples administrativamente e adequada a clientelas predominantemente B2C ou compostas por outros optantes do Simples.

**(b) Regime híbrido (opção do art. 21-A da LC 123/06, introduzido pela LC 214/2025).** O contribuinte recolhe **CBS e IBS separadamente, fora do DAS**, pelas regras gerais do IVA dual, **permitindo a transferência de créditos aos adquirentes**. Os demais tributos do Simples (IRPJ, CSLL, PIS/COFINS residuais, CPP, ICMS/ISS quando aplicáveis) continuam no DAS. É vantajoso para EPP que vende a empresas B2B do Lucro Real/Presumido interessadas em apropriar créditos integrais.

### Período de teste em 2026

2026 é **ano de teste** com alíquotas simbólicas: **CBS 0,9% + IBS 0,1%** nas notas fiscais. As **multas estão suspensas pelos 3 primeiros meses** após a regulamentação, permitindo adaptação operacional sem penalização imediata por erros formais.

### Decisão híbrido vs Simples cheio

A escolha entre o regime híbrido e o Simples cheio depende essencialmente da **composição da clientela**:

| Perfil do cliente | Recomendação inicial |
|---|---|
| Predominantemente B2C ou Simples/MEI | Permanecer no Simples cheio |
| Predominantemente B2B (Lucro Real/Presumido) que exige créditos | Avaliar regime híbrido do art. 21-A |
| Misto | Simulação comparativa obrigatória |

**Sinalizar para revisor (R-BR-S4)** toda decisão pelo regime híbrido. A escolha é anual e tem impacto direto sobre a precificação, a competitividade B2B e a carga administrativa.

---

## Seção 7 — Modelo de papel de trabalho em Excel

```
BRASIL SIMPLES NACIONAL -- Papel de Trabalho
Período: [Mês]

A. RECEITA
  A1. RBT12 (receita bruta, últimos 12 meses)       ___________
  A2. Receita do mês corrente                        ___________
  A3. Tipo de atividade / CNAE                       ___________
  A4. Anexo aplicável                                ___________

B. APURAÇÃO DA ALÍQUOTA
  B1. Faixa de receita                               ___________
  B2. Alíquota nominal                               ___________
  B3. Parcela a deduzir                              ___________
  B4. Alíquota efetiva = (A1 x B2 - B3) / A1         ___________

C. APURAÇÃO DO DAS
  C1. DAS = A2 x B4                                  ___________

D. FATOR R (se atividade do Anexo V)
  D1. Folha total (últimos 12 meses)                 ___________
  D2. Fator R = D1 / A1                              ___________
  D3. >= 28%? Se sim, aplicar Anexo III              ___________

E. CBS/IBS 2026 (se aplicável)
  E1. Opção pelo art. 21-A LC 123/06? (S/N)          ___________
  E2. CBS apartada (0,9% em 2026)                    ___________
  E3. IBS apartado (0,1% em 2026)                    ___________

SINALIZAÇÕES AO REVISOR:
  [ ] Tipo de entidade confirmado (MEI/ME/EPP)?
  [ ] CNAE verificado para seleção do Anexo?
  [ ] Fator R calculado (se Anexo V)?
  [ ] Verificação de sublimite (R$ 3.600.000)?
  [ ] Verificação de exclusão (R$ 4.800.000)?
  [ ] Decisão híbrido vs Simples cheio (2026+)?
```

---

## Seção 8 — Guia de leitura de extratos bancários

### Formatos de extratos bancários brasileiros

| Banco | Formato | Campos-chave |
|---|---|---|
| Banco do Brasil, Caixa, Itaú | CSV, PDF, OFX | Data, Histórico, Valor, Saldo |
| Bradesco, Santander | CSV, PDF | Data, Descrição, Débito, Crédito |
| Nubank, Inter, C6 | CSV | Data, Descrição, Valor |

### Termos-chave

| Termo | Indicação |
|---|---|
| PIX RECEBIDO | Receita — incluir no faturamento |
| DAS, SIMPLES | Pagamento de tributo |
| PGDAS-D | Sistema de apuração do Simples |
| DASN-SIMEI | Declaração anual do MEI |
| DEFIS | Declaração anual do Simples |
| CBS, IBS | Tributos do IVA dual (a partir de 2026) |

---

## Seção 9 — Roteiro de onboarding (fallback)

```
PERGUNTAS DE ONBOARDING -- BRASIL SIMPLES NACIONAL
1. Tipo de entidade: MEI, ME ou EPP?
2. Receita bruta nos últimos 12 meses (RBT12)?
3. Código(s) CNAE?
4. Folha de salários — últimos 12 meses?
5. Estado de registro?
6. Se MEI: próximo do teto de R$ 81.000?
7. Possui atividades em múltiplos Anexos?
8. DEFIS ou DASN-SIMEI do ano anterior disponível?
9. Há produtos com ICMS-ST?
10. Possui empregados?
11. (2026+) Composição da clientela: B2B ou B2C?
12. (2026+) Pretende optar pelo regime híbrido do art. 21-A LC 123/06?
```

---

## Seção 10 — Material de referência

### Tabelas dos Anexos (completas)

**Anexo I — Comércio:** Faixa 1: 4,00% (até 180K). Faixa 2: 7,30% (180-360K, ded. 5.940). Faixa 3: 9,50% (360-720K, ded. 13.860). Faixa 4: 10,70% (720K-1,8M, ded. 22.500). Faixa 5: 14,30% (1,8-3,6M, ded. 87.300). Faixa 6: 19,00% (3,6-4,8M, ded. 378.000).

**Anexo II — Indústria:** Faixa 1: 4,50%. Faixa 2: 7,80% (ded. 5.940). Faixa 3: 10,00% (ded. 13.860). Faixa 4: 11,20% (ded. 22.500). Faixa 5: 14,70% (ded. 85.500). Faixa 6: 30,00% (ded. 720.000).

**Anexo III — Serviços I:** Faixa 1: 6,00%. Faixa 2: 11,20% (ded. 9.360). Faixa 3: 13,50% (ded. 17.640). Faixa 4: 16,00% (ded. 35.640). Faixa 5: 21,00% (ded. 125.640). Faixa 6: 33,00% (ded. 648.000).

**Anexo IV — Serviços II:** Faixa 1: 4,50%. Faixa 2: 9,00% (ded. 8.100). Faixa 3: 10,20% (ded. 12.420). Faixa 4: 14,00% (ded. 39.780). Faixa 5: 22,00% (ded. 183.780). Faixa 6: 33,00% (ded. 828.000).

**Anexo V — Serviços III:** Faixa 1: 15,50%. Faixa 2: 18,00% (ded. 4.500). Faixa 3: 19,50% (ded. 9.900). Faixa 4: 20,50% (ded. 17.100). Faixa 5: 23,00% (ded. 62.100). Faixa 6: 30,50% (ded. 540.000).

### Principais referências legais

| Tema | Referência |
|---|---|
| Estatuto do Simples Nacional | LC 123/2006 |
| Tabelas dos Anexos | LC 123/2006, Anexos I-V (alterados pela LC 155/2016) |
| MEI | LC 123/2006, Arts. 18-A a 18-E |
| Fator R | LC 123/2006, Art. 18, § 5º-J |
| Limites de faturamento | LC 123/2006, Art. 3º |
| Sublimite ICMS/ISS | LC 123/2006, Arts. 13 e 18 |
| Reforma Tributária — IVA dual | EC 132/2023 |
| Regulamentação CBS/IBS | LC 214/2025 |
| Segunda fase / vigência 2026 | LC 227/2026 |
| Opção híbrida do Simples | LC 123/2006, Art. 21-A (incluído pela LC 214/2025) |

---

## PROIBIÇÕES

- NUNCA aplicar as alíquotas do Simples Nacional a empresas acima de R$ 4.800.000
- NUNCA permitir que profissionais regulamentados se inscrevam como MEI
- NUNCA ignorar o Fator R no cálculo de atividades do Anexo V
- NUNCA usar somente a receita da atividade corrente para definir a faixa — usar o RBT12 de TODAS as atividades
- NUNCA esquecer que o Anexo IV NÃO inclui o INSS patronal no DAS
- NUNCA tratar os valores do DAS-MEI como fixos entre anos — variam com o salário mínimo
- NUNCA omitir a verificação do sublimite de ICMS/ISS para empresas acima de R$ 3.600.000
- NUNCA apresentar cálculos como definitivos — sempre rotular como estimativa e direcionar o cliente a um contador registrado no CRC
- NUNCA recomendar a opção pelo regime híbrido do art. 21-A da LC 123/06 sem simulação comparativa e revisão por contador
- NUNCA tratar o MEI como sujeito a CBS/IBS — o MEI permanece isento e continua recolhendo apenas pelo DAS-MEI

---

## Aviso legal

Esta skill e seus resultados são fornecidos exclusivamente para fins informativos e de cálculo e não constituem aconselhamento tributário, jurídico ou financeiro. A Open Accountants e seus colaboradores não assumem qualquer responsabilidade por erros, omissões ou consequências decorrentes do uso desta skill. Todos os resultados devem ser revisados e assinados por profissional qualificado (como contador registrado no CRC ou profissional licenciado equivalente no Brasil) antes de qualquer entrega ou tomada de decisão.

A versão mais atualizada e verificada desta skill é mantida em [openaccountants.com](https://openaccountants.com). Faça login para acessar a versão mais recente, solicitar revisão profissional por contador licenciado e acompanhar atualizações conforme a legislação evoluir.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/br-simples-nacional) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. Reviewed by pending depends_on: - income-tax-workflow-base. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
