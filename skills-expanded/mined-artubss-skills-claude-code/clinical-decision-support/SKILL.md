---
name: clinical-decision-support
description: "Gere documentos profissionais de suporte à decisão clínica (CDS) para ambientes de pesquisa farmacêutica e clínica, incluindo análises de coortes de pacientes (estratificadas por biomarcadores com desfechos) e relatórios de recomendações de tratamento (diretrizes baseadas em evidências com algoritmos de decisão). Oferece suporte a classificação de evidências GRADE, análise estatística (hazard ratios, curvas de sobrevida, gráficos em cascata), integração de biomarcadores e conformidade regulatória. Gera saída em formato LaTeX/PDF pronto para publicação, otimizado para desenvolvimento de fármacos, pesquisa clínica e síntese de evidências."
allowed-tools: [Read, Write, Edit, Bash]
---

# Documentos de Suporte à Decisão Clínica

## Descrição

Gere documentos profissionais de suporte à decisão clínica (CDS) para empresas farmacêuticas, pesquisadores clínicos e tomadores de decisão médica. Esta habilidade se especializa em documentos analíticos e baseados em evidências que informam estratégias de tratamento e desenvolvimento de fármacos:

1. **Análise de Coorte de Pacientes** - Análises de grupos estratificados por biomarcadores com comparações estatísticas de desfechos
2. **Relatórios de Recomendações de Tratamento** - Diretrizes clínicas baseadas em evidências com classificação GRADE e algoritmos de decisão

Todos os documentos são gerados como arquivos LaTeX/PDF pronto para publicação, otimizados para pesquisa farmacêutica, submissões regulatórias e desenvolvimento de diretrizes clínicas.

**Nota:** Para planos de tratamento de pacientes individuais à beira do leito, use a habilidade `treatment-plans`. Esta habilidade se concentra em análises de nível de grupo e síntese de evidências para ambientes farmacêuticos/pesquisa.

## Capacidades

### Tipos de Documento

**Análise de Coorte de Pacientes**
- Estratificação de pacientes baseada em biomarcadores (subtipos moleculares, expressão gênica, IHC)
- Classificação de subtipos moleculares (p.ex., GBM mesênquima-imuno-ativo vs proneural, subtipos de câncer de mama)
- Métricas de desfecho com análise estatística (OS, PFS, ORR, DOR, DCR)
- Comparações estatísticas entre subgrupos (hazard ratios, p-valores, IC 95%)
- Análise de sobrevida com curvas de Kaplan-Meier e testes de log-rank
- Tabelas de eficácia e gráficos em cascata
- Análises de efetividade comparativa
- Relatórios de coortes farmacêuticas (subgrupos de ensaios, evidência do mundo real)

**Relatórios de Recomendações de Tratamento**
- Diretrizes de tratamento baseadas em evidências para estados de doença específicos
- Classificação de força de recomendação (sistema GRADE: 1A, 1B, 2A, 2B, 2C)
- Avaliação da qualidade da evidência (alta, moderada, baixa, muito baixa)
- Fluxogramas de algoritmo de tratamento com diagramas TikZ
- Sequenciamento de linha de terapia baseado em biomarcadores
- Caminhos de decisão com critérios clínicos e moleculares
- Documentos de estratégia farmacêutica
- Desenvolvimento de diretrizes clínicas para sociedades médicas

### Recursos Clínicos

- **Integração de Biomarcadores**: Alterações genômicas (mutações, CNV, fusões), assinaturas de expressão gênica, marcadores IHC, pontuação PD-L1
- **Análise Estatística**: Hazard ratios, p-valores, intervalos de confiança, curvas de sobrevida, regressão de Cox, testes de log-rank
- **Classificação de Evidências**: Sistema GRADE (1A/1B/2A/2B/2C), níveis CEBM de Oxford, avaliação de qualidade de evidência
- **Terminologia Clínica**: SNOMED-CT, LOINC, nomenclatura médica apropriada, nomenclatura de ensaios
- **Conformidade Regulatória**: Desidentificação HIPAA, cabeçalhos de confidencialidade, alinhamento ICH-GCP
- **Formatação Profissional**: Margens de 0,5 polegadas, recomendações codificadas por cor, pronto para publicação, adequado para submissões regulatórias

## Casos de Uso Farmacêuticos e de Pesquisa

Esta habilidade foi especificamente projetada para aplicações farmacêuticas e de pesquisa clínica:

**Desenvolvimento de Fármacos**
- **Análises de Ensaios Fase 2/3**: Análises de eficácia e segurança estratificadas por biomarcadores
- **Análises de Subgrupos**: Gráficos de floresta mostrando efeitos de tratamento em subgrupos de pacientes
- **Desenvolvimento de Diagnóstico Companheiro**: Ligação de biomarcadores à resposta ao fármaco
- **Submissões Regulatórias**: Documentação IND/NDA com resumos de evidências

**Assuntos Médicos**
- **Materiais de Educação de KOL**: Algoritmos de tratamento baseados em evidências para líderes de opinião
- **Documentos de Estratégia Médica**: Paisagem competitiva e estratégias de posicionamento
- **Materiais de Conselho Consultivo**: Estrutura de análises de coorte e recomendações de tratamento
- **Planejamento de Publicação**: Análises pronto para manuscrito para periódicos revisados por pares

**Diretrizes Clínicas**
- **Desenvolvimento de Diretrizes**: Síntese de evidências com metodologia GRADE para sociedades de especialistas
- **Recomendações de Consenso**: Desenvolvimento de algoritmo de tratamento multi-interessado
- **Padrões de Prática**: Critérios de seleção de tratamento baseados em biomarcadores
- **Medidas de Qualidade**: Métricas de desempenho baseadas em evidências

**Evidência do Mundo Real**
- **Estudos de Coorte RWE**: Análises retrospectivas de coortes de pacientes de dados EMR
- **Efetividade Comparativa**: Comparações head-to-head de tratamentos em ambientes do mundo real
- **Pesquisa de Desfechos**: Sobrevida de longo prazo e segurança na prática clínica
- **Economia da Saúde**: Análises de custo-efetividade por subgrupo de biomarcador

## Quando Usar

Use esta habilidade quando você precisar:

- **Analisar coortes de pacientes** estratificadas por biomarcadores, subtipos moleculares ou características clínicas
- **Gerar relatórios de recomendações de tratamento** com classificação de evidências para diretrizes clínicas ou estratégias farmacêuticas
- **Comparar desfechos** entre subgrupos de pacientes com análise estatística (sobrevida, taxas de resposta, hazard ratios)
- **Produzir documentos de pesquisa farmacêutica** para desenvolvimento de fármacos, ensaios clínicos ou submissões regulatórias
- **Desenvolver diretrizes de prática clínica** com classificação de evidências GRADE e algoritmos de decisão
- **Documentar seleção de terapia guiada por biomarcador** no nível populacional (não pacientes individuais)
- **Sintetizar evidências** de múltiplos ensaios ou fontes de dados do mundo real
- **Criar algoritmos de decisão clínica** com fluxogramas para sequenciamento de tratamento

**NÃO use esta habilidade para:**
- Planos de tratamento de pacientes individuais (use a habilidade `treatment-plans`)
- Documentação de cuidados clínicos à beira do leito (use a habilidade `treatment-plans`)
- Protocolos de tratamento simples específicos para pacientes (use a habilidade `treatment-plans`)

## Aprimoramento Visual com Esquemas Científicos

**⚠️ OBRIGATÓRIO: Cada documento de suporte à decisão clínica DEVE incluir pelo menos 1-2 figuras geradas por IA usando a habilidade scientific-schematics.**

Isto não é opcional. Documentos de decisão clínica requerem algoritmos visuais claros. Antes de finalizar qualquer documento:
1. Gere no mínimo UM esquema ou diagrama (p.ex., algoritmo de decisão clínica, via de tratamento ou árvore de estratificação de biomarcador)
2. Para análises de coorte: inclua diagrama de fluxo de pacientes
3. Para recomendações de tratamento: inclua fluxograma de decisão

**Como gerar figuras:**
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade para publicação com tecnologia IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "sua descrição do diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável a daltonismo, alto contraste)
- Salvamento de saídas no diretório figures/

**Quando adicionar esquemas:**
- Fluxogramas de algoritmo de decisão clínica
- Diagramas de via de tratamento
- Árvores de estratificação de biomarcador
- Diagramas de fluxo de coorte de pacientes (estilo CONSORT)
- Visualizações de curva de sobrevida
- Diagramas de mecanismo molecular
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da habilidade scientific-schematics.

---

## Estrutura do Documento

**REQUISITO CRÍTICO: Todos os documentos de suporte à decisão clínica DEVEM começar com um resumo executivo completo na página 1 que abrange toda a primeira página antes de qualquer índice ou seção detalhada.**

### Estrutura do Resumo Executivo da Página 1

A primeira página de cada documento CDS deve conter APENAS o resumo executivo com os seguintes componentes:

**Elementos Obrigatórios (todos na página 1):**
1. **Título e Tipo do Documento**
   - Título principal (p.ex., "Análise de Coorte Estratificada por Biomarcador" ou "Recomendações de Tratamento Baseadas em Evidências")
   - Subtítulo com estado de doença e foco
   
2. **Caixa de Informações do Relatório** (usando tcolorbox colorido)
   - Tipo e propósito do documento
   - Data da análise/relatório
   - Estado de doença e população de pacientes
   - Autor/instituição (se aplicável)
   - Estrutura ou metodologia de análise
   
3. **Caixas de Descobertas Principais** (3-5 caixas coloridas usando tcolorbox)
   - **Resultados Primários** (caixa azul): Principais descobertas de eficácia/desfecho
   - **Insights de Biomarcador** (caixa verde): Principais descobertas de subtipo molecular
   - **Implicações Clínicas** (caixa amarela/laranja): Implicações de tratamento acionáveis
   - **Resumo Estatístico** (caixa cinza): Hazard ratios, p-valores, estatísticas-chave
   - **Destaques de Segurança** (caixa vermelha, se aplicável): Eventos adversos críticos ou avisos

**Requisitos Visuais:**
- Use `\thispagestyle{empty}` para remover números de página da página 1
- Todo o conteúdo deve caber na página 1 (antes de `\newpage`)
- Use ambientes tcolorbox coloridos com diferentes cores para hierarquia visual
- As caixas devem ser digitalizáveis e destacar informações mais críticas
- Use listas com marcadores, não parágrafos narrativos
- Termine a página 1 com `\newpage` antes de índice ou seções detalhadas

**Estrutura LaTeX de Exemplo para Primeira Página:**
```latex
\maketitle
\thispagestyle{empty}

% Caixa de Informações do Relatório
\begin{tcolorbox}[colback=blue!5!white, colframe=blue!75!black, title=Informações do Relatório]
\textbf{Tipo de Documento:} Análise de Coorte de Pacientes\\
\textbf{Estado de Doença:} Câncer de Mama Metastático HER2-Positivo\\
\textbf{Data da Análise:} \today\\
\textbf{População:} 60 pacientes, estratificados por biomarcador quanto ao status de HR
\end{tcolorbox}

\vspace{0.3cm}

% Descoberta Principal #1: Resultados Primários
\begin{tcolorbox}[colback=blue!5!white, colframe=blue!75!black, title=Resultados de Eficácia Primária]
\begin{itemize}
    \item ORR geral: 72\% (IC 95\%: 59-83\%)
    \item PFS mediano: 18,5 meses (IC 95\%: 14,2-22,8)
    \item OS mediano: 35,2 meses (IC 95\%: 28,1-NR)
\end{itemize}
\end{tcolorbox}

\vspace{0.3cm}

% Descoberta Principal #2: Insights de Biomarcador
\begin{tcolorbox}[colback=green!5!white, colframe=green!75!black, title=Descobertas de Estratificação de Biomarcador]
\begin{itemize}
    \item HR+/HER2+: ORR 68\%, PFS mediano 16,2 meses
    \item HR-/HER2+: ORR 78\%, PFS mediano 22,1 meses
    \item Status de HR significativamente associado a desfechos (p=0,041)
\end{itemize}
\end{tcolorbox}

\vspace{0.3cm}

% Descoberta Principal #3: Implicações Clínicas
\begin{tcolorbox}[colback=orange!5!white, colframe=orange!75!black, title=Recomendações Clínicas]
\begin{itemize}
    \item Eficácia robusta observada independentemente do status de HR (Grau 1A)
    \item Pacientes HR-/HER2+ mostraram desfechos numericamente superiores
    \item Tratamento recomendado para todos os pacientes com MBC HER2+
\end{itemize}
\end{tcolorbox}

\newpage
\tableofcontents  % Índice na página 2
\newpage  % Conteúdo detalhado começa página 3
```

### Análise de Coorte de Pacientes (Seções Detalhadas - Página 3+)
- **Características da Coorte**: Dados demográficos, características basais, critérios de seleção de pacientes
- **Estratificação de Biomarcador**: Subtipos moleculares, alterações genômicas, perfis IHC
- **Exposição ao Tratamento**: Terapias recebidas, dosagem, duração do tratamento por subgrupo
- **Análise de Desfecho**: Taxas de resposta (ORR, DCR), dados de sobrevida (OS, PFS), DOR
- **Métodos Estatísticos**: Curvas de sobrevida Kaplan-Meier, hazard ratios, testes de log-rank, regressão de Cox
- **Comparações de Subgrupos**: Eficácia estratificada por biomarcador, gráficos de floresta, significância estatística
- **Perfil de Segurança**: Eventos adversos por subgrupo, modificações de dose, descontinuações
- **Recomendações Clínicas**: Implicações de tratamento baseadas em perfis de biomarcador
- **Figuras**: Gráficos em cascata, gráficos de nadador, curvas de sobrevida, gráficos de floresta
- **Tabelas**: Tabela de dados demográficos, frequência de biomarcador, desfechos por subgrupo

### Relatórios de Recomendações de Tratamento (Seções Detalhadas - Página 3+)

**Resumo Executivo da Página 1 para Recomendações de Tratamento deve incluir:**
1. **Caixa de Informações do Relatório**: Estado de doença, versão/data da diretriz, população-alvo
2. **Caixa de Recomendações Principais** (verde): Top 3-5 recomendações classificadas por GRADE por linha de terapia
3. **Caixa de Critérios de Decisão de Biomarcador** (azul): Marcadores moleculares principais influenciando seleção de tratamento
4. **Caixa de Resumo de Evidência** (cinza): Ensaios principais apoiando recomendações (p.ex., KEYNOTE-189, FLAURA)
5. **Caixa de Monitoramento Crítico** (laranja/vermelha): Requisitos essenciais de monitoramento de segurança

**Seções Detalhadas (Página 3+):**
- **Contexto Clínico**: Estado de doença, epidemiologia, paisagem de tratamento atual
- **População-Alvo**: Características do paciente, critérios de biomarcador, estadiamento
- **Revisão de Evidência**: Síntese de literatura sistemática, resumo de diretriz, dados de ensaios
- **Opções de Tratamento**: Terapias disponíveis com mecanismo de ação
- **Classificação de Evidência**: Avaliação GRADE para cada recomendação (1A, 1B, 2A, 2B, 2C)
- **Recomendações por Linha**: Terapias de primeira, segunda e subsequentes linhas
- **Seleção Guiada por Biomarcador**: Critérios de decisão baseados em perfis moleculares
- **Algoritmos de Tratamento**: Fluxogramas TikZ mostrando caminhos de decisão
- **Protocolo de Monitoramento**: Avaliações de segurança, monitoramento de eficácia, modificações de dose
- **Populações Especiais**: Idosos, comprometimento renal/hepático, comorbidades
- **Referências**: Bibliografia completa com nomes de ensaios e citações

## Formato de Saída

**REQUISITO OBRIGATÓRIO DA PRIMEIRA PÁGINA:**
- **Página 1**: Resumo executivo de página inteira com 3-5 elementos tcolorbox coloridos
- **Página 2**: Índice (opcional)
- **Página 3+**: Seções detalhadas com métodos, resultados, figuras, tabelas

**Especificações do Documento:**
- **Primário**: LaTeX/PDF com margens de 0,5 polegadas para apresentação compacta e rica em dados
- **Comprimento**: Típico 5-15 páginas (1 página resumo executivo + 4-14 páginas conteúdo detalhado)
- **Estilo**: Pronto para publicação, qualidade farmacêutica, adequado para submissões regulatórias
- **Primeira Página**: Sempre um resumo executivo completo abrangendo toda a página 1 (veja seção Estrutura do Documento)

**Elementos Visuais:**
- **Cores**: 
  - Caixas página 1: azul=dados/informação, verde=biomarcadores/recomendações, amarelo/laranja=implicações clínicas, vermelho=avisos
  - Caixas de recomendação (verde=recomendação forte, amarelo=condicional, azul=pesquisa necessária)
  - Estratificação de biomarcador (subtipos moleculares codificados por cor)
  - Significância estatística (p-valores e hazard ratios codificados por cor)
- **Tabelas**: 
  - Dados demográficos com características basais
  - Frequência de biomarcador por subgrupo
  - Tabela de desfechos (ORR, PFS, OS, DOR por subtipo molecular)
  - Eventos adversos por coorte
  - Tabelas de resumo de evidência com classificações GRADE
- **Figuras**: 
  - Curvas de sobrevida Kaplan-Meier com p-valores de log-rank e tabelas de números em risco
  - Gráficos em cascata mostrando melhor resposta por paciente
  - Gráficos de floresta para análises de subgrupos com intervalos de confiança
  - Fluxogramas de algoritmo de decisão TikZ
  - Gráficos de nadador para cronogramas de pacientes individuais
- **Estatística**: Hazard ratios com IC 95%, p-valores, tempos medianos de sobrevida, taxas de sobrevida em marcos
- **Conformidade**: Desidentificação por Safe Harbor HIPAA, avisos de confidencialidade para dados proprietários

## Integração

Esta habilidade se integra com:
- **scientific-writing**: Gerenciamento de citações, relatório estatístico, síntese de evidências
- **clinical-reports**: Terminologia médica, conformidade HIPAA, documentação regulatória
- **scientific-schematics**: Fluxogramas TikZ para algoritmos de decisão e vias de tratamento
- **treatment-plans**: Aplicações de pacientes individuais de insights derivados de coorte (bidirecional)

## Diferenciadores-Chave da Habilidade Treatment-Plans

**Suporte à Decisão Clínica (esta habilidade):**
- **Público**: Empresas farmacêuticas, pesquisadores clínicos, comitês de diretrizes, assuntos médicos
- **Escopo**: Análises de nível populacional, síntese de evidências, desenvolvimento de diretrizes
- **Foco**: Estratificação de biomarcador, comparações estatísticas, classificação de evidências
- **Saída**: Documentos analíticos de múltiplas páginas (típico 5-15 páginas) com extensas figuras e tabelas
- **Casos de Uso**: Desenvolvimento de fármacos, submissões regulatórias, diretrizes de prática clínica, estratégia médica
- **Exemplo**: "Analize 60 pacientes com câncer de mama HER2+ por status de receptor hormonal com desfechos de sobrevida"

**Habilidade Treatment-Plans:**
- **Público**: Clínicos, pacientes, equipes de cuidados
- **Escopo**: Planejamento de cuidados de pacientes individuais
- **Foco**: Objetivos SMART, intervenções específicas do paciente, planos de monitoramento
- **Saída**: Planos de cuidados acionáveis concisos de 1-4 páginas
- **Casos de Uso**: Cuidados clínicos à beira do leito, documentação EMR, planejamento centrado no paciente
- **Exemplo**: "Crie plano de tratamento para paciente de 55 anos com diabetes tipo 2 recém-diagnosticado"

**Quando usar cada uma:**
- Use **clinical-decision-support** para: análises de coorte, estudos de estratificação de biomarcador, desenvolvimento de diretriz de tratamento, documentos de estratégia farmacêutica
- Use **treatment-plans** para: planos de cuidados de pacientes individuais, protocolos de tratamento para pacientes específicos, documentação clínica à beira do leito

## Exemplo de Uso

### Análise de Coorte de Pacientes

**Exemplo 1: Estratificação de Biomarcador em NSCLC**
```
> Analise uma coorte de 45 pacientes com NSCLC estratificados por expressão de PD-L1 (<1%, 1-49%, ≥50%) 
> recebendo pembrolizumabe. Inclua desfechos: ORR, PFS mediano, OS mediano com hazard ratios 
> comparando PD-L1 ≥50% vs <50%. Gere curvas de Kaplan-Meier e gráfico em cascata.
```

**Exemplo 2: Análise de Subtipo Molecular em GBM**
```
> Gere análise de coorte para 30 pacientes com GBM classificados em Cluster 1 (Mesênquima-Imuno-Ativo) 
> e Cluster 2 (Proneural) subtipos moleculares. Compare desfechos incluindo OS mediano, taxa de PFS de 6 meses, 
> e resposta a TMZ+bevacizumabe. Inclua tabela de perfil de biomarcador e comparação estatística.
```

**Exemplo 3: Coorte HER2 em Câncer de Mama**
```
> Analise 60 pacientes com câncer de mama metastático HER2-positivo tratados com trastuzumabe-deruxetano, 
> estratificados por exposição prévia a trastuzumabe (sim/não). Inclua ORR, DOR, PFS mediano com gráfico de floresta 
> mostrando análises de subgrupos por status de receptor hormonal, metástases cerebrais e número de linhas prévias.
```

### Relatório de Recomendações de Tratamento

**Exemplo 1: Diretrizes de Câncer de Mama Metastático HER2+**
```
> Crie recomendações de tratamento baseadas em evidências para câncer de mama metastático HER2-positivo incluindo 
> seleção de terapia guiada por biomarcador. Use sistema GRADE para classificar recomendações para primeira linha 
> (trastuzumabe+pertuzumabe+taxano), segunda linha (trastuzumabe-deruxetano) e opções de terceira linha. 
> Inclua fluxograma de algoritmo de decisão baseado em metástases cerebrais, status de receptor hormonal e terapias prévias.
```

**Exemplo 2: Algoritmo de Tratamento para NSCLC Avançado**
```
> Gere relatório de recomendação de tratamento para NSCLC avançado baseado em expressão de PD-L1, mutação EGFR, 
> rearranjo ALK e status de desempenho. Inclua recomendações classificadas por GRADE para cada subtipo molecular, 
> fluxograma TikZ para seleção de terapia direcionada por biomarcador e tabelas de evidência dos ensaios KEYNOTE-189, 
> FLAURA e CheckMate-227.
```

**Exemplo 3: Sequenciamento de Linha de Terapia para Mieloma Múltiplo**
```
> Crie algoritmo de tratamento para mieloma múltiplo recém-diagnosticado até cenário recidivado/refratário. 
> Inclua recomendações GRADE para transplantável vs não transplantável, considerações de citogenética de alto risco, 
> e sequenciamento de terapia com daratumumab, carfilzomibe e terapia CAR-T. Forneça fluxograma mostrando pontos de decisão 
> em cada linha de terapia.
```

## Recursos Principais

### Classificação de Biomarcador
- Genômica: Mutações, CNV, fusões gênicas
- Expressão: RNA-seq, pontuações IHC
- Subtipos moleculares: Classificações específicas da doença
- Acionabilidade clínica: Orientação de seleção de terapia

### Métricas de Desfecho
- Sobrevida: OS (sobrevida geral), PFS (sobrevida livre de progressão)
- Resposta: ORR (taxa de resposta objetiva), DOR (duração da resposta), DCR (taxa de controle de doença)
- Qualidade: Status de desempenho ECOG, carga de sintomas
- Segurança: Eventos adversos, modificações de dose

### Métodos Estatísticos
- Análise de sobrevida: Curvas de Kaplan-Meier, testes de log-rank
- Comparações de grupos: testes-t, qui-quadrado, Fisher exato
- Tamanhos de efeito: Hazard ratios, odds ratios com IC 95%
- Significância: p-valores, correções para testes múltiplos

### Classificação de Evidência

**Sistema GRADE**
- **1A**: Recomendação forte, evidência de alta qualidade
- **1B**: Recomendação forte, evidência de qualidade moderada
- **2A**: Recomendação fraca, evidência de alta qualidade
- **2B**: Recomendação fraca, evidência de qualidade moderada
- **2C**: Recomendação fraca, evidência de baixa qualidade

**Força de Recomendação**
- **Forte**: Benefícios claramente superam riscos
- **Condicional**: Existem trade-offs, valores do paciente importantes
- **Pesquisa**: Evidência insuficiente, ensaios clínicos necessários

## Boas Práticas

### Para Análises de Coorte

1. **Transparência na Seleção de Pacientes**: Documente claramente critérios de inclusão/exclusão, fluxo de pacientes e razões para exclusões
2. **Clareza de Biomarcador**: Especifique métodos de ensaio, plataformas (p.ex., FoundationOne, Caris), pontos de corte e