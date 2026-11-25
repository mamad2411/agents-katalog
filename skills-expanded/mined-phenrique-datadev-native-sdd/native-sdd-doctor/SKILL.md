---
name: native-sdd-doctor
description: Diagnostica a instalação do Native-SDD nesta máquina sem alterar nada — CLIs, baseline do ~/.claude, versão instalada contra a do checkout. Use quando o usuário perguntar se o Native-SDD está instalado, funcionando ou atualizado, ou quando o nsp, um hook ou a statusline do framework não responder.
---

# Diagnóstico do Native-SDD

Só leitura: o instalador roda em modo `-Check`, que relata e não escreve.

## 1. Achar o framework

```bash
echo "$SDD_WORKFLOW_HOME" && test -d "$SDD_WORKFLOW_HOME/onboarding" && echo OK
```

Variável vazia ou pasta ausente já é o diagnóstico: o Native-SDD não está instalado, ou o checkout
saiu de lugar depois da instalação. Diga isso e indique reinstalar a partir do checkout (ou pelo
bootstrap remoto do README do projeto). Não procure o checkout pelo disco nem em arquivo de
configuração: a resposta é dizer o que falta, mesmo que o pedido seja para não perguntar nada.

## 2. Rodar o check

Windows:

```bash
pwsh -NoProfile -File "$SDD_WORKFLOW_HOME/onboarding/install.ps1" -Check -NonInteractive
```

Linux/macOS:

```bash
bash "$SDD_WORKFLOW_HOME/onboarding/install.sh" --check --non-interactive
```

## 3. Relatar

Resuma em poucas linhas: versão instalada × versão do checkout, o que está `OK` e cada `WARN`/`FAIL`
com a ação que o próprio instalador sugere. O código de saída zero não basta, leia as linhas de
aviso. Se a statusline mostrar `5h --`, confira a linha `Relógio` antes de suspeitar do script: o
Claude Code descarta a janela de 5h quando o relógio local já passou do reset. Não corrija nada sem
o usuário pedir. Para aplicar, a skill `native-sdd-atualizar` (ou o instalador sem `-Check`) é o
caminho.
