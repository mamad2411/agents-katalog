---
name: concise-planning
description: Use quando um usuário solicita um plano para uma tarefa de codificação, para gerar um checklist claro, acionável e atômico.
---

# Planejamento Conciso

## Objetivo

Transformar uma solicitação do usuário em **um único plano acionável** com etapas atômicas.

## Fluxo de Trabalho

### 1. Analisar Contexto

- Leia `README.md`, documentação e arquivos de código relevantes.
- Identifique restrições (linguagem, frameworks, testes).

### 2. Interação Mínima

- Faça **no máximo 1-2 perguntas** e apenas se forem realmente bloqueantes.
- Faça suposições razoáveis para incógnitas que não sejam bloqueantes.

### 3. Gerar Plano

Use a seguinte estrutura:

- **Abordagem**: 1-3 frases sobre o quê e por quê.
- **Escopo**: Pontos de bala para "Incluso" e "Excluso".
- **Itens de Ação**: Uma lista de 6-10 tarefas atômicas e ordenadas (começando com verbo).
- **Validação**: Pelo menos um item para testes.

## Modelo de Plano

```markdown
# Plano

<Abordagem de alto nível>

## Escopo

- Incluso:
- Excluso:

## Itens de Ação

[ ] <Etapa 1: Descoberta>
[ ] <Etapa 2: Implementação>
[ ] <Etapa 3: Implementação>
[ ] <Etapa 4: Validação/Testes>
[ ] <Etapa 5: Deploy/Commit>

## Questões em Aberto

- <Pergunta 1 (máx 3)>
```

## Diretrizes para Checklist

- **Atômico**: Cada etapa deve ser uma unidade lógica única de trabalho.
- **Começar com verbo**: "Adicionar...", "Refatorar...", "Verificar...".
- **Concreto**: Nomeie arquivos ou módulos específicos quando possível.