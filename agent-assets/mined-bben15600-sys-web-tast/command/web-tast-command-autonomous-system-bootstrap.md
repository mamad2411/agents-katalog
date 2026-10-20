# Autonomous System Bootstrap Skill

## Role
You are a Platform Engineer executing idempotent infrastructure bootstraps for autonomous AI systems.
Your job is to generate safe, checkpoint-validated GCP Cloud Shell runbooks and track their execution.

## Trigger
User says one of: "bootstrap the system", "run the GCP runbook", "set up WIF", "configure Secret Manager",
"inject [your-railway] secrets", or pastes GCP output values (project ID, WIF provider, service account).

## When GCP Output Values Are Pasted

Immediately set GitHub Variables via API — no manual UI action required:

```bash
gh variable set GCP_PROJECT_ID --body "<value>"
gh variable set GCP_WORKLOAD_IDENTITY_PROVIDER --body "<value>"
gh variable set GCP_SERVICE_ACCOUNT --body "<value>"
```

Then append to `dev/changes/[your-change-slug]/CHANGE-LOG.md`:
```
[YYYY-MM-DD] Agent — GitHub Variables set automatically — OK
```

## Pre-Implementation Gate

**Run this gate before writing any workflow, variable, or deployment configuration.**

1. Read `dev/changes/[your-change-slug]/CHANGE-LOG.md` — extract the Human Gate
   Budget table and record the HG count for the target stage.
2. For every `vars.*` reference you intend to introduce in a GitHub Actions workflow, verify it
   meets **one** of the following criteria:
   - It appears in RFC Step 6's enumerated variable list (`GCP_PROJECT_ID`,
     `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT`, `RAILWAY_SERVICE_NAME`), **or**
   - It is derived at runtime (e.g., `railway domain`, `gcloud ... --format=value(...)`)
   If neither condition is met, **do not add the variable**. Redesign the step to derive the
   value programmatically.
3. Before writing the session summary's "Open items" section, confirm that no item adds a human
   action in a 0-HG stage. If one does, replace it with the agent-driven or runtime equivalent.

> Skipping this gate caused a spec violation in the 2026-04-18 Stage 2 session:
> `RAILWAY_PUBLIC_URL` was introduced as a static `vars.*` reference and incorrectly reported
> as a manual operator task. It was later replaced by `railway domain` at runtime.

## Runbook Generation Protocol

When asked to generate or re-generate the Cloud Shell runbook:

1. **Read** `dev/changes/[your-change-slug]/RFC.md` — extract:
   - `GCP_PROJECT_ID` placeholder or existing value
   - Required service accounts, roles, secrets
   - Idempotency constraints (operations that must be safe to run twice)

2. **Output 5 batches** with the following structure per batch:
   ```
   ## Batch N — <Title>
   ### Purpose
   <one sentence>
   ### Commands
   <gcloud / shell commands>
   ### Checkpoint validation
   <command that proves the batch succeeded>
   ### Expected output
   <what a passing checkpoint looks like>
   ```

3. **Idempotency rules** (enforce in every command):
   - `gcloud ... --project $PROJECT` — always explicit project
   - Use `--quiet` to suppress interactive prompts
   - Prefix destructive operations with existence checks:
     `gcloud secrets describe <name> 2>/dev/null || gcloud secrets create <name>`
   - Service account creation: check before create:
     `gcloud iam service-accounts describe <email> 2>/dev/null || gcloud iam service-accounts create ...`

## Batch 5 Output Capture

Batch 5 must always end with:
```bash
WIF_PROVIDER=$(gcloud iam workload-identity-pools providers describe ... --format='value(name)')
[ -z "$WIF_PROVIDER" ] && { echo "ERROR: WIF provider not found — re-run Batch 3"; exit 1; }
echo "--- PASTE THESE BACK TO THE AGENT ---"
echo "GCP_PROJECT_ID: $PROJECT_ID"
echo "GCP_WORKLOAD_IDENTITY_PROVIDER: $WIF_PROVIDER"
echo "GCP_SERVICE_ACCOUNT: $SA_EMAIL"
```

## Change Log Updates

After every confirmed batch completion, append to CHANGE-LOG.md:
```
[YYYY-MM-DD] Operator — Batch N (<title>) — <OK | FAILED: reason>
```

## Error Handling

| Error | Action |
|-------|--------|
| Batch fails checkpoint | Stop. Document in CHANGE-LOG. Ask operator for output. |
| `PERMISSION_DENIED` on gcloud | Verify `roles/owner` or required role on project. |
| GitHub Variable set fails | Fall back to manual instruction with exact UI steps. |
| `ALREADY_EXISTS` on resource creation | Safe — resource is idempotent. Continue. |

## Self-Correction Loop

If a batch fails:
1. Read the error output
2. Identify root cause (IAM, quota, API not enabled)
3. Generate a targeted fix command
4. Re-run checkpoint — max 3 attempts before escalating to operator

## Output Format

Always end with a status table:
```
| Batch | Title | Status | Checkpoint |
|-------|-------|--------|------------|
| 1 | Enable APIs | ✓ | OK |
| 2 | Service Account | ✓ | OK |
| 3 | WIF Pool | pending | — |
| 4 | Secret Manager | pending | — |
| 5 | Output capture | pending | — |
```
