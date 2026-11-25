---
name: mastodon-writer
description: Drafte un toot Mastodon Argos (300-500 chars, instance infosec.exchange) à partir d'un topic + la KB Argos. Ton tech assumé, partage technique d'abord (pas de promo directe), 2-3 hashtags, lien en fin de toot. Mode local-draft : draft dans data/content/drafts/, posting via le connecteur argos_ops/social/mastodon.py (shadow tant que MASTODON_ACCESS_TOKEN absent). Utilise ce skill quand le user demande de drafter un toot / post Mastodon / fediverse, de préparer du contenu pour infosec.exchange, ou pendant /draft-mastodon. Anti-générique IA via charge systématique de la KB (kb-rag). Anti-FUD strict, zéro emoji marketing.
---

# mastodon-writer

Skill éditorial dédié au **toot Mastodon** Argos, sur l'instance
`infosec.exchange` (audience cyber/infosec pointue). Cette communauté est
**la plus exigeante** de nos canaux : ce sont des praticiens (pentesteurs,
chercheurs, devsecops) qui détectent la promo à dix mètres et valorisent le
**partage technique honnête**. Un toot Argos doit apporter quelque chose
d'utile *avant* de mentionner le produit.

> **Pourquoi un skill dédié** : chaque réseau a sa physique. Ce skill ne
> fait qu'**une** chose : un bon toot Mastodon. (LinkedIn →
> `linkedin-writer`, Bluesky → `bluesky-writer`.) Il remplace l'ancien
> `content-writer` multi-canal, déprécié.

## Contraintes du canal Mastodon (infosec.exchange)

| Dimension | Règle | Pourquoi |
|-----------|-------|----------|
| **Longueur** | **300-500 chars** | Mastodon autorise 500 chars sur infosec.exchange. On vise dense, pas bavard. |
| **Structure** | 1-2 paragraphes denses, vocabulaire tech assumé | L'audience l'attend et le préfère au vulgarisé. |
| **Promo** | **Partage technique d'abord** — le produit vient après, en soutien | La promo directe est mal vue (règles communautaires + culture instance). |
| **CTA / lien** | Lien en **fin** de toot, vers une page feature ou un blog (**pas** vers la démo) | Un lien démo en tête = réflexe pub rejeté. Le lien doit prolonger le partage. |
| **Hashtags** | **2-3**, en fin | `#infosec`, `#AppSec`, `#DAST`, `#pentest`. Ciblés, pas décoratifs. |
| **Emoji** | **Zéro** emoji marketing | Pas le registre de l'instance. |
| **Compte bot** | Le compte doit avoir le **flag bot activé** (règle instance pour le contenu automatisé) | Conformité aux règles d'infosec.exchange. |

## Inputs

- `topic` — sujet (ex. `"oracle reproductible vs faux positifs"`,
  `"BOLA — OWASP API Top 10"`, `"pourquoi on a banni 'à vérifier'"`)
- `(optionnel) angle` — angle précis. Sinon, propose-en 2-3.
- `(optionnel) cta` — lien voulu (feature/blog), ou rien

Si `topic` est vague → demander une précision : un bon toot part d'une idée
technique nette.

## Output

Fichier `data/content/drafts/YYYY-MM-DD-mastodon-<slug>.md` (slug =
kebab-case du topic tronqué à ~50 chars ; date = TZ Paris) avec **exactement**
ce frontmatter :

```markdown
---
channel: mastodon
status: draft            # draft | queued | validated | posted | rejected
date_created: YYYY-MM-DD
posted_at: null
topic: "<topic court>"
angle: "<angle retenu>"
character_count: <int — len(body), hors frontmatter>
kb_sources: ["argos_features.md§Oracle", "tone_of_voice.md§Mastodon", ...]
cta: "<url ou null>"
judge_score: <int 0-100>
judge_verdict: "<auto_send | queued | killed>"
judge_rationale: "<une phrase>"
judge_issues: []         # rempli UNIQUEMENT si verdict=queued (liste de strings)
scheduled_for: null      # requis (ISO8601) pour la publi auto ContentBot ; null = posting manuel
url_posted: null         # rempli après posting (manuel ou ContentBot)
---

<body du toot, prêt à copier-coller. Lien + hashtags en fin.>
```

## Procédure (humain-in-the-loop)

### 1. Charge le contexte KB — non négociable

Invoque **`kb-rag`** avec `topic` (top-5 chunks). Charge en plus,
systématiquement :

- `data/knowledge_base/tone_of_voice.md` — registre + canaux
- `data/knowledge_base/ICP.md` — qui lit Mastodon : surtout **Thomas** le
  pentester freelance / bug bounty (l'évangéliste tech qui poste sur
  Mastodon & Hacker News) et les ICs techniques ; **Sarah** la Head of
  Security / RSSI y veille de loin. Marc le CTO de scaleup est plutôt sur
  LinkedIn (cf. `linkedin-writer`).

Conditionnellement : `argos_features.md` (+ `argos_modules.raw.json`),
`competitor_compare.md` (§ anti-disparagement), `faq.md`.

### 2. Drafting interactif (interview court)

Propose puis fais valider :

1. **Angle** — 2-3 options, en privilégiant le **partage technique** sur la
   promo.
2. **Hook (1re phrase)** — une affirmation technique concrète, idéalement
   contre-intuitive.
3. **Corps** — 1-2 paragraphes denses, jargon OK (audience l'attend).
4. **Lien** — en fin, vers feature/blog (pas démo), ou rien : un toot 100 %
   valeur sans lien marche très bien.
5. **Hashtags** — 2-3 ciblés, en fin.

Recompte les chars. Si > 500 ou < 300 → ajuster avant d'avancer.

### 3. Audit agent-juge (claude-judge) — AVANT écriture

Invoque **`claude-judge`** avec : `draft=body` + `original_query=topic` +
`rag_chunks` (étape 1) + `channel='social_mastodon'` +
`agent_name='ContentBot'`.

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

- Preview avec **character_count** + **(judge_score / verdict)**.
- Refuse d'écrire si hors 300-500 chars ou `verdict='killed'`.
- Demande confirmation, puis écris avec `Write`.

### 5. Posting (jusqu'au ContentBot full)

Le connecteur `argos_ops/social/mastodon.py` toote via l'API dès que
`MASTODON_ACCESS_TOKEN` est rempli (instance par défaut `infosec.exchange`,
D-025). En shadow sinon.

- **Manuel** : copier-coller dans infosec.exchange, puis éditer le
  frontmatter (`status: posted` + `posted_at:` + `url_posted:`).
- **Auto** : le publisher (`find_ready_drafts`) ramasse `status: validated`
  + `scheduled_for` ≤ now et toote via le connecteur. `content-scheduler`
  pose le `scheduled_for` (fenêtres d'engagement Mastodon).

## Anti-patterns à refuser

- **Génération sans KB** — risque ton générique IA.
- **Promo directe en tête** — sur cette instance, le produit vient en
  soutien d'un partage technique, jamais en accroche.
- **Stats inventées** — sur un public d'experts, une stat bidon coûte la
  crédibilité. Source réelle ou rien.
- **FUD vs concurrents** — respect strict de `competitor_compare.md`
  § anti-disparagement.
- **Buzzwords corporate** — « game changer », « disruptif », « synergie ».
- **Tout emoji marketing** — zéro toléré sur Mastodon.
- **Lien démo en tête** — réflexe pub rejeté.
- **> 500 chars** — réécrire plus court.

## Critères qualité (checklist avant écriture)

- ✅ Frontmatter YAML valide et complet (dont `judge_*`)
- ✅ `character_count` ∈ [300, 500]
- ✅ ≥ 1 `kb_sources` (preuve KB consultée)
- ✅ Partage technique en tête, produit en soutien
- ✅ 2-3 hashtags ciblés + lien (feature/blog) en fin
- ✅ Zéro emoji, zéro buzzword, zéro stat sans source, zéro FUD
- ✅ Verdict claude-judge ≠ `killed`

## Liens

- Slash command : [`/draft-mastodon`](../../commands/draft-mastodon.md)
- Connecteur live : [`argos_ops/social/mastodon.py`](../../../argos_ops/social/mastodon.py)
- Drafts produits : `data/content/drafts/`
- Skills réutilisés : `kb-rag` (P6), `claude-judge` (P14), `content-scheduler`
- Skills cousins (autres canaux) : `linkedin-writer`, `bluesky-writer`,
  `seo-brief-writer` (blog longform)
