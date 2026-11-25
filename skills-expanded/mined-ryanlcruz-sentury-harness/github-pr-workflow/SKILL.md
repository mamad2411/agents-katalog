---
name: github-pr-workflow
description: "Ciclo de vida de Pull Requests do Sentury via gh CLI ou API curl."
version: 1.0.0
category: github
tags: [git, github, pr, pull-request, branch, merge]
tools_used: [executar_python]
platforms: [linux, macos, windows]
---

# GitHub Pull Request Workflow

Rotina para automatizar a abertura de branches, commits estruturados e criação de Pull Requests das análises ou correções efetuadas pelo Sentury.

## Quando Usar

- O gestor solicitar a exportação ou envio de uma correção de código/análise para o repositório principal do Sentury no GitHub.
- Submissão automatizada de relatórios executivos em markdown em repositório compartilhado de liderança.

## Prerrequisitos

- Token `$GITHUB_TOKEN` ativo no ambiente.
- Utilitário `git` e `gh` (GitHub CLI) disponíveis ou token configurado para chamadas REST.

## Procedimento

1. **Acessar/Criar Branch**:
   - `git checkout main && git pull origin main`
   - `git checkout -b feat/sentury-analysis-<id>`
2. **Efetuar Commits**:
   - Usar mensagens baseadas em Conventional Commits (ex: `feat: add root cause visual template`).
3. **Efetuar Push & Abrir PR**:
   - `git push -u origin HEAD`
   - `gh pr create --title "feat: analysis report" --body "Summary of actions"` (ou usar fallback `curl` com token de cabeçalho contra a API de Pulls do GitHub).
4. **Verificar Status de CI**:
   - Rodar `gh pr checks` para garantir que os testes passaram no repositório remoto.

## Pitfalls

- Nunca commite chaves de API (`.env` ou configurações de token) ou dados de clientes sob PII.
