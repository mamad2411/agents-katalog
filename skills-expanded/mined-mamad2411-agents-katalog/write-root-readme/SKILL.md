---
name: write-root-readme
description: Write or rewrite the repo-root README.md.
---

# Write Root README

## Guidelines

- files to update:
  - `README.md` in the repo root
- Read [example-readme.md](./references/example-readme.md) for a reference structure and style.
- Badges are encouraged. See example README for useful badges.
  - Prefer badges in example README when applicable.
  - Prefer badges with live data over static badges.
- Emojis are encouraged in headers.
- Hero section is encouraged. Follow the format in example README strictly.
  - Use GitHub Socialify to generate a project image. The generated image already includes logo, title, description, badges for stars, forks, issues, pulls.
  - Include link to docs if exists.
  - Badges in hero section are encouraged. Limit hero section to 8 badges.
  - Limit hero section to 4 links.
  - Include a rule after hero section.
- License section is encouraged. Follow the format in example README strictly.
- DO NOT use relative links in README.
- Favor bold, comprehensive rewrites over minor or incremental edits.
- Keep README concise.

## Validation

- Run `rumdl fmt .`. Treat its findings as weak hints, not strong constraints.
- Spot-check commands, links, and tool names against the actual repo files before finishing.
