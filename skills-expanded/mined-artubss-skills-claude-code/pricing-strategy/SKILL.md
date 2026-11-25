---
name: pricing-strategy
description: "Quando o usuário quer ajuda com decisões de preços, embalagem ou estratégia de monetização. Também use quando o usuário mencionar 'preços', 'tiers de preços', 'freemium', 'teste gratuito', 'embalagem', 'aumento de preço', 'métrica de valor', 'Van Westendorp', 'disposição a pagar' ou 'monetização'. Esta habilidade cobre pesquisa de preços, estrutura de tiers e estratégia de embalagem."
---

# Estratégia de Preços

Você é um especialista em preços e estratégia de monetização de SaaS com acesso a dados de pesquisa de preços e ferramentas de análise. Seu objetivo é ajudar a desenhar preços que capturem valor, impulsionem crescimento e se alinhem com a disposição a pagar dos clientes.

## Antes de Começar

Colete esse contexto (pergunte se não fornecido):

### 1. Contexto do Negócio
- Que tipo de produto? (SaaS, marketplace, e-commerce, serviço)
- Qual é o seu preço atual (se houver)?
- Qual é seu mercado-alvo? (PME, mid-market, enterprise)
- Qual é seu motion de go-to-market? (self-serve, sales-led, híbrido)

### 2. Valor & Competição
- Qual é o valor primário que você entrega?
- Quais alternativas os clientes consideram?
- Como os concorrentes precificam?
- O que faz você diferente/melhor?

### 3. Desempenho Atual
- Qual é sua taxa de conversão atual?
- Qual é sua receita média por usuário (ARPU)?
- Qual é sua taxa de churn?
- Há algum feedback sobre preço de clientes/prospects?

### 4. Objetivos
- Você está otimizando para crescimento, receita ou lucratividade?
- Está tentando subir no mercado ou expandir para baixo?
- Há alguma mudança de preço que você está considerando?

---

## Fundamentos de Preços

### Os Três Eixos de Preços

Toda decisão de preço envolve três dimensões:

**1. Embalagem** — O que está incluído em cada tier?
- Features, limites, nível de suporte
- Como os tiers diferem uns dos outros

**2. Métrica de Preço** — Pelo que você cobra?
- Por usuário, por uso, taxa fixa
- Como o preço escala com o valor

**3. Ponto de Preço** — Quanto você cobra?
- Os valores reais em reais
- O valor percebido vs. custo

### Framework de Preços Baseado em Valor

O preço deve ser baseado no valor entregue, não no custo para servir:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Valor percebido pelo cliente da sua solução            │
│  ────────────────────────────────────────────── R$5000  │
│                                                         │
│  ↑ Valor capturado (sua oportunidade)                   │
│                                                         │
│  Seu preço                                              │
│  ────────────────────────────────────────────── R$2500  │
│                                                         │
│  ↑ Excedente do consumidor (valor que cliente retém)    │
│                                                         │
│  Melhor alternativa                                     │
│  ────────────────────────────────────────────── R$1500  │
│                                                         │
│  ↑ Valor de diferenciação                               │
│                                                         │
│  Seu custo para servir                                  │
│  ────────────────────────────────────────────── R$250   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Insight principal:** Precifique entre a melhor alternativa e o valor percebido. Custo é um piso, não uma base.

---

## Métodos de Pesquisa de Preços

### Van Westendorp Price Sensitivity Meter

O Van Westendorp identifica a faixa de preço aceitável para seu produto.

**As Quatro Perguntas:**

Faça cada respondente:
1. "A que preço você consideraria [produto] tão caro que não consideraria comprá-lo?" (Muito caro)
2. "A que preço você consideraria [produto] tão barato que questionaria sua qualidade?" (Muito barato)
3. "A que preço você consideraria [produto] começando a ficar caro, mas ainda poderia considerar?" (Caro/lado alto)
4. "A que preço você consideraria [produto] uma pechincha — uma ótima compra pelo dinheiro?" (Barato/bom valor)

**Como Analisar:**

1. Plote distribuições cumulativas para cada pergunta
2. Encontre as intersecções:
   - **Ponto de Marginal Barato (PMB):** "Muito barato" cruza "Caro"
   - **Ponto de Marginal Caro (PMC):** "Muito caro" cruza "Barato"
   - **Ponto de Preço Ótimo (PPO):** "Muito barato" cruza "Muito caro"
   - **Ponto de Indiferença (PI):** "Caro" cruza "Barato"

**A faixa de preço aceitável:** PMB até PMC
**Zona de preço ótimo:** Entre PPO e PI

**Dicas de pesquisa:**
- Precisa de 100-300 respondentes para dados confiáveis
- Segmente por persona (diferentes disposições a pagar)
- Use descrições de produto realistas
- Considere adicionar perguntas de intenção de compra

**Saída de Análise Van Westendorp de Exemplo:**

```
Resultados da Análise de Sensibilidade de Preço:
────────────────────────────────────────────────
Ponto de Marginal Barato:         R$145/mês
Ponto de Preço Ótimo:             R$245/mês
Ponto de Indiferença:             R$295/mês
Ponto de Marginal Caro:           R$395/mês

Faixa recomendada: R$245-295/mês
Preço atual: R$195/mês (abaixo do ótimo)
Oportunidade: Aumento de preço de 25-50% sem impacto significativo de demanda
```

### Análise MaxDiff (Best-Worst Scaling)

MaxDiff identifica quais features os clientes mais valorizam, informando decisões de embalagem.

**Como Funciona:**

1. Liste 8-15 features que você poderia incluir
2. Mostre respondentes conjuntos de 4-5 features de cada vez
3. Pergunte: "Qual é MAIS importante? Qual é MENOS importante?"
4. Repita em múltiplos conjuntos até todas as features comparadas
5. Análise estatística produz scores de importância

**Exemplo de Pergunta de Pesquisa:**

```
Qual feature é MAIS importante para você?
Qual feature é MENOS importante para você?

□ Projetos ilimitados
□ Branding customizado
□ Suporte prioritário
□ Acesso a API
□ Analytics avançados
```

**Analisando Resultados:**

Features são ranqueadas por utility score:
- Alta utilidade = Imprescindível (incluir em tier base)
- Utilidade média = Diferenciador (usar para separar tiers)
- Baixa utilidade = Bônus (tier premium ou cortar)

**Usando MaxDiff para Embalagem:**

| Utility Score | Decisão de Embalagem |
|---------------|----------------------|
| Top 20% | Incluir em todos os tiers (pré-requisitos) |
| 20-50% | Usar para diferenciar tiers |
| 50-80% | Apenas tiers mais altos |
| Bottom 20% | Considerar cortar ou add-on premium |

### Pesquisas de Disposição a Pagar

**Método direto (simples mas enviesado):**
"Quanto você pagaria por [produto]?"

**Melhor: Método Gabor-Granger:**
"Você compraria [produto] por [R$X]?" (Sim/Não)
Varie preço entre respondentes para construir curva de demanda.

**Ainda melhor: Análise conjunta:**
Mostre pacotes de produtos em preços diferentes
Respondentes escolhem opção preferida
Análise estatística revela sensibilidade a preço por feature

---

## Métricas de Valor

### O que é uma Métrica de Valor?

A métrica de valor é o que você cobra — deve escalar com o valor que os clientes recebem.

**Boas métricas de valor:**
- Alinham preço com valor entregue
- São fáceis de entender
- Escalam quando cliente cresce
- São difíceis de burlar

### Métricas de Valor Comuns

| Métrica | Melhor Para | Exemplo |
|---------|-------------|---------|
| Por usuário/assento | Ferramentas de colaboração | Slack, Notion |
| Por uso | Consumo variável | AWS, Twilio |
| Por feature | Produtos modulares | Add-ons HubSpot |
| Por contato/registro | CRM, ferramentas de email | Mailchimp, HubSpot |
| Por transação | Pagamentos, marketplaces | Stripe, Shopify |
| Taxa fixa | Produtos simples | Basecamp |
| Compartilhamento de receita | Resultados de alto valor | Plataformas de afiliados |

### Escolhendo Sua Métrica de Valor

**Passo 1: Identifique como clientes obtêm valor**
- Qual resultado eles se importam?
- Como eles medem sucesso?
- Pelo que eles pagariam mais?

**Passo 2: Mapeie uso para valor**

| Padrão de Uso | Valor Entregue | Métrica Potencial |
|---------------|-----------------|-------------------|
| Mais membros de time usam | Mais valor de colaboração | Por usuário |
| Mais dados processados | Mais insights | Por registro/evento |
| Mais receita gerada | ROI direto | Compartilhamento de receita |
| Mais projetos gerenciados | Mais organização | Por projeto |

**Passo 3: Teste para alinhamento**

Pergunte: "Conforme um cliente usa mais de [métrica], recebe mais valor?"
- Se sim → boa métrica de valor
- Se não → preço não se alinha com valor

### Mapeando Uso para Valor: Framework

**1. Instrumente dados de uso**
Rastreie como clientes usam seu produto:
- Frequência de uso de feature
- Métricas de volume (usuários, registros, chamadas de API)
- Métricas de resultado (receita gerada, tempo economizado)

**2. Correlacione com sucesso do cliente**
- Quais padrões de uso predizem retenção?
- Quais padrões de uso predizem expansão?
- Quais clientes pagam mais, e por quê?

**3. Identifique limites de valor**
- Em qual nível de uso clientes "entendem"?
- Em qual nível eles expandem?
- Em qual nível o preço deve aumentar?

**Exemplo de Análise:**

```
Análise de Correlação Uso-Valor:
────────────────────────────────
Segmento: Clientes com alto LTV (>R$50k ARR)
Usuários ativos mensais médios: 15
Projetos médios: 8
Integrações médias: 4

Segmento: Clientes que churnaram
Usuários ativos mensais médios: 3
Projetos médios: 2
Integrações médias: 0

Insight: Valor correlaciona com adoção de time (usuários)
         e profundidade de uso (integrações)

Recomendação: Precifique por usuário, gate de integrações para tiers maiores
```

---

## Estrutura de Tiers

### Quantos Tiers?

**2 tiers:** Simples, escolha clara
- Funciona para: Divisão clara PME vs. Enterprise
- Risco: Pode deixar dinheiro na mesa

**3 tiers:** Padrão da indústria
- Bom tier = Ponto de entrada
- Melhor tier = Recomendado (ancor no melhor)
- Melhor tier = Clientes de alto valor

**4+ tiers:** Mais granularidade
- Funciona para: Ampla gama de tamanhos de cliente
- Risco: Paralisia de decisão, complexidade

### Framework Good-Better-Best

**Tier Bom (Entrada):**
- Objetivo: Remover barreiras de entrada
- Inclui: Features principais, uso limitado
- Preço: Baixo, acessível
- Alvo: Pequenos times, teste antes de comprar

**Tier Melhor (Recomendado):**
- Objetivo: Onde a maioria dos clientes cai
- Inclui: Features completas, limites razoáveis
- Preço: Seu preço "âncora"
- Alvo: Times em crescimento, usuários sérios

**Tier Melhor (Premium):**
- Objetivo: Capturar clientes de alto valor
- Inclui: Tudo, features avançadas, limites mais altos
- Preço: Premium (frequentemente 2-3x "Melhor")
- Alvo: Times maiores, power users, enterprises

### Estratégias de Diferenciação de Tier

**Gating de features:**
- Features básicas em todos os tiers
- Features avançadas em tiers maiores
- Funciona quando features têm diferenças claras de valor

**Limites de uso:**
- Mesmas features, limites diferentes
- Mais usuários, armazenamento, chamadas de API em tiers maiores
- Funciona quando valor escala com uso

**Nível de suporte:**
- Suporte por email → Suporte prioritário → Success dedicado
- Funciona para produtos com complexidade de implementação

**Acesso e customização:**
- Acesso a API, SSO, branding customizado
- Funciona para diferenciação enterprise

### Exemplo de Estrutura de Tier

```
┌────────────────┬─────────────────┬─────────────────┬─────────────────┐
│                │ Inicial         │ Pro             │ Business        │
│                │ R$145/mês       │ R$395/mês       │ R$995/mês       │
├────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Usuários       │ Até 5           │ Até 20          │ Ilimitados      │
│ Projetos       │ 10              │ Ilimitados      │ Ilimitados      │
│ Armazenamento  │ 5 GB            │ 50 GB           │ 500 GB          │
│ Integrações    │ 3               │ 10              │ Ilimitadas      │
│ Analytics      │ Básico          │ Avançado        │ Customizado     │
│ Suporte        │ Email           │ Prioritário     │ Dedicado        │
│ Acesso a API   │ ✗               │ ✓               │ ✓               │
│ SSO            │ ✗               │ ✗               │ ✓               │
│ Audit logs     │ ✗               │ ✗               │ ✓               │
└────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## Embalagem para Personas

### Identificando Personas de Preço

Clientes diferentes têm:
- Disposição a pagar diferentes
- Necessidades de features diferentes
- Processos de compra diferentes
- Percepção de valor diferente

**Segmente por:**
- Tamanho da empresa (freelancer → PME → enterprise)
- Caso de uso (marketing vs. vendas vs. suporte)
- Sofisticação (iniciante → power user)
- Indústria (normas de orçamento diferentes)

### Embalagem Baseada em Persona

**Passo 1: Defina personas**

| Persona | Tamanho | Necessidades | DaP | Exemplo |
|---------|--------|--------------|-----|---------|
| Freelancer | 1 pessoa | Features básicas | Baixa | R$95/mês |
| Pequeno Time | 2-10 | Colaboração | Média | R$245/mês |
| Empresa em Crescimento | 10-50 | Escala, integrações | Mais alta | R$745/mês |
| Enterprise | 50+ | Segurança, suporte | Alta | Customizado |

**Passo 2: Mapeie features para personas**

| Feature | Freelancer | Pequeno Time | Crescimento | Enterprise |
|---------|------------|--------------|-------------|------------|
| Features principais | ✓ | ✓ | ✓ | ✓ |
| Colaboração | — | ✓ | ✓ | ✓ |
| Integrações | — | Limitadas | Completas | Completas |
| Acesso a API | — | — | ✓ | ✓ |
| SSO/SAML | — | — | — | ✓ |
| Audit logs | — | — | — | ✓ |
| Contrato customizado | — | — | — | ✓ |

**Passo 3: Precifique para valor em cada persona**
- Pesquise disposição a pagar por segmento
- Defina preços que capturem valor sem bloquear adoção
- Considere landing pages específicas por segmento

---

## Freemium vs. Teste Gratuito

### Quando Usar Freemium

**Freemium funciona quando:**
- Produto tem efeitos virais/rede
- Usuários gratuitos fornecem valor (conteúdo, dados, referências)
- Mercado grande onde % de conversão impulsiona volume
- Baixo custo marginal para servir usuários gratuitos
- Limites claros de feature/uso para trigger de upgrade

**Riscos do freemium:**
- Usuários gratuitos podem nunca converter
- Desvaloriza percepção do produto
- Custos de suporte para usuários não-pagantes
- Mais difícil aumentar preço depois

**Exemplo: Slack**
- Tier gratuito para pequenos times
- Limite de histórico de mensagens cria trigger de upgrade
- Usuários gratuitos convidam outros (crescimento viral)
- Converte quando time atinge limite

### Quando Usar Teste Gratuito

**Teste gratuito funciona quando:**
- Produto precisa de tempo para demonstrar valor
- Investimento de onboarding/setup requerido
- B2B com comitês de compra
- Pontos de preço mais altos
- Produto é "pegajoso" uma vez configurado

**Melhores práticas de teste:**
- 7-14 dias para produtos simples
- 14-30 dias para produtos complexos
- Acesso completo (não feature-limitado)
- Contagem regressiva clara e lembretes
- Cartão de crédito opcional vs. obrigatório — trade-off

**Cartão de crédito antecipado:**
- Conversão mais alta de teste para pago (40-50% vs. 15-25%)
- Volume de teste mais baixo
- Leads melhor qualificados

### Abordagens Híbridas

**Freemium + Teste:**
- Tier gratuito com features limitadas
- Teste de features premium
- Exemplo: Zoom (40 min gratuito, teste de Pro)

**Teste reverso:**
- Comece com acesso completo
- Após teste, downgrade para tier gratuito
- Exemplo: Veja valor premium, viva com limitações até pronto

---

## Quando Aumentar Preços

### Sinais de que é Hora

**Sinais de mercado:**
- Concorrentes aumentaram preços
- Você está significativamente mais barato que alternativas
- Prospects não reclamam de preço
- Feedback "é tão barato!"

**Sinais de negócio:**
- Taxa de conversão muito alta (>40%)
- Churn muito baixo (<3% mensal)
- Clientes usando mais do que pagam
- Unit economics fortes

**Sinais de produto:**
- Você adicionou valor significativo desde último preço
- Produto é mais maduro/estável
- Novas features justificam preço mais alto

### Estratégias de Aumento de Preço

**1. Grandfather clientes existentes**
- Novo preço apenas para novos clientes
- Clientes existentes mantêm preço antigo
- Pro: Sem risco de churn
- Con: Deixa dinheiro na mesa, cria complexidade

**2. Aumento atrasado para existentes**
- Anuncie aumento 3-6 meses antes
- Dê tempo para travar preço antigo (anual)
- Pro: Justo, impulsiona conversões anuais
- Con: Algum churn, requer comunicação

**3. Aumento atrelado a valor**
- Aumente preço mas adicione features
- "Novo tier Pro com X, Y, Z"
- Pro: Aumento justificado
- Con: Requer valor novo real

**4. Reestruturação de planos**
- Mude planos completamente
- Clientes existentes mapeados para o mais próximo
- Pro: Começar de novo limpo
- Con: Disruptivo, requer mapeamento cuidadoso

### Comunicando Aumentos de Preço

**Para novos clientes:**
- Apenas atualize página de preços
- Nenhum anúncio necessário
- Monitore taxa de conversão

**Para clientes existentes:**

```
Assunto: Atualizações de preços do [Produto]

Olá [Nome],

Estou escrevendo para informar sobre mudanças futuras nos preços do [Produto].

[Contexto: o que você adicionou, por que a mudança está acontecendo]

A partir de [data], nossos preços mudarão de [antigo] para [novo].

Como cliente valioso, [o que isso significa para eles: grandfather, taxa travada, cronograma].

[Se afetados:]
Você tem até [data] para [ação: travar taxa atual, renovar em preço antigo].

[Se grandfather:]
Você continuará em sua taxa atual. Nenhuma ação necessária.

Agradecemos seu apoio contínuo ao [Produto].

[Seu nome]
```

---

## Melhores Práticas de Página de Preços

### Acima da Dobra

- Tabela clara de comparação de tiers
- Tier recomendado destacado
- Toggle mensal/anual
- CTA primária para cada tier

### Apresentação de Tier

- Lidere com tier recomendado (ênfase visual)
- Mostre progressão de valor claramente
- Use checkmarks e limites, não parágrafos
- Âncora para tier mais alto (mostre enterprise primeiro ou economias)

### Elementos Comuns

- [ ] Tabela de comparação de features
- [ ] Para quem é cada tier
- [ ] Seção de FAQ
- [ ] Opção de contato com vendas
- [ ] Destaque de desconto anual
- [ ] Garantia de devolução de dinheiro
- [ ] Logos de clientes/sinais de confiança

### Psicologia de Preço para Aplicar

- **Ancoragem:** Mostre opção de preço mais alto primeiro
- **Efeito isca:** Tier do meio deve ser obviamente melhor valor
- **Preço charm:** R$245 vs. R$250 (para foco em valor)
- **Preço redondo:** R$250 vs. R$245 (para premium)
- **Economias anuais:** Mostre preço mensal mas ofereça desconto anual (17-20%)

---

## Testando Preço

### Métodos para Testar Preço

**1. A/B teste página de preços (arriscado)**
- Visitantes diferentes veem preços diferentes
- Preocupações éticas/legais
- Pode danificar confiança se descoberto

**2. Teste geográfico**
- Teste preços mais altos em novos mercados
- Moedas/regiões diferentes
- Teste mais limpo, alcance limitado

**3. Apenas novo cliente**
- Aumente preços para clientes novos
- Compare taxas de conversão
- Monitore LTV de coorte

**4. Discrição do time de vendas**
- Teste quotes mais altas através de vendas
- Rastreie taxas de fechamento em preços diferentes
- Funciona para GTM sales-led

**5. Teste baseado em features**
- Teste embalagem diferente
- Adicione tier premium em preço mais alto
- Veja adoção sem mudar existente

### O que Medir

- Taxa de conversão em cada ponto de preço
- Receita média por usuário (ARPU)
- Receita total (conversão × preço)
- Valor vitalício do cliente
- Taxa de churn por preço pago
- Sensibilidade de preço por segmento

---

## Preços Enterprise

### Quando Adicionar Preços Customizados

Adicione "Contate Vendas" quando:
- Tamanho de deal excede R$50k+ ARR
- Clientes precisam de contratos customizados
- Implementação/onboarding requerida
- Requisitos de segurança/compliance
- Processos de procurement envolvidos

### Elementos de Tier Enterprise

**Pré-requisitos:**
- SSO/SAML
- Audit logs
- Controles de admin
- SLA de uptime
- Certificações de segurança

**Value-adds:**
- Suporte/success dedicado
- Onboarding customizado
- Sessões de treinamento
- Integrações customizadas
- Entrada prioritária em roadmap

### Estratégias de Preço Enterprise

**Por-assento em escala:**
- Descontos por volume para times grandes
- Exemplo: R$75/usuário (padrão) → R$50/usuário (100+)

**Taxa de plataforma + uso:**
- Taxa base para acesso
- Uso acima de limites
- Exemplo: R$2500/mês base + R$0,05 por chamada de API

**Contratos baseados em valor:**
- Preço atrelado à receita/resultados do cliente
- Exemplo: % de transações, compartilhamento de receita

---

## Checklist de Preços

### Antes de Definir Preços

- [ ] Definir personas de cliente-alvo
- [ ] Pesquisar preços de concorrentes
- [ ] Identificar sua métrica de valor
- [ ] Conduzir pesquisa de disposição a pagar
- [ ] Mapear features para tiers

### Estrutura de Preço

- [ ] Escolher número de tiers
- [ ] Diferenciar tiers claramente
- [ ] Definir pontos de preço baseado em pesquisa
- [ ] Criar estratégia de desconto anual
- [ ] Planejar tier enterprise/customizado

### Validação

- [ ] Testar preços com clientes-alvo
- [ ] Revisar preços com time de vendas
- [ ] Validar que unit economics funcionam
- [ ] Planejar para aumentos de preço
- [ ] Configurar rastreamento para métricas de preço

---

## Perguntas a Fazer

Se precisar de mais contexto:
1. Que pesquisa de preço você conduziu (pesquisas, análise de concorrentes)?
2. Qual é seu ARPU e taxa de conversão atual?
3. Qual é sua métrica de valor primária (pelo que clientes pagam valor)?
4. Quem são suas personas de preço principais (por tamanho, caso de uso)?
5. Você é self-serve, sales-led, ou híbrido?
6. Que mudanças de preço você está considerando?

---

## Skills Relacionadas

- **page-cro**: Para otimizar conversão de página de preços
- **copywriting**: Para copy de página de preços
- **marketing-psychology**: Para princípios de psicologia de preço
- **ab-test-setup**: Para testar mudanças de preço
- **analytics-tracking**: Para rastrear métricas de preço