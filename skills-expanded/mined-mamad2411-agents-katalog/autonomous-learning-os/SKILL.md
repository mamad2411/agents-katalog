---
name: autonomous-learning-os
description: Construit à l'utilisateur son propre dashboard d'apprentissage sur mesure — entretien de setup, deep research multi-agents sur son sujet, génération du curriculum, app Next.js au design BizOS, brief Telegram optionnel. À utiliser quand l'utilisateur veut apprendre un sujet sérieusement, se construire un cursus, ou lance ce repo.
---

# Autonomous Learning OS — skill de setup

Tu conduis l'utilisateur de « je veux apprendre X » à un dashboard d'apprentissage
qui tourne sur sa machine, rempli de sources réelles et vérifiées, en une seule
conversation.

**Ta contrainte absolue : à la fin, `npm run dev` doit afficher une app complète et
fonctionnelle, sans qu'il reste une seule étape manuelle non annoncée.** Pas de
placeholder, pas de « à toi de remplir », pas de curriculum d'exemple laissé en
place.

---

## Phase 0 — Repérage (avant de parler)

Fais ça en silence, avant la première question. Ça évite de demander ce que tu
peux voir.

```bash
bash scripts/00-detect-stack.sh
```

Le script écrit `.setup/stack.json` et affiche un résumé. Il détecte :

- les runtimes : `node`, `npm`, `python3`
- les CLIs de données : `supabase`, `railway`, `psql`, `neonctl` — **et si elles sont authentifiées**
- les CLIs de déploiement : `vercel`, `gh`
- les CLIs d'IA : `claude`, `codex`
- les variables d'environnement d'API déjà présentes dans le shell

Lis `.setup/stack.json` avant de poser la question 4 et la question 5. Si
l'utilisateur a déjà `supabase` connecté, tu proposes Supabase en premier choix,
pas en dernier.

---

## Phase 1 — L'entretien

Six questions. Pose-les **une par une**, attends la réponse, rebondis. Ce n'est
pas un formulaire : si une réponse est vague, creuse avant de passer à la suite.

Utilise l'outil de question à choix multiples quand les options sont fermées
(questions 4, 5, 6). Laisse la réponse libre pour 1, 2, 3.

### Q1 — Qu'est-ce que tu veux apprendre ?

Ouverte. Ce que tu veux en sortir :

- **Le sujet exact.** « L'IA » est trop large — tu veux savoir si c'est *entraîner
  des modèles*, *utiliser des LLM en produit*, ou *comprendre les fondations
  mathématiques*. Reformule et fais confirmer.
- **Mono-sujet ou cursus ?** Un sujet unique donne un curriculum profond. Plusieurs
  matières donnent un cursus large. **3 à 5 matières actives est ce qui tient le
  mieux dans la durée** (cf. `docs/LEARNING-SCIENCE.md`) — dis-le, puis
  **construis ce qu'il demande**. Il n'y a pas de plafond : c'est son temps.
- **Le format actuel.** Demande explicitement : *« Tu apprends comment aujourd'hui ?
  Vidéos, livres, cours en ligne, projets ? Qu'est-ce qui n'a pas marché ? »* Ça
  oriente la pondération vidéo / lecture / pratique de la recherche.

### Q2 — Où tu en es, et où tu veux aller ?

- Niveau de départ, en concret : ce qu'il sait déjà faire, pas un « intermédiaire ».
- **Le résultat visé doit être vérifiable.** « Comprendre la finance » ne l'est pas.
  « Lire un bilan et repérer trois signaux d'alerte » l'est. Reformule jusqu'à
  obtenir un critère observable — il devient l'objectif de sortie du curriculum.

### Q3 — Combien de temps par jour, sur combien de semaines ?

- Minutes par session : 15 / 30 / 45 / 60 / 90 / 120 / 180. L'app calibre la
  séquence dessus.
- Jours par semaine.
- Horizon en semaines → détermine le nombre de modules à générer
  (compte ~1 module par 2 sessions).

### Q4 — Comment on branche l'IA ?

Trois modes, décrits dans `docs/AI-PROVIDERS.md`. Propose-les dans cet ordre :

| Mode | `AI_PROVIDER` | Ce que ça veut dire |
|---|---|---|
| **Ton agent** *(recommandé)* | `claude-code` | Aucune clé. L'app prépare le prompt de correction, tu le colles à ton agent, il corrige. Zéro coût marginal. |
| **Ta CLI locale** | `cli` | L'app appelle `claude -p` ou `codex exec` sur ta machine. Détecté en phase 0. Zéro clé dans un fichier. |
| **Ta clé API** | `api` | Anthropic ou OpenAI, ta clé, ton compte. Elle va dans `app/.env.local`, qui est git-ignoré. |

**Ne propose jamais, et n'accepte jamais, une clé qui ne serait pas celle de
l'utilisateur.** Ce repo ne fournit aucune clé.

Si l'utilisateur choisit `api`, ne lui demande pas de te coller sa clé dans le
chat. Dis-lui de l'écrire lui-même dans `app/.env.local`, ou fais-le écrire par
une commande shell qu'il lance (le `!` prefix dans Claude Code).

### Q5 — Où stocker ta progression ?

Regarde `.setup/stack.json` avant de proposer.

| Option | Quand la proposer | Ce que fait l'agent |
|---|---|---|
| **Fichier local** *(défaut)* | Toujours disponible | Rien à faire. `app/.data/` est créé au premier écrit, git-ignoré. |
| **Supabase** | Si `supabase` est installé **et** authentifié | `bash scripts/03-database.sh supabase` : crée/lie le projet, applique le schéma, écrit `DATABASE_URL`. |
| **Railway** | Si `railway` est installé **et** authentifié | `bash scripts/03-database.sh railway` : provisionne Postgres, récupère l'URL, applique le schéma. |
| **Postgres existant** | Si l'utilisateur a déjà une URL | `bash scripts/03-database.sh url` puis colle l'URL. |

Le fichier local suffit pour un usage solo sur une machine. La DB sert dès qu'il
veut la progression sur plusieurs appareils ou un déploiement.

### Q6 — Tu veux un brief Telegram ?

Si oui : suis `docs/TELEGRAM.md` **avec lui**, pas à sa place. Il doit
créer son bot chez `@BotFather` (tu ne peux pas le faire), récupérer le token, lui
écrire un message, puis lancer `bash scripts/04-telegram.sh` qui résout le chat ID
et teste l'envoi.

Le message quotidien est **personnalisé sur son sujet** : le module du jour, la
source exacte à ouvrir, la durée, et la question de rappel. Le template est dans
`docs/TELEGRAM.md` — adapte-le à son domaine, ne renvoie pas un texte générique.

---

## Phase 2 — La deep research

C'est ce qui fait la valeur. **Ne la saute pas, ne la remplace pas par ce que tu
crois savoir.** Un curriculum écrit de mémoire contient des liens morts et des
cours qui n'existent plus.

Lis `research/PROMPTS.md` en entier, puis lance **quatre sous-agents en parallèle**
avec le contexte de l'entretien (sujet, niveau, objectif, temps) :

| Sous-agent | Mission | Modèle conseillé |
|---|---|---|
| `ACADEMIC` | Cours universitaires ouverts, manuels libres, papiers de référence, syllabi publics. | Sonnet 5 |
| `VIDEO` | Chaînes et playlists, **avec segments horodatés** et durée réelle. | Sonnet 5 |
| `PRACTITIONER` | Retours de terrain, études de cas, outils — étiquetés comme tels, jamais comme preuve académique. | Sonnet 5 |
| `SYLLABUS` | L'ordre des notions : prérequis, dépendances, progression. Ne cherche pas de liens, structure. | Opus / GPT-5.x |

Chaque sous-agent rend du JSON conforme à `research/curriculum.schema.json`.
Écris les rendus bruts dans `.setup/research/<agent>.json` — ils servent de trace
et permettent de relancer une seule branche si elle est faible.

### Les règles non négociables sur les sources

Elles sont dans `docs/SOURCE-POLICY.md`. Les trois qui font échouer une source :

1. **Elle doit être gratuitement accessible.** Pas de certificat payant obligatoire,
   pas de paywall. Note l'accès dans `accessNote`.
2. **Elle doit être vérifiée.** Tu ouvres le lien. Si tu ne peux pas confirmer qu'il
   répond, tu ne le mets pas. `verifiedAt` porte la date du jour.
3. **Elle doit porter une raison.** `why` explique pourquoi *cette* source pour
   *cette* notion, à *ce* niveau. « C'est un bon cours » n'est pas une raison.

Pour une vidéo, `segmentStartSeconds` et `minutes` définissent la capsule à
regarder. C'est le cœur du produit : l'utilisateur ne regarde jamais 90 minutes
par défaut, il regarde les 11 minutes qui portent la notion du jour.

### Fusion

Tu fusionnes les quatre rendus :

1. `SYLLABUS` donne l'ordre des modules.
2. `ACADEMIC` et `VIDEO` remplissent les sources de chaque module ; en cas de
   doublon, garde la plus institutionnelle et mets l'autre en `alternatives`.
3. `PRACTITIONER` alimente les exercices de transfert et les études de cas.
4. Écris `app/content/curriculum.json`.
5. **Valide :** `node scripts/validate-curriculum.mjs`. Corrige jusqu'au vert.

---

## Phase 3 — Le montage

```bash
bash scripts/01-scaffold.sh          # prépare app/, .env.local, .data/
cd app && npm install
```

Puis, selon les réponses :

```bash
bash scripts/02-configure.sh          # écrit AI_PROVIDER, APP_NAME, LEARNING_SUBJECT
bash scripts/03-database.sh <mode>    # seulement si Q5 ≠ fichier local
bash scripts/04-telegram.sh           # seulement si Q6 = oui
```

### Personnalisation visuelle

L'app porte l'UX BizOS V9 (`docs/DESIGN.md`) : wallpaper plein écran, panneaux
blancs à trait 1 px et ombre dure 5 px, Inria Serif, monochrome noir/blanc/gris.
**Ne le remplace pas, et n'y réintroduis aucune couleur d'accent.** Ce qui se
personnalise :

- Le wordmark reste `BizOS × Learning`, avec le sujet de l'utilisateur en
  sous-titre (`NEXT_PUBLIC_LEARNING_SUBJECT`).
- Le fond d'écran par défaut : `NEXT_PUBLIC_DEFAULT_WALLPAPER`. Les 12 fonds
  procéduraux livrés sont dans `app/src/lib/wallpapers.ts` — choisis-en un qui
  colle au domaine (`blueprint` pour l'ingénierie, `ledger` pour la finance,
  `synapse` pour les sciences cognitives…).
- Les icônes de matières dans `curriculum.json` (`icon`) — un glyphe simple,
  jamais un emoji couleur : la V9 est monochrome.

L'utilisateur peut changer de fond à tout moment depuis **Réglages → Apparence**,
et déposer les siens dans `app/public/wallpapers/`.

---

## Phase 4 — La vérification (obligatoire)

Tu ne déclares pas terminé sans avoir fait tourner ça :

```bash
bash scripts/05-verify.sh
```

Il enchaîne : validation du curriculum, `npm test`, `npm run build`, démarrage du
serveur, et un GET sur `/`, `/learning`, `/exercises`, `/reviews`, `/settings`.

Puis **ouvre réellement l'app** et regarde-la. Si tu as un outil de navigation,
charge `localhost:3000`, clique sur les cinq onglets, lance une vidéo, ouvre la
galerie de fonds. Un build qui passe n'est pas une preuve que l'écran est correct.

Enfin :

```bash
bash scripts/check-secrets.sh
```

Aucun secret ne doit être committable. Si le script sort en erreur, corrige avant
toute autre chose.

---

## Phase 5 — La remise

Dis à l'utilisateur, en clair et court :

1. **Ce qui tourne** — l'URL, les cinq écrans, le sujet, le nombre de modules.
2. **Ce que la recherche a trouvé** — combien de sources, de quelles institutions,
   et la plus forte selon toi.
3. **Ce qu'il fait maintenant** — sa première session, sa durée, la première source.
4. **Ce qui reste optionnel** — Telegram s'il a dit non, la DB s'il est en fichier,
   le déploiement Vercel.
5. **Comment ça se met à jour** — relancer la recherche pour le module suivant, ou
   éditer `curriculum.json` à la main.

Ne fais pas un rapport de 40 lignes. Il veut apprendre, pas lire ton compte rendu.

---

## Règles de conduite

- **Une question à la fois.** L'entretien est ce qui rend le curriculum juste.
- **Ne devine pas les sources.** Cherche, ouvre, vérifie. Un lien mort dans le
  livrable, c'est un échec.
- **Ne partage aucune clé, ne demande aucune clé qui ne soit pas la sienne.**
- **Ne laisse pas le curriculum d'exemple.** Si la recherche échoue, dis-le
  franchement et propose de relancer — ne livre pas l'exemple en prétendant que
  c'est sur mesure.
- **Le français est la langue par défaut** de l'interface et du curriculum, sauf
  demande contraire. Les titres de sources restent dans leur langue d'origine.
- **Le nombre de matières est SA décision.** Tu recommandes 3 à 5 actives, une
  fois, avec la raison. S'il en veut huit, tu construis les huit — proprement,
  sans y revenir et sans version dégradée. Un backlog est une option que tu
  proposes, jamais une limite que tu imposes.
