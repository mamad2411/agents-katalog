---
name: n1-query-fix
description: "Fix N+1 queries detected by Prosopite and Skylight. Use in autolearn mode with backlog items grouped by controller file."
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit(app/*)
  - Edit(config/*)
  - Edit(spec/*)
  - Write(app/*)
  - Write(spec/*)
  - Write(pr-description.md)
  - Bash(git status)
  - Bash(git add:*)
  - Bash(git commit:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git blame:*)
  - Bash(bash ~/dev/night-shift/.claude/skills/n1-query-fix/prosopite-setup.sh)
  - Bash(git apply:*)
  - Bash(grep:*)
  - Bash(find:*)
  - Bash(rm -f tmp/prosopite:*)
  - Bash(bundle install)
  - Bash(bundle add:*)
  - Bash(bundle exec rspec:*)
  - Bash(bundle exec rubocop:*)
  - Bash(echo:*)
  - Bash(ls:*)
  - Bash(cat tmp/prosopite:*)
  - Bash(wc:*)
  - Bash(head:*)
  - Bash(tail:*)
  - Agent
  - Skill(pr-description)
---

# Fix N+1 queries (Coordinator)

**Input :** fichier controller — `$ARGUMENTS` (ex: `app/controllers/administrateurs/attestation_templates_controller.rb`)
**Output :** commits granulaires + pr-description.md

**Architecture :** cet agent est un **coordinateur leger**. Il setup Prosopite, scanne les N+1, classifie PROD/TEST, puis delegue chaque fix a un **sous-agent isole** qui recoit uniquement le pattern a corriger. Cela evite de saturer le contexte.

**Regles Bash** :
- Pas de `$()` (command substitution)
- Pas de `;` ou `&&` pour chainer
- 1 commande simple = 1 appel Bash

---

## Etape 0 : Setup Prosopite

Lancer le script de setup (idempotent) :

```bash
bash ~/dev/night-shift/.claude/skills/n1-query-fix/prosopite-setup.sh
```

Le script : ajoute la gem si absente, `bundle install`, configure test.rb en mode log (pas raise), ajoute les hooks scan/finish dans spec_helper.rb.

**Ne PAS commiter ce setup** — il sera revert avec le worktree.

---

## Etape 1 : Lire le contexte (leger)

1. **Lire `.skill-context.json`** s'il existe — noter les patterns N+1, les endpoints et le `waste_ms`
2. **Identifier le spec file** :
   ```bash
   find spec/controllers/ -name "*$(basename $ARGUMENTS .rb)_spec.rb" -type f
   ```
   Si absent, chercher dans `spec/requests/` ou `spec/system/`.

**NE PAS lire le controller entier.** Le sub-agent le fera.

---

## Etape 2 : Scanner les N+1 (Prosopite)

```bash
rm -f tmp/prosopite-scan.log
bundle exec rspec <spec_file>
```

Puis extraire les patterns via grep — **NE PAS lire le log entier** :

```bash
grep -c 'N+1 queries detected' tmp/prosopite-scan.log
grep -A 5 'N+1 queries detected' tmp/prosopite-scan.log
```

**Sauvegarder le log AVANT** pour la PR : noter le nombre de patterns PROD et copier les 5 premieres lignes de chaque pattern. Ces extraits seront injectes dans `pr-description.md` (Etape 4).

**Classifier chaque pattern** par sa call stack :

- **PROD** : au moins une ligne `app/` dans la call stack → vrai N+1 utilisateur
- **TEST** : toutes les lignes dans `spec/` → bruit de test, ignorer

### Escalation raise mode (si 0 N+1 detecte en log mode)

Le mode log a un seuil minimum de queries qui rate certains N+1. Activer temporairement le mode raise :

1. `Edit config/environments/test.rb` → changer `Prosopite.raise = false` en `Prosopite.raise = true`
2. Re-lancer `bundle exec rspec <spec_file>` — les tests qui ont un N+1 echouent avec `Prosopite::NPlusOneQueriesError`
3. Grep le log : `grep -A 5 'N+1 queries detected' tmp/prosopite-scan.log`
4. **Revert** `Prosopite.raise = true` → `false` avant de passer aux fixes (sinon la verification post-fix echouera sur les N+1 TEST)

**Important** : ne pas utiliser `env PROSOPITE_RAISE=1` — les commandes avec variables d'env prefixees sont refusees. Toujours modifier le fichier via Edit.

---

## Etape 2a : Lire la vue (si 0 PROD)

Avant d'enrichir les fixtures, lire le controller et ses vues — le N+1 est souvent visible dans le template.

1. Lire le controller cible : identifier les actions qui chargent des collections
2. Pour chaque action, trouver la vue associee :
   ```bash
   find app/views/ -path "*$(basename $ARGUMENTS .rb | sed 's/_controller//')*" -type f
   ```
3. Grep les acces `.association` dans les vues :
   ```bash
   grep -n '\.\w\+\.\w\+' app/views/<repertoire>/*.html.*
   ```
4. Si un pattern est visible (ex: `item.association.name` dans une boucle) → activer raise mode (voir escalation ci-dessus) pour confirmer, puis passer directement au fix (Etape 3)
5. Si rien de visible → passer a l'enrichissement (Etape 2b)

---

## Etape 2b : Enrichir les fixtures (si 0 PROD)

Si aucun N+1 PROD detecte apres lecture de la vue, deleguer un **sous-agent enrichissement** :

```
Tu es un agent de detection N+1. Tu enrichis les fixtures d'un spec controller pour declencher des N+1.

## Controller cible
`<chemin controller>`

## Contexte Skylight (si disponible)
<endpoints et scores du .skill-context.json>

## Travail
1. Lire le controller — identifier les actions qui chargent des collections
2. Lire le spec existant — identifier les fixtures trop maigres (< 3 records)
3. Ajouter un context 'N+1 detection' avec :
   - `render_views`
   - `create_list(:model, 3, ...)` avec les associations suspectees
4. Lancer le scan :
   ```
   rm -f tmp/prosopite-scan.log
   bundle exec rspec <spec_file>
   ```
5. Extraire les patterns PROD :
   ```
   grep -A 5 'N+1 queries detected' tmp/prosopite-scan.log
   ```

## Repondre avec
- Nombre de patterns PROD trouves
- Pour chaque : table, association, call stack (1ere ligne app/)
- Si 0 apres enrichissement : "skip"
```

Si le sous-agent retourne "skip" → ecrire `pr-description.md` skip et terminer :
```markdown
---
title: "Tech: N+1 scan — no production N+1 found in <Controller>"
---
Aucun N+1 de production detecte apres enrichissement des fixtures (3+ records).
```

---

## Etape 3 : Deleguer fix par fix

Pour chaque pattern PROD, lancer un **sous-agent** via `Agent`. Le sous-agent recoit un prompt auto-suffisant :

```
Tu es un agent de fix N+1 queries. Tu corriges UN pattern.

## Pattern N+1
- Table : [table_name]
- SQL : [pattern SQL depuis Prosopite]
- Association : [association AR suspectee]
- Call stack (app/) : [lignes pertinentes]
- Waste estime : [Xms depuis Skylight, si disponible]

## Fichier controller
`[chemin controller]`

## Strategies de fix (choisir la plus appropriee)
- `includes(:association)` dans le scope ou controller
- `preload(:association)` pour polymorphiques ou sans filtre
- `with_attached_<nom>` pour ActiveStorage
- Scope nomme : `scope :with_x, -> { includes(:x) }`
- Ne PAS utiliser default_scope

## Travail
1. Lire le controller et le(s) model(s) concernes
2. Trouver le call site ou l'association est chargee sans eager loading :
   ```
   grep -rn ".<association>" app/models/ app/controllers/ app/views/
   ```
3. Appliquer le fix (includes/preload au bon endroit)
4. Verifier les tests :
   ```
   bundle exec rspec <spec_file>
   ```
5. Rubocop :
   ```
   bundle exec rubocop <fichiers_modifies>
   ```
6. Relancer le scan Prosopite et capturer le log APRES fix :
   ```
   rm -f tmp/prosopite-scan.log
   bundle exec rspec <spec_file>
   grep -A 5 'N+1 queries detected' tmp/prosopite-scan.log
   ```
7. Si tests verts → commit :
   ```
   git add <fichiers>
   git commit --no-gpg-sign -m "perf(<scope>): fix N+1 on <association>"
   ```

## Regles dures
- Ne modifier que du code app/ et config/ — PAS de modifs spec/ pour faire taire Prosopite
- Ne PAS ajouter includes dans un default_scope
- Preload pour polymorphiques
- Ne PAS abandonner le skill
- Ne PAS push

## Repondre avec
- `applied` ou `skipped` ou `failed`
- Fichiers modifies
- Ce qui a ete change (1-2 phrases)
- **Log Prosopite apres fix** : copier les 5 premieres lignes du grep (ou "Aucun N+1 PROD detecte" si vide)
- **Resume du changement** : 1 ligne decrivant le fix (ex: "Ajoute includes(:instructeur) dans Dossier#preloaded_commentaires")
```

**Apres chaque sous-agent :**
- Si `applied` → noter pour le pr-description.md
- Passer au pattern suivant

---

## Etape 4 : Description PR

Quand tous les patterns sont traites, ecrire `pr-description.md` :

```markdown
---
title: "Tech: fix N+1 sur <association> dans <Controller>"
---

# Probleme

N+1 detecte par [Prosopite](https://github.com/charkost/prosopite) (scan des tests) et confirme par analyse du code.

<!-- Section Skylight CONDITIONNELLE : ne rendre QUE si des donnees existent.
     Si RPM/P95 sont vides, ecrire une ligne simple avec le waste uniquement.
     Si aucune donnee Skylight → supprimer toute la section. -->

**Donnees de production** (Skylight) : waste estime Xms sur `Controller#action`.

**Triage Prosopite** : N patterns PROD / M patterns TEST ignores.

# Solution

Skill [`/n1-query-fix`](https://github.com/mfo/night-shift/blob/main/.claude/skills/n1-query-fix/SKILL.md)

### Patterns corriges

| Association | Table | Strategy | Changement |
|-------------|-------|----------|------------|
| `association` | `table` | `includes` | Ajoute a `Model#scope_method` |

### Preuve Prosopite

**Avant (N patterns PROD) :**
```
<extrait du log Prosopite AVANT fix — 5 lignes max par pattern>
```

**Apres (0 patterns PROD) :**
```
Aucun N+1 PROD detecte.
```

### Patterns ignores (TEST)

| Table | Raison |
|-------|--------|
| ... | call stack dans spec/ uniquement |

### Validation

- [x] Tests passes (rspec)
- [x] Rubocop OK
- [x] Prosopite : 0 N+1 PROD apres fix
- [x] Seuls des fichiers app/ et config/ commites

Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Regles critiques

1. **PROD only** : ne fixer que les N+1 dont le call stack passe par `app/`. Les N+1 de test (factories, before) ne sont PAS des bugs de perf.
2. **Ne pas modifier les specs** pour faire taire Prosopite. Pas de `Prosopite.pause`, pas de Preloader dans le setup.
3. **Abandonner si aucun N+1 PROD** : ecrire un pr-description.md "Skip" et terminer sans commit.
4. **Pas de default_scope** avec includes.
5. **Preload vs Includes** : `preload` pour les polymorphiques ou quand on ne filtre pas sur l'association.
6. **1 fichier controller = 1 run** : traiter tous les N+1 du controller cible, pas d'autres.
7. **GraphQL** : avant de proposer un preload (`with_attached_*`, `includes`), vérifier si un `dataloader.with(Sources::Association, ...)` résout déjà le N+1. Si oui, le preload est redondant et contre-productif (charge les données même quand le client ne demande pas le champ). Vérifier aussi que le type GraphQL expose réellement les champs concernés.
8. **GraphQL — `inverse_of` avant preload nested** : quand on ajoute un resolver GraphQL avec un preload nested (ex: `dataloader.with(Sources::Association, labels: :procedure)`), vérifier si l'association parente déclare `inverse_of`. Si `has_many :labels, inverse_of: :procedure` existe côté parent, alors ActiveRecord remplit automatiquement `label.procedure` — le preload nested est redondant. Utiliser simplement `:labels`.

## Pieges connus (retours kaizen)

### Prosopite setup

L'ancien patch (`prosopite-setup.patch`) ciblait des offsets precis de `Gemfile.lock` et cassait regulierement. Remplace par `prosopite-setup.sh` — script idempotent qui utilise `bundle install` au lieu de patcher le lockfile.

### Faux positifs GraphQL batch loaders

Prosopite detecte des N+1 dans les tests GraphQL, mais en prod les `Sources::Association` (GraphQL::Dataloader) resolvent ces N+1 par batching automatique. Le pattern Prosopite est un artefact du contexte de test (pas de dataloader actif). Avant de fixer un N+1 dont la call stack passe par `app/graphql/`, verifier si un resolver utilise deja `dataloader.with(Sources::Association, ...)` pour cette association. Si oui, ne pas ajouter de preload — c'est contre-productif.

### Faux negatifs Prosopite

Prosopite ne detecte les N+1 que si N >= 2 records. Les specs avec 1 seul record ne declenchent rien. → Enrichir les fixtures avec `create_list(:model, 3, ...)`.

### Commandes avec variables d'environnement

`VAR=value bundle exec rspec ...` et `env VAR=value` sont systematiquement refuses. Modifier `config/environments/test.rb` directement via Edit a la place.

### Skip legitime

Si apres enrichissement aucun N+1 PROD n'est trouve, ecrire un pr-description.md "Skip" avec la raison. C'est un resultat valide, pas un echec.
