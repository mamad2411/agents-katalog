---
description: Automates Supabase CLI setup, schema migration, local development, and deployment linking for CalorieCam.
globs: 
alwaysApply: false
---
# CalorieCam Setup Automation
## Rule Type: Agent Requested

This rule automates the local and remote Supabase project setup process for the CalorieCam app, using the Supabase CLI. Agents must follow these steps when asked to configure the Supabase environment or prepare the database schema for development or deployment.

---

## 🧱 Step 1: Install Supabase CLI

If not already installed:
```bash
npm install -g supabase
```

---

## 🗂 Step 2: Initialize Supabase Locally

Inside `/apps/calorie-cam/`:
```bash
supabase init
```
Creates `/supabase` with `/migrations` and `config.toml`.  
Commit this directory to version control.

---

## ✍️ Step 3: Add Database Schema

Generate a migration file and paste in the schema from `data-models.mdc`:
```bash
supabase migration new init-schema
```
Paste your schema into the generated file under `/supabase/migrations`.  
Keep this in sync with `data-models.mdc`.

---

## 🧪 Step 4: Run Supabase Locally

```bash
supabase start
```
This starts a local Supabase instance with:
- Postgres
- Supabase Studio (GUI)

---

## 🌐 Step 5: Configure Environment Variables

- Copy `.env.example` to `.env` in both `/backend` and `/mobile`.
- Fill in `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY` from the Supabase dashboard.
- Ensure these match your local or remote project as appropriate.

---

## 🚀 Step 6: Deploy Schema to Remote Supabase

To apply migrations to production:
```bash
supabase db push --project-ref <your-project-ref>
```
Or run the SQL migration manually in the Supabase dashboard.  
Verify tables and storage buckets exist in the Supabase UI.

---

## 🔗 Step 7: Link Backend and Mobile

- Ensure backend `.env` is set with correct Supabase values.
- In mobile, set API URLs and Supabase keys in `.env`.

---

## 🛠 Troubleshooting

- If you get port conflicts, stop other local Postgres/Supabase instances.
- If migration fails, check for syntax errors or out-of-sync schema.
- For connection/auth errors, double-check all environment variables.

---

## 📝 Notes

- Always commit `/supabase/migrations` and `config.toml` to version control.
- Keep `data-models.mdc` and migration files in sync.
- For more, see Supabase CLI docs: https://supabase.com/docs/guides/cli