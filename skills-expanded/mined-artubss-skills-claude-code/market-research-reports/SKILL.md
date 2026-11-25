---
name: market-research-reports
description: "Gerar relatórios abrangentes de pesquisa de mercado (50+ páginas) no estilo das principais consultorias (McKinsey, BCG, Gartner). Apresenta formatação profissional em LaTeX, geração visual extensiva com scientific-schematics e generate-image, integração profunda com research-lookup para coleta de dados, e análise estratégica multi-framework incluindo Cinco Forças de Porter, PESTLE, SWOT, TAM/SAM/SOM e Matriz BCG."
allowed-tools: [Read, Write, Edit, Bash]
---

# Relatórios de Pesquisa de Mercado

## Visão Geral

Relatórios de pesquisa de mercado são documentos estratégicos abrangentes que analisam indústrias, mercados e paisagens competitivas para informar decisões de negócios, estratégias de investimento e planejamento estratégico. Esta habilidade gera **relatórios de qualidade profissional com 50+ páginas** com conteúdo visual extenso, modelado a partir de entregas de principais consultorias como McKinsey, BCG, Bain, Gartner e Forrester.

**Características principais:**
- **Comprimento abrangente**: Relatórios são projetados para ter 50+ páginas sem restrições de tokens
- **Conteúdo visual-rico**: 5-6 diagramas-chave gerados no início (mais adicionados conforme necessário durante a redação)
- **Análise orientada por dados**: Integração profunda com research-lookup para dados de mercado
- **Abordagem multi-framework**: Cinco Forças de Porter, PESTLE, SWOT, Matriz BCG, TAM/SAM/SOM
- **Formatação profissional**: Tipografia, cores e layout de qualidade de consultoria
- **Recomendações acionáveis**: Foco estratégico com roteiros de implementação

**Formato de saída:** LaTeX com estilo profissional, compilado para PDF. Usa o pacote de estilo `market_research.sty` para formatação consistente e profissional.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Criando análise abrangente de mercado para decisões de investimento
- Desenvolvendo relatórios de indústria para planejamento estratégico
- Analisando paisagens competitivas e dinâmicas de mercado
- Conduzindo exercícios de dimensionamento de mercado (TAM/SAM/SOM)
- Avaliando oportunidades de entrada em mercado
- Preparando materiais de due diligence para atividades de M&A
- Criando conteúdo de thought leadership para posicionamento da indústria
- Desenvolvendo documentação de estratégia go-to-market
- Analisando impactos regulatórios e políticos em mercados
- Construindo business cases para lançamento de novos produtos

## Requisitos de Aprimoramento Visual

**CRÍTICO: Relatórios de pesquisa de mercado devem incluir conteúdo visual-chave.**

Todo relatório deve gerar **6 visualizações essenciais** no início, com visualizações adicionais adicionadas conforme necessário durante a redação. Comece com as visualizações mais críticas para estabelecer o framework do relatório.

### Ferramentas de Geração Visual

**Use `scientific-schematics` para:**
- Gráficos de trajetória de crescimento de mercado
- Diagramas de breakdown TAM/SAM/SOM (círculos concêntricos)
- Diagramas de Cinco Forças de Porter
- Matrizes de posicionamento competitivo
- Gráficos de segmentação de mercado
- Diagramas de cadeia de valor
- Roadmaps de tecnologia
- Heatmaps de risco
- Matrizes de priorização estratégica
- Timelines de implementação/Gráficos de Gantt
- Diagramas de análise SWOT
- Matrizes de Crescimento-Participação BCG

```bash
# Exemplo: Gerar diagrama TAM/SAM/SOM
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Diagrama de círculos concêntricos TAM SAM SOM mostrando Mercado Total Endereçável $50B no círculo externo, Mercado Endereçável Atendível $15B no círculo do meio, Mercado Atendível Obtível $3B no círculo interno, com rótulos e setas apontando para cada segmento" \
  -o figures/tam_sam_som.png --doc-type report

# Exemplo: Gerar Cinco Forças de Porter
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Diagrama de Cinco Forças de Porter com caixa central 'Rivalidade Competitiva' conectada a quatro caixas ao redor: 'Ameaça de Novos Entrantes' (acima), 'Poder de Negociação de Fornecedores' (esquerda), 'Poder de Negociação de Compradores' (direita), 'Ameaça de Substitutos' (abaixo). Cada caixa deve mostrar avaliação Alto/Médio/Baixo" \
  -o figures/porters_five_forces.png --doc-type report
```

**Use `generate-image` para:**
- Infográficos hero de resumo executivo
- Ilustrações conceituais de indústria/setor
- Visualizações de tecnologia abstrata
- Imagens de página de capa

```bash
# Exemplo: Gerar infográfico de resumo executivo
python skills/generate-image/scripts/generate_image.py \
  "Infográfico profissional de resumo executivo para relatório de pesquisa de mercado, mostrando métricas-chave em estilo moderno de visualização de dados, esquema de cores azul e verde, design minimalista limpo com ícones representando tamanho de mercado, taxa de crescimento e paisagem competitiva" \
  --output figures/executive_summary.png
```

### Visualizações Recomendadas por Seção (Gerar Conforme Necessário)

| Seção | Visualizações Prioritárias | Visualizações Opcionais |
|-------|---------------------------|----------------------|
| Resumo Executivo | Infográfico executivo (INÍCIO) | - |
| Tamanho e Crescimento de Mercado | Trajetória de crescimento (INÍCIO), TAM/SAM/SOM (INÍCIO) | Breakdown regional, crescimento de segmento |
| Paisagem Competitiva | Cinco Forças de Porter (INÍCIO), Matriz de posicionamento (INÍCIO) | Gráfico de participação de mercado, grupos estratégicos |
| Análise de Risco | Heatmap de risco (INÍCIO) | Matriz de mitigação |
| Recomendações Estratégicas | Matriz de oportunidades | Framework de priorização |
| Roteiro de Implementação | Timeline/Gantt | Rastreador de marcos |
| Tese de Investimento | Projeções financeiras | Análise de cenários |

**Comece com 6 visualizações prioritárias** (marcadas como INÍCIO acima), depois gere visualizações adicionais conforme as seções específicas forem escritas e exigirem suporte visual.

---

## Estrutura do Relatório (50+ Páginas)

### Preliminares (~5 páginas)

#### Página de Capa (1 página)
- Título e subtítulo do relatório
- Visualização hero
- Data e classificação
- Preparado para / Preparado por

#### Sumário (1-2 páginas)
- Automático do LaTeX
- Lista de Figuras
- Lista de Tabelas

#### Resumo Executivo (2-3 páginas)
- **Caixa de Snapshot de Mercado**: Métricas-chave num relance
- **Tese de Investimento**: Resumo em 3-5 bullet points
- **Principais Descobertas**: Descobertas e insights principais
- **Recomendações Estratégicas**: Top 3-5 recomendações acionáveis
- **Infográfico de Resumo Executivo**: Síntese visual dos principais pontos do relatório

---

### Análise Principal (~35 páginas)

#### Capítulo 1: Visão Geral e Definição de Mercado (4-5 páginas)

**Requisitos de Conteúdo:**
- Definição e escopo de mercado
- Mapeamento de ecossistema de indústria
- Principais stakeholders e seus papéis
- Limites de mercado e adjacências
- Contexto histórico e evolução

**Visualizações Necessárias (2):**
1. Diagrama de ecossistema/cadeia de valor de mercado
2. Diagrama de estrutura de indústria

**Pontos-chave de Dados:**
- Critérios de definição de mercado
- Segmentos incluídos/excluídos
- Escopo geográfico
- Horizonte de tempo para análise

---

#### Capítulo 2: Análise de Tamanho e Crescimento de Mercado (6-8 páginas)

**Requisitos de Conteúdo:**
- Cálculo de Mercado Total Endereçável (TAM)
- Definição de Mercado Endereçável Atendível (SAM)
- Estimativa de Mercado Atendível Obtível (SOM)
- Análise de crescimento histórico (5-10 anos)
- Projeções de crescimento (5-10 anos à frente)
- Drivers de crescimento e inibidores
- Breakdown de mercado regional
- Análise no nível de segmento

**Visualizações Necessárias (4):**
1. Gráfico de trajetória de crescimento de mercado (histórico + projetado)
2. Diagrama de círculos concêntricos TAM/SAM/SOM
3. Breakdown de mercado regional (gráfico de pizza ou treemap)
4. Comparação de crescimento de segmento (gráfico de barras)

**Pontos-chave de Dados:**
- Tamanho atual de mercado (com fonte)
- CAGR (histórico e projetado)
- Tamanho de mercado por região
- Tamanho de mercado por segmento
- Suposições-chave para projeções

**Fontes de Dados:**
Use `research-lookup` para encontrar:
- Relatórios de pesquisa de mercado (Gartner, Forrester, IDC, etc.)
- Dados de associações de indústria
- Estatísticas governamentais
- Relatórios financeiros de empresas
- Estudos acadêmicos

---

#### Capítulo 3: Drivers de Indústria e Tendências (5-6 páginas)

**Requisitos de Conteúdo:**
- Fatores macroeconômicos
- Tendências de tecnologia
- Drivers regulatórios
- Mudanças sociais e demográficas
- Fatores ambientais
- Tendências específicas de indústria

**Frameworks de Análise:**
- **Análise PESTLE**: Político, Econômico, Social, Tecnológico, Legal, Ambiental
- **Avaliação de Impacto de Tendência**: Matriz de probabilidade vs impacto

**Visualizações Necessárias (3):**
1. Timeline de tendências de indústria ou gráfico de radar
2. Matriz de impacto de drivers
3. Diagrama de análise PESTLE

**Pontos-chave de Dados:**
- Top 5-10 drivers de crescimento com impacto quantificado
- Tendências emergentes com timeline
- Fatores de disrupção

---

#### Capítulo 4: Paisagem Competitiva (6-8 páginas)

**Requisitos de Conteúdo:**
- Análise de estrutura de mercado
- Perfis dos principais players
- Análise de participação de mercado
- Posicionamento competitivo
- Barreiras à entrada
- Dinâmicas competitivas

**Frameworks de Análise:**
- **Cinco Forças de Porter**: Análise abrangente de indústria
- **Matriz de Posicionamento Competitivo**: Matriz 2x2 em dimensões-chave
- **Mapeamento de Grupos Estratégicos**: Agrupar competidores por estratégia

**Visualizações Necessárias (4):**
1. Diagrama de Cinco Forças de Porter
2. Gráfico de participação de mercado (pizza ou barras)
3. Matriz de posicionamento competitivo (2x2)
4. Mapa de grupos estratégicos

**Pontos-chave de Dados:**
- Participação de mercado por empresa (top 10)
- Avaliação de intensidade competitiva
- Avaliação de barreiras à entrada
- Avaliação de poder de fornecedor/comprador

---

#### Capítulo 5: Análise de Cliente e Segmentação (4-5 páginas)

**Requisitos de Conteúdo:**
- Definições de segmento de cliente
- Tamanho de segmento e crescimento
- Análise de comportamento de compra
- Necessidades e pontos de dor do cliente
- Processo de tomada de decisão
- Drivers de valor por segmento

**Frameworks de Análise:**
- **Matriz de Segmentação de Cliente**: Tamanho vs Crescimento
- **Canvas de Proposta de Valor**: Jobs, Pains, Gains
- **Mapeamento de Jornada do Cliente**: Awareness a Advocacy

**Visualizações Necessárias (3):**
1. Breakdown de segmentação de cliente (pizza/treemap)
2. Matriz de atratividade de segmento
3. Diagrama de jornada do cliente ou proposta de valor

**Pontos-chave de Dados:**
- Tamanhos de segmento e percentuais
- Taxas de crescimento por segmento
- Tamanho de deal médio / receita por cliente
- Custo de aquisição de cliente por segmento

---

#### Capítulo 6: Paisagem de Tecnologia e Inovação (4-5 páginas)

**Requisitos de Conteúdo:**
- Stack de tecnologia atual
- Tecnologias emergentes
- Tendências de inovação
- Curvas de adoção de tecnologia
- Análise de investimento em P&D
- Paisagem de patentes

**Frameworks de Análise:**
- **Avaliação de Prontidão de Tecnologia**: Níveis TRL
- **Posicionamento de Hype Cycle**: Onde as tecnologias se situam
- **Roadmap de Tecnologia**: Evolução ao longo do tempo

**Visualizações Necessárias (2):**
1. Diagrama de roadmap de tecnologia
2. Diagrama de curva de inovação/adoção ou hype cycle

**Pontos-chave de Dados:**
- Gastos em P&D na indústria
- Principais marcos tecnológicos
- Tendências de depósito de patentes
- Taxas de adoção de tecnologia

---

#### Capítulo 7: Ambiente Regulatório e Política (3-4 páginas)

**Requisitos de Conteúdo:**
- Framework regulatório atual
- Órgãos reguladores-chave
- Requisitos de conformidade
- Mudanças regulatórias futuras
- Tendências de política
- Avaliação de impacto

**Visualizações Necessárias (1):**
1. Timeline regulatória ou diagrama de framework regulatório

**Pontos-chave de Dados:**
- Regulações-chave e datas efetivas
- Custos de conformidade
- Riscos regulatórios
- Probabilidade de mudança de política

---

#### Capítulo 8: Análise de Risco (3-4 páginas)

**Requisitos de Conteúdo:**
- Riscos de mercado
- Riscos competitivos
- Riscos regulatórios
- Riscos de tecnologia
- Riscos operacionais
- Riscos financeiros
- Estratégias de mitigação de risco

**Frameworks de Análise:**
- **Heatmap de Risco**: Probabilidade vs Impacto
- **Registro de Risco**: Inventário abrangente de riscos
- **Matriz de Mitigação**: Risco vs estratégia de mitigação

**Visualizações Necessárias (2):**
1. Heatmap de risco (probabilidade vs impacto)
2. Matriz de mitigação de risco

**Pontos-chave de Dados:**
- Top 10 riscos com avaliações
- Pontuações de probabilidade de risco
- Pontuações de severidade de impacto
- Estimativas de custo de mitigação

---

### Recomendações Estratégicas (~10 páginas)

#### Capítulo 9: Oportunidades Estratégicas e Recomendações (4-5 páginas)

**Requisitos de Conteúdo:**
- Identificação de oportunidades
- Dimensionamento de oportunidades
- Análise de opções estratégicas
- Framework de priorização
- Recomendações detalhadas
- Fatores de sucesso

**Frameworks de Análise:**
- **Matriz de Atratividade de Oportunidade**: Atratividade vs Capacidade de Vencer
- **Framework de Opções Estratégicas**: Build, Buy, Partner, Ignore
- **Matriz de Prioridade**: Impacto vs Esforço

**Visualizações Necessárias (3):**
1. Matriz de oportunidades
2. Framework de opções estratégicas
3. Matriz de prioridade/recomendação

**Pontos-chave de Dados:**
- Tamanhos de oportunidade
- Requisitos de investimento
- Retornos esperados
- Timeline para valor

---

#### Capítulo 10: Roteiro de Implementação (3-4 páginas)

**Requisitos de Conteúdo:**
- Plano de implementação em fases
- Marcos e entregas-chave
- Requisitos de recursos
- Timeline e sequenciamento
- Dependências e caminho crítico
- Estrutura de governança

**Visualizações Necessárias (2):**
1. Timeline de implementação/Gráfico de Gantt
2. Rastreador de marcos ou diagrama de fase

**Pontos-chave de Dados:**
- Durações de fase
- Requisitos de recursos
- Marcos-chave com datas
- Alocação de orçamento por fase

---

#### Capítulo 11: Tese de Investimento e Projeções Financeiras (3-4 páginas)

**Requisitos de Conteúdo:**
- Resumo de investimento
- Projeções financeiras
- Análise de cenários
- Expectativas de retorno
- Suposições-chave
- Análise de sensibilidade

**Visualizações Necessárias (2):**
1. Gráfico de projeção financeira (receita, crescimento)
2. Comparação de análise de cenários

**Pontos-chave de Dados:**
- Projeções de receita (3-5 anos)
- Projeções de CAGR
- Expectativas de ROI/IRR
- Suposições financeiras-chave

---

### Matérias de Suporte (~5 páginas)

#### Apêndice A: Metodologia e Fontes de Dados (1-2 páginas)
- Metodologia de pesquisa
- Abordagem de coleta de dados
- Fontes de dados e citações
- Limitações e suposições

#### Apêndice B: Tabelas Detalhadas de Dados de Mercado (2-3 páginas)
- Tabelas abrangentes de dados de mercado
- Breakdowns regionais
- Detalhes de segmento
- Séries de dados históricos

#### Apêndice C: Perfis de Empresas (1-2 páginas)
- Perfis breves dos principais competidores
- Principais dados financeiros
- Áreas de foco estratégico

#### Referências/Bibliografia
- Todas as fontes citadas
- Formato BibTeX para LaTeX

---

## Workflow

### Fase 1: Pesquisa e Coleta de Dados

**Passo 1: Definir Escopo**
- Esclarecer definição de mercado
- Estabelecer limites geográficos
- Determinar horizonte de tempo
- Identificar questões-chave a responder

**Passo 2: Conduzir Pesquisa Profunda**

Use `research-lookup` extensivamente para reunir dados de mercado:

```bash
# Dados de tamanho e crescimento de mercado
python skills/research-lookup/scripts/research_lookup.py \
  "Qual é o tamanho atual de mercado e a taxa de crescimento projetada para a indústria [MERCADO]? Incluir estimativas de TAM, SAM, SOM e projeções de CAGR"

# Paisagem competitiva
python skills/research-lookup/scripts/research_lookup.py \
  "Quem são os 10 principais competidores no mercado [MERCADO]? Qual é sua participação de mercado e posicionamento competitivo?"

# Tendências de indústria
python skills/research-lookup/scripts/research_lookup.py \
  "Quais são as principais tendências e drivers de crescimento na indústria [MERCADO] para 2024-2030?"

# Ambiente regulatório
python skills/research-lookup/scripts/research_lookup.py \
  "Quais são as principais regulações e mudanças de política que afetam a indústria [MERCADO]?"
```

**Passo 3: Organização de Dados**
- Criar pasta `sources/` com notas de pesquisa
- Organizar dados por seção
- Identificar lacunas de dados
- Conduzir pesquisa de follow-up conforme necessário

### Fase 2: Análise e Aplicação de Framework

**Passo 4: Aplicar Frameworks de Análise**

Para cada framework, conduzir análise estruturada:

- **Dimensionamento de Mercado**: TAM → SAM → SOM com suposições claras
- **Cinco Forças de Porter**: Classificar cada força Alto/Médio/Baixo com fundamentação
- **PESTLE**: Analisar cada dimensão com tendências e impactos
- **SWOT**: Forças/fraquezas internas, oportunidades/ameaças externas
- **Posicionamento Competitivo**: Definir eixos, plotar competidores

**Passo 5: Desenvolver Insights**
- Sintetizar descobertas em insights-chave
- Identificar implicações estratégicas
- Desenvolver recomendações
- Priorizar oportunidades

### Fase 3: Geração Visual

**Passo 6: Gerar Todas as Visualizações**

Gerar visualizações ANTES de escrever o relatório. Use o script de geração em batch:

```bash
# Gerar todas as visualizações padrão de relatório de mercado
python skills/market-research-reports/scripts/generate_market_visuals.py \
  --topic "[NOME DO MERCADO]" \
  --output-dir figures/
```

Ou gerar individualmente:

```bash
# 1. Trajetória de crescimento de mercado
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Gráfico de barras mostrando crescimento de mercado de 2020 a 2034, com barras históricas em azul escuro (2020-2024) e barras projetadas em azul claro (2025-2034). Eixo Y mostra tamanho de mercado em bilhões USD. Incluir anotação de CAGR" \
  -o figures/01_market_growth.png --doc-type report

# 2. Breakdown TAM/SAM/SOM
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Diagrama de círculos concêntricos TAM SAM SOM. Círculo externo TAM Mercado Total Endereçável, círculo do meio SAM Mercado Endereçável Atendível, círculo interno SOM Mercado Atendível Obtível. Cada um rotulado com sigla e descrição. Gradiente azul" \
  -o figures/02_tam_sam_som.png --doc-type report

# 3. Cinco Forças de Porter
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Diagrama de Cinco Forças de Porter com caixa central 'Rivalidade Competitiva' conectada a quatro caixas ao redor: Ameaça de Novos Entrantes (acima), Poder de Negociação de Fornecedores (esquerda), Poder de Negociação de Compradores (direita), Ameaça de Substitutos (abaixo). Codificar cores por avaliação: Alto=vermelho, Médio=amarelo, Baixo=verde" \
  -o figures/03_porters_five_forces.png --doc-type report

# 4. Matriz de posicionamento competitivo
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Matriz 2x2 de posicionamento competitivo com Eixo X 'Foco de Mercado (Nicho para Amplo)' e Eixo Y 'Abordagem de Solução (Produto para Plataforma)'. Plotar 8-10 competidores como círculos rotulados de tamanhos variados. Incluir rótulos de quadrante" \
  -o figures/04_competitive_positioning.png --doc-type report

# 5. Heatmap de risco
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Matriz de heatmap de risco. Eixo X Impacto (Baixo para Crítico), Eixo Y Probabilidade (Improvável para Muito Provável). Gradiente de cores: Verde (risco baixo) para Vermelho (risco crítico). Plotar 10-12 riscos como pontos rotulados" \
  -o figures/05_risk_heatmap.png --doc-type report

# 6. (Opcional) Infográfico de resumo executivo
python skills/generate-image/scripts/generate_image.py \
  "Infográfico profissional de resumo executivo para relatório de pesquisa de mercado, estilo moderno de visualização de dados, esquema de cores azul e verde, design minimalista limpo" \
  --output figures/06_exec_summary.png
```

### Fase 4: Redação do Relatório

**Passo 7: Inicializar Estrutura de Projeto**

Criar a estrutura de projeto padrão:

```
writing_outputs/YYYYMMDD_HHMMSS_market_report_[topic]/
├── progress.md
├── drafts/
│   └── v1_market_report.tex
├── references/
│   └── references.bib
├── figures/
│   └── [todas as visualizações geradas]
├── sources/
│   └── [notas de pesquisa]
└── final/
```

**Passo 8: Escrever Relatório Usando Template**

Usar `market_report_template.tex` como ponto de partida. Escrever cada seção seguindo o guia de estrutura, garantindo:

- **Cobertura abrangente**: Cada subseção endereçada
- **Conteúdo orientado por dados**: Afirmações apoiadas por pesquisa
- **Integração visual**: Referenciar todas as figuras geradas
- **Tom profissional**: Redação no estilo consultoria
- **Sem restrições de token**: Escrever completamente, sem abreviar

**Diretrizes de Redação:**
- Usar voz ativa sempre que possível
- Começar com insights, apoiar com dados
- Usar listas numeradas para recomendações
- Incluir fontes de dados para todas as estatísticas
- Criar transições suaves entre seções

### Fase 5: Compilação e Revisão

**Passo 9: Compilar LaTeX**

```bash
cd writing_outputs/[project_folder]/drafts/
xelatex v1_market_report.tex
bibtex v1_market_report
xelatex v1_market_report.tex
xelatex v1_market_report.tex
```

**Passo 10: Revisão de Qualidade**

Verificar se o relatório atende aos padrões de qualidade:

- [ ] Contagem total de páginas é 50+ páginas
- [ ] Todas as visualizações essenciais (5-6 core + quaisquer adicionais) estão incluídas e renderizam corretamente
- [ ] Resumo executivo captura as principais descobertas
- [ ] Todos os pontos de dados têm fontes citadas
- [ ] Frameworks de análise são aplicados propriamente
- [ ] Recomendações são acionáveis e priorizadas
- [ ] Nenhuma figura ou tabela órfã
- [ ] Sumário, lista de figuras, lista de tabelas estão precisos
- [ ] Bibliografia está completa
- [ ] PDF renderiza sem erros

**Passo 11: Revisão por Pares**

Usar a habilidade de revisão por pares para avaliar o relatório:
- Avaliar abrangência
- Verificar precisão de dados
- Verificar fluxo lógico
- Avaliar qualidade de recomendação

---

## Padrões de Qualidade

### Alvos de Contagem de Páginas

| Seção | Páginas Mínimas | Páginas Alvo |
|-------|-----------------|-------------|
| Preliminares | 4 | 5 |
| Visão Geral de Mercado | 4 | 5 |
| Tamanho e Crescimento de Mercado | 5 | 7 |
| Drivers de Indústria | 4 | 6 |
| Paisagem Competitiva | 5 | 7 |
| Análise de Cliente | 3 | 5 