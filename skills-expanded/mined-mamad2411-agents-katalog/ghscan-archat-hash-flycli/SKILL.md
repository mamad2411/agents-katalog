# 🧩 AGENT MASTER PROTOCOL (ORCHESTRATOR)

## ⚖️ HIERARCHY OF TRUTH (PRIORITY)
In case of conflict, the following order of priority MUST be observed:
1. **🎯 OKR** (Strategy) - The ultimate goal.
2. **📊 BUSINESS SCENARIOS/EPICS** (Analyst) - Functional requirements.
3. **🏛️ ARCHITECTURE/INTERFACES** (Architect) - Technical contracts.
4. **🛠️ CODE** (Developer) - Implementation.

## 🔄 MODE SELECTOR (MANDATORY START)
At the start of every task, analyze the request/state and declare the active role:

1.  **🧠 DATA ENGINE MODE**: For ingesting resumes, atomizing experience, and semantic matching.
    *👉 Module: [.agents/DATA_ENGINE.md]*
2.  **🎯 STRATEGIST MODE**: For OKR alignment, market positioning, and prioritization.
    *👉 Module: [.agents/STRATEGIST.md]*
3.  **📊 ANALYST MODE**: For requirement gathering and User Story definition.
    *👉 Module: [.agents/ANALYST.md]*
4.  **🏛️ ARCHITECT MODE**: For system design (CLI + DB + Playwright) and ADRs.
    *👉 Module: [.agents/ARCHITECT.md]*
5.  **🛠️ DEVELOPER MODE**: For TDD/BDD implementation and DB schema management.
    *👉 Module: [.agents/DEVELOPER.md]*
6.  **🧪 QA MODE**: For testing browser automation and data integrity.
    *👉 Module: [.agents/QA.md]*
7.  **🚀 DEVOPS MODE**: For local infrastructure and CI/CD pipelines.
    *👉 Module: [.agents/DEVOPS.md]*
8.  **TUNER MODE**: For flight performance analysis, PID tuning, and filter optimization.
    *Module: [.agents/TUNER.md]*

---

## 🚦 ARTIFACT-DRIVEN WORKFLOW
Agents must NOT "think together". They transfer artifacts:
*   **Raw CV** ➔ **Data Engine** ➔ **Experience Atoms (DB)**.
*   **Job URL** ➔ **Data Engine** ➔ **Match Report & Tailored Draft**.
*   **Strategist** ➔ **Analyst**: Vision & High-level Goals (OKRs).
*   **Analyst** ➔ **Architect**: Requirements Doc / User Stories.
*   **Architect** ➔ **Developer**: ADR / DB Schema / API Contracts.

---

## 🚨 ESCALATION PROTOCOL
If an Agent identifies a blocker or missing data, escalate back to the source role immediately.

---

## 📦 VERSIONING POLICY (SEMANTIC VERSIONING — MANDATORY)

Version format: **`MAJOR.MINOR.PATCH`** (e.g. `1.2.3`)

| Change type | What qualifies | Version bump | Example |
|---|---|---|---|
| 🔧 **Fix / Patch** | Bug fix, typo, CI config, refactor with no new behaviour | `+0.0.1` | `1.0.0` → `1.0.1` |
| ✨ **Feature** | New command, new option, new output format, new behaviour | `+0.1.0` | `1.0.1` → `1.1.0` |
| 🎨 **Redesign** | Breaking change, architecture overhaul, new public API contract | `+1.0.0` | `1.1.0` → `2.0.0` |

### Rules
1. **ALWAYS** update `version` in `package.json` before releasing.
2. **NEVER** reuse or skip a version number.
3. After a **MINOR** bump → reset PATCH to `0`. After a **MAJOR** bump → reset MINOR and PATCH to `0`.
4. Create a Git tag matching the version: `git tag v1.2.3 && git push origin v1.2.3`.
5. The Git tag triggers the GitHub Actions release workflow automatically.

---

## 🛑 CRITICAL RULES (NON-NEGOTIABLE)
1. **NO LOGIC SIMULATION**: Never use scratch scripts or manual data manipulation to bypass service logic. If a service is missing a feature, implement it in the service code.
2. **CODE OVER SCRIPTS**: Business logic MUST reside in the `src/` directory. Scratch scripts are ONLY for one-off DB maintenance or low-level debugging.
3. **ARCHITECTURE FIRST**: Every new logic block must be traced back to an Interface or ADR.

## 🛠️ GLOBAL SHARED DIRECTIVES
*   **Context First**: Always check `application_history` in the DB before starting a search.
*   **Privacy First**: No PII should ever leave the local machine without explicit "Human-in-the-Loop" approval.
