---
name: swarm
description: "Autonomous Multi-Brain 10-Agent Swarm: Orchestrates connected AI providers (9Router, Groq, Gemini, DeepSeek, Claude, OpenAI, Ollama) to debate, generate contract-first specifications, and build software collaboratively."
allowed-tools: run_command read_file write_file edit_file
---
# TenAgent Multi-Brain Swarm Orchestrator (v1.0.1)

This skill defines the autonomous multi-brain collaborative execution protocol for the TenAgent Engineering Swarm.

## When to Activate
Activate this skill whenever the user instructs the assistant to build, scaffold, develop, or implement a project, system, module, or major feature.

## Core Directives

1. **Never Monolithic Generation**:
   The primary AI CLI assistant acts as the Swarm Conductor. Do not generate entire applications from a single uncoordinated prompt context.

2. **Trigger the Multi-Brain Pipeline**:
   The very first action must be running the collaborative swarm pipeline:
   ```powershell
   python swarm_pipeline.py "<user_prompt>"
   ```
   *(or `python stream.py swarm "<user_prompt>"`)*

   **Execution flow handled by the pipeline**:
   - Discovers all active AI keys configured in `specs/swarm-config.json` (9Router at `localhost:20128`, Groq, Gemini, DeepSeek, Claude, OpenAI, Ollama).
   - If 2+ AI models are connected: initiates an adversarial pre-flight debate (`council.py`) to stress-test race conditions, security, and scalability.
   - Maps the 10 engineering roles to the active brains.
   - Writes contract-first deliverables:
     * `specs/prd/user-stories.md`
     * `specs/architecture/adr-001.md`
     * `specs/database/schema.sql`
     * `specs/api/openapi.yaml`
     * `specs/qa/test-matrix.md`
     * `specs/security/audit-report.md`
     * `specs/signoff.md`
   - Streams real-time thoughts to `specs/terminal.log` and updates `specs/swarm-status.json`.

3. **Downstream Implementation & Test Verification**:
   - Inspect the generated contracts in `specs/`.
   - Complete the implementation files in `backend/` and `frontend/` (or `mobile/`).
   - Run tests and builds through the stream runner:
     ```powershell
     python stream.py run 07_qa "npm test" # or pytest / cargo test
     ```
