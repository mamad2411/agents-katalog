---
name: seo-brief-writer
description: Génère un brief blog SEO structuré (titre, outline H2/H3, sources, meta) à partir d'un keyword + la KB Argos. Utilise ce skill quand le user demande de drafter un brief, de préparer un article blog, ou pendant /generate-seo-brief. Anti-générique IA via charge systématique du contexte KB (kb-rag P6).
---

# seo-brief-writer

Skill éditorial pour produire des briefs blog Argos qui :

- **N'ont pas le ton générique IA** (le risque #1 selon `MASTER_PROMPT.md`)
- Sont **factuels** (s'appuient sur la KB curée — `argos_features`,
  `competitor_compare`, `pricing`, `tone_of_voice`, `ICP`, `faq`)
- Respectent **les anti-patterns** SEO du repo (cf. `data/seo/README.md` :
  pas de stats inventées, pas de FUD, comparatifs honnêtes)
- Sont **prêts à exécuter** pour ContentBot (P9) ou pour rédaction manuelle

## Inputs

- `keyword` — la requête cible (ex : `"scanner DAST sans faux positifs"`)
- `(optionnel) angle` — angle éditorial spécifique demandé par le user
- `(optionnel) target_words` — longueur cible (défaut : 1800-2200)

## Outputs

Un fichier markdown dans `data/seo/briefs/YYYY-MM-DD-<slug>.md` avec
**exactement** cette structure :

```markdown
---
keyword: "<keyword exact>"
intent: awareness | consideration | decision
cluster: <cluster du keywords.yaml>
target_words: 1800-2200
date_created: YYYY-MM-DD
status: draft | ready | published
---

# <Titre H1 — accroche pour la SERP, 55-65 caractères, contient le keyword>

> Meta description (155-160 caractères, intention claire + keyword principal)

## Pitch (intro 80-120 mots)

<3-4 phrases qui posent le problème + annoncent l'angle. Pas de "Dans cet
article, nous verrons…". Style direct, dev-tools, factuel.>

## Outline

### H2 — <Section 1>
- Bullet 1 (point clé à développer)
- Bullet 2
- Bullet 3
### H2 — <Section 2>
- ...

(Typiquement 4-6 H2, avec 2-4 H3 ou bullets sous chaque H2.)

## Sources autorité à citer (5)

1. <Source URL ou nom> — utilisé pour : <quoi>
2. ...

## Internal links Argos (3)

- `/pricing` — quand parler du pricing
- `/<page-X>` — pertinent pour <quoi>
- ...

## Mots-clés secondaires à intégrer

- <variante longue traîne 1>
- <variante longue traîne 2>
- ...

## Notes éditoriales

- Ton : <rappel cible ICP — Marc/Sarah/Thomas, tu/vous, niveau technique>
- À éviter : <FUD spécifique, comparatif risqué, etc.>
- CTA en fin : <bouton/lien recommandé>
```

## Procédure (humain-in-the-loop)

1. **Validation du keyword** — vérifier qu'il est bien dans
   `data/seo/keywords.yaml` (sinon proposer de l'ajouter avec
   cluster/intent/priority). Vérifier qu'il n'y a pas déjà un brief
   `data/seo/briefs/*<slug>*.md`.

2. **Chargement contexte KB** (via skill `kb-rag` P6, idéalement) :
   - Toujours : `tone_of_voice.md` (ton + canaux) + `ICP.md` (cible perso).
   - Selon cluster :
     - `dast-faux-positifs` → `argos_features.md` § Oracle + `competitor_compare.md`
     - `pentest-continu` → `argos_features.md` § 3 (Watch + Strategist) + `ICP.md` anti-ICP
     - `compliance-tech` → `argos_features.md` § compliance (D-014, triple)
     - `devsecops` → `argos_features.md` § CI/CD + `faq.md` § FP marking
     - `ia-correlation` → D-013 (framing informatif/audit) + `argos_features.md` § Strategist
     - `bug-bounty` → `competitor_compare.md` § HackerOne + `ICP.md` § signaux
     - `vs-competitor` → `competitor_compare.md` entier + `faq.md`

3. **Drafting du brief section par section** :
   - **Titre H1** : montrer 2-3 propositions au user, faire valider.
   - **Meta description** : compter les caractères, ne pas dépasser 160.
   - **Pitch intro** : faire valider le ton (dev-tools, anti-FUD).
   - **Outline H2/H3** : proposer 4-6 H2 avec rationale (« H2 #3 traite
     l'objection X de Marc »), faire valider, ajuster.
   - **Sources autorité** : 5 sources réelles (OWASP, CVE, papers
     académiques, blogs RSSI, jamais inventer).
   - **Internal links** : 3 max — `/pricing`, `/features`, `/blog/<slug
     existant>`. Demander à l'user si pas sûr d'une page.
   - **Mots-clés secondaires** : extraire 3-5 variantes longue traîne.
   - **Notes éditoriales** : rappels concrets pour la rédaction (qui c'est,
     ton, à éviter, CTA).

4. **Validation finale** — montrer le brief complet, demander confirmation
   avant écriture.

5. **Écriture** — sauvegarder dans `data/seo/briefs/YYYY-MM-DD-<slug>.md`
   avec :
   - `YYYY-MM-DD` = date du jour (TZ Paris)
   - `<slug>` = kebab-case du keyword tronqué à 60 chars (ex :
     `scanner-dast-sans-faux-positifs`)

6. **Notif Discord (optionnel)** — pousser un mini-message sur le webhook
   `discord_webhook_ops_logs` : « Brief SEO livré : <titre> ». Pas
   bloquant — log seulement si le webhook est configuré.

## Anti-patterns à refuser

- **Génération sans KB** — si l'user dit « génère un brief sans charger la
  KB », expliquer pourquoi c'est non (cf. § Pourquoi de `MASTER_PROMPT.md`)
  et proposer d'ajouter un seed minimal.
- **Stats inventées** — refuser « 87 % des RSSI pensent que… » sauf si
  l'user fournit une source réelle.
- **FUD vs concurrents** — respecter § anti-disparagement de
  `competitor_compare.md`. Reformuler en comparatif factuel.
- **Trop d'internal links** — max 3 dans le brief (sinon, ça lit comme une
  page d'annuaire).
- **CTA agressif** — pas de « Cliquez ici maintenant ! ». Le CTA doit
  matcher l'intent (awareness = newsletter, decision = démo).

## Tests / validation

Pas de tests Python (skill éditorial pur). Critères qualité brief :

- ✅ Titre H1 contient le keyword exact
- ✅ Meta ≤ 160 caractères
- ✅ 4-6 H2 minimum, 1-3 H3 ou bullets par H2
- ✅ Chaque H2 a un rationale qui le rattache à un persona ICP ou une
  objection FAQ
- ✅ 5 sources réelles (testées : URL doit répondre 200 ou nom +
  référence vérifiable)
- ✅ 3 internal links cohérents avec la structure du site SecHunter
- ✅ Front matter YAML correct (parseable par un futur ContentBot)

## Liens

- Slash command `/generate-seo-brief` : `.claude/commands/generate-seo-brief.md`
- Keywords seed : `data/seo/keywords.yaml`
- Briefs produits : `data/seo/briefs/`
- KB consommée : `data/knowledge_base/` (6 fichiers)
- Skill réutilisé : `kb-rag` (P6)
