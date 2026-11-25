---
name: portugal-vat-return
description: "Utilize esta skill sempre que lhe for pedido para preparar, rever ou classificar transações para uma Declaração Periódica de IVA em Portugal, para um trabalhador independente ou pequena empresa. Acione com expressões como \"preparar Declaração Periódica\", \"IVA Portugal\", \"classificar transações para IVA português\", ou qualquer pedido que envolva entrega de IVA em Portugal. Esta skill abrange apenas Portugal Continental (regime normal). As taxas reduzidas da Madeira/Açores, o regime de isenção, a isenção parcial, o regime da margem e os grupos de IVA constam do catálogo de recusas. DEVE ser carregada em conjunto com vat-workflow-base v0.1 ou posterior E com eu-vat-directive v0.1 ou posterior. LEIA SEMPRE esta skill antes de tocar em qualquer trabalho de IVA português. Trigger also on: \"prepare Declaração Periódica\", \"Portuguese VAT return\", \"IVA Portugal\", \"classify transactions for Portuguese VAT\", or any request involving Portugal VAT filing."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: PT
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/portugal-vat-return"
  tax_year: 2025
  obligation: CT
---

# Portugal — IVA (Declaração Periódica) — Skill v3.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Secção 1 — Referência rápida

**Leia esta secção na íntegra antes de classificar qualquer transação. O runbook do fluxo de trabalho encontra-se na Secção 1 do `vat-workflow-base` — siga esse runbook, com esta skill a fornecer o conteúdo específico do país e o `eu-vat-directive` a fornecer o conteúdo da diretiva da UE.**

| Campo | Valor |
|---|---|
| País | Portugal (República Portuguesa) |
| Taxa normal | 23% (Continental); 22% (Madeira); 16% (Açores) |
| Taxas reduzidas | 13% Continental / 12% Madeira / 9% Açores (intermédia: restauração, géneros alimentícios, gasóleo, alguns inputs agrícolas); 6% Continental / 5% Madeira / 4% Açores (reduzida: bens alimentares essenciais, água, livros, medicamentos, transporte de passageiros, alojamento) |
| Taxa zero | 0% (exportações, transmissões intracomunitárias B2B de bens) |
| Formulário da declaração | Declaração Periódica de IVA (campos 1–41+) |
| Portal de submissão | https://www.portaldasfinancas.gov.pt (Portal das Finanças) |
| Autoridade | Autoridade Tributária e Aduaneira (AT) |
| Moeda | Apenas EUR |
| Periodicidades | Mensal (volume de negócios > €650.000 ou Vol. B); Trimestral (volume de negócios ≤ €650.000, Vol. A) |
| Prazo | Mensal: dia 10 do 2.º mês seguinte ao fim do período; Trimestral: dia 15 do 2.º mês seguinte ao fim do trimestre |
| Skill companheira (Tier 1, fluxo) | **vat-workflow-base v0.1 ou posterior — DEVE ser carregada** |
| Skill companheira (Tier 2, diretiva UE) | **eu-vat-directive v0.1 ou posterior — DEVE ser carregada** |
| Contribuidor | Contribuidores Open Accountants |
| Data de validação | Abril 2026 |

**Campos principais da Declaração Periódica (os que utilizará com maior frequência):**

| Campo | Significado |
|---|---|
| 1 | Vendas à taxa normal — base (23%) |
| 2 | Vendas à taxa normal — IVA |
| 3 | Vendas à taxa intermédia — base (13%) |
| 4 | Vendas à taxa intermédia — IVA |
| 5 | Vendas à taxa reduzida — base (6%) |
| 6 | Vendas à taxa reduzida — IVA |
| 7 | Operações isentas com direito a dedução (exportações, intracomunitárias) |
| 8 | Operações isentas sem direito a dedução |
| 9 | Aquisições intracomunitárias — base |
| 10 | Aquisições intracomunitárias — IVA (output, autoliquidado) |
| 16 | Outras operações com IVA devido pelo adquirente (autoliquidação recebida) |
| 17 | IVA devido sobre o campo 16 |
| 20 | Total de IVA liquidado (soma dos campos de output) |
| 21 | IVA dedutível — imobilizado (bens de investimento) |
| 22 | IVA dedutível — existências (stock para revenda) |
| 23 | IVA dedutível — outros bens e serviços |
| 24 | Total de IVA dedutível |
| 40 | IVA a pagar (se 20 > 24) |
| 41 | Crédito de IVA (se 24 > 20) |

**Defaults conservadores — específicos de Portugal:**

| Ambiguidade | Default |
|---|---|
| Taxa desconhecida numa venda | 23% |
| Estatuto de IVA desconhecido numa aquisição | Não dedutível |
| País da contraparte desconhecido | Doméstico Portugal (Continental) |
| B2B ou B2C desconhecido para cliente UE | B2C, liquidar 23% |
| Proporção de utilização empresarial desconhecida | 0% de recuperação |
| Entidade faturadora de SaaS desconhecida | Autoliquidação a partir de país terceiro |
| Estatuto de input bloqueado desconhecido | Bloqueado |
| Não se sabe se a operação está no âmbito | Dentro do âmbito |

**Limiares de sinalização (red flags):**

| Limiar | Valor |
|---|---|
| HIGH transação individual | €5.000 |
| HIGH delta fiscal por default conservador | €400 |
| MEDIUM concentração numa contraparte | >40% |
| MEDIUM número de defaults conservadores | >4 |
| LOW posição absoluta de IVA líquido | €10.000 |

---

## Secção 2 — Inputs necessários e catálogo de recusas

### Inputs necessários

**Mínimo viável** — extrato bancário do período. Aceite de: CGD (Caixa Geral de Depósitos), Millennium BCP, Santander Portugal, Novo Banco, BPI, ActivoBank, Banco CTT, Revolut Business, Wise Business, ou qualquer outro.

**Recomendado** — faturas de venda (sobretudo intracomunitárias e em autoliquidação), faturas de aquisição acima de €400, NIF do cliente (9 dígitos, prefixo PT para contexto UE).

**Ideal** — ficheiro SAF-T (PT) extraído do software de faturação, Declaração Periódica do período anterior, reconciliação do crédito do campo 41.

**Política de recusa se faltar o mínimo — SOFT WARN.** Mesmo padrão que a Malta v2.0.

### Catálogo de recusas específico de Portugal

**R-PT-1 — Regime de isenção (Art.º 53.º CIVA).** *Acionador:* cliente abrangido pela isenção de pequenas empresas (volume de negócios ≤ €15.000, limiar alterado pelo OE 2024/2025 — verificar valor em vigor). *Mensagem:* "Os clientes em regime de isenção não liquidam IVA e não podem deduzir IVA suportado. Não entregam Declaração Periódica. Esta skill cobre apenas o regime normal."

**R-PT-2 — Isenção parcial (pro rata / Art.º 23.º CIVA).** *Acionador:* operações simultaneamente tributáveis e isentas, não de minimis. *Mensagem:* "Operações mistas (tributáveis e isentas) exigem aplicação do pro rata nos termos do Art.º 23.º CIVA. Recorra a um contabilista certificado."

**R-PT-3 — Regime da margem (Art.º 50.º-A a 50.º-D CIVA).** *Acionador:* bens em segunda mão, arte, antiguidades. *Mensagem:* "O regime da margem exige cálculo bem a bem. Fora do âmbito."

**R-PT-4 — Grupo de IVA.** *Acionador:* grupo de IVA. *Mensagem:* "O grupo de IVA exige consolidação. Fora do âmbito."

**R-PT-5 — Representante fiscal.** *Acionador:* não residente com representante fiscal. *Mensagem:* "Não residente com representante fiscal — fora do âmbito."

**R-PT-6 — Taxas Madeira / Açores.** *Acionador:* cliente opera na Madeira ou nos Açores. *Mensagem:* "A Madeira (22%/12%/5%) e os Açores (16%/9%/4%) têm tabelas de taxas diferentes. Esta skill cobre apenas as taxas de Portugal Continental. Recorra a um contabilista certificado familiarizado com as taxas regionais."

**R-PT-7 — Imobiliário (IVA imobiliário).** *Acionador:* operações com imóveis. *Mensagem:* "O IVA sobre operações imobiliárias é complexo. Recorra a um contabilista certificado."

**R-PT-8 — IRS/IRC em vez de IVA.** *Acionador:* o utilizador pergunta sobre IRS/IRC em vez de IVA. *Mensagem:* "Esta skill trata exclusivamente do IVA português."

**Nota importante — regime NHR/IFICI:** O regime do Residente Não Habitual (NHR), bem como o regime IFICI que o sucedeu, são regimes de IRS (imposto sobre o rendimento). **O NHR NÃO isenta de IVA.** Quem estiver em NHR/IFICI e exercer atividade económica continua sujeito às regras gerais do CIVA — incluindo registo, liquidação e dedução de IVA, e entrega da Declaração Periódica. Para análise do regime de rendimento, consulte a skill `pt-nhr-ifici`.

---

## Secção 3 — Biblioteca de padrões de fornecedores (tabela de consulta)

Pesquisa por substring sem distinção entre maiúsculas e minúsculas. Se nada coincidir, recorra à Secção 5.

### 3.1 Bancos portugueses (comissões isentas — excluir)

| Padrão | Tratamento | Notas |
|---|---|---|
| CGD, CAIXA GERAL, CAIXA GERAL DE DEPÓSITOS | EXCLUIR para comissões bancárias | Serviço financeiro, isento |
| MILLENNIUM BCP, BCP | EXCLUIR para comissões bancárias | Idem |
| SANTANDER PORTUGAL, SANTANDER PT | EXCLUIR para comissões bancárias | Idem |
| NOVO BANCO | EXCLUIR para comissões bancárias | Idem |
| BPI, BANCO BPI | EXCLUIR para comissões bancárias | Idem |
| ACTIVOBANK | EXCLUIR para comissões bancárias | Idem |
| BANCO CTT | EXCLUIR para comissões bancárias | Idem |
| REVOLUT, WISE, N26 (linhas de comissão) | EXCLUIR | Verificar subscrições tributáveis |
| JUROS, JURO | EXCLUIR | Juros, fora do âmbito |
| EMPRÉSTIMO, CRÉDITO HABITAÇÃO | EXCLUIR | Capital do empréstimo |

### 3.2 Estado português e entidades estatutárias (excluir na totalidade)

| Padrão | Tratamento | Notas |
|---|---|---|
| PORTAL DAS FINANÇAS, AT, AUTORIDADE TRIBUTÁRIA | EXCLUIR | Pagamento de imposto (IVA, IRS, IRC) |
| SEGURANÇA SOCIAL | EXCLUIR | Contribuições para a Segurança Social |
| FINANÇAS, DIREÇÃO-GERAL | EXCLUIR | Autoridade tributária |
| CONSERVATÓRIA, REGISTO COMERCIAL | EXCLUIR | Registo comercial |
| CÂMARA MUNICIPAL | EXCLUIR | Taxas municipais |
| IRN, INSTITUTO DOS REGISTOS E NOTARIADO | EXCLUIR | Registo do Estado |
| IAPMEI | EXCLUIR | Organismo público |
| ALFÂNDEGA, DIREÇÃO-GERAL DAS ALFÂNDEGAS | EXCLUIR | Alfândegas (verificar IVA na importação) |

### 3.3 Serviços públicos portugueses

| Padrão | Tratamento | Campo | Notas |
|---|---|---|---|
| EDP, EDP ENERGIA, EDP COMERCIAL | Doméstico 23% | 23 (input) | Eletricidade — taxa normal |
| GALP, GALP ENERGIA | Doméstico 23% | 23 | Energia/combustível |
| ENDESA PORTUGAL, IBERDROLA | Doméstico 23% | 23 | Energia |
| EPAL, ÁGUAS DE PORTUGAL | Doméstico 6% | 23 | Água à taxa reduzida |
| NOS, NOS COMUNICAÇÕES | Doméstico 23% | 23 | Telecomunicações — overhead |
| MEO, ALTICE PORTUGAL | Doméstico 23% | 23 | Telecomunicações/banda larga |
| VODAFONE PT, VODAFONE PORTUGAL | Doméstico 23% | 23 | Telecomunicações |
| NOWO | Doméstico 23% | 23 | Telecomunicações |

### 3.4 Seguros (isentos — excluir)

| Padrão | Tratamento | Notas |
|---|---|---|
| FIDELIDADE | EXCLUIR | Seguro, isento |
| AGEAS PORTUGAL, ALLIANZ PORTUGAL | EXCLUIR | Idem |
| TRANQUILIDADE, GENERALI PT | EXCLUIR | Idem |
| SEGURO, APÓLICE | EXCLUIR | Todos os seguros isentos |

### 3.5 Correios e logística

| Padrão | Tratamento | Campo | Notas |
|---|---|---|---|
| CTT (correio normal) | EXCLUIR para correio standard | | Serviço postal universal isento |
| CTT (encomendas, CTT Expresso) | Doméstico 23% | 23 | Serviço não universal tributável |
| DHL EXPRESS PORTUGAL | Doméstico 23% | 23 | Courier expresso |
| CHRONOPOST PORTUGAL | Doméstico 23% | 23 | Expresso |
| FEDEX, UPS PORTUGAL | Doméstico 23% | 23 | Courier |

### 3.6 Transportes (Portugal, doméstico)

| Padrão | Tratamento | Campo | Notas |
|---|---|---|---|
| CP, COMBOIOS DE PORTUGAL | Doméstico 6% | 23 (input) | Ferroviário à taxa reduzida |
| METRO LISBOA, METRO PORTO | Doméstico 6% | 23 | Metropolitano urbano |
| CARRIS, CARRIS METROPOLITANA | Doméstico 6% | 23 | Autocarros de Lisboa |
| STCP | Doméstico 6% | 23 | Autocarros do Porto |
| UBER PT, UBER PORTUGAL | Doméstico 6% (transporte) | 23 | TVDE |
| BOLT PT | Doméstico 6% | 23 | TVDE |
| TÁXI | Doméstico 6% | 23 | Táxi local |
| TAP AIR PORTUGAL (doméstico) | Doméstico 6% | 23 | Voos domésticos à taxa reduzida |
| TAP, RYANAIR, EASYJET (internacional) | EXCLUIR / 0% | | Voos internacionais isentos |
| BRISA, VIA VERDE | Doméstico 23% | 23 | Portagens de autoestrada |

### 3.7 Retalho alimentar (bloqueado salvo se setor da restauração/hotelaria)

| Padrão | Tratamento | Notas |
|---|---|---|
| CONTINENTE, MODELO | Por defeito, BLOQUEAR IVA dedutível | Aprovisionamento pessoal |
| PINGO DOCE, JERÓNIMO MARTINS | Por defeito, BLOQUEAR | Idem |
| LIDL, ALDI, INTERMARCHÉ | Por defeito, BLOQUEAR | Idem |
| MINIPREÇO, MERCADONA | Por defeito, BLOQUEAR | Idem |
| RESTAURANTE, PASTELARIA, CAFÉ | Por defeito, BLOQUEAR | Despesas de representação — ver 5.12 |

### 3.8 SaaS — fornecedores UE (autoliquidação)

| Padrão | Entidade faturadora | Campo | Notas |
|---|---|---|---|
| GOOGLE (Ads, Workspace, Cloud) | Google Ireland Ltd (IE) | 16/17 + 23 | Autoliquidação: output no 17, input no 23 |
| MICROSOFT (365, Azure) | Microsoft Ireland Operations Ltd (IE) | 16/17 + 23 | Autoliquidação |
| ADOBE | Adobe Systems Software Ireland Ltd (IE) | 16/17 + 23 | Autoliquidação |
| META, FACEBOOK ADS | Meta Platforms Ireland Ltd (IE) | 16/17 + 23 | Autoliquidação |
| LINKEDIN (paga) | LinkedIn Ireland Unlimited (IE) | 16/17 + 23 | Autoliquidação |
| SPOTIFY TECHNOLOGY | Spotify AB (SE) | 16/17 + 23 | UE, autoliquidação |
| DROPBOX | Dropbox International Unlimited (IE) | 16/17 + 23 | Autoliquidação |
| SLACK | Slack Technologies Ireland Ltd (IE) | 16/17 + 23 | Autoliquidação |
| ATLASSIAN (Jira, Confluence) | Atlassian Network Services BV (NL) | 16/17 + 23 | UE, autoliquidação |
| ZOOM | Zoom Video Communications Ireland Ltd (IE) | 16/17 + 23 | Autoliquidação |
| STRIPE (subscrição) | Stripe Technology Europe Ltd (IE) | 16/17 + 23 | Comissões de transação isentas — ver 3.11 |

### 3.9 SaaS — fornecedores fora da UE (autoliquidação)

| Padrão | Entidade faturadora | Campo | Notas |
|---|---|---|---|
| AWS (standard) | AWS EMEA SARL (LU) — verificar | 16/17 + 23 | LU → autoliquidação UE |
| NOTION | Notion Labs Inc (US) | 16/17 + 23 | Autoliquidação país terceiro |
| ANTHROPIC, CLAUDE | Anthropic PBC (US) | 16/17 + 23 | Autoliquidação país terceiro |
| OPENAI, CHATGPT | OpenAI Inc (US) | 16/17 + 23 | Autoliquidação país terceiro |
| GITHUB | GitHub Inc (US) | 16/17 + 23 | Verificar entidade IE |
| FIGMA | Figma Inc (US) | 16/17 + 23 | País terceiro |
| CANVA | Canva Pty Ltd (AU) | 16/17 + 23 | País terceiro |
| HUBSPOT | HubSpot Inc (US) ou IE — verificar | 16/17 + 23 | Depende da entidade faturadora |
| TWILIO | Twilio Inc (US) | 16/17 + 23 | País terceiro |

### 3.10 SaaS — a exceção

| Padrão | Tratamento | Porquê |
|---|---|---|
| AWS EMEA SARL | Autoliquidação UE campos 16/17 + 23 (entidade LU) | Tratamento UE standard. Se a fatura indicar IVA português, tratar como doméstico 23%. |

### 3.11 Processadores de pagamento

| Padrão | Tratamento | Notas |
|---|---|---|
| STRIPE (comissões de transação) | EXCLUIR (isento) | Serviços financeiros |
| PAYPAL (comissões de transação) | EXCLUIR (isento) | Idem |
| STRIPE (subscrição) | Autoliquidação UE 16/17 + 23 | Entidade IE |
| SUMUP, SQUARE, ZETTLE | Verificar fatura | Se portuguesa: doméstico 23%; se UE: autoliquidação |
| IFTHENPAY, EUPAGO | Verificar fatura | Processadores portugueses — comissões podem ser isentas |

### 3.12 Serviços profissionais (Portugal)

| Padrão | Tratamento | Campo | Notas |
|---|---|---|---|
| CONTABILISTA, GABINETE DE CONTABILIDADE | Doméstico 23% | 23 | Sempre dedutível |
| ADVOGADO, ESCRITÓRIO DE ADVOCACIA | Doméstico 23% | 23 | Assuntos jurídicos da atividade |
| NOTÁRIO, CARTÓRIO | Doméstico 23% | 23 | Honorários notariais da atividade |
| SOLICITADOR | Doméstico 23% | 23 | Profissional do foro |
| REVISOR OFICIAL DE CONTAS, ROC | Doméstico 23% | 23 | Auditor |

### 3.13 Salários e Segurança Social (excluir na totalidade)

| Padrão | Tratamento | Notas |
|---|---|---|
| SEGURANÇA SOCIAL | EXCLUIR | Contribuições para a Segurança Social |
| SALÁRIO, VENCIMENTO, REMUNERAÇÃO | EXCLUIR | Vencimentos |
| SUBSÍDIO, SUBSÍDIO DE FÉRIAS | EXCLUIR | Subsídios de férias/Natal |
| FUNDO DE COMPENSAÇÃO, FCT | EXCLUIR | Fundo de compensação do trabalho |

### 3.14 Imóveis e renda

| Padrão | Tratamento | Notas |
|---|---|---|
| RENDA COMERCIAL, ARRENDAMENTO COMERCIAL | Doméstico 23% | Arrendamento comercial com opção por IVA (Art.º 12.º n.º 1 al. e) CIVA) |
| RENDA, ARRENDAMENTO (habitação) | EXCLUIR | Arrendamento habitacional isento |
| IMI, IMPOSTO MUNICIPAL | EXCLUIR | Imposto sobre imóveis |
| AIMI | EXCLUIR | Adicional ao IMI |

### 3.15 Transferências internas e exclusões

| Padrão | Tratamento | Notas |
|---|---|---|
| TRANSFERÊNCIA INTERNA, MOVIMENTO INTERNO | EXCLUIR | Movimento interno |
| DIVIDENDO | EXCLUIR | Fora do âmbito |
| AMORTIZAÇÃO DE EMPRÉSTIMO | EXCLUIR | Reembolso de empréstimo |
| LEVANTAMENTO, LEVANTAMENTO ATM | TIER 2 — perguntar | Por defeito, excluir |
| REFORÇO DE CAPITAL, SUPRIMENTO | EXCLUIR | Entrada do sócio / suprimentos |

---

## Secção 4 — Exemplos resolvidos

Seis classificações totalmente resolvidas, com base num hipotético consultor de TI trabalhador independente sediado em Portugal (regime normal de IVA).

### Exemplo 1 — Autoliquidação SaaS fora da UE (Notion)

**Linha de input:**
`03.04.2026 ; NOTION LABS INC ; DÉBITO ; Subscrição mensal ; USD 16,00 ; EUR 14,68`

**Raciocínio:**
Entidade dos EUA. Autoliquidação fora da UE nos termos do Art.º 6.º n.º 6 do CIVA. O cliente autoliquida: IVA output no campo 17, IVA dedutível no campo 23. Resultado líquido zero.

**Output:**

| Data | Contraparte | Bruto | Líquido | IVA | Taxa | Campo (input) | Campo (output) | Default? | Pergunta? | Excluído? |
|---|---|---|---|---|---|---|---|---|---|---|
| 03.04.2026 | NOTION LABS INC | -14,68 | -14,68 | 3,38 | 23% | 23 | 16/17 | N | — | — |

### Exemplo 2 — Serviço UE, autoliquidação (Google Ads)

**Linha de input:**
`10.04.2026 ; GOOGLE IRELAND LIMITED ; DÉBITO ; Google Ads abril 2026 ; -850,00 ; EUR`

**Raciocínio:**
Entidade IE — autoliquidação UE. IVA output no campo 17, IVA input no campo 23. Líquido zero.

**Output:**

| Data | Contraparte | Bruto | Líquido | IVA | Taxa | Campo (input) | Campo (output) | Default? | Pergunta? | Excluído? |
|---|---|---|---|---|---|---|---|---|---|---|
| 10.04.2026 | GOOGLE IRELAND LIMITED | -850,00 | -850,00 | 195,50 | 23% | 23 | 16/17 | N | — | — |

### Exemplo 3 — Despesa de representação, tratamento em Portugal

**Linha de input:**
`15.04.2026 ; RESTAURANTE BELCANTO LISBOA ; DÉBITO ; Jantar de negócios ; -220,00 ; EUR`

**Raciocínio:**
Restaurante. Em Portugal, o IVA suportado em refeições de negócios é, em regra, dedutível ao abrigo do Art.º 21.º n.º 1 al. d) do CIVA, mas apenas 50% se forem consideradas despesas de representação. O limite de 50% aplica-se à própria dedução do IVA (e não somente à base do IRS/IRC). Por defeito: bloquear e sinalizar ao revisor. Se confirmada finalidade empresarial com documentação → 50% do IVA dedutível.

**Output:**

| Data | Contraparte | Bruto | Líquido | IVA | Taxa | Campo | Default? | Pergunta? | Excluído? |
|---|---|---|---|---|---|---|---|---|---|
| 15.04.2026 | RESTAURANTE BELCANTO LISBOA | -220,00 | -220,00 | 0 | — | — | S | Q1 | "Restaurante: IVA 50% dedutível se despesa de representação. Confirmar finalidade empresarial." |

### Exemplo 4 — Bens de investimento (imobilizado)

**Linha de input:**
`18.04.2026 ; WORTEN (SONAE) ; DÉBITO ; Portátil HP ; -1.595,00 ; EUR`

**Raciocínio:**
€1.595 brutos. Em Portugal, os ativos utilizados por mais de um ano e acima de um limiar de minimis são imobilizado (bens de investimento). O IVA suportado vai para o campo 21 (IVA dedutível — imobilizado) em vez do campo 23. Sujeito a regularização ao longo de 5 anos (móveis) ou 20 anos (imóveis) — Art.º 24.º a 26.º do CIVA.

**Output:**

| Data | Contraparte | Bruto | Líquido | IVA | Taxa | Campo | Default? | Pergunta? | Excluído? |
|---|---|---|---|---|---|---|---|---|---|
| 18.04.2026 | WORTEN | -1.595,00 | -1.296,75 | -298,25 | 23% | 21 | N | — | — |

### Exemplo 5 — Venda de serviço B2B intra-UE

**Linha de input:**
`22.04.2026 ; STUDIO KREBS GMBH ; CRÉDITO ; Fatura PT-2026-018 consultoria TI ; +3.500,00 ; EUR`

**Raciocínio:**
Serviços B2B para a Alemanha — o lugar da prestação é o país do adquirente (Art.º 6.º n.º 6 al. a) CIVA / Art.º 44.º da Diretiva). Reportar no campo 7 (operações isentas com direito a dedução). Sem IVA liquidado. Verificar o USt-IdNr alemão no VIES.

**Output:**

| Data | Contraparte | Bruto | Líquido | IVA | Taxa | Campo | Default? | Pergunta? | Excluído? |
|---|---|---|---|---|---|---|---|---|---|
| 22.04.2026 | STUDIO KREBS GMBH | +3.500,00 | +3.500,00 | 0 | 0% | 7 | S | Q2 (HIGH) | "Verificar USt-IdNr alemão no VIES" |

### Exemplo 6 — Viaturas, regras de dedução

**Linha de input:**
`28.04.2026 ; ALD AUTOMOTIVE PORTUGAL ; DÉBITO ; Renting VW Golf ; -450,00 ; EUR`

**Raciocínio:**
Renting de viatura. Em Portugal, o IVA suportado em viaturas ligeiras de passageiros não é, em regra, dedutível (Art.º 21.º n.º 1 al. a) CIVA). Exceções: táxis, ensino de condução, viaturas afetas a aluguer em empresas de rent-a-car, veículos elétricos (50% dedutíveis desde 2020), híbridos plug-in (50% dedutíveis). Um VW Golf (não elétrico) → bloqueado. Se elétrico/híbrido → 50% dedutível.

**Output:**

| Data | Contraparte | Bruto | Líquido | IVA | Taxa | Campo | Default? | Pergunta? | Excluído? |
|---|---|---|---|---|---|---|---|---|---|
| 28.04.2026 | ALD AUTOMOTIVE PORTUGAL | -450,00 | -450,00 | 0 | — | — | S | Q3 | "Viatura ligeira de passageiros: IVA bloqueado. Elétrico/híbrido (50% dedutível)?" |

---

## Secção 5 — Regras de classificação Tier 1 (compactadas)

### 5.1 Taxa normal 23% (Art.º 18.º n.º 1 al. c) CIVA)

Taxa por defeito em Portugal Continental. Vendas → campos 1/2. Aquisições → campo 23 (ou 21/22).

### 5.2 Taxa intermédia 13% (Art.º 18.º n.º 1 al. b), Lista II)

Restauração (refeições + bebidas não alcoólicas), gasóleo, certos géneros alimentares (conservas, óleos), vinho, inputs agrícolas. Vendas → campos 3/4.

### 5.3 Taxa reduzida 6% (Art.º 18.º n.º 1 al. a), Lista I)

Géneros alimentares essenciais (pão, leite, fruta, legumes, peixe, carne), água, livros, medicamentos, transporte de passageiros, alojamento, espetáculos culturais. Vendas → campos 5/6.

### 5.4 Taxa zero e isenções com direito a dedução

Exportações → campo 7. Bens intra-UE → campo 7. Serviços B2B intra-UE → campo 7.

### 5.5 Isentas sem direito a dedução (Art.º 9.º CIVA)

Saúde, ensino, seguros, serviços financeiros, arrendamento habitacional, serviço postal universal. Se significativas → **a R-PT-2 recusa**.

### 5.6 Aquisições locais

IVA suportado em fatura conforme. Bens de investimento → campo 21. Existências → campo 22. Restantes → campo 23.

### 5.7 Autoliquidação — serviços intra-UE (Art.º 6.º n.º 6)

Serviço UE: base → campo 16, IVA output → campo 17, input → campo 23. Resultado líquido zero.

### 5.8 Autoliquidação — bens intra-UE (aquisições intracomunitárias)

Bens UE: base → campo 9, IVA output → campo 10, input → campo 23/21.

### 5.9 Autoliquidação — fora da UE

Países terceiros: base → campo 16, IVA output → campo 17, input → campo 23.

### 5.10 Autoliquidação interna (Art.º 2.º n.º 1 al. i)-j) CIVA)

Portugal aplica autoliquidação interna em empreitadas de obras (serviços de construção civil), sucatas e licenças de emissão de CO2. O adquirente autoliquida o IVA.

### 5.11 Bens de investimento (imobilizado)

Ativos utilizados por mais de 1 ano → campo 21 para o IVA suportado. Sujeitos a regularização ao longo de 5 anos (móveis) ou 20 anos (imóveis), Art.º 24.º a 26.º CIVA.

### 5.12 IVA dedutível bloqueado/restringido (Art.º 21.º CIVA)

- Viaturas ligeiras de passageiros: IVA bloqueado (Art.º 21.º n.º 1 al. a)). Exceções: táxi, ensino de condução, rent-a-car. Veículos elétricos: 50% dedutível. Híbridos plug-in: 50% dedutível.
- Combustíveis: gasóleo para VP, 50% dedutível; GPL/elétrico, 100% dedutível. Gasolina: NÃO dedutível em VP.
- Despesas de representação: IVA 50% dedutível (Art.º 21.º n.º 1 al. d)). Inclui refeições de negócios — 50% do IVA, e não dedução total.
- Deslocações e alojamento: IVA dedutível se relacionado com a atividade e documentado.
- Tabaco: não dedutível.
- Uso pessoal: não dedutível.
- Ofertas: IVA dedutível apenas até 5 por mil do volume de negócios e custo unitário ≤ €50.

### 5.13 SAF-T (PT)

Portugal exige o SAF-T (Standard Audit File for Tax) a todas as empresas que utilizem software de faturação. O ficheiro SAF-T (PT) é submetido mensalmente à AT e constitui a fonte de dados mais fiável para a classificação de IVA. Quando disponível, prefira os dados do SAF-T (PT) ao extrato bancário. As faturas devem conter o código ATCUD (código único de documento) e, quando aplicável, ser comunicadas via e-fatura.

### 5.14 Vendas — domésticas locais

Liquidar 23%, 13% ou 6%. Mapear para os campos 1/3/5 conforme aplicável.

### 5.15 Vendas — B2C transfronteiriças

Acima de €10.000 → **a R-EU-5 OSS recusa**.

---

## Secção 6 — Catálogo Tier 2 (compactado)

### 6.1 Combustível e custos de viatura

*Padrão:* GALP, REPSOL, BP, CEPSA. *Default:* bloqueado (VP por defeito). *Pergunta:* "Viatura ligeira de passageiros ou comercial? Elétrico/híbrido (50% IVA dedutível)? Gasóleo para VP: 50% dedutível."

### 6.2 Restaurantes e despesas de representação

*Padrão:* restaurante, pastelaria, café. *Default:* bloquear. *Pergunta:* "Refeição de negócios (despesa de representação)? IVA 50% dedutível com documentação."

### 6.3 SaaS ambíguo

*Default:* autoliquidação país terceiro, campos 16/17 + 23. *Pergunta:* "Verificar entidade legal na fatura."

### 6.4 Transferências de sócios/titulares

*Default:* excluir como suprimento/reforço. *Pergunta:* "Pagamento de cliente, fundos próprios ou empréstimo?"

### 6.5 Entradas de particulares

*Default:* B2C doméstico 23%. *Pergunta:* "Venda? A empresa ou consumidor final?"

### 6.6 Entradas estrangeiras

*Default:* doméstico 23%. *Pergunta:* "B2B com NIF, B2C, bens/serviços, país?"

### 6.7 Aquisições de valor elevado

*Default:* campo 21 se bem de investimento. *Pergunta:* "Confirmar total da fatura."

### 6.8 Telemóvel e internet de uso misto

*Default:* 0%. *Pergunta:* "Linha dedicada à atividade ou uso misto?"

### 6.9 Saídas para particulares

*Default:* excluir. *Pergunta:* "Prestador de serviços, vencimento, reembolso, pessoal?"

### 6.10 Levantamentos de numerário

*Default:* excluir. *Pergunta:* "Para quê?"

### 6.11 Renda

*Default:* sem IVA (habitação). *Pergunta:* "Comercial com opção pelo IVA (Art.º 12.º n.º 1 al. e))?"

### 6.12 Hotelaria estrangeira

*Default:* excluir do IVA dedutível. *Pergunta:* "Deslocação em serviço?"

### 6.13 Receitas de Airbnb

*Default:* sinalizar [T2]. *Pergunta:* "Registo como Alojamento Local? Duração? Taxa reduzida de 6% para alojamento?"

### 6.14 Autoliquidação na construção

*Padrão:* empreiteiro, construção civil. *Default:* sinalizar [T2]. *Pergunta:* "Subempreiteiro de obras sujeito a autoliquidação interna?"

### 6.15 Vendas em plataformas

*Default:* se UE transfronteiriço acima de €10.000 → R-EU-5. Caso contrário, doméstico 23%. *Pergunta:* "Vende fora de Portugal?"

---

## Secção 7 — Modelo de papel de trabalho em Excel (específico de Portugal)

### Folha "Transações"

A coluna H aceita códigos de campo conforme a Secção 1.

### Folha "Resumo por Campo"

```
| 1  | Vendas 23% base | =SUMIFS(...) |
| 2  | IVA sobre vendas 23% | =1*0,23 |
| 3  | Vendas 13% base | =SUMIFS(...) |
| 4  | IVA sobre vendas 13% | =3*0,13 |
| 5  | Vendas 6% base | =SUMIFS(...) |
| 6  | IVA sobre vendas 6% | =5*0,06 |
| 7  | Isentas com direito a dedução | =SUMIFS(...) |
| 9  | Aquisições intracomunitárias base | =SUMIFS(...) |
| 10 | IVA sobre intracomunitárias | =9*0,23 |
| 16 | Outras operações em autoliquidação base | =SUMIFS(...) |
| 17 | IVA em autoliquidação | =16*0,23 |
| 20 | Total IVA liquidado | =2+4+6+10+17 |
| 21 | IVA dedutível — imobilizado | =SUMIFS(IVA suportado, ..., "21") |
| 22 | IVA dedutível — existências | =SUMIFS(..., "22") |
| 23 | IVA dedutível — outros | =SUMIFS(..., "23") |
| 24 | Total IVA dedutível | =21+22+23 |
| 40 | IVA a pagar | =MAX(0; 20-24) |
| 41 | Crédito de IVA | =MAX(0; 24-20) |
```

### Passo obrigatório de recálculo

```bash
python /mnt/skills/public/xlsx/scripts/recalc.py /mnt/user-data/outputs/portugal-vat-<period>-working-paper.xlsx
```

---

## Secção 8 — Guia de leitura de extratos bancários portugueses

**Convenções de formato CSV.** Os bancos portugueses exportam CSV com ponto-e-vírgula e datas no formato DD-MM-AAAA ou DD/MM/AAAA. Colunas comuns: Data, Descrição/Movimento, Débito, Crédito, Saldo. A CGD e o Millennium BCP utilizam formatos próprios de exportação.

**Variantes da língua.** Renda (arrendamento), salário/vencimento, juros, transferência, contribuições, fatura, reembolso, depósito, levantamento. Note-se a grafia europeia: "receção" (e não "recepção").

**Transferências internas.** "Transferência interna", "movimento entre contas". Excluir.

**Pagamentos no Portal das Finanças.** Os pagamentos de impostos aparecem como "AT", "FINANÇAS", "PAGAMENTO ESTADO". Excluir sempre.

**Segurança Social.** As contribuições aparecem como débito direto mensal. Excluir sempre.

**Integração com SAF-T.** Quando disponível, o ficheiro SAF-T (PT) fornece dados estruturados das faturas, incluindo o NIF das contrapartes, as taxas de IVA e os montantes. Preferir os dados do SAF-T (PT).

**Moeda estrangeira.** Converter em EUR à taxa do BCE.

**Prefixo IBAN.** PT = Portugal. ES, IE, FR, DE = UE. US, GB, BR = fora da UE.

---

## Secção 9 — Onboarding (fallback)

### 9.1 Tipo de entidade
*Inferência:* Lda. = sociedade; Unipessoal/Sociedade = sociedade; trabalhador independente = sole trader. *Fallback:* "Trabalhador independente, Lda. ou S.A.?"

### 9.2 Regime de IVA
*Fallback:* "Regime normal ou regime de isenção (Art.º 53.º)?"

### 9.3 NIF
*Fallback:* "Qual o seu NIF? (9 dígitos, prefixo PT para contexto UE)"

### 9.4 Período e periodicidade
*Fallback:* "Mensal (Vol. B) ou trimestral (Vol. A)?"

### 9.5 Setor de atividade
*Fallback:* "Qual a atividade da empresa?"

### 9.6 Trabalhadores
*Inferência:* débitos para a Segurança Social. *Fallback:* "Tem trabalhadores?"

### 9.7 Operações isentas
*Fallback:* "Realiza vendas isentas?" *Se sim → R-PT-2.*

### 9.8 Crédito transitado
*Perguntar sempre.* "Crédito de IVA do período anterior? (Campo 41)"

### 9.9 Clientes transfronteiriços
*Fallback:* "Clientes fora de Portugal? UE/fora da UE? B2B/B2C?"

### 9.10 Operações na Madeira/Açores
*Condicional:* "Tem operações na Madeira ou nos Açores?" *Se sim → R-PT-6 recusa.*

### 9.11 NHR / IFICI
*Condicional:* "Beneficia do regime NHR ou do regime IFICI?" *Estes regimes aplicam-se ao IRS e NÃO isentam de IVA — o IVA segue as regras gerais. Para a análise de IRS, consulte a skill `pt-nhr-ifici`.*

---

## Secção 10 — Material de referência

### Fontes

1. Código do IVA (CIVA) — https://info.portaldasfinancas.gov.pt
2. RITI (Regime do IVA nas Transações Intracomunitárias) — D.L. 290/92
3. Formulário e instruções da Declaração Periódica — Portal das Finanças
4. Especificações técnicas do SAF-T (PT) — Portaria 302/2016 (e diplomas posteriores sobre ATCUD e e-fatura)
5. Diretiva 2006/112/CE do Conselho — através da skill companheira `eu-vat-directive`
6. VIES — https://ec.europa.eu/taxation_customs/vies/
7. Regime NHR/IFICI — consultar `pt-nhr-ifici` (apenas para efeitos de IRS, sem impacto em IVA)

### Lacunas conhecidas

1. Tabelas de taxas da Madeira/Açores não incluídas (R-PT-6 recusa).
2. Autoliquidação interna na construção apenas sinalizada T2.
3. Regra dos 50% para veículos elétricos/híbridos requer a classificação atual do veículo.
4. Limiar do regime de isenção (€15.000, alterado pelo OE 2024/2025) — verificar valor em vigor.
5. A integração com SAF-T (PT) está sinalizada mas não automatizada.
6. A dedução a 50% do IVA em despesas de representação (restaurantes) exige documentação de suporte.
7. A dedução a 50% do IVA no gasóleo para VP é a atual — verificar anualmente.

### Change log

- **v3.0 (Maio 2026):** Tradução para português europeu (PT-PT). Reforço da referência ao NHR/IFICI e clarificação de que não isenta de IVA. Atualização do limiar do regime de isenção para €15.000 (OE 2024/2025) e menção explícita de SAF-T (PT), ATCUD e e-fatura.
- **v2.0 (Abril 2026):** Reescrita completa para a estrutura Malta v2.0.
- **v1.0/1.1:** Skill inicial.

### Auto-verificação (v3.0)

1. Referência rápida: sim. 2. Biblioteca de fornecedores (15): sim. 3. Exemplos resolvidos (6): sim. 4. Tier 1 (15): sim. 5. Tier 2 (15): sim. 6. Modelo Excel: sim. 7. Onboarding (11, com NHR/IFICI): sim. 8. 8 recusas: sim. 9. Referência: sim. 10. Bloqueio de viaturas com exceção EV/híbrido a 50%: sim. 11. Dedução de 50% do IVA na restauração: sim. 12. Exigência de SAF-T (PT), ATCUD e e-fatura referida: sim. 13. Continental vs Madeira/Açores: sim. 14. Estrutura de três taxas (23/13/6): sim. 15. Autoliquidação fora da UE nos campos 16/17: sim. 16. Cruzamento com `pt-nhr-ifici` e ressalva de que NHR não isenta de IVA: sim.

## Fim da Skill — Portugal IVA (Declaração Periódica) v3.0

Esta skill está incompleta sem AMBOS os ficheiros companheiros: `vat-workflow-base` v0.1+ E `eu-vat-directive` v0.1+.

---

## Aviso legal

Esta skill e os seus outputs são fornecidos apenas para fins informativos e de cálculo e não constituem aconselhamento fiscal, jurídico ou financeiro. A Open Accountants e os seus contribuidores não assumem qualquer responsabilidade por erros, omissões ou consequências decorrentes do uso desta skill. Todos os outputs devem ser revistos e validados por um profissional qualificado (designadamente, contabilista certificado, revisor oficial de contas ou outro profissional legalmente habilitado) antes de qualquer entrega ou tomada de decisão.

A versão mais atualizada e verificada desta skill é mantida em [openaccountants.com](https://openaccountants.com). Inicie sessão para aceder à versão mais recente, solicitar revisão profissional por um contabilista licenciado e acompanhar atualizações à medida que a legislação evolui.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/portugal-vat-return) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
