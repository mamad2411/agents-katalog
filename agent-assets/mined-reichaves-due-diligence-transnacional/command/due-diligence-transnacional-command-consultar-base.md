---
description: >
  Consulta uma base de dados específica para um nome. Bases disponíveis:
  fec, lda, fara, fl (Florida Sunbiz), de (Delaware), tx (Texas), oc (OpenCorporates),
  news-br (imprensa brasileira), news-us (imprensa americana).
argument-hint: "<base> \"Nome Completo\""
---

Você vai consultar a base de dados especificada no primeiro argumento, buscando
o nome que vem entre aspas em $ARGUMENTS.

## Formato esperado dos argumentos

```
fec "Carlos Ferreira"
lda "Carlos Eduardo Ferreira"
oc "Ferreira Global Ltda"
news-br "Carlos Ferreira Ferreira Global"
```

## Mapeamento de bases para sub-skills

| Base solicitada | Sub-skill / Script                                         |
|-----------------|------------------------------------------------------------|
| `fec`           | `skills/search-fec/SKILL.md` + MCP fec-finance             |
| `lda`           | `skills/search-lobby-fara/scripts/lda_search.py`           |
| `fara`          | `skills/search-lobby-fara/scripts/fara_search.py`          |
| `fl`            | `skills/search-state-corps/scripts/florida_sunbiz.py`      |
| `de`            | `skills/search-state-corps/scripts/delaware_corp.py`       |
| `tx`            | `skills/search-state-corps/scripts/texas_comptroller.py`   |
| `oc`            | `skills/search-opencorporates/scripts/opencorporates_search.py` |
| `news-br`       | `skills/search-news-archive/SKILL.md` (outlets BR)         |
| `news-us`       | `skills/search-news-archive/SKILL.md` (outlets US)         |

## Regras

1. Antes de buscar, gere as variações do nome com `expand-brazilian-identity`.
2. Cite a fonte de cada resultado no formato padrão do projeto.
3. Se a base não retornar resultados, liste as variações testadas e explique
   o contexto legal se aplicável.
4. Output em JSON seguindo `schemas/findings.schema.json`.
