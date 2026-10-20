---
description: Fecha o sprint atual — verificação final, auditoria de design, atualiza backlog/docs e sugere preview de deploy.
---

Act as the **Scrum Master** (`.claude/agents/scrum-master.md`), closing out the current sprint described in `docs/SPRINT.md`.

1. Dispatch `tester` for a final verification pass:
   - Frontend: `npm run lint` + `npm run build` (in `frontend/`).
   - Backend: `pytest` or healthcheck (in `backend/`), if the backend was touched this sprint.

2. Run the `ui-ux-review` skill against the changed pages/components (skip if no frontend changes this sprint). If there are **blocker** findings, dispatch `frontend-dev` to address them, then re-run the review once.

3. Update `docs/product-backlog.md`: mark all completed stories with ✅ and update their status. Move any "Blocked"/incomplete stories back to ⬜ with a one-line note on why they weren't finished.

4. Run the `update-readme` skill.

5. Append a short **Retrospectiva** to `docs/SPRINT.md` under this sprint:
   ```markdown
   ## Retrospectiva
   - **Entregue:** <lista do que foi concluído>
   - **Adiado:** <o que não entrou e por quê>
   - **Para o próximo sprint:** <ajuste de processo ou dívida técnica a endereçar>
   ```

6. Summarize the sprint outcome for the user.

7. Publique o trabalho **sem pedir confirmação**:
   - Faça `git push` da branch de feature e abra o **Pull Request** para `main` via `gh pr create`,
     com descrição do que mudou e por quê. Informe a URL do PR ao usuário.
   - **Não faça o merge.** O `CLAUDE.md` deste repo define GitHub Flow com "merge para `main`
     após revisão", e o push para `main` dispara auto-deploy em produção na Vercel — essa
     é a única etapa que continua sendo do mantenedor. Diga isso em uma linha, sem perguntar.
