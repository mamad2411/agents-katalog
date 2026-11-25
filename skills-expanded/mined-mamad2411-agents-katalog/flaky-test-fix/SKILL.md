---
name: flaky-test-fix
description: "Fix flaky RSpec tests identified by CI failure analysis. Backlog seeded by FlakyCiScanner (merge queue + retry signals)."
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit(app/*)
  - Edit(spec/*)
  - Edit(config/*)
  - Write(spec/*)
  - Write(pr-description.md)
  - Bash(git status)
  - Bash(git add:*)
  - Bash(git commit:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git blame:*)
  - Bash(grep:*)
  - Bash(find:*)
  - Bash(bundle exec rspec:*)
  - Bash(bundle exec rubocop:*)
  - Bash(bash ~/dev/night-shift/.claude/skills/flaky-test-fix/verify-flaky.sh:*)
  - Bash(ls:*)
  - Bash(wc:*)
  - Agent
  - Skill(pr-description)
---

# Fix Flaky Test

**Architecture :** cet agent est un **coordinateur leger**. Il lit le contexte flaky, localise les
examples concernes, puis delegue l'investigation et le fix a un **sous-agent isole** qui recoit
uniquement ce dont il a besoin. Cela evite de saturer le contexte sur les gros specs (500+ lignes).

## Input

The backlog item is a spec file path (e.g., `spec/system/admin_spec.rb`).
The context JSON contains flaky evidence:

- `test_names` — names of the flaky `it`/`scenario` blocks (stable across commits, use these to locate the tests)
- `lines` — line numbers where failures were observed (may drift between commits, prefer `test_names`)
- `merge_queue_count` — failures in merge queue branches (strongest flaky signal: no code change involved)
- `retry_count` — failures that passed on retry
- `branches` — which branches saw the failure
- `jobs` — which CI jobs failed
- `job_urls` — direct links to the failed CI jobs (include in PR description)

## Etape 1 : Triage (coordinateur — contexte leger)

**NE PAS lire le fichier spec entier.** Le sous-agent le fera.

1. Lire le contexte JSON pour extraire `test_names`, `lines`, `merge_queue_count`, `retry_count`
2. Estimer la taille du spec :
   ```bash
   wc -l < $SPEC_FILE
   ```
3. Localiser les examples flaky (grep, pas Read) :
   ```bash
   grep -n "it \|scenario \|context \|describe " $SPEC_FILE | head -30
   ```
4. Identifier la categorie probable :
   - `spec/system/` → timing/race condition (Capybara, Turbo, Stimulus)
   - `spec/models/` + jobs → async/ordering
   - `spec/graphql/` → ID collision, sequence reset
   - Autre → DB state leak, shared state

## Etape 2 : Deleguer au sous-agent

Lancer un **sous-agent** via `Agent`. Le sous-agent recoit un prompt auto-suffisant :

```
Tu es un agent de fix de test flaky. Tu corriges UN spec.

## Fichier
`<spec_file>`

## Examples flaky
<test_names ou lines>

## Evidence CI
- merge_queue_count: <N> (pas de changement de code → preuve forte)
- retry_count: <N>
- jobs: <jobs>

## Categorie suspectee
<timing | db_state | race_condition | id_collision | shared_state>

## Process

1. Lire le spec complet
2. Lire les fichiers d'implementation references (concerns, controllers JS, models)
   — LIMITER aux fichiers directement lies au test flaky, ne pas explorer le framework
3. Identifier la root cause
4. Classifier : test-side ou app-side
5. Si possible, reproduire le flaky dans un commit RED (setval sequence, travel_to, seed replay)
6. Appliquer le fix minimal
7. Lancer le spec en isolation pour verifier qu'il passe :
   ```bash
   bundle exec rspec <spec_file>:<line> --order random
   ```

## Regles

- Ne JAMAIS modifier du code metier (app/) pour un probleme de donnees de test
- Modifier app/ UNIQUEMENT pour une vraie race condition app (controller JS, flux async)
- Ne PAS skip ou quarantine le test
- Ne PAS ajouter de retry
- Changements minimaux
- Commiter avec `--no-gpg-sign`

## Patterns connus

- **ID collision GraphQL** : `GraphQL::Schema::UniqueWithinType.encode('Type', 123)` → utiliser `Float::INFINITY` comme sentinel (ne peut jamais etre un ID DB)
- **PG sequence collision** : IDs auto-generes qui collisionnent avec des IDs en dur → utiliser `Float::INFINITY` ou des IDs negatifs
- **Turbo Stream race** : `have_content('Saved')` prouve le serveur, PAS le morph DOM — attendre un element specifique au nouvel etat
- **fixture_file_upload** : IO stream consomme au premier use — incompatible avec `let_it_be`

## Output

Repondre avec un JSON :
```json
{
  "fixed": true,
  "root_cause": "ID collision: encode('Champ', 123) collides with real TypeDeChamp",
  "scope": "test",
  "files_changed": ["spec/graphql/annotation_spec.rb"],
  "commits": ["test(annotation): fix flaky via Float::INFINITY sentinel"]
}
```
Si non fixable, `"fixed": false` avec `"reason"`.
```

## Etape 3 : Verifier (coordinateur)

Apres le retour du sous-agent :

1. Si `fixed: false` → ecrire `pr-description.md` skip et terminer
2. Si `fixed: true` → verifier le diff :
   ```bash
   git diff --stat
   ```
3. Lancer le stress test :
   ```bash
   bash ~/dev/night-shift/.claude/skills/flaky-test-fix/verify-flaky.sh <spec_file>:<line>
   ```
   Le script adapte les iterations (20 system, 50 unit). Il doit sortir STABLE (exit 0).

4. Si FLAKY (exit 1) → relancer le sous-agent avec le seed qui echoue :
   ```
   Le fix precedent est insuffisant. Le verify-flaky.sh echoue au seed <seed>.
   Replay: bundle exec rspec <file> --seed <seed>
   Analyse ce qui se passe et corrige.
   ```
   Maximum 1 retry. Si toujours FLAKY → skip.

## Etape 4 : Livrer

Ecrire `pr-description.md` :

```markdown
---
title: "Tech: stabiliser les tests flaky de <spec_file>"
---

# Probleme

Le fichier `<spec_file>` echoue de maniere intermittente en CI.

### Evidence CI

| Signal | Count | Signification |
|--------|-------|---------------|
| Merge queue | <merge_queue_count> echecs | Pas de changement de code → preuve forte de flakiness |
| Retries | <retry_count> passes au retry | Le test est instable |

Branches concernees : `<branch1>`, `<branch2>`
Jobs : [`<job1>`](<job_url_1>), [`<job2>`](<job_url_2>)

Tests concernes :
- `<test_name_1>`
- `<test_name_2>`

# Solution

Skill [`/flaky-test-fix`](https://github.com/mfo/night-shift/blob/main/.claude/skills/flaky-test-fix/SKILL.md)

### Causes identifiees et fixes

| Cause | Scope | Fix | Pourquoi ca resout |
|-------|-------|-----|--------------------|
| <root cause 1> | test / app | <fix applied> | <explication en 1 ligne> |

### Preuve de stabilite

| Test | Runs | Resultat | Type |
|------|------|----------|------|
| `<test_name_1>` | 20/20 | STABLE | system |
| `<test_name_2>` | 50/50 | STABLE | unit |

Script : [`verify-flaky.sh`](https://github.com/mfo/night-shift/blob/main/.claude/skills/flaky-test-fix/verify-flaky.sh) (20 runs system, 50 runs unit, random seed a chaque run)

Generated with [Claude Code](https://claude.com/claude-code)
```

## Contraintes

- **Ne JAMAIS modifier du code metier (app/) pour un probleme de donnees de test.** Si la flakiness vient d'une collision d'IDs, d'un ordering de factory, ou d'un etat de test mal isole, le fix appartient a 100% au test. Le test litmus : "est-ce que ce changement app aurait du sens si aucun test n'etait flaky ?" — si non, c'est un fix test.
- Modifier du code app UNIQUEMENT pour une vraie race condition app (controller JS, flux async, morph timing) — ajouter des waits dans le test ne fait que masquer le vrai bug
- Ne PAS skip ou quarantine le test — le fixer
- Ne PAS ajouter de mecanisme `retry` — fixer la root cause
- Changements minimaux — ne toucher que le spec flaky et le code directement responsable de la race condition
