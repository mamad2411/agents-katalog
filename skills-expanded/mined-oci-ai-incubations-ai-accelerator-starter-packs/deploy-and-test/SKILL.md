---
name: deploy-and-test
description: Full deployment workflow - GPU capacity check across regions, region selection, ORM stack deploy, pod verification, and pack-specific testing (API + UI) via Playwright sub-agent.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Edit, Write, AskUserQuestion, WebFetch, Agent
argument-hint: [category] [size]
---

## CRITICAL: User interaction rules

Some steps in this skill require user input. Follow these rules strictly:

1. **Always use `AskUserQuestion`** for every question that needs user input. Do NOT skip questions or assume defaults.
2. **Verify the response is non-empty.** After `AskUserQuestion` returns, check that the `answers` field contains an actual selection. If the answer text after "User has answered your questions:" is empty or blank, the user was NOT actually asked. In that case:
   - **Output the question as plain text** in your response message (e.g., "Which OCI CLI profile should I use? Options: DEFAULT, SANJOSE") and **STOP and WAIT** for the user to reply in their next message.
   - Do NOT proceed with an assumed answer. Do NOT continue to the next step.
3. **Never assume a default answer.** If the user doesn't respond or the tool fails silently, halt and ask again via text output.
4. **One question at a time.** Don't batch unrelated questions — ask, wait for a real answer, then proceed.

---

# Deploy and Test

Full end-to-end deployment workflow: check GPU availability across regions, let the user pick a region, deploy the ORM stack, verify pods and outputs, run pack-specific API + UI tests via Playwright, then optionally destroy.

> **MANDATORY COMPLIANCE — READ BEFORE PROCEEDING**
>
> Every step in this skill **MUST** be executed **consecutively in order**. Do NOT skip, reorder, or combine steps. Do NOT assume a step's outcome — execute it and verify the result before moving to the next step.
>
> If you are confused, stuck, or unsure how to proceed at any step: **stop and ask the user for guidance.** Do NOT guess, improvise, or silently skip steps. The user must be informed of any deviation.
>
> Step 12b (asking the user for a test matrix) is **mandatory** — you must always ask the user whether they have additional tests, even if a base coverage spec exists. Never skip this prompt.

## Arguments

- `$0` - Starter pack category: `paas_rag`, `cuopt`, `vss`, `enterprise_rag`, `enterprise_rag_aiq`
- `$1` - Starter pack size: `poc`, `small`, `medium` (category-dependent)

If no arguments are provided, ask the user.

---

## Phase 0: Load Sandbox Environment

All temporary files, packages, and state live in an isolated sandbox created by `/setup`. **Nothing goes into the repo working tree.**

### Step 0a: Source sandbox env

```bash
# Find the most recent sandbox, or use the one already set
if [ -z "${DAT_SANDBOX}" ]; then
  DAT_SANDBOX=$(ls -td /tmp/dat-sandbox-* 2>/dev/null | head -1)
fi

if [ -z "${DAT_SANDBOX}" ] || [ ! -f "${DAT_SANDBOX}/env.sh" ]; then
  echo "ERROR: No sandbox found. Run /setup first."
  exit 1
fi

source "${DAT_SANDBOX}/env.sh"
echo "Sandbox: ${DAT_SANDBOX}"
```

This loads all environment variables into the session:

| Variable | Source | Used in |
|---|---|---|
| `DAT_SANDBOX` | Setup Step 1 | All phases — root for temp files |
| `OCI_CLI_PROFILE` | Setup Step 4 | All OCI CLI commands |
| `CORRINO_USERNAME` | Extracted from tfvars | Phase 3 login tests |
| `CORRINO_PASSWORD` | Extracted from tfvars | Phase 3 login tests |
| `COMPARTMENT_OCID` | Extracted from tfvars | Phase 2 stack creation |
| `STARTER_PACK_CATEGORY` | Extracted from tfvars | Phase 1 (can be overridden by arguments) |
| `STARTER_PACK_SIZE` | Extracted from tfvars | Phase 1 (can be overridden by arguments) |
| `PLAYWRIGHT_BROWSERS_PATH` | Setup Step 6 | Phase 3 UI tests |
| `VSS_BUCKET_NAME`, etc. | Setup Step 8 | Phase 3 pack-specific tests |

Sandbox sub-directories:

| Sub-directory | Contents |
|---|---|
| `api-results/` | curl response bodies (`VA-1.json`, `VA-5b.json`, etc.) |
| `ui-recordings/` | Continuous `.webm` video recordings from Playwright |
| `logs/` | ORM job logs, kubectl output, test reports |
| `zips/` | `lifecycle.zip` for ORM upload |
| `packages/` | npm packages, Playwright browsers |
| `venv/` | Python virtual environment |

### Step 0b: Quick prerequisite check

```bash
for tool in oci kubectl zip curl python3; do
  which "$tool" > /dev/null 2>&1 || echo "MISSING: $tool — run /setup"
done
```

If anything is missing, stop and tell the user: *"Run `/setup` first."*

---

## Phase 1: Pre-Flight — GPU Capacity & Region Selection

### Step 1: Get category and size from user

If not provided as arguments, ask:
- Category: `paas_rag`, `cuopt`, `vss`, `enterprise_rag`, `enterprise_rag_aiq`
- Size (valid options per category):
  - `cuopt`: `poc`, `small`, `medium`
  - `vss`: `small`, `medium`
  - `paas_rag`: `small`, `medium`
  - `enterprise_rag`: `small`
  - `enterprise_rag_aiq`: `small`

Also ask for `OCI_CLI_PROFILE` (common values: `SANJOSE`, `DEFAULT`) and any PR-specific testing requirements.

### Step 2: Look up required GPU shape

| Category | Size | GPU Shape | Nodes Needed |
|---|---|---|---|
| `cuopt` | `poc` | `VM.GPU.A10.2` | 1 |
| `cuopt` | `small` | `BM.GPU4.8` | 1 |
| `cuopt` | `medium` | `BM.GPU.A100-v2.8` | 1 |
| `vss` | `small` | `BM.GPU4.8` | 1 |
| `vss` | `medium` | `BM.GPU.L40S-NC.4` | 2 |
| `enterprise_rag` | `small` | `BM.GPU4.8` | 2 |
| `enterprise_rag_aiq` | `small` | `BM.GPU4.8` | 2 |
| `paas_rag` | `small` | *(no GPU required)* | 0 |
| `paas_rag` | `medium` | *(no GPU required)* | 0 |

For `paas_rag`, skip Steps 3–5 and ask the user to select any region.

### Step 3: Fetch GPU capacity dashboard

Use WebFetch to retrieve live capacity data:

```
URL: https://gpu-capacity.ai-apps-ord.oci-incubations.com/
```

Filter all rows where:
- **Shape** matches the required GPU shape
- **Status** is `AVAILABLE`
- **Available** count >= nodes needed

### Step 4: Present qualifying regions to user

Group filtered results by **Region**. A region qualifies if at least one Availability Domain meets the criteria.

Present as a numbered list:

```
Available regions for BM.GPU4.8 (need 2 nodes):
1. us-ashburn-1     — AD-1: 4 available
2. eu-frankfurt-1   — AD-2: 3 available
3. ap-tokyo-1       — AD-1: 2 available
```

If no regions qualify, report to the user and stop.

### Step 4b: Check service limit quota for qualifying regions

The capacity dashboard shows hardware availability, but deployments also require **tenancy quota**. For each region that passed Step 4's capacity filter, check the OCI service limit to confirm sufficient quota exists.

**GPU shape → limit name mapping:**

| GPU Shape | OCI Limit Name | GPUs per Node |
|---|---|---|
| `VM.GPU.A10.2` | `gpu-a10-count` | 2 |
| `BM.GPU4.8` | `gpu4-count` | 8 |
| `BM.GPU.A100-v2.8` | `gpu-a100-v2-8-count` | 8 |
| `BM.GPU.L40S-NC.4` | `gpu-l40s-nc-count` | 4 |

> **Note:** If the limit name is wrong (API returns `InvalidParameter`), discover the correct name with:
> ```bash
> oci limits definition list --service-name compute --compartment-id <TENANCY_OCID> --region <region> --all \
>   | python3 -c "import json,sys; [print(i['name'],'-',i['description']) for i in json.load(sys.stdin)['data'] if '<shape-keyword>' in i['name'].lower()]"
> ```
> Replace `<shape-keyword>` with `gpu4`, `a10`, `a100`, or `l40s` as appropriate.

**Query for each qualifying region:**

```bash
# Get tenancy OCID from terraform.tfvars
TENANCY_OCID=$(grep 'tenancy_ocid' ai-accelerator-tf/terraform.tfvars | head -1 | sed 's/.*= *"//' | sed 's/".*//')

# For each region + AD from Step 4:
oci limits resource-availability get \
  --service-name compute \
  --limit-name <limit-name> \
  --compartment-id "$TENANCY_OCID" \
  --availability-domain "<full-AD-name>" \
  --region <region>
```

The response contains `available` (remaining quota) and `used` (current usage). A region is **deployable** only if `available` >= (nodes needed × GPUs per node).

**Present a combined table:**

```
GPU Capacity + Quota for BM.GPU4.8 (need 1 node = 8 GPUs):

| # | Region         | AD   | Capacity Available | Quota Available | Quota Used | Deployable? |
|---|----------------|------|--------------------|-----------------|------------|-------------|
| 1 | us-sanjose-1   | AD-1 | 3                  | 8               | 24         | Yes         |
| 2 | ap-osaka-1     | AD-1 | 2                  | 0               | 16         | No — quota exhausted |
| 3 | uk-london-1    | AD-1 | 1                  | 0               | 0          | No — no quota |
```

If no region has both capacity AND quota, report to the user and stop.

### Step 5: User selects region

Ask the user to choose from **deployable** regions only (those with both capacity and quota). Record:
- **Region** (e.g., `us-ashburn-1`) → use as `region` in deployment
- **Availability Domain** (e.g., `AD-1`) → use as `worker_node_availability_domain`

### Step 5b: Set chosen region for all OCI commands

Once the region is chosen, **every** `oci` command for the rest of the run must use that region (stack, jobs, kubectl config, limits, etc.). Do one of the following:

**Option A — Environment variable (simplest):**
```bash
export OCI_CLI_REGION=<selected-region>
```
Append this to `${DAT_SANDBOX}/env.sh` so that re-sourcing the env in later phases keeps the region set. All subsequent `oci` commands will use `<selected-region>` without needing `--region` on each call.

**Option B — Temporary profile:** Create a small OCI config in the sandbox that uses the selected region, then use it for the rest of the run:
```bash
# Copy user's profile from ~/.oci/config, set region to selected
mkdir -p "${DAT_SANDBOX}"
# Build a minimal config: same user, tenancy, key_file, fingerprint as current profile, region=<selected-region>
export OCI_CLI_CONFIG_FILE="${DAT_SANDBOX}/oci-config"
export OCI_CLI_PROFILE=deploy
# (Write [deploy] section to OCI_CLI_CONFIG_FILE with region=<selected-region> and other keys from the user's profile.)
```
After this, all `oci` commands use the deploy profile and thus the chosen region.

Whichever option is used, **do not** rely on the default region from `~/.oci/config`; the stack and all jobs must run in the user-selected region.

---

## Phase 2: Deploy

**Region:** The selected region is already in effect from Step 5b (`OCI_CLI_REGION` or the deploy profile). All `oci resource-manager` and `oci ce` commands in this phase will use that region. You may still pass `--region <selected-region>` explicitly if desired.

### Step 6: Generate schema

```bash
cd "$(git rev-parse --show-toplevel)"
source venv/bin/activate
python3 create_final_schema.py -c $0
```

### Step 7: Create zip

Same exclusion logic as `/zip-tf`. Build FLAT (schema.yaml + .tf at the zip root)
and exclude the whole `schemas/` tree except `frontend_skins.yaml` (the only
schemas/ file Terraform reads at runtime). OCI RM's Console validates every
schema-shaped YAML in the archive and rejects source/generated/test schemas with
"Errors exist in your schema file" (see BUGS.md BUG-046). Re-add
`frontend_skins.yaml` and `starter_pack_category.auto.tfvars` (dropped by `*.tfvars`):

```bash
rm -rf ai-accelerator-tf/.terraform ai-accelerator-tf/.terraform.lock.hcl
cd ai-accelerator-tf && zip -r "${DAT_SANDBOX}/zips/lifecycle.zip" . \
  -x '.terraform/*' '.terraform.lock.hcl' '*.tfvars' '*__pycache__/*' '*.pytest_cache/*' 'tests/*' 'schemas/*'
zip "${DAT_SANDBOX}/zips/lifecycle.zip" schemas/frontend_skins.yaml starter_pack_category.auto.tfvars
```

### Step 8: Create ORM stack

Region is already set from Step 5b. Create the stack (no need to pass `--region` if `OCI_CLI_REGION` or the deploy profile is in use):

```bash
export OCI_CLI_PROFILE=<profile>   # or use deploy profile from Step 5b Option B
oci resource-manager stack create \
  --compartment-id "${COMPARTMENT_OCID}" \
  --config-source "${DAT_SANDBOX}/zips/lifecycle.zip" \
  --terraform-version "1.5.x" \
  --display-name "deploy-and-test-$0-$1" \
  --variables "{\"region\": \"<selected-region>\", \"worker_node_availability_domain\": \"<selected-ad>\", ...}"
```

Record the returned stack OCID.

### Step 9: Plan

Create a plan job (uses chosen region from Step 5b), poll until completion, check logs for errors. Stop and report to user if plan fails.

### Step 10: Apply

Create an apply job with `AUTO_APPROVED` (or from the plan job id); it will run in the chosen region. Poll until completion. Stop and report to user if apply fails.

### Step 11: Configure kubectl

Extract cluster OCID from apply logs:

```bash
oci ce cluster create-kubeconfig --cluster-id <cluster-ocid> --kube-endpoint PUBLIC_ENDPOINT
```

---

## Phase 3: Pack-Specific Testing (API + Infra + UI)

This phase executes tests against the live deployment using **just-in-time file loading** — each sub-phase reads only the file it needs.

Tests come from **two sources** that are merged together:

1. **Base coverage files** — pack-specific split test files in `.claude/skills/<category>-test-coverage/`:
   - `SKILL.md` — overview, env vars, known issues
   - `api-tests.md` — API test specs for curl execution
   - `infra-tests.md` — Infrastructure test specs for kubectl execution
   - `ui-tests.md` — UI test specs for Playwright execution
2. **User-provided test matrix** — additional tests the user wants to run.

Both are tested when both are present.

### Step 12: Locate base coverage spec + ask for user test matrix

#### 12a. Check for the base coverage files

Check if the split test coverage directory exists:

```
.claude/skills/<category>-test-coverage/SKILL.md
.claude/skills/<category>-test-coverage/api-tests.md
.claude/skills/<category>-test-coverage/ui-tests.md
.claude/skills/<category>-test-coverage/infra-tests.md
```

For example: `.claude/skills/vss-test-coverage/`, `.claude/skills/paas-rag-test-coverage/`, etc.

- **If found:** Read **only** `SKILL.md` (the overview file). Note which sub-files exist. Do NOT read `api-tests.md`, `ui-tests.md`, or `infra-tests.md` yet — they will be loaded just-in-time in their respective phases.
- **If not found:** Note it — the user-provided matrix (Step 12b) becomes the only source.

#### 12b. Ask the user for a test matrix (MANDATORY — DO NOT SKIP)

**You MUST ask this question every time, even if a base coverage spec was found in Step 12a.** Do not proceed to Step 13 without asking. Always ask:

> *"Do you have a test matrix or additional tests to run for this deployment? This can be:*
> - *A list of API endpoints to hit (method + URL + expected response)*
> - *UI pages/flows to verify*
> - *Infrastructure checks (kubectl commands, OCI CLI queries)*
> - *Or a file/URL containing the matrix*
>
> *If not, I'll proceed with the base coverage spec only."*

If the user provides a test matrix:

1. **Categorize each item** as `API`, `Infra`, or `UI` based on what it tests.
2. **Assign temporary IDs** using the pattern `UT-1`, `UT-2`, ... (User Test) to distinguish from base spec IDs.
3. **Merge with the base spec** — user tests run in addition to (not instead of) base tests.
4. **If the matrix includes UI tests**, clone the pack's frontend repo to understand the exact selectors, component structure, dialog types, and API calls before writing test code. See Step 17b for details.

#### 12c. Determine test sources

| Base spec found? | User matrix provided? | Action |
|---|---|---|
| Yes | Yes | Run both — base spec tests + user tests |
| Yes | No | Run base spec tests only |
| No | Yes | Run user tests only |
| No | No | Run basic smoke tests (subdomain resolution, health endpoint, frontend loads) |

### Step 13: Ask user for test scope

Present the **combined** test inventory and ask:

> Tests available for `<category>`:
>
> **Base coverage spec** (if present):
> - API tests: N items (from api-tests.md)
> - Infra tests: N items (from infra-tests.md)
> - UI tests: N items (from ui-tests.md)
>
> **User-provided tests** (if present):
> - API: N items
> - Infra: N items
> - UI: N items
>
> Which should I run?
> 1. All tests (recommended for fresh deploys)
> 2. P0 only from base spec + all user tests
> 3. API + UI only (skip infra)
> 4. Custom selection

Also ask if the user has any **additional test parameters** (e.g., bucket names, object keys, credentials beyond the standard Corrino admin).

### Step 14: Gather test inputs

From Phase 2 outputs and the coverage spec overview (SKILL.md), collect:

| Input | Source |
|---|---|
| `FRONTEND_URL` | `starter_pack_url` Terraform output from Phase 2 apply |
| `CORRINO_USERNAME` | `corrino_admin_username` from `terraform.tfvars` (if pack requires login) |
| `CORRINO_PASSWORD` | `corrino_admin_password` from `terraform.tfvars` (if pack requires login) |
| Pack-specific vars | Coverage spec "Environment Variables" section (e.g., `VSS_BUCKET_NAME`, `VSS_OBJECT_KEY`) — ask user for values |

### Step 15: Execute API tests

> **JUST-IN-TIME LOADING:** Read `.claude/skills/<category>-test-coverage/api-tests.md` NOW. This file is self-contained — it has every API test with endpoint, method, request body, verification criteria, priorities, timeouts, and curl commands. Execute directly from it.

For every test in `api-tests.md` that matches the chosen scope:

1. Read the endpoint, method, request body, and expected response from the file.
2. Execute via `curl` (responses saved to sandbox). The file includes ready-to-use curl commands for each test.
3. Compare HTTP status code and response body against the verification criteria.
4. Record result per test ID.
5. **Pass forward any outputs** needed by later tests (e.g., `fileId` from VA-4, `summaryId` from VA-9a).

Also execute any user-provided API tests (UT-* IDs).

**API Test Report:**

| ID | Endpoint | Expected | Actual Status | Pass? | Response Preview |
|---|---|---|---|---|---|
| (from spec) | (from spec) | (from spec) | (actual) | Y/N | first 200 chars |

### Step 16: Execute Infra tests (if selected)

> **JUST-IN-TIME LOADING:** Read `.claude/skills/<category>-test-coverage/infra-tests.md` NOW. This file is self-contained — it has every infrastructure test with kubectl/OCI CLI commands, expected output, and failure hints.

For every test in `infra-tests.md` that matches the chosen scope:

- Run `kubectl` or OCI CLI commands as specified.
- Record pass/fail per test ID.
- If a test fails, note the failure hint from the spec for the test report.

Also execute any user-provided infra tests (UT-* IDs).

### Step 17: Execute UI tests

UI tests use **standalone Playwright test specs** in `tests/e2e/<category>/` with Page Object Model, a shared browser context for single-video recording, and a banner overlay labeling each test step.

#### 17a. Run base coverage UI tests

Each pack has a pre-built Playwright spec file:

| Category | Spec file | Page objects |
|---|---|---|
| `vss` | `tests/e2e/vss/vss.spec.ts` | `tests/e2e/vss/pages/*.page.ts` |
| `paas_rag` | `tests/e2e/paas-rag/paas-rag.spec.ts` | `tests/e2e/paas-rag/pages/*.page.ts` |
| `cuopt` | `tests/e2e/cuopt/cuopt.spec.ts` | `tests/e2e/cuopt/pages/*.page.ts` |
| `enterprise_rag` | `tests/e2e/enterprise-rag/enterprise-rag.spec.ts` | `tests/e2e/enterprise-rag/pages/*.page.ts` |

If the spec file exists, run it:

```bash
cd tests/e2e
npm install  # ensure dependencies are present
BASE_URL="${STARTER_PACK_URL}" \
  VSS_BUCKET_NAME="${VSS_BUCKET_NAME}" \
  npx playwright test <category>/ --reporter=list
```

The spec produces a **single `.webm` video recording** in `tests/e2e/test-results/<category>-recording/`. All tests share one browser context with continuous video recording and a banner overlay showing which test is running.

**Key architecture of the spec files:**
- `test.describe.serial()` — tests run in order, sharing state
- `test.beforeAll()` — creates a shared `BrowserContext` with `recordVideo` and a shared `Page`
- `test.afterAll()` — closes context, finalizing the `.webm` video
- Banner overlay (`__ci__` div) labels each test step in the recording
- Smart navigation — `navigateTo()` skips `goto()` if already on the target page
- `scrollTo()` — scrolls elements into view for the recording

If the spec file does NOT exist for a category, fall back to reading `.claude/skills/<category>-test-coverage/ui-tests.md` and generating a temporary spec file following the same patterns as `tests/e2e/vss/vss.spec.ts`.

#### 17b. Handle user-provided UI tests

If the user provided UI tests in their test matrix (Step 12b):

1. **Clone the frontend repo** for the pack being tested to understand the exact selectors, component structure, and UI behavior. Frontend repos:
   - `vss` → clone the VSS Oracle UX repo (ask user for URL or check if it exists at `/tmp/<category>-frontend`)
   - Other packs → ask user for the frontend repo URL

2. **Read through the cloned frontend codebase** — focus on:
   - Component files for the pages/features the user wants tested
   - Selectors: `aria-label`, `role`, `data-testid`, element structure
   - Dialog types: does the component use `window.confirm()`, Radix dialog, or custom modals?
   - API calls: what endpoints do the UI actions trigger? (for `waitForResponse`)
   - State management: localStorage, cookies, database-backed state?

3. **Write a separate spec file** for user tests:
   ```
   tests/e2e/<category>/<category>-custom.spec.ts
   ```
   Follow the same patterns as the base spec:
   - Shared browser context with `recordVideo` → `test-results/<category>-custom-recording/`
   - Banner overlay, smart navigation, scroll-into-view
   - `test.describe.serial()` with `beforeAll`/`afterAll`
   - Page objects in `tests/e2e/<category>/pages/` (reuse existing ones where possible)

4. **Run the user test spec separately** — this produces a **second `.webm` video**:
   ```bash
   BASE_URL="${STARTER_PACK_URL}" \
     npx playwright test <category>/<category>-custom.spec.ts --reporter=list
   ```

**Two videos total:** Base spec recording + user test recording. This keeps them independent — a failure in user tests doesn't block the base spec recording and vice versa.

#### 17c. Collect UI test results

Parse the Playwright output to extract pass/fail counts:
- **Base spec:** count from `npx playwright test <category>/` output
- **User tests:** count from `npx playwright test <category>/<category>-custom.spec.ts` output
- Recordings: `tests/e2e/test-results/<category>-recording/*.webm` (base) and `tests/e2e/test-results/<category>-custom-recording/*.webm` (user)

### Step 18: Compile test report

Save the report to `${DAT_SANDBOX}/logs/test-report.txt` and display it:

```
═══════════════════════════════════════════════════
  TEST REPORT — <category> <size>
  Date:          <YYYY-MM-DD>
  Sandbox:       ${DAT_SANDBOX}
═══════════════════════════════════════════════════

  BASE SPEC (.claude/skills/<category>-test-coverage/):
    API Tests:     X/Y passed   (from api-tests.md)
    Infra Tests:   X/Y passed   (from infra-tests.md)
    UI Tests:      X/Y passed   (from ui-tests.md)

  USER-PROVIDED TESTS:
    API Tests:     X/Y passed   (UT-1, UT-3, ...)
    Infra Tests:   X/Y passed   (UT-2, ...)
    UI Tests:      X/Y passed   (UT-4, ...)

  COMBINED:  X/Y total passed

  FAILED:
  - <ID>: <description>
    Actual:   <what happened>
    Expected: <what should have happened>
    Proposed fix: <concrete diagnosis and suggested fix — e.g., "Pod vss-engine
      is in CrashLoopBackOff due to OOM; increase memory limit in
      blueprint_files.tf from 16Gi to 32Gi" or "Ingress returns 502; backend
      pod not ready — wait for NIM model loading to complete">

  API responses: ${DAT_SANDBOX}/api-results/
  UI recording (base):   tests/e2e/test-results/<category>-recording/*.webm
  UI recording (custom): tests/e2e/test-results/<category>-custom-recording/*.webm
  Full report:   ${DAT_SANDBOX}/logs/test-report.txt
═══════════════════════════════════════════════════
```

Omit the "USER-PROVIDED TESTS" section if the user did not provide a matrix. Omit "BASE SPEC" section if no base coverage file exists.

**For every failed test**, include a "Proposed fix" that:
1. Diagnoses the root cause based on the error, logs, pod status, or response body.
2. Suggests a concrete action (code change, config change, wait for readiness, retry, or escalate to user).
3. References the specific file, resource, or config that needs attention.

If any P0 test fails, flag it prominently. Do NOT auto-retry. Let the user decide whether to investigate before proceeding to Phase 4.

### Step 19: Copy artifacts to repo

Before destroy, copy test artifacts from the sandbox and test-results into the repo so they persist:

```bash
# Create artifacts directory in repo
mkdir -p .claude/test-artifacts

# Copy report
cp "${DAT_SANDBOX}/logs/test-report.txt" \
   ".claude/test-artifacts/<category>-<size>-test-report-<YYYY-MM-DD>.txt"

# Copy UI recordings from Playwright test-results
cp tests/e2e/test-results/<category>-recording/*.webm \
   ".claude/test-artifacts/<category>-<size>-base-recording.webm" 2>/dev/null || true
cp tests/e2e/test-results/<category>-custom-recording/*.webm \
   ".claude/test-artifacts/<category>-<size>-custom-recording.webm" 2>/dev/null || true

# Copy API results from sandbox
cp ${DAT_SANDBOX}/api-results/*.json \
   ".claude/test-artifacts/" 2>/dev/null || true
```

The `.claude/test-artifacts/` directory is gitignored — artifacts are for local review only, not committed.

---

## Phase 4: User Confirmation & Destroy

### Step 20: Prompt user

Show all test results. Ask if any additional manual verification is needed.

Tell the user: *"Test artifacts have been copied to `.claude/test-artifacts/`. The sandbox `${DAT_SANDBOX}/` will persist until you delete it."*

### Step 21: Destroy (on user confirmation)

Region is already set from Step 5b. Create destroy job:

```bash
oci resource-manager job create-destroy-job \
  --stack-id <stack-id> \
  --execution-plan-strategy AUTO_APPROVED
```

Poll until complete. Verify logs are clean.

---

## Error Handling

| Situation | Action |
|---|---|
| No qualifying regions | Report capacity unavailability, stop |
| Plan fails | Show logs, stop for user input |
| Apply fails | Show logs, stop for user input |
| Pods in CrashLoopBackOff | Check logs, report to user (wait and retry once) |
| Destroy fails on k8s provider | Update stack to Terraform 1.5.x and retry |
| UI tests FAIL | Report to user — user decides whether to investigate before destroy |
