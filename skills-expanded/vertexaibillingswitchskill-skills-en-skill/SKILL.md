---
name: en
description: Set up Gemini CLI's Vertex AI authentication mode, including gcloud installation, GCP auth, project setup, API enablement, ADC login, and billing auto-switch Hook deployment. Trigger when user mentions Vertex AI, ADC, Application Default Credentials, GCP project setup, or billing quota. After loading, immediately begin the interactive workflow from Step 0.
version: 1.4.1
---

## Your Role

You are an interactive setup wizard. Your task is to guide the user through the Vertex AI setup by following the workflow below, step by step.

**Core behavior rules:**
- Strictly follow the order: Step 0 → Step 1 → ... → Step 6
- You MUST ALWAYS AND ONLY use the `read_file` and `write_file` tools when handling `.env` or `settings.json` files (Explanation: Using `run_shell_command` like `echo` or `>` causes UTF-16 encoding corruption on Windows. To guarantee consistent behavior, using shell commands for writing is strictly forbidden across ALL operating systems: Mac, Linux, and Windows)
- Every step marked `ask_user` requires calling the `ask_user` tool and waiting for a response
- You must execute all steps sequentially and wait for each response
- Only use `run_shell_command` when a step explicitly instructs you to
- If a step fails, follow that step's "Failure handling" instructions

## IMPORTANT — Execute Immediately After Loading

**You must immediately perform the following action. No preamble is needed:**

1. **DO NOT** output any explanatory text
2. **DO NOT** ask "shall we begin" or wait for confirmation
3. **DIRECTLY** call `ask_user` to execute Step 0 (Disclaimer Confirmation)

This is a mandatory instruction. Skipping this step is an execution failure.

# Vertex AI Billing Switch

Automatically set up Gemini CLI's Vertex AI authentication mode and deploy a global billing auto-switch Hook.

## Usage

```
/en run the skill workflow
```

No other arguments accepted. The Project ID will be collected interactively during execution.

---

## Mandatory Interaction Rules

All steps marked with `ask_user` are **mandatory blocking points**:

- **DO NOT** assume answers
- **DO NOT** skip or omit questions
- **MUST** call `ask_user` and wait for the user's response before proceeding

Violating these rules is considered an execution failure. The entire process must restart from the beginning.

---

## Workflow

```text
Step 0: Disclaimer confirmation (ask_user, always interactive)
  ↓ ("Let me reconsider" → abort)
Step 1: Environment detection (silent checks)
  ├─ All ready (returning user)
  │   → ask_user: Switch project / Full reset
  │   → Full reset: → Step 2 onward (full flow)
  │   → Rename billing accounts: → Step R → Done
  │   → Switch: ask_user(Same account / Switch account)
  │       → Same account: Step 4(project) → Step 5(config, skip Hook deploy) → Step 6(verify)
  │       → Switch account: Step 3(auth) → Step 4(project) → Step 5(config, skip Hook deploy) → Step 6(verify)
  ├─ gcloud ready, Hook not deployed (check1 ✓ + check2 ✓ + check3 ✗)
  │   → ask_user: Deploy Hook only / Full setup
  │   → Deploy Hook only: → Step H → Step 6 (hook_only mode)
  │   → Full setup: → Step 2 onward (full flow)
  └─ gcloud not installed or not authenticated (first-time user)
      → Step 2: gcloud CLI installation
      → Step 3: GCP auth login
      → Step 4: Get/Create GCP project
      → Step 5: GCP config + Gemini CLI deployment
      → Step 6: Verify + completion summary
```

### Route Summary

| User Type | Steps |
|-----------|-------|
| First-time user | 0 → 1 → 2 → 3 → 4 → 5 → 6 |
| Returning user — Full reset | 0 → 1 → 2 → 3 → 4 → 5 → 6 |
| Returning user — Same account, switch project | 0 → 1 → 4 → 5 (skip Hook deploy) → 6 |
| Returning user — Switch account | 0 → 1 → 3 → 4 → 5 (skip Hook deploy) → 6 |
| Returning user — Rename billing accounts | 0 → 1 → R → Done |
| Returning user — Hook only (Vertex AI already configured) | 0 → 1 → H → 6 |

---

## Step 0: Disclaimer Confirmation

> **STOP — Mandatory interaction point**
> This is the first step after the skill is triggered. It always fires and cannot be skipped.

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"Please confirm that the Google Cloud account you will log in to later does not have any credit cards or other payment methods attached. We are not responsible for any charges incurred if a payment method is attached.","header":"Disclaimer","type":"choice","options":[{"label":"I understand","description":"I confirm no payment method is attached. Continue."},{"label":"Let me reconsider","description":"I need to verify first. Abort for now."}]}]}
```

### Handling logic

**"I understand"** → Proceed to Step 1

**"Let me reconsider"** → Display the following message and immediately abort:

> Aborted. Please confirm your Google Cloud account has no payment method attached, then run `/en run the skill workflow` again.

---

## Step 1: Environment Detection

This step runs silently — no user interaction unless all checks pass.

### Checks

Use `run_shell_command` to perform the following checks sequentially:

**1. Check if gcloud is installed:**

```bash
gcloud --version
```

**2. Check if gcloud is authenticated (only if check 1 passed):**

```bash
gcloud auth list --filter=status:ACTIVE --format="value(account)"
```

**3. Check if Hook is deployed (only if checks 1 and 2 passed):**

First, get the home directory:

```bash
node -e "process.stdout.write(require('os').homedir())"
```

Then check for the Hook file:

```bash
test -f {home_dir}/.gemini/hooks/vertex-ai-billing-switch-hook.mjs && echo "OK" || echo "MISSING"
```

### Decision logic

**All three checks pass (returning user)** →

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"Detected that the environment is already set up. What would you like to do?","header":"Mode","type":"choice","options":[{"label":"Switch project/account","description":"Change GCP project or Google account (skip installation steps)"},{"label":"Rename billing accounts","description":"Rename billing accounts for easier identification (e.g., Trial_Exp_20260501)"},{"label":"Full reset","description":"Run the complete setup flow from scratch"}]}]}
```

- **"Full reset"** → Continue to **Step 2** (full flow)
- **"Rename billing accounts"** → Proceed to **Step R**
- **"Switch project/account"** → Set `quick_switch = true`, then:

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"Are you switching to a different Google account, or just changing the GCP project under the same account?","header":"Account Switch","type":"choice","options":[{"label":"Same account","description":"Keep current Google login, only change the GCP project"},{"label":"Switch account","description":"Log in to a different Google account (browser will open)"}]}]}
```

  - **"Same account"** → Skip to **Step 4** (no re-authentication needed)
  - **"Switch account"** → Proceed to **Step 3**

**Checks 1 and 2 pass, check 3 fails (gcloud ready, Hook not deployed)** →

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"gcloud is installed and authenticated, but the billing switch Hook is not deployed. What would you like to do?","header":"Mode","type":"choice","options":[{"label":"Deploy Hook only","description":"Use existing Vertex AI configuration and deploy only the billing switch Hook"},{"label":"Full setup","description":"Run the complete setup flow from scratch"}]}]}
```

- **"Deploy Hook only"** → Set `hook_only = true`, proceed to **Step H**
- **"Full setup"** → Continue to **Step 2** (full flow)

**Checks 1 or 2 fail (first-time user)** → Continue to **Step 2**

---

## Step H: Deploy Hook Only

> Entry point from Step 1 when `hook_only = true`.
> The user already has Vertex AI configured and only needs the billing switch Hook deployed.

### H-1: Setup Variables

Use `run_shell_command` to get the home directory:

```bash
node -e "process.stdout.write(require('os').homedir())"
```

Store as `{home_dir}` and set:
- `{gcloud_cmd}` = `gcloud` (already verified in Step 1)
- `{skill_dir}` based on installation method:
  - Installed via Gemini CLI: `{home_dir}/.gemini/extensions/VertexAiBillingSwitchSkill/skills/en`
  - Manually installed: `{home_dir}/.gemini/skills/en`

Use `run_shell_command` to read the current GCP project (for display and options only):

```bash
gcloud config get-value project
```

Store as `{detected_project}` (if empty or `(unset)`, label as "not set").

---

### H-2: Choose GCP Project

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

> If `{detected_project}` is "not set", inform the user before calling ask_user: "gcloud does not have a default project set. Consider choosing 'Specify another project' or 'Create new project'."

Use `ask_user`:

```json
{"questions":[{"question":"The billing switch Hook needs to know which GCP project to monitor. Which project would you like to use?","header":"GCP Project","type":"choice","options":[{"label":"Use current project","description":"Use gcloud's current default project: {detected_project}"},{"label":"Specify another project","description":"Enter an existing GCP project ID"},{"label":"Create new project","description":"Let the Skill automatically create a new GCP project"}]}]}
```

#### "Use current project"

Set `{project_id}` = `{detected_project}`, proceed directly to **H-4 (Confirm deployment)**.

#### "Specify another project"

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"Enter your GCP Project ID (usually starts with gen-lang-client-):","header":"Project ID","type":"text","placeholder":"gen-lang-client-0123456789"}]}
```

Validate: if empty or clearly invalid, ask again. Store as `{project_id}`, proceed to **H-3 (Apply new project settings)**.

#### "Create new project"

**Read `references/create-project.md` and execute the full auto-create sub-flow (4-A detect billing accounts, 4-B enter project name, 4-C create, 4-D link billing, 4-E confirm).**

After obtaining `{project_id}`, proceed to **H-3 (Apply new project settings)**.

---

### H-3: Apply New Project Settings (only for "Specify another project" or "Create new project")

Inform the user:

> Switching GCP project to `{project_id}`…

Execute sequentially using `run_shell_command`:

**Update gcloud default project:**
```bash
gcloud config set project {project_id}
```

**Enable Vertex AI API:**
```bash
gcloud services enable aiplatform.googleapis.com --project={project_id}
```

**Update `~/.gemini/.env`:**

1. Use `read_file` to read `{home_dir}/.gemini/.env` (start with empty content if file doesn't exist)
2. Remove existing `GOOGLE_CLOUD_PROJECT=` and `GOOGLE_CLOUD_LOCATION=` lines
3. Append:
   ```
   GOOGLE_CLOUD_PROJECT={project_id}
   GOOGLE_CLOUD_LOCATION=global
   ```
4. Use `write_file` to write back

Proceed to **H-4 (Confirm deployment)**.

---

### H-4: Confirm Deployment

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"About to perform the following actions: 1. Copy billing switch Hook to ~/.gemini/hooks/. 2. Update settings.json and enable Hook. 3. Set authentication mode to Vertex AI. Monitoring project: {project_id}","header":"Confirm Deploy","type":"yesno"}]}
```

- **Yes** → Proceed to H-5
- **No** → Display "Cancelled. To retry, trigger this Skill again." and abort

---

### H-5: Deploy Hook

**Read `references/deploy-hook.md` and execute all deployment steps (directory creation, Hook script copy, settings.json non-destructive merge).**

> Note: Ignore the precondition at the top of that file stating "execute only when `quick_switch = false`". In the `hook_only = true` route, execute all steps directly.

Proceed to **Step 6** (`hook_only = true`).

---

## Step R: Rename Billing Accounts

> Entry point from Step 1 when "Rename billing accounts" is selected.
> This is a standalone flow that does not affect other steps.

**Read `references/rename-accounts.md` and execute the full rename workflow (R-1 list accounts, R-2 choose strategy, R-3 collect dates, R-4 confirm, R-5 execute renames).**

After completion or cancellation, the flow ends. Display:

> To continue with other operations, run the skill again.

---

## Step 2: Environment Check

### Setup variables

Use `run_shell_command` to get the home directory:

```bash
node -e "process.stdout.write(require('os').homedir())"
```

Store as `{home_dir}`. Derive: `{skill_dir}` = `{home_dir}/.gemini/skills/en`

Also set the default: `{gcloud_cmd}` = `gcloud` (if Windows installation leaves PATH not updated, this will be overwritten with the full path at the end of Step 2)

### Check gcloud CLI

> **Optimization:** If Step 1 already determined that gcloud is not installed (check 1 failed), skip this command and go directly to the conditional interaction point below.

Use `run_shell_command`:

```bash
gcloud --version
```

### Decision logic

- **Command succeeds** (gcloud installed) → Proceed to Step 3
- **Command fails** (gcloud not installed) → Trigger interaction point

### Conditional interaction point (only when gcloud is not installed)

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"Google Cloud CLI (gcloud) is not installed. It's required to connect to Vertex AI. How would you like to proceed?","header":"gcloud Setup","type":"choice","options":[{"label":"Auto install","description":"Automatically download and install gcloud CLI (~2-3 min)"},{"label":"I'll install it","description":"Go to the official site to install manually"}]}]}
```

### Handling logic

**"I'll install it"** → Display the following message and end the flow:

> Please visit https://cloud.google.com/sdk/docs/install to install Google Cloud CLI.
> Once installed, run `/en run the skill workflow` again.

**"Auto install"** → First detect the operating system platform:

Use `run_shell_command`:

```bash
node -e "process.stdout.write(process.platform)"
```

Branch based on the platform result:

---

#### If `win32` (Windows)

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"There are two ways to install gcloud CLI on Windows. Which one would you like?","header":"Install method","type":"choice","options":[{"label":"winget install","description":"Run winget install -e --id Google.CloudSDK"},{"label":"Google official","description":"Run PowerShell to download the official installer"}]}]}
```

**Read `references/install-gcloud.md` § Windows for detailed installation and verification commands after the user's choice.**

---

#### If `darwin` (macOS)

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"There are two ways to install gcloud CLI on macOS. Which one would you like?","header":"Install method","type":"choice","options":[{"label":"Homebrew install","description":"Run brew install --cask gcloud-cli"},{"label":"Google official","description":"Run curl https://sdk.cloud.google.com | bash"}]}]}
```

**Read `references/install-gcloud.md` § macOS for detailed installation and verification commands after the user's choice.**

---

#### If other platform (Linux)

**Read `references/install-gcloud.md` § Linux for installation and verification commands.**

---

## Step 3: GCP Auth Login

Both first-time users and returning users (switching accounts) must execute this step.

### Actions

First, inform the user:

> Next, a browser window will open for Google Cloud account login. Please complete the login in the browser.

Then use `run_shell_command`:

If `{gcloud_cmd}` = `gcloud` (PATH is available):
```bash
gcloud auth login
```

If `{gcloud_cmd}` is a full path (Windows installation with PATH not yet updated):
```bash
powershell -Command "& '{gcloud_cmd}' auth login"
```

- **Only** execute `gcloud auth login`
- Do **NOT** run `set project`, enable APIs, or set up ADC (the project ID is not yet known)

### Failure handling

- **Login fails — browser did not open**: If no browser window appeared, retry with `--no-launch-browser`:

  If `{gcloud_cmd}` = `gcloud`:
  ```bash
  gcloud auth login --no-launch-browser
  ```
  If `{gcloud_cmd}` is a full path:
  ```bash
  powershell -Command "& '{gcloud_cmd}' auth login --no-launch-browser"
  ```
  gcloud will print a URL in the terminal. Ask the user to open it in any browser, complete sign-in, then paste the verification code back into the terminal.

- **Login fails — other reason**: User may have cancelled the browser login. Suggest re-running the skill.

---

## Step 4: Get/Create GCP Project

> **STOP — Mandatory interaction point**
> This is a required step. It always fires and cannot be skipped.
> The Project ID must be collected via `ask_user`. Parameter passing is not supported.

### Round 1: Check if user has a project

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"Do you already have a Google AI Studio GCP project?","header":"GCP Project","type":"yesno"}]}
```

### Handling logic

**Answer "Yes"** → Proceed to Round 2

**Answer "No"** → Proceed to Round 2-alt

### Round 2: Enter Project ID

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"Enter your GCP Project ID (projects created via AI Studio usually start with gen-lang-client-) ⚠️ Disclaimer: Please make sure none of the billing accounts under this GCP account have a credit card attached. We are not responsible for any charges incurred.","header":"Project ID","type":"text","placeholder":"gen-lang-client-0123456789"}]}
```

### Validation

- Check if the input is empty
- If empty or clearly invalid, ask again
- Store `{project_id}` for subsequent steps
- Proceed to **Step 5**

### Round 2-alt: Choose creation method

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"How would you like to create a GCP project?","header":"Create method","type":"choice","options":[{"label":"Auto-create (gcloud)","description":"Automatically create a new GCP project via gcloud CLI without leaving the terminal"},{"label":"Manual (AI Studio)","description":"Go to Google AI Studio website to create manually, then come back"}]}]}
```

#### "Manual (AI Studio)" → Display the following setup guide, then end the flow:

> **How to create a GCP project:**
>
> 1. Go to [Google AI Studio](https://aistudio.google.com) and sign in with your Google account
> 2. Click **Get API Key** in the bottom-left corner
> 3. On the API Keys page, click **Create API key** in the top-right corner and follow the prompts to create a key
> 4. On the API Keys page, find the **Project** field and copy the GCP Project ID that starts with `gen-lang-client-`
> 5. On the API Keys page, find the **Billing Tier** field and set up an active **$5** credit plan
> 6. Once done, run `/en run the skill workflow` again

#### "Auto-create (gcloud)" → Execute the following sub-flow:

**4-A: Detect available billing accounts**

Use `run_shell_command`:

If `{gcloud_cmd}` = `gcloud`:
```bash
gcloud billing accounts list --format="json"
```

If `{gcloud_cmd}` is a full path:
```bash
powershell -Command "& '{gcloud_cmd}' billing accounts list --format=json"
```

Filter accounts where `open === true`.

- **No available accounts** → Display the following message and end the flow:

  > No available billing accounts detected. Please go to [Google AI Studio](https://aistudio.google.com) to set up the **$5** credit plan first, then run `/en run the skill workflow` again.

- **One available account** → Record the account, continue to 4-B

- **Multiple available accounts** →

  **STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

  Use `ask_user` to let the user choose (dynamically generate choice options, use up to 4 accounts):

  ```json
{"questions":[{"question":"Multiple billing accounts detected. Which one would you like to link to the new project?","header":"Billing","type":"choice","options":[{"label":"{displayName1}","description":"Account ID: {accountId1}"},{"label":"{displayName2}","description":"Account ID: {accountId2}"}]}]}
```

**4-B: Enter project ID base name**

**STOP — You MUST call ask_user. DO NOT assume the answer. Wait for the response before continuing.**

Use `ask_user`:

```json
{"questions":[{"question":"Enter your preferred GCP Project ID (lowercase letters, digits, hyphens only, 6-30 chars). A random suffix will be added to ensure uniqueness. Leave empty to use the default 'gemini-vertex'.","header":"Project ID","type":"text","placeholder":"gemini-vertex"}]}
```

**Read `references/create-project.md` for project ID generation logic, project creation (4-C), billing account linking (4-D), and confirmation (4-E).**

Store `{project_id}` for subsequent steps. Proceed to **Step 5**.

---

## Step 5: Failure Handling Warning (ADC Login)

In the upcoming Step 5, you will read `references/config-and-verify.md` to perform ADC login.
If you encounter **ADC login fails — browser did not open**, you MUST EXCLUSIVELY use the `ask_user` tool to guide the user to run the command manually.

**STOP — You MUST call ask_user. Wait for the response before continuing.**
Use `ask_user`:

```json
{"questions":[{"question":"The browser failed to open. To avoid URL formatting issues with the `|` prefix, please open a **NEW terminal window/tab** (leave Gemini CLI running) and manually run this command:\n\n{cmd_string}\n\nAfter successfully logging in, click confirm below to continue.","header":"Manual ADC Login","type":"choice","options":[{"label":"I have completed the login","description":"Proceed to the next step"}]}]}
```
*Hint: `{cmd_string}` is `gcloud auth application-default login --no-launch-browser --project={project_id}` (add `& "..."` if using a full path).*

---

## Step 5 & Step 6: Deploy & Verify

**Please read `references/config-and-verify.md` and execute the configuration and verification instructions sequentially.**
