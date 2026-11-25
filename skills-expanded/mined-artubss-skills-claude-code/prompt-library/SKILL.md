---
name: prompt-library
description: "Coleção curada de prompts de alta qualidade para diversos casos de uso. Inclui prompts baseados em função, templates específicos de tarefas e técnicas de refinamento de prompts. Use quando o usuário precisar de templates de prompts, prompts para dramatização, ou exemplos de prompts prontos para uso em codificação, escrita, análise ou tarefas criativas."
---

# 📝 Biblioteca de Prompts

> Uma coleção abrangente de prompts testados em batalha, inspirada em [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) e melhores práticas da comunidade.

## Quando Usar Esta Habilidade

Use esta habilidade quando o usuário:

- Precisa de templates de prompts prontos para usar
- Quer prompts baseados em função (atuar como X)
- Solicita exemplos de prompts ou inspiração
- Precisa de padrões de prompts específicos de tarefas
- Quer melhorar sua técnica de prompts

## Categorias de Prompts

### 🎭 Prompts Baseados em Função

#### Desenvolvedor Especialista

```
Act as an expert software developer with 15+ years of experience. You specialize in clean code, SOLID principles, and pragmatic architecture. When reviewing code:
1. Identify bugs and potential issues
2. Suggest performance improvements
3. Recommend better patterns
4. Explain your reasoning clearly
Always prioritize readability and maintainability over cleverness.
```

#### Revisor de Código

```
Act as a senior code reviewer. Your role is to:
1. Check for bugs, edge cases, and error handling
2. Evaluate code structure and organization
3. Assess naming conventions and readability
4. Identify potential security issues
5. Suggest improvements with specific examples

Format your review as:
🔴 Critical Issues (must fix)
🟡 Suggestions (should consider)
🟢 Praise (what's done well)
```

#### Redator Técnico

```
Act as a technical documentation expert. Transform complex technical concepts into clear, accessible documentation. Follow these principles:
- Use simple language, avoid jargon
- Include practical examples
- Structure with clear headings
- Add code snippets where helpful
- Consider the reader's experience level
```

#### Arquiteto de Sistemas

```
Act as a senior system architect designing for scale. Consider:
- Scalability (horizontal and vertical)
- Reliability (fault tolerance, redundancy)
- Maintainability (modularity, clear boundaries)
- Performance (latency, throughput)
- Cost efficiency

Provide architecture decisions with trade-off analysis.
```

### 🛠️ Prompts Específicos de Tarefas

#### Depurar Este Código

```
Debug the following code. Your analysis should include:

1. **Problem Identification**: What exactly is failing?
2. **Root Cause**: Why is it failing?
3. **Fix**: Provide corrected code
4. **Prevention**: How to prevent similar bugs

Show your debugging thought process step by step.
```

#### Explique Como se Fosse para uma Criança (ELI5)

```
Explain [CONCEPT] as if I'm 5 years old. Use:
- Simple everyday analogies
- No technical jargon
- Short sentences
- Relatable examples from daily life
- A fun, engaging tone
```

#### Refatoração de Código

```
Refactor this code following these priorities:
1. Readability first
2. Remove duplication (DRY)
3. Single responsibility per function
4. Meaningful names
5. Add comments only where necessary

Show before/after with explanation of changes.
```

#### Escrever Testes

```
Write comprehensive tests for this code:
1. Happy path scenarios
2. Edge cases
3. Error conditions
4. Boundary values

Use [FRAMEWORK] testing conventions. Include:
- Descriptive test names
- Arrange-Act-Assert pattern
- Mocking where appropriate
```

#### Documentação de API

```
Generate API documentation for this endpoint including:
- Endpoint URL and method
- Request parameters (path, query, body)
- Request/response examples
- Error codes and meanings
- Authentication requirements
- Rate limits if applicable

Format as OpenAPI/Swagger or Markdown.
```

### 📊 Prompts de Análise

#### Análise de Complexidade de Código

```
Analyze the complexity of this codebase:

1. **Cyclomatic Complexity**: Identify complex functions
2. **Coupling**: Find tightly coupled components
3. **Cohesion**: Assess module cohesion
4. **Dependencies**: Map critical dependencies
5. **Technical Debt**: Highlight areas needing refactoring

Rate each area and provide actionable recommendations.
```

#### Análise de Performance

```
Analyze this code for performance issues:

1. **Time Complexity**: Big O analysis
2. **Space Complexity**: Memory usage patterns
3. **I/O Bottlenecks**: Database, network, disk
4. **Algorithmic Issues**: Inefficient patterns
5. **Quick Wins**: Easy optimizations

Prioritize findings by impact.
```

#### Revisão de Segurança

```
Perform a security review of this code:

1. **Input Validation**: Check all inputs
2. **Authentication/Authorization**: Access control
3. **Data Protection**: Sensitive data handling
4. **Injection Vulnerabilities**: SQL, XSS, etc.
5. **Dependencies**: Known vulnerabilities

Classify issues by severity (Critical/High/Medium/Low).
```

### 🎨 Prompts Criativos

#### Brainstorm de Funcionalidades

```
Brainstorm features for [PRODUCT]:

For each feature, provide:
- Name and one-line description
- User value proposition
- Implementation complexity (Low/Med/High)
- Dependencies on other features

Generate 10 ideas, then rank top 3 by impact/effort ratio.
```

#### Gerador de Nomes

```
Generate names for [PROJECT/FEATURE]:

Provide 10 options in these categories:
- Descriptive (what it does)
- Evocative (how it feels)
- Acronyms (memorable abbreviations)
- Metaphorical (analogies)

For each, explain the reasoning and check domain availability patterns.
```

### 🔄 Prompts de Transformação

#### Migrar Código

```
Migrate this code from [SOURCE] to [TARGET]:

1. Identify equivalent constructs
2. Handle incompatible features
3. Preserve functionality exactly
4. Follow target language idioms
5. Add necessary dependencies

Show the migration step by step with explanations.
```

#### Converter Formato

```
Convert this [SOURCE_FORMAT] to [TARGET_FORMAT]:

Requirements:
- Preserve all data
- Use idiomatic target format
- Handle edge cases
- Validate the output
- Provide sample verification
```

## Técnicas de Engenharia de Prompts

### Chain of Thought (CoT)

```
Let's solve this step by step:
1. First, I'll understand the problem
2. Then, I'll identify the key components
3. Next, I'll work through the logic
4. Finally, I'll verify the solution

[Your question here]
```

### Few-Shot Learning

```
Here are some examples of the task:

Example 1:
Input: [example input 1]
Output: [example output 1]

Example 2:
Input: [example input 2]
Output: [example output 2]

Now complete this:
Input: [actual input]
Output:
```

### Padrão de Persona

```
You are [PERSONA] with [TRAITS].
Your communication style is [STYLE].
You prioritize [VALUES].

When responding:
- [Behavior 1]
- [Behavior 2]
- [Behavior 3]
```

### Saída Estruturada

```
Respond in the following JSON format:
{
  "analysis": "your analysis here",
  "recommendations": ["rec1", "rec2"],
  "confidence": 0.0-1.0,
  "caveats": ["caveat1"]
}
```

## Checklist para Melhoria de Prompts

Ao criar prompts, certifique-se:

- [ ] **Objetivo claro**: O que exatamente você quer?
- [ ] **Contexto fornecido**: Informações de fundo incluídas?
- [ ] **Formato especificado**: Como a saída deve ser estruturada?
- [ ] **Exemplos fornecidos**: Há exemplos de referência?
- [ ] **Restrições definidas**: Há limitações ou requisitos?
- [ ] **Critérios de sucesso**: Como você mede uma boa saída?

## Recursos

- [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)
- [prompts.chat](https://prompts.chat)
- [Learn Prompting](https://learnprompting.org/)

---

> 💡 **Dica**: Os melhores prompts são específicos, fornecem contexto e incluem exemplos de saída desejada.