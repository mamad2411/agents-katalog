---
name: testing-pack
description: Deploys and tests a starter pack using the two-stack preserve-infrastructure model via agent-browser. Validates ORM UI schema screens, uploads and applies infra then app stacks, monitors deployment health, and runs application smoke tests. Use when the user says 'test this pack', 'deploy and test', or 'run the two-stack test.'
user-invocable: true
allowed-tools: Bash, Read, Edit, Write, AskUserQuestion, Glob, Grep, Agent
argument-hint: [category] [size]
---

# Testing Pack

End-to-end two-stack testing orchestrator. Manages the full lifecycle: discover/create ORM stacks, validate schema UI, upload zips via CDP, apply infra then app, monitor deployment, run smoke tests, and report results.

**Two-stack model:** `deploy_application=false` creates infra-only (VCN, OKE, GPU nodes). `existing_cluster_id` creates app-only (Corrino, blueprints, Helm) on the existing cluster. App stack can be destroyed independently — GPU nodes are preserved.

## CRITICAL RULES

1. **ALL stack operations MUST use agent-browser.** Do NOT fall back to OCI CLI for stack creation, updates, or applies. The entire point of this skill is to test the user experience through the browser. OCI CLI bypasses ORM's UI validation (required fields, schema visibility) and misses bugs that real users would hit.

2. **On Step 2 (Configure Variables), check for required field validation errors** before clicking Next. Look for "This variable is required" text. If any required fields are empty, fill them via agent-browser (or ask the user for values). Do NOT skip past validation errors.

3. **OCI CLI is ONLY used for:** listing stacks (Phase 1 discovery), resolving compartment OCIDs, and kubectl/helm commands. Never for stack create/update/apply.

4. **ALWAYS Destroy before deleting an app stack.** If an app stack exists and needs to be replaced (e.g., testing a different pack on the same infra), you MUST run ORM Destroy first to clean up all Kubernetes resources (Helm releases, secrets, configmaps, PVCs). Deleting the ORM stack without destroying orphans all resources on the cluster, causing "already exists" errors on the next deploy. Use the Destroy button in agent-browser or `oci resource-manager job create-destroy-job`.

5. **Use an isolated agent-browser session** to avoid conflicts with other Claude sessions or parallel tracks. Generate a unique session name at the start:
   ```bash
   SESSION_NAME="oci-$(date +%s)"
   ```
   Use `--session $SESSION_NAME` (NOT `--session-name`) on ALL agent-browser commands. Close the session when done: `agent-browser --session $SESSION_NAME close`

   **IMPORTANT: `--session` vs `--session-name` are different flags:**
   - `--session <name>` — Creates a **separate isolated browser instance** with its own cookies, storage, and navigation. **Use this one.** This is required for parallel test tracks to avoid browser conflicts.
   - `--session-name <name>` — Only persists cookies/localStorage under a name but **shares** the browser daemon with all other sessions. Do NOT use this for parallel testing.

## Arguments

- `$0` - Category: `paas_rag`, `enterprise_rag`, `enterprise_rag_aiq`, `cuopt`, `vss`, `dox_pack`
- `$1` - Size: `poc`, `small`, `medium` (category-dependent)
- `--zip-path <path>` (optional) — Path to a pre-built ORM zip. When provided, **skip Phase -1 (worktree) and Phase 2 (zip creation)** entirely. The zip is used as-is for both infra and app stacks. This is the preferred mode during release testing, where zips are already built and verified.

---

## Phase -1: Create Isolated Worktree

**Skip this phase if `--zip-path` was provided.** Set `ZIP_PATH` to the provided path and proceed directly to Phase 0.

Create a git worktree based on the **current branch** (not main, unless the current branch IS main). This isolates the test run from the working directory so concurrent work doesn't interfere.

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
WORKTREE_NAME="testing-pack-$(date +%s)"
WORKTREE_PATH="/tmp/${WORKTREE_NAME}"
# Use --detach to avoid "already checked out" error when the branch is in use
git worktree add --detach "${WORKTREE_PATH}" HEAD
cd "${WORKTREE_PATH}"
echo "Working in worktree: ${WORKTREE_PATH} (detached at ${CURRENT_BRANCH})"
```

All subsequent commands in this skill run from `${WORKTREE_PATH}`. At the end of the test (Phase 7), clean up:

```bash
cd /tmp  # exit the worktree first
git worktree remove "${WORKTREE_PATH}" --force 2>/dev/null
```

---

## Phase 0: Gather Parameters

Always collect before proceeding. Use `AskUserQuestion` for each.

### 0a. Category and size

If not provided as arguments, ask. Valid sizes per category:

| Category | Sizes |
|---|---|
| `cuopt` | `poc`, `small`, `medium` |
| `vss` | `poc`, `small`, `medium` |
| `paas_rag` | `small`, `medium` |
| `enterprise_rag` | `small` |
| `enterprise_rag_aiq` | `small` |
| `dox_pack` | `small` |

### 0b. OCI CLI profile

Show available profiles:

```bash
grep '^\[' ~/.oci/config | tr -d '[]'
```

Ask user to select one. Common values: `SANJOSE`, `DEFAULT`.

### 0c. Region

If the user specifies a region, use it. If not, determine the region based on the pack's GPU requirements:

**For `paas_rag` (no GPU):** Ask the user which region to use. Default: `us-sanjose-1`. Any region works since paas_rag only needs CPU shapes.

**For GPU packs (`enterprise_rag`, `enterprise_rag_aiq`, `cuopt`, `vss`):** Run `/checking-capacity <category> <size>` to find regions with both hardware availability AND quota. Present the results and let the user pick a region from those with capacity. If no region has capacity, stop and report — don't deploy into a region that will fail the capacity check.

The category-to-shape mapping is defined in `ai-accelerator-tf/vars.tf` under `local.starter_pack_configs` — look up `worker_node_shape` for the given category/size. Do NOT hardcode shape mappings in this skill; always read from `vars.tf` as the source of truth.

### 0d. Compartment

Ask for compartment name. Resolve OCID:

```bash
export OCI_CLI_PROFILE=<profile>
oci iam compartment list --compartment-id-in-subtree true --all \
  --query "data[?name=='<compartment-name>'].id | [0]" --raw-output
```

### 0e. PR-specific requirements

Ask: "Any PR-specific testing requirements or variables I should know about?"

### 0f. Pack-specific required variables

Generate random values for credentials that ORM requires but are only used at apply time. These will be filled into the ORM UI on Step 2:

```bash
# Generate random admin credentials (used for all packs)
ADMIN_USER="admin"
ADMIN_PASS=$(openssl rand -base64 12 | tr -d '/+=' | head -c 16)
ADMIN_EMAIL="test@example.com"
# DB password must be 12+ chars with uppercase, lowercase, number, and special char
DB_PASS="Aa1!$(openssl rand -base64 16 | tr -d '/+=' | head -c 12)"
echo "Admin: $ADMIN_USER / $ADMIN_PASS / $ADMIN_EMAIL / DB: $DB_PASS"
```

Pack-specific credentials:

| Category | Additional variables | Action |
|---|---|---|
| `cuopt` | `cuopt_frontend_admin_username`, `cuopt_frontend_admin_password` | Generate random |
| `enterprise_rag` | (none extra) | NGC keys have defaults in vars.tf |
| `enterprise_rag_aiq` | `tavily_api_key` | Ask user — real API key |
| `paas_rag` | (none extra) | — |
| `vss` | (none extra) | NGC keys have defaults in vars.tf |
| `dox_pack` | `dac_billing_acknowledgement=true` | Set automatically |

**NGC keys (`ngc_secret`, `ngc_api_secret`):** These have default values in `vars.tf` and are hidden in the ORM schema. Do NOT ask the user for them.

**Tavily API key:** Only `enterprise_rag_aiq` requires this. Ask the user — it's a real API key with no default.

### 0g. ADB packs

If category is `paas_rag`, `enterprise_rag`, or `enterprise_rag_aiq`, note that it requires `autonomous_db_subnet`. Confirm the schema includes ADB-specific fields.

### 0h. PR number (auto-detect, or ask)

Auto-detect if an open PR exists for the current branch:

```bash
CURRENT_BRANCH=$(git -C /Users/grantneuman/workspace/ai-accelerator-starter-packs rev-parse --abbrev-ref HEAD)
PR_NUMBER=$(gh pr view "${CURRENT_BRANCH}" --repo oci-ai-incubations/ai-accelerator-starter-packs --json number,state --jq 'select(.state=="OPEN") | .number' 2>/dev/null)
echo "Current branch: ${CURRENT_BRANCH}"
echo "Open PR:       ${PR_NUMBER:-<none>}"
```

**Decision tree:**

1. **If `PR_NUMBER` is populated:** proceed — post evidence (text + screenshots) to the PR at each milestone. Record `PR_NUMBER` for later phases.
2. **If no open PR but the current branch is NOT `main`:** ask the user via `AskUserQuestion`:
   > "No open PR found for branch `${CURRENT_BRANCH}`. Would you like me to create one now so testing evidence (text + screenshots) can be posted as PR comments?"
   - **"Yes, create PR now"** — run `gh pr create --title "..." --body "..."` with a stock body ("WIP — testing in progress via /testing-pack"). Record the returned PR number. Proceed.
   - **"Skip PR posting"** — proceed without posting; save all screenshots to `/tmp/` only.
3. **If the current branch IS `main`:** skip PR posting silently (PRs don't target the main branch).
4. **If the caller passed `PR_NUMBER=<number>` explicitly in the invocation message (e.g., from `/releasing`):** use that number directly; skip the auto-detect.

**When `PR_NUMBER` is set, post a comment at each major milestone.** Save screenshots locally to `/tmp/` during the run — they will be uploaded in bulk at end-of-run via the side-branch flow in [`references/pr-screenshot-upload.md`](references/pr-screenshot-upload.md).

Basic comment template:
```bash
gh pr comment $PR_NUMBER --body "$(cat <<'EOF'
## <milestone name>

<context and text evidence>

Screenshots will be attached in the bulk upload at end-of-run.
- `/tmp/<path>.png` — <what it shows>
EOF
)"
```

**Milestones to post at:**
- Phase 3 complete: schema validation results (any bug findings captured here)
- Phase 4 complete: infra apply succeeded (OCID outputs)
- Phase 5 complete: app apply succeeded (frontend_skin_urls, starter_pack_url, pod counts)
- After each test phase (6c-1, 6c-2, 6c-3): test results table
- Phase 7: final summary with all results combined

Each comment should describe the evidence in text form (accessibility-tree snippets, test tables, kubectl output) so the PR is meaningful even before screenshots are attached. Screenshots add visual confirmation.

---

## Phase 1: Discover Existing Stacks

List ORM stacks in the compartment:

```bash
oci resource-manager stack list -c <compartment-ocid> --all \
  --lifecycle-state ACTIVE --region <region> \
  --query "data[].{id:id, name:\"display-name\", time:\"time-created\"}"
```

Classify stacks by name pattern:
- **Infra stack:** name contains `infra` or `infrastructure`
- **App stack:** name contains `app` or `application`

Report findings to user. Ask to confirm which stacks to use. Determine action:

| Infra exists? | App exists? | Action |
|---|---|---|
| Yes | Yes | Update both with new zip |
| Yes | No | Update infra, create new app stack |
| No | Yes | Create new infra, update app stack |
| No | No | Create both stacks |

Record stack OCIDs for later phases.

---

## Phase 2: Zip

**Skip this entire phase if `--zip-path` was provided.** Set `ZIP_PATH` to the provided path and proceed directly to Phase 3. The pre-built zip is used as-is — no worktree, schema gen, or zip creation needed.

When building a zip (no `--zip-path`), define `ZIP_PATH` using the unique worktree name to avoid race conditions with parallel tracks:
```bash
ZIP_PATH="/tmp/${WORKTREE_NAME}.zip"
```
All zip operations in this phase and uploads in Phases 4-5 MUST use `${ZIP_PATH}`, never a hardcoded path like `/tmp/testing-pack.zip`.

### 2a. Set category in auto.tfvars

```bash
echo 'starter_pack_category = "<category>"' > ai-accelerator-tf/starter_pack_category.auto.tfvars
```

### 2b. Regenerate schema

```bash
cd "$(git rev-parse --show-toplevel)"
source venv/bin/activate
python3 create_final_schema.py -c <category>
```

### 2c. Create zip

Same exclusion logic as `/zip-tf`. **Use a unique zip path derived from the worktree name** to avoid race conditions when multiple tracks run in parallel:

```bash
ZIP_PATH="/tmp/${WORKTREE_NAME}.zip"
rm -rf ai-accelerator-tf/.terraform ai-accelerator-tf/.terraform.lock.hcl
cd ai-accelerator-tf && zip -r "${ZIP_PATH}" . \
  -x '.terraform/*' '.terraform.lock.hcl' '*.tfvars' \
  '*__pycache__/*' '*.pytest_cache/*' 'tests/*' \
  'schemas/generated/*' 'schemas/tests/*'
zip "${ZIP_PATH}" starter_pack_category.auto.tfvars
```

### 2d. Verify zip

```bash
unzip -l "${ZIP_PATH}" | head -30
# Confirm: schema.yaml present, no .tfvars (except auto.tfvars), TF files at root

# Verify schema matches expected category
SCHEMA_TITLE=$(unzip -p "${ZIP_PATH}" schema.yaml | grep '^title:' | head -1)
echo "Schema title: ${SCHEMA_TITLE}"
# Must match expected pack — if it shows a different pack name, the zip is wrong. Stop and rebuild.
```

Same zip is used for both infra and app stacks.

---

## Phase 3: ORM UI Schema Validation

All ORM interactions use `agent-browser` in headed mode (`--headed --session $SESSION_NAME`).

### 3a. Authenticate to OCI Console

Open the OCI Console and check if authenticated. See [orm-browser-nav.md](references/orm-browser-nav.md) for the full login flow.

1. `agent-browser --headed --session $SESSION_NAME open "https://cloud.oracle.com"`
2. Take a snapshot — if login form visible (User Name / Password fields, or redirected to sign-in page), ask the user to enter credentials in the browser window. **Wait for user confirmation before proceeding.**
3. If Console home page visible, continue.

### 3b. Verify region

Take a screenshot. Check the region menu button text. If it does not match the target region, switch:

1. Click the region menu button
2. Select the target region
3. Wait for page reload
4. Screenshot to confirm

### 3c. Verify compartment

Check the compartment heading/breadcrumb. If wrong, switch using the compartment picker:

1. Click compartment dropdown
2. Type compartment name to filter
3. Click the matching treeitem
4. Wait for page reload

See `references/orm-browser-nav.md` for selector patterns.

### 3c. Validate infra stack Edit wizard

Navigate to the infra stack detail page. Click "Edit".

**Step 1 (Stack Information):** Screenshot. Verify stack name and description.

**Step 2 (Configure Variables):** Click "Next". Screenshot. Validate:
- `deploy_infrastructure` is checked / true
- `deploy_application` is unchecked / false
- GPU/node pool fields are visible
- `existing_cluster_id` is empty or hidden
- For ADB packs: `autonomous_db_subnet` field is visible

**Cancel** the wizard after validation (do not save).

### 3d. Validate app stack Edit wizard

Navigate to the app stack detail page. Click "Edit".

**Step 2 (Configure Variables):** Click through to Step 2. Screenshot. Validate:
- `deploy_application` is checked / true
- `deploy_infrastructure` is unchecked / false
- `existing_cluster_id` is populated with the infra cluster OCID
- For ADB packs: `autonomous_db_subnet` field is visible and populated

**Cancel** the wizard after validation.

### 3e. Report schema validation results

Summarize which fields were correct/incorrect. If any field is wrong, stop and report to user before proceeding to Phase 4.

---

## Phase 4: Create and Apply Infra Stack

**Do NOT create or fill in the app stack yet.** The app stack needs infra outputs (cluster OCID, ADB subnet OCID) which don't exist until infra apply succeeds.

### 4a. Upload latest zip and create/update infra stack

**Always upload the fresh zip from Phase 2** — even if the stack already exists. Phase 3 validation cancels the wizard, which discards any upload.

- If the infra stack **already exists**: navigate to it, click "Upload new zip file link" or Edit → Edit stack
- If creating **new**: navigate to Create Stack page

Upload the zip via CDP (see `references/cdp-file-upload.md`), fill in the stack name, and click through the wizard:

- Step 1: Upload zip, set name with date/time (e.g., `Enterprise RAG AIQ - Infra - 2026-04-02 0946`), click Next
- Step 2: Fill variables:
  - **CRITICAL: Verify `starter_pack_size` matches the target size** (e.g., `poc`, `small`, `medium`). The ORM schema defaults to `small` — if you're testing `poc`, you MUST change the dropdown. Deploying the wrong size silently provisions the wrong GPU shape (e.g., BM.GPU4.8 instead of VM.GPU.A10.2). This is a known pitfall — see LESSONS_LEARNED.md.
  - Uncheck `Deploy Application`
  - Check `Skip Capacity Check`
  - Fill admin/DB credentials
  - Validate no required field errors before clicking Next.
  - **SIZE VERIFICATION GATE:** Before clicking Next, take a snapshot and confirm the `starter_pack_size` dropdown displays the expected value (e.g., `poc`, `small`, `medium`). If it shows the wrong size, change it now. Do NOT proceed to Step 3 until the size is confirmed correct. Log the verified size in your status output.
- Step 3: Check "Run apply", click Create

See `references/orm-browser-nav.md` for checkbox toggling, password validation, and React Select patterns.

### 4b. Monitor infra apply with kubectl

Record the job OCID. Once the OKE cluster is created (visible in ORM logs), **connect via kubectl** and monitor both ORM logs AND actual cluster state:

1. **Poll ORM job status** every 60 seconds via OCI CLI
2. **Connect to cluster** as soon as ORM logs show the cluster is created — generate kubeconfig and patch with profile (see `references/kubeconfig-patching.md`)
3. **Check nodes and pods** via kubectl each cycle
4. **Check instance pool work requests** if ORM logs show instance_pool "Still creating..." — surfaces GPU capacity failures immediately (see `/monitoring-deployment` step 3.2)
5. **Report status** each cycle

Invoke `/monitoring-deployment` if available, or run checks inline.

**If infra fails:** invoke `/diagnosing-stack`, report to user, stop.

### 4c. Extract infra outputs

After infra succeeds, navigate to the stack's "Application Information" tab and extract:
- **Cluster OCID** — needed for `existing_cluster_id` in app stack
- **ADB Subnet OCID** — needed for `existing_autonomous_db_subnet_id` (for ADB packs)

Use agent-browser eval to get the values:
```bash
agent-browser --session $SESSION_NAME eval --stdin <<'EVALEOF'
var iframe = document.querySelector('iframe');
var doc = iframe.contentDocument || iframe.contentWindow.document;
var text = doc.body.innerText;
var cluster = text.match(/OKE Cluster OCID:\s*(ocid1\.\S+)/);
var subnet = text.match(/Autonomous DB Subnet OCID:\s*(ocid1\.\S+)/);
JSON.stringify({cluster: cluster ? cluster[1] : null, subnet: subnet ? subnet[1] : null});
EVALEOF
```

---

## Phase 5: Create and Apply App Stack

**Only proceed after infra outputs are available.**

### 5a. Upload latest zip and configure app stack

**You MUST upload the fresh zip from Phase 2** — even if the stack already exists and had a zip uploaded during schema validation (Phase 3). Phase 3 cancels the wizard, which discards the upload.

- If the app stack **already exists**: navigate to it, click "Upload new zip file link" or Edit → Edit stack
- If creating **new**: navigate to Create Stack page

Upload the zip via CDP (see `references/cdp-file-upload.md`). Then click through the wizard:

- Step 1: Upload zip, set name with date/time (e.g., `Enterprise RAG AIQ - App - 2026-04-02 0946`), click Next
- Step 2: Fill variables:
  - **CRITICAL: Verify `starter_pack_size` matches the target size** (must match infra stack). ORM defaults to `small` — if testing `poc`, you MUST change the dropdown.
  - `Deploy Application` = checked
  - `Skip Capacity Check` = checked
  - `Existing Cluster OCID` = cluster OCID from Phase 4c
  - `Existing Node Subnet OCID` = node subnet OCID from Phase 4c (**required** — without this, shared_node_pool recipes fail with nil pointer or subnetId validation error. See BUG-016.)
  - `Existing Autonomous DB Subnet OCID` = subnet OCID from Phase 4c (for ADB packs)
  - Fill admin/DB credentials (same as infra stack)
  - Validate no required field errors
  - **SIZE VERIFICATION GATE:** Before clicking Next, take a snapshot and confirm the `starter_pack_size` dropdown displays the expected value (must match infra stack). If it shows the wrong size, change it now. Do NOT proceed to Step 3 until the size is confirmed correct. Log the verified size in your status output.
- Step 3: Check "Run apply", click Create

### 5b. Monitor app apply with kubectl

Record the job OCID. **Connect to the cluster via kubectl** (using the cluster OCID from Phase 4c — see `references/kubeconfig-patching.md`) and monitor both ORM logs AND actual container status:

1. **Poll ORM job status** every 60 seconds via OCI CLI
2. **Check pods across all namespaces** via kubectl:
   ```bash
   export KUBECONFIG=$HOME/.kube/config-<short_name>
   kubectl get pods --all-namespaces --no-headers
   ```
3. **Check Helm releases** for failures:
   ```bash
   helm list --all-namespaces --all
   ```
4. **Investigate non-healthy pods** — describe pending/crashing pods, get logs
5. **Report status** each cycle: ORM job state + pod counts + any issues

This is critical — ORM logs only show "Still creating..." but kubectl reveals the actual container state (image pulls, scheduling failures, crashes). Invoke `/monitoring-deployment` if available, or run the checks inline.

**If app fails:**

1. Invoke `/diagnosing-stack` to identify root cause
2. If the failure is a **first-time error** (e.g., missing variable, bad config): fix and retry once
3. If the failure involves **orphaned resources or repeated apply failures** ("already exists", "cannot re-use name", repeated timeouts, resources stuck in bad state after cleanup attempts): **destroy both stacks and start completely fresh.** Don't waste time manually cleaning up a messy cluster — it's faster to destroy everything and recreate from scratch. This may take a long time (bare-metal GPU hosts can take up to 6 hours to recycle), but a clean start is more reliable than manually cleaning up partial state.

To destroy and start fresh:
```bash
# Destroy app stack first (if it has state)
oci resource-manager job create-destroy-job --stack-id <app_stack_ocid> --execution-plan-strategy AUTO_APPROVED
# Wait for destroy to complete, then destroy infra
oci resource-manager job create-destroy-job --stack-id <infra_stack_ocid> --execution-plan-strategy AUTO_APPROVED
# Delete both stacks after destroy completes
oci resource-manager stack delete --stack-id <app_stack_ocid> --force
oci resource-manager stack delete --stack-id <infra_stack_ocid> --force
```

After destroy completes, clean up resources that ORM destroy may not remove:

```bash
# Delete customer secret keys (quota of 2 per user — must clean up or next deploy fails)
oci iam customer-secret-key list --user-id <current_user_ocid> --query 'data[].id' --raw-output | while read key_id; do
  oci iam customer-secret-key delete --user-id <current_user_ocid> --customer-secret-key-id "$key_id" --force
done

# Delete ADB if it wasn't cleaned up by destroy (check compartment)
oci db autonomous-database list --compartment-id <compartment_ocid> --lifecycle-state AVAILABLE --query 'data[].id' --raw-output | while read adb_id; do
  oci db autonomous-database delete --autonomous-database-id "$adb_id" --force
done
```

Then restart from Phase 4 with fresh stacks. Report the failure and fresh-start to the user.

### 5c. Extract app outputs

After app succeeds, extract output URLs from "Application Information" tab:
- `starter_pack_url` — base URL for the deployed pack
- `frontend_skin_urls` — map output of `skin_name -> URL` for every deployed skin. Use this as the source of per-skin frontend URLs (a pack may deploy multiple skins). For single-skin packs the map still contains a single entry; iterate the map rather than hardcoding a skin name.
- Cluster OCID (for kubectl connection)

---

## Phase 6: Application Testing

### 6a. Get output URLs

From the app stack's "Application Information" tab in agent-browser, extract:
- Frontend URL
- API URL (if separate)

### 6b. Navigate to app

The deployed apps use self-signed certificates (nip.io domains). You must relaunch agent-browser with `--ignore-https-errors`:

```bash
agent-browser --session $SESSION_NAME close 2>/dev/null
agent-browser --headed --session $SESSION_NAME --ignore-https-errors open "https://<frontend-url>"
```

Verify the page loads (HTTP 200, expected content visible in snapshot).

### 6c. Run ALL pack-specific tests (Infra, API, UI)

Determine the test coverage directory for the category:

| Category | Test coverage directory |
|---|---|
| `paas_rag` | `.claude/skills/paas-rag-test-coverage/` |
| `enterprise_rag` | `.claude/skills/enterprise-rag-test-coverage/` |
| `enterprise_rag_aiq` | `.claude/skills/enterprise-rag-test-coverage/` |
| `cuopt` | `.claude/skills/cuopt-test-coverage/` |
| `vss` | `.claude/skills/vss-test-coverage/` |
| `dox_pack` | `.claude/skills/dox-pack-test-coverage/` |

Execute **ALL THREE** test phases in order. Do NOT skip any phase. If a test fails, record the failure and continue to the next test. Only stop the entire sequence if the frontend is unreachable (HTTP connection refused).

#### 6c-1. Execute Infra tests

> **JUST-IN-TIME LOADING:** Read `.claude/skills/<category>-test-coverage/infra-tests.md` NOW. This file is self-contained — it has every infrastructure test with kubectl/OCI CLI commands, expected output, and failure hints. Execute directly from it.

For every test in `infra-tests.md`:
1. Execute via `kubectl` or OCI CLI as specified in the file.
2. Compare output against the verification criteria.
3. Record pass/fail per test ID.

If `PR_NUMBER` is set, post results to the PR:
```bash
gh pr comment $PR_NUMBER --body "$(cat <<'EOF'
### <category>/<size> — Infra Test Results

| ID | Test | Result |
|---|---|---|
| XX-1 | Description | PASS/FAIL |
...

**X/Y passed**
EOF
)"
```

#### 6c-2. Execute API tests

> **JUST-IN-TIME LOADING:** Read `.claude/skills/<category>-test-coverage/api-tests.md` NOW. This file is self-contained — it has every API test with endpoint, method, request body, verification criteria, and curl commands. Execute directly from it.

For every test in `api-tests.md`:
1. Execute via `curl` using the frontend URL as the base URL.
2. Compare HTTP status code and response body against the verification criteria.
3. Record pass/fail per test ID.
4. Pass forward any outputs needed by later tests (e.g., collection IDs, file IDs).

If `PR_NUMBER` is set, post results to the PR (same table format as 6c-1).

#### 6c-3. Execute UI tests

> **JUST-IN-TIME LOADING:** Read `.claude/skills/<category>-test-coverage/ui-tests.md` NOW. This file is self-contained — it has every UI test with agent-browser commands, interaction steps, and verification criteria. Execute directly from it.

For every test in `ui-tests.md`:
1. Execute via `agent-browser` following the file's Session Setup and test steps.
2. Take screenshots as evidence per the file's instructions.
3. Record pass/fail per test ID.

If `PR_NUMBER` is set, post results to the PR (same table format as 6c-1).

If no test coverage directory exists for the category, fall back to basic smoke tests:
1. Frontend loads (HTTP 200)
2. Main page renders without errors
3. At least one API health endpoint returns 200

---

## Phase 7: Cleanup and Report

### 7a. Upload screenshots to PR (if PR_NUMBER set)

If `PR_NUMBER` was set in Phase 0h, upload all screenshots collected during the run to a side branch and embed them into the per-milestone PR comments. Follow the 3-step flow in [`references/pr-screenshot-upload.md`](references/pr-screenshot-upload.md):

1. Stage screenshots in `$SHOT_DIR` with `<track>/<phase>/*.png` hierarchy.
2. Push to `screenshots/pr-${PR_NUMBER}` via a **side clone** (do NOT touch the primary working tree).
3. PATCH each PR comment's body to append `![caption](<raw URL>)` for its screenshots.

Expected file layout in the screenshots branch:
```
pr-<PR_NUMBER>/
  <track or phase>/
    phase3-schema.png
    phase4-infra-success.png
    phase5-app-success.png
    frontend-loaded.png
    ui-evidence/
      PU-01-*.png
      ...
```

Skip this step if no PR number was set.

### 7b. Object Storage post-destroy cleanup handoff (`paas_rag` / `dox_pack`)

If the tested category is `paas_rag` or `dox_pack`, record the Object Storage bucket details before closing the app stack browser page:

- `paas_rag_bucket_name` from the app stack's Application Information tab
- `object_storage_namespace` from the app stack's Application Information tab
- app stack OCID and region

When this pack is destroyed, the teardown owner MUST verify the bucket is gone before moving to the next pack or destroying infra. The app stack destroy normally deletes the bucket. If app destroy fails with `409-BucketNotEmpty`, or if the bucket still exists after destroy, purge current objects plus versioned objects/delete markers, then retry app destroy if the stack still has state.

```bash
export OCI_CLI_PROFILE=<profile>
REGION=<region>
APP_STACK_ID=<app_stack_ocid>
BUCKET=<paas_rag_bucket_name_from_application_information>
NAMESPACE=<object_storage_namespace_from_application_information>
RETRY_APP_DESTROY=true  # set false if the app destroy job already SUCCEEDED

# Nothing to do if Terraform already deleted the bucket.
if ! oci os bucket get --bucket-name "${BUCKET}" --namespace-name "${NAMESPACE}" --region "${REGION}" >/dev/null 2>&1; then
  echo "Bucket ${BUCKET} is already deleted."
  exit 0
fi

# If the app destroy failed with BucketNotEmpty, purge current objects first.
oci os object bulk-delete --bucket-name "${BUCKET}" --namespace-name "${NAMESPACE}" --region "${REGION}" --force --include '*' || true

# Then purge versioned objects/delete markers. These are what normal list/bulk-delete misses.
oci os object list-object-versions --bucket-name "${BUCKET}" --namespace-name "${NAMESPACE}" --region "${REGION}" --all --output json | python3 -c '
import json
import subprocess
import sys

bucket, namespace, region = sys.argv[1:4]
payload = json.load(sys.stdin)
data = payload.get("data") or {}
items = data.get("items") if isinstance(data, dict) else data
items = items or []

for item in items:
    name = item.get("name")
    version_id = item.get("version-id") or item.get("versionId")
    if not name or not version_id:
        continue
    subprocess.run([
        "oci", "os", "object", "delete",
        "--bucket-name", bucket,
        "--namespace-name", namespace,
        "--region", region,
        "--name", name,
        "--version-id", version_id,
        "--force",
    ], check=False)

print(f"purged {len(items)} object versions/delete markers from {bucket}")
' "${BUCKET}" "${NAMESPACE}" "${REGION}"

# If the previous app destroy failed, retry it now before touching infra.
if [ "${RETRY_APP_DESTROY}" = "true" ]; then
  DESTROY_JOB_ID=$(oci resource-manager job create-destroy-job \
    --stack-id "${APP_STACK_ID}" \
    --region "${REGION}" \
    --execution-plan-strategy AUTO_APPROVED \
    --query 'data.id' \
    --raw-output)
  echo "Retry destroy job: ${DESTROY_JOB_ID}"
  # Poll this job until it reaches SUCCEEDED or FAILED before continuing.
fi

# After app destroy is complete, delete any orphaned empty bucket that remains.
if oci os bucket get --bucket-name "${BUCKET}" --namespace-name "${NAMESPACE}" --region "${REGION}" >/dev/null 2>&1; then
  oci os bucket delete \
    --bucket-name "${BUCKET}" \
    --namespace-name "${NAMESPACE}" \
    --region "${REGION}" \
    --empty \
    --force
fi
```

Do NOT proceed to infra destroy or the next CPU pack until the app destroy job has `SUCCEEDED` and `oci os bucket get` returns NotFound for the recorded bucket. Include `Object Storage bucket: deleted` or `not applicable` in the final report.

### 7c. Cleanup worktree

```bash
cd /tmp
git worktree remove "${WORKTREE_PATH}" --force 2>/dev/null
agent-browser --session $SESSION_NAME close 2>/dev/null
```

### 7d. Report

Present a structured summary:

```
=============================================
  TWO-STACK TEST REPORT - <category> <size>
  Date:   <YYYY-MM-DD>
  Region: <region>
=============================================

SCHEMA VALIDATION:
  Infra stack wizard:  PASS/FAIL
  App stack wizard:    PASS/FAIL
  Field issues:        <list any>

DEPLOYMENT:
  Infra stack apply:   PASS/FAIL  (<duration>)
  App stack apply:     PASS/FAIL  (<duration>)
  Pod status:          X/Y Running

CLUSTER HEALTH:
  Nodes:    <count> Ready
  Core pods: corrino-cp, postgres, portal — <status>
  Pack pods: <list> — <status>

INFRA TESTS:
  <test-id>: <description> — PASS/FAIL
  ...
  Result: X/Y passed

API TESTS:
  <test-id>: <description> — PASS/FAIL
  ...
  Result: X/Y passed

UI TESTS:
  <test-id>: <description> — PASS/FAIL
  ...
  Result: X/Y passed

ISSUES:
  - <issue description, affected resource, severity>
  ...

STACK IDs:
  Infra: <ocid>
  App:   <ocid>

POST-DESTROY HANDOFF:
  Object Storage bucket: <deleted / cleanup required / not applicable>
=============================================
```

---

## Error Handling

| Situation | Action |
|---|---|
| Schema validation fails | Stop, report to user, do not proceed to apply |
| CDP upload fails | Retry once; if still fails, report and stop |
| Infra apply fails | Show logs, invoke `/diagnosing-stack`, stop for user |
| App apply fails | Show logs, invoke `/diagnosing-stack`, stop for user |
| Pods not healthy after 15min | Invoke `/diagnosing-stack`, report, stop for user |
| App smoke tests fail | Report results, stop for user decision |
| Browser navigation fails | Take screenshot, report current page state, retry once |

**Never auto-remediate.** Always stop and wait for user guidance on failures.

---

## Notes

- ADB packs (`paas_rag`, `enterprise_rag`, `enterprise_rag_aiq`) need `autonomous_db_subnet` visible in both stacks.
- The same zip is used for both infra and app stacks — the schema and variables control which resources are created.
- `deploy_infrastructure` and `deploy_application` are the count-gating variables that separate the two stacks.
- After testing, the user decides whether to destroy the app stack (preserving infra) or both. Use `/destroy-stack` when ready.
