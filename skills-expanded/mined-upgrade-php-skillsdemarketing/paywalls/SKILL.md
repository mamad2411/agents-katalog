---
name: paywalls
description: Quando o usuário quiser criar ou otimizar paywalls dentro do app, telas de upgrade, modais de upsell, ou bloqueios de funcionalidade. Use também quando o usuário mencionar "paywall," "tela de upgrade," "modal de upgrade," "upsell," "bloqueio de funcionalidade," "converter grátis em pago," "conversão de freemium," "tela de fim de trial," "tela de limite atingido," "prompt de upgrade de plano," "preço dentro do app," "usuários grátis não fazem upgrade," "conversão de trial para pago," ou "como faço os usuários pagarem." Use isso para qualquer momento dentro do produto em que você está pedindo para o usuário fazer upgrade. Distinta de páginas públicas de preço (veja cro) — esta foca nos momentos de upgrade dentro do produto em que o usuário já experimentou valor. Para decisões de preço, veja pricing.
metadata:
  version: 2.0.0
---

# CRO de Paywall e Tela de Upgrade

Você é um especialista em paywalls dentro do app e fluxos de upgrade. Seu objetivo é converter usuários grátis em pagos, ou usuários em planos superiores, nos momentos em que eles já experimentaram valor suficiente para justificar o compromisso.

## Avaliação Inicial

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o nome de arquivo legado `product-marketing-context.md`, em setups mais antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o que não estiver coberto ou for específico desta tarefa.

Antes de fornecer recomendações, entenda:

1. **Contexto do Upgrade** - Freemium → Pago? Trial → Pago? Upgrade de tier? Upsell de funcionalidade? Limite de uso?

2. **Modelo de Produto** - O que é grátis? O que fica atrás do paywall? O que dispara os prompts? Taxa de conversão atual?

3. **Jornada do Usuário** - Quando isso aparece? O que ele já experimentou? O que ele está tentando fazer?

---

## Princípios Centrais

### 1. Valor Antes do Pedido

- O usuário deve ter experimentado valor real primeiro
- O upgrade deve parecer o próximo passo natural
- Timing: Depois do "momento aha," não antes

### 2. Mostre, Não Apenas Diga

- Demonstre o valor das funcionalidades pagas
- Dê um preview do que ele está perdendo
- Faça o upgrade parecer tangível

### 3. Caminho Sem Fricção

- Fácil de fazer upgrade quando estiver pronto
- Não faça o usuário caçar a página de preço

### 4. Respeite o Não

- Não prenda nem pressione
- Facilite continuar no plano grátis
- Mantenha a confiança para conversão futura

---

## Pontos de Gatilho do Paywall

### Bloqueios de Funcionalidade

Quando o usuário clica em uma funcionalidade paga:

- Explicação clara do porquê é pago
- Mostre o que a funcionalidade faz
- Caminho rápido para desbloquear
- Opção de continuar sem ela

### Limites de Uso

Quando o usuário atinge um limite:

- Indicação clara do limite atingido
- Mostre o que o upgrade oferece
- Não bloqueie abruptamente

### Fim do Trial

Quando o trial está terminando:

- Avisos antecipados (7, 3, 1 dia)
- "O que acontece" claro ao expirar
- Resuma o valor recebido

### Prompts Baseados em Tempo

Depois de X dias de uso grátis:

- Lembrete de upgrade gentil
- Destaque funcionalidades pagas não usadas
- Fácil de dispensar

---

## Componentes da Tela de Paywall

1. **Título** - Foco no que a pessoa ganha: "Desbloqueie [Funcionalidade] para [Benefício]"

2. **Demonstração de Valor** - Preview, antes/depois, "Com o Pro você poderia..."

3. **Comparação de Funcionalidades** - Destaque as diferenças principais, plano atual marcado

4. **Preço** - Claro, simples, opções anual vs. mensal

5. **Prova Social** - Depoimentos de clientes, "X times usam isso"

6. **CTA** - Específico e orientado a valor: "Comece a Ter [Benefício]"

7. **Rota de Escape** - "Agora não" ou "Continuar no Grátis" claros

---

## Tipos Específicos de Paywall

### Paywall de Funcionalidade Bloqueada

```text
[Ícone de Cadeado]
Essa funcionalidade está disponível no Pro

[Preview/screenshot da funcionalidade]

[Nome da funcionalidade] te ajuda a [benefício]:
• [Capacidade]
• [Capacidade]

[Fazer upgrade para o Pro - R$X/mês]
[Talvez depois]
```

### Paywall de Limite de Uso

```text
Você atingiu seu limite grátis

[Barra de progresso em 100%]

Grátis: 3 projetos | Pro: Ilimitado

[Fazer upgrade para o Pro]  [Apagar um projeto]
```

### Paywall de Fim de Trial

```text
Seu trial termina em 3 dias

O que você vai perder:
• [Funcionalidade usada]
• [Dado criado]

O que você conquistou:
• Criou X projetos

[Continuar no Pro]
[Me lembre depois]  [Fazer downgrade]
```

---

## Timing e Frequência

### Quando Mostrar

- Depois do momento de valor, antes da frustração
- Depois da ativação/momento aha
- Ao atingir limites genuínos

### Quando NÃO Mostrar

- Durante o onboarding (cedo demais)
- Quando o usuário está em um fluxo
- Repetidamente após dispensar

### Regras de Frequência

- Limite por sessão
- Período de resfriamento após dispensar (dias, não horas)
- Acompanhe sinais de irritação

---

## Otimização do Fluxo de Upgrade

### Do Paywall ao Pagamento

- Minimize passos
- Mantenha no contexto se possível
- Pré-preencha informações já conhecidas

### Pós-Upgrade

- Acesso imediato às funcionalidades
- Confirmação e recibo
- Guia para as novas funcionalidades

---

## Testes A/B

### O Que Testar

- Timing do gatilho
- Variações de título/copy
- Apresentação de preço
- Duração do trial
- Ênfase em funcionalidade
- Design/layout

### Métricas para Acompanhar

- Taxa de impressão do paywall
- Taxa de clique para upgrade
- Taxa de conclusão
- Receita por usuário
- Taxa de churn pós-upgrade

**Para ideias completas de experimento**: veja [references/experiments.md](references/experiments.md)

---

## Anti-Padrões a Evitar

### Dark Patterns

- Esconder o botão de fechar
- Confundir a seleção de plano
- Copy de culpa

### Matadores de Conversão

- Pedir antes de entregar valor
- Prompts frequentes demais
- Bloquear fluxos críticos
- Processo de upgrade complicado

---

## Perguntas Específicas da Tarefa

1. Qual é sua taxa atual de conversão de grátis para pago?
2. O que dispara os prompts de upgrade hoje?
3. Quais funcionalidades estão atrás do paywall?
4. Qual é o "momento aha" dos seus usuários?
5. Qual modelo de preço? (por assento, por uso, fixo)
6. App mobile, app web, ou ambos?

---

## Skills Relacionadas

- **churn-prevention**: Para fluxos de cancelamento, ofertas de retenção, e redução de churn pós-upgrade
- **cro**: Para otimização de página pública de preço
- **onboarding**: Para levar ao momento aha antes do upgrade
- **ab-testing**: Para testar variações de paywall
