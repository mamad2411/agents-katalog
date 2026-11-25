---
name: kompetansemaal-mot-kapittel
description: "Skille kompetansemål (Udir) fra kapittel (læreverk). Bruk ALLTID når eleven, læreren eller du selv blander 'mål', 'kapittel', 'tema', 'huke av læreplanen', eller spør hva som skal øves. Trigger på 'hva er forskjellen på kompetansemål og kapittel', 'er dette et mål', 'hvilket kapittel', 'huk av', 'læreplanen'."
---

# Kompetansemål mot kapittel

Dette er tre lag. Bland dem aldri.

| Lag | Hva det er | Hvem eier det | Hva du gjør med det |
|---|---|---|---|
| Kompetansemål | Offisiell formulering av hva eleven skal kunne | Udir, via `hent_lareplan` | Vurder og dekk. Huk **ikke** av. |
| Kapittel | Hvordan læreverket deler opp året | Lokal `kapitler.json` og `kapittel` på temaene | Les, noter, øv i rekkefølge. Huk **ikke** av mål. |
| Tema | Det dere faktisk hører | Lokal `temaer.json` | Ett spørsmål, én karakter, append-only høring. |

## Forskjellen som teller

Et **kompetansemål** er et vurderingskrav. Sensor, eksamen og standpunkt forholder seg til Udir-teksten, ikke til kapittelnavnet i boka.

Et **kapittel** er en arbeidsinndeling. «Markedsundersøkelser» er et kapittel. Målet det peker på, er for eksempel *bruke og utvikle markedsundersøkelser for å utforske og få innsikt i markeder og målgrupper* (`male1-04` / KM6175).

Ett kapittel treffer ofte **flere** kompetansemål. Ett kompetansemål dekkes av **flere** temaer, gjerne spredt over kapitler senere.

Dekning på et mål er **avledet**: siste karakter per tema som er koblet til målet. Du huker aldri av et kompetansemål fordi kapittelet er «ferdig».

## Arbeidsflyt

1. Bekreft `fagId` (`velg-fag-forst`).
2. Kall `hent_lareplan` når spørsmålet handler om hva som skal kunne.
3. Kall `list_kapitler` når spørsmålet handler om hvor i boka dere er.
4. Kall `list_temaer` for å høre. Hvert tema har `kapittel` og `maalIds`.
5. Når du stiller spørsmål: si både kapittelet og kompetansemålet. Ikke bare kapittelnavnet.
6. Logg på **temaet**, ikke på kapittelet og ikke på målet.

## MCP-verktøy

- `hent_lareplan` — kompetansemål
- `list_kapitler`, `hent_kapittel` — kapitler med notater, øving og temaer
- `list_temaer` — temaer med `kapittel` og `maalIds`
- `still_sporsmal` — ett tema, med målene det treffer

## Ikke

- Ikke behandle et kapittelnavn som et kompetansemål.
- Ikke si at et mål er dekket fordi kapittelet er lest.
- Ikke finn på Udir-mål. Hent dem.
- Ikke flytt en høring til et annet fag fordi kapitteltittelen ligner.
