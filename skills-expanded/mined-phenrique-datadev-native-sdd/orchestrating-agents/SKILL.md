---
name: orchestrating-agents
description: Padrões para coordenar agentes irmãos rodando em paralelo em panes/tabs/sessões separadas, e receitas opcionais para dirigir esses panes via herdr quando o binário está instalado. Use quando o pedido envolver várias sessões concorrentes do agente (panes/tabs/terminais separados), esperar uma sessão irmã terminar, ou montar um workspace de multiplexação de terminal para agentes. Não use para subagentes dentro da mesma sessão (isso é a tool Agent nativa) nem para ver quem está ativo no projeto (isso é o /peers). Funciona como documentação mesmo sem o herdr instalado.
---

# orchestrating-agents

Coordenação de **agentes irmãos concorrentes** — várias sessões/panes trabalhando ao mesmo tempo no
mesmo projeto. Duas camadas, independentes:

1. **Os 3 padrões de coordenação** — valem SEMPRE, com ou sem qualquer ferramenta. São a mesma
   disciplina já citável no command `/peers` (coordenação file-based entre sessões do Claude Code).
2. **Receitas com `herdr`** (opcional) — se o binário `herdr` estiver instalado, você pode criar e
   dirigir workspaces/tabs/panes por CLI para orquestrar agentes em panes separados. Baseado só na
   doc pública (https://herdr.dev/docs/). Sem o binário, esta seção é só referência.

## Quando usar
Gatilhos: "coordena os agentes", "roda os agentes em paralelo", "espera o agente irmão terminar",
"monta um workspace de panes pros agentes", "orquestra as sessões concorrentes". Se o pedido for
sobre o quadro de presença entre sessões do Claude Code (quem está trabalhando agora, caixa de
recados), isso é o command **`/peers`** — esta skill cobre os **padrões** e a **camada herdr**.

## Os 3 padrões de coordenação (sempre válidos)

Qualquer coordenação entre agentes concorrentes deve seguir estes três — mesma redação conceitual
do `/peers` (não divergir):

1. **Endereçar por rótulo estável, nunca por identificador volátil.** O id que identifica uma
   sessão/pane no instante (session_id, pane id) é **efêmero**: vale só enquanto aquela sessão/pane
   vive e **não sobrevive** a fechar/reabrir. É chave de entrega *naquele instante*, não uma
   referência durável — nunca o anote em docs/KB como "o agente X" nem presuma que o mesmo id volta
   depois. Para **reconhecer quem** é um irmão, use o rótulo estável e legível (o que ele está
   fazendo: branch + tarefa/summary), não o identificador de runtime.

2. **Reagir a evento, nunca ficar em laço de espera.** Leia o estado **sob demanda**, movido a
   **evento** — **jamais** um `sleep`-loop sondando à espera de que um irmão termine. Um sinal
   chega quando você consulta no próximo ponto natural do seu trabalho, não instantaneamente. Nunca
   bloqueie a sessão esperando ativamente: siga seu trabalho e cheque o estado no próximo pull. (É a
   razão de designs de coordenação serem file-based/event-driven, sem daemon de sondagem.)

3. **Verificação independente ao final — "terminou" é alegação, não evidência.** Quando um irmão
   avisa que concluiu ou que "passou", trate como **alegação**, não prova. Antes de confiar e seguir
   em cima do trabalho dele, **rode você mesmo** a verificação que importa (build, testes, critério
   de aceite) em contexto próprio — como o gate fresh-context da orquestração, que existe justamente
   para não deixar quem produziu o resultado ser o único a atestá-lo.

## Receitas com `herdr` instalado (opcional)

Primeiro **detecte** o binário — a skill funciona como documentação mesmo sem ele:

```powershell
if (Get-Command herdr -ErrorAction SilentlyContinue) {
    # herdr disponível — as receitas abaixo funcionam
} else {
    Write-Warning 'herdr não está no PATH — receitas abaixo são só referência. Instale com: install.ps1 -WithHerdr (e adicione ~/.claude/tools/herdr/<versão> ao PATH).'
}
```

`herdr` é um multiplexador de terminal controlável por CLI sobre um socket local: workspaces contêm
tabs, tabs contêm panes, e você dirige tudo por comando. Receitas (sintaxe da doc pública
https://herdr.dev/docs/socket-api/ — confira `herdr --help` / `herdr api schema` na sua versão):

| Objetivo | Comando |
|----------|---------|
| Confirmar que o servidor responde | `herdr status` |
| Criar um workspace nomeado por tarefa | `herdr workspace create --cwd ~/projeto --label native-sdd` |
| Listar / focar workspaces | `herdr workspace list` · `herdr workspace focus <workspace_id>` |
| Criar uma tab (ex.: uma por agente) | `herdr tab create --label agente-a` |
| Dividir um pane para um irmão | `herdr pane split w1:p1 --direction right` |
| Rodar um comando/agente num pane | `herdr pane run w1:p2 "npm test"` |
| Ler a saída recente de um pane | `herdr pane read w1:p2 --source recent --lines 50` |
| Mandar texto/entrada a um pane | `herdr pane send-text <pane_id> "texto"` |
| **Esperar um agente terminar (evento, não poll)** | `herdr wait agent-status w1:p1 --status done` |
| Snapshot JSON da sessão viva | `herdr api snapshot` |

**Mapeando de volta aos 3 padrões:**

- **Rótulo estável (1):** endereçe panes pelo `--label` que você deu (a tarefa/branch), e trate os
  ids tipo `w1:p2` como voláteis — reobtenha-os de `herdr workspace list` / `herdr api snapshot` a
  cada vez, nunca os persista como "o agente X".
- **Watcher, não poll (2):** para saber quando um irmão terminou, use **`herdr wait agent-status
  ... --status done`** (bloqueia até o evento) — **não** um loop de `herdr pane read` + `sleep`
  sondando a saída.
- **Verificação independente (3):** quando `herdr wait` retorna "done", isso é a **alegação** do
  irmão. Rode você mesmo o gate (testes/build) — de preferência num pane/contexto próprio — antes de
  seguir em cima do resultado dele.

## O que NÃO fazer
- **Não** sonde em `sleep`-loop o estado de um irmão — use o mecanismo de espera por evento
  (`herdr wait`, ou o pull sob demanda do `/peers`).
- **Não** persista ids voláteis (session_id, `w1:p2`) como referência durável — reobtenha do
  snapshot; enderece por rótulo estável.
- **Não** confie no "terminou" de um irmão sem rodar a verificação você mesmo.
- **Não** presuma que o `herdr` está instalado — detecte com `Get-Command herdr` e degrade para
  "só documentação" se faltar.
- **Não** invente flags do `herdr` de memória — confira `herdr --help` / `herdr api schema` na sua
  versão antes (a sintaxe da CLI evolui).
