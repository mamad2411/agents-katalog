---
name: fichiers-de-redirection
description: >
  Sort les fichiers de redirections d'une refonte à partir d'un chantier SEO Cartograph
  (MCP requis) : un fichier de 301 pour le trafic qu'on sauve, un fichier de 410 pour les
  pages qu'on abandonne, écrits sur le disque et prêts à relire. Tranche d'abord les lignes
  qui pèsent (trafic, liens entrants) puis exporte, parce qu'un export fait trop tôt ne
  contient que ce qui a déjà été décidé. Utiliser ce skill dès que l'utilisateur demande un
  fichier de redirections, un .htaccess, un bloc nginx, un CSV de redirections, « les 301 de
  la refonte », « les 410 », un plan de redirections à poser, ou veut savoir ce qu'il reste
  à arbitrer avant une mise en ligne. Nécessite le MCP SEO Cartograph connecté
  (app.tnedjar.com) et un chantier de refonte existant sur le compte.
---

# Fichiers de 301 et de 410 depuis un chantier de refonte

Le chantier de refonte tient deux listes : les URLs d'avant (avec leur trafic sur 16 mois et
leurs liens entrants) et les URLs d'après. Le moteur a déjà rapproché ce qui se rapproche
tout seul. Ce skill fait le reste : arbitrer ce qui pèse, puis écrire les fichiers.

Deux choses à garder en tête avant de commencer.

**L'export ne contient QUE les lignes décidées.** Une cible « proposée » n'entre pas dans le
fichier. Exporter un chantier à 30 % de couverture rend un fichier de 40 lignes qui a l'air
fini et qui laisse 1 800 pages dehors. La réponse de l'outil donne toujours
`reste_a_decider` : ce chiffre passe dans le rapport final, jamais sous silence.

**301 et 410 ne se posent pas au même moment.** Une 301 sauve du trafic et part avec la mise
en ligne. Une 410 dit à Google « cette page est morte, oubliez-la » : c'est un abandon
assumé, ça se relit ligne par ligne, et ça se pose après. D'où deux fichiers séparés par
défaut, jamais un seul fichier fourre-tout, sauf demande explicite.

## Prérequis

MCP SEO Cartograph connecté, et un chantier existant (`list_redesigns` non vide). Le chantier
se crée dans le back-office (SEO > Refonte) parce qu'il demande les deux listes d'URLs, qui
ne se devinent pas depuis ici. Si `list_redesigns` est vide : le dire, expliquer où le créer,
et s'arrêter. Ne pas fabriquer un plan de redirections à la main depuis un crawl : pour ça,
c'est le skill `analyse-404`, qui traite les 404 d'un site en place, pas une refonte.

## Étape 1. Trouver le chantier et lire sa couverture

`list_redesigns` (filtrer par `domain` si l'utilisateur a nommé un site). Trois chiffres
décident de la suite :

- `couverture_clics_pct` : la part du trafic en jeu qui est déjà tranchée. C'est le chiffre
  qui compte, pas la couverture en URLs : 200 pages sans trafic décidées ne valent pas une
  page à 4 000 clics laissée ouverte.
- `lignes_critiques_ouvertes` : les pages qui portent l'essentiel du trafic ou qui ont des
  liens entrants et qui ne sont toujours pas décidées. Tant que ce nombre n'est pas à zéro,
  un export est prématuré.
- `decidees_par_ia_non_relues` : ce qu'un agent a tranché sans relecture humaine. À signaler
  dans le rapport, pas à cacher.

Si la couverture clics est déjà haute et qu'il ne reste aucune ligne critique : sauter
directement à l'étape 3, l'utilisateur veut juste ses fichiers.

## Étape 2. Trancher ce qui pèse (seulement si nécessaire)

Travailler par poids, pas par ordre alphabétique. `get_redesign` avec `only_critical: true`,
puis `min_clicks` dégressif (par exemple 100, puis 20, puis 0) pour descendre la file. La
sortie est déjà triée par clics.

Lire l'état de chaque ligne :

| État | Ce que c'est | Ce qu'on en fait |
|---|---|---|
| `exact` | le chemin n'a pas bougé | rien, c'est déjà couvert |
| `a_controler` | une cible est PROPOSÉE, personne ne l'a validée | valider ou corriger, puis décider |
| `non_couverte` | aucune cible trouvée | chercher dans le vivier, ou assumer la 410 |
| `redirigee` / `supprimee` | déjà décidée | ne pas y retoucher |

Sur une ligne `a_controler`, `methode` et `appui_requetes` disent sur quoi la proposition
repose. `appui_requetes.share` est la part du trafic de l'ancienne page dont la cible
hérite : au-dessus de 0,9 la proposition est franche, en dessous de 0,7 elle se vérifie.
`requete_divergente` veut dire que les requêtes et la ressemblance de chemin désignent des
cibles différentes : c'est un arbitrage, pas un automatisme, et sur une ligne critique
il vaut mieux la laisser à l'humain que la trancher au jugé.

Sur une ligne `non_couverte`, `search_redesign_targets` avec `near` = le chemin de l'ancienne
page classe les candidates par proximité (même rubrique parente d'abord). Le bon réflexe est
le jumeau dans le même silo, pas la page d'accueil : rediriger tout un répertoire mort vers
la home dilue le signal et n'a jamais rattrapé un positionnement.

Puis `decide_redesign_urls`, par lots de 200 lignes au maximum, avec
`[{id, decision, target?}]` où `decision` vaut `rediriger`, `supprimer` ou `rouvrir`. Trois
règles :

- **`supprimer` (410) est un choix, pas un fourre-tout.** Une page sans trafic ni lien
  entrant peut partir en 410. Une page qui a du trafic ne part jamais en 410 parce qu'on
  n'a pas trouvé de cible : elle reste ouverte, et le rapport le dit.
- **Ne jamais inventer une cible.** `target` doit exister dans le vivier de droite, sinon la
  décision est refusée. Une 301 vers une page absente remplace une 404 par une autre.
- **`override_human` reste à faux.** Repasser sur une décision humaine demande une consigne
  explicite de l'utilisateur, jamais une initiative.

## Étape 3. Exporter, deux fois

Le format suit le serveur. À défaut d'information : `htaccess` pour Apache et pour un
WordPress standard, `nginx` pour un nginx, `csv` pour un CDN, un plugin de redirections ou
une relecture en tableur. Demander en une phrase si rien ne permet de trancher.

Deux appels à `export_redesign_redirects` :

1. `only: "301"` : les redirections.
2. `only: "410"` : les suppressions assumées.

Écrire le contenu du champ `fichier` sur le disque, sous le nom donné par
`nom_de_fichier_suggere` (par exemple `refonte-15-301.htaccess` et
`refonte-15-410.htaccess`), dans le répertoire courant ou à l'endroit que l'utilisateur
indique. Si l'un des deux périmètres est vide, ne pas écrire de fichier vide : le dire.

Ne rien poser sur un serveur. L'outil rend du texte, la pose est un geste humain.

## Étape 4. Le compte rendu

```
# Redirections de refonte : [domaine], chantier #[id]

## Ce qui est écrit
- refonte-[id]-301.[ext] : X redirections 301
- refonte-[id]-410.[ext] : Y suppressions 410
Couverture du trafic en jeu : Z %

## Ce qui reste dehors
[N] ligne(s) sans décision, pesant [C] clic(s), dont [K] critique(s).
[Si N = 0 : « Toutes les lignes sont décidées, ces fichiers sont complets. »]

## Décidé par l'IA dans cette passe
[Combien de lignes, et lesquelles méritent une relecture : les requete_divergente,
les cibles à share faible, les 410 sur des pages qui avaient encore un peu de trafic.]

## Avant la pose
- Vérifier que les cibles répondent en 200 sur le nouveau site.
- Poser les 301 avec la mise en ligne, les 410 après relecture.
- Un crawl après la pose (`request_crawl`) puis `compare_crawls` confirme que les 404
  sont résorbées.
```

En français par défaut. Pour un développeur, réduire le commentaire et livrer surtout les
chemins des fichiers écrits ; pour un décideur, garder les chiffres de couverture et de
trafic sauvé, et expliquer en une incise ce qu'est une 301 et une 410.
