---
description: Full build & deployment rule for CalorieCam backend API.
globs:
alwaysApply: false
---

# CalorieCam Backend API
## Rule Type: Agent Requested

Implement the CalorieCam backend using **TypeScript** with Node.js and Express. The backend must integrate GPT-4o for food analysis, store data in Supabase, and follow monorepo standards for structure and shared package usage.

---

## 📁 Project Structure

The backend must use a TypeScript setup with this structure:

```
/apps/calorie-cam/backend
  /src
    index.ts          # Entry point
    routes/           # Express route handlers
    services/         # GPT, Supabase logic
    utils/            # Common helpers
    types/            # Typed interfaces, GPT responses
  .env
  tsconfig.json
```

---

## ⚙️ Stack & Dependencies

- Node.js v16+ (nvm recommended)
- Yarn (v1.x) or PNPM (consistent with monorepo)
- Supabase account/project
- OpenAI API Key (GPT-4o access)
- Railway account (for deployment)

Install the following packages:

```bash
yarn install   # from monorepo root or backend directory
# or, if using pnpm:
pnpm add express cors dotenv zod openai @supabase/supabase-js
pnpm add -D typescript ts-node @types/express @types/node
```

Use `ts-node` for local development and `tsup` for optional production builds.

---

## 📦 Shared Packages Integration

- Use shared utility functions and types from `/packages/shared` where possible.
- Shared constants, validators, and API response types should live in `/packages/shared/types` or `/packages/shared/utils`.
- Tailor type reuse to match the food log schema and GPT-4o integration.

---

## 🔐 Auth Handling

- Accept optional JWTs via `Authorization: Bearer <token>`.
- Use Supabase’s public key or client-side verification to validate tokens.
- Associate logs with a `user_id` only if token is valid. Otherwise, allow anonymous usage.

---

## 🤖 GPT-4o Integration

- Use OpenAI Node SDK and send images to GPT-4o via `image_url`:
  - Prompt it to identify the food and estimate calories, macros.
  - If it’s not food, return a humorous message (e.g., “This is not food. It appears to be a confused iguana on a rug.”).
- Response must be structured and stored in Supabase:
  - `food_name`, `calories`, `macros`, `gpt_response`, and optionally `confidence_score`.

---

## 📡 API Endpoints

### POST `/api/upload-food-image`

- Accepts image file or URL from mobile app.
- Calls GPT-4o to analyze the image.
- Parses and validates response (use Zod).
- Stores result in Supabase (`food_logs` table).
- Returns structured response to the frontend:

```json
{
  "success": true,
  "food": {
    "name": "Cheeseburger",
    "calories": 350,
    "proteins": 18,
    "fats": 21,
    "carbs": 29
  },
  "humor": null
}
```

Or if non-food:

```json
{
  "success": false,
  "food": null,
  "humor": "This is not food; it appears to be a fidget spinner covered in cheese dust."
}
```

---

## 🛠️ Setup Steps

1. **Install dependencies:**  
   From monorepo root, run:
   ```bash
   yarn install
   ```
   or, in backend dir:
   ```bash
   yarn install
   ```

2. **Configure environment variables:**  
   - Copy `.env.example` to `.env` in `/backend`.
   - Fill in:
     - `SUPABASE_URL`
     - `SUPABASE_ANON_KEY`
     - `SUPABASE_SERVICE_KEY`
     - `OPENAI_API_KEY`
     - `NODE_ENV`
   - Ensure these match your Supabase and OpenAI project settings.

3. **Supabase setup:**  
   - Create project at https://supabase.com
   - Run schema migrations (`deploy.sh` or SQL via dashboard).
   - Confirm tables and storage buckets exist.

4. **OpenAI setup:**  
   - Get API key from https://platform.openai.com
   - Ensure GPT-4o access.

---

## 🚦 Build & Run

- **Development:**  
  ```bash
  yarn dev
  ```
  (Uses ts-node, watches for changes.)

- **Production build:**  
  ```bash
  yarn build
  yarn start
  ```
  (Builds with TypeScript, runs compiled JS.)

- **Health check:**  
  - Local: http://localhost:3000/health
  - Production: https://calorie-cam-production.up.railway.app/health

---

## 🚀 Deployment

- Deploy to Railway:
  - Connect GitHub repo.
  - Set all required environment variables in Railway dashboard.
  - Push to main branch to trigger deploy.
- Troubleshooting:
  - Check Railway build logs for missing env vars or build errors.
  - If CORS issues, verify allowed origins in Express config.

---

## 🧪 Testing

- Unit test GPT logic and Supabase storage using Vitest.
- Mock OpenAI responses for predictable test outputs.

Run tests with:
```bash
yarn test
```

---

## 🔄 Common Issues & Fixes

- **Dependency errors:**  
  - Run `yarn clean && yarn install` from root.
- **Env var issues:**  
  - Double-check `.env` and Railway dashboard for typos or missing values.
- **Build errors:**  
  - Ensure Node version matches `.nvmrc` (if present).
- **API not responding:**  
  - Check health endpoint and logs.
  - Ensure Supabase and OpenAI keys are valid.

---

## 📚 References

- [Supabase Docs](https://supabase.com/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Railway Docs](https://docs.railway.app/)
- [Express Docs](https://expressjs.com/)