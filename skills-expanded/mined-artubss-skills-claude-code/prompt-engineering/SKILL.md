---
name: prompt-engineering
description: Guia especializado em padrões de engenharia de prompts, melhores práticas e técnicas de otimização. Use quando o usuário quer melhorar prompts, aprender estratégias de prompting ou depurar comportamento de agentes.
---

# Padrões de Engenharia de Prompts

Técnicas avançadas de engenharia de prompts para maximizar desempenho, confiabilidade e controlabilidade de LLMs.

## Capacidades Centrais

### 1. Aprendizado com Poucos Exemplos (Few-Shot Learning)

Ensine o modelo mostrando exemplos em vez de explicar regras. Inclua 2-5 pares entrada-saída que demonstrem o comportamento desejado. Use quando você precisa de formatação consistente, padrões de raciocínio específicos ou tratamento de casos extremos. Mais exemplos melhoram a precisão, mas consomem tokens—equilibre com base na complexidade da tarefa.

**Exemplo:**

```markdown
Extract key information from support tickets:

Input: "My login doesn't work and I keep getting error 403"
Output: {"issue": "authentication", "error_code": "403", "priority": "high"}

Input: "Feature request: add dark mode to settings"
Output: {"issue": "feature_request", "error_code": null, "priority": "low"}

Now process: "Can't upload files larger than 10MB, getting timeout"
```

### 2. Prompting com Cadeia de Pensamento (Chain-of-Thought)

Solicite raciocínio passo a passo antes da resposta final. Adicione "Vamos pensar passo a passo" (zero-shot) ou inclua exemplos de traços de raciocínio (few-shot). Use para problemas complexos que exigem lógica de múltiplas etapas, raciocínio matemático, ou quando você precisa verificar o processo de pensamento do modelo. Melhora a precisão em tarefas analíticas em 30-50%.

**Exemplo:**

```markdown
Analyze this bug report and determine root cause.

Think step by step:

1. What is the expected behavior?
2. What is the actual behavior?
3. What changed recently that could cause this?
4. What components are involved?
5. What is the most likely root cause?

Bug: "Users can't save drafts after the cache update deployed yesterday"
```

### 3. Otimização de Prompts

Melhore prompts sistematicamente através de testes e refinamento. Comece simples, meça desempenho (precisão, consistência, uso de tokens), depois itere. Teste em entradas diversas incluindo casos extremos. Use testes A/B para comparar variações. Crítico para prompts em produção onde consistência e custo importam.

**Exemplo:**

```markdown
Versão 1 (Simples): "Resuma este artigo"
→ Resultado: Comprimento inconsistente, perde pontos-chave

Versão 2 (Adicione restrições): "Resuma em 3 pontos"
→ Resultado: Melhor estrutura, mas ainda perde nuances

Versão 3 (Adicione raciocínio): "Identifique os 3 principais achados, depois resuma cada um"
→ Resultado: Consistente, preciso, captura informações-chave
```

### 4. Sistemas de Templates

Construa estruturas de prompts reutilizáveis com variáveis, seções condicionais e componentes modulares. Use para conversas multi-turno, interações baseadas em função, ou quando o mesmo padrão se aplica a entradas diferentes. Reduz duplicação e garante consistência entre tarefas similares.

**Exemplo:**

```python
# Reusable code review template
template = """
Review this {language} code for {focus_area}.

Code:
{code_block}

Provide feedback on:
{checklist}
"""

# Usage
prompt = template.format(
    language="Python",
    focus_area="security vulnerabilities",
    code_block=user_code,
    checklist="1. SQL injection\n2. XSS risks\n3. Authentication"
)
```

### 5. Design de System Prompt

Defina comportamento global e restrições que persistem pela conversa. Configure o papel do modelo, nível de expertise, formato de saída e diretrizes de segurança. Use system prompts para instruções estáveis que não devem mudar de turno a turno, liberando tokens de mensagem de usuário para conteúdo variável.

**Exemplo:**

```markdown
System: You are a senior backend engineer specializing in API design.

Rules:

- Always consider scalability and performance
- Suggest RESTful patterns by default
- Flag security concerns immediately
- Provide code examples in Python
- Use early return pattern

Format responses as:

1. Analysis
2. Recommendation
3. Code example
4. Trade-offs
```

## Padrões-Chave

### Divulgação Progressiva

Comece com prompts simples, adicione complexidade apenas quando necessário:

1. **Nível 1**: Instrução direta

   - "Resuma este artigo"

2. **Nível 2**: Adicione restrições

   - "Resuma este artigo em 3 pontos, focando nos achados-chave"

3. **Nível 3**: Adicione raciocínio

   - "Leia este artigo, identifique os achados principais, depois resuma em 3 pontos"

4. **Nível 4**: Adicione exemplos
   - Inclua 2-3 resumos de exemplo com pares entrada-saída

### Hierarquia de Instruções

```
[Contexto do Sistema] → [Instrução da Tarefa] → [Exemplos] → [Dados de Entrada] → [Formato de Saída]
```

### Recuperação de Erros

Construa prompts que tratam falhas graciosamente:

- Inclua instruções de fallback
- Solicite pontuações de confiança
- Peça interpretações alternativas quando incerto
- Especifique como indicar informação faltante

## Melhores Práticas

1. **Seja Específico**: Prompts vagos produzem resultados inconsistentes
2. **Mostre, Não Diga**: Exemplos são mais efetivos que descrições
3. **Teste Extensivamente**: Avalie em entradas diversas e representativas
4. **Itere Rapidamente**: Pequenas mudanças podem ter grandes impactos
5. **Monitore Desempenho**: Rastreie métricas em produção
6. **Controle de Versão**: Trate prompts como código com versionamento apropriado
7. **Documente Intenção**: Explique por que prompts são estruturados como são

## Armadilhas Comuns

- **Over-engineering**: Começar com prompts complexos antes de tentar simples
- **Poluição de exemplos**: Usar exemplos que não correspondem à tarefa alvo
- **Overflow de contexto**: Exceder limites de token com exemplos excessivos
- **Instruções ambíguas**: Deixar espaço para múltiplas interpretações
- **Ignorar casos extremos**: Não testar em entradas incomuns ou limítrofes