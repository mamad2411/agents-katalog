# Release Candidate Freeze

## Objetivo

Homologar a composicao real **no ambiente staging** antes de producao, sem voltar ao modelo de staging acumulativo.

A RC existe para o **humano validar no staging**. Criar a branch `rc/*` sem promover o snapshot para `staging` **nao conclui** a criacao da RC.

## Contrato

- `Working` continua limitado a no maximo 5 tasks.
- `dev` integra somente branches individuais `task-{id}`.
- Uma RC contem de **1 a 5** tasks ja integradas/aceitas para composicao.
- A branch da RC usa `rc/X.Y.Z-rc.N`.
- A RC nasce do `master` remoto atual e recebe somente os deltas das tasks listadas no manifesto.
- O manifesto `.release/rc-manifest.json` e obrigatorio e imutavel depois do freeze.
- **`staging` DEVE representar exatamente o snapshot congelado da RC** (mesmo SHA de tip da branch `rc/X.Y.Z-rc.N` no repositorio pai e os mesmos gitlinks/pins do manifesto).
- Qualquer mudanca de SHA, task, gitlink, versao ou arquivo depois do freeze invalida a homologacao e exige nova RC.
- `master` recebe somente a **mesma RC homologada**, com os mesmos SHAs do manifesto aprovado.
- Nunca publicar o branch agregado `staging` como origem de `master`.
- Nunca criar RC pai/issue agregadora. RC e artefato tecnico de release, nao task de produto.

## Criterio de conclusao de "criar RC"

A criacao de RC so esta **concluida** quando **todas** as condicoes abaixo forem verdadeiras:

1. Branch `rc/X.Y.Z-rc.N` publicada com manifesto `frozen: true`.
2. **`origin/staging` (pai e modulos pinados no manifesto) aponta para o mesmo snapshot da RC** — HEAD de staging = tip da RC no app pai; submodulos/pins iguais ao manifesto.
3. Pipeline de deploy/build de staging disparado ou em andamento a partir desse snapshot (quando o repo tiver workflow de deploy em push de `staging`).
4. Label `rc/X.Y.Z-rc.N` aplicada em **cada** issue inventariada no manifesto (criada no repo se ainda nao existir).
5. Tasks inventariadas movidas para **In Review** somente **depois** do item 2.

Enquanto `staging` divergir da RC, o resultado e `NEXT_ACTION` de DevOps: **promover/resetar staging para o tip da RC**. Nao encerre a rodada como RC pronta so com a branch `rc/*`.

## Promocao obrigatoria para staging

- A promocao e **parte do rito de freeze**, nao um passo opcional pos-homologacao.
- Preferir atualizar `staging` para o tip da RC (fast-forward ou **reset** para o SHA da RC).
- Se o historico de `staging` divergir (RC anterior, commits extras), **resetar** `staging` para o tip da RC e o contrato. Staging acumulativo e proibido.
- Quando regras do GitHub bloquearem force-push, usar o mecanismo autorizado do repo (PR de reset `automation/reset-rc-…-staging`, bypass de regras por identidade de automacao, ou workflow de reset). O objetivo e o mesmo: **HEAD de staging = tip da RC**.
- Falha de promocao a staging = RC **nao entregue**; registrar evidencia e insistir no reset, nao no merge de historicos divergentes que misturem commits fora do manifesto.

## Manifesto minimo

```json
{
  "version": "1.10.27",
  "rc": 1,
  "branch": "rc/1.10.27-rc.1",
  "baseMaster": "<sha>",
  "tasks": [821, 826, 827],
  "repositories": {
    "ControleOnline/app-community": "<sha>",
    "ControleOnline/ui-common": "<sha>"
  },
  "frozen": true
}
```

Regras:
- `tasks`: 1..5 numeros unicos.
- `branch` deve corresponder a `version` + `rc`.
- `baseMaster` e todos os SHAs devem ser completos e registrados antes da homologacao.
- Cada gitlink do pai deve apontar para commit ja integrado na branch de RC correspondente do submodulo.
- O manifesto homologado e comparado byte-a-byte/semanticamente no gate de master.

## Label de identificacao da RC nas issues

Ao concluir o freeze (manifesto `frozen: true` + staging alinhado), **obrigatorio** aplicar em **cada** issue inventariada no manifesto a label GitHub cujo nome e exatamente o identificador da branch da RC:

- Formato: `rc/X.Y.Z-rc.N` (igual ao campo `branch` do manifesto, sem prefixo extra).
- Exemplo: branch `rc/1.10.27-rc.1` → label `rc/1.10.27-rc.1` em todas as issues de `tasks`.
- Criar a label no repositorio da issue se ainda nao existir (cor sugerida `#5319E7`, descricao `Release Candidate X.Y.Z-rc.N`).
- A label e o marcador operacional para filtrar/identificar no board quais issues pertencem a qual RC; nao substitui manifesto, coluna `In Review` nem gate de Security.
- Em `rc.N+1` (nova RC apos correcao): aplicar a label da **nova** RC; a label da RC anterior pode permanecer para historico ou ser removida a criterio do Manager — nao e bloqueio.
- A ausencia da label **nao** invalida o manifesto nem o gate de master; e higiene de identificacao e deve ser corrigida na mesma rodada de criacao da RC (DevOps no freeze; Manager pode completar ao mover para `In Review`).

## Freeze (ordem obrigatoria)

1. Atualize `master`.
2. Selecione no maximo 5 tasks elegiveis.
3. Crie a RC a partir desse `master`.
4. Integre cada task separadamente, registrando a ordem e o SHA resultante.
5. Gere o manifesto.
6. Marque `frozen: true`.
7. **Promova o snapshot para `staging` ate `origin/staging` coincidir com o tip da RC** (reset se necessario).
8. Confirme runtime/deploy de staging (workflow ou evidencia de servidor) a partir desse SHA.
9. **Aplique a label `rc/X.Y.Z-rc.N` em cada issue inventariada** (criar a label no repo se necessario).
10. Manager move as tasks inventariadas para **In Review** (homologacao humana no staging).
11. Se qualquer correcao for necessaria apos o freeze, **nao altere a RC homologada**: gere `rc.N+1` e repita a promocao a staging (e a label da nova RC).
12. Quando o humano autorizar **Deploy**, promova a **mesma** RC congelada para `master`.

## Gate de producao

Antes de master:
- manifesto existe e esta congelado;
- RC contem de 1 a 5 tasks;
- HEAD da RC e os SHAs por repositorio sao os mesmos homologados em staging;
- staging nao recebeu commit posterior ao snapshot;
- build/smokes da composicao passaram (ou `force_deploy` explicitamente registrado, se politica ativa);
- nenhuma mudanca fora do manifesto entrou;
- submodulos nao sofreram downgrade silencioso;
- versao estavel final deriva da RC homologada.

Se qualquer item divergir, falhar fechado e gerar nova RC.
