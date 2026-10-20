---
name: scenario-tester
description: Use this skill whenever the user asks to add a feature, fix a bug, refactor code, or write tests. Forces a discipline of writing test scenarios in markdown BEFORE coding, mapping each scenario 1:1 to an executable test, and maintaining tests/STATUS.md. Integrates with octo-issue-tracker via OCTO-### IDs. Triggers on: "implement", "add feature", "fix bug", "refactor", "write tests", "TDD", "ajoute", "implémente", "corrige", "code".
---

# Scenario-Tester — Discipline scénario-first

Tu n'écris JAMAIS de code de feature ou de fix sans avoir d'abord listé les scénarios de test et obtenu validation. Pas de "je code et on verra après". Le workflow ci-dessous est strict.

## Workflow obligatoire (3 phases)

### Phase 1 — Scénarios AVANT code

Quand l'utilisateur demande une nouvelle feature, un fix de bug, ou un refacto :

1. Identifie le nom de la feature en `kebab-case` (ex: `payment-flow`, `user-auth`, `csv-import`).
2. Crée ou met à jour `tests/scenarios/<feature>.md` au format ci-dessous.
3. **STOP**. Affiche les scénarios à l'utilisateur en français et demande validation explicite avant de coder quoi que ce soit.
4. Si l'utilisateur corrige/ajoute/retire des scénarios → reflète dans le fichier puis re-valide.

**Format strict de `tests/scenarios/<feature>.md`** :

```markdown
# <feature> — Scénarios de test

> Lié à : OCTO-### (si bug/issue tracker), <branche-git>

## S1 — <titre court>
**Étant donné** <contexte>
**Quand** <action>
**Alors** <résultat attendu>

## S2 — <titre court>
**Étant donné** ...
**Quand** ...
**Alors** ...

## S3 — Cas d'erreur : <titre>
**Étant donné** ...
**Quand** ...
**Alors** ...
```

Règles d'écriture :
- Chaque scénario a un **ID stable** (`S1`, `S2`, `S3`...). On n'enlève jamais un ID utilisé, on le marque `[OBSOLETE]` à la place.
- **Couvre systématiquement** : cas nominal, cas limites (vide, max, zéro, négatif), cas d'erreur (input invalide, dépendance KO, timeout).
- Titres en français, courts, **descriptifs du comportement** pas de l'implémentation.
- Pas de détails techniques (selectors, IDs DB, etc.) dans le scénario — c'est de la prose métier.

### Phase 2 — Implémentation tests + code (1:1)

Une fois les scénarios validés :

1. Crée le fichier de tests dans `tests/<feature>.{test.ts|spec.py|_test.go|...}` selon le runner détecté (voir section "Détection runner").
2. **Mapping 1:1 obligatoire** : chaque `S#` du `.md` = exactement un test dans le fichier d'implémentation. Le nom du test commence par son ID.

Exemples selon le langage :

```typescript
// vitest / jest
describe('payment-flow', () => {
  it('S1 — Refuse une carte expirée', () => { /* ... */ });
  it('S2 — Accepte un montant valide', () => { /* ... */ });
  it('S3 — Gère le timeout réseau', () => { /* ... */ });
});
```

```python
# pytest
class TestPaymentFlow:
    def test_S1_refuse_carte_expiree(self): ...
    def test_S2_accepte_montant_valide(self): ...
    def test_S3_gere_timeout_reseau(self): ...
```

```go
// go test
func TestPaymentFlow_S1_RefuseCarteExpiree(t *testing.T) { /* ... */ }
func TestPaymentFlow_S2_AccepteMontantValide(t *testing.T) { /* ... */ }
```

3. Écris les tests AVANT le code de la feature quand c'est possible (TDD). Sinon, en parallèle. **Jamais après.**
4. **Vérifie le mapping** : si tu as N scénarios dans le `.md`, tu dois avoir N tests dans le fichier. Si écart → tu corriges, tu ne caches pas.

### Phase 3 — Mise à jour de `tests/STATUS.md`

Après chaque session de travail sur une feature, mets à jour `tests/STATUS.md` à la racine du repo.

**Format strict** :

```markdown
# Test Status

> Dernière mise à jour : <date>
> Légende : [x] OK · [ ] TODO · [!] FAIL · [~] FLAKY · [-] OBSOLETE

## payment-flow
- [x] S1 — Refuse une carte expirée
- [x] S2 — Accepte un montant valide
- [ ] S3 — Gère le timeout réseau ← TODO
- [!] S4 — Double-débit en cas de retry ← OCTO-042
- [~] S5 — Webhook 3DSecure (flaky 2/10)

## user-auth
- [x] S1 — Login email+mdp valide
- [x] S2 — Refus mdp erroné
- [!] S3 — Lockout après 5 échecs ← OCTO-051
```

Règles :
- Une section `##` par feature, ordre alphabétique.
- Chaque ligne = un scénario, dans l'ordre des IDs.
- Le statut `[!]` ou `[~]` **DOIT** référencer un `OCTO-###` du `.octo/ISSUES.md` (créé par le skill octo-issue-tracker). Si l'issue n'existe pas encore, crée-la d'abord via octo-issue-tracker.
- Quand un test passe au vert, mets à jour le statut ET ferme l'issue OCTO correspondante.

## Détection du runner de tests

Au début de chaque session sur le repo, détecte le stack :

| Fichier détecté | Runner | Extension tests |
|---|---|---|
| `package.json` avec `vitest` | Vitest | `.test.ts` ou `.test.js` |
| `package.json` avec `jest` | Jest | `.test.ts` ou `.test.js` |
| `pyproject.toml` ou `pytest.ini` | pytest | `test_*.py` |
| `go.mod` | go test | `*_test.go` |
| `Cargo.toml` | cargo test | `tests/*.rs` |
| `pom.xml` ou `build.gradle` | JUnit | `*Test.java` |

Si ambigu → demande à l'utilisateur, ne devine pas.

## Lancement et lecture des résultats

Utilise la commande native du runner (`npm test`, `pytest`, `go test ./...`, `cargo test`).

Après chaque run :
1. Parse les noms de tests qui ont passé/failed (via le préfixe `S#`).
2. Mets à jour `tests/STATUS.md` automatiquement.
3. Pour chaque test en `[!]` qui n'a pas d'issue OCTO, **crée l'issue via octo-issue-tracker** avec :
   - Titre : `[<feature>] S# — <titre scénario>`
   - Severity : `high` si scénario nominal, `medium` si cas limite, `low` si edge case rare.
   - Description : sortie d'erreur du test (10 dernières lignes max).

## Intégration octo-issue-tracker

Les deux skills se parlent via les IDs `OCTO-###` :

- `scenario-tester` **lit** `.octo/ISSUES.md` pour récupérer les IDs en cours.
- `scenario-tester` **demande à octo-issue-tracker de créer** une issue quand un test fail durablement (≥ 2 runs consécutifs).
- `octo-issue-tracker` **gère** la création, le statut, la fermeture.
- Quand une issue OCTO est fermée parce qu'un test repasse vert → `scenario-tester` met `[x]` dans `STATUS.md` et retire la référence `← OCTO-###`.

Ne duplique JAMAIS l'info entre `STATUS.md` et `.octo/ISSUES.md`. `STATUS.md` = vue test-centric. `ISSUES.md` = vue bug-centric. Le lien c'est l'ID OCTO.

## Anti-patterns interdits

- ❌ Coder une feature sans avoir écrit les scénarios d'abord
- ❌ Ajouter un test sans son scénario correspondant dans le `.md`
- ❌ Modifier un scénario sans mettre à jour le test (et inversement)
- ❌ Skipper un test qui fail (`.skip`, `xit`, `@pytest.mark.skip`) sans une issue OCTO active référencée en commentaire au-dessus du test
- ❌ Mettre `[x]` dans `STATUS.md` sans avoir réellement run le test
- ❌ Cucumber/SpecFlow/Behave : on n'introduit PAS de framework BDD. Les `.md` sont de la doc, pas du code exécutable. Le mapping 1:1 est manuel et c'est très bien comme ça.

## Au démarrage de session

À la première utilisation dans un repo :

1. Vérifie l'existence de `tests/scenarios/` et `tests/STATUS.md`. Si absents → propose de les créer.
2. Vérifie que `octo-issue-tracker` est installé (présence de `.octo/` ou du skill). Si absent → préviens l'utilisateur que l'intégration bug-tracking sera désactivée.
3. Liste rapidement les features avec des `[!]` ou `[ ]` en cours dans `STATUS.md` pour rappeler le travail en attente.
