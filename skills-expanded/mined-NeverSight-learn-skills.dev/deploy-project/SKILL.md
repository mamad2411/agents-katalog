---
name: deploy-project
description: Set up continuous deployment for a Next.js + Convex project using Vercel and GitHub. After this one-time setup, every push to the main branch auto-deploys both the frontend (Vercel) and backend (Convex).
---

# Deploy Project

This skill sets up continuous deployment so that every push to GitHub automatically deploys the full application — frontend on Vercel, backend on Convex. After running this skill once, you never need to deploy manually again.

## What this skill does

1. Connects the Vercel project to the GitHub repository
2. Configures the build command so Convex deploys automatically with every Vercel build
3. Sets the required environment variables for production
4. Pushes to GitHub to trigger the first deploy
5. Verifies the live site works

## Prerequisites

Before running this skill:
- The project must be working locally (dev server runs, features work)
- The code must already be on GitHub (the `setup-project` skill handles this)
- `gh` must be authenticated (also handled by `setup-project`)

## Step 1: Authenticate with Vercel

Check if the user is already authenticated with Vercel:

```bash
npx vercel whoami
```

If not authenticated, tell the user:

> "We need to connect to Vercel — this is what puts your site on the internet. This will open your browser to sign in."

Then run:

```bash
npx vercel login
```

This is interactive — it opens the browser. Wait for the user to complete it.

Show them where to sign up if needed: "Sign up at vercel.com with your GitHub account — it's free."

## Step 2: Link the Vercel project

Link the current directory to a Vercel project:

```bash
npx vercel link
```

Follow the prompts to connect to the correct Vercel scope/team. If this is a new project, Vercel will create one.

Then connect the GitHub repo so Vercel auto-deploys on push:

```bash
npx vercel git connect
```

## Step 3: Configure the build command

The key to continuous deployment is overriding Vercel's build command so that Convex functions deploy automatically alongside the frontend.

Set the build command override in Vercel:

```bash
npx vercel env add VERCEL_BUILD_COMMAND production <<< "npx convex deploy --cmd 'npm run build'"
```

If the above doesn't work via CLI, tell the user:

> "Go to your project on vercel.com → Settings → General → Build & Development Settings. Override the Build Command to:
>
> `npx convex deploy --cmd 'npm run build'`
>
> This makes Convex deploy automatically every time Vercel builds your site."

**How this works:** When Vercel builds, `npx convex deploy` reads the deploy key, pushes your Convex functions to production, sets the `CONVEX_URL` environment variable, then runs your normal `npm run build` which picks up that URL. Both frontend and backend deploy in one step.

## Step 4: Set environment variables

The production deployment needs a Convex deploy key.

Tell the user:

> "I need you to get your production deploy key from Convex. Open your Convex dashboard (dashboard.convex.dev), go to your project → Settings → Deploy Keys, and generate a Production deploy key. Copy it and give it to me."

Once the user provides the key, set it in Vercel:

```bash
npx vercel env add CONVEX_DEPLOY_KEY production
```

Paste the key when prompted.

Also check if there are other environment variables the project needs in production (e.g., `AUTH_SECRET`, `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`). Look at `.env.local` or the Convex dashboard settings to identify what's needed. For each one:

```bash
npx vercel env add <VARIABLE_NAME> production
```

Tell the user what each variable is for in plain language so they know where to find the values.

## Step 5: Push and deploy

Commit any remaining changes and push to trigger the first deployment:

```bash
git add -A
git commit -m "Configure production deployment"
git push origin main
```

This push triggers Vercel to build the project, which in turn deploys Convex functions. Both frontend and backend go live.

Tell the user:

> "Your code is deploying now. Vercel is building the site and deploying your backend at the same time. This takes a couple of minutes."

## Step 6: Verify the live site

After the deployment completes, get the live URL:

```bash
npx vercel inspect --url
```

Or tell the user to check their Vercel dashboard for the deployment URL.

Walk the user through verifying the live site:

> "Open the live URL in your browser. Check that:
> 1. The site loads and looks right
> 2. You can sign in
> 3. The features work (data loads, forms submit, etc.)
>
> If everything works, you're live. From now on, every time you push code to GitHub, both your site and your backend update automatically."

## Recovery

- **Build fails on Vercel:** Check the build logs at vercel.com → Deployments → click the failed deploy → Build Logs. The error is usually a missing environment variable or a code error. Fix it, push again.
- **Sign-in doesn't work on live site:** The sign-in system (WorkOS) may need the production URL added to its allowed origins. Check the WorkOS dashboard and add your `.vercel.app` domain.
- **Data doesn't show on live site:** The production Convex deployment may be empty. Seed data through the Convex dashboard or run a seed function.
- **Convex deploy fails:** Make sure `CONVEX_DEPLOY_KEY` is set correctly in Vercel and scoped to Production. Regenerate the key in the Convex dashboard if needed.

## What happens after this

Once this skill completes, the deployment pipeline is fully automatic:

1. You make changes locally
2. You push to GitHub (`git push`)
3. Vercel detects the push and starts a build
4. The build command runs `npx convex deploy`, which deploys your Convex functions
5. Then `npm run build` runs, building the frontend with the production Convex URL
6. Vercel publishes the new frontend

No manual deployment steps. No CLI commands. Just push and it's live.
