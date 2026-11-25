---
name: prompt-engineering-patterns
description: "Domine técnicas avançadas de engenharia de prompts para maximizar o desempenho, confiabilidade e controlabilidade de modelos de linguagem."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Padrões de Engenharia de Prompts

Domine técnicas avançadas de engenharia de prompts para maximizar o desempenho, confiabilidade e controlabilidade de modelos de linguagem.

## Não use esta competência quando

- A tarefa não está relacionada a padrões de engenharia de prompts
- Você precisa de um domínio ou ferramenta diferente fora deste escopo

## Instruções

- Esclareça objetivos, restrições e inputs necessários.
- Aplique as melhores práticas relevantes e valide resultados.
- Forneça passos acionáveis e verificação.
- Se exemplos detalhados forem necessários, abra `resources/implementation-playbook.md`.

## Use esta competência quando

- Projetando prompts complexos para aplicações LLM em produção
- Otimizando desempenho e consistência de prompts
- Implementando padrões de raciocínio estruturado (chain-of-thought, tree-of-thought)
- Construindo sistemas few-shot learning com seleção dinâmica de exemplos
- Criando templates de prompts reutilizáveis com interpolação de variáveis
- Depurando e refinando prompts que produzem outputs inconsistentes
- Implementando system prompts para assistentes de IA especializados

## Capacidades Principais

### 1. Few-Shot Learning
- Estratégias de seleção de exemplos (similaridade semântica, amostragem de diversidade)
- Equilibrando quantidade de exemplos com restrições de janela de contexto
- Construindo demonstrações eficazes com pares input-output
- Recuperação dinâmica de exemplos de bases de conhecimento
- Tratamento de casos extremos por meio de seleção estratégica de exemplos

### 2. Chain-of-Thought Prompting
- Elicitação de raciocínio passo a passo
- Zero-shot CoT com "Let's think step by step"
- Few-shot CoT com rastros de raciocínio
- Técnicas de auto-consistência (amostragem de múltiplos caminhos de raciocínio)
- Etapas de verificação e validação

### 3. Otimização de Prompts
- Fluxos de refinamento iterativo
- Testes A/B de variações de prompts
- Medição de métricas de desempenho de prompts (acurácia, consistência, latência)
- Redução de uso de tokens mantendo qualidade
- Tratamento de casos extremos e modos de falha

### 4. Sistemas de Template
- Interpolação de variáveis e formatação
- Seções de prompt condicionais
- Templates de conversas multi-turno
- Composição de prompts baseada em papéis
- Componentes modulares de prompts

### 5. Design de System Prompt
- Definição de comportamento e restrições do modelo
- Definição de formatos e estrutura de output
- Estabelecimento de papel e expertise
- Diretrizes de segurança e políticas de conteúdo
- Definição de contexto e informações de background

## Início Rápido

```python
from prompt_optimizer import PromptTemplate, FewShotSelector

# Define a structured prompt template
template = PromptTemplate(
    system="You are an expert SQL developer. Generate efficient, secure SQL queries.",
    instruction="Convert the following natural language query to SQL:\n{query}",
    few_shot_examples=True,
    output_format="SQL code block with explanatory comments"
)

# Configure few-shot learning
selector = FewShotSelector(
    examples_db="sql_examples.jsonl",
    selection_strategy="semantic_similarity",
    max_examples=3
)

# Generate optimized prompt
prompt = template.render(
    query="Find all users who registered in the last 30 days",
    examples=selector.select(query="user registration date filter")
)
```

## Padrões-Chave

### Progressive Disclosure (Divulgação Progressiva)
Comece com prompts simples, adicione complexidade apenas quando necessário:

1. **Nível 1**: Instrução direta
   - "Resuma este artigo"

2. **Nível 2**: Adicione restrições
   - "Resuma este artigo em 3 tópicos, focando em descobertas principais"

3. **Nível 3**: Adicione raciocínio
   - "Leia este artigo, identifique as descobertas principais, depois resuma em 3 tópicos"

4. **Nível 4**: Adicione exemplos
   - Inclua 2-3 resumos exemplo com pares input-output

### Hierarquia de Instruções
```
[System Context] → [Task Instruction] → [Examples] → [Input Data] → [Output Format]
```

### Recuperação de Erros
Construa prompts que tratam falhas graciosamente:
- Inclua instruções de fallback
- Solicite scores de confiança
- Peça interpretações alternativas quando incerto
- Especifique como indicar informações faltantes

## Melhores Práticas

1. **Seja Específico**: Prompts vagos produzem resultados inconsistentes
2. **Mostre, Não Conte**: Exemplos são mais eficazes que descrições
3. **Teste Extensivamente**: Avalie em inputs diversos e representativos
4. **Itere Rapidamente**: Pequenas mudanças podem ter impactos grandes
5. **Monitore Desempenho**: Rastreie métricas em produção
6. **Controle de Versão**: Trate prompts como código com versionamento adequado
7. **Documente Intenção**: Explique por que prompts são estruturados de determinada forma

## Armadilhas Comuns

- **Over-engineering**: Começar com prompts complexos antes de tentar os simples
- **Poluição de exemplos**: Usar exemplos que não correspondem à tarefa alvo
- **Overflow de contexto**: Exceder limites de tokens com exemplos excessivos
- **Instruções ambíguas**: Deixar espaço para múltiplas interpretações
- **Ignorar casos extremos**: Não testar em inputs incomuns ou limítrofes

## Padrões de Integração

### Com Sistemas RAG
```python
# Combine retrieved context with prompt engineering
prompt = f"""Given the following context:
{retrieved_context}

{few_shot_examples}

Question: {user_question}

Provide a detailed answer based solely on the context above. If the context doesn't contain enough information, explicitly state what's missing."""
```

### Com Validação
```python
# Add self-verification step
prompt = f"""{main_task_prompt}

After generating your response, verify it meets these criteria:
1. Answers the question directly
2. Uses only information from provided context
3. Cites specific sources
4. Acknowledges any uncertainty

If verification fails, revise your response."""
```

## Otimização de Desempenho

### Eficiência de Tokens
- Remova palavras e frases redundantes
- Use abreviações consistentemente após primeira definição
- Consolide instruções similares
- Mova conteúdo estável para system prompts

### Redução de Latência
- Minimize comprimento do prompt sem sacrificar qualidade
- Use streaming para outputs de formato longo
- Cache prefixos de prompts comuns
- Batch requisições similares quando possível

## Recursos

- **references/few-shot-learning.md**: Análise profunda em seleção e construção de exemplos
- **references/chain-of-thought.md**: Técnicas avançadas de elicitação de raciocínio
- **references/prompt-optimization.md**: Fluxos de refinamento sistemático
- **references/prompt-templates.md**: Padrões de templates reutilizáveis
- **references/system-prompts.md**: Design de prompts em nível de sistema
- **assets/prompt-template-library.md**: Templates de prompts já testados em produção
- **assets/few-shot-examples.json**: Datasets de exemplos curados
- **scripts/optimize-prompt.py**: Ferramenta de otimização de prompts automatizada

## Métricas de Sucesso

Rastreie estes KPIs para seus prompts:
- **Acurácia**: Correção dos outputs
- **Consistência**: Reprodutibilidade entre inputs similares
- **Latência**: Tempo de resposta (P50, P95, P99)
- **Uso de Tokens**: Tokens médios por requisição
- **Taxa de Sucesso**: Percentual de outputs válidos
- **Satisfação do Usuário**: Avaliações e feedback

## Próximos Passos

1. Revise a biblioteca de templates de prompts para padrões comuns
2. Experimente few-shot learning para seu caso de uso específico
3. Implemente versionamento de prompts e testes A/B
4. Configure pipelines de avaliação automatizados
5. Documente suas decisões e aprendizados em engenharia de prompts