---
name: dataverse
description: "Use quando o app Power Apps ou o flow lê ou grava em tabelas Dataverse: escrever ou corrigir fórmula que filtra, ordena, compara ou grava coluna Dataverse; descobrir o nome certo de tabela ou coluna (lógico, de exibição, de schema, prefixo do publisher); decidir Choice, Lookup ou texto; montar ou atualizar o NOMES-AS-BUILT; delegação no conector Dataverse (o que delega, 500/2.000); desenhar security role, business unit, owner team ou segurança de coluna; modelar tabela, relacionamento, alternate key ou coluna calculada; importar CSV ou Excel. Termos: \"qual o nome da coluna\", \"Choice ou texto\", \"usuário vê todas as unidades\", \"importar planilha\". Não use para YAML de tela, Power Fx fora de Dataverse, combo e UX (use `powerapps-canvas`), flow, `$batch` e HTTP (use `power-automate`), procedure e SQL Server (use `sql-procedures`), soluções, ambientes e connection references (use `power-platform`)."
argument-hint: "[nomes|tipos|delegacao|seguranca|modelar|importar|as-built] [tabela ou coluna]"
user-invocable: true
---

# Dataverse nos apps Power Apps

Esta skill entrega o que o app e o flow precisam saber sobre Dataverse para não errar: o nome
certo de cada tabela e coluna **do ambiente real**, o tipo real (Choice, Lookup ou texto) e a
sintaxe que ele exige, o que delega, quem consegue ler quais linhas, como modelar e como
importar. O artefato central é o `NOMES-AS-BUILT.md` do projeto.

Fronteiras: aqui mora *como a coluna Dataverse aparece no Power Fx*, alternate key e a tabela.
O resto do Power Fx é de `powerapps-canvas`; o `$batch` e o flow são de `power-automate`; ALM
(solução, ambiente, variável de ambiente) é de `power-platform`. Padrões decididos (N1–N3, A3,
A4) ficam em `skills/power-platform/references/decisoes-padrao.md` — esta skill aponta, não
repete.

## Regras inegociáveis

1. **Leia o `NOMES-AS-BUILT.md` do projeto antes de escrever ou julgar qualquer fórmula ou flow
   que toque Dataverse.** Dicionário de dados, script de criação e plano perdem para ele (N1).
   Caminho em `power-platform.config.json` → `nomes_as_built`. Se o arquivo não existe, o
   primeiro passo é extraí-lo (`references/nomes-as-built.md`), não chutar.
   Por quê: uma tela escrita contra o dicionário precisou de várias correções no Studio; todas foram de
   nome e tipo, nenhuma de sintaxe.
2. **Um nome por contexto.** Identificador numa fórmula = nome de **exibição**; texto entre
   aspas duplas (`SortByColumns`, `DisplayFields`, `SearchFields`), OData, Web API e `$batch` =
   nome **lógico**; URL do `$batch` = **EntitySet** (plural). Nunca derive um nome do outro.
   Por quê: o lógico não sai do de exibição por regra, e o erro de coluna em string falha calado.
3. **Tipo real antes da sintaxe.** Choice compara com opção, Lookup com registro, texto com texto.
   Confirme o `AttributeType` no as-built antes de escrever o `Filter` ou o `Patch`.
   Por quê: o ambiente real trocou Lookup por Choice e por texto; a sintaxe muda em cada caso.
4. **Antes de dizer que uma coluna não existe, abra o esquema da tabela inteira** — nunca um
   extrato filtrado nem uma amostra (N3).
   Por quê: extrato com `$filter` ou export de amostra omite colunas e produz "não existe" falso.
5. **Toda consulta declara o que delega**, e o teste é `Data row limit = 1` no Studio. Ausência
   de triângulo amarelo não prova delegação.
   Por quê: consulta não delegada baixa 500 (até 2.000) linhas e filtra no cliente, sem erro.
6. **Filtro de tela não é controle de acesso** (A3). Security Role em escopo Organização deixa
   qualquer usuário com acesso à tabela ler todas as unidades por Excel, Power BI ou Web API.
   Isolamento por linha exige Owner Team + Business Unit, ou o risco aceito fica escrito.
   Por quê: o escopo de unidade na galeria é conveniência; quem lê direto da API ignora a galeria.
7. **Um só dono da criação do schema por ambiente**: script *ou* maker, nunca os dois. Criado o
   schema, extraia o as-built e passe a escrever contra ele.
   Por quê: o ambiente real foi criado à mão com o publisher padrão do tenant, com prefixo e
   tipos diferentes dos do script.
8. **Upsert e `$batch` por chave de negócio exigem alternate key em estado `Active`.**
   Por quê: chave `Pending` não resolve Lookup na importação nem no upsert, e o erro é silencioso.
9. **Texto não vira Choice nem Lookup depois.** Decida o tipo antes de importar; importar
   primeiro e ajustar depois é refazer a tabela.
   Por quê: o assistente de importação cria colunas de texto e o Dataverse não as converte. A carga
   mockup do `/pp:arquitetura` existe para errar o tipo no mockup, onde recriar é de graça.
10. **Nunca afirme "✅ feito" sobre nome ou tipo sem o comando que reencontra a evidência**
    (extração datada do ambiente). Por quê: P2 e P5 de `decisoes-padrao.md`.

## Fluxo de trabalho

1. **Classifique a tarefa e carregue só o necessário:**

   | Tarefa | Carregar |
   |---|---|
   | Escrever/corrigir fórmula ou flow que lê ou grava coluna Dataverse | `references/nomes-e-tipos.md` + o `NOMES-AS-BUILT.md` do projeto |
   | "Qual é o nome certo de…", montar ou atualizar o as-built | `references/nomes-as-built.md`, `assets/nomes-as-built-molde.md`, `scripts/extrair-nomes-as-built.py` |
   | Auditar delegação, contador, galeria que trunca | `references/delegacao-dataverse.md` |
   | "Qualquer usuário vê todas as unidades", role, BU, owner team | `references/seguranca.md` |
   | Criar tabela, relacionamento, chave, coluna calculada, auditoria | `references/modelagem.md` |
   | Importar CSV/Excel, migrar dado legado, carga com Lookup | `references/importacao-dados.md` |
| Criar as tabelas a partir da carga mockup `.xlsx`; conferir os tipos que o Dataverse deduziu | `skills/power-platform/references/carga-mockup.md` e `scripts/montar-carga-mockup.py --conferir` (do orquestrador) |
| Criar tabelas, colunas tipadas, relacionamentos e a carga mockup direto pela Web API, por um flow | `skills/power-platform/references/construtor-dataverse.md` (`montar-carga-mockup.py --flow`) |
   | "Isso já aconteceu?" (lições de campo) | `references/licoes-de-campo.md` |

2. **Confirme a trilha.** `trilha_dados` do projeto deve ser `dataverse` (A4). Se a pergunta é
   "Dataverse ou SQL Server?", não decida aqui: aponte para a matriz de tecnologia
   (`skills/power-platform/references/matriz-tecnologia.md`) e para o ADR do projeto. Sinais que empurram para SQL: dado
   corporativo já em SQL, DBA dono do schema, transação multi-tabela forte, volume por
   galeria acima do teto de delegação. Troca de trilha exige ADR.
3. **Leia o as-built** (regra 1). Anote o que está como `?` ou "não confirmado": são lacunas, e
   fórmula que depende delas diz isso por escrito.
4. **Escreva ou audite** usando a referência da tarefa. Fórmula entregue traz o destino
   (`barra de fórmulas (pt-BR: ; e ;;)` ou `YAML colado (, e ;)`, ver `decisoes-padrao.md` §3) e
   a delegabilidade declarada (T7).
5. **Feche** com a definição de pronto abaixo. Mudou nome ou tipo no ambiente? Reextraia o
   as-built *antes* de seguir.

## Referências

| Arquivo | Quando ler |
|---|---|
| `references/nomes-e-tipos.md` | Publisher e prefixo; lógico × exibição × schema × EntitySet; como o Power Fx resolve em cada contexto (row scope!); Choice × Lookup × texto: comparar, filtrar, gravar |
| `references/nomes-as-built.md` | Por que é a autoridade; como extrair (maker, Web API, pac); como manter e versionar |
| `references/delegacao-dataverse.md` | O que delega no Dataverse, diferença para o conector SQL, 500/2.000, 50.000, `In`, `StartsWith`, `CountRows` |
| `references/seguranca.md` | Security role, BU, owner team, escopo de linha, segurança de coluna, risco do escopo Organização |
| `references/modelagem.md` | Tabelas, ownership, relacionamentos, alternate keys, colunas calculadas e rollup, auditoria |
| `references/importacao-dados.md` | CSV/Excel/dataflow, ordem de carga com Lookup, como evitar a divergência script × ambiente |
| `references/licoes-de-campo.md` | Lições de campo: o que já deu errado em projetos reais e qual regra previne |
| `assets/nomes-as-built-molde.md` | Molde copiável do `NOMES-AS-BUILT.md` |

## Scripts

`<pasta-da-skill>` é o *Base directory* que aparece quando a skill é carregada. Rode **da raiz do projeto** (o script procura `power-platform.config.json` do diretório atual para cima) ou passe `--config`.

| Comando | O que checa | Exit |
|---|---|---|
| `python <pasta-da-skill>/scripts/extrair-nomes-as-built.py <export.json> --prefixo <prefixo>_` | Valida o JSON da Web API (`EntityDefinitions` + `Attributes`): E001 JSON/formato, E002 tabela sem atributos, E003 prefixo sem tabela, A001 coluna sem nome de exibição, A003 Choice sem opções, D001 exibição repetida | 0 sem erro · 1 com erro · 2 uso |
| `… --complemento <prefixo>_<tabela>=<choices.json>` (repetível) | Funde opções de Choice e destinos de Lookup vindos das consultas com cast; E004 tabela inexistente, E005 arquivo ilegível | 0 / 1 / 2 |
| `python <pasta-da-skill>/scripts/extrair-nomes-as-built.py <export.json> --prefixo <prefixo>_ --saida NOMES-AS-BUILT.md` | Idem e **gera** o markdown no formato do molde. Só escreve com `--saida` (`-` imprime); recusa sobrescrever a entrada; sem rede | 0 / 1 / 2 |

O script só lê arquivo local; a exportação em si (uma consulta à Web API) é feita por você no
navegador autenticado — passo a passo em `references/nomes-as-built.md`.

## Definição de pronto

Comandos da raiz do projeto (nota em Scripts); o lint do repositório roda da raiz do repositório.

- [ ] As-built existe, é do ambiente atual e traz a data da extração.
  Evidência: `python <pasta-da-skill>/scripts/extrair-nomes-as-built.py <export.json> --prefixo <prefixo>_ --saida <caminho do as-built>` → `0 erro(s)`.
- [ ] Toda tabela e coluna citada na fórmula ou no flow aparece no as-built com o mesmo nome.
  Evidência: `rg -n "SortByColumns|DisplayFields|SearchFields|ShowColumns" <pasta de telas>`; cada
  string listada é nome lógico presente no as-built.
- [ ] Todo `Filter`/`Patch` sobre Choice, Lookup ou texto usa a sintaxe do tipo real.
  Evidência: `rg -n "\.Selected\b" <pasta de telas>` sem `.Value` onde a coluna é Choice.
- [ ] Delegação declarada e testada. Evidência: Studio com `Data row limit = 1`, galeria e
  contadores conferidos; resultado anotado no cabeçalho da tela (T7).
- [ ] Segurança: o isolamento foi testado fora do app. Evidência: com uma conta de teste de outra
  unidade, `GET <org>/api/data/v9.2/<EntitySet>?$top=5` devolve só as linhas permitidas — ou o
  risco aceito está registrado por escrito.
- [ ] Se há upsert por chave: `GET .../EntityDefinitions(LogicalName='<tabela>')/Keys?$select=SchemaName,EntityKeyIndexStatus` → `Active`.
- [ ] `python tools/lint_skills.py skills/dataverse` → `0 erro(s)`.

## Armadilhas

1. Escrever contra o dicionário em vez do ambiente — [nomes-as-built](references/nomes-as-built.md).
2. Nome de schema em fórmula, ou nome de exibição em `SortByColumns` — [nomes-e-tipos](references/nomes-e-tipos.md).
3. Em row scope o Power Fx resolve coluna pelo nome de **exibição**; `Distinct(…; <prefixo>_coluna)` no `OnStart` derrubou todas as globais — [nomes-e-tipos](references/nomes-e-tipos.md).
4. Comparar Choice com texto ou com registro; gravar texto numa Choice — [nomes-e-tipos](references/nomes-e-tipos.md).
5. Chave primária com nome de exibição igual ao da tabela (`'tabela'` precisa de aspas) — [nomes-e-tipos](references/nomes-e-tipos.md).
6. Confiar na ausência do triângulo de delegação; `With`/`Set` sobre fonte — [delegacao-dataverse](references/delegacao-dataverse.md).
7. `CountRows` sem filtro é aproximado (cache); contador que mostra 50000 pode ser a consulta quebrada — [delegacao-dataverse](references/delegacao-dataverse.md).
8. Security Role em Organização tratada como isolamento — [seguranca](references/seguranca.md).
9. Lookup trocado por texto sem integridade: unidade inválida entra, homônimo colide — [modelagem](references/modelagem.md).
10. Importar antes de criar Choice, Lookup e chave — [importacao-dados](references/importacao-dados.md).
11. Confiar no tipo que o Dataverse deduziu do Excel: ele erra com frequência; confira com `--conferir` antes do dado real, ou crie pelo construtor, que manda o tipo do spec — `skills/power-platform/references/carga-mockup.md`, `construtor-dataverse.md`.
