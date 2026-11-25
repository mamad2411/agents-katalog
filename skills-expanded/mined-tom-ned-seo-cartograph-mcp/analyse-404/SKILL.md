---
name: analyse-404
description: >
  Décompose les 404 d'un site par SOURCE et les pondère par le TRAFIC perdu (MCP SEO
  Cartograph requis), puis sort un plan de redirections 301 prêt à poser. Sépare les
  quatre familles de 404 (liens internes cassés, pages supprimées à trafic, orphelines
  connues de Google mais absentes du crawl, régressions apparues entre deux crawls) parce
  qu'elles n'ont pas le même traitement. Utiliser ce skill dès que l'utilisateur parle de
  404, de pages introuvables, de liens cassés, de « pages mortes », d'une refonte qui a
  cassé des URLs, d'un plan de redirections, ou veut savoir quelles 404 lui coûtent du
  trafic, même sans le mot « 404 ». Nécessite le MCP SEO Cartograph connecté
  (app.tnedjar.com) avec un crawl remonté ; la Search Console connectée sert à peser le
  trafic et à rattraper les 404 que le crawl ne voit pas.
---

# 404 à trafic — toutes les 404 ne se valent pas

Une 404 sans trafic ni lien entrant n'est pas un problème : c'est du bruit propre. Une 404
sur une page qui recevait 800 impressions par mois, c'est du trafic qui part à la
poubelle. Ce skill ne liste pas les 404, il les **trie par source** (chaque source a un
traitement différent) et les **classe par trafic perdu** (on répare ce qui rapporte). Le
livrable n'est pas une liste, c'est un plan de redirections priorisé.

Deux pièges décident de la justesse du diagnostic.

**Piège 1 : le crawl ne voit qu'une partie des 404.** Il suit les liens du site. Une
ancienne URL que plus aucune page ne lie, mais que Google garde en index ou qu'un backlink
externe pointe encore, le crawl ne la croise jamais. Il faut donc croiser le crawl AVEC le
registre Search Console.

**Piège 2 : le trafic d'une page morte ne se lit PAS sur 28 jours.** C'est le piège qui
fait rater le sujet. Une page en 404 depuis trois semaines a déjà perdu ses impressions
récentes (Google a cessé de l'afficher), donc sur une fenêtre de 28 jours elle pèse zéro et
paraît inoffensive. Sa vraie valeur, c'est ce qu'elle rapportait DE SON VIVANT : il faut la
peser sur une fenêtre LARGE (jusqu'aux 16 mois que couvre la Search Console) et lire les
CLICS, pas seulement les impressions. Un breakdown qui trie les 404 sur 28 jours conclura
presque toujours « aucune 404 n'a de trafic » — et se trompera. Exemple type : des pages passées en 404 après un changement de slugs
affichent 0 impression sur 28 jours et pourtant des centaines de clics cumulés sur 16 mois.
Tout le trafic perdu reste invisible dans la fenêtre courte.

## Prérequis

MCP SEO Cartograph connecté avec au moins un crawl remonté (`list_crawl_sites` non vide).
Sans crawl, ne pas improviser : proposer de le lancer (`request_crawl`) et expliquer que
le breakdown se fait sur le crawl réel, puis s'arrêter. La Search Console connectée n'est
pas strictement obligatoire mais sans elle il n'y a ni pondération par trafic ni
rattrapage des orphelines : le dire, et le breakdown se limitera aux 404 vues par le
crawl.

## Ce dont ce skill a besoin, et où le chercher

Quatre briques de données. Pour chacune : ce qu'elle apporte, et l'outil qui la fournit.

### 1. Les 404 vues par le crawl (liens internes cassés + pages en statut 404)

C'est la base : ce que le crawl a rencontré en suivant les liens du site.

- `get_crawl_overview` : l'ampleur (combien de statuts 4xx/5xx au total). La carte avant le détail.
- `get_crawl_data` section `broken_links` : les liens internes cassés, avec la page SOURCE
  qui pointe vers la 404. Distinction essentielle ici : un lien cassé *dans le contenu*
  d'une page vivante se **corrige à la source** (on répare le lien), il ne se redirige pas.
- `get_crawl_data` section `issues` et `crawl_audit` : les 404 agrégées par type, pour
  repérer le systémique (un gabarit qui génère une URL morte sur des centaines de pages).
- `list_crawl_pages` filtré sur le statut 404/410 : la liste des pages elles-mêmes en erreur.

### 2. Le trafic perdu par page (pour pondérer) — sur une fenêtre LARGE

Sans ça, on répare à l'aveugle. Mais l'outil décisif ici est `explore_search_console` en
dimension `page` sur une **plage longue** (voir Piège 2). Régler `start_date` à ~16 mois en
arrière et lire les CLICS cumulés de chaque URL morte : c'est le trafic réellement perdu,
celui qu'une fenêtre courte efface.

- `explore_search_console` (dimension `page`, `start_date` ~16 mois) : le registre historique
  clics/impressions par page. La sortie peut être volumineuse (des milliers de pages) et être
  écrite dans un fichier ; croiser localement les chemins morts contre ce registre.
- `get_search_queries` (paramètre `url`) : les requêtes réelles d'une URL précise, utile pour
  comprendre CE que la page captait avant de mourir (et donc vers quoi la rediriger).
- Piège à connaître sur `build_redirect_plan` et `compare_crawls` : ils attachent le trafic
  sur une fenêtre courte. Un 0 impression dans leur sortie ne veut PAS dire « sans trafic » —
  ça peut être une page morte depuis longtemps. Toujours recroiser les candidates avec la
  fenêtre 16 mois avant de conclure qu'une 404 est du bruit.

### 3. Les 404 que le crawl NE VOIT PAS (orphelines, anciennes URLs, backlinks)

La brique qui rattrape le Piège 1. Deux façons :

- **Via le MCP** : `build_redirect_plan` en mode auto intègre le **registre GSC** : les URLs
  que la Search Console a remontées et qui ne sont plus dans les pages vivantes du crawl.
  Marquées « à vérifier (orpheline GSC) » car déduites de l'absence, pas d'un test HTTP.
  Paramètre `min_impressions` pour couper le bruit, `include_gsc_registry: false` pour ne
  garder que le crawl.

**Règle d'or : le crawl-vivant est la seule source de vérité pour « morte ou vivante ».** Le
registre GSC liste les URLs à trafic, vivantes ET mortes mélangées. Ne JAMAIS déduire qu'une
URL est morte parce qu'elle ressemble à un ancien schéma ou parce qu'un silo a l'air
abandonné : une URL n'est morte que si le crawl la donne en ≥ 400, ou si elle est absente de
l'ensemble des pages vivantes (statut < 400) du crawl. Pour isoler les vraies mortes,
soustraire l'ensemble vivant du crawl du registre GSC (c'est ce que fait `build_redirect_plan`
en interne). Cas vécu : un silo `/services/*` paraissait supprimé vu du registre,
alors que 90 % des pages étaient bien vivantes (statut 200) — seules trois feuilles avaient
changé de slug. Confirmer les cas ambigus avec `list_crawl_pages` (search sur le chemin) ou
`inspect_url` avant de rediriger.
- **Directement dans la Search Console, au besoin** (quand on veut la liste que Google
  lui-même qualifie de 404, y compris ce que le stockage n'a pas encore) :
  - *Indexation > Pages > « Introuvable (404) »* : la liste autoritaire des URLs que Google
    a tenté d'indexer et a reçues en 404. C'est là que sortent les URLs pointées par des
    backlinks externes ou d'anciennes URLs jamais recrawlées côté site.
  - *Performances > Pages* : les URLs qui ont eu des impressions/clics ; croiser avec les
    pages vivantes du crawl révèle celles qui avaient du trafic et n'existent plus.
  - `inspect_url` (MCP) sur une URL précise : le statut d'indexation Google réel, pour
    confirmer un cas ambigu (est-ce vraiment une 404 côté Google, ou juste absente du crawl).

### 4. La régression (une refonte ou une mise en prod a cassé des URLs)

Quand les 404 sont apparues d'un coup, la bonne question n'est pas « lesquelles » mais
« depuis quand ».

- `compare_crawls` : compare deux crawls du domaine et remonte les pages qui étaient OK
  (< 400) et sont devenues 404/410, enrichies du trafic GSC et triées dessus. Sans run_id,
  il prend les deux derniers crawls. C'est l'outil du diagnostic post-refonte.

## Étape 1 — Cadrer

`list_crawl_sites` puis `list_crawls_for_site` : confirmer le site, noter s'il existe un
crawl précédent (indispensable si le contexte est une refonte ou une chute soudaine).
Demander (ou déduire) le contexte : chute progressive, ou cassure nette après une mise en
ligne. Ça décide de l'étape 2.

## Étape 2 — Récolter les quatre familles

Dans l'ordre :

1. **Crawl** (brique 1) : `get_crawl_overview` puis `get_crawl_data` (`broken_links`,
   `issues`). Séparer d'emblée les liens cassés *dans le contenu* (à corriger à la source)
   des pages *supprimées* (à rediriger).
2. **Registre GSC** (brique 3) : `build_redirect_plan` en auto sur le domaine. Il ramène en
   une passe les 404 du crawl, les pages à trafic devenues 404, et les orphelines du
   registre GSC, déjà pondérées et avec une cible proposée par URL.
3. **Régression** (brique 4), seulement si contexte de refonte / cassure nette :
   `compare_crawls`. Il isole ce qui s'est cassé entre les deux crawls, la cause la plus
   probable étant une seule (changement d'arborescence, slugs modifiés, migration).
4. **Search Console directe** (brique 3, au besoin) : si l'utilisateur soupçonne des 404
   que même le registre stocké ne couvre pas (backlinks récents, URLs jamais recrawlées),
   l'orienter vers *Indexation > Pages > Introuvable (404)* et lui demander d'en coller la
   liste ; la passer ensuite à `build_redirect_plan` via le paramètre `urls`.

## Étape 3 — Trier par source (le breakdown)

Ranger chaque 404 dans une des quatre familles, parce que le traitement diffère :

| Famille | Ce que c'est | Traitement |
|---|---|---|
| **Lien interne cassé** | Une page vivante pointe vers une URL morte | Corriger le LIEN à la source, ne pas rediriger |
| **Page supprimée à trafic** | Une URL qui recevait des impressions n'existe plus | Redirection 301 vers la meilleure page vivante |
| **Orpheline GSC** | Google/backlinks connaissent une URL absente du crawl | Rediriger si trafic ou backlink, sinon laisser 404 |
| **Régression** | Page OK au crawl précédent, 404 au dernier | Souvent une cause unique : corriger la cause d'abord |

Dans chaque famille, classer par **clics cumulés 16 mois** (pas les impressions 28 j — voir
Piège 2). Ne pas noyer le rapport avec les 404 à zéro trafic et sans lien entrant : les
compter en bloc, pas en liste (une 404 propre n'est pas une urgence).

**Lire les liens cassés correctement.** Le crawl affiche souvent un chiffre effrayant du
type « 1 270 pages avec liens cassés ». Ce n'est pas 1 270 problèmes : c'est le nombre de
pages qui portent le lien, pas le nombre de liens morts. Toujours **dédupliquer par cible**
et trier par nombre de pages liantes. Un lien mort présent sur des centaines de pages est un
lien de gabarit (menu, pied de page) : UNE correction dans le template le résout partout. Cas
vécu : trois cibles `/?page_id=...` liées depuis les 1 270 pages du site = trois entrées de
menu cassées, une seule correction. `broken_links` donne le compteur par cible ; c'est lui
qui sépare le systémique (le template) de l'isolé (un lien dans un article).

**Trouver la bonne cible 301.** Pour une page renommée, la cible n'est pas « la home » : c'est
son **jumeau vivant dans le même silo**. La similarité lexicale seule le rate quand le slug a
été réécrit — `/services/renovation/toiture/` (morte) a pour vrai équivalent
`/services/renovation/refection-complete-de-toiture.../` (vivante), lexicalement
éloignée. Réflexe : chercher dans les pages vivantes du crawl du même répertoire parent
(`list_crawl_pages` search sur le segment) avant de se rabattre sur un parent générique.

## Étape 4 — Le plan de sortie

`build_redirect_plan` produit déjà le plan 301 (URL morte → meilleure page vivante par
similarité et préfixe de langue, priorisé par trafic) avec les exports `.htaccess` et
`nginx` prêts à coller. Deux réflexes :

- **Confiance « à vérifier »** (dont toutes les orphelines du registre GSC) : la cible est
  proposée, pas certaine. Faire relire ces lignes avant de poser. Le tool PLANIFIE, il
  n'applique rien : la pose reste une décision humaine.
- **Refonte avec liste d'anciennes URLs** : passer les URLs connues via le paramètre `urls`
  (depuis un ancien crawl, un export GSC, ou un sitemap archivé) plutôt que de compter sur
  le seul auto.

## Étape 5 — Le rapport

```
# 404 à trafic — [domaine] — [date du crawl]

## Verdict (3 phrases)
[Combien de trafic part en 404, la source dominante, la priorité n°1.]

## Chiffres clés
| 404 crawl | Orphelines GSC | Clics perdus (16 mois) | Impressions perdues (16 mois) | Régressions vs crawl précédent |

## Par famille (priorisé par clics 16 mois)
### Pages supprimées à trafic  → à rediriger
[URL morte | clics 16 mois | impressions 16 mois | cible 301 proposée | confiance]
### Orphelines GSC  → à rediriger si trafic
[idem, marquées « à vérifier »]
### Liens internes cassés  → à corriger à la source
[URL morte | page(s) qui la lient]
### Régressions  → cause commune probable
[ce qui s'est cassé entre les deux crawls, l'hypothèse de cause]

## Plan de redirections (extrait htaccess / nginx)
[le bloc généré, avec la mention « à relire avant pose, aucune application automatique »]

## Bruit (bloc, non détaillé)
[X 404 sans trafic ni lien entrant, à ignorer.]
```

En français par défaut, en anglais si demandé. Niveau adapté : client final = chaque terme
expliqué en une incise ; développeur = dense, on garde le jargon et on livre surtout les
blocs d'export.

## Étape 6 — La suite

Si le contexte est une refonte préparée dans le back-office (SEO > Refonte) et que la
demande porte sur les fichiers à poser, c'est le skill `fichiers-de-redirection` qui
prend le relais : il travaille sur le chantier, pas sur le crawl du site en place.

Si les liens internes cassés dominent, le vrai chantier est le maillage : passer le relais
au skill `chantier-maillage`. Si les 404 viennent d'une refonte, insister sur la
correction de la cause (arborescence, slugs) avant d'empiler les redirections. Une fois le
plan posé par l'utilisateur, proposer un nouveau crawl (`request_crawl`) puis
`compare_crawls` pour vérifier que les redirections ont bien résorbé les 404.
