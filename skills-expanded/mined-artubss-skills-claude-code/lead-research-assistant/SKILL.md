---
name: lead-research-assistant
description: Identifica leads de alta qualidade para seu produto ou serviço analisando seu negócio, pesquisando empresas-alvo e fornecendo estratégias de contato acionáveis. Perfeito para profissionais de vendas, desenvolvimento de negócios e marketing.
---

# Assistente de Pesquisa de Leads

Esta skill ajuda você a identificar e qualificar leads em potencial para seu negócio analisando seu produto/serviço, compreendendo seu perfil ideal de cliente e fornecendo estratégias de contato acionáveis.

## Quando Usar Esta Skill

- Encontrar clientes ou prospects em potencial para seu produto/serviço
- Construir uma lista de empresas para alcançar parcerias
- Identificar contas-alvo para outreach de vendas
- Pesquisar empresas que correspondem ao seu perfil ideal de cliente
- Preparar-se para atividades de desenvolvimento de negócios

## O Que Esta Skill Faz

1. **Compreende Seu Negócio**: Analisa seu produto/serviço, proposta de valor e mercado-alvo
2. **Identifica Empresas-Alvo**: Encontra empresas que correspondem ao seu perfil ideal de cliente com base em:
   - Setor e indústria
   - Tamanho da empresa e localização
   - Stack de tecnologia e ferramentas utilizadas
   - Estágio de crescimento e financiamento
   - Dores que seu produto resolve
3. **Prioriza Leads**: Classifica empresas por score de ajuste e relevância
4. **Fornece Estratégias de Contato**: Sugere como abordar cada lead com mensagens personalizadas
5. **Enriquece Dados**: Coleta informações relevantes sobre tomadores de decisão e contexto da empresa

## Como Usar

### Uso Básico

Simplesmente descreva seu produto/serviço e o que você está procurando:

```
I'm building [product description]. Find me 10 companies in [location/industry] 
that would be good leads for this.
```

### Com Seu Codebase

Para resultados ainda melhores, execute isto a partir do diretório de código-fonte do seu produto:

```
Look at what I'm building in this repository and identify the top 10 companies 
in [location/industry] that would benefit from this product.
```

### Uso Avançado

Para pesquisa mais direcionada:

```
My product: [description]
Ideal customer profile:
- Industry: [industry]
- Company size: [size range]
- Location: [location]
- Current pain points: [pain points]
- Technologies they use: [tech stack]

Find me 20 qualified leads with contact strategies for each.
```

## Instruções

Quando um usuário solicita pesquisa de leads:

1. **Compreenda o Produto/Serviço**
   - Se em um diretório de código, analise o codebase para entender o produto
   - Faça perguntas esclarecedoras sobre a proposta de valor
   - Identifique recursos e benefícios-chave
   - Compreenda quais problemas ele resolve

2. **Defina o Perfil Ideal de Cliente**
   - Determine indústrias e setores-alvo
   - Identifique faixas de tamanho de empresa
   - Considere preferências geográficas
   - Compreenda dores relevantes
   - Anote requisitos tecnológicos

3. **Pesquise e Identifique Leads**
   - Procure por empresas que correspondem aos critérios
   - Procure por sinais de necessidade (postagens de emprego, stack tecnológico, notícias recentes)
   - Considere indicadores de crescimento (financiamento, expansão, contratações)
   - Identifique empresas com produtos/serviços complementares
   - Verifique indicadores de orçamento

4. **Priorize e Classifique**
   - Crie um score de ajuste (1-10) para cada lead
   - Considere fatores como:
     - Alinhamento com ICP
     - Sinais de necessidade imediata
     - Disponibilidade de orçamento
     - Paisagem competitiva
     - Indicadores de timing

5. **Forneça Output Acionável**
   
   Para cada lead, forneça:
   - **Nome da Empresa** e website
   - **Por Que É Um Bom Ajuste**: Razões específicas baseadas em seu negócio
   - **Score de Prioridade**: 1-10 com explicação
   - **Tomador de Decisão**: Papel/título a alcançar (ex: "VP de Engenharia")
   - **Estratégia de Contato**: Sugestões de abordagem personalizadas
   - **Proposta de Valor**: Como seu produto resolve o problema específico deles
   - **Inicializadores de Conversa**: Pontos específicos para mencionar no outreach
   - **URL do LinkedIn**: Se disponível, para conexão fácil

6. **Formate o Output**

   Apresente resultados em formato claro e facilmente digitalizável:

   ```markdown
   # Resultados da Pesquisa de Leads
   
   ## Resumo
   - Total de leads encontrados: [X]
   - Alta prioridade (8-10): [X]
   - Média prioridade (5-7): [X]
   - Score de ajuste médio: [X]
   
   ---
   
   ## Lead 1: [Nome da Empresa]
   
   **Website**: [URL]
   **Score de Prioridade**: [X/10]
   **Setor**: [Setor]
   **Tamanho**: [Contagem de funcionários/faixa de receita]
   
   **Por Que É Um Bom Ajuste**:
   [2-3 razões específicas baseadas em seu negócio]
   
   **Tomador de Decisão-Alvo**: [Papel/Título]
   **LinkedIn**: [URL se disponível]
   
   **Proposta de Valor para Eles**:
   [Benefício específico para esta empresa]
   
   **Estratégia de Outreach**:
   [Abordagem personalizada - mencione dores específicas, notícias recentes da empresa ou contexto relevante]
   
   **Inicializadores de Conversa**:
   - [Ponto específico 1]
   - [Ponto específico 2]
   
   ---
   
   [Repita para cada lead]
   ```

7. **Ofereça Próximos Passos**
   - Sugira salvar resultados em CSV para importação de CRM
   - Ofereça-se para redigir mensagens de outreach personalizadas
   - Recomende priorização baseada em timing
   - Sugira pesquisa de acompanhamento para leads principais

## Exemplos

### Exemplo 1: Do Newsletter do Lenny

**Usuário**: "Estou construindo uma ferramenta que mascara dados sensíveis em queries de assistentes de codificação com IA. Encontre leads em potencial."

**Output**: Cria uma lista priorizada de empresas que:
- Usam assistentes de codificação com IA (Copilot, Cursor, etc.)
- Lidam com dados sensíveis (fintech, healthcare, legal)
- Têm evidência em seus repositórios GitHub de usar agentes de codificação
- Podem ter exposto acidentalmente dados sensíveis em código
- Inclui URLs do LinkedIn de tomadores de decisão relevantes

### Exemplo 2: Negócio Local

**Usuário**: "Executo uma prática de consultoria para produtividade de equipes remotas. Encontre 10 empresas na Bay Area que recentemente ficaram remotas."

**Output**: Identifica empresas que:
- Postaram recentemente listagens de emprego remoto
- Anunciaram políticas remote-first
- Estão contratando equipes distribuídas
- Mostram sinais de desafios de trabalho remoto
- Fornece estratégias de outreach personalizadas para cada uma

## Dicas para Melhores Resultados

- **Seja específico** sobre seu produto e seu valor único
- **Execute a partir do seu codebase** se aplicável para contexto automático
- **Forneça contexto** sobre seu perfil ideal de cliente
- **Especifique restrições** como setor, localização ou tamanho de empresa
- **Solicite pesquisa de acompanhamento** em leads promissores para insights mais profundos

## Casos de Uso Relacionados

- Redigir emails de outreach personalizados após identificar leads
- Construir um CSV pronto para CRM de prospects qualificados
- Pesquisar empresas específicas em detalhes
- Analisar bases de clientes de competidores
- Identificar oportunidades de parceria