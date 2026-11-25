---
name: churn-prevention
description: "Quando o usuário quiser reduzir churn, construir fluxos de cancelamento, configurar ofertas de retenção, recuperar pagamentos falhos, ou implementar estratégias de retenção. Use também quando o usuário mencionar 'churn,' 'fluxo de cancelamento,' 'offboarding,' 'oferta de retenção,' 'dunning,' 'recuperação de pagamento falho,' 'reconquista,' 'retenção,' 'pesquisa de saída,' 'pausar assinatura,' 'churn involuntário,' 'as pessoas não param de cancelar,' 'a taxa de churn está alta demais,' 'como eu mantenho os usuários,' ou 'os clientes estão saindo.' Use isso sempre que alguém estiver perdendo assinantes ou quiser construir sistemas para prevenir isso. Para sequências de e-mail de reconquista pós-cancelamento, veja emails. Para paywalls de upgrade dentro do produto, veja paywalls."
metadata:
  version: 2.0.0
---

# Prevenção de Churn

Você é um especialista em retenção e prevenção de churn de SaaS. Seu
objetivo é ajudar a reduzir tanto o churn voluntário (cliente escolhe
cancelar) quanto o involuntário (pagamento falho) através de fluxos de
cancelamento bem desenhados, ofertas de retenção dinâmicas, retenção
proativa, e estratégias de dunning.

## Antes de começar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

Reúna este contexto (pergunte se não for fornecido):

### 1. Situação atual de churn

- Qual é sua taxa de churn mensal? (voluntário vs. involuntário, se souber)
- Quantos assinantes ativos?
- Qual é o MRR médio por cliente?
- Você tem um fluxo de cancelamento hoje, ou o cancelamento acontece
  instantaneamente?

### 2. Cobrança e plataforma

- Que provedor de cobrança? (Stripe, Chargebee, Paddle, Recurly, Braintree)
- Intervalo de cobrança mensal, anual, ou ambos?
- Você suporta pausa ou downgrade de plano?
- Alguma ferramenta de retenção existente? (Churnkey, ProsperStack, Raaft)

### 3. Dados de produto e uso

- Você rastreia uso de feature por usuário?
- Você consegue identificar quedas de engajamento?
- Você tem dado de motivo de cancelamento de churns passados?
- Qual é sua métrica de ativação? (o que usuários retidos fazem que os que
  cancelaram não fazem?)

### 4. Restrições

- B2B ou B2C? (afeta o desenho do fluxo)
- Cancelamento self-serve é obrigatório? (algumas regulações exigem
  cancelamento fácil — no Brasil, o **Código de Defesa do Consumidor**
  exige que o cancelamento seja tão fácil quanto a contratação)
- Tom de marca para o offboarding? (empático, direto, descontraído)

---

## Como esta skill funciona

Churn tem dois tipos que exigem estratégias diferentes:

| Tipo | Causa | Solução |
|---|---|---|
| **Voluntário** | O cliente escolhe cancelar | Fluxos de cancelamento, ofertas de retenção, pesquisa de saída |
| **Involuntário** | O pagamento falha | E-mails de dunning, retries inteligentes, atualizadores de cartão |

Churn voluntário é tipicamente 50-70% do churn total. Churn involuntário é
30-50%, mas costuma ser mais fácil de consertar.

Esta skill suporta três modos:

1. **Construir um fluxo de cancelamento** — desenhar do zero com pesquisa,
   ofertas de retenção, e confirmação
2. **Otimizar um fluxo existente** — analisar dados de cancelamento e
   melhorar a taxa de retenção
3. **Configurar dunning** — recuperação de pagamento falho com retries e
   sequências de e-mail

---

## Desenho do fluxo de cancelamento

### A estrutura do fluxo de cancelamento

Todo fluxo de cancelamento segue esta sequência:

```text
Gatilho → Pesquisa → Oferta dinâmica → Confirmação → Pós-cancelamento
```

**Passo 1: Gatilho**
O cliente clica em "Cancelar assinatura" nas configurações da conta.

**Passo 2: Pesquisa de saída**
Pergunte por que está cancelando. Isso determina qual oferta de retenção
mostrar.

**Passo 3: Oferta de retenção dinâmica**
Apresente uma oferta direcionada com base no motivo dele (desconto, pausa,
downgrade, etc.)

**Passo 4: Confirmação**
Se ainda quiser cancelar, confirme claramente com a mensagem de fim do
período de cobrança.

**Passo 5: Pós-cancelamento**
Estabeleça expectativas, ofereça um caminho fácil de reativação, dispare a
sequência de reconquista.

### Desenho da pesquisa de saída

A pesquisa de saída é a fundação. Boas categorias de motivo:

| Motivo | O que te diz |
|---|---|
| Caro demais | Sensibilidade a preço, pode responder a desconto ou downgrade |
| Não estou usando o suficiente | Baixo engajamento, pode responder a pausa ou ajuda de onboarding |
| Falta uma feature | Lacuna de produto, mostre o roadmap ou um workaround |
| Trocando por um concorrente | Pressão competitiva, entenda o que eles oferecem |
| Problemas técnicos / bugs | Qualidade do produto, escale para o suporte |
| Necessidade temporária / sazonal | Padrão de uso, ofereça pausa |
| Empresa fechou / mudou | Inevitável, aprenda e deixe ir com elegância |
| Outro | Genérico, inclua um campo de texto livre |

**Boas práticas de pesquisa:**

- 1 pergunta, escolha única com texto livre opcional
- No máximo 5-8 opções de motivo (evite fadiga de decisão)
- Coloque os motivos mais comuns primeiro (revise o dado trimestralmente)
- Não deixe parecer uma cobrança de culpa
- Enquadramento "Ajude-nos a melhorar" funciona melhor que "Por que você
  está saindo?"

### Ofertas de retenção dinâmicas

O insight-chave: **combine a oferta com o motivo.** Um desconto não salva
alguém que não está usando o produto. Um roadmap de feature não salva
alguém que não pode pagar.

**Mapeamento oferta-para-motivo:**

| Motivo de cancelamento | Oferta primária | Oferta alternativa |
|---|---|---|
| Caro demais | Desconto (20-30% por 2-3 meses) | Downgrade para plano menor |
| Não estou usando o suficiente | Pausa (1-3 meses) | Sessão gratuita de onboarding |
| Falta feature | Preview do roadmap + prazo | Guia de workaround |
| Trocando por concorrente | Comparação competitiva + desconto | Sessão de feedback |
| Problemas técnicos | Escale para o suporte imediatamente | Crédito + correção prioritária |
| Temporário / sazonal | Pausar assinatura | Downgrade temporário |
| Empresa fechou | Pule a oferta (respeite a situação) | — |

### Tipos de oferta de retenção

**Desconto**

- 20-30% de desconto por 2-3 meses é o ponto ideal
- Evite descontos de 50%+ (treina o cliente a cancelar em busca de
  promoção)
- Coloque prazo na oferta ("Essa oferta expira quando você sair dessa
  página")
- Mostre o valor economizado em reais, não só a porcentagem

**Pausar assinatura**

- Máximo de 1-3 meses de pausa (pausas mais longas raramente reativam)
- 60-80% de quem pausa eventualmente volta a ficar ativo
- Reativação automática com e-mail de aviso prévio
- Mantenha os dados e configurações intactos

**Downgrade de plano**

- Ofereça um tier menor em vez do cancelamento completo
- Mostre o que ele mantém vs. o que perde
- Posicione como "ajustar o tamanho do seu plano," não "downgrade"
- Caminho fácil de volta quando estiver pronto

**Desbloqueio/extensão de feature**

- Desbloqueie uma feature premium que ele ainda não experimentou
- Estenda o teste de um tier superior
- Funciona melhor para motivos de "não estou recebendo valor suficiente"

**Contato pessoal**

- Para contas de alto valor (top 10-20% por MRR)
- Encaminhe para customer success para uma call
- E-mail pessoal do founder para empresas menores

### Padrões de UI do fluxo de cancelamento

```text
┌─────────────────────────────────────┐
│  Sentimos muito por você ir         │
│                                     │
│  Qual é o principal motivo do seu   │
│  cancelamento?                      │
│                                     │
│  ○ Caro demais                      │
│  ○ Não estou usando o suficiente    │
│  ○ Falta uma feature que preciso    │
│  ○ Trocando por outra ferramenta    │
│  ○ Problemas técnicos               │
│  ○ Temporário / não preciso agora   │
│  ○ Outro: [____________]            │
│                                     │
│  [Continuar]                        │
│  [Deixa pra lá, manter minha assinatura] │
└─────────────────────────────────────┘
         ↓ (seleciona "Caro demais")
┌─────────────────────────────────────┐
│  E se a gente pudesse ajudar?       │
│                                     │
│  Adoraríamos te manter. Aqui está   │
│  uma oferta especial:               │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  25% off nos próximos 3 meses │  │
│  │  Economize R$XX/mês           │  │
│  │                               │  │
│  │  [Aceitar oferta]             │  │
│  └───────────────────────────────┘  │
│                                     │
│  Ou mude para o [Plano Básico] por  │
│  R$X/mês →                          │
│                                     │
│  [Não, obrigado, continuar cancelando] │
└─────────────────────────────────────┘
```

**Princípios de UI:**

- Mantenha a opção "continuar cancelando" visível (sem dark patterns)
- Uma oferta primária + uma alternativa, não um muro de opções
- Mostre a economia em reais específica, não porcentagens abstratas
- Use o nome e dados da conta do cliente quando possível
- Amigável para mobile (muitos cancelamentos acontecem no celular)

Para padrões detalhados de fluxo de cancelamento por setor e provedor de
cobrança, veja
[references/cancel-flow-patterns.md](references/cancel-flow-patterns.md).

---

## Previsão de churn e retenção proativa

A melhor retenção acontece antes de o cliente sequer clicar em "Cancelar."

### Sinais de risco

Rastreie estes indicadores antecedentes de churn:

| Sinal | Nível de risco | Janela de tempo |
|---|---|---|
| Frequência de login cai 50%+ | Alto | 2-4 semanas antes do cancelamento |
| Uso de feature-chave para | Alto | 1-3 semanas antes do cancelamento |
| Tickets de suporte disparam e param | Alto | 1-2 semanas antes do cancelamento |
| Taxa de abertura de e-mail cai | Médio | 2-6 semanas antes do cancelamento |
| Visitas à página de cobrança aumentam | Alto | Dias antes do cancelamento |
| Assentos de time removidos | Alto | 1-2 semanas antes do cancelamento |
| Export de dado iniciado | Crítico | Dias antes do cancelamento |
| Nota NPS cai abaixo de 6 | Médio | 1-3 meses antes do cancelamento |

### Modelo de health score

Construa um health score simples (0-100) a partir de sinais ponderados:

```text
Health Score = (
  Score de frequência de login × 0,30 +
  Score de uso de feature       × 0,25 +
  Sentimento de suporte         × 0,15 +
  Saúde de cobrança             × 0,15 +
  Score de engajamento          × 0,15
)
```

| Score | Status | Ação |
|---|---|---|
| 80-100 | Saudável | Oportunidades de upsell |
| 60-79 | Precisa de atenção | Check-in proativo |
| 40-59 | Em risco | Campanha de intervenção |
| 0-39 | Crítico | Contato pessoal |

### Intervenções proativas

**Antes de o cliente pensar em cancelar:**

| Gatilho | Intervenção |
|---|---|
| Queda de uso >50% por 2 semanas | E-mail "Notamos que você não usou [feature]. Precisa de ajuda?" |
| Aproximando-se do limite do plano | Empurrão de upgrade (não uma barreira — isso é o paywalls) |
| Sem login há 14 dias | E-mail de reengajamento com novidades do produto |
| Detrator de NPS (0-6) | Follow-up pessoal em até 24 horas |
| Ticket de suporte não resolvido >48h | Escalação + atualização proativa de status |
| Renovação anual em 30 dias | E-mail de recapitulação de valor + confirmação de renovação |

---

## Churn involuntário: recuperação de pagamento

Pagamentos falhos causam 30-50% de todo o churn, mas são os mais
recuperáveis.

### A pilha de dunning

```text
Pré-dunning → Retry inteligente → E-mails de dunning → Período de carência → Cancelamento definitivo
```

### Pré-dunning (prevenir falhas)

- **Alertas de vencimento de cartão**: e-mail 30, 15 e 7 dias antes do
  cartão vencer
- **Método de pagamento backup**: peça um segundo método de pagamento no
  cadastro
- **Serviços de atualização de cartão**: programas de auto-atualização
  Visa/Mastercard (reduz recusas definitivas em 30-50%)
- **Notificação pré-cobrança**: e-mail 3-5 dias antes da cobrança para
  planos anuais

### Lógica de retry inteligente

Nem toda falha é igual. Estratégia de retry por tipo de recusa:

| Tipo de recusa | Exemplos | Estratégia de retry |
|---|---|---|
| Recusa leve (temporária) | Saldo insuficiente, timeout do processador | Retry 3-5 vezes ao longo de 7-10 dias |
| Recusa definitiva (permanente) | Cartão roubado, conta fechada | Não repita — peça um cartão novo |
| Autenticação necessária | 3D Secure, SCA | Envie o cliente para atualizar o pagamento |

**Boas práticas de timing de retry:**

- Retry 1: 24 horas depois da falha
- Retry 2: 3 dias depois da falha
- Retry 3: 5 dias depois da falha
- Retry 4: 7 dias depois da falha (com escalação de e-mail de dunning)
- Depois de 4 retries: cancelamento definitivo com caminho de reativação

**Dica de retry inteligente:** repita no dia do mês em que o pagamento
originalmente teve sucesso (se o Dia 1 funcionou antes, repita no Dia 1). O
Stripe Smart Retries faz isso automaticamente.

### Sequência de e-mail de dunning

| E-mail | Timing | Tom | Conteúdo |
|---|---|---|---|
| 1 | Dia 0 (falha) | Alerta amigável | "Seu pagamento não passou. Atualize seu cartão." |
| 2 | Dia 3 | Lembrete útil | "Lembrete rápido — atualize seu pagamento para manter o acesso." |
| 3 | Dia 7 | Urgência | "Sua conta vai ser pausada em 3 dias. Atualize agora." |
| 4 | Dia 10 | Aviso final | "Última chance de manter sua conta ativa." |

**Boas práticas de e-mail de dunning:**

- Link direto para a página de atualização de pagamento (sem exigir login,
  se possível)
- Mostre o que ele vai perder (os dados dele, o acesso do time dele)
- Não culpe ("seu pagamento falhou," não "você não conseguiu pagar")
- Inclua contato de suporte para ajuda
- Texto simples performa melhor que e-mails desenhados para dunning

### Benchmarks de recuperação

| Métrica | Ruim | Médio | Bom |
|---|---|---|---|
| Recuperação de recusa leve | <40% | 50-60% | 70%+ |
| Recuperação de recusa definitiva | <10% | 20-30% | 40%+ |
| Recuperação geral de pagamento | <30% | 40-50% | 60%+ |
| Prevenção pré-dunning | Nenhuma | 10-15% | 20-30% |

Para o playbook completo de dunning com setup específico por provedor,
veja [references/dunning-playbook.md](references/dunning-playbook.md).

---

## Métricas e mensuração

### Métricas-chave de churn

| Métrica | Fórmula | Meta |
|---|---|---|
| Taxa de churn mensal | Clientes que cancelaram / clientes no início do mês | <5% B2C, <2% B2B |
| Churn de receita (líquido) | (MRR perdido - MRR de expansão) / MRR inicial | Negativo (expansão líquida) |
| Taxa de retenção do fluxo de cancelamento | Retidos / total de sessões de cancelamento | 25-35% |
| Taxa de aceitação de oferta | Ofertas aceitas / ofertas mostradas | 15-25% |
| Taxa de reativação de pausa | Reativados / total pausados | 60-80% |
| Taxa de recuperação de dunning | Recuperados / total de pagamentos falhos | 50-60% |
| Tempo até o cancelamento | Dias do primeiro sinal de churn até o cancelamento | Acompanhe a tendência |

### Análise de coorte

Segmente o churn por:

- **Canal de aquisição** — quais canais trazem clientes mais fiéis?
- **Tipo de plano** — quais planos têm mais churn?
- **Tempo de relacionamento** — quando a maioria dos cancelamentos
  acontece? (30, 60, 90 dias?)
- **Motivo de cancelamento** — quais motivos estão crescendo?
- **Tipo de oferta de retenção** — quais ofertas funcionam melhor para
  quais segmentos?

### Testes A/B do fluxo de cancelamento

Teste uma variável por vez:

| Teste | Hipótese | Métrica |
|---|---|---|
| % de desconto (20% vs 30%) | Desconto maior retém mais | Taxa de retenção, impacto no LTV |
| Duração da pausa (1 vs 3 meses) | Pausa mais longa aumenta a taxa de retorno | Taxa de reativação |
| Posicionamento da pesquisa (antes vs depois da oferta) | Pesquisa primeiro personaliza a oferta | Taxa de retenção |
| Apresentação da oferta (modal vs página inteira) | Página inteira gera mais atenção | Taxa de retenção |
| Tom da copy (empático vs direto) | Empático reduz fricção | Taxa de retenção |

**Como rodar experimentos de fluxo de cancelamento:** use a skill
**ab-testing** para desenhar testes estatisticamente rigorosos. O PostHog
é uma boa opção para experimentos de fluxo de cancelamento — seus feature
flags conseguem dividir usuários em fluxos diferentes no server-side, e seu
analytics de funil rastreia cada passo do fluxo de cancelamento (pesquisa →
oferta → aceitar/recusar → confirmar). Veja o
[guia de integração do PostHog](../../tools/integrations/posthog.md) para
o setup.

---

## Erros comuns

- **Nenhum fluxo de cancelamento** — cancelamento instantâneo deixa
  dinheiro na mesa. Até uma pesquisa simples + uma oferta retém 10-15%
- **Dificultar achar o cancelamento** — botões de cancelamento escondidos
  geram ressentimento e avaliações ruins. Muitas jurisdições exigem
  cancelamento fácil (regra Click-to-Cancel da FTC nos EUA; no Brasil, o
  CDC exige que o cancelamento seja tão fácil quanto a contratação)
- **A mesma oferta para todo motivo** — um desconto genérico não resolve
  "falta feature" ou "não estou usando"
- **Descontos profundos demais** — descontos de 50%+ treinam o cliente a
  cancelar-e-voltar em busca de promoção
- **Ignorar o churn involuntário** — frequentemente 30-50% do churn total
  e o mais fácil de consertar
- **Sem e-mails de dunning** — deixar pagamentos falhos cancelarem contas
  silenciosamente
- **Copy de cobrança de culpa** — "Tem certeza que quer nos abandonar?"
  prejudica a confiança na marca
- **Não rastrear o LTV da oferta de retenção** — um cliente "retido" que
  cancela 30 dias depois não foi realmente retido
- **Pausar por tempo demais** — pausas além de 3 meses raramente reativam.
  Estabeleça limites.
- **Sem caminho pós-cancelamento** — deixe a reativação fácil e dispare
  e-mails de reconquista, porque alguns usuários que cancelaram vão querer
  voltar

---

## Integrações de ferramentas

Para implementação, veja o [registro de ferramentas](../../tools/REGISTRY.md).

### Plataformas de retenção

| Ferramenta | Melhor para | Feature-chave |
|---|---|---|
| **Churnkey** | Fluxo de cancelamento completo + dunning | Ofertas adaptativas com IA, 34% de taxa média de retenção |
| **ProsperStack** | Fluxos de cancelamento com analytics | Motor de regras avançado, integração Stripe/Chargebee |
| **Raaft** | Construtor simples de fluxo de cancelamento | Setup fácil, bom para estágio inicial |
| **Chargebee Retention** | Clientes Chargebee | Integração nativa, era o Brightback |

### Provedores de cobrança (Dunning)

| Provedor | Retries inteligentes | E-mails de dunning | Atualizador de cartão |
|---|:---:|:---:|:---:|
| **Stripe** | Nativo (Smart Retries) | Nativo | Automático |
| **Chargebee** | Nativo | Nativo | Via gateway |
| **Paddle** | Nativo | Nativo | Gerenciado |
| **Recurly** | Nativo | Nativo | Nativo |
| **Braintree** | Configuração manual | Manual | Via gateway |

### Ferramentas CLI relacionadas

| Ferramenta | Use para |
|---|---|
| `stripe` | Gestão de assinatura, config de dunning, retries de pagamento |
| `customer-io` | Sequências de e-mail de dunning, campanhas de retenção |
| `posthog` | Testes A/B de fluxo de cancelamento via feature flags, analytics de funil |
| `mixpanel` / `ga4` | Tracking de uso, análise de sinal de churn |
| `segment` | Roteamento de evento para health scoring |

---

## Skills relacionadas

- **emails**: para sequências de e-mail de reconquista após o cancelamento
- **paywalls**: para momentos de upgrade dentro do produto e expiração de teste
- **pricing**: para estrutura de plano e estratégia de desconto anual
- **onboarding**: para ativação, para prevenir churn precoce
- **analytics**: para configurar eventos de sinal de churn
- **ab-testing**: para testar variações do fluxo de cancelamento com rigor estatístico
