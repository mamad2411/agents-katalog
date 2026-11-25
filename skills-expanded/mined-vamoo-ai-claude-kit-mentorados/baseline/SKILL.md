---
name: baseline
description: >-
  Postura de ambiente e segurança de app web (Vite/Next + Supabase + Vercel +
  n8n) em 8 pilares — bundle, RLS, auth, rate limit, cache, observabilidade,
  segredos, perímetro. Dois modos: CONSTRUIR (projeto novo nasce apto) e AUDITAR (app em
  produção está apto?). Use em "está pronto pra prod", "auditar produção",
  "hardening", "app novo do zero".
allowed-tools:
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/doctor.sh" *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/doctor.sh *)'
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/collect.sh" *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/collect.sh *)'
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/splinter.sh" *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/splinter.sh *)'
  - 'Bash(node "${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/render.mjs" *)'
  - 'Bash(node ${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/render.mjs *)'
---

# baseline — Ambiente e Segurança

Depois de uma compactação só o começo desta skill volta ao contexto: leia o arquivo de `references/` no passo que o cita, mesmo que já tenha lido antes.

> Origem: escrito a partir da auditoria de um app real em produção (React + Vite
> + Supabase + Vercel). Quatro dos oito pilares aqui — sourcemap, rate limit de
> endpoint próprio, cache headers e error tracking — costumam só ser lembrados
> depois do primeiro incidente. Esta skill existe para inverter essa ordem.

Um padrão, dois modos. **A skill é o método; o contrato é o dado.** O método é
genérico e mora aqui. O contrato mora no repo auditado, em
`.context/docs/baseline.md`, e é ele que diz o que vale *neste* projeto — mesmo
modelo que o `/ship` já usa ao ler `.context/docs/deploy.md`.

---

## As quatro invariantes (nunca quebre)

1. **Dado indisponível nunca é evidência de risco.** Todo check resolve em
   `conforme`, `nao_conforme` ou `nao_medido` **com o motivo**. Nunca
   "provavelmente ok", nunca silêncio.
2. **Medição ausente nunca é veredito limpo.** Run que não mediu nada sai com
   exit≠0. Um relatório vazio parece aprovação e é o pior resultado possível.
3. **Cobertura é declarada.** "Nenhum achado" significa "nenhum entre o que foi
   medido". A tabela de cobertura é obrigatória no report — sem ela o report não
   está pronto.
4. **Leitura de código responde "existe?", não "funciona?".** Achado que afirma
   *comportamento* exige prova de execução. (15/08/2026: três itens foram
   fechados como "auditado e PRONTO" por grep; a gravação do cliente mostrou os
   três quebrados.)

## Regras duras

As invariantes e a regra READ-ONLY do Modo AUDITAR valem inteiras; aqui fica o que elas
não dizem.

- **Semgrep sempre com `--metrics=off` e ruleset fixo.** `--config auto` faz login
  no registry e envia a URL do projeto. **Proibido em repo de cliente.**
- **Nunca traga o valor de um segredo pro contexto.** Para provar que existe:
  `bash "${CLAUDE_PLUGIN_ROOT}/scripts/env-tem-chave.sh" .env.local KEY` (diz `presente`,
  `vazia` ou `ausente`; o deny nega `grep -c` no `.env`). Fingerprint no report, nunca o valor.
- **Ferramenta que o `doctor.sh` disse faltar deixa o pilar `nao_medido`.** Não
  preencha com heurística e chame de cobertura.

---

## Fronteira — o que esta skill NÃO é

A tabela baseline × `secscan` × auditoria × `verificacao` está em [references/fronteira.md](references/fronteira.md).

No pilar de código, **chame `secscan`** — não refaça SAST aqui.
Juiz adversarial na fase 2: um `revisor` fresco por finding `CRITICAL`/`HIGH` (`Agent` com `subagent_type: kit-vamoo:revisor`), todos em paralelo numa mensagem só. O contrato do juiz é o da `auditoria-seguranca` (`skills/auditoria-seguranca/references/fase-5-veredito.md`, pergunta 3), sem cópia aqui: o que muda por causa do formato de finding da baseline (o que entra no dispatch, para onde vai o refutado, o rebaixado) está em [references/fase2-julgar.md](references/fase2-julgar.md), passo 5.

Auditoria com fan-out por área: o workflow `audit-multidim` (o plugin entrega, como `/kit-vamoo:audit-multidim`) só roda quando a pessoa pedir um workflow; sem esse pedido, faça o fan-out com um `Agent` por área, numa mensagem só, e ofereça o workflow em uma linha. Com o workflow ou sem ele, todo `CRITICAL`/`HIGH` que sobrar passa pelo juiz acima: o juiz do workflow descarta na dúvida, e aqui descartar exige prova.

---

## Modo CONSTRUIR

App novo, feature nova, ou primeira ida ao ar. Pode escrever código.

1. **Existe `.context/docs/baseline.md`?**
   Não → gere a partir de `references/contrato-template.md` e preencha o que der
   sem perguntar (stack, superfícies, runners). O que depende de decisão
   (retenção, quem é dono da rotação) fica marcado `PENDENTE:` — não invente.
2. **Leia só o pilar que a tarefa toca.** Tocou build/CSP → `01`. Tocou migration
   → `02`. Tocou rota/papel → `03`. Tocou edge/webhook ou login → `04`. Tocou
   query/lista → `05`. Tocou tratamento de erro ou log → `06`. Tocou env/chave → `07`.
   Subiu host, painel ou domínio novo → `08`.
   Carregar os oito de uma vez é desperdício de contexto.
3. **Aplique o Contrato do pilar** usando o bloco "Como implementar" como ponto
   de partida, adaptado ao stack real do projeto — não cole cego.
4. **Prove.** Rode o comando do bloco "Como provar" e cole o output. Sem output,
   o item fica `nao_medido`, não `conforme`.
5. **Registre.** Atualize a tabela de estado do contrato. Se decidiu
   conscientemente ficar fora do padrão, isso é uma **exceção aceita** e vai na
   tabela com motivo, dono e data de revisão — não fica implícito, senão a próxima
   auditoria reabre o assunto e você paga de novo pela mesma decisão.

### A regra que evita a maior parte do retrabalho

**Ordem importa em dois pares.** Ligar `dropConsole`/`drop_debugger` antes de
existir error tracking apaga o único rastro que você teria em produção. E criar
tabela antes da policy deixa uma janela em que ela nasce aberta ou deny-all
silencioso. Nos dois casos: a segunda peça entra **no mesmo PR** que a primeira.

---

## Modo AUDITAR

App em produção. **READ-ONLY é iron rule** — mesma regra do `secscan`.

> Nunca modifique, mova ou crie código/config no projeto auditado. Nunca faça DDL
> no banco (os lints rodam como `select`, sem criar schema `lint`). Nunca teste
> endpoint de terceiro. As únicas escritas permitidas são os artefatos da
> auditoria: `findings.json`, o report, o contrato e o registro de vereditos
> (`.context/docs/security/vereditos.md`).
> Requisição além do `curl -sSI` do pilar 08 é a fase dinâmica: só quando
> pedida, nunca em produção, alvo pela política de `08-perimetro-dinamico.md`.

Quatro fases. Aplicar correção é **fora** deste modo — vai pro modo CONSTRUIR,
com contexto de regressão.

| Fase | O que faz | Escreve |
|---|---|---|
| **1 Medir** | `doctor.sh` → `collect.sh`. Determinístico, zero julgamento | `findings.json` |
| **2 Julgar** | Severidade + confiança. Aplica exceções do contrato. Juiz nos `CRITICAL`/`HIGH`; falso-positivo só com prova (`fase2-julgar.md`, passo 5) e registrado em `.context/docs/security/vereditos.md` | `report.md`, `vereditos.md` |
| **3 Propor** | Correção concreta + comando de reconferência, por finding | nada |
| **4 Reconferir** | Roda o comando de reconferência e cola o output | nada |

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/doctor.sh"     # 1. o que dá pra medir aqui
bash "${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/collect.sh"    # 2. mede (exit 3 = não mediu nada)
bash "${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/splinter.sh"   # 3. banco, se houver acesso
node "${CLAUDE_PLUGIN_ROOT}/skills/baseline/scripts/render.mjs" "/tmp/baseline-$(basename "$PWD")/findings.json"
```

Da raiz do repo, e cada linha se basta: o shell não guarda variável de uma chamada para a
outra. O Claude Code preenche o `${CLAUDE_PLUGIN_ROOT}` no texto ao carregar a skill. Doctor, collect
e render usam `/tmp/baseline-<nome do repo>`, o `--out` padrão do doctor e do collect; o render grava o
`report.md` ao lado do `findings.json` e lê dali o `tools.json`.

`doctor.sh` sempre roda primeiro. Descobrir que falta `jq` no meio do collect é
caro; descobrir antes custa 200 ms.

### Fase 2 — julgar e formato de finding

**Leia [references/fase2-julgar.md](references/fase2-julgar.md)** antes de julgar ou
escrever qualquer finding. Sem comando de reconferência o finding está incompleto.

---

## Os oito pilares

Carregue **só o que a tarefa toca**. Cada arquivo tem a mesma estrutura:
Contrato · Como implementar · Como provar · Armadilhas.

| # | Pilar | Referência | Núcleo |
|---|---|---|---|
| 01 | Frontend / bundle | `references/01-frontend.md` | sourcemap, `VITE_`/`NEXT_PUBLIC_`, CSP + headers, orçamento de bundle |
| 02 | Banco / RLS | `references/02-banco.md` | RLS, policy, `SECURITY DEFINER`, view, grant, storage |
| 03 | Auth / permissão | `references/03-auth.md` | sessão, MFA, RBAC, gate de rota **e sua contrapartida** |
| 04 | Limites / abuso | `references/04-limites.md` | rate limit, quota de LLM, webhook secret, `verify_jwt` |
| 05 | Carga / cache | `references/05-carga.md` | paginação, cache em 3 camadas, índice, gargalo, balanceamento |
| 06 | Observabilidade | `references/06-observabilidade.md` | error tracking, log estruturado, alerta, auditoria |
| 07 | Segredos | `references/07-segredos.md` | inventário, scan de HEAD+histórico, rotação, exceções |
| 08 | Perímetro | `references/08-perimetro.md` | inventário de hosts, headers na borda, painel interno, versão exposta |
| 08+ | Fase dinâmica | `references/08-perimetro-dinamico.md` | ZAP passivo + sondas com requisição; opcional |

O contrato por projeto: `references/contrato-template.md`.

---

## Adotar num repo pela primeira vez

**Leia [references/adotar.md](references/adotar.md)** antes de adotar num repo que ainda
não tem `.context/docs/baseline.md` (ordem do contrato, primeiro run, ordem entre repos).
