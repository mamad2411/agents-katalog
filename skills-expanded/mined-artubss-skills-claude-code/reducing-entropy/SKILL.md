---
name: reducing-entropy
description: Skill manual ativado apenas por solicitação explícita do usuário para minimizar o tamanho total da base de código. Mede sucesso pela quantidade final de código, não pelo esforço. Tendência para exclusão.
---

# Reduzindo Entropia

Mais código gera mais código. A entropia se acumula. Este skill tem tendência para a menor base de código possível.

**Pergunta central:** "Como fica a base de código *depois*?"

## Antes de Começar

**Carregue pelo menos um mindset de `references/`**

1. Liste os arquivos no diretório de referência
2. Leia as descrições no frontmatter para escolher qual se aplica
3. Carregue pelo menos uma
4. Declare qual você carregou e seu princípio central

**Não prossiga até fazer isso.**

## O Objetivo

O objetivo é **menos código total na base de código final** — não menos código para escrever agora.

- Escrever 50 linhas que deletam 200 linhas = ganho líquido
- Manter 14 funções para evitar escrever 2 = perda líquida
- "Sem churn" não é um objetivo. Menos código é o objetivo.

**Meça o estado final, não o esforço.**

## Três Perguntas

### 1. Qual é a menor base de código que resolve isso?

Não "qual é a menor mudança" — qual é o menor *resultado*.

- Isso poderia ser 2 funções em vez de 14?
- Isso poderia ser 0 funções (deletar a feature)?
- O que deletaríamos se fizéssemos isso?

### 2. A mudança proposta resulta em menos código total?

Conte linhas antes e depois. Se depois > antes, rejeite.

- "Melhor organizado" mas mais código = mais entropia
- "Mais flexível" mas mais código = mais entropia
- "Separação mais limpa" mas mais código = mais entropia

### 3. O que podemos deletar?

Toda mudança é uma oportunidade de deletar. Pergunte-se:

- O que isso deixa obsoleto?
- O que era necessário apenas por causa do que estamos substituindo?
- O máximo que poderíamos remover?

## Sinais de Alerta

- **"Manter o que existe"** — Viés do status quo. A questão é código total, não churn.
- **"Isso adiciona flexibilidade"** — Flexibilidade para quê? YAGNI.
- **"Melhor separação de responsabilidades"** — Mais arquivos/funções = mais código. Separação não é gratuita.
- **"Type safety"** — Vale quantas linhas? Às vezes checks em runtime com menos código vence.
- **"Mais fácil de entender"** — 14 coisas não são mais fáceis que 2 coisas.

## Quando Isso Não se Aplica

- A base de código já é mínima para o que faz
- Você está em um framework com convenções fortes (não lute contra isso)
- Requisitos de conformidade/regulatórios obrigam certas estruturas

## Mindsets de Referência

Veja `references/` para fundamentação filosófica.

Para adicionar novos mindsets, consulte `adding-reference-mindsets.md`.

---

**Tendência para exclusão. Meça o estado final.**