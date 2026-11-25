---
name: x-writer
description: Drafte un post X (ex-Twitter) ≤280 chars pour la communauté infosec/cyber Twitter — hook viral en 1re ligne, ton punchy/direct, 0-1 hashtag max. Charge la KB Argos (kb-rag), audit claude-judge avant écriture, anti-FUD strict. Mode DRAFT-ONLY : draft dans data/content/drafts/, connecteur argos_ops/social/twitter.py en shadow tant que X_ACCESS_TOKEN absent (activation live reportée — arbitrage Free vs Basic à trancher). Utilise ce skill quand le user demande de drafter un tweet / post X / Twitter, du contenu pour la cyber-Twitter, ou pendant /draft-x. Anti-générique IA via charge KB systématique.
---

# x-writer

Skill éditorial dédié au **post X (ex-Twitter)** Argos, pour la **cyber-
Twitter** (infosec, pentesters, devsecops, chercheurs). C'est l'audience la
plus proche de Mastodon… mais le **rythme** est tout autre : X récompense le
**hook qui stoppe le scroll**, le punch, parfois le côté meme. Un toot
Mastodon posé y passerait inaperçu.

> **Statut du canal** : **bas priorité + DRAFT-ONLY**. Le connecteur
> `argos_ops/social/twitter.py` reste en **shadow** (drafte, ne poste pas)
> tant que `X_ACCESS_TOKEN` n'est pas rempli, et l'activation live est
> **reportée** — le fondateur arbitrera d'abord Free vs Basic ($) côté API X.
> On drafte maintenant, on postera plus tard (manuel ou auto).

> **Pourquoi un skill dédié** : chaque réseau a sa physique. X = hook + 280
> chars. (Mastodon → `mastodon-writer`, Bluesky → `bluesky-writer`.)

## Contraintes du canal X

| Dimension | Règle | Pourquoi |
|-----------|-------|----------|
| **Longueur** | **≤ 280 chars** (hard limit) | Au-delà, l'API refuse. On vise 180-270 pour garder de l'air. |
| **Hook (ligne 1)** | C'est **90 % du job** : la 1re ligne doit arrêter le scroll | Sur X le feed défile vite ; sans hook, zéro lecture. |
| **Lien** | Une URL compte pour **~23 chars** (wrapping t.co), peu importe sa longueur réelle | Budgéter 23 chars dès qu'il y a un lien — souvent mieux sans (un post 100 % valeur perce plus). |
| **Hashtags** | **0-1 max** | X pénalise le hashtag-spam ; souvent **zéro** marche mieux. |
| **Ton** | Punchy, direct, technique mais nerveux, première personne OK | L'audience est tech et zappe le corporate. |
| **Emoji** | 0-1, technique si présent | Pas de cascade 🚀🔥💯. |

## Inputs

- `topic` — sujet (ex. `"faux positifs DAST"`, `"oracle reproductible"`,
  `"on a banni le mot 'à vérifier'"`)
- `(optionnel) angle` — sinon, propose-en 2-3 (côté hook).
- `(optionnel) cta` — lien voulu (sinon souvent rien).

Topic vague → demander précision : un bon tweet part d'une idée tranchée.

## Output

Fichier `data/content/drafts/YYYY-MM-DD-x-<slug>.md` (slug = kebab-case du
topic ~50 chars ; date = TZ Paris) avec **exactement** ce frontmatter :

```markdown
---
channel: x
status: draft            # draft | queued | validated | posted | rejected
date_created: YYYY-MM-DD
posted_at: null
topic: "<topic court>"
angle: "<angle retenu>"
character_count: <int — len(body), hors frontmatter>
kb_sources: ["argos_features.md§Oracle", "tone_of_voice.md§X", ...]
cta: "<url ou null>"
judge_score: <int 0-100>
judge_verdict: "<auto_send | queued | killed>"
judge_rationale: "<une phrase>"
judge_issues: []         # rempli UNIQUEMENT si verdict=queued
scheduled_for: null      # requis (ISO8601) pour la publi auto ; null = posting manuel
url_posted: null         # rempli après posting
---

<body du tweet, prêt à copier-coller. ≤ 280 chars.>
```

## Procédure (humain-in-the-loop)

### 1. Charge la KB — non négociable

Invoque **`kb-rag`** avec `topic` (top-5). Charge en plus :
`data/knowledge_base/tone_of_voice.md` (le ton maison, anti-FUD) +
`data/knowledge_base/ICP.md` (Thomas le pentester / la cyber-Twitter).
Conditionnellement : `argos_features.md`, `competitor_compare.md` (§ anti-
disparagement), `faq.md`.

### 2. Drafting interactif

Propose puis fais valider :

1. **Angle** — 2-3 options, chacune jugée sur son **hook potentiel**.
2. **Hook (ligne 1)** — concret, tranché, idéalement contre-intuitif. C'est
   ce qu'on travaille le plus.
3. **Corps** — 1-2 phrases nerveuses, jargon tech assumé. Pas de remplissage
   (chaque char compte).
4. **Lien / hashtag** — optionnels. Si lien : budgéter 23 chars. Si hashtag :
   1 max, ciblé (`#infosec`, `#AppSec`).

Recompte les chars à chaque itération. > 280 → réécrire plus court (ne pas
tronquer la chute).

### 3. Audit agent-juge (claude-judge) — AVANT écriture

Invoque **`claude-judge`** : `draft=body` + `original_query=topic` +
`rag_chunks` (étape 1) + `channel='social_x'` + `agent_name='ContentBot'`.

```python
from argos_ops.judge import parse_judge_json, apply_thresholds
report = parse_judge_json(judge_output_text)
verdict = apply_thresholds(report)
```

- `verdict='killed'` → **n'écris pas**. Issues + reformulation ciblée.
- `verdict='queued'` → écris avec `status: queued` + `judge_issues:`.
- `verdict='auto_send'` → écris avec `status: draft`.

Toujours écrire `judge_score`, `judge_verdict`, `judge_rationale`.

### 4. Validation finale + écriture

- Preview + **character_count** (≤ 280) + **(judge_score / verdict)**.
- Refuse d'écrire si > 280 chars ou `verdict='killed'`.
- Demande confirmation, puis écris avec `Write`.

### 5. Posting (reporté — draft-only)

Le canal est **bas priorité** : pas d'activation live tant que le fondateur
n'a pas tranché Free vs Basic côté API X. En attendant :

- **Manuel** : copier-coller le body sur X, puis maj frontmatter
  (`status: posted` + `posted_at:` + `url_posted:`).
- **Auto (plus tard)** : le connecteur `argos_ops/social/twitter.py` postera
  via l'API v2 dès que `X_ACCESS_TOKEN` (token user-context OAuth 2.0, scope
  `tweet.write`) sera rempli et le live activé.

## Anti-patterns à refuser

- **Hook mou** — « Petit thread sécu 🧵 » = scroll garanti. Le hook livre une
  idée, pas une annonce.
- **Génération sans KB** — risque ton générique IA.
- **FUD** — « votre boîte va se faire hacker ». Sur la cyber-Twitter, le
  vendor anxiogène est le cliché qu'on méprise (cf. `tone_of_voice.md`).
- **Stats inventées** — audience d'experts, une stat bidon est repérée.
- **FUD vs concurrents** — respect `competitor_compare.md` § anti-disparagement.
- **Buzzwords corporate**, **cascade d'emoji**, **2+ hashtags**.
- **> 280 chars** — réécrire, ne pas couper la chute.

## Critères qualité (checklist avant écriture)

- ✅ Frontmatter YAML valide et complet (dont `judge_*`)
- ✅ `character_count` ≤ 280 (lien compté ~23 si présent)
- ✅ Hook ligne 1 stoppe le scroll
- ✅ 0-1 hashtag, ≥ 1 `kb_sources`
- ✅ Zéro FUD, zéro stat sans source, zéro buzzword
- ✅ Verdict claude-judge ≠ `killed`

## Liens

- Slash command : [`/draft-x`](../../commands/draft-x.md)
- Connecteur live (shadow, reporté) : [`argos_ops/social/twitter.py`](../../../argos_ops/social/twitter.py)
- Setup credentials : section `# --- X / Twitter ---` de `.env.example`
- Skills réutilisés : `kb-rag` (P6), `claude-judge` (P14)
- Skills cousins (autres canaux) : `mastodon-writer`, `bluesky-writer`,
  `linkedin-writer`, `meta-writer`
