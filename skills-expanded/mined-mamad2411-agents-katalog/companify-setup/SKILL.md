---
name: companify-setup
description: Prepara a configuração .companify, a árvore de artefatos company/ e as instruções do agente. Use ao instalar ou atualizar o Companify em um projeto.
---

# Configurar o Companify

## Protocolo operacional

- **Plano e progresso:** criar um plano visível e atualizar o estado após a
  inspeção, a configuração e a validação.
- **Fontes de verdade:** ler o `AGENTS.md` do projeto, os arquivos existentes
  em `.companify/` e `company/`, `.brandfy/config.yaml` quando existir, e a
  referência [agents-consumer.md](references/agents-consumer.md).
- **Escopo e idempotência:** preservar configurações e artefatos existentes.
  O setup só cria arquivos e diretórios ausentes, e substitui apenas o bloco
  Companify no `AGENTS.md`.
- **Validação:** executar o setup com `--check` depois da escrita e revisar o
  `git diff`.
- **Resumo final:** informar arquivos criados, arquivos preservados, estágio
  configurado, validações e pendências.

## Fluxo

1. Localizar a raiz do projeto e ler suas instruções.
2. Detectar Brandfy: verificar se `.brandfy/config.yaml` e `brand/strategy.md`
   existem. Quando existirem, registrar na seção **Brandfy** do
   [template do Company Context](references/company-context-template.md) que
   o contexto de marca está disponível; quando não existirem, deixar
   explícito que o Companify está operando sem contexto de marca.
3. Executar:

   ```bash
   node <caminho-da-skill>/scripts/setup.mjs --project .
   ```

4. Abrir `.companify/config.yaml` e ajustar `company.name`, `country`,
   `language`, `currency` e `stage` com o usuário. Estágios possíveis:
   `idea`, `validation`, `pre-revenue`, `early-revenue`, `growth`, `scale`,
   `established`.
5. Quando o briefing empresarial ainda estiver incompleto, usar
   `$companify-interview` para conduzir a descoberta e preencher
   `.companify/company-context.md` sem inventar respostas.
6. Conferir o bloco delimitado por `companify:consumer` no `AGENTS.md`.
7. Executar:

   ```bash
   node <caminho-da-skill>/scripts/setup.mjs --project . --check
   ```

Depois do setup, abrir `.companify/config.yaml` e `company/README.md` para
confirmar o estágio e o status de cada artefato. Um segundo uso deve terminar
sem alterações; qualquer diferença indica configuração incompleta ou bloco do
agente antigo.

## Raciocínio do especialista

Tratar o setup como preparação de governança, não como criação do plano de
negócio. Confirmar responsáveis por respostas e aprovações, localização das
comprovações, artefatos canônicos e forma de resolver pendências. Uma estrutura
completa com informação fraca continua sendo um plano incompleto: o setup
não deve ser confundido com o trabalho de `$companify-interview`.
