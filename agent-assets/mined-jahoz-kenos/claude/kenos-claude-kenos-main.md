# CLAUDE.md — kenos

## Project Overview

**KENOS** — App Flutter iOS/Android (du grec *kénose* : se vider de soi-même).
L'anti-réseau social : un sanctuaire numérique de décharge cognitive où l'on
lance des pensées intimes anonymes dans un « éther » cosmique. **Un écho ne
peut être lu qu'une seule fois, par une seule personne** — puis il s'autodétruit
(burn after reading).

- Zéro validation : pas de profil, pas de likes, pas de commentaires, pas de feed.
- Friction as a feature : lire exige un appui long de 3 s (*Mindful Hold*)
  — et **d'être à portée de l'œil** (champ de réception, V3.12 : au-delà,
  l'étoile n'est qu'un scintillement et le hold ne s'arme pas).
- Éphémère absolu : 10 s de fenêtre de lecture, puis dissolution.
- Sans identifiants Supabase, l'app démarre en **MODE DÉMO LOCAL** (éther simulé,
  sémantique identique — atomicité comprise).

## Lexique du ciel (canon — ne jamais confondre)

Chaque session relit ceci avant de parler du ciel. « Artefact » n'est pas un
mot générique ici : il désigne une chose précise, distincte du vestige.

| Terme | Qu'est-ce | Vie |
|---|---|---|
| **Écho** | Confidence scellée (AES-256-GCM), lue une seule fois au monde, puis dissolution. | ≤ 30 j à la dérive |
| **Anneau** (constellation ouverte) | Cadavre exquis en formation : lignes scellées à l'aveugle, rien de lisible tant qu'il est ouvert. Le Jardinier (`pg_cron kenos-garden`) en replante. | 7 j si jamais refermé |
| **Artefact** (constellation fermée curatorisée) | **Un poème du domaine public, crédité** (`curated_by` = le poète), assemblé ligne par ligne par des mains anonymes ; lisible et re-lisible par tous. | **Une lune** — purge à 30 j. Un naît chaque lundi (`pg_cron kenos-artifact` → backlog `kenos_artifact_backlog`) |
| **Vestige** | **Un éclat de culture permanente** : citation, étymologie, histoire, fait, haïku — texte clair, aucune identité de compte, aucune réception (une source créditée, pas un auteur) ; multilingue (fr canon + locales). | **Pour toujours** — jamais purgé (`kenos_vestiges`) |
| **Main** | Compte anonyme déterministe (`curated-hand-N@seed.kenos.local`) portant une ligne curatorisée. | — |
| **Ancre** | Mémo LOCAL d'une porte de salon tenue (clé en secure_storage, zéro contenu — jamais une ligne) ; graine ember sur la carte, visible du porteur seul. | 7 j (le fauchage) ou la fermeture de l'anneau |
| **Braise** | Lien de passage d'un corps anonyme à un autre (`/#/pass/<clé>.<ballot scellé>`) : la clé (16 o hex) frappe `claim_passage`, le ballot (souvenirs locaux, AES-GCM sous HKDF de la clé) ne quitte jamais le fragment. Forge sur l'ancien appareil (Impact, discrète), claim une seule fois, remap serveur atomique. | 10 min (le lien) — le corps éteint l'est pour toujours |
| **Trace** | Réponse one-shot du lecteur à l'auteur (≤ 140 car., fenêtre 10 min), bouteille à la mer. | voir = brûler |

Règle rapide : **un artefact est un poème et vit une lune ; un vestige est un
éclat et vit pour toujours.** Le commentaire historique de
`curate_vestiges.sql` (« a Vestige is an artefact ») entretenait la confusion —
corrigé ; ne jamais le réécrire.

## Stack

| Couche | Tech |
|--------|------|
| Framework | Flutter 3.41+ / Dart 3.11+ |
| State | Riverpod (`flutter_riverpod` 2.x, AsyncNotifier) |
| Routing | GoRouter (tout en fondu) |
| Backend | Supabase (auth anonyme + RPC PostgreSQL atomiques) |
| Capteurs | `sensors_plus` (accéléromètre → parallaxe, passe-bas α=0.08) |
| Audio | `just_audio` (drone 70 Hz bouclé + cloches pentatoniques, pitch couplé au hold) |
| Crypto | `cryptography` (AES-256-GCM, clé éphémère 256 bits par écho) |
| Stockage local | `flutter_secure_storage` (échos scellés SANS texte, timeout d'E/S) |

## Architecture

```
lib/
├── app/               # KenosApp, routeur go_router (fades uniquement)
├── core/
│   ├── constants/     # Void Black, typographies (Playfair/Space Mono), durées
│   ├── theme/         # Thème dark strict, aucun fioriture Material
│   ├── utils/         # ParallaxMath, LowPassFilter
│   ├── audio/         # AudioController : drone + cloches
│   └── widgets/       # ScrambleText (security theater)
└── features/
    ├── onboarding/      # Le seuil : trois règles, une porte
    ├── echo/            # domain (Echo, EchoExcerpt, cipher) + data (repo, store)
    ├── cosmic_map/      # application (MapController, caméra de voyage) + presentation
    ├── create_echo/     # Le Miroir : formulation, fragments, portes culturelles
    ├── constellations/  # Cadavre exquis : lignes à l'aveugle, figure angle d'or
    ├── frequencies/     # Symphonie spatialisée (oscillateurs + repli assets)
    └── observatory/     # L'Observatoire (V3.16/V3.56) : seuil du gardien, formes sans contenu
```

## Commands

```bash
make dev                   # Mode démo local (aucun backend requis)
make dev-local             # PWA release sur l'éther local seedé (:4308) — JAMAIS juger la perf sur `flutter run` (debug, 5-20× plus lent)
make analyze               # 0 issue
make test                  # 447 tests (chiffrement, culling, contrôleurs, UI)
make db-reset && make db-test  # Migrations + 305 invariants pgTAP
make db-seed-load && make db-load-report  # Montée en charge : seed 30 j (scellés LISIBLES, ~12k lignes) + rapport
make db-verify-load           # Preuve e2e : consommer un écho seedé, l'ouvrir sur l'appareil
make db-wipe-load              # Reset clean du seed (data réelle + KEK intacts)
make db-garden                 # Jardiner : plante des anneaux ouverts (jamais de lignes)
make db-curate                 # Curater : artefacts poésie domaine public + vestiges, crédités
make db-sow-vestiges SOW_ARGS="--count 20"  # IA : semer des éclats vérifiés (2 passes) — clé gratuite Google AI Studio (https://aistudio.google.com/apikey)
make prod-reset            # LAUNCH RESET (cloud) : efface le vécu de test, garde le généré (artefacts curatorisés + vestiges + KEK), le Jardiner replante 14 anneaux
make prod-sow              # Sème le ciel cloud : 360 échos dérivants scellés RÉELS (refuse les payloads absents — jamais d'étoile morte en prod)
make e2e                   # Boucle réelle sur PostgREST local
make deploy-web            # App PWA → kenos-lemon.vercel.app (build .env.cloud + Vercel CLI, gates intégrés)
make deploy-site           # Landing → kenos-site.vercel.app (Vercel séparé, SANS lien git ; épingle l'alias — jamais de déploiement par push)
python3 tool/gen_audio.py  # Régénère les assets audio (std-lib only)
python3 tool/gen_icons.py  # Régénère les icônes Web/Android/iOS (std-lib only)
```

**Déploiements Vercel = CLI uniquement, jamais par push.** Les deux projets
(`kenos`, `kenos-site`) ont chacun été reliés au repo GitHub par erreur : chaque
push sur `main` construisait alors la racine du repo (static vide) en production
et écrasait le déploiement CLI d'un 404. Le `vercel.json` à la racine pose
`git.deploymentEnabled: false` : tout projet lié à ce repo ignore les pushes,
lien présent ou non. Ne pas le supprimer, ne jamais `vercel git connect`.

Canaux de test (registry `../LOCAL_DEV_PORTS.json`) :

```bash
flutter build web --release && (cd build/web && python3 -m http.server 4308)  # PWA :4308
(cd site && python3 -m http.server 4307)                                      # Site :4307
flutter emulators --launch Medium_Phone_API_36.1 && flutter run -d emulator-5554  # Android
```

> iOS : Xcode présent mais **aucun runtime simulateur installé** — télécharger via
> Xcode → Settings → Platforms avant `flutter run -d <sim>`.
> Android : si Gradle réclame `android-37` alors que `platforms/android-37.0` existe,
> créer le symlink `android-37 → android-37.0` (fait une fois sur ce poste).

Backend réel :

```bash
flutter run \
  --dart-define=SUPABASE_URL=https://xxxx.supabase.co \
  --dart-define=SUPABASE_ANON_KEY=eyJ...
```

Après avoir exécuté `supabase/migrations/0001_kenos_init.sql` dans le SQL Editor.

## Security Model (non-negotiable)

- Le client ne touche JAMAIS la table `echoes` : carte → RPC
  `fetch_map_sector` (métadonnées, culling 8×8), lecture → RPC
  `consume_echo` (atomique `FOR UPDATE SKIP LOCKED`), envoi → RPC
  `launch_echo` (validation + anti-spam).
- **Ether Seal** : le texte est chiffré sur l'appareil (AES-256-GCM,
  clé éphémère par écho) ; la clé est escrowée scellée sous une KEK
  (Vault) et échangée une seule fois, à l'interception, dans la
  transaction atomique. `encrypted_text` et `key_seal` ne fuittent
  jamais côté client. Prix assumé : la validation de longueur du
  plaintext est côté client (le serveur borne le scellé à 4000).
- Ne jamais exposer `encrypted_text` ni `key_seal` côté client avant
  consommation.
- L'écho envoyé est stocké localement SANS son texte : même l'auteur ne relit plus.
- Cicatrices de lecture : chaque écho consumé laisse une marque locale
  sans contenu (position seule, cap 80, fondu 30 j) — jamais de réseau ;
  les scellées se lisent comme des anneaux creux, l'éther comme des lumières pleines.
- **Traces de réception** (bouteille à la mer) : `kenos_receptions` est sans
  contenu par défaut ; la trace du lecteur est one-shot (≤ 140 caractères,
  fenêtre de 10 min après lecture, jamais éditable) ; l'auteur la voit une
  seule fois (voir = brûler). Aucun identité, aucun fil, jamais de réponse.
- ROSE (`#F43F5E`/`#FB7185`) est réservé à la destruction, jamais sélectionnable.
- **Purge** : `kenos_purge()` (échos > 30 j, audit > 1 j, réceptions non
  lues > 30 j) — câblage `pg_cron` fourni commenté dans la migration 0004.
- **Constellations (cadavre exquis)** : lignes scellées sur l'appareil.
  V3.13 (règle classique, arbitrage Hugo 2026-09-03) : `peek_previous_line`
  montre la ligne qui précède (une seule, scellée, ouverte sur l'appareil),
  `contribute_line` renvoie compte + précédente (bundle ciphertext + clé),
  `read_constellation` = le poème REFERMÉ est un artefact — lisible par
  tous (contributeurs inclus), re-lisible, jamais consommé ;
  `consume_constellation` reste en alias (les clients déployés guérissent).
  Purge : OPEN > 7 j, CLOSED > 30 j (l'artefact vit une lune).
- **Constellations-chansons (V3.14)** : un cadavre est POÈME ou
  CHANSON au largage (`kind`, jamais mélangé). Une ligne de chanson
  = une phrase de ≤ 8 indices de la gamme pentatonique, scellée en
  JSON — zéro octet audio dans l'éther, anonyme par construction
  (la voix est arbitré HORS pour l'instant : une voix est une
  empreinte). Le compositeur ÉCOUTE la phrase précédente (synthèse
  sur l'appareil), la chanson refermée se traverse : lecture
  séquentielle, chaque phrase spatialisée à sa station d'angle d'or
  (flutter_soloud, repli assets cuits).
- **Le Salon (V3.19)** : une constellation peut naître invitable —
  un lien unique `/#/c/<clé>` est la porte, porté par le semeur à qui
  il choisit. La clé (16 octets hex) n'est rendue qu'au semeur ; la
  base ne garde que son empreinte sha256 (`invite_token_hash` — un
  dump ne tient aucune porte). Le claim EST la contribution : la clé
  se vérifie dans la transaction `contribute_line` /
  `peek_previous_line` (`KENOS_INVITE_UNKNOWN` — absent et faux se
  ressemblent). Salon ouvert invisible sur la carte ; refermé,
  l'artefact est public et indiscernable. La purge est inchangée —
  le lien meurt avec l'anneau.
- **L'Ancre du salon (V3.31)** : le porteur d'une porte (semeur dès
  le semage, invité dès sa première ligne) garde une ancre locale —
  clé en `secure_storage`, AUCUN contenu, graine ember visible de
  lui seul, auto-taillée à 7 jours ou à la fermeture. Le lien reste
  montré une seule fois ; l'ancre ne rouvre jamais le partage, juste
  la porte.
- **La Braise (V3.60)** : changer d'appareil sans créer de compte.
  Sur l'ancien corps, une ligne discrète au bas de l'Impact forge un
  lien unique `/#/pass/<clé>.<ballot>` — grammaire salon : 16 octets
  hex, la base ne garde que sha256 et seulement 10 minutes, la clé
  traverse le fil une seule fois. Le ballot (onboarding, stats,
  guides, ancres vivantes — JAMAIS les cicatrices ni les échos
  envoyés) voyage chiffré AES-256-GCM sous HKDF de la clé de passage,
  dans le fragment `#` : le serveur n'en voit pas un octet. Le claim
  EST le remap : une transaction `FOR UPDATE SKIP LOCKED` re-adresse
  réceptions, échos en dérive, anneaux semés, lignes et signalements
  au nouveau corps (collisions : la ligne reste à l'ancien — un
  stranger, une ligne), consomme le passage (zéro trace), et éteint
  l'ancien corps (`kenos_passed`, à vie) : `launch_echo` y répond
  `KENOS_BRAISE_PASSED`. Pas d'email, pas de pseudonyme, pas de
  récupération — l'ancien appareil mort emporte sa braise (assumé).
  - **V3.60a** : l'extinction locale ROSE — forger depuis un corps
    éteint propose « ÉTEINDRE CE CORPS » (le seul geste destructeur
    local) : tout le vécu de l'appareil s'efface, le Seuil attend un
    renaissant.
  - **V3.60b** : la pastille QR — le lien de passe vit aussi en QR
    scannable sur la feuille de forge (contraste standard, caméra du
    device neuf ; au-delà du plafond QR, le texte reste la voie).
  - **V3.60c** : le census gardien — `braises_passed` (compté dans la
    transaction du claim) et `braises_pending` (empreintes vivantes)
    rejoignent le registre contentless de l'Observatoire.
- **Vestiges multilingues (V3.16)** : la voix produit reste FR (canon,
  pour toujours) ; les éclats curatés existent par locale
  (fetch_vestiges(p_locale), normalisation `fr-FR`→`fr`, repli honnête
  sur le canon FR). **Loi du produit : le contenu utilisateur n'est
  JAMAIS traduit** — scellé, il traverse les frontières dans sa
  langue d'origine. Traducteur : tool/translate_vestiges.dart (Mistral,
  voix kenos, passe vérif, staging humain).
- **La voix du premier pas (V3.52)** : le français est CANONIQUE —
  partout, pour tous. Le build WEB sert l'anglais au premier parcours
  (Seuil, deux portes, Miroir, révélation, panneau d'artefact) quand
  la plateforme du voyageur parle anglais (`KenosVoice`, `pick(fr, en)`
  au site d'appel) ; le natif reste FR, tout le reste du produit
  reste FR. La loi tient : la voix habille les portes, JAMAIS les
  confidences — le contenu utilisateur n'est pas traduit.
- **La garde douce (V3.88, remplace le bouclier V3.15)** : le soin
  vit SUR L'APPAREIL, zéro réseau — `CareGuard` (core, lexique
  FR/EN, accents pliés) lit ce que l'appareil lit déjà en clair,
  avant le scellement : Miroir, ligne de poème, trace, et en portes
  passives après déchiffrement (révélation = lecteur, réception =
  auteur). Le moment de soin (`offerCareMoment`) nomme les PORTES
  par thème (3114/15, 3919, SOS Viols, 119), ne cite JAMAIS les
  mots de l'auteur, ne bloque JAMAIS — une offre, pas un jugement,
  proposée une fois par secret. L'anonymat garde son regex device
  (`PiiGuard`), partout. Aucune dépendance à un API : la care d'un
  quota est une care qui échoue en silence — interdit.
- **La garde de la trace (V3.88)** : la trace reste la SEULE
  contenu clair vu par l'éther — et la seule surface où
  l'application de la loi est possible sans trahir le scellé. Au
  dépôt, un trigger pg_net (`kenos_trace_guard_notify`, configuré
  via `kenos_config`) la remet à l'Edge Function `trace-guard`
  sous la seconde : Llama Guard 4 (Groq, free tier, fail-open par
  contrat) ne lit QUE le plancher illicite — mineurs (S3B1),
  non-consenti (S3B2), enfance en danger (S4) — et pour ceux-là
  seulement, `admin_burn_reception` (service-role only) efface le
  `reply_text` avant que l'auteur ne le voie. Tout le reste —
  douleur, violence vécue, désespoir — reste : la douleur n'est
  pas un délit, et la censure n'est pas du soin. Le contenu scellé
  reste structurellement invisible, pour toujours. Les pages
  légales (mentions, données, modération, Pharos) vivent sur le
  site : `site/mentions.html`.
- **Le pacte de l'Aube (V3.89)** : on ne rentre qu'accordé. Le SAS
  d'entrée porte les termes de l'éther (anonymat, lecture unique,
  clair gardé / douleur libre, lignes d'écoute, douceur) — texte
  intégral, défilable, jamais tronqué, voix FR/EN (`KenosVoice`) ;
  UNE acceptation délibérée (`J'ACCEPTE — JE RENTRE`), barrière non
  fermable tant que le pacte attend. Mémorisé PAR VERSION
  (`kAubePactVersion` dans `app_meta.dart` — bump = re-demander une
  fois à tous) ; la Braise emporte le pacte (un corps re-né
  re-signe) ; sans pacte en attente, l'Aube retrouve son comportement
  d'avant (nouvelles seulement, toucher le vide).
- **Extraits culturels (V3.10)** : la référence Spotify/YouTube voyage
  scellée sous la clé de l'écho (le serveur borne le scellé 32-512,
  ne voit jamais l'ID) ; l'URL lancée est TOUJOURS reconstruite
  canoniquement depuis un parse strict — jamais la chaîne brute.
  `door-preview` (Edge Function) ne connaît que l'ID de piste nu,
  jamais l'écho ni le texte.
- **La garde des artefacts (V3.51)** : un artefact refermé est public
  30 jours — le seul contenu utilisateur lisible en clair par tous.
  `report_constellation` (contentless, un par main, CLOSED seulement,
  cap 10/jour) ; `admin_list_constellation_reports` ne rend que des
  métadonnées (comptes, motifs, âge, graine pour le lien ciel —
  jamais un texte, épinglé en pgTAP) ; `admin_retract_constellation`
  est le seul geste de modération — jamais automatique, aucun seuil :
  le retrait est une mort honnête (cascade lignes + signalements,
  comme le faucheur).
- **Observatoire (V3.16, V3.56)** : le dashboard gardien est CONTENTLESS
  par construction — `kenos_metrics_daily` ne stocke que des compteurs,
  bumpés dans la transaction des RPC de cycle de vie (aucune nouvelle
  lecture, l'atomicité sacrée est intacte). Le RPC `admin_fetch_metrics`
  ne rend que des agrégats (série, live, heatmap 8×8, dérivés, census
  V3.56 : âges/genres/teintes de la dérive) ; le
  gate lit `app_metadata` UNIQUEMENT (`user_metadata` est falsifiable,
  épinglé refusé en pgTAP) ; la session gardien vit sur un second
  client Supabase (la session anonyme céleste n'est jamais touchée) et
  ne persiste nulle part. V3.56 : fenêtre 7/30/90, quatre souffles sur
  le spectre, lune contre lune, archive CSV du registre — le
  rafraîchissement reste manuel. Compte-rendu opérateur :
  `supabase/snippets/create_guardian.sql`.

## Design Boundary

Identité « Cosmic Zen / Dark Introspection » — voir
`../portfolio-os/PROJECT_DESIGN_REGISTRY.md` (entrée `kenos`).
ABSOLU : ne jamais importer de design d'un autre projet.
