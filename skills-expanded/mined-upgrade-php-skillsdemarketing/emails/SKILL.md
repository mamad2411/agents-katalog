---
name: emails
description: Quando o usuário quiser criar ou otimizar uma sequência de e-mail, campanha de drip, fluxo automatizado de e-mail ou programa de e-mail de lifecycle. Use também quando o usuário mencionar "sequência de e-mail," "campanha de drip," "sequência de nutrição," "e-mails de onboarding," "sequência de boas-vindas," "e-mails de reengajamento," "automação de e-mail," "e-mails de lifecycle," "e-mails por gatilho," "funil de e-mail," "workflow de e-mail," "que e-mails devo enviar," "série de boas-vindas," ou "cadência de e-mail." Use isso para qualquer fluxo automatizado com múltiplos e-mails. Para e-mails de prospecção fria, veja cold-email. Para onboarding dentro do produto, veja onboarding.
metadata:
  version: 2.0.0
---

# Desenho de Sequência de E-mail

Você é um especialista em e-mail marketing e automação. Seu objetivo é criar
sequências de e-mail que nutrem relacionamentos, geram ação e movem as
pessoas em direção à conversão.

## Avaliação inicial

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

Antes de criar uma sequência, entenda:

1. **Tipo de sequência**
   - Sequência de boas-vindas/onboarding
   - Sequência de nutrição de lead
   - Sequência de reengajamento
   - Sequência pós-compra
   - Sequência baseada em evento
   - Sequência educacional
   - Sequência de vendas

2. **Contexto da audiência**
   - Quem são eles?
   - O que os fez entrar nessa sequência?
   - O que já sabem/acreditam?
   - Qual é o relacionamento atual deles com você?

3. **Objetivos**
   - Objetivo principal de conversão
   - Objetivos de construção de relacionamento
   - Objetivos de segmentação
   - O que define sucesso?

---

## Princípios centrais

### 1. Um e-mail, uma missão

- Cada e-mail tem um propósito principal
- Um CTA principal por e-mail
- Não tente fazer tudo de uma vez

### 2. Valor antes do pedido

- Lidere com utilidade
- Construa confiança através de conteúdo
- Conquiste o direito de vender

### 3. Relevância antes de volume

- Menos e-mails, melhores, vencem
- Segmente para relevância
- Qualidade > frequência

### 4. Caminho claro à frente

- Todo e-mail move a pessoa para algum lugar
- Links devem fazer algo útil
- Deixe os próximos passos óbvios

---

## Estratégia de sequência de e-mail

### Tamanho da sequência

- Boas-vindas: 3-7 e-mails
- Nutrição de lead: 5-10 e-mails
- Onboarding: 5-10 e-mails
- Reengajamento: 3-5 e-mails

Depende de:

- Duração do ciclo de vendas
- Complexidade do produto
- Estágio do relacionamento

### Timing/Intervalos

- E-mail de boas-vindas: imediato
- Início da sequência: 1-2 dias de intervalo
- Nutrição: 2-4 dias de intervalo
- Longo prazo: semanal ou quinzenal

Considere:

- B2B: evite fins de semana
- B2C: teste fins de semana
- Fusos horários: envie no horário local (no Brasil, atenção aos horários de
  Brasília e demais fusos)

### Estratégia de assunto (subject line)

- Claro > espirituoso
- Específico > vago
- Orientado a benefício ou curiosidade
- 40-60 caracteres ideal
- Teste emoji (eles dividem opiniões)

**Padrões que funcionam:**

- Pergunta: "Ainda travado em X?"
- Como fazer: "Como [alcançar resultado] em [prazo]"
- Número: "3 formas de [benefício]"
- Direto: "[Primeiro nome], seu [coisa] está pronto"
- Gancho de história: "O erro que cometi com [tema]"

### Texto de preview

- Estende o assunto
- ~90-140 caracteres
- Não repita o assunto
- Complete o pensamento ou adicione mistério

---

## Visão geral dos tipos de sequência

### Sequência de boas-vindas (pós-cadastro)

**Tamanho**: 5-7 e-mails ao longo de 12-14 dias
**Objetivo**: Ativar, construir confiança, converter

E-mails-chave:

1. Boas-vindas + entrega do valor prometido (imediato)
2. Vitória rápida (dia 1-2)
3. História/Por quê (dia 3-4)
4. Prova social (dia 5-6)
5. Superar objeção (dia 7-8)
6. Destaque de feature central (dia 9-11)
7. Conversão (dia 12-14)

### Sequência de nutrição de lead (pré-venda)

**Tamanho**: 6-8 e-mails ao longo de 2-3 semanas
**Objetivo**: Construir confiança, demonstrar expertise, converter

E-mails-chave:

1. Entrega da isca digital + introdução (imediato)
2. Expandir o tema (dia 2-3)
3. Aprofundar no problema (dia 4-5)
4. Framework de solução (dia 6-8)
5. Case de sucesso (dia 9-11)
6. Diferenciação (dia 12-14)
7. Tratamento de objeção (dia 15-18)
8. Oferta direta (dia 19-21)

### Sequência de reengajamento

**Tamanho**: 3-4 e-mails ao longo de 2 semanas
**Gatilho**: 30-60 dias de inatividade
**Objetivo**: Reconquistar ou limpar a lista

E-mails-chave:

1. Check-in (preocupação genuína)
2. Lembrete de valor (novidades)
3. Incentivo (oferta especial)
4. Última chance (ficar ou cancelar inscrição)

### Sequência de onboarding (usuários do produto)

**Tamanho**: 5-7 e-mails ao longo de 14 dias
**Objetivo**: Ativar, levar ao momento aha, fazer upgrade
**Nota**: Coordene com o onboarding dentro do produto — o e-mail apoia, não duplica

E-mails-chave:

1. Boas-vindas + primeiro passo (imediato)
2. Ajuda para começar (dia 1)
3. Destaque de feature (dia 2-3)
4. História de sucesso (dia 4-5)
5. Check-in (dia 7)
6. Dica avançada (dia 10-12)
7. Upgrade/expansão (dia 14+)

**Para templates detalhados**: veja
[references/sequence-templates.md](references/sequence-templates.md)

---

## Tipos de e-mail por categoria

### E-mails de onboarding

- Série de novos usuários
- Série de novos clientes
- Lembretes de passos-chave do onboarding
- Convites para novos usuários

### E-mails de retenção

- Upgrade para plano pago
- Upgrade para plano superior
- Pedido de avaliação
- Ofertas de suporte proativo
- Relatórios de uso do produto
- Pesquisa NPS
- Programa de indicação

### E-mails de cobrança

- Mudar para anual
- Recuperação de pagamento falho
- Pesquisa de cancelamento
- Lembretes de renovação próxima

### E-mails de uso

- Resumos diários/semanais/mensais
- Notificações de eventos-chave
- Celebração de marcos (milestones)

### E-mails de reconquista

- Testes gratuitos expirados
- Clientes cancelados

### E-mails de campanha

- Resumo mensal / newsletter
- Promoções sazonais
- Atualizações de produto
- Resumo de notícias do setor
- Atualizações de preço

**Para referência detalhada de tipos de e-mail**: veja
[references/email-types.md](references/email-types.md)

---

## Diretrizes de copy de e-mail

### Estrutura

1. **Gancho**: a primeira linha prende a atenção
2. **Contexto**: por que isso importa para o leitor
3. **Valor**: o conteúdo útil
4. **CTA**: o que fazer a seguir
5. **Despedida**: fechamento humano e caloroso

### Formatação

- Parágrafos curtos (1-3 frases)
- Espaço em branco entre seções
- Bullet points para escaneabilidade
- Negrito para ênfase (com moderação)
- Mobile-first (a maioria lê no celular)

### Tom

- Conversacional, não formal
- Primeira pessoa (eu/nós) e segunda pessoa (você)
- Voz ativa
- Leia em voz alta — soa humano?

### Extensão

- 50-125 palavras para transacional
- 150-300 palavras para educacional
- 300-500 palavras para storytelling

### Diretrizes de CTA

- Botões para ações principais
- Links para ações secundárias
- Um CTA principal claro por e-mail
- Texto do botão: ação + resultado

**Para diretrizes detalhadas de copy, personalização e testes**: veja
[references/copy-guidelines.md](references/copy-guidelines.md)

---

## Formato de saída

### Visão geral da sequência

```text
Nome da sequência: [Nome]
Gatilho: [O que inicia a sequência]
Objetivo: [Objetivo principal de conversão]
Tamanho: [Número de e-mails]
Timing: [Intervalo entre e-mails]
Condições de saída: [Quando a pessoa sai da sequência]
```

### Para cada e-mail

```text
E-mail [#]: [Nome/Propósito]
Envio: [Timing]
Assunto: [Subject line]
Preview: [Texto de preview]
Corpo: [Copy completa]
CTA: [Texto do botão] → [Destino do link]
Segmento/Condições: [Se aplicável]
```

### Plano de métricas

O que medir e os benchmarks

---

## Perguntas específicas da tarefa

1. O que dispara a entrada nessa sequência?
2. Qual é o objetivo/ação de conversão principal?
3. O que a pessoa já sabe sobre você?
4. Que outros e-mails ela está recebendo?
5. Qual é a performance atual de e-mail?

---

## Integrações de ferramentas

Para implementação, veja o [registro de ferramentas](../../tools/REGISTRY.md).
Principais ferramentas de e-mail:

| Ferramenta | Melhor para | MCP | Guia |
|---|---|:---:|---|
| **Customer.io** | Automação baseada em comportamento | - | [customer-io.md](../../tools/integrations/customer-io.md) |
| **Mailchimp** | E-mail marketing para pequenas/médias empresas | ✓ | [mailchimp.md](../../tools/integrations/mailchimp.md) |
| **Nitrosend** | E-mail nativo em IA (sequências via prompts) | ✓ | [nitrosend.md](../../tools/integrations/nitrosend.md) |
| **Resend** | Transacional amigável para devs | ✓ | [resend.md](../../tools/integrations/resend.md) |
| **SendGrid** | E-mail transacional em escala | - | [sendgrid.md](../../tools/integrations/sendgrid.md) |
| **Kit** | Focado em criadores/newsletter | - | [kit.md](../../tools/integrations/kit.md) |

---

## Skills relacionadas

- **lead-magnets**: para planejar iscas digitais que alimentam sequências de nutrição
- **churn-prevention**: para fluxos de cancelamento, ofertas de retenção e estratégia de cobrança (o e-mail apoia isso)
- **onboarding**: para onboarding dentro do produto (o e-mail apoia isso)
- **copywriting**: para as landing pages que os e-mails linkam
- **ab-testing**: para testar elementos do e-mail
- **popups**: para popups de captura de e-mail
- **revops**: para estágios de lifecycle que disparam sequências de e-mail
