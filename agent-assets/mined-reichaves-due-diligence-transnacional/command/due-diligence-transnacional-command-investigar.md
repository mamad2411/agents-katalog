---
description: >
  Roda o pipeline completo de due diligence transnacional para qualquer pessoa
  física com vínculos nos EUA. Busca em FEC, LDA, FARA, registros corporativos
  estaduais (FL, DE, TX), OpenCorporates e imprensa BR/EUA. Produz dossiê PDF
  com fontes e níveis de confiança. Suporta qualquer país de origem via
  origin_country no target.yaml.
argument-hint: "Nome Completo do Alvo"
---

Você vai conduzir uma investigação de due diligence transnacional para a pessoa
cujo nome está em $ARGUMENTS.

Aja como o orquestrador definido em `skills/due-diligence-transnacional/SKILL.md`.

## Regras obrigatórias

1. **Siga os 5 estágios** definidos no SKILL.md — não pule nenhum.
2. **Pare nas revisões humanas** obrigatórias entre os estágios 2→3 e 4→5.
   Mostre o que vai ser feito e aguarde confirmação explícita antes de avançar.
3. **Cite fonte em toda afirmação.** Use o formato:
   `(Fonte: <base>, ID <id>, consultado em DD/MM/AAAA)`
4. **Use níveis de confiança** da escala em
   `skills/due-diligence-transnacional/references/confidence-levels.md`.
5. **"Não encontrado" é um achado válido.** Liste as variações testadas.

## Fluxo esperado

```
Estágio 1: Coletar contexto do alvo → salvar em cases/<slug>/target.yaml
Estágio 2: Gerar variações → PARAR → aguardar aprovação
Estágio 3: Buscas em paralelo (FEC, LDA, FARA, state-corps, OC, imprensa)
Estágio 4: Triangular achados → PARAR → apresentar consolidado
Estágio 5: Gerar dossiê PDF
```

## Contexto ético

Antes de iniciar, confirmar:
- O alvo tem relevância pública (gestor de empresa, político, doador, etc.)?
- Há razão jornalística documentada?
- O alvo possui algum vínculo com os EUA (empresa registrada, atividade de lobby, doação eleitoral, etc.)?

Se não: informar ao usuário que o pipeline é restrito a investigações de interesse público com vínculo americano.

## Idioma e país de origem

O pipeline opera em português (padrão) ou inglês. Para targets não-brasileiros
ou dossier em inglês, o `target.yaml` deve conter:

```yaml
origin_country: "PE"          # ISO 3166-1 alpha-2 do país do alvo
investigation_language: "en-US"  # dossier e comunicações em inglês
```

Vide `README.md` seção "Using in English" para exemplo completo.
