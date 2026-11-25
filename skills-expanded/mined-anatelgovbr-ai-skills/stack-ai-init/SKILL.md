---
name: stack-ai-init
description: >
  Instala a estrutura minima da stack de IA em um repositorio de destino: AGENTS.md,
  CLAUDE.md, .agents/skills/ com a skill-creator, o SpecKit completo em .specify/ e as
  integracoes de Claude Code, GitHub Copilot, OpenCode e VS Code, com documentação
  inicial de arquitetura, requisitos e operação. Copia os artefatos
  como estao, preserva permissoes e nao toca no que o destino ja escreveu.

  Use quando o pedido for instalar, adicionar, levar, copiar, portar, provisionar ou
  atualizar a stack de IA, o SpecKit, o AGENTS.md ou as skills em outro repositorio;
  preparar um projeto para trabalhar com agentes; ou conferir se uma instalacao
  existente ainda bate com o que a skill distribui.

  Nao usar para popular o AGENTS.md com conhecimento do projeto, investigar codigo ou
  criar skill nova: isso e da stack-ai-build-project-context e da skill-creator.
---

# stack-ai-init

Deposita a estrutura minima da stack de IA na raiz de um repositorio de destino. Nada mais.

Esta skill copia os artefatos da stack e preserva os arquivos próprios do destino. A avaliação da organização da aplicação se limita à estrutura visível da raiz. A `stack-ai-build-project-context` investiga o código e enriquece a stack em outra rodada.

## Regra de nao enriquecimento

Toda a decisao ja esta tomada dentro de `assets/`. Voce nao escolhe arquivo, nao adapta conteudo, nao renomeia pasta, nao preenche `AGENTS.md`, nao ajusta caminho para a arquitetura do destino e nao acrescenta item por achar que faz sentido. Se o desenvolvedor pedir algo alem da instalacao, diga que isso e outra tarefa e siga com a instalacao.

Se voce acha que a carga precisa mudar, o caminho e editar `assets/` desta skill (ver `references/payload.md`), nunca improvisar durante a instalacao de um destino.

## O que e instalado

| Grupo | Conteudo |
|---|---|
| Raiz | `AGENTS.md`, `CLAUDE.md`, `.gitignore` |
| `ops/` | `README.md` introdutório e `roteiro.md` para planejar ambientes e testes. Cada documento é criado quando falta, inclusive em uma pasta existente |
| `.agents/references/` | `speckit.md`, a regra de manutencao das fases; `template-revisao-tecnica.md`, o formato do relatorio de revisao tecnica, para a skill de revisao do projeto |
| `.agents/security/` | `guia-seguranca.md`, 19 topicos de risco agnosticos de linguagem, com rastreio para OWASP Top 10:2025 e CWE; `mapa-cwe-guia.md`, ponte da `owasp-playbook`, com a traducao de CWE para topico e as secoes que o projeto preenche |
| `.agents/skills/` | 22 skills: a `skill-creator`, as 10 fases do SpecKit em `speckit-<fase>/`, a `owasp-playbook`, com o OWASP Secure Agent Playbook copiado em `upstream/`, e 10 skills de apoio: 4 de terceiros (`caveman`, `grill-me`, `grilling` e `writing-for-agents`), a `frontend-design` da Anthropic e 5 mantidas pela Anatel no repositorio `ai-skills` (`configuracao-de-testes-unitarios`, `dicionario-dados-db-scan-codebase-docs`, `gauntlet-loop-forge`, `manual-creator-scan-codebase` e `stack-ai-build-project-context`) |
| `.claude/` | `settings.json`, que registra o marketplace local e liga o plugin `stack-ai` |
| `.claude-plugin/` | `marketplace.json`, o plugin local que aponta o Claude Code para `.agents/skills/`; o nome do marketplace sai do diretorio de destino |
| `.github/` | `copilot-instructions.md` |
| `.opencode/` | `opencode.json` e `.gitignore` |
| `.specify/` | scripts, templates, workflows, manifestos e `memory/constitution.md` |
| `.vscode/` | as tres chaves `chat.*` que apontam o Copilot para `.agents/skills/` |
| `docs/stack-ai/` | a documentacao da stack para quem usa: indice, conceito, SpecKit, manutencao e prompts genericos |
| `docs/architecture/` | a documentação de arquitetura do projeto: `README.md` com a organização da pasta, `ADR-TEMPLATE.md` e `adr/README.md`, com as regras de ADR |
| `docs/requisitos-ancorados/padrao/` | as regras do formato dos requisitos do sistema e os quatro templates; os documentos de requisitos do projeto nascem na raiz de `docs/requisitos-ancorados/`, a partir desses templates |

Inventario completo, exclusoes e o motivo de cada uma: `references/payload.md`.

## Como cada ferramenta chega nas skills

Nenhuma das tres usa symlink. Cada uma tem um caminho proprio de configuracao, todos apontando para `.agents/skills/`:

| Ferramenta | Caminho |
|---|---|
| Claude Code | plugin local `stack-ai`, do marketplace local do repositorio, declarado em `.claude-plugin/marketplace.json` e ligado em `.claude/settings.json` |
| Copilot | chave `chat.agentSkillsLocations` em `.vscode/settings.json` |
| OpenCode | chave `skills.paths` em `.opencode/opencode.json` |

No Claude Code o plugin so vale a partir da segunda sessao: a primeira abertura na pasta registra o marketplace, a seguinte ja carrega as skills. Avise isso ao desenvolvedor no relatorio final.

### Nome do marketplace

O plugin chama-se sempre `stack-ai`, entao a invocacao e `/stack-ai:<skill>` em qualquer repositorio. O marketplace, nao: cada repositorio tem o seu.

O Claude Code guarda os marketplaces em um registro da maquina, em `~/.claude/plugins/known_marketplaces.json`, com um caminho so por nome. Dois repositorios com o mesmo nome de marketplace disputam a mesma entrada: o segundo perde, e passa a receber as skills do primeiro sem aviso nenhum. Como a chave de plugin e `<plugin>@<marketplace>`, basta o marketplace ser unico.

**Destino que ainda nao tem nome.** Os dois arquivos da carga trazem `{{MARKETPLACE}}` no lugar do nome, e a instalacao troca pelo nome do diretorio de destino reduzido a `[a-z0-9-]`, com o prefixo `stack-ai-`. Um destino em `meu-projeto` recebe `stack-ai-meu-projeto`. Nenhum parametro a informar.

**Destino que ja tem nome.** O nome do destino vale, seja ele qual for. A derivacao e so o padrao de criacao, nao um formato a impor: o que o nome precisa e ser unico entre repositorios, e um que ja existe e funciona ja cumpre isso. A instalacao le o nome em `.claude-plugin/marketplace.json`, cai para a chave `stack-ai@<marketplace>` de `enabledPlugins` quando aquele arquivo falta, e usa o que achar nos dois arquivos. Nada e acrescentado ao lado do que ja esta la, e o `verificar` nao acusa divergencia por causa do nome.

Renomear uma instalacao existente nao traz ganho: quebraria a chave `stack-ai@<marketplace>` ja ligada e deixaria uma entrada orfa no registro da maquina.

## Fluxo

### 1. Confirme o destino e avalie o isolamento da aplicação

O caminho da raiz do repositorio de destino e informado pelo desenvolvedor. Nunca assuma o repositorio atual, nunca deduza o destino de um arquivo aberto. Sem caminho, pergunte.

Liste apenas as entradas da raiz e confira o tipo de `src` e `fontes` por metadados. Se houver um único diretório real com um desses nomes, relate-o como candidato a concentrar o código da aplicação. A existência da pasta indica uma convenção possível, sem confirmar onde todo o código está.

Se houver dois candidatos, nenhum, uma entrada de tipo inesperado ou indicação de outro nome, confirme com o desenvolvedor onde fica o código e se há mais de uma raiz. Aceite o local que ele indicar. Para um projeto sem código que queira definir um diretório, sugira `src/`. Registre no plano a pasta observada ou a dúvida em aberto e prossiga com a simulação e as demais etapas autorizadas.

Preserve a estrutura da aplicação. Restrinja a avaliação a nomes e tipos das entradas, sem abrir código, criar diretórios de aplicação, mover arquivos ou escolher tecnologia.

### 2. Simule

```bash
python3 <caminho-desta-skill>/scripts/instalar_stack.py simular --destino <raiz do destino>
```

Use o caminho absoluto da propria skill: o diretorio de trabalho da sessao e quase sempre o
destino ou outro repositorio, e `scripts/` relativo aponta para o lugar errado ou para nada.

Se a instalação do Python 3 responder por `python`, use esse comando no lugar de `python3`.

### 3. Mostre o plano e peca confirmacao

Apresente quantos arquivos seriam criados, preservados ou mesclados, quais documentos de `ops/` faltam e quais caminhos têm colisões. Escrever na raiz de outro repositorio e acao dificil de reverter; so instale depois do "pode ir".

### 4. Instale

```bash
python3 <caminho-desta-skill>/scripts/instalar_stack.py instalar --destino <raiz do destino>
```

Use `--sobrescrever` somente quando o desenvolvedor pedir explicitamente para atualizar arquivos da stack que ja existem e divergem. Preserve sempre `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/architecture/README.md` e todos os arquivos existentes de `ops/`.

### 5. Relate

Diga o que foi criado, o que foi preservado e por que, e o que ficou pendente. Informe a localização observada ou indicada para a aplicação e o resultado de `ops/README.md` e `ops/roteiro.md`. Depois aponte os tres proximos passos que pertencem ao desenvolvedor:

1. preencher o `AGENTS.md` com contexto, dependencias e limites de escrita do projeto;
2. instalar uma das ferramentas suportadas, se ainda nao usar nenhuma;
3. ler `docs/stack-ai/README.md`, que explica a stack recem-instalada, e linkar a pasta do `README.md` do projeto. Esse passo e do desenvolvedor porque a carga nunca escreve no `README.md` do destino, entao sem o link a documentacao chega e ninguem descobre que ela existe.

Se o repositorio de destino ja for versionado, lembre que a mudanca deve ir em branch propria e Pull Request.

## Regras de colisao

| Situacao | O que acontece |
|---|---|
| Arquivo da stack ausente no destino | criado |
| Arquivo da stack identico ao da carga | ignorado, sem ruido |
| Arquivo da stack diferente | preservado; so muda com `--sobrescrever` |
| `AGENTS.md`, `CLAUDE.md`, `README.md` e `docs/architecture/README.md` ja existentes | preservados sempre, mesmo com `--sobrescrever` |
| `ops/` existente | recebe somente `README.md` e `roteiro.md` que estiverem ausentes, mesmo com `--sobrescrever`; o instalador relata colisões de tipo, links e junções como `erro` e preserva esses caminhos |
| `.gitignore` da raiz | criado quando ausente; se já existe, recebe acréscimos no fim. O padrão `.env*` vale em qualquer profundidade e fica depois de eventuais regras de exceção (`!`) no mesmo arquivo |
| `.gitignore` de destino que ja tem pasta `specs/` | recebe as linhas que faltam, menos a que ignora `specs/`: o destino fica como esta, ignorando ou versionando |
| `.vscode/settings.json` do destino | recebe so as chaves e subchaves que faltam; valor ja definido nao muda |
| `.claude/settings.json` do destino | recebe so as chaves e subchaves que faltam; marketplace e plugin ja declarados pelo time nao mudam |
| Destino que ja declara marketplace com nome diferente do derivado | o nome do destino vale; a carga adota ele nos dois arquivos e nao acrescenta chave nenhuma |
| `.vscode/settings.json` ou `.claude/settings.json` com comentario ou virgula sobrando | nao e tocado; o relatorio traz as chaves para acrescentar a mao |

Rodar de novo no mesmo destino nao muda nada e sai com codigo 0.

O ambiente de `ops/` é responsabilidade do projeto. A skill deixa intactos os `.gitignore` de subpastas, cujas regras podem prevalecer, e os arquivos já rastreados pelo Git.

## Vocabulario do relatorio

`criado`, `substituido`, `mesclado`, `ignorado-igual` e `proprio-do-destino` sao resultados limpos. `ignorado-existe`, `ignorado-protegido`, `manual`, `divergente` e `ausente` sao pendencias que o desenvolvedor precisa ver. `erro` interrompe a confianca no resultado e deve ser investigado antes de qualquer outra coisa.

Codigos de saida: `0` sem pendencia, `1` com pendencia, `2` erro.

## Conferir uma instalacao antiga

```bash
python3 <caminho-desta-skill>/scripts/instalar_stack.py verificar --destino <raiz do destino>
```

Nao escreve nada. Compara arquivo a arquivo por sha256 e devolve `igual`, `divergente` ou `ausente`. `AGENTS.md`, `CLAUDE.md`, `README.md` e `docs/architecture/README.md` aparecem como `proprio-do-destino`, porque ali divergir e o esperado.

Para `ops/`, verifica individualmente a presença de `README.md` e `roteiro.md`. Arquivos comuns existentes aparecem como `proprio-do-destino` sem leitura do conteúdo. Caminhos vagos aparecem como `ausente`. Links, junções e ocupações de tipo incompatível aparecem como `erro`.

Nos dois arquivos JSON que recebem o nome do marketplace, a comparacao ignora apenas diferencas de fim de linha.

Arquivo executável na carga que perdeu a permissão de execução no destino aparece como `divergente`, mesmo com o conteúdo igual, e só volta a ser executável com `--sobrescrever`.

## Manutencao da carga

`assets/stack/` e a fonte de verdade da stack: quem mantem edita esses arquivos direto, com o nome mapeado para `dot-` onde houver ponto. Nao existe repositorio molde de onde puxar. Somente as skills selecionadas em `references/payload.md` sao copiadas a mao de `.agents/skills/` deste repositorio para a carga, sem script de sincronizacao. O inventario, as exclusoes e o passo a passo de uma alteracao estao nesse arquivo.
