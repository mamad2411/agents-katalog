---
description: >
  Gera o dossiê PDF final a partir de um arquivo findings-consolidated.json.
  Usa a sub-skill generate-dossier-pdf com template ReportLab. Requer
  revisão humana dos achados antes de executar.
argument-hint: "caminho/para/findings-consolidated.json"
---

Você vai gerar o dossiê PDF final a partir do arquivo de achados consolidados
em $ARGUMENTS.

Aja como a sub-skill definida em `skills/generate-dossier-pdf/SKILL.md`.

## Antes de gerar

1. Leia o arquivo de achados fornecido.
2. Apresente um **resumo dos achados** ao usuário:
   - Quantos hits por base
   - Achados de maior confiança (`confirmado`, `provavel`)
   - Offshore flags (se houver)
   - Lacunas identificadas
3. **Pergunte ao usuário** se deseja confirmar, remover algum achado,
   ou adicionar contexto antes de gerar o PDF.
4. Só gere o PDF após confirmação explícita.

## Estrutura do dossiê

O PDF deve seguir a estrutura definida em `skills/generate-dossier-pdf/SKILL.md`:

1. Capa com metadados (alvo, data, investigador)
2. Resumo executivo
3. Metodologia e bases consultadas
4. Variações de nome testadas
5. Achados por base (com fonte e nível de confiança)
6. Triangulações
7. Lacunas e próximas frentes
8. Contexto legal aplicável
9. Apêndice: timestamps de todas as consultas

## Saída

PDF salvo em `cases/<slug-do-alvo>/dossier-<data>.pdf`

Confirmar localização do arquivo ao final.
