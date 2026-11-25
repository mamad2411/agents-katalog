---
name: sql-procedures
description: "Use quando o trabalho for o backend SQL Server de um app Power Apps: escrever, revisar ou corrigir procedure chamada pelo Power Automate (\"Table1 vem vazio\", NOCOUNT, XACT_ABORT, retorno status/description/id/url, código de resultado), modelo de dados (prefixos Id_/Flg_/Dt_, flags de perfil, chaves, collation), coluna calculada para delegação (\"filtro de data não delega\", \"CountRows não delega\", Ref_DtInclusao), escopo por unidade com @Filtros JSON, pacote e pedido de DDL ao DBA (banco congelado, provas de ambiente), GRANT EXECUTE da conta do conector ou migração de dados de legado para SQL Server. Não use para Power Fx, tela ou delegação do lado do app (use `powerapps-canvas`), flow, Try/Catch ou autorização no flow (use `power-automate`), Dataverse (use `dataverse`) nem arquitetura e protocolo de trabalho (use `power-platform`)."
argument-hint: "[procedure|modelo|delegacao|escopo|dba|migracao|auditar] [alvo]"
user-invocable: true
---

# sql-procedures

Produz o backend SQL Server dos apps Power Apps: procedures de escrita e de leitura chamadas pelo
Power Automate, o modelo de dados que elas e o app usam, as colunas calculadas que fazem o filtro
delegar, o pacote e o pedido de DDL ao DBA e a migração de dados do legado. Padrões decididos
(contrato de retorno, banco, nomes) vivem em
[decisoes-padrao.md](../power-platform/references/decisoes-padrao.md); esta skill ensina o **como** e
confere com `scripts/lint-procedure.py`. O flow que chama a procedure e a autorização dentro dele são
de `power-automate`; a fórmula que consome a coluna calculada é de `powerapps-canvas`.

## Regras inegociáveis

1. **Procedure de escrita abre com `SET NOCOUNT ON; SET XACT_ABORT ON;`**, com transação onde há mais
   de um statement e sempre com `dbo.` nas referências.
   Por quê: sem `NOCOUNT`, o rowcount de cada DML pode virar result set e o retorno some calado; sem
   `XACT_ABORT`, erro de runtime deixa escrita parcial. (B1; `lint P001/P002/P003`)
2. **O retorno é 1 result set, 1 linha, 4 colunas** (`status`, `description`, `id`, `url`), em todos os
   desfechos, inclusive zero linha gravada; `id` é texto, nada é `NULL`.
   Por quê: o flow lê `ResultSets/Table1[0]`; só o primeiro result set chega e uma linha a menos
   quebra o contrato inteiro sem erro. (C1; `lint P004`)
3. **`description` é um código ASCII de vocabulário fechado**; a frase é do flow.
   Por quê: a procedure não monta texto; código desconhecido no flow responde `error`, nunca vai cru
   ao usuário. (C2; [padrao-procedure.md](references/padrao-procedure.md) §4)
4. **Todo `OUTPUT` de DML usa `INTO @tabela`.**
   Por quê: `OUTPUT` sem `INTO` devolve linhas ao cliente (rouba o retorno) e falha em tabela com
   trigger. (`lint P011`)
5. **O flow decide, a procedure executa** (A2): variante **declarativa** por padrão; a **clássica**
   (`IF` + `TRY/CATCH` + `THROW`) ou o bloco de autorização defensiva só com ADR e um dos sinais de
   `seguranca-e-permissoes.md` §4.
   Por quê: o banco tende a congelar e a regra precisa continuar editável sem DBA; o custo é que o
   banco deixa de ser a última barreira, e isso tem de estar escrito.
6. **Data de auditoria vem do banco** (`SYSUTCDATETIME()` na procedure, `Dt_Alteracao` no trigger),
   nunca por parâmetro.
   Por quê: o relógio do cliente faz a linha nascer horas adiante das demais.
7. **Filtro de data para o app: coluna `Ref_<col> AS DATEDIFF(day, 0, <col>) PERSISTED`**, nunca
   `CAST(<data> AS INT)`.
   Por quê: o filtro de data direto não delega atrás de gateway, e `CAST` arredonda (13h vira o dia
   seguinte). (B2; `lint P006`)
8. **Número exato não sai de `CountRows`:** conte no servidor (procedure de contagem) ou use `Sum` de
   coluna constante; senão, mostre o teto (`2.000+`).
   Por quê: `CountRows` não delega no conector SQL e erra calado acima do teto. (B3)
9. **Escopo é parâmetro resolvido pelo flow; o banco obedece e falha fechado:** `NULL` = tudo, sigla =
   uma unidade, `''` casa nada; escopo em `AND` com o filtro do usuário.
   Por quê: a conta do conector é compartilhada e o filtro da tela é UX, não controle (A3).
10. **A conta do conector tem `GRANT EXECUTE` e `SELECT` onde o app lê; nenhum DML.**
    Por quê: é o que fecha, por construção, o `Patch` direto na tabela.
11. **Nome de objeto e de coluna vem do ambiente** (`sys.procedures`, `sys.columns`), com a grafia exata:
    o `NOMES-AS-BUILT` vence o plano. (N1; `lint P005`)
    Por quê: o nome real divergiu do documentado e o conector é sensível a maiúsculas: erra em runtime.
12. **Banco congelado: o critério é "o objeto guarda dado próprio?"**; coluna calculada costuma ser
    aceita, tabela/coluna que guarda dado/view/mudança de assinatura costumam ser recusadas. (B4)
    Por quê: planejar o schema antes do primeiro deploy custa um pedido; depois, uma negociação.
13. **Sem SQL dinâmico por concatenação** e sem `NOLOCK`; `ERROR_MESSAGE()` nunca no retorno.
    Por quê: injeção, leitura suja e vazamento de esquema. (`lint P009/P010`)
14. **Antes de entregar: `lint-procedure.py` com 0 erro** e as provas de ambiente rodadas.
    Por quê: validador que nunca acusou nada não provou que valida (P4); já houve procedure entregue
    sem nunca ter sido compilada.

## Fluxo de trabalho

1. **Descubra a tarefa e carregue só as referências dela:**

| Tarefa | Carregar |
|---|---|
| Escrever ou revisar uma procedure de escrita | `padrao-procedure.md`, `assets/procedure-escrita-molde.sql`, `contrato-proc-flow.md` |
| Escolher declarativa × clássica | `padrao-procedure.md` §5 e §7 |
| Leitura com filtros, contagem, exportação | `padrao-procedure.md` §9, `assets/funcao-leitura-molde.sql`, `escopo-por-unidade.md` |
| Contrato entre procedure e flow, parâmetro em JSON | `contrato-proc-flow.md`, `assets/contrato-procedure-molde.md` |
| Tabela, coluna, chave, flag, trigger, collation | `modelo-de-dados.md` |
| "O filtro de data não delega", contador errado, status derivado | `colunas-calculadas-delegacao.md` |
| Escopo por unidade, código de unidade | `escopo-por-unidade.md` |
| Conta do conector, GRANT, "a procedure autoriza?" | `seguranca-e-permissoes.md` |
| Pacote ao DBA, pedido de DDL, banco congelado, provas | `deploy-e-dba.md`, `assets/pedido-ddl-dba-molde.md` |
| Carga do legado para SQL Server | `migracao-dados.md` |
| Dado fictício no banco de DEV para testar tela e procedure (`carga-mockup.sql`) | `skills/power-platform/references/carga-mockup.md` §6 (script `montar-carga-mockup.py` do orquestrador) |
| Entender o que já deu errado em projetos reais | `licoes-de-campo.md` |
| Auditar procedures existentes | rode o lint (abaixo) e `padrao-procedure.md` §13 |

2. **Leia o ambiente antes de escrever** (N1, N3): nomes de procedure (`sys.procedures`), tabelas e
   colunas com tipo e nulidade (`sys.columns`), PKs, `Flg_*` anuláveis, collation e nível de
   compatibilidade. Consultas prontas em `modelo-de-dados.md` §10 e `deploy-e-dba.md` §3. Nome que
   não foi lido do ambiente é **hipótese**: marque.
3. **Escolha a variante** (`padrao-procedure.md` §5). Sem sinal em contrário, declarativa. Registre no
   contrato qual foi e por quê.
4. **Escreva a partir do molde**, uma ação de negócio por procedure; parâmetro em cinco classes
   (a PK, b valores, c chamador, d trilha, e flags); literais de estado no corpo.
5. **Escreva o contrato** (`assets/contrato-procedure-molde.md`): assinatura com classe, tabela de
   códigos, obrigações do flow, testes de aceite. Confira contra o flow (`contrato-proc-flow.md` §4).
6. **Rode o lint e as provas** (tabela abaixo e `deploy-e-dba.md` §3). Corrija na fonte, não no `.sql`
   gerado.
7. **Entregue ao DBA** (`deploy-e-dba.md`): DDL à mão, procedures numeradas, `GRANT` por último,
   itens em hold marcados.
8. **Feche com o portão do projeto** (skill `power-platform`).

## Referências

| Arquivo | Quando ler |
|---|---|
| [padrao-procedure.md](references/padrao-procedure.md) | envelope, retorno, vocabulário de códigos, declarativa × clássica, `UPDLOCK/HOLDLOCK`, parâmetros, `OUTPUT` |
| [contrato-proc-flow.md](references/contrato-proc-flow.md) | o que a procedure promete, obrigações do flow, checklist de divergência, parâmetro JSON |
| [modelo-de-dados.md](references/modelo-de-dados.md) | prefixos, auditoria, trigger, flags, perfil, collation, `CHAR`, índices únicos |
| [colunas-calculadas-delegacao.md](references/colunas-calculadas-delegacao.md) | `Ref_` de data, contagem, status derivado, índice, entrega ao DBA |
| [escopo-por-unidade.md](references/escopo-por-unidade.md) | os três estados do escopo, lista via JSON, códigos prefix-free, `StartsWith` e `NULL` |
| [seguranca-e-permissoes.md](references/seguranca-e-permissoes.md) | conta de serviço, o que a procedure autoriza, quando discordar de A2, consultas de verificação |
| [deploy-e-dba.md](references/deploy-e-dba.md) | ordem de scripts, provas de ambiente, congelamento, nomes as-built, conferência final |
| [migracao-dados.md](references/migracao-dados.md) | playbook de carga: staging, validação, trigger, reseed, reconciliação, rollback |
| [licoes-de-campo.md](references/licoes-de-campo.md) | defeitos que a revisão adversarial achou, a ponte entre schema proposto e real, divergência que some |
| `assets/procedure-escrita-molde.sql` | molde de UPDATE de estado e de INSERT com guarda (passa no lint) |
| `assets/funcao-leitura-molde.sql` | função inline com `@Filtros` JSON + escopo, contagem e listagem |
| `assets/contrato-procedure-molde.md` | contrato por procedure, com classes de parâmetro e códigos |
| `assets/pedido-ddl-dba-molde.md` | pedido de DDL com critério, prova, risco e rollback |

## Scripts

`<pasta-da-skill>` é o *Base directory* que aparece quando a skill é carregada. Rode **da raiz do
projeto** (o script procura `power-platform.config.json` do diretório atual para cima) ou passe
`--config`. Só **leem**; não escrevem em disco.

| Comando | O que checa | Exit |
|---|---|---|
| `python <pasta-da-skill>/scripts/lint-procedure.py <pasta ou arquivo>` | cada `CREATE/ALTER PROCEDURE\|FUNCTION` de `.sql` e de blocos ```` ```sql ```` em `.md`: `P001` NOCOUNT, `P002` XACT_ABORT, `P003` TRAN sem COMMIT, `P004` retorno de 4 colunas, `P005` nome, `P006` CAST de data para INT, `P007` `SELECT *`, `P008` sem schema, `P009` SQL dinâmico concatenado, `P010` NOLOCK, `P011` OUTPUT sem INTO | 0 sem erro · 1 com erro · 2 uso incorreto |
| `python <pasta-da-skill>/scripts/lint-procedure.py` | sem argumento usa `pastas.procedures` e `ignorar` de `power-platform.config.json` | idem |
| `python <pasta-da-skill>/scripts/lint-procedure.py x.sql --padrao-nome "^usp_\w+$"` | regex de nome (default aceita `usp_` e `SP_`); também `padrao_nome_procedure` no config | idem |
| `python <pasta-da-skill>/scripts/lint-procedure.py x.sql --colunas-retorno ""` | desliga `P004`; também `colunas_retorno_procedure` no config | idem |

Saída: `caminho:linha: ERRO|AVISO P0xx mensagem` e `N erro(s), M aviso(s)`. Comentários e literais
são ignorados ao casar padrões. Dispense uma linha com `-- lint-ok P009` e **uma frase dizendo por
quê**. O lint não substitui compilar numa instância: ele não resolve nomes nem tipos.

## Definição de pronto

Cada item tem evidência executável; "feito" sem comando e saída não vale. Comandos da raiz do projeto (nota em Scripts).

- [ ] `python <pasta-da-skill>/scripts/lint-procedure.py <pasta>` → `0 erro(s)`; avisos restantes têm decisão escrita
- [ ] a procedure compila numa instância de DEV (`SET PARSEONLY ON` não basta) e o teste N-1 passa:
      `EXEC` de cada procedure de escrita devolve **1** result set, **1** linha, **4** colunas, também
      quando grava zero linha
- [ ] provas de ambiente rodadas e coladas (`deploy-e-dba.md` §3): `COMPATIBILITY_LEVEL >= 130` se há
      JSON, `OUTPUT ... INTO` com trigger ativo, identidade do app × coluna, collation
- [ ] consultas de `seguranca-e-permissoes.md` §7 voltam vazias: conta sem DML (direto e por papel); `NOCOUNT` em toda
      procedure e trigger; sem SQL dinâmico não revisado
- [ ] vocabulário de códigos igual no `.sql`, no contrato e no `Switch` do flow
      (`contrato-proc-flow.md` §4, itens 1 a 8)
- [ ] `Flg_*` sem coluna anulável (consulta de `modelo-de-dados.md` §4 vazia) e códigos de unidade
      prefix-free, se usa `StartsWith` (consulta de `escopo-por-unidade.md` §5 vazia)
- [ ] os quatro testes de escopo do `escopo-por-unidade.md` §8 dão os resultados esperados
- [ ] pedido de DDL preenchido com saída real das consultas, sem placeholder
- [ ] o contrato diz qual variante, quais obrigações o flow tem e o que a trilha **não** prova

## Armadilhas

As dez mais caras:

1. **Sem `SET NOCOUNT ON`** (inclusive em trigger): o retorno muda sem erro.
   [padrao-procedure.md §2](references/padrao-procedure.md), [modelo-de-dados.md §3](references/modelo-de-dados.md)
2. **`OUTPUT` sem `INTO`**, ou ler `Dt_Alteracao` pelo `OUTPUT` de tabela com trigger.
   [padrao-procedure.md §11](references/padrao-procedure.md)
3. **`CAST(<data> AS INT)`** em coluna de filtro: arredonda.
   [colunas-calculadas-delegacao.md §3](references/colunas-calculadas-delegacao.md)
4. **`NULL` de escopo passando por `coalesce`** no flow: vira `''` e o relatório volta vazio.
   [escopo-por-unidade.md §2](references/escopo-por-unidade.md)
5. **Parâmetro do tamanho exato do valor** (`NVARCHAR(36)` para GUID): trunca em silêncio.
   [padrao-procedure.md §10](references/padrao-procedure.md)
6. **`Flg_*` anulável**: `NULL` em flag nega (ou libera) tudo, sem segunda linha de defesa.
   [modelo-de-dados.md §4](references/modelo-de-dados.md)
7. **Identidade com duas colunas** (e-mail no app, UPN na procedure): toda escrita negada.
   [seguranca-e-permissoes.md §5](references/seguranca-e-permissoes.md)
8. **`@Id_UsuarioChamador` tratado como prova de autoria**: é declaração do chamador.
   [seguranca-e-permissoes.md §5](references/seguranca-e-permissoes.md)
9. **Rodar o gerador sobre gabarito corrigido à mão**, ou nome de procedure da documentação em vez do
   real. [deploy-e-dba.md §7](references/deploy-e-dba.md)
10. **Pedir ao DBA tabela/view/coluna nova depois do congelamento** sem a saída que a tela ou o flow
    teria sem ela. [deploy-e-dba.md §6](references/deploy-e-dba.md)
