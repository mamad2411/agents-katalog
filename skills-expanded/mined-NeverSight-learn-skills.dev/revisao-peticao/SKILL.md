---
name: revisao-peticao
description: "Use somente quando invocada explicitamente para revisao final de peticao antes do protocolo, com veredicto, itens criticos, itens importantes, pendencias, prova/documentacao e riscos de ajuste."
---

# Revisao de Peticao

Usar esta skill apenas por selecao explicita do usuario.

Revisar a peca como controle de qualidade pre-protocolo. Priorizar risco real, bloqueadores e coerencia processual. Nao agir como reescrita automatica.

## Coordenacao com o stack atual

- Usar esta skill quando a peca ja existir em texto, `.docx` ou PDF convertido em texto.
- Se a peca estiver em `.docx`, combinar com `doc` quando a leitura ou a edicao estrutural depender do arquivo.
- Se a peca ainda nao existir ou estiver so em briefing, usar `peticao-final`, nao esta skill.
- Nao depender de perfil externo, runtime legado ou tools fora do ambiente atual.

## Objetivo

Responder, antes do protocolo:

1. A peca pode ser protocolada ou nao.
2. Quais sao os bloqueadores.
3. Quais ajustes importantes reduzem risco.
4. O que ainda falta preencher, provar ou definir.

## Criterios de sucesso

- Veredicto unico: `APROVADA`, `APROVADA COM RESSALVAS` ou `REQUER REVISAO`.
- Itens separados por gravidade: critico, importante ou aprimoramento.
- Coerencia entre fatos, fundamentos, provas e pedidos testada.
- Pendencias objetivas listadas sem transformar duvida em certeza.
- Nenhum fato, documento, qualificacao ou precedente inventado.

## Modo de operacao

Revisar primeiro. So aplicar correcoes se o usuario pedir expressamente.

Nao fazer:

- reescrever a peca inteira por conta propria
- inventar jurisprudencia, fatos, documentos ou qualificacoes
- tratar pendencia relevante como detalhe menor

## Fluxo essencial

1. Checar admissibilidade processual aparente:
   - competencia;
   - legitimidade;
   - interesse de agir ou adequacao da via;
   - prazo/tempestividade, quando houver dado no material;
   - requisitos especificos da especie;
   - fundamento minimo para pedidos urgentes.
2. Testar coerencia logica:
   - fatos sustentam pedidos?
   - fundamentos conversam com narrativa?
   - ha contradicao interna?
   - ha pedido sem causa de pedir?
   - ha topico de merito sem providencia concreta?
3. Revisar qualidade argumentativa:
   - ordem dos argumentos;
   - clareza da tese central;
   - excesso de subsidiarias;
   - pedidos com verbo inadequado;
   - linguagem vaga, panfletaria ou sem densidade;
   - placeholders como `[COMPLETAR]`.
4. Auditar lastro probatorio e documental:
   - fato relevante sem documento;
   - prova fraca tratada como plena;
   - documento impugnavel sem cautela;
   - pedido dependente de prova ausente;
   - narrativa mais forte que os documentos.
5. Mapear pendencias antes do protocolo.
6. Emitir veredicto e plano de correcao.

## Regras de parada

Marcar como pendencia, nao como certeza, quando faltar dado para verificar requisito relevante. Se a peca depender de jurisprudencia nao confirmada, nao pesquisar de forma ampla por padrao; indicar exatamente onde a pesquisa faz falta, salvo se o usuario pedir a verificacao.

## Classificacao dos achados

Usar esta regua:

- `Item critico`: impede protocolo seguro ou atinge o nucleo da tese.
- `Item importante`: nao bloqueia por si so, mas aumenta risco processual ou argumentativo.
- `Sugestao de aprimoramento`: melhora a peca, sem condicionar protocolo.

## Pendencias comuns

- campos incompletos;
- qualificacoes ausentes;
- valor da causa indefinido;
- documentos nao listados ou nao correlacionados;
- pedidos sem suporte fatico suficiente;
- referencias normativas ou jurisprudenciais pendentes;
- fecho, data, local, OAB ou requerimentos finais ausentes.

## Veredicto

Escolher apenas uma opcao:

- `APROVADA`: em condicoes de protocolo
- `APROVADA COM RESSALVAS`: protocolar so apos corrigir itens criticos ou pendencias objetivas apontadas
- `REQUER REVISAO`: nao protocolar ate resolver os bloqueadores

## Formato de saida

Entregar neste formato:

```text
PARECER DE REVISAO SENIOR

VEREDICTO
- [APROVADA / APROVADA COM RESSALVAS / REQUER REVISAO]

ITENS CRITICOS
- [se houver]

ITENS IMPORTANTES
- [se houver]

SUGESTOES DE APRIMORAMENTO
- [se houver]

PENDENCIAS ANTES DO PROTOCOLO
- [COMPLETAR]: [...]
- [JURISPRUDENCIA]: [...]
- valor da causa: [definido/indefinido]

AVALIACAO GERAL
- [2 a 4 linhas sobre forca, fragilidade e foco de correcao]
```

## Fechamento

Ao final:

- perguntar se o usuario quer que as correcoes criticas e importantes sejam aplicadas
- se o usuario pedir aplicacao, corrigir apenas os pontos necessarios
- se a peca estiver aprovada, dizer de forma objetiva que esta em condicoes de protocolo
