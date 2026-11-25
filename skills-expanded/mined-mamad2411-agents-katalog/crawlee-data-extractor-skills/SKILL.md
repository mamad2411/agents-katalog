---
name: crawlee-data-extractor-skills
description: Enterprise-grade web scraping and data extraction skill powered by Crawlee. Features anti-blocking stealth browsers, proxy rotation, and structured JSON output for dynamic web apps.
---

# 🌟 Crawlee Data Extractor Skill

## Overview
A powerful, stealthy web crawler built on top of [Crawlee](https://crawlee.dev/). It is designed to handle modern, complex websites (SPA, React/Vue) that aggressively block simple HTTP requests. It uses full browser automation (Playwright/Puppeteer under the hood) disguised as a real user to scrape data cleanly into JSON.

## Features
- **Anti-Blocking Engine:** Uses `PlaywrightCrawler` with stealth plugins to bypass simple bot protections.
- **Auto Resource Scaling:** Automatically manages concurrency and memory limits.
- **Smart Retries:** Fails gracefully and retries on timeouts.
- **Headless Mode:** Runs seamlessly in background environments with virtual framebuffers (Xvfb).

## Prerequisite Setup
Since this utilizes the Crawlee Node.js ecosystem, ensure dependencies are installed the first time you run this:
```bash
cd scripts/
npm install crawlee playwright
npx playwright install chromium
```

## Basic Usage

The core script is `scrape.js` located in the `scripts/` folder. It expects a target URL and an output filename.

```bash
node scripts/scrape.js --url "https://news.ycombinator.com/" --output "/tmp/data.json"
```

## Agentic Workflows
For an LLM or Agent, you should invoke this skill whenever the user asks to "scrape", "extract", or "crawl" a specific site, especially if the site relies heavily on JavaScript rendering. After running the tool, read the resulting JSON file and process the data as requested.
