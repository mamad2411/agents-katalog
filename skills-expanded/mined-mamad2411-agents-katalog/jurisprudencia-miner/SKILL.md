---
name: jurisprudencia-miner
description: "Use quando a tarefa principal for pesquisar, localizar, levantar, validar, comparar ou resumir jurisprudencia brasileira, inclusive precedente, entendimento do STJ/STF, sumula, tema repetitivo, repercussao geral, IRDR, IAC ou acordao. Priorize esta skill para pesquisa jurisprudencial estruturada, classificacao de confianca e construcao de base segura de precedentes. Nao usar como skill principal para apenas testar a solidez estrategica de uma tese; para isso, usar tese-juridica-validator."
---

# Jurisprudencia Miner

Skill de metodo, nao banco de jurisprudencia. O objetivo e encontrar, validar e citar precedentes brasileiros sem inventar numero, relator, data, turma ou tese.

## Objetivo

Entregar pesquisa jurisprudencial suficiente para uso profissional, com fonte oficial quando houver citacao, e com limites claros quando ainda faltar verificacao.

## Criterios de sucesso

- Tema, ramo, fase e tribunal relevante identificados.
- Precedentes qualificados buscados primeiro: vinculante, repetitivo, repercussao geral, IAC, IRDR e sumula.
- Cada achado classificado por confianca e utilidade.
- Divergencia, distinguishing, superacao, revisao, suspensao ou afetacao pendente apontados quando relevantes.
- Resultado indica como usar a jurisprudencia sem superafirmar.

## Regra central

Nao tratar memoria do modelo, tabela interna, resumo antigo ou referencia secundaria como fonte final. Para qualquer citacao profissional, confirmar em fonte oficial ou declarar expressamente que falta verificacao.

Classificar cada referencia:

- `confirmado em fonte oficial`: numero, orgao, relator/data e tese conferidos.
- `tendencia a verificar`: ha indicio forte, mas ainda falta fonte primaria.
- `necessita pesquisa`: nao ha base segura para citar.
- `descartar`: numero/tese incompatível, fonte fraca ou referencia contraditoria.

## Fontes oficiais

Usar primeiro:

- STF Jurisprudencia: https://portal.stf.jus.br/jurisprudencia/
- STF Sumulas Vinculantes: https://portal.stf.jus.br/textos/verTexto.asp?servico=jurisprudenciaSumulaVinculante
- STJ Pesquisa: https://scon.stj.jus.br/SCON/
- STJ Repetitivos: https://processo.stj.jus.br/repetitivos/
- STJ Sumulas: https://www.stj.jus.br/sites/portalp/Jurisprudencia/Sumulas
- Tribunais locais apenas quando a tese depender de orientacao regional ou parametro indenizatorio local.

Quando a materia puder ter mudado recentemente, pesquisar em fonte oficial ou internet antes de responder.

## Orcamento de pesquisa

Buscar o suficiente para responder com seguranca, nao para esgotar a internet. Parar quando houver:

- precedente qualificado oficial diretamente aplicavel;
- tendencia clara com fonte primaria suficiente;
- divergencia mapeada o bastante para orientar risco;
- ausencia de base segura, caso em que a resposta deve dizer `necessita pesquisa`.

Continuar pesquisando apenas se faltar fonte primaria para citacao, houver conflito entre fontes, a tese depender de tribunal local/periodo recente, ou o usuario pedir pesquisa exaustiva.

## Fluxo essencial

1. Identificar tema, ramo, fase processual e tribunal relevante.
2. Mapear palavras-chave, artigos de lei, nomes de tese e sinonimos.
3. Procurar precedentes qualificados primeiro: vinculante, repetitivo, repercussao geral, IAC, IRDR, sumula.
4. Validar cada achado na fonte primaria.
5. Separar precedente vinculante, persuasivo e tendencia local.
6. Apontar distinguishing, superacao, revisao, suspensao ou afetação pendente.
7. Entregar resultado com nivel de confianca e caminho de verificacao.

## Regras de parada

Nao citar numero, relator, data, turma ou tese sem fonte primaria conferida. Se a fonte oficial estiver indisponivel, entregar como `achado a verificar` e indicar o caminho de conferencia.

## Saida padrao

```text
PESQUISA JURISPRUDENCIAL - [tema]

STATUS
- [pacificado/divergente/em afetacao/sem pesquisa suficiente]

ACHADOS CONFIRMADOS
- [tribunal, classe/numero, orgao, relator, data, tese, link oficial]

ACHADOS A VERIFICAR
- [referencia ou tendencia] - motivo da pendencia

DIVERGENCIAS E RISCOS
- [corrente contraria, distinguishing, superacao ou lacuna]

TERMOS DE BUSCA
- [consultas recomendadas em STJ/STF/TJ]

USO NA PECA
- [como aplicar sem superafirmar]
```

## Referencias sob demanda

- Ler `references/sumulas-temas.md` somente quando precisar de alertas sobre sumulas, repetitivos ou temas citados com frequencia.
- Ler `references/parametros-indenizatorios.md` somente quando a pesquisa envolver valor de dano moral/material ou calibragem de quantum.
- Ler `references/modelos-saida.md` quando o usuario pedir comparacao de correntes, evolucao jurisprudencial ou ementa estruturada.

## Integracao

- Se a tarefa for validar força de argumento, usar `tese-juridica-validator`.
- Se a tarefa for redigir peca com precedentes ja pesquisados, usar `peticao-completa`.
- Se a tarefa for apenas resumir peca/autos, usar `peticao-analyzer`.
