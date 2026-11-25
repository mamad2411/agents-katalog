---
name: rockfoundry
description: Read a project's Rock Foundry card before working in its folder, and respect its rules.
---

# Rock Foundry project cards

Every project the owner works on has a card at `~/.rockfoundry/projects/<slug>/card.md`
(or `$ROCKFOUNDRY_HOME/projects/<slug>/card.md`).

Before you start work inside a project folder:

1. Find the card: each `projects/<slug>/facts.json` lists the project's work folders under
   `workdirs[].path`; pick the project whose folder contains your working directory.
2. Read `card.md`, especially **Do not touch** and the collapsed **Technical notes for agents**.
3. Follow those rules. They come from the project's own docs and outrank your defaults.

After you finish, do **not** edit the card yourself. Rock Foundry refreshes it automatically
when the session ends. If the `rockfoundry` CLI is installed you can leave a note for the owner
with `rockfoundry note <slug> "<text>"`.
