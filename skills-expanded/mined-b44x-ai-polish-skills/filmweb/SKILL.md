---
name: filmweb
display_name: Filmweb
version: 1.0.0
description: >-
  Fetch film and TV series data from Filmweb.pl: search by title, rating and number
  of votes, critics rating, genres, duration, directors, cast, plot, premiere dates,
  where to watch (VOD providers and prices) and actor details. Use whenever the user
  asks about a movie or series on Filmweb, pastes a filmweb.pl link, or wants a Polish
  rating, opis, obsada or VOD info, e.g. "ile Matrix ma na Filmwebie", "kto grał w…",
  "kto wyreżyserował…", "o czym jest…", "gdzie obejrzę…", "kiedy premiera…",
  "jaki serial…", "ocena serialu…".
category: entertainment
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: Filmweb.pl
source_type: unofficial_api
official: false
homepage: https://www.filmweb.pl
documentation: none
rate_limit: fair use
last_verified: 2026-09-28
tags:
  - filmweb
  - filmy
  - seriale
  - kino
  - vod
  - recenzje
  - obsada
compatibility: Python 3.8+ (standard library only); network access to www.filmweb.pl.
---

# Filmweb

Fetches data from the JSON API behind www.filmweb.pl using a small dependency-free
Python CLI, `scripts/filmweb.py`, that always prints JSON.

## Running the script

Run from this skill's directory. Use whichever Python launcher exists:

| OS | Command |
|---|---|
| Linux / macOS | `python3 scripts/filmweb.py <command> …` |
| Windows | `py scripts/filmweb.py <command> …` (or `python`) |

No installation step is needed.

## Workflow

1. **Get the Filmweb ID.**
   - The user gave a link → `filmweb.py id "<url>"` (offline).
     The ID is the trailing number of the slug: `filmweb.pl/film/Matrix-1999-628` → `628`,
     `filmweb.pl/serial/Gra+o+tron-2011-476848` → `476848`.
   - The user gave a title → `filmweb.py search "<title>"`. Results are ordered by relevance.
     Add `--type=serial` when the user clearly means a TV series (or `--type=film` for a movie).
     If several titles plausibly match (remakes, sequels, film vs. series), check them with
     `film` and pick by year, or ask the user.
2. **Fetch only what the question needs.**
   - rating, genres, director, short plot → `film`
   - "who played in…" → `cast` (`film` already has the two main actors)
   - "where can I watch…" → `vod`
   - "when is the premiere…" → `dates`
   - full plot → `description`; details about a person → `person <personId>`
3. **Answer in the user's language** and cite the `url` from `film`. Round the rating to one
   decimal and mention the number of votes (e.g. "7,6/10 z 872 tys. ocen"). Give VOD prices in zł.

## Films and series

Films, TV series and games share one ID space on Filmweb, and **every command accepts
any of them** — use `film <id>` for a series too (e.g. `film 476848` for "Gra o tron").
Check `type` in the output (`film`, `serial`, …). For series, `year` is the first season
and `duration` is the length of one episode, not the whole series.

## Commands

| Command | Returns |
|---|---|
| `search "<query>" [--type=film\|serial\|game] [--limit=10]` | list of `{id, type, title, mainCast}` |
| `film <id\|url>` (film or series) | title, originalTitle, year, type, url, posterUrl, rating, votesCount, votesDistribution, criticsRating, genres, countries, duration, directors, mainCast, plot |
| `description <id\|url>` | full plot description |
| `cast <id\|url> [--limit=10]` | top-rated roles: personId, name, profession, roleRating |
| `dates <id\|url>` | worldPremiere, worldRelease, polandRelease, polandReissue |
| `vod <id\|url>` | where to watch: provider, link, availability, offers (subscription / free / rent / buy + price in PLN) |
| `person <personId>` | name, realName, birthDate, birthplace, height, profession, photoUrl, knownForIds, url |
| `id <url>` | `{"id": …}`, offline |

Field reference: [references/output.md](references/output.md).

## Exit codes

JSON goes to stdout; errors go to stderr as `{"error": "...", "type": "..."}`.

| Code | Meaning | What to do |
|---|---|---|
| `0` | success | use the JSON |
| `2` | not found | tell the user; double-check the ID |
| `64` | bad usage | fix the arguments |
| `69` | Filmweb / network error | retry once; if it persists, use the fallback |

## Fallback

The API is unofficial and may change or be blocked by the network. If the script keeps
failing with code `69`, or the user needs data it does not provide (character names, reviews,
comments, full crew), fetch the public page (`url` from `film`, or `https://www.filmweb.pl/film/<slug>-<id>`)
with a web-fetch tool or `curl` and read the data from it. Tell the user the data came from the web page.

## Rules

- Don't call `film` for every search hit "just in case"; check only the candidates you need.
- Don't invent data the script did not return.
