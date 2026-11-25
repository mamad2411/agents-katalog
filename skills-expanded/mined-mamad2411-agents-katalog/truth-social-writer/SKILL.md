---
name: truth-social-writer
description: Drafte un post Truth Social (fork Mastodon, ≤500 chars) — canal EXPÉRIMENTAL, le plus bas priorité du Sprint contenu (audience US généraliste/politique ~0 overlap avec l'ICP Argos cyber FR). Règle n°1 = BRAND SAFETY : strictement apolitique, sensibilisation sécurité grand public neutre, jamais de contenu culture-war/partisan. Anglais en général (audience US). Charge la KB (kb-rag), audit claude-judge avant écriture, anti-FUD strict. Mode DRAFT-ONLY : connecteur argos_ops/social/truth_social.py shadow tant que TRUTH_SOCIAL_ACCESS_TOKEN absent (accès API à demander). Utilise ce skill quand le user demande de drafter un post Truth Social / Truth, ou pendant /draft-truth.
---

# truth-social-writer

Skill éditorial dédié au **post Truth Social**. Truth Social est un **fork
de Mastodon** (même API, ≤500 chars). Mais soyons honnêtes sur le contexte :

> ⚠️ **Canal le plus expérimental et le plus bas priorité du Sprint
> contenu.** Truth Social est une plateforme **US généraliste / politique**
> dont l'audience n'a **quasiment aucun recouvrement** avec l'ICP Argos
> (CTO/RSSI de scaleups **françaises**, B2B cybersécurité). On y est par
> exploration / présence de marque, pas pour convertir.
>
> **Mode DRAFT-ONLY** : l'accès API Truth Social n'est pas ouvert librement
> (le fondateur doit le demander). Le connecteur
> `argos_ops/social/truth_social.py` reste en shadow tant que
> `TRUTH_SOCIAL_ACCESS_TOKEN` n'est pas rempli.
>
> 💡 **À reconsidérer** : vu le décalage d'audience, ça vaut le coup de se
> demander si ce canal mérite l'effort. Si le user hésite, dis-le-lui
> franchement — mieux vaut 4 canaux bien tenus qu'un 5e qui ne parle à
> personne.

## La règle n°1 : BRAND SAFETY (apolitique strict)

Truth Social est fortement **connoté politiquement** (registre culture-war
US). Argos est une marque **technique et neutre**. Le risque de marque est
de se faire happer par le registre de la plateforme. Donc, sans exception :

- **Zéro contenu politique / partisan / culture-war.** Jamais.
- **Ne réagis jamais** à l'actualité politique, ne reprends jamais les codes
  ou hashtags militants de la plateforme.
- Reste sur de la **sensibilisation sécurité grand public neutre** : des
  faits utiles, intemporels, applicables à n'importe qui (« vérifier la
  sécurité de son site », « sauvegardes », « mots de passe »).
- En cas de doute sur la neutralité d'un angle → **ne pas écrire**.

C'est le garde-fou le plus important du skill. Un seul post mal calibré ici
peut coller à la marque une couleur qu'on ne veut pas.

## Contraintes du canal

| Dimension | Règle | Pourquoi |
|-----------|-------|----------|
| **Longueur** | ≤ **500 chars** (moteur Mastodon) | Au-delà, l'API refuse. |
| **Langue** | **Anglais** en général (audience US) | Le FR n'aurait quasi aucun lecteur ici. Exploratoire de toute façon. |
| **Registre** | Neutre, factuel, sécurité grand public | Pas de jargon pointu (l'audience n'est pas cyber), mais surtout **rien de politique**. |
| **Hashtags** | 0-2, neutres (`#cybersecurity`, `#smallbusiness`) | Jamais de hashtag militant / partisan. |
| **Emoji** | 0-1 | Pas de cascade. |

## Inputs

- `topic` — sujet (toujours **neutre**, sécurité grand public)
- `(optionnel) angle` — sinon, propose-en 2-3, tous neutres.
- `(optionnel) cta` — lien (souvent rien).

Si `topic` a la moindre coloration politique → **refuser** et proposer un
angle sécurité neutre.

## Output

Fichier `data/content/drafts/YYYY-MM-DD-truth-<slug>.md` (slug = kebab-case
du topic ~50 chars ; date = TZ Paris) avec **exactement** ce frontmatter :

```markdown
---
channel: truth
status: draft            # draft | queued | validated | posted | rejected
date_created: YYYY-MM-DD
posted_at: null
topic: "<topic court>"
angle: "<angle retenu>"
character_count: <int — len(body), hors frontmatter>
kb_sources: ["faq.md§...", "pricing.md§Free", ...]
cta: "<url ou null>"
judge_score: <int 0-100>
judge_verdict: "<auto_send | queued | killed>"
judge_rationale: "<une phrase>"
judge_issues: []         # rempli UNIQUEMENT si verdict=queued
scheduled_for: null      # requis (ISO8601) pour la publi auto ; null = posting manuel
url_posted: null         # rempli après posting
---

<body du post, prêt à copier-coller. ≤ 500 chars. Neutre, apolitique.>
```

## Procédure (humain-in-the-loop)

### 1. Charge la KB

Invoque **`kb-rag`** avec `topic` (top-5). Charge en plus
`data/knowledge_base/tone_of_voice.md` (anti-FUD) et, selon le topic,
`faq.md` / `pricing.md` (tier d'entrée) / `argos_features.md`. **Traduis**
en grand public neutre — ne colle pas de jargon ni de claim non sourcé.

### 2. Drafting interactif

1. **Angle** — 2-3 options, **toutes neutres** (sécurité grand public).
   Recale immédiatement tout angle qui flirterait avec le politique.
2. **Hook** — une info utile et neutre.
3. **Corps** — 1-3 phrases simples, anglais en général.
4. **Lien / hashtag** — optionnels, neutres.

Recompte les chars (≤ 500).

### 3. Audit agent-juge (claude-judge) — AVANT écriture

Invoque **`claude-judge`** : `draft=body` + `original_query=topic` +
`rag_chunks` (étape 1) + `channel='social_truth'` + `agent_name='ContentBot'`.

```python
from argos_ops.judge import parse_judge_json, apply_thresholds
report = parse_judge_json(judge_output_text)
verdict = apply_thresholds(report)
```

- `verdict='killed'` → **n'écris pas**. Ici le juge surveille surtout
  **tone** (FUD ou dérive non-neutre) et **factual** (claim inventé).
- `verdict='queued'` → écris avec `status: queued` + `judge_issues:`.
- `verdict='auto_send'` → écris avec `status: draft`.

Toujours écrire `judge_score`, `judge_verdict`, `judge_rationale`.

### 4. Validation finale + écriture

- Preview + **character_count** (≤ 500) + **(judge_score / verdict)**.
- Refuse d'écrire si > 500 chars, `verdict='killed'`, ou **moindre doute de
  neutralité**.
- Demande confirmation, puis écris avec `Write`.

### 5. Posting (reporté — draft-only)

Accès API à demander par le fondateur. En attendant : posting **manuel**
(copier-coller + maj frontmatter `status: posted` + `posted_at:` +
`url_posted:`). Auto plus tard via le connecteur une fois
`TRUTH_SOCIAL_ACCESS_TOKEN` rempli.

## Anti-patterns à refuser (le 1er est non négociable)

- **Tout contenu politique / partisan / culture-war / réaction à l'actu
  politique** — refus immédiat, c'est la règle de marque n°1.
- **Hook mou** · **génération sans KB**.
- **FUD** — le vendor anxiogène est le cliché qu'on méprise (`tone_of_voice.md`).
- **Stats inventées** · **claim produit inventé** (coller à la KB).
- **Jargon cyber pointu** (audience non technique) · **buzzwords corporate**.
- **> 500 chars** · **cascade d'emoji** · **hashtag militant**.

## Critères qualité (checklist avant écriture)

- ✅ **100 % neutre / apolitique** (le critère qui prime)
- ✅ Frontmatter YAML valide et complet (dont `judge_*`)
- ✅ `character_count` ≤ 500
- ✅ ≥ 1 `kb_sources`, zéro FUD, zéro stat sans source
- ✅ Verdict claude-judge ≠ `killed`

## Liens

- Slash command : [`/draft-truth`](../../commands/draft-truth.md)
- Connecteur (shadow, accès à demander) : [`argos_ops/social/truth_social.py`](../../../argos_ops/social/truth_social.py)
- Setup credentials : section `# --- Truth Social ---` de `.env.example`
- Skills réutilisés : `kb-rag` (P6), `claude-judge` (P14)
- Skills cousins : `mastodon-writer`, `bluesky-writer`, `x-writer`,
  `linkedin-writer`, `meta-writer`
