---
name: roteiro-pauta-quente
description: "Pesquisa as pautas mais quentes e em alta do nicho do usuário na web, seleciona a melhor oportunidade de conteúdo e transforma em um roteiro completo pronto para gravar, entregue como arquivo .docx profissional. Use esta skill sempre que alguém pedir para buscar tendências de conteúdo, encontrar pautas em alta, descobrir o que está bombando no nicho, criar conteúdo baseado em tendências, fazer roteiro sobre assunto do momento, transformar trend em vídeo, ou pedir ideias de conteúdo atualizadas. Também aciona quando mencionarem 'pauta quente', 'trend do momento', 'o que tá em alta', 'conteúdo do dia', 'roteiro baseado em tendência', 'o que tá bombando', 'pautas trending', 'conteúdo viral', ou qualquer pedido que combine buscar tendências atuais + criar roteiro pronto para gravar. Funciona para qualquer nicho de conteúdo digital: marketing, tecnologia, IA, negócios, saúde, educação, lifestyle, etc."
---

# Roteiro Pauta Quente — Da Tendência ao Roteiro em Minutos

Skill que pesquisa as pautas mais quentes do nicho do usuário, seleciona a melhor oportunidade de conteúdo e entrega um roteiro completo pronto para gravar, em formato .docx profissional.

## O que esta skill faz

1. Pesquisa tendências atuais no nicho do usuário usando web search
2. Filtra e ranqueia as pautas por potencial de viralização
3. Seleciona a melhor oportunidade
4. Transforma em um roteiro completo (com hook, fala scriptada, CTA)
5. Entrega como arquivo .docx formatado e pronto para usar

## Fluxo de Trabalho

### Passo 1 — Entender o nicho

Se o usuário não informou o nicho, perguntar de forma direta:
"qual é o seu nicho de conteúdo? (ex: marketing digital, IA, fitness, culinária...)"

Se já informou, seguir direto para a pesquisa.

Informações úteis (mas não obrigatórias) para refinar a busca:
- Nicho específico (ex: "marketing para e-commerce" em vez de só "marketing")
- Plataforma principal (Instagram, TikTok, YouTube — default: Instagram)
- Tom de voz preferido (informal, profissional, divertido — default: informal/acessível)

Não travar o fluxo pedindo muita informação. Se tem o nicho, já pode rodar.

### Passo 2 — Pesquisar tendências

Usar web search para buscar pautas quentes. Fazer pelo menos 3-4 buscas variadas:

**Buscas recomendadas:**
1. "[nicho] tendências [mês atual] [ano]" — para pegar o que está em alta agora
2. "[nicho] polêmica OU novidade OU atualização" — para pegar assuntos que geram debate
3. "[nicho] Instagram OU TikTok viral" — para ver o que está performando nas redes
4. "[nicho] news" ou termos específicos do nicho em inglês — para pegar tendências globais antes de chegarem ao Brasil

**Fontes de qualidade para tendências:**
- Portais de notícias do nicho
- Threads e posts virais no X/Twitter
- Newsletters especializadas
- Google Trends
- Lançamentos de ferramentas/produtos recentes

### Passo 3 — Filtrar e ranquear

Dos resultados encontrados, selecionar 3-5 pautas e ranquear usando estes critérios:

| Critério | Peso | O que avaliar |
|----------|------|---------------|
| Timing | Alto | É novidade? Está no pico de atenção? |
| Potencial de opinião | Alto | Dá pra dar um ângulo próprio? Gera debate? |
| Relevância pro público | Alto | O público do nicho se importa com isso? |
| Facilidade de produção | Médio | Dá pra gravar rápido sem muita produção? |
| Potencial de viralização | Médio | Tem elementos de curiosidade/polêmica/surpresa? |

Apresentar as pautas ranqueadas ao usuário:

```
🔥 pautas quentes do momento para [nicho]:

1. [pauta] — ⭐ potencial muito alto
   por que: [explicação em 1 linha]

2. [pauta] — ⭐ potencial alto
   por que: [explicação em 1 linha]

3. [pauta] — ⭐ potencial médio-alto
   por que: [explicação em 1 linha]

💎 minha recomendação: a pauta #1 porque [razão estratégica].

quer que eu crie o roteiro da #1 ou prefere outra?
```

Se o usuário quiser ir rápido ("tanto faz, faz o melhor"), criar direto o roteiro da pauta #1 sem esperar confirmação.

### Passo 4 — Criar o roteiro

O roteiro deve ser completo e scriptado (falas escritas, não apenas tópicos). Estrutura:

```
🎬 ROTEIRO: [título do vídeo]

📌 Pauta: [qual tendência está sendo abordada]
🎯 Ângulo: [qual o posicionamento/opinião sobre o tema]
⏱️ Duração estimada: [X segundos/minutos]
📱 Formato: reels / tiktok / stories

═══════════════════════════════════════════

📱 TELA INICIAL (copy que aparece na tela):
[frase impactante, máximo 2 linhas, lowercase]

═══════════════════════════════════════════

🎤 ROTEIRO COMPLETO:

[ABERTURA — hook falado, 3-5 segundos]
"[fala exata]"

[CONTEXTO — situar o espectador, 5-10 segundos]
"[fala exata]"

[DESENVOLVIMENTO — conteúdo principal, opinião, demonstração]
"[fala exata]"

[se aplicável: CORTA PRA TELA / DEMONSTRAÇÃO]
[narração durante a demonstração]

[VOLTA PRO APRESENTADOR]

[FECHAMENTO + CTA — 5-10 segundos]
"[fala exata com CTA claro]"

═══════════════════════════════════════════

📝 LEGENDA:
[legenda curta e direta para o post]

#️⃣ HASHTAGS:
[hashtags relevantes ao tema e nicho]

═══════════════════════════════════════════

💡 DICAS DE GRAVAÇÃO:
- [dica 1 sobre enquadramento, ritmo ou edição]
- [dica 2 sobre momento ideal de publicar]
- [dica 3 sobre como maximizar o alcance desse conteúdo]
```

### Passo 5 — Gerar o .docx

Criar o roteiro como arquivo .docx formatado profissionalmente usando a biblioteca docx (Node.js).

O documento deve ter:
- Título estilizado no topo
- Seções bem divididas com headings
- Formatação limpa e fácil de ler no celular (muitos criadores leem o roteiro no telefone enquanto gravam)
- Font size confortável (12-14pt para o corpo)
- Espaçamento generoso entre seções

```bash
npm install -g docx 2>/dev/null
```

Criar o script Node.js para gerar o .docx e salvar na pasta de outputs.

## Regras de Qualidade do Roteiro

### Tom de voz
- Natural e conversacional (como se estivesse falando, não lendo)
- Adaptar ao tom que o criador usa (se informou) ou usar informal/acessível como default
- Sem jargões excessivos sem explicação
- Frases curtas e diretas — lembrar que é pra ser FALADO, não lido

### Sobre a pauta quente
- A pauta precisa ser ATUAL (última semana idealmente, máximo último mês)
- Se não encontrar nada verdadeiramente quente, ser honesto e sugerir uma pauta evergreen com ângulo atual
- Sempre dar um ângulo/opinião sobre a pauta — não é notícia, é conteúdo com posicionamento
- Conectar a pauta com algo prático pro público ("e o que isso significa pra você que [situação do público]")

### Sobre o hook
- O hook é a parte mais importante do roteiro
- Precisa funcionar tanto como texto na tela quanto como fala
- Deve gerar curiosidade ou espanto nos primeiros 3 segundos
- Em lowercase (padrão Instagram)

### Sobre o CTA
- Sempre incluir um CTA claro no final
- Sugerir palavra-chave para comentário relacionada ao tema
- Pedir para salvar e seguir
- Ser específico: "comenta [PALAVRA] que eu te mando [algo de valor]"

## Checklist de qualidade

Antes de entregar:
- [ ] A pauta é realmente atual e relevante?
- [ ] O hook gera curiosidade nos primeiros 3 segundos?
- [ ] O roteiro está scriptado (falas completas, não tópicos)?
- [ ] O tom é natural e parece fala, não texto?
- [ ] Tem CTA claro com palavra-chave para comentário?
- [ ] A legenda é curta e direta?
- [ ] O .docx está formatado e legível?
- [ ] O conteúdo tem um ângulo/opinião própria (não é só notícia)?
- [ ] A duração estimada é realista para o formato?

