---
name: dl-capitalize
description: Capitalise un workflow repetitif en fichier .workflow.md chainskills. Detecte les patterns, cristallise les etapes, rend executable par Haiku.
---

# Capitalisation Workflow → .workflow.md

Tu vas cristalliser un workflow repetitif en fichier `.workflow.md` pour le framework chainskills.

## Etapes

1. **Analyser la session** : Identifier les actions repetees (outils utilises, fichiers modifies, patterns)
2. **Extraire les invariants** : Ce qui est identique a chaque execution (structure, validations, patterns)
3. **Extraire les variables** : Ce qui change (noms, chemins, configs) → deviennent des `inputs:`
4. **Cristalliser** : Ecrire le .workflow.md avec le format ci-dessous

## Format .workflow.md obligatoire

```markdown
---
name: <kebab-case>
description: <ce que fait le workflow>
version: 0.1.0
inputs:
  - name: <param>
    type: string|number|boolean|list
    required: true|false
    description: <description>
outputs:
  - name: <result>
    type: string|object
    description: <description>
tags: [datalake, <category>]
metadata:
  author: TheWatcher01
  project: datalake-souverain
---

# Step N — Titre

Description en langage naturel.

@call shell.exec("commande $variable") -> $resultat
@agent copilot: "Prompt avec $context" -> $output
@assert $condition "message erreur"
@parallel:
## Branche A
@call ...
## Branche B
@call ...
```

## Directives disponibles

| Directive | Usage |
|-----------|-------|
| `@call shell.exec("cmd") -> $var` | Commande shell |
| `@agent copilot: "prompt" -> $var` | Deleguer au LLM |
| `@if $var == "val":` | Condition |
| `@for $item in $list:` | Boucle |
| `@parallel:` | Execution parallele (DAG) |
| `@try: ... @on-error: log and continue` | Gestion erreurs |
| `@assert $var != "" "msg"` | Validation |
| `@output $var -> $result` | Declarer un output |
| `@workflow sub-workflow:` | Composer des sous-workflows |

## Regles de capitalisation

1. **Copier+adapter > generer** : Toujours referencer les templates existants dans le workflow
2. **Deterministe > creatif** : Les steps shell sont deterministes, `@agent` seulement pour les taches creatives
3. **Paralleliser** : Utiliser `@parallel:` pour les steps independants (ex: lire template + lire config)
4. **Provenance** : Inclure `lineage_run_id` dans tout workflow data
5. **Testable** : Chaque workflow doit pouvoir etre `--dry-run`

## Ou sauvegarder

Ecrire dans : `~/projects/chainskills/cli-mcp-core/templates/datalake/<name>.workflow.md`

## Workflows existants (ne pas dupliquer)

- `add-crawler` — Nouveau crawler (AsyncGenerator + TokenBucket + CircuitBreaker)
- `add-api-route` — Nouvelle route Hono
- `add-data-import` — Import dataset (CSV/JSON/API)
- `fix-type-errors` — Correction erreurs TypeScript
- `cross-ref-source` — Cross-reference entre sources
- `verify-data` — Verification ISO 8000-8 (dans templates/data/)
