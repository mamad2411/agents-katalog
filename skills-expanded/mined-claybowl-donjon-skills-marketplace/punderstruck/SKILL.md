# punderstruck

A “pun discovery” skill that queries Datamuse in real time for phonetic collisions (sounds-like, homophones, compound splits), then constructs candidates using a punchline-first method and scores each on 5 criteria (25-point scale). It only serves puns scoring ≥17/25; if none clear the bar it “digs deeper” instead of shipping mediocre wordplay.

## Triggers
- "make a pun"
- "generate pun"
- "pun discovery"
- "wordplay"
- "dad joke"
- "pun generator"

## Description
This skill creates original puns by querying the Datamuse API for phonetic relationships and constructing punchline-first candidates. It evaluates puns on a 25-point scale across 5 criteria and only delivers puns scoring 17/25 or higher. If no puns meet the threshold, it continues searching rather than delivering subpar wordplay.

## Features
- Topic-focused puns
- "Roast" heat levels 1-4
- Jargon-to-wordplay "translate"
- Quote/lyric "remix"
- Multi-format "compose" (haiku/limerick/sonnet/etc.)
- "Explain" mode that dissects the mechanics after delivering the pun

## Usage
Use when you need clever, original wordplay or puns for content creation, social media, or lightening the mood in technical discussions.

## Example
```
/punderstruck make a pun about artificial intelligence
/punderstruck roast level 3 about blockchain developers
/punderstruck explain why "time flies like an arrow" is funny
```
