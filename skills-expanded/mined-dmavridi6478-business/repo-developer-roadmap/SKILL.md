---
name: repo-developer-roadmap
description: How to use roadmap.sh and its source repo (kamranahmedse/developer-roadmap) to give a user a structured learning path for a tech role or topic (Claude Code, AI Engineer, DevOps, Python, Data Analyst, Product Manager and 70+ more). Use when someone asks "what should I learn" for a developer, data or product role.
---

# developer-roadmap (`kamranahmedse/developer-roadmap`, roadmap.sh)

Cloned shallow at `/home/user/kamranahmedse/developer-roadmap` (re-clone `git clone --depth 1 https://github.com/kamranahmedse/developer-roadmap`). The roadmap definitions are content under `roadmaps/<slug>/` (one folder per roadmap, with markdown topic content); the repo is also a pnpm workspace (`package.json`, `pnpm-workspace.yaml`). Check `license` before reusing content. The note saved only `roadmap.sh`.

## Roadmaps relevant to this workspace (all present in the README)
Claude Code, AI Engineer, AI Agents, AI Product Builder, AI Data Scientist, AI Red Teaming, Vibe Coding, Forward Deployed Engineer, Data Analyst, BI Analyst, Power BI, MLOps, Product Manager, Engineering Manager, Python, Django, Git/GitHub, API Design, DevOps, DevSecOps, Cyber Security, Software Architect, QA, Docker, Kubernetes. Run `ls roadmaps/` for the full set; do not assume a roadmap exists without checking.

## Procedure to build a learning plan
1. Ask: current level, target role, hours per week, deadline.
2. Read `roadmaps/<slug>/` (or `https://roadmap.sh/<slug>`) and list nodes grouped into stages.
3. Mark what the learner already knows, cut optional branches, and order the rest.
4. Produce a dated plan with one project per stage; link to matching skills here (`30-days-of-python`, `90-days-cybersecurity`, `learning-roadmap`, `ai-skills-roadmap-2026`).
5. Re-check topics against current docs; roadmaps lag fast-moving areas.

## Related
`free-utility-learning-resources`, `learning-roadmap`, `roadmapcareer`.
