---
name: scientific-writing
description: "Competência essencial para a ferramenta de pesquisa e escrita profunda. Escreva manuscritos científicos em parágrafos completos (nunca em pontos de marcação). Use processo de duas etapas: (1) criar esboços de seção com pontos-chave usando research-lookup, (2) converter para prosa fluida. Estrutura IMRAD, citações (APA/AMA/Vancouver), figuras/tabelas, diretrizes de relatório (CONSORT/STROBE/PRISMA), para artigos de pesquisa e submissões em revistas."
allowed-tools: [Read, Write, Edit, Bash]
---

# Escrita Científica

## Visão Geral

**Esta é a competência essencial para a ferramenta de pesquisa e escrita profunda**—combinando pesquisa profunda orientada por IA com outputs bem formatados. Todo documento produzido é apoiado por busca abrangente de literatura e citações verificadas através da competência research-lookup.

Escrita científica é um processo para comunicar pesquisa com precisão e clareza. Elabore manuscritos usando estrutura IMRAD, citações (APA/AMA/Vancouver), figuras/tabelas e diretrizes de relatório (CONSORT/STROBE/PRISMA). Aplique esta competência para artigos de pesquisa e submissões em revistas.

**Princípio Crítico: Sempre escreva em parágrafos completos com prosa fluida. Nunca submeta pontos de marcação no manuscrito final.** Use um processo de duas etapas: primeiro crie esboços de seção com pontos-chave usando research-lookup, depois converta esses esboços em parágrafos completos.

## Quando Usar Esta Competência

Esta competência deve ser usada quando:
- Redigir ou revisar qualquer seção de um manuscrito científico (resumo, introdução, métodos, resultados, discussão)
- Estruturar um artigo de pesquisa usando IMRAD ou outros formatos padrão
- Formatar citações e referências em estilos específicos (APA, AMA, Vancouver, Chicago, IEEE)
- Criar, formatar ou melhorar figuras, tabelas e visualizações de dados
- Aplicar diretrizes de relatório específicas do estudo (CONSORT para ensaios, STROBE para estudos observacionais, PRISMA para revisões)
- Redigir resumos que atendam aos requisitos da revista (estruturados ou não estruturados)
- Preparar manuscritos para submissão em revistas específicas
- Melhorar clareza, concisão e precisão da escrita
- Garantir o uso adequado de terminologia e nomenclatura específicas do campo
- Abordar comentários de revisores e revisar manuscritos

## Aprimoramento Visual com Esquemas Científicos

**⚠️ OBRIGATÓRIO: Todo artigo científico DEVE incluir pelo menos 1-2 figuras geradas por IA usando a competência scientific-schematics.**

Isto não é opcional. Artigos científicos sem elementos visuais estão incompletos. Antes de finalizar qualquer documento:
1. Gere no mínimo UM esquema ou diagrama usando scientific-schematics
2. Prefira 2-3 figuras para artigos abrangentes (fluxograma de métodos, visualização de resultados, diagrama conceitual)

**Como gerar figuras:**
- Use a competência **scientific-schematics** para gerar diagramas de qualidade para publicação alimentados por IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "sua descrição do diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltonismo, alto contraste)
- Salvamento de outputs no diretório figures/

**Quando adicionar esquemas:**
- Fluxogramas de design de estudo e metodologia (CONSORT, PRISMA, STROBE)
- Diagramas de estrutura conceitual
- Ilustrações de fluxo de trabalho experimental
- Diagramas de pipeline de análise de dados
- Diagramas de vias biológicas ou mecanismos
- Visualizações de arquitetura de sistemas
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da competência scientific-schematics.

---

## Capacidades Essenciais

### 1. Estrutura e Organização do Manuscrito

**Formato IMRAD**: Guie artigos através da estrutura padrão Introduction, Methods, Results, And Discussion (Introdução, Métodos, Resultados e Discussão) usada na maioria das disciplinas científicas. Isto inclui:
- **Introdução**: Estabeleça contexto da pesquisa, identifique lacunas, declare objetivos
- **Métodos**: Detalhe design do estudo, populações, procedimentos e abordagens de análise
- **Resultados**: Apresente achados objetivamente sem interpretação
- **Discussão**: Interprete resultados, reconheça limitações, proponha direções futuras

Para orientação detalhada sobre estrutura IMRAD, consulte `references/imrad_structure.md`.

**Estruturas Alternativas**: Suporte formatos específicos de disciplinas incluindo:
- Artigos de revisão (narrativa, sistemática, scoping)
- Relatos de caso e séries de casos
- Meta-análises e análises agrupadas
- Artigos teóricos/modelagem
- Artigos de métodos e protocolos

### 2. Orientação para Escrita Específica de Seção

**Composição de Resumo**: Redija resumos concisos e autossuficientes (100-250 palavras) que capturem o propósito do artigo, métodos, resultados e conclusões. Suporte tanto resumos estruturados (com seções rotuladas) quanto formatos não estruturados em parágrafo único.

**Desenvolvimento de Introdução**: Construa introduções atrativas que:
- Estabeleçam a importância do problema de pesquisa
- Reviem literatura relevante sistematicamente
- Identifiquem lacunas ou controvérsias no conhecimento
- Declarem claras questões ou hipóteses de pesquisa
- Expliquem a novidade e significância do estudo

**Documentação de Métodos**: Garanta reprodutibilidade através de:
- Descrições detalhadas de participantes/amostra
- Documentação clara de procedimentos
- Métodos estatísticos com justificativa
- Especificações de equipamento e materiais
- Declarações de aprovação ética e consentimento

**Apresentação de Resultados**: Apresente achados com:
- Fluxo lógico de resultados primários para secundários
- Integração com figuras e tabelas
- Significância estatística com tamanhos de efeito
- Relatório objetivo sem interpretação

**Construção de Discussão**: Sintetize achados por:
- Relacionamento de resultados com questões de pesquisa
- Comparação com literatura existente
- Reconhecimento honesto de limitações
- Proposição de explicações mecanísticas
- Sugestão de implicações práticas e pesquisa futura

### 3. Gerenciamento de Citação e Referência

Aplique estilos de citação corretamente em disciplinas. Para guias de estilo abrangentes, consulte `references/citation_styles.md`.

**Principais Estilos de Citação:**
- **AMA (American Medical Association)**: Citações em número sobrescrito, comum em medicina
- **Vancouver**: Citações numeradas entre colchetes, padrão biomédico
- **APA (American Psychological Association)**: Citações em texto autor-data, comum em ciências sociais
- **Chicago**: Notas-bibliografia ou autor-data, humanidades e ciências
- **IEEE**: Colchetes numerados, engenharia e ciência da computação

**Boas Práticas:**
- Cite fontes primárias quando possível
- Inclua literatura recente (últimos 5-10 anos para campos ativos)
- Equilibre distribuição de citações entre introdução e discussão
- Verifique todas as citações contra fontes originais
- Use software de gerenciamento de referências (Zotero, Mendeley, EndNote)

### 4. Figuras e Tabelas

Crie visualizações de dados eficazes que aprimorem a compreensão. Para boas práticas detalhadas, consulte `references/figures_tables.md`.

**Quando Usar Tabelas vs. Figuras:**
- **Tabelas**: Dados numéricos precisos, conjuntos complexos, múltiplas variáveis exigindo valores exatos
- **Figuras**: Tendências, padrões, relacionamentos, comparações melhor compreendidas visualmente

**Princípios de Design:**
- Torne cada tabela/figura auto-explicativa com legendas completas
- Use formatação e terminologia consistentes em todos os elementos de apresentação
- Rotule todos os eixos, colunas e linhas com unidades
- Inclua tamanhos de amostra (n) e anotações estatísticas
- Siga a diretriz "uma tabela/figura por 1000 palavras"
- Evite duplicar informações entre texto, tabelas e figuras

**Tipos de Figura Comuns:**
- Gráficos de barras: Comparando categorias discretas
- Gráficos de linha: Mostrando tendências ao longo do tempo
- Gráficos de dispersão: Exibindo correlações
- Gráficos de caixa: Mostrando distribuições e outliers
- Mapas de calor: Visualizando matrizes e padrões

### 5. Diretrizes de Relatório por Tipo de Estudo

Assegure completude e transparência seguindo padrões de relatório estabelecidos. Para detalhes de diretrizes abrangentes, consulte `references/reporting_guidelines.md`.

**Diretrizes Principais:**
- **CONSORT**: Ensaios clínicos randomizados
- **STROBE**: Estudos observacionais (coorte, caso-controle, transversal)
- **PRISMA**: Revisões sistemáticas e meta-análises
- **STARD**: Estudos de acurácia diagnóstica
- **TRIPOD**: Estudos de modelo de predição
- **ARRIVE**: Pesquisa com animais
- **CARE**: Relatos de caso
- **SQUIRE**: Estudos de melhoria de qualidade
- **SPIRIT**: Protocolos de estudo para ensaios clínicos
- **CHEERS**: Avaliações econômicas

Cada diretriz fornece checklists garantindo que todos os elementos metodológicos críticos sejam relatados.

### 6. Princípios e Estilo de Escrita

Aplique princípios fundamentais de escrita científica. Para orientação detalhada, consulte `references/writing_principles.md`.

**Clareza**:
- Use linguagem precisa e sem ambiguidades
- Defina termos técnicos e abreviações no primeiro uso
- Mantenha fluxo lógico dentro e entre parágrafos
- Use voz ativa quando apropriado para clareza

**Concisão**:
- Elimine palavras e frases redundantes
- Favoreça sentenças mais curtas (média de 15-20 palavras)
- Remova qualificadores desnecessários
- Respeite limites de palavras rigorosamente

**Acurácia**:
- Relate valores exatos com precisão apropriada
- Use terminologia consistente em todo o documento
- Distingua entre observações e interpretações
- Reconheça incerteza apropriadamente

**Objetividade**:
- Apresente resultados sem viés
- Evite superestimar achados ou implicações
- Reconheça evidência conflitante
- Mantenha tom profissional e neutro

### 7. Processo de Escrita: Do Esboço aos Parágrafos Completos

**CRÍTICO: Sempre escreva em parágrafos completos, nunca submeta pontos de marcação em artigos científicos.**

Artigos científicos devem ser escritos em prosa completa e fluida. Use esta abordagem de duas etapas para escrita eficaz:

**Etapa 1: Criar Esboços de Seção com Pontos-Chave**

Ao começar uma nova seção:
1. Use a competência research-lookup para reunir literatura e dados relevantes
2. Crie um esboço estruturado com pontos de marcação marcando:
   - Argumentos ou achados principais a apresentar
   - Estudos-chave a citar
   - Pontos de dados e estatísticas a incluir
   - Fluxo lógico e organização
3. Esses pontos de marcação servem como andaime—NÃO são o manuscrito final

**Exemplo de esboço (seção Introdução):**
```
- Contexto: IA em descoberta de medicamentos ganhando tração
  * Cite revisões recentes (Smith 2023, Jones 2024)
  * Métodos tradicionais são lentos e caros
- Lacuna: Aplicação limitada a doenças raras
  * Apenas 2 estudos anteriores (Lee 2022, Chen 2023)
  * Pequenos conjuntos de dados permanecem um desafio
- Nossa abordagem: Aprendizado de transferência de doenças comuns
  * Arquitetura inovadora combinando X e Y
- Objetivos do estudo: Validar em 3 conjuntos de dados de doença rara
```

**Etapa 2: Converter Pontos-Chave em Parágrafos Completos**

Uma vez que o esboço está pronto, expanda cada ponto de marcação em prosa apropriada:

1. **Transforme pontos de marcação em sentenças completas** com sujeitos, verbos e objetos
2. **Adicione transições** entre sentenças e ideias (porém, além disso, em contraste, subsequentemente)
3. **Integre citações naturalmente** dentro de sentenças, não como listas
4. **Expanda com contexto e explicação** que pontos de marcação omitem
5. **Garanta fluxo lógico** de uma sentença para a próxima dentro de cada parágrafo
6. **Varie a estrutura de sentença** para manter o engajamento do leitor

**Exemplo de conversão para prosa:**

```
Abordagens de inteligência artificial ganharam tração significativa em pipelines de 
descoberta de medicamentos na última década (Smith, 2023; Jones, 2024). Embora esses 
métodos computacionais mostrem promessa para acelerar a identificação de candidatos 
terapêuticos, abordagens experimentais tradicionais permanecem lentas e intensivas em 
recursos, frequentemente exigindo anos de trabalho laboratorial e investimento financeiro 
substancial. Porém, a aplicação de IA a doenças raras foi limitada, com apenas dois 
estudos anteriores demonstrando resultados de prova de conceito (Lee, 2022; Chen, 2023). 
O obstáculo principal foi a escassez de dados de treinamento para condições afetando 
pequenas populações de pacientes.

Para abordar este desafio, desenvolvemos uma abordagem de aprendizado de transferência 
que aproveita conhecimento de doenças comuns bem caracterizadas para predizer alvos 
terapêuticos para condições raras. Nossa arquitetura neural inovadora combina camadas 
convolucionais para extração de características moleculares com mecanismos de atenção 
para modelagem de interação proteína-ligante. O objetivo deste estudo foi validar nossa 
abordagem em três conjuntos de dados de doença rara independentes, avaliando tanto a 
acurácia preditiva quanto a interpretabilidade biológica dos resultados.
```

**Diferenças-Chave Entre Esboços e Texto Final:**

| Esboço (Etapa de Planejamento) | Manuscrito Final |
|--------------------------------|-----------------|
| Pontos de marcação e fragmentos | Sentenças e parágrafos completos |
| Notas telegráficas | Explicações completas com contexto |
| Lista de citações | Citações integradas em prosa |
| Ideias abreviadas | Argumentos desenvolvidos com transições |
| Apenas para seus olhos | Para publicação e revisão por pares |

**Erros Comuns a Evitar:**

- ❌ **Nunca** deixe pontos de marcação no manuscrito final
- ❌ **Nunca** submeta listas onde parágrafos deveriam estar
- ❌ **Não** use listas numeradas ou com marcadores em seções Resultados ou Discussão (exceto casos específicos como hipóteses do estudo ou critérios de inclusão)
- ❌ **Não** escreva fragmentos de sentença ou pensamentos incompletos
- ✅ **Faça** uso ocasional de listas apenas em Métodos (ex: critérios de inclusão/exclusão, listas de materiais)
- ✅ **Faça** garantir que cada seção flua como prosa conectada
- ✅ **Faça** ler parágrafos em voz alta para verificar fluxo natural

**Quando Listas SÃO Aceitáveis (Casos Limitados):**

Listas podem aparecer em artigos científicos apenas em contextos específicos:
- **Métodos**: Critérios de inclusão/exclusão, materiais e reagentes, características de participantes
- **Materiais Suplementares**: Protocolos estendidos, listas de equipamento, parâmetros detalhados
- **Nunca em**: Resumo, Introdução, Resultados, Discussão, Conclusões

**Integração com Research Lookup:**

A competência research-lookup é essencial para a Etapa 1 (criando esboços):
1. Procure por artigos relevantes usando research-lookup
2. Extraia achados principais, métodos e dados
3. Organize achados como pontos de marcação em seu esboço
4. Depois converta o esboço para parágrafos completos na Etapa 2

Este processo de duas etapas garante que você:
- Reúna e organize informações sistematicamente
- Crie estrutura lógica antes de escrever
- Produza prosa polida e pronta para publicação
- Mantenha foco no fluxo narrativo

### 8. Formatação Específica de Revista

Adapte manuscritos aos requisitos da revista:
- Siga diretrizes do autor para estrutura, comprimento e formato
- Aplique estilos de citação específicos da revista
- Atenda especificações de figuras/tabelas (resolução, formatos de arquivo, dimensões)
- Inclua declarações obrigatórias (financiamento, conflitos de interesse, disponibilidade de dados, aprovação ética)
- Cumpra limites de palavras para cada seção
- Formate de acordo com requisitos de template quando fornecido

### 9. Linguagem e Terminologia Específicas do Campo

Adapte linguagem, terminologia e convenções para combinar com a disciplina científica específica. Cada campo possui vocabulário estabelecido, fraseados preferidos e convenções específicas de domínio que sinalizam expertise e garantem clareza para o público-alvo.

**Identifique Convenções Linguísticas Específicas do Campo:**
- Revise terminologia usada em artigos recentes de alto impacto na revista-alvo
- Anote abreviações, unidades e sistemas de notação específicos do campo
- Identifique termos preferidos (ex: "participantes" vs. "sujeitos," "composto" vs. "droga," "espécimes" vs. "amostras")
- Observe como métodos, organismos ou técnicas são tipicamente descritos

**Ciências Biomédicas e Clínicas:**
- Use terminologia anatômica e clínica precisa (ex: "infarto do miocárdio" não "ataque cardíaco" em escrita formal)
- Siga nomenclatura padronizada de doença (ICD, DSM, SNOMED-CT)
- Especifique nomes de medicamentos usando nomes genéricos primeiro, nomes de marca entre parênteses se necessário
- Use "pacientes" para estudos clínicos, "participantes" para pesquisa comunitária
- Siga nomenclatura Human Genome Variation Society (HGVS) para variantes genéticas
- Relate valores de laboratório com unidades padrão (unidades SI na maioria das revistas internacionais)

**Biologia Molecular e Genética:**
- Use itálicos para símbolos de genes (ex: *TP53*), fonte regular para proteínas (ex: p53)
- Siga nomenclatura de genes específica de espécie (maiúsculas para humano: *BRCA1*; inicial minúscula para camundongo: *Brca1*)
- Especifique nomes de organismos em cheio na primeira menção, então use abreviações aceitas (ex: *Escherichia coli*, depois *E. coli*)
- Use notação genética padrão (ex: +/+, +/-, -/- para genótipos)
- Empregue terminologia estabelecida para técnicas moleculares (ex: "PCR quantitativo" ou "qPCR," não "PCR em tempo real")

**Química e Ciências Farmacêuticas:**
- Siga nomenclatura IUPAC para compostos químicos
- Use nomes sistemáticos para compostos inovadores, nomes comuns para substâncias bem conhecidas
- Especifique estruturas químicas usando notação padrão (ex: SMILES, InChI para bancos de dados)
- Relate concentrações com unidades apropriadas (mM, μM, nM, ou % m/v, v/v)
- Descreva rotas de síntese usando nomenclatura de reação aceita
- Use termos como "biodisponibilidade," "farmacocinética," "IC50" consistentemente com definições de campo

**Ecologia e Ciências Ambientais:**
- Use nomenclatura binomial para espécies (itálica: *Homo sapiens*)
- Especifique autoridades taxonômicas na primeira menção de espécie quando relevante
- Empregue classificações padronizadas de habitat e ecossistema
- Use terminologia consistente para métricas ecológicas (ex: "riqueza de espécies," "índice de diversidade de Shannon")
- Descreva métodos de amostragem com termos padrão de campo (ex: "transecto," "quadrado," "captura-recaptura")

**Física e Engenharia:**
- Siga unidades SI consistentemente a menos que convenções de campo determinem o contrário
- Use notação padrão para quantidades físicas (escalares vs. vetores, tensores)
- Empregue terminologia estabelecida para fenômenos (ex: "emaranhamento quântico," "fluxo laminar")
- Especifique equipamento com números de modelo e fabricantes quando relevante
- Use notação matemática consistente com padrões de campo (ex: ℏ para constante reduzida de Planck)

**Neurociência:**
- Use nomenclatura padronizada de região cerebral (ex: consulte atlas como Allen Brain Atlas)
- Especifique coordenadas para regiões cerebrais usando sistemas estereotáxicos estabelecidos
- Siga convenções para terminologia neural (ex: "potencial de ação" não "spike" em escrita formal)
- Use "atividade neural," "disparo neuronal," "ativação cerebral" apropriadamente baseado em método de medição
- Descreva técnicas de gravação com especificidade apropriada (ex: "patch clamp de célula inteira," "gravação extracelular")

**Ciências Sociais e Comportamentais:**
- Use linguagem focada na pessoa quando apropriada (ex: "pessoas com esquizofrenia" não "esquizofrênicos")
- Empregue construtos psicológicos padronizados e nomes de avaliação validados
- Siga diretrizes APA para reduzir viés em linguagem
- Especifique frameworks teóricos usando terminologia estabelecida
- Use "participantes" em vez de "sujeitos" para pesquisa humana

**Princípios Gerais:**

**Combine Expertise do Público-Alvo:**
- Para revistas especializadas: Use terminologia específica do campo livremente, defina apenas termos altamente especializados ou inovadores
- Para revistas de impacto amplo (ex: *Nature*, *Science*): Defina mais termos técnicos, forneça contexto para conceitos especializados
- Para públicos interdisciplinares: Equilibre precisão com acessibilidade, defina termos no primeiro uso

**Defina Termos Técnicos Estrategicamente:**
- Defina abreviações no primeiro uso: "ácido ribonucleico mensageiro (mRNA)"
- Forneça breves explicações para técnicas especializadas ao escrever para públicos mais amplos
- Evite definir excessivamente termos bem conhecidos do público-alvo (sinaliza falta de familiaridade com o campo)
- Crie um glossário se numerosos termos especializados forem inevitáveis

**Mantenha Consistência:**
- Use o mesmo termo para o mesmo conceito em todo o documento (não alterne entre "medicação," "droga" e "produto farmacêutico")
- Siga um sistema consistente de abreviações (decida sobre "PCR" ou "reação em cadeia da polimerase" após primeira definição)
- Aplique o mesmo sistema de nomenclatura em todo (especialmente para genes, espécies, químicos)

**Evite Erros de Mistura de Campos:**
- Não use terminologia clínica para ciência básica (ex: não chame camundongos de "pacientes")
- Evite coloquialismos ou termos muito gerais no lugar de terminologia precisa do campo
- Não importe terminologia de campos adjacentes sem garantir uso apropriado

**Verifique Uso de Terminologia:**
- Consulte guias de estilo específicos do campo e recursos de nomenclatura
- Verifique como termos são usados em artigos recentes da revista-alvo
- Use bancos de dados e ontologias específicas de domínio (ex: Gene Ontology, termos MeSH)
- Quando incerto, cite uma referência-chave que estabeleça terminologia

### 10. Armadilhas Comuns a Evitar

**Principais Razões de Rejeição:**
1. Estatísticas inapropriadas, incompletas ou insuficientemente descritas
2. Superinterpretação de resultados ou conclusões não apoiadas
3. Métodos mal descritos afetando reprodutibilidade
4. Amostras pequenas, enviesadas ou inapropriadas
5. Qualidade de escrita pobre ou texto difícil de acompanhar
6. Revisão de literatura inadequada ou contexto insuficiente
7. Figuras e tabelas que são pouco claras ou mal projetadas
8. Falha em seguir diretrizes de relatório

**Questões de Qualidade de Escrita:**
- Misturar tempos verbais inapropriadamente (use passado para métodos/resultados, presente para fatos estabelecidos)
- Jargão excessivo ou acrônimos indefinidos
- Quebras de parágrafo que interrompem fluxo lógico
- Transições faltantes entre seções
- Notação ou terminologia inconsistente

## Workflow para Desenvolvimento de Manuscrito

**Etapa 1: Planejamento**
1. Identifique revista-alvo e revise diretrizes do autor
2. Determine diretriz aplicável (CONSORT, STROBE, etc.)
3. Esboce estrutura do manuscrito (geralmente IMRAD)
4. Planeje figuras e tabelas como backbone dos dados do artigo

**Etapa 2: Redação** (Use processo de duas etapas para escrita em cada seção)
1. Comece com figuras e tabelas (a história de dados essencial)
2. Para cada seção abaixo, siga o processo de duas etapas:
   - **Primeiro**: Crie esboço com pontos de marcação usando research-lookup
   - **Segundo**: Converta pontos de marcação para parágrafos completos com prosa fluida
3. Redija Métodos (frequentemente mais fácil de redigir primeiro)
4. Esboce Resultados (descrevendo figuras/tabelas objetivamente)
5. Componha Discussão (interpretando achados)
6. Escreva Introdução (contextualizando a questão de pesquisa)
7. Elabore Resumo (sintetizando a história completa)
8. Crie Título (conciso e descritivo)

**Lembre-se**: Pontos de marcação são apenas para planejamento—o manuscrito final deve estar em parágrafos completos.

**Etapa 3: Revisão**
1. Verifique fluxo lógico e "fio vermelho" em todo o texto
2. Confirme consistência em terminologia e notação
3. Garanta que figuras/tabelas sejam auto-explicativas
4. Confirme aderência às diretrizes de relatório
5. Verifique que todas as citações são precisas e propriamente formatadas
6. Cheque contagem de palavras para cada seção
7. Revise para gramática, ortografia e clareza

**Etapa 4: Preparação Final**
1. Formate de acordo com requisitos da revista
2. Prepare materiais suplementares
3. Redija carta de apresentação realçando significância
4. Complete checklists de submissão
5. Reúna todas as declarações e formulários obrigatórios

## Integração com Outras Competências Científicas

Esta competência funciona eficazmente com:
- **Competências de análise de dados**: Para gerar resultados a relatar
- **Análise estatística**: Para determinar apresentações estatísticas apropriadas
- **Competências de revisão de literatura**: Para contextualizar pesquisa
- **Ferramentas de criação de figuras**: Para desenvolver visualizações de qualidade para publicação

## Referências

Esta competência inclui arquivos de referência abrangentes cobrindo aspectos específicos de escrita científica:

- `references/imrad_structure.md`: Guia detalhado para formato IMRAD