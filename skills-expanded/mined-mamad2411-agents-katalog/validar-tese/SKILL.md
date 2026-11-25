---
name: validar-tese
description: "Use para testar tese juridica, argumento ou estrategia processual: chance de exito, fragilidades, ataques da parte contraria, coerencia normativa e resistencia jurisprudencial. Nao usar para mera busca de precedentes; nesse caso use pesquisa-jurisprudencial."
---

# Validar Tese

Testa uma tese juridica antes de usa-la em peca, recurso, negociacao ou decisao. A saida deve mostrar força, fragilidade e como a parte contraria atacaria.

## Objetivo

Classificar a solidez argumentativa de uma tese juridica sem fingir precisao numerica. A resposta deve separar norma, fatos, prova, jurisprudencia, inferencia, lacuna e risco adversarial.

## Criterios de sucesso

- Tese formulada em uma frase verificavel.
- Contexto minimo identificado: parte, fase, tribunal, pedido e prova disponivel.
- Cinco dimensoes avaliadas com base e risco.
- Jurisprudencia marcada como confirmada, a verificar ou contraria.
- Reformulacao sugerida quando a tese estiver ampla, vulneravel ou mal conectada ao pedido.

## Regra central

Nao atribuir probabilidade numerica rigida sem dados empiricos do caso, vara, tribunal e periodo. Usar niveis argumentativos auditaveis.

Niveis:

- `forte`: base normativa clara, prova coerente e precedentes confirmados.
- `defensavel`: tese plausivel, mas depende de fato, prova ou tribunal.
- `fragil`: lacuna normativa, prova insuficiente ou jurisprudencia contraria.
- `temeraria`: contraria a precedente qualificado, norma clara ou fatos dos autos.
- `necessita pesquisa`: falta base segura para classificar.

## Cinco dimensoes

1. `validade normativa`: norma vigente, hierarquia, especialidade, revogacao.
2. `lastro fatico-probatorio`: fatos provados sustentam a conclusao?
3. `consistencia jurisprudencial`: precedentes confirmados favorecem, dividem ou contrariam?
4. `coerencia interna`: premissas levam ao pedido sem contradicao?
5. `vulnerabilidade adversarial`: quais ataques previsiveis e como prevenir?

## Fluxo essencial

1. Formular a tese em uma frase.
2. Identificar contexto: autor/reu, fase, tribunal, pedido e prova disponivel.
3. Testar cada dimensao.
4. Se houver citacao jurisprudencial nao confirmada e ela for decisiva, chamar `pesquisa-jurisprudencial`.
5. Separar certeza, inferencia e ponto pendente.
6. Sugerir reformulacao se a tese estiver ampla demais.

## Orcamento de pesquisa

Usar conhecimento juridico para triagem inicial, mas nao tratar memoria do modelo como fonte final. Pesquisar jurisprudencia somente quando a classificacao depender de precedente atual/qualificado, quando houver citacao a ser usada em peca, ou quando o usuario pedir validacao jurisprudencial.

## Regras de parada

Classificar como `necessita pesquisa` quando faltarem fatos, provas, norma vigente ou fonte jurisprudencial segura. Nao compensar lacuna probatoria com retorica.

## Saida padrao

```text
VALIDACAO DE TESE

TESE
- [formulacao objetiva]

CLASSIFICACAO
- [forte/defensavel/fragil/temeraria/necessita pesquisa]

D1 - NORMA
- base:
- risco:

D2 - FATOS E PROVAS
- suporte:
- lacunas:

D3 - JURISPRUDENCIA
- confirmado:
- a verificar:
- contrario:

D4 - COERENCIA
- ponto forte:
- contradicao ou salto logico:

D5 - ATAQUE ADVERSARIAL
- ataque previsivel:
- resposta:

REFORMULACAO RECOMENDADA
- [se necessario]
```

## Referencias sob demanda

- Ler `references/teses-por-area.md` somente para lembrar familias de teses e perguntas de pesquisa. Nao usar como fonte final.
