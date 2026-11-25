---
name: fullstack-deploy
description: Complete full-stack development and deployment pipeline using Supabase (database + storage), any Vercel-supported framework (Next.js, Flask, FastAPI, Vue.js, etc.), GitHub (version control), and Vercel (hosting). This skill should be used when the user requests to build and deploy a complete application from requirements to production URL, or when phrases like "create an app", "build a website", "deploy to production", or "full-stack project" are mentioned.
---

# Full-Stack Development & Deployment Pipeline

**One sentence:** Take a user idea from requirements to a live production domain in a single conversation.

> **English summary:** This skill automates the full lifecycle of a web app — requirements, database design with Supabase, application development with any Vercel-supported framework, GitHub repo creation, and production deployment on Vercel with public URL. The user only needs to paste one prompt and provide a few API keys in `.env`.

## Agent Quick Start

When this skill is loaded, follow this checklist before doing anything else:

1. **Load credentials:**
   ```bash
   set -a && source .env && set +a
   ```
   If `.env` is missing or empty, stop and ask the user to copy `.env.example` to `.env` and fill it.
   
   Required Supabase credentials for full automation:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY` (for the frontend/client)
   - `SUPABASE_SERVICE_ROLE_KEY` (for server-side/admin operations)
   - `SUPABASE_MANAGEMENT_TOKEN` (for automated SQL execution)
   
   If `SUPABASE_MANAGEMENT_TOKEN` is missing, explain that database setup will require manual execution in the Supabase SQL Editor.

2. **Verify tooling:**
   ```bash
   gh auth status        # must be logged in
   vercel --version      # Vercel CLI must be installed
   ```

3. **Create a todo list** with `TodoWrite` covering all 6 phases so the user can watch progress.

4. **One-line prompt template** you can suggest to the user:
   - 中文：`/fullstack-deploy 我要做一个 [一句话描述]，前端用 [框架]，数据库用 Supabase，部署到 Vercel。请从零开始完成需求分析、代码开发、GitHub 仓库创建和线上部署，最终给我一个可访问的生产环境 URL。`
   - English: `/fullstack-deploy Build me a [one-sentence description] using [framework], Supabase for the database, and deploy it to Vercel. Take it from requirements to a live production URL.`

5. **Autonomy rule:** Once the user confirms the idea and stack, do not ask for permission on every small step. Execute the pipeline, update todos, and report at phase boundaries.

## Purpose

Automate the entire lifecycle from requirements gathering to production deployment, including:
- Database schema design and setup (Supabase)
- Application development (any Vercel-supported framework)
- Version control (Git + GitHub)
- Production deployment (Vercel)
- Environment variable configuration
- Public URL provisioning

## When to Use This Skill

Use this skill when the user wants to:
- Build a complete application from scratch
- Create a web app with database functionality
- Deploy an existing project to production
- Set up a full development-to-deployment pipeline
- Integrate Supabase database with a web framework

Trigger phrases include: "build an app", "create a website", "deploy my project", "full-stack application", "production deployment"

## Workflow Overview

The complete workflow follows these phases:

### Phase 1: Requirements & Planning

1. **Gather Requirements** - Understand user needs, features, and tech preferences.
2. **Choose Framework** - Use the decision tree below; consult `references/frameworks.md` for details.
3. **Design Database** - Plan tables, relationships, RLS policies, storage needs.

**Framework Decision Tree:**
- Full-stack React app with SSR/API routes? → **Next.js**
- Fast modern SPA, any frontend? → **Vite + React/Vue/Svelte**
- Python API/backend? → **FastAPI** (async) or **Flask** (simple)
- Content-heavy/static site? → **Astro** or **Hugo**
- Need admin interface and batteries included? → **Django**

### Phase 2: Database Setup (Supabase)

1. **Create SQL Schema** - Generate complete `database.sql` file with:
   - Table definitions with proper data types
   - Primary keys, foreign keys, and indexes
   - Row Level Security (RLS) policies
   - Triggers for auto-updating timestamps
   - Sample data (optional)

2. **Create Storage Setup** (if needed) - Generate `storage-setup.sql` for:
   - Public or private buckets
   - Storage policies for anonymous/authenticated access
   - MIME type restrictions

3. **Execute SQL automatically** - Use the Supabase Management API to run `database.sql` without manual dashboard work:
   ```bash
   set -a && source .env && set +a
   jq -Rs '{query: .}' database.sql | \
   curl -s -X POST "https://api.supabase.com/v1/projects/{project-ref}/database/query" \
     -H "Authorization: Bearer $SUPABASE_MANAGEMENT_TOKEN" \
     -H "Content-Type: application/json" \
     -d @-
   ```
   - The project ref is the subdomain of your `SUPABASE_URL` (e.g., `mclpscvtkxldycxoidoc`).
   - Verify the schema by querying the newly created table.

4. **Fallback to manual setup** - If `SUPABASE_MANAGEMENT_TOKEN` is not available, provide the `database.sql` file and ask the user to run it in the Supabase SQL Editor.

### Phase 3: Application Development

1. **Initialize Project** - Set up framework-specific project structure.
2. **Install Dependencies** - Framework-specific packages + Supabase client.
3. **Configure Environment** - Create `.env.local` with values from `.env`:
   ```bash
   set -a && source .env && set +a
   # then write NEXT_PUBLIC_SUPABASE_URL=$SUPABASE_URL etc.
   ```
4. **Implement Features**:
   - Database client setup
   - API routes/endpoints
   - UI components
   - Authentication (if needed)
   - File upload (if using Storage)
5. **Test Locally** - Run dev server and verify functionality.

### Phase 4: Git & GitHub

Always source `.env` first:
```bash
set -a && source .env && set +a
```

1. **Initialize Git**:
   ```bash
   git init
   ```

2. **Create .gitignore** - Exclude sensitive files and build artifacts:
   - Must include: `.env*`, `node_modules/`, `.next/`, `dist/`, `.vercel`, `__pycache__/`

3. **Initial Commit**:
   ```bash
   git add .
   git commit -m "Initial commit: [Project description]

   🎉 Features:
   - [Feature 1]
   - [Feature 2]

   🚀 Generated with Claude Code (https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

4. **Get GitHub Username**:
   ```bash
   curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep '"login"'
   ```

5. **Create GitHub Repository**:
   ```bash
   curl -X POST \
     -H "Authorization: token $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/user/repos \
     -d '{"name":"[REPO_NAME]","description":"[DESCRIPTION]","private":false}'
   ```

6. **Push to GitHub**:
   ```bash
   git remote add origin https://$GITHUB_TOKEN@github.com/[USERNAME]/[REPO_NAME].git
   git push -u origin main
   ```

### Phase 5: Vercel Deployment

Always source `.env` first:
```bash
set -a && source .env && set +a
```

1. **Install Vercel CLI** (if not installed):
   ```bash
   npm install -g vercel
   ```

2. **Initial Deployment** - Deploy and capture project/team IDs:
   ```bash
   vercel --token $VERCEL_TOKEN --yes --prod
   ```
   Note: Initial deployment may fail due to missing environment variables.

3. **Get Project Information** - Retrieve project ID and team ID from API or error messages.

4. **Configure Environment Variables**:
   ```bash
   curl -X POST \
     "https://api.vercel.com/v10/projects/[PROJECT_ID]/env?teamId=$VERCEL_TEAM_ID" \
     -H "Authorization: Bearer $VERCEL_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "key": "ENV_VAR_NAME",
       "value": "ENV_VAR_VALUE",
       "type": "encrypted",
       "target": ["production", "preview", "development"]
     }'
   ```

5. **Redeploy with Environment Variables**:
   ```bash
   vercel --token $VERCEL_TOKEN --prod --force
   ```

6. **Disable Deployment Protection** - Make site publicly accessible:
   ```bash
   curl -X PATCH \
     "https://api.vercel.com/v9/projects/[PROJECT_ID]?teamId=$VERCEL_TEAM_ID" \
     -H "Authorization: Bearer $VERCEL_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"ssoProtection":null,"passwordProtection":null}'
   ```

7. **Verify Deployment**:
   ```bash
   curl -s "[PRODUCTION_URL]" -o /dev/null -w "%{http_code}"
   ```
   Expected: 200 (OK)

### Phase 6: Completion & Handoff

1. **Verify All Components**:
   - ✅ Database schema executed
   - ✅ Application runs locally
   - ✅ Code pushed to GitHub
   - ✅ Deployed to Vercel
   - ✅ Environment variables configured
   - ✅ Site publicly accessible

2. **Provide URLs**:
   - Production URL: `https://[project-name]-[team].vercel.app`
   - GitHub Repository: `https://github.com/[username]/[repo-name]`
   - Vercel Dashboard: `https://vercel.com/[team]/[project-name]`

3. **Document Setup** - Create README.md or CLAUDE.md with:
   - Project overview
   - Development commands (`npm run dev`, `npm run build`)
   - Environment variables required
   - Database setup instructions
   - Architecture notes

## Framework-Specific Guidance

Refer to `references/frameworks.md` for detailed configuration for each framework. Key considerations:

**Next.js:**
- Use `NEXT_PUBLIC_` prefix for client-side env vars
- API routes in `app/api/`
- Automatic TypeScript support

**Flask:**
- Requires `vercel.json` for routing
- Use `requirements.txt` for dependencies
- Entry point typically `app.py` or `main.py`

**FastAPI:**
- Similar to Flask but uses ASGI
- Automatic API docs at `/docs`
- Use `uvicorn` for local dev

**Vue.js:**
- Use `VUE_APP_` prefix for env vars
- Build output to `dist/`
- Supports both SPA and SSR (Nuxt)

## Credentials Management

All deployment credentials are managed via environment variables:

1. Copy `.env.example` to `.env` and fill in real values.
2. Before running any credential-dependent command, execute:
   ```bash
   set -a && source .env && set +a
   ```
3. Alternatively, advanced users can put the same variables in `.claude/settings.json` under `"env"`; Claude Code will auto-load them for every Bash call.
4. `references/credentials.md` documents what each key is for and where to obtain it, including the three Supabase tokens:
   - `SUPABASE_ANON_KEY` for frontend/client access
   - `SUPABASE_SERVICE_ROLE_KEY` for server-side/admin access
   - `SUPABASE_MANAGEMENT_TOKEN` for automated SQL execution

**Never commit `.env` or `.claude/settings.json` to Git.** They are already ignored by `.gitignore`.

## Error Handling

**Common Issues:**

1. **Build fails due to missing env vars**
   - Solution: Add env vars via Vercel API, then redeploy

2. **Vercel shows 401/authentication required**
   - Solution: Disable ssoProtection and passwordProtection

3. **Database connection fails**
   - Solution: Verify Supabase URL and key are correct
   - Check RLS policies allow intended access

4. **GitHub push fails**
   - Solution: Verify token has `repo` permission
   - Check if remote already exists

5. **Deployment timeout**
   - Solution: Check build logs, optimize dependencies

## Best Practices

1. **Security**
   - Always use `.gitignore` to exclude `.env*` files
   - Use encrypted env vars in Vercel
   - Implement RLS policies in Supabase
   - Never commit credentials

2. **Code Quality**
   - Include TypeScript for type safety (when using JS/TS)
   - Use consistent formatting
   - Add helpful comments for complex logic
   - Create CLAUDE.md for future Claude instances

3. **User Experience**
   - Use TodoWrite tool to track progress
   - Provide clear status updates
   - Test thoroughly before declaring completion
   - Share all relevant URLs at the end

4. **Efficiency**
   - Run parallel operations when possible
   - Reuse credential lookups
   - Cache responses when appropriate
   - Use background processes for long-running tasks

## Complete Example Workflow

When user says: "Build me a task management app with user authentication"

1. **Requirements**: Todo CRUD, user accounts, database persistence
2. **Framework**: Choose Next.js (full-stack, good auth support)
3. **Database Design**:
   - users table (id, email, created_at)
   - todos table (id, user_id, title, completed, created_at)
   - RLS: Users can only see their own todos
4. **Development**: Create Next.js app with:
   - Supabase client setup
   - Auth UI (signup/login)
   - Todo CRUD API routes
   - React components for todo list
5. **Git & GitHub**: Initialize, commit, create repo, push
6. **Vercel**: Deploy, add env vars (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`)
   - `SUPABASE_SERVICE_ROLE_KEY` and `SUPABASE_MANAGEMENT_TOKEN` stay in `.env` for server-side/automation use and are not exposed to the browser.
7. **Completion**: Provide production URL, GitHub link, verify functionality

## Workflow Optimization

**Use TodoWrite tool** to track progress through phases:
1. Database setup
2. Application development
3. Git initialization
4. GitHub repository creation
5. Vercel deployment
6. Environment configuration
7. Public URL verification

Mark each step as completed immediately after finishing to give user visibility into progress.

**Run parallel operations** when dependencies allow:
- Git operations can happen while deployment is building
- Multiple environment variables can be added simultaneously
- GitHub username lookup and repo creation can be pipelined

## Post-Deployment

After successful deployment, inform user about:
- **Automatic deployments**: Future pushes to main branch will auto-deploy
- **Vercel dashboard**: Where to view logs, analytics, and settings
- **Environment variables**: How to update them if needed
- **Database changes**: Recommend migration strategy for schema updates
- **Custom domains**: How to add custom domain in Vercel (if desired)

## Iteration and Updates

When user requests changes after deployment:
1. Make code changes locally
2. Test with `npm run dev` or equivalent
3. Commit changes to Git
4. Push to GitHub
5. Vercel automatically redeploys
6. Verify changes in production

For database schema changes:
1. Create migration SQL file
2. Execute it automatically via the Supabase Management API using `SUPABASE_MANAGEMENT_TOKEN`
3. Update application code to match new schema
4. Deploy application changes
5. If `SUPABASE_MANAGEMENT_TOKEN` is unavailable, run the migration SQL in the Supabase SQL Editor manually
