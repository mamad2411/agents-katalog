# .cursorrules – Custom Rule File for Modular AI Agent System

<!-- @format -->

## 🧠 Current Project: Modular AI Agent System
**Goal**: Design a Pythonic, GPU-accelerated, local-first AI research agent framework

---

## 🔧 Development Workflow (Strict Sequence)
1. `masterplan.md`: Define system goals, stack, data model, deployment, agent capabilities
2. `stubout.md`: Create live frontend, backend dummy endpoints, stubbed files for core modules
3. `fullycode.md`: Production code for agents, orchestration, memory, integrations, and infra

**Important**: Frontend UI (Vite + React + Tailwind + shadcn/ui) must be running from stubout onwards.
Monitor for integration errors between frontend and FastAPI backend.

---

## ⚙️ Tools and Tech Stack

### Frontend
- Vite + React + TypeScript
- TailwindCSS + shadcn/ui
- Zustand (local state)
- React Query / SWR (data fetching)

### Backend
- Python 3.11+
- FastAPI (async endpoints)
- Pydantic v2
- Prefect (multi-agent orchestration)
- `llama.cpp` + Vulkan
- ChromaDB (primary)
- Optional: Weaviate, Pinecone
- uv (Python package manager)

### Deployment
- Docker (local)
- Terraform (cloud/G5 GPU EC2)
- Shared Dockerfile for local/cloud

---

## 📁 Project Structure
```bash
/ai-agent-framework
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── lib/
├── backend/
│   ├── agents/
│   ├── api/
│   ├── llm/
│   ├── memory/
│   ├── orchestration/
│   ├── integrations/
│   └── main.py
├── infra/
│   ├── Dockerfile
│   └── terraform/
```

---

## 🧩 Stub File Guidelines (Phase 2)
Each Python stub must include:
- Purpose comment
- Filepath comment
- Placeholder imports
- Empty class/function declarations
- `# TODO:` markers

Each frontend stub:
- React component shell (with component label)
- Route-page structure scaffolded
- Component folder organized by feature

---

## 📐 Best Practices
- Treat agents as modular tools
- Build generic interfaces for LLM, memory, tools
- Keep LLM inference abstracted from agent class
- Use Pydantic for all structured I/O
- Use shared memory namespace architecture with timestamp-based sync

---

## 📜 Project Rules
1. **Frontend must run first** and persist across all phases
2. Use **dummy API responses** until backend logic is ready
3. Keep backend modular and testable
4. Prioritize GPU-ready models and reasoning agents
5. Stick to three-phase process, no phase merging
6. Integrations (Slack, Notion, etc.) are abstracted modules
7. Store sync metadata in Chroma and periodically back up to S3
8. Agents may reason recursively and query others
9. Add timestamps + agent priority to resolve memory conflicts
10. Include **full absolute paths** in all file references, whether in operations, discussions, or questions about files
11. Use **uv** as Python package manager for faster dependency installation
12. **Check editor windows** for running servers before executing commands
13. **Monitor server logs** continuously for issues and correct them immediately when they occur

---

## 📒 Scratchpad
### Current Conversation State
- Phase 1: ✅ `masterplan.md` complete
- Phase 2: ✅ `stubout.md` basic implementation complete
  - Frontend and backend stubs implemented and working
  - API integration successful
- Phase 3: ⏳ Preparing for `fullycode.md`
- Next focus: Core module stubs implementation

### Server Status
- Backend: Running on http://localhost:8000
  - Health endpoint: /health
  - API prefix: /api
  - Start with: `cd backend && source .venv/Scripts/activate && python -m uvicorn main:app --reload --port 8000`
  - Status: ✅ Running and receiving API requests
- Frontend: Running on http://localhost:5173 
  - Start with: `cd frontend && npm run dev`
  - Status: ✅ Running successfully, displaying agent list from API
- For both servers: Use improved `./run-dev.sh` script
- Watch console output for warnings/errors and address immediately

---

## 📚 Lessons
- Always scaffold the frontend and verify it's bootstrapped before backend logic
- Use minimal dummy responses to test backend APIs
- Prefer smaller quantized models (`gemma-3-4b-it`) to fit 12GB GPU budget
- Setup Chroma with local collections first; add Pinecone/Weaviate layer later
- Cloud fallback must use a single Dockerfile with Vulcan-ready base image
- Use uv for Python package management (faster than pip)
- Create virtual environments with `uv venv` before installing packages
- Add proper activation commands in scripts (`source .venv/Scripts/activate` on Windows)
- Check if servers are already running before starting new ones
- Troubleshoot npm dependency issues by clearing node_modules and package-lock.json
- Docker builds for LLM compilation need optimized parameters and stable release tags
- Use `-j$(nproc)` for parallel compilation in Docker builds to speed up the process

---

## ✅ TODO
[X] Create masterplan.md
[X] Create stubout.md with frontend priority
[X] Create fullycode.md structure
[X] Set up backend environment with uv
[X] Get backend server running correctly
[X] Fix frontend Rollup dependency issues
[X] Get frontend server running correctly
[X] Generate working frontend stub (Vite + React + Tailwind)
[X] Wire dummy backend endpoints
[ ] Implement stubs for core modules: agent, memory, llm, orchestration, integrations
[ ] Add robust error handling to frontend API calls
[ ] Implement proper API response validation
[ ] Complete the testing infrastructure
