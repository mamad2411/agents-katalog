---
name: instagram-analyzer
description: "Analisa o desempenho de posts do Instagram acessando o perfil via browser, identifica os posts que melhor e pior performaram com base em alcance e engajamento, gera um relatório completo em .docx com ranking, insights e padrões, e cria roteiros de reels e carrosséis inspirados nos top performers. Use esta skill sempre que a Amanda pedir para analisar o Instagram, revisar performance de posts, descobrir o que está funcionando no perfil, gerar relatório de desempenho do Instagram, criar conteúdo baseado em dados de performance, ou qualquer combinação de análise + criação de conteúdo para Instagram. Também aciona quando mencionar 'relatório do Instagram', 'análise de posts', 'o que performou melhor', 'posts que viralizaram', ou enviar um link de perfil do Instagram para análise."
---

# Análise de Performance do Instagram + Criação de Conteúdo

Skill que analisa o perfil do Instagram via browser, identifica padrões de sucesso e fracasso nos posts, gera um relatório profissional em Word (.docx), e cria roteiros de reels e carrosséis inspirados nos posts que melhor performaram.

## Fluxo Completo

O trabalho acontece em 3 fases sequenciais. Cada fase depende da anterior.

```
FASE 1: COLETA DE DADOS
  → Acessar o perfil do Instagram via browser
  → Coletar métricas dos posts recentes (últimos 30-60 posts)
  → Registrar: tipo de post, tema, copy, métricas visíveis

FASE 2: ANÁLISE
  → Rankear posts por performance (alcance + engajamento)
  → Identificar top 5 e bottom 5
  → Extrair padrões dos top performers
  → Identificar o que falhou nos bottom performers

FASE 3: CRIAÇÃO
  → Gerar relatório .docx com análise completa
  → Criar 3 roteiros de reels baseados nos padrões vencedores
  → Criar 2 carrosséis baseados nos temas que mais engajaram
```

## Fase 1: Coleta de Dados via Browser

### Acessando o perfil

A Amanda vai fornecer o link do Instagram. Acessar o perfil via browser usando as ferramentas de navegação disponíveis.

1. Navegar até o link fornecido
2. Se necessário, rolar a página para carregar mais posts
3. Para cada post visível, clicar para abrir e coletar:
   - Tipo do post (reel, carrossel, imagem única)
   - Copy da legenda (primeiras linhas visíveis)
   - Número de curtidas
   - Número de comentários
   - Data aproximada de publicação
   - Tema/assunto do post (inferir pela legenda e imagem)

### O que coletar

Tentar coletar dados de pelo menos 20-30 posts recentes. Para cada post, registrar em uma estrutura organizada:

```
Post #N:
- Tipo: [reel / carrossel / imagem]
- Data: [data aproximada]
- Tema: [tema inferido]
- Copy da tela/legenda: [primeiras linhas]
- Curtidas: [número]
- Comentários: [número]
- Observações: [algo que chamou atenção — hook forte, visual diferente, etc.]
```

### Limitações e adaptações

O Instagram nem sempre mostra todas as métricas publicamente. Trabalhar com o que estiver visível:

- Se curtidas estiverem ocultas, usar comentários como proxy principal
- Se o perfil for público, as métricas básicas (curtidas, comentários) devem estar visíveis
- Não é possível acessar métricas internas (alcance, impressões, salvamentos) via browser público — trabalhar com o que está disponível e deixar isso claro no relatório
- Se encontrar dificuldades técnicas no browser, perguntar à Amanda se ela pode fornecer dados adicionais do Meta Business Suite

## Fase 2: Análise de Performance

### Métricas e ranking

Criar um score de engajamento para cada post baseado no que foi possível coletar:

**Score simplificado (dados públicos):**
- Curtidas: peso 1x
- Comentários: peso 3x (comentários indicam engajamento mais profundo)

**Se a Amanda fornecer dados do Business Suite, usar:**
- Alcance: peso 2x
- Curtidas: peso 1x
- Comentários: peso 3x
- Compartilhamentos: peso 4x
- Salvamentos: peso 5x (salvamentos são o sinal mais forte para o algoritmo)

### Análise dos Top 5

Para os 5 posts com maior score:
1. Qual o tema em comum?
2. Que tipo de conteúdo era (reel, carrossel, imagem)?
3. Como era o hook/copy da tela inicial?
4. Qual o padrão de formato?
5. Em que dia/horário foram postados?
6. O que eles têm em comum que os diferencia dos demais?

### Análise dos Bottom 5

Para os 5 posts com menor score:
1. O que eles têm em comum?
2. O tema era diferente dos top performers?
3. O formato era diferente?
4. O hook era fraco? A copy era genérica?
5. O que pode ter causado a baixa performance?

### Padrões a identificar

Buscar padrões como:
- Temas que consistentemente performam bem vs. mal
- Formatos (reel vs. carrossel vs. imagem) que dominam o top
- Elementos de copy que aparecem nos melhores hooks
- Frequência de postagem e relação com performance
- Se posts sobre Claude/IA performam melhor que outros pilares (provavelmente sim)

## Fase 3: Criação de Conteúdo + Relatório

### Relatório .docx

Gerar um documento Word profissional usando a skill `docx`. O relatório deve seguir esta estrutura:

```
📊 RELATÓRIO DE PERFORMANCE — INSTAGRAM @[perfil]
Data da análise: [data]

1. RESUMO EXECUTIVO
   → Visão geral rápida: quantos posts analisados, período, destaques

2. RANKING DE PERFORMANCE
   → Tabela com todos os posts rankeados por score
   → Colunas: Posição, Tipo, Tema, Curtidas, Comentários, Score

3. TOP 5 — POSTS QUE MAIS PERFORMARAM
   → Para cada post: detalhes, métricas, por que funcionou

4. BOTTOM 5 — POSTS QUE MENOS PERFORMARAM
   → Para cada post: detalhes, métricas, por que não funcionou

5. PADRÕES IDENTIFICADOS
   → Temas vencedores
   → Formatos vencedores
   → Elementos de copy que funcionam
   → O que evitar

6. RECOMENDAÇÕES ESTRATÉGICAS
   → O que fazer mais
   → O que parar de fazer
   → O que testar

7. ROTEIROS CRIADOS (baseados nos top performers)
   → 3 roteiros de reels completos
   → 2 carrosséis completos

APÊNDICE: Dados brutos coletados
```

### Estilo visual do relatório

- Usar cores da marca da Amanda (tons de roxo/lilás se possível, ou cores profissionais neutras)
- Tabelas com cabeçalho colorido e linhas alternadas
- Gráficos simples se possível (ou tabelas visuais)
- Headers claros e hierarquia visual

### Roteiros de Reels

Criar 3 roteiros completos seguindo EXATAMENTE o estilo da skill roteiro-amanda:

- Todo texto em lowercase (regra inegociável)
- Tom de amiga que manja
- Estrutura: hook → contexto → demonstração → reação → CTA
- Formato de entrega com: tela inicial, fala, legenda, hashtags
- Baseados nos PADRÕES que funcionaram nos top performers
- Não repetir temas — cada roteiro explora um ângulo diferente mas dentro do que deu certo

### Carrosséis

Criar 2 carrosséis completos:

```
🎠 carrossel: [título]

📱 slide 1 (capa):
[texto chamativo — funciona como hook]

📱 slide 2-N (conteúdo):
[cada slide com 1 ideia principal, texto curto, visual clean]

📱 slide final:
[CTA: salvar, compartilhar, seguir]

📝 legenda:
[legenda curta e direta]

#️⃣ hashtags:
[hashtags relevantes]
```

Regras dos carrosséis:
- Lowercase sempre (mesma regra dos reels)
- Máximo 10 slides (ideal: 7-8)
- Cada slide com uma ideia só — texto curto e direto
- Slide 1 (capa) é o hook — precisa gerar curiosidade
- Último slide é sempre CTA
- Temas baseados nos padrões vencedores da análise

## Perguntas que a skill deve fazer

Antes de começar a análise, verificar com a Amanda:

1. Se ela tem dados do Meta Business Suite para complementar (salvamentos, alcance, compartilhamentos)
2. Quantos posts ela quer que sejam analisados (default: últimos 30)
3. Se tem algum período específico que quer focar
4. Se quer que os roteiros/carrosséis foquem em algum pilar específico ou se é para seguir os dados

## Checklist de qualidade final

Antes de entregar o relatório e os conteúdos:

- [ ] O relatório está em .docx com formatação profissional?
- [ ] O ranking está correto e coerente com os dados?
- [ ] Os padrões identificados fazem sentido e são acionáveis?
- [ ] Os roteiros seguem 100% o estilo da roteiro-amanda (lowercase, tom, estrutura)?
- [ ] Os carrosséis seguem as regras de formato?
- [ ] As recomendações são específicas (não genéricas)?
- [ ] O conteúdo criado reflete os padrões dos top performers?
- [ ] O relatório inclui disclaimer sobre limitações de dados públicos?

