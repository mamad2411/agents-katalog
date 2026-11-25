---
name: hermeticidade-de-teste
description: Testes que escrevem fora da própria bolha — variável de ambiente do executor (GIT_DIR, CARGO_TARGET_DIR) atravessando a fronteira que o teste existe para garantir, o resíduo permanente que isso deixa no repositório real, e como limpá-lo sem apagar trabalho. Carregar antes de escrever teste que spawna processo (git, cargo, npm, sandbox), ao ver teste que falha só num contexto (no hook sim, no terminal não), e ao encontrar branch, commit ou worktree que ninguém reconhece.
---

# Hermeticidade de teste — quando o ambiente atravessa a bolha

Um teste que cria "um repositório temporário" e roda `git` dentro dele só é hermético se nada do ambiente de quem o chamou alcançar o processo filho. O executor (hook de git, CI, outro script) costuma exportar variáveis que mudam o alvo do comando sem nenhum erro.

## 1. `GIT_DIR` — o mais caro, porque deixa resíduo permanente

O git invoca hooks com `GIT_DIR` (e às vezes `GIT_WORK_TREE`/`GIT_INDEX_FILE`) apontando para o repositório que está sendo empurrado. Tudo que o hook spawna herda — inclusive a suíte de testes, cujos testes de "repositório temporário" passam a operar no repositório REAL.

Casos de origem: dezenas de testes reprovando juntos só dentro do hook (zero no terminal); e branches/commits de teste aparecendo no repositório real, que ninguém reconhecia.

Correção nos dois lados:
- no hook/executor: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE` antes de rodar qualquer gate;
- no teste: construa o `env` do processo filho explicitamente, sem essas variáveis, e com `GIT_CONFIG_GLOBAL` apontando para um arquivo do próprio teste.

## 2. Variável de saída do build — falha determinística que parece bug do produto

`CARGO_TARGET_DIR` (e equivalentes) redireciona artefatos; um teste que procura o binário no lugar padrão falha sempre num contexto e nunca no outro. Leia o caminho da variável, não presuma o padrão.

## 3. O caso inverso: a variável que PRECISA existir

Alguns executores exigem uma variável para funcionar no ambiente (ex.: plataforma do browser de teste). Limpar o ambiente inteiro quebra o teste por outro motivo. Hermeticidade é escolher o que entra, não apagar tudo.

## 4. Processo com NOME controlado

Teste que mata ou procura processo por nome casa o próprio comando (`pgrep -f`/`pkill -f` encontram a linha do shell que os chamou). Use PID, `pidof` pelo caminho do executável, ou um arquivo-marcador escrito pelo processo.

## 5. Serviço "isolado" que busca coisas fora da bolha

Diretório de dados, cache de modelo, porta, arquivo de PID, config do usuário: confira cada um antes de declarar um serviço de teste isolado. Uma peça esquecida contamina o teste seguinte — e, com executor persistente (runner self-hosted), o job seguinte.

## Como suspeitar antes de perder um dia

- Falha só num contexto (hook, CI, sua máquina)? Compare o `env` dos dois contextos antes de olhar o código.
- Muitos testes de famílias diferentes reprovando juntos, nenhum do seu diff? Ambiente, não código.
- Branch/commit/worktree que ninguém reconhece? Pode ser resíduo de teste — confira autor, mensagem e data contra a execução da suíte.

## Limpar resíduo sem apagar trabalho

Classifique antes (ver `varredura-git-multi-repo`): resíduo de teste tem padrão reconhecível (mensagem fixa, autor de teste, arquivo de fixture). Prove que o conteúdo não existe em nenhum trabalho real antes de remover, e remova pela referência exata.

## A regra que sobra

Teste que spawna processo declara o ambiente do filho por inteiro. Herança implícita é o defeito.
