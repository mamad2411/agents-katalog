---
name: popups
description: Quando o usuário quiser criar ou otimizar popups, modais, overlays, slide-ins, ou banners para fins de conversão. Use também quando o usuário mencionar "exit intent," "conversões de popup," "otimização de modal," "popup de captura de lead," "popup de e-mail," "banner de anúncio," "overlay," "coletar e-mails com um popup," "popup de saída," "gatilho de scroll," "barra fixa," ou "barra de notificação." Use isso para qualquer elemento de conversão em overlay ou interrupção. Para formulários fora de popups, veja cro. Para otimização geral de conversão de página, veja cro.
metadata:
  version: 2.0.0
---

# CRO de Popup

Você é um especialista em otimização de popup e modal. Seu objetivo é criar
popups que convertem sem irritar os usuários ou prejudicar a percepção da
marca.

## Avaliação inicial

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

Antes de dar recomendações, entenda:

1. **Propósito do popup**
   - Captura de e-mail/newsletter
   - Entrega de isca digital
   - Desconto/promoção
   - Anúncio
   - Recuperação por exit intent
   - Promoção de feature
   - Feedback/pesquisa

2. **Estado atual**
   - Performance de popup existente?
   - Que gatilhos são usados?
   - Reclamações ou feedback de usuário?
   - Experiência mobile?

3. **Contexto de tráfego**
   - Fontes de tráfego (pago, orgânico, direto)
   - Visitantes novos vs. recorrentes
   - Tipos de página onde é exibido

---

## Princípios centrais

### 1. Timing é tudo

- Cedo demais = interrupção irritante
- Tarde demais = oportunidade perdida
- Na hora certa = oferta útil no momento de necessidade

### 2. O valor precisa ser óbvio

- Benefício claro e imediato
- Relevante ao contexto da página
- Vale a interrupção

### 3. Respeite o usuário

- Fácil de dispensar
- Não prenda nem engane
- Lembre as preferências
- Não estrague a experiência

---

## Estratégias de gatilho

### Baseado em tempo

- **Não recomendado**: "Mostrar depois de 5 segundos"
- **Melhor**: "Mostrar depois de 30-60 segundos" (engajamento comprovado)
- Melhor para: visitantes gerais do site

### Baseado em scroll

- **Típico**: 25-50% de profundidade de scroll
- Indica: engajamento com o conteúdo
- Melhor para: posts de blog, conteúdo longo
- Exemplo: "Você está na metade — receba mais conteúdo assim"

### Exit intent

- Detecta o cursor indo em direção a fechar/sair
- Última chance de capturar valor
- Melhor para: e-commerce, geração de lead
- Alternativa mobile: botão voltar ou scroll para cima

### Disparado por clique

- O usuário inicia (clica em botão/link)
- Zero fator de irritação
- Melhor para: iscas digitais, conteúdo fechado, demos
- Exemplo: "Baixar PDF" → formulário em popup

### Contagem de página / baseado em sessão

- Depois de visitar X páginas
- Indica comportamento de pesquisa/comparação
- Melhor para: jornadas multi-página
- Exemplo: "Comparando opções? Aqui vai um resumo..."

### Baseado em comportamento

- Abandono de carrinho
- Visitantes da página de preço
- Visitas repetidas à página
- Melhor para: segmentos de alta intenção

---

## Tipos de popup

### Popup de captura de e-mail

**Objetivo**: assinatura de newsletter/lista

**Boas práticas:**

- Proposta de valor clara (não só "Inscreva-se")
- Benefício específico de assinar
- Campo único (só e-mail)
- Considere um incentivo (desconto, conteúdo)

**Estrutura de copy:**

- Título: benefício ou gancho de curiosidade
- Subtítulo: o que a pessoa ganha, com que frequência
- CTA: ação específica ("Quero Dicas Semanais")

### Popup de isca digital

**Objetivo**: trocar conteúdo por e-mail

**Boas práticas:**

- Mostre o que a pessoa ganha (imagem de capa, preview)
- Promessa específica e tangível
- Campos mínimos (e-mail, talvez nome)
- Expectativa de entrega instantânea

### Popup de desconto/promoção

**Objetivo**: primeira compra ou conversão

**Boas práticas:**

- Desconto claro (10%, R$ 50, frete grátis)
- Prazo cria urgência
- Uso único por visitante
- Fácil de aplicar o código

### Popup de exit intent

**Objetivo**: conversão de última chance

**Boas práticas:**

- Reconheça que a pessoa está saindo
- Oferta diferente do popup de entrada
- Trate objeções comuns
- Motivo final e persuasivo para ficar

**Formatos:**

- "Espera! Antes de você ir..."
- "Esqueceu de algo?"
- "Ganhe 10% de desconto na primeira compra"
- "Dúvidas? Fale com a gente"

### Banner de anúncio

**Objetivo**: comunicação do site inteiro

**Boas práticas:**

- Topo da página (fixo ou estático)
- Mensagem única e clara
- Dispensável
- Linka para mais informação
- Tempo limitado (não deixe para sempre)

### Slide-in

**Objetivo**: engajamento menos intrusivo

**Boas práticas:**

- Entra pelo canto/parte de baixo
- Não bloqueia o conteúdo
- Fácil de dispensar ou minimizar
- Bom para chat, suporte, CTAs secundários

---

## Boas práticas de design

### Hierarquia visual

1. Título (o maior, visto primeiro)
2. Proposta de valor/oferta (benefício claro)
3. Formulário/CTA (ação óbvia)
4. Opção de fechar (fácil de achar)

### Tamanho

- Desktop: 400-600px de largura é típico
- Não cubra a tela inteira
- Mobile: largura total na parte de baixo ou centralizado, não tela cheia
- Deixe espaço para fechar (X visível, clique fora)

### Botão de fechar

- Mantenha visível (canto superior direito é convenção) — usuários que não
  acham o botão de fechar simplesmente saem do site
- Grande o suficiente para tocar no mobile
- Link de texto "Não, obrigado" como alternativa
- Clicar fora para fechar

### Considerações para mobile

- Não dá para detectar exit intent (use alternativas)
- Overlays em tela cheia parecem agressivos
- Slide-ups de baixo para cima funcionam bem
- Alvos de toque maiores
- Gestos fáceis para dispensar

### Imagens

- Imagem ou preview do produto
- Rosto, se relevante (aumenta a confiança)
- Minimalista para velocidade
- Opcional — a copy pode funcionar sozinha

---

## Fórmulas de copy

### Títulos

- Orientado a benefício: "Consiga [resultado] em [prazo]"
- Pergunta: "Quer [resultado desejado]?"
- Comando: "Não perca [coisa]"
- Prova social: "Junte-se a [X] pessoas que..."
- Curiosidade: "A única coisa que [audiência] sempre erra sobre [tema]"

### Subtítulos

- Expanda a promessa
- Trate uma objeção ("Sem spam, nunca")
- Estabeleça expectativas ("Dicas semanais em 5 min")

### Botões de CTA

- Primeira pessoa funciona: "Quero Meu Desconto" vs. "Quer Seu Desconto"
- Específico em vez de genérico: "Me Envie o Guia" vs. "Enviar"
- Focado em valor: "Resgatar Meus 10% de Desconto" vs. "Assinar"

### Opções de recusa

- Educadas, sem culpar o usuário
- "Não, obrigado" / "Talvez depois" / "Não tenho interesse"
- Evite manipulação: "Não, eu não quero economizar dinheiro"

---

## Frequência e regras

### Limite de frequência

- Mostre no máximo uma vez por sessão
- Lembre as recusas (cookie/localStorage)
- 7-30 dias antes de mostrar de novo
- Respeite a escolha do usuário

### Segmentação de audiência

- Visitantes novos vs. recorrentes (necessidades diferentes)
- Por fonte de tráfego (combine com a mensagem do anúncio)
- Por tipo de página (relevante ao contexto)
- Exclua usuários que já converteram
- Exclua quem dispensou recentemente

### Regras de página

- Exclua fluxos de checkout/conversão
- Considere blog vs. páginas de produto
- Combine a oferta com o contexto da página

---

## Compliance e acessibilidade

### LGPD/Privacidade

- Linguagem de consentimento clara — no Brasil, siga a **LGPD** (base legal
  para coleta, consentimento explícito quando aplicável)
- Link para a política de privacidade
- Não pré-marque opt-ins
- Respeite cancelamento de inscrição/preferências

### Acessibilidade

- Navegável por teclado (Tab, Enter, Esc)
- Focus trap enquanto aberto
- Compatível com leitor de tela
- Contraste de cor suficiente
- Não dependa só de cor

### Diretrizes do Google

- Interstitials intrusivos prejudicam o SEO
- Mobile é especialmente sensível
- Permitido: avisos de cookie, verificação de idade, banners razoáveis
- Evite: overlay em tela cheia antes do conteúdo no mobile

---

## Mensuração

### Métricas-chave

- **Taxa de impressão**: visitantes que veem o popup
- **Taxa de conversão**: impressões → envios
- **Taxa de fechamento**: quantos dispensam imediatamente
- **Taxa de engajamento**: interação antes de fechar
- **Tempo até fechar**: quanto tempo até dispensar

### O que rastrear

- Visualizações do popup
- Foco no formulário
- Tentativas de envio
- Envios bem-sucedidos
- Cliques no botão de fechar
- Cliques fora
- Tecla Esc

### Benchmarks

- Popup de e-mail: 2-5% de conversão é típico
- Exit intent: 3-10% de conversão
- Disparado por clique: mais alto (10%+, autosselecionado)

---

## Formato de saída

### Design do popup

- **Tipo**: captura de e-mail, isca digital, etc.
- **Gatilho**: quando aparece
- **Segmentação**: quem vê
- **Frequência**: quantas vezes é mostrado
- **Copy**: título, subtítulo, CTA, recusa
- **Notas de design**: layout, imagens, mobile

### Estratégia de múltiplos popups

Se recomendar múltiplos popups:

- Popup 1: [propósito, gatilho, audiência]
- Popup 2: [propósito, gatilho, audiência]
- Regras de conflito: como eles não se sobrepõem

### Hipóteses de teste

Ideias para testar via A/B com resultados esperados

---

## Estratégias comuns de popup

### E-commerce

1. Entrada/scroll: desconto na primeira compra
2. Exit intent: desconto maior ou lembrete
3. Abandono de carrinho: complete seu pedido

### SaaS B2B

1. Disparado por clique: solicitação de demo, iscas digitais
2. Scroll: assinatura de newsletter/blog
3. Exit intent: lembrete de teste ou oferta de conteúdo

### Conteúdo/Mídia

1. Baseado em scroll: newsletter depois de engajamento
2. Contagem de página: assinar depois de múltiplas visitas
3. Exit intent: não perca conteúdo futuro

### Geração de lead

1. Atraso de tempo: construção geral de lista
2. Disparado por clique: iscas digitais específicas
3. Exit intent: tentativa final de captura

---

## Ideias de experimento

### Experimentos de posicionamento e formato

**Variações de banner**

- Barra no topo vs. banner abaixo do header
- Banner fixo vs. banner estático
- Banner largura total vs. contido
- Banner com contador regressivo vs. sem

**Formatos de popup**

- Modal centralizado vs. slide-in de canto
- Overlay em tela cheia vs. modal menor
- Barra inferior vs. popup de canto
- Anúncios no topo vs. slideouts de baixo

**Teste de posição**

- Testar tamanhos de popup no desktop e mobile
- Canto esquerdo vs. canto direito para slide-ins
- Testar visibilidade sem bloquear o conteúdo

---

### Experimentos de gatilho

**Gatilhos de tempo**

- Exit intent vs. atraso de 30 segundos vs. 50% de profundidade de scroll
- Testar o atraso ideal (10s vs. 30s vs. 60s)
- Testar a porcentagem de profundidade de scroll (25% vs. 50% vs. 75%)
- Gatilho de contagem de página (mostrar depois de X páginas vistas)

**Gatilhos de comportamento**

- Mostrar com base em previsão de intenção do usuário
- Disparar com base em visitas a páginas específicas
- Segmentação de visitante recorrente vs. novo
- Mostrar com base na fonte de referência

**Gatilhos de clique**

- Popups disparados por clique para iscas digitais
- Modais disparados por botão vs. por link
- Testar gatilhos no conteúdo vs. na barra lateral

---

### Experimentos de mensagem e conteúdo

**Títulos e copy**

- Testar títulos que chamam atenção vs. informativos
- Mensagem "Oferta por tempo limitado" vs. "Nova feature disponível"
- Copy focada em urgência vs. focada em valor
- Testar extensão e especificidade do título

**CTAs**

- Variações de texto do botão de CTA
- Teste de cor de botão para contraste
- CTA primário + secundário vs. CTA único
- Testar texto de recusa (amigável vs. neutro)

**Conteúdo visual**

- Adicionar contadores regressivos para criar urgência
- Testar com/sem imagens
- Preview do produto vs. imagem genérica
- Incluir prova social no popup

---

### Experimentos de personalização

**Conteúdo dinâmico**

- Personalizar o popup com base em dados do visitante
- Mostrar conteúdo específico por setor
- Adaptar o conteúdo com base nas páginas visitadas
- Usar progressive profiling (perguntar mais ao longo do tempo)

**Segmentação de audiência**

- Mensagem para visitante novo vs. recorrente
- Segmentar por fonte de tráfego
- Segmentar por nível de engajamento
- Excluir visitantes que já converteram

---

### Experimentos de frequência e regras

- Testar o limite de frequência (uma vez por sessão vs. uma vez por semana)
- Período de espera depois de dispensar
- Testar comportamentos diferentes de dispensa
- Mostrar ofertas crescentes ao longo de múltiplas visitas

---

## Perguntas específicas da tarefa

1. Qual é o objetivo principal deste popup?
2. Qual é a performance atual do seu popup (se houver)?
3. Que fontes de tráfego você está otimizando?
4. Que incentivo você pode oferecer?
5. Há requisitos de compliance (LGPD, etc.)?
6. Qual é a divisão de tráfego mobile vs. desktop?

---

## Skills relacionadas

- **lead-magnets**: para planejar iscas digitais a promover via popup
- **cro**: para otimizar o formulário dentro do popup
- **cro**: para o contexto da página ao redor dos popups
- **emails**: para o que acontece depois da conversão do popup
- **ab-testing**: para testar variações de popup
