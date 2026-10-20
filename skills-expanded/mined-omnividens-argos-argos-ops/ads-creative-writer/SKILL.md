---
name: ads-creative-writer
description: Génère 3 variantes d'annonce Ads (Google Ads / LinkedIn Ads / Meta Ads) à partir d'un objectif + persona ICP + KB Argos. Mode shadow uniquement (P12, 2026-05-14) — pas de publication API tant que le fondateur n'a pas branché un budget pub. Utilise ce skill quand le user demande de drafter une annonce, de générer des variantes A/B, ou pendant /draft-ad. Anti-générique IA via charge KB (kb-rag P6). Respecte les contraintes plateforme (longueur, headline count, disclaimer).
---

# ads-creative-writer

Skill éditorial pour produire des variantes d'annonces Argos qui :

- **Respectent les contraintes plateforme** (longueurs strictes, nombre de
  headlines / descriptions, char limits)
- **Sont alignées ICP** (Marc / Sarah / Thomas — cf. `ICP.md`)
- **Évitent les anti-patterns** : FUD vs concurrent, claims sans source,
  buzzwords corporate (cf. `tone_of_voice.md` § 4)
- **Sont prêtes à coller** dans l'interface de la plateforme (Google Ads
  Editor, LinkedIn Campaign Manager, Meta Ads Manager)

> **Mode shadow (P12 2026-05-14)** : ce skill produit des drafts dans
> `data/ads/drafts/`. La publication automatique via API arrive quand
> le fondateur active un budget pub et fournit les credentials.

## Plateformes supportées + contraintes 2026

| Plateforme | Format | Headlines | Descriptions | Display URL | Anti-pattern critique |
|---|---|---|---|---|---|
| **Google Ads (Search RSA)** | Responsive Search Ad | 3-15 × ≤ 30 chars | 2-4 × ≤ 90 chars | path1/path2 ≤ 15 chars | Pas de superlatifs interdits par Google (« le meilleur », « numéro 1 ») sans source vérifiable |
| **LinkedIn Ads (Sponsored Content)** | Single image | 1 × headline ≤ 150 chars | 1 × intro ≤ 600 chars | — | Public BtoB tech — pas de hype, pas d'emoji marketing |
| **Meta Ads (Facebook/Instagram)** | Image / Video | 1 × primary text ≤ 125 chars, 1 × headline ≤ 40 chars | 1 × description ≤ 30 chars | — | B2B Argos = canal **bas priorité** (audience moins matchée). Focus testimonial / case study si on y va |

## Inputs

- `platform` — `google_search | linkedin_sponsored | meta_image`
- `objective` — `awareness | consideration | leads | demo`
- `persona` — `marc | sarah | thomas` (cf. `ICP.md`)
- `angle` — angle éditorial (cf. `tone_of_voice.md`)
- `(optionnel) keyword` — si Google Ads RSA, le keyword cible
- `(optionnel) cta` — CTA spécifique voulu (par défaut : « Démo 20 min »
  pour leads/demo ; « Lire le benchmark » pour awareness)

## Outputs

Un fichier markdown dans `data/ads/drafts/YYYY-MM-DD-<platform>-<slug>.md`
avec frontmatter + 3 variantes (A/B/C) prêtes à copier-coller :

```markdown
---
platform: google_search | linkedin_sponsored | meta_image
status: draft | validated | live | rejected
date_created: YYYY-MM-DD
objective: awareness | consideration | leads | demo
persona: marc | sarah | thomas
keyword: "<keyword ou null>"
angle: "<angle retenu>"
kb_sources: ["pricing.md§3", "argos_features.md§Oracle", ...]
final_url: https://omnividens.fr/<lp>
display_url_path1: <≤15 chars>
display_url_path2: <≤15 chars>
posted_at: null
posted_campaign_id: null
---

## Variante A — <angle court>

**Headlines** (RSA = 3-15) :
1. <texte ≤ 30 chars>
2. <texte ≤ 30 chars>
3. <texte ≤ 30 chars>
...

**Descriptions** (RSA = 2-4) :
1. <texte ≤ 90 chars>
2. <texte ≤ 90 chars>

**Sitelinks** (optionnel, ≤ 25 chars chacun) :
- /pricing — Tarifs Pro Max
- /blog/oracle — Notre approche

**Note éditoriale** : <pourquoi cette variante, persona viseé, mesure
de succès attendue>

---

## Variante B — <angle court>
[... même structure ...]

---

## Variante C — <angle court>
[... même structure ...]
```

> **LinkedIn / Meta** : adapter la structure (1 seul headline + 1 description, pas
> de sitelinks). Inclure suggestion image (description) — pas d'image générée.

## Procédure (humain-in-the-loop)

### 1. Validation des inputs

- Si `platform` hors liste → demander laquelle.
- Si `objective` non spécifié → demander (impact direct sur le CTA).
- Si `persona` non spécifié → proposer le plus pertinent selon le keyword
  (Marc = sécu in-house ; Sarah = lead dev / CTO ; Thomas = MSP).

### 2. Chargement contexte KB

Invoquer le skill `kb-rag` (P6) avec `objective + persona` (top-5 chunks).
Charger systématiquement :

- `data/knowledge_base/tone_of_voice.md` — vocabulaire registre maison +
  banni
- `data/knowledge_base/ICP.md` — persona + signaux d'achat
- `data/knowledge_base/argos_features.md` — différenciants techniques
  (oracle, modules, Strategist, Watch)
- `data/knowledge_base/competitor_compare.md` — règles anti-disparagement

### 3. Drafting interactif (3 variantes diversifiées)

Proposer 3 angles **différents** (pas 3 paraphrases) avec rationale court :

- **Variante A — Tech-first** : différenciant produit (oracle, modules,
  preuve reproductible). Persona Marc.
- **Variante B — Bénéfice ops** : ROI temps équipe, coût FP, intégration
  CI/CD. Persona Sarah.
- **Variante C — Risque / urgence légitime** : OWASP, compliance ; AUCUN
  FUD. Persona Thomas / RSSI senior.

Pour chaque variante, **compter les caractères** au fur et à mesure et
**refuser** si une contrainte plateforme est violée.

### 4. Audit agent-juge (P14)

Avant écriture, invoque `claude-judge` pour CHAQUE variante avec :
`draft = bloc variante complet` + `original_query = objective + persona` +
`rag_chunks` + `channel = 'ads_<platform>'` + `agent_name = 'AdBot'`.

Parse via `argos_ops.judge.parse_judge_json` + `apply_thresholds`.

- Variante avec `verdict=killed` → ne l'inclus PAS dans le draft final.
  Re-propose une 4e variante.
- Variantes `queued` ou `auto_send` → on garde, en notant les
  `judge_score` au frontmatter agrégé.

### 5. Validation finale + écriture

- Preview les 3 variantes (ou 2 si une a été killed) + character_count
  pour chaque champ + `(judge_score moyen / pire verdict)`.
- Demander : « OK pour écrire dans `data/ads/drafts/<filename>.md` ? »
- Si oui, écrire. Slug = kebab-case de `<objective>-<persona>` tronqué
  à 50 chars.

### 6. Notif Discord (optionnel)

Pousser sur `DISCORD_WEBHOOK_OPS_LOGS` si configuré :
« Ad creative draft livré : [<platform>] <objective>/<persona> ·
`data/ads/drafts/<file>` ».

## Anti-patterns à refuser fermement

- **Génération sans KB** — refuser, expliquer le risque.
- **3 variantes paraphrasées** — refuser, exiger 3 angles vraiment
  différents (sinon le split-test ne mesure rien).
- **Stats inventées** — toute statistique chiffrée doit avoir une source
  réelle (OWASP, CVE, benchmark interne sourcé). Sinon retirer.
- **FUD vs concurrents** — respect strict `competitor_compare.md` § 10.
  Pas de « moins lent que Burp », pas de « plus complet que Acunetix »
  sans benchmark publiable.
- **Superlatifs Google-bannis** — « le meilleur », « numéro 1 », « parfait »,
  « 100 % » sans source vérifiable → rejet Google Ads (Editorial policy).
- **Buzzwords corporate** — « innovant », « disruptif », « game changer »,
  « synergie ». Cf. `tone_of_voice.md` § 4.
- **Emoji marketing en cascade** — 🚀🔥💯. Acceptable : 1 emoji
  technique sobre côté LinkedIn (📊 sur un benchmark) si pertinent.
- **Persona incohérent avec keyword** — ex : keyword « DAST CI/CD » sur
  persona Thomas (MSP) au lieu de Sarah (lead dev). Refuser et
  re-proposer.

## Cycle de vie d'un draft

| Status | Sens | Qui transitionne |
|---|---|---|
| `draft` | Sortie du skill, en attente de relecture | skill (création) |
| `validated` | Le fondateur a relu, prêt à pousser en plateforme | fondateur (manuel) |
| `live` | Publié en plateforme (campaign_id renseigné dans frontmatter) | fondateur (manuel jusqu'à activation API) ou futur AdBot Python |
| `rejected` | Pas publié — raison dans le frontmatter | fondateur |

## Tests / validation

Pas de tests Python (skill éditorial pur, pattern P9-DRAFT / P10-MVP).
Critères qualité par variante :

- ✅ Toutes les contraintes longueur respectées (compter avant valider)
- ✅ Au moins 1 `kb_sources` listée
- ✅ 3 angles vraiment différents (test : couper les 3 hooks, est-ce
  qu'on devine que c'est le même produit ?)
- ✅ Zéro superlatif Google-banni
- ✅ Zéro stat sans source

## Liens

- Slash command `/draft-ad` : `.claude/commands/draft-ad.md`
- Skill cousin : `ads-optimizer` (analyse perf campagnes, propose actions)
- Skill réutilisé : `kb-rag` (P6), `claude-judge` (P14)
- Plan P12 full : `docs/ARGOS_OPS_PLAN.md` § Partie 12
- Cycle : `data/ads/drafts/` (output) → `data/ads/campaigns/` (manifeste
  live, rempli par fondateur) → mesure perf via `ads-optimizer`
