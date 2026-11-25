---
name: avalonia-zafiro-development
description: Regras obrigatórias de habilidades, convenções e comportamento para desenvolvimento Avalonia UI com o toolkit Zafiro.
---

# Desenvolvimento Avalonia Zafiro

Esta habilidade define as convenções obrigatórias e regras de comportamento para desenvolver aplicações multiplataforma com Avalonia UI e o toolkit Zafiro. Essas regras priorizam manutenibilidade, correção e uma abordagem funcional-reativa.

## Pilares Principais

1.  **MVVM Funcional-Reativo**: Lógica MVVM pura usando DynamicData e ReactiveUI.
2.  **Segurança & Previsibilidade**: Tratamento explícito de erros com tipos `Result` e evitar exceções para fluxo de controle.
3.  **Excelência Multiplataforma**: ViewModels estritamente independentes de Avalonia e composição em vez de herança.
4.  **Zafiro em Primeiro Lugar**: Aproveite abstrações e helpers existentes do Zafiro para evitar redundância.

## Guias

- [Habilidades Técnicas Principais & Arquitetura](core-technical-skills.md): Habilidades fundamentais e princípios arquiteturais.
- [Padrões de Nomenclatura & Codificação](naming-standards.md): Regras para nomenclatura, campos e tratamento de erros.
- [Regras Avalonia, Zafiro & Reativas](avalonia-reactive-rules.md): Diretrizes específicas para UI, integração Zafiro e pipelines DynamicData.
- [Atalhos Zafiro](zafiro-shortcuts.md): Mapeamentos concisos para operações comuns de Rx/Zafiro.
- [Padrões Comuns](patterns.md): Padrões avançados como `RefreshableCollection` e Validação.

## Procedimento Antes de Escrever Código

1.  **Busque Primeiro**: Procure no codebase por implementações similares ou helpers Zafiro existentes.
2.  **Extensões Reutilizáveis**: Se um helper estiver faltando, proponha um novo método de extensão reutilizável em vez de incorporar lógica complexa.
3.  **Pipelines Reativos**: Certifique-se de que operadores DynamicData sejam usados em vez de Rx puro quando aplicável.