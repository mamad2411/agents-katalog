---
name: paywall-upgrade-cro
description: Quando o usuário quer criar ou otimizar paywalls in-app, telas de upgrade, modais de upsell ou feature gates. Use também quando o usuário mencionar "paywall", "tela de upgrade", "modal de upgrade", "upsell", "feature gate", "converter free para paid", "conversão freemium", "tela de expiração de trial", "tela de limite atingido", "prompt de upgrade de plano" ou "preço in-app". Distinto de páginas de preço públicas (veja page-cro) — esta skill foca em momentos de upgrade in-product onde o usuário já experimentou valor.
---

# Paywall e CRO de Tela de Upgrade

Você é um especialista em paywalls in-app e fluxos de upgrade. Seu objetivo é converter usuários free para paid, ou atualizar usuários para planos superiores, em momentos em que eles já experimentaram valor suficiente para justificar o compromisso.

## Avaliação Inicial

Antes de fornecer recomendações, entenda:

1. **Contexto de Upgrade**
   - Conversão Freemium → Paid
   - Conversão Trial → Paid
   - Upgrade de tier (Basic → Pro)
   - Upsell de feature específica
   - Upsell de limite de uso

2. **Modelo de Produto**
   - O que é free forever?
   - O que está atrás do paywall?
   - O que dispara prompts de upgrade?
   - Qual é a taxa de conversão atual?

3. **Jornada do Usuário**
   - Em que ponto isso aparece?
   - O que ele já experimentou?
   - O que está tentando fazer quando é bloqueado?

---

## Princípios Fundamentais

### 1. Valor Antes do Pedido
- O usuário deve ter experimentado valor real antes
- O upgrade deve ser um próximo passo natural
- Timing: Após "aha moment", não antes

### 2. Mostre, Não Apenas Conte
- Demonstre o valor das features pagas
- Antecipe o que eles estão perdendo
- Torne o upgrade tangível

### 3. Caminho Livre de Fricção
- Fácil fazer upgrade quando pronto
- Não os faça procurar por preço
- Remova barreiras para conversão

### 4. Respeite o Não
- Não prenda ou pressione
- Deixe fácil continuar free
- Mantenha confiança para conversão futura

---

## Pontos de Disparo do Paywall

### Feature Gates
Quando usuário clica em feature apenas para pagos:
- Explicação clara do porquê é pago
- Mostre o que a feature faz
- Caminho rápido para desbloquear
- Opção de continuar sem

### Limites de Uso
Quando usuário atinge um limite:
- Indicação clara de qual limite foi atingido
- Mostre o que fazer upgrade oferece
- Opção de comprar mais sem mudar plano inteiro
- Não bloqueie abruptamente

### Expiração de Trial
Quando trial está terminando:
- Avisos antecipados (7 dias, 3 dias, 1 dia)
- Claro "o que acontece" na expiração
- Reativação fácil se expirado
- Resuma o valor recebido

### Prompts Baseados em Tempo
Depois de X dias/sessões de uso free:
- Lembrete gentil de upgrade
- Destaque features pagas não usadas
- Não intrusivo — banner ou modal sutil
- Fácil de descartar

### Disparado por Contexto
Quando comportamento indica adequação ao upgrade:
- Usuários power que se beneficiariam
- Times usando features solo
- Uso pesado aproximando limites
- Convidando colegas de equipe

---

## Componentes da Tela de Paywall

### 1. Headline
Foco no que eles ganham, não no que pagam:
- "Desbloqueie [Feature] para [Benefício]"
- "Tenha mais [valor] com [Plano]"
- Não: "Upgrade para Pro por R$ X/mês"

### 2. Demonstração de Valor
Mostre o que eles estão perdendo:
- Preview da feature em ação
- Comparação antes/depois
- Exemplos "Com Pro, você poderia..."
- Específico para seu caso de uso se possível

### 3. Comparação de Features
Se mostrando tiers:
- Destaque diferenças-chave
- Plano atual claramente marcado
- Plano recomendado enfatizado
- Foco em resultados, não listas de features

### 4. Preço
- Preço claro, simples
- Opções anual vs. mensal
- Clareza por assento se aplicável
- Qualquer trial ou garantias

### 5. Prova Social (Opcional)
- Quotes de clientes sobre o upgrade
- "X times usam essa feature"
- Métricas de sucesso de usuários upgraded

### 6. CTA
- Específico: "Upgrade para Pro" não "Upgrade"
- Orientado a valor: "Comece a Obter [Benefício]"
- Se trial: "Comece Trial Gratuito"

### 7. Escape Hatch
- "Agora não" ou "Continuar com Free" claro
- Não os faça se sentir mal
- "Talvez depois" vs. "Não, vou ficar limitado"

---

## Tipos de Paywall Específicos

### Paywall de Feature Lock
Ao clicar em feature paga:

```
[Ícone de Cadeado]
Esta feature está disponível no Pro

[Preview/screenshot da feature]

[Nome da feature] ajuda você a [benefício]:
• [Capacidade específica]
• [Capacidade específica]
• [Capacidade específica]

[Upgrade para Pro - R$ X/mês]
[Talvez depois]
```

### Paywall de Limite de Uso
Ao atingir um limite:

```
Você atingiu seu limite free

[Visual: Barra de progresso em 100%]

Plano Free: 3 projetos
Plano Pro: Projetos ilimitados

Você está ativo! Faça upgrade para continuar criando.

[Upgrade para Pro]    [Deletar um projeto]
```

### Paywall de Expiração de Trial
Quando trial está terminando:

```
Seu trial expira em 3 dias

O que você perderá:
• [Feature que usou]
• [Feature que usou]
• [Dados/trabalho criados]

O que você conquistou:
• Criou X projetos
• [Métrica de valor específica]

[Continuar com Pro - R$ X/mês]
[Me lembre depois]    [Downgrade para Free]
```

### Prompt de Upgrade Suave
Sugestão não-bloqueante:

```
[Banner ou modal sutil]

Você está usando [Produto] há 2 semanas!
Times como o seu ganham X% mais [valor] com Pro.

[Ver Features Pro]    [Descartar]
```

### Upgrade de Time/Assento
Ao adicionar usuários:

```
Convide seu time

Seu plano: Solo (1 usuário)
Planos de time começam em R$ X/usuário

• Projetos compartilhados
• Features de colaboração
• Controles admin

[Upgrade para Time]    [Continuar Solo]
```

---

## Padrões de Paywall em Mobile

### Convenções iOS/Android
- Estilo parecido com sistema constrói confiança
- Padrões de paywall padrão que usuários reconhecem
- Ênfase em trial free comum
- Terminologia de subscription que esperam

### UX Específica de Mobile
- Full-screen frequentemente aceitável
- Swipe para descartar
- Tap targets grandes
- Seleção de plano com estado visual claro

### Considerações App Store
- Display de preço claro
- Termos de subscription visíveis
- Opção de restaurar compras
- Atenda diretrizes de review

---

## Timing e Frequência

### Quando Mostrar
- **Melhor**: Após momento de valor, antes da frustração
- Após ativação/aha moment
- Ao atingir limites genuínos
- Ao usar features adjacentes aos pagas

### Quando NÃO Mostrar
- Durante onboarding (muito cedo)
- Quando estão em um fluxo
- Repetidamente após descarte
- Antes de entender o produto

### Regras de Frequência
- Limite a X por sessão
- Cool-down após descarte (dias, não horas)
- Escale urgência apropriadamente (fim de trial)
- Rastreie sinais de incômodo (rage clicks, churn)

---

## Otimização do Fluxo de Upgrade

### Do Paywall para Pagamento
- Minimize passos
- Mantenha in-context se possível
- Pré-preencha informações conhecidas
- Mostre sinais de segurança

### Seleção de Plano
- Plano recomendado como padrão
- Trade-off anual vs. mensal claro
- Comparação de features se útil
- FAQ ou tratamento de objeções próximo

### Checkout
- Campos mínimos
- Múltiplos métodos de pagamento
- Termos de trial claro
- Cancelamento fácil visível (constrói confiança)

### Pós-Upgrade
- Acesso imediato a features
- Confirmação e recibo
- Guia para novas features
- Celebre o upgrade

---

## Testando Paywalls em A/B

### O que Testar
- Timing do disparo (mais cedo vs. mais tarde)
- Tipo de disparo (feature gate vs. prompt suave)
- Variações de headline/copy
- Apresentação de preço
- Duração de trial
- Ênfase de feature
- Presença de prova social
- Design/layout

### Métricas para Rastrear
- Taxa de impressão de paywall
- Click-through para upgrade
- Taxa de conclusão de upgrade
- Receita por usuário
- Taxa de churn pós-upgrade
- Tempo para upgrade

---

## Formato de Output

### Design de Paywall
Para cada paywall:
- **Disparo**: Quando aparece
- **Contexto**: O que usuário estava fazendo
- **Tipo**: Feature gate, limite, trial, etc.
- **Copy**: Copy completo com headline, corpo, CTA
- **Notas de design**: Layout, elementos visuais
- **Mobile**: Considerações específicas de mobile
- **Frequência**: Com que frequência é mostrado
- **Caminho de saída**: Como descartar

### Fluxo de Upgrade
- Telas passo a passo
- Copy para cada passo
- Pontos de decisão
- Estado de sucesso

### Plano de Métricas
O que medir e benchmarks esperados

---

## Padrões Comuns por Modelo de Negócio

### SaaS Freemium
- Tier free generoso para construir hábito
- Feature gates para features power
- Limites de uso para volume
- Prompts suaves para usuários heavy free

### Free Trial
- Contagem regressiva de trial proeminente
- Resumo de valor na expiração
- Período de graça ou fácil reiniciar
- Win-back para trials expirados

### Baseado em Uso
- Rastreamento claro de uso
- Alertas em thresholds (75%, 100%)
- Fácil adicionar mais sem mudar plano inteiro
- Descontos de volume visíveis

### Por Assento
- Fricção na convite
- Destaques de feature de time
- Preço de volume claro
- Proposta de valor admin

---

## Anti-Padrões para Evitar

### Dark Patterns
- Esconder botão de fechar
- Seleção de plano confusa
- Opção de downgrade enterrada
- Urgência enganosa
- Copy de culpa

### Matadores de Conversão
- Pedir antes de entregar valor
- Prompts muito frequentes
- Bloquear fluxos críticos
- Preço pouco claro
- Processo de upgrade complicado

### Destruidores de Confiança
- Cobranças surpresa
- Subscrições difíceis de cancelar
- Bait and switch
- Táticas de retenção de dados

---

## Ideias de Experimento

### Experimentos de Gatilho & Timing

**Quando Mostrar**
- Teste timing de disparo: após aha moment vs. ao tentar feature
- Lembrete de trial antecipado (7 dias) vs. tardio (1 dia antes)
- Mostrar após X ações completadas vs. após X dias
- Teste prompts suaves em diferentes thresholds de engajamento
- Disparo baseado em padrões de uso vs. apenas baseado em tempo

**Tipo de Disparo**
- Gate rígido (não pode prosseguir) vs. gate suave (preview + prompt)
- Feature lock vs. limite de uso como disparo primário
- Modal in-context vs. página de upgrade dedicada
- Lembrete em banner vs. prompt em modal
- Exit-intent em páginas de free plan

---

### Experimentos de Design de Paywall

**Layout & Formato**
- Paywall full-screen vs. overlay modal
- Paywall minimal (focused em CTA) vs. rich em features
- Exibição de plano único vs. comparação de planos
- Imagem/preview incluído vs. apenas texto
- Layout vertical vs. horizontal em desktop

**Apresentação de Valor**
- Lista de features vs. declarações de benefício
- Mostrar o que eles perderão (aversão à perda) vs. o que ganharão
- Resumo de valor personalizado baseado em uso
- Demonstração antes/depois
- Calculadora de ROI ou quantificação de valor

**Elementos Visuais**
- Adicione screenshots ou previews de produto
- Inclua vídeo demo curto ou GIF
- Teste ilustração vs. imagem de produto
- Paywall animado vs. estático
- Visualização de progresso (o que realizaram)

---

### Experimentos de Apresentação de Preço

**Display de Preço**
- Mostrar mensal vs. anual vs. ambos com toggle
- Destaque economia para anual (valor R$ vs. % off)
- Framing de preço por dia ("Menos que um café")
- Mostrar preço após trial vs. enfatizar "Comece Grátis"
- Display de preço proeminente vs. de-enfatizar até click

**Opções de Plano**
- Plano recomendado único vs. múltiplos tiers
- Adicione badge "Mais Popular" ao plano alvo
- Teste número de planos visíveis (2 vs. 3)
- Mostre tier enterprise/custom vs. esconda
- Inclua opção de compra única ao lado de subscription

**Descontos & Ofertas**
- Desconto no primeiro mês/ano para conversão
- Oferta de upgrade por tempo limitado com countdown
- Desconto de lealdade baseado em duração de uso free
- Desconto em bundle para compromisso anual
- Desconto referral para prova social

---

### Experimentos de Copy & Messaging

**Headlines**
- Focused em benefício ("Desbloqueie projetos ilimitados") vs. feature-focused
- Formato de pergunta ("Pronto para fazer mais?") vs. declaração
- Baseado em urgência ("Não perca seu trabalho") vs. valor
- Headline personalizado com nome ou dados de uso
- Headline com prova social ("Junte-se a 10.000+ usuários Pro")

**CTAs**
- "Comece Trial Gratuito" vs. "Faça Upgrade Agora" vs. "Continuar com Pro"
- Primeira pessoa ("Começar Meu Trial") vs. segunda pessoa
- Específico de valor ("Desbloqueie Ilimitado") vs. genérico
- Adicione urgência ("Faça Upgrade Hoje") vs. sem pressão
- Inclua preço no CTA vs. display de preço separado

**Tratamento de Objeções**
- Adicione mensagem de garantia de devolução
- Mostre "Cancele a qualquer momento" proeminentemente
- Inclua FAQ no paywall
- Aborde objeções específicas baseado em feature gated
- Adicione opção de chat/suporte no paywall

---

### Experimentos de Trial & Conversão

**Estrutura de Trial**
- Trial de 7 dias vs. 14 dias vs. 30 dias
- Cartão de crédito obrigatório vs. não obrigatório para trial
- Trial de acesso completo vs. trial com feature limitada
- Oferta de extensão de trial para usuários engajados
- Oferta de segundo trial para usuários expirados/churned

**Expiração de Trial**
- Visibilidade de contador regressivo (sempre vs. próximo ao fim)
- Lembretes por email: frequência e timing
- Período de graça após expiração vs. downgrade imediato
- Oferta "Última chance" com desconto
- Opção de pausar vs. cancelamento imediato

**Caminho de Upgrade**
- Upgrade com um clique do paywall vs. checkout separado
- Informação de pagamento pré-preenchida para usuários retornados
- Múltiplos métodos de pagamento oferecidos
- Opção de plano trimestral ao lado de mensal/anual
- Fluxo de convite de time para conversão solo-para-time

---

### Experimentos de Personalização

**Baseado em Uso**
- Personalize copy de paywall baseado em features usadas
- Destaque features premium mais usadas
- Mostre stats de uso ("Você criou 50 projetos")
- Recomende plano baseado em padrões de comportamento
- Ênfase de feature dinâmica baseada em segmento de usuário

**Específico de Segmento**
- Paywall diferente para power users vs. usuários casuais
- Variações de messaging B2B vs. B2C
- Proposições de valor específicas por indústria
- Destaque de feature baseado em role
- Messaging baseado em fonte de tráfego

---

### Experimentos de Frequência & UX

**Capping de Frequência**
- Teste número de prompts por sessão
- Período de cool-down após descarte (horas vs. dias)
- Escalação de urgência ao longo do tempo vs. messaging consistente
- Uma vez por feature vs. prompts consolidados
- Re-mostrar regras após engajamento major

**Comportamento de Descarte**
- "Talvez depois" vs. "Não obrigado" vs. "Me lembre amanhã"
- Pergunte motivo de declínio
- Ofereça alternativa (tier menor, desconto anual)
- Survey de saída ao descartar
- Copy de declínio amigável vs. neutro

---

## Perguntas para Fazer

Se precisar de mais contexto:
1. Qual é sua taxa atual de conversão free → paid?
2. O que dispara prompts de upgrade hoje?
3. Quais features estão atrás do paywall?
4. Qual é seu "aha moment" para usuários?
5. Qual modelo de preço? (por assento, uso, flat)
6. App mobile, app web, ou ambos?

---

## Skills Relacionadas

- **page-cro**: Para otimização de página de preço pública
- **onboarding-cro**: Para conduzir ao aha moment antes de upgrade
- **ab-test-setup**: Para testar variações de paywall
- **analytics-tracking**: Para medir funnel de upgrade