---
name: gh-address-comments
description: Ajudar a responder comentários de review/issue no PR aberto do GitHub para o branch atual usando gh CLI; verificar autenticação gh primeiro e solicitar ao usuário que se autentique se não estiver conectado.
metadata:
  short-description: Responder comentários em um review de PR do GitHub
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "echo \"[$(date)] GH Address Comments: Executed gh command to address PR comments\" >> ~/.claude/gh-address-comments.log"
---

# Gerenciador de Comentários de PR

Guia para encontrar o PR aberto do branch atual e responder seus comentários com gh CLI. Execute todos os comandos `gh` com acesso de rede elevado.

Pré-requisito: garanta que `gh` está autenticado (por exemplo, execute `gh auth login` uma vez), depois execute `gh auth status` com permissões escalonadas (inclua escopos workflow/repo) para que os comandos `gh` funcionem. Se o sandbox bloquear `gh auth status`, reexecute-o com `sandbox_permissions=require_escalated`.

## 1) Inspecionar comentários que precisam de atenção
- Execute scripts/fetch_comments.py que exibirá todos os comentários e threads de review no PR

## 2) Solicitar clarificação ao usuário
- Numere todas as threads de review e comentários e forneça um resumo curto do que seria necessário para aplicar uma correção
- Pergunte ao usuário quais comentários numerados devem ser respondidos

## 3) Se o usuário escolher comentários
- Aplique correções para os comentários selecionados

Notas:
- Se gh encontrar problemas de autenticação/taxa durante a execução, solicite ao usuário que se reautentique com `gh auth login`, depois tente novamente.