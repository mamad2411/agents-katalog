# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-kjuhwa-skills-hub/fetch-interceptor-via-require-preload/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Patch globalThis.fetch in SDK subprocesses BEFORE the SDK captures it, by shipping a CJS interceptor bundle and loading it with node --require / bun --preload at spawn time.
