---
name: research-grants
description: "Escreva propostas de pesquisa competitivas para NSF, NIH, DOE e DARPA. Formatação específica de agências, critérios de revisão, preparação orçamentária, impactos amplos, declarações de significância, narrativas de inovação e conformidade com requisitos de submissão."
allowed-tools: [Read, Write, Edit, Bash]
---

# Redação de Propostas de Pesquisa

## Visão Geral

A redação de propostas de pesquisa é o processo de desenvolvimento de propostas competitivas de financiamento para agências federais e fundações. Domine requisitos específicos de agências, critérios de revisão, estrutura narrativa, preparação orçamentária e conformidade para submissões do NSF (National Science Foundation), NIH (National Institutes of Health), DOE (Department of Energy) e DARPA (Defense Advanced Research Projects Agency).

**Princípio Crítico: Propostas são documentos persuasivos que devem demonstrar simultaneamente rigor científico, inovação, viabilidade e impacto amplo.** Cada agência possui prioridades distintas, critérios de revisão, requisitos de formatação e objetivos estratégicos que devem ser abordados.

## Quando Usar Esta Competência

Esta competência deve ser usada quando:
- Escrever propostas de pesquisa para programas do NSF, NIH, DOE ou DARPA
- Preparar descrições de projeto, objetivos específicos ou narrativas técnicas
- Desenvolver declarações de impactos amplos ou significância
- Criar cronogramas de pesquisa e planos de marco
- Preparar justificativas orçamentárias e planos de alocação de pessoal
- Responder a solicitações de programa ou anúncios de financiamento
- Abordar comentários de revisores em resubmissões
- Planejar propostas colaborativas multi-institucionais
- Escrever seções de dados preliminares ou viabilidade
- Preparar biosketches, CVs ou descrições de instalações

## Aprimoramento Visual com Esquemas Científicos

**⚠️ OBRIGATÓRIO: Toda proposta de pesquisa DEVE incluir no mínimo 1-2 figuras geradas por IA usando a competência scientific-schematics.**

Isto não é opcional. Propostas de pesquisa sem elementos visuais estão incompletas e são menos competitivas. Antes de finalizar qualquer documento:
1. Gere no mínimo UM esquema ou diagrama (ex: cronograma de projeto, fluxograma de metodologia ou estrutura conceitual)
2. Prefira 2-3 figuras para propostas abrangentes (fluxo de trabalho de pesquisa, gráfico de Gantt, visualização de dados preliminares)

**Como gerar figuras:**
- Use a competência **scientific-schematics** para gerar diagramas com qualidade de publicação com suporte de IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- O Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "descrição do seu diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens com qualidade de publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltônicos, alto contraste)
- Salvamento de outputs no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de metodologia de pesquisa e fluxo de trabalho
- Gráficos de cronograma de Gantt
- Ilustrações de estrutura conceitual
- Diagramas de arquitetura de sistema (para propostas técnicas)
- Fluxogramas de design experimental
- Diagramas de atividades de impactos amplos
- Diagramas de redes de colaboração
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da competência scientific-schematics.

---

## Visão Geral Específica de Agências

### NSF (National Science Foundation)
**Missão**: Promover o progresso da ciência e avançar a saúde, prosperidade e bem-estar nacional

**Características Principais**:
- Mérito Intelectual + Impactos Amplos (ponderação igual)
- Limite de 15 páginas para descrição de projeto (maioria dos programas)
- Ênfase em educação, diversidade e benefício social
- Pesquisa colaborativa encorajada
- Ênfase em dados abertos e ciência aberta
- Processo de revisão de mérito com painel + revisores ad hoc

### NIH (National Institutes of Health)
**Missão**: Potencializar a saúde, prolongar a vida e reduzir doenças e incapacidades

**Características Principais**:
- Objetivos Específicos (1 página) + Estratégia de Pesquisa (12 páginas para R01)
- Significância, Inovação, Abordagem como critérios de revisão centrais
- Dados preliminares tipicamente necessários para R01s
- Ênfase em rigor, reprodutibilidade e relevância clínica
- Orçamentos modulares (incrementos de $250K) para maioria dos R01s
- Múltiplas oportunidades de resubmissão

### DOE (Department of Energy)
**Missão**: Assegurar a segurança e prosperidade dos EUA através de desafios energéticos, ambientais e nucleares

**Características Principais**:
- Foco em energia, clima, ciência computacional, ciências básicas de energia
- Frequentemente requer compartilhamento de custos ou parcerias industriais
- Ênfase em colaboração com laboratórios nacionais
- Forte integração computacional e experimental
- Inovação energética e caminhos de comercialização
- Varia por escritório (ARPA-E, Office of Science, EERE, etc.)

### DARPA (Defense Advanced Research Projects Agency)
**Missão**: Fazer investimentos estratégicos em tecnologias inovadoras para segurança nacional

**Características Principais**:
- Pesquisa transformadora com alto risco e alta recompensa
- Foco em problemas "DARPA-difíceis" (e se for verdade, quem se importa)
- Ênfase em protótipos, demonstrações e caminhos de transição
- Frequentemente requer múltiplas fases (viabilidade, desenvolvimento, demonstração)
- Forte rastreamento de gerenciamento de projeto e marcos
- Teaming e colaboração frequentemente necessários
- Varia dramaticamente por gerente de programa e BAA (Broad Agency Announcement)

## Componentes Principais de Propostas de Pesquisa

### 1. Resumo Executivo / Resumo do Projeto / Abstrato

Toda proposta precisa de uma visão geral concisa que comunique os elementos essenciais da pesquisa tanto para revisores técnicos quanto para oficiais de programa.

**Propósito**: Fornecer um resumo independente que capture a visão de pesquisa, significância e abordagem

**Comprimento**:
- NSF: 1 página (Project Summary com Visão Geral, Mérito Intelectual, Impactos Amplos separados)
- NIH: 30 linhas (Project Summary/Abstrato)
- DOE: Varia (tipicamente 1 página)
- DARPA: Varia (frequentemente 1-2 páginas)

**Elementos Essenciais**:
- Declaração clara do problema ou questão de pesquisa
- Por que este problema importa (significância, urgência, impacto)
- Abordagem novel ou inovação
- Resultados e deliverables esperados
- Qualificações da equipe
- Impactos amplos ou caminho translacional

**Estratégia de Escrita**:
- Abra com uma observação atraente que estabeleça importância
- Use linguagem acessível (evite jargão nas primeiras sentenças)
- Declare objetivos específicos e mensuráveis
- Transmita entusiasmo e confiança
- Garanta que cada sentença agregue valor (sem preenchimento)
- Termine com visão transformadora ou declaração de impacto

**Erros Comuns a Evitar**:
- Ser muito técnico ou detalhado (guarde para descrição de projeto)
- Falhar em articular "por que agora" ou "por que esta equipe"
- Objetivos ou resultados vagos
- Negligenciar impactos amplos ou significância
- Declarações genéricas que poderiam se aplicar a qualquer proposta

### 2. Descrição de Projeto / Estratégia de Pesquisa

A narrativa técnica central que apresenta o plano de pesquisa em detalhe.

**Estrutura Varia por Agência:**

**Descrição de Projeto NSF** (tipicamente 15 páginas):
- Introdução e contexto
- Objetivos e questões de pesquisa
- Resultados preliminares (se aplicável)
- Plano e metodologia de pesquisa
- Cronograma e marcos
- Impactos amplos (integrados ao longo ou seção separada)
- Suporte anterior do NSF (se aplicável)

**Estratégia de Pesquisa NIH** (12 páginas para R01):
- Significância (por que o problema importa)
- Inovação (o que é novel e transformador)
- Abordagem (plano de pesquisa detalhado)
  - Dados preliminares
  - Design de pesquisa e métodos
  - Resultados esperados
  - Problemas potenciais e abordagens alternativas

**Narrativa de Projeto DOE** (varia):
- Contexto e significância
- Abordagem técnica e inovação
- Qualificações e experiência
- Instalações e recursos
- Gerenciamento de projeto e cronograma

**Volume Técnico DARPA** (varia):
- Desafio técnico e inovação
- Abordagem e metodologia
- Cronograma e marcos
- Deliverables e métricas
- Qualificações da equipe
- Avaliação de risco e mitigação

Para orientação específica detalhada de agências, consulte:
- `references/nsf_guidelines.md`
- `references/nih_guidelines.md`
- `references/doe_guidelines.md`
- `references/darpa_guidelines.md`

### 3. Objetivos Específicos (NIH) ou Objetivos (NSF/DOE/DARPA)

Metas claras e testáveis que estruturam o plano de pesquisa.

**Página de Objetivos Específicos NIH** (1 página):
- Parágrafo de abertura: Lacuna no conhecimento e significância
- Meta de longo prazo e objetivos imediatos
- Hipótese central ou questão de pesquisa
- 2-4 objetivos específicos com sub-objetivos
- Resultados esperados e impacto
- Parágrafo de retorno: Por que isto importa

**Estrutura para Cada Objetivo:**
- Declaração de objetivo (1-2 sentenças, começa com verbo de ação)
- Justificativa (por que este objetivo, suporte de dados preliminares)
- Hipótese de trabalho (predição testável)
- Resumo de abordagem (visão geral breve de métodos)
- Resultados esperados e interpretação

**Estratégia de Escrita**:
- Faça objetivos independentes mas complementares
- Garanta que cada objetivo seja alcançável dentro de cronograma e orçamento
- Forneça detalhe suficiente para julgar viabilidade
- Inclua planos de contingência ou abordagens alternativas
- Use estrutura paralela através dos objetivos
- Declare claramente o que será aprendido de cada objetivo

Para orientação detalhada, consulte `references/specific_aims_guide.md`.

### 4. Impactos Amplos (NSF) / Significância (NIH)

Articule o valor social, educacional ou translacional da pesquisa.

**Impactos Amplos NSF** (componente crítico, ponderação igual com Mérito Intelectual):

NSF avalia explicitamente impactos amplos. Aborde pelo menos uma destas áreas:
1. **Avançando descoberta e compreensão enquanto promove ensino, treinamento e aprendizado**
   - Integração de pesquisa e educação
   - Treinamento de estudantes e pós-docs
   - Desenvolvimento curricular
   - Materiais e recursos educacionais

2. **Ampliando participação de grupos sub-representados**
   - Estratégias de recrutamento e retenção
   - Parcerias com instituições que servem minorias
   - Alcance a comunidades sub-representadas
   - Programas de mentoria

3. **Aprimorando infraestrutura para pesquisa e educação**
   - Instalações compartilhadas ou instrumentação
   - Ciberinfrastrutura e recursos de dados
   - Ferramentas ou bancos de dados para toda comunidade
   - Software ou métodos de código aberto

4. **Disseminação ampla para aprimorar compreensão científica e tecnológica**
   - Alcance público e comunicação científica
   - Programas educacionais K-12
   - Exposições de museus ou engajamento de mídia
   - Resumos de política ou engajamento de stakeholders

5. **Benefícios para a sociedade**
   - Impacto econômico ou comercialização
   - Benefícios de saúde, ambiente ou segurança nacional
   - Tomada de decisão informada
   - Desenvolvimento de força de trabalho

**Estratégia de Escrita para Impactos Amplos NSF**:
- Seja específico com atividades concretas, não declarações vagas
- Forneça cronograma e marcos para atividades de impactos amplos
- Explique como impactos serão medidos e avaliados
- Conecte a recursos institucionais e programas existentes
- Demonstre compromisso através de esforços preliminares ou parcerias
- Integre com plano de pesquisa (não agregado)

**Significância NIH**:
- Aborda problema importante ou barreira crítica ao progresso
- Melhora conhecimento científico, capacidade técnica ou prática clínica
- Potencial de levar a melhores resultados, intervenções ou compreensão
- Rigor de pesquisa anterior na área
- Alinhamento com missão NIH e prioridades de institutos

Para orientação detalhada, consulte `references/broader_impacts.md`.

### 5. Inovação e Potencial Transformador

Articule o que é novel, criativo e transformador de paradigma sobre a pesquisa.

**Elementos de Inovação a Destacar**:
- **Inovação Conceitual**: Novos frameworks, modelos ou teorias
- **Inovação Metodológica**: Técnicas, abordagens ou tecnologias novel
- **Inovação Integradora**: Combinando disciplinas ou abordagens de novas maneiras
- **Inovação Translacional**: Novos caminhos de descoberta para aplicação
- **Inovação de Escala**: Escopo ou resolução sem precedentes

**Estratégia de Escrita**:
- Declare claramente o que é inovador (não assuma que é óbvio)
- Explique por que abordagens atuais são insuficientes
- Descreva como sua inovação supera limitações
- Forneça evidência que inovação é viável (dados preliminares, prova de conceito)
- Distinga avanços incrementais de transformadores
- Equilibre inovação com viabilidade (não demasiado arriscado)

**Erros Comuns**:
- Reivindicar novidade sem demonstrar conhecimento de trabalho anterior
- Confundir "novo para mim" com "novo para o campo"
- Prometer em excesso sem evidência de suporte
- Ser demasiado incremental (variação menor de trabalho existente)
- Ser demasiado especulativo (sem caminho para sucesso)

### 6. Abordagem e Métodos de Pesquisa

Descrição detalhada de como a pesquisa será conduzida.

**Componentes Essenciais**:
- Design e framework geral de pesquisa
- Métodos detalhados para cada objetivo
- Tamanhos de amostra, poder estatístico e planos de análise
- Cronograma e sequência de atividades
- Coleta, gerenciamento e análise de dados
- Abordagens de controle e validação de qualidade
- Problemas potenciais e estratégias alternativas
- Medidas de rigor e reprodutibilidade

**Estratégia de Escrita**:
- Forneça detalhe suficiente para reprodutibilidade e avaliação de viabilidade
- Use sub-títulos e figuras para melhorar organização
- Justifique escolha de métodos e abordagens
- Aborde limitações potenciais proativamente
- Inclua dados preliminares demonstrando viabilidade
- Mostre que você considerou todo o processo de pesquisa
- Equilibre detalhe com legibilidade (use materiais suplementares para detalhes extensos)

**Para Pesquisa Experimental**:
- Descreva design experimental (controles, réplicas, cegamento)
- Especifique materiais, reagentes e equipamento
- Detalhe protocolos de coleta de dados
- Explique planos de análise estatística
- Aborde rigor e reprodutibilidade

**Para Pesquisa Computacional**:
- Descreva algoritmos, modelos e software
- Especifique datasets e abordagens de validação
- Explique recursos computacionais necessários
- Aborde disponibilidade de código e documentação
- Descreva benchmarking e métricas de performance

**Para Pesquisa Clínica ou Translacional**:
- Descreva população estudada e recrutamento
- Detalhe protocolos de intervenção ou tratamento
- Explique medidas de resultado e avaliações
- Aborde aprovações regulatórias (IRB, IND, IDE)
- Descreva design e monitoramento de ensaio clínico

Para orientação metodológica detalhada por disciplina, consulte `references/research_methods.md`.

### 7. Dados Preliminares e Viabilidade

Demonstre que a pesquisa é alcançável e a equipe é capaz.

**Propósito**:
- Prove que a abordagem proposta pode funcionar
- Mostre que a equipe possui expertise necessária
- Demonstre acesso a recursos necessários
- Reduza risco percebido para revisores
- Forneça fundação para trabalho proposto

**O Que Incluir**:
- Estudos piloto ou resultados de prova de conceito
- Desenvolvimento ou otimização de método
- Acesso a recursos únicos (amostras, dados, colaboradores)
- Publicações relevantes de sua equipe
- Modelos ou simulações preliminares
- Avaliações de viabilidade ou cálculos de poder

**Requisitos NIH**:
- Aplicações R01 tipicamente requerem dados preliminares substanciais
- Aplicações R21 podem ter requisitos menos rigorosos
- Investigadores novos podem ter menos dados preliminares
- Dados preliminares devem apoiar diretamente objetivos propostos

**Abordagem NSF**:
- Dados preliminares menos comumente necessários que NIH
- Podem ser importantes para abordagens de alto risco ou novel
- Podem fortalecer proposta para programas competitivos

**Estratégia de Escrita**:
- Apresente dados mais atraentes que apoiam sua abordagem
- Conecte claramente dados preliminares a objetivos propostos
- Reconheça limitações e como trabalho proposto as abordará
- Use figuras e visualizações de dados efetivamente
- Evite sobre-interpretar ou exagerar descobertas preliminares
- Mostre trajetória de seu programa de pesquisa

### 8. Cronograma, Marcos e Plano de Gerenciamento

Demonstre que o projeto é bem-planejado e alcançável dentro do cronograma proposto.

**Elementos Essenciais**:
- Cronograma faseado com marcos claros
- Sequência lógica e dependências
- Cronogramas realistas para cada atividade
- Pontos de decisão e critérios de go/no-go
- Estratégias de mitigação de risco
- Alocação de recursos ao longo do tempo
- Plano de coordenação para equipes multi-institucionais

**Formatos de Apresentação**:
- Gráficos de Gantt mostrando atividades sobrepostas
- Detalhamento ano-a-ano de atividades
- Marcos trimestrais e deliverables
- Tabela de objetivos/tarefas com cronograma e pessoal

**Estratégia de Escrita**:
- Seja realista sobre o que pode ser alcançado
- Construa tempo para atrasos ou percalços inesperados
- Mostre que cronograma se alinha com orçamento e pessoal
- Demonstre compreensão de cronogramas regulatórios (IRB, IACUC)
- Inclua tempo para disseminação e impactos amplos
- Aborde como progresso será monitorado e avaliado

**Ênfase DARPA**:
- Particularmente importante para propostas DARPA
- Marcos técnicos claros com métricas mensuráveis
- Deliverables trimestrais e relatórios
- Estrutura baseada em fases com critérios de saída
- Planejamento de demonstração e transição

Para orientação detalhada, consulte `references/timeline_planning.md`.

### 9. Qualificações de Equipe e Colaboração

Demonstre que a equipe possui expertise, experiência e recursos para ter sucesso.

**Elementos Essenciais**:
- Qualificações de PI e expertise relevante
- Papéis e contribuições de Co-I e colaboradores
- Histórico na área de pesquisa
- Expertise complementar através da equipe
- Suporte institucional e recursos
- Histórico de colaboração anterior (se aplicável)
- Plano de mentoria e treinamento (para estudantes/pós-docs)

**Estratégia de Escrita**:
- Destaque publicações e accomplishments mais relevantes
- Defina claramente papéis e responsabilidades
- Mostre que composição de equipe é necessária (não apenas conveniente)
- Demonstre colaborações bem-sucedidas anteriores
- Explique como equipe será gerenciada e coordenada
- Explique compromisso institucional e suporte

**Biosketches / CVs**:
- Siga formatos específicos de agências (NSF, NIH, DOE, DARPA diferem)
- Destaque publicações e accomplishments mais relevantes
- Inclua atividades sinérgicas e colaborações
- Mostre trajetória e produtividade
- Aborde qualquer lacuna de carreira ou interrupção

**Cartas de Colaboração**:
- Compromissos e contribuições específicos
- Demonstra parceria genuína
- Inclui compartilhamento de recursos ou acordos de acesso
- Assinado e em papel timbrado

Para orientação detalhada, consulte `references/team_building.md`.

### 10. Orçamento e Justificativa Orçamentária

Desenvolva orçamentos realistas que se alinhem com trabalho proposto e diretrizes de agência.

**Categorias Orçamentárias** (típicas):
- **Pessoal**: Salário e encargos para PI, co-Is, pós-docs, estudantes, pessoal
- **Equipamento**: Itens >$5.000 (varia por agência)
- **Viagem**: Conferências, colaborações, trabalho de campo
- **Materiais e Suprimentos**: Consumíveis, reagentes, software
- **Outros Custos Diretos**: Custos de publicação, incentivos a participantes, consultoria
- **Custos Indiretos (F&A)**: Overhead institucional (taxas variam)
- **Subadjudicações**: Custos para instituições colaboradoras

**Considerações Específicas de Agência**:

**NSF**:
- Justificativa de orçamento completo necessária
- Compartilhamento de custos genericamente não necessário (mas pode fortalecer proposta)
- Até 2 meses de salário de verão para faculdade
- Suporte a estudantes de pós-graduação encorajado

**NIH**:
- Orçamentos modulares para ≤$250K custos diretos por ano (R01)
- Orçamentos detalhados para >$250K ou adjudicações complexas
- Teto de salário se aplica (~$221.900 para 2024)
- Limitado a 1 mês (8,33% FTE) para maioria dos PIs

**DOE**:
- Frequentemente requer compartilhamento de custos (especialmente ARPA-E)
- Orçamento detalhado com detalhamento trimestral
- Requer cartas de compromisso institucional
- Orçamentos de colaboração de laboratório nacional separados

**DARPA**:
- Orçamentos detalhados por fase e tarefa
- Requer dados de custo de suporte para grandes compras
- Frequentemente requer estruturas cost-plus ou preço fixo firme
- Orçamento de viagem para reuniões de programa

**Escrita de Justificativa Orçamentária**:
- Justifique cada item de linha em termos do plano de pesquisa
- Explique percentuais de esforço para pessoal
- Descreva equipamento específico e por que necessário
- Justifique viagem (conferências, colaborações)
- Explique papéis e taxas de consultante
- Mostre como orçamento se alinha com cronograma

Para orientação orçamentária detalhada, consulte `references/budget_preparation.md`.

## Critérios de Revisão por Agência

Entender como propostas são avaliadas é crítico para escrever aplicações competitivas.

### Critérios de Revisão NSF

**Mérito Intelectual** (principal):
- Qual é o potencial da atividade proposta de avançar conhecimento?
- Quão bem concebida e organizada é a atividade proposta?
- Há acesso suficiente a recursos?
- Quão bem-qualificado é o indivíduo, equipe ou instituição para conduzir atividades propostas?

**Impactos Amplos** (igualmente importante):
- Qual é o potencial da atividade proposta de beneficiar a sociedade?
- Em que medida a proposta aborda impactos amplos de maneiras significativas?

**Considerações Adicionais**:
- Integração de pesquisa e educação
- Diversidade e inclusão
- Resultados de suporte anterior do NSF (se aplicável)

### Critérios de Revisão NIH

**Critérios Pontuados** (escala 1-9, 1 = excepcionalmente, 9 = fraco):

1. **Significância**
   - Aborda problema importante ou barreira crítica
   - Melhora conhecimento científico, capacidade técnica ou prática clínica
   - Alinha-se com missão NIH

2. **Investigador(es)**
   - Bem-adequado ao projeto
   - Histórico de accomplishments
   - Treinamento e expertise adequados

3. **Inovação**
   - Conceitos, abordagens, metodologias ou intervenções novel
   - Desafia paradigmas existentes
   - Aborda problema importante de maneiras criativas

4. **Abordagem**
   - Bem-razoada e apropriada
   - Rigorosa e reprodutível
   - Adequadamente considera problemas potenciais
   - Viável dentro de cronograma

5. **Ambiente**
   - Suporte institucional e recursos
   - Ambiente científico contribui para probabilidade de sucesso

**Considerações Adicionais de Revisão** (não pontuadas mas discutidas):
- Proteções para sujeitos humanos
- Inclusão de mulheres, minorias e crianças
- Bem-estar de animais vertebrados
- Biohazards
- Resposta de resubmissão (se aplicável)
- Apropriação de orçamento e cronograma

### Critérios de Revisão DOE

Varia por escritório de programa, mas genericamente inclui:
- Mérito científico e/ou técnico
- Apropriação do método proposto ou abordagem
- Competência de pessoal e adequação de instalações
- Razoabilidade e apropriação de orçamento
- Relevância a missão e objetivos de programa DOE

### Critérios de Revisão DARPA

**Considerações específicas de DARPA**:
- Mérito científico e técnico geral
- Potencial de contribuição a missão DARPA
- Relevância a objetivos de programa declarados
- Planos e capacidade de alcançar transição de tecnologia
- Qualificações e experiência de equipe proposta
- Realismo de custos propostos e disponibilidade de fundos

**Questões-chave que DARPA Faz**:
- **E se você tiver sucesso?** (Impacto se pesquisa funcionar)
- **E se você estiver certo?** (Implicações de sua hipótese)
- **Quem se importa?** (Por que importa para segurança nacional)

Para critérios de revisão detalhados por agência, consulte `references/review_criteria.md`.

## Princípios de Escrita para Propostas Competitivas

### Clareza e Acessibilidade

**Escreva para Múltiplos Públicos**:
- Revisores técnicos em seu campo (scrutinizarão métodos)
- Revisores em campos relacionados mas não idênticos (precisam de contexto)
- Oficiais de programa (procuram alinhamento com objetivos de agência)
- Membros de painel lendo 15+ propostas (precisam de organização clara)

**Estratégias**:
- Use títulos e sub-títulos claros
- Comece seções com parágrafos de visão geral
-