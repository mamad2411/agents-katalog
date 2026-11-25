---
name: powerapps-canvas
description: "Use quando o trabalho for Power Apps Canvas: criar ou alterar tela, galeria, modal, toast, loading, filtro, aba ou formulário; escrever ou corrigir fórmula Power Fx; gerar ou revisar YAML .pa.yaml para colar no Studio (\"não cola\", PA2108, `;` ou `;;`); combo/ComboBox que não acha o valor (SearchFields, DisplayFields); delegação no conector SQL (\"a galeria vem vazia\", \"o contador mostra 2.000\", CountRows, filtro de data); timers, auto-refresh e debounce; a chamada .Run() de um flow do lado do app (loading, IfError, toast); tokens fx*, nomenclatura, acessibilidade e escopo por perfil e unidade na tela. Não use para divergência entre KPI e galeria sem causa óbvia (use `power-platform`), definição do flow, Try/Catch e HTTP (use `power-automate`), procedure, DDL e coluna calculada (use `sql-procedures`), tabelas, Choice, Security Role e delegação no Dataverse (use `dataverse`), ALM, Power BI, model-driven ou Power Pages."
argument-hint: "[tela|componente|formula|auditar|refactor|performance] [alvo]"
user-invocable: true
---

# Power Apps Canvas

Produz e revisa telas Canvas como **YAML `.pa.yaml` colável no Studio** e Power Fx no dialeto
certo para o destino. Padrão: ManualLayout + controles Classic, canvas 1920x1080, tokens `fx*`,
escrita sempre por flow. Os padrões decididos do kit (contrato app e flow, separadores, telas,
nomes) estão em
[decisoes-padrao.md](../power-platform/references/decisoes-padrao.md); esta skill os aplica.

## Regras inegociáveis

1. **Separador por destino.** YAML colado: `,` entre argumentos, `;` encadeia, `.` decimal.
   Barra de fórmulas pt-BR (`App.OnStart`, `App.Formulas`): `;`, `;;`, `,`. Nunca `;;` em YAML.
   Todo bloco de código diz o destino. Por quê: misturar não parseia em nenhum dos dois.
2. **YAML válido pelo schema.** Toda propriedade começa com `=`; indentação de 2 espaços;
   `Control: Tipo@versão` com a versão do app; fórmula de várias linhas em `|-`; `Control` e
   `Variant` sem fórmula; a ordem de `Children` é o z-index. Por quê: o Studio valida antes de
   colar e rejeita o bloco inteiro.
3. **Só propriedade atestada naquele tipo de controle.** Antes de emitir propriedade nova,
   procure-a no mesmo tipo já usado no app; recusas conhecidas em
   [propriedades-inexistentes.md](references/propriedades-inexistentes.md). Por quê: uma
   propriedade inexistente (PA2108) derruba o bloco inteiro.
4. **Cor, fonte, medida e texto por token `fx*`.** Nada de `RGBA(` literal em tela. Por quê:
   um valor, um lugar; migrar literais depois é trabalho manual e caro.
5. **Delegação declarada por escrito.** Todo `Filter`, `LookUp`, `CountRows` e filtro de data
   tem delegação conferida e declarada no cabeçalho da tela, e o teto aparece na UI
   (`2.000+`). Prefira `StartsWith`. `Search` e `"x" in coluna` delegam só em texto (viram `LIKE '%x%'`, sem índice); `coluna in [lista]`/coleção não delega no SQL; nunca `LookUp(fonte)` dentro de galeria.
   Por quê: falha calada, sem erro e sem aviso. [delegacao.md](references/delegacao.md)
6. **Toda chamada `.Run()` dentro de `IfError`**; sucesso é `status <> "error"` (resposta em
   branco é erro); ids com `Text(id, "[$-en-US]0")` (YAML); depois de gravar, `Refresh` e recontagem.
   Por quê: timeout ou flow desligado deixa o overlay preso ou fecha o modal como sucesso.
   [chamada-flow.md](references/chamada-flow.md)
7. **A tela não grava direto com regra de negócio e não autoriza.** Escrita passa por flow;
   permissão na tela é flag do perfil (UX); sem perfil resolvido, sem acesso (fail-closed). Por
   quê: o cliente é manipulável e a conta do conector é compartilhada.
   [escopo-e-permissao.md](references/escopo-e-permissao.md)
8. **Toda global nasce no `OnStart`; named formula não lê global.** Por quê: `Blank() = 0` é
   falso (galeria vazia sem erro) e named formula não recalcula com `Refresh()`.
9. **O nome vem do ambiente real**, não do dicionário: coluna, tabela e prefixo de
   `NOMES-AS-BUILT` (skill `dataverse`); extrato filtrado não prova esquema. Por quê: coluna
   errada em `SearchFields`/`SortByColumns` não dá erro.
10. **O validador não é o portão suficiente: o portão é o script mais colar no Studio** (e
    *Data row limit* = 1 num clone). Por quê: o script só vê o que está no arquivo; PA2108 e
    delegação só o Studio confirma.
11. **Fim de `Children` da tela: conteúdo, modais, loading, toast. Todo timer tem regra de
    parada.** Por quê: modal acima do toast e `Repeat` sem parada foram defeitos reais.

## Fluxo de trabalho

### 1. Carregue só o que a tarefa exige

| Tarefa | Carregue |
|---|---|
| tela ou componente novo | **catálogo primeiro**: [assets/componentes/INDICE.md](assets/componentes/INDICE.md) (25 componentes coláveis); depois `assets/tela-molde.md`, [ux-componentes.md](references/ux-componentes.md), [yaml-pa-formato.md](references/yaml-pa-formato.md), [nomenclatura.md](references/nomenclatura.md) |
| modal, toast, loading | [ux-feedback.md](references/ux-feedback.md), [chamada-flow.md](references/chamada-flow.md) |
| fórmula Power Fx | [powerfx-essencial.md](references/powerfx-essencial.md) |
| dado, filtro, contador, data, "vem vazio" | [delegacao.md](references/delegacao.md) |
| app lento, galeria travando | [performance.md](references/performance.md), [delegacao.md](references/delegacao.md) |
| auto-refresh, debounce, polling, toast que não some | [timers-async.md](references/timers-async.md) |
| botão que grava (chama flow) | [chamada-flow.md](references/chamada-flow.md) |
| perfil, unidade, "vê dado de outra unidade" | [escopo-e-permissao.md](references/escopo-e-permissao.md) |
| cor, fonte, medida, mensagens | [design-tokens.md](references/design-tokens.md), `assets/app-formulas-tokens.md` |
| `OnStart` e globais | `assets/app-onstart-molde.md` |
| contraste, foco, leitor de tela | [acessibilidade.md](references/acessibilidade.md) |
| "PA2108", "não cola" | [propriedades-inexistentes.md](references/propriedades-inexistentes.md), [yaml-pa-formato.md](references/yaml-pa-formato.md) |
| auditoria de uma tela | [anti-padroes.md](references/anti-padroes.md), [estilo.md](references/estilo.md) e o que o achado indicar |

Arquivo de tela grande: nunca leia inteiro; `Grep` para localizar e `Read` com janelas de 200 a
400 linhas.

### 2. Antes de gerar, responda a si mesmo

- Qual tela e qual prefixo? Qual a trilha de dados (`trilha_dados` no
  `power-platform.config.json`)?
- Quais fontes e **colunas reais**? São delegáveis para o filtro pedido? Qual é o teto?
- O dado vai no `OnStart`, no `OnVisible`, em named formula ou sob demanda?
- Já existe bloco equivalente em [ux-componentes.md](references/ux-componentes.md)? Reutilize.
- Esta ação precisa de flow (regra de negócio, mais de um efeito, autorização)? Se sim, o flow é
  da skill `power-automate`; aqui só o lado da tela.

### 3. Entregue, nesta ordem

1. **O YAML ou Power Fx pronto**, sem placeholder que o usuário precise adivinhar.
2. **Como aplicar**, em **uma** das três vias (detalhe em
   [yaml-pa-formato.md](references/yaml-pa-formato.md) §7): *Code view* (bloco de controle, diga o
   controle-pai); *barra de fórmulas* (propriedade isolada: controle e propriedade); *objeto App*
   (`OnStart` e `Formulas`: digitar; não há Code view do App). Diga o **dialeto**.
3. **Avisos**: delegação e teto, dependência de variável não inicializada, impacto de
   desempenho, o que não foi verificado no Studio.

### 4. Valide

Rode o script **e** cole no Studio (regra 10). Corrija antes de responder: não entregue YAML que
o Studio vai recusar.

### 5. Sub-comandos

`/powerapps-canvas <sub> <alvo>`; sem sub-comando, infira pela pergunta.

| Sub | Faz |
|---|---|
| `tela <nome>` | tela completa a partir de `assets/tela-molde.md` |
| `componente <tipo>` | bloco de [ux-componentes.md](references/ux-componentes.md): `header`, `kpi`, `abas`, `filtros`, `galeria`, `badge`, `modal`, `loading`, `toast`, `selecao`, `vazio` |
| `formula <descrição>` | Power Fx com delegação verificada e tratamento de erro; diz a propriedade e o dialeto |
| `auditar <arquivo\|tela>` | achados com severidade, `arquivo` e código do validador, em 5 eixos: dados e delegação, desempenho, UX, acessibilidade, convenções |
| `refactor <trecho>` | antes e depois, com o ganho esperado, mantendo o comportamento |
| `performance` | o que carrega quando, o que vira named formula, o que adia, o que paraleliza, que timers rodam |

## Referências

| Arquivo | Quando ler |
|---|---|
| [yaml-pa-formato.md](references/yaml-pa-formato.md) | gramática, escape, indentação, versões de controle, colar no Studio |
| [powerfx-essencial.md](references/powerfx-essencial.md) | variáveis, coleções, erro, datas, texto, navegação, Patch x flow |
| [delegacao.md](references/delegacao.md) | o que delega (SQL e Dataverse), teto, contagem, data `Ref_*`, busca |
| [performance.md](references/performance.md) | `OnStart`, `Concurrent`, carga adiada, paginação, medir |
| [timers-async.md](references/timers-async.md) | Timer: auto-refresh, debounce, toast, timeout, polling |
| [chamada-flow.md](references/chamada-flow.md) | botão que grava: loading, `IfError(.Run)`, toast, refresh |
| [escopo-e-permissao.md](references/escopo-e-permissao.md) | flags por perfil, fail-closed, `""` = todas, unidade de gravação |
| [ux-componentes.md](references/ux-componentes.md) | catálogo de blocos corrigido (cabeçalho, filtros, galeria, botões) |
| [ux-feedback.md](references/ux-feedback.md) | modal, loading, toast |
| [design-tokens.md](references/design-tokens.md) | famílias `fx*`, contraste, tipografia, grid, mensagens |
| [acessibilidade.md](references/acessibilidade.md) | checklist WCAG AA e limites da plataforma |
| [nomenclatura.md](references/nomenclatura.md) | controle, variável, coleção, token, flow |
| [propriedades-inexistentes.md](references/propriedades-inexistentes.md) | tabela PA2108 e como verificar no Studio |
| [estilo.md](references/estilo.md) | anatomia de arquivo, golden files, gate, decisão Classic |
| [anti-padroes.md](references/anti-padroes.md) | os mais caros, com porquê, correção e código do validador |
| [licoes-de-campo.md](references/licoes-de-campo.md) | o que já deu errado em apps reais e qual regra previne |
| [assets/componentes/INDICE.md](assets/componentes/INDICE.md) | catálogo de componentes coláveis (cabeçalho, menu lateral, menu no topo, tela inicial com cartões, filtros, galeria-tabela, modais, toast, loading…): um `.md` por componente, validado |
| [assets/tela-molde.md](assets/tela-molde.md) | tela YAML completa e colável |
| [assets/app-formulas-tokens.md](assets/app-formulas-tokens.md) | bloco `App.Formulas` com os tokens |
| [assets/app-onstart-molde.md](assets/app-onstart-molde.md) | `App.OnStart` em ordem de dependência |

## Scripts

Lê blocos cercados e YAML puro (sem verde falso). Só lê; lê `power-platform.config.json` (`pastas.telas`,
`telas_formato`, `ignorar`, `trilha_dados`, `prefixo_publisher`) subindo diretórios ou por
`--config`. Rode **da raiz do projeto** (o script procura `power-platform.config.json` do
diretório atual para cima) ou passe `--config`; a pasta da skill aparece como *Base directory*
quando ela é carregada.

| Comando | O que checa | Exit |
|---|---|---|
| `python <pasta-da-skill>/scripts/validar-telas.py <arquivo-ou-pasta>` | parse com linha (T001), `=` (T002), `Control@versão` (T003 a T005), nome duplicado (T006), `;;` (T007), PA2108 (T008), `RGBA(` (T009), kebab-case (T010), `in`/`Search` (T011), chave repetida (T012), `.Run(` sem `IfError` (T018), z-order (T016) | 0 sem erro, 1 com erro, 2 uso incorreto |
| `python <pasta-da-skill>/scripts/validar-telas.py --trilha sql-server <pasta>` | acrescenta `CountRows`/`CountIf` sem delegação (T013) | idem |
| `python <pasta-da-skill>/scripts/validar-telas.py --codigos` | lista os códigos | 0 |

Formato `auto`: `.md` com blocos ```` ```yaml ```` valida cada bloco; `.md` sem cerca é YAML puro,
lido inteiro; arquivo que não é tela (documentação, bloco de barra de fórmulas) gera **um** aviso T020. Bloco com
`# validador: ignorar` é pulado. Tabela completa dos códigos em
[anti-padroes.md](references/anti-padroes.md) §7.

## Definição de pronto

- [ ] `python <pasta-da-skill>/scripts/validar-telas.py <tela>` devolve `0 erro(s)` (avisos justificados por escrito).
- [ ] O bloco foi **colado no Studio** sem `PA2108` (evidência: o controle aparece na árvore).
- [ ] *Data row limit* = 1 num clone: a galeria continua listando (evidência: lista não vazia).
- [ ] Cabeçalho de delegação escrito; contadores com teto `fxTxtTeto` (grep de `CountRows`).
- [ ] `grep -c "RGBA(" <tela>` = 0 fora de fórmula multilinha de status.
- [ ] Todo botão que chama flow: `IfError`, `varShowLoading` desligado em todos os caminhos,
      testado com o flow desligado (evidência: toast vermelho, overlay fechado).
- [ ] Todo `Filter` de fonte com escopo tem o predicado (grep dos `Filter(`).
- [ ] Contraste >= 4,5:1 e Accessibility checker sem erro novo (evidência: relatório do checker).
- [ ] Timers com parada (`Reset: =!flag`, `Start` ligado à tela); `.Run()` fora de `Items`.
- [ ] Dialeto do destino declarado em cada bloco entregue.

## Armadilhas

As dez mais caras (detalhe e correção em [anti-padroes.md](references/anti-padroes.md)):

1. `CountRows` sobre SQL mostrando o teto como total: [delegacao.md](references/delegacao.md) §3.
2. `.Run()` sem `IfError`; overlay preso: [chamada-flow.md](references/chamada-flow.md).
3. Filtro de data direto atrás de gateway: coluna `Ref_*`: [delegacao.md](references/delegacao.md) §4.
4. `Filter` com escopo sem o predicado de unidade (vazamento sem aviso): [escopo-e-permissao.md](references/escopo-e-permissao.md) §5.
5. `;;` em YAML ou `,` na barra de fórmulas: [yaml-pa-formato.md](references/yaml-pa-formato.md) §2.
6. Propriedade não atestada derrubando o bloco (PA2108): [propriedades-inexistentes.md](references/propriedades-inexistentes.md).
7. `SearchFields`/`SortByColumns` com coluna errada (falha calada): [delegacao.md](references/delegacao.md) §7.
8. Timer com `Repeat` sem parada e toast sem `Reset`: [timers-async.md](references/timers-async.md) §7.
9. Fórmula de linha única com `: ` ou ` #` (quebra ou trunca): [yaml-pa-formato.md](references/yaml-pa-formato.md) §4.
10. Global não declarada no `OnStart` (`Blank() = 0`): [app-onstart-molde.md](assets/app-onstart-molde.md).
