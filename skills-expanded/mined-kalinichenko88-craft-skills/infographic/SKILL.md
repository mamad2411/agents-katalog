---
name: infographic
description: Use when drawing or updating the scenario pictures in docs/ that a skill's README links, or when a change makes one of them false.
argument-hint: "[docs/<skill>]"
---

# Scenario infographics

The pictures in `docs/<skill>/` show a skill to a developer who has never
heard of it. Codex draws them with its built-in `image_gen` tool, from the brief
next to them: `docs/<skill>/brief.md`. The brief is the source of the pictures.
To change a picture, change its brief and draw it again.

## The test

Someone shows one picture. In ten seconds the reader must know what the skill
is for, when it starts, and what they get. Start from the scenarios that the
user sees, not from how the skill works inside. The first set for
`docs/github/` failed this test: it drew the scripts, the subagent and the
flags as a flowchart, with many arrows and small labels.

## The set

- `00-overview.png`: landscape, three columns — START, DURING THE WORK,
  FINISH — with one scene and one caption each.
- `01-<scenario>.png`, `02-…`: portrait, one per scenario. A trigger box
  ("WHEN: …"), four numbered scenes, and a result box ("YOU GET: …").

The words:

- Plain English, short sentences, one meaning each. A scene title is a
  question or a short statement; a caption is one or two sentences.
- What the user meets, not the mechanism: an issue number, a branch name, a
  commit subject. No command flags, script names, file paths or tool names.
- The same example numbers in every picture of a set. In `docs/github/`: #91
  the task, #15 an issue it closes too, #12 an open issue on the same code,
  #97 a new issue.
- Each picture has four scenes. A new step that the user sees replaces the
  weakest scene; it does not become a fifth.

The look is the `<style>` block of `docs/github/brief.md`. A new set copies
that brief and changes only the footer's skill name and the `<image>` blocks.

## Draw

1. Change `docs/<skill>/brief.md`: the strings to draw are the quoted ones.
2. Make a scratch directory, `$dir`. Copy the brief there, and delete each
   `<image>` block whose picture does not change: Codex draws every block it
   gets. Convert the set's current pictures to PNG there, as the style
   reference; a new set takes the pictures of `docs/github/`:

   ```bash
   for f in docs/github/*.webp; do dwebp -quiet "$f" -o "$dir/ref-$(basename "$f" .webp).png"; done
   ```

3. Run Codex in the background. It reads the brief from stdin (`-`):

   ```bash
   bash skills/review-loop/scripts/time-limit.sh 1800 codex exec -s workspace-write -C "$dir" \
     --skip-git-repo-check -o "$dir/last.md" - -i "$dir"/ref-*.png <"$dir/brief.md" >"$dir/codex.log" 2>&1
   ```

4. Check each new PNG yourself, against the brief, letter by letter. The tool
   adds text that is not in the brief (ticket numbers such as "#42") and drops
   short labels (a box's "main"). For each fault, ask Codex for one targeted
   edit with that image as the reference; at most two retries per picture.
5. Convert: `cwebp -quiet -q 85 "$dir/01-start.png" -o docs/github/01-start.webp`.
   A picture is about 0.2 MB as WebP and 1.9 MB as PNG, and the plugin installs
   as a copy of the whole repository. Keep the file names, so that the links in
   `skills/<skill>/README.md` and the root README still work.
6. Commit the brief and the pictures together. When a title changed, update
   the alt text in `skills/<skill>/README.md`, and for the overview also in the
   root README.

## When a picture is out of date

A change to a skill can make a caption false, or add a step the user sees that
no picture shows. *Docs move with the change* in the base prompt covers the
pictures too: read their text in the brief, which is the same text, against
the new behaviour. A false caption is a docs fix of the same change. A new
step goes in only when it passes the ten-second test.
