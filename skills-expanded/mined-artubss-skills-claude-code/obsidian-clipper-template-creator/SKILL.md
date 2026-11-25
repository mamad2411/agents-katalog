---
name: obsidian-clipper-template-creator
description: Guia para criar templates para o Obsidian Web Clipper. Use quando quiser criar um novo template de clipping, entender variáveis disponíveis ou formatar conteúdo cortado.
---

# Obsidian Web Clipper Template Creator

Esta skill ajuda você a criar templates JSON importáveis para o Obsidian Web Clipper.

## Fluxo de trabalho

1.  **Identifique a Intenção do Usuário:** site específico (YouTube), tipo específico (Receita), ou clipping geral?
2.  **Verifique Bases Existentes:** O usuário provavelmente tem um schema "Base" definido em `Templates/Bases/`.
    *   **Ação:** Leia `Templates/Bases/*.base` para encontrar uma categoria correspondente (ex: `Recipes.base`).
    *   **Ação:** Use as propriedades definidas na Base para estruturar as propriedades do template do Clipper.
    *   Veja [references/bases-workflow.md](references/bases-workflow.md) para detalhes.
3.  **Busque & Analise URL de Referência:** Valide variáveis contra uma página real.
    *   **Ação:** Peça ao usuário uma URL de exemplo do conteúdo que quer clipar (se não fornecida).
    *   **Ação:** Use `WebFetch` para recuperar o HTML da página.
    *   **Ação:** Analise o HTML para Schema.org JSON, Meta tags e CSS selectors.
    *   Veja [references/analysis-workflow.md](references/analysis-workflow.md) para técnicas de análise.
4.  **Rascunhe o JSON:** Crie um objeto JSON válido seguindo o schema.
    *   Veja [references/json-schema.md](references/json-schema.md).
5.  **Verifique Variáveis:** Assegure que as variáveis escolhidas (Preset, Schema, Selector) existem na sua análise.
    *   Veja [references/variables.md](references/variables.md).

## Formato de Saída

**SEMPRE** exiba o resultado final como um bloco de código JSON que o usuário possa copiar e importar.

```json
{
  "schemaVersion": "0.1.0",
  "name": "My Template",
  ...
}
```

## Recursos

*   [references/variables.md](references/variables.md) - Variáveis de dados disponíveis.
*   [references/filters.md](references/filters.md) - Filtros de formatação.
*   [references/json-schema.md](references/json-schema.md) - Documentação de estrutura JSON.
*   [references/bases-workflow.md](references/bases-workflow.md) - Como mapear Bases para Templates.
*   [references/analysis-workflow.md](references/analysis-workflow.md) - Como validar dados de página.

### Documentação Oficial
*   [Variables](https://help.obsidian.md/web-clipper/variables)
*   [Filters](https://help.obsidian.md/web-clipper/filters)
*   [Templates](https://help.obsidian.md/web-clipper/templates)

## Exemplos

Veja [assets/](assets/) para exemplos JSON.