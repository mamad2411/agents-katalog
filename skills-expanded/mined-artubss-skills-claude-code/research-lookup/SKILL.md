---
name: research-lookup
description: "Buscar informações de pesquisa atual usando os modelos Sonar Pro Search ou Sonar Reasoning Pro da Perplexity através do OpenRouter. Seleciona automaticamente o melhor modelo com base na complexidade da consulta. Pesquise artigos acadêmicos, estudos recentes, documentação técnica e informações gerais de pesquisa com citações."
allowed-tools: [Read, Write, Edit, Bash]
---

# Busca de Informações de Pesquisa

## Visão Geral

Esta skill permite buscas em tempo real de informações de pesquisa usando os modelos Sonar da Perplexity através do OpenRouter. Ela seleciona inteligentemente entre **Sonar Pro Search** (busca rápida e eficiente) e **Sonar Reasoning Pro** (raciocínio analítico profundo) com base na complexidade da consulta. A skill fornece acesso a literatura acadêmica atual, estudos recentes, documentação técnica e informações gerais de pesquisa com citações apropriadas e atribuição de fontes.

## Quando Usar Esta Skill

Use esta skill quando você precisar:

- **Informações de Pesquisa Atual**: Estudos, artigos e descobertas mais recentes em um campo específico
- **Verificação de Literatura**: Verificar fatos, estatísticas ou afirmações contra pesquisa atual
- **Pesquisa de Contexto**: Reunir contexto e evidência de suporte para redação científica
- **Fontes de Citação**: Encontrar artigos e estudos relevantes para citar em manuscritos
- **Documentação Técnica**: Consultar especificações, protocolos ou metodologias
- **Desenvolvimentos Recentes**: Manter-se atualizado com tendências emergentes e avanços
- **Dados Estatísticos**: Encontrar estatísticas recentes, resultados de pesquisas ou descobertas
- **Opiniões de Especialistas**: Acessar insights de entrevistas recentes, análises ou comentários

## Aprimoramento Visual com Esquemas Científicos

**Ao criar documentos com esta skill, sempre considere adicionar diagramas e esquemas científicos para aprimorar a comunicação visual.**

Se seu documento não contiver esquemas ou diagramas:
- Use a skill **scientific-schematics** para gerar diagramas de qualidade de publicação com IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Para novos documentos:** Esquemas científicos devem ser gerados por padrão para representar visualmente conceitos-chave, fluxos de trabalho, arquiteturas ou relacionamentos descritos no texto.

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "descrição do seu diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade de publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltonismo, alto contraste)
- Salvamento de saídas no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de fluxo de informações de pesquisa
- Ilustrações de fluxo de trabalho de processamento de consultas
- Árvores de decisão de seleção de modelo
- Diagramas de arquitetura de integração de sistema
- Visualizações de pipeline de recuperação de informações
- Frameworks de síntese de conhecimento
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da skill scientific-schematics.

---

## Capacidades Principais

### 1. Consultas de Pesquisa Acadêmica

**Pesquisar Literatura Acadêmica**: Consulte artigos recentes, estudos e análises em domínios específicos:

```
Exemplos de Consulta:
- "Avanços recentes em edição de genes CRISPR 2024"
- "Ensaios clínicos mais recentes para tratamento de Alzheimer"
- "Aplicações de aprendizado de máquina em descoberta de fármacos revisão sistemática"
- "Impactos da mudança climática na biodiversidade meta-análise"
```

**Formato de Resposta Esperado**:
- Resumo dos principais achados da literatura recente
- Citação de 3-5 artigos mais relevantes com autores, títulos, periódicos e anos
- Estatísticas ou achados-chave destacados
- Identificação de lacunas de pesquisa ou controvérsias
- Links para artigos completos quando disponível

### 2. Informações Técnicas e Metodológicas

**Buscas de Protocolo e Método**: Encontre procedimentos detalhados, especificações e metodologias:

```
Exemplos de Consulta:
- "Protocolo de Western blot para detecção de proteínas"
- "Métodos de preparação de biblioteca de sequenciamento de RNA"
- "Análise de poder estatístico para ensaios clínicos"
- "Métricas de avaliação de modelos de aprendizado de máquina"
```

**Formato de Resposta Esperado**:
- Procedimentos ou protocolos passo a passo
- Materiais e equipamento necessários
- Parâmetros críticos e considerações
- Solução de problemas comuns
- Referências a protocolos padrão ou artigos seminais

### 3. Informações Estatísticas e de Dados

**Estatísticas de Pesquisa**: Consulte estatísticas atuais, resultados de pesquisas e dados de pesquisa:

```
Exemplos de Consulta:
- "Prevalência de diabetes na população dos EUA 2024"
- "Estatísticas globais de adoção de energia renovável"
- "Taxas de vacinação COVID-19 por país"
- "Pesquisa de adoção de IA no setor de saúde"
```

**Formato de Resposta Esperado**:
- Estatísticas atuais com datas e fontes
- Metodologia de coleta de dados
- Intervalos de confiança ou margens de erro quando disponível
- Comparação com anos anteriores ou benchmarks
- Citações de pesquisas ou estudos originais

### 4. Assistência de Citação e Referência

**Localização de Citação**: Localize artigos e estudos relevantes para citação em manuscritos:

```
Exemplos de Consulta:
- "Artigos fundamentais sobre arquitetura transformer"
- "Trabalhos seminais em computação quântica"
- "Estudos-chave sobre mitigação da mudança climática"
- "Ensaios históricos em imunoterapia do câncer"
```

**Formato de Resposta Esperado**:
- 5-10 artigos mais influentes ou relevantes
- Informações bibliográficas completas (autores, título, periódico, ano, DOI)
- Breve descrição da contribuição de cada artigo
- Métricas de impacto de citação quando disponível (h-index, contagem de citações)
- Fatores de impacto de periódicos e rankings

## Seleção Automática de Modelo

Esta skill possui **seleção inteligente de modelo** com base na complexidade da consulta:

### Tipos de Modelo

**1. Sonar Pro Search** (`perplexity/sonar-pro-search`)
- **Caso de Uso**: Busca de informações simples e direta
- **Melhor Para**: 
  - Consultas de busca simples de fatos
  - Pesquisas de publicação recente
  - Buscas básicas de protocolo
  - Recuperação de dados estatísticos
- **Velocidade**: Respostas rápidas
- **Custo**: Menor custo por consulta

**2. Sonar Reasoning Pro** (`perplexity/sonar-reasoning-pro`)
- **Caso de Uso**: Consultas analíticas complexas que requerem raciocínio profundo
- **Melhor Para**:
  - Análise comparativa ("comparar X vs Y")
  - Síntese de múltiplos estudos
  - Avaliação de trade-offs ou controvérsias
  - Explicação de mecanismos ou relacionamentos
  - Análise crítica e interpretação
- **Velocidade**: Mais lenta, mas mais completa
- **Custo**: Maior custo por consulta, mas fornece insights mais profundos

### Avaliação de Complexidade

A skill detecta automaticamente a complexidade da consulta usando estes indicadores:

**Palavras-chave de Raciocínio** (ativa Sonar Reasoning Pro):
- Analítica: `comparar`, `contrastar`, `analisar`, `análise`, `avaliar`, `criticar`
- Comparativa: `versus`, `vs`, `vs.`, `comparado a`, `diferenças entre`, `similaridades`
- Síntese: `meta-análise`, `revisão sistemática`, `síntese`, `integrar`
- Causal: `mecanismo`, `por que`, `como funciona`, `explicar`, `relacionamento`, `relacionamento causal`, `mecanismo subjacente`
- Teórica: `framework teórico`, `implicações`, `interpretar`, `raciocínio`
- Debate: `controvérsia`, `conflitante`, `paradoxo`, `debate`, `conciliar`
- Trade-offs: `prós e contras`, `vantagens e desvantagens`, `trade-off`, `tradeoff`, `trade offs`
- Complexidade: `multifacetado`, `interação complexa`, `análise crítica`

**Pontuação de Complexidade**:
- Palavras-chave de raciocínio: 3 pontos cada (ponderação alta)
- Múltiplas perguntas: 2 pontos por marca de interrogação
- Estruturas de sentença complexas: 1,5 pontos por indicador de cláusula (e, ou, mas, porém, enquanto, embora)
- Consultas muito longas: 1 ponto se >150 caracteres
- **Limite**: Consultas com pontuação ≥3 acionam Sonar Reasoning Pro

**Resultado Prático**: Até uma única palavra-chave de raciocínio forte (comparar, explicar, analisar, etc.) acionará o modelo Sonar Reasoning Pro mais poderoso, garantindo que você obtenha análise profunda quando necessário.

**Exemplo de Classificação de Consulta**:

✅ **Sonar Pro Search** (busca simples):
- "Avanços recentes em edição de genes CRISPR 2024"
- "Prevalência de diabetes na população dos EUA"
- "Protocolo de Western blot para detecção de proteínas"

✅ **Sonar Reasoning Pro** (análise complexa):
- "Comparar e contrastar vacinas de mRNA vs vacinas tradicionais para tratamento de câncer"
- "Explicar o mecanismo subjacente do relacionamento entre microbioma intestinal e depressão"
- "Analisar a controvérsia em torno de IA no diagnóstico médico e avaliar trade-offs"

### Substituição Manual

Você pode forçar um modelo específico usando o parâmetro `force_model`:

```python
# Forçar Sonar Pro Search para busca rápida
research = ResearchLookup(force_model='pro')

# Forçar Sonar Reasoning Pro para análise profunda
research = ResearchLookup(force_model='reasoning')

# Seleção automática (padrão)
research = ResearchLookup()
```

Uso de linha de comando:
```bash
# Forçar Sonar Pro Search
python research_lookup.py "sua consulta" --force-model pro

# Forçar Sonar Reasoning Pro
python research_lookup.py "sua consulta" --force-model reasoning

# Automático (sem flag)
python research_lookup.py "sua consulta"
```

## Integração Técnica

### Configuração da API OpenRouter

Esta skill integra-se com OpenRouter (openrouter.ai) para acessar os modelos Sonar da Perplexity:

**Especificações do Modelo**:
- **Modelos**: 
  - `perplexity/sonar-pro-search` (busca rápida)
  - `perplexity/sonar-reasoning-pro-online` (análise profunda)
- **Modo de Busca**: Modo acadêmico/acadêmico (prioriza fontes revisadas por pares)
- **Contexto de Busca**: Sempre usa contexto de busca `alto` para resultados de pesquisa mais aprofundados e abrangentes
- **Janela de Contexto**: 200K+ tokens para pesquisa abrangente
- **Capacidades**: Busca de artigos acadêmicos, geração de citações, análise acadêmica
- **Saída**: Respostas ricas com citações e links de fonte de bases de dados acadêmicas

**Requisitos de API**:
- Chave de API OpenRouter (defina como variável de ambiente `OPENROUTER_API_KEY`)
- Conta com créditos suficientes para consultas de pesquisa
- Atribuição e citação apropriadas de fontes

**Configuração de Modo Acadêmico**:
- Mensagem do sistema configurada para priorizar fontes acadêmicas
- Busca focada em periódicos e publicações revisadas por pares
- Extração aprimorada de citações para referências acadêmicas
- Preferência por literatura acadêmica recente (2020-2024)
- Acesso direto a bases de dados e repositórios acadêmicos

### Qualidade e Confiabilidade de Resposta

**Verificação de Fonte**: A skill prioriza:
- Artigos e periódicos acadêmicos revisados por pares
- Fontes institucionais respeitáveis (universidades, agências governamentais, ONGs)
- Publicações recentes (2-3 anos é o preferido)
- Periódicos e conferências de alto impacto
- Pesquisa primária sobre fontes secundárias

**Padrões de Citação**: Todas as respostas incluem:
- Informações bibliográficas completas
- DOI ou URLs estáveis quando disponível
- Datas de acesso para fontes web
- Atribuição clara de citações diretas ou dados

## Melhores Práticas de Consulta

### 1. Estratégia de Seleção de Modelo

**Para Buscas Simples (Sonar Pro Search)**:
- Artigos recentes sobre um tópico específico
- Dados estatísticos ou taxas de prevalência
- Protocolos ou metodologias padrão
- Localização de citação para artigos específicos
- Recuperação de informações factuais

**Para Análise Complexa (Sonar Reasoning Pro)**:
- Estudos comparativos e síntese
- Explicações de mecanismo
- Avaliação de controvérsia
- Análise de trade-off
- Frameworks teóricos
- Relacionamentos multifacetados

**Dica Profissional**: A seleção automática é otimizada para a maioria dos casos. Use `force_model` apenas se você tiver requisitos específicos ou souber que a consulta precisa de raciocínio mais profundo do que o detectado.

### 2. Consultas Específicas e Focadas

**Boas Consultas** (acionarão modelo apropriado):
- "Ensaios clínicos randomizados de vacinas de mRNA para tratamento de câncer 2023-2024" → Sonar Pro Search
- "Comparar a eficácia e segurança de vacinas de mRNA vs vacinas tradicionais para tratamento de câncer" → Sonar Reasoning Pro
- "Explicar o mecanismo por qual efeitos off-target de CRISPR ocorrem e estratégias para minimizá-los" → Sonar Reasoning Pro

**Consultas Ruins**:
- "Conte-me sobre IA" (muito amplo)
- "Pesquisa sobre câncer" (falta especificidade)
- "Notícias recentes" (muito vago)

### 3. Formato de Consulta Estruturado

**Estrutura Recomendada**:
```
[Tópico] + [Aspecto Específico] + [Período] + [Tipo de Informação]
```

**Exemplos**:
- "Edição de genes CRISPR + efeitos off-target + 2024 + ensaios clínicos"
- "Computação quântica + correção de erro + avanços recentes + artigos de análise"
- "Energia renovável + eficiência solar + 2023-2024 + dados estatísticos"

### 4. Consultas de Acompanhamento

**Acompanhamentos Eficazes**:
- "Mostre-me a citação completa para o artigo Smith et al. 2024"
- "Quais são as limitações desta metodologia?"
- "Encontre estudos similares usando abordagens diferentes"
- "Que controvérsias existem nesta área de pesquisa?"

## Integração com Redação Científica

Esta skill aprimora a redação científica fornecendo:

1. **Suporte a Revisão de Literatura**: Reúna pesquisa atual para seções de introdução e discussão
2. **Validação de Métodos**: Verifique protocolos e procedimentos contra padrões atuais
3. **Contextualização de Resultados**: Compare achados com estudos recentes similares
4. **Aprimoramento de Discussão**: Apoie argumentos com evidência mais recente
5. **Gerenciamento de Citação**: Forneça citações corretamente formatadas em múltiplos estilos

## Tratamento de Erro e Limitações

**Limitações Conhecidas**:
- Corte de informação: Respostas limitadas aos dados de treinamento (típicamente 2023-2024)
- Conteúdo por assinatura: Pode não acessar texto completo atrás de paywalls
- Pesquisa emergente: Pode perder artigos muito recentes ainda não indexados
- Bases de dados especializadas: Não pode acessar bases de dados proprietárias ou restritas

**Condições de Erro**:
- Limites de taxa de API ou cota excedida
- Problemas de conectividade de rede
- Consultas malformadas ou ambíguas
- Indisponibilidade ou manutenção do modelo

**Estratégias de Fallback**:
- Reformule consultas para maior clareza
- Divida consultas complexas em componentes mais simples
- Use períodos de tempo mais amplos se dados recentes indisponíveis
- Referência cruzada com múltiplas variações de consulta

## Exemplos de Uso

### Exemplo 1: Busca Simples de Literatura (Sonar Pro Search)

**Consulta**: "Avanços recentes em mecanismos de atenção transformer 2024"

**Modelo Selecionado**: Sonar Pro Search (busca simples)

**Resposta Inclui**:
- Resumo de 5 artigos-chave de 2024
- Citações completas com DOIs
- Inovações e melhorias-chave
- Benchmarks de desempenho
- Direções de pesquisa futura

### Exemplo 2: Análise Comparativa (Sonar Reasoning Pro)

**Consulta**: "Comparar e contrastar as vantagens e limitações de modelos baseados em transformer versus RNNs tradicionais para modelagem sequencial"

**Modelo Selecionado**: Sonar Reasoning Pro (análise complexa necessária)

**Resposta Inclui**:
- Comparação detalhada através de múltiplas dimensões
- Análise de diferenças arquitetônicas
- Trade-offs em eficiência computacional vs desempenho
- Recomendações de caso de uso
- Síntese de evidência de múltiplos estudos
- Discussão de debates em andamento no campo

### Exemplo 3: Verificação de Método (Sonar Pro Search)

**Consulta**: "Protocolos padrão para análise de citometria de fluxo"

**Modelo Selecionado**: Sonar Pro Search (busca de protocolo)

**Resposta Inclui**:
- Protocolo passo a passo de análise recente
- Controles e calibrações necessários
- Armadilhas comuns e solução de problemas
- Referência a artigo de metodologia definitiva
- Abordagens alternativas com prós/contras

### Exemplo 4: Explicação de Mecanismo (Sonar Reasoning Pro)

**Consulta**: "Explicar o mecanismo subjacente de como vacinas de mRNA acionam respostas imunológicas e por que diferem de vacinas tradicionais"

**Modelo Selecionado**: Sonar Reasoning Pro (requer raciocínio causal)

**Resposta Inclui**:
- Explicação mecânica detalhada
- Processos biológicos passo a passo
- Análise comparativa com vacinas tradicionais
- Interações a nível molecular
- Integração de conceitos de imunologia e farmacologia
- Evidência de pesquisa recente

### Exemplo 5: Dados Estatísticos (Sonar Pro Search)

**Consulta**: "Estatísticas globais de adoção de IA em saúde 2024"

**Modelo Selecionado**: Sonar Pro Search (busca de dados)

**Resposta Inclui**:
- Taxas atuais de adoção por região
- Tamanho de mercado e projeções de crescimento
- Metodologia de pesquisa e tamanho de amostra
- Comparação com anos anteriores
- Citações de relatórios de pesquisa de mercado

## Considerações de Desempenho e Custo

### Tempos de Resposta

**Sonar Pro Search**:
- Tempo de resposta típico: 5-15 segundos
- Melhor para coleta rápida de informação
- Adequado para consultas em lote

**Sonar Reasoning Pro**:
- Tempo de resposta típico: 15-45 segundos
- Vale a espera para consultas analíticas complexas
- Fornece raciocínio e síntese mais completos

### Otimização de Custo

**Benefícios de Seleção Automática**:
- Economiza custos usando Sonar Pro Search para consultas simples
- Reserva Sonar Reasoning Pro para consultas que verdadeiramente se beneficiam de análise mais profunda
- Otimiza o balanço entre custo e qualidade

**Casos de Substituição Manual**:
- Forçar Sonar Pro Search quando o orçamento é limitado e velocidade é prioridade
- Forçar Sonar Reasoning Pro ao trabalhar em pesquisa crítica que requer profundidade máxima
- Usar para seções específicas de artigos (ex: Pro Search para métodos, Reasoning para discussão)

**Melhores Práticas**:
1. Confie na seleção automática para a maioria dos casos
2. Revise os resultados da consulta - se Sonar Pro Search não fornecer profundidade suficiente, reformule com palavras-chave de raciocínio
3. Use consultas em lote estrategicamente - combine buscas simples para minimizar contagem total de consulta
4. Para análises de literatura, comece com Sonar Pro Search para amplitude, depois use Sonar Reasoning Pro para síntese

## Considerações de Segurança e Ética

**Uso Responsável**:
- Verifique todas as informações contra fontes primárias quando possível
- Atribua claramente todos os dados e citações a fontes originais
- Evite apresentar resumos gerados por IA como pesquisa original
- Respeite restrições de copyright e licenciamento
- Use para assistência em pesquisa, não para contornar paywalls ou assinaturas

**Integridade Acadêmica**:
- Sempre cite fontes originais, não a ferramenta de IA
- Use como ponto de partida para buscas de literatura
- Siga diretrizes institucionais para uso de ferramentas de IA
- Mantenha transparência sobre métodos de pesquisa

## Ferramentas Complementares

Além de research-lookup, o redator científico tem acesso a **WebSearch** para:

- **Verificação rápida de metadados**: Consulte DOIs, anos de publicação, nomes de periódicos, volume/número de página
- **Fontes não-acadêmicas**: Notícias, blogs, documentação técnica, eventos atuais
- **Informações gerais**: Informações da empresa, detalhes do produto, estatísticas atuais
- **Referência cruzada**: Verifique detalhes de citação encontrados através de research-lookup

**Quando usar qual ferramenta:**
| Tarefa | Ferramenta |
|--------|-----------|
| Encontrar artigos acadêmicos | research-lookup |
| Busca de literatura | research-lookup |
| Análise profunda/comparação | research-lookup (Sonar Reasoning Pro) |
| Consultar DOI/metadados | WebSearch |
| Verificar ano de publicação | WebSearch |
| Encontrar volume/páginas de periódico | WebSearch |
| Eventos atuais/notícias | WebSearch |
| Fontes não-acadêmicas | WebSearch |

## Resumo

Esta skill funciona como um assistente de pesquisa poderoso com seleção inteligente de modelo dual:

- **Inteligência Automática**: Analisa a complexidade da consulta e seleciona o modelo ideal (Sonar Pro Search ou Sonar Reasoning Pro)
- **Custo-Efetivo**: Usa Sonar Pro Search mais rápido e barato para buscas simples
- **Análise Profunda**: Ativa automaticamente Sonar Reasoning Pro para consultas comparativas, analíticas e teóricas complexas
- **Controle Flexível**: Substituição manual disponível quando você sabe exatamente que nível de análise precisa
- **Foco Acadêmico**: Ambos os modelos configurados para priorizar literatura revisada por pares e acadêmica
- **WebSearch Complementar**: Use junto com WebSearch para verificação de metadados e fontes não-acadêmicas

Seja você precisando de localização rápida de fatos ou síntese analítica profunda, esta skill se adapta automaticamente para fornecer o nível certo de suporte de pesquisa para suas necessidades de redação científica.