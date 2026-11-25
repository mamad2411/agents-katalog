# UTH Governance Pack

If `.superpower/` exists, first read `.superpower/using-superpowers/SKILL.md` as the local-only Superpower workflow entry for maintaining this pack.

This repository is a distributable UTH engineering-governance pack, not a target project.

Keep this entry short. Full rules live in:

- `README.md`
- `docs/guide/installation.md`
- `docs/AGENT_工程治理启动手册.md`
- `docs/TEMPLATES_工程治理模板.md`
- `docs/HOOKS_工程治理门禁手册.md`
- `docs/FLOW_全链路流程图.md`
- `skills/`
- `tools/uth-hooks/`
- `scripts/install.py`

Versioning belongs to the outer package folder or release artifact. Do not add
version suffixes to internal handbook/template filenames.

## When Applying This Pack

Follow `docs/guide/installation.md` and prefer `scripts/install.py`.
Installation is global and does not initialize the current project. Project
onboarding is a separate explicit action handled by `uth-onboarding`.

1. **Skills**
   - Copy or install `skills/uth-*` and `skills/uth-sp-*` into the skill directory loaded by the target runtime.
   - If the runtime location is unknown, ask the user where that agent loads skills from.

2. **Tools**
   - Do not install hook tools globally.
   - `uth-onboarding` copies bundled hook tools into the target project as `tools/uth-hooks/`.
   - The project-local hook runner is `tools/uth-hooks/uth-hook.py`.

3. **Project Governance Docs**
   - Do not create project docs during installation.
   - Create project docs only when the user explicitly runs `uth-onboarding` or explicitly asks to enable UTH in that target project.
   - `uth-onboarding` creates `.uth-governance/project.json`; without that marker, other `uth-*` scenes should stay silent unless the user explicitly asks to enable UTH.

Do not copy this pack's old task packages, archives, `current-state`, or context docs as target-project facts.

## Hook Usage

The packaged hook runner accepts JSON events and returns `PASS`, `WARN`, `ASK`, or `BLOCK`.

```bash
python tools/uth-hooks/uth-hook.py --event event.json --config tools/uth-hooks/config.example.json
```

For stdin:

```bash
echo '{"type":"git-write","active_scene":"uth-git","commands":["git commit -m test"],"git_plan_present":true,"user_git_confirmed":true}' | python tools/uth-hooks/uth-hook.py --event -
```

L0/L1/L2/L3 are implemented in the reference runner:

- L1: ambiguity, scene transitions, worker Prompt dispatch, UTH-SP trigger decision.
- L2: file write scope, Git write confirmation, UTF-8 doc guard, script guard.
- L3: scene closeout evidence gates. L3 checks supplied evidence and documented
  exceptions; it does not rerun expensive compile/test commands.

## Editing This Pack

- Use `skill-creator` when editing any `skills/**` files.
- Use explicit UTH-SP maintenance intent when editing `skills/uth-sp-*/**`.
- Run UTF-8/no-BOM checks after changing governance Markdown or scripts.
- Do not run Git writes unless the user explicitly asks for Git closure.
