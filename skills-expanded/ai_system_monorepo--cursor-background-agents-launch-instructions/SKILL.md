# Launch Instructions for Cursor Background Agents

Follow these steps. You can copy/paste prompt files into each agent.

## 1) Prepare Branches
1. Ensure you are in the repo root.
2. Run:
   - bash background-agents/scripts/prepare_integration_branch.sh
   - Optionally push: git push -u origin integration

## 2) Open Cursor and Start Agents
1. In Cursor, open this repository.
2. For each framework, open the corresponding file under `background-agents/prompts/`.
3. Start a Background Agent and paste the full prompt content.
4. Use the naming convention (e.g., `F1-Discovery`).
5. Confirm the agent uses the latest repo snapshot.

## 3) Phase Sequence (Swarm with Guardrails)
- Phase 1 (immediately): 01-discovery.md, 02-planning.md, 03-ux.md
- Phase 2 (after first drafts): 04-architecture.md, 06-implementation-fe.md, 06-implementation-be.md, 05-data-ml.md (optional)
- Phase 3: 07-qa.md, 08-security.md, 09-release.md, 10-observability.md

## 4) Integration & Merging
- Agents open PRs targeting integration.
- Use nightly merge trains; resolve conflicts via automated tests and contract suites.

## 5) Monitoring
- Review agent status updates in their threads.
- Ensure CI is green on integration.
- Promote builds to staging once QA and Security gates pass.

## 6) Handoffs
- Validate quality gates per framework before handoff.
- Keep ADRs, API contracts, design tokens, and runbooks versioned.

