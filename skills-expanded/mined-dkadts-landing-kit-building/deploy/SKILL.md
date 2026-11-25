---
name: deploy
description: Deploys to Vercel. Verifies /audit passed. Helps configure domain, DNS, and secret storage. Offers Google Cloud Secret Manager as the recommended store for sensitive API keys. Post-deploy smoke test.
---

# /deploy

Final step. Publishes the landing to production. DOES NOT RUN if `/audit` did not pass.

## When to use

- After `/audit` with pass verdict.
- Updates to an already-deployed landing (then the gate is only audit).

## Requirements — HARD BLOCKING

- `site/_audit-report.md` exists with verdict = OK.
- No uncommitted changes in git (user commits themselves — CLAUDE.md rule 5).
- `vercel.json` present.
- All env vars from `brief/06-technical.md` are configured wherever the user chose to store them (Vercel Dashboard, or Google Cloud Secret Manager — see Step 3a).

## Process

**Step 1. Verify readiness**

- Read `site/_audit-report.md`, verdict must be OK.
- Read `brief/06-technical.md` — domain, region, env vars.
- Read `brief/blocks/contact-form.md` — which backend (affects env vars).

**Step 2. First deploy vs update**

If first deploy:
- User installs Vercel CLI: `npm i -g vercel`.
- Init: `vercel` (asks project, domain, etc.).
- Configure secret storage (Step 3a).
- Configure env vars (Step 3b).
- Configure domain (Step 4): DNS at the registrar → Vercel.

If update:
- `vercel --prod` (or via GitHub integration, if wired).

**Step 3a. Secret storage choice**

**Ask the user how to store sensitive keys** before writing anything to Vercel. Options:

**Option A. Vercel env vars only** (simplest, default)
- Secrets live in Vercel Dashboard → Settings → Environment Variables.
- Marked as "Sensitive" so they're write-only after creation.
- Trade-off: rotation is manual, audit log is Vercel Enterprise-tier, and multi-project secret sharing means duplicating values.
- Good fit for: single-landing projects, hobby projects, agencies with one client per Vercel team.

**Option B. Google Cloud Secret Manager** (recommended for production / multi-project)
- Secrets live in a central GCP project.
- IAM-controlled access, versioning, audit log out of the box, easy rotation.
- Vercel serverless functions read secrets at runtime via `@google-cloud/secret-manager` using a service account.
- Only two values live in Vercel env vars: `GCP_PROJECT_ID` and `GCP_SA_KEY_JSON` (base64-encoded service account key).

If the user picks Option B, walk them through:

1. **Create the GCP project** (if none exists):
   ```
   gcloud projects create <PROJECT_ID> --name="<Client name>"
   gcloud config set project <PROJECT_ID>
   gcloud services enable secretmanager.googleapis.com
   ```

2. **Create each secret** (repeat per key):
   ```
   echo -n "<the-real-value>" | gcloud secrets create RESEND_API_KEY --data-file=-
   ```
   (Do NOT paste the real value into chat. User runs the command themselves in their terminal.)

3. **Create a service account with read-only access**:
   ```
   gcloud iam service-accounts create landing-secret-reader \
     --display-name="Landing Secret Reader"

   gcloud projects add-iam-policy-binding <PROJECT_ID> \
     --member="serviceAccount:landing-secret-reader@<PROJECT_ID>.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"

   gcloud iam service-accounts keys create sa-key.json \
     --iam-account=landing-secret-reader@<PROJECT_ID>.iam.gserviceaccount.com
   ```

4. **Base64-encode the key file and store in Vercel**:
   ```
   base64 -w0 sa-key.json    # Linux
   # or
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("sa-key.json"))    # PowerShell
   ```
   Paste the base64 output into a Vercel env var named `GCP_SA_KEY_JSON`. Also add `GCP_PROJECT_ID`.

5. **Read secrets from a Vercel serverless function**:
   ```js
   // api/send-form.js
   import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

   const credentials = JSON.parse(
     Buffer.from(process.env.GCP_SA_KEY_JSON, 'base64').toString('utf8')
   );
   const client = new SecretManagerServiceClient({ credentials });

   async function getSecret(name) {
     const [version] = await client.accessSecretVersion({
       name: `projects/${process.env.GCP_PROJECT_ID}/secrets/${name}/versions/latest`,
     });
     return version.payload.data.toString('utf8');
   }

   export default async function handler(req, res) {
     const apiKey = await getSecret('RESEND_API_KEY');
     // ... use apiKey
   }
   ```

6. **Delete `sa-key.json` locally after upload** — do not commit it.

7. **After setup**, the only Vercel env vars are `GCP_PROJECT_ID`, `GCP_SA_KEY_JSON`, and non-sensitive config (`FROM_EMAIL`, `TO_EMAIL`, `ALLOWED_ORIGIN`).

Record the choice in `site/_deploy-log.md` under "Secret storage:".

**Step 3b. Env vars checklist** (if backend)

Show which variables must be set (Vercel Dashboard Production; or GCP Secret Manager if Option B):

```
From brief/blocks/contact-form.md:
- RESEND_API_KEY (Sensitive)  ← from resend.com dashboard
- FROM_EMAIL                   ← e.g. orders@yourdomain.com
- REPLY_TO_EMAIL               ← e.g. hello@yourdomain.com
- TO_EMAIL                     ← where the form submission lands
- ALLOWED_ORIGIN               ← e.g. https://www.yourdomain.com

If Secret Manager (Option B):
- GCP_PROJECT_ID
- GCP_SA_KEY_JSON (Sensitive, base64-encoded)
```

User fills these themselves. NEVER read secrets from local `.env` files or paste them into chat.

**Step 4. Domain setup** (first time)

- Vercel Dashboard → Domains → Add.
- Show required DNS records:
  - `A` record: `76.76.21.21` for apex
  - `CNAME`: `cname.vercel-dns.com` for www
- Pick redirect: www → apex or apex → www (see `brief/06-technical.md`).
- SSL — auto (Let's Encrypt).

**Step 5. First deploy command**

```
vercel login
vercel link
vercel --prod
```

**Step 6. Smoke test after deploy**

Open production URL:
- Homepage loads in < 2 s?
- LCP good? (Lighthouse mobile.)
- Form submits? (Test submit with a test email.)
- Analytics working? (Open GA DebugView / FB Pixel Helper.)
- Cookie banner fires? (If applicable.)
- Open /privacy — link exists in footer?
- Mobile emulation — no battle-tested breakages?

**Step 7. Post-deploy report**

`site/_deploy-log.md` (append per deploy):

```markdown
## Deploy 2026-08-08 16:00
- URL: https://www.example.com
- Commit: <hash>
- Region: fra1
- Secret storage: GCP Secret Manager (project: landing-clients-prod)
- Lighthouse:
  - Perf: 95
  - A11y: 100
  - Best practices: 100
  - SEO: 100
- Smoke test: pass
- Env vars: 3 in Vercel (GCP creds + non-sensitive), 5 in GCP Secret Manager
- DNS: propagated
- Notes: <anything unusual>
```

**Step 8. If it fails**

Rollback: `vercel rollback` — return to the previous deployment.

Env var error → update in Vercel Dashboard or GCP → redeploy.

Code error → fix locally → rerun `/audit` → rerun `/deploy`.

## Rules of behavior

- **Do not deploy if audit fails.** Full stop.
- **Do not set env vars yourself.** User does it in Dashboard / gcloud — they're sensitive.
- **Do not commit.** Do not run git commands. CLAUDE.md rule 5.
- **Always smoke-test after deploy.** Automatic pipelines do not replace live-eye verification.
- **Never paste real secret values into chat.** User runs `gcloud secrets create ... --data-file=-` themselves.

## What NOT to do

- Do not change vercel.json without user request.
- Do not wire external services (Cloudflare Workers, Netlify redirect, etc.) without discussion.
- Do not deploy to staging and prod simultaneously — verify staging first.
- Do not commit `sa-key.json` or any `.env` file — verify `.gitignore` covers them.

## Next

- Monitor first hours (analytics, Vercel error logs).
- Discuss: post-deploy monitoring?
- Plan next edits (edits → audit → deploy).
