---
name: ai-project-structure
version: "2.15.0"
description: Cria, atualiza e valida a estrutura Markdown multiagente (AGENTS.md, CLAUDE.md, GEMINI.md e memoria em docs/ com SESSION, MEMORY, CONSENSUS, DECISIONS, TASKS) para projeto tocado por varias IAs ou sessoes. Use quando o pedido citar essa estrutura, seus arquivos ou a skill pelo nome ("estrutura multiagente", "AGENTS.md e docs/", "memoria do projeto em docs/"); para converter um diretorio, ATUALIZAR para a versao nova da skill ou VALIDAR a estrutura; para ativar specs, ativar, rodar ou configurar o loop, ou ativar o modulo github (comunidade, templates, CI); ou para rodar consenso com outros modelos ("roda um consenso", "segunda opiniao", "revalida o achado", "retoma a rodada"). NAO dispare sozinha em pedido generico de criar projeto, pasta, repositorio ou scaffold ("cria projeto", "inicia projeto novo", "monta a base") que nao cite a estrutura; quem decide se o projeto precisa dela e o usuario ou o agente gestor, e no maximo ofereca em uma linha. Cria os arquivos de fato.
---

# AI Project Structure

Esta skill **cria a estrutura Markdown multiagente em um projeto novo**, copiando os templates de `assets/` para o destino, preenchendo `PROJECT_CONTEXT.md` com nome e objetivo informados pelo usuario, e abrindo a primeira entrada em `SESSION.md`.

A estrutura tem como nucleo:
- raiz minima com arquivos de entrada dos agentes (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`);
- memoria do projeto em `docs/` com `PROJECT_CONTEXT`, `SESSION`, `MEMORY`, `CONSENSUS`, `TASKS`, `DECISIONS`, `QUALITY`, `CHANGELOG` e `archive/`;
- arquivos opcionais (`ARCHITECTURE`, `API`, `DATA_MODEL`, `GLOSSARY`, `ONBOARDING`, `ROADMAP`, `PROMPTS`, `STACK`);
- modulo opcional de specs (`docs/specs/`) para trabalho tamanho-feature;
- modulo opcional de loop, que executa uma tarefa verificavel sem supervisao. Nunca entra no scaffold e so pode ser ativado em projeto que ja tem comando real em "Testes E Validacao" de `QUALITY.md`;
- modulo opcional `github`, que entrega a camada GitHub do repositorio (arquivos de comunidade, templates de issue e PR, `dependabot.yml`, `ci.yml`). So entra com resposta explicita na pergunta 5; com ele ativo, a raiz minima admite tambem `.github/` e dotfiles de configuracao (como `.gitattributes`).

A partir da versao 2.2.0 a estrutura tambem cobra que o trabalho seja verificavel:

- toda tarefa concluida em `TASKS.md` carrega uma sub-linha `Evidencia:`, e a tarefa aberta pode declarar antes como sera verificada com `(verifica: <comando>)`;
- tarefa travada por pergunta ao usuario vai para a secao `## Aguardando Usuario`, com a pergunta registrada e um campo para a resposta;
- cada entrada de `CONSENSUS.md` declara `Metodo`, `Exposicao previa a outras posicoes` e `Rodada`, para que consenso fraco nao fique parecido com consenso forte.

A partir da versao 2.4.0, `CONSENSUS.md` deixa de servir so para debate:

- entrada que declara `**Achado:** <identificador>` e um **achado**, com disposicao de quem registrou e revalidacao por outro modelo. O identificador e livre; o validador confere que o campo existe e tem valor;
- achado que declarou `**Escapou de verificacao:** sim` traz a secao `Por Que Nada Pegou Antes`, que transforma defeito escapado em conserto de portao;
- o teto de tres rodadas saiu. Da quarta rodada em diante a entrada declara `**Pendente da rodada anterior:**`.

A partir da versao 2.6.0, o validador acusa como ERRO seis contradicoes estruturais que antes passavam em silencio: tarefa concluida sem data, marcador verifica com comando vazio, marcadores em ordem invertida, bloco `loop` sem par ou sem versao, arquivo do nucleo vazio e ID repetido entre o `TASKS.md` vivo e `docs/archive/TASKS-*.md`. O marcador verifica so vale no fim da linha (seguido, no maximo, de outros marcadores); mencao em prosa nao declara comando.

A partir da versao 2.7.0, o validador tambem acusa como AVISO evidencia sem campos preenchidos, espera sem resposta ou marcador bloqueada, exposicao `nao` apos a rodada 1, proximo passo vazio, cerca de codigo aberta, spec concluida sem evidencia, status de tarefa dentro de spec, ID de tarefa fora de `T-NNN`, marcador bloqueada fora de Aguardando Usuario e data de adocao invalida. O marcador verifica so vale no fim da linha (seguido, no maximo, de outros marcadores); mencao em prosa nao declara comando.

## Fluxo

Execute na ordem.

### 0. Identifique o modo

Se o destino ja tem `AGENTS.md` e `docs/SESSION.md` com entradas reais (datas fora de blocos de codigo), isto NAO e um scaffold novo: siga o fluxo de **Atualizacao** em `references/atualizacao.md` desta skill. Se o usuario pediu para validar a estrutura ou criar/ativar specs em projeto existente, veja as secoes no fim deste arquivo. Caso contrario, siga os passos abaixo.

### 1. Confirme o diretorio de destino

Por padrao o destino e o diretorio atual de trabalho (`pwd`). Pergunte ao usuario "criar a estrutura aqui em `<pwd>` ou em outro caminho?" e use o que ele responder. Se ele indicar uma pasta que ainda nao existe, crie-a.

### 2. Verifique conflitos antes de criar

Liste arquivos do destino que coincidem com algum arquivo da estrutura. Se houver conflito, **nao sobrescreva** - pare e pergunte ao usuario o que fazer. Veja a secao "Resolucao De Conflitos" abaixo.

### 3. Entrevista

Regra de ouro: se o pedido inicial do usuario ja respondeu uma pergunta, NAO a repita - registre a resposta e siga. Faca apenas as perguntas em aberto, numeradas, com opcoes numeradas. Toda pergunta aceita resposta livre. "Avançar" adia a resposta e vira pendencia registrada - **nunca autoriza inferir a resposta**.

O usuario pode responder tudo de uma vez (ex: "1: minha-loja; 2: loja de camisetas; 3: 1; 4: 1; 5: 1").

```text
**1. Qual o nome do projeto?**
   1. Usar o nome da pasta de destino: "<nome-da-pasta>"
   2. Escrever outra resposta

**2. Qual o objetivo do projeto?** (uma a tres frases: o que faz e para quem)
   1. Escrever a resposta
   2. Avançar - deixa "(A preencher.)" no PROJECT_CONTEXT.md e cria a tarefa
      "Preencher objetivo do projeto" em TASKS.md

**3. Estrutura completa ou minimal?**
   1. Minimal (recomendado para comecar) - so o nucleo
   2. Completa - nucleo + opcionais (ARCHITECTURE, API, DATA_MODEL, GLOSSARY,
      ONBOARDING, ROADMAP, PROMPTS, STACK)
   3. Escrever outra resposta (ex: "minimal + ARCHITECTURE")

**4. Ativar o modulo de specs (docs/specs/)?**
   1. Nao (recomendado) - da para ativar depois pedindo a esta skill
   2. Sim - cria docs/specs/README.md e insere o bloco de specs em AGENTS.md

**5. Ativar a camada GitHub (modulo github)?**
   1. Nao (recomendado) - da para ativar depois pedindo a esta skill
   2. Sim, em ingles (en) - comunidade, templates, dependabot e ci.yml em ingles
   3. Sim, em portugues (pt-BR) - os mesmos arquivos em portugues
```

Sem preferencia clara nas perguntas 3, 4 e 5, sugira as opcoes marcadas como recomendadas. Na pergunta 5, "Avançar" ou silencio contam como nao responder: o modulo `github` nao ativa sem resposta explicita, e a lingua nunca e escolhida por inferencia.

Nao pergunte sobre git. **Nao inicialize repositorio git** a menos que o usuario peca explicitamente.

### 4. Copie os arquivos do `assets/` desta skill para o destino

Mantenha exatamente a estrutura de pastas (raiz + `docs/` + `docs/archive/`).

**Nucleo (sempre criado):**

```
AGENTS.md
CLAUDE.md
GEMINI.md
docs/README.md
docs/PROJECT_CONTEXT.md
docs/SESSION.md
docs/MEMORY.md
docs/CONSENSUS.md
docs/TASKS.md
docs/DECISIONS.md
docs/QUALITY.md
docs/CHANGELOG.md
docs/archive/README.md
```

**Opcionais (so para "completa"):**

```
docs/ARCHITECTURE.md
docs/API.md
docs/DATA_MODEL.md
docs/GLOSSARY.md
docs/ONBOARDING.md
docs/ROADMAP.md
docs/PROMPTS.md
docs/STACK.md
```

`STACK.md` tambem pode nascer depois, sozinho, quando o projeto ganhar codigo: e o mapa de tecnologias, pacotes e links de documentacao oficial que o agente consulta antes de mexer na stack.

**Modulo de specs (so se ativado na pergunta 4):**

- copie `assets/docs/specs/README.md` para `docs/specs/README.md`;
- insira o conteudo de `assets/partials/AGENTS-specs-block.md` em `AGENTS.md`, logo apos o marcador `<!-- ai-project-structure:core:end -->` e antes de "## Regras Do Projeto".

**Modulo github (so se ativado na pergunta 5):** siga `references/github.md`: copie a lista da lingua escolhida de `assets/github/<lingua>/`, pergunte item a item `docs/CODE_OF_CONDUCT.md` (default sim) e `.gitattributes` (default nao), preencha `{{SKILL_VERSION}}` e `{{QUALITY_COMMAND}}` do `ci.yml` e insira o conteudo de `assets/partials/AGENTS-github-block.md` em `AGENTS.md`, depois do ultimo bloco gerenciado e antes de "## Regras Do Projeto". No scaffold novo nao ha arquivo pre-existente; em projeto existente, arquivo que ja existe e pulado e listado.

**Nunca copie `assets/partials/` para o projeto-alvo** - e material de insercao da skill, nao template de arquivo.

### 5. Preencha `docs/PROJECT_CONTEXT.md`

Substitua os placeholders das secoes:

- **Objetivo Do Projeto**: cole o objetivo informado pelo usuario. Se o usuario avancou a pergunta 2, deixe "(A preencher.)" e crie a tarefa "Preencher objetivo do projeto" em `TASKS.md` - nunca invente um objetivo.
- **Publico Ou Usuario Final**: deixe placeholder marcando que o usuario deve preencher (ex: "(A preencher.)").

Mantenha as demais secoes como estao no template - elas serao preenchidas pelo usuario depois. Adicione no topo, antes da primeira secao, uma linha indicando o nome do projeto:

```md
**Nome do projeto:** <nome informado>
```

### 5b. Preencha a data de adocao em `docs/TASKS.md`

No cabecalho de `docs/TASKS.md`, troque o placeholder do marcador `(convencoes-2-2-0-desde: AAAA-MM-DD)` pela data de hoje. E a data a partir da qual a evidencia de fechamento passa a ser cobrada nesse projeto. Sem ela, o validador nao cobra evidencia de nenhuma tarefa.

### 6. Adicione a primeira entrada em `docs/SESSION.md`

O template termina no fim do bloco cercado de "Modelo Para Nova Sessao". Insira **depois** desse bloco, no fim do arquivo, nunca dentro da cerca:

```md
## AAAA-MM-DD - <agente que executou (ex: Claude, Codex, Gemini)>

### Objetivo

- Inicializar a estrutura multiagente para o projeto "<nome>".

### O Que Foi Feito

- Criada a estrutura Markdown multiagente (nivel <completa | minimal>) em <caminho absoluto>.
- `PROJECT_CONTEXT.md` preenchido com nome e objetivo informados pelo usuario.

### Arquivos Criados Ou Alterados

- (Listar todos os arquivos criados, com caminho relativo a raiz do novo projeto.)

### Decisoes Tomadas

- Nivel de estrutura escolhido: <completa | minimal>.
- Modulo de specs: <ativado | nao ativado>.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Preencher os demais campos de `PROJECT_CONTEXT.md` (publico, estado atual, restricoes, fora de escopo).
- Preencher `TASKS.md` com tarefas iniciais.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: estrutura pronta; proxima acao depende do projeto.
```

Use a data de hoje no formato AAAA-MM-DD.

### 7. Reporte ao usuario

No final, liste de forma curta:

- caminho absoluto do destino;
- nivel escolhido (completa ou minimal), se o modulo de specs foi ativado e se o modulo `github` foi ativado (e em que lingua);
- versao da estrutura: 2.15.0;
- arquivos criados (em arvore);
- proximo passo sugerido: preencher os demais campos de `PROJECT_CONTEXT.md` e adicionar tarefas iniciais em `TASKS.md`;
- oferta: "quer validar a estrutura? `python3 <dir-desta-skill>/scripts/validate_structure.py <destino>`".

## Resolucao De Conflitos

Se um arquivo do destino tem o mesmo nome de um arquivo da estrutura:

- **Conteudo identico ao template**: pule esse arquivo, nao precisa fazer nada.
- **Conteudo diferente**: pergunte ao usuario, por arquivo:
  - **(a) preservar o existente** (pular esse arquivo);
  - **(b) substituir pelo template** (sobrescreve apos confirmacao explicita);
  - **(c) mostrar diff e decidir caso a caso**.

Nunca sobrescreva sem confirmacao explicita do usuario para aquele arquivo. Em duvida, prefira preservar - o usuario sempre pode substituir manualmente depois.

Se o destino ja parece ser um projeto desta estrutura (ja tem `AGENTS.md` e `docs/SESSION.md` com entradas reais), nao siga com o scaffold: use o fluxo de **Atualizacao** (`references/atualizacao.md`) - provavelmente o usuario quer atualizar ou validar, nao recriar.

## Atualizar Ou Validar Estrutura Existente

Para projeto que ja usa esta estrutura:

- **Atualizar** para a versao atual da skill (v1 → v2, ou v2 → v2.x): siga `references/atualizacao.md`. O fluxo detecta a versao pelos marcadores em `AGENTS.md`, mostra diff por bloco e nunca sobrescreve sem confirmacao por item.
- **Validar**: rode `python3 <dir-desta-skill>/scripts/validate_structure.py <projeto>` e reporte o resultado. `--strict` trata avisos como falha. `--codigos` troca o relatorio por uma linha por diagnostico (`NIVEL|CODIGO|ARQUIVO|SUJEITO`): e o que usar para montar portao, porque o codigo e estavel e a redacao da mensagem nao.

## Criar Spec Ou Ativar O Modulo Em Projeto Existente

Siga `references/specs.md` para: ativar o modulo de specs em um projeto que nao o tem, ou criar uma nova spec (`docs/specs/NNNN-slug.md`) com entrevista curta e tarefas em `TASKS.md`.

## Rodar Uma Tarefa Com O Loop

Quando o usuario pedir para rodar o loop em uma tarefa (ex: "roda o loop na T-042", "manda a T-042 para o loop executar"), **monte a chamada para ele**. Ele nao deve precisar lembrar flags.

1. **Confirme que o modulo esta ativo** no projeto: o `AGENTS.md` precisa ter o bloco entre `ai-project-structure:loop:start` e `loop:end`. Sem isso, ofereca a ativacao (secao abaixo) em vez de rodar.
2. **Confira a tarefa.** Ela precisa ter `(verifica: <comando>)`. Se nao tiver, nao invente um comando: mostre a tarefa e pergunte qual comando prova que ela ficou pronta. Tarefa sem portao nao entra no loop.
3. **Leia os perfis** em `docs/MEMORY.md`, secao `## User`. Eles mapeiam intencao e ferramenta para o comando do agente. Se nao existirem, pergunte qual ferramenta e qual modelo usar, e **ofereca registrar o perfil** ali para nao perguntar de novo. Nunca invente nome de modelo nem flag: se nao souber, pergunte (regra "Nunca Inferir").
4. **Se os perfis de executar tiverem degraus de esforco**, proponha um a partir da tarefa e diga o motivo em uma linha, seguindo "Escolher O Nivel De Esforco" em `references/loop.md`. Na duvida entre dois, proponha o mais baixo.
5. **Monte e mostre o comando antes de rodar**, para o usuario poder corrigir:

```bash
<dir-desta-skill>/scripts/loop.sh --tarefa T-042 --agente "<perfil escolhido>"
```

6. **Rode e reporte** o que aconteceu, traduzindo o exit code: 0 fechou com evidencia, 2 o portao falhou em todas as tentativas, 3 a tarefa foi para "Aguardando Usuario" com uma pergunta, 4 o comando do agente esta mal configurado. Em 3, mostre a pergunta que ficou registrada.

A tabela de comandos por ferramenta, as armadilhas de flag e o formato dos perfis estao em `references/loop.md`.

Dentro de uma thread do Cloudroom, o `--agente` pode ser `scripts/cloudroom_agente.py`, que roda a tarefa como filho visivel na barra do Cloudroom. Uso, exit codes e limites (inclusive o de que o `--projeto` tem de ser a pasta da thread) estao em `references/cloudroom.md`.

**Configurar os perfis**: quando o usuario pedir para ver, trocar ou criar perfil ("configura os perfis do loop", "que modelo o loop esta usando", "quero trocar o modelo"), siga a secao "Configurar Os Perfis" de `references/loop.md`. Ela mostra o que existe hoje, pergunta o que mudar com opcoes numeradas e confirma os nomes de modelo na propria CLI antes de gravar.

## Rodar Uma Rodada De Consenso

Quando o usuario pedir uma segunda opiniao de outros modelos (ex: "roda um consenso sobre isso", "pede ao Codex e ao Grok", "revalida o achado N10 com outro modelo", "retoma a rodada"), **monte a chamada de `scripts/consenso.py` para ele**. A pessoa nao deve precisar lembrar flags.

1. **Confirme a pergunta em arquivo.** `debate` recebe `--pergunta` como caminho. Se a pergunta ainda esta so na conversa, escreva-a num arquivo, mostre o texto e peca confirmacao antes de rodar. Para achado, confirme o titulo exato da entrada em `docs/CONSENSUS.md`.
2. **Leia os perfis de consenso** em `docs/MEMORY.md`, secao `## User`, e monte cada `--agente ID "COMANDO"` a partir deles. Nunca invente modelo nem flag: sem perfil, pergunte qual ferramenta e qual modelo e ofereca registrar o perfil. Comando somente-leitura por ferramenta esta em `references/consenso.md`. Debate pede dois agentes ou mais; achado, um ou mais.
3. **Pergunte a rodada** quando nao for a primeira, e quais posicoes anteriores entram (`--anterior`). O script nunca deduz o numero nem os anteriores; da rodada 4 em diante, `--pendente` e texto da pessoa.
4. **Mostre o comando antes de rodar**, para a pessoa corrigir. Lembre que nao ha teto de custo: N agentes e modelo caro gastam plano dela.

```bash
<dir-desta-skill>/scripts/consenso.py debate --projeto . --pergunta pergunta.txt \
  --agente codex "<perfil de consenso do Codex>" --agente grok "<perfil de consenso do Grok>"
```

5. **Rode e traduza o exit code**: 0 a rodada fechou e a minuta (ou a revalidacao) esta em `docs/CONSENSUS.md`; 2 nenhum agente deu posicao, `CONSENSUS.md` intacto; 5 outra rodada ativa no projeto, nada foi alterado; 6 padrao de segredo, a rodada parou e o material esta fora do projeto. Exit 1 e erro de uso ou rodada interrompida; a mensagem cita o comando de retomada. Em 5 e 6, mostre a mensagem do script e **nunca limpe o lock nem retome por conta propria**: retomar e comando explicito da pessoa.
6. **Entregue sem julgar.** As secoes de julgamento (`Pontos De Acordo`, `Riscos E Tradeoffs`, `Consenso Final`, `Decisao Para Registrar Em DECISIONS.md`) nascem com "(A preencher.)" e sao da pessoa. Nao resuma as posicoes como se fossem consenso, nao declare convergencia e nao decida por maioria; diga onde estao a entrada e o sidecar `docs/consensus/<run-id>/` e deixe a pessoa ler.

Limites, ditos sempre que couber: a varredura de segredo tem falso negativo, nao ha teto de custo e `docs/MEMORY.md` desatualizado dispara o revisor errado. Uso, exit codes, forma da entrada, retomada e "O Que A Operacao Nunca Faz" estao em `references/consenso.md`.

## Ativar O Modulo De Loop

Siga `references/loop.md`. **Nunca ative no scaffold**, em nenhum nivel, e nunca ofereca a ativacao por conta propria: ela e sempre pedido explicito do usuario.

Antes de tocar qualquer arquivo, confira o portao: a secao "Testes E Validacao" de `docs/QUALITY.md` do projeto-alvo precisa ter comando executavel. Vazia, ou ainda com o texto do template, a ativacao e **recusada**, com o motivo dito ao usuario. Um loop sem portao real nao sabe se o trabalho ficou bom, e um portao falso e pior que nenhum.

## Ativar O Modulo GitHub

Siga `references/github.md`. **Nunca ative sem resposta explicita**: sem resposta na pergunta 5 (ou fora do scaffold, sem pedido claro do usuario), o modulo `github` nao ativa, e a lingua dos arquivos (`en` ou `pt-BR`) nunca e escolhida por inferencia.

A skill copia arquivos e insere o bloco em `AGENTS.md`. Ela **nao roda `gh`** nem faz push, tag ou Release: a configuracao do repositorio e o fluxo de versao sao checklist em `references/github.md`, feitos pela pessoa ou pelo agente de chat com o sim dela. Arquivo que ja existe no projeto e pulado e listado, nunca mesclado.

## Arquivos Em `assets/`

Os templates ficam em `assets/`:

```text
assets/
  AGENTS.md
  CLAUDE.md
  GEMINI.md
  partials/
    AGENTS-specs-block.md   (material de insercao; nunca copiado ao projeto)
    AGENTS-loop-block.md    (idem, so quando o modulo de loop e ativado)
    AGENTS-github-block.md  (idem, so quando o modulo github e ativado)
  github/
    en/  pt-BR/             (so copiado quando o modulo github e ativado; mesma lista nas duas linguas:
                             docs/ com comunidade, .github/ com templates, dependabot.yml e ci.yml, .gitattributes)
  docs/
    README.md
    PROJECT_CONTEXT.md
    SESSION.md
    MEMORY.md
    CONSENSUS.md
    TASKS.md
    DECISIONS.md
    QUALITY.md
    CHANGELOG.md
    PROMPTS.md
    ARCHITECTURE.md
    API.md
    DATA_MODEL.md
    GLOSSARY.md
    ONBOARDING.md
    ROADMAP.md
    STACK.md
    specs/
      README.md             (so copiado quando o modulo de specs e ativado)
    archive/
      README.md
```

Eles sao templates limpos: `SESSION.md`, `CONSENSUS.md`, `TASKS.md`, `DECISIONS.md`, `CHANGELOG.md` e `ROADMAP.md` nao trazem entradas historicas. `PROJECT_CONTEXT.md` tem placeholders que voce preenche no passo 5.

## Validacao

Antes de finalizar, rode o validador:

```bash
python3 <dir-desta-skill>/scripts/validate_structure.py <destino>
```

Zero erros esperado em scaffold recem-criado. Se o Python nao estiver disponivel, confira manualmente:

- todos os arquivos esperados foram criados no destino (lista do passo 4 conforme o nivel escolhido);
- `PROJECT_CONTEXT.md` foi preenchido com nome e objetivo informados (ou "(A preencher.)" registrado como pendencia, se o usuario avancou);
- `SESSION.md` recebeu a primeira entrada (passo 6) e nao apenas o template;
- `AGENTS.md` contem os marcadores `ai-project-structure:core:start`/`end` (e `specs` e `github`, se ativados);
- nenhum arquivo existente foi sobrescrito sem permissao;
- `docs/archive/` existe (mesmo que so com `README.md`);
- `docs/TASKS.md` tem a secao `## Aguardando Usuario` e a data preenchida no marcador `(convencoes-2-2-0-desde:)`;
- nenhum repositorio git foi inicializado (a menos que o usuario tenha pedido).
