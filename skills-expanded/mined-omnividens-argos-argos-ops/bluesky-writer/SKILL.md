---
name: bluesky-writer
description: Drafte un post Bluesky (≤300 graphemes) à partir d'un topic + la KB Argos, ton tech early-adopters / infosec, hook punchy ligne 1 + hashtag #infosec ou #cyber, CTA optionnel vers omnividens.fr. Mode local-draft (Sprint B) — le draft part dans data/content/drafts/, le posting passe par le connecteur argos_ops/social/bluesky.py (shadow tant que BLUESKY_HANDLE/APP_PASSWORD absents). Utilise ce skill quand le user demande de drafter un post Bluesky / bsky, de préparer du contenu pour le réseau AT Protocol, ou pendant /draft-bluesky. Anti-générique IA via charge systématique de la KB (kb-rag). Anti-FUD strict.
---

# bluesky-writer

Skill éditorial pour produire un post **Bluesky** Argos qui sonne juste
sur ce réseau précis. Bluesky n'est pas « Twitter en plus petit » : son
audience early-adopters est largement composée de gens tech qui ont fui X,
beaucoup d'infosec, de devs, de chercheurs. Ils détectent le ton corporate
et le marketing IA générique à dix mètres. Le post doit donc être **dense,
technique, et honnête** — pas une pub déguisée.

C'est le canal **quick win 100 % gratuit** du Sprint contenu : l'API AT
Protocol est gratuite et illimitée (un *app password* gratuit depuis
bsky.app → Settings → App Passwords suffit). Pas de quota payant à arbitrer
comme sur X.

> **Pourquoi un skill dédié et pas `content-writer` générique** : chaque
> réseau a sa physique propre (longueur, rich text, tonalité, ce que
> l'audience tolère). Mélanger Bluesky / LinkedIn / Mastodon dans un seul
> skill produit du contenu mou qui ne colle parfaitement à aucun. Ce skill
> ne fait qu'**une** chose : un bon post Bluesky.

## Contraintes du canal Bluesky

| Dimension | Règle | Pourquoi |
|-----------|-------|----------|
| **Longueur** | ≤ **300 graphemes** (hard limit API) | Au-delà, `createRecord` refuse le post. On vise 200-290 pour garder de l'air. |
| **Hook** | 1re ligne = l'accroche, lisible seule | Le feed Bluesky tronque ; la 1re ligne décide si on déplie. |
| **Hashtags** | 1 à 3, dont **#infosec** ou **#cyber** | Sur-tagger fait spam. Le connecteur les rend cliquables (facets), donc ils servent vraiment à la découverte. |
| **Liens** | URL en clair (ex. `https://omnividens.fr`), CTA optionnel | Le connecteur génère les facets → le lien est cliquable. Pas besoin de raccourcisseur. **Un lien compte dans les 300 graphemes** (pas de t.co qui raccourcit). |
| **Ton** | Tech, direct, première personne OK | L'audience est technique et l'attend. Pas de « nous sommes ravis de vous annoncer ». |
| **Emoji** | 0-1 max, technique si présent (📊 sur un bench) | Les cascades 🚀🔥💯 trahissent le bot marketing. |

> **Graphemes ≠ caractères Python** : un emoji ou un caractère composé
> peut compter pour 1 grapheme mais plusieurs code points. Pour rester
> safe, traite `len(body)` (code points) comme borne haute — si
> `len(body) ≤ 300`, le post passe forcément. La constante de référence
> côté code est `argos_ops.social.bluesky.MAX_GRAPHEMES`.

## Inputs

- `topic` — sujet du post (ex. `"oracle reproductible vs faux positifs"`,
  `"OWASP API Top 10 — BOLA"`, `"pourquoi on a banni 'à vérifier'"`)
- `(optionnel) angle` — angle éditorial précis. Sinon, propose-en 2-3.
- `(optionnel) cta` — lien voulu (par défaut `https://omnividens.fr` ou rien)

Si `topic` est vague (« cybersécurité », « la tech »), demande une
précision — un bon post Bluesky part d'une idée nette, pas d'un thème.

## Output

Un fichier markdown dans
`data/content/drafts/YYYY-MM-DD-bluesky-<slug>.md` avec **exactement** ce
frontmatter (slug = kebab-case du topic, tronqué à ~50 chars ; date = TZ
Paris) :

```markdown
---
channel: bluesky
status: draft            # draft | queued | validated | posted | rejected
date_created: YYYY-MM-DD
posted_at: null
topic: "<topic court>"
angle: "<angle retenu>"
character_count: <int — len(body) en code points, hors frontmatter>
kb_sources: ["argos_features.md§Oracle", "tone_of_voice.md§Bluesky", ...]
cta: "<url ou null>"
judge_score: <int 0-100>
judge_verdict: "<auto_send | queued | killed>"
judge_rationale: "<une phrase>"
judge_issues: []         # rempli UNIQUEMENT si verdict=queued (liste de strings)
scheduled_for: null      # requis (ISO8601) pour la publi auto ContentBot ; null = posting manuel
url_posted: null         # rempli après posting (manuel ou ContentBot)
---

<body du post, exactement ce qui sera publié — prêt à copier-coller
ou à envoyer au connecteur. Hashtags et lien inclus dans le texte.>
```

Le body est livré **prêt à publier** : pas de markdown (`**bold**` ne
rend pas sur Bluesky), pas de smart quotes exotiques, sauts de ligne
respectés. Le lien et les hashtags vivent **dans le texte** (le connecteur
construit les facets à partir du texte brut).

## Procédure (humain-in-the-loop)

### 1. Charge le contexte KB — non négociable

Le risque n°1 (cf. `MASTER_PROMPT.md`) est le ton générique IA. L'antidote
est de partir de faits réels issus de la KB curée, pas d'inventer.

Invoque le skill **`kb-rag`** avec `topic` (top-5 chunks). Charge en plus,
systématiquement :

- `data/knowledge_base/tone_of_voice.md` — registre + canaux
- `data/knowledge_base/ICP.md` — qui lit Bluesky côté Argos (plutôt
  Sarah la pentesteuse / Thomas le dev sécu que Marc le RSSI corporate)

Conditionnellement selon le topic :
- feature produit → `argos_features.md` (+ `argos_modules.raw.json`)
- comparaison concurrent → `competitor_compare.md` (§ anti-disparagement)
- objection / question → `faq.md`
- prix → `pricing.md`

### 2. Drafting interactif (interview court)

Propose puis fais valider, étape par étape :

1. **Angle** — 2-3 options avec rationale court (« angle A montre l'oracle
   à un public qui a déjà été brûlé par des faux positifs »). Sur Bluesky,
   l'angle « partage technique » > l'angle « promo ».
2. **Hook (ligne 1)** — la phrase qui doit donner envie de déplier. Une
   idée forte, concrète, idéalement contre-intuitive ou chiffrée (avec
   source réelle).
3. **Corps** — 1-2 phrases denses qui tiennent la promesse du hook. Pas de
   remplissage. Vocabulaire tech assumé.
4. **CTA** — soft. Lien vers une page feature / blog / `omnividens.fr`, ou
   rien. Sur Bluesky, un post 100 % valeur sans lien marche très bien.
5. **Hashtags** — 1 à 3, dont `#infosec` ou `#cyber`. Les choisir pour la
   découverte réelle (`#appsec`, `#pentest`, `#DAST`), pas pour décorer.

Recompte les graphemes à chaque itération. Si > 300 → raccourcis **avant**
d'aller plus loin, ne va pas jusqu'à l'écriture.

### 3. Audit agent-juge (claude-judge) — AVANT écriture

Invoque le skill **`claude-judge`** avec : `draft=body` +
`original_query=topic` + `rag_chunks` (de l'étape 1) +
`channel='social_bluesky'` + `agent_name='ContentBot'`.

Parse le verdict côté Python :

```python
from argos_ops.judge import parse_judge_json, apply_thresholds
report = parse_judge_json(judge_output_text)
verdict = apply_thresholds(report)
```

Conséquences :

- `verdict='killed'` → **n'écris pas**. Montre les issues (factual / tone /
  legal défaillant) et propose une reformulation ciblée.
- `verdict='queued'` → écris avec `status: queued` et liste les issues
  dans le frontmatter (`judge_issues:`). Le post existe mais demande une
  correction humaine avant validation.
- `verdict='auto_send'` → écris avec `status: draft` (l'humain valide
  encore visuellement avant posting).

Dans **tous** les cas, écris `judge_score`, `judge_verdict`,
`judge_rationale` dans le frontmatter — traçabilité pour l'audit ultérieur.

### 4. Validation finale + écriture

- Affiche le post complet en preview avec **character_count** et le
  **(judge_score / verdict)**.
- Refuse d'écrire si > 300 graphemes ou si `verdict='killed'`.
- Demande : « OK pour écrire dans `data/content/drafts/<filename>.md` ? »
- Si oui, écris avec le tool `Write`.

### 5. Rappel posting (jusqu'au live ContentBot)

Le connecteur `argos_ops/social/bluesky.py` reste en **shadow** tant que
`BLUESKY_HANDLE` + `BLUESKY_APP_PASSWORD` ne sont pas dans `.env.local`
(cf. bsky.app → Settings → App Passwords). En attendant, deux options :

- **Manuel** : copier-coller le body dans https://bsky.app, puis éditer le
  frontmatter : `status: posted` + `posted_at:` + `url_posted:`.
- **Semi-auto (test)** : `uv run python scripts/test_bluesky.py --message "<body>"`
  une fois les credentials remplis — poste en live et renvoie l'URL.

**Publication auto (ContentBot full)** : le publisher
(`find_ready_drafts`) ne ramasse un draft que s'il a `status: validated`
**ET** un `scheduled_for` (ISO8601) ≤ maintenant. Deux nuances Bluesky
aujourd'hui :

- Le canal `bluesky` est déjà câblé dans
  `argos_ops/social/publisher.py` — dès que le draft a ces deux champs et
  que les credentials sont remplis, il part en live.
- Le skill `content-scheduler` (qui pose `scheduled_for`) **ne couvre pas
  encore Bluesky** (fenêtres d'engagement définies pour LinkedIn/Mastodon/X
  seulement). En attendant, soit poser `scheduled_for` à la main, soit
  rester en **posting manuel** (le chemin `status: posted` ci-dessus, qui
  marche dès maintenant).

## Anti-patterns à refuser

L'audience Bluesky est tech et allergique au marketing creux. Refuse et
reformule si tu te surprends à produire :

- **Génération sans KB** — risque ton générique IA. Charge la KB d'abord.
- **Stats inventées** — « 87 % des RSSI… » sans source réelle = retirer ou
  demander la source. Sur un réseau d'experts, une stat bidon est repérée
  et coûte la crédibilité.
- **FUD vs concurrents** — respect strict de `competitor_compare.md`
  § anti-disparagement. Pas de « contrairement à [concurrent] qui rate… ».
- **Buzzwords corporate** — « game changer », « disruptif », « révolution-
  naire », « synergie » → reformuler en concret.
- **Hook mou** — « Petit thread sur la sécurité 🧵 » ne donne envie de rien.
  Le hook doit livrer une idée, pas annoncer qu'on va parler.
- **Sur-tagging** — 4+ hashtags = spam. 1-3 ciblés.
- **Cascade d'emoji** — 🚀🔥💯. Bannir.
- **Dépassement 300 graphemes** — ne pas tronquer brutalement à la fin ;
  réécrire plus court en gardant l'idée.

## Critères qualité (checklist avant écriture)

- ✅ Frontmatter YAML valide et complet (dont `judge_*`)
- ✅ `character_count` ≤ 300
- ✅ ≥ 1 `kb_sources` (preuve que la KB a été consultée)
- ✅ Hook tient seul sur la 1re ligne
- ✅ 1 à 3 hashtags, dont `#infosec` ou `#cyber`
- ✅ Zéro buzzword corporate, zéro stat sans source, zéro FUD
- ✅ Verdict claude-judge ≠ `killed`

## Liens

- Slash command : [`/draft-bluesky`](../../commands/draft-bluesky.md)
- Connecteur live : [`argos_ops/social/bluesky.py`](../../../argos_ops/social/bluesky.py)
- Setup credentials : bsky.app → Settings → App Passwords (app password, jamais le mdp du compte)
- Drafts produits : `data/content/drafts/`
- Skills réutilisés : `kb-rag` (P6), `claude-judge` (P14)
- Skills cousins (autres canaux) : `linkedin-writer`, `mastodon-writer`,
  `seo-brief-writer` (blog longform)
