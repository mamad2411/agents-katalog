---
name: maintain-agents
description: Revisar, criar ou atualizar arquivos AGENTS.md do workspace C:\codes somente quando o usuario solicitar explicitamente. Use para alterar regras persistentes, alinhar instrucoes entre raiz, controle de chamados e skills, numerar regras, remover contradicoes, ou garantir que AGENTS.md aponte para C:\codes\skills e para o controle de chamados.
metadata:
  camada: atividade
  escopo_negativo:
    - nao edita SKILL.md (maintain-skills)
    - nao executa operacoes git (maintain-git)
  dependencias:
    - maintain-skills
  saidas:
    - AGENTS.md normalizados por contexto
  triggers:
    - revisar agents.md
    - atualizar regras de contexto
---

# Manter Agents

## Objetivo

Manter arquivos `AGENTS.md` curtos, numerados e coerentes com `C:\codes\AGENTS.md`.

## Apelidos

1. `root` significa `C:\codes\AGENTS.md`.
2. `ctrl_chamados` significa `C:\codes\tools\chamados` e as skills `maintain-tickets` e `register-ticket-session`.
3. Preservar estes apelidos ao alterar qualquer `AGENTS.md`.

## Uso

1. Usar somente quando o usuario solicitar manutencao de `AGENTS.md`.
2. Nao invocar automaticamente para tarefas comuns.

## Limites

1. Nao criar regras globais fora de `C:\codes\AGENTS.md`.
2. Nao duplicar regras completas entre `root`, `ctrl_chamados`, `skills` e projetos.
3. Nao alterar regras de projeto sem pedido explicito.
4. Nao alterar `AGENTS.md` de outro contexto sem pedido registrado no `plan` do contexto dono, salvo pedido explicito do usuario.
5. Fora do proposito desta skill, devolver ao `route-skills-by-context` (nao improvisar).

## Fluxo

1. Ler `C:\codes\AGENTS.md`.
2. Identificar quais `AGENTS.md` sao afetados.
3. Manter a raiz `C:\codes\AGENTS.md` como entrada principal do workspace.
4. Manter regras detalhadas de chamados em `C:\codes\tools\chamados\AGENTS.md`.
5. Manter boas praticas de skills em `C:\codes\skills\AGENTS.md`.
6. Evitar repetir textos longos entre arquivos.
7. Preferir regras numeradas, curtas e verificaveis.
8. Validar que nao ha referencia a pastas antigas ou conflitantes.
9. Preservar a regra global de autonomia por contexto: cada contexto altera a si mesmo.
10. Quando `AGENTS.md` precisar apontar para tools, usar `C:\codes\tools` somente depois de existir plano aprovado.

## Saida esperada

1. `AGENTS.md` alterado somente no escopo solicitado.
2. Regras com fundamento, proposito e limite explicitos.
3. Nenhuma contradicao com `C:\codes\AGENTS.md`.


## Correlacao Obrigatoria de Skills

1. Antes de qualquer mudanca persistente, executar `route-skills-by-context`.
2. Registrar na sessao ativa:
- skill executora
- skills de apoio
- motivo da escolha
- validacao da escolha
3. Sem esse registro, manter atividade como `bloqueado`.
