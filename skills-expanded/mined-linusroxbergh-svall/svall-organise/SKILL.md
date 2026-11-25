---
name: svall-organise
description: Tidy the fleet by naming, noting, linking and regrouping every robot in one pass.
---

# Organise the fleet

Never move the home island or the robots on it. Do not write names, notes,
links or descriptions yourself; the scribe does. Give each `svall scribe sweep`
a 10-minute timeout.

1. `svall scribe sweep` writes names, notes and links for every robot. If
   it says the scribe is off, report that line as it is and stop. Do not move
   anything or run it again.

2. `svall status` lists every id, name, island, state, cwd and note.

3. Move a robot only when its island clearly does not describe what it is
   doing; when in doubt, leave it. Group by task or topic, not by repo, unless
   the shared work is the repo itself: two agents in one repo on unrelated work
   belong on different islands.

4. For a group with no island yet, first check the list from step 2: a name
   that differs only in case is that island, and creating a colliding one is
   refused. Then:

       svall island create review
       svall robot move bob --island review

   Name the island after the task, short and lower case.

5. Run `svall island delete <name>` only on an island that is empty and yours.

6. `svall scribe sweep --islands` writes a description and links for every
   island.

Say what you changed: the output of both sweeps as it is, then one line per
move or island.
