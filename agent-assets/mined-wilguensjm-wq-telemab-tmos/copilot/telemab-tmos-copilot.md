# TMOS Copilot Session Rule

Before every coding session in this repository, review:
- docs/TMOS_ENGINEERING_STANDARDS.md

Mandatory behavior:
1. Follow backend-only gateway architecture.
2. Prevent frontend direct provider communication.
3. Reuse shared provider interface and event/audit schemas.
4. Identify duplication/conflicts before coding.
5. Explain design changes before major refactors.
6. Keep changes minimal, testable, and maintainable.

Do not begin implementation until the task includes a brief architecture-fit explanation and implementation plan.
