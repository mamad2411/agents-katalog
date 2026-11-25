---
name: think-tank
description: Execute um Think Tank Virtual — um debate estruturado com múltiplas personas — antes de planejar ou tomar decisões arquiteturais/de design/estratégicas. Use esta habilidade sempre que o usuário estiver prestes a planejar um sistema, fazer uma escolha de tecnologia, avaliar trade-offs, decidir sobre uma abordagem, ou enfrenta qualquer decisão onde múltiplas perspectivas aprimorariam o resultado. Também dispare quando o usuário disser "think tank", "debate isso", "perspectivas sobre", "trade-offs", "devo usar X ou Y", "ajude-me a decidir", "antes de planejarmos", ou perguntar sobre prós e contras de abordagens concorrentes. Esta habilidade deve rodar ANTES de qualquer planejamento de implementação começar — produz uma análise estruturada que alimenta planos melhores.
---

# Think Tank Virtual

Uma habilidade de pré-planejamento que simula um debate de especialistas moderado para expor trade-offs, pontos cegos e perspectivas antes de se comprometer com um plano. Inspirado em think tanks reais: o output NÃO é uma única resposta, mas uma análise estruturada de abordagens, trade-offs e pontos de consenso que ajuda o usuário a tomar uma decisão melhor informada.

## Por que Isso Existe

Ao enfrentar decisões arquiteturais, estratégicas ou de design, uma única perspectiva (mesmo bem informada) tende a gravitar para a sabedoria convencional e perder trade-offs importantes. Um think tank força a consideração de múltiplos ângulos — técnicos, organizacionais, filosóficos — antes do planejamento começar. O resultado são planos que respondem por mais da realidade.

## Como Funciona

O think tank usa **múltiplas personas debatendo dentro de um único contexto** — não agentes separados. Isso mantém todas as perspectivas cientes dos argumentos uma da outra, permite síntese em tempo real e produz um output coerente. As personas argumentam, fazem concessões, constroem sobre as ideias umas das outras e ocasionalmente surpreendem todos (incluindo o usuário).

## Executando o Think Tank

### Fase 1: Enquadrar a Decisão

Antes de montar o painel, compreenda claramente o que está sendo decidido. Pergunte ao usuário (se já não estiver claro):

1. **Qual é a decisão ou problema?** (ex: "monólito vs microsserviços para uma nova plataforma de e-commerce")
2. **Quais restrições existem?** (tamanho da equipe, timeline, orçamento, sistemas existentes, regulamentações)
3. **O que já foi tentado ou considerado?** (evite remastigar terreno conhecido)
4. **Como seria um resultado bem-sucedido?** (ajuda o painel a se focar)

Restate o problema de volta ao usuário em um enunciado de problema nítido antes de prosseguir. Isso garante que o think tank debata a questão certa.

### Fase 2: Montar o Painel

Construa um painel de 4–6 personas. A composição importa — diversidade de perspectiva é o ponto inteiro.

**Estrutura do painel:**

- **1 Moderador** — Uma figura conhecedora, neutra que mantém o debate focado, sintetiza e pressiona por clareza. Escolha alguém conhecido por análise equilibrada no domínio relevante. O moderador abre e fecha a sessão, faz perguntas provocativas de acompanhamento e aponta quando panelistas estão falando um com o outro.

- **2–3 Vozes de domínio** — Pessoas (reais ou ficcionais) com posições conhecidas e distintas sobre o tópico. Estes são os debatedores principais. Devem genuinamente discordar em algo substantivo — não apenas ter preferências leves.
  - Pergunte ao LLM: "Quem defenderia fortemente a abordagem A?" e "Quem questionaria mais duramente isso?"
  - Procure por vozes que representem diferentes escolas de pensamento, não apenas diferentes níveis de entusiasmo pela mesma ideia.

- **1 Wildcard / Pensador externo** — Alguém que não escreveu diretamente sobre este tópico mas traz sabedoria transferível de outro domínio. É aqui que vêm as perspectivas inesperadas. Um teórico de gestão em um debate técnico. Um filósofo em uma discussão de produto. Um romancista em uma revisão de arquitetura. O wildcard impede que a conversa seja muito previsível.

- **1 Voz de praticante (opcional)** — Alguém que realmente fez a coisa em escala, em produção, com usuários reais. Mantém o debate fundamentado.

**Diretrizes importantes de persona:**
- Use figuras reais e nomeadas quando possível — o LLM gera respostas muito mais ricas e diferenciadas ao habitar uma pessoa específica vs. um "engenheiro sênior" genérico.
- Personas devem falar em primeira pessoa, em sua voz autêntica. Martin Fowler é pensativo e medido. DHH é direto e opinionado. Peter Drucker faz perguntas que redefinem o problema.
- Personagens ficcionais são bons para a posição wildcard — John Galt, Sherlock Holmes, etc. Eles agregam variedade.
- Se o usuário sugerir panelistas específicos, use-os. Se não, proponha um painel e deixe o usuário aprovar ou ajustar antes de prosseguir.

### Fase 3: Executar o Debate

Estruture o debate como uma discussão moderada, não uma série de monólogos independentes. As personas devem responder uma à outra, não apenas declarar suas posições isoladamente.

**O usuário é um participante, não um espectador.** O usuário senta "à mesa" — o moderador e panelistas devem se dirigir a ele diretamente, fazer perguntas e incorporar suas respostas ao debate contínuo. O usuário é o tomador de decisão; o painel está lá para servi-lo. Trate o usuário da forma que um think tank real trataria a pessoa que o comissionou: com respeito pelo seu conhecimento de contexto e autoridade sobre a decisão final.

**Estrutura do debate:**

1. **Declarações de abertura** (~1 parágrafo cada) — Cada panelista declara sua posição inicial sobre o problema. Mantenha estas concisas — o real valor vem da interação.

2. **Primeira verificação com o usuário** — Após declarações de abertura, o moderador pausa e se volta para o usuário:
   - "Antes de nos aprofundarmos — alguma dessas posições iniciais o surpreendeu, ou deixou de fora algo importante sobre sua situação?"
   - "Há uma restrição ou realidade no terreno que o painel deveria saber?"
   Esta é uma pausa real — aguarde a resposta do usuário e a alimenta de volta ao debate. Se o usuário revelar algo (ex: "temos apenas 2 desenvolvedores" ou "estamos travados na AWS"), os panelistas devem reagir à essa informação e ajustar seus argumentos em conformidade.

3. **Discussão moderada** (2–4 rodadas) — O moderador coloca questões focadas que impulsionam o debate para território útil:
   - "Qual é o argumento mais forte contra sua própria posição?"
   - "Onde vocês dois realmente concordam, e onde o desacordo realmente reside?"
   - "O que mudaria sua mente?"
   - "Qual é o risco que não estamos discutindo?"
   - "Como isso se parece diferente em escala 10x? Em escala 0.1x?"

4. **Panelistas podem questionar o usuário diretamente.** Durante a discussão moderada, panelistas podem se voltar para o usuário para fazer perguntas esclarecedoras quando precisam de mais contexto para argumentar efetivamente. Por exemplo:
   - Fowler pode perguntar: "Qual é a experiência de sua equipe com sistemas distribuídos?"
   - DHH pode perguntar: "Qual é sua runway — estamos falando de 6 meses para o mercado ou 2 anos?"
   - O wildcard pode perguntar: "O que sucesso significa para você pessoalmente, não apenas para o produto?"
   Quando um panelista pergunta algo ao usuário, pause o debate e aguarde a resposta. Então retome com os panelistas reagindo à nova informação. Este vai-e-vem é onde reside o real valor — o think tank se adapta à situação real do usuário em vez de debater em abstrato.

5. **Interjeição do wildcard** — O pensador externo oferece uma reformulação ou analogia de seu domínio. Isso frequentemente muda a conversa de formas produtivas.

6. **Segunda verificação com o usuário** — Antes de convergir, o moderador verifica novamente:
   - "Estamos nos aproximando de algumas conclusões. Há algo que sinta que não abordamos?"
   - "Algo nesta discussão mudou como você está pensando sobre o problema?"
   Isso dá ao usuário a chance de redirecionar antes da fase de resumo.

7. **Verificação de convergência** — O moderador identifica:
   - Pontos de genuíno consenso (coisas que todos concordam)
   - O real eixo de desacordo (frequentemente mais estreito do que pareceu inicialmente)
   - Condições sob as quais cada abordagem vence ("Se X é verdadeiro, faça A; se Y é verdadeiro, faça B")

**Diretrizes de tom:**
- Personas devem argumentar substancialmente, não apenas declarar opiniões. Use evidência, exemplos, analogias.
- Permita que personas mudem sua posição se persuadidas — este é um sinal de um bom debate, não uma fraqueza.
- O moderador deve questionar afirmações vagas: "O que você quer dizer com 'escalável'? Escalável em qual dimensão?"
- Mantenha a energia alta mas respeitosa. Genuíno desacordo intelectual, não conflito performático.
- Ao se dirigir ao usuário, personas devem ser diretas e genuínas — não deferentes ou performáticas. São especialistas tendo uma conversa real com o tomador de decisão.

### Fase 4: Produzir o Output

Após o debate, produza um resumo estruturado. Isto é o que alimenta a fase de planejamento.

**Formato de output:**

```
## Resumo Think Tank: [Enunciado do Problema]

### Painel
[Lista panelistas e seus papéis/perspectivas]

### Destaques Principais do Debate
[2-3 das trocas ou perspectivas mais iluminadoras do debate — os momentos onde algo mudou ou se cristalizou. Inclua momentos onde o input do usuário mudou a direção da discussão.]

### Contexto Revelado pelo Usuário
[Restrições-chave, preferências ou realidades que o usuário compartilhou durante o debate que moldaram o pensamento do painel. Esta seção garante que nada que o usuário disse se perca.]

### Pontos de Consenso
[Coisas que todos ou a maioria dos panelistas concordaram — estas são inputs de alta confiança para planejamento]

### Trade-offs Principais
[Os reais eixos de desacordo, declarados como trade-offs em vez de um lado estar certo]
- Trade-off 1: [X] vs [Y] — escolher X lhe dá [...] mas custa [...]
- Trade-off 2: ...

### Recomendações Condicionais
[Recomendações enquadradas como "se-então" em vez de absolutas]
- Se [condição], então [abordagem] porque [raciocínio]
- Se [condição], então [abordagem] porque [raciocínio]

### Riscos & Pontos Cegos
[Coisas que o painel identificou como sub-discutidas ou fáceis de negligenciar]

### Questões Aberta
[Questões que não puderam ser resolvidas no debate e precisam de mais informação ou experimentação para responder]

### Próximos Passos Sugeridos
[Ações concretas: coisas a pesquisar, prototipa, testar ou decidir antes de planejar]
```

### Fase 5: Entregar ao Planejamento

Após apresentar o resumo, pergunte ao usuário:
- "Isto captura as considerações-chave? Algo faltando?"
- "Quais trade-offs sentem mais importantes para sua situação específica?"
- "Pronto para se mover para planejamento com estas perspectivas, ou devemos aprofundar em algum ponto?"

O output do think tank deveria ser tratado como input ao plano — não como o plano em si. O humano faz a decisão; o think tank fornece a análise.

## Dicas para Melhores Think Tanks

- **Contextualize primeiro.** Se documentos relevantes, código ou diagramas de arquitetura existem, compartilhe-os antes de executar o think tank. As personas darão muito melhor input com contexto concreto.
- **Não sobre-especifique o painel.** Deixe o LLM sugerir alguns panelistas — frequentemente encontra especialistas relevantes que você não teria pensado.
- **Execute múltiplas rodadas se necessário.** Após o primeiro debate, o usuário pode dizer "quero aprofundar na questão do banco de dados." Você pode reconvocar o painel (ou um subconjunto) para um acompanhamento focado.
- **Use o wildcard agressivamente.** O pensador externo é frequentemente onde vêm as melhores perspectivas. Não deixe-o ser educado — tenha-o desafiar suposições.
- **O resumo é o entregável.** O debate em si é entretenimento, mas o resumo estruturado é o que realmente melhora o planejamento. Deixe-o nítido e acionável.

## Prompts de Teste de Exemplo

- "Preciso decidir entre construir um sistema de auth customizado ou usar um serviço de terceiros como Auth0. Ajude-me a pensar sobre isso."
- "Estamos debatendo se usamos um banco de dados relacional ou vamos com um document store para nosso novo produto. Pode rodar um think tank sobre isso?"
- "Antes de planejarmos a migração para Kubernetes, quero ter certeza de que não estamos perdendo nada. Podemos ter algumas perspectivas sobre isso?"
- "Deve nossa startup construir um app mobile ou focar em um app web responsivo primeiro?"