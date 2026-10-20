# Major AI Skills (Gemini CLI)

Installable agent skill library: CAD, video, 3D, design, desktop utilities, devops, token efficiency, and common-sense prompting.

## How to use

- Skills live under `skills/<id>/SKILL.md` and load when relevant.
- Prefer a small set for a task (do not load the entire catalog into one session).
- Install selectively with:

```bash
npx major-ai-skills --gemini --skills blender,figma,ffmpeg
# or
gemini extensions install https://github.com/alivirgo/Major-AI-Skills
```

## Catalog

- Index: `skills_index.json`
- Human catalog: `CATALOG.md`
- Site: https://alivirgo.github.io/Major-AI-Skills/
- Medium FAQ: https://medium.com/@alithetechguy/what-are-ai-agent-skills-claude-code-cursor-skill-md-explained-plus-392-skill-library-to-instal-a4218fa6f0b5
- Agents index: https://alivirgo.github.io/Major-AI-Skills/llms.txt
