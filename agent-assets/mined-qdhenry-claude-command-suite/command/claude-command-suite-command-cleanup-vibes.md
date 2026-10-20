---
name: cleanup-vibes
description: Transform a vibecoded project into a properly structured, deployment-ready codebase with secrets extracted and organized folders
---

<objective>
Transform a vibecoded project into a clean, deployment-ready codebase. Vibecoded projects typically have hardcoded API keys, flat/disorganized folder structures, no .env files, and no documentation.

This command detects the project type (TypeScript, Python, or hybrid TS frontend + Python backend), reorganizes the folder structure following industry conventions, extracts all embedded secrets into .env files, and generates deployment-ready documentation.
</objective>

<context>
Project files: !`find . -maxdepth 1 -not -name '.' -not -name '.git' -not -name 'node_modules' -not -name '__pycache__' -not -name '.venv' -not -name 'venv' | head -40`
Package files: !`for f in package.json pyproject.toml requirements.txt setup.py Pipfile Cargo.toml; do [ -f "$f" ] && echo "$f"; done; true`
Current structure: !`find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*' -not -path '*/venv/*' -not -path '*/.next/*' -not -path '*/dist/*' -not -path '*/.DS_Store' | head -80`
Existing env files: !`ls -la .env* 2>/dev/null || echo "No .env files found"`
Existing gitignore: !`cat .gitignore 2>/dev/null || echo "No .gitignore found"`
</context>

<process>

## Phase 1: Project Detection

1. Analyze the project to determine its type:
   - **TypeScript/JavaScript**: Has `package.json`, `.ts`/`.tsx`/`.js`/`.jsx` files
   - **Python**: Has `requirements.txt`, `pyproject.toml`, `setup.py`, or `.py` files
   - **Hybrid**: Both present (Python backend + React/TS frontend)
2. Identify the framework(s) in use (Next.js, React, Express, FastAPI, Flask, Django, etc.)
3. Identify the entry points and main application logic

## Phase 2: Secret Extraction (Parallel Sub-Agents)

Deploy 3 parallel sub-agents using the Task tool to scan for embedded secrets:

**Agent 1 - Credential Scanner**: Scan ALL files for patterns matching:
  - API keys (`sk-`, `pk_`, `api_key`, `apiKey`, `API_KEY`, `Bearer `)
  - Auth tokens (`token`, `secret`, `password`, `credential`)
  - Database URLs (`mongodb://`, `postgres://`, `mysql://`, `redis://`)
  - Cloud provider keys (AWS `AKIA`, GCP, Azure, Cloudflare)
  - Service-specific keys (Stripe, OpenAI, Anthropic, Twilio, SendGrid, Firebase)
  - OAuth client IDs and secrets
  - Any string that looks like a base64-encoded secret or JWT

**Agent 2 - URL/Endpoint Scanner**: Scan for hardcoded:
  - API base URLs that should be configurable
  - Webhook URLs
  - Database connection strings
  - Service endpoints (localhost references with ports)

**Agent 3 - Config Scanner**: Scan for:
  - Hardcoded port numbers
  - Environment-specific values (dev/staging/prod URLs)
  - Feature flags or toggles
  - Third-party service configuration values

Compile all findings into a unified secrets inventory.

## Phase 3: Create .env Files

1. Create `.env` with all extracted secrets organized by category:
   ```
   # ============================================
   # Application
   # ============================================
   PORT=3000
   NODE_ENV=development

   # ============================================
   # Database
   # ============================================
   DATABASE_URL=<extracted-value>

   # ============================================
   # Authentication
   # ============================================
   API_KEY=<extracted-value>
   ```
2. Create `.env.example` with the same structure but placeholder values:
   ```
   PORT=3000
   NODE_ENV=development
   DATABASE_URL=your_database_url_here
   API_KEY=your_api_key_here
   ```
3. Replace all hardcoded values in source files with environment variable references:
   - TypeScript/JS: `process.env.VARIABLE_NAME`
   - Python: `os.environ.get("VARIABLE_NAME")` or using `python-dotenv`

## Phase 4: Folder Restructure

Based on the detected project type, reorganize into the appropriate structure:

**TypeScript/Next.js project:**
```
src/
  app/              # Next.js App Router (or pages/)
  components/       # React components
  lib/              # Shared utilities, API clients
  hooks/            # Custom React hooks
  types/            # TypeScript type definitions
  styles/           # Global styles
  config/           # App configuration (reads from env)
public/             # Static assets
tests/              # Test files
```

**TypeScript/Express or Node project:**
```
src/
  routes/           # API route handlers
  controllers/      # Business logic
  models/           # Data models
  middleware/        # Express middleware
  services/         # External service integrations
  utils/            # Shared utilities
  types/            # TypeScript types
  config/           # Configuration (reads from env)
tests/              # Test files
```

**Python project:**
```
src/ (or app/)
  api/              # API routes/views
  models/           # Data models
  services/         # Business logic
  utils/            # Shared utilities
  config/           # Configuration (reads from env)
tests/              # Test files
```

**Hybrid (Python backend + TS frontend):**
```
backend/
  app/              # Python application
    api/
    models/
    services/
    config/
  requirements.txt
  pyproject.toml
frontend/
  src/
    app/
    components/
    lib/
    hooks/
    types/
  package.json
  tsconfig.json
```

Rules:
- Do NOT move files if the project already has a sensible structure — only reorganize scattered files
- Update all import paths after moving files
- Verify no circular dependencies are introduced

## Phase 5: Configuration & Deployment Readiness

1. Ensure `.gitignore` exists and includes:
   - `.env` (never commit secrets)
   - `node_modules/`, `__pycache__/`, `.venv/`, `dist/`, `.next/`
   - OS files (`.DS_Store`, `Thumbs.db`)
   - IDE files (`.vscode/`, `.idea/`)
2. Ensure `tsconfig.json` exists and is properly configured (for TS projects)
3. Ensure `requirements.txt` or `pyproject.toml` has all dependencies (for Python projects)
4. Add a `config/` module that centralizes all environment variable reads with validation
5. Verify the project builds/runs after restructuring

## Phase 6: README Generation

Generate a comprehensive `README.md` with:
- Project name and one-line description
- Tech stack summary
- Prerequisites (Node.js version, Python version, etc.)
- Setup instructions (clone, install deps, configure env)
- How to copy `.env.example` to `.env` and fill in values
- Development commands (start, test, build, lint)
- Folder structure overview
- Deployment instructions (relevant to detected hosting platform if any)
- Environment variables table (name, description, required/optional)

</process>

<verification>
Before completing, verify:
- Run `grep -r "sk-\|api_key\|apiKey\|API_KEY\|secret\|password\|Bearer " --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" src/ app/ 2>/dev/null` to confirm no secrets remain in source
- `.env` file exists with real values
- `.env.example` file exists with placeholder values
- `.env` is listed in `.gitignore`
- The project builds without errors (`npm run build` or `python -c "import app"`)
- All imports resolve correctly after restructuring
- README.md is accurate and complete
</verification>

<output>
Files created/modified:
- `.env` — All secrets organized by category
- `.env.example` — Template with placeholder values
- `.gitignore` — Updated to exclude secrets and build artifacts
- `README.md` — Comprehensive project documentation
- `src/config/` or `config/` — Centralized environment variable module
- Restructured source files with updated imports
</output>

<success_criteria>
- Zero hardcoded secrets remain in source files
- All secrets extracted to .env with proper categorization
- .env.example mirrors .env structure with safe placeholder values
- .gitignore prevents .env from being committed
- Folder structure follows conventions for the detected project type
- All imports and references updated — project compiles/runs
- README provides clear setup and deployment instructions
- Project is ready for a fresh developer to clone, configure .env, and run
</success_criteria>
