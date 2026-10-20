# Coding Agent Guide

## 📂 Project Structure

This project is structured as a decentralized, multi-agent mesh:
* **`almp-orchestrator/`**: The Root Orchestrator which routes state, coordinates waves, and manages Human-in-the-Loop gates.
* **`almp-discover/`**, **`almp-assess/`**, **`almp-plan/`**, **`almp-characterization/`**, **`almp-transform/`**, **`almp-verify/`**, **`almp-cutover/`**, **`almp-capture/`**: The 8 individual phase agents.
* **`app/` / `skills/`**: Inside each agent folder, `app/` contains ADK logic and `skills/` contains declarative migration rulebooks and accompanying deterministic Python tools.
* **`run_local_eval.py`**: The unified test harness to execute and validate the setup/logic of all 8 agents locally.
* **`run_all_playgrounds.py`**: The script that boots all 8 agents locally on background ports (`8001-8008`) and launches the Root Orchestrator in an interactive, web-based playground interface.
* **`docs/`**: Holds architecture guides, cloud-deployment guidelines, and IAM security matrices.

---

## 🛠️ ADK & Agent Skills

This platform is powered by the **Google Agent Development Kit (ADK)**. Follow these strict patterns when writing agent logic:
1. Use adk and google agent skills for building and updating agents.

---

## 🚀 Prerequisites & Local Setup

Install the CLI (one-time):
```bash
uv tool install google-agents-cli
```

Configure local environment and authenticate with Google Cloud:
```bash
# Sync all workspace packages and instantiate the local virtual environment (.venv)
uv sync

# Authenticate for local GenAI Vertex model inference
gcloud auth login
gcloud auth application-default login
```

---

## 📐 Development Phases

### Phase 1: Understand Requirements
Before writing any code, understand the project's requirements, constraints, and success criteria. Review existing documentation inside `docs/` and `README.md`.

### Phase 2: Build and Implement
Use `agents-cli playground` or the local multi-agent stack `uv run run_all_playgrounds.py` for interactive testing. Iterate based on user feedback.

### Phase 3: The Evaluation Loop (Main Iteration Phase)
To validate changes across the multi-agent mesh, run the local evaluation suite: `run_all_playgrounds.py`

For single-agent iterations, use `agents-cli eval generate` followed by `agents-cli eval grade` in the agent's folder. Expect 5-10+ iterations. Once you have a baseline, reach for `agents-cli eval compare` (regression diffs), `agents-cli eval analyze` (cluster failure modes).

### Phase 4: Pre-Deployment Tests
Run `uv run pytest tests/unit tests/integration`. Fix issues until all tests pass. Verify if the deployment already exists in gemini enterprise agent platform and call it out.

### Phase 5: Deploy
**Requires explicit human approval.** Run `run_all_playgrounds_geap.py` only after user confirms. Refer to @README.md for additional details.  Do not run @deployment/ terraform for infra provisioning as it is just for reference.

---

## 🛠️ Development Commands

| Command | Purpose |
|---------|---------|
| `uv run run_all_playgrounds.py` | Boot all 8 phase agents locally and open interactive Orchestrator UI |
| `agents-cli playground` | Standalone local testing for a single phase agent |
| `uv run run_local_eval.py` | Run local evaluation suite to validate all 8 agents |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests |
| `agents-cli eval dataset synthesize` | Synthesize multi-turn eval scenarios for your agent |
| `agents-cli eval generate` | Run agent on eval dataset, produce traces |
| `agents-cli eval grade` | Run agent evaluations on the traces |
| `agents-cli eval compare` | Compare two grade-results files (regression check) |
| `agents-cli eval analyze` | Cluster failure modes from grade results |
| `agents-cli eval metric list` | List built-in metrics available in the SDK |
| `agents-cli eval optimize` | Auto-tune agent prompts using eval data |
| `agents-cli lint` | Check code quality |
| `agents-cli infra single-project` | Set up project infrastructure (Terraform) |
| `agents-cli deploy` | Deploy to dev |
| `agents-cli scaffold enhance` | Add deployment target or CI/CD to project |
| `agents-cli scaffold upgrade` | Upgrade project to latest version |

---

## 🛡️ Operational Guidelines for Coding Agents

- **Code preservation**: Only modify code directly targeted by the user's request. Preserve all surrounding code, config values (e.g., `model`), comments, and formatting.
- Always share the plan/artifact and get it approved before implementation.
- **NEVER change the model** unless explicitly asked.
- **Model 404 errors**: Fix `GOOGLE_CLOUD_LOCATION` (e.g., `global` instead of `us-east1`), not the model name.
- **ADK tool imports**: Import the tool instance, not the module: `from google.adk.tools.load_web_page import load_web_page`
- **Run Python with `uv`**: `uv run python script.py`. Run `agents-cli install` first.
- **Check Existing Deployments**: Always query existing deployments (e.g. check `deployment_metadata.json` files or run `agents-cli deploy --status`) before attempting to deploy or redeploy the stack. Do not recreate resources if they already exist unless specifically requested.
- **Dependency Versions**: Never update, alter, or override any package dependency versions in `pyproject.toml`, `requirements.txt`, or other package manifests unless specified and explicitly requested/approved by the user.
- **Stop on repeated errors**: If the same error appears 3+ times, fix the root cause instead of retrying.

- **Terraform conflicts** (Error 409): Use `terraform import` instead of retrying creation.
