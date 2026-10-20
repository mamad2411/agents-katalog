---
name: aporte-dividendos
description: >
  Analisa uma carteira de dividendos a partir de uma planilha XLSX de posição
  (ex.: export da B3 com abas de Ações e FIIs) e decide como distribuir um valor
  disponível para aporte entre os ativos. Para cada ativo instancia o agente
  analista-dividendos (em ondas de no máximo 5 em paralelo), consolida os
  pareceres aplicando os métodos Barsi (ações e FIIs) e Dornelas (FIIs), e
  devolve a alocação sugerida em R$ por ativo. Use quando o usuário pedir para
  analisar a carteira / planilha e distribuir um aporte.
disable-model-invocation: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Agent
  - Skill
---

# Aporte em carteira de dividendos

Orquestra a análise de uma carteira e distribui um valor de aporte entre os ativos.

## Entradas (de `$ARGUMENTS`)

1. **Caminho do XLSX** da posição (ex.: `posicao-2026-06-23-18-15-57.xlsx`). Se o
   usuário não passar, use o XLSX mais recente no diretório do projeto.
2. **Valor disponível para investimento** em R$ (ex.: `5000`, `R$ 5.000,00`).

Se faltar o valor de aporte, **pergunte** antes de prosseguir. Não invente o valor.

## Passo 0 — Ler recomendações XP (sinal secundário)

Antes de tudo, colha as carteiras recomendadas XP como **sinal de confirmação** (nunca
override do teu método). Uma vez só, no início.

1. Ache a pasta de mês mais recente em `/home/dev/repos/my-tools/carteiras/`
   (ex.: `Carteiras recomendadas XP Junho 2026`). Se houver várias, use a mais nova.
2. Com o **Read tool** (suporta PDF, use `pages`), leia **apenas** o subset de dividendos/FII:
   - `Top Dividendos XP – <mês>.pdf`
   - `Carteira Top Dividendos Plus – <mês>.pdf`
   - `Carteira Dividendos Gráfica – <mês>.pdf`
   - `Carteira Fundamentalista de Fundos Imobiliários – <mês>.pdf`
   - `Estratégia Quant Carteira Viva de Renda com FIIs – <mês>.pdf`

   Ignore as demais (ETFs, renda fixa, global, small caps, ESG) — não são dividendos BR.
3. Extraia por PDF a lista de **tickers** (e peso-alvo/rank se aparecer). Monte um mapa:
   `xp[TICKER] = { carteiras: [nomes], peso_alvo?: %, rank? }`.

Se a pasta não existir ou nenhum PDF de dividendos estiver lá, **siga sem o sinal XP**
(registre "sem recomendações XP") — o método próprio basta.

Esse mapa fica só no teu contexto (main thread). **Não** repasse ao agente do Passo 2 —
o parecer dele tem que ser independente da XP.

## Passo 1 — Extrair a carteira

Rode o extrator (parser stdlib, lê todas as abas, não exige openpyxl):

```bash
python3 /home/dev/repos/my-tools/.claude/skills/aporte-dividendos/scripts/extract_carteira.py "<CAMINHO_XLSX>"
```

Saída JSON: `abas[]` com `aba`, `tipo` (`acao` | `fii` | `desconhecido`) e
`ativos[]` (`ticker`, `produto`, `quantidade`, `preco_fechamento`,
`valor_atualizado`); e `total_atualizado`.

- Ignore ativos com `valor_atualizado` e `preco_fechamento` ambos zero/nulos
  (ex.: frações como `RECR12`), mas registre que foram pulados.
- Se `tipo` vier `desconhecido`, classifique pelo sufixo do ticker (FII normalmente
  termina em `11` e é fundo imobiliário) ou deixe o agente classificar.

## Passo 2 — Analisar cada ativo (ondas de 5)

Para **cada ticker**, instancie o subagente `analista-dividendos` (agentType
`analista-dividendos`) passando só o ticker e o tipo provável. Ele já pesquisa
dados atuais via Tavily e devolve parecer estruturado com veredito e preço-teto.

**Regra de paralelismo: no máximo 5 agentes por vez.** Dispare em ondas — envie 5
chamadas `Agent` numa única mensagem, aguarde todas, então a próxima onda de 5,
até cobrir todos os tickers. Não passe de 5 em paralelo.

Guarde, por ticker: tipo (ação/FII), veredito (Comprar na baixa / Acumular /
Observar / Evitar), preço atual, preço-teto/justo e os pontos-chave.

## Passo 3 — Consolidar com os frameworks dos livros

Reúna todos os pareceres num texto único e aplique as bases de conhecimento:

- **Sempre** invoque a skill `barsi-dividendos` (vale para ações e FIIs): ranqueie
  pela ótica de renda perene/previdenciária — setor perene, dividendo recorrente
  e sustentável, preço abaixo do valor ("comprar na baixa"), preço-teto por
  DY-alvo.
- **Para os FIIs**, invoque também a skill `dornelas-fiis`: P/VP (caro/barato vs
  patrimônio), DY, vacância física/financeira, queima de caixa (rendimento
  sustentável vs distribuição artificial), tipo de fundo e impacto de IR.

Use os frameworks dessas skills para transformar os pareceres em um **score base**
por ativo (priorize "Comprar na baixa" abaixo do preço-teto; penalize
"Observar/Evitar", P/VP esticado, queima de caixa, dividendo inflado).

### Fator XP (aplicado sobre o score base)

Cruze cada ticker com o mapa `xp[]` do Passo 0. XP é **confirmação secundária, nunca
override** — Barsi/Dornelas + o parecer do agente mandam. Ajuste:

| Condição | Efeito |
|---|---|
| Em carteira XP **e** veredito "Comprar na baixa"/"Acumular" | boost **+15–20%** (confirmação dupla) |
| Em 2+ carteiras XP (ex.: Top Div + Fundamentalista) | boost no **topo** da faixa |
| Em carteira XP **mas** veredito "Observar" | boost pequeno **+5%** (XP vê valor, teu método não — cautela) |
| Em carteira XP **mas** veredito "Evitar" | **sem boost** — método próprio vence. **Loga a divergência** |
| **Não** em nenhuma carteira XP | score base puro, **sem penalidade** |

`score_final = score_base * (1 + boost_xp)`.

**Sempre registre divergências** XP↔análise (XP recomenda e teu método reprova, ou o
inverso) — esse sinal é mais útil que o consenso. Vai no resumo do Passo 5.

## Passo 4 — Distribuir o aporte

Distribua o **valor disponível** entre os ativos conforme a prioridade:

- Concentre nos ativos com melhor veredito **e** preço atual abaixo do preço-teto.
- Respeite a lógica de carteira: não jogue tudo num só ativo; busque diversificação
  entre setores perenes (Barsi) e entre tipos de FII (Dornelas), sem reforçar o que
  está "Evitar".
- Pode sugerir **R$ 0** para ativos a apenas observar/evitar e explicar o porquê.
- A soma das alocações ≈ valor disponível (informe sobras por indivisibilidade de
  cotas, se relevante).

## Passo 5 — Entregar

Tabela final, ordenada por valor de aporte (maior → menor):

```
| Ticker | Tipo | Veredito | Preço atual | Preço-teto | XP | Aporte (R$) | % do aporte | Motivo |
```

Coluna **XP** = quais carteiras XP listam o ticker (ex.: `TopDiv, Fund.FII`) ou `—`.

Depois:
- **Resumo da estratégia** do rateio (por que concentrou onde concentrou), incluindo
  onde a XP **confirmou** e onde **divergiu** da tua análise.
- **Total alocado** vs valor disponível e eventual sobra.
- Ressalva: parecer analítico **educacional**, não recomendação formal de
  investimento.

Por fim, **salve o relatório completo em Markdown na raiz do projeto**:
`/home/dev/repos/my-tools/aporte-<AAAA-MM-DD>.md` (data do dia). Conteúdo: a tabela
de distribuição, o resumo da estratégia, os pareceres resumidos por ativo (veredito,
preço, teto, P/VP quando FII, nota-chave), as confirmações/divergências XP e a
ressalva. Se o arquivo do dia já existir, sobrescreva.

## Regras

- Nunca invente cotações/indicadores — vêm dos agentes (Tavily). Sem dado: registre
  "não encontrado" e seja conservador na alocação.
- Recomendação XP = sinal **secundário** de confirmação, nunca override. "Evitar" pela
  tua análise vence estar em carteira XP. Sem PDFs XP: siga sem o sinal.
- Máximo 5 agentes em paralelo, sempre.
- Valores em R$, percentuais explícitos.
