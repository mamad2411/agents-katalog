---
name: linkedin-writer
description: Drafte un post LinkedIn organique Argos (1300-2000 chars) à partir d'un topic + la KB Argos. Hook ligne 1 → 3-4 paragraphes courts → CTA soft → 3-5 hashtags. Persona Marc (CTO scaleup, cœur de cible) + Sarah (Head of Security / RSSI), ton pro mais humain, anti-buzzword corporate, 1 emoji technique max. Mode local-draft : draft dans data/content/drafts/, posting via le connecteur argos_ops/social/linkedin.py (shadow tant que LINKEDIN_PERSONAL_ACCESS_TOKEN absent). Utilise ce skill quand le user demande de drafter un post LinkedIn, de préparer du contenu LinkedIn, ou pendant /draft-linkedin. Anti-générique IA via charge systématique de la KB (kb-rag). Anti-FUD strict.
---

# linkedin-writer

Skill éditorial dédié au **post LinkedIn** Argos. LinkedIn est notre canal
n°1 pour toucher les décideurs sécu (RSSI, DSI, lead AppSec). L'audience y
est professionnelle mais lassée du contenu corporate creux — un bon post
LinkedIn Argos est **concret, utile, et honnête**, jamais une pub déguisée
en « insight ».

> **Pourquoi un skill dédié** : chaque réseau a sa physique (longueur,
> format, tonalité, ce que l'audience tolère). Ce skill ne fait qu'**une**
> chose : un bon post LinkedIn. (Mastodon → `mastodon-writer`, Bluesky →
> `bluesky-writer`.) Il remplace l'ancien `content-writer` multi-canal,
> déprécié.

## Contraintes du canal LinkedIn

| Dimension | Règle | Pourquoi |
|-----------|-------|----------|
| **Longueur** | **1300-2000 chars** (body) | Assez pour développer une idée, pas un mur. LinkedIn tronque après ~3 lignes avec un « …voir plus ». |
| **Hook** | 1re ligne forte, lisible seule | C'est ce qui décide du clic « voir plus » dans le feed. |
| **Structure** | 3-4 paragraphes courts (≤ 4 lignes), 1 idée chacun, séparés par une ligne vide | LinkedIn casse souvent le formatting ; les blocs aérés se lisent mieux au mobile. |
| **CTA** | Soft : « Démo ? », lien `omnividens.fr/blog/<post>`, ou question ouverte | LinkedIn pénalise les liens sortants dans le corps — un CTA conversationnel marche souvent mieux. |
| **Hashtags** | **3-5**, en fin de post | Au-delà de 5, l'algo punit (cf. `tone_of_voice.md`). |
| **Emoji** | 1 emoji **technique** max (📊 sur un bench), zéro cascade marketing | 🚀🔥💯 = registre pub, pas le nôtre. |
| **Markdown** | Aucun (`**gras**` ne rend pas) | Body livré prêt à copier-coller, ponctuation propre. |

## Inputs

- `topic` — sujet (ex. `"faux positifs DAST"`, `"correction hebdo SecHunter
  v2.4"`, `"OWASP API Top 10 — BOLA"`)
- `(optionnel) angle` — angle éditorial précis. Sinon, propose-en 2-3.
- `(optionnel) cta` — CTA voulu (lien démo / blog, ou question)

Si `topic` est vague (« cybersécurité », « la tech ») → demander une
précision : un bon post part d'une idée nette, pas d'un thème.

## Output

Fichier `data/content/drafts/YYYY-MM-DD-linkedin-<slug>.md` (slug =
kebab-case du topic tronqué à ~50 chars ; date = TZ Paris) avec **exactement**
ce frontmatter :

```markdown
---
channel: linkedin
status: draft            # draft | queued | validated | posted | rejected
date_created: YYYY-MM-DD
posted_at: null
topic: "<topic court>"
angle: "<angle retenu>"
character_count: <int — len(body), hors frontmatter>
kb_sources: ["pricing.md§Pro Max", "competitor_compare.md§Acunetix", ...]
cta: "<lien/texte ou null>"
judge_score: <int 0-100>
judge_verdict: "<auto_send | queued | killed>"
judge_rationale: "<une phrase>"
judge_issues: []         # rempli UNIQUEMENT si verdict=queued (liste de strings)
scheduled_for: null      # requis (ISO8601) pour la publi auto ContentBot ; null = posting manuel
url_posted: null         # rempli après posting (manuel ou ContentBot)
---

<body du post, prêt à copier-coller dans LinkedIn>
```

## Procédure (humain-in-the-loop)

### 1. Charge le contexte KB — non négociable

Le risque n°1 (cf. `MASTER_PROMPT.md`) est le ton générique IA. L'antidote
est de partir de faits réels issus de la KB curée.

Invoque **`kb-rag`** avec `topic` (top-5 chunks). Charge en plus,
systématiquement :

- `data/knowledge_base/tone_of_voice.md` — registre + canaux
- `data/knowledge_base/ICP.md` — qui lit LinkedIn : **Marc** le CTO de
  scaleup (cœur de cible, porte la sécu en plus du reste, objecte sur le
  bruit des faux positifs et le time-to-value) et **Sarah** la Head of
  Security / RSSI (deuxième cercle, objecte sur compliance / BYOK / audit).
  Thomas le pentester freelance est plutôt sur Mastodon (cf. `mastodon-writer`).

Conditionnellement selon le topic : `argos_features.md`
(+ `argos_modules.raw.json`), `competitor_compare.md` (§ anti-disparagement),
`faq.md`, `pricing.md`.

### 2. Drafting interactif (interview court)

Propose puis fais valider, étape par étape :

1. **Angle** — 2-3 options avec rationale (« angle A traite l'objection X
   de Marc »).
2. **Hook (ligne 1)** — la phrase qui déclenche le « voir plus ».
3. **Corps** — 3-4 paragraphes courts, 1 idée chacun, ligne vide entre eux.
   Vocabulaire pro et technique mais pas hermétique : Marc est CTO (il code)
   mais la sécu n'est pas sa spécialité — éviter le jargon pentest pur.
4. **CTA** — soft, matché à l'intent (démo, blog, ou question ouverte).
5. **Hashtags** — 3-5, ciblés (`#cybersécurité`, `#RSSI`, `#AppSec`,
   `#DAST`), pas décoratifs.

Recompte les chars à chaque itération. Si hors bornes 1300-2000 →
ajuster avant d'avancer.

### 3. Audit agent-juge (claude-judge) — AVANT écriture

Invoque **`claude-judge`** avec : `draft=body` + `original_query=topic` +
`rag_chunks` (étape 1) + `channel='social_linkedin'` +
`agent_name='ContentBot'`.

```python
from argos_ops.judge import parse_judge_json, apply_thresholds
report = parse_judge_json(judge_output_text)
verdict = apply_thresholds(report)
```

- `verdict='killed'` → **n'écris pas**. Montre les issues (factual / tone /
  legal) et propose une reformulation ciblée.
- `verdict='queued'` → écris avec `status: queued` + `judge_issues:`.
- `verdict='auto_send'` → écris avec `status: draft`.

Dans tous les cas, écris `judge_score`, `judge_verdict`, `judge_rationale`
au frontmatter.

### 4. Validation finale + écriture

- Preview du post complet avec **character_count** + **(judge_score /
  verdict)**.
- Refuse d'écrire si hors 1300-2000 chars ou `verdict='killed'`.
- Demande confirmation, puis écris avec `Write`.

### 5. Posting (jusqu'au ContentBot full)

Le connecteur `argos_ops/social/linkedin.py` poste via l'API LinkedIn dès
que le token est rempli (App #1 perso `LINKEDIN_PERSONAL_ACCESS_TOKEN`, ou
App #2 Page `LINKEDIN_PAGE_ACCESS_TOKEN` après approbation CMA — cf. memo
project). En shadow sinon.

- **Manuel** : copier-coller dans LinkedIn, puis éditer le frontmatter
  (`status: posted` + `posted_at:` + `url_posted:`).
- **Auto** : le publisher (`find_ready_drafts`) ramasse les drafts
  `status: validated` + `scheduled_for` ≤ now et poste via le connecteur.
  Le skill `content-scheduler` pose le `scheduled_for` (fenêtres
  d'engagement LinkedIn).

## Anti-patterns à refuser

- **Génération sans KB** — risque ton générique IA.
- **Stats inventées** — « 87 % des RSSI… » sans source réelle = retirer ou
  demander la source.
- **FUD vs concurrents** — respect strict de `competitor_compare.md`
  § anti-disparagement. Pas de « contrairement à [concurrent] qui rate… ».
- **Buzzwords corporate** — « game changer », « disruptif », « innovant »,
  « synergie », « révolutionnaire » → reformuler en concret.
- **Emoji marketing en cascade** — 🚀🔥💯. 1 emoji technique max.
- **CTA agressif** — « Cliquez ici maintenant ! », « Ne ratez pas ! ».
- **> 5 hashtags** — l'algo punit.
- **Mur de texte** — un seul gros paragraphe. Aérer en blocs courts.

## Critères qualité (checklist avant écriture)

- ✅ Frontmatter YAML valide et complet (dont `judge_*`)
- ✅ `character_count` ∈ [1300, 2000]
- ✅ ≥ 1 `kb_sources` (preuve KB consultée)
- ✅ Hook tient seul sur la 1re ligne
- ✅ 3-5 hashtags ciblés en fin de post
- ✅ Zéro buzzword corporate, zéro stat sans source, zéro FUD
- ✅ Verdict claude-judge ≠ `killed`

## Liens

- Slash command : [`/draft-linkedin`](../../commands/draft-linkedin.md)
- Connecteur live : [`argos_ops/social/linkedin.py`](../../../argos_ops/social/linkedin.py)
- Drafts produits : `data/content/drafts/`
- Skills réutilisés : `kb-rag` (P6), `claude-judge` (P14), `content-scheduler`
- Skills cousins (autres canaux) : `mastodon-writer`, `bluesky-writer`,
  `seo-brief-writer` (blog longform)
