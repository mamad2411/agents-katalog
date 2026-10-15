---
name: playwright-scraper-skill
description: Playwright-based web scraping skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk.
version: 1.2.0
author: Simon Chan
---

# Playwright Scraper Skill

A Playwright-based web scraping skill with anti-bot protection. Choose the best approach based on the target website's anti-bot level.

---

## 🎯 Use Case Matrix

| Target Website | Anti-Bot Level | Recommended Method | Script |
|---------------|----------------|-------------------|--------|
| **Regular Sites** | Low | web_fetch tool | N/A (built-in) |
| **Dynamic Sites** | Medium | Playwright Simple | `scripts/playwright-simple.js` |
| **Cloudflare Protected** | High | **Playwright Stealth** ⭐ | `scripts/playwright-stealth.js` |

---

## 📦 Installation

```bash
cd playwright-scraper-skill
npm install
npx playwright install chromium
```

---

## 🚀 Quick Start

### 1️⃣ Simple Sites (No Anti-Bot)

Use built-in `web_fetch` tool for static sites.

---

### 2️⃣ Dynamic Sites (Requires JavaScript)

Use **Playwright Simple**:

```bash
node scripts/playwright-simple.js "https://example.com"
```

---

### 3️⃣ Anti-Bot Protected Sites (Cloudflare etc.)

Use **Playwright Stealth**:

```bash
node scripts/playwright-stealth.js "https://m.discuss.com.hk/#hot"
```

**Features:**
- Hide automation markers (`navigator.webdriver = false`)
- Realistic User-Agent (iPhone, Android)
- Random delays to mimic human behavior
- Screenshot and HTML saving support

---

## 📖 Script Descriptions

### `scripts/playwright-simple.js`
- **Use Case:** Regular dynamic websites
- **Speed:** Fast (3-5 seconds)
- **Anti-Bot:** None
- **Output:** JSON (title, content, URL)

### `scripts/playwright-stealth.js` ⭐
- **Use Case:** Sites with Cloudflare or anti-bot protection
- **Speed:** Medium (5-20 seconds)
- **Anti-Bot:** Medium-High (hides automation, realistic UA)
- **Output:** JSON + Screenshot + HTML file
- **Verified:** 100% success on Discuss.com.hk

---

## 🔧 Customization

All scripts support environment variables:

```bash
# Set screenshot path
SCREENSHOT_PATH=/path/to/screenshot.png node scripts/playwright-stealth.js URL

# Set wait time (milliseconds)
WAIT_TIME=10000 node scripts/playwright-simple.js URL

# Enable headful mode (show browser)
HEADLESS=false node scripts/playwright-stealth.js URL

# Save HTML
SAVE_HTML=true node scripts/playwright-stealth.js URL

# Custom User-Agent
USER_AGENT="Mozilla/5.0 ..." node scripts/playwright-stealth.js URL
```

---

## 🛡️ Anti-Bot Techniques Summary

### ✅ Effective Anti-Bot Measures
1. **Hide `navigator.webdriver`** — Essential
2. **Realistic User-Agent** — Use real devices (iPhone, Android)
3. **Mimic Human Behavior** — Random delays, scrolling
4. **Avoid Framework Signatures** — Crawlee, Selenium are easily detected
5. **Use `addInitScript` (Playwright)** — Inject before page load

### ❌ Ineffective Anti-Bot Measures
1. **Only changing User-Agent** — Not enough
2. **Using high-level frameworks (Crawlee)** — More easily detected
3. **Docker isolation** — Doesn't help with Cloudflare

---

## 🔍 Troubleshooting

### Issue: 403 Forbidden
**Solution:** Use `playwright-stealth.js`

### Issue: Cloudflare Challenge Page
**Solution:**
1. Increase wait time (10-15 seconds)
2. Try `headless: false` (headful mode sometimes has higher success rate)
3. Consider using proxy IPs

---

## 📚 References

- [Playwright Official Docs](https://playwright.dev/)
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)