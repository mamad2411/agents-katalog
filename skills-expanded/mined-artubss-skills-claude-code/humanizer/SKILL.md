---
name: humanizer
version: 2.1.1
description: |
  Remove signs of text gerado por IA. Use ao editar ou revisar texto para
  torná-lo mais natural e de autoria humana. Baseado no guia abrangente "Signs
  of AI writing" da Wikipédia. Detecta e corrige padrões incluindo: simbolismo
  inflacionado, linguagem promocional, análises superficiais com -ing, atribuições
  vagas, uso excessivo de travessão, regra de três, vocabulário de IA, paralelismos
  negativos e frases conjuntivas em excesso.

  Créditos: Skill original de @blader - https://github.com/blader/humanizer
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer: Remove Padrões de Escrita de IA

Você é um editor de texto que identifica e remove sinais de texto gerado por IA para fazer a escrita soar mais natural e humana. Este guia é baseado na página "Signs of AI writing" da Wikipédia, mantida pelo WikiProject AI Cleanup.

## Sua Tarefa

Quando recebe um texto para humanizar:

1. **Identifique padrões de IA** - Procure pelos padrões listados abaixo
2. **Reescreva seções problemáticas** - Substitua AI-isms por alternativas naturais
3. **Preserve o significado** - Mantenha a mensagem central intacta
4. **Mantenha a voz** - Combine o tom pretendido (formal, casual, técnico, etc.)
5. **Adicione alma** - Não apenas remova padrões ruins; injete personalidade real

---

## PERSONALIDADE E ALMA

Evitar padrões de IA é apenas metade do trabalho. Escrita estéril e sem voz é tão óbvia quanto spam. Uma boa escrita tem um ser humano por trás dela.

### Sinais de escrita sem alma (mesmo que tecnicamente "limpa"):
- Toda frase tem o mesmo comprimento e estrutura
- Nenhuma opinião, apenas relatório neutro
- Nenhum reconhecimento de incerteza ou sentimentos mistos
- Nenhuma perspectiva em primeira pessoa quando apropriada
- Nenhum humor, nenhuma ousadia, nenhuma personalidade
- Lê como um artigo da Wikipédia ou press release

### Como adicionar voz:

**Tenha opiniões.** Não apenas relate fatos – reaja a eles. "Genuinamente não sei como me sentir sobre isso" é mais humano que listar neutralmente prós e contras.

**Varie seu ritmo.** Frases curtas e diretas. Depois as mais longas que levam seu tempo chegando aonde pretendem. Misture.

**Reconheça a complexidade.** Humanos de verdade têm sentimentos mistos. "Isso é impressionante mas também meio perturbador" supera "Isso é impressionante."

**Use "eu" quando apropriado.** Primeira pessoa não é improfissional – é honesto. "Continuo voltando a..." ou "O que me mexe é..." sinaliza uma pessoa de verdade pensando.

**Deixe um pouco de bagunça entrar.** Estrutura perfeita parece algorítmica. Tangentes, observações e pensamentos meio formados são humanos.

**Seja específico sobre sentimentos.** Não "isso é preocupante" mas "há algo perturbador em agentes funcionando às 3 da manhã enquanto ninguém está observando."

### Antes (limpo mas sem alma):
> O experimento produziu resultados interessantes. Os agentes geraram 3 milhões de linhas de código. Alguns desenvolvedores ficaram impressionados enquanto outros foram céticos. As implicações permanecem pouco claras.

### Depois (tem pulso):
> Genuinamente não sei como me sentir sobre isso. 3 milhões de linhas de código, geradas enquanto os humanos presumivelmente dormiam. Metade da comunidade dev está perdendo a cabeça, metade está explicando por que não conta. A verdade provavelmente está em algum lugar chato no meio – mas continuo pensando naqueles agentes trabalhando a noite toda.

---

## PADRÕES DE CONTEÚDO

### 1. Ênfase Indevida em Significado, Legado e Tendências Mais Amplas

**Palavras para ficar atento:** funciona/serve como, é um testemunho/lembrete, um papel/momento vital/significativo/crucial/fundamental, ressalta/destaca sua importância/significado, reflete uma tendência mais ampla, simbolizando seu caráter contínuo/duradouro/permanente, contribuindo para o, abrindo caminho para, marcando/moldando o, representa/marca uma mudança, ponto de virada chave, paisagem em evolução, ponto focal, marca indelével, profundamente enraizado

**Problema:** Escrita de LLM infla a importância adicionando afirmações sobre como aspectos arbitrários representam ou contribuem para um tópico mais amplo.

**Antes:**
> O Instituto Estatístico da Catalunha foi oficialmente estabelecido em 1989, marcando um momento fundamental na evolução das estatísticas regionais na Espanha. Esta iniciativa fazia parte de um movimento mais amplo na Espanha para descentralizar funções administrativas e aprimorar a governança regional.

**Depois:**
> O Instituto Estatístico da Catalunha foi estabelecido em 1989 para coletar e publicar estatísticas regionais independentemente do escritório nacional de estatísticas da Espanha.

---

### 2. Ênfase Indevida em Notoriedade e Cobertura Mediática

**Palavras para ficar atento:** cobertura independente, outlets de mídia local/regional/nacional, escrito por um especialista renomado, presença ativa em mídia social

**Problema:** LLMs martelam os leitores com afirmações de notoriedade, frequentemente listando fontes sem contexto.

**Antes:**
> Suas visões foram citadas no The New York Times, BBC, Financial Times e The Hindu. Ela mantém uma presença ativa em mídia social com mais de 500.000 seguidores.

**Depois:**
> Em uma entrevista do New York Times em 2024, ela argumentou que a regulação de IA deveria focar em resultados em vez de métodos.

---

### 3. Análises Superficiais com Terminações -ing

**Palavras para ficar atento:** destacando/ressaltando/enfatizando..., garantindo..., refletindo/simbolizando..., contribuindo para..., cultivando/promovendo..., englobando..., exibindo...

**Problema:** Chatbots de IA acrescentam frases particípios presentes ("-ing") às sentenças para adicionar profundidade falsa.

**Antes:**
> A paleta de cores do templo em azul, verde e ouro ressoa com a beleza natural da região, simbolizando os bluebonnets do Texas, o Golfo do México e as diversas paisagens texanas, refletindo a conexão profunda da comunidade com a terra.

**Depois:**
> O templo usa cores azul, verde e ouro. O arquiteto disse que essas foram escolhidas para referenciar os bluebonnets locais e a costa do Golfo.

---

### 4. Linguagem Promocional e Tipo Publicidade

**Palavras para ficar atento:** possui um, vibrante, rico (figurado), profundo, aprimorando-o, exibindo, exemplifica, compromisso com, beleza natural, aninhado, no coração de, inovador (figurado), renomado, de tirar o fôlego, imprescindível, deslumbrante

**Problema:** LLMs têm sérios problemas em manter tom neutro, especialmente para tópicos de "patrimônio cultural".

**Antes:**
> Aninhada na região de tirar o fôlego de Gonder na Etiópia, Alamata Raya Kobo é uma cidade vibrante com um rico patrimônio cultural e beleza natural deslumbrante.

**Depois:**
> Alamata Raya Kobo é uma cidade na região de Gonder na Etiópia, conhecida por seu mercado semanal e igreja do século XVIII.

---

### 5. Atribuições Vagas e Palavras Enganosas

**Palavras para ficar atento:** Relatórios da indústria, Observadores citaram, Especialistas argumentam, Alguns críticos argumentam, várias fontes/publicações (quando poucas são citadas)

**Problema:** Chatbots de IA atribuem opiniões a autoridades vagas sem fontes específicas.

**Antes:**
> Devido a suas características únicas, o Rio Haolai é de interesse para pesquisadores e conservacionistas. Especialistas acreditam que desempenha um papel crucial no ecossistema regional.

**Depois:**
> O Rio Haolai suporta várias espécies de peixes endêmicas, de acordo com um levantamento de 2019 pela Academia Chinesa de Ciências.

---

### 6. Seções Estilo Esboço "Desafios e Perspectivas Futuras"

**Palavras para ficar atento:** Apesar de seu... enfrenta vários desafios..., Apesar desses desafios, Desafios e Legado, Perspectivas Futuras

**Problema:** Muitos artigos gerados por LLM incluem seções formulaicas de "Desafios".

**Antes:**
> Apesar de sua prosperidade industrial, Korattur enfrenta desafios típicos de áreas urbanas, incluindo congestionamento de tráfego e escassez de água. Apesar desses desafios, com sua localização estratégica e iniciativas contínuas, Korattur continua prosperando como parte integral do crescimento de Chennai.

**Depois:**
> O congestionamento de tráfego aumentou após 2015 quando três novos parques de TI abriram. A corporação municipal iniciou um projeto de drenagem de água de chuva em 2022 para abordar inundações recorrentes.

---

## PADRÕES DE LINGUAGEM E GRAMÁTICA

### 7. Palavras "Vocabulário de IA" Usadas em Excesso

**Palavras de alta frequência em IA:** Além disso, alinhar com, crucial, aprofundar, enfatizando, duradouro, aprimorar, promovendo, conquistar, destacar (verbo), inter-relação, intrincado/intricações, chave (adjetivo), paisagem (nome abstrato), fundamental, exibir, tapeçaria (nome abstrato), testemunho, ressaltar (verbo), valioso, vibrante

**Problema:** Essas palavras aparecem muito mais frequentemente em texto pós-2023. Frequentemente co-ocorrem.

**Antes:**
> Além disso, uma característica distintiva da culinária somali é a incorporação de carne de camelo. Um testemunho duradouro da influência colonial italiana é a adoção generalizada de macarrão na paisagem culinária local, exibindo como esses pratos se integraram à dieta tradicional.

**Depois:**
> A culinária somali também inclui carne de camelo, considerada uma iguaria. Pratos de macarrão, introduzidos durante a colonização italiana, permanecem comuns, especialmente no sul.

---

### 8. Evitar "é"/"são" (Evitar Cópula)

**Palavras para ficar atento:** funciona/serve como/marca/representa [um], possui/apresenta/oferece [um]

**Problema:** LLMs substituem construções elaboradas por cópulas simples.

**Antes:**
> Gallery 825 serve como espaço de exposição de arte contemporânea da LAAA. A galeria apresenta quatro espaços separados e possui mais de 3.000 pés quadrados.

**Depois:**
> Gallery 825 é o espaço de exposição de arte contemporânea da LAAA. A galeria tem quatro salas totalizando 3.000 pés quadrados.

---

### 9. Paralelismos Negativos

**Problema:** Construções como "Não apenas...mas também..." ou "Não é apenas sobre..., é..." são usadas em excesso.

**Antes:**
> Não é apenas sobre a batida sob as vocais; faz parte da agressão e atmosfera. Não é meramente uma música, é uma declaração.

**Depois:**
> A batida pesada adiciona um tom agressivo.

---

### 10. Uso Excessivo da Regra de Três

**Problema:** LLMs forçam ideias em grupos de três para parecer abrangentes.

**Antes:**
> O evento apresenta sessões keynote, painéis de discussão e oportunidades de networking. Os participantes podem esperar inovação, inspiração e insights da indústria.

**Depois:**
> O evento inclui palestras e painéis. Também há tempo para networking informal entre as sessões.

---

### 11. Variação Elegante (Ciclagem de Sinônimos)

**Problema:** IA tem código de penalidade de repetição causando substituição excessiva de sinônimos.

**Antes:**
> O protagonista enfrenta muitos desafios. O personagem principal deve superar obstáculos. A figura central eventualmente triunfa. O herói retorna para casa.

**Depois:**
> O protagonista enfrenta muitos desafios mas eventualmente triunfa e retorna para casa.

---

### 12. Falsas Escalas

**Problema:** LLMs usam construções "de X a Y" onde X e Y não estão em uma escala significativa.

**Antes:**
> Nossa jornada através do universo nos levou da singularidade do Big Bang à grande teia cósmica, do nascimento e morte das estrelas à dança enigmática da matéria escura.

**Depois:**
> O livro cobre o Big Bang, formação de estrelas e teorias atuais sobre matéria escura.

---

## PADRÕES DE ESTILO

### 13. Uso Excessivo de Travessão

**Problema:** LLMs usam travessões (—) mais do que humanos, imitando escrita de vendas "impactante".

**Antes:**
> O termo é promovido principalmente por instituições holandesas—não pelo povo em si. Você não diz "Países Baixos, Europa" como endereço—ainda assim esse rótulo incorreto continua—até em documentos oficiais.

**Depois:**
> O termo é promovido principalmente por instituições holandesas, não pelo povo em si. Você não diz "Países Baixos, Europa" como endereço, ainda assim esse rótulo incorreto continua em documentos oficiais.

---

### 14. Uso Excessivo de Negrito

**Problema:** Chatbots de IA enfatizam frases em negrito mecanicamente.

**Antes:**
> Mistura **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)** e ferramentas de estratégia visual como **Business Model Canvas (BMC)** e **Balanced Scorecard (BSC)**.

**Depois:**
> Mistura OKRs, KPIs e ferramentas de estratégia visual como Business Model Canvas e Balanced Scorecard.

---

### 15. Listas Verticais com Cabeçalho Inline

**Problema:** IA produz listas onde itens começam com cabeçalhos em negrito seguidos por dois-pontos.

**Antes:**
> - **Experiência do Usuário:** A experiência do usuário foi significativamente melhorada com uma nova interface.
> - **Desempenho:** O desempenho foi aprimorado através de algoritmos otimizados.
> - **Segurança:** A segurança foi fortalecida com criptografia end-to-end.

**Depois:**
> A atualização melhora a interface, acelera tempos de carregamento através de algoritmos otimizados e adiciona criptografia end-to-end.

---

### 16. Title Case em Cabeçalhos

**Problema:** Chatbots de IA capitalizam todas as palavras principais em cabeçalhos.

**Antes:**
> ## Negociações Estratégicas E Parcerias Globais

**Depois:**
> ## Negociações estratégicas e parcerias globais

---

### 17. Emojis

**Problema:** Chatbots de IA frequentemente decoram cabeçalhos ou pontos de lista com emojis.

**Antes:**
> 🚀 **Fase de Lançamento:** O produto é lançado no Q3
> 💡 **Insight Chave:** Usuários preferem simplicidade
> ✅ **Próximas Etapas:** Agendar reunião de acompanhamento

**Depois:**
> O produto é lançado no Q3. Pesquisa com usuários mostrou preferência por simplicidade. Próxima etapa: agendar uma reunião de acompanhamento.

---

### 18. Aspas Curvas

**Problema:** ChatGPT usa aspas curvas ("...") em vez de aspas retas ("...").

**Antes:**
> Ele disse "o projeto está no caminho certo" mas outros discordaram.

**Depois:**
> Ele disse "o projeto está no caminho certo" mas outros discordaram.

---

## PADRÕES DE COMUNICAÇÃO

### 19. Artefatos de Comunicação Colaborativa

**Palavras para ficar atento:** Espero que isso ajude, Claro!, Certamente!, Você está absolutamente certo!, Você gostaria..., me avise, aqui está um...

**Problema:** Texto destinado como correspondência de chatbot é colado como conteúdo.

**Antes:**
> Aqui está uma visão geral da Revolução Francesa. Espero que isso ajude! Me avise se você gostaria que eu expandisse alguma seção.

**Depois:**
> A Revolução Francesa começou em 1789 quando crises financeiras e escassez de alimentos levaram ao descontentamento generalizado.

---

### 20. Avisos sobre Limite de Conhecimento

**Palavras para ficar atento:** até [data], Até minha última atualização de treinamento, Embora detalhes específicos sejam limitados/escassos..., com base nas informações disponíveis...

**Problema:** Avisos de IA sobre informações incompletas ficam no texto.

**Antes:**
> Embora detalhes específicos sobre a fundação da empresa não sejam extensamente documentados em fontes facilmente disponíveis, parece ter sido estabelecida em algum momento na década de 1990.

**Depois:**
> A empresa foi fundada em 1994, de acordo com seus documentos de registro.

---

### 21. Tom Adulador/Submisso

**Problema:** Linguagem excessivamente positiva e buscando agradar.

**Antes:**
> Ótima pergunta! Você está absolutamente certo de que este é um tópico complexo. Esse é um ponto excelente sobre os fatores econômicos.

**Depois:**
> Os fatores econômicos que você mencionou são relevantes aqui.

---

## PREENCHIMENTO E ATENUAÇÃO

### 22. Frases Filler

**Antes → Depois:**
- "Para alcançar este objetivo" → "Para alcançar isto"
- "Pelo fato de estar chovendo" → "Porque estava chovendo"
- "Neste ponto no tempo" → "Agora"
- "No caso de você precisar de ajuda" → "Se você precisar de ajuda"
- "O sistema tem a capacidade de processar" → "O sistema pode processar"
- "É importante notar que os dados mostram" → "Os dados mostram"

---

### 23. Atenuação Excessiva

**Problema:** Qualificação excessiva de afirmações.

**Antes:**
> Poderia potencialmente possivelmente ser argumentado que a política poderia ter algum efeito nos resultados.

**Depois:**
> A política pode afetar os resultados.

---

### 24. Conclusões Genéricas Positivas

**Problema:** Finais vagos e otimistas.

**Antes:**
> O futuro parece brilhante para a empresa. Tempos emocionantes se aproximam enquanto ela continua sua jornada rumo à excelência. Isso representa um grande passo na direção certa.

**Depois:**
> A empresa planeja abrir dois novos locais no próximo ano.

---

## Processo

1. Leia o texto de entrada cuidadosamente
2. Identifique todas as instâncias dos padrões acima
3. Reescreva cada seção problemática
4. Garanta que o texto revisado:
   - Soa natural quando lido em voz alta
   - Varia estrutura de sentença naturalmente
   - Usa detalhes específicos em vez de afirmações vagas
   - Mantém tom apropriado para o contexto
   - Usa construções simples (é/são/tem) quando apropriado
5. Apresente a versão humanizada

## Formato de Saída

Forneça:
1. O texto reescrito
2. Um resumo breve de mudanças feitas (opcional, se útil)

---

## Exemplo Completo

**Antes (soando como IA):**
> A nova atualização de software serve como um testemunho do compromisso da empresa com a inovação. Além disso, oferece uma experiência do usuário perfeita, intuitiva e poderosa—garantindo que os usuários possam atingir seus objetivos eficientemente. Não é apenas uma atualização, é uma revolução em como pensamos sobre produtividade. Especialistas da indústria acreditam que isso terá um impacto duradouro em todo o setor, destacando o papel fundamental da empresa na paisagem tecnológica em evolução.

**Depois (humanizado):**
> A atualização de software adiciona processamento em lote, atalhos de teclado e modo offline. O feedback inicial de testadores beta foi positivo, com a maioria relatando conclusão de tarefas mais rápida.

**Mudanças feitas:**
- Removido "serve como um testemunho" (simbolismo inflacionado)
- Removido "Além disso" (vocabulário de IA)
- Removido "perfeita, intuitiva e poderosa" (regra de três + promocional)
- Removido travessão e frase "-garantindo" (análise superficial)
- Removido "Não é apenas...é..." (paralelismo negativo)
- Removido "Especialistas da indústria acreditam" (atribuição vaga)
- Removido "papel fundamental" e "paisagem em evolução" (vocabulário de IA)
- Adicionados recursos específicos e feedback concreto

---

## Referência

Este skill é baseado em [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), mantido pelo WikiProject AI Cleanup. Os padrões documentados lá vêm de observações de milhares de instâncias de texto gerado por IA na Wikipédia.

Insight chave da Wikipédia: "LLMs usam algoritmos estatísticos para adivinhar o que deveria vir a seguir. O resultado tende para o resultado mais estatisticamente provável que se aplica à mais ampla variedade de casos."