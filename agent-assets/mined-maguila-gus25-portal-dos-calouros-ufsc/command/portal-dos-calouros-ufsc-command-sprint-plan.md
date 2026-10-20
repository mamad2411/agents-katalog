---
description: Planeja o próximo sprint — faz grooming do backlog e produz um plano de sprint em docs/SPRINT.md para aprovação do usuário.
---

Act as the **Scrum Master** (`.claude/agents/scrum-master.md`), running sprint planning for this project.

1. Read `docs/product-backlog.md` and `docs/SPRINT.md`.
   - If `docs/SPRINT.md` has an active (not-yet-reviewed) sprint, stop and tell the user to run `/sprint-review` first.
   - Otherwise, archive the previous sprint's content into a "Sprints Anteriores" section at the bottom of `docs/SPRINT.md` (keep it brief — sprint number, goal, outcome).

2. Dispatch the `product-owner` subagent (via Task) to groom `docs/product-backlog.md`: re-prioritize given the current project state (`git log --oneline -10` for recent activity), and confirm which items are genuinely sprint-ready (no unresolved dependencies).

3. Select stories for this sprint, in dependency order (e.g. B-29 slug map before B-30 FastAPI skeleton; architecture decisions before implementation). Keep the sprint small enough to realistically execute in one `/sprint-run`.

4. Write the new sprint to `docs/SPRINT.md`:
   ```markdown
   # Sprint <N>

   ## Objetivo
   <uma ou duas frases>

   ## Histórias
   | História | ID | Agente | Status |
   |----------|----|--------|--------|
   | <história do backlog> | B-XX | <nome do subagente> | Not Started |

   ## Definition of Done
   - [ ] npm run lint passa (frontend)
   - [ ] npm run build passa (frontend)
   - [ ] pytest passa (backend, quando existir)
   - [ ] ui-ux-review sem findings bloqueadores
   - [ ] docs/product-backlog.md atualizado com novos status
   - [ ] README atualizado se houve mudança estrutural
   ```

5. Present the plan to the user. Do not start implementation in this command.

   > Quando `/sprint-plan` é chamado **sozinho**, pare aqui — o usuário decide quando rodar `/sprint-run`. Quando é chamado **de dentro de `/sprint-cycle`**, não pare e não peça aprovação: siga direto para a execução.
