---
name: novo
description: "Use quando for começar um app Power Apps novo do zero: etapa 1 do pipeline do kit (Orquestrador). Recebe a ideia, cria a pasta do projeto, o git, o power-platform.config.json, o 00-LEIA-PRIMEIRO.md e o ESTADO.md, e aponta o próximo comando. Não use para app que já existe (descreva o problema e o orquestrador `power-platform` escolhe o caminho) nem para continuar um projeto já iniciado (use `/pp:progresso`)."
argument-hint: "[a ideia do app: uma frase, uma lista ou um texto colado]"
user-invocable: true
disable-model-invocation: true
---

# /pp:novo — Orquestrador: início do projeto

Primeira etapa do pipeline (`KIT/skills/power-platform/references/pipeline.md`). Em 5 minutos o
projeto ganha a estrutura que todas as etapas seguintes leem. Nada de tela, tabela ou fluxo aqui.

`KIT` = `${CLAUDE_PLUGIN_ROOT}` (a pasta do plugin). Formato de banner, checkpoint e próximo passo:
`KIT/skills/power-platform/references/formato-saida.md`. Script de estado:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py" <comando>
```

## Antes de começar

1. Procure `ESTADO.md` na pasta atual e nas de cima. **Se existe**, o projeto já foi iniciado: rode
   `estado.py mostrar`, mostre a saída e pare.
2. Mostre o banner `PP ► NOVO PROJETO` e diga em uma frase o que vai acontecer.

## Passos

1. **A ideia, do jeito que vier.** Se `$ARGUMENTS` trouxe, use. Senão pergunte: "Conte a ideia do
   app: uma frase, uma lista bagunçada, um texto colado, um print ou uma planilha servem. Quanto
   mais vier agora, menos o brainstorm vai perguntar." Aceite o que vier, sem pedir formato.
   - Tire dela a **ideia em uma frase** (o que resolve e para quem) para o `ESTADO.md`.
   - Senha, chave ou token no meio: não grave e avise para trocar.
   - Veio só uma frase: siga; o brainstorm conduz o resto.
2. **O nome.** Proponha um nome curto, derivado da ideia (ex.: `Pedidos`), e confirme. Sem
   espaço nem acento no nome da pasta.
3. **Três escolhas numa rodada só:** uma chamada de `AskUserQuestion` com as três perguntas
   (são independentes; o usuário responde tudo de uma vez):
   - header `Pasta`: "Usar esta pasta" (recomendado quando ela está vazia ou só tem material do
     projeto) ou "Criar a subpasta `<Nome>/` aqui";
   - header `Commits`: "Cada etapa faz um commit no fim (Recomendado)" ou "Eu cuido dos commits";
   - header `Modelos`, "Quem pensa e quem executa?": Equilibrado (Recomendado), Máximo, Econômico,
     Herdar. O `preview` de cada opção é o bloco do perfil que
     `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py" perfis` imprime;
     a descrição, a frase "quando" de `KIT/skills/power-platform/references/modelos.md` §1.
   Resposta livre em Modelos (ex.: "Opus em tudo"): o perfil mais próximo mais as trocas
   `--sessao`, `--planejamento`, `--execucao` do passo 5.
   Na subpasta, avise já: as próximas sessões precisam ser abertas **dentro dela** (feche e abra o
   Claude Code lá; `/clear` não troca de pasta).
4. **Crie a estrutura** na raiz do projeto:
   - `git init` se a pasta não está dentro de um repositório;
   - `.gitignore` com: `dist/`, `.env`, `*.msapp`, `*.zip`, `__pycache__/`, `*.tmp`,
     `AMBIENTE-AS-BUILT/capturas/`, `docs/planejamento/**/capturas/`, `.claude/settings.local.json`;
   - `power-platform.config.json` a partir de `KIT/skills/power-platform/assets/power-platform.config.exemplo.json`:
     `projeto` = nome; **tire** `trilha_dados` e `prefixo_publisher` (a arquitetura decide);
     `git_commit_por_etapa` da resposta em Commits;
   - `00-LEIA-PRIMEIRO.md` a partir de `KIT/skills/power-platform/assets/leia-primeiro-molde.md`, com a ideia;
   - pastas `docs/planejamento/` e `docs/decisoes/`;
   - `docs/planejamento/ideia-bruta.md` no molde `KIT/skills/power-platform/assets/ideia-bruta-molde.md`:
     o que veio no passo 1 (texto como veio; print ou planilha descritos na tabela de anexos) e a
     seção 3 preenchida com o que já dá para tirar, cada item com a origem. Não complete o que a
     ideia não diz: bloco sem informação fica "—".
5. **Modelos:** `modelos.py aplicar <perfil> [trocas]` da raiz do projeto (na subpasta,
   `--raiz <Nome>` antes de `aplicar`). Mostre a saída e diga em uma linha: as próximas etapas
   abrem a sessão em `<modelo>` e cada agente recebe o seu; esta sessão continua no modelo atual.
6. **Estado:** `estado.py iniciar --projeto "<Nome>" --ideia "<ideia em uma frase>"` (na subpasta,
   acrescente `--raiz <Nome>`).
7. **Commit** (se `git_commit_por_etapa`): `git add -A` e `git commit -m "pp(novo): estrutura do projeto <Nome>"`.
   O `.claude/settings.local.json` fica fora (é pessoal).

## Portão de saída

`ESTADO.md`, `power-platform.config.json` (com `modelos`) e `00-LEIA-PRIMEIRO.md` existem na raiz,
e `docs/planejamento/ideia-bruta.md` guarda tudo o que o usuário mandou;
`git status` funciona. Confira com `ls` e `modelos.py mostrar` antes de encerrar.

## Encerrar

Resumo em até 4 linhas (pasta, arquivos criados) e o bloco "Próximo passo" que o `iniciar`
imprimiu, sem mudar nada. Se o projeto foi para uma subpasta, acrescente uma linha antes do bloco:
"Abra o Claude Code dentro de `<Nome>/` para a próxima etapa".
