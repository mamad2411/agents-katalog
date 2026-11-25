---
name: url2png
description: Convert URL to PNG suitable for mobile reading.
metadata: {"openclaw":{"always":false,"emoji":"🦞","homepage":"https://clawhub.ai/guoqiao/url2png","os":["darwin","linux"],"requires":{"bins":["uv"]}}}
triggers:
- "/url2png <url>"
- "Save this url as image ..."
- "Take long screenshot for this url"
---

# URL to PNG

Given a url for a webpage, convert it to png suitable for mobile view.

See [examples](https://github.com/guoqiao/skills/tree/main/url2png/examples)


## Requirements

- `uvx`

## Installation

```bash
bash ${baseDir}/install.sh
```

The script will:

- install `shot-scraper` as uv tool
- install `chromium` browser module for shot-scraper/playwright

## Usage

```bash
bash ${baseDir}/url2png.sh "${url}"
```
Path to png will be printed to stdout.

## Agent Instructions

1. Execute the `url2png.sh` script with url as an argument.
2. The script will output a path to a png file.
3. Send the file to the user. **Crucial:** To avoid compression or dimension limits (especially on Telegram), send the image as a **document/file**, do not send as a photo.
