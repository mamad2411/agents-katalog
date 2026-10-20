---
name: harden-fix
description: "Fix a qualified security vulnerability with TDD. Use when user has an audit file to fix."
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(bundle exec rspec:*)
  - Bash(bundle exec rubocop:*)
  - Bash(git add:*)
  - Bash(git commit:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git status)
  - Bash(git checkout -b:*)
  - Bash(gh pr create:*)
  - Bash(gh gist create:*)
  - Bash(gh auth setup-git:*)
  - Bash(git clone:*)
  - Bash(git -C /tmp/:*)
  - Bash(cp:*)
  - Bash(grep:*)
  - Skill(screenshot-gist)
  - Agent
---

# Harden Fix — Corriger une faille de sécurité

Agent spécialisé dans la correction de failles de sécurité avec approche TDD rigoureuse.

**Mission :** Prendre un fichier d'audit (`/harden-audit`), écrire un test prouvant la faille, corriger, produire une PR pédagogique.

---

## Documents de référence

1. **`checklist.md`** — Checklist par étape
2. **`../harden-audit/patterns.md`** — Patterns validés

---

## Étape 1 : Gate d'entrée

### 1a. Vérification du fichier d'audit

Lire `$ARGUMENTS` et vérifier selon `../harden-audit/contract.md` :
- `status: qualified` → Continuer
- `chain_verified: false` ou `confidence: low` → Re-vérification obligatoire (étape 2b)
- `status` ≠ `qualified` → Suggérer `/harden-audit` d'abord
- `verdict: faux positif` → STOP

Extraire : type faille (OWASP/CWE), score DREAD, STR/test_vector, fichiers impactés, root cause.

### 1b. Mode fast-track (sans fichier d'audit)

Si `$ARGUMENTS` vide ou invalide → créer audit minimal inline :
1. Demander : type de faille, endpoint, root cause suspectée
2. Créer `audits/YYYY-MM-DD-[slug]-audit.md` avec champs minimaux (`contract.md`), `confidence: low`, `chain_verified: false`
3. Continuer — re-vérification obligatoire

---

## Étape 2 : Analyse du code vulnérable

1. Lire les fichiers listés dans l'audit
2. Confirmer la root cause
3. Cartographier les points de correction

---

## Étape 2b : Re-vérification indépendante (TOUJOURS exécutée)

Re-tracer la chaîne : Route → Controller → before_action → Service → Model → DB. Lister chaque maillon avec `fichier:ligne`.

**Fast-track :** si l'audit a `confidence: high` ET `chain_verified: true` ET type ≠ IDOR/BAC → présenter un résumé court au user et demander confirmation rapide. Sinon → tracer la chaîne complète.

**Attention : authenticate ≠ authorize.** Un `before_action :authenticate_user!` ne protège PAS contre les IDOR entre utilisateurs authentifiés. Vérifier l'autorisation (scope user, policy, authorize), pas seulement l'authentification.

Puis présenter au user (5 lignes max par section) :

```
### Preuves que la faille est réelle
- [faits du code : absence de protection, données exposées]

### Preuves que la faille est un faux positif
- [faits du code : protection en aval, signaux d'intention, données déjà publiques]
- (AU MINIMUM un fait. Si aucune preuve de FP trouvable, écrire : "Aucune protection trouvée à aucun maillon de la chaîne (vérifié : [liste fichiers lus])")

### Ce que je ne peux pas déterminer depuis le code
- [ex: est-ce que ce comportement est voulu ?]
```

**Le user tranche.** Présenter les preuves, attendre la décision du user.

**Verdict :**
- User confirme faille réelle → continuer (fusionner avec validation du plan Étape 3 en un seul checkpoint si possible)
- User confirme faux positif → **STOP — mettre à jour l'audit**
- Preuves contradictoires → **STOP — demander au user**

**Si le user dit "débrouille-toi" :** écrire les preuves dans l'audit, marquer `confidence: low`, `chain_verified: true`, et continuer. Signaler dans la PR ce qui reste à valider par un humain.

---

## Étape 3 : Plan de commits

**Ne jamais coder sans plan validé.**

**Pattern TDD Sécurité (Red → Green → Harden) :**

```
Commit 1: test(security): add spec proving [faille]
  → Test PASSE = la faille existe
  → Ex: user non autorisé PEUT accéder → expect(:ok)

Commit 2: fix(security): [description du fix]
  → Appliquer le correctif minimal
  → Inverser l'assertion : expect(:unauthorized)
  → Tous les tests passent

Commit 3: refactor(security): [durcissement] (optionnel)
  → Edge cases, hardening complémentaire
```

**Attention assertions :**
- Commit 1 : `expect(:ok)` quand user non autorisé accède → passe = faille réelle
- Commit 2 : même scénario → `expect(:unauthorized)` → passe = faille corrigée

**Valider le plan avec l'utilisateur AVANT de coder.**

---

## Étape 4 : Commit 1 — Test prouvant la faille (RED)

1. Écrire le test de sécurité (request/model/system spec selon type)
2. Le test DOIT passer (prouve la faille)
3. Vérifier tous les tests verts
4. Commit : `test(security): add spec proving [description]`

---

## Étape 5 : Commit 2 — Fix + inversion assertion (GREEN)

1. Appliquer le correctif minimal
   - **Si nouveau fichier :** vérifier `config/initializers/inflections.rb` pour le casing des acronymes
2. Mettre à jour l'assertion du test (comportement corrigé)
3. Vérifier tous les tests verts + non-régression
4. Commit : `fix(security): [description]`

---

## Étape 6 : Mettre à jour audit et index

Mettre à jour le frontmatter de l'audit : `status: fixed`, `fixed_date`, `fix_pr`.
Mettre à jour `audits/INDEX.md`.

---

## Étape 7 : PR explicative

Reprendre les infos de l'audit (analogie, STR, impact) pour la PR :

```markdown
## Problème

[Type de faille] sur [endpoint]. Source : [YesWeHack / audit / interne]. Criticité : [DREAD /15].
Audit : `[chemin audit]`

### La faille en 30 secondes
[Analogie de l'audit]

### Steps to reproduce (avant ce fix)
[STR de l'audit]

## Solution

### Ce qui a été corrigé
- [Changement — pourquoi]

### Preuve par les tests
- **Test rouge** (commit 1) : prouve la faille — [scénario]
- **Test vert** (commit 2) : prouve la correction — [assertion inversée]

### Avant / Après (optionnel)
Utiliser `/screenshot-gist` pour uploader les screenshots.

### Points d'attention review
- [ ] Le fix ne casse pas [feature liée]
- [ ] Le test couvre le scénario d'exploitation
- [ ] Pas d'impact sur les utilisateurs légitimes
```

---

## Découper en PRs atomiques (si multi-failles sur une branche)

1. `git log --oneline main..<branche>` — identifier commits par faille
2. `git worktree add /tmp/fix-<slug> main` — branche isolée
3. Cherry-pick les commits de la faille
4. Push + PR depuis le worktree
5. Nettoyer après merge

---

## Livrable

- Test prouvant la faille (commit 1)
- Fix + assertion inversée (commit 2)
- PR explicative avec preuve par les tests
- Fichier d'audit mis à jour (`status: fixed`)
- Aucune régression
