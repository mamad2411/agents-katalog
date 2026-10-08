---
name: cinematic-film
description: >
  Fabrique un court film animé cinématique (60–120 s, 16:9 ou 9:16) sur n'importe quel sujet — vulgarisation,
  voyage/descente/timeline (océan, espace, corps humain, histoire, montagne, ville, économie), storytelling
  narratif — avec Remotion + three.js : assets peints générés par gpt-image et découpés, personnage narrateur
  riggé dont la bouche suit la voix, voix off TTS française ou anglaise, musique et bruitages synthétisés libres
  de droits, caméra en plan-séquence continu, brouillard/lumière/particules réels, post-prod bloom + grain,
  HUD de données (compteur, relevés, règle, étiquettes ancrées). Utilise ce skill DÈS QUE l'utilisateur veut
  « une vidéo qualité », « un rendu wow », « pas un PowerPoint », « pas un collage », une vidéo YouTube/TikTok/X
  explicative avec des personnages qui bougent, un documentaire animé, des fun facts par niveau, un mini-film
  mystérieux/épique, ou parle de Remotion + gpt-image / TTS pour une vidéo — même sans dire « film ».
  Pour une démo produit SaaS avec captures d'écran réelles, préférer promo-video.
---

# cinematic-film — un vrai film animé, pas un diaporama

Le skill produit un MP4 1080p où tout bouge, respire et s'éclaire : un narrateur vivant, des créatures ou
personnages qui se déforment vraiment, des décors dans le brouillard, un HUD de données qui rend le
propos éducatif, un son qui monte en tension. Il a été construit en produisant « Abysses » (descente
0 → 10 935 m en 94 s, voir `references/example-abysses.md` et les deux planches PNG dans `references/`).
Le socle (`templates/base`) est générique : on change le sujet en éditant **trois choses** — le script
(`scripts/vo-script.json`), les assets (`scripts/assets.json` + `process.json`) et la mise en scène
(`src/film.config.ts`, `src/scene/Story.tsx`, `src/tags.ts`).

`<skill>` = le dossier de ce SKILL.md. Les scripts s'exécutent depuis la racine du projet vidéo.

## 0. Cadrer avec l'utilisateur, puis écrire le scénario (avant tout code)

Poser, en une seule fois, ce qui change tout : format (16:9 / 9:16), durée, langue, **le narrateur** (qui
parle ? un savant, un capitaine, une IA, un enfant…), le ton (mystérieux, épique, drôle, tendre), et le
**parcours** : quel axe on suit (descente, montée, avancée, remontée dans le temps) et quelle valeur le
compteur affiche (mètres, années, km, °C, %). S'il dit « débrouille-toi », ne pas redemander : choisir et
documenter.

Puis écrire le scénario dans le chat sous forme de paliers (8 à 12 pour 90 s) : `valeur | ce qu'on voit |
le fait dit par la voix`. Compter les mots : ~150–170 mots pour 90 s. Vérifier chaque chiffre (sources
fiables) : une erreur factuelle discrédite tout le film. Prévoir une **révélation** avant le noir final.
Attendre le go (ou un « je te laisse gérer »). Lire `references/wow.md` maintenant : il explique ce qui
distingue ce rendu d'un montage d'images, et ces choix se prennent au moment du scénario.

## 1. Scaffolder

```bash
node <skill>/scripts/setup.mjs ../mon-film-video --name "Titre" --port 3012
```
Projet séparé (dossier frère) : Remotion 4.0.529, three, r3f 9, postprocessing, sharp, socle copié, scripts
du pipeline copiés dans `scripts/`, configs vides écrites, `npm install` (2–4 min). Ensuite `npx tsc
--noEmit` doit être vert et `node scripts/stills.mjs 100 --scale=0.5` doit produire une image (fond
dégradé + rayons + particules, sans assets) : c'est la preuve que le pipeline WebGL headless marche sur
cette machine avant d'investir dans les assets.

## 2. Voix off et timeline (la timeline est la colonne vertébrale, tout s'y cale)

1. Remplir `scripts/vo-script.json` : `lines` (id, texte, `label`/`sub` affichés à l'écran, `value` du
   compteur, `gapAfter`), `voice.instructions` (le personnage, le ton, le rythme), `events` (impacts,
   arrêt caméra, révélation, `blackout`, `title`) exprimés relativement aux répliques.
   Écrire les nombres en toutes lettres.
2. `node scripts/gen-vo.mjs ash` — et faire pareil avec `onyx` et `cedar` sur une phrase si l'utilisateur
   veut choisir (envoyer les 3 wav). Les voix : ash (mûre, chaleureuse), onyx (grave, lente), cedar
   (naturelle, rapide).
3. `node scripts/build-timeline.mjs ash 1.06` — nettoie les silences, accélère de 6 % (imperceptible),
   normalise, écrit `src/timeline.json` avec les frames de chaque réplique et des événements. Si le total
   dépasse la durée voulue : raccourcir des répliques ou monter à 1.08, jamais au-delà de 1.12.

## 3. Assets peints (gpt-image-2.5) et découpage

1. Écrire `scripts/assets.json` : un `styleSuffix` commun (voir `references/prompts.md`, lire ce fichier
   avant d'écrire les prompts : orientation « facing left », marges, hublot magenta, portrait riggable,
   décors à fondu) et une entrée par asset (`model` sunburst pour les héros, flare pour le reste ; `size`
   selon la forme ; `quality` high seulement pour les héros). 20–25 assets ≈ 5 $ et 3 min.
2. `node scripts/gen-assets.mjs` (4 en parallèle, reprend là où ça s'est arrêté ; `--force id` pour
   regénérer un asset).
3. `node scripts/contact-sheet.mjs` puis **regarder** `public/assets/contact-sheet.png` (outil Read) :
   orientation, marges, cohérence de style, hublot bien magenta. Regénérer ce qui cloche avec un prompt
   corrigé. Pour le narrateur, ouvrir `public/assets/grid-<id>.png` et relever les rectangles de la tête,
   de la bouche (ou moustache), des sourcils, et les points cou/yeux.
4. Remplir `scripts/process.json` (chroma du véhicule, parts du narrateur, fondus des décors) puis
   `node scripts/process-assets.mjs` → `public/assets/*.png` + `meta.json` (dimensions, trou, points).

## 4. Musique et bruitages

`scripts/audio.json` : `mood` (dark-ambient, wonder, epic, tension), `root`, à partir de quelle réplique la
pulsation / le battement de cœur / les craquements apparaissent, les `impacts` sur des événements, le
`riserBefore` (montée coupée net). Puis `node scripts/make-audio.mjs` → `music.wav` + `sfx.wav`, calés sur
la timeline. Tout est synthétisé : zéro droit d'auteur. Si l'utilisateur fournit une musique, la déposer
dans `public/audio/music.wav` (vérifier la licence) et baisser `musicVolume`.

## 5. Mise en scène

- `src/film.config.ts` : `CAMERA` (axe, sens, vitesse, arrêt sur événement, distance), `SHAKES`,
  `ENV_KEYS` (couleur/brouillard/lumières/particules par avancement 0→1), `NARRATOR` (assets, alignement,
  projecteur, réactions), `HUD` (compteur, relevés calculés, règle, titre, tagline, handle).
- `src/scene/Story.tsx` : placer monuments/décors avec `anchorPos(beatId, u, v, z)`, écrire les
  trajectoires des créatures (fonctions `frame → pose`, attachées à `camAxis(frame)` quand elles doivent
  rester à l'écran), choisir le `mode` de déformation de chaque `Sprite3D`, attacher des `pointLight` aux
  éléments lumineux, prévoir la révélation (`noFog`, `scaleY` qui s'ouvre).
- `src/tags.ts` : les étiquettes ancrées (« 93 m · Statue de la Liberté »), fenêtres de frames.
- Les fichiers de l'exemple (`templates/example-abysses/src/scene/Creatures.tsx`, `Landmarks.tsx`,
  `lib/choreo.ts`) montrent des bancs instanciés, une approche du hublot, un passage devant la caméra, des
  parois empilées, un sol, une révélation. S'en inspirer sans copier le sujet.

Règles de mise en scène (détail et pourquoi dans `references/wow.md`) : la caméra avance, le monde est
fixe ; loin = z négatif dans le brouillard, proche = z positif ; rien d'immobile sauf les monuments ; dans
le noir on ne voit que ce que le faisceau touche ; un événement physique (choc, arrêt, révélation) toutes
les 20–30 s.

## 6. Vérifier avec des images fixes rendues en headless (pas seulement le Studio)

```bash
node scripts/stills.mjs 100 300 600 900 1200 1500 1800 2100 2400 2700 --scale=0.5 --sheet
```
Regarder `out/stills/sheet.png` (Read). Chercher : sprite manquant ou noir (voir `references/pitfalls.md`,
section headless), bloc noir net (NaN dans un shader), élément blanc surexposé (`tint` sombre, `emissive`
0), objet invisible dans le noir (`emissive`, PointLight, `noFog`), texte HUD qui chevauche, étiquette qui
sort du cadre, narrateur mal aligné dans son hublot (ajuster `NARRATOR.align`/`headScale`). Corriger,
re-rendre les frames concernées, jusqu'à ce que chaque palier soit propre. Le Studio (`npm run studio`)
sert à naviguer vite, mais il masque les bugs de rendu headless.

## 7. Rendre et livrer

```bash
npx remotion render Film out/film.mp4 --gl=angle --codec=h264 --crf=17 --concurrency=4
```
(~10 min pour 90 s en 1080p avec bloom ; `--gl=swangle` si angle échoue.) Puis vérifier avec ffprobe
(durée, pistes vidéo + audio), extraire 3–4 images du MP4 aux moments non encore vus (`ffmpeg -ss`),
mesurer le niveau (`ffmpeg -af volumedetect`, viser −16 à −20 dB de moyenne) et envoyer le MP4
(SendUserFile). Dire clairement que le mix n'a pas été écouté et comment ajuster (`musicVolume`,
`sfxVolume`, `voiceVolume` sont des props de la composition ; `scripts/audio.json` pour la matière).

Le récap de livraison tient seul : où est le fichier, durée/format, la liste des paliers, ce qui a été
vérifié, les commandes pour changer une réplique (vo-script → gen-vo → build-timeline → make-audio →
render) ou une voix.

## Pièges à connaître avant de coder
Lire `references/pitfalls.md`. Les deux qui coûtent des heures : (1) en headless, Remotion ne dessine
qu'une frame three.js par image — d'où le composer impératif, le préchargement des textures/audio et
`Readvance` déjà dans le socle, à ne pas contourner ; (2) `pow()` d'une base négative dans un shader donne
NaN et le bloom le transforme en bloc noir.
