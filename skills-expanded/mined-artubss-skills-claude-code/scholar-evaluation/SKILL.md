# Avaliação de Pesquisa

## Visão Geral

Aplique o framework ScholarEval para avaliar sistematicamente trabalhos acadêmicos e de pesquisa. Esta habilidade fornece metodologia de avaliação estruturada baseada em critérios de avaliação de pesquisa revisados por pares, permitindo análise abrangente de artigos acadêmicos, propostas de pesquisa, revisões de literatura e escrita acadêmica em múltiplas dimensões de qualidade.

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- Avaliar artigos de pesquisa quanto à qualidade e rigor
- Avaliar a abrangência e qualidade de revisões de literatura
- Revisar design de metodologia de pesquisa
- Pontuar abordagens de análise de dados
- Avaliar escrita e apresentação acadêmica
- Fornecer feedback estruturado sobre trabalho acadêmico
- Fazer benchmarking de qualidade de pesquisa contra critérios estabelecidos
- Avaliar prontidão para publicação em veículos-alvo
- Fornecer avaliação quantitativa para complementar peer review qualitativo

## Aprimoramento Visual com Esquemas Científicos

**Ao criar documentos com esta habilidade, sempre considere adicionar diagramas científicos e esquemas para aprimorar a comunicação visual.**

Se seu documento ainda não contém esquemas ou diagramas:
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade de publicação alimentados por IA
- Simplesmente descreva o diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará o esquema automaticamente

**Para novos documentos:** Esquemas científicos devem ser gerados por padrão para representar visualmente conceitos-chave, workflows, arquiteturas ou relações descritas no texto.

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "sua descrição do diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade de publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Acessibilidade garantida (compatível com daltonismo, alto contraste)
- Salvamento de outputs no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de framework de avaliação
- Árvores de decisão de critérios de avaliação de qualidade
- Visualizações de workflow acadêmico
- Fluxogramas de metodologia de avaliação
- Visualizações de rubrica de pontuação
- Diagramas de processo de avaliação
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre a criação de esquemas, consulte a documentação da habilidade scientific-schematics.

---

## Workflow de Avaliação

### Etapa 1: Avaliação Inicial e Definição de Escopo

Comece identificando o tipo de trabalho acadêmico sendo avaliado e o escopo da avaliação:

**Tipos de Trabalho:**
- Artigo de pesquisa completo (empírico, teórico ou revisão)
- Proposta ou protocolo de pesquisa
- Revisão de literatura (sistemática, narrativa ou scoping)
- Capítulo de tese ou dissertação
- Resumo de conferência ou artigo curto

**Escopo de Avaliação:**
- Abrangente (todas as dimensões)
- Direcionado (aspectos específicos como metodologia ou escrita)
- Comparativo (benchmarking contra outro trabalho)

Peça ao usuário para esclarecer se o escopo for ambíguo.

### Etapa 2: Avaliação Baseada em Dimensões

Avalie sistematicamente o trabalho nas dimensões ScholarEval. Para cada dimensão aplicável, avalie qualidade, identifique forças e fraquezas, e forneça pontuações quando apropriado.

Consulte `references/evaluation_framework.md` para critérios detalhados e rubricas para cada dimensão.

**Dimensões de Avaliação Principal:**

1. **Formulação do Problema e Questões de Pesquisa**
   - Clareza e especificidade das questões de pesquisa
   - Significância teórica ou prática
   - Viabilidade e adequação de escopo
   - Novidade e potencial de contribuição

2. **Revisão de Literatura**
   - Abrangência de cobertura
   - Síntese crítica vs. mera sumarização
   - Identificação de lacunas de pesquisa
   - Atualidade e relevância das fontes
   - Contextualização apropriada

3. **Metodologia e Design de Pesquisa**
   - Adequação às questões de pesquisa
   - Rigor e validade
   - Reprodutibilidade e transparência
   - Considerações éticas
   - Reconhecimento de limitações

4. **Coleta de Dados e Fontes**
   - Qualidade e adequação dos dados
   - Tamanho da amostra e representatividade
   - Procedimentos de coleta de dados
   - Credibilidade e confiabilidade das fontes

5. **Análise e Interpretação**
   - Adequação dos métodos analíticos
   - Rigor da análise
   - Coerência lógica
   - Consideração de explicações alternativas
   - Alinhamento resultados-afirmações

6. **Resultados e Achados**
   - Clareza de apresentação
   - Rigor estatístico ou qualitativo
   - Qualidade de visualização
   - Precisão da interpretação
   - Discussão de implicações

7. **Escrita e Apresentação Acadêmica**
   - Clareza e organização
   - Tom e estilo acadêmico
   - Gramática e mecânica
   - Fluxo lógico
   - Acessibilidade ao público-alvo

8. **Citações e Referências**
   - Completude de citações
   - Qualidade e adequação das fontes
   - Precisão de citações
   - Equilíbrio de perspectivas
   - Aderência a padrões de citação

### Etapa 3: Pontuação e Classificação

Para cada dimensão avaliada, forneça:

**Avaliação Qualitativa:**
- Forças principais (2-3 pontos específicos)
- Áreas de melhoria (2-3 pontos específicos)
- Problemas críticos (se houver)

**Pontuação Quantitativa (Opcional):**
Use uma escala de 5 pontos quando aplicável:
- 5: Excelente - Qualidade exemplar, publicável em veículos de topo
- 4: Bom - Qualidade forte com pequenas melhorias necessárias
- 3: Adequado - Qualidade aceitável com áreas notáveis de melhoria
- 2: Precisa de Melhoria - Revisões significativas necessárias
- 1: Deficiente - Problemas fundamentais exigindo revisão maior

Para calcular pontuações agregadas programaticamente, use `scripts/calculate_scores.py`.

### Etapa 4: Sintetizar Avaliação Geral

Forneça um resumo de avaliação integrado:

1. **Avaliação Geral de Qualidade** - Julgamento holístico do mérito acadêmico do trabalho
2. **Forças Principais** - 3-5 forças principais entre dimensões
3. **Fraquezas Críticas** - 3-5 áreas primárias exigindo atenção
4. **Recomendações Prioritárias** - Lista de melhorias classificada por impacto
5. **Prontidão para Publicação** (se aplicável) - Avaliação de adequação a veículos-alvo

### Etapa 5: Fornecer Feedback Acionável

Transforme descobertas de avaliação em feedback construtivo e acionável:

**Estrutura de Feedback:**
- **Específico** - Referencie seções exatas, parágrafos ou números de página
- **Acionável** - Forneça sugestões concretas de melhoria
- **Priorizado** - Classifique recomendações por importância e viabilidade
- **Equilibrado** - Reconheça forças enquanto aborda fraquezas
- **Baseado em Evidências** - Fundamente feedback em critérios de avaliação

**Opções de Formato de Feedback:**
- Relatório estruturado com análise dimensão-por-dimensão
- Comentários anotados mapeados para seções específicas do documento
- Resumo executivo com achados-chave e recomendações
- Análise comparativa contra padrões de benchmark

### Etapa 6: Considerações Contextuais

Ajuste a abordagem de avaliação com base em:

**Estágio de Desenvolvimento:**
- Rascunho inicial: Foco em problemas conceituais e estruturais
- Rascunho avançado: Foco em refinamento e polimento
- Submissão final: Verificação de qualidade abrangente

**Propósito e Veículo:**
- Artigo de journal: Padrões altos para rigor e contribuição
- Artigo de conferência: Balanço entre novidade e clareza de apresentação
- Trabalho estudantil: Feedback educacional com foco no desenvolvimento
- Proposta de bolsa: Ênfase em viabilidade e impacto

**Normas Específicas da Disciplina:**
- Campos STEM: Ênfase em reprodutibilidade e rigor estatístico
- Ciências sociais: Balanço entre padrões quantitativos e qualitativos
- Humanidades: Foco em argumentação e interpretação acadêmica

## Recursos

### references/evaluation_framework.md

Critérios de avaliação detalhados, rubricas e indicadores de qualidade para cada dimensão ScholarEval. Carregue esta referência ao conduzir avaliações para acessar diretrizes de avaliação específicas e rubricas de pontuação.

Padrões de busca para acesso rápido:
- "Critérios de Formulação de Problema"
- "Rubrica de Revisão de Literatura"
- "Avaliação de Metodologia"
- "Indicadores de qualidade de dados"
- "Padrões de rigor de análise"
- "Checklist de qualidade de escrita"

### scripts/calculate_scores.py

Script Python para calcular pontuações de avaliação agregadas a partir de classificações em nível de dimensão. Suporta média ponderada, análise de limiar e visualização de pontuação.

Uso:
```bash
python scripts/calculate_scores.py --scores <dimension_scores.json> --output <report.txt>
```

## Melhores Práticas

1. **Manter Objetividade** - Base as avaliações em critérios estabelecidos, não em preferências pessoais
2. **Ser Abrangente** - Avalie todas as dimensões aplicáveis sistematicamente
3. **Fornecer Evidências** - Apoie avaliações com exemplos específicos do trabalho
4. **Permanecer Construtivo** - Enquadre fraquezas como oportunidades de melhoria
5. **Considerar Contexto** - Ajuste expectativas com base no estágio e propósito do trabalho
6. **Documentar Justificativa** - Explique o raciocínio por trás de avaliações e pontuações
7. **Encorajar Forças** - Reconheça explicitamente o que o trabalho faz bem
8. **Priorizar Feedback** - Foque em melhorias de alto impacto primeiro

## Exemplo de Workflow de Avaliação

**Solicitação do Usuário:** "Avalie este artigo de pesquisa sobre aprendizado de máquina para descoberta de fármacos"

**Processo de Resposta:**
1. Identificar tipo de trabalho (artigo de pesquisa empírica) e escopo (avaliação abrangente)
2. Carregar `references/evaluation_framework.md` para critérios detalhados
3. Avaliar sistematicamente cada dimensão:
   - Formulação do problema: Questão de pesquisa clara sobre desempenho do modelo ML
   - Revisão de literatura: Cobertura abrangente de trabalho recente em ML e descoberta de fármacos
   - Metodologia: Arquitetura de aprendizado profundo apropriada com procedimentos de validação
   - [Continuar através de todas as dimensões...]
4. Calcular pontuações de dimensão e avaliação geral
5. Sintetizar achados em relatório estruturado destacando:
   - Metodologia forte e código reproduzível
   - Precisa de avaliação de dataset mais diversa
   - Escrita poderia melhorar clareza na seção de resultados
6. Fornecer recomendações priorizadas com sugestões específicas

## Integração com Scientific Writer

Esta habilidade integra-se perfeitamente com o workflow scientific writer:

**Após Geração de Artigo:**
- Use Scholar Evaluation como alternativa ou complemento ao peer review
- Gere `SCHOLAR_EVALUATION.md` juntamente com `PEER_REVIEW.md`
- Forneça pontuações quantitativas para rastrear melhoria nas revisões

**Durante Revisão:**
- Re-avalie dimensões específicas após abordar feedback
- Rastreie melhorias de pontuação em múltiplas versões
- Identifique fraquezas persistentes exigindo atenção

**Preparação para Publicação:**
- Avalie prontidão para journal/conferência-alvo
- Identifique lacunas antes de submissão
- Faça benchmarking contra padrões de publicação

## Observações

- O rigor de avaliação deve corresponder ao propósito e estágio do trabalho
- Algumas dimensões podem não se aplicar a todos os tipos de trabalho (ex: coleta de dados para artigos puramente teóricos)
- Diferenças culturais e disciplinares em normas acadêmicas devem ser consideradas
- Este framework complementa, não substitui, expertise específica de domínio
- Use em combinação com habilidade de peer-review para avaliação abrangente

## Citação

Esta habilidade é baseada no framework ScholarEval introduzido em:

**Moussa, H. N., Da Silva, P. Q., Adu-Ampratwum, D., East, A., Lu, Z., Puccetti, N., Xue, M., Sun, H., Majumder, B. P., & Kumar, S. (2025).** _ScholarEval: Research Idea Evaluation Grounded in Literature_. arXiv preprint arXiv:2510.16234. [https://arxiv.org/abs/2510.16234](https://arxiv.org/abs/2510.16234)

**Resumo:** ScholarEval é um framework de avaliação aumentada por recuperação que avalia ideias de pesquisa com base em dois critérios fundamentais: solidez (a validade empírica de métodos propostos baseada em literatura existente) e contribuição (o grau de avanço feito pela ideia em diferentes dimensões em relação à pesquisa anterior). O framework alcança cobertura significativamente maior de pontos de avaliação anotados por especialistas e é consistentemente preferido sobre sistemas baseline em termos de acionabilidade, profundidade e suporte de evidências da avaliação.