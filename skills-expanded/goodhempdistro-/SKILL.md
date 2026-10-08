# Cursor Agent Project Rules (AUTOPUSH)

You are operating in FULLY AUTONOMOUS DEV MODE.

After EVERY task you perform that changes the repository (code, migrations, configs, docs), you MUST:

1) Ensure the code compiles:
- If package.json exists, run: npm run build
- If build is too slow or missing, run: npm run typecheck (if available)

2) Stage, commit, and push automatically using the provided script:
- Run: powershell -ExecutionPolicy Bypass -File scripts/ai_autopush.ps1

Rules:
- Never ask the user to run git commands.
- Never leave changes uncommitted.
- If there are no changes, still push (safe no-op).
- Commit message must be short, scoped to the change, and start with: fix: or chore: or feat:
- Do not run destructive commands.
