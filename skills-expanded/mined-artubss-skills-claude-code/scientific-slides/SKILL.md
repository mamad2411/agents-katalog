---
name: scientific-slides
description: "Crie apresentações e palestras para conferências de pesquisa. Use para criar slides do PowerPoint, apresentações em conferências, seminários, apresentações de pesquisa, defesa de tese ou qualquer palestra científica. Fornece estrutura de slides, modelos de design, orientação sobre timing e validação visual. Funciona com PowerPoint e LaTeX Beamer."
allowed-tools: [Read, Write, Edit, Bash]
---

# Scientific Slides

## Visão Geral

Apresentações científicas são um meio crítico para comunicar pesquisa, compartilhar descobertas e engajar com audiências acadêmicas e profissionais. Esta habilidade fornece orientação abrangente para criar apresentações científicas eficazes, desde estrutura e desenvolvimento de conteúdo até design visual e preparação para entrega.

**Foco Principal**: Apresentações orais para conferências, seminários, defesas e palestras profissionais.

**FILOSOFIA DE DESIGN CRÍTICA**: Apresentações científicas devem ser VISUALMENTE ATRATIVAS e BASEADAS EM PESQUISA. Evite a todo custo slides secos e repletos de texto. Ótimas apresentações científicas combinam:
- **Visuais atraentes**: Figuras de alta qualidade, imagens, diagramas (não apenas bullet points)
- **Contexto de pesquisa**: Citações apropriadas de pesquisa que estabeleçam credibilidade
- **Texto mínimo**: Bullet points como prompts, você fornece a explicação verbalmente
- **Design profissional**: Esquemas de cores modernos, forte hierarquia visual, espaço em branco generoso
- **Conduzido por narrativa**: Arco narrativo claro, não apenas dumps de dados

**Lembre-se**: Apresentações chatas = ciência esquecida. Torne seus slides visualmente memoráveis enquanto mantém rigor científico através de citações apropriadas.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Preparar apresentações em conferências (5-20 minutos)
- Desenvolver seminários acadêmicos (45-60 minutos)
- Criar apresentações de defesa de tese ou dissertação
- Projetar apresentações de pitch de bolsas
- Preparar apresentações de journal club
- Fazer palestras de pesquisa em instituições ou empresas
- Ensinar ou fazer apresentações tutoriais sobre tópicos científicos

## Geração de Slides com Nano Banana Pro

**Esta habilidade usa Nano Banana Pro AI para gerar slides de apresentação impressionantes automaticamente.**

Existem dois workflows dependendo do formato de saída:

### Workflow Padrão: Slides em PDF (Recomendado)

Gere cada slide como uma imagem completa usando Nano Banana Pro, depois combine em PDF. Isso produz os resultados visualmente mais impressionantes.

**Como funciona:**
1. **Planeie o deck**: Crie um plano detalhado para cada slide (título, pontos-chave, elementos visuais)
2. **Gere slides**: Chame Nano Banana Pro para cada slide para criar imagens de slide completas
3. **Combine em PDF**: Reúna imagens de slides em uma apresentação única em PDF

**Passo 1: Planeie Cada Slide**

Antes de gerar, crie um plano detalhado para sua apresentação:

```markdown
# Plano de Apresentação: Introdução ao Machine Learning

## Slide 1: Slide de Título
- Título: "Machine Learning: Da Teoria à Prática"
- Subtítulo: "Conferência de IA 2025"
- Palestrante: Dra. Jane Smith, Universidade XYZ
- Visual: Fundo abstrato moderno com rede neural

## Slide 2: Introdução
- Título: "Por Que Machine Learning Importa"
- Pontos-chave: Adoção industrial, aplicações inovadoras, potencial futuro
- Visual: Ícones mostrando diferentes aplicações de ML (saúde, finanças, robótica)

## Slide 3: Conceitos Fundamentais
- Título: "Os Três Tipos de Aprendizado"
- Conteúdo: Supervisionado, Não supervisionado, Reforço
- Visual: Diagrama de três partes mostrando cada tipo com exemplos

... (continue para todos os slides)
```

**Passo 2: Gere Cada Slide**

Use o script `generate_slide_image.py` para criar cada slide.

**CRÍTICO: Protocolo de Consistência de Formatação**

Para garantir formatação unificada em todos os slides de uma apresentação:

1. **Defina uma Meta de Formatação** no início de sua apresentação e inclua em CADA prompt:
   - Esquema de cores (ex: "fundo azul escuro, texto branco, acentos dourados")
   - Estilo tipográfico (ex: "títulos em sans-serif negrito, texto do corpo limpo")
   - Estilo visual (ex: "estética minimalista, profissional, corporativa")
   - Abordagem de layout (ex: "espaço em branco generoso, conteúdo alinhado à esquerda")

2. **Sempre anexe o slide anterior** ao gerar slides subsequentes usando `--attach`:
   - Isso permite que Nano Banana Pro veja e combine o estilo existente
   - Cria continuidade visual em todo o deck
   - Garante cores, fontes e linguagem de design consistentes

3. **Autor padrão é "K-Dense"** a menos que outro nome seja especificado

4. **Inclua citações diretamente no prompt** para slides que referenciem pesquisa:
   - Adicione citações no texto do prompt para que apareçam no slide gerado
   - Use formato: "Inclua citação: (Autor et al., Ano)" ou "Mostre referência: Autor et al., Ano"
   - Para múltiplas citações, liste todas no prompt
   - Citações devem aparecer em texto pequeno na parte inferior do slide ou perto do conteúdo relevante

5. **Anexe figuras existentes para slides de resultados** (CRÍTICO para apresentações orientadas por dados):
   - Ao criar slides sobre resultados, SEMPRE procure figuras existentes em:
     - O diretório de trabalho (ex: `figures/`, `results/`, `plots/`, `images/`)
     - Arquivos de entrada ou diretórios fornecidos pelo usuário
     - Qualquer visualização de dados, gráficos ou figuras relevantes para a apresentação
   - Use `--attach` para incluir essas figuras para que Nano Banana Pro possa incorporá-las:
     - Anexe a figura de dados real para slides de resultados
     - Anexe diagramas relevantes para slides de metodologia
     - Anexe logos ou imagens institucionais para slides de título
   - Ao anexar figuras de dados, descreva o que deseja no prompt:
     - "Crie um slide apresentando o gráfico de resultados anexado com principais descobertas destacadas"
     - "Construa um slide em torno dessa figura anexada, adicione título e bullet points explicando os dados"
     - "Incorpore o gráfico anexado em um slide de resultados com interpretação"
   - **Antes de gerar slides de resultados**: Liste arquivos no diretório de trabalho para encontrar figuras relevantes
   - Múltiplas figuras podem ser anexadas: `--attach fig1.png --attach fig2.png`

**Exemplo com consistência de formatação, citações e anexos de figura:**

```bash
# Slide de título (primeiro slide - estabelece o estilo)
python scripts/generate_slide_image.py "Slide de título para apresentação: 'Machine Learning: Da Teoria à Prática'. Subtítulo: 'Conferência de IA 2025'. Palestrante: K-Dense. META DE FORMATAÇÃO: Fundo azul escuro (#1a237e), texto branco, acentos dourados (#ffc107), design minimalista, fontes sans-serif, margens generosas, sem elementos decorativos." -o slides/01_title.png

# Slide de conteúdo com citações (anexe slide anterior para consistência)
python scripts/generate_slide_image.py "Slide de apresentação intitulado 'Por Que Machine Learning Importa'. Três pontos-chave com ícones simples: 1) Adoção industrial, 2) Aplicações inovadoras, 3) Potencial futuro. CITAÇÕES: Inclua na parte inferior em texto pequeno: (LeCun et al., 2015; Goodfellow et al., 2016). META DE FORMATAÇÃO: Combine o estilo do slide anexado - fundo azul escuro, texto branco, acentos dourados, design profissional minimalista, sem desordem visual." -o slides/02_intro.png --attach slides/01_title.png

# Slide de contexto com múltiplas citações
python scripts/generate_slide_image.py "Slide de apresentação intitulado 'Revolução do Deep Learning'. Marcos principais: Breakthrough ImageNet (2012), arquitetura transformer (2017), modelos GPT (2018-presente). CITAÇÕES: Mostre referências na parte inferior: (Krizhevsky et al., 2012; Vaswani et al., 2017; Brown et al., 2020). META DE FORMATAÇÃO: Combine o estilo do slide anexado exatamente - mesmas cores, fontes, design minimalista." -o slides/03_background.png --attach slides/02_intro.png

# SLIDE DE RESULTADOS - Anexe figura de dados real do diretório de trabalho
# Primeiro, verifique quais figuras existem: ls figures/ ou ls results/
python scripts/generate_slide_image.py "Slide de apresentação intitulado 'Resultados de Desempenho do Modelo'. Crie um slide apresentando o gráfico de acurácia anexado. Principais descobertas a destacar: 1) Acurácia de 95% alcançada, 2) Supera baseline em 12%, 3) Consistente em conjuntos de teste. CITAÇÕES: Inclua na parte inferior: (Nossos resultados, 2025). META DE FORMATAÇÃO: Combine o estilo do slide anexado exatamente." -o slides/04_results.png --attach slides/03_background.png --attach figures/accuracy_chart.png

# SLIDE DE RESULTADOS - Comparação com múltiplas figuras
python scripts/generate_slide_image.py "Slide de apresentação intitulado 'Comparação Antes vs Depois'. Construa um slide de comparação lado a lado usando as duas figuras anexadas. Esquerda: resultados baseline, Direita: nossos resultados melhorados. Adicione rótulos breves explicando a melhoria. META DE FORMATAÇÃO: Combine o estilo do slide anexado exatamente." -o slides/05_comparison.png --attach slides/04_results.png --attach figures/baseline.png --attach figures/improved.png

# SLIDE DE METODOLOGIA - Anexe diagrama existente
python scripts/generate_slide_image.py "Slide de apresentação intitulado 'Arquitetura do Sistema'. Apresente o diagrama de arquitetura anexado com bullet points explicativos breves: 1) Processamento de entrada, 2) Inferência do modelo, 3) Geração de saída. META DE FORMATAÇÃO: Combine o estilo do slide anexado exatamente." -o slides/06_architecture.png --attach slides/05_comparison.png --attach diagrams/system_architecture.png
```

**IMPORTANTE: Antes de criar slides de resultados, sempre:**
1. Liste arquivos no diretório de trabalho: `ls -la figures/` ou `ls -la results/`
2. Verifique diretórios fornecidos pelo usuário para figuras relevantes
3. Anexe TODAS as figuras relevantes que devem aparecer no slide
4. Descreva como Nano Banana Pro deve incorporar as figuras anexadas

**Modelo de Prompt:**

Inclua esses elementos em cada prompt (customize conforme necessário):
```
[Descrição do conteúdo do slide]
CITAÇÕES: Inclua na parte inferior: (Autor1 et al., Ano; Autor2 et al., Ano)
META DE FORMATAÇÃO: [Cor de fundo], [cor do texto], [cor de acento], design profissional minimalista, sem elementos decorativos, consistente com o estilo do slide anexado.
```

**Passo 3: Combine em PDF**

```bash
# Combine todos os slides em uma apresentação em PDF
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

### Workflow PPT: PowerPoint com Visuais Gerados

Ao criar apresentações em PowerPoint, use Nano Banana Pro para gerar imagens e figuras para cada slide, depois adicione texto separadamente usando a habilidade PPTX.

**Como funciona:**
1. **Planeie o deck**: Crie plano de conteúdo para cada slide
2. **Gere visuais**: Use Nano Banana Pro com flag `--visual-only` para criar imagens para slides
3. **Construa PPTX**: Use a habilidade PPTX (html2pptx ou baseada em modelo) para criar slides com visuais gerados e texto separado

**Passo 1: Gere Visuais para Cada Slide**

```bash
# Gere uma figura para o slide de introdução
python scripts/generate_slide_image.py "Ilustração profissional mostrando aplicações de machine learning: diagnóstico médico, análise financeira, veículos autônomos e robótica. Design flat moderno, ícones coloridos em fundo branco." -o figures/ml_applications.png --visual-only

# Gere um diagrama para o slide de métodos
python scripts/generate_slide_image.py "Diagrama de arquitetura de rede neural mostrando camada de entrada, três camadas ocultas e camada de saída. Estilo limpo e técnico com conexões de nó. Esquema de cores azul e cinza." -o figures/neural_network.png --visual-only

# Gere um gráfico conceitual para resultados
python scripts/generate_slide_image.py "Comparação antes e depois mostrando melhoria: lado esquerdo mostra dados desordenados, lado direito mostra insights organizados. Seta conectando-os. Estilo profissional empresarial." -o figures/results_visual.png --visual-only
```

**Passo 2: Construa PowerPoint com Habilidade PPTX**

Use o workflow html2pptx da habilidade PPTX para criar slides que incluam:
- Imagens geradas da etapa 1
- Título e texto do corpo adicionados separadamente
- Layout e formatação profissional

Consulte `document-skills/pptx/SKILL.md` para documentação completa de criação de PPTX.

---

## Referência do Script Nano Banana Pro

### generate_slide_image.py

Gere slides de apresentação ou visuais usando Nano Banana Pro AI.

```bash
# Slide completo (padrão) - gera slide completo como imagem
python scripts/generate_slide_image.py "descrição do slide" -o output.png

# Apenas visual - gera apenas a imagem/figura para incorporar em PPT
python scripts/generate_slide_image.py "descrição visual" -o output.png --visual-only

# Com imagens de referência anexadas (Nano Banana Pro verá essas)
python scripts/generate_slide_image.py "Crie um slide explicando este gráfico" -o slide.png --attach chart.png
python scripts/generate_slide_image.py "Combine essas em um slide de comparação" -o compare.png --attach before.png --attach after.png
```

**Opções:**
- `-o, --output`: Caminho do arquivo de saída (obrigatório)
- `--attach IMAGE`: Anexe arquivo(s) de imagem como contexto para geração (pode ser usado múltiplas vezes)
- `--visual-only`: Gere apenas o visual/figura, não um slide completo
- `--iterations`: Máximo de iterações de refinamento (padrão: 2)
- `--api-key`: Chave OpenRouter API (ou defina variável de ambiente OPENROUTER_API_KEY)
- `-v, --verbose`: Saída detalhada

**Anexando Imagens de Referência:**

Use `--attach` quando quiser que Nano Banana Pro veja imagens existentes como contexto:
- "Crie um slide sobre esses dados" + anexe o gráfico de dados
- "Faça um slide de título com este logo" + anexe o logo
- "Combine essas figuras em um slide" + anexe múltiplas imagens
- "Explique este diagrama em um slide" + anexe o diagrama

**Configuração de Ambiente:**
```bash
export OPENROUTER_API_KEY='sua_chave_api_aqui'
# Obtenha a chave em: https://openrouter.ai/keys
```

### slides_to_pdf.py

Combine múltiplas imagens de slides em um único PDF.

```bash
# Combine arquivos PNG
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf

# Combine arquivos específicos em ordem
python scripts/slides_to_pdf.py title.png intro.png methods.png -o talk.pdf

# Do diretório (ordenado por nome de arquivo)
python scripts/slides_to_pdf.py slides/ -o presentation.pdf
```

**Opções:**
- `-o, --output`: Caminho do PDF de saída (obrigatório)
- `--dpi`: Resolução do PDF (padrão: 150)
- `-v, --verbose`: Saída detalhada

**Dica:** Nomeie slides com números para ordenação correta: `01_title.png`, `02_intro.png`, etc.

---

## Escrita de Prompt para Geração de Slides

### Prompts de Slide Completo (Workflow PDF)

Para slides completos, inclua:
1. **Tipo de slide**: Slide de título, slide de conteúdo, slide de diagrama, etc.
2. **Título**: O texto do título do slide
3. **Conteúdo**: Pontos-chave, itens de bullet ou descrições
4. **Elementos visuais**: Que imagens, ícones ou gráficos incluir
5. **Estilo de design**: Esquema de cores, clima, estética

**Exemplos de prompts:**

```
Slide de título:
"Slide de título para uma apresentação de pesquisa médica. Título: 'Avanços em Imunoterapia do Câncer'. Subtítulo: 'Resultados de Ensaio Clínico 2024'. Tema médico profissional com hélice de DNA sutil no fundo. Esquema de cores azul marinho e branco."

Slide de conteúdo:
"Slide de apresentação intitulado 'Principais Descobertas'. Três bullet points: 1) Melhoria de 40% na taxa de resposta, 2) Efeitos colaterais reduzidos, 3) Resultados de sobrevida estendida. Inclua ícones médicos relevantes. Design limpo e profissional com cores verde e branco."

Slide de diagrama:
"Slide de apresentação mostrando a metodologia da pesquisa. Título: 'Desenho do Estudo'. Fluxograma mostrando: Triagem de Pacientes → Randomização → Grupos de Tratamento (A, B, Controle) → Acompanhamento → Análise. Diagrama de fluxo estilo CONSORT. Estilo acadêmico profissional."
```

### Prompts Apenas Visual (Workflow PPT)

Para imagens a incorporar em PowerPoint, foque apenas no elemento visual:

```
"Fluxograma mostrando pipeline de machine learning: Coleta de Dados → Pré-processamento → Treinamento do Modelo → Validação → Implantação. Estilo técnico limpo, cores azul e cinza."

"Ilustração conceitual de computação em nuvem com servidores, fluxo de dados e dispositivos conectados. Design flat moderno, adequado para apresentação empresarial."

"Diagrama científico do processo de divisão celular mostrando fases da mitose. Estilo educacional com rótulos, cores seguras para daltônicos."
```

---

## Melhoria Visual com Esquemas Científicos

Além da geração de slides, use a habilidade **scientific-schematics** para diagramas técnicos:

**Quando usar scientific-schematics em vez disso:**
- Diagramas técnicos complexos (diagramas de circuitos, estruturas químicas)
- Figuras de qualidade para publicação (limiar de qualidade mais alto)
- Diagramas que exigem revisão de precisão científica

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "sua descrição de diagrama" -o figures/output.png
```

Para orientação detalhada sobre criação de esquemas, consulte a documentação da habilidade scientific-schematics.

---

## Capacidades Principais

### 1. Estrutura e Organização de Apresentação

Construa apresentações com fluxo narrativo claro e estrutura apropriada para diferentes contextos. Para orientação detalhada, consulte `references/presentation_structure.md`.

**Arco Narrativo Universal**:
1. **Hook**: Capture atenção (30-60 segundos)
2. **Contexto**: Estabeleça importância (5-10% da palestra)
3. **Problema/Lacuna**: Identifique o que é desconhecido (5-10% da palestra)
4. **Abordagem**: Explique sua solução (15-25% da palestra)
5. **Resultados**: Apresente principais descobertas (40-50% da palestra)
6. **Implicações**: Discuta significado (15-20% da palestra)
7. **Fechamento**: Conclusão memorável (1-2 minutos)

**Estruturas Específicas por Tipo de Palestra**:
- **Palestras em conferências (15 min)**: Focadas em 1-2 descobertas principais, métodos mínimos
- **Seminários acadêmicos (45 min)**: Cobertura abrangente, métodos detalhados, múltiplos estudos
- **Defesas de tese (60 min)**: Visão geral completa da dissertação, todos os estudos cobertos
- **Pitches de bolsa (15 min)**: Ênfase em significância, viabilidade e impacto
- **Journal clubs (30 min)**: Análise crítica do trabalho publicado

### 2. Princípios de Design de Slides

Crie slides profissionais, legíveis e acessíveis que aprimorem a compreensão. Para diretrizes de design completas, consulte `references/slide_design_principles.md`.

**ANTI-PADRÃO: Evite Apresentações Secas e Repletas de Texto**

❌ **O Que Torna Apresentações Secas e Esquecíveis:**
- Paredes de texto (mais de 6 bullets por slide)
- Fontes pequenas (<24pt texto do corpo)
- Apenas texto preto em fundo branco (sem interesse visual)
- Sem imagens ou gráficos (apenas bullet points)
- Modelos genéricos sem customização
- Bullet points densos e semelhantes a parágrafos
- Contexto de pesquisa faltante (sem citações)
- Todos os slides parecem iguais (repetitivo)

✅ **O Que Torna Apresentações Atrativas e Memoráveis:**
- VISUAIS DE ALTA QUALIDADE dominam (figuras, fotos, diagramas, ícones)
- Texto grande e claro como acento (não o conteúdo principal)
- Esquemas de cores modernos e propositais (não temas padrão)
- Espaço em branco generoso (slides respiram)
- Contexto baseado em pesquisa (citações apropriadas de research-lookup)
- Variedade nos layouts de slide (não todas listas de bullet)
- Fluxo conduzido por narrativa com âncoras visuais
- Aparência profissional e polida

**Princípios de Design Principais**:

**Abordagem Visual-First** (CRÍTICA):
- Comece com visuais (figuras, imagens, diagramas), adicione texto como suporte
- Todo slide deve ter FORTE elemento visual (figura, gráfico, foto, diagrama)
- Texto explica ou complementa visuais, não os substitui
- Pense: "Como posso mostrar isso, não apenas contar?"
- Meta: 60-70% conteúdo visual, 30-40% texto

**Simplicidade com Impacto**:
- Uma ideia principal por slide
- TEXTO MÍNIMO (3-4 bullets, 4-6 palavras cada preferível)
- Espaço em branco generoso (40-50% do slide)
- Foco visual claro
- Escolhas de design ousadas e confiantes

**Tipografia para Engajamento**:
- Fontes sans-serif (Arial, Calibri, Helvetica)
- FONTES GRANDES: 24-28pt para texto do corpo (não mínimo 18pt)
- 36-44pt para títulos de slide (deixe em negrito)
- Alto contraste (mínimo 4.5:1, prefira 7:1)
- Use tamanho para hierarquia, não apenas peso

**Cor para Impacto**:
- PALETAS DE CORES MODERNAS (não azul/cinza padrão)
- Considere seu tópico: biotech? cores vibrantes. Física? escuros elegantes. Saúde? tons quentes.
- Paleta limitada (3-5 cores total)
- Combinações de alto contraste
- Segura para daltônicos (evite combinações vermelho-verde)
- Use cor propositalmente (não decoração)

**Layout para Interesse Visual**:
- Varie layouts (não todas listas de bullet)
- Use layouts de duas colunas (texto + figura)
- Figuras de tela inteira para resultados principais
- Composições assimétricas (mais interessantes que centradas)
- Regra dos terços para pontos focais
- Consistente mas não repetitivo

### 3. Visualização de Dados para Slides

Adapte figuras científicas para contexto de apresentação. Para orientação detalhada, consulte `references/data_visualization_slides.md`.

**Principais Diferenças de Figuras de Journal**:
- Simplifique, não replique
- Fontes maiores (mínimo 18-24pt)
- Menos painéis (divida entre slides)
- Rótulos diretos (não legendas)
- Ênfase através de cor e tamanho
- Divulgação progressiva para dados complexos

**Melhores Práticas de Visualização**:
- **Gráficos de barras**: Comparando categorias discretas
- **Gráficos de linha**: Tendências e trajetórias
- **Gráficos de dispersão**: Relacionamentos e correlações
- **Mapas de calor**: Dados de matriz e padrões
- **Diagramas de rede**: Relacionamentos e conexões

**Erros Comuns a Evitar**:
- Fontes minúsculas (<18pt)
- Muitos painéis em um slide
- Legendas complexas
- Contraste insuficiente
- Layouts desordenados

### 4. Orientação Específica por Tipo de Palestra

Diferentes contextos de apresentação exigem abordagens diferentes. Para orientação abrangente sobre cada tipo, consulte `references/talk_types_guide.md`.

**Palestras em Conferências** (10-20 minutos):
- Estrutura: Breve introdução → métodos mínimos → principais resultados → conclusão rápida
- Foco: 1-2 descobertas principais apenas
- Estilo: Atrativo, rápido, memorável
- Meta: Gerar interesse, networking, ser convidado

**Seminários Acadêmicos** (45-60 minutos):
- Estrutura: Cobertura abrangente com métodos detalhados
- Foco: Múltiplas descobertas, profundidade de análise
- Estilo: Acadêmico, interativo, orientado para discussão
- Meta: Demonstrar expertise, obter feedback, colaborar

**Defesas de Tese** (45-60 minutos):
- Estrutura: Visão geral completa da dissertação, todos os estudos
- Foco: Demonstrando maestria e pensamento independente
- Estilo: Formal, abrangente, preparado para interrogação
- Meta: Passar no exame, defender decisões de pesquisa

**Pitches de Bolsa** (10-20 minutos):
- Estrutura: Problema → significância → abordagem → viabilidade → impacto
- Foco: Inovação, dados preliminares, qualificações da equipe
- Estilo: Persuasivo, focado em resultados e impacto
- Meta: Garantir financiamento, demonstrar viabilidade

**Journal Clubs** (20-45 minutos):
- Estrutura: Contexto → métodos → resultados → análise crítica
- Foco: Compreensão e crítica de trabalho publicado
- Estilo: Educacional, crítico, facilitador de discussão
- Meta: Aprender, criticar, discutir implicações

### 5. Opções de Implementação

#### Nano Banana Pro PDF (Padrão - Recomendado)

**Melhor para**: Slides visualmente impressionantes, criação rápida, audiências não-técnicas

**Esta é a abordagem padrão e recomendada.** Gere cada slide como uma imagem completa usando IA.

**Workflow**:
1. Planeie cada slide (título, conteúdo, elementos visuais)
2. Gere cada slide com `generate_slide_image.py`
3. Combine em PDF com `slides_to_pdf.py`

```bash
# Gere slides
python scripts/generate_slide_image.py "Título: Introdução..." -o slides/01.png
python scripts/generate_slide_image.py "Título: Métodos..." -o slides/02.png

# Combine em PDF
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

**Vantagens**:
- Resultados mais visualmente impressionantes
- Criação rápida (descreva e gere)
- Sem exigência de habilidades de design
- Aparência consistente e profissional
- Perfeito para audiências gerais

**