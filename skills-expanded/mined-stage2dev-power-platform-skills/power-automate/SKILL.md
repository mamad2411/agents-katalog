---
name: power-automate
description: "Use quando o trabalho envolver flow do Power Automate: desenhar ou revisar um flow chamado pelo app (trigger Power Apps V2, Response de 4 campos, Try/Catch, Switch por ação), cola esse flow no designer (clipboard, escopo colável, allConnectionData), autorização e escopo por unidade dentro do flow, chamar procedure SQL (Execute stored procedure), receber lote de sistema externo por HTTP com token, gravar no Dataverse por $batch/upsert, escopo de log, expressão que estoura em execução (if não curto-circuita, string(null), outputs de Select), contrato tela-flow-procedure, ou verificar um JSON de flow. Não use para a chamada .Run() do lado do app (use `powerapps-canvas`), a procedure e o DDL (use `sql-procedures`), tabelas e Security Role (use `dataverse`), nem ambientes, soluções e connection references em geral (use `power-platform`)."
argument-hint: "[desenhar|colar|verificar|contrato|http|batch|log] [flow]"
user-invocable: true
---

# power-automate

Produz flows do Power Automate **coláveis no designer e verificáveis**: o escopo JSON com a
anatomia padrão (autorizar -> normalizar -> validar -> gravar -> responder, `Catch` completo),
o contrato com a tela, o desenho de SQL, HTTP, `$batch` e log, e o `scripts/verificar-fluxo.py`
que acusa os defeitos que só estouram em execução. Padrões decididos (F1-F6, C1-C6, A1-A4) estão
em [decisoes-padrao.md](../power-platform/references/decisoes-padrao.md) -- esta skill os
implementa, não os redefine.

## Regras inegociáveis

1. **O flow decide; a procedure executa.** O flow normaliza, valida, autoriza e traduz o código
   da escrita em mensagem. Por quê: regra no cliente é contornável e a conta do conector é
   compartilhada.
2. **A identidade do chamador vem do contexto** (`MyProfile_V2`), nunca de parâmetro do trigger.
   Por quê: quem chama por fora da tela diria quem é.
3. **Autorização por ação**: cada `Caso_<acao>` confere a flag da própria ação antes da primeira
   escrita; zero linha de perfil = negar. Por quê: um portão único antes do `Switch` deixou quem
   cadastra encerrar de forma irreversível.
4. **Flag de segurança nasce ligada** em `CONFIG`. Por quê: um escopo por unidade nasceu
   desligado e qualquer perfil gravou em qualquer unidade.
5. **Resposta sempre com os 4 campos** `{status, description, id, url}` (texto), `status` em
   `success|warning|error`. Por quê: a tela lê `ret.url` num flow que não exporta.
6. **Todo `Nega_*` é um par `Response` + `Terminate`.** Por quê: `Response` não encerra o flow; o
   próximo nó roda com a resposta já enviada.
7. **O `Catch` escuta `Failed`, `TimedOut` e `Skipped`.** Por quê: os irmãos do `Try` (perfil,
   chamador) falhando deixam o `Try` `Skipped` e a execução termina sem `Response`.
8. **Parâmetros do trigger são posicionais e texto; parâmetro novo entra no fim.** Por quê:
   inserir no meio faz os valores deslizarem e o flow grava o campo errado sem erro.
9. **Escrita em SQL só por `Execute stored procedure (V2)`**; nome de procedure e de connection
   reference vêm do ambiente, nunca do documento. Por quê: `Insert/Update row` não funciona com
   trigger no servidor e nomes supostos custaram colagens.
10. **Nenhum nome de ambiente literal fora do `CONFIG`** (servidor, GUID, tabela `dev*`):
    variável de ambiente e connection reference. Por quê: promover para produção vira editar o
    flow.
11. **Protege o argumento, não a condição**: `if()` avalia os dois ramos, e `string(null)` é `''`.
    Por quê: as duas coisas estouraram em execução, em sítios que "já tinham sido corrigidos".
12. **O arquivo que o designer devolveu é o gabarito; gerador só escreve em `dist/`.** Por quê:
    regerar sobre o gabarito apagou uma correção que só existia no disco.
13. **Entrada externa por trigger HTTP separado**, credencial no cabeçalho, resposta derivada do
    resultado real da validação. Por quê: uma `Condição` de constantes deixou o ramo 401 morto.

## Fluxo de trabalho

1. **Comece pelo catálogo** (`assets/componentes/INDICE.md`): se existe bloco para a peça, use-o em vez de escrever
   do zero. Depois classifique a tarefa e carregue só o que ela pede:

| Tarefa | Carregue |
|---|---|
| Desenhar ou revisar um flow chamado pela tela | `references/anatomia-flow.md`, `references/contrato-app-flow.md`, `assets/flow-gravar-molde.json` |
| Montar um flow por peças (CONFIG, chamador, Switch, autorizar, gravar, Catch, log, HTTP, `$batch`…) | `assets/componentes/INDICE.md` — 34 blocos coláveis, cada um validado, com ordem de montagem |
| Permissão, perfil, escopo por unidade | `references/autorizacao-no-flow.md` |
| Entregar/colar no designer, montar o JSON | `references/formato-clipboard.md`, `references/gabarito-designer.md` |
| Expressão que falha só em execução | `references/expressoes-wdl-armadilhas.md` |
| Flow que grava em SQL | `references/sql-no-flow.md` (a procedure é de `sql-procedures`) |
| Receber lote de sistema externo | `references/http-entrada-externa.md`, `references/dataverse-batch-upsert.md` |
| Criar tabelas e carga mockup no Dataverse pela Web API (flow pronto, `$batch`) | `skills/power-platform/references/construtor-dataverse.md` (do orquestrador) |
| Log de execução, suporte | `references/log-execucao.md` |
| Gerar flows por script, pipeline | `references/gerador-e-gabarito.md` |
| Documento de contrato | `assets/contrato-flow-molde.md` |
| Entender de onde veio um padrão | `references/licoes-de-campo.md` |

2. **Mapeie antes de escrever:** ambiente e idioma do designer; connection references que
   existem (`power-platform`); nome AS-BUILT da procedure ou da tabela (`sql-procedures`,
   `dataverse`); quais ações o flow tem e a flag de cada uma; destino do log (ADR).
3. **Escreva o contrato primeiro** (`assets/contrato-flow-molde.md`): chamada, tabela de
   parâmetros posicionais, autorização por ação, tabela código -> mensagem.
4. **Parta do molde** `assets/flow-gravar-molde.json`: troque `<procedure_...>`,
   `<prefixo>_...` e os nomes de ação; mantenha a estrutura. O trigger é **digitado à mão** na
   ordem do contrato (não é colável).
5. **Verifique antes de colar** (e de novo no que o designer devolver): `python <pasta-da-skill>/scripts/verificar-fluxo.py <arquivo-ou-pasta>`.
6. **Cole** (`Ctrl+V` no ponto de inserção do designer, de cima para baixo; o trigger já deve existir), religue as
   conexões, rode com um usuário de teste
   **sem** permissão, um com permissão e um de outra unidade, e confira o histórico.
7. **Devolva o que o designer devolveu** ao gabarito (arquivo somente leitura) e, se for gerar,
   traga as diferenças para o gerador antes do segundo flow (`gerador-e-gabarito.md`).

## Referências

| Arquivo | Quando ler |
|---|---|
| `references/anatomia-flow.md` | Antes de desenhar qualquer flow chamado pela tela; Nega/Terminate e Catch |
| `references/contrato-app-flow.md` | Trigger, Response de 4 campos, código -> mensagem, parâmetro novo, job assíncrono |
| `references/autorizacao-no-flow.md` | Perfil, flag por ação, escopo por unidade, fail-closed |
| `references/formato-clipboard.md` | Envelopes de escopo e de folha, como colar, `allConnectionData`, idioma do trigger |
| `references/gabarito-designer.md` | R1-R13: o que o designer devolve, o que bloqueia e o que só normaliza |
| `references/expressoes-wdl-armadilhas.md` | `if()`, `string(null)`, `outputs()` x `body()`, `bit`, 8.192 caracteres, `@{}` |
| `references/sql-no-flow.md` | `Execute stored procedure (V2)`, ler o retorno, limites do conector |
| `references/http-entrada-externa.md` | Trigger Request, token no cabeçalho, status real, aceite x síncrono, N=1 x lote |
| `references/dataverse-batch-upsert.md` | `$batch`, changeset, upsert, 429, paginação |
| `references/log-execucao.md` | Escopo `Log`, tabelas pai/filho, `workflow().run.name`, tensão com `Terminate` |
| `references/gerador-e-gabarito.md` | Gerador seguro, gabarito imutável, round-trip |
| `references/licoes-de-campo.md` | Defeitos reais de flows (SQL, HTTP + `$batch`) e a regra que previne cada um |
| `assets/componentes/INDICE.md` | Catálogo de blocos coláveis (`.md` explicado + `.json` validado), maturidade e ordem de montagem |
| `assets/flow-gravar-molde.json` | Escopo colável de partida (passa no verificador) |
| `assets/contrato-flow-molde.md` | Molde do contrato tela <-> flow <-> procedure |

## Scripts

`<pasta-da-skill>` é o *Base directory* que aparece quando a skill é carregada. Rode **da raiz do projeto** (o script procura `power-platform.config.json` do diretório atual para cima) ou passe `--config`.

| Comando | O que checa | Exit |
|---|---|---|
| `python <pasta-da-skill>/scripts/verificar-fluxo.py <arquivo\|pasta>` | F001 JSON; F002 envelope; F003/F019 identidade e segmentos do nó; F004 nome duplicado; F005 `runAfter` órfão; F006 referência a ação inexistente; F007 `items()`; F008 caso de `Switch`; F009 `Catch` sem `Skipped`; F010 `Response` sem os 4 campos; F011 `outputs()` de `Select`/`Query`; F012 `coalesce(string())`; F013 expressão > 8.192; F014 literal de ambiente; F015 `Response` sem `Terminate`; F016 condição constante; F017 conexão ausente; F018 `@{}` em parâmetro; F020 condição de `If` em texto ou sem `and`/`or`; F021 `Inicializar variável` fora da raiz; F022 variável sozinha num campo colado; F023 `Fazer até` em texto colado | 0 sem erro, 1 com erro, 2 uso incorreto |
| `python <pasta-da-skill>/scripts/verificar-fluxo.py --estrito <...>` | também `coalesce(string(x), '')` (F012) | idem |
| `python <pasta-da-skill>/scripts/verificar-fluxo.py --config <arquivo>` | usa `pastas.flows` e `ignorar` de `power-platform.config.json` | idem |

Formatos lidos: envelope de escopo e de folha do clipboard (`.json`, ou `.md` com só o JSON) e
`definition` de solução exportada. Só lê; saída `caminho:ação: ERRO|AVISO Fnnn mensagem`.

## Definição de pronto

Comandos da raiz do projeto (ver nota em Scripts).

- [ ] `python <pasta-da-skill>/scripts/verificar-fluxo.py <flow>` -> `0 erro(s)` (avisos lidos e justificados no contrato).
- [ ] Contrato do flow preenchido; nº de argumentos do `.Run()` == nº de parâmetros do trigger.
- [ ] Teste de negação executado: usuário sem a flag da ação recebe `error` e **nada** é gravado.
- [ ] Teste de falha de conector: com a connection reference desligada, o app recebe a mensagem do
      `Catch` (nunca timeout).
- [ ] Nenhum literal de ambiente fora do `CONFIG` (F014 limpo ou aviso justificado).
- [ ] O JSON devolvido pelo designer está em `gabarito/` (somente leitura) e nenhum gerador
      escreve sobre ele.
- [ ] Tarefa marcada feita traz a coluna Evidência: comando, saída e data (P2).

## Armadilhas

1. `if()` não protege a chamada de dentro: proteja o argumento --
   [expressoes-wdl-armadilhas.md](references/expressoes-wdl-armadilhas.md) §1.
2. `coalesce(string(x), '0')` nunca cai no fallback -- mesmo arquivo, §2.
3. `outputs('Select')` devolve o envelope; use `body()` -- §3.
4. `bit` do SQL chega `true`/`false`; comparar com `1` ou com o booleano `true` inverte a regra -- §4.
5. Caso de `Switch` com nome de ação derruba a colagem --
   [anatomia-flow.md](references/anatomia-flow.md) §5.
6. `Catch` sem `Skipped`: execução sem `Response` -- mesmo arquivo, §4.
7. `Response` sem `Terminate` responde duas vezes -- mesmo arquivo, §3.
8. Ordem `mail`/`userPrincipalName` invertida nega todo mundo --
   [autorizacao-no-flow.md](references/autorizacao-no-flow.md) §1.
9. Rodar o gerador com edição manual no disco apaga a correção --
   [gerador-e-gabarito.md](references/gerador-e-gabarito.md) §2.
10. 200 antes de gravar sem declarar que é aceite --
    [http-entrada-externa.md](references/http-entrada-externa.md) §5.
