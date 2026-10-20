---
name: devopeiro
description: Resolve incidentes Kubernetes de ponta a ponta sem interação humana. Dado um namespace e a descrição do problema, investiga autonomamente no cluster e no repositório local, executa correções iterativas até todos os pods do escopo estarem Running/Ready, e gera documentação completa do incidente (investigation.md, action_log.md, POSTMORTEM.md). Use esta skill sempre que o usuário reportar que uma aplicação no Kubernetes não está funcionando, pods em CrashLoopBackOff, serviço indisponível, erro de deploy, banco não conecta, ou qualquer problema em cluster Kubernetes — mesmo que o usuário não use termos técnicos como "incidente" ou "troubleshoot". Ative também com frases como "minha app caiu", "o pod não sobe", "algo errado no cluster", "aplicação fora do ar no k8s", "me ajuda a resolver esse problema no Kubernetes".
---

## O que esta skill faz

Recebe a descrição de um incidente Kubernetes do usuário e executa três fases em sequência, sem nenhuma interação humana:

1. **Investigação** — coleta evidências no cluster e no repositório, formula hipótese de causa raiz
2. **Correção iterativa** — aplica correções, verifica o estado, repete até convergir ou atingir o limite
3. **Documentação** — gera artefatos completos do incidente

Ao final, todos os documentos são salvos em `incidents/YYYY-MM-DD-<slug>/` na raiz do projeto.

---

## Input esperado do usuário

A skill precisa de dois elementos para operar:
- **Namespace** onde a aplicação reside
- **Descrição do problema** (pode ser vaga — "não está funcionando" é suficiente)

Se o namespace não for mencionado, assuma `default` e registre essa suposição no `investigation.md`.

---

## Arquitetura: três subagentes sequenciais

Execute **sempre** nesta ordem. Cada subagente recebe os artefatos do anterior como contexto.

---

### Subagente 1 — INVESTIGADOR

**Objetivo:** Entender o estado atual do cluster e do repositório para formular uma hipótese de causa raiz.

**Ferramentas disponíveis:** MCP Kubernetes (`kubectl_get`, `kubectl_describe`, `kubectl_logs`) + leitura de arquivos do repositório local.

**Sequência de investigação:**

1. `kubectl get pods -n <namespace> -o wide` — panorama geral dos pods
2. `kubectl get deployments,services,pvc,secrets,configmaps -n <namespace>` — recursos de suporte
3. Para cada pod com problema (não `Running/Ready`):
   - `kubectl describe pod <nome> -n <namespace>` — eventos e configuração
   - `kubectl logs <nome> -n <namespace> --tail=50` — logs atuais
   - `kubectl logs <nome> -n <namespace> --previous --tail=50` — logs do crash anterior (se aplicável)
4. Procurar manifests no repositório (`k8s/`, `manifests/`, `deploy/`, raiz do projeto) e comparar com o que está no cluster — divergências são causa raiz em potencial

**Critérios para parar a investigação:** Quando houver evidências suficientes para formular uma hipótese. Não investigar recursos fora do namespace e escopo dados pelo usuário.

**Output — `incidents/YYYY-MM-DD-<slug>/investigation.md`:**

```markdown
# Investigação do Incidente — <data> — <slug>

## Escopo
- Namespace: <namespace>
- Problema relatado: <descrição do usuário>

## Estado do cluster no momento da investigação
[kubectl get pods com status e nó de cada pod]

## Evidências coletadas
[Para cada pod com problema: describe resumido + logs relevantes]

## Divergências repositório vs cluster
[Se encontradas: o que o manifesto diz vs o que está rodando]

## Hipótese de causa raiz
[Causa principal + causas secundárias em cascata, se houver]

## Plano de correção
[Ações planejadas em ordem de execução]
```

---

### Subagente 2 — CORRETOR

**Objetivo:** Executar o plano de correção e iterar até todos os pods do escopo estarem `Running/Ready` ou atingir o limite de 10 tentativas.

**Ferramentas disponíveis:** MCP Kubernetes completo (`kubectl_patch`, `kubectl_delete`, `kubectl_rollout`, `kubectl_scale`, `kubectl_apply`, `kubectl_get`, `kubectl_describe`, `kubectl_logs`).

**Loop de correção:**

```
PARA cada iteração (máximo 10):
  1. Ler o plano de correção do investigation.md (ou re-investigar se iteração > 1)
  2. Aplicar a próxima correção
  3. Aguardar estabilização (verificar pods a cada ~15s, até 2 minutos)
  4. kubectl get pods -n <namespace>
  5. SE todos os pods do escopo estão Running/Ready → encerrar com sucesso
  6. SE não → re-investigar o estado atual (sem assumir hipótese anterior)
     e formular próxima correção
FIM DO LOOP
```

**Regras importantes:**
- Registrar cada ação com timestamp antes de executar
- Ao re-investigar entre iterações, não assumir que a hipótese anterior estava correta — o cluster pode ter revelado um problema diferente
- Problemas de `Multi-Attach` (PVC RWO em nós diferentes): deletar pods antigos com `--grace-period=0` e remover ReplicaSets obsoletos para liberar o volume
- Se o mesmo pod continua sendo recriado por um ReplicaSet antigo, deletar o ReplicaSet, não apenas o pod

**Critério de sucesso:** `kubectl get pods -n <namespace>` mostra todos os pods do escopo com `STATUS=Running` e `READY` igual ao esperado (ex: `1/1`).

**Se atingir 10 iterações sem convergir:**
- Parar imediatamente
- Registrar estado atual do cluster
- Avisar o usuário: "Atingi o limite de 10 tentativas de correção sem conseguir estabilizar todos os pods. O estado atual do cluster e todas as ações executadas estão documentados em `incidents/<pasta>/`. Intervenção manual necessária."
- Continuar para o Subagente 3 para documentar o estado parcial

**Output — `incidents/YYYY-MM-DD-<slug>/action_log.md`:**

```markdown
# Log de Ações — <data> — <slug>

## Status final
[RESOLVIDO / PARCIALMENTE RESOLVIDO — <N> iterações]

## Estado final dos pods
[kubectl get pods output]

## Ações executadas

### Iteração 1 — <timestamp>
**Hipótese:** <causa identificada>
**Ação:** <o que foi executado e por quê>
**Resultado:** <o que aconteceu após a ação>
**Estado dos pods após:** <Running/CrashLoopBackOff/etc>

### Iteração 2 — <timestamp>
[...]
```

---

### Subagente 3 — DOCUMENTADOR

**Objetivo:** Consolidar toda a informação coletada nas fases anteriores em um pós-mortem completo e reutilizável.

**Input:** `investigation.md` + `action_log.md` da pasta do incidente.

**Output — `incidents/YYYY-MM-DD-<slug>/POSTMORTEM.md`:**

```markdown
# Pós-Mortem: <título descritivo do incidente>

**Data do incidente:** YYYY-MM-DD
**Duração:** <início até resolução>
**Severidade:** Crítica / Alta / Média / Baixa
**Status:** Resolvido / Parcialmente Resolvido
**Namespace:** <namespace>

---

## Resumo executivo
[2-3 frases: o que quebrou, por que, como foi resolvido]

---

## Linha do tempo
| Horário | Evento |
|---|---|
[timestamps reais das ações do action_log + momentos-chave]

---

## Causa raiz
[Causa principal com evidências diretas — logs, eventos, comandos executados]

### Causas secundárias (cascata)
[Se houver problemas que foram consequência da causa principal]

---

## Impacto
- **Disponibilidade:** <percentual ou descrição>
- **Pods afetados:** <lista>
- **Dados:** <perda de dados ou não>

---

## Resolução aplicada
[Descrição técnica do que foi feito, com os patches/comandos exatos aplicados em blocos de código]

---

## Lições aprendidas
### O que deu errado
### O que funcionou bem

---

## Ações preventivas
| # | Ação | Prazo |
|---|---|---|

---

## Guia para incidentes futuros

### Sintomas que indicam este problema
### Passos de diagnóstico
```bash
# comandos exatos para identificar o problema
```
### Passos de correção
```bash
# comandos exatos para corrigir
```
### Armadilhas conhecidas
[O que pode dar errado durante a correção e como evitar]
```

---

## Convenções de nomenclatura

- **Slug do incidente:** primeiras palavras do problema relatado em kebab-case. Ex: `postgres-crashloopbackoff`, `app-econnrefused`, `pod-pending-pvc`
- **Pasta:** `incidents/YYYY-MM-DD-<slug>/`
- **Data:** data real do incidente no formato YYYY-MM-DD

---

## Comportamento em caso de incidente não resolvido

Se o Subagente 2 encerrou por limite de tentativas:
- O `POSTMORTEM.md` deve ter `Status: Parcialmente Resolvido`
- A seção "Resolução aplicada" deve documentar o que foi tentado e por que não convergiu
- A seção "Ações preventivas" deve incluir como retomar a investigação manualmente
- Avisar o usuário ao final com o caminho da pasta do incidente
