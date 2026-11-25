---
name: astrology-engine
description: Compute reproducible Western, Vedic, relationship and location astrology locally with explicit profiles and uncertainty.
version: 4.0.0
---

# Astrology Engine agent skill

Use the installed `astroengine` CLI, `python -m astroengine` from the repository,
or Python `astroengine.agent.run_tool(name, parameters)`. No provider/API key is
required. This manifest is checked in; deployment to a host agent's skill registry
is a separate installation action, not claimed by its presence here.

## Discover before selecting a method

Run `astroengine capabilities` for availability and `astroengine tools` for full
JSON request schemas. Planned/research/legacy states are not new safe-path methods.
Twenty-six computation tools currently exist: chart, vedic, vargas, dashas,
panchanga, relationship (CLI alias synergy-json), location, western, runic,
wheel, solar-arc, profection, watch, elect, stars, asteroids, midpoints,
draconic, dossier, chinese-tibetan-other, forecast, mantras, yogas,
shadbala, ashtakavarga and jaimini. Catalog schemas and
Python routing are local contracts, not an already-running MCP/HTTP server.

## Required input and profiles

Ask for birth/event date, civil time if known, coordinates and explicit IANA
zone/UTC. City-only input needs a separate confirmed geocoding step. Never assume
London, UTC or coordinates (0,0). Unknown time can use flagged local-noon positions;
angles/houses/profections are omitted and location analysis refuses. DST fold/gap
requires a known UTC instant. Carry warning metadata into the interpretation.

Jyotisha tools default to sidereal/Lahiri/whole-sign/mean nodes, with explicit
supported ayanamsa/node variants. General chart/Western/relationship/location
commands default to tropical/Placidus/true nodes. Two births have independent
coordinates, zones and certainty. Do not mix zodiac frames or node conventions.

## Computation then interpretation

Always compute positions; never fabricate coordinates or unsupported methods.
Check exit status before parsing JSON; stdout is a successful result only. Exit 2
has stderr JSON for calculation failures (argparse syntax errors use normal text).
Use the returned request, UTC, backend flags and method to explain provenance.
Position precision is not independent accuracy certification.

Treat interpretations as symbolic and non-deterministic. Synergy is a versioned
modern heuristic with traceable contributions, not a compatibility probability.
Norse correspondences are an optional modern cultural overlay, not reconstructed
historical astrological practice. Keep traditional school disagreements visible.
The runic tool implements Pennick (2023) as a modern synthesis: lunar mansions use
the declared Alcyone-anchor convention, and the Ch. 8 interpretive statements are
labeled as interpretation, never presented as computed fact. The
chinese-tibetan-other tool covers the Oracles program's Eastern arts — Chinese
zodiac (ganzhi year anchored 1984 = Jia-Zi, NaYin, allies/clashes, Lunar New Year
boundaries), Four Pillars/BaZi (year turning at Lichun, jie month branches via
ephemeris, day ganzhi from verified anchors), Tibetan astrology (element-animal
year, rabjung, mewa, parkha, five forces with lineage variation disclosed) — plus
Younger Futhark, Anglo-Saxon futhorc and Ogham readings. Calendrical anchors are
cross-checked against published tables rather than recalled.

## Scope boundaries

Vargas: sixteen named classical sign mappings, including unequal D30; variants
and the source D27 discrepancy are documented. Vimshottari: maha/antar timelines
with explicit year clock; antars anchor before birth. Panchanga: instant elements,
civil weekday, no sunrise vara/calendar/festivals yet. Location: relocation and
geometric angular longitudes at an exact latitude, not kilometer distances or
parans. Western: civil annual profection, integer harmonics and sensitive midpoints.

Shadbala, ashtakavarga, yoga/dosha engines, Jaimini/KP, alternate dashas, muhurta
and further techniques remain in ROADMAP. Do not report
that all astrology or all Jyotisha has already been implemented.

Legacy text compatibility now validates inputs and suppresses unknown-time houses.
It reports actual planetary backends and optional missing-body warnings, but raw
event search/approximate location math still need migration. Prefer structured
methods when available and keep capability states/evidence in the report.
