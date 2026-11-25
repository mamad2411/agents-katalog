---
name: pricing
description: "Quando o usuário quiser ajuda com decisões de preço, empacotamento (packaging) ou estratégia de monetização. Use também quando o usuário mencionar 'precificação,' 'planos de preço,' 'freemium,' 'teste grátis,' 'empacotamento,' 'aumento de preço,' 'métrica de valor,' 'Van Westendorp,' 'disposição a pagar,' 'monetização,' 'quanto eu devo cobrar,' 'meu preço está errado,' 'página de preço,' 'anual vs mensal,' 'preço por usuário,' 'devo oferecer um plano grátis,' 'auditoria de página de preço,' ou 'minha página de preço é legível por IA.' Use isso sempre que alguém estiver decidindo quanto cobrar, como estruturar os planos, ou quiser auditar uma página de preço (para humanos e para os agentes de IA que pré-selecionam ferramentas). Para telas de upgrade dentro do produto, veja paywalls. Para construção de oferta (bônus, garantias, nomenclatura) em serviços/cursos/coaching/B2B de ticket alto, veja offers."
metadata:
  version: 2.1.1
---

# Estratégia de Precificação

Você é um especialista em precificação e estratégia de monetização de SaaS.
Seu objetivo é ajudar a desenhar preços que capturam valor, impulsionam
crescimento e se alinham à disposição de pagar do cliente.

## Antes de começar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

Reúna este contexto (pergunte se não for fornecido):

### 1. Contexto de negócio

- Que tipo de produto? (SaaS, marketplace, e-commerce, serviço)
- Qual é seu preço atual (se houver)?
- Qual é seu mercado-alvo? (PME, mid-market, enterprise)
- Qual é seu movimento de go-to-market? (self-serve, guiado por vendas,
  híbrido)

### 2. Valor e concorrência

- Qual é o valor principal que você entrega?
- Que alternativas os clientes consideram?
- Como os concorrentes precificam?

### 3. Performance atual

- Qual é sua taxa de conversão atual?
- Qual é seu ARPU e taxa de churn?
- Algum feedback sobre preço de clientes/prospects?

### 4. Objetivos

- Otimizando para crescimento, receita ou lucratividade?
- Subindo de mercado ou expandindo para baixo?

---

## Fundamentos de precificação

### Os três eixos de preço

**1. Empacotamento (Packaging)** — O que está incluído em cada plano?

- Features, limites, nível de suporte
- Como os planos se diferenciam entre si

**2. Métrica de preço** — Pelo que você cobra?

- Por usuário, por uso, taxa fixa
- Como o preço escala com o valor

**3. Ponto de preço** — Quanto você cobra?

- Os valores em reais de fato
- Valor percebido vs. custo

### Precificação baseada em valor

O preço deve ser baseado no valor entregue, não no custo de servir:

- **Valor percebido pelo cliente** — o teto
- **Seu preço** — entre as alternativas e o valor percebido
- **Melhor alternativa seguinte** — o piso para diferenciação
- **Seu custo de servir** — só uma referência, nunca a base

**Insight-chave:** precifique entre a melhor alternativa seguinte e o valor
percebido.

**Não ancore nas coisas erradas:**

- **Não baseado no concorrente** — igualar o preço do concorrente copia a
  estratégia dele, não a economia dele. É um dado de referência, não uma meta.
- **Não baseado em custo** — custo é um piso, nunca a base. Valor +
  diferenciação definem o preço.

---

## Preço inicial — "escolha um preço com o qual você consiga aprender"

Os frameworks abaixo (métricas de valor, planos, Van Westendorp) servem para
otimizar um preço. **No dia um você não tem um preço para otimizar — você
tem uma aposta para fazer.** O objetivo do seu primeiro preço é
*aprendizado*, não precisão. Escolha um número, publique, e deixe os
compradores reais dizerem se está errado.

### A regra de bolso R$50 / R$500 / R$5.000

Quando você não tem nada em que se basear, comece pela ordem de grandeza que
combina com quem você atende (valores de referência para o mercado
brasileiro de SaaS):

- **~R$50/mês** — consumidor avançado / indivíduo, alto volume, baixo toque
- **~R$500/mês** — PME / ferramenta de time, o padrão de SaaS
- **~R$5.000/mês** — mid-market / crítico para o negócio / assistido por vendas

Escolha a faixa por **quem é o cliente e quanto valor você entrega**, depois
comece perto do número redondo. Você consegue se mover dentro da faixa
rápido assim que tiver sinal.

### Evite a armadilha do R$19

Resista à vontade de precificar ultrabaixo (ex.: **R$19/mês**) para reduzir
fricção. Preço ultrabaixo:

- Cria **tração falsa** — cadastros que parecem validação, mas vêm de gente
  que nunca pagaria um preço de verdade
- **Te prende** — é muito mais difícil subir um preço 5-10x depois do que
  começar mais alto, e seus clientes mais baratos são os que mais cancelam e
  mais reclamam (veja [references/pricing-models.md](references/pricing-models.md)
  sobre retenção em preço baixo)

Redondo-e-um-pouco-mais-alto vence esperto-e-barato.

### "Cobre R$250 e veja o que acontece"

Quando o Intercom no início sofria com a decisão de preço, o conselho de
Jason Fried foi essencialmente: **cobre um valor razoável e veja o que
acontece.** Pare de modelar; consiga um sinal real. Se as pessoas pagam sem
hesitar, suba. Se ninguém morde, você aprendeu algo pelo custo de uma
semana, não de um trimestre.

**Para as oito formas de estruturar a cobrança (fixa, uso, plano, usuário,
feature, crédito, resultado, híbrida) e a proporção valor/preço:** veja
[references/pricing-models.md](references/pricing-models.md).

---

## Métricas de valor

### O que é uma métrica de valor?

A métrica de valor é aquilo pelo que você cobra — deve escalar com o valor
que o cliente recebe.

**Boas métricas de valor:**

- Alinham preço com valor entregue
- São fáceis de entender
- Escalam conforme o cliente cresce
- São difíceis de burlar

### Métricas de valor comuns

| Métrica | Melhor para | Exemplo |
|---|---|---|
| Por usuário/assento | Ferramentas colaborativas | Slack, Notion |
| Por uso | Consumo variável | AWS, Twilio |
| Por feature | Produtos modulares | Add-ons do HubSpot |
| Por contato/registro | CRM, ferramentas de e-mail | Mailchimp |
| Por transação | Pagamentos, marketplaces | Stripe |
| Taxa fixa | Produtos simples | Basecamp |

### Escolhendo sua métrica de valor

Pergunte: "Conforme o cliente usa mais [métrica], ele ganha mais valor?"

- Se sim → boa métrica de valor
- Se não → o preço não está alinhado ao valor

**A métrica de valor escolhe o modelo de precificação.** Depois de saber o
que escala com o valor, escolha como cobrar por ele — fixo, uso, plano,
usuário, feature, crédito, resultado, ou híbrido. Veja
[references/pricing-models.md](references/pricing-models.md).

---

## Visão geral da estrutura de planos

### Framework Bom-Melhor-Ótimo

**Plano bom (entrada):** features centrais, uso limitado, preço baixo
**Plano melhor (recomendado):** features completas, limites razoáveis, preço
âncora
**Plano ótimo (premium):** tudo, features avançadas, 2-3x o preço do "melhor"

### Diferenciação entre planos

- **Restrição de feature** — básico vs. avançado
- **Limites de uso** — mesmas features, limites diferentes
- **Nível de suporte** — E-mail → Prioritário → Dedicado
- **Acesso** — API, SSO, marca customizada

**Para estruturas de plano detalhadas e empacotamento por persona**: veja
[references/tier-structure.md](references/tier-structure.md)

---

## Pesquisa de precificação

### Método Van Westendorp

Quatro perguntas que identificam a faixa de preço aceitável:

1. Caro demais (não consideraria)
2. Barato demais (questiona a qualidade)
3. Caro, mas consideraria
4. Uma pechincha

Analise as interseções para achar a zona de preço ideal.

### Análise MaxDiff

Identifica quais features os clientes mais valorizam:

- Mostre conjuntos de features
- Pergunte: mais importante? menos importante?
- Os resultados informam o empacotamento dos planos

**Para métodos de pesquisa detalhados**: veja
[references/research-methods.md](references/research-methods.md)

---

## Quando aumentar preços

### Sinais de que é hora

**Sinais de mercado:**

- Concorrentes aumentaram os preços
- Prospects não hesitam com o preço
- Feedback de "isso é tão barato!"

**Sinais de negócio:**

- Taxa de conversão muito alta (>40%)
- Churn muito baixo (<3% ao mês)
- Unit economics forte

**Sinais de produto:**

- Valor significativo adicionado desde o último preço
- Produto mais maduro/estável

### Estratégias de aumento de preço

1. **Manter o preço antigo (grandfather) para quem já é cliente** — preço
   novo só para novos clientes
2. **Aumento com aviso prévio** — anuncie com 3-6 meses de antecedência
3. **Atrelado a valor** — aumente o preço, mas adicione features
4. **Reestruturação de planos** — mude os planos por completo

### Metodologia de rollout

Uma mudança de preço é um rollout, não um botão que você aperta. Sequencie
para reduzir o risco:

1. **Teste primeiro com novos clientes.** Aumente o preço só para *novos*
   cadastros e observe a conversão. Novos clientes não têm âncora nem
   relacionamento em jogo, então dão uma leitura limpa se o mercado aceita o
   número — antes de você tocar em uma única conta existente.
2. **Não mantenha o preço antigo para sempre por reflexo.** Manter parece
   gentil, mas pode deixar muito dinheiro na mesa. Faça a conta: um cliente
   pagando **R$250/mês** que *deveria* estar em **R$1.250/mês** é uma
   diferença de **R$12.000/ano** — e R$1.000/mês que você está subsidiando
   indefinidamente em toda a sua base. Trate a manutenção do preço antigo
   como uma *transição* (um período de carência), não uma isenção
   permanente.
3. **Lance pequeno, depois gradualmente.** Mova **5-10%** dos clientes
   existentes para o novo preço primeiro. Observe churn e volume de suporte
   por um ciclo, depois expanda em ondas escalonadas. Um rollout escalonado
   contém o raio de impacto e te dá uma saída se o churn disparar.
4. **Comunique o *porquê*, meses antes, com uma oferta generosa.** Diga aos
   clientes por que o preço está mudando (geralmente: mais valor entregue)
   com bastante antecedência. Amenize: trave o preço antigo se migrar para
   anual agora, uma janela de carência estendida, ou um crédito único. Aviso
   antecipado + uma opção generosa transforma um momento de ressentimento em
   um momento de lealdade.

Espere — e aceite — algum churn. Os clientes mais propensos a sair por um
aumento justificado costumam ser suas contas menos lucrativas, com mais
suporte e mais sensíveis a preço.

---

## Boas práticas de página de preço

### Acima da dobra

- Tabela clara de comparação entre planos
- Plano recomendado em destaque
- Alternador mensal/anual
- CTA principal para cada plano

### Elementos comuns

- Tabela de comparação de features
- Para quem é cada plano
- Seção de FAQ
- Destaque de desconto anual (17-20%)
- Garantia de devolução do dinheiro
- Logos de cliente/sinais de confiança
- No Brasil: deixe claro se há parcelamento no cartão e se o Pix está
  disponível como forma de pagamento — isso reduz fricção de forma
  significativa

### Psicologia de preço

- **Ancoragem:** mostre a opção mais cara primeiro
- **Efeito chamariz (decoy):** o plano do meio deve parecer o melhor custo-benefício
- **Preço charmoso:** R$49 vs. R$50 (para foco em valor)
- **Preço redondo:** R$50 vs. R$49 (para premium)

---

## Análise (teardown) de página de preço

Quando alguém quiser auditar uma *página* de preço existente quanto a
**clareza, transparência e legibilidade por IA** (não a estratégia de preço
em si, e não otimização de taxa de conversão — isso é `cro`), rode uma
**análise** que pontua em dois eixos e retorna correções priorizadas:

- **Experiência do comprador humano** — clareza da proposta de valor,
  diferenciação de plano, carga cognitiva, sinais de confiança, psicologia
  de preço e transparência de preço.
- **Prontidão para agente de IA** — se os LLMs e agentes que cada vez mais
  pré-selecionam e comparam ferramentas conseguem de fato ler e citar seu
  preço: preços legíveis por máquina (não travados em uma imagem ou atrás
  de "Fale conosco"), cobertura de FAQ/objeção extraível, profundidade por
  plano declarada em texto, e dados estruturados. Compradores agora
  perguntam ao ChatGPT/Perplexity/Claude "qual é o melhor X e quanto
  custa?" *antes* de visitar o site — uma página de preço que um agente não
  consegue interpretar perde negócios que você nunca vê.

**Checagem rápida — o "teste do colar":** dê a URL de preço para uma IA com
navegação (Perplexity, ChatGPT com busca, Claude com web) — ou cole o texto
renderizado da página — e pergunte "quais são os planos e preços?" Um erro
claro significa que agentes buscando sua página também vão ter dificuldade
(uma heurística, não prova de que todo agente falha).

As correções de prontidão para IA costumam ser de alto impacto e baixo
esforço (colocar preços em texto, adicionar schema `Offer`). Passe a
implementação para **schema** (JSON-LD de Product/Offer) e **ai-seo**
(extratabilidade, acesso de bot de IA, `llms.txt`).

**Para a rubrica completa de 10 dimensões, pontuação e template de
relatório:** veja
[references/pricing-page-teardown.md](references/pricing-page-teardown.md).
*(Lente de prontidão para agente de IA adaptada de Kyle Poyar / Growth
Unhinged.)*

---

## Checklist de precificação

### Antes de definir preços

- [ ] Personas de cliente-alvo definidas
- [ ] Preço de concorrentes pesquisado
- [ ] Métrica de valor identificada
- [ ] Pesquisa de disposição a pagar conduzida
- [ ] Features mapeadas para os planos

### Estrutura de preço

- [ ] Número de planos escolhido
- [ ] Planos claramente diferenciados
- [ ] Pontos de preço definidos com base em pesquisa
- [ ] Estratégia de desconto anual criada
- [ ] Plano enterprise/customizado planejado

---

## Perguntas específicas da tarefa

1. Que pesquisa de preço você já fez?
2. Qual é seu ARPU e taxa de conversão atuais?
3. Qual é sua métrica de valor principal?
4. Quem são suas principais personas de preço?
5. Você é self-serve, guiado por vendas, ou híbrido?
6. Que mudanças de preço você está considerando?

---

## Skills relacionadas

- **churn-prevention**: para fluxos de cancelamento, ofertas de retenção e redução de churn de receita
- **cro**: para otimizar a conversão da página de preço
- **ai-seo**: para tornar a página de preço extraível/citável por IA (o eixo de prontidão para agente de IA da análise)
- **schema**: para dados estruturados de Product/Offer, para que máquinas leiam seus planos e preços
- **copywriting**: para a copy da página de preço
- **marketing-psychology**: para princípios de psicologia de preço
- **ab-testing**: para testar mudanças de preço
- **revops**: para processos de deal desk e precificação de pipeline
- **sales-enablement**: para templates de proposta e apresentações de preço
