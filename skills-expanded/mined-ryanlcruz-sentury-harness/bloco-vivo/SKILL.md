---
name: bloco-vivo
vitrine:
  grupo: 'Visuais'
  rotulo: 'bloco interativo na resposta'
description: "HTML ou SVG interativo dentro da resposta, com o visual e os ícones do Sentury: cartões de número, tabelas, sliders, calculadoras, abas."
version: 1.0.0
author: Sentury
license: MIT
metadata:
  category: creative
---

# Bloco vivo

Um bloco ` ```vivo ` (HTML ou SVG dentro) na resposta vira um quadro interativo
na conversa. Ele roda isolado da página: script funciona (slider, calculadora,
abas, filtro), mas não há rede, não há recurso de fora (fonte, imagem por URL,
biblioteca por CDN) e o bloco não alcança o resto do chat. Tudo o que ele
precisa vai escrito dentro dele.

` ```html ` e ` ```svg ` continuam sendo código: aparecem para ler e copiar, com
um botão para a pessoa ver desenhado. Use-os quando ela pediu o código; use
` ```vivo ` quando você quer mostrar.

## Quando usar

- A resposta fica mais clara com forma: um número grande com a variação, uma
  comparação lado a lado, uma tabela que se filtra, uma simulação ("e se o
  preço subir 10%?").
- A pessoa vai mexer em algo: um slider, um seletor, uma calculadora.

Para texto, lista ou tabela simples, markdown basta. Para entrega que a pessoa
vai baixar, gere o arquivo.

## Painel: o caminho curto

Para o caso comum, descreva o que mostrar num bloco ` ```painel ` com JSON, e
o Sentury monta no visual dele. É mais curto que HTML, sai sempre igual e não
quebra: componente que não existe vira um aviso. Um objeto, uma lista de
objetos ou `{"componentes": [...]}`.

Cor é escolha sua: `cor` aceita um nome (`verde`, `vermelho`, `amarelo`,
`laranja`, `azul`, `roxo`, `rosa`, `ciano`, `cinza`, `ouro`, `tinta`) ou um hex
(`#16a34a`). Use a cor para dizer algo (vermelho para o que estourou, verde para
o que está bem), não para enfeitar. Sem `cor`, medidor e progresso pintam pela
faixa: verde até 75%, amarelo até 90%, vermelho acima.

Componentes (`tipo`):

- `numeros`: cartões de número. `itens`: `rotulo`, `valor`, e opcionais `variacao`, `sentido` (`bom`, `ruim`, `atencao`, `neutro`), `icone`, `cor`, `sub`.
- `tabela`: `colunas` (lista de títulos) e `linhas` (lista de listas); `titulo` opcional. Número em célula alinha à direita.
- `barras`: comparação proporcional. `itens`: `rotulo`, `valor` (número), `cor` e `icone` opcionais; `titulo`, `unidade`, `cor` (de todas) e `maximo` (escala) opcionais.
- `medidor`: anel com o número no centro, para uso e meta (disco, memória, orçamento). `rotulo`, `valor`, `maximo` (padrão 100), `centro` (texto do meio), `sub`, `cor`; ou `itens` com vários medidores lado a lado e `titulo`.
- `rosca`: fatias de um todo, com legenda e percentual. `itens`: `rotulo`, `valor`, `cor`; `centro` (`valor` e `rotulo`), `titulo`, `unidade` opcionais.
- `linha`: série no tempo. `rotulos` (um por ponto) e `series`: `nome`, `cor`, `pontos` (números); `titulo`, `unidade`, `area` (falso tira o preenchimento) opcionais.
- `progresso`: quanto já foi usado de um total (discos, cotas, metas). `itens`: `rotulo`, `usado`, `total`, `unidade`, `icone` ou `app`, `cor`, `sub`.
- `lista`: linhas com ícone. `itens`: `titulo`, `sub`, `icone` ou `app`, `valor`, `cor`; `titulo` opcional.

Quando o item é um programa, use `app` com o nome dele (`steam`, `vscode`, `spotify`, `chrome`, `discord`) em vez de `icone`: o Sentury tem uma tabela de programas com ícone e cor, e programa fora dela ganha a inicial numa cor fixa. Em `lista`, sem `titulo` o nome do programa vira o título. `barras` também aceita `app` por item.
- `simulador`: um controle deslizante e resultados que mudam com ele. `controle`: `rotulo`, `min`, `max`, `passo`, `inicial`, `unidade`. `resultados`: `rotulo`, `formula` (só aritmética com `x`, por exemplo `120.4 * (1 + x / 100)`), `formato` (`numero`, `moeda`, `porcento`), `casas`, `unidade` (por exemplo `mil`), `cor`. `enviar` opcional: mensagem proposta com `{x}` no lugar do valor escolhido.
- `aviso`: `texto`, `sentido` (`info`, `bom`, `atencao`, `ruim`), `icone` e `cor` opcionais.
- `passos`: `itens` com `texto` e `feito` (verdadeiro ou falso); `titulo` opcional.
- `texto`: um parágrafo, com `titulo` opcional.

```painel
[
  {"tipo": "medidor", "titulo": "Discos", "itens": [
    {"rotulo": "C:", "valor": 412, "maximo": 476, "sub": "412 de 476 GB"},
    {"rotulo": "D:", "valor": 380, "maximo": 931, "sub": "380 de 931 GB"}
  ]},
  {"tipo": "rosca", "titulo": "O que ocupa o C:", "unidade": "GB",
   "centro": {"valor": "412 GB", "rotulo": "usados"},
   "itens": [{"rotulo": "Jogos", "valor": 168, "cor": "roxo"}, {"rotulo": "Vídeos", "valor": 97, "cor": "azul"},
             {"rotulo": "Sistema", "valor": 74, "cor": "cinza"}, {"rotulo": "Outros", "valor": 73, "cor": "ouro"}]},
  {"tipo": "lista", "titulo": "Maiores pastas", "itens": [
    {"app": "steam", "sub": "C:/Program Files (x86)/Steam", "valor": "151 GB", "cor": "vermelho"},
    {"titulo": "Vídeos", "sub": "C:/Users/voce/Videos", "icone": "film", "valor": "97 GB"}
  ]},
  {"tipo": "simulador", "titulo": "E se apagar parte dos vídeos?",
   "controle": {"rotulo": "Apagar", "min": 0, "max": 97, "passo": 1, "inicial": 40, "unidade": " GB"},
   "resultados": [{"rotulo": "Uso do C: depois", "formula": "(412 - x) / 476 * 100", "formato": "porcento", "casas": 0}],
   "enviar": "Liste os vídeos que somam {x} GB para eu escolher o que apagar"}
]
```

Quando o painel não alcança (um diagrama próprio, uma interação diferente),
escreva o HTML num bloco ` ```vivo ` com o kit abaixo.

## O kit

O visual do Sentury já está dentro do bloco. Use as classes em vez de inventar
cor ou fonte:

- `cartao`: caixa clara com borda e cantos arredondados.
- `grade`: cartões lado a lado, que quebram em telas estreitas.
- `linha` (itens na horizontal) e `coluna` (na vertical).
- `rotulo` (título pequeno em caixa alta), `numero` (número grande), `sub` (texto secundário).
- `bom`, `atencao`, `ruim`: cor do sentido (subiu bem, cuidado, piorou).
- `etiqueta` e `etiqueta ouro`: selo pequeno.
- `botao` e `botao principal`.
- `tabela` (em `<table class="tabela">`).
- `barra` com um `<span style="width:62%">` dentro: barra de proporção; a cor vai no `background` do span.
- Cor livre também no HTML: `cor-verde`, `cor-vermelho` (texto) e `fundo-verde`, `fundo-vermelho` (fundo), e o mesmo para amarelo, laranja, azul, roxo, rosa, ciano e cinza; ou um hex no `style`.
- `selo`: quadradinho para um ícone, com a cor no `style`.
- Variáveis de cor: `--tinta`, `--tinta-2`, `--tinta-3`, `--tela`, `--painel`, `--borda`, `--ouro`, `--ouro-forte`, `--ouro-suave`, `--ouro-tinta`, `--bom`, `--atencao`, `--ruim`.

Ícones de linha, os mesmos da interface (não use emoji):
`<svg class="ic"><use href="#ic-NOME"/></svg>`, com NOME um destes:

check, x, triangle-alert, info, circle-check, circle-x, circle-alert,
arrow-up, arrow-down, arrow-right, arrow-left, trending-up, trending-down,
minus, plus, search, clock, calendar, user, users, file-text, folder,
database, chart-column, chart-line, chart-pie, dollar-sign, percent, globe,
mail, phone, map-pin, star, zap, shield-check, lock, settings, refresh-cw,
download, external-link, lightbulb, target, flag, package, truck,
shopping-cart, building, heart, list-checks, layers, sparkles, gauge, timer,
hourglass, thumbs-up, thumbs-down, message-square, bell, eye, funnel, circle-dot,
hard-drive, cpu, memory-stick, monitor, app-window, film, music, image,
gamepad-2, code, trash, archive, cloud, wifi, battery-medium, smartphone,
terminal, message-circle, video, pen-tool, book-open, sheet, presentation, box

O ícone herda a cor do texto: `<span class="bom"><svg class="ic"><use href="#ic-trending-up"/></svg> 12%</span>`.

## Mandar uma mensagem de volta

`sentury.enviar("texto")` propõe uma mensagem ao Sentury, por exemplo num botão
"Simular com 15%". A pessoa vê o texto e confirma antes de ele ir; vai como
mensagem dela. Use para o próximo passo que precisa do modelo, não para cada
clique: o que o script resolve sozinho fica no bloco.

## Números

Número no bloco precisa ter vindo de um resultado desta conversa ou de uma
conta sobre ele, como no texto. Bloco bonito com número inventado parece mais
confiável que um erro, e é pior.

## Exemplo

```vivo
<div class="grade">
  <div class="cartao">
    <div class="rotulo">Vendas de setembro</div>
    <div class="numero">R$ 120,4 mil</div>
    <div class="sub bom"><svg class="ic"><use href="#ic-trending-up"/></svg> 8% sobre agosto</div>
  </div>
  <div class="cartao">
    <div class="rotulo">Simular reajuste</div>
    <input type="range" id="r" min="0" max="20" value="5">
    <div class="linha"><span class="numero" id="v"></span><span class="sub">com reajuste de <b id="p"></b>%</span></div>
    <button class="botao" onclick="sentury.enviar('Detalhe o efeito de um reajuste de ' + r.value + '% nas vendas')">
      <svg class="ic"><use href="#ic-message-square"/></svg> Pedir análise
    </button>
  </div>
</div>
<script>
  const r = document.getElementById('r');
  const mostrar = () => {
    p.textContent = r.value;
    v.textContent = 'R$ ' + (120.4 * (1 + r.value / 100)).toFixed(1).replace('.', ',') + ' mil';
  };
  r.oninput = mostrar; mostrar();
</script>
```
