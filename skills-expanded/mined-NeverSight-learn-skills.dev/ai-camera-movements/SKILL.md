---
name: ai-camera-movements
description: Extract the complete AI Camera Movements library with categories, prompts, preview videos, and posters.
host: aicameramovements.com
trusted: false
source: agent
version: 1.0.0
args: []
triggers:
  - scrape AI Camera Movements
  - extract the camera movement prompt library
  - get prompts from aicameramovements.com
  - list AI camera moves and prompts
  - pull the camera movement reference library
---

# AI Camera Movements scraper

Reads the public library at https://aicameramovements.com/ and returns every movement in page order. Output is JSON with source, items, and count; each item contains ordinal, code, name, category, prompt, video, and poster.

## Usage

```
$ $B skill run ai-camera-movements
{ "source": "https://aicameramovements.com/", "items": [...], "count": 46 }
```
