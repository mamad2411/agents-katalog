---
name: fechar-task
description: Use when implementation is verified and ready to ship for a Track task — commit, push, set status in_review with reviewer via MCP; never open a PR and never mark completed
---

# Fechar Task

## Visão geral

Híbrido de Superpowers `finishing-a-development-branch` + entrega Track.

**Anuncie:** "Usando fechar-task para enviar ao review."

**Pré-requisito:** `verificar-antes-de-enviar` verde **nesta** sessão. Se não rodou, volte e rode.

## Lei de ferro

```
COMMIT + PUSH OK → SÓ ENTÃO update_dev_task (in_review + reviewer)
NÃO ABRIR PR
NUNCA complete_dev_task / status completed
```

Se o push falhar → **não** mexa no status Track.  
Se o MCP falhar com **401** depois do push → invoque `setup`, depois retente `update_dev_task`.  
Se o MCP falhar por outro motivo depois do push → avise inconsistência (código no remote, Track desatualizado).

## Processo

### 1. Confirmar verificação

Sem evidência fresca de `verificar-antes-de-enviar` → pare e verifique.

### 2. Git: commit

Siga as regras do repo / usuário para commit (mensagem via HEREDOC se for o padrão do projeto).  
Não commitar secrets (`.env`, credentials).  
Não fazer commit se o humano não pediu e a regra do workspace exige pedido explícito — **exceto** quando o humano já pediu para fechar/enviar a task (este skill implica autorização de commit+push para essa entrega).

Se a regra do usuário for "só commit quando eu pedir": pergunte "Posso fazer commit e push agora?" antes do Step 3 — a menos que o pedido atual já seja explicitamente fechar/enviar.

### 3. Git: push

```bash
git push -u origin HEAD
```

(ou o remote/branch já configurados)

Branch: preferir `feat/**` quando o CI do remoto só roda nesses padrões.

**Push falhou?** Pare. Não chame MCP de status. Mostre o erro.

### 4. NÃO abrir PR

**Padrão do Contexto Certo:** commit + push da branch e colocar a task em review no Track.  
**Não** rode `gh pr create` nem abra PR no GitHub/GitLab.

Exceções só se o humano pedir **explicitamente** "abre o PR" / "cria o PR" nesta conversa.

Para `pullRequestLink` no MCP, use a **URL da branch no remote** (ex.: `https://github.com/org/repo/tree/feat/minha-branch`), não URL de PR.

### 5. Track MCP: `in_review`

Chame `update_dev_task` com:

- `releaseId` + `taskId`
- `status`: `in_review`
- `reviewerId`: quem pediu o trabalho / assigner  
  - Se ambíguo: `list_squad_members` + **pergunte**
- `pullRequestLink`: URL da branch no remote (não invente; omita se não souber montar)

**Proibido:** `complete_dev_task` e qualquer path que marque a task como concluída/completed.

### 6. Reportar ao humano

```markdown
## Entrega

- Branch: <url da branch no remote>
- Verificação: <comandos + resultado>
- Track: task <id> → in_review (reviewer: <nome>)
- PR: não aberto (humano abre se quiser)
- Próximo: review humano — agente não marca completed
```

### 7. Oferecer plano de QA (se feature pronta)

Depois do report, consulte o MCP: se **todas** as dev tasks da feature estão `in_review` ou `completed` (ignore `canceled`; design em `backlog` não bloqueia), **ofereça** — não execute sozinho:

> Feature \<nome\> parece pronta para QA. Quer que eu gere o plano de CTs manuais em `docs/qa/manual-tests/` (padrão Hous3)?

- Se o humano aceitar → invoque **`gerar-plano-qa`**
- Se recusar ou ignorar → pare; não grave CTs

## Opções se o humano ainda não quer push

Se a verificação passou mas o humano hesita, ofereça menu curto (estilo Superpowers):

1. Commit + push + `in_review` agora (sem PR)  
2. Só commit local (sem push / sem MCP)  
3. Manter working tree (não fechar ainda)  

Não invente merge na `main`/`staging` sem pedido. Não force-push. Não abra PR “por precaução”.

## Sinais vermelhos

| Pensamento | Realidade |
|------------|-----------|
| "Marco completed para limpar a fila" | Proibido |
| "Push falhou mas já atualizo o Track" | Ordem: push primeiro |
| "Reviewer sou eu mesmo sem perguntar" | Só se o MCP/humano deixou claro |
| "Sem PR o review fica incompleto" | Fluxo padrão: branch + Track `in_review`; PR só se o humano pedir |
| "Vou abrir o PR porque o gh está aí" | Proibido no padrão |
| "Verification da conversa passada basta" | Evidência fresca |

## Nunca

- Abrir PR (`gh pr create` ou equivalente) sem pedido explícito do humano
- `complete_dev_task`
- Merge/deploy em nome do humano sem pedido
- Force push em main/master
- Atualizar Track com status de sucesso após push falho
- Pular verificação porque "é só um typo"
