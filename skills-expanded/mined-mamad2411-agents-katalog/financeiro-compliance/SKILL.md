---
name: "financeiro-compliance"
description: |
  Skills para gestão financeira, conformidade regulatória brasileira (LGPD, Receita
  Federal), contratos e análise de riscos. Cobre Simples Nacional, MEI, LGPD, DRE,
  fluxo de caixa e contratos conforme o Código Civil e CDC brasileiros.
version: 1.0.0
license: MIT
tags:
  - financeiro
  - compliance
  - lgpd
  - impostos
  - contratos
  - fluxo-caixa
  - receita-federal
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/financeiro-compliance.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Financeiro, Jurídico & Compliance (Nível PODEROSO)

Skills especializadas para gestão financeira e conformidade regulatória brasileira. Cobre o ciclo financeiro completo de PMEs, startups e empresas de médio porte: do planejamento do fluxo de caixa ao compliance com LGPD, passando por impostos, contratos e análise de riscos.

Este domínio é indispensável para CFOs, controllers, advogados, contadores e empreendedores que precisam navegar a complexidade tributária, regulatória e contratual do Brasil com segurança e eficiência.

**AVISO LEGAL:** As skills deste domínio fornecem orientação geral e frameworks de análise. Para decisões tributárias, jurídicas ou de compliance com impacto financeiro relevante, sempre consulte um contador ou advogado habilitado.

## Início Rápido

### Claude Code
```
/read financeiro-compliance/SKILL.md
```
Depois acesse a sub-skill pelo contexto:
```
/read financeiro-compliance/fluxo-caixa/SKILL.md
/read financeiro-compliance/impostos-br/SKILL.md
/read financeiro-compliance/conformidade-lgpd/SKILL.md
```

### Cursor
Adicione em `.cursor/rules/financeiro-compliance.md`:
```
Use as skills de financeiro-compliance para análise financeira, tributária e jurídica.
Contexto obrigatório: legislação brasileira (CC, CDC, CLT, LGPD, Receita Federal).
Aviso em cada resposta: recomende consulta profissional para decisões de alto impacto.
```

### Codex
Adicione em `AGENTS.md`:
```markdown
## Financeiro, Jurídico e Compliance
Ao criar análises financeiras ou materiais de compliance, use os padrões de
financeiro-compliance/SKILL.md. Sempre use o sistema tributário brasileiro (Simples,
Lucro Presumido, Lucro Real) e a legislação vigente. Inclua aviso de consulta profissional.
```

### Windsurf
Em Windsurf Settings > AI Rules, adicione:
```
Para tarefas financeiras e de compliance: aplique os frameworks de financeiro-compliance.
Moeda: sempre R$. Sistema tributário: Simples Nacional / Lucro Presumido / Lucro Real.
Legislação: CC, CDC, CLT, LGPD, RFB. Sempre adicionar aviso para consulta profissional.
```

### OpenClaw
```
/skill financeiro-compliance
```

---

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Fluxo de Caixa | `fluxo-caixa/` | Modelagem, projeções e gestão de capital de giro |
| DRE & Balanço | `dre-balanco/` | DRE, balanço patrimonial e análise de resultados BR |
| Impostos BR | `impostos-br/` | Simples Nacional, Lucro Presumido, Lucro Real, MEI |
| LGPD Compliance | `conformidade-lgpd/` | DPIA, políticas de privacidade, contratos de dados |
| Contratos BR | `contratos-br/` | Contratos conforme CC, CDC e CLT brasileiros |
| Gestão de Riscos | `gestao-riscos/` | Matriz de riscos e planos de mitigação |
| Cobrança | `cobranca/` | Scripts de cobrança respeitando o CDC |
| KPIs Financeiros | `kpis-financeiros/` | LTV, CAC, MRR, ARR, payback em R$ |
| Due Diligence | `due-diligence/` | Checklist para M&A, investimento e parcerias |
| Open Finance & PIX | `open-finance-pix/` | Estratégias com PIX, Open Finance e recorrência |

---

## Exemplos de Uso

### Modelar fluxo de caixa de startup
```
Use a skill fluxo-caixa para modelar a projeção de caixa dos próximos 12 meses
de uma startup de SaaS B2B. Receitas: MRR atual R$ 35k, crescimento esperado 15%/mês.
Custos fixos: R$ 28k/mês (equipe + infra). CAC: R$ 1.200. LTV projetado: R$ 8.400.
Quando ficamos sem caixa se o crescimento cair para 8%/mês? Quanto capital precisamos captar?
```

### Orientação tributária para escolha de regime
```
Use a skill impostos-br. Tenho uma empresa de consultoria de TI com faturamento
de R$ 1,8M/ano e margem EBITDA de 35%. Tenho 4 sócios com distribuição de lucros.
Qual regime tributário é mais vantajoso: Simples Nacional Anexo V, Lucro Presumido
ou Lucro Real? Mostre a carga tributária estimada em cada cenário.
```

### Criar política de privacidade LGPD
```
Use a skill conformidade-lgpd para criar a política de privacidade de um marketplace
de serviços que coleta: nome, CPF, email, endereço, dados de pagamento e histórico
de compras. O site atende consumidores e prestadores de serviço.
Inclua: base legal para cada tratamento, direitos dos titulares, contato do DPO
e procedimento de solicitação de exclusão de dados.
```

### Elaborar contrato de prestação de serviços
```
Use a skill contratos-br e elabore um contrato de prestação de serviços de
desenvolvimento de software sob demanda. Partes: empresa desenvolvedora (PJ)
e cliente (empresa). Pontos críticos: escopo, prazo, propriedade intelectual,
sigilo, forma de pagamento por milestone e rescisão. Regime: Civil (não CLT).
```

### Criar matriz de riscos
```
Use a skill gestao-riscos para criar uma matriz de riscos para uma empresa
de logística de última milha operando em São Paulo. Mapeie riscos:
operacionais, regulatórios (ANTT), financeiros, de pessoal (CLT/acidente)
e de tecnologia. Classifique por probabilidade × impacto e sugira mitigações.
```

### Calcular e apresentar KPIs financeiros
```
Use a skill kpis-financeiros. Nossa empresa SaaS tem:
MRR: R$ 87k, churn mensal: 3,2%, CAC: R$ 1.450, ticket médio: R$ 290/mês.
Calcule: LTV, LTV/CAC, payback period, ARR, MRR Churn em R$ e NDR.
Compare com benchmarks SaaS e mostre onde estamos abaixo do esperado.
```

### Conduzir due diligence de aquisição
```
Use a skill due-diligence para criar o checklist completo de due diligence
de uma empresa de e-commerce com faturamento de R$ 4M/ano. Preciso avaliar
para uma possível aquisição. Cubra: financeiro, jurídico, tributário,
trabalhista, contratos, propriedade intelectual e passivos ocultos.
```

---

## Contexto Brasileiro

### Sistema Tributário Brasileiro

O Brasil tem um dos sistemas tributários mais complexos do mundo. As principais modalidades para PMEs:

| Regime | Faturamento Anual | Alíquota Aproximada | Indicado para |
|--------|------------------|---------------------|---------------|
| MEI | Até R$ 81.000 | Valor fixo (~R$ 70/mês) | Autônomo solo |
| Simples Nacional | Até R$ 4,8M | 4-19% dependendo do anexo | PME com margem |
| Lucro Presumido | Até R$ 78M | ~11-13% sobre faturamento | Prestação de serviços |
| Lucro Real | Sem limite | 15-25% sobre lucro real | Alta margem ou prejuízo |

### LGPD — Lei Geral de Proteção de Dados
- Vigente desde 2020, com sanções aplicadas desde 2021
- ANPD (Autoridade Nacional de Proteção de Dados): órgão regulador
- Multa máxima: 2% do faturamento BR, até R$ 50M por infração
- DPO (Encarregado de Dados): obrigatório para empresas que tratam dados em larga escala
- Bases legais para tratamento: consentimento, legítimo interesse, execução de contrato, etc.

### Direito Contratual Brasileiro
- **CC (Código Civil)** — Regula contratos em geral e relações B2B
- **CDC (Código de Defesa do Consumidor)** — Protege relações B2C; cláusulas abusivas são nulas
- **CLT (Consolidação das Leis do Trabalho)** — Relações de emprego; reconhecimento de vínculo é risco
- **Garantia mínima** — CDC exige 90 dias para bens duráveis, 30 para não duráveis

### PIX e Open Finance
- PIX: 42% de todas as transações financeiras BR em 2024
- Parcelamento no PIX (Pix Parcelado/BNPL): crescimento acelerado em 2024-2025
- Open Finance: compartilhamento de dados financeiros entre instituições; regulado pelo BACEN

---

## Configuração de Harness

### Para Claude Code — trecho de CLAUDE.md global a adicionar

```markdown
## Financeiro e Compliance BR
- Análises financeiras sempre em R$ com contexto do sistema tributário brasileiro
- Regime tributário: verificar se MEI, Simples Nacional, Lucro Presumido ou Lucro Real
- LGPD: sempre verificar compliance antes de qualquer feature que colete dados de usuários
- Contratos: verificar conformidade com CC, CDC ou CLT conforme a natureza da relação
- KPIs: usar benchmarks do mercado brasileiro (SaaS BR, e-commerce BR, varejo BR)
- Aviso legal: incluir recomendação de consulta profissional em análises tributárias e jurídicas
```

### Para Cursor — trecho de .cursorrules a adicionar

```
## Financeiro e Compliance (BR)
- Moeda: R$ (Real Brasileiro) em todos os cálculos e apresentações
- Tributário: Simples Nacional, Lucro Presumido, Lucro Real — verifique o regime da empresa
- LGPD obrigatório: qualquer feature de coleta de dados deve ter análise de compliance
- Contratos BR: aplicar CDC para B2C, CC para B2B, CLT para relações de trabalho
- Aviso: recomendar contabilista/advogado para decisões de alto impacto tributário ou jurídico
```

### Para Codex — trecho de AGENTS.md a adicionar

```markdown
## Agente Financeiro e Compliance
Especialidade: gestão financeira e regulatória no mercado brasileiro

Regras:
1. Moeda: R$ com separador decimal por vírgula (padrão BR)
2. Impostos: identificar regime tributário antes de qualquer análise fiscal
3. LGPD: flag automático em features que coletam dados pessoais de titulares BR
4. Contratos: citar artigos do CC, CDC ou CLT relevantes
5. Aviso legal: toda análise jurídica/tributária inclui recomendação de consulta profissional
6. Open Finance/PIX: considerar integração com ecossistema financeiro digital BR
```

---

## Regras

1. **Aviso Legal Obrigatório** — Toda análise tributária, jurídica ou contratual deve incluir o aviso: "Esta análise é orientativa. Consulte um contador/advogado habilitado para decisões com impacto financeiro relevante."

2. **Regime Tributário Primeiro** — Antes de qualquer análise tributária, identifique o regime da empresa (MEI, Simples, Lucro Presumido ou Real). Regimes diferentes têm obrigações e cargas completamente distintas.

3. **LGPD por Padrão** — Qualquer feature, formulário ou sistema que coleta dados pessoais deve ser avaliado sob a perspectiva da LGPD. Identifique a base legal para cada tratamento.

4. **Moeda e Formato BR** — Valores sempre em R$ com vírgula como separador decimal (R$ 1.500,00). Datas no formato DD/MM/AAAA. CNPJ/CPF com pontuação padrão.

5. **Separação Conta PJ/PF** — A confusão entre conta pessoa jurídica e pessoa física é o erro mais custoso do MEI e pequeno empresário brasileiro. Sempre enfatizar a separação.

6. **Conformidade CDC nas Relações B2C** — Em contratos e políticas de e-commerce, sempre verificar: direito de arrependimento 7 dias, garantia mínima, proibição de cláusulas abusivas.

7. **Risco de Vínculo Empregatício** — Ao estruturar contratos com prestadores PJ, sempre alertar sobre os requisitos que configuram relação de emprego (subordinação, habitualidade, pessoalidade, onerosidade).

8. **Prazo de Prescrição** — Mencionar prazos de prescrição relevantes em análises de risco: 5 anos tributário, 2 anos trabalhista (após demissão), 10 anos civil padrão.

9. **Open Finance e BACEN** — Qualquer integração financeira deve estar em conformidade com as regulamentações do BACEN, especialmente para empresas com operações de pagamento, crédito ou câmbio.

10. **Documentação e Evidências** — Para compliance, documentação é a diferença entre uma multa e uma absolvição. Sempre recomendar políticas de retenção de documentos conforme a legislação brasileira.
