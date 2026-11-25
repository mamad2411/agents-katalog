---
name: tg-miniapp-fastbuild
description: Deploy a Telegram Mini App to production with BotFather, GitHub, and Railway (React + Vite frontend, Node.js + Express + Telegraf backend, PostgreSQL), including bilingual bot copy and share links. Use when creating, deploying, or debugging a Telegram Mini App or its Railway, webhook, or share-link setup.
---

# tg-miniapp-fastbuild

A step-by-step guide for taking a Telegram Mini App to production with Railway, GitHub, and BotFather. It comes from a real deployment, and the gotchas section lists what went wrong there.

---

## What This Skill Does

Guides an AI agent (or developer) through the complete process of deploying a Telegram Mini App from zero to production, covering:

- Telegram Bot creation via BotFather
- GitHub repo setup
- Railway deployment (frontend + backend + PostgreSQL as separate services)
- Webhook registration
- Multi-language Bot copy

---

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite |
| Backend | Node.js + Express + Telegraf |
| Database | PostgreSQL |
| Hosting | Railway |
| CI/CD | GitHub → Railway auto-deploy |

---

## Project Structure

```
project-root/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── data/
│   │   └── hooks/
│   ├── railway.json      ← build config, use npm install NOT npm ci
│   └── package.json
├── backend/
│   ├── src/
│   │   └── index.js
│   └── package.json
```

**Critical:** Frontend and backend must be deployed as separate Railway services, each with their own Root Directory setting.

---

## Deployment Flow

```
BotFather → GitHub → Railway (PostgreSQL) → Railway (Backend) → Railway (Frontend) → BotFather (Menu Button)
```

### Step 1: Create Bot

```
BotFather → /newbot → save Token immediately
```

- Token is shown only once
- @username cannot be changed after creation
- `Edit Name` only changes display name, not @handle

### Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main
```

Create repo as **Private**. Do not initialize with README or .gitignore.

### Step 3: Railway — PostgreSQL

`New Project` → `Empty Project` → `+ New` → `Database` → `Add PostgreSQL`

Copy `DATABASE_URL` from the database Variables tab.

### Step 4: Railway — Backend

`+ New` → `GitHub Repo` → select repo → `Settings` → `Source` → `Add Root Directory` → `backend`

**Environment variables:**

| Key | Value |
|-----|-------|
| `DATABASE_URL` | copied from PostgreSQL |
| `BOT_TOKEN` | from BotFather |
| `FRONTEND_URL` | `http://localhost:3000` (update later) |
| `MINI_APP_URL` | `http://localhost:3000` (update later) |
| `WEBHOOK_URL` | leave empty (update later) |
| `SKIP_VERIFY` | `false` |

After deploy goes green → `Settings` → `Networking` → `Generate Domain` → save URL.

### Step 5: Railway — Frontend

`+ New` → `GitHub Repo` → same repo → Root Directory → `frontend`

**Environment variables:**

| Key | Value |
|-----|-------|
| `VITE_API_URL` | backend Railway URL |
| `VITE_BOT_USERNAME` | bot username without @ |

After deploy goes green → Generate Domain → save URL.

### Step 6: Update Backend Variables

| Key | Update to |
|-----|-----------|
| `FRONTEND_URL` | `https://FRONTEND.up.railway.app` |
| `MINI_APP_URL` | `https://FRONTEND.up.railway.app` |
| `WEBHOOK_URL` | `https://BACKEND.up.railway.app` |

Railway auto-redeploys. Check Deploy Logs for:
```
[bot] Webhook registered: https://BACKEND.up.railway.app/bot/webhook
```

### Step 7: BotFather — Menu Button

```
/mybots → select bot → Bot Settings → Menu Button → Configure menu button
```

1. Send URL first: `https://FRONTEND.up.railway.app`
2. Send button label second: `✦ Open [App Name]`

BotFather asks URL first, label second — order matters.

---

## Code Templates

### /start Command (bilingual)

```javascript
bot.command('start', async (ctx) => {
  const lang = ctx.from?.language_code?.startsWith('ru') ? 'ru' : 'en'

  const copy = {
    en: {
      message: "Your welcome message here.",
      button: "Open App",
    },
    ru: {
      message: "Ваше приветственное сообщение.",
      button: "Открыть",
    },
  }

  await ctx.reply(copy[lang].message, {
    reply_markup: {
      inline_keyboard: [[
        { text: copy[lang].button, web_app: { url: process.env.MINI_APP_URL } }
      ]]
    }
  })
})
```

### Webhook Registration

```javascript
await bot.telegram.setWebhook(`${process.env.WEBHOOK_URL}/bot/webhook`)
```

### Bilingual State Architecture (React)

```javascript
const [lang, setLang] = useState(null)       // 'en' | 'ru' | etc.
const [page, setPage] = useState('language') // start at language selection

const langData = lang === 'ru'
  ? { questions: questionsRu, types: typesRu, ... }
  : { questions: questionsEn, types: typesEn, ... }
```

### Share Link Format

```javascript
// Always use this format — other formats redirect to telegram.org
const shareUrl = `https://t.me/${BOT_USERNAME}/app`
```

---

## Gotchas (Read Before You Start)

| Issue | Cause | Fix |
|-------|-------|-----|
| `PORT variable must be integer` | Manually set PORT in Railway | Delete PORT from Variables — Railway injects it automatically |
| `Cannot find module 'dotenv'` | dotenv in devDependencies | Move to dependencies, push again |
| `npm ci` fails — lock file out of sync | package-lock.json not committed | Run `npm install` locally, commit the updated lock file |
| `EBUSY: resource busy or locked` | Railway build cache conflict | Change `npm ci` to `npm install` in `railway.json` |
| Bot /start no response | Webhook not registered | Check WEBHOOK_URL includes `https://` |
| Share link opens telegram.org | Wrong link format | Use `https://t.me/BOT_NAME/app` only |
| Desktop Telegram can't open link | Platform limitation | Expected behavior — works in browser and mobile |
| `Root Directory` field not visible | Wrong Settings section | It's under `Source`, not `Build` |

---

## Post-Deploy Checklist

- [ ] `/start` returns welcome message + button
- [ ] Button opens Mini App on mobile
- [ ] All question pages render correctly
- [ ] Result page shows correct language content
- [ ] Share link opens Mini App (not telegram.org)
- [ ] Restart flow returns to language selection
- [ ] No horizontal overflow at 375px viewport
- [ ] Railway frontend + backend both show Active (green)

---

## Platform Support

| Platform | Mini App Support |
|----------|----------------|
| Telegram mobile (iOS/Android) | ✅ Full support |
| Browser (via link) | ✅ Redirects to Telegram Web |
| Telegram Desktop (Windows/Mac) | ❌ Not supported |
| Telegram Web (web.telegram.org) | ✅ Supported |

Desktop limitation is a Telegram constraint — not fixable.

---

## Ongoing Maintenance

- **Deploy updates:** push to `main` → Railway auto-deploys
- **Update env vars:** Railway console → Variables → save → auto-redeploy
- **Check build errors:** Deployments → View Logs → Build Logs
- **Check runtime errors:** Deployments → View Logs → Deploy Logs
- **Database URL:** internal Railway address, not exposed externally, safe
