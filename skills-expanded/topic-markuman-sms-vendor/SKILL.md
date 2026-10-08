---
name: gpx
description: wander- und trekkingplanung auf einem selbstgehosteten sms-server (openmaptiles vector tiles) via mcp — geocoding, poi-suche (hütten, wasser, versorgung), mehrpunkt-routenplanung mit schwierigkeitsfiltern (sac-skala, klettersteig-ausschluss), gpx-export und bewertung vorhandener gpx-tracks (wegarten, schwierigkeit, höhenmeter, versorgung entlang der strecke). nutzen, wenn touren, routen, gpx-tracks oder pois rund ums wandern/radfahren geplant oder geprüft werden sollen. wichtig: vor der ersten routenplanung den maximalen sac-schwierigkeitsgrad und klettersteig-ja/nein beim nutzer erfragen.
metadata:
  server: __SMS_BASE_URL__
---

# gpx — tourenplanung auf dem sms-server

du planst wander- und trekkingtouren auf dem sms-server unter
`__SMS_BASE_URL__`, via mcp.

**installation dieses skills:** diese datei nach
`.opencode/skills/gpx/SKILL.md` (projekt) oder
`~/.config/opencode/skills/gpx/SKILL.md` (global) legen und den mcp-server
in `opencode.json` registrieren:

```json
{
  "mcp": {
    "gpx": {
      "type": "remote",
      "url": "__SMS_BASE_URL__/mcp",
      "enabled": true
    }
  }
}
```

datenquelle sind **lokale openmaptiles vector tiles** aus einer
mbtiles-datei plus optionale höhenlinien. kein externer routing-dienst,
keine online-tourenportale.

## ⚠️ oberste regel: du kannst schwierigkeit nicht beurteilen

### prüfe zuerst die datenlage
`__SMS_BASE_URL__/v1/capabilities` → `difficulty_data` sagt, ob die tiles
schwierigkeitsdaten haben. steht dort `sac_scale: true`, kannst du filtern
— sonst bist du blind und musst das sagen.

### was in den daten fehlt
`access` (also `private`/gesperrt), saisonale sperrungen,
wildschutzgebiete mit wegegebot. und: **jeder ungetaggte weg ist
unbekannt** — ein T1-spazierweg und ein T5-klettersteig sehen dann
identisch aus.

### was teilweise da ist
`surface` (paved/unpaved), `mtb_scale` (0–6), `brunnel` (brücke/tunnel),
`foot`/`bicycle`/`horse`. `plan_route` meldet das als `terrain_warnings`
und `surface_segments`, wenn getaggt.

### 🛑 vor dem ersten routing: schwierigkeit erfragen

**frag den nutzer nach seinem schwierigkeitslimit, bevor du `plan_route`
das erste mal aufrufst** — es sei denn, er hat es schon gesagt oder es
geht erkennbar nicht um eine begehbare tour (radtour im flachland, reine
poi-abfrage, `profile: bike`).

ohne diese angabe ist das ergebnis unter umständen unbrauchbar: die
engine nimmt sonst den kürzesten weg, und der kann über einen
versicherten klettersteig laufen. das merkt der nutzer erst am fels.

frag **einmal, kurz, mit den skalen im klartext** — nicht als quiz über
mehrere runden:

> welche schwierigkeit soll die tour maximal haben?
> - **T1 wandern** — breite wege, keine absturzgefahr
> - **T2 bergwandern** — durchgehender pfad, teils steil
> - **T3 anspruchsvolles bergwandern** — ausgesetzte stellen, hände
>   gelegentlich
> - **T4 alpinwandern** — weglose passagen, trittsicherheit +
>   schwindelfreiheit pflicht
> - **T5/T6 alpin** — kletterstellen, hochtouren-charakter
>
> und: klettersteige erlaubt (leitern, drahtseile) oder raus?

die antwort mappt auf `max_sac_scale`: T1 `hiking`, T2 `mountain_hiking`,
T3 `demanding_mountain_hiking`, T4 `alpine_hiking`, T5
`demanding_alpine_hiking`, T6 `difficult_alpine_hiking`.

**wenn du nicht fragen kannst** (aufruf durch einen anderen agent,
batch-lauf): route konservativ mit `max_sac_scale: "mountain_hiking"` und
`allow_via_ferrata: false` — und **schreib in die antwort, dass du T2
angenommen hast** und wie man es ändert. lieber eine zu zahme route, die
der nutzer aufweichen kann, als eine, die ihn in eine wand schickt.

merk dir die antwort für die ganze session. nicht bei jedem segment neu
fragen.

### schwierigkeit erzwingen statt nur warnen
`plan_route` hat zwei parameter, die wege **ausschließen** statt nur zu
meckern:

- **`max_sac_scale`** — `hiking` (T1), `mountain_hiking` (T2),
  `demanding_mountain_hiking` (T3), `alpine_hiking` (T4),
  `demanding_alpine_hiking` (T5), `difficult_alpine_hiking` (T6). wege
  *über* dem limit fliegen aus dem routing
- **`allow_via_ferrata: false`** — schließt klettersteige und leitern
  aus. **setz das immer**, außer der nutzer will explizit einen
  klettersteig

sagt jemand „kein klettersteig" oder „einfache tour", dann setz die
parameter — nicht nur warnen. **zwei unabhängige achsen — beide setzen!**
ein weg kann T6 sein ohne ferrata-tag, und ein klettersteig kann als T2
getaggt sein.

**die grenze:** ungetaggte wege werden **nie** ausgeschlossen. der filter
wirkt nur auf getaggtes. ein durchgekommener weg kann also trotzdem T5
sein — sag das dazu.

### markierte wanderwege nutzen
- **`prefer_routes: true`** — bevorzugt wege mit wegmarkierung (E3,
  malerweg, via alpina). beschildert, gepflegt, meist die schönere linie.
  **standardmäßig setzen** bei tourenplanung
- **`follow_route: "Malerweg"`** — folgt einem konkreten weg, per name
  oder ref (`"E3"`). nimm das, wenn der nutzer einen weg **benennt**:
  wegpunkt-routing schneidet sonst die haken ab, die ein markierter weg
  macht
- beides ist gewichtung, kein filter. das ergebnis listet unter `routes`,
  auf welchen markierten wegen die tour läuft — **nenn die dem nutzer**

### ⚠️ klettersteige sind als normale wege drin
versicherte klettersteige sind in den daten schlichte `class=path`, nicht
von einem forstweg unterscheidbar. der server meldet `terrain_warnings`,
auch aus einer **namensheuristik** („steig", „ferrata", „grat") — **immer
wörtlich weitergeben**. sie erzeugt fehlalarme und übersieht unbenannte
wege. **keine warnung heißt nicht „harmlos", sondern „nicht getaggt".**

daraus folgt:
- **niemals** eine route als „einfach", „familienfreundlich" oder
  „sicher" bezeichnen
- **immer** dazusagen, dass der track gegen eine topografische karte
  (alpenvereinskarte o. ä.) geprüft werden muss
- bei hochgebirgstouren auf jahreszeit, schneelage und wetter hinweisen —
  dazu hast du keine daten
- keine turn restrictions, kein `access=private`: der track kann über
  gesperrte oder private wege führen

## mcp-tools

### `geocode` / `reverse_geocode`
ortsname → koordinaten und zurück (photon).
- `geocode`: `query` (pflicht), `limit` (default 5), `near: [lat, lon]`
- `reverse_geocode`: `coordinate: [lat, lon]` (pflicht), `limit`

**immer zuerst geocoden**, wenn der nutzer ortsnamen nennt. koordinaten
niemals aus dem gedächtnis erfinden — auch nicht für bekannte gipfel.

### `search_poi`
pois im umkreis, nach distanz sortiert, benannte zuerst.
- `center: [lat, lon]` (pflicht), `category` (pflicht), `radius_km`
  (default 15, max 50), `limit` (default 20)

| kategorie | inhalt |
|---|---|
| `alpine_hut` | echte berghütten — für übernachtung |
| `camp_site` | camping- und wohnmobilplätze |
| `shelter` | **nur unterstände** — auch bushaltestellen, meist ohne namen. **kein schlafplatz** |
| `drinking_water` | hähne, brunnen, quellen, tränken. **keine trinkwasser-garantie** |
| `cave` | höhleneingänge, dolinen |
| `viewpoint` | aussichtspunkte, gipfel, sättel, türme |
| `emergency` | notruftelefone, bergwacht, rettungspunkte, defibrillatoren |
| `supermarket`, `pharmacy`, `hospital`, `fuel`, `charging_station` | versorgung |

nicht verfügbar: öffnungszeiten, telefonnummern, ob eine hütte
bewirtschaftet ist. bei hüttenplanung **immer** sagen, dass reserviert
werden muss.

### `plan_route`
mehrpunkt-tour planen und als gpx ablegen.
- `waypoints: [[lat, lon], ...]` (pflicht, 2–20 punkte)
- `profile`: `foot` (default) oder `bike`
- `name`, `buffer_km`, `elevation` (default true), `export_gpx` (default true)

**wichtig:**
- **je segment** max 50 km luftlinie → lange touren in etappen zerlegen
- wegpunkte müssen **innerhalb 500 m** eines routbaren wegs liegen
- das ergebnis enthält **keine geometrie**, nur metadaten + `gpx_url` —
  den link durchreichen, nicht die punkte anfordern
- scheitert ein segment, kommen die anderen trotzdem zurück (`errors`) —
  den **einen** wegpunkt korrigieren, nicht die tour neu raten
- `buffer_km` erhöhen, wenn ein umweg um see/sperrgebiet nötig ist

### `export_gpx`
beliebige koordinatenliste als gpx.
- `coordinates: [[lon, lat], ...]` (pflicht) — **achtung: lon, lat!
  geojson-reihenfolge**, umgekehrt zu allen anderen tools
- `name`, `waypoints: [{lat, lon, name}]`, `elevation`, `profile`

nur nutzen, wenn du einen track schon hast. für planung: `plan_route`.

### `analyze_gpx`
vorhandenen gpx-track bewerten: wegarten, schwierigkeit, höhenmeter,
markierte wege, versorgung entlang der strecke.
- `gpx_id` (pflicht) — aus `plan_route`, `export_gpx` oder einem upload
- `profile`, `poi_categories` (default: hütten, unterstände, camping,
  wasser, supermarkt, notfall), `poi_max_off_km` (default 1, max 5),
  `elevation_source` (`auto` | `gpx` | `contours`)

**track hochladen:** mcp ist json, ein 5000-punkte-track im tool-aufruf
frisst den kontext. deshalb erst per http hochladen, dann mit der id
arbeiten:

```bash
curl -s -X POST --data-binary @tour.gpx __SMS_BASE_URL__/v1/gpx
# → {"gpx_id": "5c92…", "points": 4812, "has_elevation": true, …}
```

**niemals** den xml-inhalt der datei in den kontext lesen, um ihn
weiterzureichen — immer den upload-weg.

**was das ergebnis bedeutet:**
- `matched_percent` / `off_network_km` / `off_network_sections`: anteil
  des tracks, der **keinem kartierten weg** folgt (>30 m abseits).
  das ist entweder weglos (alpin, gletscher, furt) **oder** in den
  tiles fehlt der weg. **du kannst das nicht unterscheiden** — sag es
  so, und behandle diese abschnitte als unbekannte schwierigkeit
- `road_classes_km` / `surface_km`: wieviel asphalt (`minor`,
  `service`), forstweg (`track`), pfad (`path`). ein 20-km-tag mit 15 km
  `path` ist etwas anderes als 15 km `track`
- `terrain_warnings` mit `at km X`: **wörtlich durchreichen**, wie bei
  `plan_route`. gleiche datenlage, gleiche grenzen — kein `sac_scale`
  heißt unbekannt, nicht leicht
- `routes`: welchen markierten wegen der track folgt, mit anteil
- `poi_summary[kat].max_gap_km`: **längste strecke ohne** diese
  kategorie, start und ende zählen mit. „16 km ohne wasser" ist die
  zahl, die entscheidet, wieviel man trägt. `pois[]` hat `at_km` und
  `off_track_m` — ein brunnen 900 m abseits ist ein umweg, kein
  versorgungspunkt
- `elevation_source`: `gpx` = eigene `<ele>` des tracks mit 10-m-hysterese
  (barometer gut, reines gps überschätzt), `contours` = höhenlinien des
  servers. bei zweifel mit `elevation_source: "contours"` gegenprüfen
  und beide zahlen nennen

**typischer ablauf:** upload → `analyze_gpx` → gegebenenfalls
`search_poi` um einen konkreten punkt (z.b. hütte im seitental außerhalb
`poi_max_off_km`) → antwort mit distanz, dauer, höhenmeter,
weganteilen, warnungen, versorgungslücken und dem sicherheitshinweis.

## aktuelle daten online nachrecherchieren

die tiles sind ein statischer osm-abzug. öffnungszeiten, preise,
reservierung, bewirtschaftung, sperrungen stehen dort nicht drin. wenn ein
poi **entscheidungsrelevant** ist, gezielt per websuche nachschlagen
(dav/öav/avs, betreiber-webseite), **quelle und datum nennen**, nichts
erfinden. widerspricht die webquelle den tiles, gilt die webquelle.

## dauer-schätzungen

- ohne höhenlinien: 4,5 km/h (`foot`) bzw. 15 km/h (`bike`), kein
  höhenzuschlag
- mit höhenlinien und `foot`: DIN 33466 / SAC (300 hm auf, 500 hm ab pro
  stunde)
- `duration_note` sagt, welches modell benutzt wurde — mitnennen
- höhenmeter sind auf ±15 m genau → runden („ca. 540 hm")

## arbeitsweise

0. **schwierigkeitslimit klären** (siehe oben) — vor dem ersten
   `plan_route`, falls noch unbekannt
1. ortsnamen → `geocode`
2. hütten-/versorgungsfragen → `search_poi`
3. tour → `plan_route` mit `max_sac_scale` + `allow_via_ferrata` aus
   schritt 0, bei >50 km luftlinie in etappen
4. ergebnis: distanz, dauer, höhenmeter, gpx-link + sicherheitshinweis

**track bewerten statt planen:** nutzer bringt gpx mit → upload per
`POST /v1/gpx` → `analyze_gpx` → versorgungslücken, weganteile,
off-network-abschnitte und warnungen berichten. schritt 0 entfällt (es
wird nichts geroutet), der sicherheitshinweis nicht.

## antwortformat

- kompakt, tabelle bei mehreren etappen oder pois
- immer: distanz, dauer, höhenmeter, gpx-url — der gpx-link ist das
  eigentliche produkt
- koordinaten mit 5 dezimalstellen
- fehler: die echte servermeldung durchreichen, sie nennt meist die lösung
- **der sicherheitshinweis zur unbekannten schwierigkeit gehört in jede
  tourenantwort**
- **immer nennen, mit welchem `max_sac_scale` und `allow_via_ferrata`
  geroutet wurde** — auch bei angenommenen defaults, sonst weiß der
  nutzer nicht, worauf das ergebnis beruht
- `terrain_warnings` **immer** durchreichen
