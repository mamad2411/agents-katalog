# Padrão de skill deste repositório

Toda skill em `skills/` segue este documento. O que é verificável está no lint
(`python tools/lint_skills.py`); o resto é checado em revisão.

## Sumário

1. [Estrutura do repositório](#1-estrutura-do-repositório)
2. [Estrutura de uma skill](#2-estrutura-de-uma-skill)
3. [Frontmatter](#3-frontmatter)
4. [Corpo do SKILL.md](#4-corpo-do-skillmd)
5. [Referências](#5-referências)
6. [Scripts](#6-scripts)
7. [Fronteiras entre skills](#7-fronteiras-entre-skills)
8. [Sanitização](#8-sanitização)
9. [Versionamento](#9-versionamento)
10. [Como validar antes de commitar](#10-como-validar-antes-de-commitar)

---

## 1. Estrutura do repositório

```
.claude-plugin/plugin.json        manifesto do plugin (versão semver)
.claude-plugin/marketplace.json   permite /plugin marketplace add <repo>
skills/<nome>/                    uma pasta por skill
agents/agente-<nome>.md           agentes do pipeline (subagentes com papel fixo, chamados pelas etapas)
tests/<nome>/                     testes dos scripts da skill (pytest) + fixtures
tests/_lint/                      testes do lint (fora da varredura de sanitização)
tools/lint_skills.py              lint deste padrão
docs/                             este padrão, configuração por projeto
CHANGELOG.md
```

## 2. Estrutura de uma skill

```
skills/<nome>/
├── SKILL.md        obrigatório
├── references/     conhecimento carregado sob demanda (.md)
│   └── licoes-de-campo.md lições de produção sem projeto, domínio, data ou contagem (opcional)
├── scripts/        validadores e ferramentas (Python)
├── assets/         moldes copiáveis: tela, contrato, proc, flow, tokens
└── prompts/        só no orquestrador: modelos de prompt para auditoria de app existente
```

- A pasta se chama `references/` (plural). `reference/` é recusada pelo lint.
- Testes **não** ficam dentro da skill — ficam em `tests/<nome>/`.

### Dois tipos de skill

| Tipo | Exemplos | Quem invoca | Corpo |
|---|---|---|---|
| **Domínio e orquestrador** | `powerapps-canvas`, `power-automate`, `sql-procedures`, `dataverse`, `power-platform` | o modelo, pela `description`, ou o usuário | seções da §4 |
| **Etapa do pipeline** | `novo`, `brainstorm`, `design`, `mockups`, `prototipo`, `arquitetura`, `construir`, `testar`, `homologar`, `publicar`, `progresso` | **só o usuário**, pelo comando `/pp:<etapa>` (`disable-model-invocation: true`) | seções da §4.1 |

A skill de etapa é fina: o conhecimento fica nas skills de domínio e nas referências do
orquestrador, que ela aponta por `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/...` (o lint só confere
caminhos relativos à própria skill).

## 3. Frontmatter

```yaml
---
name: powerapps-canvas            # igual ao nome da pasta, kebab-case
description: "Use quando ... Não use para ... (use `outra-skill`)."
argument-hint: "[tela|formula|auditar] [alvo]"   # opcional
user-invocable: true
---
```

Regras para `description` (é ela que decide se a skill dispara):

- Português, até 1024 caracteres, começa com **"Use quando"**.
- Lista **verbos e objetos concretos** e os termos que a pessoa digita
  ("cola esse flow no designer", "o número não bate", "procedure de baixa").
- Termina com **"Não use para ..."** apontando a skill certa para os casos vizinhos.
- Nunca depende de o modelo julgar "complexidade" ou "tamanho" da tarefa.

## 4. Corpo do SKILL.md

Ordem fixa das seções:

1. **Título + 1 parágrafo** — o que a skill produz.
2. **Regras inegociáveis** — numeradas, imperativas; cada uma com `Por quê:` em uma linha.
3. **Fluxo de trabalho** — o passo 1 é a tabela *tarefa → referências a carregar* (no orquestrador,
   logo depois de ler o projeto).
4. **Referências** — tabela `arquivo → quando ler`.
5. **Scripts** — tabela `comando → o que checa → exit code`.
6. **Definição de pronto** — checklist em que cada item tem evidência executável
   (comando + resultado esperado), nunca só "✅".
7. **Armadilhas** (opcional) — as 10 mais caras, cada uma com link para a referência.

Limites: aviso acima de 250 linhas, erro acima de 500. O detalhe vai para `references/`.

### 4.1 Corpo de uma skill de etapa

1. **Título** `/pp:<etapa> — <quem executa>` + 1 parágrafo (etapa N, bloco do desenho, o que sai).
2. **Antes de começar**: `estado.py comecar <etapa>` (exit 1 = fora de ordem: mostrar e parar),
   o que ler, o modo (novo, retomar, ajuste).
3. **Passos**: numerados; checkpoints no formato de `references/formato-saida.md` do orquestrador;
   agentes chamados com `RAIZ` e `KIT`, e a entrega deles conferida.
4. **Portão de saída**: checklist do que prova que a etapa terminou.
5. **Encerrar**: `estado.py concluir|reabrir`, commit se `git_commit_por_etapa`, resumo e o bloco
   "Próximo passo" **impresso pelo script**, nunca escrito à mão.

Alvo: até 100 linhas. Etapa nunca invoca a seguinte: o usuário abre uma sessão nova e roda o comando.

### 4.2 Agentes (`agents/agente-<nome>.md`)

- `name` igual ao arquivo; `description` diz a etapa que o chama e o que **não** faz.
- `tools` mínimos para a entrega (sem Bash quando não precisa rodar nada; sem escrita quando só lê).
  `skills:` com `pp:<skill>` para pré-carregar a skill de domínio, e o corpo manda ler o `SKILL.md`
  se ela não veio.
- Recebe `RAIZ` e `KIT`; nunca fala com o usuário (subagente não pergunta): dúvida vira item da entrega.
- Termina com a seção **Entrega**, de formato fixo: é o que a etapa confere.


## 5. Referências

- **Sumário obrigatório** em arquivo com mais de 300 linhas (seção `## Sumário` ou `## Índice`
  nas primeiras 40 linhas). Acima de 1000 linhas, dividir.
- **Fonte em todo comportamento de plataforma não óbvio**: link do Microsoft Learn, ou
  `[verificado: projeto de referência]`, ou `[não verificado]`. Blog de terceiro não é fonte
  quando contradiz a documentação por conector.
- **Código exemplar completo e colável** — sem `...`, sem pseudo-YAML — e sempre dizendo o
  **destino**: `barra de fórmulas (pt-BR: ; e ;;)` ou `YAML colado (, e ;)`.
- **Só genérico**: as skills não descrevem nenhum projeto. O que um projeto ensinou entra como
  regra (com o `Por quê:`) ou em `references/licoes-de-campo.md`, sem nome de empresa, projeto,
  tela, domínio de negócio, data de evento ou contagem real. Exemplos usam a entidade neutra
  `Pedido` e o escopo `Unidade` (siglas `AAA`, `BBB`).
- Nenhuma referência a `arquivo:linha` de projeto sem o comando que reencontra o trecho
  (linhas envelhecem; nomes de controle e de ação, não).

## 6. Scripts

- Python ≥ 3.10, só biblioteca padrão + PyYAML.
- `argparse` com `--help`. Exit `0` = sem erro, `1` = achou erro, `2` = uso incorreto.
- Saída por achado: `caminho:linha: ERRO|AVISO <CÓDIGO> mensagem` (validador de JSON de uma linha usa o
  nome da ação no lugar da linha: `caminho:<Acao>:`). Última linha: `N erro(s), M aviso(s)`.
- **Só leem** por padrão. Escrever exige flag explícita, nunca sobre o arquivo de entrada.
  Gerador escreve só em `dist/`.
- **Prova de que acusa**: todo validador tem em `tests/<skill>/` pelo menos uma fixture que
  passa e uma que falha com o código de erro esperado. Um validador que nunca acusou nada não
  provou que valida.
- Configuração do projeto: `power-platform.config.json` (ver [CONFIG.md](CONFIG.md)),
  procurado do diretório atual para cima, ou `--config <arquivo>`. Sem config, o script roda
  com defaults genéricos e diz isso na saída.

## 7. Fronteiras entre skills

Cada assunto tem **um** dono. As outras skills apontam para ele em vez de repetir.

| Assunto | Dono | Quem só aponta |
|---|---|---|
| Padrões decididos (contrato de retorno, separadores, layout, nomes) | `power-platform` → `references/decisoes-padrao.md` | todas |
| Pipeline `/pp:*`, `ESTADO.md`, formato de saída das etapas | `power-platform` → `references/pipeline.md`, `formato-saida.md`, `scripts/estado.py` | skills de etapa |
| Protocolo de trabalho, fila `GOAL.md`, investigar, subagentes, portão final | `power-platform` | — |
| ALM: soluções, ambientes, variáveis de ambiente, connection references | `power-platform` → `references/alm-ambientes.md` | power-automate, dataverse |
| YAML de tela, Power Fx, UX, tokens; delegação no conector **SQL** | `powerapps-canvas` | sql-procedures |
| Delegação no conector **Dataverse** | `dataverse` → `references/delegacao-dataverse.md` | powerapps-canvas |
| Chamada `.Run()` do lado do app (loading, toast, `IfError`, refresh) | `powerapps-canvas` | power-automate |
| Definição de flow, clipboard do designer, Try/Catch, HTTP, `$batch`, log | `power-automate` | — |
| Autorização e escopo dentro do flow | `power-automate` | powerapps-canvas, sql-procedures |
| Procedure, DDL, coluna calculada, transação, migração de dados SQL | `sql-procedures` | powerapps-canvas |
| Tabelas Dataverse, Choice/Lookup/texto, Security Role, NOMES-AS-BUILT | `dataverse` | powerapps-canvas |

## 8. Sanitização

O repositório pode ir para o GitHub. **Nunca** entra:

- caminho absoluto de máquina (`C:\Users\...`, `/home/...`, pastas do OneDrive); <!-- lint-ok -->
- nome de servidor, instância, banco, tenant, org ou ambiente reais;
- ID real de connection reference, flow, app, ambiente ou GUID copiado de produção;
- e-mail ou nome de pessoa; dado de negócio real (cliente, unidade, valor);
- nome da empresa ou do projeto de origem, nomes de tela, domínio de negócio, contagens e datas do projeto.

Use placeholders: `<prefixo>_`, `<servidor>\<instancia>`, `<banco>`, `<ambiente>`,
`usuario@contoso.com`. Projeto de origem é sempre "projeto de referência", sem nome.

O lint pega os padrões genéricos (caminho absoluto, e-mail, GUID). Nomes internos
específicos vão em `tools/sanitizacao.local.txt` — **um regex por linha, arquivo não
versionado** (está no `.gitignore`, porque listar os nomes já seria vazá-los).

## 9. Versionamento

- Versão semver em `.claude-plugin/plugin.json` e no `marketplace.json`, iguais.
- Toda mudança entra no `CHANGELOG.md`. Mudar uma regra inegociável é no mínimo *minor*.

## 10. Como validar antes de commitar

```bash
python tools/lint_skills.py          # padrão + sanitização; exit 0 obrigatório
python -m pytest tests -q            # scripts das skills e o próprio lint
claude plugin validate .             # manifesto e frontmatter
```
