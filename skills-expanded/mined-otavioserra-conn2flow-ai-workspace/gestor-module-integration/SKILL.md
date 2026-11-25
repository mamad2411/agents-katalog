---
name: gestor-module-integration
description: 'Use quando criar, corrigir, revisar ou refatorar módulos do gestor em projetos privados Conn2Flow. Especialmente quando houver risco de esquecer modulo-id, JSON, função *_start(), autorun no final, switch($_GESTOR["opcao"]), switch($_GESTOR["ajax-opcao"]), resources, hooks, API ou widget.'
user-invocable: false
---

# Integração de módulo do gestor

Use esta skill quando a tarefa não é apenas uma regra de negócio isolada, mas um ajuste estrutural em módulo do gestor.

## Quando usar

- criar módulo novo em `gestor/modulos/`
- corrigir módulo que responde parcialmente no runtime
- refatorar módulo com risco de quebrar bootstrap, interface ou AJAX
- revisar diff de módulo que parece funcional no arquivo, mas incompleto no gestor

## Procedimento

1. Releia as [leituras mínimas](./references/leituras-minimas.md) antes da primeira edição.
2. Confirme o contrato estrutural usando o [checklist de integração](./references/checklist-integracao.md).
3. Se a tarefa tocar hook, API ou widget, inclua essas camadas na leitura e no diff, em vez de concluir pelo PHP principal sozinho.
4. Escolha um módulo simples e um módulo mais rico como referência antes de copiar padrões.
5. Depois da primeira edição substantiva, valide no menor escopo capaz de falsificar a integração.
6. Se ainda houver dúvida estrutural, releia o fluxo do core do Conn2Flow que inclui o módulo e fecha interface/AJAX antes de ampliar o diff.

## Erros comuns de snippet

Ao revisar ou gerar código para módulos do gestor, tome cuidado com erros que aparecem frequentemente em snippets de `gestor`, `db`, `javascript/ajax` e `models`:

- não use `$_REQUEST[$post_nome]` sem `isset()` ou `empty()`, para evitar warnings e notices de PHP.
- confirme se a chamada de banco de dados é a função correta (`banco_select`, `banco_update`, etc.) e válida no ambiente atual.
- verifique se strings PHP terminam em `;` e se o código de modelo tem delimitadores de tags `<!-- cel < -->` e `<!-- cel > -->` corretos.
- para AJAX, confirme que o frontend envia `ajaxOpcao` e que o backend trata `$_GESTOR['ajax-opcao']` no switch correspondente.
- ao usar helpers de modelo, verifique se `modelo_var_troca`, `modelo_var_troca_tudo`, `modelo_tag_val`, `modelo_tag_troca_val`, `modelo_var_in` e `modelo_tag_del` estão sendo usados de forma consistente.

## O que esta skill evita

- módulo com funções de negócio, mas sem `*_start()`
- branch normal sem `interface_iniciar()` e `interface_finalizar()`
- branch AJAX sem `interface_ajax_iniciar()` e `interface_ajax_finalizar()`
- JSON, pages ou variables incoerentes com o PHP e o HTML
- hooks, API ou widget esquecidos quando o módulo depende deles

## Referência humana complementar

- [guia prático de integração](../../../docs/gestor-modulos-integracao-pratica.md)