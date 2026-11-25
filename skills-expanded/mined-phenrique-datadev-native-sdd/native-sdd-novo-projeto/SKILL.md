---
name: native-sdd-novo-projeto
description: Cria um projeto novo com o scaffold do Native-SDD, ou equipa um diretório que já existe (.claude/, AGENTS.md, CLAUDE.md, pre-commit anti-segredo). Use quando o usuário pedir para criar, começar ou iniciar um projeto com SDD/Native-SDD, ou para pôr o Native-SDD numa pasta existente. Funciona de qualquer pasta, sem o atalho nsp.
---

# Criar ou equipar um projeto com o Native-SDD

## 1. Achar o framework

O instalador grava o caminho do checkout em `SDD_WORKFLOW_HOME` (pelo `env` do
`~/.claude/settings.json`). Confira antes de tudo:

```bash
echo "$SDD_WORKFLOW_HOME" && test -f "$SDD_WORKFLOW_HOME/onboarding/new-project.ps1" && echo OK
```

Se a variável está vazia ou o arquivo não existe, pare e diga ao usuário: o Native-SDD não está
instalado nesta máquina, ou o checkout saiu de lugar. A correção é rodar o instalador de novo
(`install.ps1` no Windows, `install.sh` no Linux/macOS) a partir do checkout, ou o bootstrap remoto
do README do projeto. Não procure o checkout pelo disco nem em arquivo de configuração: a resposta
é dizer o que falta, mesmo que o pedido seja para não perguntar nada.

## 2. Combinar o alvo com o usuário

- **Caminho.** Se o usuário não disse, pergunte. Nunca crie dentro do próprio `$SDD_WORKFLOW_HOME`:
  o projeto aninhado carregaria os dois `AGENTS.md` na mesma sessão.
- **Perfil.** `mvp` é o default e o recomendado. `full` só se o usuário pedir (tem mais rules
  always-on e os hooks de orquestração).
- **Git.** Ofereça `-Git` (init e commit inicial) quando a pasta ainda não for repositório.

Diretório que já existe é seguro: arquivo idêntico é pulado e arquivo diferente ganha backup antes.
Para conferir antes de escrever, rode primeiro com `-DryRun`.

## 3. Rodar

```bash
pwsh -NoProfile -File "$SDD_WORKFLOW_HOME/onboarding/new-project.ps1" -Path "<caminho>" -Git
# perfil completo: acrescente -Profile full · só simular: -DryRun
```

O `pwsh` existe em toda máquina com o Native-SDD instalado (o instalador depende dele também no
Linux/macOS). Leia a saída: `WARN` não é sucesso. O caso comum é o commit inicial falhar por falta
de `user.name`/`user.email` no git, e então o projeto foi criado e só o commit ficou para trás.
Relate isso ao usuário. Não faça o commit por ele nem escolha uma identidade git em nome dele.

Projeto que **já** tem `.claude/.scaffold-version` não se recria: para trazer a versão nova do
scaffold, use `-Update` (preserva o que o usuário customizou).

## 4. Depois

Diga ao usuário para abrir o Claude Code **dentro** da pasta do projeto e rodar `/setup`, que
preenche o contexto do projeto. Nesta sessão as instruções do projeto novo não estão carregadas.
