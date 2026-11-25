---
name: setup
description: >-
  Termina de instalar o Claude Starter Kit depois do /plugin install — escreve o
  CLAUDE.md global, liga a barra de status e mescla as preferências, que são as
  partes que um plugin não consegue instalar sozinho. Depois ajuda a preencher o
  CLAUDE.md com os dados de quem está instalando. Roda uma vez, e de novo depois
  de atualização grande. Só dispara quando você chama: /kit-vamoo:setup.
disable-model-invocation: true
allowed-tools:
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/kit-setup.sh" *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/kit-setup.sh *)'
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/instrucoes-projeto.sh" --check *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/instrucoes-projeto.sh --check *)'
---

# Terminar a instalação do kit

O `/plugin install` entregou as skills, os comandos e os guard-rails de git.
Falta o resto — e falta por um motivo técnico, não por descuido:
o `settings.json` de um plugin só aceita as chaves `agent` e
`subagentStatusLine`. **CLAUDE.md global, barra de status, idioma e lista de
permissões não podem vir num plugin.** É isto que esta skill instala.

Depois de uma compactação só o começo desta skill volta ao contexto: leia o arquivo de
`references/` no passo que o cita, mesmo que já tenha lido antes.

## 1. Rode o setup

**No Windows, confira antes se existe `bash`.** Os guard-rails do kit (commit na main,
push forçado, `rm -r` fora das pastas descartáveis, leitura de segredo) são scripts bash
chamados pelos hooks. Sem o Git para Windows, o hook falha aberto e **nenhuma guarda roda**:
sobram só as regras `ask`/`deny` do `settings.json`. No PowerShell:

```powershell
Get-Command bash -ErrorAction SilentlyContinue
```

Saída vazia: diga à pessoa, em português, que sem o Git para Windows
(https://git-scm.com/download/win) as guardas do kit não rodam, recomende instalar e
reiniciar o Claude Code, e só então siga. O próprio `kit-setup.sh` também precisa do bash.

Sempre com `--dry-run` primeiro, e mostre a saída para a pessoa:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/kit-setup.sh" --dry-run
```

**Se a saída disser "Nada feito", pare aqui.** O `~/.claude` desta máquina é do kit
do time (tem o `.team-manifest`), e quem manda nele é o instalador de lá. Não siga
para os passos 2 e 3 e não edite o `~/.claude/CLAUDE.md`, que é o do time. Explique
isso à pessoa. Não contorne com `--force`, a não ser que ela peça explicitamente:
ele tira o `agents.md` do time e instala o `subagentes.md` e a barra de status daqui.

Confirmado, rode de verdade:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/kit-setup.sh"
```

O script faz backup de tudo que toca em `~/.claude/backup-kit-<data>/` antes de
mexer (ficam os 3 mais recentes). Se a pessoa tem algo próprio em `~/.claude`
que a limpeza da instalação antiga poderia levar — uma skill do kit que ela
editou, um script com nome igual —, liste em `~/.claude/.keep-local` (um
caminho por linha, relativo a `~/.claude`, glob simples) **antes** de rodar sem
`--dry-run`. Estas decisões já vêm tomadas nele, e vale dizer em voz alta:

- **`CLAUDE.md` que já existir não é sobrescrito.** O modelo do kit fica em
  `~/.claude/CLAUDE.kit.md` pra comparar. Só troca com `--force`, e só se a
  pessoa pedir.
- **As regras de subagente ficam em `~/.claude/subagentes.md`.** O `agents.md`
  que versões anteriores do kit instalavam sai, com cópia no backup: em disco que
  não diferencia maiúscula de minúscula (o padrão no macOS e no Windows), o Claude
  Code o lia como `AGENTS.md` em toda sessão. Listado no `.keep-local`, ele fica, e
  a saída avisa. A cópia fica em `~/.claude/backup-agents-md/`, fora da rotação dos
  backups. Um `AGENTS.md` de outra ferramenta ou escrito pela pessoa fica intocado: o
  setup só tira o arquivo gravado como `agents.md`, em minúsculas, e o `AGENTS.md` com
  a linha "Fica em `~/.claude/agents.md`" do modelo antigo do kit.
- **A barra de status tem dois modos.** O painel tem até 7 linhas: modelo, custo, tokens,
  contexto, os limites de 5h e de 7 dias e o PR. O curto é a linha única de antes:
  diretório, branch, PR e contexto. Instalação nova fica no painel. Quem já tinha a barra e
  nunca escolheu continua no curto. Pergunte qual a pessoa prefere e acrescente
  `--statusline painel` ou `--statusline curto` aos dois comandos acima. A escolha fica em
  `~/.claude/statusline-modo` e vale até ela rodar o setup com a outra.
- **Modo sem perguntas, só para quem pedir.** Se a pessoa chamou a skill com `--sem-perguntas`
  ou `--com-perguntas`, ou pediu para o kit parar de pedir confirmação, acrescente a opção aos
  dois comandos acima. Não ofereça por conta própria. O modo põe o modo de permissão em
  `bypassPermissions` (**Ignorar permissões**), tira as regras `ask` de comando e deixa só o
  que não tem volta perguntando. Antes de rodar sem `--dry-run`, leia para ela, de
  [references/decisoes-do-setup.md](references/decisoes-do-setup.md), o que deixa de pedir
  confirmação, o que ainda pergunta e o que continua barrado. Depois, **diga os dois passos
  do app de desktop** que estão lá (ligar **Allow bypass permissions mode** em Settings > Code
  e escolher **Ignorar permissões** no seletor de cada pasta): sem eles o app segue pedindo
  "Permitir". Vale nos setups seguintes, até o `--com-perguntas`.
- **Leia [references/decisoes-do-setup.md](references/decisoes-do-setup.md)** e diga à pessoa
  também o que está lá: o `settings.json` é mesclado, o modo de permissão vira Auto (e como
  ficar no Accept edits ou no Manual), o que entra e sai do `allow`/`ask` e o auto-update do
  kit ligado.
- **No app de desktop, o seletor vence o arquivo.** O modo escolhido no seletor ao
  lado do botão de enviar é lembrado por pasta e ganha do `defaultMode`. Se ele
  mostrar **Manual** (ou **Ask permissions**, em versão antiga), diga à pessoa para
  trocar uma vez para **Auto** em cada pasta onde escolheu Manual.

## 2. Preencha o CLAUDE.md com os dados da pessoa

O template vem com campos `<entre-colchetes>`. Um CLAUDE.md com os colchetes
ainda lá é pior que nenhum: o modelo lê `<sua stack>` como instrução literal.

Se o setup disse "Você já tem um CLAUDE.md — não mexi nele", o arquivo é da
pessoa: não edite. Mostre o que o modelo do kit traz de diferente
(`diff ~/.claude/CLAUDE.md ~/.claude/CLAUDE.kit.md`) e pergunte o que ela quer
trazer. Se ele também avisou que esse CLAUDE.md ainda cita `agents.md`, mostre a
linha (`grep -n 'agents\.md' ~/.claude/CLAUDE.md`) e proponha trocar o nome por
`subagentes.md`; edite só com o OK dela. Se ele avisou que o CLAUDE.md ainda manda
usar o dotcontext, mostre a seção (`grep -n -i 'init the context\|dotcontext'
~/.claude/CLAUDE.md`) e proponha trocá-la pela "Projeto: memória, instruções e fluxo" do
`CLAUDE.kit.md`; também só com o OK dela. O resto deste passo vale quando o setup
instalou o CLAUDE.md.

Leia `~/.claude/CLAUDE.md`, colete o que falta **numa pergunta só** e edite o
arquivo:

- Como a pessoa quer ser chamada
- A stack do dia a dia (ex.: React + Supabase, Python + FastAPI, WordPress)
- Nível: quer explicação didática a cada passo, ou resposta direta?
- Se já usa GitHub com mais gente ou trabalha sozinha

Não invente resposta: se ela não souber a stack, deixe genérico e diga que dá
pra ajustar depois — o arquivo é dela.

## 3. Confira que pegou

```bash
claude plugin list | grep -A2 kit-vamoo     # deve aparecer enabled
ls ~/.claude/CLAUDE.md ~/.claude/statusline-command.sh
node -e 'const s=require(require("os").homedir()+"/.claude/settings.json");
console.log("auto-update:", s.extraKnownMarketplaces?.["vamoo-ai"]?.autoUpdate)'
```

A última linha deve dizer `auto-update: true`. Ela é o que garante que a pessoa
não fique presa na versão de hoje — **o Claude Code só sincroniza essa flag para
o `known_marketplaces.json` quando uma sessão nova começa**, então ela só passa a
valer depois do reinício do passo seguinte.

**Diga pra pessoa reiniciar o Claude Code** — e diga que é pra tudo, não só pra
barra. A sessão que está aberta começou com o `settings.json` antigo: idioma,
lista de permissões e barra de status só valem no próximo start. Sem esse aviso
a pessoa conclui que o setup não pegou e vai debugar um problema que não existe.

Depois de reiniciar, a barra mostra diretório, branch, alterações não salvas,
à frente/atrás do remoto, `gh✓`, PR aberto e o contexto em número absoluto.

Projeto que já existia, com `CLAUDE.md` ou `AGENTS.md` próprio, migra para o `AGENTS.md` como fonte com `bash "${CLAUDE_PLUGIN_ROOT}/scripts/instrucoes-projeto.sh" --check <repo>` (classe e proposta, só lê) e depois `--apply`, que grava só nas classes seguras e mostra o diff antes, e num repositório git sem `.worktreeinclude` copia o modelo (é ele que leva o `.env` ignorado para o worktree novo). Na primeira sessão de trabalho nesse projeto, a ordem é: o `--check`, depois o `/kit-vamoo:memoria-projeto` (põe a memória do projeto em `.context/memoria/`), depois a linha de base (rodar type-check, lint e testes e anotar o que já falhava antes de mexer).

## Se algo não estiver funcionando

| Sintoma | Causa | Conserto |
|---|---|---|
| Barra não aparece | Claude Code não foi reiniciado, ou falta `node` | Reiniciar; `node --version` |
| `/kit-vamoo:` não completa nenhuma skill | Plugin instalado mas não recarregado | `/reload-plugins` |
| Hook não bloqueia commit na main | Sem `node` — os hooks falham em aberto de propósito | Instalar o Node.js LTS |
| Skill aparece duas vezes | Instalação antiga pelo `install.sh` ainda em `~/.claude/skills/` | O `kit-setup.sh` remove pelo manifesto; rode-o de novo |
| `gh✗` na barra | GitHub CLI ausente ou deslogado | `gh auth login` (opcional — só perde a visão de PR) |
