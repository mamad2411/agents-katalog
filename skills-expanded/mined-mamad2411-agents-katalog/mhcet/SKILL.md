# PrepMaster — Cursor IDE Context
# ─────────────────────────────────────────────────────────────
# Read this FULLY before touching any file. This project has
# specific patterns — breaking them creates subtle bugs.
# ─────────────────────────────────────────────────────────────

## PROJECT OVERVIEW
B2B/B2C EdTech SaaS for MHCET Law (5-Year LLB) exam preparation.
- Platform: PrepMaster (brand) / MHCET (project folder)
- Live URL: https://mhcet-azure.vercel.app
- Admin login: admin@mhcet.com (local password: set in seed / `changeAdminPassword.js` — do not commit real passwords)

## MONOREPO STRUCTURE
```
/
├── frontend/        ← Next.js 14 App Router (deployed on Vercel)
├── backend/         ← Express.js API (deployed on Railway)
├── docs/            ← CSV question banks, roadmap
├── railway.json     ← Railway deploy config
└── nixpacks.toml    ← Railway build config
```

## TECH STACK

### Frontend (`/frontend`)
- **Framework**: Next.js 14 (App Router, TypeScript)
- **Styling**: Vanilla CSS (`app/global.css`) — NO Tailwind, NO CSS Modules
- **State**: React hooks only — NO Redux, NO Zustand
- **API calls**: All to `process.env.NEXT_PUBLIC_API_URL` (set in `.env.local`)
- **Auth**: JWT stored in `localStorage` as key `token`
- **Key pages**:
  - `/tests` — browse & start mocks
  - `/tests/[testId]/take` — exam engine (server-synced timer)
  - `/results/[attemptId]` — post-exam results + AI explain
  - `/admin/*` — admin panel (tests, import, users, tenants, audit)
  - `/dashboard` — student analytics

### Backend (`/backend`)
- **Framework**: Express.js (ESM — `"type": "module"` in package.json)
- **DB**: PostgreSQL via `pg` pool → `/backend/src/db/pool.js`
- **Auth**: JWT middleware → `/backend/src/middleware/auth.js`
- **Queue**: BullMQ + Upstash Redis (ONLY for `/api/explain` — import is SYNC)
- **AI**: DeepSeek (`deepseek-chat`) via OpenAI-compatible SDK
- **Migrations**: Auto-run at startup via `runMigrations()` in `index.js`
- **Port**: 4000 (local), Railway sets PORT automatically

## ENVIRONMENT VARIABLES

### Backend (`.env` — NEVER commit)
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mhcet
JWT_SECRET=<generate a long random string; 32+ chars in production>
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=<from DeepSeek console; set only in backend/.env or Railway — never commit>
DEEPSEEK_MODEL=deepseek-chat
REDIS_URL=<Upstash or local Redis URL; see backend/.env.example>
CORS_ORIGIN=http://localhost:3000
PORT=4000
```

### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:4000
```

### Production env vars live in:
- **Vercel** dashboard → Environment Variables
- **Railway** dashboard → mhcet service → Variables

## DATABASE SCHEMA (key tables)
```sql
users          — id, email, password_hash, role (admin/student), plan
tenants        — id, name, slug (B2B institutes)
tests          — id, title, topic, duration_seconds, is_active, author_id (NULL=public); optional Markdown `general_instructions` / `general_instructions_hi` (pre-exam rules; admin-editable)
questions      — id, test_id, prompt, option_a..d, correct_option, subject, hint, official_explanation
attempts       — id, user_id, test_id, status (in_progress/submitted), score
answers        — id, attempt_id, question_id, selected_option
question_explanations — id, question_id, content_hash, answer, explanation, concept, example, model (AI cache)
audit_logs     — all admin actions
```

### Migrations
- Location: `/backend/src/db/migrations/`
- Format: `NNN_description.sql` (sequential numbers)
- Run: `npm run migrate` (in `/backend`) or auto on server start
- Latest: `016_tests_general_instructions.sql`
- ⚠️ NEVER edit existing migration files — always add a new one

## KEY PATTERNS TO FOLLOW

### 1. API Routes (backend)
```js
// Pattern: Router → middleware → handler → HttpError
import { HttpError } from '../utils/httpError.js';

router.get('/path', authMiddleware, async (req, res, next) => {
  try {
    // req.userId is set by authMiddleware (JWT sub)
    // req.userRole is 'admin' | 'student'
    const result = await pool.query('SELECT ...', [params]);
    res.json(result.rows);
  } catch (e) {
    next(e); // Always use next(e) — errorHandler middleware formats response
  }
});
```

### 2. Admin-only routes
```js
import { requireAdmin } from '../middleware/requireAdmin.js';
adminRouter.use(authMiddleware);
adminRouter.use(requireAdmin);
```

### 3. CSV Import — ALWAYS SYNCHRONOUS (no queue)
```js
// ✅ Correct — sync import (worker not running on Railway)
const result = await importQuestionsFromCSV(testId, csvText, userId);
res.json({ status: 'done', ...result });

// ❌ NEVER do this — BullMQ worker not deployed
queue.add('import', { csvText }); // Jobs never get picked up
```

### 4. AI Explain — Uses BullMQ queue (worker IS running via Upstash)
```js
// explain route queues job → Upstash Redis → Railway worker picks up
// Local dev: run `npm run worker` in /backend separately
```

### 5. Frontend API calls
```js
// Always use the api utility, not fetch directly
import { apiFetch } from '@/lib/api'; // handles token + base URL

// Auth header pattern
const token = localStorage.getItem('token');
fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/...`, {
  headers: { Authorization: `Bearer ${token}` }
});
```

### 6. Analytics filters
```sql
-- Personal mocks EXCLUDED from recommendations
WHERE t.author_id IS NULL  -- NULL = platform-wide public test
```

## CSV QUESTION FORMAT
Headers: `question,optionA,optionB,optionC,optionD,correct,subject,hint,explanation`
- Optional Hindi columns (any subset): `questionHi,optionAHi,optionBHi,optionCHi,optionDHi,hintHi,explanationHi` — imported into `questions.*_hi` fields; UI falls back to English when a Hindi cell is empty.
- `correct`: A, B, C, or D (uppercase)
- `subject`: exactly one of:
  - `Legal Aptitude`
  - `GK & Current Affairs`
  - `Logical Reasoning`
  - `English`
  - `Basic Math`
- `hint` and `explanation` are optional

Available CSVs in `/docs/`:
- `combined_150_questions.csv` — 150Q (30 per subject)
- `combined_120_questions.csv` — 120Q (24 per subject)
- `mock_gk_gs_60q_10min.csv` — 60 GK questions
- `section_csvs/` — individual subject CSVs (30Q each)

## DEPLOYMENT

### Local dev
```bash
# Terminal 1 — Backend API
cd backend && npm run dev   # runs on :4000

# Terminal 2 — Frontend
cd frontend && npm run dev  # runs on :3000

# Terminal 3 — BullMQ Worker (only needed for AI explain testing)
cd backend && npm run worker
```

### Production
- **Frontend**: Vercel auto-deploys on `git push origin main`
- **Backend**: Railway auto-deploys on `git push origin main`
- Backend URL: `https://mhcet-production-2e2a.up.railway.app`
- Frontend URL: `https://mhcet-azure.vercel.app`

### Production admin
- Password: set via `backend/scripts/changeAdminPassword.js`
- Set password via env when running the script (do not document real passwords in repo)

## CURRENT STATUS (as of April 2026)
- ✅ 3 public tests in production (after recreation)
- ✅ DeepSeek AI explanations working (local + production)
- ✅ Sync CSV import working (no worker needed)
- ✅ Analytics filters exclude personal mocks
- ✅ Footer hides Login/Signup for logged-in users
- ✅ Migration 014 applied (question_explanations cache table)
- ⚠️ AI explain on production needs REDIS_URL in Railway mhcet service

## THINGS TO NEVER DO
1. ❌ Don't edit `.env` files and commit them — they're gitignored
2. ❌ Don't use BullMQ queue for CSV imports (worker not running)
3. ❌ Don't modify existing migration SQL files — add a new one
4. ❌ Don't add Tailwind — project uses vanilla CSS
5. ❌ Don't use `console.log` in backend — use `logInfo`/`logWarn` from `./utils/logger.js`
6. ❌ Don't bypass `authMiddleware` on any non-public route
7. ❌ Don't hardcode the API URL — always use `process.env.NEXT_PUBLIC_API_URL`
