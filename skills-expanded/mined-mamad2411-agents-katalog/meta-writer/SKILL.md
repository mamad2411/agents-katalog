---
name: meta-writer
description: Drafte un post Facebook Page Argos (court, ~300-500 chars) pour un public TPE/PME NON-TECHNIQUE (le patron « Patrick » qui a peur du hack mais n'y connaît rien). Ton simple, chaleureux, rassurant, ZÉRO jargon (pas de DAST/OWASP/CVE/pentest), métaphores grand public, CTA offre entry-level (Free / Pro 39€). Anti-FUD STRICT (jamais « votre site va se faire pirater »). Mode local-draft : draft dans data/content/drafts/, posting via argos_ops/social/meta.py (shadow tant que META_PAGE_* absent). Utilise ce skill quand le user demande de drafter un post Facebook / Meta / pour la Page FB, du contenu grand public TPE/PME, ou pendant /draft-meta. Charge la KB (kb-rag) pour les FAITS puis traduit en grand public.
---

# meta-writer

Skill éditorial dédié au **post Facebook Page** Argos. C'est le **mouton
noir** des writers Argos : tous les autres (LinkedIn, Mastodon, Bluesky, X)
parlent à des gens **cyber-savvy** (Marc le CTO, Sarah la RSSI, Thomas le
pentester). **Facebook, non.** Facebook, c'est là où traînent les **petits
patrons de TPE/PME** qui ne connaissent rien à la sécu mais qui ont une
boule au ventre à l'idée que leur site se fasse pirater.

On élargit l'audience par **le bas du funnel** : on parle à des gens qui ne
liront jamais un thread infosec, mais qui peuvent cliquer sur « tester mon
site gratuitement ».

> **Pourquoi un skill dédié** : la persona Facebook est si différente que
> réutiliser le ton des autres writers serait un contresens total. Un post
> Mastodon technique ferait fuir Patrick ; un post Facebook jargonneux le
> perdrait à la 2e ligne.

## La persona : « Patrick », patron de TPE/PME

ICP.md ne le décrit pas encore (4e persona à ajouter). En attendant, garde
en tête :

- **Qui** : patron / gérant d'une boîte de 10-50 personnes (artisan + e-shop,
  agence, cabinet, resto avec réservation en ligne, PME industrielle…).
- **Niveau cyber** : ~0. Il sait allumer un ordi, pas ce qu'est une « faille ».
- **Sa peur** : « j'ai un site / une boutique en ligne, j'ai entendu parler
  de boîtes qui se font pirater, je sais même pas si je suis protégé ».
- **Pas de DSI, pas de budget IT**, souvent un prestataire web externe qui a
  fait le site il y a 3 ans et qu'il ne rappelle jamais.
- **Ce qui le fait cliquer** : la simplicité et la **réassurance**. « Je peux
  lancer une vérification en quelques minutes », « sans rien installer »,
  « gratuit pour commencer ».

## Les 5 règles d'or (lis-les avant d'écrire)

### 1. Anti-FUD STRICT — c'est LA règle

La peur est l'émotion la plus facile à activer chez Patrick… et c'est
**exactement** pour ça qu'on ne le fait pas. Jouer sur la peur d'un public
vulnérable et non-averti, c'est contraire à la charte brand Argos **et**
ça nous range avec les vendeurs d'antivirus anxiogènes. On **reconnaît**
l'inquiétude, puis on **rassure tout de suite** — on ne l'amplifie jamais.

| ❌ FUD (interdit) | ✅ Réassurance (le bon registre) |
|---|---|
| « Votre site va se faire pirater. » | « Savez-vous si votre site est bien protégé ? On peut lancer une vérification simplement, sans être expert. » |
| « 60 % des PME piratées ferment dans l'année. » | « Vérifier la sécurité de son site, c'est devenu aussi simple que de checker ses mails. » |
| « Vos données clients sont en danger. » | « Protéger les données de vos clients, ça commence par un petit check régulier. » |

Le hook peut nommer **doucement** la préoccupation (« On se demande tous si
notre site est bien protégé »), jamais la dramatiser.

### 2. ZÉRO jargon

Patrick décroche au premier mot technique. **Bannis** : DAST, SAST, OWASP,
CVE, pentest, payload, injection SQL, XSS, scan, vulnérabilité (dis
« faille » ou « problème »), endpoint, CI/CD…

Utilise des **métaphores du quotidien** :
- « comme une alarme pour votre maison, mais pour votre site web »
- « un petit contrôle technique, comme pour la voiture »
- « ça regarde si une porte est restée ouverte sur votre site »

### 3. Ton simple, chaleureux, conversationnel

On parle à un humain inquiet, pas à un acheteur B2B. Phrases courtes,
tutoiement OU vouvoiement chaleureux (cohérent dans le post), **une
question** souvent (Facebook récompense les commentaires).

### 4. CTA = l'offre d'entrée, jamais l'enterprise

Patrick n'achètera jamais « Pro Max 249 €/mois ». Son entrée, c'est
**Free** (tester sans carte bleue) ou **Pro 39 €/mois**. Le CTA est doux :
« Testez gratuitement », « Voyez où vous en êtes », lien vers `omnividens.fr`.

> Note prod : une page d'atterrissage simplifiée « Argos pour TPE » n'existe
> peut-être pas encore. En attendant, pointer vers `omnividens.fr` (ou la
> page la plus simple). Si tu le remarques, signale-le au fondateur.

### 5. Pas de comparaison concurrent

Patrick ne connaît ni Acunetix ni Detectify. Toute comparaison technique
est hors-sujet (et `competitor_compare.md` § anti-disparagement s'applique
de toute façon). On parle de **son** problème, pas du marché.

## Contraintes de format (Facebook organique)

| Dimension | Règle | Pourquoi |
|-----------|-------|----------|
| **Longueur** | court : **~300-500 chars**, 1-3 phrases | Facebook tronque et l'audience scrolle vite ; un pavé ne sera pas lu. |
| **Hook** | 1re phrase = la préoccupation nommée en douceur OU une question | C'est ce qui arrête le scroll. |
| **Question** | en inclure une souvent | L'algo FB pousse les posts qui génèrent des commentaires. |
| **Emoji** | 1-2 **grand public** OK (🔒 ✅ 👍), pas de cascade | Sur FB c'est naturel et chaleureux (≠ Mastodon). Pas 🚀🔥💯. |
| **Lien / CTA** | doux, en fin | Vers l'offre d'entrée. |
| **Hashtags** | 0-2 max, simples (#cybersécurité #TPE) | FB n'est pas un canal à hashtags ; ne pas surcharger. |

## Inputs

- `topic` — sujet (ex. `"vérifier si mon site est protégé"`, `"sauvegardes"`,
  `"mots de passe de l'équipe"`, `"site fait il y a 3 ans jamais mis à jour"`)
- `(optionnel) angle` — sinon, propose-en 2-3 (toujours côté réassurance).
- `(optionnel) cta` — par défaut « tester gratuitement » → `omnividens.fr`.

Si `topic` est trop technique pour la persona (« configurer un WAF »),
**reformule** en préoccupation Patrick (« est-ce que mon site est protégé
contre les attaques ») avant d'écrire.

## Output

Fichier `data/content/drafts/YYYY-MM-DD-meta-<slug>.md` (slug = kebab-case du
topic, ~50 chars ; date = TZ Paris) avec **exactement** ce frontmatter :

```markdown
---
channel: meta
status: draft            # draft | queued | validated | posted | rejected
date_created: YYYY-MM-DD
posted_at: null
topic: "<topic court>"
angle: "<angle retenu>"
character_count: <int — len(body), hors frontmatter>
kb_sources: ["pricing.md§Free/Pro", "faq.md§...", ...]
cta: "<url ou null>"
judge_score: <int 0-100>
judge_verdict: "<auto_send | queued | killed>"
judge_rationale: "<une phrase>"
judge_issues: []         # rempli UNIQUEMENT si verdict=queued
scheduled_for: null      # requis (ISO8601) pour la publi auto ; null = posting manuel
url_posted: null         # rempli après posting (manuel ou ContentBot)
---

<body du post, prêt à copier-coller dans Facebook>
```

## Procédure (humain-in-the-loop)

### 1. Charge la KB pour les FAITS — puis traduis

Invoque **`kb-rag`** avec `topic` (top-5). Charge surtout :

- `data/knowledge_base/pricing.md` — pour citer **juste** le tier d'entrée
  (Free / Pro 39€), jamais les tiers enterprise.
- `data/knowledge_base/faq.md` — les vraies questions clients.
- `data/knowledge_base/argos_features.md` — ce qu'Argos fait **vraiment**
  (pour ne rien inventer)… mais **traduis** : ne copie jamais une phrase
  technique de la KB telle quelle. La KB est écrite pour Marc/Sarah ; toi tu
  parles à Patrick.

> N'invente aucune capacité produit. Si un bénéfice n'est pas dans la KB,
> ne le promets pas — reformule en bénéfice prudent et vrai.
>
> **Piège fréquent — temps chiffré** : la KB dit « signup < 5 min » (la
> rapidité de **démarrage**), PAS « résultat en 5 min » (un scan dure
> 2-45 min selon la cible, cf. `faq.md`). Ne promets jamais un **temps de
> résultat** chiffré (« savoir si protégé en 5 min »). Reste sur « lancer
> une vérification en quelques minutes » / « simplement ».

### 2. Drafting interactif

Propose puis fais valider :

1. **Angle** — 2-3 options, **toutes côté réassurance** (« angle A : le
   contrôle simple, sans être expert », « angle B : protéger les données de
   ses clients »).
2. **Hook** — préoccupation nommée en douceur, ou question. Jamais dramatisé.
3. **Corps** — 1-3 phrases simples, une métaphore si utile.
4. **CTA** — doux, vers l'offre d'entrée.
5. **Emoji / hashtag** — 1-2 grand public max.

Recompte les chars (cible 300-500). Trop long → raccourcir.

### 3. Audit agent-juge (claude-judge) — AVANT écriture

Invoque **`claude-judge`** : `draft=body` + `original_query=topic` +
`rag_chunks` (étape 1) + `channel='social_meta'` + `agent_name='ContentBot'`.

```python
from argos_ops.judge import parse_judge_json, apply_thresholds
report = parse_judge_json(judge_output_text)
verdict = apply_thresholds(report)
```

- `verdict='killed'` → **n'écris pas**. Le plus probable ici : axe **tone**
  (FUD détecté) ou **factual** (capacité inventée). Reformule côté
  réassurance / fais coller à la KB.
- `verdict='queued'` → écris avec `status: queued` + `judge_issues:`.
- `verdict='auto_send'` → écris avec `status: draft`.

Toujours écrire `judge_score`, `judge_verdict`, `judge_rationale`.

### 4. Validation finale + écriture

- Preview + **character_count** + **(judge_score / verdict)**.
- Refuse d'écrire si > 500 chars ou `verdict='killed'`.
- Demande confirmation, puis écris avec `Write`.

### 5. Posting (jusqu'au ContentBot full)

Le connecteur `argos_ops/social/meta.py` poste sur la Page via la Graph API
dès que `META_PAGE_ID` + `META_PAGE_ACCESS_TOKEN` sont remplis
(token de Page via Meta Business Suite, scope `pages_manage_posts`). En
**shadow** sinon (draft-only).

- **Manuel** : copier-coller dans la Page Facebook, puis maj frontmatter
  (`status: posted` + `posted_at:` + `url_posted:`).
- **Auto** : le publisher ramasse `status: validated` + `scheduled_for`.

## Anti-patterns à refuser

- **FUD / peur amplifiée** — le pire ici. Reformule côté réassurance.
- **Jargon** — un seul mot technique et Patrick décroche.
- **Stats anxiogènes inventées** — « X % des PME piratées… » : retirer.
- **CTA enterprise** — Pro Max / Custom n'ont rien à faire ici.
- **Capacité produit inventée** — coller à la KB, traduit mais vrai.
- **Pavé** — > 500 chars, 5 paragraphes : personne ne lit.
- **Cascade d'emoji** — 1-2 max, grand public.

## Critères qualité (checklist avant écriture)

- ✅ Frontmatter YAML valide et complet (dont `judge_*`)
- ✅ `character_count` ≤ ~500
- ✅ **Zéro jargon** (relis : aucun mot qu'un non-tech ne comprendrait)
- ✅ **Zéro FUD** (le post rassure, n'effraie pas)
- ✅ ≥ 1 `kb_sources` (les faits viennent de la KB, traduits)
- ✅ CTA = offre d'entrée (Free / Pro), pas enterprise
- ✅ Verdict claude-judge ≠ `killed`

## Liens

- Slash command : [`/draft-meta`](../../commands/draft-meta.md)
- Connecteur live : [`argos_ops/social/meta.py`](../../../argos_ops/social/meta.py)
- Setup credentials : Meta Business Suite (token de Page, scope `pages_manage_posts`)
- Persona (mémoire) : `project_metawriter_smb_persona`
- Skills réutilisés : `kb-rag` (P6), `claude-judge` (P14)
- Skills cousins (autres canaux, persona cyber-expert) : `linkedin-writer`,
  `mastodon-writer`, `bluesky-writer`
