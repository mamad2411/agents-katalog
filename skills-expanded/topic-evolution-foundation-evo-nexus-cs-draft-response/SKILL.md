---
name: cs-draft-response
description: Redige uma resposta profissional voltada ao cliente adaptada à situação e ao relacionamento. Use para responder uma pergunta de produto, responder a uma escalação ou incidente, entregar uma má notícia como atraso ou won't-fix, recusar um feature request, ou responder a um problema de billing. / Draft a professional customer-facing response tailored to the situation and relationship. Use when answering a product question, responding to an escalation or outage, delivering bad news like a delay or won't-fix, declining a feature request, or replying to a billing issue.
argument-hint: "<descrição da situação>"
---

# /cs-draft-response

> Se encontrar integrações não configuradas, verifique [CONNECTORS.md](../../CONNECTORS.md).

Redigir uma resposta profissional voltada ao cliente adaptada à situação, ao relacionamento com o cliente e ao contexto de comunicação.

## Usage

```
/cs-draft-response <contexto sobre a pergunta, problema ou solicitação do cliente>
```

Exemplos:
- `/cs-draft-response Acme Corp perguntando quando a nova feature de dashboard vai lançar`
- `/cs-draft-response Escalação de cliente — integração deles está fora há 2 dias`
- `/cs-draft-response Respondendo a um feature request que não vamos construir`
- `/cs-draft-response Cliente teve erro de billing e quer resolução ASAP`

## Workflow

### 1. Entender o Contexto

Analisar o input do usuário para determinar:

- **Cliente**: Para quem é a comunicação? Verificar contexto de conta se disponível.
- **Tipo de situação**: Pergunta, problema, escalação, anúncio, negociação, má notícia, boa notícia, acompanhamento
- **Urgência**: É sensível ao tempo? Há quanto tempo o cliente está esperando?
- **Canal**: Email, ticket de suporte, chat ou outro (ajustar formalidade adequadamente)
- **Estágio do relacionamento**: Novo cliente, estabelecido, frustrado/escalado
- **Nível do stakeholder**: Usuário final, gerente, executivo, técnico, negócio

### 2. Pesquisar Contexto

Coletar background relevante de fontes disponíveis:

**Gmail MCP:**
- Correspondência anterior com esse cliente sobre esse tópico
- Quaisquer compromissos ou timelines compartilhados anteriormente
- Tom e estilo do thread existente

**discord-get-messages** (`/discord-get-messages`) e **int-whatsapp** (`/int-whatsapp`):
- Discussões internas sobre esse cliente ou tópico
- Qualquer orientação de produto, Devs ou liderança
- Situações similares e como foram tratadas

**int-evo-crm** (`/int-evo-crm`):
- Detalhes da conta e nível de plano
- Informações de contato e stakeholders principais
- Escalações anteriores ou problemas sensíveis

**int-evo-crm** (tickets relacionados):
- Tickets relacionados e suas resoluções
- Problemas conhecidos ou workarounds
- Status de SLA e compromissos de tempo de resposta

**Notion MCP:**
- Documentação oficial ou artigos de ajuda para referenciar
- Informações do roadmap de produto (se compartilháveis)
- Documentação de política ou processo

### 3. Gerar o Rascunho

Produzir uma resposta adaptada à situação:

```
## Rascunho de Resposta

**Para:** [Nome do contato do cliente]
**Assunto/Re:** [Assunto/tópico]
**Canal:** [Email / Ticket / Chat]
**Tom:** [Empático / Profissional / Técnico / Comemorativo / Direto]

---

[Texto do rascunho da resposta]

---

### Notas para Você (internas — não enviar)
- **Por que essa abordagem:** [Racional para escolhas de tom e conteúdo]
- **Coisas a verificar:** [Quaisquer fatos ou compromissos a confirmar antes de enviar]
- **Fatores de risco:** [Qualquer coisa sensível sobre essa resposta]
- **Acompanhamento necessário:** [Ações a tomar após enviar]
- **Nota de escalação:** [Se isso deve ser revisado por alguém antes]
```

### 4. Executar Verificações de Qualidade

Antes de apresentar o rascunho, verificar:

- [ ] Tom corresponde à situação e ao relacionamento
- [ ] Sem compromissos além do que está autorizado
- [ ] Sem detalhes do roadmap de produto que não devem ser compartilhados externamente
- [ ] Referências precisas a conversas anteriores
- [ ] Próximos passos claros e titularidade definida
- [ ] Adequado para o nível do stakeholder (não muito técnico para executivos, não muito vago para engenheiros)
- [ ] Tamanho adequado para o canal (mais curto para chat, mais completo para email)

### 5. Oferecer Iterações

Após apresentar o rascunho:
- "Quer que eu ajuste o tom? (mais formal, mais casual, mais empático, mais direto)"
- "Devo adicionar ou remover algum ponto específico?"
- "Quer que eu torne isso mais curto/longo?"
- "Devo redigir uma versão para um stakeholder diferente?"
- "Quer que eu redija a nota de escalação interna também?"
- "Devo preparar uma mensagem de acompanhamento para enviar após [X dias] sem resposta?"

---

## Boas Práticas de Comunicação com Clientes

### Princípios Fundamentais

1. **Começar com empatia**: Reconhecer a situação do cliente antes de ir para soluções
2. **Ser direto**: Ir ao ponto — clientes são ocupados. Bottom-line-up-front.
3. **Ser honesto**: Nunca prometer demais, nunca enganar, nunca esconder más notícias em jargão
4. **Ser específico**: Usar detalhes concretos, timelines e nomes — evitar linguagem vaga
5. **Assumir responsabilidade**: Assumir a responsabilidade quando apropriado. "Nós" não "o sistema" ou "o processo"
6. **Fechar o loop**: Cada resposta deve ter um próximo passo claro ou call to action
7. **Corresponder à energia deles**: Se estão frustrados, ser empático primeiro. Se estão animados, ser entusiasmado.

### Estrutura de Resposta

Para a maioria das comunicações com clientes, seguir essa estrutura:

```
1. Reconhecimento / Contexto (1-2 frases)
   - Reconhecer o que disseram, perguntaram ou estão vivenciando
   - Mostrar que você entende a situação deles

2. Mensagem Central (1-3 parágrafos)
   - Entregar a informação principal, resposta ou atualização
   - Ser específico e concreto
   - Incluir detalhes relevantes que eles precisam

3. Próximos Passos (1-3 bullets)
   - O que VOCÊ vai fazer e até quando
   - O que ELES precisam fazer (se houver)
   - Quando vão ter notícias suas

4. Fechamento (1 frase)
   - Encerramento cordial mas profissional
   - Reforçar que você está disponível se precisarem
```

### Diretrizes de Extensão

- **Chat/IM**: 1-4 frases. Ir ao ponto imediatamente.
- **Resposta de ticket de suporte**: 1-3 parágrafos curtos. Estruturado e escaneável.
- **Email**: 3-5 parágrafos no máximo. Respeitar a caixa de entrada deles.
- **Resposta de escalação**: Tão longo quanto necessário para ser completo, mas bem estruturado com headers.
- **Comunicação executiva**: Mais curto é melhor. 2-3 parágrafos no máximo. Orientado a dados.

## Diretrizes de Tom e Estilo

### Espectro de Tom

| Situação | Tom | Características |
|-----------|------|----------------|
| Boa notícia / conquistas | Comemorativo | Entusiasmado, caloroso, parabenizador, orientado ao futuro |
| Atualização rotineira | Profissional | Claro, conciso, informativo, amigável |
| Resposta técnica | Preciso | Preciso, detalhado, estruturado, paciente |
| Entrega atrasada | Responsável | Honesto, empático, orientado à ação, específico |
| Má notícia | Direto | Direto, empático, orientado à solução, respeitoso |
| Problema / incidente | Urgente | Imediato, transparente, acionável, tranquilizador |
| Escalação | Executivo | Composto, assumindo responsabilidade, apresentando plano, confiante |
| Billing / conta | Preciso | Claro, factual, empático, focado na resolução |

### Ajustes de Tom por Estágio do Relacionamento

**Novo Cliente (0-3 meses):**
- Mais formal e profissional
- Contexto e explicação extras (não assumir conhecimento prévio)
- Oferecer proativamente ajuda e recursos
- Construir confiança através de confiabilidade e responsividade

**Cliente Estabelecido (3+ meses):**
- Caloroso e colaborativo
- Pode referenciar histórico compartilhado e conversas anteriores
- Comunicação mais direta e eficiente
- Demonstrar consciência dos objetivos e prioridades deles

**Cliente Frustrado ou Escalado:**
- Empatia e reconhecimento extras
- Urgência nos tempos de resposta
- Planos de ação concretos com compromissos específicos
- Loops de feedback mais curtos

### Regras de Estilo de Escrita

**FAZER:**
- Usar voz ativa ("Vamos investigar" não "Isso será investigado")
- Usar "eu" para compromissos pessoais e "nós" para compromissos do time
- Nomear pessoas específicas ao atribuir ações ("O Danilo do nosso time de Devs vai...")
- Usar a terminologia do cliente, não o jargão interno da Evolution
- Incluir datas e horários específicos, não termos relativos ("até sexta-feira dia 24 de janeiro" não "em alguns dias")
- Quebrar respostas longas com headers ou bullet points

**NÃO FAZER:**
- Usar jargão corporativo ou buzzwords
- Transferir culpa para outros times, sistemas ou processos
- Usar voz passiva para evitar responsabilidade ("Erros foram cometidos")
- Incluir ressalvas ou hedging desnecessários que minam a confiança
- Copiar pessoas desnecessariamente — incluir apenas quem precisa estar na conversa
- Usar pontos de exclamação excessivamente (um por email no máximo, se houver)

## Abordagens por Situação

**Respondendo uma pergunta de produto:**
- Começar com a resposta direta
- Fornecer links para documentação relevante (Notion)
- Oferecer conectar com o recurso certo se necessário
- Se não souber a resposta: dizer honestamente, comprometer-se a descobrir, dar um prazo

**Respondendo a um problema ou bug:**
- Reconhecer o impacto no trabalho deles
- Indicar o que você sabe sobre o problema e seu status
- Fornecer workaround se disponível
- Definir expectativas para o prazo de resolução
- Comprometer-se com atualizações em intervalos regulares

**Tratando uma escalação:**
- Reconhecer a gravidade e a frustração deles
- Assumir responsabilidade (sem desviar ou dar desculpas)
- Fornecer um plano de ação claro com prazo
- Identificar a pessoa responsável pela resolução
- Oferecer uma reunião ou chamada se a gravidade justificar

**Entregando má notícia (sunset de feature, atraso, não-vamos-corrigir):**
- Ser direto — não enterrar a notícia
- Explicar o raciocínio honestamente
- Reconhecer o impacto específico neles
- Oferecer alternativas ou mitigação
- Fornecer um caminho claro adiante

**Compartilhando boa notícia (lançamento de feature, marco, reconhecimento):**
- Começar com o resultado positivo
- Conectar aos objetivos ou caso de uso específico deles
- Sugerir próximos passos para capitalizar na boa notícia
- Expressar entusiasmo genuíno

**Recusando uma solicitação (feature request, desconto, exceção):**
- Reconhecer a solicitação e seu raciocínio
- Ser honesto sobre a decisão
- Explicar o porquê sem ser dismissivo
- Oferecer alternativas quando possível
- Deixar a porta aberta para conversa futura

## Templates de Resposta para Cenários Comuns

### Reconhecendo um Bug Report

```
Olá [Nome],

Obrigado por reportar isso — entendo como [impacto específico]
seria frustrante para o seu time.

Confirmei o problema e escalei para nosso time de Devs como
prioridade [nível]. Aqui está o que sabemos até agora:
- [O que está acontecendo]
- [O que está causando, se conhecido]
- [Workaround, se disponível]

Vou te atualizar até [data/horário específico] com um prazo de resolução.
Enquanto isso, [detalhes do workaround se aplicável].

Me avise se tiver perguntas ou se isso está te impactando de
outras formas que devo saber.

Att,
[Seu nome]
```

### Reconhecendo um Problema de Billing ou Conta

```
Olá [Nome],

Obrigado por entrar em contato — entendo que problemas de billing
precisam de atenção imediata, e quero garantir que isso seja resolvido
rapidamente.

Verifiquei sua conta e aqui está o que estou vendo:
- [O que aconteceu — explicação factual clara]
- [Impacto na conta — cobranças, acesso, etc.]

Aqui está o que estou fazendo para resolver:
- [Ação 1 — com prazo]
- [Ação 2 — se aplicável]

[Se a resolução for imediata: "Isso foi corrigido e você deve
ver a mudança refletida em até [prazo]."]
[Se precisar de investigação: "Estou escalando isso para nosso time financeiro
e terei uma atualização para você até [data específica]."]

Me desculpe pelo inconveniente. Me avise se tiver alguma
dúvida sobre sua conta.

Att,
[Seu nome]
```

### Respondendo a um Feature Request que Não Vamos Construir

```
Olá [Nome],

Obrigado por compartilhar esse pedido — entendo por que [capacidade]
seria valiosa para [seu caso de uso].

Discuti isso com nosso time de produto, e isso não é algo que
planejamos construir no curto prazo. O motivo principal é [explicação
honesta e respeitosa — ex: atende um caso de uso restrito, conflita
com a direção da nossa arquitetura, etc.].

Dito isso, quero garantir que você possa atingir seu objetivo. Aqui estão
algumas alternativas:
- [Abordagem alternativa 1]
- [Abordagem alternativa 2]
- [Integração ou workaround se aplicável]

Também documentei seu pedido no nosso sistema de feedback, e se nossa
direção mudar, vou te avisar.

Alguma dessas alternativas funcionaria para o seu time? Posso me aprofundar
em qualquer uma delas.

Att,
[Seu nome]
```

### Comunicação de Incidente ou Outage

```
Olá [Nome],

Queria entrar em contato diretamente para informar sobre um problema
afetando [serviço/feature] que sei que o seu time depende.

**O que aconteceu:** [Explicação clara e não técnica]
**Impacto:** [Como afeta especificamente eles]
**Status:** [Atual — investigando / identificado / corrigindo / resolvido]
**Previsão de resolução:** [Horário específico se conhecido, ou "vamos atualizar a cada X horas"]

[Se aplicável: "Enquanto isso, você pode [workaround]."]

Estou pessoalmente acompanhando isso e vou te atualizar assim que tivermos
uma resolução.

Me desculpe pela interrupção no trabalho do seu time. Levamos isso a sério
e [o que estamos fazendo para prevenir recorrência, se conhecido].

[Seu nome]
```

### Acompanhamento Após Silêncio

```
Olá [Nome],

Queria verificar — enviei [o que enviou] em [data] e
queria garantir que não se perdeu.

[Breve lembrete do que você precisa deles ou do que está oferecendo]

Se não for um bom momento, sem problemas — me avise quando seria melhor,
e posso me reconectar então.

Att,
[Seu nome]
```

## Orientação de Acompanhamento e Escalação

### Cadência de Acompanhamento

| Situação | Timing de Acompanhamento |
|-----------|-----------------|
| Pergunta sem resposta | 2-3 dias úteis |
| Problema de suporte aberto | Diário até resolver para crítico, 2-3 dias para padrão |
| Action items pós-reunião | Dentro de 24 horas (enviar notas), depois verificar no prazo |
| Check-in geral | Conforme necessário para problemas contínuos |
| Após entregar má notícia | 1 semana para verificar impacto e sentimento |

### Quando Escalar

**Escalar para seu gerente/Davidson quando:**
- Cliente ameaça cancelar ou reduzir significativamente
- Cliente solicita exceção à política que você não pode autorizar
- Um problema ficou sem resolução por mais tempo do que o SLA permite
- Cliente solicita contato direto com liderança
- Você cometeu um erro que precisa de envolvimento sênior para resolver

**Escalar para Produto/Devs quando:**
- Bug é crítico e está bloqueando o negócio do cliente
- Gap de feature está causando uma perda competitiva
- Cliente tem requisitos técnicos únicos além do suporte padrão
- Problemas de integração requerem investigação dos Devs

**Formato de escalação:**
```
ESCALAÇÃO: [Nome do Cliente] — [Resumo em uma linha]

Urgência: [Crítico / Alto / Médio]
Impacto no cliente: [O que está quebrado para eles]
Histórico: [Background breve — 2-3 frases]
O que tentei: [Ações tomadas até agora]
O que preciso: [Ajuda específica ou decisão necessária]
Prazo: [Quando isso precisa ser resolvido]
```
