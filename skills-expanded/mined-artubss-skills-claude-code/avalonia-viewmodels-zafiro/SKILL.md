---
name: avalonia-viewmodels-zafiro
description: Padrões ideais para criação de ViewModel e Wizard em Avalonia usando Zafiro e ReactiveUI.
---

# ViewModels Avalonia com Zafiro

Esta skill fornece um conjunto de melhores práticas e padrões para criar ViewModels, Wizards e gerenciar navegação em aplicações Avalonia, aproveitando o poder do **ReactiveUI** e do kit de ferramentas **Zafiro**.

## Princípios Fundamentais

1.  **Abordagem Funcional-Reativa**: Use ReactiveUI (`ReactiveObject`, `WhenAnyValue`, etc.) para gerenciar estado e lógica.
2.  **Comandos Aprimorados**: Utilize `IEnhancedCommand` para melhor gerenciamento de comandos, incluindo relatório de progresso e atributos de nome/texto.
3.  **Padrão Wizard**: Implemente fluxos complexos usando `SlimWizard` e `WizardBuilder` para uma abordagem declarativa e mantível.
4.  **Descoberta Automática de Seções**: Use o atributo `[Section]` para registrar e descobrir seções de UI automaticamente.
5.  **Composição Limpa**: Mapeie ViewModels para Views usando `DataTypeViewLocator` e gerencie dependências na `CompositionRoot`.

## Guias

- [ViewModels & Comandos](viewmodels.md): Criando ViewModels robustos e gerenciando comandos.
- [Wizards & Fluxos](wizards.md): Construindo wizards multi-etapa com `SlimWizard`.
- [Navegação & Seções](navigation_sections.md): Gerenciando navegação e UIs baseadas em seções.
- [Composição & Mapeamento](composition.md): Melhores práticas para conexão View-ViewModel e injeção de dependência.

## Referência de Exemplo

Para implementações no mundo real, consulte o projeto **Angor**:
- `CreateProjectFlowV2.cs`: Excelente exemplo de construção complexa de Wizard.
- `HomeViewModel.cs`: ViewModel de seção simples usando comandos funcional-reativos.