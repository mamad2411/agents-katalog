---
name: address-github-comments
description: Use when you need to address review or issue comments on an open GitHub Pull Request using the gh CLI.
---

# Responder a Comentários do GitHub

## Visão Geral

Responda de forma eficiente a comentários de review em PR ou feedback em issues usando o GitHub CLI (`gh`). Esta skill garante que todo feedback seja endereçado sistematicamente.

## Pré-requisitos

Certifique-se de que `gh` está autenticado.

```bash
gh auth status
```

Se não estiver logado, execute `gh auth login`.

## Fluxo de Trabalho

### 1. Inspecionar Comentários

Obtenha os comentários do PR da branch atual.

```bash
gh pr view --comments
```

Ou use um script customizado, se disponível, para listar threads.

### 2. Categorizar e Planejar

- Liste os comentários e threads de review.
- Proponha uma correção para cada um.
- **Aguarde confirmação do usuário** sobre quais comentários endereçar primeiro, se houver muitos.

### 3. Aplicar Correções

Aplique as mudanças de código para os comentários selecionados.

### 4. Responder aos Comentários

Uma vez corrigidos, responda às threads como resolvidas.

```bash
gh pr comment <PR_NUMBER> --body "Addressed in latest commit."
```

## Erros Comuns

- **Aplicar correções sem entender o contexto**: Sempre leia o código ao redor de um comentário.
- **Não verificar autenticação**: Verifique `gh auth status` antes de começar.