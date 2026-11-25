---
name: outbound-personalizer
description: Génère **1 ligne hyper-personnalisée** à insérer en début de cold email Argos, à partir d'une fiche `data/outbound/enriched/<lead>.md`. Évite les openers génériques (« j'ai vu votre profil ») et les fake compliments. La ligne doit prouver qu'on a lu une source publique précise et qu'elle motive le contact. Anti-fake-perso strict. Utilise ce skill quand le user prépare un envoi outbound, importe une séquence depuis lead-enricher, ou pendant /personalize-outbound.
---

# outbound-personalizer

Skill **éditorial chirurgical**. Une ligne, 80-180 caractères, qui doit
faire ouvrir le mail. Pas plus.

> **Pourquoi un skill dédié** : la perso est ce qui distingue un cold
> email accepté d'un cold email signalé comme spam. Sous-traiter à un
> LLM générique produit des « j'ai trouvé votre profil intéressant »
> qui font fuir. Ce skill encode la grille anti-fake-perso et impose
> une source publique citée.

## Inputs

- `enriched_path` — chemin vers la fiche
  `data/outbound/enriched/<lead>.md` produite par `lead-enricher`
- `(optionnel) sequence_step` — `1 | 2 | 3 | 4 | 5` (touche dans la
  séquence outbound). Influence le ton (touche 1 = découverte, touche
  5 = dernière relance / « break-up email »)
- `(optionnel) angle` — angle souhaité (`oracle`, `compliance`,
  `ci_cd`, `audit`, etc.)

## Output

Insertion dans le frontmatter du fichier enriched :

```yaml
personalizer:
  line_1: "<la ligne, 80-180 chars>"
  source_cited: "<URL ou identifiant source publique observée>"
  rationale: "<pourquoi cette ligne — ce qu'elle prouve à propos du lead>"
  generated_at: 2026-05-14T12:30+02:00
  angle: "oracle" | "compliance" | "ci_cd" | "audit" | "funding" | "hiring"
```

Le payload est **prêt à coller** comme première phrase d'un draft
outbound. Le fondateur (ou futur OutboundBot Python en P13.B) compose
le reste de l'email autour de cette ligne.

## Anatomie d'une ligne qui marche

Recette : **[fait observé public] + [implication pour le lead]**

### Bons exemples

- > « Vu votre récent post sur la migration GitLab CI → ArgoCD chez ACME — la couche DAST pré-merge devient pénible à câbler proprement, c'est exactement ce qu'on a creusé chez Omnividens. »
  - Source : LinkedIn post du lead (URL)
  - Angle : ci_cd
  - Prouve : on a lu un post précis daté, on a compris le sujet tech

- > « Bravo pour la levée série A annoncée la semaine dernière — la phase où l'équipe sécu passe de 1 à 4 personnes est typiquement celle où le DAST manuel craque. »
  - Source : article Maddyness / TechCrunch (URL)
  - Angle : funding + hiring
  - Prouve : on suit l'actu sectorielle, on connaît la dynamique d'équipe

- > « Vu votre annonce de poste 'Application Security Engineer' chez ACME (publiée le 12 mai) — pendant qu'on cherche le profil, un scanner DAST qui n'envoie pas 800 faux positifs allège l'attente. »
  - Source : URL annonce de poste publique
  - Angle : hiring
  - Prouve : on a regardé concrètement le poste ouvert, daté

### Mauvais exemples (à refuser systématiquement)

- ❌ « J'ai vu votre profil LinkedIn intéressant »
  - Pourquoi nul : 0 fait précis, classique du cold opener spammy
- ❌ « Félicitations pour vos belles réalisations »
  - Pourquoi nul : fake compliment générique, déclenche méfiance
- ❌ « Sachant que ACME est leader dans son secteur, vous êtes sûrement intéressé par »
  - Pourquoi nul : flatterie + pitch direct, ratio bullshit élevé
- ❌ « J'ai remarqué que vous travaillez dans la cybersécurité »
  - Pourquoi nul : trop vague (« cybersécurité » = tout le monde)
- ❌ « Notre solution innovante pourrait transformer votre approche »
  - Pourquoi nul : buzzwords (`innovante`, `transformer`), zéro fait

## Règles strictes (anti-fake-perso)

1. **Une source publique citée** — URL exacte dans `source_cited`,
   ou identifiant traçable (« post LinkedIn 2026-05-10 »). Si pas de
   source précise → refuser, demander à l'humain d'en fournir une ou
   passer le lead en `dnq`.

2. **Un fait spécifique et daté** — pas « vous travaillez dans X »,
   mais « vous avez fait Y le ZZ ». Si rien de précis n'est trouvé →
   refuser.

3. **Pas de flatterie gratuite** — pas de « bravo », « félicitations »,
   « impressionnant » SANS un fait concret derrière. Le compliment doit
   être ancré.

4. **Pas de pitch dans la ligne 1** — la ligne ne vend pas Argos. Elle
   établit la légitimité du contact. Le pitch vient ligne 2-3 du mail
   complet, pas ici.

5. **Pas de mention de prix / features** — pas de « pour 249 €/mois ».
   La ligne 1 est sociale, pas commerciale.

6. **Pas de « j'ai » répété** — varier les ouvertures, ne pas commencer
   tous les emails de la séquence par « J'ai vu... »

7. **80-180 caractères** — moins = trop sec, plus = on perd l'attention.

8. **Cohérence avec le BANT** — si le BANT score < 60, la ligne doit
   être plus soft (newsletter / content) que démo. Pas de poussée
   commerciale sur un lead tiède.

## Anti-patterns à refuser

- **Personnalisation falsifiée** — inventer un fait que la source ne
  contient pas (« j'ai vu votre keynote DevSecCon » alors qu'il n'a
  rien donné). Plus toxique qu'un opener générique : si le lead vérifie,
  rupture de confiance immédiate.
- **Fake citation** — paraphraser au point que le lead ne reconnaît
  pas ses propres mots. Sous-cas du précédent.
- **Mention d'info perso au-delà du pro public** — adresse perso,
  vie privée, famille, opinions politiques. Out, même si trouvable.
- **Tone négatif sur le lead** — « j'imagine que vous avez des
  problèmes de X », « vous galérez probablement avec Y » → off.
- **Sequence step ignoré** — touche 1 ≠ touche 5. La 5e doit être un
  « break-up » court (« je vous laisse tranquille, dernière question
  rapide : »), pas un nouveau pitch.

## Audit agent-juge (P14) — recommandé

Avant écriture, invoque `claude-judge` avec `draft=line_1` +
`original_query=topic outbound` + `channel='email'` +
`agent_name='OutboundBot'`. Verdict :

- `killed` → ligne refusée. Re-propose en corrigeant l'axe fail (souvent
  factual : claim non sourcé, ou tone : flatterie générique)
- `queued` → flag, demander validation explicite au fondateur avant
  envoi
- `auto_send` → OK pour insertion frontmatter

## Procédure

### 1. Lecture de l'enriched

- Charger le frontmatter du fichier
- Refuser si `status == "dnq"` (does not qualify — ne pas relancer)
- Refuser si `bant_score < 40` sauf si l'humain valide explicitement

### 2. Recherche signal personnalisable (humain-in-the-loop si besoin)

À partir des `sources` listées dans l'enriched :

- LinkedIn profile : derniers posts (3 derniers, datés < 60 jours)
- Page entreprise : annonces récentes, posts blog, actualités levée
- GitHub org si tech : commits récents, repos publics actifs
- Page carrières : postes ouverts (signal hiring sécu)

Si **aucun fait précis et daté < 60 jours** n'émerge → refuser de générer
une ligne (mieux vaut ne pas envoyer que envoyer un opener générique).
Proposer à l'humain de :

- soit passer le lead en touche newsletter / contenu (BANT-froid)
- soit passer en `dnq` si vraiment rien à dire

### 3. Drafting

- Proposer 2-3 lignes candidates avec angles différents
- Compter les caractères de chaque (80-180)
- Demander au fondateur de choisir / valider / corriger

### 4. Audit claude-judge

- Cf. § ci-dessus

### 5. Écriture

- Patch le frontmatter de l'enriched
- Status final : `personalizer` rempli, `status` reste `validated` (ou
  passe à `validated` si c'était `draft`)

## Liens

- Skill cousin : `lead-enricher` (produit l'enriched)
- ICP : `data/knowledge_base/ICP.md`
- Tone : `data/knowledge_base/tone_of_voice.md`
- Compliance outbound : `docs/COMPLIANCE.md` § 2 (intérêt légitime BtoB,
  opt-out 1-clic obligatoire)
- Audit Tier 1 : `.claude/skills/claude-judge/SKILL.md` (P14)
- Plan P13 : `docs/ARGOS_OPS_PLAN.md` § Partie 13
