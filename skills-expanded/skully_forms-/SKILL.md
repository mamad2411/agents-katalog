# 🤖 Cursor AI Codebase Rulebook

Welcome to the tRPC Monorepo! To optimize performance, preserve your token context window, and guarantee pristine output, you MUST follow our **Self-Routing Context Protocol**.

---

## 🛑 CRITICAL DIRECTIVE: STRICT LAZY-LOADING CONTEXT BOUNDARIES

Do NOT scan all directories or read all context files. You must lazy-load documentation strictly as follows:

1. **SINGLE ENTRYPOINT READ**: At the beginning of a session or task, read ONLY `/docs/llm-wiki/README.md` or `/docs/llm-wiki/ai-agent-guidelines.md` to identify active context tags for your task.
2. **STRICT ISOLATION**: Do NOT open files in other directories.
   - If task matches `#db` (Drizzle, migrations, schemas) -> open ONLY files under `docs/llm-wiki/database/`.
   - If task matches `#api` (tRPC routers, endpoints) -> open ONLY files under `docs/llm-wiki/api-trpc/`.
   - If task matches `#ui` (styling, Next.js page layouts, Tailwind v4) -> open ONLY files under `docs/llm-wiki/frontend-design/`.
   - If task matches `#workflow` (build scripts, dev startup) -> open ONLY files under `docs/llm-wiki/workflows/`.
3. **NO BULK SCANS**: Do NOT execute recursive directory sweeps or full-repo grepping. Ingest files on-demand, one-by-one, at the exact sub-step they are needed.

---

## ✍️ MANDATORY: AGENT CONTEXT SYNC (LAST ACTION)

Before concluding your execution or declaring a task complete, you MUST append a new thought ledger file under `/docs/llm-wiki/thoughts/` named in format `YYYY-MM-DD-[agent]-[topic].md`.

This file must record:
1. **Scope/Context**: What was built or refactored.
2. **Design Rationale & Trade-offs**: Why decisions were made.
3. **Blockers & Workarounds**: Pitfalls you solved.
4. **Active State & Handover**: What the next agent needs to do immediately.

Always ensure the latest database changes sync to `/docs/llm-wiki/database/contracts/` and API changes sync to `/docs/llm-wiki/api-trpc/endpoint-contracts.md`.
