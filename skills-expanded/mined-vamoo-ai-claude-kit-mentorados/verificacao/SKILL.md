---
name: verificacao
description: >-
  Casos de verificação end-to-end aprendidos em produção: testar TODOS os ramos,
  rodar TODOS os runners, pegar o erro REAL de prod antes do repro, inspecionar
  a UI. Use antes de declarar "pronto" em fix com ramos, mudança de UI, erro de
  prod mascarado, bug difícil, pasta com múltiplos runners, e ANTES de qualquer
  disparo que chega numa pessoa (mensagem, e-mail, cobrança, webhook). Gatilhos:
  "pronto", "verificar", "debug", "testar antes de entregar", "dry-run", "pode disparar?".
---

# Verificação e2e — casos de produção

Os princípios (verificar antes de afirmar, tsc+lint, caminho real do usuário)
vivem no CLAUDE.md. Aqui ficam os casos de produção, por categoria.

## Fix em fluxo com ramos → teste TODOS os ramos

Mexeu em nó/módulo/função **compartilhado** por N ramos (IF/Switch, texto vs
áudio, N webhooks/tipos de evento, feliz vs erro) → exercite os N antes de
"pronto". O que conserta um ramo pode quebrar o irmão. Verificar só um caminho
e declarar pronto já mascarou regressão (fix de áudio num workflow n8n que quebrou o
ramo de texto, 2026-06-17).

## Múltiplos runners → rode TODOS

Um mesmo arquivo de teste pode ser coletado por mais de um runner (vitest
globando `supabase/functions/**` além do deno; jest+vitest). Adicionou teste
numa pasta coberta por N runners → registre nas listas include/exclude de cada
um E rode os N. Validar só um runner mascarou regressão (teste deno coletado
pelo vitest quebrou a suíte, 2026-06-29).

## Erro de prod mascarado → pegue o erro REAL primeiro

Digest / "Server Components render" / Sentry / 500-503 genérico: pegue o erro
REAL primeiro — logs/Observability do Vercel pelo digest, Sentry, ou peça pro
usuário colar — ANTES de montar repro local. Repro que não exercita o caminho
real engana: passa verde e some o bug (ex: render em vitest/jsdom NÃO tem
fronteira RSC, então erro server→client de Next "passa"). O erro real aponta
arquivo:linha na hora; horas de eliminação não. No caso RSC ("Functions cannot be passed
directly to Client Components", digest constante), leia
[`references/rsc-client-boundary.md`](references/rsc-client-boundary.md).

## Bug difícil → um loop vermelho antes da hipótese

Bug que não se explica no primeiro olhar, regressão de desempenho ou falha intermitente: antes
de ler código para montar teoria, tenha **um comando já rodado** que fica vermelho com o
sintoma exato que a pessoa relatou, em segundos e com o mesmo veredito toda vez. Só então:
reduza o caso ao mínimo, escreva 3 a 5 hipóteses que dizem o que preveem e mostre à pessoa,
instrumente uma variável por vez com log marcado (`[DEBUG-a4f2]`, que sai por grep), e
escreva o teste de regressão antes do fix. As formas de montar o loop, o caso intermitente e o
checklist de limpeza: [`references/diagnostico-de-bug.md`](references/diagnostico-de-bug.md).

## Mudança que toca UI → inspeção visual

Rode o app (o comando de dev do projeto, na seção `## Comandos` do `AGENTS.md`) e
exercite a mudança antes de "pronto", incluindo estados interativos (clique,
hover, loading, empty) — static check não pega blur, layout quebrado nem botão
morto. Se você tiver o MCP do navegador, estado, texto e erro se conferem lendo
a página como texto (`read_page`, `get_page_text`); screenshot só onde o pixel é
a evidência (blur, layout, cor), e QA visual com mais de 2 screenshots vai para um
subagente, que devolve o veredito em texto. Sem ele, peça à pessoa que abra a página e diga
(ou mande o print de) o que viu. Isso é bug de entrega, não polimento.

QA em subagent devolve o veredito no formato de `references/qa-taxonomia.md`:
severidade (crítico/alto/médio/baixo), categoria, passos e a contagem do que
foi coberto. "Nenhum achado" sem contagem é relatório vazio.

## O que só um humano consegue verificar → roteiro, não pedido no meio da prosa

"O áudio toca no celular", "a notificação chegou", "o PDF sai certo na
impressora": build e teste verdes não dizem nada sobre isso. Em feature com
**mídia, push ou impressão**, o roteiro humano faz parte do pronto, como `tsc` e
lint. Pedido em prosa ("dá uma olhada se tocou?") volta solto e não vira
evidência: **escreva um roteiro** num arquivo, a pessoa roda no terminal dela, e
as respostas voltam em `KEY=VALUE`:

```bash
# /tmp/roteiro-push.txt (escrito pelo agente)
passo Abra o app no celular e entre com a conta de teste
captura CHEGOU Dispare o lembrete pelo painel. A notificação chegou? (s/n)
captura ERRO Se não chegou, cole o erro do console (ou 'nenhum')

# o que a pessoa roda, num terminal dela
bash "${CLAUDE_PLUGIN_ROOT}/scripts/hitl-loop.sh" /tmp/roteiro-push.txt --saida /tmp/capturado.txt
```

Regras do roteiro:

- **Você não roda o script no seu Bash**: sem terminal ele sai 2 ("sem terminal
  interativo") antes da primeira pergunta. Quem roda é a pessoa.
- **Comando pronto para colar, com caminhos absolutos**: o `${CLAUDE_PLUGIN_ROOT}`
  vem preenchido para você, mas o terminal da pessoa não conhece a variável.
- **Uma pergunta por observação, com resposta objetiva** (s/n, o número, a
  mensagem colada). "Deu certo?" não é observação.
- **Enter vazio reprova** (exit 1 nomeando a variável). **Exit 0 quer dizer
  "todas respondidas", não "passou"**: `CHEGOU=n` com exit 0 é reprovação.
- **A resposta é a evidência**: cole o bloco `--- capturado ---` do `--saida` no
  relatório, igual output de `tsc`. Vale para o degrau 3 (smoke real) do efeito
  colateral externo abaixo: quem confirma que chegou é quem recebeu.

## CI vermelho ou teste instável → o erro literal antes da hipótese

Pegue a mensagem literal (`gh run view <id> --log-failed`; rerodado e verde, a
tentativa 1 sai pelo `gh api .../attempts/1/logs`) antes de olhar diff e
arquitetura. "Instável" exige as três juntas: fora do seu diff, passa local **e**
o rerun fecha verde. O caso que ensinou isso, os comandos completos e as duas
causas que mais voltam (`sleep` no lugar de condição; o teste que suja o estado,
achado com `scripts/find-polluter.sh`) estão em `references/testes-flaky.md`.

## Refactor de arquivo grande → tsc do projeto inteiro

Extrair código muda o tipo inferido em call sites que você não abriu, e pode empurrar o
arquivo de destino acima do teto. O check de "pronto" de um refactor é o `tsc` do projeto
inteiro e o lint de novo, nunca só o arquivo mexido. Onde cortar e as duas pegadinhas com
exemplo: [`references/refactor-por-costura.md`](references/refactor-por-costura.md).

## Efeito colateral externo → simulado, dry-run, e só então o real

Vale para tudo que sai da sua máquina e chega numa pessoa: mensagem de
WhatsApp, e-mail, cobrança, webhook em sistema de terceiro, post. Aqui "rodei e
passou" e "mandei mensagem errada pra 200 pessoas" são separados por um degrau
só, e ele quase nunca é escrito:

1. **Simulado** — provider fake/mock. Prova a lógica, prova ramo, não prova
   integração.
2. **Dry-run com o envio final bloqueado** — o fluxo REAL roda inteiro (fila,
   template, dedupe, guard de pausa, montagem do payload), e a última chamada,
   a que entrega, é a única coisa desligada. Logue o payload exato que teria
   saído e confira destinatário, texto e contagem. É aqui que aparecem os erros
   que o mock não tem: destinatário duplicado, template com variável vazia,
   lista maior do que devia.
3. **Smoke real e limitado, com autorização explícita** — um destinatário, seu
   próprio número, e você olhando. Nunca um lote, nunca "só pra ver se sobe".

O degrau 2 é o que costuma faltar: sem ele, o primeiro exercício do caminho
real de verdade é o disparo em produção. Um flag de ambiente (`DRY_RUN=1`) que
corta só o `POST` de entrega custa uma linha e é o que separa teste de
incidente.

**A contagem antes do disparo é parte do teste.** Antes de tirar o freio,
imprima quantos vão receber e quem são os 3 primeiros. Número que surpreende =
não dispare; um filtro está errado.

## Fechamento

Converta o teste descartável em ao menos UM teste que fica no repo. Depois do fix: causa
raiz e como prevenir a categoria do bug. Antes de
reportar, leia o `git diff`, que mostra inclusive o que entrou sem querer; reabrir
cada arquivo editado não acrescenta nada.
