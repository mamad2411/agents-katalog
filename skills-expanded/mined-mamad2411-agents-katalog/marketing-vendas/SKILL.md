---
name: "marketing-vendas"
description: |
  Skills para funis de vendas, propostas comerciais, tratamento de objeções e
  publicidade digital com contexto do mercado brasileiro. Cobre desde o primeiro
  contato com o prospect até o fechamento, retenção e expansão de receita em R$.
version: 1.0.0
license: MIT
tags:
  - marketing
  - vendas
  - funil
  - proposta
  - ads
  - publicidade
  - objecoes
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read marketing-vendas/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/marketing-vendas.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Marketing, Vendas & Publicidade (Nível PODEROSO)

Skills especializadas para todo o ciclo de receita: atração, conversão e retenção. Cobre funis de vendas B2B e B2C, propostas comerciais, scripts de vendas e estratégias de publicidade digital com foco nas dinâmicas do mercado brasileiro.

Este domínio é ideal para vendedores, gerentes de vendas, profissionais de marketing, donos de negócio e agências que operam no mercado brasileiro e precisam de frameworks práticos, contextualizados e prontos para uso.

## Início Rápido

### Claude Code
```
/read marketing-vendas/SKILL.md
```
Depois acesse a sub-skill pelo contexto:
```
/read marketing-vendas/funil-vendas/SKILL.md
/read marketing-vendas/proposta-comercial/SKILL.md
/read marketing-vendas/script-vendas/SKILL.md
```

### Cursor
Adicione em `.cursor/rules/marketing-vendas.md`:
```
Use as skills de marketing-vendas para qualquer tarefa de vendas, funil ou publicidade.
Sempre considere o contexto do mercado brasileiro: precificação em R$, ciclo de vendas BR,
legislação do CDC e comportamento do consumidor nacional.
```

### Codex
Adicione em `AGENTS.md`:
```markdown
## Marketing, Vendas e Publicidade
Ao criar qualquer material de vendas, use os padrões de marketing-vendas/SKILL.md.
Contexto BR obrigatório: mencione PIX, parcelamento, LGPD em propostas comerciais,
e adapte os scripts para o estilo de comunicação brasileiro (mais relacional, menos frio).
```

### Windsurf
Em Windsurf Settings > AI Rules, adicione:
```
Para tarefas de vendas e marketing: aplique os frameworks de marketing-vendas.
Pricing sempre em R$ com parcelamento. Scripts de vendas com tom consultivo e
relacionamento — o brasileiro compra de quem confia, não apenas de quem tem o melhor preço.
```

### OpenClaw
```
/skill marketing-vendas
```

---

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Funil de Vendas | `funil-vendas/` | Mapeamento, diagnóstico e otimização de funis TOFU/MOFU/BOFU |
| Proposta Comercial | `proposta-comercial/` | Propostas e orçamentos profissionais com precificação BR |
| Objeções de Vendas | `objecoes-vendas/` | Roteiros para tratar objeções: preço, tempo, concorrência |
| Brand Voice | `voz-da-marca/` | Definição e manual de tom de voz da marca |
| Pitch Deck | `deck-de-pitch/` | Apresentações de vendas, pitch para investidores e board |
| Follow-up | `follow-up/` | Sequências de follow-up por email, WhatsApp e telefone |
| Script de Vendas | `script-vendas/` | Scripts para cold call, discovery e fechamento |
| Case Study | `estudo-de-caso/` | Cases de sucesso, depoimentos e provas sociais |
| Promo Strategy | `estrategia-promocional/` | Estratégia de promoções sazonais BR (Black Friday, Natal, etc.) |
| Competitor Analysis | `analise-competitiva/` | Análise competitiva e posicionamento de mercado BR |

---

## Exemplos de Uso

### Diagnosticar e otimizar funil de vendas
```
Use a skill funil-vendas para diagnosticar meu funil atual.
Dados: 10.000 visitantes/mês → 3% viram leads (300 leads) → 15% convertem
em reunião (45 reuniões) → 20% fecham (9 clientes) → ticket médio R$ 2.400.
Identifique onde estou perdendo mais oportunidade e sugira ações concretas
para melhorar a conversão em cada etapa do funil.
```

### Criar proposta comercial B2B
```
Use a skill proposta-comercial e crie uma proposta para consultoria de
processos para uma distribuidora de alimentos de médio porte em SP.
Escopo: mapeamento de processos + treinamento da equipe + 3 meses de acompanhamento.
Investimento: R$ 18.000 (à vista) ou R$ 7.500/mês por 3 meses.
Inclua apresentação do problema, metodologia, entregáveis, cronograma e termos de pagamento.
```

### Tratar objeção de preço
```
Use a skill objecoes-vendas. O cliente disse: "Está caro, vi uma opção
mais barata por R$ 300 a menos". Produto: serviço de consultoria de SEO
R$ 1.500/mês. Mostre como responder essa objeção sem dar desconto desnecessário,
usando argumentos de ROI e valor, não apenas justificativas de custo.
```

### Criar script de follow-up por WhatsApp
```
Use a skill follow-up e crie uma sequência de 5 mensagens de follow-up para
WhatsApp após uma reunião de descoberta com prospect que não deu retorno.
Tom: cordial, direto, não insistente. Variações para dias 1, 3, 7, 14 e 30.
Produto: software de gestão para academias, ticket R$ 297/mês.
```

### Criar pitch deck para investidores
```
Use a skill deck-de-pitch e estruture um pitch deck de 12 slides para captação
de R$ 500k (rodada anjo) de uma startup de edtech B2B para treinamento
corporativo. Inclua: problema, solução, mercado, tração, modelo de negócio,
time, uso dos recursos e próximos passos.
```

### Analisar concorrentes
```
Use a skill analise-competitiva para criar uma análise competitiva da minha
empresa de software de gestão contábil para contadores. Concorrentes: Omie,
Conta Azul, Bling. Eu quero identificar os gaps de posicionamento e encontrar
onde posso competir com vantagem no mercado de pequenas contabilidades.
```

### Criar case de sucesso
```
Use a skill estudo-de-caso para transformar estas notas de cliente em um case
estruturado: "Empresa de 15 funcionários, estava perdendo R$ 25k/mês em
desperdício de estoque. Após 90 dias usando nosso sistema, reduziu perdas
em 78% e aumentou margem em 12 pontos percentuais."
```

### Criar estratégia de Black Friday
```
Use a skill estrategia-promocional e crie o plano completo de Black Friday para
uma loja de moda feminina online. Faturamento médio mensal: R$ 85k.
Histórico da Black Friday passada: R$ 230k (3 dias). Meta deste ano: R$ 300k.
Inclua: cronograma de ações, tiers de desconto, estratégia de aquecimento
(2 semanas antes), email + ads + WhatsApp.
```

---

## Contexto Brasileiro

### Comportamento do Comprador Brasileiro

- **Relacional, não transacional** — Brasileiros compram de quem confiam. Relacionamento antes de pitch.
- **WhatsApp como canal primário** — 93% dos brasileiros usam WhatsApp diariamente; é o CRM informal do país
- **Parcelamento como decisor de compra** — "Cabe no bolso" é mais importante que o preço total para muitos
- **Referência e indicação** — Programas de indicação têm altíssima performance no Brasil
- **Sensibilidade a datas comemorativas** — Black Friday BR é fenômeno; Dia das Mães e Natal são picos de receita

### Ciclo de Vendas B2B no Brasil

- **Tomada de decisão em grupo** — Especialmente em PMEs, decisão envolve sócio/cônjuge/contador
- **Prazo de pagamento** — Boleto 30/60/90 dias é padrão em B2B; PIX está crescendo
- **Contrato e NDA** — PMEs brasileiras assinam mais por confiança; enterprise exige documentação
- **Região faz diferença** — Sul/Sudeste: mais formal; Nordeste/Centro-Oeste: mais relacional
- **Horário de negócios** — Ligações de vendas: 9h-12h e 14h-17h, segunda a sexta

### Sazonalidade de Vendas BR

| Mês | Evento | Oportunidade |
|-----|--------|--------------|
| Jan-Fev | Início do ano / Carnaval | Planejamento anual, resolução de problemas |
| Março | Dia do Consumidor (15/03) | E-commerce e SaaS |
| Maio | Dia das Mães (2º domingo) | Presentes, moda, beleza |
| Junho | Arraiá / Junho | Alimentação, turismo, eventos |
| Agosto | Dia dos Pais (2º domingo) | Presentes, eletrônicos, serviços |
| Novembro | Black Friday (última sexta) | Todos os setores — maior pico do ano |
| Dezembro | Natal e Ano Novo | Presentes, viagens, celebrações |

---

## Configuração de Harness

### Para Claude Code — trecho de CLAUDE.md global a adicionar

```markdown
## Marketing, Vendas e Publicidade
- Ao criar materiais de vendas ou marketing, use os padrões de marketing-vendas/SKILL.md
- Precificação sempre em R$ com opções de parcelamento (PIX, boleto, cartão)
- Scripts de vendas com tom consultivo e relacionamento — evite abordagem agressiva
- Propostas comerciais devem incluir: valor tangível entregue, metodologia, prazo e forma de pagamento
- Follow-up por WhatsApp é o canal mais efetivo no Brasil — priorize scripts para este canal
- Considere a sazonalidade brasileira em campanhas e estratégias promocionais
```

### Para Cursor — trecho de .cursorrules a adicionar

```
## Vendas e Marketing (BR)
- Contexto de mercado brasileiro obrigatório em qualquer material de vendas
- Preços em R$ com breakdown de parcelamento (PIX à vista, 6x, 12x cartão)
- Scripts de vendas: consultivo primeiro, fechamento depois
- Objeções comuns BR: "está caro", "preciso pensar", "minha empresa não tem budget agora"
- White label e LGPD: mencionar compliance em propostas para enterprise
- Sazonalidade: considerar Black Friday, Natal e datas comemorativas BR
```

### Para Codex — trecho de AGENTS.md a adicionar

```markdown
## Agente de Marketing e Vendas
Especialidade: ciclo completo de receita no mercado brasileiro

Regras:
1. Tom consultivo e relacional — nunca agressivo ou insistente em excesso
2. Preços sempre em R$ com opções de parcelamento
3. Scripts de WhatsApp são prioridade para follow-up no BR
4. Propostas B2B: incluir NDA, prazo de pagamento em boleto/PIX, contrato
5. Sazonalidade BR: mapear todas as datas comemorativas relevantes para o setor
6. Indicação e prova social são os gatilhos mais poderosos no mercado BR
```

---

## Regras

1. **Relacionamento Antes do Pitch** — No Brasil, construir confiança antes de apresentar a solução é fundamental. Scripts devem ter fase de rapport antes da descoberta.

2. **Contexto de PIX e Parcelamento** — Toda proposta comercial ou material de vendas deve incluir as opções de pagamento com valores por parcela. "Cabe no bolso" é critério de decisão.

3. **WhatsApp é o CRM do Brasil** — Qualquer sequência de follow-up deve ter versão para WhatsApp. Mensagens de texto curtas, sem pressão, com link para contexto.

4. **ROI em Reais** — Ao argumentar valor, sempre traduza para R$ de retorno, economia ou faturamento adicional. Abstrações não convencem o empresário brasileiro.

5. **Prova Social Localizada** — Cases de sucesso, depoimentos e números de clientes brasileiros têm muito mais peso que exemplos internacionais.

6. **Objeções São Perguntas Disfarçadas** — Quando o cliente diz "está caro", está perguntando "vale o preço?". Ensinar a decodificar e responder objeções é mais valioso que scripts de fechamento.

7. **Funil é Processo, Não Evento** — Qualquer diagnóstico de funil deve analisar cada etapa individualmente com métricas específicas (taxa de conversão por etapa).

8. **LGPD no Processo de Vendas** — Cold email e prospecção ativa devem respeitar a LGPD. Sempre obtenha consentimento explícito para comunicações marketing.

9. **Análise Competitiva Honesta** — Ao analisar concorrentes, seja objetivo. Identifique onde o concorrente é genuinamente melhor e onde há gap a explorar.

10. **Métricas de Vaidade vs. Métricas de Negócio** — Seguidores, curtidas e impressões não pagam boletos. Sempre alinhe métricas de marketing a resultados de receita.
