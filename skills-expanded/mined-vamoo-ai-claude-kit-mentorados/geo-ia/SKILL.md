---
name: geo-ia
description: >-
  Site aparecer nas respostas do ChatGPT e do Perplexity (GEO): base técnica, indexação no
  Google e no Bing, medição semanal com Canonry e decisão de conteúdo por pergunta. Só
  dispara quando você chama: /kit-vamoo:geo-ia.
disable-model-invocation: true
---

# GEO: aparecer quando alguém pergunta para uma IA

> Origem: o site institucional da VAMOO AI, de 23/10 a 03/11/2026. A primeira medição deu 0
> de 14 nas perguntas sem marca. A causa não era falta de conteúdo: três das quatro páginas
> comerciais não estavam no índice do Google, e só a home estava no do Bing. Os erros que se
> repetiram: decidir página nova antes de as IAs conseguirem ver as que já existiam, e
> comparar semanas com metade dos provedores sem perceber.

## Fronteira

| Pergunta | Onde |
|---|---|
| "Por que a IA não cita meu site e o que faço?" | esta skill |
| "O site está lento?" | `otimizar-app` |
| "Posso dizer que está pronto?" | `verificacao` |
| "Manda pro ar" | `ship` |

## Regra que decide tudo: indexação antes de conteúdo

Sem a página no índice, nenhuma mudança de copy ou página nova tem atribuição. A ordem é
fixa, e cada fase só começa quando a anterior foi conferida:

0. **Linha de base**: as perguntas, medidas antes de mexer em qualquer coisa.
1. **Base técnica**: o crawler consegue ler o site.
2. **Indexação**: as páginas comerciais estão no Google **e** no Bing.
3. **Remedição**: as mesmas perguntas, nas mesmas IAs.
4. **Conteúdo**: só então título, página nova, guia e fontes de fora.

O Bing pesa tanto quanto o Google: o ChatGPT com busca usa muito o índice dele. Página
indexada só no Google ainda é página invisível para parte das respostas.

## 0. As perguntas e a linha de base

- **9 perguntas**: 7 sem marca, no jeito que o cliente do mentorado pergunta ("empresa que
  faz X em Y", "curso de X para o time"), e 2 de marca ("O que é <marca>?", "Quem é <fundador>
  da <marca>?"). As de marca mostram se a IA conhece a empresa; as sem marca mostram se ela
  recomenda.
- As perguntas ficam num arquivo versionado do projeto (`geo-perguntas.txt`, na pasta
  `scripts/` dele), uma por linha.
  Trocar uma pergunta quebra a comparação com as semanas anteriores: registre a data.
- Meça antes de qualquer edit. Sem o número de partida, nenhum ganho depois é demonstrável.

Como medir (Canonry local e Action semanal no GitHub): [references/medicao.md](references/medicao.md).

## 1. Base técnica

Checklist com o porquê de cada item e o gate pós-build:
[references/base-tecnica.md](references/base-tecnica.md).

- `robots.txt`, `sitemap.xml` (sem `lastmod` inventado), `llms.txt` e `llms-full.txt`.
- HTML pré-renderizado por rota. SPA que só monta no navegador entrega página vazia para
  boa parte dos crawlers de IA.
- `title` e primeira frase de cada página dizendo a intenção ("treinamento de X in company",
  não "Bem-vindo").
- JSON-LD montado do mesmo dado que a página mostra: FAQPage com as perguntas da página,
  Organization com `sameAs` e `foundingDate` verdadeiros.
- 404 de verdade (status 404, `noindex`, sem canonical) e `www` redirecionando para o apex.
- IndexNow avisado a cada deploy (Bing, Copilot e outros).

## 2. Indexação: conferir, não supor

Passo a passo no Search Console e no Bing Webmaster Tools:
[references/indexacao.md](references/indexacao.md).

- **Inspeção de URL**, página por página. O relatório de cobertura tem atraso de dias.
- Estados que importam: Google "URL está no Google"; Bing "Indexed successfully". "Descoberta,
  mas não rastreada" no Bing é o caso mais comum e se resolve com "Request indexing".
- Mudou título ou texto? Peça indexação de novo. O Google guarda o que leu no último
  rastreamento, e um deploy depois dele não muda o índice sozinho.
- Pedir indexação é envio na conta do mentorado: confirme antes de clicar.

## 3. Remedição

- Mesmas 9 perguntas, mesmos provedores. Rodada com um provedor faltando não se compara com
  semana cheia: o script da medição avisa no topo do relatório
  (`scripts/geo-provedores.sh`).
- As respostas variam entre rodadas. Leia a tendência de várias semanas; uma citação isolada
  não é resultado.
- Separe citada (o link aparece nas fontes) de mencionada (o nome aparece no texto).

## 4. Conteúdo: decidir por pergunta

Matriz por pergunta, frentes e quando página nova vale a pena:
[references/plano-conteudo.md](references/plano-conteudo.md).

- Para cada pergunta sem marca: qual página deveria ganhar, o que as páginas citadas têm e a
  nossa não, e quem de fora aparece (mídia, lista de "melhores", instituição).
- Primeiro ajuste o que existe (título, descrição, FAQ). Página nova só para intenção que de
  fato é outra; página quase igual à existente divide a relevância.
- Pergunta dominada por imprensa ou instituição não se ganha com página: é trabalho fora do
  site (lista, release, evento, podcast).
- Número só com fonte. Nome, tela ou setor identificável de cliente do mentorado só com
  autorização escrita.

## Armadilhas que já custaram uma semana

| Sintoma | Causa | O que fazer |
|---|---|---|
| Medição verde, mas só um provedor no resultado | a API do provedor falhou e a saída ficava fora do log | `geo-provedores.sh` no script; ler o log do passo "Medir" |
| Perplexity 403 "requires paid credits" com saldo na conta | o saldo é crédito gratuito (assinatura); a Agent API só aceita crédito comprado | comprar crédito; o nível de uso -1 e o histórico de faturas vazio confirmam |
| Placar com "Window: 2 run(s)" e números que não batem com a lista | runner self-hosted (ou o Mac) guarda o `~/.canonry` entre rodadas | `visibility-stats --last-runs 1` e `sources --run-id`, como no script |
| Título novo no ar, resposta da IA com o antigo | Google rastreou antes do deploy | inspeção de URL e "Solicitar indexação" |
| Bing não lista o site para importar do Search Console | a importação não mostra propriedade de domínio | adicionar manual e verificar pela meta `msvalidate.01` |
| 404, robots ou Content-Type "errados" no preview | preview com login (SSO) | testar só em produção, com `curl` |
| Chave de provedor no histórico do shell | `--api-key` na linha de comando | chave por arquivo `600` ou pelo dashboard; nos Secrets do repo para a Action |

## Saída

Ao fim de cada fase, registre em `.context/docs/geo.md` do projeto: data, o que foi
conferido e onde (Search Console, Bing, run da medição). A decisão de conteúdo vai num
plano separado (`.context/docs/geo-plano-conteudo.md`) com a matriz por pergunta.

Veredito de remedição, sempre nesta forma: estado de indexação por página nos dois índices,
comparação das rodadas (com provedores presentes em cada uma) e se a fase 4 está liberada.
