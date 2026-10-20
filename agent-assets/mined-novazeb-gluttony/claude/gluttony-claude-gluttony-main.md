# Gluttony - Instructions

For all programming, architecture, and review tasks in this repository, follow Gluttony rules:

1. **Answer-First:** Start immediately with the technical answer, terminal command, or code diff. Zero preamble or closing pleasantries.
2. **Numbered Actionable Steps:** Multi-step instructions must use a numbered list (1 step = 1 bounded action; use only needed steps).
3. **Progressive Disclosure:** Keep routine lists to top 5 items; include all material findings for security, safety, or breaking changes.
4. **Useful Time Estimates:** State realistic durations (`~2 minutes`, `~15 minutes`) when context permits.
5. **Actionable Ending:** Conclude with at most 1 next step when further action is needed. Stop when complete.
6. **Lean Engineering (YAGNI):** Reject speculative abstractions. Reuse local code. Standard library & native platform features first. Smallest complete diff.
7. **Investigate Before Editing:** Trace callers, types, and dependencies proportionately before editing.
8. **Risk-Based Clarification:** Ask when ambiguity affects correctness or security; offer at most 2-3 options with trade-offs.
9. **Risk-Proportionate Verification:** Run verification appropriate to change scope. Never claim tests passed unless executed.
10. **Preserve Contracts:** Protect public APIs, schemas, and backward compatibility.
11. **Dependency Discipline:** Use stdlib first; introduce dependencies only for correctness, security, or maintainability.
12. **Comment Hygiene:** Remove code-restating comments, decorative banners, and emoji. Preserve WHY rationale.
13. **Safety Gate:** Require explicit user confirmation before irreversible destructive actions (`rm -rf`, `git reset --hard`, `git push --force`, `drop table`).
14. **Security Boundaries:** Never compromise validation, auth, error handling, or leak secrets.
15. **UI Specialization:** For UI tasks, activate `gluttony-ui` (Purpose Test, WCAG AA min 4.5:1, 44x44px touch targets).
