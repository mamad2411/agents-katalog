---
name: specsfy-setup
description: Preparar e monitorar PROJECT.md e os contextos .specsfy de stack, regras e banco. Use no setup ou ao reconciliar mudanças da aplicação.
---

# Preparar contexto do projeto

## Modo de interação

Modo de interação: `perguntas`.
Antes de formular qualquer pergunta, leia e aplique o
`Contrato de perguntas numeradas` de `.specsfy/Spec.md`.

1. Ler `AGENTS.md`, `CLAUDE.md` e instruções locais antes de escrever.
2. Ler [as diretrizes publicáveis](references/framework-instructions.md) quando
   precisar auditar o bloco reservado em arquivos de agentes.
3. Executar `specsfy doctor --project <raiz>` e corrigir cada requisito
   ausente antes de preparar o contexto. O diagnóstico confere Node.js, Git,
   npm, acesso ao projeto e o `skills CLI`, com fallback por `npx`.
4. Executar `node scripts/setup_context.mjs --project <raiz>`.
   Renderizar `PROJECT.md`, `STACK.md`, `RULES.md` e `DATABASE.md` a partir de
   `.specsfy/templates/custom/<Nome>.md` quando existir ou dos arquivos
   gerenciados `.specsfy/templates/Project.md`, `Stack.md`, `Rules.md` e
   `Database.md` caso contrário; não manter modelos paralelos embutidos no
   script.
5. No início e no fim de cada mudança, executar:

   ```bash
   node scripts/monitor_context.mjs --project <raiz> --check
   ```

6. Inspecionar os quatro arquivos iniciais, `.specsfy/PACKAGES.md` quando
   gerado e a fonte de stack usada pelo script.
7. Nunca substituir um arquivo de contexto existente, mesmo com conteúdo
   incompleto. Em `AGENTS.md` e `CLAUDE.md`, atualizar somente o bloco
   delimitado do framework e preservar tudo fora dele.
8. Para completar ou corrigir stack, regras ou dados, anunciar o handoff e
   carregar respectivamente `$specsfy-aux-stack`, `$specsfy-aux-rules` ou
   `$specsfy-aux-database`.
9. Quando aplicação, persistência ou dependências mudar, carregar
   `$specsfy-documentator` depois das auxiliares e reconstruir `docs/` e
   `.specsfy/PACKAGES.md` a partir de todo o projeto.
10. Somente quando a pessoa solicitar ou indicar explicitamente o uso de
   Gitflow para o projeto (ver [references/gitflow.md](references/gitflow.md)),
   anunciar o handoff, carregar `$specsfy-specialist-gitflow` e registrar a
   convenção de branches confirmada em `RULES.md` via `$specsfy-aux-rules`.
   Nunca propor, presumir ou aplicar Gitflow a partir da estrutura de
   branches do repositório, da presença de uma branch `develop` ou de
   qualquer outro sinal implícito.

Não contornar um resultado `PENDING`. Atualizar o documento indicado e executar
o monitor novamente. Para mudança de aplicação sem impacto material na história
ou finalidade, registrar essa avaliação nas fontes da tarefa e repetir com
`--acknowledge-project-no-change`. Aplicar a mesma disciplina a regras com
`--acknowledge-rules-no-change`; nunca usar o reconhecimento para ocultar uma
mudança documental real.

Manter `PROJECT.md` na raiz. Manter `STACK.md`, `RULES.md`, `DATABASE.md` e
`PACKAGES.md` em `.specsfy/`. Tratar esses documentos como contexto derivado do
projeto, não como spec, gate ou autorização de implementação.

Em projeto com mais de um framework, registrar todas as fontes observadas;
não escolher silenciosamente um único stack. Se nenhum framework for
identificado, criar o modelo genérico e declarar que a confirmação está
pendente.
