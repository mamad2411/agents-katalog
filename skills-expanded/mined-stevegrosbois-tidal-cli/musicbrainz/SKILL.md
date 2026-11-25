---
name: musicbrainz
description: >
  Interroge l'API publique MusicBrainz pour récupérer des métadonnées musicales fiables :
  recherche d'artistes, discographies complètes (release-groups : albums, EPs, singles, lives,
  compilations), détails de releases (labels, formats, dates, pays), recordings, œuvres,
  relations entre entités (membres de groupe, collaborations, liens externes type Discogs/Wikidata),
  tags/genres, et identifiants MBID pour croiser avec d'autres services (Last.fm, Tidal, Discogs).
  Utilise ce skill dès que l'utilisateur demande la discographie d'un groupe, des dates de sortie
  précises, des éditions/formats d'album, des informations sur la formation d'un groupe, ou plus
  généralement des métadonnées musicales que Last.fm ou Tidal ne fournissent pas de façon exhaustive.
---

# MusicBrainz API Skill

Accède aux métadonnées musicales de la base communautaire MusicBrainz.

## Configuration

**Aucune authentification requise** pour les requêtes en lecture.

**Obligatoire** : un header `User-Agent` identifiant le client, sinon MusicBrainz peut bloquer les requêtes (ils prennent ça très au sérieux). Format recommandé :

```
User-Agent: tidal-cli/0.1 ( steve@grosbois.fr )
```

**Rate limit** : 1 requête par seconde maximum par User-Agent. Pour des séries de requêtes, ajoute un `sleep 1` entre chaque appel.

**Base URL** : `https://musicbrainz.org/ws/2/`
**Docs** : https://musicbrainz.org/doc/MusicBrainz_API
**Format** : ajouter `&fmt=json` à chaque requête (sinon XML par défaut)

## Concepts clés

MusicBrainz distingue trois types de requêtes :

| Type | Usage | Exemple |
|---|---|---|
| **Lookup** | Récupérer une entité connue par son MBID | `/artist/<mbid>` |
| **Browse** | Lister les entités liées à une autre | `/release-group?artist=<mbid>` |
| **Search** | Recherche full-text (Lucene) | `/artist?query=architects` |

Et plusieurs niveaux d'entités à comprendre :

- **artist** : un groupe ou une personne
- **release-group** : une "œuvre" abstraite (ex : l'album *Holy Hell*), indépendamment des éditions
- **release** : une édition spécifique (CD UK 2018, vinyle US 2019, deluxe Japan…)
- **recording** : un enregistrement audio précis (apparaît sur une ou plusieurs releases)
- **work** : une composition (paroles + musique), distincte de ses enregistrements

Pour une discographie, on travaille presque toujours au niveau **release-group**.

## Workflow type : discographie d'un groupe

### 1. Trouver le MBID de l'artiste

```bash
curl -s -H "User-Agent: tidal-cli/0.1 ( steve@grosbois.fr )" \
  "https://musicbrainz.org/ws/2/artist/?query=artist:Architects%20AND%20country:GB&fmt=json&limit=5"
```

- Filtrer par `country:` ou `tag:` aide à désambiguïser (il y a plusieurs "Architects" : UK metalcore, US punk, etc.)
- Le score Lucene est dans `score` (0-100)
- Récupérer `id` (= MBID, un UUID)

### 2. Récupérer la discographie (release-groups)

```bash
curl -s -H "User-Agent: tidal-cli/0.1 ( steve@grosbois.fr )" \
  "https://musicbrainz.org/ws/2/release-group?artist=<mbid>&type=album&fmt=json&limit=100"
```

- `type` (primary) : `album`, `single`, `ep`, `broadcast`, `other`
- Pour exclure compilations/lives, garder `secondary-types` vide : filtrer côté client sur `secondary-types == []`
- Pour les inclure : ajouter `|compilation`, `|live`, `|remix`, `|soundtrack`, `|demo` au paramètre `type`

Exemple combiné (albums studio + EPs, sans compilations/lives) :
```bash
curl -s -H "User-Agent: tidal-cli/0.1 ( steve@grosbois.fr )" \
  "https://musicbrainz.org/ws/2/release-group?artist=<mbid>&type=album|ep&fmt=json&limit=100"
```

Champs utiles dans la réponse :
- `title`
- `first-release-date` (YYYY-MM-DD, parfois juste YYYY)
- `primary-type`, `secondary-types`
- `id` (MBID du release-group, à utiliser pour drill-down)

### 3. (Optionnel) Détailler les éditions d'un album

```bash
curl -s -H "User-Agent: tidal-cli/0.1 ( steve@grosbois.fr )" \
  "https://musicbrainz.org/ws/2/release?release-group=<rg-mbid>&fmt=json&inc=labels+media&limit=100"
```

Donne pour chaque édition : pays, date, label, format (CD/vinyle/digital), nombre de pistes.

## Endpoints essentiels

### Recherche (full-text Lucene)

```bash
# Artistes
curl -s -H "User-Agent: ..." \
  "https://musicbrainz.org/ws/2/artist/?query=Architects&fmt=json&limit=10"

# Release-groups (album par titre + artiste)
curl -s -H "User-Agent: ..." \
  "https://musicbrainz.org/ws/2/release-group/?query=release:Holy%20Hell%20AND%20artist:Architects&fmt=json"

# Recordings (morceaux)
curl -s -H "User-Agent: ..." \
  "https://musicbrainz.org/ws/2/recording/?query=recording:Doomsday%20AND%20artist:Architects&fmt=json"
```

Syntaxe Lucene utile :
- `artist:"exact name"` pour forcer le match exact
- `country:GB`, `tag:metalcore`, `type:album`
- Booléens `AND`, `OR`, `NOT`

### Lookup par MBID

```bash
# Artiste avec discographie + relations + tags
curl -s -H "User-Agent: ..." \
  "https://musicbrainz.org/ws/2/artist/<mbid>?fmt=json&inc=release-groups+tags+url-rels+artist-rels"
```

Valeurs `inc` utiles pour un artiste :
- `release-groups` : la discographie d'un coup (limite 25, sinon utiliser browse)
- `aliases` : autres orthographes / noms
- `tags`, `genres` : tags communautaires
- `ratings` : note communautaire
- `url-rels` : liens externes (Wikipedia, Discogs, Spotify, Bandcamp, site officiel…)
- `artist-rels` : membres du groupe, collaborateurs
- `recording-rels` : enregistrements impliquant l'artiste

Combiner avec `+` (URL-encodé). Exemple : `inc=release-groups+url-rels+tags`.

### Browse (lister des entités liées)

```bash
# Tous les release-groups d'un artiste (utiliser ça plutôt que inc= pour > 25 éléments)
curl -s -H "User-Agent: ..." \
  "https://musicbrainz.org/ws/2/release-group?artist=<mbid>&fmt=json&limit=100&offset=0"

# Toutes les releases d'un release-group (= toutes les éditions d'un album)
curl -s -H "User-Agent: ..." \
  "https://musicbrainz.org/ws/2/release?release-group=<mbid>&fmt=json&inc=labels+media"

# Tous les enregistrements d'une release (= tracklist)
curl -s -H "User-Agent: ..." \
  "https://musicbrainz.org/ws/2/release/<mbid>?fmt=json&inc=recordings+artist-credits"
```

Browse supporte la pagination via `limit` (max 100) et `offset`.

## Patterns courants

### Trouver un artiste avec désambiguïsation

Souvent plusieurs artistes portent le même nom. Stratégie :

1. Lancer une recherche large : `?query=Architects&fmt=json&limit=10`
2. Trier par `score` (le 1er est généralement le bon)
3. Si plusieurs candidats proches, utiliser le champ `disambiguation` retourné, ou affiner avec `country:` / `tag:` / `type:Group`

### Lister les sorties par ordre chronologique

Trier côté client par `first-release-date`. Attention : certaines entrées ont une date partielle (`2018` au lieu de `2018-10-26`) ou vide.

### Récupérer les liens vers d'autres services

`inc=url-rels` retourne un tableau `relations` où chaque relation a un `type` (`discogs`, `wikipedia`, `wikidata`, `spotify`, `bandcamp`, `official homepage`, etc.) et une `url.resource`. Très utile pour passer d'un MBID à un ID Discogs/Spotify/etc.

### Croiser avec Last.fm

Last.fm expose le MBID dans la plupart de ses réponses (`mbid` dans `artist.getinfo`). Une fois un MBID en main, on peut basculer entre les deux services sans réambiguïser.

## jq utiles

```bash
# Liste compacte : "YYYY — Titre (type)"
jq -r '.["release-groups"][] | "\(.["first-release-date"][:4]) — \(.title) (\(.["primary-type"]))"' \
  | sort

# Filtrer les albums studio uniquement (pas de secondary-type)
jq '.["release-groups"][] | select(.["secondary-types"] | length == 0) | select(.["primary-type"] == "Album")'

# Récupérer juste le 1er artiste d'une recherche
jq '.artists[0] | {id, name, country, disambiguation, score}'

# Extraire les liens externes
jq '.relations[] | select(.["target-type"] == "url") | {type, url: .url.resource}'
```

## Notes

- **Toujours envoyer un User-Agent identifiable**. Un User-Agent absent ou générique (`curl/x.y`) peut renvoyer 403.
- **Respecter le 1 req/sec** : `sleep 1` entre les appels pour les workflows multi-étapes.
- **MBID = UUID** : format `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`. Persistant et stable, idéal pour stocker des références.
- **Données communautaires** : la complétude varie selon la popularité de l'artiste. Pour le metal / metalcore (genres préférés de l'utilisateur), la couverture est généralement excellente.
- **Pas de pochettes ici** : pour les artworks, MusicBrainz a un service séparé (Cover Art Archive) accessible via `https://coverartarchive.org/release/<release-mbid>/front`.