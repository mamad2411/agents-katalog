---
name: painel-sob-medida
vitrine:
  grupo: 'Entrega'
  rotulo: 'painel escrito na hora, e não um molde'
# Curta E SEM CONECTIVO. O `_tokens` da descoberta nao filtra palavra de
# ligacao, entao cada `de`/`um`/`em` na descricao vale 0,4 contra qualquer
# consulta em portugues. Esta descricao ja roubou a skill de causa-raiz e a
# de plano de acao antes de encurtar.
description: "HTML escrito sob medida, sem molde pronto. Formas: lado a lado, numero grande, secoes."
version: 1.0.0
author: Sentury
license: MIT
metadata:
  gatilhos:
    - 'painel (sob medida|do meu jeito|diferente)'
    - 'monta(r)? (um|uma)? (painel|dashboard|relat[óo]rio visual)'
    - 'do jeito que eu (quero|pedi)'
    - '(lado a lado|comparando).{0,30}(painel|visual|tela)'
  category: cognitive
---

# Montar um painel escrevendo o HTML

Molde acerta o caso médio e erra todo o resto — comparar dois períodos lado a
lado, abrir com um número grande, agrupar por assunto em vez de por
ferramenta, esconder o que não interessa. Pedir isso a um molde é pedir para
ele virar outro molde.

Escrever o HTML custa uma chamada de `executar_python` e devolve exatamente o
que foi pedido, sem nenhuma peça nova no motor.

## Como

Dentro do `executar_python` você tem:

- **as tabelas do setor ativo**, já como DataFrame, pelo nome;
- **`resultado_NNN`** — os resultados já computados nesta conversa;
- **`save_html('nome.html', conteudo)`** — grava e entrega o arquivo.

A regra que não muda: **os números vêm dos dados**. Nada de valor escrito à
mão no HTML, nem de exemplo que sobrou de outro painel. Se um número não saiu
de uma tabela ou de um `resultado_NNN`, ele não entra.

## O mínimo que funciona

```python
import pandas as pd

# `vendas` aqui é uma tabela declarada pelo setor ativo. Use as que existem.
por_mes = vendas.groupby("mes")["valor"].sum().reset_index()
linhas = "".join(
    f"<tr><td>{r.mes}</td><td>{r.valor:,.2f}</td></tr>"
    for r in por_mes.itertuples()
)

html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Vendas por mês</title>
<style>
  body {{ font: 16px/1.5 system-ui, sans-serif; margin: 40px; color: #1a1a1a; }}
  table {{ border-collapse: collapse; width: 100%; max-width: 640px; }}
  td, th {{ padding: 10px 14px; border-bottom: 1px solid #e5e5e5; text-align: left; }}
  .numero {{ font-size: 48px; font-weight: 600; letter-spacing: -0.02em; }}
</style></head>
<body>
  <p class="numero">{por_mes["valor"].sum():,.2f}</p>
  <p>total no período, em {len(por_mes)} meses</p>
  <table><tbody>{linhas}</tbody></table>
</body></html>"""

save_html("vendas-por-mes.html", html)
```

## Comparar dois recortes lado a lado

O caso que o molde não faz. Duas colunas, mesma escala, diferença destacada.

```python
a = dados[dados["periodo"] == "2026-01"]
b = dados[dados["periodo"] == "2026-02"]

def bloco(titulo, df):
    return f"""<section>
      <h2>{titulo}</h2>
      <p class="numero">{df["valor"].mean():.1f}</p>
      <p>{len(df)} registros</p>
    </section>"""

delta = b["valor"].mean() - a["valor"].mean()
sinal = "sobe" if delta > 0 else "cai"

html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>
  body {{ font: 16px/1.5 system-ui, sans-serif; margin: 40px; }}
  .lado-a-lado {{ display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }}
  .numero {{ font-size: 44px; font-weight: 600; margin: 8px 0; }}
  .delta {{ margin-top: 24px; padding: 16px; background: #f6f6f6; border-radius: 8px; }}
</style></head><body>
  <div class="lado-a-lado">{bloco("Janeiro", a)}{bloco("Fevereiro", b)}</div>
  <p class="delta">Entre um e outro, {sinal} {abs(delta):.1f}.</p>
</body></html>"""

save_html("comparativo.html", html)
```

## Gráfico sem biblioteca de front

SVG inline resolve barra, linha e pizza, e não depende de rede nem de script —
o painel abre igual em qualquer lugar, inclusive offline.

```python
valores = por_mes["valor"].tolist()
rotulos = por_mes["mes"].tolist()
teto = max(valores) or 1
largura, altura = 640, 220

barras = "".join(
    f'<rect x="{i * (largura // len(valores)) + 8}" '
    f'y="{altura - (v / teto) * (altura - 30):.0f}" '
    f'width="{largura // len(valores) - 16}" '
    f'height="{(v / teto) * (altura - 30):.0f}" rx="3" fill="#4F6F52"/>'
    for i, v in enumerate(valores)
)
eixo = "".join(
    f'<text x="{i * (largura // len(valores)) + (largura // len(valores)) // 2}" '
    f'y="{altura - 6}" font-size="11" text-anchor="middle" fill="#666">{r}</text>'
    for i, r in enumerate(rotulos)
)
grafico = f'<svg viewBox="0 0 {largura} {altura}" width="100%">{barras}{eixo}</svg>'
```

## O que não fazer

- **Não use `<script>`.** O painel é um arquivo que a pessoa abre, muitas vezes
  sem internet. Um gráfico que só existe depois de um CDN carregar é um painel
  que às vezes não existe.
- **Não invente número para completar a tela.** Falta dado, o painel diz que
  falta. Tabela com linha inventada é pior que tabela curta.
- **Não colapse o HTML numa linha só** com `\n` literais. Aspas triplas com
  quebras de linha de verdade, e o `save_html(...)` numa linha separada.

## Painel que se atualiza

Um painel escrito por você não precisa ser uma foto. Ele vira **vivo** sem
nenhuma tecnologia nova, porque as peças já existem: o painel é um artefato, e
o workflow sabe disparar.

A pessoa pede "quero isso atualizado toda segunda". Você monta o painel uma
vez, e cria um workflow com gatilho de relógio cujo passo é justamente
**refazer este painel**. A cada disparo o HTML é escrito de novo com os dados
de agora, no mesmo nome de arquivo — e o artefato que ela abre está sempre
fresco.

Duas coisas que fazem isso funcionar em vez de acumular lixo:

- **Mesmo nome de arquivo.** `save_html("painel-semanal.html", ...)` em toda
  execução. Nome com data gera um painel novo por semana e ninguém sabe qual
  olhar.
- **Carimbe a hora dentro do painel.** Uma linha discreta com quando aquilo
  foi medido. Painel sem data é a forma mais fácil de alguém decidir com
  número velho.

```python
from datetime import datetime

rodape = f'<p class="quando">Medido em {datetime.now():%d/%m/%Y às %H:%M}.</p>'
```

Por que não fazer o HTML se atualizar sozinho, com script buscando dado: o
painel deixaria de abrir offline, precisaria de um endereço público e de
autorização, e passaria a ser um pequeno sistema em vez de um arquivo. A
regeneração por gatilho entrega o mesmo resultado e continua sendo um arquivo
que a pessoa guarda, manda por e-mail e abre no avião.

## Quando isto NAO e o caminho

Pedido de um numero, uma tabela, uma resposta em texto. Painel e entrega
visual; quando a pergunta cabe numa frase, a frase e melhor que um arquivo.

Para o arquivo chegar a pessoa, o `save_html` grava e o `entregar_arquivo`
anexa na conversa. Escrever no disco nao entrega nada a quem esta do outro
lado.
