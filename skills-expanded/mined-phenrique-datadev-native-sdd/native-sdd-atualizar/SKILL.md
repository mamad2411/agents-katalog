---
name: native-sdd-atualizar
description: Atualiza o Native-SDD desta máquina — traz a versão nova do framework e reaplica o baseline do ~/.claude, mostrando antes o que vai mudar.
disable-model-invocation: true
---

# Atualizar o Native-SDD

Só roda quando o usuário chama `/native-sdd-atualizar`: mexe no `~/.claude` dele.

## 1. Achar o framework

```bash
echo "$SDD_WORKFLOW_HOME" && test -d "$SDD_WORKFLOW_HOME/onboarding" && echo OK
```

Vazia ou ausente: pare e diga que o Native-SDD não está instalado (ou o checkout saiu de lugar), e
que a saída é reinstalar a partir do checkout ou pelo bootstrap remoto do README do projeto. Não
procure o checkout pelo disco nem em arquivo de configuração.

## 2. Trazer a versão nova

Depende de como o checkout chegou:

- **Clone git** (`git -C "$SDD_WORKFLOW_HOME" rev-parse --git-dir` responde):
  ```bash
  git -C "$SDD_WORKFLOW_HOME" status --short
  git -C "$SDD_WORKFLOW_HOME" pull --ff-only
  ```
  Com mudança local ou `pull` recusado, pare e mostre ao usuário. Não faça stash, reset nem merge.
- **Sem `.git`** (instalado pelo bootstrap, em `~/.claude/.native-sdd-src`): a atualização é rodar o
  bootstrap de novo, que baixa a última release. Mostre o comando do README do projeto e deixe o
  usuário rodar. Não baixe nada por conta própria.

## 3. Mostrar e aplicar

Simule primeiro e resuma o que muda:

```bash
pwsh -NoProfile -File "$SDD_WORKFLOW_HOME/onboarding/install.ps1" -DryRun -NonInteractive   # Windows
bash "$SDD_WORKFLOW_HOME/onboarding/install.sh" --dry-run --non-interactive                 # Linux/macOS
```

Com o ok do usuário, rode o mesmo comando sem `-DryRun`/`--dry-run`. Arquivo do `~/.claude` que o
usuário editou fica preservado e aparece listado. Não use `-OverwriteCustom` sem ele pedir.

Projetos já criados não mudam com isto: cada um se atualiza com
`new-project.ps1 -Path <projeto> -Update`.
